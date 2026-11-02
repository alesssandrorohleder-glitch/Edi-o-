import React from 'react';
import {Composition} from 'remotion';
import {PortfolioUI} from './PortfolioUI';

export const RemotionRoot: React.FC = () => (
  <Composition id="PortfolioUI" component={PortfolioUI} durationInFrames={32 * 30} fps={30} width={1080} height={1920} />
);
