from comum_shorts import *
SAIDA = "s14_inga.mp4"
FIM = 67.0
FINAL = "INQUÉRITO SOMBRIO"
CREDITO_ANIM = "Ilustração: Inquérito Sombrio"
REAL = dict(src="w_inga_1.jpg", tag="real", fit=0)  # foto real do sítio (Wikimedia Commons, CC BY 2.0)
CENAS = [
    ("essas marcas", dict(REAL, pan=(0.5, 0.5), zoom=(1.45, 1.6))),
    ("e ate hoje", dict(A("itacoatiara", tag="ilus", luz=1), zoom=(1.15, 1.25))),
    ("esta e a pedra", dict(REAL, zoom=(1.0, 1.1))),
    ("no agreste", T("brasil", pin=[-35.6, -7.28], nome="INGÁ (PB)", zoom=1.4)),
    ("um paredao", dict(REAL, pan=(0.3, 0.5), zoom=(1.2, 1.35))),
    ("coberto de simbolos", A("itacoatiara", tag="ilus", luz=1)),
    ("nao da para datar", dict(src="b_s14_caatinga.mp4", ss=1, tag="banco", fit=0, sat=0.7)),
    ("pesquisadores estimam", dict(T("citacao", texto="5 A 7 MIL ANOS", tam=110, autor="ESTIMATIVA PELOS SÍTIOS DA REGIÃO"))),
    ("mais antigas", dict(src="b_s14_piramides.mp4", ss=2, tag="banco", fit=0, sat=0.6, texto="PIRÂMIDES DE GIZÉ: ~4.500 ANOS")),
    ("e quem fez", T("perguntas", frases=["FENÍCIOS?", "EXTRATERRESTRES?"])),
    ("para os arqueologos", dict(REAL, pan=(0.6, 0.5), zoom=(1.25, 1.4))),
    ("povos que viviam", dict(A("itacoatiara", tag="ilus"), texto="ANTES DOS TUPIS E CARIRIS")),
    ("ha quem veja", A("itacoatiara", tag="ilus", sol=1)),
    ("outros enxergam", A("itacoatiara", tag="ilus", ceu=1)),
    ("em 1944", A("documento", tag="rec", titulo="PATRIMÔNIO NACIONAL", linhas=["Itacoatiaras do Rio Ingá", "Ingá · Paraíba", "Tombamento: 1944"], carimbo="TOMBADO", tc=1.6)),
    ("as teorias", dict(src="b_s14_estrelas.mp4", ss=4, tag="banco", fit=0)),
    ("mas a mensagem", dict(REAL, pan=(0.45, 0.55), zoom=(1.35, 1.5))),
    ("e se essas marcas", dict(A("itacoatiara", tag="ilus", luz=1), zoom=(1.15, 1.25))),
]
