# Código-fonte dos vídeos — @alecreator_motion

Uma pasta por vídeo. Leia o `CLAUDE-contexto.md` (estilo, ajustes pedidos, prompts e como renderizar).

- `index.html` = vídeo (canvas). `audio/*.py` = geradores da trilha/efeitos; `audio/trilha_final.mp3` = áudio final.
- `04-ui-app-pulsa-REMOTION/projeto-remotion` = único projeto Remotion (rode `npm install` e o `.bat`).
- `_fontes/` = instale no Windows antes de renderizar.
- `_ferramentas/` = render_h.js / snap_h.js (Node + Playwright + ffmpeg).
- Pastas com `_frames_src/`: rode `python preparar_frames.py` antes (recria as sequências de quadros dos clipes).
