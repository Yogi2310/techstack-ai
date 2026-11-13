/**
 * OfficeBackground.tsx — 16-bit pixel art scrolling office background.
 * Internal grid: 180×320 art pixels, each = 6×6 real pixels (S=6).
 * Background strip is 360px wide and scrolls leftward.
 *
 * Layout (art pixel Y):
 *   0-30:   HUD (handled by HUD.tsx)
 *   31-85:  Ceiling + upper wall + window (sunset outside)
 *   86-230: Office wall with desks, monitors, whiteboard, signs
 *   231-280: Floor
 *   281-284: Floor-wall join shadow
 *   285-320: Crowd (handled by Crowd.tsx)
 */

import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { PAL, S } from './Palette';

function R(ax: number, ay: number, aw: number, ah: number, fill: string, key?: string | number) {
  return <rect key={key} x={ax * S} y={ay * S} width={aw * S} height={ah * S} fill={fill} />;
}

/** Sunset window (art pixels, relative to top-left of window) */
function SunsetWindow({ ax, ay }: { ax: number; ay: number }) {
  return (
    <g transform={`translate(${ax * S},${ay * S})`}>
      {/* frame */}
      {R(0,0,36,52,PAL.winFrame)}
      {/* glass pane */}
      {R(2,2,32,48,PAL.winSky)}
      {/* sunset gradient bands */}
      {R(2,2,32,8,PAL.skyTop)}
      {R(2,10,32,8,PAL.skyMid)}
      {R(2,18,32,10,PAL.skyOrange)}
      {R(2,28,32,12,PAL.skyYellow)}
      {R(2,40,32,10,PAL.sunYellow)}
      {/* sun disc */}
      {R(14,38,8,2,PAL.sunYellow)}
      {R(12,40,12,4,PAL.sunYellow)}
      {R(14,44,8,2,PAL.sunYellow)}
      {/* cloud 1 */}
      {R(4,8,10,3,PAL.winCloud)}
      {R(6,6,6,2,PAL.winCloud)}
      {/* cloud 2 */}
      {R(18,14,12,3,PAL.winCloud)}
      {R(20,12,8,3,PAL.winCloud)}
      {/* window cross divider */}
      {R(0,24,36,2,PAL.winFrame)}
      {R(16,2,2,48,PAL.winFrame)}
      {/* glint on glass */}
      {R(3,3,2,8,'rgba(255,255,255,0.15)')}
      {/* PIXEL SIGN on wall above window */}
      {R(-2,-14,40,10,PAL.hudBg)}
      {R(-1,-13,38,8,PAL.wall)}
      <text
        x={-1 * S}
        y={-6 * S}
        fontSize={5 * S}
        fontFamily="'Courier New', monospace"
        fontWeight="900"
        fill={PAL.sunYellow}
        letterSpacing={1}
      >
        OFFICE QUEST
      </text>
    </g>
  );
}

/** Ceiling light fixture */
function CeilLight({ ax, ay }: { ax: number; ay: number }) {
  return (
    <>
      {R(ax, ay, 24, 2, PAL.hudBorder)}
      {R(ax+1, ay+2, 22, 2, PAL.ceilLight)}
      {R(ax+2, ay+4, 20, 1, '#fffff0')}
    </>
  );
}

