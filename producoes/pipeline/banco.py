"""Banco de imagens via Openverse (CC0, domínio público e CC BY), sem chave de API.

  python3 banco.py buscar "night forest fog" [n]     -> lista resultados (id, licença, tamanho, fonte, título)
  python3 banco.py baixar <id> <nome.jpg>             -> baixa em src/ e registra o crédito em ../banco_creditos.json

Limite sem chave: 20 pedidos/min e 200/dia (cada busca e cada download contam 1).
Licenças aceitas: cc0, pdm (domínio público) e by (exige crédito, que o motor coloca no canto do vídeo).
"""
import json, os, sys, time, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
CRED = os.path.join(BASE, "..", "banco_creditos.json")
API = "https://api.openverse.org/v1/images/"
UA = {"User-Agent": "CasosSemResposta/1.0 (canal educativo)"}


def pedir(url, binario=False):
    for tent in range(4):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)
            restante = r.headers.get("x-ratelimit-available-anon_sustained")
            dados = r.read()
            if restante is not None:
                print(f"  (pedidos restantes hoje: {restante})", file=sys.stderr)
            return dados if binario else json.loads(dados)
        except urllib.error.HTTPError as e:
            if e.code == 429 and tent < 3:
                time.sleep(20 * (tent + 1)); continue
            raise


def creditos():
    return json.load(open(CRED, encoding="utf-8")) if os.path.exists(CRED) else {}


def buscar(q, n=20):
    d = pedir(API + "?" + urllib.parse.urlencode({"q": q, "license": "cc0,pdm,by", "page_size": n, "size": "large", "mature": "false"}))
    print(f"{d['result_count']} resultados para {q!r}")
    os.makedirs(SRC, exist_ok=True); cp = os.path.join(SRC, "_busca.json")
    cache = json.load(open(cp)) if os.path.exists(cp) else {}
    cache.update({r["id"]: r for r in d["results"]}); json.dump(cache, open(cp, "w"))
    for r in d["results"]:
        print(f"{r['id']}  {r['license']:4} {r.get('width') or 0:>5}x{r.get('height') or 0:<5} {r['source'][:10]:10} {(r['title'] or '')[:60]}")


def baixar(id_, nome):
    cp = os.path.join(SRC, "_busca.json")
    cache = json.load(open(cp)) if os.path.exists(cp) else {}
    meta = cache.get(id_) or pedir(API + id_ + "/")  # usa os dados da busca para economizar pedidos
    os.makedirs(SRC, exist_ok=True)
    destino = os.path.join(SRC, nome)
    open(destino, "wb").write(pedir(API + id_ + "/thumb/?full_size=true&compressed=false", binario=True))
    lic = meta["license"].upper() if meta["license"] in ("cc0", "pdm") else f"CC {meta['license'].upper()} {meta.get('license_version') or ''}".strip()
    autor = (meta.get("creator") or "").strip()
    texto = f"Foto: {autor} ({lic}) via {meta['source']}" if autor and meta["license"] == "by" else f"Imagem: {meta['source']} ({lic})"
    c = creditos()
    c[nome] = {"id": id_, "credito": texto, "licenca": meta["license"], "autor": autor, "fonte": meta["source"],
               "pagina": meta.get("foreign_landing_url"), "titulo": meta.get("title")}
    json.dump(c, open(CRED, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print("ok", nome, "|", texto)


def restaurar():
    """Baixa de novo todas as imagens registradas (src/ não vai para o git)."""
    for nome, info in creditos().items():
        if not os.path.exists(os.path.join(SRC, nome)):
            baixar(info["id"], nome); time.sleep(3.2)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "buscar": buscar(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 20)
    elif cmd == "baixar": baixar(sys.argv[2], sys.argv[3])
    elif cmd == "restaurar": restaurar()
