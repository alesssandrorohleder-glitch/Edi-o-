import { interpolate, random } from "remotion";
import { C, CLAMP } from "./theme";

// Gentle wind: two slow sines so neighbouring stalks never move in lockstep.
export const sway = (frame: number, phase: number, amp = 3) =>
  Math.sin(frame / 30 * 1.5 + phase) * amp + Math.sin(frame / 30 * 0.6 + phase * 2.3) * amp * 0.5;

// Big sprout silhouette from the brand card, used as a watermark.
export const LeafMark: React.FC<{ readonly x: number; readonly y: number; readonly scale?: number; readonly rotate?: number; readonly color?: string; readonly opacity?: number }> = ({
  x,
  y,
  scale = 1,
  rotate = 0,
  color = C.white,
  opacity = 0.07,
}) => (
  <g transform={`translate(${x} ${y}) rotate(${rotate}) scale(${scale})`} opacity={opacity} fill={color}>
    <path d="M-30 0 C -60 -180, -40 -360, 30 -520 L 70 -505 C 10 -360, 0 -190, 40 0 Z" />
    <path d="M30 -520 C -160 -640, -130 -900, 90 -1040 C 190 -860, 190 -650, 30 -520 Z" />
    <path d="M10 -300 C 90 -420, 250 -440, 360 -420 C 320 -300, 200 -240, 10 -300 Z" />
  </g>
);

type WheatProps = {
  readonly x: number;
  readonly y: number;
  readonly h: number;
  readonly grow?: number;
  readonly angle?: number;
  readonly color?: string;
  readonly scale?: number;
  readonly grains?: number;
};

// A wheat stalk drawn upward from (x, y). `grow` 0..1: stem first, then the ear fills grain by grain.
export const Wheat: React.FC<WheatProps> = ({ x, y, h, grow = 1, angle = 0, color = C.gold, scale = 1, grains = 14 }) => {
  const stem = h * Math.min(1, grow / 0.55);
  const ear = Math.max(0, (grow - 0.45) / 0.55);
  const gap = 10;
  return (
    <g transform={`translate(${x} ${y}) rotate(${angle}) scale(${scale})`}>
      <path d={`M0 0 Q -8 ${-stem * 0.5} 0 ${-stem}`} stroke={color} strokeWidth={4} fill="none" strokeLinecap="round" />
      {stem > h * 0.4 && (
        <path d={`M-2 ${-h * 0.32} C -30 ${-h * 0.42}, -46 ${-h * 0.55}, -52 ${-h * 0.7} C -30 ${-h * 0.6}, -12 ${-h * 0.5}, -2 ${-h * 0.4} Z`} fill={color} opacity={0.85} />
      )}
      {Array.from({ length: grains }, (_, i) => {
        const t = Math.min(1, Math.max(0, ear * grains - i));
        if (t <= 0) return null;
        const side = i % 2 === 0 ? -1 : 1;
        const gy = -h - 8 - i * gap;
        const s = t * (1 - i / (grains * 2.2));
        return (
          <g key={i} transform={`translate(${side * 7} ${gy}) rotate(${side * 26}) scale(${s})`}>
            <line x1={0} y1={-10} x2={side * 6} y2={-58} stroke={color} strokeWidth={1.6} opacity={0.7} />
            <ellipse rx={6.5} ry={13} fill={color} />
          </g>
        );
      })}
    </g>
  );
};

