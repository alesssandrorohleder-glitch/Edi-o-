import { Composition } from "remotion";
import { MyComposition } from "./Composition";
import { ConsorcioReels } from "./Consorcio/ConsorcioReels";
import { CEREAIS_FRAMES, CereaisRohleder } from "./Cereais/CereaisRohleder";

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
      <MyComposition />
    </>
  );
};
