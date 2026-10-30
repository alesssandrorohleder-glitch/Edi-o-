import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";

// A skewed dark-green panel that sweeps bottom-to-top across the cut (16 frames, cut at frame 8).
export const GreenWipe: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ overflow: "hidden", pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          left: -200,
          right: -200,
          top: 0,
          height: 2600,
          backgroundColor: "#0c2416",
          rotate: "-8deg",
          translate: interpolate(frame, [0, 16], ["0px 2100px", "0px -2700px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.7, 0, 0.3, 1),
          }),
        }}
      />
    </AbsoluteFill>
  );
};
