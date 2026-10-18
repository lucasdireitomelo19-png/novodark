"""Motor de montagem de vídeos longos na horizontal (1920x1080, só voz).

Uso: python3 motor_h.py <pasta_do_video>
A pasta precisa ter: narracao.mp3, palavras.json e cenas.py com:
  FIM (duração total), SAIDA, FINAL (texto final opcional),
  CENAS = [("trecho da narração onde a cena começa", {opções}), ...]
Opções iguais às do motor vertical, mais:
  src="anim:<cena>" + p={...}  -> animação gerada por anim/anim.html
  credito="..."                -> crédito no canto (padrão deduzido da fonte)
"""
import importlib.util, json, os, re, subprocess, sys, unicodedata

W, H, FPS = 1920, 1080, 30
BASE = os.path.dirname(os.path.abspath(__file__))
SRC, FONTS, ANIM = os.path.join(BASE, "src"), os.path.join(BASE, "fonts"), os.path.join(BASE, "anim")

pasta = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.dirname(pasta))  # permite "from comum_shorts import *"
spec = importlib.util.spec_from_file_location("cenas", os.path.join(pasta, "cenas.py"))
cfg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cfg)
FIM = cfg.FIM
VERT = getattr(cfg, "VERTICAL", False)
if VERT:
    W, H = 1080, 1920
TMP = os.path.join(pasta, "tmp"); os.makedirs(TMP, exist_ok=True)

def run(cmd):
    subprocess.run(cmd, check=True)

# ---------------- âncoras -> tempos ----------------
palavras = json.load(open(os.path.join(pasta, "palavras.json")))
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", s)
tokens, inicio_char = [], []
texto_norm = ""
for p in palavras:
    for parte in norm(p["w"]).split():
        inicio_char.append((len(texto_norm), p["t"]))
        texto_norm += parte + " "
def tempo_da_ancora(ancora, desde):
    alvo = " ".join(norm(ancora).split()) + " "
    pos = texto_norm.find(alvo, desde)
    if pos < 0:
        raise SystemExit(f"Âncora não encontrada: {ancora!r}")
    t = next(t for c, t in reversed(inicio_char) if c <= pos)
    return t, pos + 1

CENAS, cursor = [], 0
for i, (ancora, opc) in enumerate(cfg.CENAS):
    t, cursor = (0.0, cursor) if i == 0 else tempo_da_ancora(ancora, cursor)
    CENAS.append(dict(opc, t=round(max(0.0, t - 0.15), 3)))

# guarda as cenas originais (uma animação e um conjunto de efeitos sonoros por cena)
for k, c in enumerate(CENAS):
    c["_cena"] = k
ORIG = [dict(c) for c in CENAS]
def fim_orig(k):
    return ORIG[k + 1]["t"] if k + 1 < len(ORIG) else FIM

