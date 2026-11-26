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

### 23 — Festival "ONDA" (lançamento de evento, portfólio fictício) — `23-festival-onda`
- Nasceu como "SOLSTÍCIO" (sol laranja + retícula, `solsticio_v3.html`) — Ale reprovou: nome, laranja "antigo", vídeo vazio e músicas (techno/afro sintetizados).
- v4 ONDA: **cromo líquido iridescente** frio (shader WebGL meia resolução, violeta/azul + brilhos brancos + reflexos verde-ácido) e **texto preenchido de cromo**
  (letra clara + cromo por cima, sempre legível); verde ácido #C6FF3D / violeta #6B2BFF / preto / gelo #E9ECF4; Bebas Neue + Inter.
- **Uma cena nova a cada 2s** (16 cenas) e nada parado: ondas de linhas no bumbo, partículas, selo girando, faixa diagonal correndo, varredura atrás de cada nome,
  transições de 0,3s variadas (empurrão, círculo com contorno verde, cortina diagonal, zoom).
- Roteiro: SENTE/ESSA/NOVA/ONDA → logo cromado → 20—21 DEZ (contador) → mapa + pin "BAÍA DO SOL" + coordenadas → line-up sáb (2 cenas) e dom (fundo verde, 2 cenas) →
  3 PALCOS (luzes) → 40 ARTISTAS (contador + 40 pontos) → 48H (relógio) → ingresso 3D preto/verde com faixa holográfica (gira) + "esgota em" → logo → CTA.
- ✅ Vídeo aprovado ("ficou perfeito"). Música final = faixa enviada pelo Ale (`audio/musica_ale.mp3`: ~123bpm esticada p/ 120bpm com atempo 0,9757 e alinhada com a batida forte no seg. 2; `trilha_ale.mp3` = música + efeitos sutis e variados só nos movimentos grandes — `audio/sfx_onda.py`: impacto, ar, swoosh, plop do pin, riser, vidro, varredura, papel, brilho holográfico, sub, swell reverso, sino). Coordenadas sob "BAÍA DO SOL" removidas.
- Música sintetizada alternativa: techno clean do VERANO (`audio/audio_onda.py`), SFX nos cortes. Antigas em `audio/solsticio_*.py`. Render: `node render.js out/video`.

### 24 — Academia "FORJA" (academia 24h, portfólio fictício) — `24-academia-forja`
- v1 (preto/vermelho, halter/anilha/kettlebell 3D, `v1_generico.html`) — Ale: "muito genérico".
- v2 **com conceito: FORJA = forjar aço** ("Todo aço começa bruto. Você é a matéria-prima."): metal em brasa (cor de corpo negro branco→amarelo→laranja→vermelho → aço),
  `hotText()` (letra incandescente que esfria até aço escovado), faíscas de forja com rastro e gravidade, brasas, vapor, shader de **metal fundido** (crosta escura + rachaduras brilhando).
- Roteiro 120bpm/32s (cena a cada 2s): TODO/AÇO/COMEÇA/BRUTO. → matéria-prima (metal fundido) → logo em brasa esfriando → 1 AQUECER (barra esquentando, °C) →
  2 MOLDAR (martelo na bigorna a cada batida) → modalidades em brasa → 3 TEMPERAR (peça na água + vapor) → check-in no app → FORJADO NA DISCIPLINA (halter 3D + vapor) →
  24H (split-flap) → preço estampado em chapa de aço (R$ 89,90 em brasa) → "1ª SEMANA GRÁTIS" marcada a ferro quente na madeira → logo → CTA.
- Trilha phonk 120bpm + efeitos de forja (`audio/audio_forja.py`: bigorna nas palavras e marteladas, chiado na água/ferro, fogo). Render: `node render.js out/video`.

### 25 — Festa "FREAKNC" (estética do @freaknclabel — label/festa underground) — `25-festa-freaknc`
- Estética absorvida dos posts deles: **roxo #9B2FE0 + amarelo-mostarda #F4C22B + preto/grafite**, fotos em **retícula duotone**, nome repetido em pilha
  (condensada gigante — Anton), **letra psicodélica distorcida** (`warpText`, Bowlby One fatiada com seno), **nome em arco** em volta de círculo, **janela Windows XP**
  "FREAKNC PRESENTS:", código de barras, "YOUR UNDERGROUND LABEL"/"PRESENTS:"/"2026", texto justificado (Archivo Black). Logo "freaknc" recriado (Fredoka 700 + "k" espelhado)
  — **trocar pelo arquivo oficial** se o Ale mandar. Fontes baixadas do Google Fonts em `fonts/`.
