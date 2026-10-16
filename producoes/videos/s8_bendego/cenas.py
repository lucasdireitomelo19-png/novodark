from comum_shorts import *
SAIDA = "s8_meteorito_bendego.mp4"
FINAL = "BENDEGÓ"
CENAS = [
    ("em 1784", T("brasil", pin=[-39.33, -10.44], nome="MONTE SANTO, BA", zoom=0.9)),
    ("escura pesada demais", A("pedra")),
    ("era um meteorito", A("meteoro")),
    ("o maior ja encontrado", A("pedra", texto="O MAIOR DO BRASIL")),
    ("ele recebeu o nome", T("citacao", texto="BENDEGÓ")),
    ("e pesa mais de cinco", A("pedra", texto="MAIS DE 5 TONELADAS")),
    ("quase todo feito de ferro", A("pedra", texto="QUASE TODO FERRO")),
    ("tentaram levar a pedra", A("estrada")),
    ("e o meteorito caiu", A("pedra")),
    ("so em 1888", A("documento", tag="rec", titulo="1888", linhas=["Ordem do imperador", "Dom Pedro II"])),
    ("em 2018 o museu nacional", A("museu", fogo=1, legenda="SETEMBRO DE 2018")),
    ("mas no meio das cinzas", A("pedra", fogo=1)),
    ("intacto", A("pedra", fogo=1, texto="INTACTO")),
    ("uma pedra que atravessou", A("meteoro")),
]
