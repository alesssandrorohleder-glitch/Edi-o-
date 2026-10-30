import { Composition } from "remotion";
import { MyComposition } from "./Composition";
import { ConsorcioReels } from "./Consorcio/ConsorcioReels";

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
      <MyComposition />
    </>
  );
};
