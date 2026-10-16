from comum_shorts import *
SAIDA = "s5_disco_de_ubatuba.mp4"
FINAL = "UBATUBA, 1957"
CENAS = [
    ("em setembro de 1957", A("jornal", tag="rec", titulo="A CARTA|MISTERIOSA")),
    ("dentro do envelope", A("fragmentos", texto="PEDAÇOS DE METAL")),
    ("o remetente dizia", T("brasil", pin=[-45.07, -23.43], nome="UBATUBA, SP", zoom=0.9)),
    ("quando viu um disco", A("praia", explosao=2.5)),
    ("segundo ele o objeto", A("praia", explosao=0.3)),
    ("espalhando fragmentos", A("praia", fragmentos=1)),
    ("os pedacos foram levados", A("fragmentos")),
    ("era magnesio", A("fragmentos", texto="MAGNÉSIO")),
    ("para alguns ufologos", T("teoria", icone="ovni", num="PARA UNS", titulo="PROVA FÍSICA")),
    ("para outros investigadores", T("teoria", icone="crime", num="PARA OUTROS", titulo="FARSA")),
    ("e tem um detalhe", A("documento", tag="rec", titulo="REMETENTE", linhas=["Nome: ?", "Endereço: ?"], carimbo="NUNCA IDENTIFICADO", tc=1.2)),
    ("ate hoje os fragmentos", A("praia", fragmentos=1)),
]
