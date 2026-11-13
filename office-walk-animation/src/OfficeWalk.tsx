/**
 * OfficeWalk.tsx — 16-bit pixel art game composition.
 *
 * SVG canvas: 1080×1920 real pixels.
 * Art pixels: S=6 (1 art px = 6×6 real px).
 * Art canvas: 180×320.
 *
 * Layout (art pixel Y):
 *   0-30:   HUD bar
 *   31-281: Office scene (background + character)
 *   282-320: Crowd + sign
 *
 * All pixel art is drawn with integer-aligned rects for crisp look.
 * SVG shape-rendering="crispEdges" enforces pixel-perfect rendering.
 */

import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { PAL, S } from './Palette';
import { OfficeBackground } from './OfficeBackground';
import { OfficeWorker } from './OfficeWorker';
import { GameHUD, DamageNumber } from './HUD';
import { Crowd } from './Crowd';
import { SLIP_FRAME } from './PaperStack';

/** Screen-flash effect for the paper slip event */
function SlipFlash() {
  const frame = useCurrentFrame();
  if (frame < SLIP_FRAME) return null;

  const age = frame - SLIP_FRAME;
  if (age > 12) return null;

  // 2-frame alternating flash
  const on = Math.floor(age / 3) % 2 === 0;
  if (!on) return null;

  return (
    <rect
      x={0}
      y={0}
      width={180 * S}
      height={320 * S}
      fill={`rgba(255,100,0,${0.18 - age * 0.015})`}
    />
  );
}

/** Scanline overlay for retro CRT feel */
function Scanlines() {
  // Every other 2 real pixels = every 1/3 art pixel
  // We draw semi-transparent lines every 2 real pixels
  const lines: React.ReactElement[] = [];
  for (let y = 0; y < 1920; y += 4) {
    lines.push(
      <rect key={y} x={0} y={y} width={1080} height={1} fill="rgba(0,0,0,0.08)" />
    );
  }
  return <>{lines}</>;
}

/** Vignette overlay for cinematic corners */
function Vignette() {
  return (
    <defs>
      <radialGradient id="vig" cx="50%" cy="50%" r="70%">
        <stop offset="60%" stopColor="transparent" />
        <stop offset="100%" stopColor="rgba(0,0,0,0.5)" />
      </radialGradient>
    </defs>
  );
}

export function OfficeWalkComposition() {
  const frame = useCurrentFrame();
  const slipped = frame >= SLIP_FRAME;
  const heartsLeft = slipped ? 2 : 3;

  return (
    <AbsoluteFill style={{ background: '#000', overflow: 'hidden' }}>
      <svg
        width={1080}
        height={1920}
        viewBox={`0 0 ${180 * S} ${320 * S}`}
        xmlns="http://www.w3.org/2000/svg"
        style={{ display: 'block' }}
        shapeRendering="crispEdges"
      >
        {/* Vignette gradient definition */}
        <Vignette />

        {/* ── Base background colour ── */}
        <rect x={0} y={0} width={180 * S} height={320 * S} fill={PAL.wall} />

        {/* ── Office background (scrolling) ── */}
        <OfficeBackground />

        {/* ── Character sprite ── */}
        <OfficeWorker />

        {/* ── HUD overlay (top 30 art rows) ── */}
        <GameHUD heartsLeft={heartsLeft} />

        {/* ── Crowd at bottom ── */}
        <Crowd />

        {/* ── Damage number ("-1 HP") ── */}
        <DamageNumber />

        {/* ── Paper slip screen flash ── */}
        <SlipFlash />

        {/* ── Vignette ── */}
        <rect
          x={0} y={0}
          width={180 * S}
          height={320 * S}
          fill="url(#vig)"
          style={{ pointerEvents: 'none' }}
        />

        {/* ── Scanlines ── */}
        <Scanlines />
      </svg>
    </AbsoluteFill>
  );
}
