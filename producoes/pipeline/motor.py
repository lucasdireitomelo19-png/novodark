"""Motor de montagem de Shorts (1080x1920, 61 s, só voz).

Uso: python3 motor.py <pasta_do_video>
A pasta precisa ter: narracao.mp3, palavras.json e cenas.py (com CENAS, CREDITO, FINAL).
"""
import importlib.util, json, os, subprocess, sys

W, H, FPS, FIM = 1080, 1920, 30, 61.0
BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
FONTS = os.path.join(BASE, "fonts")

pasta = os.path.abspath(sys.argv[1])
spec = importlib.util.spec_from_file_location("cenas", os.path.join(pasta, "cenas.py"))
cfg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cfg)
CENAS = cfg.CENAS
os.makedirs(os.path.join(pasta, "tmp"), exist_ok=True)

def run(cmd):
    subprocess.run(cmd, check=True)

def dur_de(i):
    return (CENAS[i + 1]["t"] if i + 1 < len(CENAS) else FIM) - CENAS[i]["t"]

# ---------------- cenas ----------------
partes = []
for i, c in enumerate(CENAS):
    dur, vel = dur_de(i), c.get("vel", 1.0)
    out = os.path.join(pasta, "tmp", f"parte_{i:02d}.mp4")
    partes.append(out)
    chave = json.dumps({k: v for k, v in c.items() if k not in ("texto", "tag")}, sort_keys=True) + f"{dur:.3f}"
    if os.path.exists(out) and open(out + ".key").read() == chave:
        continue
    arq = os.path.join(SRC, c["src"])
    imagem = arq.lower().endswith((".jpg", ".png"))
    f = []
    if vel != 1.0:
        f.append(f"setpts=PTS/{vel}")
    if c.get("crop"):
        x, y, w, h = c["crop"]
        f.append(f"crop={w}:{h}:{x}:{y}")
    if c.get("fit"):
        # imagem inteira sobre fundo desfocado (para fotos pequenas ou que não podem ser cortadas)
        f.append(f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                 f"boxblur=40:3,eq=brightness=-0.15[bg];[b]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                 f"[bg][fg]overlay=(W-w)/2:(H-h)/2")
    else:
        f.append(f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}")
    z0, z1 = c.get("zoom", (1.07, 1.15))
    zoom = f"{z0}+{z1 - z0}*t/{dur:.3f}"
    if c.get("punch"):
        zoom += "+0.25*max(0,1-t/0.3)"
    f.append(f"scale=w='trunc({W}*({zoom})/2)*2':h=-2:eval=frame:flags=bicubic")
    a = c.get("shake", 0)
    px, py = c.get("pan", (0.5, 0.5))   # ponto focal (0-1) para onde a câmera aponta
    xs = f"(iw-ow)*{px}" + (f"+{a}*sin(47*t)+{a*0.6}*sin(29*t+1)" if a else "")
    ys = f"(ih-oh)*{py}" + (f"+{a*0.8}*sin(41*t+2)+{a*0.5}*sin(23*t)" if a else "")
    f.append(f"crop={W}:{H}:x='max(0,min(iw-ow,{xs}))':y='max(0,min(ih-oh,{ys}))'")
    f.append(f"setsar=1,fps={FPS},eq=contrast=1.07:saturation={c.get('sat', 1.15)}")
    if c.get("chuva"):
        # chuva de vidro horizontal (ilustração): faíscas esticadas varrendo a tela de lado
        f.append("format=gbrp[q];"
                 f"nullsrc=s={W//2}x{H//2}:r={FPS},geq=lum='if(lt(random(1),0.0035),255,0)':cb=128:cr=128,"
                 f"avgblur=sizeX=28:sizeY=1,lutyuv=y='min(255,val*14)':u=128:v=128,scale={W}:{H},"
                 "rotate=-0.18:fillcolor=black,"
                 "format=gbrp,colorchannelmixer=rr=0.75:gg=0.9:bb=1.0[r];"
                 "[q][r]blend=all_mode=screen:shortest=1,format=yuv420p")
    if c.get("flash"):
        f.append("fade=t=in:st=0:d=0.15:color=white")
    entrada = ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur + 0.1:.3f}", "-i", arq] if imagem else \
              ["-ss", str(c.get("ss", 0)), "-t", f"{dur * vel + 0.2:.3f}", "-i", arq]
    run(["ffmpeg", "-v", "error", "-y", *entrada, "-filter_complex", ",".join(f).replace(",split", ",split"),
         "-an", "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "fast", "-crf", "17",
         "-pix_fmt", "yuv420p", out])
    open(out + ".key", "w").write(chave)
    print("ok", os.path.basename(out), f"{dur:.2f}s", c["src"])

lista = os.path.join(pasta, "tmp", "lista.txt")
with open(lista, "w") as fh:
    fh.writelines(f"file '{p}'\n" for p in partes)
bruto = os.path.join(pasta, "tmp", "video_bruto.mp4")
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", bruto])

