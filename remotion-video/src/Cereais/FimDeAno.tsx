import { AbsoluteFill, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { LeafMark, MiniWheat, rnd, Sprout, sway, Wheat } from "./parts";
import { Body, countUp, Kicker, Title } from "./Text";
import { BODY, C, CLAMP, HEAD } from "./theme";

// Year-end thank-you Reel, 1080x1920, 40s. Text stays inside the Reels safe area (y 260-1500).
const W = 1080;
const H = 1920;
const FADE = 15;

const Svg: React.FC<{ readonly children: React.ReactNode; readonly style?: React.CSSProperties }> = ({ children, style }) => (
  <svg viewBox={`0 0 ${W} ${H}`} width={W} height={H} style={{ position: "absolute", inset: 0, ...style }}>
    {children}
  </svg>
);

const BrandBg: React.FC<{ readonly from?: string; readonly to?: string }> = ({ from = C.brand, to = C.deep }) => (
  <AbsoluteFill style={{ background: `radial-gradient(ellipse 100% 70% at 50% 42%, ${from} 0%, ${to} 100%)` }} />
);

const Stack: React.FC<{ readonly children: React.ReactNode; readonly top: number; readonly gap?: number }> = ({ children, top, gap = 28 }) => (
  <div style={{ position: "absolute", left: 90, right: 90, top, display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center", gap }}>
    {children}
  </div>
);

const FieldEdge: React.FC<{ readonly color: string; readonly count?: number }> = ({ color, count = 70 }) => {
  const frame = useCurrentFrame();
  return (
    <>
      {Array.from({ length: count }, (_, i) => (
        <MiniWheat key={i} x={(i / count) * (W + 40) - 20 + rnd(`ve${i}`, -5, 5)} y={H + 5} h={rnd(`vh${i}`, 90, 190)} angle={sway(frame, i * 0.45, 3)} color={color} />
      ))}
    </>
  );
};

// Slow golden motes drifting upward; low, steady opacity (no flicker).
const Motes: React.FC<{ readonly count?: number }> = ({ count = 40 }) => {
  const frame = useCurrentFrame();
  return (
    <>
      {Array.from({ length: count }, (_, i) => {
        const speed = rnd(`ms${i}`, 0.8, 1.8);
        const y = ((rnd(`my${i}`, 0, H + 200) - frame * speed) % (H + 200) + H + 200) % (H + 200) - 100;
        const x = rnd(`mx${i}`, 0, W) + Math.sin(frame / 40 + i) * 12;
        return <circle key={i} cx={x} cy={y} r={rnd(`mr${i}`, 2.5, 6)} fill={C.gold} opacity={rnd(`mo${i}`, 0.18, 0.4)} />;
      })}
    </>
  );
};

/* 1 — Logo reveal (the opening SFX hit lands at frame 24). */
const Abertura: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const icon = spring({ frame: frame - 16, fps, config: { damping: 13 } });
  const wipe = interpolate(frame, [34, 66], [0, 100], { ...CLAMP, easing: Easing.inOut(Easing.cubic) });
  const cereais = interpolate(frame, [28, 46], [0, 1], CLAMP);
  return (
    <AbsoluteFill>
      <BrandBg />
      <Svg>
        <LeafMark x={820} y={2000} scale={1.4 + frame * 0.001} rotate={-6 + frame * 0.03} opacity={0.08} />
        <LeafMark x={120} y={1500} scale={0.55} rotate={18} opacity={0.05} />
        <FieldEdge color={C.dark} />
      </Svg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", scale: interpolate(frame, [0, 150], [1, 1.05]) }}>
        <Img src={staticFile("cereais/icon.png")} style={{ width: 300, scale: icon, rotate: `${(1 - icon) * -30}deg` }} />
        <Img src={staticFile("cereais/cereais.png")} style={{ width: 340, marginTop: 40, opacity: cereais, translate: `0px ${(1 - cereais) * 20}px` }} />
        <Img src={staticFile("cereais/rohleder.png")} style={{ width: 900, marginTop: 22, clipPath: `inset(0 ${100 - wipe}% 0 0)` }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* 2 — 26 anos na ativa. */
const Anos: React.FC = () => {
  const frame = useCurrentFrame();
  const xs = [120, 240, 360, 480, 600, 720, 840, 960];
  return (
    <AbsoluteFill>
      <BrandBg from={C.teal} to={C.deep} />
      <Svg>
        {xs.map((x, i) => (
          <Wheat
            key={x}
            x={x + rnd(`ax${i}`, -25, 25)}
            y={H + 10}
            h={rnd(`ah${i}`, 330, 470)}
            grow={interpolate(frame, [8 + i * 6, 100 + i * 6], [0, 1], { ...CLAMP, easing: Easing.out(Easing.quad) })}
            angle={sway(frame, i * 0.9, 2.5)}
            scale={1.2}
            grains={14}
            color={i % 3 === 1 ? C.goldDark : C.gold}
          />
        ))}
      </Svg>
      <Stack top={300} gap={10}>
        <Kicker text="DESDE 2000" delay={4} />
        <div style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 470, lineHeight: 1, color: C.gold, fontVariantNumeric: "tabular-nums", marginTop: 10 }}>
          {countUp(frame, 6, 60, 26)}
        </div>
        <div style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 120, lineHeight: 1, color: C.white, opacity: interpolate(frame, [50, 66], [0, 1], CLAMP) }}>
          anos na ativa
        </div>
        <div style={{ marginTop: 30 }}>
          <Body delay={70} size={44} italic>
            ao lado do produtor rural.
          </Body>
        </div>
      </Stack>
    </AbsoluteFill>
  );
};

/* 3 — Trajetória 2000 → 2026: a sprout grows into wheat as the year counts up. */
const Trajetoria: React.FC = () => {
  const frame = useCurrentFrame();
  const grow = interpolate(frame, [10, 150], [0, 1], { ...CLAMP, easing: Easing.inOut(Easing.quad) });
  const year = 2000 + countUp(frame, 10, 140, 26);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 90% 60% at 50% 70%, #ffffff 0%, ${C.mint} 55%, #dfe9da 100%)` }} />
      <Svg>
        <LeafMark x={900} y={2050} scale={1.4} rotate={-12} color={C.brand} opacity={0.06} />
        <path d={`M0 ${H - 120} C 300 ${H - 170}, 780 ${H - 170}, ${W} ${H - 120} L${W} ${H} L0 ${H} Z`} fill={C.brand} />
        <Sprout x={300} y={H - 150} s={interpolate(frame, [20, 40], [0, 2.2], CLAMP)} angle={sway(frame, 1, 3)} />
        <Sprout x={800} y={H - 150} s={interpolate(frame, [30, 50], [0, 2], CLAMP)} angle={sway(frame, 2, 3)} />
        <Wheat x={540} y={H - 150} h={560} grow={grow} angle={sway(frame, 0, 1.5)} scale={1.35} grains={16} color={C.goldDark} />
      </Svg>
      <Stack top={280} gap={22}>
        <Kicker text="NOSSA HISTÓRIA" color={C.mid} delay={4} />
        <div style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 210, lineHeight: 1, color: C.brand, fontVariantNumeric: "tabular-nums" }}>{year}</div>
        <Title text="Uma história que cresce junto com o campo" size={68} color={C.deep} accent={C.mid} accentWords={["campo"]} align="center" delay={24} />
      </Stack>
    </AbsoluteFill>
  );
};