- Artistas = silhuetas ilustradas em retícula (`djFig` + `halftone`), **placeholder para as fotos reais**. Line-up/data/local/preço fictícios (NOVAK, MARA V, LUMI, KAEL B2B RUSSO; 13.12; local secreto; lote 1 R$ 40).
- Roteiro 120bpm/32s (cena a cada 2s): BUILT/FOR THE/DANCE/FLOOR → logo + PRESENTS → FREAK OUT #01 (psicodélico) → 13.12 → artistas (pilha / arco / janela XP / B2B grade 2026) →
  manifesto justificado → HOUSE·TECH HOUSE·MINIMAL + público → LOCAL SECRETO → ingresso → INGRESSOS NO LINK DA BIO → logo "Built for the dancefloor." → @freaknclabel.
- v2 ("muito genérico"): linguagem de **colagem impressa** — stop-motion 12qps (`hold`/`jit`), fita adesiva, rabiscos de marcador animados (`scribble`, `arrowS`, `highlight`),
  adesivos serrilhados, textura de papel/xerox por cima, transição de **papel rasgado**, nomes esticados na vertical, cursor do Windows clicando. Logo **oficial** recortado do print do Ale (`logo_freaknc_mask.png`, tingido nas 2 cores da marca). v1 em `v1_limpo.html`.
- Música = faixa do Ale (`audio/musica_ale.mp3`: 129bpm → 120bpm, entrada forte alinhada no seg. 2, 4 compassos do meio repetidos p/ fechar 32s); `trilha_ale.mp3` = música + SFX a 50%.
- v3: **mídias reais do Ale** em `midia/` (fora do git): vídeo do HOMRICH nos CDJs (recorte só da filmagem, trecho limpo 13–15,6s) em cartão com fita, retrato KOSMA 88 no círculo com arco,
  EN_RRICH tocando dentro da janela XP, grade 2026 com EN_RRICH + KOSMA 88, vídeo da festa (luz vermelha) atrás do manifesto, vídeo do público (cabine) em HOUSE/TECH HOUSE/MINIMAL.
  Quadros extraídos a 30fps com ffmpeg (`frameAt`). Render: `node render.js out/video`.

### 26 — CLIENTE (Haskell) "DENSI RESIST" — explicativo com boneca narrando — `26-haskell-densi-resist`
- Áudio da narração enviado pelo Ale (transcrito com faster-whisper `small`, palavras com tempo em `lipsync.json`); boneca 3D de feltro (imagem do Ale) **fala com lip-sync**:
  boca deformada por faixas (lábio inferior/queixo descem conforme a energia vocal 250–3000 Hz, sibilantes fecham), piscadas, balanço. Centro/ângulo da boca: M=[566,370], 0,255 rad.
- **Boca aprovada só no formato "natural"**: o corte segue a linha REAL do lábio de baixo traçada na imagem (`LIP`), então dentes e lábio de cima da própria imagem ficam no lugar;
  NUNCA desenhar dentes brancos/lábios por cima nem cortar em linha reta (gera "dois lábios"/dentes duplicados — Ale reprovou). Abertura pequena (MD=17), `lipsync2.py` (dinâmica por sílaba + largura por vogal).
- Áudio final = `audio/voz2.wav` (19,9s, termina em "juntos vão melhorar em 85% a queda capilar" → card JUNTOS 85%). **Sem legenda** (Ale pediu para tirar). Tempos antigos remapeados por `warp()` (`KN`).
  Cabeça inclina separada do corpo (`headWarp`, usa o recorte), pulinhos nas palavras fortes (`EMPH`).
