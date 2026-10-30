import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { FONT } from "./fonts";

const GREEN = "#22c55e";

type Word = { readonly text: string; readonly accent?: boolean };

const WORDS: Word[] = [
  { text: "3", accent: true },
  { text: "sinais" },
  { text: "de" },
  { text: "que" },
  { text: "o" },
  { text: "consórcio", accent: true },
  { text: "é" },
  { text: "melhor" },
  { text: "que" },
  { text: "o" },
  { text: "financiamento" },
];

const PUNCH = 4 + 5 * 2; // frame "consórcio" lands

export const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const shake = frame >= PUNCH && frame < PUNCH + 8 ? (frame % 2 === 0 ? 1 : -1) * (PUNCH + 8 - frame) * 1.6 : 0;

  return (
    <AbsoluteFill
      style={{
        padding: "0 90px",
        justifyContent: "center",
        scale: interpolate(frame, [0, 75], [1.0, 1.07], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        translate: `${shake}px ${-shake / 2}px`,
      }}
    >
      <div
        style={{
          alignSelf: "flex-start",
          padding: "14px 28px",
          borderRadius: 999,
          backgroundColor: GREEN,
          color: "#04140a",
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: 34,
          letterSpacing: "0.12em",
          scale: interpolate(frame, [0, 12], [0.4, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.spring({ damping: 8 }),
            output: "perceptual-scale",
          }),
          rotate: interpolate(frame, [0, 12], ["-8deg", "0deg"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.spring({ damping: 8 }),
          }),
        }}
      >
        CONSÓRCIO × FINANCIAMENTO
      </div>
      <h1
        style={{
          margin: "48px 0 0",
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: 124,
          lineHeight: 1.0,
          letterSpacing: "-0.03em",
          color: "#ffffff",
        }}
      >
        {WORDS.map((w, i) => {
          const start = 4 + i * 2;
          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                marginRight: "0.22em",
                color: w.accent ? GREEN : "#ffffff",
                textShadow: w.accent ? "0 0 40px rgba(34, 197, 94, 0.55)" : "none",
                opacity: interpolate(frame, [start, start + 4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
                translate: interpolate(frame, [start, start + 16], ["0px 110px", "0px 0px"], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                  easing: Easing.spring({ damping: 8 }),
                }),
                scale: interpolate(frame, [start, start + 16], [w.accent ? 1.9 : 0.55, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                  easing: Easing.spring({ damping: 8 }),
                  output: "perceptual-scale",
                }),
                rotate: interpolate(frame, [start, start + 16], [w.accent ? "-10deg" : "6deg", "0deg"], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                  easing: Easing.spring({ damping: 8 }),
                }),
              }}
            >
              {w.text}
            </span>
          );
        })}
      </h1>
    </AbsoluteFill>
  );
};
