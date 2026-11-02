// ============================================================
//  TEMPLATE DE MARCA — troque tudo aqui para reaproveitar
//  com outro cliente (cores, nome, textos e números).
// ============================================================
export const brand = {
  name: 'Pulsa',
  handle: '@alecreator_motion',
  // trilha + efeitos sonoros (arquivo dentro da pasta /public). Deixe '' para sem som.
  audio: 'pulsa-audio.wav',

  colors: {
    bg: '#0E0F13',        // fundo
    card: '#1A1C23',      // cards
    accent: '#B8F34A',    // destaque (verde-limão)
    accentInk: '#0E0F13', // texto sobre o destaque
    text: '#F4F4F5',      // texto principal
    muted: '#8A8F98',     // texto secundário
    line: '#2A2D36',      // divisórias / trilho das barras
  },

  user: {name: 'Ana', initial: 'A'},

  home: {
    greeting: 'Olá,',
    totalLabel: 'Total guardado',
    total: 12480,
    yearGoal: 20000,
    yearGoalLabel: 'da meta do ano',
    goalsTitle: 'Suas metas',
  },

  // icon: 'plane' | 'car' | 'shield'
  goals: [
    {name: 'Viagem', icon: 'plane', saved: 3730, target: 8000},
    {name: 'Carro', icon: 'car', saved: 6250, target: 10000},
    {name: 'Reserva', icon: 'shield', saved: 2500, target: 5000},
  ],

  detail: {
    goalIndex: 1, // qual card o cursor toca (1 = Carro)
    of: 'de',
    chartTitle: 'Depósitos mensais',
    months: ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN'],
    values: [800, 1900, 2600, 3800, 5000, 6250],
    saveButton: 'Guardar dinheiro',
  },

  sheet: {title: 'Quanto guardar?', amount: '250', confirm: 'Confirmar'},

  success: {title: 'Dinheiro guardado!', notifSub: 'agora'},
  // a notificação usa: `Meta ${porcentagem}% concluída`
  notifTemplate: (pct: number) => `Meta ${pct}% concluída`,

  final: {
    line1: 'Essa marca não existe.',
    line2: ['Essa', 'estética', 'pode', 'ser', 'sua.'],
    highlightWord: 'sua.',
    // icon: 'film' | 'play' | 'phone' | 'spark'
    services: [
      {icon: 'film', label: 'Reels animados'},
      {icon: 'play', label: 'Vídeos explicativos'},
      {icon: 'phone', label: 'UI animada e demo de app'},
      {icon: 'spark', label: 'Animação de logo'},
    ],
    cta: 'Me chama no direct',
  },
};

export const money = (v: number) => 'R$ ' + Math.round(v).toLocaleString('pt-BR');
export type Brand = typeof brand;