# ---------------- legendas, etiquetas e textos de apoio ----------------
palavras = json.load(open(os.path.join(pasta, "palavras.json")))
def ts(s):
    h, s = divmod(max(s, 0), 3600); m, s = divmod(s, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

grupos, atual = [], []
for k, p in enumerate(palavras):
    atual.append(p)
    prox = palavras[k + 1] if k + 1 < len(palavras) else None
    pausa = prox is None or prox["t"] - (p["t"] + p["d"]) > 0.22
    longo = prox is not None and sum(len(x["w"]) + 1 for x in atual) + len(prox["w"]) > 16
    if len(atual) >= 3 or pausa or longo:
        grupos.append(atual); atual = []
if atual:
    grupos.append(atual)

ev = []
for gi, g in enumerate(grupos):
    fim_g = grupos[gi + 1][0]["t"] if gi + 1 < len(grupos) else FIM
    fim_g = min(fim_g, g[-1]["t"] + g[-1]["d"] + 0.6)
    for wi, p in enumerate(g):
        fim = g[wi + 1]["t"] if wi + 1 < len(g) else fim_g
        txt = []
        for wj, q in enumerate(g):
            w = q["w"].upper().rstrip(".,!?:…")
            txt.append(r"{\c&H00E5FF&}" + w + r"{\c&HFFFFFF&}" if wj == wi else w)
        pop = r"{\fscx115\fscy115\t(0,90,\fscx100\fscy100)}" if wi == 0 else ""
        ev.append(f"Dialogue: 3,{ts(p['t'])},{ts(fim)},Legenda,,0,0,0,,{pop}{' '.join(txt)}")

ROTULOS = {"real": ("Real", "● IMAGEM REAL"), "sim": ("Anim", "SIMULAÇÃO NASA"),
           "anim": ("Anim", "ANIMAÇÃO"), "ilus": ("Anim", "ILUSTRAÇÃO")}
for i, c in enumerate(CENAS):
    t0, t1 = c["t"], c["t"] + dur_de(i)
    if c.get("tag"):
        estilo, texto = ROTULOS[c["tag"]]
        ev.append(f"Dialogue: 1,{ts(t0)},{ts(t1)},{estilo},,0,0,0,,{texto}")
    if c.get("circulo"):
        ev.append(f"Dialogue: 2,{ts(t0 + 0.3)},{ts(t1)},Destaque,,0,0,0,,"
                  r"{\an7\pos(540,960)\p1\bord7\shad0\1a&HFF&\3c&H00E5FF&\fad(200,0)}"
                  "m -70 0 b -70 -39 -39 -70 0 -70 b 39 -70 70 -39 70 0 b 70 39 39 70 0 70 b -39 70 -70 39 -70 0{\\p0}")
    if c.get("texto"):
        ev.append(f"Dialogue: 2,{ts(t0 + 0.1)},{ts(t1)},Destaque,,0,0,0,,"
                  r"{\fad(120,0)\fscx70\fscy70\t(0,160,\fscx100\fscy100)}" + c["texto"])

ultimo_fim = palavras[-1]["t"] + palavras[-1]["d"]
ev.append(f"Dialogue: 4,{ts(ultimo_fim + 0.15)},{ts(FIM)},Final,,0,0,0,,"
          r"{\fad(200,0)\fscx60\fscy60\t(0,250,\fscx100\fscy100)}" + cfg.FINAL)

ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Legenda,Montserrat Thin ExtraBold,98,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,7,4,2,70,70,600,1
Style: Destaque,Montserrat Thin ExtraBold,84,&H0000E5FF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,1,0,1,6,5,8,60,60,330,1
Style: Final,Montserrat Thin ExtraBold,120,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,2,0,1,8,6,5,60,60,0,1
Style: Real,Montserrat Thin ExtraBold,40,&H00FFFFFF,&H00FFFFFF,&H001E1EE6,&H00000000,0,0,0,0,100,100,2,0,3,12,0,8,40,40,230,1
Style: Anim,Montserrat Thin ExtraBold,30,&H00FFFFFF,&H00FFFFFF,&H70000000,&H00000000,0,0,0,0,100,100,2,0,3,10,0,8,40,40,230,1
Style: Credito,Montserrat Thin ExtraBold,28,&H40FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,2,0,2,40,40,90,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{ts(0)},{ts(FIM)},Credito,,0,0,0,,{cfg.CREDITO}
""" + "\n".join(ev) + "\n"
ass_path = os.path.join(pasta, "tmp", "legendas.ass")
open(ass_path, "w", encoding="utf-8").write(ass)

# ---------------- render final (somente voz) ----------------
saida = os.path.join(pasta, cfg.SAIDA)
run(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-i", os.path.join(pasta, "narracao.mp3"),
     "-filter_complex",
     "[1:a]aresample=44100,highpass=f=75,equalizer=f=170:t=q:w=1:g=2.5,equalizer=f=3200:t=q:w=1.4:g=2,"
     "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
     "aecho=0.9:0.6:35|60:0.10|0.06,aformat=channel_layouts=stereo,"
     f"apad,atrim=0:{FIM},loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=disabled[a];"
     f"[0:v]vignette=angle=0.55,noise=alls=5:allf=t,ass={ass_path}:fontsdir={FONTS},"
     f"fade=t=out:st={FIM - 0.4}:d=0.4,trim=0:{FIM}[v]",
     "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
     "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{FIM}",
     "-movflags", "+faststart", saida])
print("PRONTO:", saida)
