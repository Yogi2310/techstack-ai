/**
 * HUD.tsx — 16-bit game HUD overlay
 * Top bar: OFFICE QUEST logo, hearts, tasks, steps, XP bar
 * Drawn at art-pixel resolution (180×320 grid, 1px = 6 real px).
 */

import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { PAL, S } from './Palette';
import { getSpriteFrame, getStepCount, getXP, SPRITE_STEP } from './WalkCycle';
import { SLIP_FRAME } from './PaperStack';

/** Draw a solid art-pixel rectangle */
function R(ax: number, ay: number, aw: number, ah: number, fill: string, key?: string) {
  return <rect key={key} x={ax * S} y={ay * S} width={aw * S} height={ah * S} fill={fill} />;
}

/** Pixel-art 3×5 font bitmap for digits + letters (minimal set) */
const FONT: Record<string, number[][]> = {
  '0': [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
  '1': [[0,1,0],[1,1,0],[0,1,0],[0,1,0],[1,1,1]],
  '2': [[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1]],
  '3': [[1,1,1],[0,0,1],[0,1,1],[0,0,1],[1,1,1]],
  '4': [[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],
  '5': [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],
  '6': [[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]],
  '7': [[1,1,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0]],
  '8': [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]],
  '9': [[1,1,1],[1,0,1],[1,1,1],[0,0,1],[1,1,1]],
  '/': [[0,0,1],[0,1,0],[0,1,0],[1,0,0],[1,0,0]],
  ':': [[0],[1],[0],[1],[0]],
  ' ': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
  'T': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
  'A': [[0,1,0],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
  'S': [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],
  'K': [[1,0,1],[1,1,0],[1,1,0],[1,0,1],[1,0,1]],
  'E': [[1,1,1],[1,0,0],[1,1,0],[1,0,0],[1,1,1]],
  'P': [[1,1,0],[1,0,1],[1,1,0],[1,0,0],[1,0,0]],
  'X': [[1,0,1],[1,0,1],[0,1,0],[1,0,1],[1,0,1]],
  '+': [[0,1,0],[0,1,0],[1,1,1],[0,1,0],[0,1,0]],
  '-': [[0,0,0],[0,0,0],[1,1,1],[0,0,0],[0,0,0]],
};

/** Render pixel-art text at art coordinates */
function PixelText({
  text, ax, ay, color, scale = 1,
}: {
  text: string; ax: number; ay: number; color: string; scale?: number;
}) {
  const elems: React.ReactElement[] = [];
  let cx = ax;
  for (const ch of text.toUpperCase()) {
    const bitmap = FONT[ch] || FONT[' '];
    const w = bitmap[0].length;
    for (let row = 0; row < 5; row++) {
      for (let col = 0; col < w; col++) {
        if (bitmap[row][col]) {
          elems.push(
            <rect
              key={`${cx},${ay},${col},${row}`}
              x={(cx + col) * S * scale}
              y={(ay + row) * S * scale}
              width={S * scale}
              height={S * scale}
              fill={color}
            />
          );
        }
      }
    }
    cx += w + 1;
  }
  return <>{elems}</>;
}

/** Single heart (5×5 art pixels) */
function Heart({ ax, ay, filled }: { ax: number; ay: number; filled: boolean }) {
  const c = filled ? PAL.heartFull : PAL.heartEmpty;
  const sh = filled ? PAL.heartSh : PAL.heartEmpty;
  // heart shape in 5×5 pixel art
  const rows = [
    [0,1,0,1,0],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [0,1,1,1,0],
    [0,0,1,0,0],
  ];
  return (
    <>
      {rows.map((row, ry) =>
        row.map((on, rx) =>
          on ? (
            <rect
              key={`h${ax}${ay}${rx}${ry}`}
              x={(ax + rx) * S}
              y={(ay + ry) * S}
              width={S}
              height={S}
              fill={ry === 0 ? (on ? c : 'none') : ry >= 3 ? sh : c}
            />
          ) : null
        )
      )}
    </>
  );
}

/** XP bar (art pixels) */
function XPBar({ ax, ay, aw, ah, pct }: { ax:number; ay:number; aw:number; ah:number; pct:number }) {
  const filled = Math.round(pct * aw);
  return (
    <>
      {R(ax-1, ay-1, aw+2, ah+2, PAL.xpBorder)}
      {R(ax, ay, aw, ah, PAL.xpBg)}
      {filled > 0 && R(ax, ay, filled, ah, PAL.xpFill)}
      {/* shine */}
      {filled > 1 && R(ax, ay, filled, 1, '#66ff88')}
    </>
  );
}

export function GameHUD({ heartsLeft }: { heartsLeft: number }) {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const steps = getStepCount(frame);
  const xp = getXP(frame, durationInFrames) / 100;

  // HUD panel: Y=1 to Y=30 (art pixels)
  // Top banner: Y=1-13
  // Stats row: Y=14-24
  // XP row: Y=25-29

  return (
    <g>
      {/* ── HUD background panel ── */}
      {R(0, 0, 180, 31, PAL.hudBg)}
      {/* top border */}
      {R(0, 0, 180, 1, PAL.hudBorderHi)}
      {/* bottom border */}
      {R(0, 30, 180, 1, PAL.hudBorder)}
      {/* inner top line */}
      {R(1, 1, 178, 1, PAL.hudBorder)}

      {/* ── OFFICE QUEST title ── */}
      {/* Use SVG text for the title since it's larger */}
      <text
        x={5 * S}
        y={10 * S}
        fontSize={8 * S}
        fontFamily="'Courier New', monospace"
        fontWeight="bold"
        fill={PAL.sunYellow}
        style={{ imageRendering: 'pixelated' } as React.CSSProperties}
        letterSpacing={2}
      >
        OFFICE QUEST
      </text>

      {/* ── Hearts ── */}
      <Heart ax={130} ay={2} filled={heartsLeft >= 1} />
      <Heart ax={137} ay={2} filled={heartsLeft >= 2} />
      <Heart ax={144} ay={2} filled={heartsLeft >= 3} />

      {/* ── TASKS label ── */}
      <PixelText text="TASKS" ax={2} ay={16} color={PAL.taskText} />
      <PixelText text="3/10" ax={22} ay={16} color={PAL.hudText} />

      {/* divider */}
      {R(44, 15, 1, 11, PAL.hudBorder)}

      {/* ── STEPS ── */}
      <PixelText text="STEPS" ax={47} ay={16} color={PAL.hudSub} />
      <PixelText text={String(steps).padStart(3, ' ')} ax={68} ay={16} color={PAL.hudText} />

      {/* divider */}
      {R(90, 15, 1, 11, PAL.hudBorder)}

      {/* ── XP label ── */}
      <PixelText text="XP" ax={93} ay={16} color={PAL.hudSub} />
      {/* XP bar */}
      <XPBar ax={103} ay={16} aw={72} ah={9} pct={xp} />
    </g>
  );
}

/** Floating "-1" damage number after paper slip */
export function DamageNumber() {
  const frame = useCurrentFrame();
  if (frame < SLIP_FRAME) return null;

  const age = frame - SLIP_FRAME;
  const duration = 60; // 1 second
  if (age > duration) return null;

  const t = age / duration;
  // floats up and fades
  const artY = Math.round(120 - t * 30);
  const artX = 95;
  const opacity = 1 - t;

  return (
    <g opacity={opacity}>
      {/* background chip */}
      {R(artX - 2, artY - 2, 20, 11, PAL.minusBg)}
      {R(artX - 1, artY - 1, 18, 9, PAL.minus)}
      {/* "-1" text in white */}
      <PixelText text="-1" ax={artX + 1} ay={artY} color={PAL.white} />
      {/* HP text */}
      <PixelText text="HP" ax={artX + 9} ay={artY} color={PAL.white} />
    </g>
  );
}
