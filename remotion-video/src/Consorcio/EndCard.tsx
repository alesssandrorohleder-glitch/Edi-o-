import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { FONT } from "./fonts";

const GREEN = "#22c55e";

type Props = { readonly handle: string };

// Closing card: follow call-to-action with the Instagram handle.
export const EndCard: React.FC<Props> = ({ handle }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ padding: "0 90px", justifyContent: "center", alignItems: "center", textAlign: "center" }}>
      <div
        style={{
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: 92,
          lineHeight: 1,
          letterSpacing: "-0.03em",
          color: "#ffffff",
          translate: interpolate(frame, [0, 14], ["0px -80px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.spring({ damping: 9 }),
          }),
          opacity: interpolate(frame, [0, 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        Siga para
        <br />
        <span style={{ color: GREEN }}>mais dicas</span>
      </div>

      <div
        style={{
          marginTop: 70,
          display: "flex",
          alignItems: "center",
          gap: 26,
          padding: "26px 40px",
          borderRadius: 999,
          backgroundColor: "rgba(255, 255, 255, 0.06)",
          border: `3px solid ${GREEN}`,
          scale: interpolate(frame, [6, 22], [0.5, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.spring({ damping: 8 }),
            output: "perceptual-scale",
          }),
          opacity: interpolate(frame, [6, 11], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        <svg width="76" height="76" viewBox="0 0 24 24" style={{ flex: "0 0 auto" }}>
          <rect x="2.5" y="2.5" width="19" height="19" rx="5.5" fill="none" stroke={GREEN} strokeWidth="2.2" />
          <circle cx="12" cy="12" r="4.3" fill="none" stroke={GREEN} strokeWidth="2.2" />
          <circle cx="17.4" cy="6.6" r="1.4" fill={GREEN} />
        </svg>
        <span style={{ fontFamily: FONT, fontWeight: 900, fontSize: 52, color: "#ffffff", letterSpacing: "-0.01em" }}>{handle}</span>
      </div>

      <div
        style={{
          marginTop: 40,
          fontFamily: FONT,
          fontWeight: 800,
          fontSize: 36,
          letterSpacing: "0.12em",
          color: "rgba(255, 255, 255, 0.7)",
          opacity: interpolate(frame, [18, 26], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        SALVE ESTE VÍDEO
      </div>
    </AbsoluteFill>
  );
};
