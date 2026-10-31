import { AbsoluteFill, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { BrandBg, Dissolve, Stack, Svg } from "./FimDeAno";
import { LeafMark } from "./parts";
import { Body, Kicker, Title } from "./Text";
import { BODY, C, CLAMP, HEAD } from "./theme";

// Agribusiness data Reel (1080x1920, 50s). Figures: Conab 12º lev. 2025/26 (set/2026) and
// 1º lev. 2026/27 (15/out/2026), Anec 2026 soybean exports, Emater/RS 2026 wheat area.
const W = 1080;
const UP = C.sprout;
const DOWN = "#e07a5f";
const dec = (n: number, d = 1) => new Intl.NumberFormat("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d }).format(n);
const ease = (frame: number, a: number, b: number) => interpolate(frame, [a, b], [0, 1], { ...CLAMP, easing: Easing.inOut(Easing.cubic) });

const Big: React.FC<{ readonly value: string; readonly unit: string; readonly color?: string; readonly size?: number }> = ({ value, unit, color = C.gold, size = 210 }) => (
  <div style={{ display: "flex", alignItems: "baseline", justifyContent: "center", gap: 20 }}>
    <span style={{ fontFamily: HEAD, fontWeight: 900, fontSize: size, lineHeight: 0.95, color, fontVariantNumeric: "tabular-nums" }}>{value}</span>
    <span style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 50, lineHeight: 1.05, color: C.white, textAlign: "left", whiteSpace: "pre-line" }}>{unit}</span>
  </div>
);

const Chip: React.FC<{ readonly text: string; readonly color?: string; readonly delay?: number }> = ({ text, color = UP, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - delay, fps, config: { damping: 14 } });
  return (
    <div
      style={{
        padding: "12px 26px",
        borderRadius: 999,
        border: `2px solid ${color}`,
        backgroundColor: "rgba(0, 0, 0, 0.18)",
        color,
        fontFamily: BODY,
        fontWeight: 700,
        fontSize: 32,
        letterSpacing: "0.04em",
        scale: 0.7 + 0.3 * s,
        opacity: s,
      }}
    >
      {text}
    </div>
  );
};

const Source: React.FC<{ readonly text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: 90,
        right: 90,
        top: 1480,
        textAlign: "center",
        fontFamily: BODY,
        fontSize: 24,
        color: "rgba(255, 255, 255, 0.55)",
        opacity: interpolate(frame, [20, 36], [0, 1], CLAMP),
      }}
    >
      {text}
    </div>
  );
};

// Faint data grid behind every data scene.
const Grid: React.FC = () => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 20], [0, 1], CLAMP);
  return (
    <g opacity={0.06 * o} stroke={C.white} strokeWidth={2}>
      {Array.from({ length: 21 }, (_, i) => (
        <line key={`h${i}`} x1={0} x2={W} y1={i * 96} y2={i * 96} />
      ))}
      {Array.from({ length: 12 }, (_, i) => (
        <line key={`v${i}`} y1={0} y2={1920} x1={i * 96} x2={i * 96} />
      ))}
    </g>
  );
};

const Steps: React.FC<{ readonly n: number }> = ({ n }) => (
  <div style={{ position: "absolute", top: 190, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 12 }}>
    {[1, 2, 3, 4, 5].map((i) => (
      <div key={i} style={{ width: i === n ? 46 : 14, height: 14, borderRadius: 7, backgroundColor: i === n ? C.gold : "rgba(255, 255, 255, 0.25)" }} />
    ))}
  </div>
);

const DataScene: React.FC<{ readonly n?: number; readonly children: React.ReactNode; readonly svg?: React.ReactNode; readonly from?: string }> = ({ n, children, svg, from = C.brand }) => (
  <AbsoluteFill>
    <BrandBg from={from} to={C.deep} />
    <Svg>
      <Grid />
      {svg}
    </Svg>
    {n !== undefined && <Steps n={n} />}
    {children}
  </AbsoluteFill>
);