/* 4 — Cultura do campo: rows in perspective under a calm sky. */
const Cultura: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const HZ = 1020;
  const rows = Array.from({ length: 15 }, (_, i) => i - 7);
  const draw = interpolate(frame, [0, 36], [0, 1], { ...CLAMP, easing: Easing.out(Easing.cubic) });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: `linear-gradient(180deg, #dce9d6 0%, ${C.mint} 45%, #f3ecd6 55%)` }} />
      <Svg style={{ scale: interpolate(frame, [0, 225], [1, 1.1]), transformOrigin: "50% 60%" }}>
        <defs>
          <linearGradient id="vsoil" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#8a6a45" />
            <stop offset="1" stopColor={C.soil} />
          </linearGradient>
        </defs>
        <path d={`M0 ${HZ - 30} C 260 ${HZ - 80}, 600 ${HZ - 50}, ${W} ${HZ - 30} L${W} ${HZ} L0 ${HZ} Z`} fill={C.leaf} opacity={0.55} />
        <rect x={0} y={HZ} width={W} height={H - HZ} fill="url(#vsoil)" />
        {rows.map((k) => {
          const bx = 540 + k * 170;
          const hx = 540 + k * 14;
          return <line key={k} x1={hx} y1={HZ} x2={hx + (bx - hx) * draw} y2={HZ + (H - HZ) * draw} stroke={C.mid} strokeWidth={6} opacity={0.55} strokeLinecap="round" />;
        })}
        {rows.map((k) =>
          Array.from({ length: 9 }, (_, j) => {
            const d = Math.pow((j + 1) / 9, 2);
            const y = HZ + (H - HZ) * d;
            const x = 540 + k * 14 + (k * 170 - k * 14) * d;
            const s = spring({ frame: frame - (22 + (8 - j) * 6 + Math.abs(k) * 1.5), fps, config: { damping: 12 } }) * (0.25 + d * 1.9);
            return <Sprout key={`${k}-${j}`} x={x} y={y} s={s} angle={sway(frame, k + j, 4)} />;
          }),
        )}
      </Svg>
      <Stack top={290} gap={26}>
        <Kicker text="CULTURA DO CAMPO" color={C.brand} delay={8} />
        <Title text="Orgulho de ser do campo" size={96} color={C.deep} accent={C.mid} accentWords={["campo"]} align="center" delay={14} />
        <Body color="rgba(22, 49, 34, 0.82)" delay={38} size={40}>
          O trabalho, a família e a terra fazem parte de quem somos.
        </Body>
      </Stack>
    </AbsoluteFill>
  );
};