# retenção: nenhum plano passa de RITMO segundos. Planos longos viram cortes de câmera
# (outro enquadramento da mesma imagem ou animação, continuando de onde parou)
CARTOES = ("capitulo", "citacao", "data", "teoria", "perguntas", "final")
RITMO = getattr(cfg, "RITMO", 2.8 if VERT else 3.5)
QUADROS = [((1.0, 1.06), (0.5, 0.5)), ((1.22, 1.16), (0.35, 0.45)), ((1.12, 1.2), (0.65, 0.55)), ((1.3, 1.24), (0.5, 0.4))]
final = []
for i, c in enumerate(CENAS):
    fim = CENAS[i + 1]["t"] if i + 1 < len(CENAS) else FIM
    dur = fim - c["t"]
    anim = c["src"].startswith("anim:")
    cartao = anim and c["src"][5:] in CARTOES
    limite = RITMO * (1.8 if cartao else 1.0)
    if dur > limite and not c.get("inteiro"):
        n = int(dur // limite) + 1
        for k in range(n):
            d = dict(c, t=round(c["t"] + dur * k / n, 3), _sub=k)
            fontes = [c["src"]] + list(c.get("alt", []))
            if len(fontes) > 1 and fontes[k % len(fontes)] != c["src"]:
                d["src"] = fontes[k % len(fontes)]  # corte para outra imagem/animação dentro da mesma cena
                d.pop("ss", None); d.pop("crop", None)
                if not d["src"].startswith("anim:"):
                    d["tag"] = "banco"
            if k:
                d.pop("texto", None); d.pop("flash", None); d.pop("punch", None); d.pop("capitulo", None)
                if not c["src"].lower().endswith((".jpg", ".png")):
                    d["ss"] = c.get("ss", 0) + dur * k / n * c.get("vel", 1.0)
                if cartao:
                    d["zoom"] = (1.08, 1.12) if k % 2 else (1.0, 1.04)
                else:
                    (z, pan) = QUADROS[k % len(QUADROS)]
                    d["zoom"], d["pan"] = z, pan
            elif anim:
                d.setdefault("zoom", (1.0, 1.04) if cartao else (1.0, 1.07))
            final.append(d)
    else:
        if anim:
            c.setdefault("zoom", (1.0, 1.04) if cartao else (1.0, 1.07))
        final.append(c)
CENAS = final

# efeitos visuais automáticos: flash e tremor nos capítulos, tremor e glitch nos cartões, glitch alternado nas trocas de cena
troca = 0
for c in CENAS:
    if os.path.basename(c["src"]).startswith("b_") and "tag" not in c:
        c["tag"] = "banco"
    if c.get("_sub"):
        continue
    nome = c["src"][5:] if c["src"].startswith("anim:") else ""
    if nome == "capitulo":
        c.setdefault("flash", 1); c.setdefault("tremor", 16)
    elif nome in ("teoria", "citacao", "perguntas"):
        c.setdefault("tremor", 10); c.setdefault("glitch", 1)
    else:
        troca += 1
        if troca % (2 if VERT else 3) == 0:
            c.setdefault("glitch", 1)

def dur_de(i):
    return (CENAS[i + 1]["t"] if i + 1 < len(CENAS) else FIM) - CENAS[i]["t"]

if os.environ.get("CHECK"):
    for i, c in enumerate(CENAS):
        print(f"{i:03d} {c['t']:7.2f} {dur_de(i):5.2f}s  {c['src']}")
    print("planos:", len(CENAS), "| média:", round(FIM / len(CENAS), 2), "s")
    sys.exit()

# ---------------- animações ----------------
jobs = []
for k, c in enumerate(ORIG):
    if c["src"].startswith("anim:"):
        saida = os.path.join(TMP, f"anim_{k:03d}.mp4")
        jobs.append(dict(saida=saida, cena=c["src"][5:], dur=round(fim_orig(k) - c["t"] + 0.3, 3), p=c.get("p", {}), w=W, h=H))
for c in CENAS:
    if c["src"].startswith("anim:") and c["src"] != ORIG[c["_cena"]]["src"]:
        raise SystemExit(f"alt só aceita imagens/vídeos do banco (cena {c['_cena']}): {c['src']}")
    if c["src"].startswith("anim:"):
        c["_arq"] = os.path.join(TMP, f"anim_{c['_cena']:03d}.mp4")
        c.setdefault("ss", round(c["t"] - ORIG[c["_cena"]]["t"], 3))
if jobs:
    jp = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jp, "w"))
    env = dict(os.environ, NODE_PATH=subprocess.check_output(["npm", "root", "-g"], text=True).strip())
    # várias instâncias do navegador em paralelo (cada uma pega uma fatia dos jobs)
    N = int(os.environ.get("WORKERS", max(1, (os.cpu_count() or 2) - 1)))
    procs = [subprocess.Popen(["node", os.path.join(ANIM, "render_anim.js"), jp, str(k), str(N)], env=env) for k in range(N)]
    if any(p.wait() for p in procs):
        raise SystemExit("falha ao renderizar animações")

