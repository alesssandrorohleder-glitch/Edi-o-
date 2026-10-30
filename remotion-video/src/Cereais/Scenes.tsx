import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { BigEar, CornCob, Harvester, LeafMark, MiniWheat, rnd, SoyPlant, Sprout, sway, Wheat } from "./parts";
import { Body, countUp, fmt, Kicker, Title } from "./Text";
import { BODY, C, CLAMP, HEAD } from "./theme";

const Svg: React.FC<{ readonly children: React.ReactNode; readonly style?: React.CSSProperties }> = ({ children, style }) => (
  <svg viewBox="0 0 1920 1080" width={1920} height={1080} style={{ position: "absolute", inset: 0, ...style }}>
    {children}
  </svg>
);

const TextCol: React.FC<{ readonly children: React.ReactNode; readonly width?: number; readonly top?: number; readonly left?: number }> = ({
  children,
  width = 760,
  top,
  left = 140,
}) => (
  <div style={{ position: "absolute", left, width, top, bottom: top === undefined ? 0 : undefined, height: top === undefined ? "100%" : undefined, display: "flex", flexDirection: "column", justifyContent: top === undefined ? "center" : "flex-start", gap: 26 }}>
    {children}
  </div>
);

const BrandBg: React.FC<{ readonly from?: string; readonly to?: string }> = ({ from = C.brand, to = C.deep }) => (
  <AbsoluteFill style={{ background: `radial-gradient(ellipse 90% 80% at 40% 45%, ${from} 0%, ${to} 100%)` }} />
);

// Low field silhouette along the bottom edge.
const FieldEdge: React.FC<{ readonly color: string; readonly count?: number; readonly base?: number }> = ({ color, count = 120, base = 1085 }) => {
  const frame = useCurrentFrame();
  return (
    <>
      {Array.from({ length: count }, (_, i) => (
        <MiniWheat key={i} x={(i / count) * 1960 - 20 + rnd(`fe${i}`, -6, 6)} y={base} h={rnd(`fh${i}`, 70, 150)} angle={sway(frame, i * 0.4, 3)} color={color} />
      ))}
    </>
  );
};