/** Pixel art desk + monitor */
function Desk({ ax, ay }: { ax: number; ay: number }) {
  return (
    <>
      {/* desk surface */}
      {R(ax, ay, 50, 3, PAL.deskTop)}
      {/* desk body */}
      {R(ax+2, ay+3, 46, 20, PAL.desk)}
      {/* left leg */}
      {R(ax+4, ay+23, 5, 15, PAL.desk)}
      {/* right leg */}
      {R(ax+40, ay+23, 5, 15, PAL.desk)}
      {/* shadow under desk */}
      {R(ax+1, ay+38, 48, 2, '#00000030')}

      {/* monitor stand */}
      {R(ax+22, ay-8, 4, 8, '#333')}
      {R(ax+16, ay-10, 16, 2, '#444')}
      {/* monitor frame */}
      {R(ax+10, ay-30, 28, 22, PAL.monitor)}
      {/* screen */}
      {R(ax+12, ay-28, 24, 18, PAL.screen)}
      {/* screen content (line chart) */}
      {R(ax+13, ay-18, 3, 1, PAL.screenLine)}
      {R(ax+16, ay-21, 3, 4, PAL.screenLine)}
      {R(ax+19, ay-19, 3, 2, PAL.screenLine)}
      {R(ax+22, ay-24, 3, 7, PAL.screenLine)}
      {R(ax+25, ay-22, 3, 5, PAL.screenLine)}
      {R(ax+28, ay-25, 3, 8, PAL.screenLine)}
      {/* screen glow */}
      {R(ax+13, ay-27, 22, 1, '#4466ff20')}
      {/* keyboard */}
      {R(ax+8, ay+1, 20, 1, '#555')}
      {R(ax+8, ay, 20, 1, '#666')}
      {/* mouse */}
      {R(ax+32, ay, 6, 2, '#888')}
      {/* papers on desk */}
      {R(ax+4, ay-1, 12, 1, PAL.paper)}
      {R(ax+4, ay-2, 12, 1, '#fff')}
      {/* mug */}
      {R(ax+44, ay-6, 4, 6, '#c0392b')}
      {R(ax+44, ay-7, 4, 1, '#a52820')}
    </>
  );
}

/** Pixel art whiteboard with bar chart */
function Whiteboard({ ax, ay }: { ax: number; ay: number }) {
  const bars = [14, 22, 11, 26, 18, 24, 10];
  const colors = [PAL.wbBar1, PAL.wbBar2, PAL.wbBar1, PAL.wbBar3, PAL.wbBar2, PAL.wbBar1, PAL.wbBar3];
  return (
    <>
      {/* frame */}
      {R(ax, ay, 56, 44, PAL.wbFrame)}
      {/* surface */}
      {R(ax+1, ay+1, 54, 42, PAL.wb)}
      {/* bars */}
      {bars.map((h, i) => (
        <React.Fragment key={i}>
          {R(ax + 3 + i * 7, ay + 1 + 42 - h, 5, h - 2, colors[i])}
        </React.Fragment>
      ))}
      {/* baseline */}
      {R(ax+1, ay+41, 54, 1, '#aaa')}
      {/* title text */}
      <text
        x={(ax + 8) * S}
        y={(ay + 8) * S}
        fontSize={4 * S}
        fontFamily="'Courier New', monospace"
        fontWeight="bold"
        fill="#333"
      >
        Q4 SALES
      </text>
      {/* marker tray */}
      {R(ax, ay+44, 56, 3, '#aaa')}
      {R(ax+2, ay+45, 8, 2, '#e74c3c')}
      {R(ax+12, ay+45, 8, 2, '#2c3e50')}
    </>
  );
}

/** Plant */
function Plant({ ax, ay }: { ax: number; ay: number }) {
  return (
    <>
      {/* pot */}
      {R(ax+2, ay, 12, 2, PAL.potDark)}
      {R(ax+1, ay+2, 14, 12, PAL.pot)}
      {R(ax, ay+14, 16, 2, PAL.potDark)}
      {/* stem */}
      {R(ax+7, ay-14, 2, 14, '#5d4037')}
      {/* leaves */}
      {R(ax+9, ay-14, 7, 3, PAL.plant)}
      {R(ax+1, ay-12, 7, 3, PAL.plant)}
      {R(ax+10, ay-20, 6, 3, PAL.plant)}
      {R(ax+1, ay-18, 7, 3, PAL.plant)}
      {R(ax+5, ay-24, 7, 4, PAL.plant)}
      {/* leaf shadow */}
      {R(ax+10, ay-13, 3, 2, PAL.plantDark)}
      {R(ax+1, ay-11, 3, 2, PAL.plantDark)}
    </>
  );
}

/** Water cooler */
function WaterCooler({ ax, ay }: { ax: number; ay: number }) {
  return (
    <>
      {/* body */}
      {R(ax+1, ay, 14, 24, '#c8dce8')}
      {R(ax, ay+2, 16, 20, '#d8ecf8')}
      {R(ax+1, ay+24, 14, 4, '#aaa')}
      {/* bottle */}
      {R(ax+4, ay-18, 8, 18, '#a0cce8')}
      {R(ax+5, ay-20, 6, 2, '#7ab0d0')}
      {/* nozzle buttons */}
      {R(ax+2, ay+10, 4, 3, '#3399ff')}
      {R(ax+10, ay+10, 4, 3, '#ff4444')}
      {/* legs */}
      {R(ax+2, ay+28, 4, 8, '#bbb')}
      {R(ax+10, ay+28, 4, 8, '#bbb')}
    </>
  );
}