// Points filling a heart (classic parametric outline, interior sampled on a grid).
const HEART: ReadonlyArray<readonly [number, number]> = (() => {
  const inside = (x: number, y: number) => Math.pow(x * x + y * y - 1, 3) - x * x * y * y * y <= 0;
  const pts: [number, number][] = [];
  for (let gy = 1.3; gy >= -1.2; gy -= 0.085) {
    for (let gx = -1.3; gx <= 1.3; gx += 0.085) {
      if (inside(gx, gy)) pts.push([gx, gy]);
    }
  }
  return pts;
})();

/* 5 — Obrigado: grains fly in and settle into a heart. */
const Obrigado: React.FC = () => {
  const frame = useCurrentFrame();
  const CX = 540;
  const CY = 1060;
  const R = 300;
  const breathe = 1 + 0.015 * Math.sin(Math.max(0, frame - 110) / 14);
  return (
    <AbsoluteFill>
      <BrandBg />
      <Svg>
        <LeafMark x={960} y={2000} scale={1.2} rotate={-14} opacity={0.06} />
        <g transform={`translate(${CX} ${CY}) scale(${breathe})`}>
          {HEART.map(([hx, hy], i) => {
            const delay = 10 + rnd(`hd${i}`, 0, 70);
            const t = interpolate(frame, [delay, delay + 34], [0, 1], { ...CLAMP, easing: Easing.out(Easing.cubic) });
            if (t <= 0) return null;
            const sx = rnd(`hsx${i}`, -700, 700);
            const sy = 1100 + rnd(`hsy${i}`, 0, 400);
            const tx = hx * R;
            const ty = -hy * R;
            const x = sx + (tx - sx) * t;
            const y = sy + (ty - sy) * t;
            return <ellipse key={i} cx={x} cy={y} rx={9} ry={13} transform={`rotate(${rnd(`hr${i}`, -60, 60) * (1 - t * 0.4)} ${x} ${y})`} fill={i % 4 === 0 ? C.goldDark : C.gold} />;
          })}
        </g>
      </Svg>
      <Stack top={270} gap={22}>
        <Kicker text="OBRIGADO" delay={4} />
        <Title text="A cada cliente que confia no nosso trabalho" size={74} align="center" accentWords={["confia"]} delay={10} />
      </Stack>
      <Stack top={1440}>
        <Body delay={100} size={42}>
          Vocês fazem parte da nossa história.
        </Body>
      </Stack>
    </AbsoluteFill>
  );
};

