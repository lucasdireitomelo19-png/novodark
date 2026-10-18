import json, re, os
S = "/tmp/claude-0/-home-user-novodark/c77a4c46-df71-5c2e-8f10-77760764214f/scratchpad/central/"
E = "/home/user/lucasdireitomelo19-png/edittest/producoes/"
N = "/home/user/novodark/producoes/"
ext = json.load(open(S + "extraido.json"))
def achar(arq, sec):
    for e in ext:
        if e["arquivo"].startswith(arq) and sec in e["secao"]:
            return {k: v for k, v in e.items() if k not in ("arquivo", "secao")}
    raise SystemExit(f"faltou {arq} {sec}")
def bloco(txt, depois):
    i = txt.index(depois); m = re.search(r"```[a-z]*\n(.*?)```", txt[i:], re.S); return m.group(1).strip()
def inline(txt, depois, rotulo):
    i = txt.index(depois); m = re.search(r"\*\*" + rotulo + r"[^*]*\*\*:?\s*`([^`]+)`", txt[i:]); return m.group(1).strip()
desc = open(E + "descricoes.md", encoding="utf-8").read()
reels_parte = desc[desc.index("# Legendas para Instagram Reels"):]
deriv = desc[desc.index("# Shorts derivados"):]
docs = []
def add(id_, canal, tipo, ordem, nome, status, leg, **kw):
    docs.append({"id": id_, "data": dict(canal=canal, tipo=tipo, ordem=ordem, nome=nome, status=status, data_pub=kw.get("data_pub", ""), hora=kw.get("hora", ""),
        plataformas={}, legendas={k: v for k, v in leg.items() if v}, notas=kw.get("notas", ""), video_asset=kw.get("asset", ""),
        video_url=("/_blob/" + kw["asset"]) if kw.get("asset") else "", video_link="", atualizado="2026-10-18T00:00:00Z")})
NOTA_LS = "Status importado do repositório edittest: confirme se já foi publicado e marque as plataformas."
# ---------------- Lado Sombrio do Universo ----------------
for o, (sec, nome) in enumerate([("01 · Buraco negro", "Queda num buraco negro (simulação NASA)"), ("02 · Voyager 1", "Voyager 1"), ("03 · Planeta de vidro", "HD 189733 b, o planeta de vidro")], 1):
    l = achar("descricoes", sec); l["reels"] = bloco(reels_parte, "## " + sec.split(" (")[0])
    add(f"lado-{o:02d}", "lado", "short", o, nome, "Pronto", l, notas=NOTA_LS)
l = {"yt_titulo": "Por que o universo está em silêncio? A assustadora teoria da Floresta Negra",
     "yt_desc": bloco(open(E + "04_floresta_negra_10min.md", encoding="utf-8").read(), "## Descrição para o YouTube"),
     "tags": re.search(r"\*\*04\*\* `([^`]+)`", desc).group(1), "comentario": "Se você recebesse uma mensagem de outra civilização, responderia ou ficaria em silêncio? 👇"}
add("lado-04", "lado", "longo", 4, "A Teoria da Floresta Negra (10 min)", "Pronto", l, notas=NOTA_LS)
for o, (sec, nome) in zip((5, 6, 7), [("05 · O sinal Wow!", "O sinal Wow!"), ("06 · Nós já gritamos", "Nós já gritamos"), ("07 · A floresta escura", "A floresta escura")]):
    i = deriv.index("## " + sec); j = deriv.index("###", i) if "###" in deriv[i:] else len(deriv)
    titulo = re.search(r"\*\*Título \(YouTube\):\*\* `([^`]+)`", deriv[i:]).group(1)
    yt = bloco(deriv, "## " + sec)
    v = deriv.index("### " + sec)
    tt = bloco(deriv, "### " + sec); rl = bloco(deriv[v:], "**Reels**")
    tags = re.search(r"\*\*0" + str(o) + r"\*\* `([^`]+)`", desc).group(1)
    add(f"lado-{o:02d}", "lado", "short", o, nome, "Pronto", {"yt_titulo": titulo, "yt_desc": yt, "tiktok": tt, "reels": rl, "tags": tags}, notas=NOTA_LS + " Short derivado do vídeo da Floresta Negra.")
