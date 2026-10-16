from comum_shorts import *
SAIDA = "s4_varginha.mp4"
FINAL = "VARGINHA, 1996"
CENAS = [
    ("vinte de janeiro de 1996", T("brasil", pin=[-45.43, -21.55], nome="VARGINHA, MG", zoom=0.9)),
    ("num dia de chuva forte", A("criatura", mostrar=0)),
    ("viram algo agachado", A("criatura")),
    ("elas contaram que era", A("criatura")),
    ("e que fugiram correndo", A("rua")),
    ("em poucos dias", A("jornal", tag="rec", titulo="O ET DE|VARGINHA")),
    ("surgiram boatos", A("estrada", chuva=1)),
    ("de caminhoes militares", A("estrada")),
    ("de um ser levado", A("documento", tag="rec", titulo="BOATOS", linhas=["Captura pelo Exército?", "Hospital?"])),
    ("a cidade virou", T("citacao", texto="A CAPITAL|DOS ETs")),
    ("mas um inquerito do exercito", A("documento", tag="rec", titulo="INQUÉRITO POLICIAL MILITAR", linhas=["Criatura capturada: não"])),
    ("e a figura vista", A("documento", tag="rec", titulo="INQUÉRITO POLICIAL MILITAR", linhas=["Criatura capturada: não", "Figura vista: morador da cidade"], carimbo="CONCLUSÃO", tc=1.2)),
    ("trinta anos depois", A("criatura")),
    ("um mal entendido", T("perguntas", frases=["Um mal-entendido?", "Ou algo nunca contado?"])),
]
