from comum_shorts import *
# S16 · Corpos em sacos em SP (caso em andamento, out/2026) — padrão novo: footage real em todas as cenas.
# Cuidado editorial: nenhuma imagem de corpo, nenhum nome de vítima, nenhum suspeito; o vídeo não afirma que existe serial killer.
SAIDA = "s16_sacos_sp.mp4"
FIM = 59.5
FINAL = "INQUÉRITO SOMBRIO"
WHOOSH = False
CIDADE = ("vento", -30)
def P(src, **k): return dict(src=src, tag="banco", fit=0, **k)
CENAS = [
    ("a internet diz", P("b_s16_celular.mp4", ss=6, sat=0.9, zoom=(1.0, 1.08), texto="“SERIAL KILLER EM SP?”")),
    ("a policia diz", P("b_s16_policia_luzes.mp4", ss=1, sat=0.7, pan=(0.0, 0.38), zoom=(2.0, 2.1))),
    ("e os corpos", P("b_s16_saco_agua.mp4", ss=2, sat=0.0, zoom=(1.1, 1.2), sfx=[("impacto", 0.2, -18)])),
    ("entre o comeco", P("b_s16_sp_predios.mp4", ss=3, sat=0.6, texto="SET → OUT 2026")),
    ("pelo menos nove", P("b_s16_sp_carro.mp4", ss=2, sat=0.55, texto="9 MORTES OFICIAIS (ATÉ 15/10)")),
    ("quase sempre", P("b_s16_sp_rua.mp4", ss=2, sat=0.5, ambiente=CIDADE)),
    ("enroladas em sacos", P("b_s16_sacos.mp4", ss=1, sat=0.15, crop=(40, 300, 560, 780), zoom=(1.05, 1.15))),
    ("deixadas na rua", P("b_s16_sp_rua2.mp4", ss=3, sat=0.5)),
    ("ate numa represa", P("b_s16_represa.mp4", ss=1, sat=0.6, ambiente=("agua", -26))),
    ("nas redes", P("b_s16_celular.mp4", ss=12, sat=0.6, pan=(0.6, 0.5), zoom=(1.2, 1.3))),
    ("mas a secretaria", dict(T("citacao", texto="“NÃO HÁ INDÍCIOS|DE QUE OS CRIMES|SEJAM DA MESMA PESSOA”", tam=58, autor="SSP-SP, OUTUBRO DE 2026"), silencio=1)),
    ("e que o saco", P("b_s16_saco_agua.mp4", ss=7, sat=0.0, zoom=(1.3, 1.4), texto="O SACO NÃO LIGA OS CASOS")),
    ("a principal linha", P("b_s16_sp_rua2.mp4", ss=9, sat=0.45, pan=(0.3, 0.5), zoom=(1.1, 1.2))),
    ("o chamado tribunal", dict(P("b_s16_beco_chuva.mp4", ss=1, sat=0.4, ambiente=("chuva", -26)), texto="“TRIBUNAL DO CRIME”")),
    ("os julgamentos", P("b_s16_sp_noite.mp4", ss=4, sat=0.5, zoom=(1.1, 1.2))),
    ("em um dos casos", P("b_s16_sp_rua.mp4", ss=10, sat=0.5, pan=(0.65, 0.5), zoom=(1.15, 1.25))),
    ("ninguem foi apontado", dict(P("b_s16_sp_noite.mp4", ss=12, sat=0.5), silencio=1)),
    ("e a pergunta", P("b_s16_sp_predios.mp4", ss=18, sat=0.5, zoom=(1.0, 1.12))),
    ("ou a mesma", P("b_s16_sp_noite.mp4", ss=8, sat=0.45, pan=(0.6, 0.5), zoom=(1.2, 1.35))),
]
