# Canais dark · regras de produção

Pipeline e instruções de uso: `producoes/README.md`. Entregas: página "Central dos Canais" (claude.ai/artifact/UZ3YFHzLpBjiJj3Mskzj1q, coleção `videos` do banco) e "Inquérito Sombrio · Entregas" (claude.ai/artifact/YaDQyFQxwNBrj6TBXS38D7).

## Imagem real sempre (regra do dono do canal, vale para TODO vídeo)
- **90% do tempo de tela é VÍDEO real (footage em movimento).** Foto (mesmo real) e animação somadas ficam em no máximo 10% do vídeo. Foto com Ken Burns não conta como vídeo.
- A linguagem visual principal é **imagem real**: vídeo real (Pixabay) e foto real (Wikimedia Commons, acervos em domínio público). Animação é exceção.
- Se a narração cita um objeto, lugar ou máquina, **mostre um vídeo ou foto real dele**: falou de F-5 ou Mirage, aparece um caça de verdade (foto do F-5/Mirage da FAB no Commons + footage de caça no Pixabay); falou de radar, aparece uma tela de radar real; falou de navio, um navio.
- Ordem de preferência: footage real literal → footage real contextual → foto/documento real (arquivo, Commons) → mapa → animação. Animação só para o que não dá para filmar (rota, número, reconstrução) e nunca como plano principal de um trecho.
- Antes de montar, fazer o plano visual com busca real (várias palavras-chave por trecho, nota de relevância ≥ 8, rejeitar imagem bonita mas sem relação).
- Footage genérico leva a etiqueta IMAGEM ILUSTRATIVA; foto real do caso/arquivo leva IMAGEM REAL. Nunca apresentar footage genérico como registro do caso.

## Outras regras do canal
- Shorts com no máximo 61 s (130–145 palavras). Voz: Antonio (`pipeline/narrar_antonio.py`).
- Nunca inventar fatos; casos em andamento seguem a posição oficial e citam a data dos dados.
- Sem whoosh automático em todo corte (`WHOOSH = False`), ambiente e silêncio antes das revelações.
