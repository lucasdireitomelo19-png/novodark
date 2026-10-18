"""Vídeos do Mixkit (Mixkit Stock Video Free License: uso livre, inclusive comercial, sem atribuição obrigatória;
o motor credita mesmo assim). Sem chave de API.

  python3 mixkit.py buscar fighter-jet            -> lista vídeos da página do termo (id | slug)
  python3 mixkit.py baixar 46954 b_mk_jato.mp4    -> baixa o MP4 (1080p, ou 720p se não houver) em src/ e registra o crédito

Use termos em inglês com hífen, como na URL do site: mixkit.co/free-stock-video/<termo>/
"""
import fcntl, json, os, re, sys, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
SRC, CRED = os.path.join(BASE, "src"), os.path.join(BASE, "..", "banco_creditos.json")
UA = {"User-Agent": "Mozilla/5.0 (InqueritoSombrio)"}


def pagina(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", "ignore")


def buscar(termo):
    html = pagina(f"https://mixkit.co/free-stock-video/{termo}/")
    for slug, id_ in sorted(set(re.findall(r'/free-stock-video/([a-z0-9-]+)-(\d+)/', html)), key=lambda x: x[1]):
        print(f"{id_:>7} | {slug}")


def baixar(id_, nome):
    os.makedirs(SRC, exist_ok=True)
    for q in ("1080", "720"):
        try:
            d = urllib.request.urlopen(urllib.request.Request(f"https://assets.mixkit.co/videos/{id_}/{id_}-{q}.mp4", headers=UA), timeout=300).read()
            if len(d) > 100_000: break
        except Exception:
            d = None
    if not d: raise SystemExit(f"não consegui baixar o vídeo {id_}")
    open(os.path.join(SRC, nome), "wb").write(d)
    with open(CRED + ".lock", "w") as t:
        fcntl.flock(t, fcntl.LOCK_EX)
        c = json.load(open(CRED, encoding="utf-8")) if os.path.exists(CRED) else {}
        c[nome] = {"id": f"mixkit:video:{id_}", "credito": "Vídeo: Mixkit", "licenca": "mixkit", "fonte": "mixkit",
                   "pagina": f"https://mixkit.co/free-stock-video/{id_}/"}
        json.dump(c, open(CRED, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print("ok", nome, q + "p", f"{len(d) // 1024} KB")


if __name__ == "__main__":
    if sys.argv[1] == "buscar": buscar(sys.argv[2])
    else: baixar(sys.argv[2], sys.argv[3])