/* 1 — Gancho. */
const Gancho: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const icon = spring({ frame: frame - 16, fps, config: { damping: 13 } });
  const bars = [0.35, 0.55, 0.45, 0.7, 0.62, 0.85, 1.0];
  return (
    <DataScene
      svg={
        <>
          <LeafMark x={900} y={2000} scale={1.3} rotate={-8} opacity={0.06} />
          {bars.map((h, i) => {
            const g = ease(frame, 10 + i * 5, 50 + i * 5);
            const bh = 520 * h * g;
            return <rect key={i} x={110 + i * 125} y={1920 - 120 - bh} width={90} height={bh} rx={14} fill={i === bars.length - 1 ? C.gold : C.white} opacity={i === bars.length - 1 ? 0.5 : 0.08} />;
          })}
        </>
      }
    >
      <Stack top={300} gap={30}>
        <Img src={staticFile("cereais/icon.png")} style={{ width: 150, scale: icon }} />
        <Kicker text="PANORAMA DO AGRO" delay={20} />
        <Title text="Os números que movem o campo" size={104} align="center" accentWords={["campo"]} delay={26} />
        <Body delay={50} size={40}>
          Soja, milho e trigo: o que você precisa saber.
        </Body>
      </Stack>
    </DataScene>
  );
};

/* 2 — Safra total + donut (participação projetada 2026/27). */
const Safra: React.FC = () => {
  const frame = useCurrentFrame();
  const value = interpolate(frame, [8, 60], [0, 361.7], { ...CLAMP, easing: Easing.out(Easing.cubic) });
  const R = 200;
  const CIRC = 2 * Math.PI * R;
  const segs = [
    { label: "Soja", v: 181.6, color: C.gold },
    { label: "Milho", v: 148, color: UP },
    { label: "Outros grãos", v: 367.1 - 181.6 - 148, color: "rgba(255,255,255,0.35)" },
  ];
  let acc = 0;
  return (
    <DataScene
      n={1}
      svg={
        <g transform="translate(540 1080) rotate(-90)">
          <circle r={R} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth={64} />
          {segs.map((s, i) => {
            const frac = s.v / 367.1;
            const p = ease(frame, 50 + i * 18, 80 + i * 18);
            const el = <circle key={s.label} r={R} fill="none" stroke={s.color} strokeWidth={64} strokeDasharray={`${CIRC * frac * p} ${CIRC}`} strokeDashoffset={-CIRC * acc} />;
            acc += frac;
            return el;
          })}
        </g>
      }
    >
      <Stack top={260} gap={22}>
        <Kicker text="SAFRA DE GRÃOS 2025/26" delay={4} />
        <Big value={dec(value)} unit={"milhões\nde toneladas"} />
        <Chip text="▲ RECORDE · +2,6% NO ANO" delay={50} />
      </Stack>
      <div style={{ position: "absolute", left: 340, width: 400, top: 1010, textAlign: "center", opacity: interpolate(frame, [100, 120], [0, 1], CLAMP) }}>
        <div style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 64, color: C.white, lineHeight: 1 }}>9 em 10</div>
        <div style={{ fontFamily: BODY, fontSize: 26, color: "rgba(255,255,255,0.75)", marginTop: 8 }}>toneladas são soja ou milho</div>
      </div>
      <div style={{ position: "absolute", left: 90, right: 90, top: 1330, display: "flex", justifyContent: "center", gap: 34 }}>
        {segs.map((s, i) => (
          <div key={s.label} style={{ display: "flex", alignItems: "center", gap: 10, fontFamily: BODY, fontSize: 28, color: C.white, opacity: interpolate(frame, [60 + i * 18, 76 + i * 18], [0, 1], CLAMP) }}>
            <div style={{ width: 22, height: 22, borderRadius: 6, backgroundColor: s.color }} />
            {s.label} {dec((s.v / 367.1) * 100, 0)}%
          </div>
        ))}
      </div>
      <Source text="Fonte: Conab (set/2026). Participação: projeção 2026/27 de 367,1 mi t (out/2026)." />
    </DataScene>
  );
};

