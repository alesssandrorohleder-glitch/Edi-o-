import React from 'react';
import {AbsoluteFill, Audio, Easing, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Inter';
import {brand, money} from './brand';
import {Icon} from './icons';

const {fontFamily} = loadFont('normal', {weights: ['400', '500', '600', '700'], subsets: ['latin']});
const C = brand.colors;

// ---------------- layout ----------------
// Celular centralizado dentro da área segura do Reels (250px topo / 350px rodapé)
const PHONE = {w: 700, h: 1320, x: 190, y: 250, bezel: 16};
const SCR = {w: PHONE.w - PHONE.bezel * 2, h: PHONE.h - PHONE.bezel * 2, x: PHONE.x + PHONE.bezel, y: PHONE.y + PHONE.bezel};
const toCanvas = (sx: number, sy: number) => ({x: SCR.x + sx, y: SCR.y + sy});

// ---------------- timeline (frames @30fps) ----------------
const T = {
  splashOut: 82,
  home: 92,
  tapCard: 298,
  expand: 304,
  chart: 345,
  tapButton: 468,
  sheetOpen: 474,
  keys: [512, 536, 566],
  tapConfirm: 598,
  sheetClose: 604,
  success: 612,
  overlayOut: 682,
  update: 690,
  notif: 698,
  exit: 750,
  final: 810,
};

// ---------------- helpers ----------------
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = Easing.bezier(0.33, 1, 0.68, 1);
const easeIO = Easing.inOut(Easing.cubic);
const useSpring = (start: number, config: any = {damping: 18, mass: 0.8, stiffness: 120}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return frame < start ? 0 : spring({frame: frame - start, fps, config});
};
const fadeUp = (frame: number, start: number, dist = 30, dur = 18) => {
  const k = interpolate(frame, [start, start + dur], [0, 1], {...clamp, easing: ease});
  return {opacity: k, transform: `translateY(${(1 - k) * dist}px)`};
};
// Feedback de toque: encolhe para 0.96 e volta
const press = (frame: number, tap: number) =>
  interpolate(frame, [tap - 4, tap, tap + 8], [1, 0.96, 1], {...clamp, easing: easeIO});

const base: React.CSSProperties = {fontFamily, color: C.text, fontVariantNumeric: 'tabular-nums'};

// ---------------- background ----------------
const Background: React.FC = () => {
  const f = useCurrentFrame();
  const gx = 540 + Math.sin(f / 90) * 180;
  const gy = 900 + Math.cos(f / 120) * 220;
  return (
    <AbsoluteFill style={{background: '#050506'}}>
      <div
        style={{
          position: 'absolute', left: gx - 450, top: gy - 450, width: 900, height: 900, borderRadius: '50%',
          background: `radial-gradient(circle, ${C.accent}2E 0%, ${C.accent}10 40%, transparent 70%)`, filter: 'blur(80px)',
        }}
      />
    </AbsoluteFill>
  );
};

// ---------------- small UI pieces ----------------
const Bar: React.FC<{pct: number; h?: number}> = ({pct, h = 16}) => (
  <div style={{height: h, borderRadius: h, background: C.line, overflow: 'hidden'}}>
    <div style={{width: `${pct}%`, height: '100%', borderRadius: h, background: C.accent}} />
  </div>
);

const pctOf = (g: {saved: number; target: number}) => Math.floor((g.saved / g.target) * 100);

// ---------------- splash ----------------
const Splash: React.FC = () => {
  const f = useCurrentFrame();
  const s = useSpring(14, {damping: 12, stiffness: 140});
  const word = interpolate(f, [24, 42], [0, 1], {...clamp, easing: ease});
  const out = interpolate(f, [T.splashOut, T.splashOut + 12], [1, 0], {...clamp, easing: easeIO});
  return (
    <AbsoluteFill style={{background: C.bg, alignItems: 'center', justifyContent: 'center', opacity: out}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 24, transform: `scale(${0.9 + out * 0.1})`}}>
        <div style={{width: 110, height: 110, borderRadius: 34, background: C.accent, transform: `scale(${s})`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          {/* símbolo: pulso */}
          <svg width={70} height={70} viewBox="0 0 24 24" fill="none">
            <path d="M2 12h5l2-5 4 10 2-5h7" stroke={C.accentInk} strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round"
              pathLength={1} strokeDasharray={1} strokeDashoffset={1 - interpolate(f, [20, 44], [0, 1], {...clamp, easing: ease})} />
          </svg>
        </div>
        <div style={{...base, fontSize: 84, fontWeight: 700, letterSpacing: -2, opacity: word, transform: `translateX(${(1 - word) * -20}px)`}}>
          {brand.name}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------- home ----------------
const GoalCard: React.FC<{g: any; i: number; style?: React.CSSProperties; hideContent?: boolean}> = ({g, i, style, hideContent}) => (
  <div style={{position: 'absolute', left: 24, top: 600 + i * 160, width: 620, height: 140, borderRadius: 32, background: C.card, ...style}}>
    {!hideContent && (
      <>
        <div style={{position: 'absolute', left: 28, top: 28, width: 84, height: 84, borderRadius: 24, background: `${C.accent}1F`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <Icon name={g.icon} size={46} color={C.accent} />
        </div>
        <div style={{...base, position: 'absolute', left: 136, top: 22, fontSize: 42, fontWeight: 600}}>{g.name}</div>
        <div style={{...base, position: 'absolute', left: 136, top: 74, fontSize: 40, color: C.muted}}>{money(g.saved)}</div>
        <div style={{...base, position: 'absolute', right: 32, top: 44, fontSize: 44, fontWeight: 700, color: C.accent}}>{pctOf(g)}%</div>
      </>
    )}
  </div>
);

const Home: React.FC<{cardPressScale: number; hideCard: boolean}> = ({cardPressScale, hideCard}) => {
  const f = useCurrentFrame();
  const t0 = T.home;
  const count = interpolate(f, [t0 + 14, t0 + 74], [0, brand.home.total], {...clamp, easing: Easing.out(Easing.cubic)});
  const barK = useSpring(t0 + 30, {damping: 20, stiffness: 70});
  const yearPct = Math.floor((brand.home.total / brand.home.yearGoal) * 100);
  return (
    <AbsoluteFill style={{background: C.bg}}>
      <div style={{...base, position: 'absolute', left: 40, top: 70, fontSize: 48, fontWeight: 700, ...fadeUp(f, t0 + 2)}}>
        {brand.home.greeting} {brand.user.name}
      </div>
      <div style={{position: 'absolute', right: 40, top: 62, width: 76, height: 76, borderRadius: 38, background: C.card, display: 'flex', alignItems: 'center', justifyContent: 'center', ...fadeUp(f, t0 + 6)}}>
        <span style={{...base, fontSize: 40, fontWeight: 600, color: C.accent}}>{brand.user.initial}</span>
      </div>

      <div style={{position: 'absolute', left: 24, top: 170, width: 620, height: 330, borderRadius: 36, background: C.card, padding: 36, boxSizing: 'border-box', ...fadeUp(f, t0 + 8, 40, 22)}}>
        <div style={{...base, fontSize: 40, color: C.muted}}>{brand.home.totalLabel}</div>
        <div style={{...base, fontSize: 96, fontWeight: 700, letterSpacing: -2, marginTop: 8, lineHeight: 1.1}}>{money(count)}</div>
        <div style={{marginTop: 26}}><Bar pct={yearPct * barK} /></div>
        <div style={{...base, fontSize: 40, color: C.muted, marginTop: 18}}>
          <span style={{color: C.accent, fontWeight: 700}}>{Math.round(yearPct * barK)}%</span> {brand.home.yearGoalLabel}
        </div>
      </div>

      <div style={{...base, position: 'absolute', left: 40, top: 528, fontSize: 44, fontWeight: 700, ...fadeUp(f, t0 + 40)}}>{brand.home.goalsTitle}</div>

      {brand.goals.map((g, i) => {
        const k = useSpring(t0 + 52 + i * 10, {damping: 16, stiffness: 110});
        const isTarget = i === brand.detail.goalIndex;
        return (
          <GoalCard key={i} g={g} i={i} hideContent={isTarget && hideCard}
            style={{opacity: isTarget && hideCard ? 0 : k, transform: `translateY(${(1 - k) * 80}px) scale(${isTarget ? cardPressScale : 1})`}} />
        );
      })}

      {/* tab bar */}
      <div style={{position: 'absolute', left: 24, top: 1150, width: 620, height: 104, borderRadius: 52, background: C.card, display: 'flex', alignItems: 'center', justifyContent: 'space-around', ...fadeUp(f, t0 + 70)}}>
        {['home', 'chart', 'plus', 'user'].map((n, i) => (
          <Icon key={n} name={n} size={44} color={i === 0 ? C.accent : C.muted} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ---------------- detail (shared element) ----------------
const Chart: React.FC<{progress: number}> = ({progress}) => {
  const W = 548, H = 280, vals = brand.detail.values, max = Math.max(...vals) * 1.1;
  const pts = vals.map((v, i) => [20 + (i / (vals.length - 1)) * (W - 40), H - (v / max) * H]);
  const d = pts.map((p, i) => `${i ? 'L' : 'M'}${p[0]},${p[1]}`).join(' ');
  const area = `${d} L${pts[pts.length - 1][0]},${H} L${pts[0][0]},${H} Z`;
  const lastIdx = Math.min(vals.length - 1, Math.floor(progress * (vals.length - 1) + 0.001));
  return (
    <svg width={W} height={H + 10} style={{overflow: 'visible'}}>
      <defs>
        <linearGradient id="ga" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={C.accent} stopOpacity={0.35} />
          <stop offset="1" stopColor={C.accent} stopOpacity={0} />
        </linearGradient>
        <clipPath id="reveal"><rect x={0} y={-20} width={W * progress} height={H + 40} /></clipPath>
      </defs>
      {[0.25, 0.5, 0.75, 1].map((g) => (
        <line key={g} x1={0} x2={W} y1={H * g} y2={H * g} stroke={C.line} strokeWidth={2} />
      ))}
      <path d={area} fill="url(#ga)" clipPath="url(#reveal)" />
      <path d={d} fill="none" stroke={C.accent} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - progress} />
      {pts.map((p, i) => i <= lastIdx && progress > 0 && (
        <circle key={i} cx={p[0]} cy={p[1]} r={i === lastIdx ? 11 : 7} fill={i === lastIdx ? C.accent : C.bg} stroke={C.accent} strokeWidth={4} />
      ))}
    </svg>
  );
};

const Detail: React.FC<{expand: number; buttonScale: number; saved: number; pctSpring: number}> = ({expand, buttonScale, saved, pctSpring}) => {
  const f = useCurrentFrame();
  const g = brand.goals[brand.detail.goalIndex];
  const i = brand.detail.goalIndex;
  // retângulo do card (home) -> tela inteira
  const from = {x: 24, y: 600 + i * 160, w: 620, h: 140, r: 32};
  const to = {x: 0, y: 0, w: SCR.w, h: SCR.h, r: 54};
  const L = (a: number, b: number) => a + (b - a) * expand;
  const content = interpolate(expand, [0.55, 1], [0, 1], clamp);
  const chartP = interpolate(f, [T.chart, T.chart + 70], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)});
  const pct = pctSpring;
  // o cabeçalho some enquanto a notificação está na tela (sem sobreposição)
  const headerFade = interpolate(f, [T.notif - 2, T.notif + 8, T.exit - 8, T.exit + 2], [1, 0, 0, 1], clamp);
  return (
    <div style={{position: 'absolute', left: L(from.x, to.x), top: L(from.y, to.y), width: L(from.w, to.w), height: L(from.h, to.h), borderRadius: L(from.r, to.r), background: C.card, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, background: C.bg, opacity: content}} />
      <div style={{position: 'absolute', left: 0, top: 0, width: SCR.w, height: SCR.h, opacity: content, transform: `translateY(${(1 - content) * 30}px)`}}>
        <div style={{opacity: headerFade}}>
        <div style={{position: 'absolute', left: 32, top: 70}}><Icon name="back" size={56} color={C.text} /></div>
        <div style={{...base, position: 'absolute', left: 110, top: 66, fontSize: 56, fontWeight: 700}}>{g.name}</div>
        <div style={{position: 'absolute', right: 40, top: 62, width: 76, height: 76, borderRadius: 24, background: `${C.accent}1F`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <Icon name={g.icon} size={44} color={C.accent} />
        </div>
        </div>
        <div style={{...base, position: 'absolute', left: 40, top: 168, fontSize: 104, fontWeight: 700, letterSpacing: -3}}>{money(saved)}</div>
        <div style={{...base, position: 'absolute', left: 40, top: 300, fontSize: 40, color: C.muted}}>{brand.detail.of} {money(g.target)}</div>
        <div style={{...base, position: 'absolute', right: 40, top: 296, fontSize: 48, fontWeight: 700, color: C.accent}}>{Math.floor(pct + 0.05)}%</div>
        <div style={{position: 'absolute', left: 40, top: 370, width: SCR.w - 80}}><Bar pct={pct} h={20} /></div>

        <div style={{position: 'absolute', left: 24, top: 432, width: 620, height: 520, borderRadius: 36, background: C.card}}>
          <div style={{...base, position: 'absolute', left: 36, top: 32, fontSize: 40, fontWeight: 600}}>{brand.detail.chartTitle}</div>
          <div style={{position: 'absolute', left: 36, top: 120}}><Chart progress={chartP} /></div>
          {brand.detail.months.map((m, k) => {
            const n = brand.detail.months.length;
            // mostra rótulos alternados para não encostarem (texto mínimo de 40px)
            if (k % 2 !== 0 && k !== n - 1) return null;
            const px = 36 + 20 + (k / (n - 1)) * (548 - 40);
            return (
              <span key={m + k} style={{...base, position: 'absolute', left: px - 60, top: 440, width: 120, textAlign: 'center', fontSize: 40, color: C.muted, opacity: interpolate(chartP, [k / n, k / n + 0.15], [0.25, 1], clamp)}}>{m}</span>
            );
          })}
        </div>

        <div style={{position: 'absolute', left: 24, top: 1090, width: 620, height: 124, borderRadius: 62, background: C.accent, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 16, transform: `scale(${buttonScale})`}}>
          <Icon name="plus" size={44} color={C.accentInk} stroke={2.6} />
          <span style={{...base, fontSize: 44, fontWeight: 700, color: C.accentInk}}>{brand.detail.saveButton}</span>
        </div>
      </div>
    </div>
  );
};

// ---------------- bottom sheet ----------------
const KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '0', 'del'];
const SHEET_TOP = 300;
const keyCenter = (k: string) => {
  const idx = KEYS.indexOf(k), r = Math.floor(idx / 3), c = idx % 3;
  return {x: 24 + c * 208 + 98, y: SHEET_TOP + 300 + r * 122 + 55};
};
const CONFIRM = {x: SCR.w / 2, y: SHEET_TOP + 855};

const Sheet: React.FC = () => {
  const f = useCurrentFrame();
  const open = useSpring(T.sheetOpen, {damping: 20, stiffness: 130});
  const close = useSpring(T.sheetClose, {damping: 22, stiffness: 140});
  const y = SCR.h * (1 - open) + (SCR.h - SHEET_TOP) * close;
  const typedCount = T.keys.filter((k) => f >= k).length;
  const digits = brand.sheet.amount.slice(0, typedCount);
  const dim = open * (1 - close) * 0.6;
  if (f < T.sheetOpen) return null;
  return (
    <>
      <div style={{position: 'absolute', inset: 0, background: `rgba(0,0,0,${dim})`}} />
      <div style={{position: 'absolute', left: 0, top: SHEET_TOP + y, width: SCR.w, height: SCR.h - SHEET_TOP, background: C.card, borderTopLeftRadius: 48, borderTopRightRadius: 48}}>
        <div style={{position: 'absolute', left: SCR.w / 2 - 40, top: 18, width: 80, height: 8, borderRadius: 4, background: C.line}} />
        <div style={{...base, position: 'absolute', width: '100%', textAlign: 'center', top: 52, fontSize: 44, fontWeight: 600}}>{brand.sheet.title}</div>
        <div style={{...base, position: 'absolute', width: '100%', top: 140, display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: 14}}>
          <span style={{fontSize: 56, fontWeight: 600, color: C.muted}}>R$</span>
          <span style={{fontSize: 112, fontWeight: 700, letterSpacing: -2, color: digits ? C.text : C.line, display: 'flex'}}>
            {(digits || '0').split('').map((d, i) => {
              const k = interpolate(f, [T.keys[i] ?? 0, (T.keys[i] ?? 0) + 8], [0, 1], {...clamp, easing: ease});
              return <span key={i} style={{display: 'inline-block', transform: `translateY(${(1 - (digits ? k : 1)) * 30}px) scale(${0.7 + 0.3 * (digits ? k : 1)})`, opacity: digits ? k : 1}}>{d}</span>;
            })}
            <span style={{width: 6, height: 100, background: C.accent, marginLeft: 8, alignSelf: 'center', opacity: Math.floor(f / 15) % 2 ? 0 : 1}} />
          </span>
        </div>
        {KEYS.map((k, idx) => {
          const r = Math.floor(idx / 3), c = idx % 3;
          const tapIdx = ['2', '5', '0'].indexOf(k);
          const s = tapIdx >= 0 ? press(f, T.keys[tapIdx]) : 1;
          const lit = tapIdx >= 0 ? interpolate(f, [T.keys[tapIdx] - 2, T.keys[tapIdx], T.keys[tapIdx] + 10], [0, 1, 0], clamp) : 0;
          return (
            <div key={k} style={{position: 'absolute', left: 24 + c * 208, top: 300 + r * 122, width: 196, height: 110, borderRadius: 28, background: lit > 0 ? `rgba(184,243,74,${0.12 + 0.2 * lit})` : '#22252E', display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${s})`}}>
              {k === 'del' ? <Icon name="del" size={48} color={C.text} /> : <span style={{...base, fontSize: 52, fontWeight: 600}}>{k}</span>}
            </div>
          );
        })}
        <div style={{position: 'absolute', left: 24, top: 800, width: 620, height: 110, borderRadius: 55, background: C.accent, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${press(f, T.tapConfirm)})`}}>
          <span style={{...base, fontSize: 44, fontWeight: 700, color: C.accentInk}}>{brand.sheet.confirm}</span>
        </div>
      </div>
    </>
  );
};

// ---------------- success ----------------
const Success: React.FC = () => {
  const f = useCurrentFrame();
  const pop = useSpring(T.success + 4, {damping: 10, stiffness: 150});
  if (f < T.success || f > T.overlayOut + 20) return null;
  const inK = interpolate(f, [T.success, T.success + 12], [0, 1], {...clamp, easing: ease});
  const outK = interpolate(f, [T.overlayOut, T.overlayOut + 14], [1, 0], {...clamp, easing: easeIO});
  const ring = interpolate(f, [T.success + 4, T.success + 28], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const check = interpolate(f, [T.success + 20, T.success + 38], [0, 1], {...clamp, easing: ease});
  const cx = SCR.w / 2, cy = 520;
  return (
    <div style={{position: 'absolute', inset: 0, background: `rgba(14,15,19,${0.88 * inK})`, opacity: outK}}>
      <svg width={SCR.w} height={SCR.h} style={{position: 'absolute', inset: 0}}>
        <g transform={`translate(${cx},${cy}) scale(${0.8 + 0.2 * pop})`}>
          <circle r={120} fill={`${C.accent}14`} />
          <circle r={120} fill="none" stroke={C.accent} strokeWidth={10} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - ring} transform="rotate(-90)" />
          <path d="M-50,2 L-14,38 L54,-34" fill="none" stroke={C.accent} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - check} />
        </g>
      </svg>
      <div style={{...base, position: 'absolute', width: '100%', textAlign: 'center', top: 700, fontSize: 52, fontWeight: 700, ...fadeUp(f, T.success + 30)}}>{brand.success.title}</div>
      <div style={{...base, position: 'absolute', width: '100%', textAlign: 'center', top: 780, fontSize: 44, color: C.accent, fontWeight: 600, ...fadeUp(f, T.success + 36)}}>+ {money(Number(brand.sheet.amount))}</div>
    </div>
  );
};

const Confetti: React.FC = () => {
  const f = useCurrentFrame();
  const t = f - (T.success + 24);
  if (t < 0 || t > 100) return null;
  return (
    <>
      {new Array(36).fill(0).map((_, i) => {
        const a = random(`a${i}`) * Math.PI * 2;
        const v = 6 + random(`v${i}`) * 9;
        const x = SCR.w / 2 + Math.cos(a) * (140 + v * t);
        const y = 520 + Math.sin(a) * (140 + v * t * 0.8) + 0.09 * t * t;
        const o = interpolate(t, [0, 6, 70, 100], [0, 1, 1, 0], clamp);
        const w = 10 + random(`w${i}`) * 8;
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: w, height: w * 0.45, borderRadius: 3, background: i % 3 === 0 ? C.text : C.accent, opacity: o * 0.9, transform: `rotate(${t * (4 + random(`r${i}`) * 8)}deg)`}} />;
      })}
    </>
  );
};

const Notification: React.FC<{pct: number}> = ({pct}) => {
  const f = useCurrentFrame();
  const k = useSpring(T.notif, {damping: 16, stiffness: 120});
  const out = interpolate(f, [T.exit - 8, T.exit + 4], [0, 1], {...clamp, easing: easeIO});
  if (f < T.notif) return null;
  return (
    <div style={{position: 'absolute', left: 24, top: 76 - (1 - k) * 12 - out * 12, opacity: Math.min(1, k * 1.4) * (1 - out), transformOrigin: '50% 0%', transform: `scale(${0.94 + 0.06 * Math.min(1, k)})`, width: 620, height: 112, borderRadius: 36, background: 'rgba(34,37,46,0.96)', border: `2px solid ${C.line}`, boxShadow: '0 20px 50px rgba(0,0,0,.5)', display: 'flex', alignItems: 'center', gap: 24, padding: '0 28px', boxSizing: 'border-box'}}>
      <div style={{width: 88, height: 88, borderRadius: 26, background: C.accent, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
        <Icon name="lock" size={50} color={C.accentInk} stroke={2.4} />
      </div>
      <div>
        <div style={{...base, fontSize: 40, fontWeight: 700, lineHeight: 1.15}}>{brand.notifTemplate(pct)}</div>
        <div style={{...base, fontSize: 40, color: C.muted, lineHeight: 1.15}}>{brand.goals[brand.detail.goalIndex].name} · {brand.success.notifSub}</div>
      </div>
    </div>
  );
};

// ---------------- cursor ----------------
type K = [number, number, number, number]; // frame, x, y, opacity (coords da tela do app)
const cardC = {x: 334, y: 600 + brand.detail.goalIndex * 160 + 70};
const btnC = {x: 334, y: 1090 + 62};
const K2 = keyCenter('2'), K5 = keyCenter('5'), K0 = keyCenter('0');
const CURSOR: K[] = [
  [262, 560, 1180, 0], [270, 540, 1120, 1], [294, cardC.x, cardC.y, 1], [312, cardC.x, cardC.y, 1], [322, cardC.x + 60, cardC.y + 60, 0],
  [438, 520, 1000, 0], [446, 480, 1050, 1], [464, btnC.x, btnC.y, 1], [480, btnC.x, btnC.y, 1],
  [508, K2.x, K2.y, 1], [518, K2.x, K2.y, 1], [532, K5.x, K5.y, 1], [542, K5.x, K5.y, 1], [562, K0.x, K0.y, 1], [572, K0.x, K0.y, 1],
  [594, CONFIRM.x, CONFIRM.y, 1], [604, CONFIRM.x, CONFIRM.y, 1], [616, CONFIRM.x + 40, CONFIRM.y + 80, 0],
];
const TAPS = [T.tapCard, T.tapButton, ...T.keys, T.tapConfirm];

const Cursor: React.FC = () => {
  const f = useCurrentFrame();
  let i = CURSOR.findIndex((k) => k[0] > f);
  if (i <= 0) return null;
  const a = CURSOR[i - 1], b = CURSOR[i];
  const k = easeIO((f - a[0]) / (b[0] - a[0]));
  const sx = a[1] + (b[1] - a[1]) * k, sy = a[2] + (b[2] - a[2]) * k, o = a[3] + (b[3] - a[3]) * k;
  if (o <= 0.01) return null;
  const tap = TAPS.find((t) => f >= t - 4 && f <= t + 16);
  const squeeze = tap !== undefined ? interpolate(f, [tap - 4, tap, tap + 8], [1, 0.78, 1], {...clamp, easing: easeIO}) : 1;
  const ring = tap !== undefined ? interpolate(f, [tap, tap + 16], [0, 1], {...clamp, easing: ease}) : 0;
  return (
    <>
      {tap !== undefined && f >= tap && (
        <div style={{position: 'absolute', left: sx - 44, top: sy - 44, width: 88, height: 88, borderRadius: 44, border: '4px solid rgba(255,255,255,0.7)', opacity: (1 - ring) * o, transform: `scale(${1 + ring * 1.4})`}} />
      )}
      <div style={{position: 'absolute', left: sx - 40, top: sy - 40, width: 80, height: 80, borderRadius: 40, background: 'rgba(255,255,255,0.35)', border: '3px solid rgba(255,255,255,0.75)', boxShadow: '0 6px 24px rgba(0,0,0,0.35)', opacity: o, transform: `scale(${squeeze})`}} />
    </>
  );
};

// ---------------- phone ----------------
const Phone: React.FC = () => {
  const f = useCurrentFrame();
  const enter = useSpring(0, {damping: 16, mass: 1, stiffness: 70});
  const exitK = interpolate(f, [T.exit, T.final], [0, 1], {...clamp, easing: Easing.in(Easing.cubic)});
  const exitS = useSpring(T.exit, {damping: 200, stiffness: 60});
  const ty = (1 - enter) * 1500;
  const rx = (1 - enter) * 28 + exitS * -6;
  const ry = (1 - enter) * -18 + exitS * 18;
  const rz = exitS * -8;
  const sc = 1 - exitS * 0.5;
  const op = 1 - exitK;

  const expand = useSpring(T.expand, {damping: 20, stiffness: 110});
  const g = brand.goals[brand.detail.goalIndex];
  const amount = Number(brand.sheet.amount);
  const savedNow = interpolate(f, [T.update, T.update + 24], [g.saved, g.saved + amount], {...clamp, easing: Easing.out(Easing.cubic)});
  const pctFrom = (g.saved / g.target) * 100, pctTo = ((g.saved + amount) / g.target) * 100;
  const up = useSpring(T.update + 2, {damping: 11, stiffness: 120});
  const pctNow = pctFrom + (pctTo - pctFrom) * up;
  const finalPct = Math.round(pctTo);

  return (
    <AbsoluteFill style={{perspective: 2200}}>
      <div style={{position: 'absolute', left: PHONE.x, top: PHONE.y, width: PHONE.w, height: PHONE.h, opacity: op,
        transform: `translateY(${ty}px) rotateX(${rx}deg) rotateY(${ry}deg) rotateZ(${rz}deg) scale(${sc})`, transformStyle: 'preserve-3d'}}>
        <div style={{position: 'absolute', inset: 0, borderRadius: 86, background: 'linear-gradient(145deg,#2A2C33,#141519)', boxShadow: `0 60px 120px rgba(0,0,0,0.6), 0 0 0 2px #34363E, inset 0 0 0 2px #0A0A0C`}} />
        <div style={{position: 'absolute', left: PHONE.bezel, top: PHONE.bezel, width: SCR.w, height: SCR.h, borderRadius: 70, overflow: 'hidden', background: C.bg}}>
          {f >= T.home - 2 && <Home cardPressScale={press(f, T.tapCard)} hideCard={f >= T.expand} />}
          {f >= T.expand && <Detail expand={expand} buttonScale={press(f, T.tapButton)} saved={savedNow} pctSpring={pctNow} />}
          <Sheet />
          <Success />
          <Confetti />
          <Notification pct={finalPct} />
          {f < T.splashOut + 14 && <Splash />}
          {/* dynamic island */}
          <div style={{position: 'absolute', left: SCR.w / 2 - 90, top: 18, width: 180, height: 46, borderRadius: 23, background: '#000'}} />
        </div>
      </div>
      {/* cursor fica acima da tela, em coordenadas do canvas */}
      <div style={{position: 'absolute', left: SCR.x, top: SCR.y, width: SCR.w, height: SCR.h, opacity: op}}>
        <Cursor />
      </div>
    </AbsoluteFill>
  );
};

// ---------------- final card ----------------
const Word: React.FC<{w: string; start: number; color?: string; size: number; weight?: number}> = ({w, start, color = C.text, size, weight = 700}) => {
  const k = useSpring(start, {damping: 16, stiffness: 130});
  return <span style={{display: 'inline-block', marginRight: size * 0.26, opacity: k, transform: `translateY(${(1 - k) * 40}px)`, color, fontSize: size, fontWeight: weight}}>{w}</span>;
};

const Final: React.FC = () => {
  const f = useCurrentFrame();
  const s = T.final;
  const svcK = brand.final.services.map((_, i) => useSpring(s + 52 + i * 7, {damping: 18, stiffness: 140}));
  if (f < T.final - 2) return null;
  const bgIn = interpolate(f, [s - 2, s + 10], [0, 1], clamp);
  const l1 = brand.final.line1.split(' ');
  const l2 = brand.final.line2;
  const listStart = s + 52;
  const ctaStart = s + 96;
  return (
    <AbsoluteFill style={{...base, opacity: bgIn}}>
      <div style={{position: 'absolute', left: 90, top: 330, width: 900}}>
        <div style={{lineHeight: 1.2}}>{l1.map((w, i) => <Word key={i} w={w} start={s + 2 + i * 4} size={56} weight={500} color={C.muted} />)}</div>
        <div style={{lineHeight: 1.12, marginTop: 28}}>
          {l2.map((w, i) => <Word key={i} w={w} start={s + 24 + i * 5} size={92} color={w === brand.final.highlightWord ? C.accent : C.text} />)}
        </div>
      </div>
      <div style={{position: 'absolute', left: 90, top: 820, width: 900}}>
        {brand.final.services.map((it, i) => {
          const k = svcK[i];
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: 28, height: 104, opacity: k, transform: `translateX(${(1 - k) * -50}px)`}}>
              <div style={{width: 76, height: 76, borderRadius: 22, background: `${C.accent}1F`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                <Icon name={it.icon} size={44} color={C.accent} progress={interpolate(f, [listStart + i * 7, listStart + i * 7 + 16], [0, 1], {...clamp, easing: ease})} />
              </div>
              <span style={{fontSize: 46, fontWeight: 500}}>{it.label}</span>
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', left: 90, top: 1310, width: 900}}>
        <div style={{fontSize: 60, fontWeight: 700, ...fadeUp(f, ctaStart, 30, 16)}}>{brand.final.cta}</div>
        <div style={{fontSize: 60, fontWeight: 700, color: C.accent, marginTop: 10, ...fadeUp(f, ctaStart + 8, 30, 16)}}>{brand.handle}</div>
      </div>
    </AbsoluteFill>
  );
};

export const PortfolioUI: React.FC = () => (
  <AbsoluteFill style={{background: '#050506'}}>
    {brand.audio ? <Audio src={staticFile(brand.audio)} /> : null}
    <Background />
    <Phone />
    <Final />
  </AbsoluteFill>
);
