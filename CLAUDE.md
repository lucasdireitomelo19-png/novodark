# Instruções do projeto · Inquérito Sombrio

Canal dark de mistérios e casos reais (Brasil e mundo). Produção em `producoes/` (veja `producoes/README.md`).

## Regra obrigatória: todo vídeo pronto vai para a Central dos Canais

Central dos Canais (página com banco de dados dos dois canais): https://claude.ai/artifact/UZ3YFHzLpBjiJj3Mskzj1q

Sempre que um vídeo ficar pronto (render final conferido: duração, -14 LUFS, folha de quadros revisada), **no mesmo turno**:

1. **Anexar o vídeo**
   - Shorts: comprimir para menos de 15 MB e enviar como asset da Central:
     `ffmpeg -i entrada.mp4 -c:v libx264 -preset slow -b:v 1650k -maxrate 2200k -bufsize 3300k -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart saida.mp4`
     Depois: Artifact `publish` com `url` da Central, `asset: true` e `file_paths`. Guardar o `id` em `video_asset` e `/_blob/<id>` em `video_url`.
   - Vídeos longos passam do limite de arquivo: deixar `video_link` vazio e avisar o dono para colar o link (Drive ou YouTube não listado). Mandar a versão leve pelo chat.
2. **Escrever as legendas das três plataformas** (campo `legendas`), só com fatos checados do roteiro:
   - `yt_titulo` (até 100 caracteres; nos Shorts, terminar com `#shorts`), `yt_desc` (2 parágrafos contando o caso, uma pergunta, "Inscreva-se…", hashtags com `#shorts` primeiro), `tags` (separadas por vírgula).
   - `tiktok`: curta, gancho na primeira frase, pergunta, 3 a 5 hashtags.
   - `reels`: conta a história em poucas linhas, termina com "📌 Salva…" ou "👉 comenta" e "🔎 Siga @inqueritosombrio", 5 a 7 hashtags.
   - `comentario`: pergunta para fixar.
   - Vídeo longo: também `tiktok` e `reels` de divulgação, apontando para o vídeo completo no YouTube.
3. **Gravar no banco** (ArtifactData, coleção `videos`):
   - id: `inq-sNN` (Short) ou `inq-vNN` (longo); no Lado Sombrio do Universo, `lado-NN`.
   - campos: `canal` (`inquerito` | `lado`), `tipo` (`short` | `longo`), `ordem`, `nome`, `status` (`Roteiro`, `Em produção`, `Revisar`, `Pronto`, `Agendado`, `Publicado`), `data_pub`, `hora`, `plataformas` ({yt, tt, ig}), `legendas`, `notas`, `video_asset`, `video_url`, `video_link`, `atualizado`.
   - Vídeo pronto entra como `Pronto`. Ao refazer um vídeo existente, atualizar o mesmo documento (`update` com `if_version`) e trocar o asset.
4. Avisar o dono no fim: o que entrou na Central e o que falta (por exemplo, link de vídeo longo).

## Padrão de produção
- Retenção: fotos de banco (`pipeline/banco.py`, `pipeline/pexels.py`), efeitos sonoros e trilha (`pipeline/sfx.py`), cortes de 2,7 a 3,5 s, legenda que salta.
- Nunca inventar fatos; etiquetas honestas (ILUSTRAÇÃO, RECRIAÇÃO, IMAGEM ILUSTRATIVA).
- Marca: "Inquérito Sombrio" (@inqueritosombrio), logo e capa em `producoes/marca/`.
