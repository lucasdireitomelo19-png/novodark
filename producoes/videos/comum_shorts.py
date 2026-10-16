# Configuração comum dos Shorts (1080x1920, 61 s, só voz). Cada cenas.py faz: from comum_shorts import *
VERTICAL = True
FIM = 61.0
MAX_PLANO = 7.0
CREDITO_ANIM = "Ilustração: Casos Sem Resposta"
def A(_cena, tag="ilus", **p): return dict(src="anim:" + _cena, p=p, tag=tag)
def T(_cena, **p): return A(_cena, tag=None, **p)