d5 = open(E + "05_dentro_buraco_negro_10min.md", encoding="utf-8").read(); l = achar("05_dentro", "05"); l["yt_desc"] = bloco(d5, "## Descrição para o YouTube")
add("lado-08", "lado", "longo", 8, "O que existe dentro de um buraco negro? (10 min)", "Agendado", l, data_pub="2026-10-18", hora="19:00", notas=NOTA_LS)
for o, (arq, nome) in zip((9, 10, 11), [("06_estrela", "Estrela de nêutrons"), ("07_terra", "E se a Terra parasse de girar?"), ("08_buraco", "Buraco que atravessa a Terra")]):
    add(f"lado-{o:02d}", "lado", "short", o, nome, "Pronto", achar(arq, arq[:2]), notas=NOTA_LS)
for k, (sec, nome) in enumerate([("1 · Simulação", "E se o universo for uma simulação?"), ("2 · Betelgeuse", "Betelgeuse vai explodir"), ("3 · ʻOumuamua", "ʻOumuamua"), ("4 · Vácuo falso", "Vácuo falso"),
        ("5 · BLC1", "BLC1"), ("6 · Esferas de Dyson", "Esferas de Dyson"), ("7 · Estrela de Tabby", "Estrela de Tabby"), ("8 · Planeta Nove", "Planeta Nove"),
        ("9 · Rajadas", "Rajadas rápidas de rádio"), ("10 · Vazio", "Vazio de Boötes")]):
    add(f"lado-{12 + k:02d}", "lado", "short", 12 + k, nome, "Pronto", achar("09_lote", sec), notas=NOTA_LS + " Lote viral 01 (~45 s).")
for k, (sec, nome, dia, hora) in enumerate([("1 · Vênus", "Em Vênus, um dia dura mais que um ano", "2026-10-17", "09:00"), ("2 · A Lua", "A Lua está fugindo da Terra", "2026-10-17", "13:00"),
        ("3 · As pegadas", "As pegadas na Lua", "2026-10-17", "20:00"), ("4 · Saturno", "Saturno flutuaria na água", "2026-10-18", "09:00"),
        ("5 · Netuno", "Os ventos de Netuno", "2026-10-18", "13:00"), ("6 · O buraco negro que canta", "O buraco negro que canta", "2026-10-18", "20:00")]):
    add(f"lado-{22 + k:02d}", "lado", "short", 22 + k, nome, "Agendado", achar("2026-10-17", sec), data_pub=dia, hora=hora, notas=NOTA_LS)
# ---------------- Inquérito Sombrio ----------------
d1 = open(N + "01_mascaras_de_chumbo.md", encoding="utf-8").read(); d2 = open(N + "02_operacao_prato.md", encoding="utf-8").read()
def longo(d, titulo_re):
    return {"yt_titulo": re.search(r"## 1\. TÍTULO\s*\n+\*\*(.+?)\*\*", d).group(1), "yt_desc": bloco(d, "DESCRIÇÃO (YouTube)"),
            "tags": re.search(r"\*\*Tags:\*\* (.+)", d).group(1).strip(), "comentario": re.search(r"\*\*Comentário fixado:\*\*\s*\n> (.+)", d).group(1).strip()}
add("inq-v01", "inquerito", "longo", 1, "O caso das máscaras de chumbo (10 min)", "Pronto", longo(d1, ""),
    notas="Versão no padrão de retenção (fotos de banco, efeitos sonoros, cortes rápidos). Trocar 'Casos Sem Resposta' por 'Inquérito Sombrio' no crédito e no cartão final antes de publicar.")
add("inq-v02", "inquerito", "longo", 2, "Operação Prato (10 min)", "Em produção", longo(d2, ""), notas="Roteiro, narração e cenas prontos. Falta renderizar no padrão de retenção, com fotos de banco.")
sl = open(N + "shorts_lote1.md", encoding="utf-8").read()
nomes = ["Máscaras de chumbo", "Operação Prato", "Noite Oficial dos OVNIs", "Varginha", "Disco de Ubatuba", "Ilha da Queimada Grande", "Fordlândia", "Meteorito Bendegó", "Luzia"]
assets = ["c8b0f917c6d32ac83d4fa989e1bd5355", "8a54cb9fd33660e9054b7a6cfb130d21", "692ae084a5e10af15e957ad57b6ba16e", "2e80c5b0e8300250ec3696c87a286248", "d8c19d2c1cfe55f2265a7d70223d83ef",
          "fd8dfd51bd99f951bd1d808a3dffd822", "ff54329678035c023af97e28be2a29ac", "84dacba5ee395778d7d01de3e478953f", "40f7a00b7e83d69f2231a616ac2f1053"]
