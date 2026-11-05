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

### 15 — Pet shop "FOCINHO" — `15-pet-shop-focinho`
- Creme/laranja #FF7A3D/navy/menta/amarelo, Poppins; personagens vetoriais (cachorro e gato desenhados no canvas, sem fotos).
- Roteiro: "Seu pet merece o melhor dia" (patinhas) → logo FOCINHO → banho & tosa (banheira + bolhas) → 4 serviços em cards →
  1º banho 30% OFF (R$ 69,90 → 48,90) → leva e traz grátis (van) → CTA fictício.
- Transição: máscara circular (bolha) a 0,45s. Trilha ukulele-pop 120bpm (`audio/audio_focinho.py`, gera também `so_efeitos.mp3`).
- Render: `node ../_ferramentas/render_h.js index.html out/video 0,4,8,14,20,24,28,34`.

### 16 — Construtora "NIDO" (portfólio fictício do 14) — `16-construtora-nido`
- Mesma animação/tempos/trilha do 14 (cliente não fechou), **sem nada da Metrocasa**: logo, nome, fotos, renders, plantas,
  empreendimentos, telefone, @, slogan "Sonhar" e ofertas específicas (Uber/ITBI/149 mil) removidos.
- Marca fictícia NIDO (casinha vetorial em 3 peças), verde #12866F no lugar do vermelho; slogan "Seu lugar começa aqui."
- Fotos trocadas por ilustração vetorial (prédios, piscina, churrasqueira, plantas em linha). Preço "R$ 199 MIL*" + "*Condições ilustrativas".
- Termina com CTA de portfólio. `gerar_de_14.py` reaplica as trocas sobre o index do 14.
- Render: `node ../_ferramentas/render_h.js index.html out/video 0,4,8,12,16,20,24,28,34,40`.

### 17 — Esmalteria "AMORA" (portfólio fictício do 13) — `17-esmalteria-amora`
- Mesma animação/tempos/trilha do 13, **sem nada da Cereja**: logo, nome, slogan, filmagens da loja, Caraíva/Pinheiros,
  endereço, @s e WhatsApp removidos.
