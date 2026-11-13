/**
 * OfficeWorker.tsx — 16-bit pixel art office worker sprite.
 * Drawn on the internal 180×320 art-pixel grid (1 art px = 6 real px).
 *
 * Character size: ~16 wide × 32 tall art pixels.
 * Ground level: art Y = 230.
 * Character fixed at art X = 72 (40% from left).
 *
 * Walk animation: 4 discrete frames advanced every SPRITE_STEP real frames.
 */

import React from 'react';
import { useCurrentFrame } from 'remotion';
import { PAL, S } from './Palette';
import { getSpriteFrame, SPRITE_STEP } from './WalkCycle';
import { PaperStack } from './PaperStack';

/** Art-pixel rect helper */
function R(ax: number, ay: number, aw: number, ah: number, fill: string, key?: string | number) {
  return <rect key={key} x={ax * S} y={ay * S} width={aw * S} height={ah * S} fill={fill} />;
}

// ── Character constants ────────────────────────────────────────────────────
const CX = 72;    // character art-pixel X (fixed on screen, background scrolls)
const GY = 230;   // ground level art-pixel Y (bottom of feet)
const CW = 16;    // character art width
const CH = 32;    // character art height

type SpriteFrame = 0 | 1 | 2 | 3;

/** Leg positions per walk frame [leftLegX, rightLegX, leftFootY, rightFootY] */
const LEG_POSES: [number, number, number, number][] = [
  // F0: contact (both near center)
  [0,  5, GY-2, GY-2],
  // F1: left foot forward
  [-2, 7, GY-3, GY],
  // F2: passing (feet cross)
  [2,  3, GY-2, GY-2],
  // F3: right foot forward (mirror of F1)
  [2, -1, GY,   GY-3],
];

/** Upper-body bob (1px per frame, discrete) */
const BODY_BOB: number[] = [0, -1, -1, 0];

/** Arm swing per frame: [leftArmYOffset, rightArmYOffset] */
const ARM_SWING: [number, number][] = [
  [0, 0],
  [1, -1],
  [0, 0],
  [-1, 1],
];

