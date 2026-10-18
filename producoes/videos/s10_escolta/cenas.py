from comum_shorts import *
# S10 v3 · A escolta de 13 objetos — regra "90% vídeo": todo trecho em footage real (Mixkit, Pixabay, NASA, Commons);
# animação só no radar com os 7 + 6 contatos e no instante em que a luz se apaga (~4,5 s de 50 s).
SAIDA = "s10_escolta.mp4"
FIM = 50.5
FINAL = "INQUÉRITO SOMBRIO"
WHOOSH = False
CREDITO_ANIM = "Recriação: Inquérito Sombrio"
NOITE = ("vento", -30)
import os
F5 = "b_c_f5_formacao.mp4" if os.path.exists(os.path.join(os.path.dirname(__file__), "../../pipeline/src/b_c_f5_formacao.mp4")) else None
def P(src, **k): return dict(src=src, tag="banco", fit=0, **k)
CENAS = [
    ("cada ponto", P("b_mk_radar_antena.mp4", ss=0.5, sat=0.35, noite=1, crop=(640, 30, 400, 690), zoom=(1.0, 1.1), texto="OBJETOS NÃO IDENTIFICADOS", ambiente=NOITE)),
    ("naquela noite", P("b_mk_nuvens_lua.mp4", ss=2, sat=0.5)),
    ("eles estavam", P("b_mk_jato_48865.mp4", ss=2, sat=0.4, noite=1)),
    ("19 de maio", P("b_mk_aeroporto_noite.mp4", ss=1, sat=0.5, texto="19 DE MAIO DE 1986")),
    ("o capitao marcio", P("b_mk_decolagem_noite.mp4", ss=2, sat=0.5, texto="SANTA CRUZ (RJ) · 22h50")),
    ("num caca f-5", P(F5, ss=3, sat=0.5, texto="F-5", noite=1) if F5 else P("b_mk_jato_46953.mp4", ss=2, sat=0.45, noite=1)),
    ("para cacar luzes", P("b_mk_jato_48865.mp4", ss=12, sat=0.4, noite=1)),
    ("ele ve uma luz", P("b_ceu_lua_nuvens.mp4", ss=6, sat=0.6, zoom=(1.15, 1.25))),
    ("e de repente", A("luz", tag="rec", apaga=0.5)),
    ("numerosos trafegos", P("b_cockpit_noite.mp4", ss=66, sat=0.6, zoom=(1.05, 1.15), texto="“NUMEROSOS TRÁFEGOS A SEIS HORAS”")),
    ("logo atras dele", P("b_mk_jato_48863.mp4", ss=1, sat=0.4, noite=1)),
    ("sete de um lado", A("escolta", tag="rec", passo=0, rotulos=1)),
    ("o capitao faz", P("b_mk_jato_48864.mp4", ss=5.5, sat=0.4, noite=1)),
    ("e nao encontra", dict(P("b_mk_nuvens_lua.mp4", ss=8, sat=0.45), silencio=1)),
    ("quatro dias depois", P("b_mk_aeroporto_noite.mp4", ss=6, sat=0.45, pan=(0.7, 0.5), zoom=(1.15, 1.25), texto="23 DE MAIO DE 1986")),
    ("tecnicamente", P("b_mk_decolagem_noite.mp4", ss=7.5, sat=0.4, zoom=(1.1, 1.2), texto="“TECNICAMENTE, NÃO TEMOS EXPLICAÇÃO” · MINISTRO DA AERONÁUTICA")),
    ("se fosse voce", P("b_cockpit_noite.mp4", ss=60, sat=0.5, zoom=(1.1, 1.2))),
    ("teria feito", P("b_mk_jato_48864.mp4", ss=2, sat=0.4, noite=1)),
]
