/**
 * WalkCycle.tsx — 16-bit pixel art stepped walk cycle
 * Animation advances in discrete steps (not smooth) for sprite feel.
 */

/** How many real frames between sprite frame advances (10fps walk) */
export const SPRITE_STEP = 6;
/** Number of walk frames in the sprite sheet */
export const WALK_FRAMES = 4;
/** Full stride = WALK_FRAMES × SPRITE_STEP real frames */
export const STRIDE_FRAMES = WALK_FRAMES * SPRITE_STEP; // 24

/** Returns discrete sprite frame index 0-3 */
export function getSpriteFrame(frame: number): number {
  return Math.floor(frame / SPRITE_STEP) % WALK_FRAMES;
}

/** Step count (how many full strides completed) */
export function getStepCount(frame: number): number {
  return Math.floor(frame / STRIDE_FRAMES);
}

/** XP 0-100 based on overall progress */
export function getXP(frame: number, total: number): number {
  return Math.round((frame / total) * 100);
}