- Marca fictícia AMORA (wordmark tipográfico + amorinha), paleta ameixa (#3A1233/#6E2A6B/#9B3D8F); cerejas → amoras vetoriais.
- Filmagens trocadas por ilustração: café na xícara e esmaltes nos arcos; pôr do sol na praia no "REFÚGIO pra sua rotina".
- Cena "nova unidade" genérica ("chegando em seu bairro"). Termina com CTA de portfólio. `gerar_de_13.py` reaplica as trocas.
- Render: `node ../_ferramentas/render_h.js index.html out/video 0,3.84,7.68,11.52,15.36,19.2,23.04,26.88,30.72,36.48`.

### 18 — CLIENTE: Gaia Tabacaria (Cerro Largo/RS) — `18-cliente-gaia-tabacaria`
- Filmagens reais do cliente (27 clipes, 60fps; C4106/4123/4136/4156-58 são horizontais e são recortados para 9:16).
- Pipeline: `./estabilizar.sh <pasta dos .mov>` (vidstab 2 passes + grade leve) → `python preparar_frames.py`
  (iguala cor/exposição de cada clipe à média do conjunto + look único: pretos levantados, sombras frias/realces quentes) →
  `node render_gaia.js out/gaia_video` (servidor local + carrega quadros sob demanda; `node render_gaia.js out/s 1.2,3.4` tira prints).
- Brutos e quadros ficam fora do git (pesados). Logo do cliente (`logo_gaia.png`) usada sem alteração, só com máscara suave na borda.
- Fontes: Bebas Neue (igual aos posts deles) + Cinzel, em `fonts/`. Paleta: verde/roxo/dourado da logo.
- Roteiro 128bpm (78 tempos, 36,5s): anel de fumaça em faixa cinema "O RITUAL COMEÇA AQUI" → "SINTA O SABOR" → logo + Cerro Largo →
  "TUDO PRO SEU MOMENTO" → Narguilés / Acessórios / Carvão / Essências / E muito mais (cortes na batida, whip + blur) →
  fumaça "VIVA A EXPERIÊNCIA" → Teleentrega de sexta (pedidos até meio-dia) → Horários (qua/qui/sáb/dom 11h–15h) →
  logo + @gaia.tabacaria + "Venda proibida para menores de 18 anos" (obrigatório — Lei 9.294/96).
- v2 (feedback do Ale): tirar zoom sem sentido na abertura, bordas/linhas/pílulas douradas, raios, flashes, ecos de texto e
  vazamentos de luz ("brega"); fumaça sobreposta bem leve; edição menos engessada → cada take com transição própria
  (corte seco no beat, whip H/V, zoom-through, push, dissolve, dip, revelação por fumaça). Sem tela dividida (Ale não gostou de 2 imagens ao mesmo tempo); sequência de fumaça com poucas cenas longas (2 × 1,9s), não muitos cortes curtos. Nada de sobreposição/dissolve entre filmagens: transição "zoom" = zoom com desfoque radial no take A, troca seca no meio, take B sai do zoom; final entra passando pelo preto. O take anterior continua rodando durante a transição (sem congelar) + rampas de velocidade
  e animações de texto variadas (sobe da máscara, tracking, pop central, palavras trocando a cada batida).
- Trilha TECHNO sintetizada (`audio/audio_gaia.py`): kick + rumble, baixo rolante, acid com filtro ressonante, sidechain,
  breakdown com riser + rolo de caixa. Sugestão Suno: `Dark hypnotic techno, rolling bassline, acid 303 line, punchy kick with rumble, 128 BPM, instrumental`.

### 19 — CLIENTE: Rittú (skin care de luxo) — `19-cliente-rittu-skincare`
- Nasceu como "NOCTÉA" (nome provisório); marca real = **RITTÚ** → final de cliente (logo + "Sua pele, em outro nível." + "Conheça a coleção"), SEM frase de portfólio.
- Pendentes do cliente: @ do Instagram, logo oficial, nomes reais dos produtos e ativos/claims (Sérum Noturno, Crème Étoile, 72h, ativos são provisórios).
- v1 (astrológica, vetorial — Ale não gostou: escuro/parado, produto "desenhado", astrologia, ritmo) guardada em `v1/`.
- v2: **produtos em 3D real (three.js r160, `lib/`)** — `scene3d.js`: vidro verde com transmissão/clearcoat, colar dourado com anéis gravados,
  bulbo de borracha, rótulo em textura de canvas (Cormorant + Jost), pote com creme em espiral, frasco de essência, pódios;
  estúdio com parede de luz esmeralda (shader), piso espelhado (reflexo por cópia espelhada), sombra de contato + poça de luz,
  texto atrás do produto como plano 3D. Pós: profundidade de campo (BokehPass, foco = distância câmera→alvo) + brilho 2D
  nos pontos de luz + vinheta + grão. **Não usar UnrealBloomPass** (gera blocos pretos/NaN nos reflexos no SwiftShader).
- Editorial de grife: Cormorant Garamond itálico + Jost espaçada; textos sobem de máscara ou entram do desfoque.
- Takes (120bpm, cortes na batida): macro do colar "A noite" → giro whip "é sua aliada" → conta-gotas sobe (luz varrendo)
  → gota cai com anel no piso → órbita com "Lua Nova" atrás + REGENERA → 3 ativos em cortes de 1,5s → pote abre (Crème Étoile)
  → coleção nos pódios (Noite Verde) → logo RITTÚ → fechamento da marca. Transições: whip H/V, zoom-through, varredura de luz, corte com punch.
- Trilha melodic house (`audio/audio_noctea.py`: Em–Cmaj7–G–D/F#, pluck com filtro, stabs FM, vocal chops, drop no 2s,
  breakdown no pote, corte seco no logo) + `so_efeitos.mp3`. Render: `node render.js out/video` (WebGL via SwiftShader, ~15 min).
- Imagens estáticas dos produtos (2048², estúdio + PNG transparente, 10 vistas): `node render_stills.js <pasta>` (vistas em `stills.html`).

- **Fotos "reais" por path tracing** (`photo.html` + `render_photo.js <saida.png> <vista> <amostras> [w] [h]`, lib `three-gpu-pathtracer` 0.0.23
  com patch de `environmentRotation` p/ three r160): luz física, refração real, softboxes emissivos + fundo em degradê esmeralda.
  Vistas: serum, serum_aberto, pote, colecao. ~15 min/foto a 1080x1920/160 amostras; depois `nlmeans` p/ tirar ruído.
- IA de vídeo grátis (Hugging Face ZeroGPU): cota ~2 min/dia por conta (todos os espaços). LTX-Video distilled funcionou
  (upload via /gradio_api/upload, `gerar_ia_ltx.py`); bons: gota no líquido e fita de seda. FLUX Kontext pede 90s/imagem.

### 20 — UI animada "KORA" (banco digital, portfólio fictício, "nível acima do Pulsa") — `20-ui-app-kora` — ✅ ESTILO APROVADO ("muito profissional"): usar como base para UI animada
- iPhone 3D em three.js (titânio, lentes, botões; `lib/` = three r160 + RoomEnvironment), tela = canvas 720×1560 desenhado por quadro
  e usado como textura (`drawScreen`). Camadas da UI saltam da tela em 3D (card de saldo, selo +12,4%, widgets de vidro), cartão de metal
  com borda iridescente. Fundo/textos/partículas em 2D por cima (WebGL com fundo transparente). Motion blur por subamostras nos giros.
- Paleta: preto #05060A, íris #7B6CFF → ciano #4DE3FF, menta #3DF5A7; Inter / Inter Display (`fonts/`).
- Roteiro 120bpm/32s: "Seu dinheiro sem atrito." → celular sobe girando + boot do logo → home (saldo contando, card levanta, Pix chega
  pela Dynamic Island) → push na tela: Pix (digita 250, desliza, sucesso + confete) → cartão de metal → widgets (cashback, cofrinho, 112% do CDI)
  → montagem na batida (gastos, investimentos, cartão, Face ID) → costas do aparelho com logo + sonic logo → CTA de portfólio.
- Trilha house limpa D–Bm–G–A + UI SFX (`audio/audio_kora.py`, gera `so_efeitos.mp3`). Render: `node render.js out/video` (~30 min, SwiftShader).

### 21 — UI animada "AERA" (app de viagens, portfólio fictício, evolução do 20) — `21-ui-app-aera`
- Mesma base técnica do KORA, em **tema claro estilo keynote**: iPhone titânio branco, sombra real na parede (`ShadowMaterial` + VSM),
  **relógio 3D** com troca de foco entre aparelhos (camadas 1/2 renderizadas separadas + desfoque), cartão de embarque 3D com recortes,
  palavra gigante "LISBOA" atrás do celular (plano 3D), mapa pontilhado com rota e avião, ilustrações de destino vetoriais (sem fotos).
- Paleta: papel #F2EFE9, tinta #101216, laranja #FF5A1F; Inter / Inter Display. Logo fictício "aera." (círculo laranja + aviãozinho).
- Roteiro 120bpm/32s: "Sua próxima viagem começa aqui." → celular cai e assenta → busca "Lisboa" (card levanta, −11% hoje, alerta de preço na Dynamic Island)
  → mapa + reserva (confete) → cartão de embarque → relógio "Avisos no pulso" → montagem (hotel, roteiro, gastos em €, check-in) → costas com logo "Viaje leve." → CTA.
- Trilha house solar E–C#m–A–B (`audio/audio_aera.py`, base no da KORA). Render: `node render.js out/video`.

### 22 — Explicativo "kuida" (app de saúde, portfólio fictício, evolução do 05 Lavo) — `22-explicativo-kuida`
- Canvas 2D (sem WebGL): ilustração flat "premium" (degradês suaves, sombras, grão, vinheta), personagem com rig (`person()`: tronco,
  cabeça, braço/perna com cotovelo/joelho, piscar, boca falando, febre/rubor) — Bia, Dr. Rafael e o entregador.
- Truque: o celular pequeno na mão é o MESMO `phoneMock()` do celular grande → zoom contínuo entra na tela.
- Roteiro 120bpm/36s: "Acordou mal?" (despertador, espirro, termômetro 38,2°) → 1 Conte o que sente (toques nos sintomas) →
  2 Consulta por vídeo (médico fala, balões) → 3 Receita na hora (sai do celular, assinatura, carimbo) → 4 Remédio na porta (cidade com parallax,
  moto, campainha, entrega) → íris para a sala "Em poucas horas, você de volta." → círculo teal vira logo kuida → CTA de portfólio.
- Paleta creme/teal #0F5C56/menta/coral #FF7A66; Poppins + Inter. Trilha pop C–G–Am–F (`audio/audio_kuida.py`, SFX: despertador, espirro, bip, campainha, carimbo).

### 23 — Festival "SOLSTÍCIO" (lançamento de evento, portfólio fictício) — `23-festival-solsticio`
- Diferente de todos: **shader WebGL** (gradiente líquido fbm + sol em degradê + anéis no bumbo + retícula/halftone) em meia resolução
  + tipografia suíça/brutalista (Bebas Neue gigante ajustada à largura, grade de colunas, Inter) em canvas 2D. Tudo pulsa no kick (BT=0,5s).
- Paleta osso #EDE6D6 / preto / vermelho #FF3B1F / azul #2430FF / sol #FFB21F. Line-up e artistas fictícios.
- Roteiro 120bpm/32s: "DOIS / DIAS / DE / SOL" (uma palavra por batida, cores invertendo) → sol nasce + letras de SOLSTÍCIO caindo →
  data "20—21" em contador rolante (sol cresce e vira o fundo) → line-up sáb (osso) e dom (azul) linha a linha → números (3 palcos, 40 artistas…) →
  ingresso gira e entra (Lote 1 R$ 189 + "esgota em" contando) → logo → CTA de portfólio. Transições: íris pelo sol, empurrão vertical, cortina com faixa amarela, dip.
- v2 (feedback do Ale): resquício do dígito no contador da data (recorte justo), acentos cortados pelas máscaras/linhas (recorte com folga + mais espaço no line-up),
  **ingresso 3D realista** (three.js: papel com textura/relevo, picote com recortes, faixa holográfica iridescente, luz passando), trilha **TECHNO**
  (kick + rumble, baixo rolante, acid ressonante, stab) e efeitos mais estéticos (swell reverso → impacto com cauda, blips filtrados com reverb, stab no final).
- v3: data sem corte no topo (dígito parado desenhado sem recorte); música trocada para **afro/melodic house** (congas, shaker, grave quente,
  melodia com eco) — versão techno guardada em `audio/audio_solsticio_techno.py`. Suno: `Melodic afro house festival anthem, organic percussion, warm deep bass, uplifting pluck melody, 120 BPM, instrumental`.
- `audio/audio_solsticio.py`. Render: `node render.js out/video`.
