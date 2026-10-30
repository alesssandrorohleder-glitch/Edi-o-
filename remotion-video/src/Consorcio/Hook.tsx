import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { FONT } from "./fonts";

const GREEN = "#22c55e";

type Word = { readonly text: string; readonly accent?: boolean };

const WORDS: Word[] = [
  { text: "3" , accent: true },
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

export const Hook: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ padding: "0 90px", justifyContent: "center" }}>
      <div
        style={{
          alignSelf: "flex-start",
          padding: "14px 28px",
          borderRadius: 999,
          border: `3px solid ${GREEN}`,
          color: GREEN,
          fontFamily: FONT,
          fontWeight: 800,
          fontSize: 34,
          letterSpacing: "0.12em",
          opacity: interpolate(frame, [0, 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          translate: interpolate(frame, [0, 18], ["0px 30px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.spring({ damping: 12 }),
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
          const start = 6 + i * 3;
          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                marginRight: "0.22em",
                color: w.accent ? GREEN : "#ffffff",
                opacity: interpolate(frame, [start, start + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
                translate: interpolate(frame, [start, start + 24], ["0px 90px", "0px 0px"], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                  easing: Easing.spring({ damping: 9 }),
                }),
                scale: interpolate(frame, [start, start + 24], [0.6, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                  easing: Easing.spring({ damping: 9 }),
                  output: "perceptual-scale",
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
