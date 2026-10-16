from comum_shorts import *
SAIDA = "s3_noite_oficial_dos_ovnis.mp4"
FINAL = "19 DE MAIO DE 1986"
CENAS = [
    ("na noite de dezenove", A("radar", n=21, legenda="19 DE MAIO DE 1986")),
    ("cerca de vinte e um", A("radar", n=21, legenda="21 OBJETOS?")),
    ("voando sobre sao paulo", T("brasil", pin=[-46.6, -23.5], nome="SÃO PAULO · RIO · GOIÁS", zoom=0.5)),
    ("pilotos viram", A("cacas", luzes=6)),
    ("e a forca aerea", A("cacas", luzes=5)),
    ("jatos f 5 e mirage", A("cacas", luzes=4)),
    ("segundo os relatos", A("cacas", luzes=7)),
    ("nenhum caca conseguiu", A("radar", n=21)),
    ("dias depois", A("jornal", tag="rec", titulo="“NÃO HÁ|EXPLICAÇÃO”")),
    ("por isso essa data", T("citacao", texto="A NOITE OFICIAL|DOS OVNIS")),
    ("os documentos ficaram", A("documento", tag="rec", titulo="FORÇA AÉREA BRASILEIRA", linhas=["19/05/1986", "Objetos não identificados"], carimbo="ARQUIVO NACIONAL", tc=1.2)),
    ("ate hoje ninguem sabe", A("cacas", luzes=8)),
]
