from comum_shorts import *
SAIDA = "s13_trindade.mp4"
FIM = 69.5
FINAL = "INQUÉRITO SOMBRIO"
CREDITO_ANIM = "Ilustração: Inquérito Sombrio"
PB = dict(tag="banco", fit=0, sat=0.0)  # footage em preto e branco: cara de arquivo de 1958
CENAS = [
    ("em 1958", dict(A("foto_disco", tag="rec", k=0.45, pronto=1), zoom=(1.1, 1.18))),
    ("o que apareceu", dict(src="b_s13_navio_nuvens.mp4", ss=5, **PB)),
    ("16 de janeiro", T("data", l1="16 DE JANEIRO DE 1958", l2="12h20 · NAVIO ALMIRANTE SALDANHA")),
    ("o navio almirante", dict(src="b_s13_navio.mp4", ss=2, **PB)),
    ("esta perto da ilha", dict(T("brasil", pin=[-29.3, -20.5], nome="TRINDADE", zoom=0.2), inteiro=1)),
    ("numa missao", dict(src="b_s13_mar.mp4", ss=5, **PB)),
    ("marinheiros apontam", dict(src="b_s13_navio_nuvens.mp4", ss=30, **PB)),
    ("o fotografo civil", T("ficha", nome="ALMIRO BARAÚNA", idade="", prof="FOTÓGRAFO CIVIL", cidade="A BORDO DO SALDANHA")),
    ("segundo ele", dict(A("foto_disco", tag="rec", k=0.15, flash=1, num="Foto 1 · recriação"), texto="6 FOTOS · 14 SEGUNDOS")),
    ("nelas aparece", dict(A("foto_disco", tag="rec", k=0.5, flash=1, num="Foto 2 · recriação"))),
    ("passando sobre o pico", dict(A("foto_disco", tag="rec", k=0.8, flash=1, num="Foto 3 · recriação"))),
    ("em fevereiro", dict(src="b_s13_grafica.mp4", ss=1, **PB)),
    ("e o ministro", A("jornal", tag="rec", titulo="DISCO VOADOR|SOBRE A TRINDADE")),
    ("chega a falar", T("citacao", texto="UM SEGREDO QUE|NÃO PODE SER|EXPLICADO", autor="MINISTRO DA MARINHA, 1958")),
    ("mas existe o outro lado", T("citacao", texto="O OUTRO LADO")),
    ("barauna tinha experiencia", A("fotos", tag="rec", n=4, legenda="Montagens · recriação")),
    ("anos antes", dict(A("foto_disco", tag="rec", sem=1, num="Foto falsa desmontada · recriação"))),
    ("em 2010", dict(src="b_s11_tv.mp4", tag="banco", fit=0, sat=0.0, zoom=(1.15, 1.3), texto="2010 · “FOI FARSA”")),
    ("barauna morreu", A("ficha", tag="ilus", nome="ALMIRO BARAÚNA", idade="", prof="FOTÓGRAFO", cidade="NUNCA CONFIRMOU A FARSA")),
    ("dezenas de testemunhas", dict(src="b_s13_mar.mp4", ss=20, **PB)),
    ("uma camera", dict(A("foto_disco", tag="rec", k=0.5))),
    ("duas versoes", T("perguntas", frases=["AS FOTOS", "OU O AMIGO?"])),
    ("em quem voce", dict(A("foto_disco", tag="rec", k=0.45), zoom=(1.1, 1.18))),
]
