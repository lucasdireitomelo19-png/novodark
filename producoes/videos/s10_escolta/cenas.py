from comum_shorts import *
SAIDA = "s10_escolta.mp4"
FIM = 65.0
FINAL = "INQUÉRITO SOMBRIO"
CREDITO_ANIM = "Ilustração: Inquérito Sombrio"
B = dict(tag="banco", fit=0, noite=1)  # footage do Pixabay em tela cheia, virada em noite
CENAS = [
    ("cada ponto nesse radar", dict(A("escolta", tag="rec", de=-0.5, passo=0.02), zoom=(1.0, 1.12))),
    ("e naquela noite", dict(src="b_s10_caca_nuvens.mp4", ss=0.5, tag="banco", fit=0, sat=0.35)),
    ("19 de maio", T("data", l1="19 DE MAIO DE 1986", l2="22h50 · BASE AÉREA DE SANTA CRUZ (RJ)")),
    ("o capitao marcio", dict(src="b_s10_caca_b.mp4", ss=3.0, pan=(0.75, 0.5), **B)),
    ("decola de santa cruz", T("brasil", pin=[-43.69, -22.93], nome="SANTA CRUZ (RJ)", zoom=1.4)),
    ("a missao", A("radar", n=21, legenda="DESDE AS 20h")),
    ("ele ve uma luz", A("luz")),
    ("e de repente", A("luz", apaga=0.9)),
    ("entao o controle", dict(src="b_s10_lua.mp4", ss=4, tag="banco", fit=0, zoom=(1.2, 1.35))),
    ("numerosos trafegos", T("citacao", texto="“NUMEROSOS TRÁFEGOS|A SEIS HORAS|DA SUA AERONAVE”", fonte="MAQ", tam=70, autor="CONTROLE DE VOO · 22h59")),
    ("seis horas logo", dict(A("escolta", tag="rec", de=0.2, passo=0.1), texto="LOGO ATRÁS DELE")),
    ("treze contatos", dict(A("escolta", tag="rec", passo=0), texto="13 CONTATOS")),
    ("sete de um lado", A("escolta", tag="rec", passo=0, rotulos=1)),
    ("como uma escolta", dict(A("cacas", luzes=13), texto="ESCOLTA?")),
    ("o capitao faz uma curva", dict(src="b_s10_caca_c.mp4", ss=1.0, vel=1.3, glitch=1, **B)),
    ("e nao encontra nada", dict(src="b_s10_nuvens.mp4", ss=10, vel=2.0, **B)),
    ("nem no ceu", A("escolta", tag="rec", vazio=1)),
    ("quatro dias depois", T("data", l1="23 DE MAIO DE 1986", l2="COLETIVA DO MINISTRO DA AERONÁUTICA")),
    ("tecnicamente", T("citacao", texto="“TECNICAMENTE, DIRIA|AOS SENHORES QUE|NÃO TEMOS EXPLICAÇÃO”", tam=64, autor="BRIG. OCTÁVIO MOREIRA LIMA")),
    ("em 2009", A("documento", tag="rec", titulo="RELATÓRIO · COMDA", linhas=["Data: 2 de junho de 1986", "Assunto: objetos não", "identificados em 19/05/1986", "Divulgado em 2009"], carimbo="ARQUIVO NACIONAL", tc=2.2)),
    ("eram solidos", T("citacao", texto="“SÓLIDOS”|“REFLETEM, DE CERTA|FORMA, INTELIGÊNCIA”", tam=66, autor="RELATÓRIO OFICIAL DA FAB")),
    ("se fosse voce", A("escolta", tag="rec", passo=0)),
]
