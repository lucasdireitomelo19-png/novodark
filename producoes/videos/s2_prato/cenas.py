from comum_shorts import *
SAIDA = "s2_operacao_prato.mp4"
FINAL = "OPERAÇÃO PRATO"
CENAS = [
    ("em 1977", A("vila")),
    ("uma pequena ilha no para", T("brasil", pin=[-48.23, -0.94], nome="COLARES, PA", zoom=0.8)),
    ("eles diziam que luzes", A("vila", feixe=1)),
    ("que deixavam marcas", A("vila", feixe=1)),
    ("que sugavam as forcas", A("vila", feixe=1, fogueira=1)),
    ("o povo deu um nome", T("citacao", texto="“CHUPA-CHUPA”", autor="como os moradores chamavam as luzes")),
    ("familias passavam a noite", A("vila", fogueira=1)),
    ("o caso ficou tao grave", A("radar", n=6, legenda="FORÇA AÉREA BRASILEIRA")),
    ("era a operacao prato", A("ficha", nome="Uyrangê Hollanda", idade="Capitão", prof="Força Aérea Brasileira", cidade="Operação Prato, 1977")),
    ("durante meses", A("documento", tag="rec", titulo="OPERAÇÃO PRATO", linhas=["Relatórios", "Desenhos", "Fotografias"], carimbo="CONFIDENCIAL", tc=1.5)),
    ("o relatorio oficial concluiu", A("documento", tag="rec", titulo="RELATÓRIO FINAL", linhas=["Seres de outro planeta:", "sem provas"])),
    ("mas vinte anos depois", A("vila", feixe=1)),
    ("hollanda contou", T("citacao", texto="“OBJETOS QUE|NÃO SABIA EXPLICAR”", autor="Hollanda, em entrevista (1997)")),
    ("poucos meses depois", T("citacao", texto="POUCOS MESES|DEPOIS...")),
    ("o que realmente aconteceu", A("vila", feixe=1)),
]
