import { AbsoluteFill, Sequence, staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { EndCard } from "./EndCard";
import { FONT } from "./fonts";
import { GreenWipe } from "./GreenWipe";
import { Hook } from "./Hook";
import { MovingGradient } from "./MovingGradient";
import { Savings } from "./Savings";
import { SignItem } from "./SignItem";

type Props = { readonly economia: number; readonly instagram: string };

const ListHeader: React.FC = () => (
  <div
    style={{
      fontFamily: FONT,
      fontWeight: 900,
      fontSize: 40,
      letterSpacing: "0.16em",
      color: "#22c55e",
      marginBottom: 70,
    }}
  >
    3 SINAIS
  </div>
);

const Sfx: React.FC<{ readonly src: string; readonly volume?: number }> = ({ src, volume = 1 }) => (
  <Audio src={staticFile(`sfx/${src}.mp3`)} volume={volume} />
);

// 15s at 30fps on a 120 BPM grid (one beat = 15 frames).
// Hook 0-2.5s, list 2.5-10.5s (one sign every 2.5s), savings 10.5-13s, end card 13-15s.
export const ConsorcioReels: React.FC<Props> = ({ economia, instagram }) => {
  const { fps } = useVideoConfig();
  const LIST = Math.round(2.5 * fps);
  const SIGN = Math.round(2.5 * fps);
  const SAVINGS = Math.round(10.5 * fps);
  const END = 13 * fps;
  const WIPE_LEAD = 8;

  return (
    <AbsoluteFill style={{ backgroundColor: "#050a07" }}>
      <MovingGradient />

      <Sequence name="Gancho" durationInFrames={LIST}>
        <Hook />
      </Sequence>

      <Sequence name="3 sinais" from={LIST} durationInFrames={SAVINGS - LIST}>
        <AbsoluteFill style={{ padding: "470px 90px 0" }}>
          <ListHeader />
          <div style={{ display: "flex", flexDirection: "column", gap: 80 }}>
            <Sequence name="Sinal 1" durationInFrames={3 * SIGN + 15} layout="none">
              <SignItem index={1} title="Você não tem pressa" body="Dá para esperar a contemplação e planejar a compra." dimAt={SIGN} />
            </Sequence>
            <Sequence name="Sinal 2" from={SIGN} durationInFrames={2 * SIGN + 15} layout="none">
              <SignItem index={2} title="Quer fugir dos juros" body="No consórcio não há juros, só taxa de administração." dimAt={SIGN} />
            </Sequence>
            <Sequence name="Sinal 3" from={2 * SIGN} durationInFrames={SIGN + 15} layout="none">
              <SignItem index={3} title="Pode dar um lance" body="Com lance, você pode antecipar a sua contemplação." />
            </Sequence>
          </div>
        </AbsoluteFill>
      </Sequence>

      <Sequence name="Economia" from={SAVINGS} durationInFrames={END - SAVINGS}>
        <Savings target={economia} />
      </Sequence>

      <Sequence name="Instagram" from={END}>
        <EndCard handle={instagram} />
      </Sequence>

      {[LIST, SAVINGS, END].map((cut) => (
        <Sequence key={cut} name="Wipe" from={cut - WIPE_LEAD} durationInFrames={16}>
          <GreenWipe />
        </Sequence>
      ))}

      {/* Trilha */}
      <Audio src={staticFile("music.wav")} volume={(f) => Math.min(1, f / 6) * (f > 14 * fps ? Math.max(0, (15 * fps - f) / fps) : 1) * 0.8} />

      {/* Efeitos sonoros */}
      <Sequence name="SFX impacto gancho" from={14} layout="none">
        <Sfx src="impact-bass-1" volume={0.55} />
      </Sequence>
      {[LIST, SAVINGS, END].map((cut) => (
        <Sequence key={`w${cut}`} name="SFX whoosh" from={cut - WIPE_LEAD - 2} layout="none" durationInFrames={30}>
          <Sfx src="whoosh" volume={0.7} />
        </Sequence>
      ))}
      {[0, 1, 2].map((i) => (
        <Sequence key={`p${i}`} name={`SFX pop ${i + 1}`} from={LIST + i * SIGN + 1} layout="none" durationInFrames={20}>
          <Sfx src="pop" volume={0.75} />
        </Sequence>
      ))}
      {Array.from({ length: 10 }, (_, i) => (
        <Sequence key={`c${i}`} name="SFX tick" from={SAVINGS + 5 + i * 4} layout="none" durationInFrames={8}>
          <Sfx src="click-soft" volume={0.35} />
        </Sequence>
      ))}
      <Sequence name="SFX impacto economia" from={SAVINGS + Math.round(1.5 * fps)} layout="none">
        <Sfx src="impact-bass-2" volume={0.6} />
      </Sequence>
      <Sequence name="SFX brilho" from={SAVINGS + Math.round(1.5 * fps)} layout="none">
        <Sfx src="sparkle" volume={0.45} />
      </Sequence>
      <Sequence name="SFX plim" from={END + 8} layout="none">
        <Sfx src="notification" volume={0.6} />
      </Sequence>
    </AbsoluteFill>
  );
};
