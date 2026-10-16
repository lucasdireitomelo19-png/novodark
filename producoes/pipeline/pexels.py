"""Fotos e vídeos do Pexels (licença Pexels: uso livre, crédito opcional — o motor coloca mesmo assim).

Precisa da variável de ambiente PEXELS_API_KEY (configurada nas variáveis do ambiente, nunca no código).

  python3 pexels.py fotos  "dark forest night" [n]       -> lista fotos (id, tamanho, autor)
  python3 pexels.py videos "rain window night" [n]       -> lista vídeos (id, duração, tamanho, autor)
  python3 pexels.py baixar_foto  <id> <b_nome.jpg>        -> baixa em src/ (resolução ~2K) e registra o crédito
  python3 pexels.py baixar_video <id> <b_nome.mp4> [vert] -> baixa o MP4 HD (horizontal, ou vertical com "vert")

Arquivos começam com "b_" para o motor aplicar o tratamento de cor, a etiqueta IMAGEM ILUSTRATIVA e o crédito.
"""
import json, os, sys, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
CRED = os.path.join(BASE, "..", "banco_creditos.json")


def pedir(url, binario=False):
    chave = os.environ.get("PEXELS_API_KEY")
    if not chave:
        raise SystemExit("Defina PEXELS_API_KEY nas variáveis do ambiente.")
    req = urllib.request.Request(url, headers={"Authorization": chave, "User-Agent": "CasosSemResposta/1.0"})
    dados = urllib.request.urlopen(req, timeout=120).read()
    return dados if binario else json.loads(dados)


def baixar_url(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": "CasosSemResposta/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r, open(destino, "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b: break
            f.write(b)


def registrar(nome, id_, autor, pagina, tipo):
    c = json.load(open(CRED, encoding="utf-8")) if os.path.exists(CRED) else {}
    c[nome] = {"id": f"pexels:{tipo}:{id_}", "credito": f"{'Vídeo' if tipo == 'video' else 'Foto'}: {autor} / Pexels",
               "licenca": "pexels", "autor": autor, "fonte": "pexels", "pagina": pagina}
    json.dump(c, open(CRED, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)


def fotos(q, n=15):
    d = pedir("https://api.pexels.com/v1/search?" + urllib.parse.urlencode({"query": q, "per_page": n, "orientation": "landscape"}))
    for f in d["photos"]:
        print(f"{f['id']:>10}  {f['width']}x{f['height']}  {f['photographer'][:25]:25} {f.get('alt', '')[:60]}")


def videos(q, n=15):
    d = pedir("https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": q, "per_page": n}))
    for v in d["videos"]:
        print(f"{v['id']:>10}  {v['duration']:>3}s  {v['width']}x{v['height']}  {v['user']['name'][:25]:25} {v['url'][-60:]}")


def baixar_foto(id_, nome):
    f = pedir(f"https://api.pexels.com/v1/photos/{id_}")
    os.makedirs(SRC, exist_ok=True)
    baixar_url(f["src"]["large2x"], os.path.join(SRC, nome))
    registrar(nome, id_, f["photographer"], f["url"], "foto"); print("ok", nome)


def baixar_video(id_, nome, vertical=False):
    v = pedir(f"https://api.pexels.com/videos/videos/{id_}")
    arqs = [a for a in v["video_files"] if a.get("file_type") == "video/mp4" and a.get("width") and a.get("height")]
    arqs = [a for a in arqs if (a["height"] > a["width"]) == vertical] or arqs
    alvo = 1920 if not vertical else 1080
    a = min(arqs, key=lambda a: (abs(max(a["width"], a["height"]) - (alvo if not vertical else 1920)), -a["width"]))
    os.makedirs(SRC, exist_ok=True)
    baixar_url(a["link"], os.path.join(SRC, nome))
    registrar(nome, id_, v["user"]["name"], v["url"], "video"); print("ok", nome, f"{a['width']}x{a['height']}", f"{v['duration']}s")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "fotos": fotos(args[0], int(args[1]) if len(args) > 1 else 15)
    elif cmd == "videos": videos(args[0], int(args[1]) if len(args) > 1 else 15)
    elif cmd == "baixar_foto": baixar_foto(args[0], args[1])
    elif cmd == "baixar_video": baixar_video(args[0], args[1], len(args) > 2 and args[2] == "vert")