- Roteiro 18,5s: boneca "Amigas, eu li tudo…" + selo DENSI RESIST → mergulho no fio (imagem de referência do folículo, Ken Burns) → ATIVO EXCLUSIVO Haskell → MINOXI CARE G2 + ancoragem
  (raízes de luz, anéis, bullets) → sobe pelo fio → PEPTÍDEOS PRO (corrente de esferas enrolando o fio) → NIACINAMIDA (filme protetor brilhante) → termina na NIACINAMIDA (17,2s, sem final: o trecho entra no meio de outro vídeo). Tudo em Poppins.
  Nas cenas microscópicas (fio em tela cheia) a boneca aparece recortada sem fundo (`midia/boneca_rec.png`, rembg isnet), corpo inteiro no canto inferior direito narrando (`dollMini`, lip-sync mascarado pelo recorte); boneca com movimento leve (balanço, respiração, acenos nas palavras fortes); legenda palavra a palavra com destaque roxo #6B2C7E. Sem logo oficial (o do briefing veio cortado) — pedir o arquivo.

### 27 — Telão de LED "DJ ViNi" (4×2 m, loop) — `27-telao-dj-vini`
- 3840×1920 (2:1), 30fps, **loop perfeito de 10s** (tudo periódico em 10s; 120bpm = 20 batidas). Prata/azul/preto, sem áudio.
- v1 2D (`v1_2d.html`) — Ale: "muito simples/básico" e pediu **menos brilho em volta** (borda com só 3 brilhos discretos).
- v2 **3D real (three.js r160, `lib/`)**: letreiro extrudado com chanfro (contornos da Racing Sans One em `glyphs.json`, extraídos com fontTools),
  face cromada = textura de gradiente animada (varredura de luz) + reflexo de ambiente próprio (PMREM com painéis prata/azul), lateral azul metálica, neon atrás;
  parede de caixas de som 3D (cone + calota cromada que se movem na batida, anel de LED), piso espelhado (palco construído 2×, cópia com `scale.y=-1`),
  feixes de luz aditivos, partículas, câmera em órbita suave. Pós em 2D: bloom em 1/8 da resolução, vinheta, estrelas nos pingos dos "i" (ponto 3D projetado), borda.
- Cuidados: face plana de metal reflete uma cor só (por isso o gradiente em textura); cone do falante precisa ficar para fora do gabinete; não pôr barras/objetos
  pequenos atrás dos vãos das letras (parecem pontos). `?s=0.5` (env `Q='?s=0.5'`) renderiza o 3D em meia resolução para teste.
- Render: `node render.js out/video` · imagem PNG: `node still.js saida.png 1.3`.

### 28 — Reels narrado "Queda de braço" (perigos + fortalecimento, 65s) — `28-queda-de-braco`
- Narração por TTS offline **Piper** (`pt_BR-faber-medium`, baixado de huggingface.co/rhasspy/piper-voices; `--length-scale 0.9`) — o Edge TTS (Bing) é bloqueado na rede.
  Conferir pronúncia transcrevendo com faster-whisper; ajustes que funcionaram: "martélo", "rósca", "Segue lá o perfil", "Protege o ombro".
  `audio/roteiro.txt` (1 fala por linha) → `audio/falas/NN.wav` → `audio/montar_voz.py` (corta silêncio, pausas `GAP`) → `audio/voz.wav` + `falas.json` (falas + palavras com tempo).
- Trilha de fundo leve (`audio/trilha.py`: lo-fi house 120bpm Am–F–C–G, sidechain pela voz, ~15 dB abaixo da fala) + SFX nos cortes/impactos (prioridade, ≥0,45s) →
  `trilha_final.mp3`, `so_musica.mp3`, `so_efeitos.mp3`, `narracao.mp3`.
- Canvas 2D: 18 cenas (corte a cada 2–5s, transições whip/zoom/up/círculo de 0,24s), vermelho = perigo, verde-limão = fortalecimento; Anton + Poppins.
  Ilustração: `limb()` com anatomia (deltoide, bíceps/tríceps, braquiorradial, brilho, vincos, contorno), `fist()` peça única com nós/polegar/unha, `clasp()` (mãos travadas), ossos em raio-x, atleta com rig (`arm()`, `athlete()`).
  Ale pediu melhorar braços/ilustrações e as mãos ("estranhas") — corrigido assim. `g.reset()` em cada cena (clip vazava entre quadros).
- Render: `node render.js out/video` (~9 min) e mux com `audio/trilha_final.mp3`.

