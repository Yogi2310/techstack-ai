// ── Muscular Mannequin Animator ──
// Draws a dark gray, anatomically muscular humanoid figure
// inspired by viral fitness "Muscle Dude" style characters.

class WorkoutAnimator {
  constructor() {
    this.width = 1080;
    this.height = 1920;
    this.activeExercise = 'pushup';
    this.glowColor = '#facc15';
    this.musclePulse = 0;
  }

  setExercise(ex) { this.activeExercise = ex; }
  setGlowColor(hex) { this.glowColor = hex; }

  // ── Color Palette ──
  get SKIN_DARK()  { return '#2a2a2e'; }
  get SKIN_MID()   { return '#3a3a40'; }
  get SKIN_LIGHT() { return '#555560'; }
  get SKIN_HIGH()  { return '#70707a'; }
  get OUTLINE()    { return '#1a1a1e'; }

  // ── Primitive Helpers ──

  // Thick muscular limb segment with 3D shading
  drawMuscularLimb(ctx, x1, y1, x2, y2, thickA, thickB, bulge) {
    const angle = Math.atan2(y2 - y1, x2 - x1);
    const len = Math.hypot(x2 - x1, y2 - y1);
    const perpX = Math.cos(angle + Math.PI / 2);
    const perpY = Math.sin(angle + Math.PI / 2);
    const dirX = Math.cos(angle);
    const dirY = Math.sin(angle);

    // Compute control points for the muscle bulge shape
    const midX = (x1 + x2) / 2;
    const midY = (y1 + y2) / 2;
    const bulgeThick = Math.max(thickA, thickB) + bulge;

    ctx.save();

    // Outer muscle shape (dark fill)
    ctx.beginPath();
    ctx.moveTo(x1 + perpX * thickA, y1 + perpY * thickA);
    ctx.quadraticCurveTo(
      midX + perpX * bulgeThick, midY + perpY * bulgeThick,
      x2 + perpX * thickB, y2 + perpY * thickB
    );
    ctx.lineTo(x2 - perpX * thickB, y2 - perpY * thickB);
    ctx.quadraticCurveTo(
      midX - perpX * bulgeThick * 0.85, midY - perpY * bulgeThick * 0.85,
      x1 - perpX * thickA, y1 - perpY * thickA
    );
    ctx.closePath();

    // 3D gradient fill
    const grd = ctx.createLinearGradient(
      midX + perpX * bulgeThick, midY + perpY * bulgeThick,
      midX - perpX * bulgeThick, midY - perpY * bulgeThick
    );
    grd.addColorStop(0, this.SKIN_LIGHT);
    grd.addColorStop(0.35, this.SKIN_MID);
    grd.addColorStop(0.65, this.SKIN_DARK);
    grd.addColorStop(1, this.OUTLINE);
    ctx.fillStyle = grd;
    ctx.fill();

    // Subtle outline
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Specular highlight streak
    ctx.beginPath();
    const hlOff = 0.6;
    ctx.moveTo(
      x1 + dirX * len * 0.15 + perpX * thickA * hlOff,
      y1 + dirY * len * 0.15 + perpY * thickA * hlOff
    );
    ctx.quadraticCurveTo(
      midX + perpX * bulgeThick * hlOff,
      midY + perpY * bulgeThick * hlOff,
      x2 - dirX * len * 0.15 + perpX * thickB * hlOff,
      y2 - dirY * len * 0.15 + perpY * thickB * hlOff
    );
    ctx.strokeStyle = this.SKIN_HIGH;
    ctx.lineWidth = 3;
    ctx.globalAlpha = 0.5;
    ctx.stroke();

    ctx.restore();
  }