export function OfficeWorker() {
  const frame = useCurrentFrame();
  const sf = getSpriteFrame(frame) as SpriteFrame;

  const bob = BODY_BOB[sf];
  const [laOff, raOff] = ARM_SWING[sf];
  const [llX, rlX, llFootY, rlFootY] = LEG_POSES[sf];

  // Art-pixel top of character
  const topY = GY - CH;

  // Shorthand head/body/limb art positions
  const headTop   = topY + bob;
  const bodyTop   = headTop + 7;
  const bodyBot   = bodyTop + 10;
  const hipY      = bodyBot;

  // ── Shadow ────────────────────────────────────────────────────────────────
  // ── Rear leg (draw first, behind body) ────────────────────────────────────
  const rlArtX = CX + rlX;
  const rlTopY = hipY;
  const rlKneeY = rlTopY + 7;

  // ── Front leg ─────────────────────────────────────────────────────────────
  const llArtX = CX + llX;
  const llTopY = hipY;
  const llKneeY = llTopY + 7;

  // ── Paper stack on front arm ───────────────────────────────────────────────
  // Front arm (right, as character faces right) is at CX+13, bodyTop+2
  const paperAX = CX + 13;
  const paperAY = bodyTop + 3 + raOff;

  return (
    <>
      {/* ── Ground shadow ── */}
      <ellipse
        cx={(CX + 8) * S}
        cy={GY * S}
        rx={10 * S}
        ry={2 * S}
        fill="rgba(0,0,0,0.3)"
      />

      {/* ══════════════ REAR LEG ══════════════ */}
      {/* Upper leg */}
      {R(rlArtX + 3, rlTopY, 4, 7, PAL.trouserSh)}
      {/* Lower leg (slight knee bend) */}
      {R(rlArtX + 3, rlKneeY, 4, 6, PAL.trouserSh)}
      {/* Shoe */}
      {R(rlArtX + 2, rlFootY, 7, 2, '#0a0a0a')}
      {R(rlArtX + 1, rlFootY + 2, 8, 1, '#1a1a1a')}

      {/* ══════════════ REAR ARM (left, behind body) ══════════════ */}
      {R(CX - 1, bodyTop + 1 + laOff, 2, 7, PAL.shirtSh)}
      {/* hand */}
      {R(CX - 1, bodyTop + 8 + laOff, 2, 2, PAL.skinSh)}

      {/* ══════════════ BODY (torso + head) ══════════════ */}
      {/* Shirt torso */}
      {R(CX + 2, bodyTop, 11, 10, PAL.shirt)}
      {/* Shirt shadow on left */}
      {R(CX + 2, bodyTop, 2, 10, PAL.shirtSh)}
      {/* Collar (white) */}
      {R(CX + 5, bodyTop, 2, 2, PAL.white)}
      {R(CX + 9, bodyTop, 2, 2, PAL.white)}
      {/* Tie */}
      {R(CX + 7, bodyTop + 2, 2, 7, PAL.tie)}
      {R(CX + 7, bodyTop, 2, 2, PAL.tieHi)}
      {/* Tie shadow */}
      {R(CX + 8, bodyTop + 3, 1, 5, PAL.tie)}
      {/* Shirt buttons */}
      {R(CX + 6, bodyTop + 2, 1, 1, PAL.shirtSh)}
      {R(CX + 6, bodyTop + 5, 1, 1, PAL.shirtSh)}
      {R(CX + 6, bodyTop + 8, 1, 1, PAL.shirtSh)}
      {/* Trouser waistband */}
      {R(CX + 2, hipY - 2, 11, 2, PAL.trouserSh)}

      {/* Neck */}
      {R(CX + 6, headTop + 5, 4, 2, PAL.skin)}

      {/* ── HEAD ── */}
      {/* Hair */}
      {R(CX + 3, headTop, 10, 2, PAL.hair)}
      {R(CX + 2, headTop + 1, 11, 2, PAL.hair)}
      {/* Face */}
      {R(CX + 3, headTop + 2, 10, 5, PAL.skin)}
      {/* Face shadow (right side) */}
      {R(CX + 11, headTop + 2, 2, 5, PAL.skinSh)}
      {/* Eye */}
      {R(CX + 9, headTop + 3, 2, 2, PAL.white)}
      {R(CX + 10, headTop + 3, 1, 1, '#1a1a1a')}
      {/* Eyebrow */}
      {R(CX + 9, headTop + 2, 3, 1, PAL.hair)}
      {/* Ear */}
      {R(CX + 3, headTop + 3, 1, 2, PAL.skinSh)}
      {/* Mouth */}
      {R(CX + 9, headTop + 6, 3, 1, '#c07050')}
      {/* Hair side */}
      {R(CX + 3, headTop + 2, 1, 4, PAL.hair)}

      {/* ══════════════ FRONT ARM (right, carries papers) ══════════════ */}
      {/* Upper arm */}
      {R(CX + 13, bodyTop + 1 + raOff, 2, 6, PAL.shirt)}
      {/* Forearm (extends right for carrying) */}
      {R(CX + 14, bodyTop + 7 + raOff, 5, 2, PAL.skin)}
      {/* Hand grip */}
      {R(CX + 18, bodyTop + 6 + raOff, 2, 3, PAL.skin)}

      {/* Paper stack on forearm */}
      <PaperStack ax={paperAX} ay={paperAY} />

      {/* ══════════════ FRONT LEG ══════════════ */}
      {/* Upper leg */}
      {R(llArtX + 3, llTopY, 4, 7, PAL.trouser)}
      {/* Trouser crease */}
      {R(llArtX + 5, llTopY, 1, 7, PAL.trouserSh)}
      {/* Lower leg */}
      {R(llArtX + 3, llKneeY, 4, 6, PAL.trouser)}
      {/* Shoe */}
      {R(llArtX + 2, llFootY, 7, 2, PAL.shoe)}
      {R(llArtX + 1, llFootY + 2, 8, 1, '#1a1a1a')}
      {/* Shoe shine */}
      {R(llArtX + 3, llFootY, 2, 1, '#333')}
    </>
  );
}
