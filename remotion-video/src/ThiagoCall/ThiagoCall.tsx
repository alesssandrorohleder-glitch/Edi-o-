import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Audio } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import { FONT } from "../Consorcio/fonts";
import {
  DURATION,
  LEAD,
  type Line,
  QUESTION,
  SEGMENT_A,
  SEGMENT_B,
  TEAR,
} from "./timeline";

const MONO = "IBM Plex Mono";
for (const weight of ["500", "600"]) {
  loadFont({ family: MONO, url: staticFile(`fonts/IBMPlexMono-${weight}.woff2`), weight });
}

const W = 1080;
const H = 1920;
const HEAD = 1500; // world y of the printer slot
const TAPE_W = 860;
const TAPE_X = (W - TAPE_W) / 2;
const INK = "#2b2724";
const GREEN = "#22c55e";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const easeOut = Easing.bezier(0.16, 1, 0.3, 1);
const soft = Easing.bezier(0.45, 0, 0.15, 1);

// How much paper a list of lines has pushed out of the slot at frame t.
const fed = (lines: Line[], t: number) =>
  lines.reduce((sum, l) => sum + l.h * interpolate(t, [l.at, l.at + l.dur], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) }), 0);

const tops = (lines: Line[]) => {
  let y = 0;
  return lines.map((l) => {
    const top = y;
    y += l.h;
    return top;
  });
};
const length = (lines: Line[]) => lines.reduce((s, l) => s + l.h, 0);

const LEN_A = length(SEGMENT_A);
const TOPS_A = tops(SEGMENT_A);
const TOPS_B = tops(SEGMENT_B);

const feedAt = (t: number) => LEAD + fed(SEGMENT_A, t) + fed(SEGMENT_B, t);

// Camera: scale and how far above the slot the frame centre sits.
const CAM: ReadonlyArray<readonly [number, number, number]> = [
  [0, 1.22, 330],
  [100, 1.2, 340],
  [170, 1.16, 370],
  [268, 1.02, 430],
  [292, 0.98, 480],
  [392, 0.6, 700],
  [424, 0.59, 700],
  [468, 1.16, 260],
  [486, 1.17, 260],
  [514, 1.3, 150],
  [548, 1.3, 210],
  [600, 1.26, 300],
  [722, 1.24, 400],
  [DURATION, 1.24, 400],
];

const camera = (t: number) => {
  const frames = CAM.map((k) => k[0]);
  const s = interpolate(t, frames, CAM.map((k) => k[1]), { ...clamp, easing: soft });
  const above = interpolate(t, frames, CAM.map((k) => k[2]), { ...clamp, easing: soft });
  return { s, fy: HEAD - above };
};

