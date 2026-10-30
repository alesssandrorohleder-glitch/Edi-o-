import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { FONT } from "./fonts";

const GREEN = "#22c55e";
const brl = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });

type Props = { readonly target: number };

export const Savings: React.FC<Props> = ({ target }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const value = interpolate(frame, [0.3 * fps, 2.1 * fps], [0, target], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  return (
    <AbsoluteFill style={{ padding: "0 90px", justifyContent: "center", alignItems: "center", textAlign: "center" }}>
      <div
        style={{
          fontFamily: FONT,
          fontWeight: 800,
          fontSize: 40,
          letterSpacing: "0.14em",
          color: "rgba(255, 255, 255, 0.75)",
          opacity: interpolate(frame, [0, 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
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
          textShadow: "0 0 60px rgba(34, 197, 94, 0.45)",
          scale: interpolate(frame, [0, 0.8 * fps], [0.7, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.spring({ damping: 9 }),
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
          opacity: interpolate(frame, [1.4 * fps, 1.8 * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          translate: interpolate(frame, [1.4 * fps, 2.2 * fps], ["0px 30px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.spring({ damping: 12 }),
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
          opacity: interpolate(frame, [1.8 * fps, 2.2 * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        Valor ilustrativo. Simule o seu caso.
      </div>
    </AbsoluteFill>
  );
};
