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
spec = importlib.util.spec_from_file_location("cenas", os.path.join(pasta, "cenas.py"))
cfg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cfg)
FIM = cfg.FIM
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

# divide automaticamente planos longos de vídeo/imagem (> MAX s) para manter o ritmo
MAX = getattr(cfg, "MAX_PLANO", 7.0)
final = []
for i, c in enumerate(CENAS):
    fim = CENAS[i + 1]["t"] if i + 1 < len(CENAS) else FIM
    dur = fim - c["t"]
    if dur > MAX and not c["src"].startswith("anim:") and not c.get("inteiro"):
        n = int(dur // (MAX * 0.75)) + 1
        for k in range(n):
            d = dict(c, t=round(c["t"] + dur * k / n, 3))
            if k:
                d.pop("texto", None); d.pop("flash", None); d.pop("punch", None)
                if not c["src"].lower().endswith((".jpg", ".png")):
                    d["ss"] = c.get("ss", 0) + dur * k / n * c.get("vel", 1.0)
                d["pan"] = [(0.3, 0.5), (0.7, 0.5), (0.5, 0.3), (0.5, 0.7)][k % 4]
                z0, z1 = c.get("zoom", (1.05, 1.13))
                d["zoom"] = (z1, z0) if k % 2 else (z0, z1)
            final.append(d)
    else:
        final.append(c)
CENAS = final

def dur_de(i):
    return (CENAS[i + 1]["t"] if i + 1 < len(CENAS) else FIM) - CENAS[i]["t"]

if os.environ.get("CHECK"):
    for i, c in enumerate(CENAS):
        print(f"{i:03d} {c['t']:7.2f} {dur_de(i):5.2f}s  {c['src']}")
    print("planos:", len(CENAS), "| média:", round(FIM / len(CENAS), 2), "s")
    sys.exit()

# ---------------- animações ----------------
jobs = []
for i, c in enumerate(CENAS):
    if c["src"].startswith("anim:"):
        saida = os.path.join(TMP, f"anim_{i:03d}.mp4")
        jobs.append(dict(saida=saida, cena=c["src"][5:], dur=round(dur_de(i) + 0.2, 3), p=c.get("p", {})))
        c["_arq"] = saida
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
    f = []
    if vel != 1.0:
        f.append(f"setpts=PTS/{vel}")
    if c.get("crop"):
        x, y, w, h = c["crop"]; f.append(f"crop={w}:{h}:{x}:{y}")
    if c.get("fit"):
        f.append(f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                 f"boxblur=40:3,eq=brightness=-0.15[bg];[b]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                 f"[bg][fg]overlay=(W-w)/2:(H-h)/2")
    else:
        f.append(f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}")
    z0, z1 = c.get("zoom", (1.0, 1.0) if anim else (1.05, 1.13))
    if (z0, z1) != (1.0, 1.0) or c.get("shake"):
        zoom = f"{z0}+{z1 - z0}*t/{dur:.3f}"
        f.append(f"scale=w='trunc({W}*({zoom})/2)*2':h=-2:eval=frame:flags=bicubic")
        a = c.get("shake", 0); px, py = c.get("pan", (0.5, 0.5))
        xs = f"(iw-ow)*{px}" + (f"+{a}*sin(47*t)+{a*0.6}*sin(29*t+1)" if a else "")
        ys = f"(ih-oh)*{py}" + (f"+{a*0.8}*sin(41*t+2)+{a*0.5}*sin(23*t)" if a else "")
        f.append(f"crop={W}:{H}:x='max(0,min(iw-ow,{xs}))':y='max(0,min(ih-oh,{ys}))'")
    f.append(f"setsar=1,fps={FPS}" + ("" if anim else f",eq=contrast=1.06:saturation={c.get('sat', 1.12)}"))
    if c.get("flash"):
        f.append("fade=t=in:st=0:d=0.15:color=white")
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
    pausa = prox is None or prox["t"] - (p["t"] + p["d"]) > 0.25
    longo = prox is not None and sum(len(x["w"]) + 1 for x in atual) + len(prox["w"]) > 38
    if pausa or longo or len(atual) >= 7:
        grupos.append(atual); atual = []
if atual:
    grupos.append(atual)
ev = []
for gi, g in enumerate(grupos):
    fim_g = grupos[gi + 1][0]["t"] if gi + 1 < len(grupos) else FIM
    fim_g = min(fim_g, g[-1]["t"] + g[-1]["d"] + 0.5)
    for wi, p in enumerate(g):
        fim = g[wi + 1]["t"] if wi + 1 < len(g) else fim_g
        txt = [(r"{\c&H00C8FF&}" + q["w"] + r"{\c&HFFFFFF&}") if wj == wi else q["w"] for wj, q in enumerate(g)]
        ev.append(f"Dialogue: 3,{ts(p['t'])},{ts(fim)},Legenda,,0,0,0,,{' '.join(txt)}")

ROTULOS = {"real": ("Real", "● IMAGEM REAL"), "sim": ("Anim", "SIMULAÇÃO"), "anim": ("Anim", "ANIMAÇÃO"), "ilus": ("Anim", "ILUSTRAÇÃO"), "rec": ("Anim", "RECRIAÇÃO")}
def credito_padrao(src):
    if src.startswith("anim:"): return getattr(cfg, "CREDITO_ANIM", "Ilustração: Casos Sem Resposta")
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
ass_path = os.path.join(TMP, "legendas.ass"); open(ass_path, "w", encoding="utf-8").write(ass)

# ---------------- render final (somente voz) ----------------
saida = os.path.join(pasta, cfg.SAIDA)
run(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-i", os.path.join(pasta, "narracao.mp3"),
     "-filter_complex",
     "[1:a]aresample=44100,highpass=f=75,equalizer=f=170:t=q:w=1:g=2.5,equalizer=f=3200:t=q:w=1.4:g=2,"
     "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
     "aecho=0.9:0.6:35|60:0.10|0.06,aformat=channel_layouts=stereo,"
     f"apad,atrim=0:{FIM},loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=disabled[a];"
     f"[0:v]vignette=angle=0.5,noise=alls=4:allf=t,ass={ass_path}:fontsdir={FONTS},"
     f"fade=t=in:d=0.4,fade=t=out:st={FIM - 1.0}:d=1.0,trim=0:{FIM}[v]",
     "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
     "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{FIM}",
     "-movflags", "+faststart", saida])
print("PRONTO:", saida)
print("CAPITULOS:", json.dumps([(round(c["t"]), c.get("capitulo")) for c in CENAS if c.get("capitulo")], ensure_ascii=False))
