import { Composition } from "remotion";
import { MyComposition } from "./Composition";
import { ConsorcioReels } from "./Consorcio/ConsorcioReels";
import { CEREAIS_FRAMES, CereaisRohleder } from "./Cereais/CereaisRohleder";
import { CereaisFimDeAno, FIM_DE_ANO_FRAMES } from "./Cereais/FimDeAno";
import { CereaisNatal, NATAL_FRAMES } from "./Cereais/Natal";
import { AGRO_FRAMES, CereaisAgro } from "./Cereais/Agro";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ConsorcioReels"
        component={ConsorcioReels}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ economia: 87000, instagram: "@thiagoidehara_invest" }}
      />
      <Composition id="CereaisRohleder" component={CereaisRohleder} durationInFrames={CEREAIS_FRAMES} fps={30} width={1920} height={1080} />
      <Composition id="CereaisFimDeAno" component={CereaisFimDeAno} durationInFrames={FIM_DE_ANO_FRAMES} fps={30} width={1080} height={1920} />
      <Composition id="CereaisNatal" component={CereaisNatal} durationInFrames={NATAL_FRAMES} fps={30} width={1080} height={1920} />
      <Composition id="CereaisAgro" component={CereaisAgro} durationInFrames={AGRO_FRAMES} fps={30} width={1080} height={1920} />
      <MyComposition />
    </>
  );
};
