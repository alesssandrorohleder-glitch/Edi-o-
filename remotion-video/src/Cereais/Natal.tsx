import { AbsoluteFill, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { Abertura, BrandBg, Dissolve, FieldEdge, Stack, Svg } from "./FimDeAno";
import { LeafMark, rnd, sway, Wheat } from "./parts";
import { Body, Kicker, Title } from "./Text";
import { BODY, C, CLAMP } from "./theme";

// Christmas Reel, 1080x1920, 20s.
const W = 1080;
const H = 1920;
const RED = "#c8443a";
const CREAM = "#f4efe3";

// Slow, soft snowfall (steady opacity, no flicker).
const Snow: React.FC<{ readonly count?: number }> = ({ count = 70 }) => {
  const frame = useCurrentFrame();
  return (
    <>
      {Array.from({ length: count }, (_, i) => {
        const speed = rnd(`ss${i}`, 1.2, 2.6);
        const y = ((rnd(`sy${i}`, 0, H + 100) + frame * speed) % (H + 100)) - 50;
        const x = rnd(`sx${i}`, 0, W) + Math.sin(frame / 35 + i) * 18;
        return <circle key={i} cx={x} cy={y} r={rnd(`sr${i}`, 3, 8)} fill={CREAM} opacity={rnd(`so${i}`, 0.25, 0.6)} />;
      })}
    </>
  );
};

const Star: React.FC<{ readonly r: number }> = ({ r }) => {
  const pts = Array.from({ length: 10 }, (_, i) => {
    const a = -Math.PI / 2 + (i * Math.PI) / 5;
    const rr = i % 2 === 0 ? r : r * 0.45;
    return `${(Math.cos(a) * rr).toFixed(1)},${(Math.sin(a) * rr).toFixed(1)}`;
  }).join(" ");
  return <polygon points={pts} fill={C.white} stroke={C.gold} strokeWidth={4} strokeLinejoin="round" />;
};

// Grain positions filling a three-tier tree (normalised: y 0 top → 1 base, x ±0.5).
const TIERS = [
  [0.0, 0.42, 0.27],
  [0.2, 0.7, 0.37],
  [0.44, 1.0, 0.48],
] as const;
const TREE: ReadonlyArray<{ x: number; y: number; garland: boolean }> = (() => {
  const pts: { x: number; y: number; garland: boolean }[] = [];
  for (let y = 0.04; y <= 1.0; y += 0.03) {
    for (let x = -0.5; x <= 0.5; x += 0.03) {
      const inside = TIERS.some(([t, b, w]) => y >= t && y <= b && Math.abs(x) <= (w * (y - t)) / (b - t));
      if (inside) pts.push({ x, y, garland: Math.abs(((y * 3.2 + x * 1.4) % 0.32) - 0.16) < 0.022 });
    }
  }
  return pts;
})();
const ORNAMENTS = [
  [-0.08, 0.3], [0.1, 0.36], [-0.2, 0.58], [0.16, 0.62], [0.02, 0.5],
  [-0.3, 0.88], [-0.06, 0.82], [0.24, 0.9], [0.36, 0.95], [0.08, 0.96],
] as const;

/* 2 — A Christmas tree assembled from golden grains. */
const Arvore: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const TH = 860;
  const TOP = 660;
  const star = spring({ frame: frame - 120, fps, config: { damping: 10 } });
  return (
    <AbsoluteFill>
      <BrandBg from={C.brand} to={C.deep} />
      <Svg>
        <LeafMark x={940} y={2000} scale={1.2} rotate={-12} opacity={0.05} />
        <Snow />
        <g transform={`translate(540 ${TOP})`}>
          <rect x={-32} y={TH} width={64} height={70} rx={8} fill={C.soil} opacity={interpolate(frame, [10, 30], [0, 1], CLAMP)} />
          {TREE.map((p, i) => {
            // Bottom grains land first so the tree builds upward.
            const delay = 8 + (1 - p.y) * 70 + rnd(`td${i}`, 0, 22);
            const t = interpolate(frame, [delay, delay + 30], [0, 1], { ...CLAMP, easing: Easing.out(Easing.cubic) });
            if (t <= 0) return null;
            const sx = rnd(`tsx${i}`, -600, 600);
            const sy = 1350 + rnd(`tsy${i}`, 0, 300);
            const tx = p.x * TH;
            const ty = p.y * TH;
            const x = sx + (tx - sx) * t;
            const y = sy + (ty - sy) * t;
            return (
              <ellipse
                key={i}
                cx={x}
                cy={y}
                rx={p.garland ? 7 : 9}
                ry={p.garland ? 10 : 13}
                transform={`rotate(${rnd(`tr${i}`, -50, 50)} ${x} ${y})`}
                fill={p.garland ? CREAM : i % 4 === 0 ? C.goldDark : C.gold}
              />
            );
          })}
          {ORNAMENTS.map(([ox, oy], i) => {
            const s = spring({ frame: frame - (96 + i * 4), fps, config: { damping: 9 } });
            return <circle key={i} cx={ox * TH} cy={oy * TH} r={17 * s} fill={i % 3 === 2 ? C.white : RED} stroke="rgba(0,0,0,0.15)" strokeWidth={2} />;
          })}
          <g transform={`translate(0 -14) scale(${star}) rotate(${(1 - star) * -90 + Math.sin(frame / 25) * 3})`}>
            <circle r={70} fill={C.gold} opacity={0.18} />
            <Star r={52} />
          </g>
        </g>
      </Svg>
      <Stack top={260} gap={20}>
        <Kicker text="NATAL 2026" delay={4} />
        <div>
          <Title text="Do nosso campo" size={80} align="center" delay={10} />
          <Title text="para a sua mesa" size={80} align="center" accentWords={["mesa"]} delay={18} />
        </div>
      </Stack>
    </AbsoluteFill>
  );
};

