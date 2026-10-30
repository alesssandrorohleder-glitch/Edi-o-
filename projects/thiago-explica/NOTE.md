# NOTE: "Como funciona o consórcio" (40 s, narrado)

**Arquivos:** `renders/thiago-explica-instagram.mp4` (CRF 23) e `renders/thiago-explica.mp4` (master). O código está em `remotion-video/src/ThiagoExplica/`.

## A ideia
Uma roda de 12 esferas (o grupo) em volta de um pote (o fundo comum). É um diagrama só, que se transforma do começo ao fim:
1. as parcelas enchem o pote;
2. uma luz escolhe quem recebe a carta de crédito;
3. aparecem o sorteio e o lance;
4. "juros" leva um risco por cima;
5. a roda inteira fica verde (todos contemplados);
6. a roda se fecha em volta da foto do Thiago.

## Real e ilustrativo
- **Real:** a foto (com o espaço acima da cabeça completado com IA, LaMa), o @ e os fatos gerais de consórcio (parcela, fundo comum, sorteio e lance, sem juros com taxa de administração, todos contemplados até o fim do grupo).
- **Ilustrativo:** o grupo de 12 pessoas e o nível do pote. Não há valores nem prazos.
- **Narração:** Kokoro pt-BR (voz pm_alex), sintetizada e não é a voz do Thiago. Por isso fala dele na terceira pessoa ("Chama o Thiago no direct"). Conferida com o Whisper, que transcreveu as 9 frases iguais ao roteiro.

## Portões (`look.py`)
- **G0, G2 e G3:** PASS. Hold final de 1,20 s.
- **Áudio:** −14,0 LUFS, pico em −1,5 dBTP. A música abaixa 8 dB sob a voz (medido pelo `mix.py`).
- **G1 e G4 (no olho):** as legendas têm 84 px. Um herói por frame: a roda.
- **G5:** auditoria manual, sem elementos de tela.
- **Movimento:** baixo pela régua do `look.py`, porque o fundo é claro e liso e os objetos são pequenos em relação ao quadro.

## O que eu ainda melhoraria
- **Voz:** uma voz real, do próprio Thiago ou de um locutor, deixaria o vídeo mais pessoal do que a voz sintética.