// Cheap stalk for dense fields; `cut` turns it into stubble.
export const MiniWheat: React.FC<{ readonly x: number; readonly y: number; readonly h: number; readonly angle: number; readonly color: string; readonly cut?: boolean }> = ({
  x,
  y,
  h,
  angle,
  color,
  cut = false,
}) =>
  cut ? (
    <line x1={x} y1={y} x2={x + 1} y2={y - h * 0.14} stroke={color} strokeWidth={2.5} strokeLinecap="round" opacity={0.8} />
  ) : (
    <g transform={`translate(${x} ${y}) rotate(${angle})`}>
      <line x1={0} y1={0} x2={0} y2={-h} stroke={color} strokeWidth={2.5} strokeLinecap="round" />
      <ellipse cx={0} cy={-h - h * 0.17} rx={h * 0.07} ry={h * 0.19} fill={color} />
      <line x1={0} y1={-h - h * 0.3} x2={-h * 0.06} y2={-h - h * 0.55} stroke={color} strokeWidth={1.2} />
      <line x1={0} y1={-h - h * 0.3} x2={h * 0.06} y2={-h - h * 0.55} stroke={color} strokeWidth={1.2} />
    </g>
  );

// Two-leaf sprout, echoing the logo icon.
export const Sprout: React.FC<{ readonly x: number; readonly y: number; readonly s: number; readonly angle?: number }> = ({ x, y, s, angle = 0 }) =>
  s <= 0 ? null : (
    <g transform={`translate(${x} ${y}) rotate(${angle}) scale(${s})`}>
      <path d="M0 0 C -2 -14, 2 -26, 0 -36" stroke={C.mid} strokeWidth={4} fill="none" strokeLinecap="round" />
      <path d="M0 -34 C -10 -52, -34 -56, -44 -48 C -36 -34, -16 -30, 0 -34 Z" fill={C.sprout} />
      <path d="M0 -30 C 8 -50, 30 -60, 42 -54 C 38 -38, 18 -28, 0 -30 Z" fill={C.leaf} />
    </g>
  );

// Close-up wheat ear: 16 tiers of three grains, revealed bottom-up by `shown` (0..48).
export const BigEar: React.FC<{ readonly shown: number }> = ({ shown }) => {
  const tiers = 16;
  return (
    <g>
      <path d="M0 60 C -6 240, 8 420, 0 640" stroke={C.goldDark} strokeWidth={12} fill="none" strokeLinecap="round" />
      {Array.from({ length: tiers }, (_, r) => {
        const y = 30 - r * 44;
        const taper = 1 - r / (tiers * 1.9);
        return [0, 1, 2].map((k) => {
          const idx = r * 3 + k;
          const t = Math.min(1, Math.max(0, shown - idx));
          if (t <= 0) return null;
          const side = k === 0 ? -1 : k === 1 ? 1 : 0;
          const sc = t * taper;
          return (
            <g key={idx} transform={`translate(${side * 26 * taper} ${y - (side === 0 ? 22 : 0)}) rotate(${side * 22}) scale(${sc})`}>
              {side !== 0 && <line x1={side * 4} y1={-30} x2={side * 46} y2={-210} stroke={C.goldDark} strokeWidth={3} strokeLinecap="round" opacity={0.75} />}
              <ellipse rx={side === 0 ? 19 : 22} ry={side === 0 ? 33 : 38} fill={side === 0 ? C.goldDark : C.gold} />
              <path d="M0 -30 C 6 -10, 6 10, 0 30" stroke={C.goldDark} strokeWidth={2.5} fill="none" opacity={0.5} />
            </g>
          );
        });
      })}
    </g>
  );
};