/* 6 — Boas festas + logo (the ending SFX starts at frame 26). */
const Festas: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logo = spring({ frame: frame - 4, fps, config: { damping: 16 } });
  const xs = [90, 200, 320, 760, 880, 990];
  return (
    <AbsoluteFill>
      <BrandBg />
      <Svg>
        <LeafMark x={880} y={1980} scale={1.3} rotate={-4 + frame * 0.03} opacity={0.07} />
        <Motes />
        <FieldEdge color={C.dark} />
        {xs.map((x, i) => (
          <Wheat key={x} x={x} y={H + 10} h={rnd(`fh${i}`, 300, 420)} angle={sway(frame, i, 2.5) + (x < 540 ? -6 : 6)} scale={1.1} grains={14} color={i % 2 ? C.goldDark : C.gold} />
        ))}
      </Svg>
      <Stack top={300} gap={0}>
        <Img src={staticFile("cereais/logo.png")} style={{ width: 640, scale: 0.85 + 0.15 * logo, opacity: logo }} />
        <div style={{ marginTop: 110 }}>
          <Title text="Boas festas!" size={130} align="center" delay={26} />
        </div>
        <div style={{ marginTop: 20 }}>
          <Title text="E uma safra próspera em 2027!" size={52} color={C.gold} align="center" delay={40} />
        </div>
        <div style={{ marginTop: 44 }}>
          <Body delay={64} size={38}>
            Obrigado por 26 anos de confiança.
          </Body>
        </div>
      </Stack>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 1530,
          textAlign: "center",
          fontFamily: BODY,
          fontWeight: 500,
          fontSize: 26,
          letterSpacing: "0.35em",
          color: "rgba(255, 255, 255, 0.7)",
          opacity: interpolate(frame, [80, 100], [0, 1], CLAMP),
        }}
      >
        GUARANI DAS MISSÕES · RS
      </div>
    </AbsoluteFill>
  );
};

const Dissolve: React.FC<{ readonly children: React.ReactNode; readonly first?: boolean }> = ({ children, first = false }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        opacity: first ? 1 : interpolate(frame, [0, FADE], [0, 1], CLAMP),
        scale: first ? 1 : interpolate(frame, [0, FADE + 10], [1.04, 1], { ...CLAMP, easing: Easing.out(Easing.cubic) }),
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

const SCENES = [
  { name: "Abertura", len: 150, C: Abertura },
  { name: "26 anos", len: 180, C: Anos },
  { name: "2000 → 2026", len: 180, C: Trajetoria },
  { name: "Cultura do campo", len: 210, C: Cultura },
  { name: "Obrigado", len: 210, C: Obrigado },
  { name: "Boas festas", len: 270, C: Festas },
] as const;

export const FIM_DE_ANO_FRAMES = SCENES.reduce((a, s) => a + s.len, 0);

export const CereaisFimDeAno: React.FC = () => {
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
        src={staticFile("cereais/music-40.wav")}
        volume={(f) => interpolate(f, [0, 20, durationInFrames - 3 * fps, durationInFrames - 2], [0.35, 0.8, 0.8, 0], CLAMP)}
      />
      <Sequence name="SFX abertura" from={0} layout="none">
        <Audio src={staticFile("sfx/abertura-reveal.mp3")} volume={0.75} />
      </Sequence>
      {starts.slice(1, -1).map((st) => (
        <Sequence key={st} name="SFX transição" from={st - 6} durationInFrames={30} layout="none">
          <Audio src={staticFile("sfx/whoosh-short.mp3")} volume={0.2} />
        </Sequence>
      ))}
      <Sequence name="SFX final" from={last + 26} layout="none">
        <Audio src={staticFile("sfx/festa-final.mp3")} volume={0.6} />
      </Sequence>
    </AbsoluteFill>
  );
};
