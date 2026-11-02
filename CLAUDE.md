# CLAUDE.md — Edi-o-

## Preferências de trabalho
- Sempre que possível, otimize para gastar menos tokens: respostas curtas, sem leituras ou passos desnecessários.

## Templates de vídeo
Cada vídeo do portfólio @alecreator_motion fica em `src/templates/<NN-nome>/` e serve de template.
Ferramentas de render compartilhadas em `src/templates/_ferramentas/`, fontes em `src/templates/_fontes/`.
Índice rápido: `src/templates/README.md`.


## ⚠️ Importante: tecnologia de cada vídeo
- **Só o vídeo 04 (Pulsa) é Remotion** (React/TSX, `brand.ts`, renderiza com `npx remotion render`).
- **Todos os outros (01–03, 05–14) são HTML + canvas 2D**, renderizados quadro a quadro:
  - `index.html` expõe `window.draw(t)` (determinístico, t em segundos) e `window.DUR`.
  - `_ferramentas/render_h.js` abre o HTML no Chromium (Playwright), chama `draw(f/30)` para cada frame,
    gera JPEG e manda para o ffmpeg (libx264, crf 18, 30fps), uma cena por arquivo → concat → mux com o áudio.
  - A trilha e os efeitos sonoros são **gerados por código** (Python + numpy/scipy) em `audio/*.py`.
    O resultado final de cada vídeo está em `audio/trilha_final.mp3`.
- Para migrar para Remotion: cada `sN(t)` vira uma `<Sequence>`/composição; o `t` vira `frame/fps`;
  as cores e textos do topo do arquivo vão para o `brand.ts`. A lógica de animação (easings, tempos) pode ser copiada.

## Como renderizar um vídeo HTML
```
cd <pasta-do-video>
python preparar_frames.py          # só se a pasta tiver _frames_src (recria as sequências JPG dos clipes)
python -m http.server 8765         # em outro terminal
set BASEURL=http://localhost:8765/
node ../_ferramentas/render_h.js index.html out/video 0,4,8,...   # tempos de corte das cenas
```
- Fontes: instale as fontes de `_fontes/` no Windows antes (o canvas usa as fontes do sistema).
- `snap_h.js index.html 2.5 7.0` gera prints de quadros para conferir layout.
- Vídeos com imagens embutidas em base64 (01–10) abrem direto via `file://`.

## Preferências gerais do Ale (valem para todos os vídeos)
- Reels 9:16, 1080x1920, 30fps. Área segura: nada importante a <250px do topo e <350px do rodapé. Texto ≥ 40px.
- **Sem rótulos tipo "Estilo 01" no topo.** Sem letras miúdas no topo da tela.
- **Música**: animada e sincronizada; cortes caindo na batida. Sem "duas frequências" (sem detune nem acordes embolados).
  As trilhas sintetizadas por código foram o ponto fraco — o melhor resultado é usar música real (Suno/biblioteca do
  Instagram) e entregar também uma versão **só com efeitos**.
- **Efeitos sonoros** em níveis: suaves para textos pequenos, mais fortes só para frases grandes/impactos.
  Nunca sobrepostos (mínimo ~0,45s entre efeitos), nada exagerado.
- **Recortes** limpos: sem sombra/halo cinza, sem partes faltando. Conferir cantos e base das peças.
- **Sem filtros estranhos** nas fotos. Quando parecer "cara de IA": tirar saturação de laranja/ciano, levantar o preto,
  suavizar realces, sombras frias/luzes quentes, leve blur (0,5px) + grão fino + vinheta.
- **Logos de clientes: nunca alterar.** No máximo adicionar elementos em volta (ex.: cerejinha em cima do "I").
- Portfólio fictício termina com "Essa marca não existe. Mas o seu … pode ficar assim." + serviços + "Me chama no direct" + @alecreator_motion.
  Vídeo de cliente real NÃO tem essa frase.
- Movimento: muito motion quando pedido (whip pans, máscaras, texto atrás do produto, partículas), mas transições
  fluidas (máscara/empurrão suave), não cortes secos com glitch.

## Vídeos

### 01 — Kinetic type "Grão Norte" (café) — `portfolio_estilo01_kinetic` / `motion_v2/v3`
- Tipografia cinética; preto/creme/laranja. Ajustes pedidos: música no ritmo, remover rótulos do topo,
  consertar faixa "SÓ HOJE / FRETE GRÁTIS" e o "30%", adicionar efeitos sonoros nas entradas/saídas.

### 02 — Tech "NOVYX" (fintech futurista) — `portfolio_tech_novyx`
- Fundo escuro, neon, UI de cartão e gráficos, glow.

### 03 — Luxo "VÉRA" — `portfolio_luxo_vera_final` / `_produto`
- Preto/dourado/creme, serifa geométrica elegante (TeX Gyre Adventor/Pagella). `index.html` = versão final com a foto
  do produto do Ale (`vera_bottle.png`); `v3b.html` e `v3l.html` são versões anteriores.
