"""Narração com a voz pt-BR-AntonioNeural (edge-tts, grátis), gerada frase a frase para soar mais natural.

Uso: python3 narrar_antonio.py <pasta_do_video> [velocidade_base, ex. +10] [tom, ex. -2]
Lê o mesmo blocos.json da narração ElevenLabs: [{"id", "texto", "pausa", "radio"?, "vel"?, "tom"?}].
  vel / tom (opcionais, por bloco): somam à velocidade (%) e ao tom (Hz) base. Ex.: gancho mais lento, perseguição mais rápida.

O que faz a voz ficar mais fluida que o roteiro inteiro de uma vez:
  - cada frase é gerada sozinha, com o silêncio das pontas cortado pelos tempos das palavras;
  - as pausas são desenhadas: vírgula curta, ponto médio, interrogação e reticências longas, e a pausa do bloco no fim;
  - velocidade e tom variam por bloco (o motor de voz não varia sozinho);
  - fade de 15 ms em cada frase, sem cliques na emenda.
Gera narracao/a_<n>.mp3 (cache por frase), narracao.mp3, narracao_final.wav e palavras.json ({t, d, w, fim?}).
"""
import asyncio, hashlib, json, os, re, subprocess, sys
import edge_tts
import numpy as np

VOZ = "pt-BR-AntonioNeural"
SR = 48000
PAUSAS = {",": 0.12, ";": 0.18, ":": 0.2, ".": 0.3, "!": 0.32, "?": 0.38, "…": 0.5}

pasta = os.path.abspath(sys.argv[1])
vel_base = int(sys.argv[2]) if len(sys.argv) > 2 else 10
tom_base = int(sys.argv[3]) if len(sys.argv) > 3 else -2
blocos = json.load(open(os.path.join(pasta, "blocos.json"), encoding="utf-8"))
dn = os.path.join(pasta, "narracao"); os.makedirs(dn, exist_ok=True)


async def tts(texto, rate, pitch, mp3):
    c = edge_tts.Communicate(texto, VOZ, rate=rate, pitch=pitch, boundary="WordBoundary", proxy=os.environ.get("HTTPS_PROXY"))
    words = []
    with open(mp3, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary": words.append({"t": ch["offset"] / 1e7, "d": ch["duration"] / 1e7, "w": ch["text"]})
    return words


def frase(texto, vel, tom):
    rate, pitch = f"{vel:+d}%", f"{tom:+d}Hz"
    chave = hashlib.sha1(json.dumps([VOZ, texto, rate, pitch]).encode()).hexdigest()[:16]
    mp3, js = os.path.join(dn, f"a_{chave}.mp3"), os.path.join(dn, f"a_{chave}.json")
    if not os.path.exists(js):
        for tentativa in range(4):  # a conexão com o serviço de voz às vezes cai; tenta de novo
            try:
                words = asyncio.run(tts(texto, rate, pitch, mp3)); break
            except Exception as e:
                if tentativa == 3: raise
                print("tentando de novo:", type(e).__name__, flush=True)
        json.dump(words, open(js, "w"), ensure_ascii=False)
    return mp3, json.load(open(js))


def ler(arq, filtro=None):
    cmd = ["ffmpeg", "-v", "error", "-i", arq] + (["-af", filtro] if filtro else []) + ["-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()


RADIO = "highpass=f=350,lowpass=f=3200,acrusher=bits=10:mix=0.25,volume=1.6"
partes, palavras, t = [], [], 0.0
for b in blocos:
    # "..." vira reticências (pausa longa); frases terminam em . ! ? … ou :
    texto = b["texto"].replace("...", "…")
    frases = [f.strip() for f in re.findall(r'[^.!?…:]+[.!?…:]*["”]?', texto) if f.strip()]
    for i, fr in enumerate(frases):
        mp3, words = frase(fr, vel_base + b.get("vel", 0), tom_base + b.get("tom", 0))
        x = ler(mp3, RADIO if b.get("radio") else None)
        if b.get("radio"):
            x = x + np.random.default_rng(1).normal(0, 0.012, len(x)).astype(np.float32)
        # corta o silêncio das pontas pelos tempos das palavras
        a = max(0, int((words[0]["t"] - 0.04) * SR)); z = min(len(x), int((words[-1]["t"] + words[-1]["d"] + 0.12) * SR))
        x = x[a:z]; f = int(0.015 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
        # palavras: alinha cada palavra falada com o texto para saber onde há pontuação
        cur = 0
        for k, w in enumerate(words):
            m = re.search(re.escape(w["w"]), fr[cur:]); fim = k == len(words) - 1
            if m:
                cur += m.end(); fim = fim or bool(re.match(r'["”]?[,.;:!?…]', fr[cur:]))
            palavras.append(dict({"t": round(t + w["t"] - a / SR, 3), "d": round(w["d"], 3), "w": w["w"]}, **({"fim": 1} if fim else {})))
        final = re.search(r"([,.;:!?…])[\"”]?\s*$", fr)
        pausa = PAUSAS.get(final.group(1), 0.25) if final else 0.2
        if i == len(frases) - 1:
            pausa = max(pausa, b.get("pausa", 0))
        partes += [x, np.zeros(int(pausa * SR), np.float32)]
        t += (len(x) + int(pausa * SR)) / SR

# trocas.json (opcional): junta palavras faladas por extenso numa só palavra escrita (legenda e âncoras com números)
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
print(f"narração: {len(voz) / SR:.2f}s | {len(palavras)} palavras | velocidade base {vel_base:+d}% | tom {tom_base:+d}Hz")