/* 3 — Soja: recorde + barras 2025/26 × 2026/27. */
const Soja: React.FC = () => {
  const frame = useCurrentFrame();
  const value = interpolate(frame, [8, 60], [0, 180.4], { ...CLAMP, easing: Easing.out(Easing.cubic) });
  const rows = [
    { label: "Safra 2025/26", v: 180.4, color: C.gold },
    { label: "Projeção 2026/27", v: 181.6, color: UP },
  ];
  return (
    <DataScene n={2} from={C.teal}>
      <Stack top={260} gap={22}>
        <Kicker text="SOJA" delay={4} />
        <Big value={dec(value)} unit={"milhões\nde toneladas"} />
        <Chip text="★ MAIOR SAFRA DA HISTÓRIA" color={C.gold} delay={46} />
      </Stack>
      <div style={{ position: "absolute", left: 90, right: 90, top: 900, display: "flex", flexDirection: "column", gap: 44 }}>
        {rows.map((r, i) => {
          const p = ease(frame, 60 + i * 16, 105 + i * 16);
          return (
            <div key={r.label}>
              <div style={{ display: "flex", justifyContent: "space-between", fontFamily: BODY, fontSize: 32, color: C.white, marginBottom: 12 }}>
                <span>{r.label}</span>
                <span style={{ fontWeight: 700, fontVariantNumeric: "tabular-nums" }}>{dec(r.v * p)} mi t</span>
              </div>
              <div style={{ height: 54, borderRadius: 14, backgroundColor: "rgba(255,255,255,0.08)" }}>
                <div style={{ width: `${(r.v / 200) * 100 * p}%`, height: "100%", borderRadius: 14, backgroundColor: r.color }} />
              </div>
            </div>
          );
        })}
        <div style={{ display: "flex", justifyContent: "center", marginTop: 16 }}>
          <Chip text="Área 2026/27: 49,3 mi ha  ▲ 1,4%" delay={120} />
        </div>
      </div>
      <Source text="Fonte: Conab, 12º lev. 2025/26 (set/2026) e 1º lev. 2026/27 (out/2026)." />
    </DataScene>
  );
};

/* 4 — Exportação de soja: anel de progresso jan–jul vs projeção do ano. */
const Exportacao: React.FC = () => {
  const frame = useCurrentFrame();
  const R = 210;
  const CIRC = 2 * Math.PI * R;
  const p = ease(frame, 30, 100);
  const frac = 84.8 / 114;
  return (
    <DataScene
      n={3}
      svg={
        <g transform="translate(540 1010) rotate(-90)">
          <circle r={R} fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth={46} />
          <circle r={R} fill="none" stroke={C.gold} strokeWidth={46} strokeLinecap="round" strokeDasharray={`${CIRC * frac * p} ${CIRC}`} />
        </g>
      }
    >
      <Stack top={260} gap={20}>
        <Kicker text="EXPORTAÇÃO DE SOJA" delay={4} />
        <Title text="Recorde atrás de recorde" size={88} align="center" accentWords={["recorde"]} delay={10} />
      </Stack>
      <div style={{ position: "absolute", left: 300, width: 480, top: 900, textAlign: "center" }}>
        <div style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 104, color: C.gold, lineHeight: 1, fontVariantNumeric: "tabular-nums" }}>{dec(84.8 * p)}</div>
        <div style={{ fontFamily: BODY, fontSize: 28, color: "rgba(255,255,255,0.8)", marginTop: 10 }}>mi t embarcadas</div>
        <div style={{ fontFamily: BODY, fontSize: 28, color: "rgba(255,255,255,0.8)" }}>jan–jul/2026</div>
      </div>
      <Stack top={1290} gap={18}>
        <Chip text="Abril/2026: 16,75 mi t · maior mês da história" color={C.gold} delay={100} />
        <Chip text="Projeção do ano: ~114 mi t (recorde)" delay={120} />
      </Stack>
      <Source text="Fonte: Anec (projeções e embarques 2026)." />
    </DataScene>
  );
};