### 29 — Reels narrado "3 técnicas de queda de braço" (Top Roll, Hook, Press, 44,5s) — `29-tecnicas-queda-de-braco`
- 1º da série de 5 ideias pro canal de queda de braço (ordem pedida: 2 → 1 → 3 → 4 → 5): (1) "O erro que quebra braços" (câmera lenta errado × certo),
  (2) **3 técnicas** ✅, (3) treino de 10 min em casa (toalha/garrafa/elástico), (4) mito ou verdade, (5) desafio 30 dias de pegada (série).
- Mesmo pipeline/visual do 28: `head.part` (helpers + `wrestle()` com parâmetros dc/sh/eh/eo_/ct p/ animar as técnicas) + `scenes.part` (16 cenas) + `tail.part` → `cat > index.html`.
  Extras: `hand()` (mão abrindo, 2 falanges), `arrow()`, `techCard()`. Pronúncia: "rúqui (Hook)", "Você puxa a mão…", "Coloque o ombro…".
- **Textos sempre acima de y≈1450** (legenda e nome do perfil do Instagram cobrem a parte de baixo; botões ficam na direita) — Ale pediu; aplicado também no 28 (contador REP foi pro alto).
- Render: `node render.js out/video` (~5 min) + mux com `audio/trilha_final.mp3`.

### 30 — Reels narrado "O erro que quebra braços" (postura errada × certa, 32,8s) — `30-erro-queda-de-braco`
- Vídeo 1 da série (2 ✅, 1 ✅, faltam 3, 4, 5). Mesma estrutura do 29 (`head.part` + `scenes.part` + `tail.part`).
- Gancho em câmera lenta (selo 0,25×, faixas de cinema) → osso quebrando → **vista de cima** (`topView(g,cx,cy,s,w)`: mesa, adversário, herói; `w`=1 errado: ombro longe,
  tronco e rosto virados, cone de visão vermelho; `w`=0 certo: cone verde no braço) → torção + "força direto pro osso" → jeito certo com 3 checagens (o corpo vai se ajeitando)
  → "pro músculo, não pro osso" → errado × certo → "manda pra quem vive te desafiando" (avião de papel) → segue o perfil.
- Pronúncia: "êrro", "olha o jeito certo", "O peito virado pra mão".

### 31 — Reels narrado "Treino de 10 min pra antebraço em casa" (toalha, garrafa, elástico, 44s) — `31-treino-antebraco-casa`
- Vídeo 3 da série (feitos: 2, 1, 3; faltam 4 mito ou verdade e 5 desafio 30 dias). Mesma estrutura do 29/30.
- Props desenhados: `towel()` (toalha torcendo com listras), `bottle()` (PET com água balançando — recriar o path antes do stroke, senão sai um retângulo),
  `palmHand()` (mão de frente com dedos abrindo em leque; elástico = elipse envolvendo as pontas), `bookmark()` (salvar), `badge()` (tempo/reps no alto à direita), `drops()`.
- Exercícios: torção de toalha → rósca de punho com garrafa → alavanca com garrafa → elástico nos dedos → aperto máximo na toalha; 3 voltas / 30s; 3x por semana → barra "força da pegada".
- Usar "x" e não "×" nos contadores (o "×" fica minúsculo na Anton). "Segue lá o perfil" funciona como frase separada.
- **Queda de braço: os dois competidores lutam com a MESMA mão (direita) e seguram o pino com a outra, em cantos opostos** — na vista de cima, a mão direita do adversário
  fica à esquerda da tela (Ale apontou o erro; corrigido no `topView` do 30).