  // Smooth mannequin head (featureless sphere with 3D shading)
  drawHead(ctx, x, y, radius) {
    ctx.save();

    // Head sphere
    const grd = ctx.createRadialGradient(
      x - radius * 0.25, y - radius * 0.3, radius * 0.1,
      x, y, radius
    );
    grd.addColorStop(0, this.SKIN_HIGH);
    grd.addColorStop(0.4, this.SKIN_MID);
    grd.addColorStop(0.85, this.SKIN_DARK);
    grd.addColorStop(1, this.OUTLINE);

    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = grd;
    ctx.fill();
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Subtle chin line
    ctx.beginPath();
    ctx.arc(x, y + radius * 0.15, radius * 0.75, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 1.5;
    ctx.globalAlpha = 0.25;
    ctx.stroke();

    ctx.restore();
  }

  // Anatomical torso with pecs, abs, and obliques
  drawTorso(ctx, shoulderLX, shoulderLY, shoulderRX, shoulderRY, hipLX, hipLY, hipRX, hipRY, intensity) {
    ctx.save();

    const sxC = (shoulderLX + shoulderRX) / 2;
    const syC = (shoulderLY + shoulderRY) / 2;
    const hxC = (hipLX + hipRX) / 2;
    const hyC = (hipLY + hipRY) / 2;
    const sWidth = Math.abs(shoulderRX - shoulderLX);
    const hWidth = Math.abs(hipRX - hipLX);

    // Main torso outline shape
    ctx.beginPath();
    ctx.moveTo(shoulderLX, shoulderLY);
    // Lat spread curve (left)
    ctx.quadraticCurveTo(
      shoulderLX - sWidth * 0.08, (shoulderLY + hipLY) * 0.45,
      hipLX, hipLY
    );
    ctx.lineTo(hipRX, hipRY);
    // Lat spread curve (right)
    ctx.quadraticCurveTo(
      shoulderRX + sWidth * 0.08, (shoulderRY + hipRY) * 0.45,
      shoulderRX, shoulderRY
    );
    ctx.closePath();

    // 3D torso gradient
    const tGrd = ctx.createLinearGradient(shoulderLX, syC, shoulderRX, syC);
    tGrd.addColorStop(0, this.OUTLINE);
    tGrd.addColorStop(0.2, this.SKIN_DARK);
    tGrd.addColorStop(0.45, this.SKIN_MID);
    tGrd.addColorStop(0.55, this.SKIN_LIGHT);
    tGrd.addColorStop(0.8, this.SKIN_MID);
    tGrd.addColorStop(1, this.OUTLINE);
    ctx.fillStyle = tGrd;
    ctx.fill();
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // ── Pectoral muscles ──
    const pecY = syC + (hyC - syC) * 0.08;
    const pecW = sWidth * 0.37;
    const pecH = (hyC - syC) * 0.22;

    // Left pec
    ctx.beginPath();
    ctx.ellipse(sxC - sWidth * 0.17, pecY, pecW, pecH, -0.08, 0, Math.PI * 2);
    ctx.fillStyle = this.SKIN_MID;
    ctx.fill();
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 1.8;
    ctx.globalAlpha = 0.55;
    ctx.stroke();

    // Right pec
    ctx.globalAlpha = 1;
    ctx.beginPath();
    ctx.ellipse(sxC + sWidth * 0.17, pecY, pecW, pecH, 0.08, 0, Math.PI * 2);
    ctx.fillStyle = this.SKIN_LIGHT;
    ctx.globalAlpha = 0.3;
    ctx.fill();
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 1.8;
    ctx.globalAlpha = 0.55;
    ctx.stroke();

    // ── Center chest line (sternum) ──
    ctx.globalAlpha = 0.5;
    ctx.beginPath();
    ctx.moveTo(sxC, syC + (hyC - syC) * 0.02);
    ctx.lineTo(sxC, syC + (hyC - syC) * 0.35);
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // ── Abs (6-pack) ──
    ctx.globalAlpha = 0.45;
    const absTop = syC + (hyC - syC) * 0.38;
    const absH = (hyC - syC) * 0.1;
    const absW = sWidth * 0.14;
    const absGap = 6;
    for (let row = 0; row < 3; row++) {
      const rowY = absTop + row * (absH + absGap);
      // Left ab
      ctx.beginPath();
      ctx.roundRect(sxC - absW - 4, rowY, absW, absH, 5);
      ctx.strokeStyle = this.OUTLINE;
      ctx.lineWidth = 2;
      ctx.stroke();
      // Right ab
      ctx.beginPath();
      ctx.roundRect(sxC + 4, rowY, absW, absH, 5);
      ctx.stroke();
    }

    // ── Center ab line (linea alba) ──
    ctx.beginPath();
    ctx.moveTo(sxC, absTop - 5);
    ctx.lineTo(sxC, absTop + 3 * (absH + absGap));
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 2.5;
    ctx.globalAlpha = 0.5;
    ctx.stroke();

    // ── Active muscle glow overlay ──
    if (intensity > 0.05) {
      ctx.globalAlpha = intensity * 0.15;
      ctx.fillStyle = this.glowColor;
      ctx.shadowColor = this.glowColor;
      ctx.shadowBlur = 25;
      ctx.beginPath();
      ctx.moveTo(shoulderLX, shoulderLY);
      ctx.quadraticCurveTo(
        shoulderLX - sWidth * 0.08, (shoulderLY + hipLY) * 0.45,
        hipLX, hipLY
      );
      ctx.lineTo(hipRX, hipRY);
      ctx.quadraticCurveTo(
        shoulderRX + sWidth * 0.08, (shoulderRY + hipRY) * 0.45,
        shoulderRX, shoulderRY
      );
      ctx.closePath();
      ctx.fill();
      ctx.shadowBlur = 0;
    }

    ctx.restore();
  }

  // Spherical joint with 3D gradient
  drawJoint(ctx, x, y, r) {
    ctx.save();
    const grd = ctx.createRadialGradient(x - r * 0.25, y - r * 0.25, r * 0.1, x, y, r);
    grd.addColorStop(0, this.SKIN_HIGH);
    grd.addColorStop(0.5, this.SKIN_MID);
    grd.addColorStop(1, this.OUTLINE);
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = grd;
    ctx.fill();
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.restore();
  }

  // Deltoid (shoulder cap muscle)
  drawDeltoid(ctx, sx, sy, armTopX, armTopY, outward) {
    ctx.save();
    const perpDir = outward; // 1 for right, -1 for left
    const capW = 42;
    const capH = 35;
    ctx.beginPath();
    ctx.ellipse(sx + perpDir * 5, sy, capW, capH, perpDir * 0.2, 0, Math.PI * 2);

    const grd = ctx.createRadialGradient(
      sx + perpDir * 5 - capW * 0.2, sy - capH * 0.2, 3,
      sx + perpDir * 5, sy, capW
    );
    grd.addColorStop(0, this.SKIN_HIGH);
    grd.addColorStop(0.5, this.SKIN_MID);
    grd.addColorStop(1, this.SKIN_DARK);
    ctx.fillStyle = grd;
    ctx.fill();
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 2;
    ctx.globalAlpha = 0.6;
    ctx.stroke();
    ctx.restore();
  }

  // Muscle glow overlay on limbs
  drawMuscleGlow(ctx, x1, y1, x2, y2, width, intensity) {
    if (intensity < 0.05) return;
    ctx.save();
    ctx.lineWidth = width;
    ctx.strokeStyle = this.glowColor;
    ctx.globalAlpha = intensity * 0.18 * this.musclePulse;
    ctx.shadowColor = this.glowColor;
    ctx.shadowBlur = 20;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.restore();
  }

  // Dumbbell
  drawDumbbell(ctx, x, y, angle) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);

