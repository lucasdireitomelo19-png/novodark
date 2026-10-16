from comum_shorts import *
SAIDA = "s6_ilha_da_queimada_grande.mp4"
FINAL = "ENTRADA PROIBIDA"
CENAS = [
    ("a cerca de trinta e cinco", T("brasil", pin=[-46.67, -24.49], nome="ILHA DA QUEIMADA GRANDE", zoom=1.0)),
    ("existe uma ilha", A("ilha", farol=1)),
    ("e a ilha da queimada", A("ilha", tarde=1, legenda="ILHA DAS COBRAS")),
    ("la vive uma serpente", A("cobra")),
    ("a jararaca ilhoa", A("cobra")),
    ("ela ficou isolada", A("ilha", tarde=1)),
    ("sem mamiferos para caçar", A("cobra")),
    ("e dizem que seu veneno", A("cobra")),
    ("hoje existem alguns milhares", T("citacao", texto="ALGUNS MILHARES|DE SERPENTES")),
    ("a internet costuma dizer", T("citacao", texto="5 COBRAS POR M²?", autor="exagero, segundo pesquisadores")),
    ("mesmo assim a visita", A("ilha", farol=1, legenda="VISITA PROIBIDA")),
    ("so entram pesquisadores", A("documento", tag="rec", titulo="AUTORIZAÇÃO", linhas=["Somente pesquisa científica"], carimbo="ACESSO RESTRITO", tc=1.0)),
    ("e nao e so para proteger", A("cobra")),
    ("a jararaca ilhoa esta ameacada", T("citacao", texto="AMEAÇADA|DE EXTINÇÃO")),
]
