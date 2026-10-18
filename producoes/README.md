# Casos Sem Resposta · produções

Canal dark de mistérios e casos reais brasileiros. Vídeos longos de 10:00 (1920x1080, só voz), montados automaticamente com **animações próprias** (morro à noite, máscaras, bilhetes, mapas, relógios, fichas, jornais recriados). Não usamos fotos reais das pessoas envolvidas.

O pipeline foi adaptado do canal *Lado Sombrio do Universo* (repo `edittest`): mesma narração, mesma montagem por âncoras de texto, mesmas legendas palavra a palavra.

## Vídeos produzidos

| # | Caso | Documento de produção | Arquivo final |
|---|---|---|---|
| 01 | As máscaras de chumbo (Niterói, 1966) | [01_mascaras_de_chumbo.md](01_mascaras_de_chumbo.md) | `mascaras_de_chumbo_10min.mp4` |
| 02 | Operação Prato (Colares, 1977) | [02_operacao_prato.md](02_operacao_prato.md) | `operacao_prato_10min.mp4` |
| S1–S9 | Shorts de temas variados | [shorts_lote1.md](shorts_lote1.md) | `videos/s*/s*.mp4` |
| S10 | A escolta de 13 objetos (FAB, 1986) | [videos/s10_escolta/roteiro.md](videos/s10_escolta/roteiro.md) | `videos/s10_escolta/s10_escolta.mp4` |
| S11 | Mach 15: o alvo do Mirage (FAB, 1986) | [videos/s11_mach15/roteiro.md](videos/s11_mach15/roteiro.md) | `videos/s11_mach15/s11_mach15.mp4` |
| S12 | Percy Fawcett e a cidade Z (1925) | [videos/s12_fawcett/roteiro.md](videos/s12_fawcett/roteiro.md) | `videos/s12_fawcett/s12_fawcett.mp4` |
| S13 | Ilha da Trindade: as fotos de 1958 | [videos/s13_trindade/roteiro.md](videos/s13_trindade/roteiro.md) | `videos/s13_trindade/s13_trindade.mp4` |
| S14 | Pedra do Ingá (PB) | [videos/s14_inga/roteiro.md](videos/s14_inga/roteiro.md) | `videos/s14_inga/s14_inga.mp4` |

Os MP4 não ficam no git (são grandes). Eles são regerados pelo processo abaixo.

## Como produzir um vídeo novo

```bash
cd producoes/pipeline
pip install edge-tts                       # voz pt-BR-AntonioNeural (grátis)

# 1. Roteiro (~1.300 palavras para 10 min)
mkdir -p ../videos/v2_tema && $EDITOR ../videos/v2_tema/roteiro.txt

# 2. Narração (ajusta a velocidade sozinha; deixe ~8 s no fim para o texto final)
SSL_CERT_FILE=/root/.ccr/ca-bundle.crt python3 narrar.py ../videos/v2_tema 592.5 -6

# 3. Cenas: copie videos/v1_mascaras/cenas.py e troque as âncoras (trechos da narração)
CHECK=1 python3 motor_h.py ../videos/v2_tema     # confere tempos de cada plano
WORKERS=4 python3 motor_h.py ../videos/v2_tema   # gera o MP4 de 600,0 s

# 4. Thumbnails A/B (configuradas em ../videos/v2_tema/thumbs.json)
NODE_PATH=$(npm root -g) node anim/thumb.js ../videos/v2_tema
```

### Shorts (1080x1920, 61 s)

O mesmo motor faz os Shorts. O `cenas.py` começa com `from comum_shorts import *` (liga `VERTICAL`, `FIM = 61.0` e os atalhos `A()` e `T()`). Todas as animações se adaptam sozinhas ao formato vertical.

```bash
SSL_CERT_FILE=/root/.ccr/ca-bundle.crt python3 narrar.py ../videos/s10_tema 59.4 0
WORKERS=4 python3 motor_h.py ../videos/s10_tema
```

### Narração frase a frase e footage do Pixabay (desde o s10)

Padrão do canal: voz Antonio com `narrar_antonio.py` (grátis). Ele gera cada frase separada, corta o silêncio das pontas e desenha as pausas pela pontuação; `vel`/`tom` por bloco no `blocos.json` dão variação (gancho mais lento, perseguição mais rápida). O `narrar_eleven.py` lê o mesmo `blocos.json`, para quando houver créditos do ElevenLabs.

```bash
SSL_CERT_FILE=/root/.ccr/ca-bundle.crt ../../.venv/bin/python narrar_antonio.py ../videos/s11_mach15 10 -2
```

