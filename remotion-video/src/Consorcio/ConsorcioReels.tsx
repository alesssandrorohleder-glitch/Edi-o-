import { AbsoluteFill, Easing, Sequence, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import "./fonts";
import { FONT } from "./fonts";
import { Hook } from "./Hook";
import { MovingGradient } from "./MovingGradient";
import { Savings } from "./Savings";
import { SignItem } from "./SignItem";

const ListHeader: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        fontFamily: FONT,
        fontWeight: 800,
        fontSize: 40,
        letterSpacing: "0.14em",
        color: "#22c55e",
        marginBottom: 70,
        opacity: interpolate(frame, [0, 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        translate: interpolate(frame, [0, 20], ["0px -30px", "0px 0px"], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.spring({ damping: 12 }),
        }),
      }}
    >
      3 SINAIS
    </div>
  );
};

export const ConsorcioReels: React.FC<{ readonly economia: number }> = ({ economia }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#050a07" }}>
      <MovingGradient />

      <Sequence name="Gancho" durationInFrames={3 * fps}>
        <Hook />
      </Sequence>

      <Sequence name="3 sinais" from={3 * fps} durationInFrames={9 * fps}>
        <AbsoluteFill style={{ padding: "230px 90px 0" }}>
          <ListHeader />
          <div style={{ display: "flex", flexDirection: "column", gap: 80 }}>
            <Sequence name="Sinal 1" durationInFrames={9 * fps} layout="none">
              <SignItem index={1} title="Você não tem pressa" body="Dá para esperar a contemplação e planejar a compra." dimAt={3 * fps} />
            </Sequence>
            <Sequence name="Sinal 2" from={3 * fps} durationInFrames={6 * fps} layout="none">
              <SignItem index={2} title="Quer fugir dos juros" body="No consórcio não há juros, só taxa de administração." dimAt={3 * fps} />
            </Sequence>
            <Sequence name="Sinal 3" from={6 * fps} durationInFrames={3 * fps} layout="none">
              <SignItem index={3} title="Pode dar um lance" body="Com lance, você pode antecipar a sua contemplação." />
            </Sequence>
          </div>
        </AbsoluteFill>
      </Sequence>

      <Sequence name="Economia" from={12 * fps} durationInFrames={3 * fps}>
        <Savings target={economia} />
      </Sequence>
    </AbsoluteFill>
  );
};