/* 5 — Milho: coluna empilhada por safra (projeção 2026/27). */
const Milho: React.FC = () => {
  const frame = useCurrentFrame();
  const value = interpolate(frame, [8, 60], [0, 148], { ...CLAMP, easing: Easing.out(Easing.cubic) });
  const PX = 4.0;
  const BASE = 1410;
  const parts = [
    { label: "1ª safra", v: 32.1, color: UP },
    { label: "2ª safra", v: 113.3, color: C.gold },
    { label: "3ª safra", v: 148 - 32.1 - 113.3, color: C.white },
  ];
  let y = BASE;
  return (
    <DataScene
      n={4}
      from={C.teal}
      svg={
        <>
          {parts.map((s, i) => {
            const p = ease(frame, 50 + i * 22, 80 + i * 22);
            const h = s.v * PX * p;
            const top = y - h;
            const full = s.v * PX;
            const labelY = y - full / 2;
            y -= full;
            return (
              <g key={s.label}>
                <rect x={250} y={top} width={240} height={Math.max(0, h - 4)} rx={10} fill={s.color} opacity={i === 2 ? 0.8 : 1} />
                <g opacity={p}>
                  <line x1={510} x2={570} y1={labelY} y2={labelY} stroke="rgba(255,255,255,0.5)" strokeWidth={3} />
                  <text x={590} y={labelY + 12} fontFamily={BODY} fontSize={34} fill={C.white}>
                    {s.label}: <tspan fontWeight={700}>{i === 2 ? "~" : ""}{dec(s.v)} mi t</tspan>
                  </text>
                </g>
              </g>
            );
          })}
        </>
      }
    >
      <Stack top={260} gap={22}>
        <Kicker text="MILHO · PROJEÇÃO 2026/27" delay={4} />
        <Big value={dec(value, 0)} unit={"milhões\nde toneladas"} />
        <Chip text="▲ +2,4% · CONSUMO INTERNO +6,6% (ETANOL)" delay={46} />
      </Stack>
      <Source text="Fonte: Conab, 1º levantamento 2026/27 (out/2026)." />
    </DataScene>
  );
};

/* 6 — Trigo: barras 2025 × 2026 (queda). */
const Trigo: React.FC = () => {
  const frame = useCurrentFrame();
  const PX = 64;
  const BASE = 1400;
  const grow = ease(frame, 40, 80);
  const drop = ease(frame, 95, 135);
  const prev = 7.8;
  const now = prev - (prev - 5.7) * drop;
  const bar = (x: number, v: number, color: string, label: string, val: string, ghost?: number) => (
    <g>
      {ghost !== undefined && <rect x={x} y={BASE - ghost * PX * grow} width={220} height={ghost * PX * grow} rx={12} fill="none" stroke={DOWN} strokeWidth={4} strokeDasharray="14 10" opacity={drop} />}
      <rect x={x} y={BASE - v * PX * grow} width={220} height={v * PX * grow} rx={12} fill={color} />
      <text x={x + 110} y={BASE - v * PX * grow - 24} textAnchor="middle" fontFamily={HEAD} fontWeight={900} fontSize={52} fill={C.white} opacity={grow}>
        {val}
      </text>
      <text x={x + 110} y={BASE + 52} textAnchor="middle" fontFamily={BODY} fontSize={34} fill="rgba(255,255,255,0.8)">
        {label}
      </text>
    </g>
  );
  return (
    <DataScene
      n={5}
      svg={
        <>
          <line x1={150} x2={930} y1={BASE} y2={BASE} stroke="rgba(255,255,255,0.4)" strokeWidth={3} />
          {bar(230, prev, "rgba(255,255,255,0.35)", "2025", "~7,8")}
          {bar(630, now, C.gold, "2026", dec(now), prev)}
        </>
      }
    >
      <Stack top={260} gap={22}>
        <Kicker text="TRIGO · SAFRA 2026" delay={4} />
        <Big value="5,7" unit={"milhões\nde toneladas"} />
        <Chip text="▼ −27% NA PRODUÇÃO · ÁREA NO RS −30%" color={DOWN} delay={100} />
      </Stack>
      <Source text="Fontes: Conab (out/2026) e Emater/RS (área 2026). 2025 estimado a partir da variação." />
    </DataScene>
  );
};

