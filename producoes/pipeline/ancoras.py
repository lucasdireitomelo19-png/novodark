"""Converte trechos da narração em tempos (para cenas.py dos Shorts)."""
import json, os, re, unicodedata
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9 ]+", " ", "".join(c for c in s if unicodedata.category(c) != "Mn"))
def montar(pasta, lista):
    pal = json.load(open(os.path.join(pasta, "palavras.json")))
    txt, ini = "", []
    for p in pal:
        for parte in norm(p["w"]).split():
            ini.append((len(txt), p["t"])); txt += parte + " "
    cur, out = 0, []
    for i, (anc, opc) in enumerate(lista):
        if i == 0:
            t = 0.0
        else:
            alvo = " ".join(norm(anc).split()) + " "
            pos = txt.find(alvo, cur)
            if pos < 0: raise SystemExit(f"Âncora não encontrada: {anc!r}")
            t = max(0.0, next(t for c, t in reversed(ini) if c <= pos) - 0.1); cur = pos + 1
        out.append(dict(opc, t=round(t, 2)))
    return out
