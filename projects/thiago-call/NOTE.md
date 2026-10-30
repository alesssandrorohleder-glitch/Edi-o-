# NOTE: Thiago Idehara, convite para call (25 s)

**Arquivos:** `renders/thiago-call.mp4` (master, CRF 18) e `renders/thiago-call-instagram.mp4` (CRF 23, faststart, ~38 MB). O código está em `remotion-video/src/ThiagoCall/`.

## A ideia
É uma calculadora com impressora em cima de uma mesa de nogueira. Toda frase do filme sai impressa na fita. A conta da parcela cresce para 60 meses de "parcela + juros", trava em `Total …… ?` e a fita é rasgada. O pedaço novo diz "Existe outra conta. Ela fecha diferente." e imprime o retrato do Thiago. A pergunta que fica no ar ("quanto dá a conta inteira?") é o assunto da call. Isso combina com os posts dele, que comparam Entrada / Taxa / Prazo / Parcela / Valor total.

## O que é real e o que é ilustrativo
- **Real:** o @, a foto de perfil (release "Fotos Thiago") e a bio "Especialista em consórcios: imóveis, veículos, investimentos".
- **Ilustrativo:** "60 meses" é um prazo de exemplo, não há nenhum valor em reais e os itens de custo (juros, IOF, seguro, tarifa de cadastro) são genéricos. A calculadora, a mesa e as texturas foram feitas em código. A trilha e os efeitos foram sintetizados (`scripts/thiago_sound.py`) a partir dos tempos das linhas. Só o whoosh do rasgo veio do repositório.
- **O retrato** é a foto real convertida em impressão térmica (pontilhado), sem gerar nenhuma pessoa.

## Portões (números do `look.py`, render final)
- **G0:** PASS. 25,00 s, 1080x1920, 30 fps, áudio presente.
- **G2:** PASS. Nenhuma sequência com mais de 3 frames parados.
- **G3:** PASS. Hold final de 0,00 s: o filme termina em movimento (a luz respira e o grão está vivo); a última mudança da câmera é no frame 718. Plano único, sem corte, por isso a parte do CTA não foi calculada pelo script; pelo storyboard, o CTA vai do frame 570 ao 750 (24 %).
- **Áudio:** −14,2 LUFS, true peak −1,0 dBFS. O script marca "silêncio digital 13,85–14,13 s". **É de propósito:** é a pausa antes do `?`.
- **G1 e G4 (no olho, pela folha de contato):** todo frame tem um herói só, a fita. Em escala de 1,2, as frases ficam com cerca de 77 px (0,04 H). No streaming dos 60 meses o texto fica pequeno e borrado de propósito, para mostrar velocidade e não para ser lido.
- **G5:** o `lint.mjs` não rodou, porque precisa de um Chrome que esta sessão não consegue abrir. Fiz a auditoria à mão: não há nome no canto, contador, barra de progresso, frase alinhada à esquerda nem digitação letra por letra. Todo texto sai impresso na fita.
- **Movimento:** 2,0/255, abaixo da faixa de vídeos feitos por humanos (4,4–9,8). É um plano único e calmo, e a energia só sobe no streaming.

## Descrição de cada frame da folha de contato
0,8 s: papel em branco, com a primeira linha saindo da fenda. 2,3 s: "Todo mundo faz a conta da parcela." 3,9 s e 5,5 s: entra "Quase ninguém faz a conta inteira." 7 s e 8,6 s: os itens + juros, + IOF… 10,1 s: a câmera recua e a fita começa a borrar. 11,7 s e 13,3 s: a fita corre a tela inteira e as teclas da calculadora aparecem pequenas. 14,8 s: "Total ……" com o `?` grande. 16,4 s: close no `?`, logo antes do rasgo. 18 s: a fita rasgada com "Existe outra conta." 19,5 s: "Eu faço essa conta com você." 21 s e 22,6 s: o retrato sai impresso. 24,2 s: o recibo inteiro, com "Me chama no direct." e @thiagoidehara_invest ✓.

## O que eu ainda melhoraria
- **O primeiro segundo é papel quase vazio.** No feed, o gancho poderia começar já com "Parcela … cabe no bolso ✓" no meio da tela.
- **O chamado final** poderia usar o WhatsApp da bio (14 99747-4699) em vez do direct, se for esse o canal que ele prefere.
- **Uma narração** (Kokoro pt-BR) dobraria a retenção para quem assiste com som.
