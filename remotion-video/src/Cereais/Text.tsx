import { Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { BODY, C, CLAMP, HEAD } from "./theme";

// "C E R E A I S"-style spaced kicker with a short rule, like the brand card.
export const Kicker: React.FC<{ readonly text: string; readonly color?: string; readonly delay?: number }> = ({
  text,
  color = C.gold,
  delay = 0,
}) => {
  const frame = useCurrentFrame() - delay;
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 22,
        fontFamily: BODY,
        fontWeight: 500,
        fontSize: 28,
        letterSpacing: "0.4em",
        color,
        opacity: interpolate(frame, [0, 12], [0, 1], CLAMP),
        translate: `${interpolate(frame, [0, 20], [-40, 0], { ...CLAMP, easing: Easing.out(Easing.cubic) })}px 0px`,
      }}
    >
      <div style={{ width: interpolate(frame, [4, 24], [0, 60], { ...CLAMP, easing: Easing.out(Easing.cubic) }), height: 3, backgroundColor: color }} />
      {text}
    </div>
  );
};

// Heavy rounded headline; each word rises out of a mask.
export const Title: React.FC<{
  readonly text: string;
  readonly size?: number;
  readonly color?: string;
  readonly accent?: string;
  readonly accentWords?: readonly string[];
  readonly delay?: number;
  readonly align?: "left" | "center";
}> = ({ text, size = 96, color = C.white, accent = C.gold, accentWords = [], delay = 0, align = "left" }) => {
  const frame = useCurrentFrame() - delay;
  const { fps } = useVideoConfig();
  return (
    <div
      style={{
        fontFamily: HEAD,
        fontWeight: 900,
        fontSize: size,
        lineHeight: 1.04,
        letterSpacing: "-0.01em",
        color,
        textAlign: align,
      }}
    >
      {text.split(" ").map((w, i) => {
        const p = spring({ frame: frame - i * 3, fps, config: { damping: 18, mass: 0.8 } });
        return (
          <span key={i} style={{ display: "inline-block", overflow: "hidden", verticalAlign: "bottom", paddingBottom: "0.08em", marginBottom: "-0.08em" }}>
            <span
              style={{
                display: "inline-block",
                marginRight: "0.24em",
                color: accentWords.includes(w) ? accent : color,
                translate: `0px ${(1 - p) * 110}%`,
              }}
            >
              {w}
            </span>
          </span>
        );
      })}
    </div>
  );
};

export const Body: React.FC<{ readonly children: React.ReactNode; readonly color?: string; readonly delay?: number; readonly size?: number; readonly italic?: boolean }> = ({
  children,
  color = "rgba(255, 255, 255, 0.82)",
  delay = 0,
  size = 36,
  italic = false,
}) => {
  const frame = useCurrentFrame() - delay;
  return (
    <div
      style={{
        fontFamily: BODY,
        fontWeight: italic ? 400 : 400,
        fontStyle: italic ? "italic" : "normal",
        fontSize: size,
        lineHeight: 1.4,
        color,
        opacity: interpolate(frame, [0, 14], [0, 1], CLAMP),
        translate: `0px ${interpolate(frame, [0, 22], [24, 0], { ...CLAMP, easing: Easing.out(Easing.cubic) })}px`,
      }}
    >
      {children}
    </div>
  );
};

export const countUp = (frame: number, start: number, dur: number, to: number) =>
  Math.round(interpolate(frame, [start, start + dur], [0, to], { ...CLAMP, easing: Easing.bezier(0.25, 0.1, 0.25, 1) }));

export const fmt = (n: number) => new Intl.NumberFormat("pt-BR").format(n);
