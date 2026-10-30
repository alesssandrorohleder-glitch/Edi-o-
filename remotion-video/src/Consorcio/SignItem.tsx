import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { FONT } from "./fonts";

const GREEN = "#22c55e";

type Props = {
  readonly index: number;
  readonly title: string;
  readonly body: string;
  /** Frame (inside this item's sequence) at which the next item takes focus; this one dims. */
  readonly dimAt?: number;
};

// One sign of the list: badge pops with a ring burst, text whips in from the side, then dims.
export const SignItem: React.FC<Props> = ({ index, title, body, dimAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        display: "flex",
        gap: 40,
        alignItems: "flex-start",
        opacity: dimAt === undefined
          ? 1
          : interpolate(frame, [dimAt, dimAt + 0.25 * fps], [1, 0.35], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        scale: dimAt === undefined
          ? 1
          : interpolate(frame, [dimAt, dimAt + 0.3 * fps], [1, 0.94], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.bezier(0.16, 1, 0.3, 1),
            }),
        transformOrigin: "0% 50%",
      }}
    >
      <div style={{ position: "relative", flex: "0 0 auto", width: 132, height: 132 }}>
        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: 40,
            border: `6px solid ${GREEN}`,
            scale: interpolate(frame, [2, 18], [0.8, 2.1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.16, 1, 0.3, 1) }),
            opacity: interpolate(frame, [2, 18], [0.9, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          }}
        />
        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: 32,
            backgroundColor: GREEN,
            color: "#04140a",
            fontFamily: FONT,
            fontWeight: 900,
            fontSize: 84,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 0 50px rgba(34, 197, 94, 0.45)",
            scale: interpolate(frame, [0, 0.6 * fps], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.spring({ damping: 7 }),
              output: "perceptual-scale",
            }),
            rotate: interpolate(frame, [0, 0.6 * fps], ["-40deg", "0deg"], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.spring({ damping: 7 }),
            }),
          }}
        >
          {index}
        </div>
      </div>
      <div style={{ flex: 1 }}>
        <div
          style={{
            fontFamily: FONT,
            fontWeight: 900,
            fontSize: 76,
            lineHeight: 1.02,
            letterSpacing: "-0.025em",
            color: "#ffffff",
            opacity: interpolate(frame, [2, 7], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
            translate: interpolate(frame, [2, 0.6 * fps], ["220px 0px", "0px 0px"], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.spring({ damping: 9 }),
            }),
          }}
        >
          {title}
        </div>
        <div
          style={{
            marginTop: 18,
            fontFamily: FONT,
            fontWeight: 500,
            fontSize: 42,
            lineHeight: 1.3,
            color: "rgba(255, 255, 255, 0.75)",
            opacity: interpolate(frame, [8, 15], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
            translate: interpolate(frame, [8, 24], ["0px 30px", "0px 0px"], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.spring({ damping: 12 }),
            }),
          }}
        >
          {body}
        </div>
      </div>
    </div>
  );
};