/* 1 — Abertura: logo assembles over the brand green. */
export const Abertura: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const icon = spring({ frame: frame - 8, fps, config: { damping: 14 } });
  const wipe = interpolate(frame, [34, 70], [0, 100], { ...CLAMP, easing: Easing.inOut(Easing.cubic) });
  const cereais = interpolate(frame, [26, 46], [0, 1], CLAMP);
  return (
    <AbsoluteFill>
      <BrandBg />
      <Svg>
        <LeafMark x={1560} y={1240} scale={1.25 + frame * 0.0008} rotate={-6 + frame * 0.02} opacity={0.08} />
        <LeafMark x={260} y={1180} scale={0.6} rotate={14} opacity={0.05} />
        <FieldEdge color={C.dark} />
      </Svg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 0, scale: interpolate(frame, [0, 210], [1, 1.04]) }}>
        <Img src={staticFile("cereais/icon.png")} style={{ width: 250, scale: icon, rotate: `${(1 - icon) * -30}deg` }} />
        <Img
          src={staticFile("cereais/cereais.png")}
          style={{ width: 290, marginTop: 34, opacity: cereais, translate: `0px ${(1 - cereais) * 20}px`, letterSpacing: 0 }}
        />
        <Img src={staticFile("cereais/rohleder.png")} style={{ width: 820, marginTop: 20, clipPath: `inset(0 ${100 - wipe}% 0 0)` }} />
        <div
          style={{
            marginTop: 40,
            fontFamily: BODY,
            fontWeight: 500,
            fontSize: 26,
            letterSpacing: "0.4em",
            color: "rgba(255, 255, 255, 0.7)",
            opacity: interpolate(frame, [80, 100], [0, 1], CLAMP),
          }}
        >
          GUARANI DAS MISSÕES · RS
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* 2 — Campo: rows drawn in perspective, sprouts popping toward the horizon. */
export const Campo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const HZ = 470;
  const rows = Array.from({ length: 25 }, (_, i) => i - 12);
  const draw = interpolate(frame, [0, 40], [0, 1], { ...CLAMP, easing: Easing.out(Easing.cubic) });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: `linear-gradient(180deg, #dce9d6 0%, ${C.mint} 60%, #f3ecd6 100%)` }} />
      <Svg style={{ scale: interpolate(frame, [0, 270], [1, 1.12]), transformOrigin: "50% 40%" }}>
        <defs>
          <linearGradient id="soil" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#8a6a45" />
            <stop offset="1" stopColor={C.soil} />
          </linearGradient>
        </defs>
        <path d={`M0 ${HZ - 30} C 300 ${HZ - 70}, 600 ${HZ - 40}, 960 ${HZ - 20} S 1600 ${HZ - 70}, 1920 ${HZ - 30} L1920 ${HZ} L0 ${HZ} Z`} fill={C.leaf} opacity={0.55} />
        <rect x={0} y={HZ} width={1920} height={1080 - HZ} fill="url(#soil)" />
        {rows.map((k) => {
          const bx = 960 + k * 190;
          const hx = 960 + k * 16;
          return (
            <line key={k} x1={hx} y1={HZ} x2={hx + (bx - hx) * draw} y2={HZ + (1080 - HZ) * draw} stroke={C.mid} strokeWidth={6 + Math.abs(k) * 0.2} opacity={0.55} strokeLinecap="round" />
          );
        })}
        {rows.map((k) =>
          Array.from({ length: 9 }, (_, j) => {
            const d = Math.pow((j + 1) / 9, 2);
            const y = HZ + (1080 - HZ) * d;
            const x = 960 + k * 16 + (k * 190 - k * 16) * d;
            const delay = 25 + (8 - j) * 6 + Math.abs(k) * 1.5;
            const s = spring({ frame: frame - delay, fps, config: { damping: 12 } }) * (0.25 + d * 1.9);
            return <Sprout key={`${k}-${j}`} x={x} y={y} s={s} angle={sway(frame, k + j, 4)} />;
          }),
        )}
      </Svg>
      <TextCol top={80} width={1300}>
        <Kicker text="CEREAIS ROHLEDER" color={C.brand} delay={20} />
        <Title text="Tudo começa no campo" size={92} color={C.deep} accent={C.mid} accentWords={["campo"]} delay={26} />
        <Body color="rgba(22, 49, 34, 0.8)" delay={44}>
          Cuidado com o solo, com a semente e com cada safra.
        </Body>
      </TextCol>
    </AbsoluteFill>
  );
};

/* 3 — Curiosidade: trigo há 10 mil anos. */
export const Trigo: React.FC = () => {
  const frame = useCurrentFrame();
  const stalks = [1040, 1150, 1260, 1370, 1480, 1590, 1700, 1810];
  return (
    <AbsoluteFill>
      <BrandBg from={C.teal} to={C.deep} />
      <Svg>
        <LeafMark x={1900} y={1300} scale={1.1} rotate={-18} opacity={0.05} />
        <path d="M900 1080 C 1200 1010, 1600 1000, 1920 1030 L1920 1080 Z" fill={C.deep} />
        {stalks.map((x, i) => (
          <Wheat
            key={x}
            x={x + rnd(`tx${i}`, -20, 20)}
            y={1060}
            h={rnd(`th${i}`, 470, 640)}
            grow={interpolate(frame, [10 + i * 7, 110 + i * 7], [0, 1], { ...CLAMP, easing: Easing.out(Easing.quad) })}
            angle={sway(frame, i * 0.9, 2.5)}
            scale={1.25}
            grains={16}
            color={i % 3 === 1 ? C.goldDark : C.gold}
          />
        ))}
      </Svg>
      <TextCol>
        <Kicker text="VOCÊ SABIA?" delay={6} />
        <div style={{ display: "flex", alignItems: "baseline", gap: 24 }}>
          <span style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 210, lineHeight: 0.95, color: C.gold, fontVariantNumeric: "tabular-nums" }}>
            {fmt(countUp(frame, 14, 70, 10000))}
          </span>
          <span style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 72, color: C.white, opacity: interpolate(frame, [60, 80], [0, 1], CLAMP) }}>anos</span>
        </div>
        <Body delay={40}>
          O trigo é cultivado pelo ser humano há mais de 10 mil anos. É um dos cereais mais antigos do mundo.
        </Body>
      </TextCol>
    </AbsoluteFill>
  );
};

