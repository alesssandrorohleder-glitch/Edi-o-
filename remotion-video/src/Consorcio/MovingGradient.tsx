import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

// Two green glows drifting over a near-black base; they swell a little on every beat (120 BPM).
export const MovingGradient: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();
  const t = (frame / durationInFrames) * Math.PI * 2;
  const beat = fps / 2;
  const pulse = Math.exp(-(frame % beat) / 4);

  const x1 = 25 + 18 * Math.sin(t * 1.4);
  const y1 = 22 + 10 * Math.cos(t * 1.1);
  const x2 = 78 - 16 * Math.sin(t * 1.2 + 1);
  const y2 = 78 + 9 * Math.cos(t * 1.5 + 2);
  const a1 = 0.3 + 0.14 * pulse;
  const a2 = 0.22 + 0.1 * pulse;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#050a07",
        backgroundImage: [
          `radial-gradient(circle at ${x1}% ${y1}%, rgba(34, 197, 94, ${a1}), rgba(34, 197, 94, 0) ${46 + 4 * pulse}%)`,
          `radial-gradient(circle at ${x2}% ${y2}%, rgba(16, 185, 129, ${a2}), rgba(16, 185, 129, 0) 50%)`,
          "linear-gradient(180deg, rgba(5, 10, 7, 0) 60%, rgba(5, 10, 7, 0.85) 100%)",
        ].join(", "),
      }}
    />
  );
};