/* 7 — Encerramento com logo (assinatura sonora repete a da abertura). */
const Encerramento: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logo = spring({ frame: frame - 70, fps, config: { damping: 16 } });
  return (
    <DataScene from={C.brand} svg={<LeafMark x={900} y={2000} scale={1.3} rotate={-6 + frame * 0.03} opacity={0.07} />}>
      <Stack top={300} gap={0}>
        <Title text="Informação de qualidade" size={92} align="center" delay={6} />
        <Title text="para decidir melhor no campo." size={54} color={C.gold} align="center" delay={18} />
        <div style={{ marginTop: 90 }}>
          <Img src={staticFile("cereais/logo.png")} style={{ width: 640, scale: 0.85 + 0.15 * logo, opacity: logo }} />
        </div>
        <div style={{ marginTop: 60 }}>
          <Body delay={100} size={38}>
            Siga e acompanhe o mercado com a gente.
          </Body>
        </div>
      </Stack>
    </DataScene>
  );
};

const SCENES = [
  { name: "Gancho", len: 120, C: Gancho },
  { name: "Safra de grãos", len: 210, C: Safra },
  { name: "Soja", len: 240, C: Soja },
  { name: "Exportação", len: 210, C: Exportacao },
  { name: "Milho", len: 210, C: Milho },
  { name: "Trigo", len: 240, C: Trigo },
  { name: "Encerramento", len: 270, C: Encerramento },
] as const;

const FADE = 15;
export const AGRO_FRAMES = SCENES.reduce((a, s) => a + s.len, 0);

export const CereaisAgro: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  let at = 0;
  const starts = SCENES.map((s) => {
    const st = at;
    at += s.len;
    return st;
  });
  const last = starts[starts.length - 1];

  return (
    <AbsoluteFill style={{ backgroundColor: C.deep }}>
      {SCENES.map((s, i) => (
        <Sequence key={s.name} name={s.name} from={starts[i]} durationInFrames={s.len + (i < SCENES.length - 1 ? FADE : 0)}>
          <Dissolve first={i === 0}>
            <s.C />
          </Dissolve>
        </Sequence>
      ))}

      <Audio
        src={staticFile("cereais/music-agro.wav")}
        volume={(f) => interpolate(f, [0, 20, durationInFrames - 3 * fps, durationInFrames - 2], [0.35, 0.75, 0.75, 0], CLAMP)}
      />
      <Sequence name="SFX abertura" from={0} layout="none">
        <Audio src={staticFile("sfx/abertura-reveal.mp3")} volume={0.75} />
      </Sequence>
      {starts.slice(1).map((st) => (
        <Sequence key={st} name="SFX transição" from={st - 6} durationInFrames={30} layout="none">
          <Audio src={staticFile("sfx/whoosh-short.mp3")} volume={0.2} />
        </Sequence>
      ))}
      <Sequence name="SFX assinatura" from={last + 70 - 24} layout="none">
        <Audio src={staticFile("sfx/abertura-reveal.mp3")} volume={0.6} />
      </Sequence>
    </AbsoluteFill>
  );
};