/* 4 — Curiosidade: até 50 grãos por espiga (close-up). */
export const Espiga: React.FC = () => {
  const frame = useCurrentFrame();
  const shown = interpolate(frame, [16, 120], [0, 48], { ...CLAMP, easing: Easing.inOut(Easing.quad) });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 70% 90% at 72% 50%, #ffffff 0%, ${C.mint} 55%, #dfe9da 100%)` }} />
      <Svg>
        <LeafMark x={1700} y={1250} scale={1.3} rotate={-10} color={C.brand} opacity={0.06} />
        <g transform={`translate(1390 820) rotate(${8 + sway(frame, 0, 1.5)}) scale(${interpolate(frame, [0, 255], [0.98, 1.06])})`}>
          <BigEar shown={shown} />
        </g>
      </Svg>
      <TextCol>
        <Kicker text="VOCÊ SABIA?" color={C.mid} delay={6} />
        <div style={{ display: "flex", alignItems: "baseline", gap: 24 }}>
          <span style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 230, lineHeight: 0.95, color: C.brand, fontVariantNumeric: "tabular-nums" }}>
            {Math.round((shown / 48) * 50)}
          </span>
          <span style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 72, color: C.deep }}>grãos</span>
        </div>
        <Body color="rgba(22, 49, 34, 0.82)" delay={40}>
          Uma única espiga de trigo pode carregar até 50 grãos. E cada grão também é uma semente.
        </Body>
      </TextCol>
    </AbsoluteFill>
  );
};

/* 5 — Curiosidade regional: Santa Rosa, berço nacional da soja. */
export const Soja: React.FC = () => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [6, 200], [0, 1], { ...CLAMP, easing: Easing.out(Easing.quad) });
  return (
    <AbsoluteFill>
      <BrandBg from={C.brand} to={C.deep} />
      <Svg>
        <LeafMark x={1880} y={1220} scale={1} rotate={-24} opacity={0.05} />
        <path d="M980 1080 C 1200 1020, 1560 1010, 1920 1040 L1920 1080 Z" fill={C.deep} />
        <g transform="translate(1420 1060) scale(1.25)">
          <SoyPlant p={p} frame={frame} />
        </g>
      </Svg>
      <TextCol>
        <Kicker text="VOCÊ SABIA?" delay={6} />
        <span style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 200, lineHeight: 0.95, color: C.gold, fontVariantNumeric: "tabular-nums" }}>
          {countUp(frame, 12, 60, 1914)}
        </span>
        <Title text="Berço nacional da soja" size={72} delay={40} />
        <Body delay={64}>Santa Rosa, aqui nas Missões, registrou em 1914 o primeiro cultivo comercial de soja do Brasil.</Body>
      </TextCol>
    </AbsoluteFill>
  );
};

/* 6 — Curiosidade: fileiras pares no milho. */
export const Milho: React.FC = () => {
  const frame = useCurrentFrame();
  const START = 24;
  const rowsCount = frame < START ? 0 : Math.min(16, 2 * (Math.floor((frame - START) / 9) + 1));
  return (
    <AbsoluteFill>
      <BrandBg from={C.teal} to={C.deep} />
      <Svg>
        <LeafMark x={1120} y={1260} scale={0.9} rotate={10} opacity={0.05} />
        <g transform={`translate(1400 560) rotate(${14 + sway(frame, 1, 1)}) scale(${interpolate(frame, [0, 240], [0.96, 1.04])})`}>
          <CornCob frame={frame} start={START} />
        </g>
      </Svg>
      <TextCol>
        <Kicker text="VOCÊ SABIA?" delay={6} />
        <div style={{ display: "flex", alignItems: "baseline", gap: 24 }}>
          <span style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 230, lineHeight: 0.95, color: C.gold, fontVariantNumeric: "tabular-nums", minWidth: 270 }}>{rowsCount}</span>
          <span style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 72, color: C.white }}>fileiras</span>
        </div>
        <Body delay={40}>Toda espiga de milho tem um número par de fileiras de grãos. O mais comum é 16.</Body>
      </TextCol>
    </AbsoluteFill>
  );
};

