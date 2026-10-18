from comum_shorts import *
# S10 v2 · A escolta de 13 objetos — refeito com IMAGEM REAL (regra do canal: animação só para reconstrução).
# Real: fotos da FAB no Commons (Base Aérea de Santa Cruz, F-5 decolando, F-5E no hangar), cabine noturna (NASA via Pixabay),
# caças em formação e céu noturno (Pixabay). Recriação só no radar com os 13 contatos e na luz vista pelo piloto.
SAIDA = "s10_escolta.mp4"
FIM = 50.5
FINAL = "INQUÉRITO SOMBRIO"
WHOOSH = False
CREDITO_ANIM = "Recriação: Inquérito Sombrio"
NOITE = ("vento", -30)
def R(src, **k): return dict(src=src, tag="real", **k)
def P(src, **k): return dict(src=src, tag="banco", fit=0, **k)
CENAS = [
    ("cada ponto", dict(A("escolta", tag="rec", de=-0.5, passo=0.02), zoom=(1.0, 1.1))),
    ("naquela noite", P("b_ceu_lua_nuvens.mp4", ss=3, sat=0.5, zoom=(1.1, 1.2), ambiente=NOITE)),
    ("eles estavam", P("b_jatos_formacao.mp4", ss=0.5, sat=0.35, noite=1)),
    ("19 de maio", R("w_santa_cruz.jpg", fit=1, zoom=(1.0, 1.08), texto="19 DE MAIO DE 1986")),
    ("o capitao marcio", R("w_santa_cruz.jpg", pan=(0.35, 0.5), zoom=(1.3, 1.42), texto="BASE AÉREA DE SANTA CRUZ (RJ)", sat=0.0)),
    ("num caca f-5", R("w_f5e_fab2.jpg", pan=(0.5, 0.55), zoom=(1.1, 1.22), texto="NORTHROP F-5E · FAB")),
    ("para cacar luzes", R("w_f5_decolando.jpg", pan=(0.45, 0.62), zoom=(1.6, 1.75), sat=0.5)),
    ("ele ve uma luz", A("luz", tag="rec")),
    ("e de repente", A("luz", tag="rec", apaga=1.0)),
    ("numerosos trafegos", P("b_cockpit_noite.mp4", ss=10, sat=0.6, zoom=(1.05, 1.15), texto="“NUMEROSOS TRÁFEGOS A SEIS HORAS”")),
    ("logo atras dele", A("escolta", tag="rec", de=0.0, passo=0.1)),
    ("sete de um lado", A("escolta", tag="rec", passo=0, rotulos=1)),
    ("o capitao faz", P("b_jatos_formacao.mp4", ss=4, sat=0.35, noite=1, pan=(0.6, 0.4), zoom=(1.2, 1.3))),
    ("e nao encontra", dict(P("b_ceu_lua_nuvens.mp4", ss=14, sat=0.4, zoom=(1.0, 1.08)), silencio=1)),
    ("quatro dias depois", R("w_santa_cruz.jpg", pan=(0.75, 0.5), zoom=(1.25, 1.35), sat=0.0, texto="23 DE MAIO DE 1986")),
    ("tecnicamente", T("citacao", texto="“TECNICAMENTE, DIRIA|AOS SENHORES QUE|NÃO TEMOS EXPLICAÇÃO”", tam=58, autor="MINISTRO DA AERONÁUTICA, 1986")),
    ("se fosse voce", R("w_f5_decolando.jpg", pan=(0.4, 0.62), zoom=(1.9, 2.05), sat=0.4)),
    ("teria feito", P("b_ceu_lua_nuvens.mp4", ss=20, sat=0.45, zoom=(1.15, 1.25))),
]
