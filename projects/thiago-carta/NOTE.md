# NOTE: "A hora do lance" (25 s)

**Arquivos:** `renders/thiago-lance-instagram.mp4` (CRF 23, ~22 MB) e `renders/thiago-lance.mp4` (master, CRF 18). O código está em `remotion-video/src/ThiagoLance/` e o som em `scripts/thiago_lance_sound.py`.

## A ideia
Envelopes de cotas na mesa de nogueira da série. Um carimbo espera a hora certa. No sorteio ele ameaça descer e volta; depois do lance, escrito à mão, ele bate e marca CONTEMPLADA. O cartão do Thiago sai de dentro do envelope com "Qual é a sua hora? Eu te mostro numa call."

## Real e ilustrativo
- **Real:** a foto (com os cantos completados por IA, como no vídeo 1), o @ e o tema (o envelope "carta contemplada" e os posts dele).
- **Ilustrativo:** os números das cotas e a bolinha 27. Não há valores, porcentagens nem prazos.

## Portões (`look.py`)
- **G0, G2 e G3:** PASS. Hold final de 0,93 s.
- **Áudio:** −14,0 LUFS, pico em −1,4 dBTP.
- **Silêncio digital** entre 14,4 e 15,7 s: é de propósito. É a pausa em que só o relógio toca antes do carimbo.
- **G1 e G4 (no olho):** um herói por frame (etiqueta, bolinha, caneta, carimbo, cartão). O texto das etiquetas tem cerca de 77 px.
- **G5:** auditoria manual, porque o `lint.mjs` precisa de um Chrome que esta sessão não abre. Não há elementos de tela: todo texto está num objeto.
- **Movimento:** 3,2/255, abaixo da faixa de vídeos feitos por humanos. É um plano calmo e contínuo.

## O que eu ainda melhoraria
- **Etiqueta vazia:** a etiqueta da cota 0521 aparece vazia por uns 0,3 s antes de a caneta entrar.
- **Final:** o carimbo CONTEMPLADA fica cortado na borda de baixo. Dá para recuar a câmera um pouco para ele aparecer junto com o cartão.