/* 7 — Colheita: combine crosses the field, leaving stubble behind. */
export const Colheita: React.FC = () => {
  const frame = useCurrentFrame();
  const hx = interpolate(frame, [0, 270], [-760, 1500]);
  const GY = 930;
  const SC = 0.9;
  const cutLine = hx + 560 * SC;
  const band = (y: number, gapX: number, h: number, color: string, key: string, cuts: boolean) =>
    Array.from({ length: Math.ceil(1960 / gapX) }, (_, i) => {
      const x = i * gapX + rnd(`${key}${i}`, -gapX * 0.4, gapX * 0.4);
      return <MiniWheat key={`${key}${i}`} x={x} y={y + rnd(`${key}y${i}`, -6, 6)} h={h * rnd(`${key}h${i}`, 0.85, 1.1)} angle={sway(frame, x * 0.01, 2.5)} color={color} cut={cuts && x < cutLine} />;
    });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, #d7e6d2 0%, #eef0dc 55%, #f3e7c4 100%)" }} />
      <Svg>
        <path d="M0 610 C 260 560, 520 590, 760 600 S 1300 560, 1920 600 L1920 660 L0 660 Z" fill={C.teal} opacity={0.5} />
        {Array.from({ length: 14 }, (_, i) => (
          <circle key={i} cx={1180 + i * 46 + rnd(`tr${i}`, -10, 10)} cy={618 + rnd(`ty${i}`, -8, 8)} r={rnd(`trr${i}`, 22, 40)} fill={C.brand} opacity={0.75} />
        ))}
        <g transform="translate(250 640)" fill="#e9ede4">
          <rect x={0} y={-170} width={80} height={170} />
          <path d="M0 -170 Q 40 -215 80 -170 Z" />
          <rect x={95} y={-130} width={70} height={130} />
          <path d="M95 -130 Q 130 -170 165 -130 Z" />
          <rect x={0} y={-110} width={165} height={6} fill={C.teal} opacity={0.4} />
        </g>
        <rect x={0} y={640} width={1920} height={440} fill="url(#field)" />
        <defs>
          <linearGradient id="field" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#d7b562" />
            <stop offset="1" stopColor="#b78b37" />
          </linearGradient>
        </defs>
        {band(670, 13, 26, "#c49a45", "a", false)}
        {band(720, 15, 36, "#b98d3c", "b", false)}
        {band(790, 17, 48, "#a97f33", "c", false)}
        {band(860, 19, 62, C.goldDark, "d", true)}
        {band(905, 20, 70, "#a77a2c", "e", true)}
        {Array.from({ length: 36 }, (_, i) => {
          const birth = i * 7;
          const age = frame - birth;
          if (age < 0 || age > 70) return null;
          const ox = interpolate(birth, [0, 270], [-760, 1500]);
          return (
            <ellipse key={i} cx={ox - 40 - age * 2.4 + rnd(`dx${i}`, -30, 30)} cy={GY - 230 - age * 1.4 + rnd(`dy${i}`, -20, 20)} rx={rnd(`dr${i}`, 18, 40)} ry={rnd(`dr${i}`, 10, 22)} fill="#e7d3a0" opacity={(1 - age / 70) * 0.35} />
          );
        })}
        <g transform={`translate(${hx} ${GY}) scale(${SC})`}>
          <Harvester dist={hx + 760} />
        </g>
        {band(1050, 24, 96, "#9c7029", "f", false)}
      </Svg>
      <TextCol top={70}>
        <Kicker text="NO CAMPO" color={C.brand} delay={8} />
        <Title text="Tecnologia na colheita" size={84} color={C.deep} accent={C.mid} accentWords={["colheita"]} delay={14} />
        <Body color="rgba(22, 49, 34, 0.82)" delay={34} size={32}>
          A colheitadeira corta, debulha e separa os grãos da palha em uma única passada.
        </Body>
      </TextCol>
    </AbsoluteFill>
  );
};

