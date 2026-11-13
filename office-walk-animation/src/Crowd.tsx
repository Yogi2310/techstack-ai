/**
 * Crowd.tsx — pixel art crowd of coworkers at the bottom.
 * They hold a sign: "GO!" → "OOPS" after paper slip.
 * They bob up and down with a simple 2-frame animation.
 * Art pixels, 180×36 strip at bottom of canvas (Y=284 to Y=320).
 */

import React from 'react';
import { useCurrentFrame } from 'remotion';
import { PAL, S } from './Palette';
import { SLIP_FRAME } from './PaperStack';

function R(ax: number, ay: number, aw: number, ah: number, fill: string, key?: string | number) {
  return <rect key={key} x={ax * S} y={ay * S} width={aw * S} height={ah * S} fill={fill} />;
}

/** A single pixel art coworker (10×20 art pixels at their base) */
function PixelPerson({
  ax, ay, color, shadowColor, armUp, bob,
}: {
  ax: number; ay: number; color: string; shadowColor: string;
  armUp: boolean; bob: number;
}) {
  const by = ay + bob; // bobbing offset

  return (
    <>
      {/* head */}
      {R(ax+2, by-18, 6, 6, PAL.skin)}
      {R(ax+2, by-19, 6, 2, PAL.hair)}
      {R(ax+6, by-16, 1, 2, '#1a1a1a')} {/* eye */}

      {/* body */}
      {R(ax+1, by-12, 8, 8, color)}
      {R(ax+1, by-12, 2, 8, shadowColor)}

      {/* arms - raised up holding sign */}
      {armUp
        ? <>
            {R(ax-1, by-16, 2, 8, color)}  {/* left arm up */}
            {R(ax+9, by-16, 2, 8, color)}  {/* right arm up */}
          </>
        : <>
            {R(ax-1, by-11, 2, 6, color)}  {/* left arm down */}
            {R(ax+9, by-11, 2, 6, color)}  {/* right arm down */}
          </>
      }

      {/* legs */}
      {R(ax+1, by-4, 3, 8, '#2a3a4a')}
      {R(ax+5, by-4, 3, 8, '#2a3a4a')}
      {/* shoes */}
      {R(ax, by+4, 4, 2, PAL.shoe)}
      {R(ax+5, by+4, 4, 2, PAL.shoe)}
    </>
  );
}

/** The sign banner */
function SignBanner({ ax, ay, text, color }: { ax: number; ay: number; text: string; color: string }) {
  return (
    <>
      {/* sign board */}
      {R(ax, ay, 48, 20, PAL.signBrd)}
      {R(ax+1, ay+1, 46, 18, PAL.signBg)}
      {/* pole lines from crowd hands */}
      {R(ax+10, ay+20, 2, 10, '#8b7050')}
      {R(ax+36, ay+20, 2, 10, '#8b7050')}
      {/* sign text */}
      <text
        x={(ax + 4) * S}
        y={(ay + 14) * S}
        fontSize={10 * S}
        fontFamily="'Courier New', monospace"
        fontWeight="900"
        fill={color}
        letterSpacing={2}
      >
        {text}
      </text>
    </>
  );
}

/** Crowd area strip — Y=282 to Y=320 (38 art pixels tall) */
export function Crowd() {
  const frame = useCurrentFrame();
  const slipped = frame >= SLIP_FRAME;

  // 2-frame bob cycle: every 15 frames
  const bobCycle = Math.floor(frame / 15) % 2;
  const bob = bobCycle === 1 ? -1 : 0;

  // After paper slip: excited animation (faster + different poses)
  const excitedCycle = slipped ? Math.floor(frame / 6) % 2 : bobCycle;
  const excitedBob = slipped ? (excitedCycle === 1 ? -2 : 0) : bob;

  // People configuration [x offset, arm up on frame 0]
  const people: { dx: number; colorIdx: number; armUpOnEven: boolean }[] = [
    { dx: 2,   colorIdx: 0, armUpOnEven: true  },
    { dx: 15,  colorIdx: 1, armUpOnEven: false },
    { dx: 28,  colorIdx: 2, armUpOnEven: true  },
    { dx: 41,  colorIdx: 3, armUpOnEven: false },
    { dx: 54,  colorIdx: 4, armUpOnEven: true  },
    { dx: 67,  colorIdx: 0, armUpOnEven: false },
    { dx: 80,  colorIdx: 1, armUpOnEven: true  },
    // right side crowd holding sign poles
    { dx: 115, colorIdx: 2, armUpOnEven: true  },
    { dx: 128, colorIdx: 3, armUpOnEven: false },
    { dx: 141, colorIdx: 4, armUpOnEven: true  },
    { dx: 154, colorIdx: 0, armUpOnEven: false },
    { dx: 167, colorIdx: 1, armUpOnEven: true  },
  ];

  const BASE_Y = 316; // feet level

  const signText   = slipped ? '  OOPS' : '  GO!';
  const signColor  = slipped ? PAL.oopsColor : PAL.goColor;

  return (
    <>
      {/* Dark crowd floor strip */}
      <rect x={0} y={282 * S} width={180 * S} height={38 * S} fill='#0a0818' />
      {/* crowd gradient at top */}
      <rect x={0} y={282 * S} width={180 * S} height={2 * S} fill='#00000060' />

      {/* Render all crowd people */}
      {people.map((p, i) => {
        const cycle = slipped ? excitedCycle : bobCycle;
        const armUp = p.armUpOnEven ? cycle === 0 : cycle === 1;
        const personBob = slipped ? excitedBob : bob;
        return (
          <PixelPerson
            key={i}
            ax={p.dx}
            ay={BASE_Y}
            color={PAL.crowd[p.colorIdx]}
            shadowColor={PAL.crowdSh[p.colorIdx]}
            armUp={armUp}
            bob={personBob}
          />
        );
      })}

      {/* Sign held by people at dx=100 to dx=120 */}
      <SignBanner ax={91} ay={285} text={signText} color={signColor} />

      {/* Crowd chant text */}
      {!slipped && (
        <text
          x={2 * S}
          y={320 * S}
          fontSize={4 * S}
          fontFamily="'Courier New', monospace"
          fill={PAL.hudSub}
          letterSpacing={1}
        >
          {frame % 30 < 15 ? '♪ WORK WORK WORK ♪' : '♪ GO GO GO! ♪'}
        </text>
      )}
      {slipped && (
        <text
          x={2 * S}
          y={320 * S}
          fontSize={4 * S}
          fontFamily="'Courier New', monospace"
          fill={PAL.oopsColor}
          letterSpacing={1}
        >
          {frame % 20 < 10 ? '⚠ PAPER DROPPED! ⚠' : '!! SAVE THE PAPERS !!'}
        </text>
      )}
    </>
  );
}