/* 3 — Feliz Natal + logo. */
const FelizNatal: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logo = spring({ frame: frame - 4, fps, config: { damping: 16 } });
  const xs = [90, 200, 320, 760, 880, 990];
  return (
    <AbsoluteFill>
      <BrandBg />
      <Svg>
        <LeafMark x={880} y={1980} scale={1.3} rotate={-4 + frame * 0.03} opacity={0.07} />
        <Snow />
        <FieldEdge color={C.dark} />
        {xs.map((x, i) => (
          <Wheat key={x} x={x} y={H + 10} h={rnd(`nh${i}`, 300, 420)} angle={sway(frame, i, 2.5) + (x < 540 ? -6 : 6)} scale={1.1} grains={14} color={i % 2 ? C.goldDark : C.gold} />
        ))}
      </Svg>
      <Stack top={300} gap={0}>
        <Img src={staticFile("cereais/logo.png")} style={{ width: 600, scale: 0.85 + 0.15 * logo, opacity: logo }} />
        <div style={{ marginTop: 100 }}>
          <Title text="Feliz Natal!" size={140} align="center" delay={18} />
        </div>
        <div style={{ marginTop: 34 }}>
          <Body delay={36} size={42}>
            Que a sua mesa seja farta
            <br />e o seu lar cheio de paz.
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
          opacity: interpolate(frame, [60, 80], [0, 1], CLAMP),
        }}
      >
        GUARANI DAS MISSÕES · RS
      </div>
    </AbsoluteFill>
  );
};

const SCENES = [
  { name: "Abertura", len: 105, C: Abertura },
  { name: "Árvore de grãos", len: 255, C: Arvore },
  { name: "Feliz Natal", len: 240, C: FelizNatal },
] as const;

const FADE = 15;
export const NATAL_FRAMES = SCENES.reduce((a, s) => a + s.len, 0);

export const CereaisNatal: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const starts = [0, SCENES[0].len, SCENES[0].len + SCENES[1].len];

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
        src={staticFile("cereais/music-natal.wav")}
        volume={(f) => interpolate(f, [0, 20, durationInFrames - 2.5 * fps, durationInFrames - 2], [0.35, 0.8, 0.8, 0], CLAMP)}
      />
      <Sequence name="SFX abertura" from={0} layout="none">
        <Audio src={staticFile("sfx/abertura-reveal.mp3")} volume={0.75} />
      </Sequence>
      <Sequence name="SFX transição" from={starts[1] - 6} durationInFrames={30} layout="none">
        <Audio src={staticFile("sfx/whoosh-short.mp3")} volume={0.2} />
      </Sequence>
      <Sequence name="SFX estrela" from={starts[1] + 120} layout="none">
        <Audio src={staticFile("sfx/sparkle.mp3")} volume={0.4} />
      </Sequence>
      <Sequence name="SFX final" from={starts[2] + 18} layout="none">
        <Audio src={staticFile("sfx/festa-final.mp3")} volume={0.6} />
      </Sequence>
    </AbsoluteFill>
  );
};