/* 8 — Curiosidade: safra brasileira; grain pours from a spout onto a growing pile. */
export const Graos: React.FC = () => {
  const frame = useCurrentFrame();
  const PX = 1430;
  const NY = 250;
  const H = interpolate(frame, [0, 200], [40, 380], { ...CLAMP, easing: Easing.out(Easing.quad) });
  const pileY = (x: number) => 1090 - H * Math.exp(-Math.pow((x - PX) / 300, 2));
  const pilePath = `M${PX - 900} 1090 ` + Array.from({ length: 61 }, (_, i) => {
    const x = PX - 900 + i * 30;
    return `L${x} ${pileY(x).toFixed(1)}`;
  }).join(" ") + ` L${PX + 900} 1090 Z`;
  return (
    <AbsoluteFill>
      <BrandBg from={C.brand} to={C.deep} />
      <Svg>
        <defs>
          <clipPath id="pile">
            <path d={pilePath} />
          </clipPath>
        </defs>
        {Array.from({ length: 280 }, (_, i) => {
          const birth = i * 0.72;
          const age = frame - birth;
          if (age < 0) return null;
          const x = PX + rnd(`gx${i}`, -26, 26) + age * rnd(`gv${i}`, -1.4, 1.4);
          const y = NY + 0.6 * age * age;
          if (y > pileY(x)) return null;
          return <ellipse key={i} cx={x} cy={y} rx={7} ry={10} transform={`rotate(${rnd(`gr${i}`, 0, 180) + age * 6} ${x} ${y})`} fill={i % 4 === 0 ? C.goldDark : C.gold} />;
        })}
        <path d={pilePath} fill={C.gold} />
        <g clipPath="url(#pile)">
          {Array.from({ length: 420 }, (_, i) => (
            <ellipse key={i} cx={rnd(`px${i}`, PX - 700, PX + 600)} cy={rnd(`py${i}`, 680, 1090)} rx={8} ry={11} transform={`rotate(${rnd(`pr${i}`, 0, 180)})`} style={{ transformBox: "fill-box", transformOrigin: "center" }} fill={i % 3 === 0 ? C.goldDark : "#efc969"} opacity={0.9} />
          ))}
        </g>
        <path d={`M1920 140 L${PX + 60} 200`} stroke={C.dark} strokeWidth={56} strokeLinecap="round" />
        <path d={`M${PX + 40} 190 L${PX} ${NY - 6}`} stroke={C.dark} strokeWidth={48} strokeLinecap="round" />
        <path d={`M1920 140 L${PX + 60} 200`} stroke={C.white} strokeWidth={6} opacity={0.15} />
      </Svg>
      <TextCol width={720}>
        <Kicker text="VOCÊ SABIA?" delay={6} />
        <span style={{ fontFamily: HEAD, fontWeight: 900, fontSize: 210, lineHeight: 0.95, color: C.gold, fontVariantNumeric: "tabular-nums" }}>
          +{countUp(frame, 12, 70, 300)}
        </span>
        <Title text="milhões de toneladas" size={68} delay={34} />
        <Body delay={56}>de grãos são colhidas no Brasil a cada safra.</Body>
        <Body delay={70} size={22} color="rgba(255, 255, 255, 0.5)">
          Fonte: Conab
        </Body>
      </TextCol>
    </AbsoluteFill>
  );
};

/* 9 — Encerramento: full logo and contact. */
export const Final: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - 4, fps, config: { damping: 16 } });
  return (
    <AbsoluteFill>
      <BrandBg />
      <Svg>
        <LeafMark x={1580} y={1240} scale={1.3} rotate={-4 + frame * 0.03} opacity={0.08} />
        <LeafMark x={300} y={1200} scale={0.7} rotate={16} opacity={0.05} />
        <FieldEdge color={C.dark} />
      </Svg>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <Img src={staticFile("cereais/logo.png")} style={{ width: 760, scale: 0.85 + 0.15 * s, opacity: s }} />
        <div
          style={{
            marginTop: 48,
            textAlign: "center",
            fontFamily: BODY,
            fontSize: 30,
            lineHeight: 1.5,
            color: "rgba(255, 255, 255, 0.85)",
            opacity: interpolate(frame, [24, 40], [0, 1], CLAMP),
            translate: `0px ${interpolate(frame, [24, 44], [16, 0], { ...CLAMP, easing: Easing.out(Easing.cubic) })}px`,
          }}
        >
          Linha Bom Jardim · Guarani das Missões/RS
          <br />
          <span style={{ fontWeight: 700 }}>(55) 99623-3792</span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
