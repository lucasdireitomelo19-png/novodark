"""Narração com ElevenLabs, um áudio por bloco do roteiro, com tempos palavra a palavra.

Uso: python3 narrar_eleven.py <pasta_do_video> [velocidade]
A pasta precisa ter blocos.json: [{"id", "texto", "pausa" (s depois do bloco), "radio" (opcional)}].
Precisa de ELEVENLABS_API_KEY no ambiente (arquivo .env na raiz, nunca no código).
Gera narracao/<id>.mp3 (cache: só pede de novo o bloco cujo texto ou ajuste mudou),
narracao.mp3, narracao_final.wav e palavras.json no formato do motor ({t, d, w}).
"""
import base64, hashlib, json, os, re, subprocess, sys, urllib.request
import numpy as np

VOZ = os.environ.get("ELEVEN_VOZ", "nPczCjzI2devNBz1zQrb")  # Brian: grave, documental
MODELO = os.environ.get("ELEVEN_MODELO", "eleven_multilingual_v2")
SR = 48000

pasta = os.path.abspath(sys.argv[1])
vel = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
blocos = json.load(open(os.path.join(pasta, "blocos.json"), encoding="utf-8"))
dn = os.path.join(pasta, "narracao"); os.makedirs(dn, exist_ok=True)


def tts(i, b):
    ajustes = {"stability": 0.42, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": vel}
    corpo = {"text": b["texto"], "model_id": MODELO, "voice_settings": ajustes,
             "previous_text": blocos[i - 1]["texto"] if i else None,
             "next_text": blocos[i + 1]["texto"] if i + 1 < len(blocos) else None}
    chave = hashlib.sha1(json.dumps([VOZ, corpo], sort_keys=True).encode()).hexdigest()
    mp3, js = os.path.join(dn, b["id"] + ".mp3"), os.path.join(dn, b["id"] + ".json")
    if os.path.exists(js) and json.load(open(js)).get("chave") == chave:
        return mp3, json.load(open(js))["alinhamento"]
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(corpo).encode(), method="POST",
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=180))
    open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
    json.dump({"chave": chave, "alinhamento": r["alignment"]}, open(js, "w"), ensure_ascii=False)
    print("gerado", b["id"], flush=True)
    return mp3, r["alignment"]


def ler(arq, filtro=None):
    cmd = ["ffmpeg", "-v", "error", "-i", arq] + (["-af", filtro] if filtro else []) + ["-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)


# rádio de cabine: banda estreita, saturação leve e chiado
RADIO = "highpass=f=350,lowpass=f=3200,acrusher=bits=10:mix=0.25,volume=1.6"
partes, palavras, t = [], [], 0.0
for i, b in enumerate(blocos):
    mp3, al = tts(i, b)
    x = ler(mp3, RADIO if b.get("radio") else None)
    if b.get("radio"):
        x = x + np.random.default_rng(1).normal(0, 0.012, len(x)).astype(np.float32)
    # palavras a partir do alinhamento por caractere
    ch, ini, fim = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    atual, t0, t1 = "", None, None
    for c, a, z in list(zip(ch, ini, fim)) + [(" ", 0, 0)]:
        if c.isspace():
            w = re.sub(r"^[^\w]+|[^\w?]+$", "", atual)
            if w: palavras.append(dict({"t": round(t + t0, 3), "d": round(t1 - t0, 3), "w": w}, **({"fim": 1} if re.search(r"[.?!:,]\W*$", atual) else {})))
            atual, t0 = "", None
        else:
            atual += c; t0 = a if t0 is None else t0; t1 = z
    partes += [x, np.zeros(int(b.get("pausa", 0) * SR), np.float32)]
    t += (len(x) + int(b.get("pausa", 0) * SR)) / SR

# trocas.json (opcional): [["mil novecentos e oitenta e seis", "1986"], ...] junta palavras faladas
# por extenso numa só palavra escrita, para a legenda e as âncoras ficarem com números
tj = os.path.join(pasta, "trocas.json")
for falado, escrito in (json.load(open(tj, encoding="utf-8")) if os.path.exists(tj) else []):
    alvo, k = falado.lower().split(), 0
    while k + len(alvo) <= len(palavras):
        if [p["w"].lower() for p in palavras[k:k + len(alvo)]] == alvo:
            fim_ = palavras[k + len(alvo) - 1]
            palavras[k:k + len(alvo)] = [dict({"t": palavras[k]["t"], "d": round(fim_["t"] + fim_["d"] - palavras[k]["t"], 3), "w": escrito}, **({"fim": 1} if fim_.get("fim") else {}))]
        k += 1

voz = np.concatenate(partes)
wav = os.path.join(pasta, "narracao_final.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", str(SR), wav], input=voz.tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "libmp3lame", "-b:a", "192k", os.path.join(pasta, "narracao.mp3")], check=True)
json.dump(palavras, open(os.path.join(pasta, "palavras.json"), "w"), ensure_ascii=False)
print(f"narração: {len(voz) / SR:.2f}s | {len(palavras)} palavras | velocidade {vel}")
