/**
 * PaperStack.tsx — pixel art paper stack + slip event.
 * Stack sits on the character's forearm.
 * At SLIP_FRAME the top sheet slips off and tumbles downward.
 */

import React from 'react';
import { useCurrentFrame } from 'remotion';
import { PAL, S } from './Palette';

export const SLIP_FRAME = Math.round(2.7 * 60); // 162

/** Art-pixel rect helper */
function R(ax: number, ay: number, aw: number, ah: number, fill: string, key?: string | number) {
  return <rect key={key} x={ax * S} y={ay * S} width={aw * S} height={ah * S} fill={fill} />;
}

/** A single pixel art paper sheet at art coords */
function PaperSheet({ ax, ay, flip = false }: { ax: number; ay: number; flip?: boolean }) {
  return (
    <>
      {R(ax, ay, 10, 13, PAL.paperLine)}
      {R(ax+1, ay, 8, 12, PAL.paper)}
      {/* ruled lines */}
      {[2,4,6,8,10].map(ly => R(ax+2, ay+ly, 6, 1, PAL.paperLine, ly))}
      {/* fold corner */}
      {flip
        ? R(ax, ay, 3, 3, PAL.paperLine)
        : R(ax+7, ay, 3, 3, PAL.paperLine)}
    </>
  );
}

interface PaperStackProps {
  /** Art-pixel X of the forearm */
  ax: number;
  /** Art-pixel Y of the forearm */
  ay: number;
}

export function PaperStack({ ax, ay }: PaperStackProps) {
  const frame = useCurrentFrame();
  const slipped = frame >= SLIP_FRAME;
  const age = slipped ? frame - SLIP_FRAME : 0;

  // ── 4 sheets stacked (each offset by 1px up) ──
  const sheetCount = 4;

  // Slipping sheet animation (discrete pixel-art steps, every 2 frames)
  const slipStep = Math.floor(age / 2);
  const slipX = Math.min(slipStep * 2, 50);     // drifts right
  const slipY = slipStep > 5
    ? Math.min((slipStep - 5) * 3, 80)           // falls after drift
    : -Math.min(slipStep * 1, 6);                // initial float-up
  const slipFlip = Math.floor(age / 8) % 2 === 1; // tumbles every 8 frames
  const slipVisible = slipped && age < 90;        // disappears after 90 frames

  // The sheets sit on top of the arm
  const stackAx = ax;
  const stackAy = ay - 14;

  return (
    <>
      {/* Remaining stack (all sheets after slip = 3) */}
      {Array.from({ length: slipped ? sheetCount - 1 : sheetCount }).map((_, i) => (
        <PaperSheet
          key={i}
          ax={stackAx - i}
          ay={stackAy - i}
        />
      ))}

      {/* Slipping sheet */}
      {slipVisible && (
        <PaperSheet
          ax={stackAx + slipX - slipStep}
          ay={stackAy + slipY}
          flip={slipFlip}
        />
      )}
    </>
  );
}
