import { Composition } from "remotion";
import { MyComposition } from "./Composition";
import { ConsorcioReels } from "./Consorcio/ConsorcioReels";
import { ThiagoCall } from "./ThiagoCall/ThiagoCall";
import { DURATION } from "./ThiagoCall/timeline";
import { ThiagoLance } from "./ThiagoLance/ThiagoLance";
import { StyleFrame } from "./ThiagoExplica/StyleFrame";
import { DURATION as EXPLICA_DURATION, ThiagoExplica } from "./ThiagoExplica/ThiagoExplica";
import { DURATION as LANCE_DURATION } from "./ThiagoLance/timeline";

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
      <Composition id="ThiagoCall" component={ThiagoCall} durationInFrames={DURATION} fps={30} width={1080} height={1920} />
      <Composition id="ThiagoLance" component={ThiagoLance} durationInFrames={LANCE_DURATION} fps={30} width={1080} height={1920} />
      <Composition id="ExplicaStyle" component={StyleFrame} durationInFrames={1} fps={30} width={1080} height={1920} defaultProps={{ kind: 1 as 1 | 2 | 3 }} />
      <Composition id="ThiagoExplica" component={ThiagoExplica} durationInFrames={EXPLICA_DURATION} fps={30} width={1080} height={1920} />
      <MyComposition />
    </>
  );
};
