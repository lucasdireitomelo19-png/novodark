from comum_shorts import *
SAIDA = "s1_mascaras_de_chumbo.mp4"
FINAL = "AGUARDAR SINAL."
CENAS = [
    ("em 1966", A("morro", corpos=1, zoom=0.4, vel=0)),
    ("de terno de capa de chuva", A("morro", corpos=1, chuva=0.6, vel=2)),
    ("e com mascaras de chumbo", A("mascara", duas=1)),
    ("nao havia sinal de luta", A("documento", tag="rec", titulo="LOCAL DO ACHADO", linhas=["Sinais de luta: não", "Ferimentos: nenhum"])),
    ("mas no bolso de um deles", A("caderno", tag="rec")),
    ("dezesseis e trinta", A("bilhete", tag="rec", ate=1, rapido=1)),
    ("dezoito e trinta", A("bilhete", tag="rec", ate=2, rapido=1)),
    ("apos efeito", A("bilhete", tag="rec", ate=3, rapido=1)),
    ("aguardar sinal", A("bilhete", tag="rec", ate=5, rapido=1)),
    ("os dois eram tecnicos", A("ficha", nome="Manoel e Miguel", idade="32 e 34 anos", prof="Técnicos em eletrônica", cidade="Campos dos Goytacazes")),
    ("disseram a familia", A("mapa", sp=1, x=1, niteroi=1)),
    ("nenhuma capsula foi encontrada", A("teoria", icone="capsula", num="NÃO ENCONTRADO", titulo="NENHUMA CÁPSULA")),
    ("quase todo o dinheiro", A("dinheiro", texto="O DINHEIRO SUMIU")),
    ("e uma moradora", A("morro", luz=1, vel=3)),
    ("subindo e descendo", A("morro", luz=1, zoom=0.4, vel=0)),
    ("a autopsia nao descobriu", A("documento", tag="rec", titulo="LAUDO", linhas=["Toxicológico: não feito"], carimbo="INDETERMINADA", tc=1.0)),
    ("o caso nunca foi resolvido", T("citacao", texto="NUNCA|RESOLVIDO")),
    ("afinal que sinal", A("morro", luz=1, corpos=1, vel=2)),
]
