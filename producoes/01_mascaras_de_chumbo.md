# 01 — O caso das máscaras de chumbo (vídeo longo, 10 min)

**Arquivo final:** `mascaras_de_chumbo_10min.mp4` · 1920x1080 · 10:00 · só voz (pt-BR-AntonioNeural, -6%)
**Visual:** 100% animações próprias (`pipeline/anim/anim.html`). Sem fotos reais das vítimas, dos corpos ou dos documentos. Documentos e jornais aparecem como RECRIAÇÃO e cenas desenhadas como ILUSTRAÇÃO.

---

## 1. TÍTULO

**Encontrados mortos com máscaras de chumbo: o caso que a polícia nunca resolveu**

Alternativas para teste A/B:
- O bilhete mais misterioso do Brasil: "aguardar sinal, máscara"
- Máscaras de chumbo: o mistério de Niterói que ninguém explica até hoje

**Thumbnails:** `videos/v1_mascaras/thumb_a.jpg` ("NUNCA RESOLVIDO", máscara de chumbo) e `thumb_b.jpg` ("AGUARDAR SINAL", morro com a luz laranja).

## 2. GANCHO (0–35 s)

> "Agosto de 1966. Um jovem sobe um morro em Niterói para soltar pipa. Lá em cima, no meio do mato, ele vê dois homens deitados lado a lado. Os dois de terno. Os dois de capa de chuva. E os dois mortos. No rosto, cada um usava uma máscara feita de chumbo…"

## 3. ROTEIRO

Texto completo em [`videos/v1_mascaras/roteiro.txt`](videos/v1_mascaras/roteiro.txt) (1.289 palavras, 9:52 de narração).

**Capítulos do YouTube:** veja a seção 6 (Descrição).

## 4. CHECAGEM DE FATOS

| Fato no roteiro | Status | Fonte |
|---|---|---|
| Corpos achados na tarde de 20/ago/1966 no Morro do Vintém, Niterói, por um jovem que soltava pipa | ✔ | Wikipedia (Lead masks case); Mental Floss |
| Polícia e bombeiros só chegaram ao local no dia seguinte (terreno difícil) | ✔ | Wikipedia |
| Terno, capa de chuva, máscaras de chumbo; sem sinais de luta ou trauma | ✔ | Wikipedia; Skeptoid #398 |
| Pacote com garrafa de água vazia e duas toalhas | ✔ | Wikipedia; Skeptoid |
| Máscaras: folhas finas de chumbo recortadas à mão em formato de óculos, sem hastes | ✔ | Skeptoid |
| Manoel Pereira da Cruz (32) e Miguel José Viana (34), técnicos em eletrônica de Campos dos Goytacazes | ✔ | Skeptoid; Linha Direta |
| Vistos pela família em 17/ago; disseram que iam a São Paulo comprar carro e material | ✔ | Wikipedia (material); Linha Direta (carro e equipamento) |
| Levavam cerca de 3 milhões de cruzeiros; a maior parte sumiu | ⚠️ dito como "segundo os relatos da época" | Skeptoid |
| Chegaram de ônibus a Niterói por volta de 14h30 | ✔ | Wikipedia |
| Compraram capas de chuva (chovia) e uma garrafa de água num bar | ✔ | Wikipedia; Skeptoid |
| Atendente: Miguel muito nervoso, olhando o relógio; última vez vistos | ✔ | Wikipedia; Mental Floss |
| Bilhete: "16:30 estar no local determinado. 18:30 ingerir cápsulas, após efeito proteger metais aguardar sinal máscara", num caderno com anotações técnicas | ✔ | Wikipedia; Skeptoid |
| Nenhuma cápsula encontrada | ✔ | Skeptoid |
| Moradora relatou objeto redondo alaranjado subindo e descendo sobre o morro, sem fotos | ✔ (nome omitido de propósito) | Skeptoid; Draco |
| Autópsia tardia, corpos decompostos, IML sobrecarregado, toxicológico nunca feito, causa indeterminada | ✔ | Wikipedia; Skeptoid |
| Elcio Gomes: grupo de "espiritualistas científicos"; aparelho que explodiu meses antes | ✔ (atribuído ao depoimento dele) | Skeptoid |
| Relatos de uso de alucinógenos e da luz que cegaria | ✔ (dito como relatos, não fato) | Wikipedia; Skeptoid |
| Caso nunca solucionado; conhecido lá fora como "Lead masks case" | ✔ | todas |

