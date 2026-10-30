import { Composition } from "remotion";
import { MyComposition } from "./Composition";
import { ConsorcioReels } from "./Consorcio/ConsorcioReels";
import { ThiagoCall } from "./ThiagoCall/ThiagoCall";
import { DURATION } from "./ThiagoCall/timeline";

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
      <MyComposition />
    </>
  );
};
