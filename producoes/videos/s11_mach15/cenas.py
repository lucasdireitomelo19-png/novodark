from comum_shorts import *
SAIDA = "s11_mach15.mp4"
FIM = 63.0
FINAL = "INQUÉRITO SOMBRIO"
CREDITO_ANIM = "Ilustração: Inquérito Sombrio"
B = dict(tag="banco", fit=0, noite=1)
CENAS = [
    ("18 mil quilometros", T("velocidade", ate=18375, inicio=0.55)),
    ("foi o que um piloto", dict(src="b_s10_caca_nuvens.mp4", ss=2.0, tag="banco", fit=0, sat=0.35)),
    ("nessa velocidade", A("rota", tag="sim")),
    ("19 de maio", T("data", l1="19 DE MAIO DE 1986", l2="~23h · BASE AÉREA DE ANÁPOLIS (GO)")),
    ("o capitao armindo", dict(src="b_s10_caca_b.mp4", ss=5.0, pan=(0.75, 0.5), **B)),
    ("decola de anapolis", T("brasil", pin=[-48.95, -16.33], nome="ANÁPOLIS (GO)", zoom=1.3)),
    ("o radar de bordo", A("alvo", tag="rec", fase="zig")),
    ("o alvo faz zigue", A("alvo", tag="rec", fase="zig", legenda="ZIGUE-ZAGUE")),
    ("mas la fora", dict(src="b_s10_lua.mp4", ss=8, tag="banco", fit=0, zoom=(1.2, 1.35), texto="SEM CONTATO VISUAL")),
    ("quando ele chega perto", A("alvo", tag="rec", fase="foge", tf=1.0)),
    ("e some da tela", A("alvo", tag="rec", fase="vazio", legenda="CONTATO PERDIDO")),
    ("pelos calculos", dict(src="b_s11_jato_vert.mp4", ss=1, tag="banco", fit=0, noite=1, vel=1.4)),
    ("15 vezes", T("velocidade", modo="barras")),
    ("anos depois", dict(src="b_s11_tv.mp4", tag="banco", fit=0, zoom=(1.15, 1.3), texto="TV GLOBO · 1993")),
    ("se existe aviao", T("citacao", texto="“SE EXISTE AVIÃO|QUE POSSA DESENVOLVER|ESSA VELOCIDADE,|EU DESCONHEÇO”", tam=60, autor="CAP. ARMINDO VIRIATO")),
    ("ate o relatorio", A("documento", tag="rec", titulo="RELATÓRIO · COMDA", linhas=["Data: 2 de junho de 1986", "Acelerações súbitas", "Curvas de 90 graus", "Divulgado em 2009"], carimbo="ARQUIVO NACIONAL", tc=2.2)),
    ("entao me diz", dict(A("alvo", tag="rec", fase="zig"), texto="O QUE VOA ASSIM?")),
]