    // Bar
    ctx.fillStyle = '#4a4a4f';
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(-40, -6, 80, 12, 6);
    ctx.fill();
    ctx.stroke();

    // Weight plates
    const drawPlate = (ox) => {
      ctx.save();
      ctx.translate(ox, 0);
      ctx.fillStyle = this.SKIN_DARK;
      ctx.strokeStyle = this.OUTLINE;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(-16, -28, 32, 56, 4);
      ctx.fill();
      ctx.stroke();

      // Inner ridge
      ctx.fillStyle = this.SKIN_MID;
      ctx.beginPath();
      ctx.roundRect(-10, -22, 20, 44, 3);
      ctx.fill();
      ctx.restore();
    };

    drawPlate(-42);
    drawPlate(42);

    ctx.restore();
  }

  // Pull-up bar
  drawBar(ctx, x1, y, x2) {
    ctx.save();
    const grd = ctx.createLinearGradient(x1, y - 12, x1, y + 12);
    grd.addColorStop(0, '#606068');
    grd.addColorStop(0.5, '#808088');
    grd.addColorStop(1, '#404048');
    ctx.fillStyle = grd;
    ctx.strokeStyle = this.OUTLINE;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.roundRect(x1, y - 10, x2 - x1, 20, 10);
    ctx.fill();
    ctx.stroke();
    ctx.restore();
  }

  // Floor line
  drawFloor(ctx, w, y) {
    ctx.save();
    ctx.strokeStyle = '#3a3a42';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(w * 0.03, y);
    ctx.lineTo(w * 0.97, y);
    ctx.stroke();

    // Floor reflection gradient
    const grd = ctx.createLinearGradient(0, y, 0, y + 120);
    grd.addColorStop(0, 'rgba(255,255,255,0.025)');
    grd.addColorStop(1, 'transparent');
    ctx.fillStyle = grd;
    ctx.fillRect(w * 0.1, y, w * 0.8, 120);
    ctx.restore();
  }

  // Background grid
  drawBackgroundGrid(ctx, w, h, time) {
    ctx.save();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.015)';
    ctx.lineWidth = 1;
    const size = 80;
    for (let x = 0; x < w; x += size) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (let y = 0; y < h; y += size) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }
    ctx.restore();
  }

  // ── Full Character Builder ──
  // Draws the full mannequin given joint positions
  drawCharacter(ctx, joints, intensity) {
    const {
      headX, headY,
      neckX, neckY,
      shoulderLX, shoulderLY, shoulderRX, shoulderRY,
      elbowLX, elbowLY, elbowRX, elbowRY,
      handLX, handLY, handRX, handRY,
      hipLX, hipLY, hipRX, hipRY,
      kneeLX, kneeLY, kneeRX, kneeRY,
      footLX, footLY, footRX, footRY
    } = joints;

    // Draw order: back limbs → torso → front limbs → head

    // ── Back Leg (left) ──
    this.drawMuscleGlow(ctx, hipLX, hipLY, kneeLX, kneeLY, 50, intensity);
    this.drawMuscularLimb(ctx, hipLX, hipLY, kneeLX, kneeLY, 32, 24, 16);  // Quad/ham
    this.drawMuscularLimb(ctx, kneeLX, kneeLY, footLX, footLY, 22, 14, 10); // Calf
    this.drawJoint(ctx, kneeLX, kneeLY, 16);
    this.drawJoint(ctx, footLX, footLY, 11);

    // ── Back Arm (left) ──
    this.drawMuscleGlow(ctx, shoulderLX, shoulderLY, elbowLX, elbowLY, 40, intensity);
    this.drawMuscularLimb(ctx, shoulderLX, shoulderLY, elbowLX, elbowLY, 26, 20, 14); // Bicep/tri
    this.drawMuscularLimb(ctx, elbowLX, elbowLY, handLX, handLY, 18, 12, 6); // Forearm
    this.drawJoint(ctx, elbowLX, elbowLY, 13);
    this.drawJoint(ctx, handLX, handLY, 10);

    // ── Torso ──
    this.drawTorso(ctx,
      shoulderLX, shoulderLY, shoulderRX, shoulderRY,
      hipLX, hipLY, hipRX, hipRY,
      intensity
    );

    // ── Deltoids (shoulder caps, drawn over torso edge) ──
    this.drawDeltoid(ctx, shoulderLX, shoulderLY, elbowLX, elbowLY, -1);
    this.drawDeltoid(ctx, shoulderRX, shoulderRY, elbowRX, elbowRY, 1);

    // ── Front Leg (right) ──
    this.drawMuscleGlow(ctx, hipRX, hipRY, kneeRX, kneeRY, 50, intensity);
    this.drawMuscularLimb(ctx, hipRX, hipRY, kneeRX, kneeRY, 32, 24, 16);
    this.drawMuscularLimb(ctx, kneeRX, kneeRY, footRX, footRY, 22, 14, 10);
    this.drawJoint(ctx, kneeRX, kneeRY, 16);
    this.drawJoint(ctx, footRX, footRY, 11);

    // ── Front Arm (right) ──
    this.drawMuscleGlow(ctx, shoulderRX, shoulderRY, elbowRX, elbowRY, 40, intensity);
    this.drawMuscularLimb(ctx, shoulderRX, shoulderRY, elbowRX, elbowRY, 26, 20, 14);
    this.drawMuscularLimb(ctx, elbowRX, elbowRY, handRX, handRY, 18, 12, 6);
    this.drawJoint(ctx, elbowRX, elbowRY, 13);
    this.drawJoint(ctx, handRX, handRY, 10);

    // ── Neck ──
    this.drawMuscularLimb(ctx, neckX, neckY, (shoulderLX + shoulderRX) / 2, (shoulderLY + shoulderRY) / 2, 16, 22, 4);

    // ── Head ──
    this.drawHead(ctx, headX, headY, 42);

    // ── Hip/Shoulder Joints ──
    this.drawJoint(ctx, shoulderLX, shoulderLY, 18);
    this.drawJoint(ctx, shoulderRX, shoulderRY, 18);
    this.drawJoint(ctx, hipLX, hipLY, 18);
    this.drawJoint(ctx, hipRX, hipRY, 18);
  }

  // ── Main Render ──
  render(ctx, time, activeProgress, workoutProgress) {
    this.musclePulse = 0.5 + 0.5 * Math.sin(time * 10);
    const w = this.width;
    const h = this.height;
    timeSecs = time;

    this.drawBackgroundGrid(ctx, w, h, time);

    switch (this.activeExercise) {
      case 'pushup':  this.animatePushup(ctx, w, h, activeProgress, time); break;
      case 'squat':   this.animateSquat(ctx, w, h, activeProgress, time); break;
      case 'pullup':  this.animatePullup(ctx, w, h, activeProgress, time); break;
      case 'curl':    this.animateCurl(ctx, w, h, activeProgress, time); break;
      case 'plank':   this.animatePlank(ctx, w, h, activeProgress, time); break;
      case 'deadlift':    this.animateDeadlift(ctx, w, h, activeProgress, time); break;
      case 'shoulderpress': this.animateShoulderPress(ctx, w, h, activeProgress, time); break;
      case 'lunge':       this.animateLunge(ctx, w, h, activeProgress, time); break;
      case 'crunch':      this.animateCrunch(ctx, w, h, activeProgress, time); break;
      case 'jumpingjack': this.animateJumpingJack(ctx, w, h, activeProgress, time); break;
      case 'mountainclimber': this.animateMountainClimber(ctx, w, h, activeProgress, time); break;
      case 'tricepdip':   this.animateTricepDip(ctx, w, h, activeProgress, time); break;
      case 'lateralraise': this.animateLateralRaise(ctx, w, h, activeProgress, time); break;
      case 'bentoverrow':  this.animateBentOverRow(ctx, w, h, activeProgress, time); break;
      case 'jumpsquat':    this.animateJumpSquat(ctx, w, h, activeProgress, time); break;
    }
  }

  // ── Exercise Animations ──

  // 1. PUSH-UP
  animatePushup(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.62;
    this.drawFloor(ctx, w, floorY);

    // Side view push-up: body is mostly horizontal
    const handX = w * 0.68, handY = floorY;
    const footX = w * 0.22, footY = floorY - 10;

    const shoulderX = w * 0.62, shoulderY = floorY - 170 + f * 100;
    const hipX = w * 0.38, hipY = shoulderY + (footY - shoulderY) * 0.35 + f * 15;
    const kneeX = (footX + hipX) / 2, kneeY = (footY + hipY) / 2;

    const elbowX = shoulderX + 55 + f * 40, elbowY = (shoulderY + handY) / 2 - 25 + f * 20;

    const neckX = shoulderX + 30, neckY = shoulderY - 35;
    const headX = neckX + 25, headY = neckY - 30;

    // Use symmetrical joint positions (side view = L and R overlap)
    const off = 12; // slight depth offset
    this.drawCharacter(ctx, {
      headX, headY,
      neckX, neckY,
      shoulderLX: shoulderX - off, shoulderLY: shoulderY + off * 0.5,
      shoulderRX: shoulderX + off, shoulderRY: shoulderY - off * 0.5,
      elbowLX: elbowX - off, elbowLY: elbowY + off * 0.3,
      elbowRX: elbowX + off, elbowRY: elbowY - off * 0.3,
      handLX: handX - off * 0.5, handLY: handY,
      handRX: handX + off * 0.5, handRY: handY,
      hipLX: hipX - off, hipLY: hipY + off * 0.3,
      hipRX: hipX + off, hipRY: hipY - off * 0.3,
      kneeLX: kneeX - off, kneeLY: kneeY + off * 0.3,
      kneeRX: kneeX + off, kneeRY: kneeY - off * 0.3,
      footLX: footX - off * 0.5, footLY: footY,
      footRX: footX + off * 0.5, footRY: footY,
    }, f);
  }

  // 2. SQUAT
  animateSquat(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.72;
    this.drawFloor(ctx, w, floorY);

    const cx = w * 0.5;

    const footSpread = 120;
    const footLX = cx - footSpread, footRX = cx + footSpread, footY = floorY;

    const kneeBend = f * 140;
    const kneeLX = footLX - 30 * f, kneeLY = floorY - 250 + kneeBend;
    const kneeRX = footRX + 30 * f, kneeRY = kneeLY;

    const hipDrop = f * 200;
    const hipLX = cx - 55, hipRX = cx + 55;
    const hipY = floorY - 480 + hipDrop;

    const shoulderLX = cx - 80, shoulderRX = cx + 80;
    const shoulderY = hipY - 280;

    const neckX = cx, neckY = shoulderY - 30;
    const headX = cx, headY = neckY - 50;

    // Arms forward for balance
    const armAngle = 0.2 + f * 0.5;
    const armLen = 170;
    const elbowLX = shoulderLX - 50 - f * 40, elbowRX = shoulderRX + 50 + f * 40;
    const elbowY = shoulderY + 100 + f * 30;
    const handLX = elbowLX - 30, handRX = elbowRX + 30;
    const handY = elbowY + 80;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY,
      shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY: elbowY,
      elbowRX, elbowRY: elbowY,
      handLX, handLY: handY,
      handRX, handRY: handY,
      hipLX, hipLY: hipY,
      hipRX, hipRY: hipY,
      kneeLX, kneeLY: kneeLY,
      kneeRX, kneeRY: kneeRY,
      footLX, footLY: footY,
      footRX, footRY: footY,
    }, f);
  }

  // 3. PULL-UP
  animatePullup(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const barY = h * 0.22;
    this.drawBar(ctx, w * 0.2, barY, w * 0.8);

    const cx = w * 0.5;
    const liftY = -200 * f;

    const handLX = cx - 130, handRX = cx + 130, handY = barY + 5;
    const shoulderLX = cx - 80, shoulderRX = cx + 80;
    const shoulderY = barY + 280 + liftY;

    const elbowLX = shoulderLX - 60 - f * 50;
    const elbowRX = shoulderRX + 60 + f * 50;
    const elbowY = (handY + shoulderY) / 2 + 20 * (1 - f);

    const neckX = cx, neckY = shoulderY - 30;
    const headX = cx, headY = neckY - 48;

    const hipLX = cx - 50, hipRX = cx + 50;
    const hipY = shoulderY + 300;

    const kneeLX = hipLX - 15 - 30 * f, kneeRX = hipRX + 15 + 30 * f;
    const kneeY = hipY + 230;
    const footLX = kneeLX + 10, footRX = kneeRX - 10;
    const footY = kneeY + 210;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY,
      shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY: elbowY,
      elbowRX, elbowRY: elbowY,
      handLX, handLY: handY,
      handRX, handRY: handY,
      hipLX, hipLY: hipY,
      hipRX, hipRY: hipY,
      kneeLX, kneeLY: kneeY,
      kneeRX, kneeRY: kneeY,
      footLX, footLY: footY,
      footRX, footRY: footY,
    }, f);
  }

  // 4. BICEP CURL
  animateCurl(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.72;
    this.drawFloor(ctx, w, floorY);

    const cx = w * 0.5;

    const footLX = cx - 70, footRX = cx + 70, footY = floorY;
    const kneeLX = cx - 55, kneeRX = cx + 55, kneeY = floorY - 260;
    const hipLX = cx - 50, hipRX = cx + 50, hipY = floorY - 490;
    const shoulderLX = cx - 75, shoulderRX = cx + 75, shoulderY = floorY - 780;

    const neckX = cx, neckY = shoulderY - 30;
    const headX = cx, headY = neckY - 50;

    // Right arm curling
    const elbowRX = shoulderRX + 20, elbowRY = shoulderY + 180;
    const curlAngle = Math.PI * 0.5 - f * Math.PI * 0.85;
    const forearmLen = 170;
    const handRX = elbowRX + Math.cos(curlAngle) * forearmLen;
    const handRY = elbowRY + Math.sin(curlAngle) * forearmLen;

    // Left arm relaxed at side
    const elbowLX = shoulderLX - 20, elbowLY = shoulderY + 180;
    const handLX = elbowLX - 10, handLY = elbowLY + 160;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY,
      shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY,
      elbowRX, elbowRY,
      handLX, handLY,
      handRX, handRY,
      hipLX, hipLY: hipY,
      hipRX, hipRY: hipY,
      kneeLX, kneeLY: kneeY,
      kneeRX, kneeRY: kneeY,
      footLX, footLY: footY,
      footRX, footRY: footY,
    }, f);

    // Dumbbell in right hand
    this.drawDumbbell(ctx, handRX, handRY, curlAngle + Math.PI / 2);
  }

  // 5. PLANK
  animatePlank(ctx, w, h, p, time) {
    const wobble = Math.sin(p * Math.PI * 6) * 5;
    const floorY = h * 0.62;
    this.drawFloor(ctx, w, floorY);

    const footX = w * 0.22, footY = floorY - 10;
    const elbowX = w * 0.68, elbowY = floorY - 80;
    const handX = elbowX + 100, handY = floorY;

    const shoulderX = w * 0.62, shoulderY = floorY - 180 + wobble;
    const hipX = w * 0.38, hipY = shoulderY + (footY - shoulderY) * 0.35 + wobble * 0.5;
    const kneeX = (footX + hipX) / 2, kneeY = (footY + hipY) / 2;

    const neckX = shoulderX + 30, neckY = shoulderY - 32;
    const headX = neckX + 22, headY = neckY - 28;

    const off = 12;
    const coreIntensity = 0.5 + 0.5 * Math.sin(p * Math.PI * 2);

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX: shoulderX - off, shoulderLY: shoulderY + off * 0.4,
      shoulderRX: shoulderX + off, shoulderRY: shoulderY - off * 0.4,
      elbowLX: elbowX - off, elbowLY: elbowY + off * 0.3,
      elbowRX: elbowX + off, elbowRY: elbowY - off * 0.3,
      handLX: handX - off * 0.5, handLY: handY,
      handRX: handX + off * 0.5, handRY: handY,
      hipLX: hipX - off, hipLY: hipY + off * 0.3,
      hipRX: hipX + off, hipRY: hipY - off * 0.3,
      kneeLX: kneeX - off, kneeLY: kneeY + off * 0.3,
      kneeRX: kneeX + off, kneeRY: kneeY - off * 0.3,
      footLX: footX - off * 0.5, footLY: footY,
      footRX: footX + off * 0.5, footRY: footY,
    }, coreIntensity);
  }

  // 6. DEADLIFT
  animateDeadlift(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.72;
    this.drawFloor(ctx, w, floorY);
    const cx = w * 0.5;

    const footLX = cx - 80, footRX = cx + 80, footY = floorY;
    const kneeLX = cx - 65, kneeRX = cx + 65;
    const kneeY = floorY - 250 + f * 40;

    const hipLX = cx - 50, hipRX = cx + 50;
    const hipY = floorY - 440 + f * 180;

    const shoulderLX = cx - 85, shoulderRX = cx + 85;
    const shoulderY = hipY - 260 - f * 40;

    const neckX = cx, neckY = shoulderY - 30;
    const headX = cx, headY = neckY - 48;

    const elbowLX = shoulderLX - 10, elbowRX = shoulderRX + 10;
    const elbowY = shoulderY + 170 + f * 60;
    const handLX = elbowLX + 10, handRX = elbowRX - 10;
    const handY = elbowY + 140 + f * 40;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY, shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY: elbowY, elbowRX, elbowRY: elbowY,
      handLX, handLY: handY, handRX, handRY: handY,
      hipLX, hipLY: hipY, hipRX, hipRY: hipY,
      kneeLX, kneeLY: kneeY, kneeRX, kneeRY: kneeY,
      footLX, footLY: footY, footRX, footRY: footY,
    }, f);

    // Barbell on the ground
    this.drawBar(ctx, w * 0.1, handY + 6, w * 0.9);
  }

  // 7. SHOULDER PRESS
  animateShoulderPress(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.72;
    this.drawFloor(ctx, w, floorY);
    const cx = w * 0.5;

    const footLX = cx - 70, footRX = cx + 70, footY = floorY;
    const kneeLX = cx - 55, kneeRX = cx + 55, kneeY = floorY - 260;
    const hipLX = cx - 50, hipRX = cx + 50, hipY = floorY - 490;
    const shoulderLX = cx - 80, shoulderRX = cx + 80, shoulderY = floorY - 780;

    const neckX = cx, neckY = shoulderY - 30;
    const headX = cx, headY = neckY - 50;

    const elbowLX = shoulderLX - 60 - f * 20;
    const elbowRX = shoulderRX + 60 + f * 20;
    const elbowY = shoulderY - 40 - f * 120;

    const handLX = elbowLX - 20 + f * 40;
    const handRX = elbowRX + 20 - f * 40;
    const handY = elbowY - 130 - f * 60;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY, shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY: elbowY, elbowRX, elbowRY: elbowY,
      handLX, handLY: handY, handRX, handRY: handY,
      hipLX, hipLY: hipY, hipRX, hipRY: hipY,
      kneeLX, kneeLY: kneeY, kneeRX, kneeRY: kneeY,
      footLX, footLY: footY, footRX, footRY: footY,
    }, f);

    this.drawDumbbell(ctx, handLX, handY, 0);
    this.drawDumbbell(ctx, handRX, handY, 0);
  }

  // 8. LUNGE
  animateLunge(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.72;
    this.drawFloor(ctx, w, floorY);
    const cx = w * 0.5;

    const footLX = cx - 140 - f * 60, footRX = cx + 100 + f * 60;
    const footY = floorY;

    const kneeLX = footLX + 50, kneeRX = footRX - 30;
    const kneeLY = floorY - 280 + f * 120;
    const kneeRY = floorY - 120 - f * 60;

    const hipLX = cx - 50, hipRX = cx + 50;
    const hipY = floorY - 460 + f * 140;

    const shoulderLX = cx - 75, shoulderRX = cx + 75;
    const shoulderY = hipY - 290;

    const neckX = cx, neckY = shoulderY - 28;
    const headX = cx, headY = neckY - 48;

    const elbowLX = shoulderLX - 20, elbowRX = shoulderRX + 20;
    const elbowY = shoulderY + 160;
    const handLX = elbowLX, handRX = elbowRX;
    const handY = elbowY + 130;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY, shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY: elbowY, elbowRX, elbowRY: elbowY,
      handLX, handLY: handY, handRX, handRY: handY,
      hipLX, hipLY: hipY, hipRX, hipRY: hipY,
      kneeLX, kneeLY, kneeRX, kneeRY,
      footLX, footLY: footY, footRX, footRY: footY,
    }, f);
  }

  // 9. CRUNCH
  animateCrunch(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.65;
    this.drawFloor(ctx, w, floorY);

    const cx = w * 0.5;
    const hipX = cx, hipY = floorY - 30;

    const footLX = cx + 200 - f * 30, footRX = cx + 220 - f * 30;
    const footY = floorY;
    const kneeLX = cx + 140, kneeRX = cx + 160;
    const kneeY = floorY - 180;

    const shoulderLX = cx - 100 + f * 60, shoulderRX = cx - 80 + f * 60;
    const shoulderY = floorY - 50 - f * 120;

    const neckX = (shoulderLX + shoulderRX) / 2 - 20;
    const neckY = shoulderY - 25;
    const headX = neckX - 15, headY = neckY - 30;

    const elbowLX = shoulderLX - 30, elbowRX = shoulderRX + 30;
    const elbowY = shoulderY + 10;
    const handLX = headX - 20, handRX = headX + 40;
    const handY = headY;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY, shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY: elbowY, elbowRX, elbowRY: elbowY,
      handLX, handLY: handY, handRX, handRY: handY,
      hipLX: hipX - 30, hipLY: hipY, hipRX: hipX + 30, hipRY: hipY,
      kneeLX, kneeLY: kneeY, kneeRX, kneeRY: kneeY,
      footLX, footLY: footY, footRX, footRY: footY,
    }, f);
  }

  // 10. JUMPING JACK
  animateJumpingJack(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.72;
    const jumpH = f * 30;
    this.drawFloor(ctx, w, floorY);
    const cx = w * 0.5;

    const footSpread = 50 + f * 120;
    const footLX = cx - footSpread, footRX = cx + footSpread;
    const footY = floorY - jumpH;

    const kneeLX = cx - footSpread * 0.6, kneeRX = cx + footSpread * 0.6;
    const kneeY = footY - 260;

    const hipLX = cx - 50, hipRX = cx + 50;
    const hipY = footY - 490;

    const shoulderLX = cx - 80, shoulderRX = cx + 80;
    const shoulderY = hipY - 280;

    const neckX = cx, neckY = shoulderY - 30;
    const headX = cx, headY = neckY - 50;

    const armAngle = -0.3 - f * 2.0;
    const armLen = 180;
    const elbowLX = shoulderLX + Math.cos(Math.PI + armAngle) * armLen * 0.5;
    const elbowLY = shoulderY + Math.sin(Math.PI + armAngle) * armLen * 0.5;
    const elbowRX = shoulderRX + Math.cos(armAngle) * armLen * 0.5;
    const elbowRY = shoulderY + Math.sin(armAngle) * armLen * 0.5;
    const handLX = shoulderLX + Math.cos(Math.PI + armAngle) * armLen;
    const handLY = shoulderY + Math.sin(Math.PI + armAngle) * armLen;
    const handRX = shoulderRX + Math.cos(armAngle) * armLen;
    const handRY = shoulderY + Math.sin(armAngle) * armLen;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY, shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY, elbowRX, elbowRY,
      handLX, handLY, handRX, handRY,
      hipLX, hipLY: hipY, hipRX, hipRY: hipY,
      kneeLX, kneeLY: kneeY, kneeRX, kneeRY: kneeY,
      footLX, footLY: footY, footRX, footRY: footY,
    }, f);
  }

  // 11. MOUNTAIN CLIMBER
  animateMountainClimber(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.62;
    this.drawFloor(ctx, w, floorY);

    const handX = w * 0.72, handY = floorY;
    const shoulderX = w * 0.65, shoulderY = floorY - 220;

    const hipX = w * 0.42, hipY = shoulderY + 100;

    const neckX = shoulderX + 28, neckY = shoulderY - 32;
    const headX = neckX + 20, headY = neckY - 28;

    const off = 14;
    const elbowX = (shoulderX + handX) / 2 + 20;
    const elbowY = (shoulderY + handY) / 2 - 20;

    // Alternating legs
    const frontKneeX = hipX + 80 + f * 120;
    const frontKneeY = hipY + 80 - f * 60;
    const frontFootX = frontKneeX + 40;
    const frontFootY = floorY - 20 - f * 80;

    const backKneeX = hipX - 80 - (1 - f) * 60;
    const backKneeY = hipY + 100 + (1 - f) * 30;
    const backFootX = w * 0.18 - (1 - f) * 30;
    const backFootY = floorY - 10;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX: shoulderX - off, shoulderLY: shoulderY + off * 0.4,
      shoulderRX: shoulderX + off, shoulderRY: shoulderY - off * 0.4,
      elbowLX: elbowX - off, elbowLY: elbowY + off * 0.3,
      elbowRX: elbowX + off, elbowRY: elbowY - off * 0.3,
      handLX: handX - off * 0.5, handLY: handY,
      handRX: handX + off * 0.5, handRY: handY,
      hipLX: hipX - off, hipLY: hipY + off * 0.3,
      hipRX: hipX + off, hipRY: hipY - off * 0.3,
      kneeLX: backKneeX, kneeLY: backKneeY,
      kneeRX: frontKneeX, kneeRY: frontKneeY,
      footLX: backFootX, footLY: backFootY,
      footRX: frontFootX, footRY: frontFootY,
    }, f);
  }

  // 12. TRICEP DIP
  animateTricepDip(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.72;
    this.drawFloor(ctx, w, floorY);
    const cx = w * 0.5;

    const benchY = floorY - 200;
    this.drawBar(ctx, w * 0.25, benchY, w * 0.75);

    const handLX = cx - 90, handRX = cx + 90, handY = benchY;

    const shoulderLX = cx - 70, shoulderRX = cx + 70;
    const shoulderY = benchY + 80 + f * 120;

    const elbowLX = shoulderLX - 40 - f * 30;
    const elbowRX = shoulderRX + 40 + f * 30;
    const elbowY = (handY + shoulderY) / 2 + f * 30;

    const neckX = cx, neckY = shoulderY - 28;
    const headX = cx, headY = neckY - 48;

    const hipLX = cx - 45, hipRX = cx + 45;
    const hipY = shoulderY + 270;

    const kneeLX = cx - 60, kneeRX = cx + 60;
    const kneeY = hipY + 200;
    const footLX = kneeLX + 60, footRX = kneeRX - 60;
    const footY = floorY;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY, shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY: elbowY, elbowRX, elbowRY: elbowY,
      handLX, handLY: handY, handRX, handRY: handY,
      hipLX, hipLY: hipY, hipRX, hipRY: hipY,
      kneeLX, kneeLY: kneeY, kneeRX, kneeRY: kneeY,
      footLX, footLY: footY, footRX, footRY: footY,
    }, f);
  }

  // 13. LATERAL RAISE
  animateLateralRaise(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.72;
    this.drawFloor(ctx, w, floorY);
    const cx = w * 0.5;

    const footLX = cx - 70, footRX = cx + 70, footY = floorY;
    const kneeLX = cx - 55, kneeRX = cx + 55, kneeY = floorY - 260;
    const hipLX = cx - 50, hipRX = cx + 50, hipY = floorY - 490;
    const shoulderLX = cx - 80, shoulderRX = cx + 80, shoulderY = floorY - 780;

    const neckX = cx, neckY = shoulderY - 30;
    const headX = cx, headY = neckY - 50;

    const raiseAngle = f * Math.PI * 0.42;
    const armLen = 180;
    const elbowLX = shoulderLX + Math.cos(Math.PI / 2 + raiseAngle) * armLen * 0.55 * -1;
    const elbowLY = shoulderY + Math.sin(Math.PI / 2 + raiseAngle) * armLen * 0.55;
    const elbowRX = shoulderRX + Math.cos(Math.PI / 2 + raiseAngle) * armLen * 0.55;
    const elbowRY = shoulderY + Math.sin(Math.PI / 2 + raiseAngle) * armLen * 0.55;

    const handLX = shoulderLX + Math.cos(Math.PI / 2 + raiseAngle) * armLen * -1;
    const handLY = shoulderY + Math.sin(Math.PI / 2 + raiseAngle) * armLen;
    const handRX = shoulderRX + Math.cos(Math.PI / 2 + raiseAngle) * armLen;
    const handRY = shoulderY + Math.sin(Math.PI / 2 + raiseAngle) * armLen;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY, shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY, elbowRX, elbowRY,
      handLX, handLY, handRX, handRY,
      hipLX, hipLY: hipY, hipRX, hipRY: hipY,
      kneeLX, kneeLY: kneeY, kneeRX, kneeRY: kneeY,
      footLX, footLY: footY, footRX, footRY: footY,
    }, f);

    this.drawDumbbell(ctx, handLX, handLY, Math.PI / 2 + raiseAngle);
    this.drawDumbbell(ctx, handRX, handRY, Math.PI / 2 + raiseAngle);
  }

  // 14. BENT-OVER ROW
  animateBentOverRow(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.72;
    this.drawFloor(ctx, w, floorY);
    const cx = w * 0.5;

    const footLX = cx - 80, footRX = cx + 80, footY = floorY;
    const kneeLX = cx - 65, kneeRX = cx + 65, kneeY = floorY - 260;

    const hipLX = cx - 50, hipRX = cx + 50;
    const hipY = floorY - 440;

    const shoulderLX = cx - 90 + 40, shoulderRX = cx + 90 - 40;
    const shoulderY = hipY - 180;

    const neckX = (shoulderLX + shoulderRX) / 2 - 30;
    const neckY = shoulderY - 25;
    const headX = neckX - 20, headY = neckY - 35;

    const elbowLX = shoulderLX - 20 - f * 50;
    const elbowRX = shoulderRX + 20 + f * 50;
    const elbowY = shoulderY + 120 - f * 80;

    const handLX = elbowLX + 10;
    const handRX = elbowRX - 10;
    const handY = elbowY + 100 - f * 60;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY, shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY: elbowY, elbowRX, elbowRY: elbowY,
      handLX, handLY: handY, handRX, handRY: handY,
      hipLX, hipLY: hipY, hipRX, hipRY: hipY,
      kneeLX, kneeLY: kneeY, kneeRX, kneeRY: kneeY,
      footLX, footLY: footY, footRX, footRY: footY,
    }, f);

    this.drawDumbbell(ctx, handLX, handY, 0);
    this.drawDumbbell(ctx, handRX, handY, 0);
  }

  // 15. JUMP SQUAT
  animateJumpSquat(ctx, w, h, p, time) {
    const f = 0.5 - 0.5 * Math.cos(p * Math.PI * 2);
    const floorY = h * 0.72;
    this.drawFloor(ctx, w, floorY);
    const cx = w * 0.5;

    const jumpPhase = f < 0.5 ? f * 2 : 2 - f * 2;
    const jumpH = jumpPhase * 120;
    const squat = f < 0.5 ? (0.5 - f) * 2 : (f - 0.5) * 2;

    const footSpread = 100 + squat * 40;
    const footLX = cx - footSpread, footRX = cx + footSpread;
    const footY = floorY - jumpH;

    const kneeLX = footLX + 15 - squat * 20;
    const kneeRX = footRX - 15 + squat * 20;
    const kneeY = footY - 250 + squat * 100;

    const hipLX = cx - 55, hipRX = cx + 55;
    const hipY = footY - 470 + squat * 150;

    const shoulderLX = cx - 80, shoulderRX = cx + 80;
    const shoulderY = hipY - 280;

    const neckX = cx, neckY = shoulderY - 30;
    const headX = cx, headY = neckY - 50;

    const armUp = jumpPhase;
    const elbowLX = shoulderLX - 40 - armUp * 30;
    const elbowRX = shoulderRX + 40 + armUp * 30;
    const elbowY = shoulderY - 20 - armUp * 100;
    const handLX = elbowLX - 10 + armUp * 30;
    const handRX = elbowRX + 10 - armUp * 30;
    const handY = elbowY - 100 - armUp * 40;

    this.drawCharacter(ctx, {
      headX, headY, neckX, neckY,
      shoulderLX, shoulderLY: shoulderY, shoulderRX, shoulderRY: shoulderY,
      elbowLX, elbowLY: elbowY, elbowRX, elbowRY: elbowY,
      handLX, handLY: handY, handRX, handRY: handY,
      hipLX, hipLY: hipY, hipRX, hipRY: hipY,
      kneeLX, kneeLY: kneeY, kneeRX, kneeRY: kneeY,
      footLX, footLY: footY, footRX, footRY: footY,
    }, f);
  }
}

let timeSecs = 0.0;
const animator = new WorkoutAnimator();
