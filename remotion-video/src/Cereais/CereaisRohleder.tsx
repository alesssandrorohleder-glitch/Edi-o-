import { AbsoluteFill, Easing, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { Abertura, Campo, Colheita, Espiga, Final, Graos, Milho, Soja, Trigo } from "./Scenes";
import { C, CLAMP } from "./theme";

const FADE = 15;

// Each scene dissolves in over the tail of the previous one, with a slight settle in scale.
const Dissolve: React.FC<{ readonly children: React.ReactNode; readonly first?: boolean }> = ({ children, first = false }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        opacity: first ? 1 : interpolate(frame, [0, FADE], [0, 1], CLAMP),
        scale: first ? 1 : interpolate(frame, [0, FADE + 10], [1.04, 1], { ...CLAMP, easing: Easing.out(Easing.cubic) }),
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

const SCENES = [
  { name: "Abertura", len: 210, C: Abertura },
  { name: "Campo", len: 240, C: Campo },
  { name: "Trigo 10 mil anos", len: 255, C: Trigo },
  { name: "Espiga 50 grãos", len: 255, C: Espiga },
  { name: "Soja Santa Rosa", len: 270, C: Soja },
  { name: "Milho fileiras", len: 240, C: Milho },
  { name: "Colheita", len: 270, C: Colheita },
  { name: "Grãos safra", len: 210, C: Graos },
  { name: "Encerramento", len: 150, C: Final },
] as const;

export const CEREAIS_FRAMES = SCENES.reduce((a, s) => a + s.len, 0);

const Sfx: React.FC<{ readonly src: string; readonly volume: number }> = ({ src, volume }) => <Audio src={staticFile(`sfx/${src}.mp3`)} volume={volume} />;

export const CereaisRohleder: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  let at = 0;
  const starts = SCENES.map((s) => {
    const st = at;
    at += s.len;
    return st;
  });

  return (
    <AbsoluteFill style={{ backgroundColor: C.deep }}>
      {SCENES.map((s, i) => (
        <Sequence key={s.name} name={s.name} from={starts[i]} durationInFrames={s.len + (i < SCENES.length - 1 ? FADE : 0)}>
          <Dissolve first={i === 0}>
            <s.C />
          </Dissolve>
        </Sequence>
      ))}

      <Audio
        src={staticFile("cereais/music.wav")}
        volume={(f) => interpolate(f, [0, 10, durationInFrames - 3 * fps, durationInFrames - 4], [0, 0.85, 0.85, 0], CLAMP)}
      />
      <Sequence name="SFX logo" from={6} layout="none">
        <Sfx src="sparkle" volume={0.35} />
      </Sequence>
      {starts.slice(1).map((st) => (
        <Sequence key={st} name="SFX transição" from={st - 6} durationInFrames={30} layout="none">
          <Sfx src="whoosh-short" volume={0.22} />
        </Sequence>
      ))}
      <Sequence name="SFX logo final" from={starts[8] + 4} layout="none">
        <Sfx src="sparkle" volume={0.35} />
      </Sequence>
    </AbsoluteFill>
  );
};