**Não usado por falta de confirmação:** nome da testemunha da luz, "carona num jipe" até o morro, ligação com seitas específicas, exumação.

Fontes:
- https://en.wikipedia.org/wiki/Lead_masks_case
- https://skeptoid.com/episodes/4398
- https://www.mentalfloss.com/crime/bizarre-lead-mask-deaths-1966
- https://editoradraco.substack.com/p/o-enigma-das-mascaras-de-chumbo

## 5. DIVISÃO POR CENAS

São 120 planos (média de 5 s), definidos em [`videos/v1_mascaras/cenas.py`](videos/v1_mascaras/cenas.py).

| Capítulo | Visual principal |
|---|---|
| Introdução | Cartão "Agosto de 1966" → morro ao entardecer com pipa → silhuetas no alto do morro → máscaras → bilhete recriado |
| 1. O Morro do Vintém | Data datilografada → lanternas da polícia subindo → "local do achado" e "encontrado no local" em fichas → close das máscaras |
| 2. Quem eram eles | Fichas ilustradas (sem foto) → osciloscópio → mapa Campos → São Paulo (X) → Niterói → estrada à noite → relógio 14:30 |
| 3. As últimas horas | Rua de Niterói com chuva → bar → relógio até 16:30 |
| 4. O bilhete | Bilhete escrito linha a linha e depois linha por linha sublinhada → perguntas em cascata |
| 5. A luz no céu | Jornal recriado → luz laranja subindo e descendo sobre o morro |
| 6. A prova que se perdeu | Laudo recriado com carimbo "CAUSA: INDETERMINADA" |
| 7. Espiritualistas científicos | Ficha de Elcio Gomes → osciloscópio que explode → luz que cegaria |
| 8. As teorias | Cartões Contato / Experimento / Crime → perguntas que não se encaixam |
| Fechamento | Jornal → "Lead Masks Case" → bilhete → chamada para o próximo caso (Operação Prato) |

## 6. DESCRIÇÃO (YouTube)

```
Em agosto de 1966, dois técnicos em eletrônica foram encontrados mortos no alto do Morro do Vintém, em Niterói. Estavam de terno, capa de chuva e com máscaras de chumbo sobre os olhos. Ao lado, um bilhete: "16:30 estar no local determinado. 18:30 ingerir cápsulas, após efeito proteger metais aguardar sinal máscara."

Quase 60 anos depois, o caso das máscaras de chumbo continua sem solução. Neste vídeo, você vai conhecer os fatos, a luz vista no céu, a autópsia que nunca respondeu nada e as três teorias que tentam explicar o mistério.

CAPÍTULOS
0:00 Introdução
0:46 O Morro do Vintém
1:56 Quem eram eles
2:47 As últimas horas
3:32 O bilhete
4:35 A luz no céu
5:21 A prova que se perdeu
6:09 Os espiritualistas científicos
7:01 As teorias
8:49 Nunca solucionado

Fontes consultadas: reportagens da época citadas por Skeptoid (B. Dunning, 2014), Wikipedia (Lead masks case), Mental Floss.
Todas as imagens são ilustrações e recriações feitas pelo canal. Não há fotos reais das vítimas.

#misterio #casosreais #máscarasdechumbo #niteroi #casosemresposta
```

**Tags:** máscaras de chumbo, caso das máscaras de chumbo, morro do vintém, mistério brasileiro, casos não resolvidos, mistérios do brasil, niterói 1966, lead masks case, casos reais, ovni brasil

**Comentário fixado:**
> Na sua opinião: foi crime, um experimento que deu errado ou algo que a gente ainda não explica? 👇 E qual caso brasileiro você quer ver aqui?

## 7. CHECAGEM TÉCNICA

- Duração: 600,000 s ✔ · Volume: -14,0 LUFS ✔ · Pico: -1,4 dBFS ✔
- Folha de quadros revisada: sem telas pretas, etiquetas RECRIAÇÃO/ILUSTRAÇÃO em todas as cenas desenhadas ✔