### 32 — Reels narrado "Mito ou verdade" (4 afirmações, formato quiz, 43s) — `32-mito-ou-verdade`
- Vídeo 4 da série (feitos 2, 1, 3, 4; falta o 5 — desafio 30 dias de pegada). Mesma estrutura do 29–31.
- Quiz: `claim()` (#n + afirmação com aspas), `buttons()` (MITO vermelho / VERDADE verde + barra de tempo com tique a cada 0,5s), `stamp()` (carimbo diagonal + onda), `explain()`.
  #1 mais forte sempre ganha → MITO (técnica/alavanca vira a disputa) · #2 braço grande vence → MITO (antebraço/punho/tendões) ·
  #3 dá pra quebrar o braço → VERDADE (osso torce e parte) · #4 canhoto tem vantagem → VERDADE (luta de esquerda = `wrestle` espelhado; barras de treino D×E).
- SFX de quiz: `buzz()` (mito), `correct()` (verdade), `ticks()`; final "Qual delas te surpreendeu? Comenta aí!" com balões de comentário.

### 33 — Reels narrado "Desafio 30 dias de pegada" (ep. 1 — dia 1, 37s) — `33-desafio-30-dias`
- Vídeo 5 da série (✅ série completa: 2, 1, 3, 4, 5). `head.part` + `helpers.part` (props do 31: toalha, garrafa, badge…) + `scenes.part` + `tail.part`.
- Calendário de 30 dias (`calGrid`), "DIA 01", teste 1 pendurado na barra (de costas, `stopwatch`), teste 2 pinça com livro (`pinch`), caderno com caneta anotando
  BARRA/PINÇA (ponto de partida), rotina diária (toalha · rósca · aperto, dia rolando ao fundo), dia 30 com barras DIA 1 × DIA 30 + "?", "Comenta EU TOPO" (balões), segue até o dia 30.
- Pronúncia: "eu tôpo", "rósca". Próximos episódios possíveis: dia 7/15 (progresso) e dia 30 (resultado) reaproveitando este arquivo.

### Referência de canal: @theory_armwrestling (TikTok) — `src/templates/_referencias/theory_armwrestling.md`
- Estilo que viraliza (até 7,4 mi views): filmagem real na mesa + **HUD de biomecânica** (linhas de esqueleto, ângulos em graus, % de vantagem, medidor "Mechanical Advantage",
  mãos em contorno com mapa de calor, diagrama do pad visto de cima), pouco texto, 15–30s, uma ideia por vídeo, regras da WAF citadas.
- Acesso: ambiente "Edi-o-" com tiktok.com + CDNs de mídia liberados; `yt-dlp` precisa de permissão `Bash(yt-dlp *)` (o Ale adicionou).

### Perfil do Ale no TikTok: **@armwerstlingdicas — "ARMWERSTLING Every Day"** (71,7 mil seguidores) — onde os vídeos 28–34 são postados
- Foto de perfil: `src/templates/_perfil_armwerstling/` (`head.part` + `avatar.part` → `node render.js <saida> 0` e recortar 1080×1080 a partir de y=420):
  mãos travadas em close + HUD verde (#36F27A) + anel brilhante; o PNG vai como `avatar.png` em cada vídeo novo.
- **Chamada final dos próximos vídeos**: cartão com a foto de perfil (`AV` = avatar.png, círculo com borda verde), nome "ARMWERSTLING Every Day",
  "@armwerstlingdicas", botão SEGUIR → ✓ SEGUINDO, e "SEGUE O PERFIL" + "@armwerstlingdicas" embaixo (ver cena 9 do vídeo 34).

### 34 — "Por que o hook perde pro top roll" (29,5s) — `34-hook-vs-toproll` — 1º no estilo @theory_armwrestling
- Ginásio escuro (parede de concreto + grama), mesa oficial vermelha/branca com almofadas azuis, título cinza translúcido no topo e HUD:
  `skel()` (esqueleto ombro–cotovelo–punho), `lever()` (linha de alavanca do punho ao ponto de contato), `gauge()` (medidor "VANTAGEM MECÂNICA" com %),
  `handIcon()` (mão em contorno com mapa de calor), `arcDeg()` (ângulo do punho), `chip()` (rótulos). `stage()` = `wrestle()` com zoom + pontos-chave mapeados.
- Roteiro: ponto de contato → hook: alavanca curta/força máxima → top roll sobe a mão rumo aos dedos → +20% de alavanca → ≈ −18% de força (modelo simples, citado na tela)
  → dedos abrem, punho cede, pressão de lado → defesa: pegada baixa perto do punho → segue o perfil (com foto e @).

### 35 — "A posição que anula o hook" (anti-hook, 27,5s) — `35-anti-hook` — estilo HUD do 34
- Mesmo kit do 34 (`gym`, `stage`, `gauge`, `handIcon`, `lever`, `chip`) + `HOOK`/`ANTI` (poses do `wrestle`), `mix()` (interpola poses), `arw()` (seta), `glow()` (calor).
- Roteiro: perdendo pro hook → carga nas pontas dos dedos (calor vermelho) → alavanca curta = força máxima (78% x 100%) → não lute contra o punho (X na seta)
  → anti-hook: sobe a pegada + puxa pra trás, alavanca dele estica → **linha de carga** animada dos seus dedos pro punho dele → medidor vira (100% x 82%) → comenta → segue o perfil.
- Render: `node render.js out/video` + mux com `audio/trilha_final.mp3`.

### 36 — "Puxe com as costas" (45s) — `36-puxe-com-as-costas` — estilo HUD do 34
- Kit do 34/35 + `backView()` (atleta de COSTAS na mesa: dorsais brilham `lat`, bíceps vermelho `bic`, força subindo das costas até a mão `flow`), `along()`, `fbar()` (barras de força), `step()` (número do passo).
- Roteiro: só puxa com o braço → cansa em 10s (barra de energia) → bíceps é pequeno → campeões puxam com as costas (grande dorsal) → ombro atrás da mão + braço travado
  → braço vira corda → força nasce nas costas e chega na mão → passos 1 ombro na linha / 2 braço fechado / 3 gira o tronco (remada) → força quase dobra (*modelo simples) → remada + barra fixa → comenta → segue.
- Pronúncia: "Os campeões" (no lugar de "quem ganha"), "Passo um/dois/três".

### 37 — "Altura da pegada" (60s) — `37-altura-da-pegada` — estilo HUD do 34
- Kit do 34–36 + poses `HIGH`/`LOW`/`NEU`/`PULL`, `ruler()` (régua de altura VOCÊ x ELE), `door()` (porta vista de cima, empurrão perto da dobradiça), `gloves()` (mãos do juiz).
- Roteiro: altura da mão decide → mão alta = alavanca (dedos por cima) → alavanca longa pra ele → mão baixa = punho preso → porta perto da dobradiça → menos força chega
  → pequena na mão / enorme no braço → 2 dedos mais alto, vantagem muda → passos (suba os dedos, punho levemente enrolado, traga pro corpo) → juiz arruma, GO!, quem sobe primeiro manda
  → puxe com as costas (link com o 36) → rosca de punho + pinça → comenta → segue.
- Pronúncia: "Com a mão alta/baixa" (só "Mão alta" sai "Não alta"), "alavanca comprida", "sóbe".

### 38 — "3 faltas que tiram sua vitória" (60s) — `38-faltas-waf` — estilo HUD do 34, **gancho forte**
- Ale: "os vídeos não estão subindo" → gancho visual + frase de efeito: "Você venceu. E mesmo assim, perdeu a luta." — vitória com flash + confete,
  congela (`desat` = dessatura + tinta vermelha), apito, carimbo gigante "FALTA!" (`stamp` com onda de choque), círculo no cotovelo, e REBOBINA (◀◀ + linhas) com "?" → loop aberto "Fica até a última" (3ª carta trancada).
- Kit novo: `stage2` (stage + mapa `M` p/ marcar a almofada), `padMark`, `tv()` (vista de cima: `rel` solta o pino, `lean` ombro passa do centro, `line`/`lineRed`), `whistle`, `badge3` (FALTA n/3), `confetti`.
- Faltas: 1 soltar o pino · 2 ombro passa da linha do centro (juiz para a luta) · 3 cotovelo sai da almofada (a mais comum; vitória com cotovelo fora não vale) → dica → compartilha → segue.
- SFX novos em `trilha.py`: `whistle_s` (apito), `rewind`. Pronúncia: "Primeira/Segunda/Terceira falta", "Largou o pino".

### 39 — "Por que treinar a 90°" (60s) — `39-treino-90-graus` — estilo HUD do 34 + gancho forte
- Gancho: braço gigante flexionando "REP 246" + "BÍCEPS TODO DIA" → corte pra mesa, perde em 3s (cronômetro) → congela + carimbo "PERDEU EM 3s". Frase: "Ele treina bíceps todo dia. E perdeu em três segundos."
- Kit novo: `bigArm` (braço flexionando com tronco), `protractor` (transferidor no cotovelo), `chart` (força x ângulo: curva `band` ±15° com queda vermelha fora / curva `torque` com PICO em 90°),
  `towelRig` (atleta puxando toalha presa no poste, cotovelo 90°), `timerRing`.
- Roteiro: 90° → na mesa o braço luta em 90° → na academia passa voando (rosca com transferidor) → força específica do ângulo ±15°, fora cai → forte na academia trava na mesa
  → bíceps tem mais força perto de 90° → isometria com toalha (passos: 90°, 10s sem mexer, 5x) → 3x/semana no fim do treino → força sobe → compartilha → segue.

### 40 — "Seu dedão te faz perder" (60s) — `40-polegar` — estilo HUD do 34 + gancho forte
- 1º da nova lista de 5 ideias: (1) dedão ✅ · (2) "Ele pesa 60 kg e te venceu" · (3) "A luta acaba nos 3 primeiros segundos" · (4) pronação, o músculo que ninguém treina · (5) mão pequena não é desculpa.
- Gancho: zoom rápido na pegada → close do dedão solto brilhando vermelho → dedo dele prende → mão abre → dessatura + carimbo "MÃO ABERTA". Frase: "Seu dedão está te fazendo perder. E você nem percebe."
- Kit novo: `grip()` (vista de perto da pegada: `th` 1 solto / 0 travado no indicador / -1 escondido, `open`/`openF` dedos abrindo, `grab`, `knuck` nó do dedão, `mir` + troca de cores p/ mostrar o dedão DELE), `cap()` (dedo em cápsula), `lockIcon`.
- Pronúncia: usar "dedão" (o Piper fala "poligar"); "trava da sua mão" (não "pegada" — saiu "peidada"); "pinça de aço".

### 41 — "Ele pesa 60 kg e acabou de te vencer" (60s) — `41-magro-vence` — estilo HUD do 34 + gancho forte
- 2º da lista nova. Gancho: balanças digitais 95 KG (você) x 60 KG (ele) → corte pra mesa, perde → flash + dessatura + carimbo "60 KG VENCEU".
- Kit novo: `scaleRead` (balança digital), `tag`, `foreLever` (antebraço longo x curto com partículas de força), `steelTendon` (tendões virando cabo de aço), `seesaw` (gangorra 95 kg perto do apoio x 60 kg longe — o leve ganha).
- Roteiro: braço curto = alavanca menor → braço comprido trabalha contra você → tendões (músculo semanas x tendão anos) → magrinho aguenta, grandão sente o cotovelo
  → técnica (sobe a pegada, abre a mão, puxa com as costas) → gangorra "quem usa a alavanca" → treino de punho e dedos → técnicas no perfil (grade de vídeos) → compartilha → segue.
- Pronúncia: "Antebraço curto. Alavanca menor." (frase corrida embola), "o magrinho".

### 42 — CLIENTE: Victoria Flores Floricultura (Campo Limpo/SP) — `42-cliente-victoria-flores`
- Post estratégico de vitrine (sem data/sem preço — preço é decisão da loja), pacote Reels 24s + carrossel 7 artes 1080x1350 + `legenda.txt`. Ale quer vender por R$ 250+.
- Identidade da loja: vermelho rosa/vinho + dourado (logo com rosas e script dourado), site em vermelho #9B0000/creme. Great Vibes (script, Google Fonts) + Cormorant + Poppins; kit em `common.js`.
- Fotos = recortes dos stories (`midia/*.jpg`, trocar pelos originais quando o Ale mandar); logo recortado do print de perfil, sem alteração (só máscara circular).
- Diferencial (site deles): "Somos especialistas em rosas" + "única floricultura da região com câmara fria". Unidade 1 Estr. do Campo Limpo 4421 (11) 94614-3887, seg–sex 8–20h, dom/fer 8–14h;
  Unidade 2 Rua Serra da Esperança 02 (Arrastão/Praça do Campo Limpo) (11) 92091-1669, seg–sex 8–19h, dom/fer fechado. @victoriafloresfloricultura. Cliente real: SEM frase de portfólio.
- Render: `node render.js out/video` (Reels) · `node render_carrossel.js out/carrossel`. Trilha C–G–Am–F sem voz (`audio/trilha.py`) + `so_efeitos.mp3`.

### 43 — CLIENTE: Lótus Presentes de Luxo (@lotuspresentes, 77 mil seg., SP) — `43-cliente-lotus-presentes` — "alto padrão"
- Pacote Reels 27,5s + carrossel 7 artes + `legenda.txt` + prévia com marca d'água (`marca_dagua.py`). Identidade deles: bordô #7E1D3B + dourado + creme; Playfair Display (Google Fonts) + Poppins; kit em `common.js`.
- Gancho: "Algumas pessoas merecem mais do que flores." → "Merecem um momento." (buquê de rosas gigante). Transição: cortina diagonal com fio dourado; textos sobem de máscara; poeira dourada; varredura de luz nas fotos.
- "Mais pedidos" com preços do site (12 rosas R$ 219,90 · 7 girassóis R$ 189,90 · 50 rosas R$ 679,90 — conferir antes de postar); produtos recortados do catálogo: selo "% OFF" apagado por cor + fundo branco → transparente.
- Contato: WhatsApp (11) 98830-5325 · Rua Paul Valery, 47 – Chácara Santo Antônio · lotuspresentes.com.br · entrega no mesmo dia na Grande SP · loja física/compra segura/atendimento humanizado (do post deles). Slogan "Seu carinho, em forma de presente."

### 44 — Sítio Verde Hortifruti (site → vídeo) — `44-cliente-sitio-verde`
- Reels 34s feito só com textos e fotos de sitioverdehortifruti.com.br (14 fotos 1280² baixadas em `midia/`; host liberado no ambiente "Edi-o-"). Logo do site sem alteração.
- Identidade: verde #006636 + verde-limão #8CC63F + vermelho do pingo #E3262C, Poppins; etiquetas coloridas (`tag`), palavras com mola (`pop`), folhinhas caindo, transição empurrão lateral com faixa limão.
- Roteiro: "Você sabe quando a sua fruta foi colhida?" (morangos) → "No Sítio Verde, há pouquíssimo tempo." (hortifruti premium) → fruta no copo → salada de frutas/sucos 100% naturais → café do Sítio Verde
  → adega (importados e nacionais) → floricultura → qualidade premium (mercado, açougue gourmet, padaria artesanal, peixaria) → delivery com veículos próprios → 10 lojas (SP, Guarulhos, SJC, Jacareí) → em breve Brooklin → logo + #vemprosítioverde.

### 45 — Elite Flores Morumbi (@eliteflores, 34 mil seg.) — site → Reels "mais motion graphics" — `45-cliente-elite-flores`
- 31,5s com dados do site eliteflores.com.br (preços/produtos) + imagens do catálogo (`stack.flowermarket.com.br/.../produto/600_<id>.jpg`; o id da imagem ≠ cod do produto) + foto do story (buquê gigante) + logo do perfil.
- Preto/branco/vermelho (pingo do logo) + blush; Great Vibes + Poppins. MG: contador 0→500 ROSAS, revelação em círculo, anel de texto girando no logo, produtos recortados entrando com giro,
  selo de preço vermelho com mola, contador "a partir de R$ 125", transição com 3 faixas diagonais (vermelho/preto/branco).
- Produtos: 12 rosas R$225 · 12 girassóis R$185 · hortênsia R$125 · 12 rosas + coração Lindt R$330 · 7 colombianas + balão R$241 · orquídea azul R$410 / branca na taça R$550 · cesta café da manhã R$365 (conferir no site).
- Contato: WhatsApp (11) 98115-1001 · televendas (11) 3739-0404 · Av. Dr. Guilherme Dumont Vilares, 2013 – Morumbi · eliteflores.com.br. Slogan "Flores que encantam...".

### 46 — Thais² Flores e Decorações (@thaisflores02, Campo Limpo/SP) — `46-cliente-thais-flores`
- Reels 28s motion graphics com fotos/legendas do Instagram + preços do catálogo do WhatsApp (lírios R$250, café da manhã a partir de R$145, gérbera R$50, begônia R$60, antúrio R$70, orquídeas a partir de R$150).
- Identidade do logo: creme, moldura geométrica dourada (hexágonos desenhados), anel roxo, Great Vibes + Poppins; fotos dentro de hexágono; transição hexágono crescendo; vinheta + grão.
- Ale pediu "bem profissional": girassóis vetoriais (clip-art) trocados por brilhos dourados finos. Slogan "Transformamos flores em sentimentos!", entrega SP e região, Estr. de Itapecerica 1746, (11) 91500-6171.
