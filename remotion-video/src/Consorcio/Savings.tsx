import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { FONT } from "./fonts";

const GREEN = "#22c55e";
const brl = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });

// Fixed particle layout (x %, start delay in frames, rise in px, size) so every render is identical.
const PARTICLES = [
  [8, 0, 900, 46], [18, 6, 760, 34], [27, 2, 980, 54], [36, 10, 820, 30], [45, 4, 1000, 42],
  [54, 12, 700, 36], [63, 1, 940, 50], [72, 8, 860, 32], [81, 3, 1020, 44], [90, 9, 780, 38],
  [14, 14, 880, 28], [50, 16, 960, 30], [86, 13, 900, 26],
] as const;

type Props = { readonly target: number };

export const Savings: React.FC<Props> = ({ target }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const land = Math.round(1.5 * fps);
  const value = interpolate(frame, [4, land], [0, target], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.33, 0, 0.2, 1),
  });

  return (
    <AbsoluteFill style={{ padding: "0 90px", justifyContent: "center", alignItems: "center", textAlign: "center" }}>
      {PARTICLES.map(([x, delay, rise, size], i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: `${x}%`,
            top: 1500,
            fontFamily: FONT,
            fontWeight: 900,
            fontSize: size,
            color: GREEN,
            opacity: interpolate(frame, [delay, delay + 8, delay + 40, delay + 60], [0, 0.85, 0.5, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
            translate: interpolate(frame, [delay, delay + 60], ["0px 0px", `0px ${-rise}px`], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.bezier(0.2, 0.6, 0.3, 1),
            }),
          }}
        >
          {i % 3 === 0 ? "R$" : "+"}
        </div>
      ))}
      <div
        style={{
          fontFamily: FONT,
          fontWeight: 800,
          fontSize: 40,
          letterSpacing: "0.14em",
          color: "rgba(255, 255, 255, 0.8)",
          opacity: interpolate(frame, [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        ECONOMIA POSSÍVEL
      </div>
      <div
        style={{
          marginTop: 30,
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: 158,
          letterSpacing: "-0.04em",
          lineHeight: 1,
          color: GREEN,
          fontVariantNumeric: "tabular-nums",
          textShadow: `0 0 ${interpolate(frame, [land, land + 10], [110, 55], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}px rgba(34, 197, 94, 0.55)`,
          scale: frame < land
            ? interpolate(frame, [0, 10], [0.6, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                easing: Easing.spring({ damping: 9 }),
                output: "perceptual-scale",
              })
            : interpolate(frame, [land, land + 14], [1.16, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                easing: Easing.spring({ damping: 7 }),
                output: "perceptual-scale",
              }),
        }}
      >
        {brl.format(Math.round(value))}
      </div>
      <div
        style={{
          marginTop: 44,
          fontFamily: FONT,
          fontWeight: 800,
          fontSize: 56,
          lineHeight: 1.15,
          color: "#ffffff",
          opacity: interpolate(frame, [land - 6, land + 2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          translate: interpolate(frame, [land - 6, land + 12], ["0px 30px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.spring({ damping: 10 }),
          }),
        }}
      >
        sem pagar juros
      </div>
      <div
        style={{
          marginTop: 28,
          fontFamily: FONT,
          fontWeight: 500,
          fontSize: 30,
          color: "rgba(255, 255, 255, 0.5)",
          opacity: interpolate(frame, [land, land + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        Valor ilustrativo. Simule o seu caso.
      </div>
    </AbsoluteFill>
  );
};
