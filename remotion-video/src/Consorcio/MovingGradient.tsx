import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

// Two green glows drifting slowly over a near-black base.
export const MovingGradient: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const t = (frame / durationInFrames) * Math.PI * 2;

  const x1 = 25 + 18 * Math.sin(t * 1.4);
  const y1 = 22 + 10 * Math.cos(t * 1.1);
  const x2 = 78 - 16 * Math.sin(t * 1.2 + 1);
  const y2 = 78 + 9 * Math.cos(t * 1.5 + 2);
  const a1 = 0.3;
  const a2 = 0.22;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#050a07",
        backgroundImage: [
          `radial-gradient(circle at ${x1}% ${y1}%, rgba(34, 197, 94, ${a1}), rgba(34, 197, 94, 0) 46%)`,
          `radial-gradient(circle at ${x2}% ${y2}%, rgba(16, 185, 129, ${a2}), rgba(16, 185, 129, 0) 50%)`,
          "linear-gradient(180deg, rgba(5, 10, 7, 0) 60%, rgba(5, 10, 7, 0.85) 100%)",
        ].join(", "),
      }}
    />
  );
};
