"""Imagens do Wikimedia Commons (domínio público e licenças livres), com crédito registrado.

  python3 commons.py "Canudos 1897"                      -> lista arquivos (título | licença | tamanho | url)
  python3 commons.py baixar "File:Canudos village.jpg" w_canudos_vila.jpg
                                                          -> baixa ~1920 px em src/ e registra o crédito

Use o prefixo "w_" e marque a cena com tag="real" (foto real) no cenas.py.
O Commons limita pedidos seguidos (HTTP 429): o script espera e tenta de novo.
"""
import fcntl, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
CRED = os.path.join(BASE, "..", "banco_creditos.json")
UA = {"User-Agent": "InqueritoSombrio/1.0 (canal educativo; github lucasdireitomelo19-png/novodark)"}
API = "https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url|size|extmetadata&iiurlwidth=1920&"


def get(u, binario=False):
    for k in range(6):
        try:
            d = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
            return d if binario else json.loads(d)
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == 5: raise
            time.sleep(10 * (k + 1))


def info(p):
    ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
    autor = re.sub(r"<[^>]+>", "", m.get("Artist", {}).get("value", "")).strip() or "autor desconhecido"
    return ii, m.get("LicenseShortName", {}).get("value", "?"), autor


def buscar(q):
    d = get(API + "generator=search&gsrnamespace=6&gsrlimit=8&gsrsearch=" + urllib.parse.quote(q))
    for p in (d.get("query", {}).get("pages", {}) or {}).values():
        ii, lic, autor = info(p)
        print(p["title"][:70], "|", lic, "|", ii.get("width"), "x", ii.get("height"), "|", autor[:40])


def baixar(titulo, nome):
    d = get(API + "titles=" + urllib.parse.quote(titulo))
    p = list(d["query"]["pages"].values())[0]; ii, lic, autor = info(p)
    os.makedirs(SRC, exist_ok=True)
    open(os.path.join(SRC, nome), "wb").write(get(ii.get("thumburl") or ii["url"], binario=True))
    with open(CRED + ".lock", "w") as trava:
        fcntl.flock(trava, fcntl.LOCK_EX)
        c = json.load(open(CRED, encoding="utf-8")) if os.path.exists(CRED) else {}
        c[nome] = {"id": "commons:" + titulo, "credito": f"Foto: {autor[:60]} / Wikimedia Commons ({lic})", "licenca": lic.lower(),
                   "autor": autor, "fonte": "wikimedia commons", "pagina": ii.get("descriptionurl", "")}
        json.dump(c, open(CRED, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print("ok", nome, ii.get("thumbwidth") or ii.get("width"), "x", ii.get("thumbheight") or ii.get("height"), "|", lic, "|", autor[:40])


if __name__ == "__main__":
    if sys.argv[1] == "baixar": baixar(sys.argv[2], sys.argv[3])
    else: buscar(sys.argv[1])
