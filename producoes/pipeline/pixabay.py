"""Vídeos e fotos do Pixabay (licença Pixabay: uso livre, crédito opcional — o motor coloca mesmo assim).

Precisa de PIXABAY_API_KEY no ambiente (arquivo .env na raiz, nunca no código).

  python3 pixabay.py videos "fighter jet night" [n]       -> lista vídeos (id, duração, tamanho, autor, tags)
  python3 pixabay.py fotos  "night sky clouds" [n]         -> lista fotos
  python3 pixabay.py baixar_video <id> <b_nome.mp4>        -> baixa o MP4 (~1920 px) em src/ e registra o crédito
  python3 pixabay.py baixar_foto  <id> <b_nome.jpg>        -> baixa a foto grande em src/ e registra o crédito

Arquivos começam com "b_" para o motor aplicar o tratamento de cor, a etiqueta IMAGEM ILUSTRATIVA e o crédito.
"""
import json, os, sys, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
CRED = os.path.join(BASE, "..", "banco_creditos.json")
UA = {"User-Agent": "InqueritoSombrio/1.0"}


def pedir(caminho, **q):
    chave = os.environ.get("PIXABAY_API_KEY")
    if not chave:
        raise SystemExit("Defina PIXABAY_API_KEY no .env.")
    url = f"https://pixabay.com/api/{caminho}?" + urllib.parse.urlencode(dict(q, key=chave))
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))


def baixar_url(url, destino):
    os.makedirs(SRC, exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r, open(destino, "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b: break
            f.write(b)


def registrar(nome, id_, autor, pagina, tipo):
    c = json.load(open(CRED, encoding="utf-8")) if os.path.exists(CRED) else {}
    c[nome] = {"id": f"pixabay:{tipo}:{id_}", "credito": f"{'Vídeo' if tipo == 'video' else 'Foto'}: {autor} / Pixabay",
               "licenca": "pixabay", "autor": autor, "fonte": "pixabay", "pagina": pagina}
    json.dump(c, open(CRED, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)


def videos(q, n=15):
    for v in pedir("videos/", q=q, per_page=n, safesearch="true")["hits"]:
        g = v["videos"]["large"] if v["videos"]["large"]["url"] else v["videos"]["medium"]
        print(f"{v['id']:>9}  {v['duration']:>3}s  {g['width']}x{g['height']}  {v['user'][:18]:18} {v['tags'][:60]}")


def fotos(q, n=15):
    for f in pedir("", q=q, per_page=n, image_type="photo", safesearch="true")["hits"]:
        print(f"{f['id']:>9}  {f['imageWidth']}x{f['imageHeight']}  {f['user'][:18]:18} {f['tags'][:60]}")


def baixar_video(id_, nome):
    v = pedir("videos/", id=id_)["hits"][0]
    g = next(v["videos"][k] for k in ("large", "medium", "small") if v["videos"][k]["url"] and v["videos"][k]["width"] <= 1920 or k == "small")
    baixar_url(g["url"], os.path.join(SRC, nome))
    registrar(nome, id_, v["user"], v["pageURL"], "video"); print("ok", nome, f"{g['width']}x{g['height']}", f"{v['duration']}s")


def baixar_foto(id_, nome):
    f = pedir("", id=id_)["hits"][0]
    baixar_url(f["largeImageURL"], os.path.join(SRC, nome))
    registrar(nome, id_, f["user"], f["pageURL"], "foto"); print("ok", nome)


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "videos": videos(args[0], int(args[1]) if len(args) > 1 else 15)
    elif cmd == "fotos": fotos(args[0], int(args[1]) if len(args) > 1 else 15)
    elif cmd == "baixar_video": baixar_video(args[0], args[1])
    elif cmd == "baixar_foto": baixar_foto(args[0], args[1])
