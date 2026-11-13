/**
 * Root.tsx
 * Remotion root that registers the composition.
 */

import React from "react";
import { Composition } from "remotion";
import { OfficeWalkComposition } from "./OfficeWalk";

export function RemotionRoot() {
  return (
    <>
      <Composition
        id="OfficeWalk"
        component={OfficeWalkComposition}
        durationInFrames={300}   // 5 seconds × 60 fps
        fps={60}
        width={1080}
        height={1920}
      />
    </>
  );
}