// Corn cob seen from the front: 8 visible kernel columns (the hidden back holds the other 8 of 16 rows).
export const CornCob: React.FC<{ readonly frame: number; readonly start: number }> = ({ frame, start }) => {
  const H = 720;
  const W = 250;
  const rows = 22;
  const cols = 8;
  const halfW = (v: number) => (W / 2) * Math.sqrt(Math.max(0, 1 - Math.pow(Math.abs(v), 5))) * (1 - 0.16 * (1 - v) / 2);
  const husk = interpolate(frame, [start - 30, start], [0, 1], CLAMP);
  return (
    <g>
      <path d={`M-30 ${H / 2 + 40} C -260 ${H / 2 - 40}, -250 ${-H / 4}, -170 ${-H / 2 + 60} C -150 ${-H / 6}, -130 ${H / 4}, 20 ${H / 2 + 20} Z`} fill={C.leaf} opacity={husk} />
      <path d={`M30 ${H / 2 + 40} C 260 ${H / 2 - 30}, 250 ${-H / 4}, 180 ${-H / 2 + 120} C 150 ${-H / 6}, 120 ${H / 4}, -20 ${H / 2 + 20} Z`} fill={C.mid} opacity={husk} />
      <ellipse cx={0} cy={0} rx={W / 2 - 4} ry={H / 2 - 6} fill="#c99a35" />
      {Array.from({ length: cols }, (_, j) => {
        const th = (-78 + j * (156 / (cols - 1))) * (Math.PI / 180);
        return Array.from({ length: rows }, (_, r) => {
          const v = -0.93 + r * (1.86 / (rows - 1));
          const hw = halfW(v);
          const appear = start + j * 9 + r * 1.1;
          const t = interpolate(frame, [appear, appear + 8], [0, 1], CLAMP);
          if (t <= 0) return null;
          const kw = (hw * 2 / cols) * 1.18 * Math.cos(th) * t;
          const kh = (H / rows) * 0.86 * t;
          const light = Math.cos(th);
          return (
            <rect
              key={`${j}-${r}`}
              x={Math.sin(th) * hw - kw / 2}
              y={v * (H / 2) - kh / 2}
              width={kw}
              height={kh}
              rx={Math.min(kw, kh) * 0.35}
              fill={`rgb(${Math.round(196 + 46 * light)}, ${Math.round(140 + 52 * light)}, ${Math.round(40 + 40 * light)})`}
            />
          );
        });
      })}
      <path d={`M-20 ${-H / 2 + 10} C -40 ${-H / 2 - 60}, -10 ${-H / 2 - 110}, 30 ${-H / 2 - 150}`} stroke="#d8c08a" strokeWidth={4} fill="none" opacity={husk} />
      <path d={`M0 ${-H / 2 + 10} C 10 ${-H / 2 - 70}, 40 ${-H / 2 - 100}, 70 ${-H / 2 - 120}`} stroke="#c9ad74" strokeWidth={4} fill="none" opacity={husk} />
    </g>
  );
};

const Wheel: React.FC<{ readonly x: number; readonly r: number; readonly rot: number }> = ({ x, r, rot }) => (
  <g transform={`translate(${x} ${-r})`}>
    <circle r={r} fill="#1d2a24" />
    <circle r={r * 0.58} fill={C.gold} />
    <g transform={`rotate(${rot})`}>
      {[0, 72, 144, 216, 288].map((a) => (
        <line key={a} x1={0} y1={0} x2={Math.cos((a * Math.PI) / 180) * r * 0.5} y2={Math.sin((a * Math.PI) / 180) * r * 0.5} stroke={C.goldDark} strokeWidth={6} />
      ))}
    </g>
    <circle r={r * 0.16} fill={C.dark} />
  </g>
);