for k, nome in enumerate(nomes, 1):
    i = sl.index(f"### s{k} ·"); j = sl.find("### s", i + 5); sec = sl[i: j if j > 0 else len(sl)]
    tit = re.search(r"\*\*Título:\*\* (.+)", sec).group(1).strip(); leg = re.search(r"\*\*Legenda[^*]*\*\* (.+)", sec).group(1).strip()
    l = {"yt_titulo": tit, "tiktok": leg, "reels": leg}
    if k == 3:
        l = {"yt_titulo": "A noite em que caças da FAB perseguiram 21 OVNIs 🛸 #shorts",
             "yt_desc": "19 de maio de 1986. Radares detectaram cerca de 21 objetos desconhecidos no céu de São Paulo, Rio de Janeiro e Goiás. Pilotos e controladores de voo viram as luzes, e a Força Aérea Brasileira mandou caças F-5 e Mirage para interceptá-las. Nenhum avião conseguiu alcançá-las.\n\nDias depois, o ministro da Aeronáutica admitiu que não havia explicação. Os documentos do caso hoje estão no Arquivo Nacional.\n\nO que você acha que eram aquelas luzes? Comenta aqui. 👇\nInscreva-se no Inquérito Sombrio para mais casos que nunca foram resolvidos.\n\n#shorts #ovni #noiteoficialdosovnis #ufo #misterio #casosreais #fab #ufologia #inqueritosombrio",
             "tiktok": "A Força Aérea mandou caças atrás de 21 OVNIs… e não conseguiu alcançar nenhum 🛸\n\n19 de maio de 1986, céu de SP, RJ e Goiás. Até o ministro da Aeronáutica admitiu que não havia explicação.\n\nO que eram aquelas luzes? 👇\n\n#ovni #misterio #ufo #noiteoficialdosovnis #casosreais",
             "reels": "19 de maio de 1986. Os radares do Brasil detectaram cerca de 21 objetos desconhecidos no céu de São Paulo, Rio de Janeiro e Goiás. 🛸\n\nPilotos viram. Controladores de voo viram. E a Força Aérea mandou caças F-5 e Mirage para interceptar as luzes.\n\nNenhum avião conseguiu alcançá-las.\n\nDias depois, o próprio ministro da Aeronáutica admitiu: não havia explicação. Os documentos ficaram guardados por décadas e hoje estão no Arquivo Nacional.\n\n👉 O que você acha que eram aquelas luzes? Comenta aqui.\n🔎 Siga @inqueritosombrio para mais casos que nunca foram resolvidos.\n\n#ovni #noiteoficialdosovnis #ufo #misterio #casosreais #forcaaereabrasileira #fab #ufologia #misteriosdobrasil #inqueritosombrio",
             "comentario": "Balões, fenômeno natural ou algo que a gente ainda não entende? 👇"}
    if k == 1:
        l["reels"] = "Em 1966, dois homens foram encontrados mortos no alto de um morro em Niterói. 🔎\n\nDe terno, de capa de chuva e com máscaras de chumbo cobrindo os olhos. No bolso, um bilhete: \"aguardar sinal, máscara\".\n\nNenhuma cápsula foi encontrada. O dinheiro sumiu. E a causa da morte? Indeterminada.\n\nQuase 60 anos depois, o caso nunca foi resolvido.\n\n👉 Que sinal você acha que eles esperavam? Comenta aqui.\n📁 O caso completo está no YouTube: link na bio.\n\n#misterio #casosreais #truecrime #casosnaoresolvidos #mascarasdechumbo #niteroi #misteriosdobrasil #ovni #inqueritosombrio"
    status, nota = ("Pronto", "Versão no padrão de retenção.") if k == 1 else ("Revisar", "Versão antiga, sem fotos de banco e efeitos sonoros: refazer no padrão de retenção." + (" Também tem textos encostando na legenda." if k in (5, 6, 8, 9) else ""))
    add(f"inq-s{k:02d}", "inquerito", "short", k, nome, status, l, asset=assets[k - 1], notas=nota + " Trocar a marca 'Casos Sem Resposta' por 'Inquérito Sombrio'.")
os.makedirs(S + "docs", exist_ok=True)
for d in docs: json.dump(d["data"], open(S + f"docs/{d['id']}.json", "w"), ensure_ascii=False)
print(len(docs), "documentos;", sum(len(d["data"]["legendas"]) for d in docs), "legendas")
for d in docs: print(d["id"], d["data"]["status"], d["data"]["nome"][:40], sorted(d["data"]["legendas"]))