Chaves ficam em `.env` na raiz do repositório (ignorado pelo git): `ELEVENLABS_API_KEY`, `PIXABAY_API_KEY`. Pacotes Python ficam em `.venv` (`edge-tts`, `faster-whisper`, `numpy`, `scipy`).

```bash
set -a; . ../../.env; set +a
# narração por blocos (blocos.json), com cache por bloco e tempos palavra a palavra; trocas.json vira números na legenda
../../.venv/bin/python narrar_eleven.py ../videos/s10_escolta 1.15
# footage
python3 pixabay.py videos "fighter jet" 8
python3 pixabay.py baixar_video 284488 b_s10_caca_nuvens.mp4
# render e capas verticais A/B
WORKERS=4 ../../.venv/bin/python motor_h.py ../videos/s10_escolta
NODE_PATH=$(npm root -g) node anim/capa_short.js ../videos/s10_escolta
```

Novidades do motor: opção `noite=1` (footage de dia vira noite), legenda quebra no fim de frase. Novas cenas: `escolta`, `luz`, `alvo` (radar do Mirage), `velocidade` (contador/barras), `rota` (Rio–SP), `fogueiras`, `foto_disco` (foto P&B recriada), `itacoatiara` (rocha gravada, `luz`/`sol`/`ceu`); `bilhete` aceita `linhas` e `pronto`. O cache dos planos agora percebe animação refeita; ainda assim, ao mudar `anim.html`, apague `videos/<video>/tmp/anim_*`.

O cache de animações (`videos/*/tmp`) usa os parâmetros da cena como chave. Se você mudar o desenho em `anim.html`, apague a pasta `tmp` do vídeo antes de renderizar de novo.

## Animações disponíveis (`pipeline/anim/anim.html`)

| Cena | Parâmetros | Uso |
|---|---|---|
| `morro` | `tarde`, `luz`, `corpos`, `pipa`, `chuva`, `lanternas`, `zoom`, `vel` | Morro à noite ou ao entardecer, luz no céu, silhuetas |
| `mascara` | `duas` | Máscara(s) de chumbo em close |
| `bilhete` | `ate`, `todos`, `foco`, `rapido` | Bilhete manuscrito aparecendo linha a linha |
| `caderno` | — | Página de anotações técnicas |
| `mapa` | `sp`, `x`, `niteroi`, `legenda` | Rota no mapa do estado do Rio |
| `relogio` | `de`, `ate`, `legenda` | Relógio andando entre dois horários |
| `data` | `l1`, `l2` | Cartão datilografado (data e local) |
| `capitulo`, `citacao`, `perguntas` | textos | Cartões de capítulo, frase e perguntas em cascata |
| `ficha` | `nome`, `idade`, `prof`, `cidade` | Ficha policial ilustrada (sem foto real) |
| `documento` | `titulo`, `linhas`, `carimbo`, `tc` | Laudo ou relatório com carimbo |
| `jornal` | `titulo` | Capa de jornal recriada |
| `teoria` | `icone` (`ovni`, `capsula`, `crime`), `num`, `titulo` | Cartões de teoria |
| `rua`, `estrada`, `eletronica`, `dinheiro`, `final` | variados | Ambientação |
| `brasil` | `pin=[lon, lat]`, `nome`, `zoom`, `legenda` | Mapa do Brasil com marcador |
| `radar` | `n`, `legenda` | Tela de radar com alvos |
| `cacas` | `luzes` | Caças cruzando o céu com luzes |
| `vila` | `feixe`, `fogueira` | Vila ribeirinha à noite, feixe de luz descendo |
| `ilha`, `cobra` | `farol`, `tarde`, `legenda` | Ilha no mar, serpente (ilustração) |
| `fordlandia` | `ruina`, `noite`, `legenda` | Cidade industrial na floresta |
| `meteoro`, `pedra` | `fogo`, `texto` | Bola de fogo; meteorito em close |
| `cranio`, `museu` | `scan`, `rachado`, `fogo`, `texto`, `legenda` | Crânio (ilustração); prédio em chamas |
| `praia`, `fragmentos` | `explosao`, `fragmentos`, `texto` | Praia à noite com explosão; pedaços de metal |
| `criatura` | `mostrar` | Vulto agachado com olhos vermelhos, na chuva |
| `fotos` | `n`, `seed`, `legenda` | Fotos recriadas espalhadas na mesa |

Para um caso novo, acrescente cenas ao `anim.html` no mesmo padrão `draw(t, dur, p)` e registre no objeto `CENAS`.

Fontes: Montserrat (OFL), Caveat (OFL) e Special Elite (Apache 2.0).
