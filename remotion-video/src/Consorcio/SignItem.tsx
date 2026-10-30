import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { FONT } from "./fonts";

const GREEN = "#22c55e";

type Props = {
  readonly index: number;
  readonly title: string;
  readonly body: string;
  /** Frame (inside the list scene) at which the next item takes focus; this one dims. */
  readonly dimAt?: number;
};

// One sign of the list: springs in from the side, then dims when the next one arrives.
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
          : interpolate(frame, [dimAt, dimAt + 0.3 * fps], [1, 0.38], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        translate: interpolate(frame, [0, 0.9 * fps], ["-140px 0px", "0px 0px"], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.spring({ damping: 10 }),
        }),
      }}
    >
      <div
        style={{
          flex: "0 0 auto",
          width: 132,
          height: 132,
          borderRadius: 32,
          backgroundColor: GREEN,
          color: "#04140a",
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: 84,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          scale: interpolate(frame, [0, 0.7 * fps], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.spring({ damping: 8 }),
            output: "perceptual-scale",
          }),
          rotate: interpolate(frame, [0, 0.7 * fps], ["-25deg", "0deg"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.spring({ damping: 8 }),
          }),
        }}
      >
        {index}
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
            opacity: interpolate(frame, [3, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
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
            color: "rgba(255, 255, 255, 0.72)",
            opacity: interpolate(frame, [10, 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
            translate: interpolate(frame, [10, 28], ["0px 24px", "0px 0px"], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.spring({ damping: 14 }),
            }),
          }}
        >
          {body}
        </div>
      </div>
    </div>
  );
};
