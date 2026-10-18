from comum_shorts import *
SAIDA = "s12_fawcett.mp4"
FIM = 67.5
FINAL = "INQUÉRITO SOMBRIO"
CREDITO_ANIM = "Ilustração: Inquérito Sombrio"
B = dict(tag="banco", fit=0)
CARTA = ["Dead Horse Camp,", "29 de maio de 1925", "", "\"You need have no", "fear of any failure...\""]
CENAS = [
    ("em 1925", dict(A("bilhete", tag="rec", linhas=CARTA, pronto=1, foco=3), zoom=(1.12, 1.2))),
    ("foi a ultima noticia", dict(src="b_s12_selva_vert.mp4", ss=2, sat=0.6, **B)),
    ("o coronel britanico", T("ficha", nome="PERCY FAWCETT", idade="57 ANOS", prof="CORONEL E EXPLORADOR", cidade="DESAPARECIDO EM 1925")),
    ("estava no mato grosso", T("brasil", pin=[-53.2, -12.5], nome="ALTO XINGU (MT)", zoom=1.2)),
    ("atras de uma cidade", dict(src="b_s12_mapas.mp4", ss=1, sat=0.6, **B)),
    ("ele a chamava", T("citacao", texto="Z", tam=300)),
    ("com ele apenas", T("perguntas", frases=["Jack Fawcett, o filho", "Raleigh Rimell, o amigo"])),
    ("num ponto que", T("data", l1="29 DE MAIO DE 1925", l2="ACAMPAMENTO DO CAVALO MORTO")),
    ("fawcett mandou os guias", dict(src="b_s12_rio_vert.mp4", ss=4, sat=0.55, **B)),
    ("nunca mais sairam", dict(src="b_s12_selva_tarde.mp4", ss=6, sat=0.45, fit=0, zoom=(1.0, 1.25), escurecer=1)),
    ("expedicoes foram", dict(src="b_s12_chuva.mp4", ss=2, sat=0.5, **B)),
    ("decadas depois", T("citacao", texto="O ANEL DA FAMÍLIA", autor="ACHADO DÉCADAS DEPOIS")),
    ("ossos atribuidos", A("documento", tag="rec", titulo="ANÁLISE DE OSSADA", linhas=["Ossos atribuídos a", "Percy Fawcett", "", "Resultado:"], carimbo="NÃO ERAM DELE", tc=2.6)),
    ("os kalapalo contam", A("fogueiras", tag="ilus")),
    ("depois de cinco dias", A("fogueiras", tag="ilus", apagar=1.2)),
    ("e a cidade z", dict(src="b_s12_selva_vert.mp4", ss=20, sat=0.6, **B)),
    ("pesquisas no alto xingu", T("brasil", pin=[-53.2, -12.5], nome="KUHIKUGU · ALTO XINGU", zoom=1.4)),
    ("ligadas por estradas", dict(src="b_s12_rio_vert.mp4", ss=16, sat=0.55, **B, texto="DEZENAS DE MILHARES DE PESSOAS")),
    ("talvez fawcett", dict(src="b_s12_fogueira.mp4", ss=2, sat=0.6, **B)),
    ("so nao voltou", A("fogueiras", tag="ilus", apagar=0.4)),
]