// Combine harvester facing right; ground at y = 0; `dist` = distance travelled (drives wheels and reel).
export const Harvester: React.FC<{ readonly dist: number }> = ({ dist }) => {
  const deg = (r: number) => ((dist / r) * 180) / Math.PI;
  return (
    <g>
      <path d="M70 -350 L-150 -420" stroke={C.dark} strokeWidth={22} strokeLinecap="round" />
      <path d="M-150 -420 L-160 -380" stroke={C.dark} strokeWidth={16} strokeLinecap="round" />
      <path d="M40 -320 L70 -395 L300 -395 L320 -320 Z" fill={C.dark} />
      <path d="M0 -100 L0 -300 Q0 -322 22 -322 L405 -322 L440 -230 L440 -100 Z" fill={C.brand} />
      <rect x={0} y={-222} width={440} height={14} fill={C.white} opacity={0.9} />
      <rect x={250} y={-455} width={14} height={70} rx={4} fill={C.deep} />
      <path d="M300 -322 L312 -448 L424 -448 L444 -322 Z" fill={C.dark} />
      <path d="M318 -334 L327 -434 L410 -434 L428 -334 Z" fill="#cfe3d6" opacity={0.9} />
      <path d="M430 -250 L570 -150 L570 -92 L430 -150 Z" fill={C.dark} />
      <path d="M520 -112 L720 -112 L742 -28 L500 -28 Z" fill={C.gold} />
      <path d="M500 -28 L742 -28" stroke={C.goldDark} strokeWidth={8} strokeDasharray="10 8" />
      <g transform={`translate(624 -150) rotate(${deg(70)})`}>
        <circle r={70} fill="none" stroke={C.white} strokeWidth={4} opacity={0.85} />
        {[0, 60, 120, 180, 240, 300].map((a) => {
          const ca = Math.cos((a * Math.PI) / 180);
          const sa = Math.sin((a * Math.PI) / 180);
          return (
            <g key={a}>
              <line x1={0} y1={0} x2={ca * 70} y2={sa * 70} stroke={C.white} strokeWidth={4} opacity={0.85} />
              <line x1={ca * 70 - sa * 14} y1={sa * 70 + ca * 14} x2={ca * 70 + sa * 14} y2={sa * 70 - ca * 14} stroke={C.white} strokeWidth={8} strokeLinecap="round" />
            </g>
          );
        })}
      </g>
      <Wheel x={90} r={62} rot={deg(62)} />
      <Wheel x={330} r={100} rot={deg(100)} />
    </g>
  );
};

// Soybean plant growing from (0, 0) upward; `p` 0..1.
export const SoyPlant: React.FC<{ readonly p: number; readonly frame: number }> = ({ p, frame }) => {
  const nodes = [
    { y: -150, side: -1 },
    { y: -260, side: 1 },
    { y: -370, side: -1 },
    { y: -470, side: 1 },
    { y: -560, side: -1 },
    { y: -640, side: 1 },
  ];
  const stemLen = 700;
  return (
    <g>
      <path d="M0 0 C -20 -200, 20 -450, 0 -700" stroke={C.mid} strokeWidth={14} fill="none" strokeLinecap="round" strokeDasharray={stemLen} strokeDashoffset={stemLen * (1 - Math.min(1, p / 0.5))} />
      {nodes.map((n, i) => {
        const t = interpolate(p, [0.08 + i * 0.07, 0.3 + i * 0.07], [0, 1], CLAMP);
        const pod = interpolate(p, [0.55 + i * 0.05, 0.72 + i * 0.05], [0, 1], CLAMP);
        const s = sway(frame, i * 1.3, 2);
        return (
          <g key={i} transform={`translate(0 ${n.y})`}>
            <g transform={`rotate(${n.side * 40 + s}) scale(${t})`}>
              <line x1={0} y1={0} x2={0} y2={-150} stroke={C.mid} strokeWidth={6} />
              {[-50, 0, 50].map((a) => (
                <ellipse key={a} cx={0} cy={-210} rx={34} ry={64} transform={`rotate(${a} 0 -150)`} fill={a === 0 ? C.sprout : C.leaf} />
              ))}
            </g>
            {[0, 1, 2].map((k) => (
              <g key={k} transform={`rotate(${-n.side * (35 + k * 28)}) translate(0 ${16 + k * 4}) scale(${pod})`}>
                <path d="M-2 0 C 22 6, 26 30, 22 46 C 30 58, 30 80, 20 92 C 26 106, 18 124, 2 130 C -14 118, -16 100, -10 90 C -20 76, -18 56, -10 46 C -16 30, -16 8, -2 0 Z" fill="#a9b45a" stroke="#7d8a3a" strokeWidth={3} />
                {[24, 68, 108].map((cy) => (
                  <ellipse key={cy} cx={6} cy={cy} rx={11} ry={14} fill="#d9d08a" opacity={0.85} />
                ))}
              </g>
            ))}
          </g>
        );
      })}
    </g>
  );
};

export const rnd = (seed: string, a: number, b: number) => a + random(seed) * (b - a);