const Check: React.FC<{ readonly size: number; readonly color: string; readonly progress?: number }> = ({ size, color, progress = 1 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" style={{ display: "inline-block", verticalAlign: "-0.12em", marginLeft: 14 }}>
    <path
      d="M4 12.5l5 5L20 6.5"
      fill="none"
      stroke={color}
      strokeWidth={2.6}
      strokeLinecap="round"
      strokeLinejoin="round"
      pathLength={1}
      strokeDasharray={1}
      strokeDashoffset={1 - progress}
    />
  </svg>
);

const PrintedLine: React.FC<{ readonly line: Line; readonly t: number }> = ({ line, t }) => {
  const base: React.CSSProperties = { position: "absolute", left: 44, right: 40, color: INK, whiteSpace: "pre" };
  switch (line.kind) {
    case "item":
      return (
        <div style={{ ...base, top: 14, fontFamily: MONO, fontWeight: 500, fontSize: 46, lineHeight: "60px" }}>
          {line.text}
          {line.check ? <Check size={44} color={INK} /> : null}
        </div>
      );
    case "big":
      return (
        <div style={{ ...base, top: 23, fontFamily: MONO, fontWeight: 600, fontSize: 64, lineHeight: "74px", letterSpacing: "-0.02em" }}>
          {line.text}
        </div>
      );
    case "stream":
      return (
        <div style={{ ...base, top: 8, fontFamily: MONO, fontWeight: 500, fontSize: 40, lineHeight: "50px", opacity: 0.82 }}>
          {line.text}
        </div>
      );
    case "rule":
      return <div style={{ position: "absolute", left: 56, right: 56, top: 20, borderTop: `4px dashed ${INK}`, opacity: 0.7 }} />;
    case "total": {
      const p = interpolate(t, [QUESTION, QUESTION + 9], [0, 1], { ...clamp, easing: easeOut });
      return (
        <>
          <div style={{ ...base, top: 150, fontFamily: MONO, fontWeight: 600, fontSize: 76, lineHeight: "90px", letterSpacing: "-0.02em" }}>
            {line.text}
          </div>
          {t >= QUESTION ? (
            <div
              style={{
                position: "absolute",
                right: 56,
                top: -40,
                fontFamily: MONO,
                fontWeight: 600,
                fontSize: 330,
                lineHeight: "300px",
                color: INK,
                transform: `scale(${interpolate(p, [0, 1], [3.5, 1])})`,
                transformOrigin: "50% 60%",
                filter: `blur(${interpolate(p, [0, 1], [10, 0])}px)`,
              }}
            >
              ?
            </div>
          ) : null}
        </>
      );
    }
    case "handle": {
      const check = interpolate(t, [line.at + 12, line.at + 24], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
      return (
        <div style={{ ...base, top: 30, fontFamily: FONT, fontWeight: 800, fontSize: 54, lineHeight: "70px", letterSpacing: "-0.02em" }}>
          {line.text}
          <Check size={58} color={GREEN} progress={check} />
        </div>
      );
    }
    default:
      return null;
  }
};

// Calculator keys below the slot; "=" is pressed just before the total prints.
const KEYS = [
  ["7", "8", "9", "×", "−"],
  ["4", "5", "6", "+", "="],
];
const PRESS = 397;

const Keys: React.FC<{ readonly t: number }> = ({ t }) => {
  const press = interpolate(t, [PRESS, PRESS + 2, PRESS + 7], [0, 1, 0], clamp);
  return (
    <>
      {KEYS.flatMap((row, r) =>
        row.map((label, c) => {
          const down = label === "=" ? press : 0;
          return (
            <div
              key={label}
              style={{
                position: "absolute",
                left: W / 2 - 535 + c * 220,
                top: HEAD + 120 + r * 168 + down * 7,
                width: 190,
                height: 128,
                borderRadius: 26,
                background: `linear-gradient(180deg, ${down > 0.5 ? "#1f1e21" : "#2f2d31"} 0%, #1b1a1d 100%)`,
                boxShadow: `inset 0 2px 0 rgba(255,235,210,0.14), 0 ${10 - down * 7}px ${18 - down * 10}px rgba(0,0,0,0.6)`,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontFamily: FONT,
                fontWeight: 500,
                fontSize: 58,
                color: "rgba(236,228,214,0.72)",
              }}
            >
              {label}
            </div>
          );
        }),
      )}
    </>
  );
};

// Zigzag edge for torn paper (teeth 22 px wide, 10 px deep).
const zigzag = (edge: "top" | "bottom") => {
  const teeth = Math.round(TAPE_W / 22);
  const pts: string[] = [];
  for (let i = 0; i <= teeth; i++) {
    const x = (i / teeth) * 100;
    const deep = i % 2 === 0 ? 0 : 10;
    pts.push(edge === "top" ? `${x}% ${deep}px` : `${x}% calc(100% - ${deep}px)`);
  }
  return edge === "top"
    ? `polygon(${pts.join(", ")}, 100% 100%, 0% 100%)`
    : `polygon(0% 0%, 100% 0%, ${pts.reverse().join(", ")})`;
};

const paperStyle = (height: number): React.CSSProperties => ({
  position: "absolute",
  left: 0,
  width: TAPE_W,
  height,
  backgroundColor: "#f1ece1",
  backgroundImage: `linear-gradient(90deg, rgba(60,40,20,0.16), rgba(60,40,20,0) 14%, rgba(255,250,240,0.18) 70%, rgba(60,40,20,0.12)), url(${staticFile("thiago/paper.png")})`,
  backgroundSize: "100% 100%, 512px 512px",
});

const Segment: React.FC<{
  readonly lines: Line[];
  readonly lineTops: number[];
  readonly t: number;
  readonly lead: number;
  readonly height: number;
  readonly clip?: string;
}> = ({ lines, lineTops, t, lead, height, clip }) => (
  <div style={{ ...paperStyle(height), clipPath: clip }}>
    {lines.map((line, i) =>
      t >= line.at ? (
        <div key={i} style={{ position: "absolute", left: 0, right: 0, top: lead + lineTops[i], height: line.h }}>
          <PrintedLine line={line} t={t} />
        </div>
      ) : null,
    )}
  </div>
);

export const ThiagoCall: React.FC = () => {
  const t = useCurrentFrame();
  const F = feedAt(t);
  const v = F - feedAt(t - 1);
  const { s, fy } = camera(t);

  // The jolt when the "?" lands.
  const jolt = t >= QUESTION ? 16 * Math.exp(-(t - QUESTION) / 3.5) * Math.sin((t - QUESTION) * 2.4) : 0;
  const fx = W / 2 + 14 * Math.sin(t / 70);
  const tx = W / 2 - fx * s;
  const ty = H / 2 - fy * s + jolt;

  // Tear: tension, then the top piece is yanked up and out of frame.
  const tension = interpolate(t, [TEAR - 8, TEAR], [0, -16], { ...clamp, easing: Easing.in(Easing.quad) });
  const yank = interpolate(t, [TEAR, TEAR + 26], [0, -2900], { ...clamp, easing: Easing.in(Easing.cubic) });
  const yankRot = interpolate(t, [TEAR, TEAR + 26], [0, -9], { ...clamp, easing: Easing.in(Easing.quad) });
  const torn = t >= TEAR;

  const tapeTop = HEAD - F;
  const blur = Math.min(Math.abs(v) * s * 0.42, 38);
  const breathe = 1 + 0.04 * Math.sin(t / 22);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d0907", overflow: "hidden" }}>
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <filter id="feedblur" x="-5%" y="-20%" width="110%" height="140%">
          <feGaussianBlur stdDeviation={`0 ${blur.toFixed(2)}`} />
        </filter>
      </svg>

      <div style={{ position: "absolute", left: 0, top: 0, transformOrigin: "0 0", transform: `translate(${tx}px, ${ty}px) scale(${s})` }}>
        {/* Desk */}
        <Img
          src={staticFile("thiago/desk.jpg")}
          style={{ position: "absolute", left: -900, top: HEAD - 2900, width: 2900, height: 4100, filter: "blur(1.5px)" }}
        />

        {/* Paper, clipped at the slot */}
        <div style={{ position: "absolute", left: TAPE_X - 200, top: HEAD - 12000, width: TAPE_W + 400, height: 12000, overflow: "hidden" }}>
          <div style={{ position: "absolute", left: 200, top: 12000 - HEAD, width: TAPE_W, filter: blur > 0.6 ? "url(#feedblur)" : undefined }}>
            {/* Segment A: from the lead paper to the total */}
            <div
              style={{
                position: "absolute",
                left: 0,
                top: tapeTop + (torn ? yank : tension),
                transformOrigin: "100% 100%",
                transform: `rotate(${torn ? yankRot : 0}deg)`,
                filter: "drop-shadow(-22px 26px 26px rgba(0,0,0,0.55))",
              }}
            >
              <Segment lines={SEGMENT_A} lineTops={TOPS_A} t={t} lead={LEAD} height={LEAD + LEN_A} clip={torn ? zigzag("bottom") : undefined} />
            </div>
            {/* Segment B: the clean tape after the tear */}
            <div style={{ position: "absolute", left: 0, top: tapeTop + LEAD + LEN_A, filter: "drop-shadow(-22px 26px 26px rgba(0,0,0,0.55))" }}>
              <Segment lines={SEGMENT_B} lineTops={TOPS_B} t={t} lead={0} height={2600} clip={torn ? zigzag("top") : undefined} />
            </div>
          </div>
        </div>

        {/* Printer body, slot and tear bar */}
        <div
          style={{
            position: "absolute",
            left: W / 2 - 640,
            top: HEAD - 26,
            width: 1280,
            height: 1300,
            borderRadius: "46px 46px 0 0",
            background: "linear-gradient(180deg, #343236 0%, #1c1b1e 9%, #141316 100%)",
            boxShadow: "inset 0 2px 0 rgba(255,235,210,0.16), 0 -18px 50px rgba(0,0,0,0.45)",
          }}
        />
        <Keys t={t} />
        <div style={{ position: "absolute", left: W / 2 - 480, top: HEAD - 7, width: 960, height: 16, borderRadius: 8, background: "#050405" }} />
        <div
          style={{
            position: "absolute",
            left: W / 2 - 470,
            top: HEAD - 22,
            width: 940,
            height: 20,
            background: "linear-gradient(180deg, #d9d6d0, #8d8a86 55%, #5b5956)",
            clipPath: zigzag("bottom"),
            boxShadow: "0 6px 10px rgba(0,0,0,0.5)",
          }}
        />
      </div>

      {/* Lamp: warm key from top right, falloff and vignette */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 90% 60% at 82% 8%, rgba(255,182,112,${0.2 * breathe}), rgba(255,182,112,0) 70%)`,
          mixBlendMode: "screen",
        }}
      />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 85% 75% at 62% 38%, rgba(0,0,0,0) 35%, rgba(0,0,0,0.62) 100%)" }} />
      <AbsoluteFill
        style={{
          backgroundImage: `url(${staticFile(`thiago/grain${t % 4}.png`)})`,
          backgroundSize: "512px 512px",
          mixBlendMode: "overlay",
          opacity: 0.32,
        }}
      />

      <Audio src={staticFile("thiago/mix.wav")} />
    </AbsoluteFill>
  );
};
