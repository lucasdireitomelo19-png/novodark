import re, json, sys, os
def campos(txt):
    d = {}
    def cb(after):  # primeiro bloco de código depois de uma posição
        m = re.search(r"```[a-z]*\n(.*?)```", txt[after:], re.S); return m.group(1).strip() if m else None
    m = re.search(r"\*\*T[íi]tulo[^*]*\*\*:?\s*`([^`]+)`", txt) or re.search(r"\*\*T[íi]tulo[^*]*\*\*\s*\n```[a-z]*\n(.*?)```", txt, re.S) \
        or re.search(r"##\s*1\.\s*T[ÍI]TULO\s*\n+\*\*(.+?)\*\*", txt)
    if m: d["yt_titulo"] = m.group(1).strip()
    m = re.search(r"\*\*Descri[çc][ãa]o[^*]*\*\*", txt) or re.search(r"\n##+[^\n]*DESCRI[ÇC][ÃA]O[^\n]*\n", txt)
    if m:
        v = cb(m.end());  d["yt_desc"] = v if v else None
    m = re.search(r"\*\*Tags[^*]*\*\*:?\s*`([^`]+)`", txt)
    if m: d["tags"] = m.group(1).strip()
    m = re.search(r"\*\*TikTok[^*]*\*\*:?\s*`([^`]+)`", txt)
    if m: d["tiktok"] = m.group(1).strip()
    else:
        m = re.search(r"\*\*TikTok[^*]*\*\*:?\s*\n", txt) or re.search(r"\n###\s*TikTok\s*\n", txt)
        if m: d["tiktok"] = cb(m.end())
    m = re.search(r"\*\*Reels[^*]*\*\*:?\s*\n", txt) or re.search(r"\n###\s*Reels\s*\n", txt)
    if m: d["reels"] = cb(m.end())
    m = re.search(r"\*\*Coment[áa]rio fixado[^*]*\*\*:?\s*\n?>?\s*`?([^\n`]+)", txt)
    if m: d["comentario"] = m.group(1).strip().strip('*').strip()
    return {k: v for k, v in d.items() if v}
out = []
for f in sys.argv[1:]:
    t = open(f, encoding="utf-8").read()
    secs = re.split(r"\n(?=## )", t)
    inteiro = campos(t) if len(secs) < 3 or re.match(r"\d\d_", os.path.basename(f)) and "lote" not in f else None
    if inteiro and "descricoes" not in f and "semanas" not in f and "lote" not in f and "shorts_lote" not in f:
        out.append({"arquivo": os.path.basename(f), "secao": t.split("\n")[0][2:60], **inteiro}); continue
    for s in secs:
        c = campos(s)
        if len(c) >= 2: out.append({"arquivo": os.path.basename(f), "secao": s.split("\n")[0][3:70], **c})
json.dump(out, open(sys.argv[0].replace("extrai.py", "extraido.json"), "w"), ensure_ascii=False, indent=1)
for o in out: print(o["arquivo"][:22], "|", o["secao"][:45], "|", ",".join(k for k in o if k not in ("arquivo","secao")))