# ---------------- planos ----------------
partes = []
for i, c in enumerate(CENAS):
    dur, vel = dur_de(i), c.get("vel", 1.0)
    out = os.path.join(TMP, f"parte_{i:03d}.mp4")
    partes.append(out)
    chave = json.dumps({k: v for k, v in c.items() if k not in ("texto", "tag", "credito")}, sort_keys=True) + f"{dur:.3f}"
    if os.path.exists(out) and os.path.exists(out + ".key") and open(out + ".key").read() == chave:
        continue
    anim = c["src"].startswith("anim:")
    arq = c.get("_arq") or os.path.join(SRC, c["src"])
    imagem = arq.lower().endswith((".jpg", ".png"))
    banco = os.path.basename(arq).startswith("b_")
    if VERT and banco and "fit" not in c:
        c = dict(c, fit=1)
    f = []
    if vel != 1.0:
        f.append(f"setpts=PTS/{vel}")
    if c.get("crop"):
        x, y, w, h = c["crop"]; f.append(f"crop={w}:{h}:{x}:{y}")
    if c.get("fit"):
        f.append(f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                 f"boxblur=40:3,eq=brightness=-0.15[bg];[b]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                 f"[bg][fg]overlay=(W-w)/2:(H-h)/2" + (",unsharp=5:5:0.8" if banco else ""))
    else:
        f.append(f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}" + (",unsharp=5:5:0.8" if banco else ""))
    z0, z1 = c.get("zoom", (1.0, 1.0) if anim else (1.05, 1.13))
    if (z0, z1) != (1.0, 1.0) or c.get("shake") or c.get("tremor"):
        if (z0, z1) == (1.0, 1.0): z0, z1 = 1.04, 1.04
        zoom = f"{z0}+{z1 - z0}*t/{dur:.3f}"
        f.append(f"scale=w='trunc({W}*({zoom})/2)*2':h=-2:eval=frame:flags=bicubic")
        a = c.get("shake", 0); px, py = c.get("pan", (0.5, 0.5)); tr = c.get("tremor", 0)
        xs = f"(iw-ow)*{px}" + (f"+{a}*sin(47*t)+{a*0.6}*sin(29*t+1)" if a else "") + (f"+{tr}*exp(-5*t)*sin(53*t)" if tr else "")
        ys = f"(ih-oh)*{py}" + (f"+{a*0.8}*sin(41*t+2)+{a*0.5}*sin(23*t)" if a else "") + (f"+{tr*0.8}*exp(-5*t)*sin(61*t+1)" if tr else "")
        f.append(f"crop={W}:{H}:x='max(0,min(iw-ow,{xs}))':y='max(0,min(ih-oh,{ys}))'")
    if banco:
        f.append(f"setsar=1,fps={FPS},eq=contrast=1.12:brightness=-0.07:saturation={c.get('sat', 0.72)}:gamma=0.92,"
                 "colorbalance=rs=-0.05:bs=0.08:rh=0.06:bh=-0.04")
        if c.get("noite"):  # "noite americana": footage de dia vira noite (escuro, azulado, dessaturado)
            f.append("eq=brightness=-0.04:gamma=0.85:saturation=0.5,colorbalance=rs=-0.1:gs=-0.03:bs=0.18:rm=-0.06:bm=0.1,"
                     "curves=all='0/0 0.5/0.38 1/0.85'")
    else:
        f.append(f"setsar=1,fps={FPS}" + ("" if anim else f",eq=contrast=1.06:saturation={c.get('sat', 1.12)}"))
    if c.get("flash"):
        f.append("fade=t=in:st=0:d=0.15:color=white")
    if c.get("glitch"):
        f.append("rgbashift=rh=-14:bh=14:gv=6:enable='lt(t,0.16)',noise=alls=45:allf=t:enable='lt(t,0.12)'")
    if c.get("escurecer"):
        f.append(f"fade=t=out:st={max(dur - 0.6, 0):.3f}:d=0.6")
    entrada = ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur + 0.1:.3f}", "-i", arq] if imagem else \
              ["-ss", str(c.get("ss", 0)), "-t", f"{dur * vel + 0.2:.3f}", "-i", arq]
    run(["ffmpeg", "-v", "error", "-y", *entrada, "-filter_complex", ",".join(f),
         "-an", "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out])
    open(out + ".key", "w").write(chave)
    print("ok", os.path.basename(out), f"{dur:.2f}s", c["src"], flush=True)

lista = os.path.join(TMP, "lista.txt")
with open(lista, "w") as fh:
    fh.writelines(f"file '{p}'\n" for p in partes)
bruto = os.path.join(TMP, "video_bruto.mp4")
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", bruto])

# ---------------- legendas por frase, etiquetas, textos e créditos ----------------
def ts(s):
    h, s = divmod(max(s, 0), 3600); m, s = divmod(s, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"
grupos, atual = [], []
for k, p in enumerate(palavras):
    atual.append(p)
    prox = palavras[k + 1] if k + 1 < len(palavras) else None
    pausa = prox is None or prox["t"] - (p["t"] + p["d"]) > 0.25 or p.get("fim")
    longo = prox is not None and sum(len(x["w"]) + 1 for x in atual) + len(prox["w"]) > (22 if VERT else 38)
    if pausa or longo or len(atual) >= (4 if VERT else 7):
        grupos.append(atual); atual = []
if atual:
    grupos.append(atual)
ev = []
for gi, g in enumerate(grupos):
    fim_g = grupos[gi + 1][0]["t"] if gi + 1 < len(grupos) else FIM
    fim_g = min(fim_g, g[-1]["t"] + g[-1]["d"] + 0.5)
    for wi, p in enumerate(g):
        fim = g[wi + 1]["t"] if wi + 1 < len(g) else fim_g
        txt = [(r"{\c&H00C8FF&\fscx122\fscy122\t(0,90,\fscx108\fscy108)}" + q["w"] + r"{\c&HFFFFFF&\fscx100\fscy100}") if wj == wi else q["w"] for wj, q in enumerate(g)]
        ev.append(f"Dialogue: 3,{ts(p['t'])},{ts(fim)},Legenda,,0,0,0,,{' '.join(txt)}")

ROTULOS = {"real": ("Real", "● IMAGEM REAL"), "sim": ("Anim", "SIMULAÇÃO"), "anim": ("Anim", "ANIMAÇÃO"), "ilus": ("Anim", "ILUSTRAÇÃO"), "rec": ("Anim", "RECRIAÇÃO"), "banco": ("Anim", "IMAGEM ILUSTRATIVA")}
BANCO = json.load(open(os.path.join(BASE, "..", "banco_creditos.json"), encoding="utf-8")) if os.path.exists(os.path.join(BASE, "..", "banco_creditos.json")) else {}
def credito_padrao(src):
    if src.startswith("anim:"): return getattr(cfg, "CREDITO_ANIM", "Ilustração: Casos Sem Resposta")
    if src in BANCO: return BANCO[src]["credito"]
    for pref, cr in (("bh_", "NASA Goddard"), ("vgi_", "NASA/JPL-Caltech"), ("vg_", "NASA/JPL-Caltech"), ("hd_webb", "NASA/STScI"),
                     ("hdi_", "NASA"), ("hd_", "ESA/Hubble, M. Kornmesser"), ("eso_", "ESO"), ("ns_", "NASA SVS"), ("fl_hawking", "NASA/Paul Alers")):
        if src.startswith(pref): return cr
    return ""
for i, c in enumerate(CENAS):
    t0, t1 = c["t"], c["t"] + dur_de(i)
    if c.get("tag"):
        est, txt = ROTULOS[c["tag"]]; ev.append(f"Dialogue: 1,{ts(t0)},{ts(t1)},{est},,0,0,0,,{txt}")
    cr = c.get("credito", credito_padrao(c["src"]))
    if cr: ev.append(f"Dialogue: 1,{ts(t0)},{ts(t1)},Credito,,0,0,0,,{cr}")
    if c.get("texto"):
        ev.append(f"Dialogue: 2,{ts(t0 + 0.1)},{ts(t1)},Destaque,,0,0,0,," r"{\fad(150,150)}" + c["texto"])
if getattr(cfg, "FINAL", ""):
    fim_voz = palavras[-1]["t"] + palavras[-1]["d"]
    ev.append(f"Dialogue: 4,{ts(fim_voz + 0.2)},{ts(FIM)},Final,,0,0,0,," r"{\fad(400,0)}" + cfg.FINAL)
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Legenda,Montserrat Thin ExtraBold,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,2,2,160,160,70,1
Style: Destaque,Montserrat Thin ExtraBold,72,&H0040C8FF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,2,0,1,5,3,8,100,100,90,1
Style: Final,Montserrat Thin ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,3,0,1,6,4,5,100,100,0,1
Style: Real,Montserrat Thin ExtraBold,26,&H00FFFFFF,&H00FFFFFF,&H001E1EE6,&H00000000,0,0,0,0,100,100,2,0,3,8,0,7,50,50,45,1
Style: Anim,Montserrat Thin ExtraBold,22,&H00FFFFFF,&H00FFFFFF,&H70000000,&H00000000,0,0,0,0,100,100,2,0,3,7,0,7,50,50,45,1
Style: Credito,Montserrat Thin ExtraBold,20,&H50FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,1.5,0,9,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
if VERT:
    # Shorts: legenda grande no meio da tela, etiquetas e créditos maiores
    ass = ass.replace("Style: Legenda,Montserrat Thin ExtraBold,54,", "Style: Legenda,Montserrat Thin ExtraBold,76,").replace(",2,160,160,70,1\n", ",2,70,70,400,1\n", 1)
    ass = ass.replace("Style: Destaque,Montserrat Thin ExtraBold,72,", "Style: Destaque,Montserrat Thin ExtraBold,80,").replace(",8,100,100,90,1\n", ",8,60,60,260,1\n", 1)
    ass = ass.replace("Style: Final,Montserrat Thin ExtraBold,96,", "Style: Final,Montserrat Thin ExtraBold,92,")
    ass = ass.replace(",7,50,50,45,1\n", ",7,50,50,150,1\n").replace(",9,40,40,40,1\n", ",9,40,40,150,1\n")
ass_path = os.path.join(TMP, "legendas.ass"); open(ass_path, "w", encoding="utf-8").write(ass)

# ---------------- trilha e efeitos sonoros (mixados em numpy) ----------------
import numpy as np
from scipy.io import wavfile
SR = 48000
SFX = os.path.join(BASE, "sfx")
if not os.path.exists(os.path.join(SFX, "drone.wav")):  # a biblioteca de sons é gerada, não vai para o git
    run([sys.executable, os.path.join(BASE, "sfx.py")])
_cache = {}
def som(nome):
    if nome not in _cache:
        sr, x = wavfile.read(os.path.join(SFX, nome + ".wav"))
        _cache[nome] = x.astype(np.float32) / 32768.0
    return _cache[nome]
N = int(FIM * SR)
efeitos = np.zeros((N, 2), np.float32)
def tocar(nome, t, db=-10.0, dur=None):
    x = som(nome); i0 = int(max(t, 0) * SR)
    if dur is not None:  # ambiente em loop, com fade de entrada e saída
        n = int(dur * SR); reps = n // len(x) + 1; x = np.tile(x, (reps, 1))[:n].copy()
        f = min(int(0.6 * SR), n // 3)
        if f > 0: x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
    n = min(len(x), N - i0)
    if n > 0: efeitos[i0:i0 + n] += x[:n] * (10 ** (db / 20))

ultima_troca = -9
for k, c in enumerate(ORIG):
    t0, t1 = c["t"], fim_orig(k); dur = t1 - t0
    nome = c["src"][5:] if c["src"].startswith("anim:") else ""
    pp = c.get("p", {})
    # transição: whoosh em toda troca de cena
    if k and nome != "capitulo":
        tocar(["whoosh", "whoosh_curto", "whoosh_grave"][k % 3], t0 - 0.35, -15 if VERT else -17)
    if nome == "capitulo":
        tocar("riser", t0 - 3.0, -14); tocar("impacto", t0 - 0.02, -6)
    elif nome in ("teoria", "citacao", "perguntas"):
        tocar("impacto", t0, -12); tocar("glitch", t0, -20)
    elif nome == "data":
        tocar("datilografia", t0 + 0.1, -13)
    elif nome == "documento":
        tocar("datilografia", t0 + 0.3, -16)
        if pp.get("carimbo"): tocar("carimbo", t0 + pp.get("tc", dur * 0.5), -6)
    elif nome == "ficha":
        tocar("datilografia", t0 + 0.4, -17)
    elif nome == "jornal":
        tocar("estatica", t0, -18); tocar("whoosh_grave", t0 - 0.2, -12)
    elif nome == "radar":
        for tt in np.arange(t0 + 0.3, t1, 2.86): tocar("ping", tt, -15)
    elif nome == "fotos":
        for i in range(pp.get("n", 5)): tocar("obturador", t0 + i * 0.35 + 0.1, -10)
    elif nome == "eletronica":
        tocar("estatica", t0, -20)
        if pp.get("explode"): tocar("impacto", t0 + dur * 0.6, -6)
    elif nome == "praia" and "explosao" in pp:
        tocar("impacto", t0 + pp["explosao"], -5)
    elif nome in ("meteoro", "cacas"):
        tocar("whoosh_grave", t0 + 0.3, -8)
    if nome in ("mascara", "criatura") or (nome == "bilhete" and "foco" in pp):
        for tt in np.arange(t0 + 0.2, t1 - 0.3, 0.95): tocar("coracao", tt, -9)
    if pp.get("chuva") or nome in ("rua", "criatura") or (nome == "estrada" and pp.get("chuva")):
        tocar("chuva", t0, -22, dur)
    if pp.get("fogueira") or (nome in ("museu", "pedra") and pp.get("fogo")):
        tocar("fogo", t0, -20, dur)
    for (nm, off, db) in c.get("sfx", []):  # efeitos pedidos à mão no cenas.py
        tocar(nm, t0 + off, db)
if getattr(cfg, "FINAL", ""):
    fv = palavras[-1]["t"] + palavras[-1]["d"]
    tocar("riser", fv - 2.8, -14); tocar("impacto", fv + 0.2, -5)

# trilha de fundo em loop, abaixando quando a voz fala (ducking)
voz = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(pasta, "narracao.mp3"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                   capture_output=True, check=True).stdout, np.float32)
voz = np.pad(voz, (0, max(0, N - len(voz))))[:N]
bl = int(SR * 0.05); rms = np.sqrt(np.convolve(voz ** 2, np.ones(bl) / bl, mode="same"))
fala = np.clip(rms / (np.percentile(rms[rms > 1e-4], 60) + 1e-9), 0, 1)
fala = np.convolve(fala, np.ones(int(SR * 0.3)) / int(SR * 0.3), mode="same")
ganho = 1.0 - 0.55 * fala
trilha = som(getattr(cfg, "TRILHA", "drone")); trilha = np.tile(trilha, (N // len(trilha) + 1, 1))[:N].copy()
trilha *= (10 ** (getattr(cfg, "TRILHA_DB", -21) / 20)) * ganho[:, None]
f = int(SR * 3); trilha[-f:] *= np.linspace(1, 0, f)[:, None]
fundo = trilha + efeitos
pico = np.max(np.abs(fundo))
if pico > 0.95: fundo *= 0.95 / pico
fundo_path = os.path.join(TMP, "fundo.wav"); wavfile.write(fundo_path, SR, (fundo * 32767).astype(np.int16))

# ---------------- render final (voz + trilha + efeitos) ----------------
saida = os.path.join(pasta, cfg.SAIDA)
run(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-i", os.path.join(pasta, "narracao.mp3"), "-i", fundo_path,
     "-filter_complex",
     "[1:a]aresample=48000,highpass=f=75,equalizer=f=170:t=q:w=1:g=2.5,equalizer=f=3200:t=q:w=1.4:g=2,"
     "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
     "aecho=0.9:0.6:35|60:0.10|0.06,aformat=channel_layouts=stereo,"
     # loudnorm segura ~3 s de análise e não devolve o fim do áudio: por isso a voz e a mixagem
     # entram com 5 s de silêncio a mais e são cortadas no tamanho certo depois
     f"apad,atrim=0:{FIM + 5},loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,atrim=0:{FIM}[voz];"
     "[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.5[bg];"
     "[voz][bg]amix=inputs=2:normalize=0:duration=longest,"
     f"apad=pad_dur=5,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.84:level=disabled,atrim=0:{FIM}[a];"
     f"[0:v]vignette=angle=0.5,noise=alls=4:allf=t,ass={ass_path}:fontsdir={FONTS},"
     + ("" if VERT else "fade=t=in:d=0.4,") + f"fade=t=out:st={FIM - 1.0}:d=1.0,trim=0:{FIM}[v]",
     "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
     "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{FIM}",
     "-movflags", "+faststart", saida])
print("PRONTO:", saida)
print("CAPITULOS:", json.dumps([(round(c["t"]), c.get("capitulo")) for c in CENAS if c.get("capitulo")], ensure_ascii=False))
