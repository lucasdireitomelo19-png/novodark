from comum_shorts import *
# S17 · "A teoria do serial killer de SP" — versão de suspense focada no padrão que alimenta a teoria; a posição da polícia entra como virada.
# Footage Pixabay em todas as cenas (etiqueta IMAGEM ILUSTRATIVA). Sem corpos, sem nomes de vítimas, sem suspeitos.
SAIDA = "s17_teoria_sp.mp4"
FIM = 57.0
FINAL = "INQUÉRITO SOMBRIO"
WHOOSH = False
CIDADE = ("vento", -30)
def P(src, **k): return dict(src=src, tag="banco", fit=0, **k)
CENAS = [
    ("nove corpos", P("b_s16_saco_agua.mp4", ss=2, sat=0.0, zoom=(1.12, 1.22), texto="9 CORPOS", sfx=[("impacto", 0.05, -15)])),
    ("o mesmo jeito", P("b_s16_sacos.mp4", ss=1, sat=0.15, crop=(40, 300, 560, 780), zoom=(1.05, 1.15))),
    ("em pouco mais", P("b_s16_sp_predios.mp4", ss=3, sat=0.5, texto="5/9 → 13/10")),
    ("a internet ja", P("b_s16_celular.mp4", ss=6, sat=0.9, zoom=(1.0, 1.1), texto="“SERIAL KILLER?”")),
    ("desde o comeco", P("b_s16_sp_carro.mp4", ss=2, sat=0.55)),
    ("pessoas vem sendo", P("b_s16_sp_noite.mp4", ss=4, sat=0.5, ambiente=CIDADE)),
    ("amarradas", P("b_s16_sp_rua.mp4", ss=2, sat=0.45)),
    ("enroladas em sacos", P("b_s16_saco_agua.mp4", ss=6, sat=0.0, zoom=(1.3, 1.4))),
    ("uma no jabaquara", P("b_s16_sp_rua2.mp4", ss=3, sat=0.5, texto="JABAQUARA · 5/9")),
    ("outra numa ciclovia", P("b_s16_sp_rua.mp4", ss=10, sat=0.45, pan=(0.65, 0.5), zoom=(1.15, 1.25), texto="VIA PARQUE · 2/10")),
    ("outra na agua", P("b_s16_represa.mp4", ss=1, sat=0.6, texto="REPRESA DO RIACHO GRANDE · 13/10", ambiente=("agua", -26))),
    ("o padrao se repetiu", P("b_s16_celular.mp4", ss=14, sat=0.7, pan=(0.6, 0.5), zoom=(1.2, 1.3))),
    ("mas quando", dict(P("b_s17_farois.mp4", ss=2, sat=0.6), silencio=1)),
    ("a pista apontou", P("b_s16_beco_chuva.mp4", ss=1, sat=0.4, ambiente=("chuva", -26))),
    ("uma familia contou", P("b_s17_dirigindo.mp4", ss=3, sat=0.5)),
    ("para a policia", P("b_s16_policia_luzes.mp4", ss=1, sat=0.7, pan=(0.0, 0.38), zoom=(2.0, 2.1))),
    ("isso e caracteristica", dict(T("citacao", texto="“ISSO É CARACTERÍSTICA|DE TRIBUNAL DO CRIME”", tam=60, autor="DELEGADA DO DHPP, OUTUBRO DE 2026"), sfx=[("impacto", 0.1, -16)])),
    ("os julgamentos", P("b_s16_sp_noite.mp4", ss=12, sat=0.45, zoom=(1.1, 1.2))),
    ("ate agora", dict(P("b_s16_sp_rua2.mp4", ss=10, sat=0.45, pan=(0.3, 0.5), zoom=(1.1, 1.2)), texto="NENHUM PRESO")),
    ("entao me diz", P("b_s16_sp_predios.mp4", ss=18, sat=0.5, zoom=(1.0, 1.12))),
    ("ou um tribunal", P("b_s16_saco_agua.mp4", ss=4.5, sat=0.0, zoom=(1.1, 1.2))),
]