- Ajustes: letras ruins e efeitos exagerados → refazer com nome VÉRA e fonte geométrica; música "duas frequências" →
  trilha house limpa e mais animada; cortes na batida.

### 04 — UI animada app "Pulsa" (REMOTION) — `PortfolioUI_pulsa_com_som`
- Verde-limão #B8F34A, `brand.ts`, cenas de tela de celular (saldo, pix, notificação, sucesso).
- Ajustes: notificação abaixo da câmera (dynamic island), cabeçalho some, % arredondado com `Math.floor(pct+0.05)`;
  hooks antes de early return (erro React #310).

### 05 — Explicativo "Lavo" (lavanderia por app) — `portfolio_explicativo_lavo`
- Personagem/ilustração flat; passo a passo (agenda → coleta → volta limpinha). Ajuste: mancha marrom no rosto do boneco.

### 06 — Hamburgueria "Chapa Real" — `portfolio_varejo_chapa_real`
- Amarelo/vermelho/preto, burger montando em camadas (recortes reais), preço riscado, contagem regressiva, CTA forte.
- Ajustes: usar fotos reais (burger, batata, Coca lata) com recorte preciso — copo/lata com base elíptica traçada
  ponto a ponto. Aviso: marca de terceiros (Coca-Cola) não pode em cliente real.

### 07 — Institucional "Vértice" (arquitetura/construção) — `portfolio_institucional_vertice`
- Planta desenhada em linha, cômodos, tipografia limpa.

### 08 — Pizzaria "Forno 900" — `portfolio_pizzaria_forno900`
- Estética de pizzaria (vermelho/creme/verde manjericão), pizza girando, ingredientes caindo.

### 09 — Sushi "Maré" — `portfolio_sushi_mare_motion_v3` (final = `index.html`, versão v10)
- Branco/coral/preto, recortes de nigiri/uramaki/hot roll com texto atrás da peça, whip pans, partículas, samba-house.
- Ajustes: "simples demais / cara de cardápio" → mais motion; filtro estranho nas fotos → só denoise+lanczos+unsharp leve;
  "HOT ROLL" coberto pela foto → título abaixo dos rolls; halo/sombra nos recortes → erodir borda + inpaint;
  preço em cada sushi (18,90 / 24,90 / 26,90 / 29,90 / combinado 30 peças 89,90).
- `v8s.html` (Umi) e `v9m.html` (Maré cardápio) = versões anteriores.

### 10 — Logo reveal (bloom, ATLAS, volt, órbita) — `portfolio_logo_reveal`
- 4 logos fictícios com animação e sonic-logo próprio cada; CTA "Esses logos não existem…".

### 11 — Tênis "ZEFYR ZF-1 Phantom" — (final v7)
- Editorial: cinza-papel/preto, verde-limão só em detalhe, tipografia grande alinhada à margem.
- Ajustes: sobreposição no seg. 10 + "cara de IA" → tirar glitch/RGB split/speed lines/HUD; mais fluido (empurrões
  verticais, frame blending 24→30fps); recorte do tênis (sombra no chão traçada à mão); congelar a queda no quadro
  limpo do impacto (antes de deformar); gancho do vidro quebrando no início; vídeo macro no lugar de cenas estáticas;
  sem letras miúdas no topo. Trilha funk-phonk 128bpm sincronizada (cortes a cada 3,75s).

### 12 — Imobiliário "VERANO Residence" — `portfolio_imobiliario_verano_v5_techno`
- Navy/creme/dourado, serifa Lora, planta desenhada em linha, mapa com rotas, ícones de lazer, preço "A partir de R$ 1,2 mi".
- Ajustes: trocar takes (sala, varanda, piscina rasante) — tirar o 1º take da piscina (rápido demais);
  **tirar cara de IA** com grade (ver `grade.sh`); música: piano ficou "péssima" → **techno clean** aprovado.

### 13 — CLIENTE: Esmalteria Cereja (Caraíva + Pinheiros) — `cereja_esmalteria_motion_v3`
- Estética da loja: vermelho cereja/vinho, verde de bananeira, luz âmbar de luminária de palha, mosaico vermelho.
- Fontes: serifa grossa (Noto Serif JP Black) + itálico Lora + Latin Modern Dunhill (fina) + Poppins (cena Pinheiros, igual ao post deles).
- Roteiro: "Quando a beleza pede CEREJA no topo" → PAUSA só sua → logo com luminárias → experiência → cores (leque) →
  café, vinho & cuidado (janelas em arco) → refúgio em Caraíva → "A Cereja está chegando em Pinheiros" (Rua Arthur de Azevedo, 972) → 2 @ + WhatsApp.
- Ajustes: animação do seg. 20 (arcos sem blocos vazios, contorno desenhado, cerejinhas balançando);
  **não substituir o "I" de ESMALTERIA por cereja** — só uma cerejinha pequena em cima; não mudar o logo.
- @cereja_esmalteria_caraiva · @cereja_esmalteria_pinheiros · (11) 99824-1389 · trilha bossa-house 125bpm (referência: "Bossa Moves").

### 14 — CLIENTE: Construtora Metrocasa — `metrocasa_motion_v3`
- Vermelho #E31E24 / grafite / branco, Poppins Bold (≈Montserrat), script "Sonhar" (TeX Gyre Chorus).
- Logo: casinha recriada em **polígonos vetoriais** (`icon_polys.json`), wordmark suavizado 2x — não alterar desenho.
- Roteiro: "Você ainda PAGA ALUGUEL?" (boleto amassa) → logo monta + "Nunca pare de Sonhar" → linha do metrô por zonas →
  prédio sobe → render real (Prime Alto do Ipiranga) → carrossel de empreendimentos → lazer → plantas reais (Studio 23–25m², 2 dorms 34m²) →
  "R$ 149 MIL* à vista" + ITBI/registro grátis + Uber + MCMV + "*Consulte condições" → (11) 5061-0022 · @construtorametrocasa.
- Ajustes: logo/nome mal cortados (corrigido); música → pop acústico "feel good" (v3). Oferta do Mega Feirão válida até 01/11 — confirmar.

## Prompts que funcionaram melhor (Leonardo / Seedance)
Dica geral: gerar a **imagem** primeiro e depois **imagem → vídeo**, em 9:16, clipes de 4–6s sem cortes; gerar 2–3 versões
e escolher a que não deforma o produto; usar só o trecho limpo do clipe.

**Tênis (fotos de estúdio, ótimas para recorte):**
- `Professional product photography of a futuristic running sneaker, perfect side profile view, facing right, white and black upper with neon lime green accents and sole details, chunky sculpted midsole, no logos, no text, isolated on plain solid light gray background, soft studio lighting, ultra sharp, 8k, commercial catalog shot`
- `Futuristic white black and neon lime green sneaker smashing through a pane of glass in slow motion, glass shards exploding toward the camera, dark studio, neon lime backlight, cinematic, vertical 9:16, no logos, no text, 4k, sneaker commercial` (melhor gancho)
- `Extreme macro shot sliding fast across the textured neon lime sole of a futuristic sneaker, then quick pull back revealing the full sneaker floating in darkness, sharp studio light, vertical 9:16, no logos, no text, 4k`
- `Futuristic white black and neon lime green sneaker levitating and slowly rotating in mid-air, thin neon lime light trails orbiting around it, dark smoky studio background...`
- Giro 360: `...slowly rotating 360 degrees on a turntable, centered, plain solid dark charcoal background...`

**Imobiliário (VERANO):**
- `Cinematic drone shot rising fast from street level along the tower facade to the top, revealing the city skyline at blue hour, smooth motion, slight lens flare, vertical 9:16`
- `Slow camera push toward the floor-to-ceiling windows revealing the sunset city view, sheer curtains gently moving, golden hour light, vertical 9:16` (sala — o melhor take)
- `Low angle camera gliding just above the water surface of the infinity pool toward the skyline at dusk, gentle ripples, vertical 9:16`

**Música (Suno) — caminho recomendado:**
- Imobiliário: `Clean minimal techno, hypnotic, luxury, deep punchy kick, rolling bassline, crisp hats, 120 BPM, instrumental`
- Tênis: `Brazilian phonk, hype sneaker commercial, 128 BPM, punchy distorted 808 bass, cowbell melody, hard drums, short intro build-up then heavy drop, instrumental`
- Esmalteria: `Organic tropical house, warm and elegant, acoustic percussion, soft groovy bassline, Brazilian beach lounge vibe, 125 BPM, instrumental`
- Construtora popular: `Brazilian funk pop, upbeat, energetic, catchy synth hook, 808 bass, commercial, 120 BPM, instrumental`

## Técnicas reaproveitáveis (estão no código)
- Recorte: GrabCut com prior por polígono/limiar + remoção de sombra (baixa saturação, lisa, tocando a borda) + descontaminação de halo branco;
  polígono traçado à mão para bases (lata, copo, sola de tênis).
- "Texto atrás": desenha foto → texto → recorte com a mesma transformação da foto.
- Frame blending para clipes 24fps em 30fps; congelar no quadro limpo antes de a IA deformar.
- Transições: máscara diagonal (ângulo do telhado da Metrocasa), folhas de palmeira varrendo (Cereja), empurrão vertical (Zefyr), dissolve + zoom (Verano).
- Performance: evitar `ctx.filter = blur()` por frame (cachear em sprite) — renderizar fica 20x mais rápido.
