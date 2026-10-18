from comum_shorts import *
# S15 · Canudos — padrão novo: imagem real em todas as cenas (fotos de arquivo de 1897, fotos atuais do açude e footage Pixabay).
# Nenhuma animação além do cartão final. Corte seco (sem whoosh automático), vento de ambiente, silêncio antes das revelações.
SAIDA = "s15_canudos.mp4"
FIM = 58.5
FINAL = "INQUÉRITO SOMBRIO"
WHOOSH = False
VENTO = ("vento", -26)
def R(src, **k): return dict(src=src, tag="real", **k)           # foto real (arquivo ou atual)
def P(src, **k): return dict(src=src, tag="banco", fit=0, **k)    # footage Pixabay (ilustrativo)
CENAS = [
    ("existe uma cidade", R("w_canudos_ruinas_3.jpg", pan=(0.55, 0.5), zoom=(1.0, 1.12), ambiente=VENTO)),
    ("em 1897", R("w_canudos_vila.jpg", fit=1, zoom=(1.0, 1.08), texto="1897", sat=0.0)),
    ("um arraial", R("w_canudos_planta.jpg", fit=1, zoom=(1.0, 1.1), texto="ARRAIAL DE CANUDOS · PLANTA DE 1897")),
    ("guiados pelo", R("w_canudos_vila.jpg", pan=(0.62, 0.55), zoom=(1.25, 1.35), texto="ANTÔNIO CONSELHEIRO", sat=0.0)),
    ("a republica", R("w_canudos_batalhao.jpg", fit=1, zoom=(1.0, 1.08))),
    ("tres expedicoes", R("w_canudos_batalhao.jpg", pan=(0.35, 0.5), zoom=(1.15, 1.25), texto="3 EXPEDIÇÕES DERROTADAS")),
    ("a quarta", R("w_canudos_batalhao.jpg", pan=(0.7, 0.5), zoom=(1.2, 1.32), texto="~10 MIL SOLDADOS")),
    ("em outubro", R("w_canudos_igreja_1897.jpg", pan=(0.5, 0.35), zoom=(1.0, 1.15), texto="OUTUBRO DE 1897", sfx=[("impacto", 0.9, -16)])),
    ("as estimativas", P("b_s15_fogo.mp4", ss=3, sat=0.5, texto="15 A 30 MIL MORTOS (ESTIMATIVAS)", ambiente=("fogo", -24))),
    ("euclides da cunha", P("b_s15_livro.mp4", ss=0.5, sat=0.6, texto="EUCLIDES DA CUNHA · OS SERTÕES")),
    ("canudos nao se rendeu", dict(R("w_canudos_igreja_1897.jpg", pan=(0.5, 0.75), zoom=(1.3, 1.4)), silencio=1, texto="“CANUDOS NÃO SE RENDEU”", sfx=[("impacto", 0.1, -14)])),
    ("os sobreviventes", R("w_canudos_prisioneiros.jpg", fit=1, zoom=(1.0, 1.1), ambiente=VENTO)),
    ("mas no fim", P("b_s15_barragem.mp4", ss=1, sat=0.55, texto="AÇUDE DE COCOROBÓ · DNOCS")),
    ("e a nova canudos", P("b_s15_represa.mp4", ss=2, sat=0.6, pan=(0.25, 0.5), zoom=(1.05, 1.15), ambiente=("agua", -22))),
    ("nos anos noventa", R("w_cocorobo_barragem.jpg", zoom=(1.0, 1.12), texto="ANOS 1990: A SECA", ambiente=VENTO)),
    ("e as ruinas voltaram", dict(R("w_canudos_ruinas_2.jpg", pan=(0.3, 0.5), zoom=(1.1, 1.2)), silencio=1)),
    ("as paredes da igreja", R("w_canudos_ruinas_4.jpg", pan=(0.45, 0.5), zoom=(1.05, 1.15))),
    ("o cemiterio", R("w_canudos_ruinas_5.jpg", pan=(0.6, 0.6), zoom=(1.1, 1.2))),
    ("desde entao", P("b_s15_lama.mp4", ss=2, sat=0.7, ambiente=VENTO)),
    ("canudos volta", R("w_canudos_seca.jpg", zoom=(1.0, 1.12))),
    ("como se a cidade", R("w_canudos_ruinas_3.jpg", pan=(0.45, 0.5), zoom=(1.12, 1.25))),
]