/** Ceiling lights at the top */
function Ceiling({ scrollX }: { scrollX: number }) {
  // 4 lights spaced across 360px background
  const positions = [10, 100, 190, 280, 350];
  return (
    <>
      {positions.map(px => (
        <CeilLight key={px} ax={px - scrollX} ay={31} />
      ))}
    </>
  );
}

export function OfficeBackground() {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Scroll speed: background moves 1 art pixel every 2 frames (90 art px over 300 frames)
  const rawScroll = frame * 0.3;
  // Background tile width is 360px; loop it
  const BGW = 360;
  const scrollX = rawScroll % BGW;

  // Visible art pixel range: 0 to 179 (canvas is 180 wide)
  // We render 2 background strips side by side and use scrollX offset

  const bgOffset = -Math.floor(scrollX);

  return (
    <g>
      {/* ── Sky/wall base fill (the whole art canvas minus HUD area) ── */}
      <rect x={0} y={31 * S} width={180 * S} height={254 * S} fill={PAL.wall} />

      {/* Upper strip: horizon gradient above the wall */}
      <rect x={0} y={31 * S} width={180 * S} height={30 * S} fill={PAL.wallStripe} />

      {/* ── SCROLLING CONTENT (clipped to canvas width) ── */}
      <clipPath id="bgClip">
        <rect x={0} y={31 * S} width={180 * S} height={254 * S} />
      </clipPath>
      <g clipPath="url(#bgClip)">
        {/* Two copies of the background for seamless loop */}
        {[0, 1].map(copy => {
          const ox = bgOffset + copy * BGW;
          if (ox > 180 || ox + BGW < 0) return null;
          return (
            <g key={copy} transform={`translate(${ox * S},0)`}>
              {/* Wall stripes (vertical decoration) */}
              {[0, 72, 144, 216, 288].map(wx => (
                <rect key={wx} x={wx * S} y={31 * S} width={1 * S} height={254 * S} fill={PAL.wallStripe} />
              ))}

              {/* Ceiling */}
              <rect x={0} y={31 * S} width={BGW * S} height={8 * S} fill={PAL.ceil} />
              {/* Ceiling light strip */}
              <rect x={0} y={38 * S} width={BGW * S} height={1 * S} fill={PAL.wallStripe} />

              {/* Ceiling lights */}
              <CeilLight ax={8} ay={31} />
              <CeilLight ax={100} ay={31} />
              <CeilLight ax={192} ay={31} />
              <CeilLight ax={300} ay={31} />

              {/* Sunset window 1 */}
              <SunsetWindow ax={20} ay={50} />

              {/* Desk 1 */}
              <Desk ax={6} ay={170} />

              {/* Plant 1 */}
              <Plant ax={80} ay={218} />

              {/* Whiteboard */}
              <Whiteboard ax={100} ay={112} />

              {/* Desk 2 */}
              <Desk ax={160} ay={170} />

              {/* Sunset window 2 */}
              <SunsetWindow ax={225} ay={50} />

              {/* Water cooler */}
              <WaterCooler ax={295} ay={192} />

              {/* Desk 3 */}
              <Desk ax={310} ay={170} />

              {/* Plant 2 */}
              <Plant ax={225} ay={218} />
            </g>
          );
        })}
      </g>

      {/* ── Floor ── */}
      <rect x={0} y={231 * S} width={180 * S} height={4 * S} fill={PAL.floorShine} />
      <rect x={0} y={235 * S} width={180 * S} height={45 * S} fill={PAL.floor} />
      {/* Floor tile lines */}
      {Array.from({ length: 10 }).map((_, i) => (
        <rect key={i} x={i * 18 * S} y={231 * S} width={1 * S} height={49 * S} fill={PAL.floorLine} />
      ))}
      {/* Floor-wall shadow line */}
      <rect x={0} y={280 * S} width={180 * S} height={2 * S} fill='#00000040' />

      {/* ── Baseboard ── */}
      <rect x={0} y={228 * S} width={180 * S} height={3 * S} fill={PAL.wallStripe} />
    </g>
  );
}
