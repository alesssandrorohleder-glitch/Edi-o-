# Código-fonte dos vídeos — @alecreator_motion

Uma pasta por vídeo. Leia o `CLAUDE-contexto.md` (estilo, ajustes pedidos, prompts e como renderizar).

- `index.html` = vídeo (canvas). `audio/*.py` = geradores da trilha/efeitos; `audio/trilha_final.mp3` = áudio final.
- `04-ui-app-pulsa-REMOTION/projeto-remotion` = único projeto Remotion (rode `npm install` e o `.bat`).
- `_fontes/` = instale no Windows antes de renderizar.
- `_ferramentas/` = render_h.js / snap_h.js (Node + Playwright + ffmpeg).
- `15-pet-shop-focinho/` = pet shop fictício (gerado nesta sessão; trilha em `audio/audio_focinho.py`, cortes `0,4,8,14,20,24,28,34`).
- `16-construtora-nido/` = versão portfólio (fictícia) do 14 Metrocasa, sem marca/fotos do cliente; `gerar_de_14.py` recria o index a partir do 14.
- `17-esmalteria-amora/` = versão portfólio (fictícia) do 13 Cereja, sem marca/filmagens do cliente; `gerar_de_13.py` recria o index a partir do 13.
- `18-cliente-gaia-tabacaria/` = CLIENTE Gaia Tabacaria: filmagens estabilizadas + cor uniformizada; render com `node render_gaia.js out/gaia_video` (ver CLAUDE.md).
- Pastas com `_frames_src/`: rode `python preparar_frames.py` antes (recria as sequências de quadros dos clipes).
