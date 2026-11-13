// ============================================================
// KidsFlix Generator v3 — Animated Cartoon Characters
// Pure Canvas 2D: hand-drawn characters + animated effects
// ============================================================
export const CANVAS_W = 1080;
export const CANVAS_H = 1920;

// ─── Content pool ────────────────────────────────────────────
const CONTENT = {
  cartoon:[
    {emoji:'🐷',text:'Peppa LOVES\nMuddy Puddles!',accent:'Jump in every puddle! 🌧️',color:'#ff6eb4'},
    {emoji:'🦈',text:'Baby Shark\nDoo Doo Doo!',accent:'Most watched video EVER! 🎉',color:'#4fc3f7'},
    {emoji:'🐱',text:'Tom chases Jerry\nevery day!',accent:'But they\'re BEST friends! 🤝',color:'#ffa726'},
    {emoji:'🐾',text:'Bluey lives in\nAustralia!',accent:'Her dad Bandit is so funny! 😂',color:'#42a5f5'},
    {emoji:'🚔',text:'Chase is on\nthe Case!',accent:'No job too big for PAW Patrol! 🐶',color:'#5c6bc0'},
    {emoji:'💪',text:'Chhota Bheem\nis STRONGEST!',accent:'Laddoos give him power! 🍡',color:'#66bb6a'},
    {emoji:'🏎️',text:'Lightning McQueen\nKA-CHOW!',accent:'Speed is his superpower! ⚡',color:'#ff7043'},
    {emoji:'💛',text:'Minions speak\nMinionese!',accent:'Banana! Bello! 🍌',color:'#ffee58'},
    {emoji:'🌟',text:'Doraemon has a\nmagic pocket!',accent:'Any gadget you wish for! 🎁',color:'#7c4dff'},
    {emoji:'❤️',text:'SpongeBob lives\nin Bikini Bottom!',accent:'He has the BEST laugh! 😂',color:'#ffca28'},
  ],
  maths:[
    {emoji:'➕',text:'1 + 1 = 2\nYou DID IT!',accent:'Addition makes numbers bigger! 🎉',color:'#7c4dff'},
    {emoji:'🔢',text:'1 2 3 4 5\nCount with me!',accent:'Counting is the FIRST step! ⭐',color:'#00bcd4'},
    {emoji:'🔺🟦⭕',text:'Triangle\nSquare Circle!',accent:'Shapes are EVERYWHERE! 👀',color:'#ff6f00'},
    {emoji:'✖️',text:'2 × 2 = 4\nTimes tables!',accent:'Sing it: Two twos are FOUR! 🎵',color:'#e91e63'},
    {emoji:'🌙⭐',text:'Odd Numbers:\n1 3 5 7 9!',accent:'Can\'t split them in two! 🤔',color:'#673ab7'},
    {emoji:'🍕',text:'Half means\ndivide by 2!',accent:'Half of 4 equals 2! 🍕',color:'#f44336'},
    {emoji:'📏',text:'Measure in\nCentimetres!',accent:'A ruler helps us measure! 📐',color:'#2196f3'},
    {emoji:'🕐',text:'Big hand at 12\nmeans O\'clock!',accent:'Can you read the clock? ⏰',color:'#ff9800'},
    {emoji:'💰',text:'Coins add up\nto make money!',accent:'Learning money is useful! 💵',color:'#4caf50'},
    {emoji:'🔟',text:'Count by 10s:\n10 20 30 40!',accent:'Tens make big numbers easy! 💯',color:'#9c27b0'},
  ],
  stories:[
    {emoji:'🐢',text:'Tortoise WON\nthe Race!',accent:'Slow and steady wins! 💪',color:'#4caf50'},
    {emoji:'🐷🏠',text:'Three Little Pigs\nbuild houses!',accent:'Brick house was STRONGEST! 🧱',color:'#ff6f00'},
    {emoji:'🦁',text:'Lion helped\ntiny Mouse!',accent:'Small friends help too! 💕',color:'#ffd600'},
    {emoji:'🥿✨',text:'Cinderella lost\nher slipper!',accent:'Kindness always wins! 👑',color:'#e91e63'},
    {emoji:'🌱',text:'Jack climbed\nthe Beanstalk!',accent:'Bravery = great adventures! ⚡',color:'#66bb6a'},
    {emoji:'🐣',text:'Ugly Duckling\nbecame a SWAN!',accent:'Never judge by looks! 🦢',color:'#42a5f5'},
    {emoji:'🐺',text:'Little Red Hood\nmet the Wolf!',accent:'Always stay on safe path! 🌲',color:'#8d6e63'},
    {emoji:'🍎',text:'Snow White ate\nthe magic apple!',accent:'Be careful who you trust! ⚠️',color:'#ef5350'},
    {emoji:'🪈',text:'Magic flute led\nrats away!',accent:'Music is powerful! 🎵',color:'#26a69a'},
    {emoji:'🌟',text:'Panchatantra:\nBe wise always!',accent:'Old stories teach best! 📖',color:'#ff6f00'},
  ],
  science:[
    {emoji:'🌤️',text:'Sky is BLUE\nbecause of light!',accent:'Sunlight scatters blue! ☀️',color:'#29b6f6'},
    {emoji:'🌱',text:'Seeds grow into\nbig tall trees!',accent:'Water + Soil + Sunlight! ☀️',color:'#66bb6a'},
    {emoji:'🪐',text:'Solar System\nhas 8 Planets!',accent:'Mercury is closest to Sun! 🌞',color:'#7c4dff'},
    {emoji:'🦖',text:'T-Rex had tiny\nfront arms!',accent:'Dinosaurs: 65 million years ago! 🦴',color:'#ff7043'},
    {emoji:'🌋',text:'Volcanoes shoot\nhot LAVA!',accent:'Lava reaches 1000°C! 🔥',color:'#f44336'},
    {emoji:'🌈',text:'Rainbows have\n7 colours!',accent:'ROYGBIV — say it fast! 🎨',color:'#ff4081'},
    {emoji:'🐘',text:'Elephants\nNEVER forget!',accent:'Best memory in the world! 🧠',color:'#78909c'},
    {emoji:'🌙',text:'Earth spins to\nmake Day & Night!',accent:'One spin = 24 hours! ⏰',color:'#3949ab'},
    {emoji:'❤️',text:'Heart beats\n100,000 times/day!',accent:'Pumps blood everywhere! 💪',color:'#e53935'},
    {emoji:'🍎',text:'GRAVITY pulls\neverything down!',accent:'Newton discovered gravity! 🌍',color:'#43a047'},
  ]
};

const GRADIENTS = {
  cartoon:[['#c026d3','#7c3aed'],['#f97316','#fbbf24'],['#0ea5e9','#8b5cf6'],['#ec4899','#f97316']],
  maths:  [['#4f46e5','#7c3aed'],['#0891b2','#4f46e5'],['#d97706','#dc2626'],['#059669','#0891b2']],
  stories:[['#16a34a','#2563eb'],['#d97706','#dc2626'],['#7c3aed','#16a34a'],['#be185d','#7c3aed']],
  science:[['#0284c7','#7c3aed'],['#059669','#0284c7'],['#dc2626','#d97706'],['#0ea5e9','#10b981']],
};

export function getGradient(cat){const l=GRADIENTS[cat]||GRADIENTS.cartoon;return l[Math.floor(Math.random()*l.length)];}
export function getContent(cat,n){const p=[...(CONTENT[cat]||CONTENT.cartoon)].sort(()=>Math.random()-.5);const r=[];for(let i=0;i<n;i++)r.push(p[i%p.length]);return r;}

// ─── Particle system ─────────────────────────────────────────
const PARTS = Array.from({length:22},()=>({
  x:Math.random()*1080, y:Math.random()*1920,
  r:8+Math.random()*18, speed:1+Math.random()*2,
  drift:(Math.random()-.5)*.7, phase:Math.random()*Math.PI*2,
  shape:Math.floor(Math.random()*3),
  col:['#fff','#ffd600','#ff80ab','#80d8ff','#b9f6ca','#ea80fc'][Math.floor(Math.random()*6)],
}));

function drawStar(ctx,cx,cy,or,ir,n){
  ctx.beginPath();
  for(let i=0;i<n*2;i++){
    const r=i%2===0?or:ir,a=(i*Math.PI)/n-Math.PI/2;
    i===0?ctx.moveTo(cx+r*Math.cos(a),cy+r*Math.sin(a)):ctx.lineTo(cx+r*Math.cos(a),cy+r*Math.sin(a));
  }ctx.closePath();
}
function pill(ctx,x,y,w,h,r){
  r=Math.min(r,w/2,h/2);
  ctx.beginPath();
  ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);
  ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);
  ctx.lineTo(x+r,y+h);ctx.arcTo(x,y+h,x,y+h-r,r);
  ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);ctx.closePath();
}
function wrapText(ctx,text,x,y,maxW,lh){
  text.split('\n').forEach(para=>{
    let line='';
    para.split(' ').forEach(w=>{
      const t=line?line+' '+w:w;
      if(ctx.measureText(t).width>maxW&&line){ctx.fillText(line,x,y);line=w;y+=lh;}else line=t;
    });
    if(line){ctx.fillText(line,x,y);y+=lh;}
    y+=lh*.1;
  });
  return y;
}

// ─── CARTOON CHARACTER DRAWERS ────────────────────────────────

// ── Star Buddy (Cartoon category) ──
function drawStarBuddy(ctx, cx, cy, t) {
  const blink = Math.sin(t * 0.8) > 0.92;
  const wave  = Math.sin(t * 3) * 0.25;
  const jump  = Math.abs(Math.sin(t * 2.5)) * 40;
  cy -= jump;

  ctx.save();
  // Body — big yellow star
  ctx.fillStyle = '#ffd600';
  ctx.shadowColor = 'rgba(255,214,0,0.5)'; ctx.shadowBlur = 40;
  drawStar(ctx, cx, cy, 200, 90, 5);
  ctx.fill();

  // Body shine
  ctx.fillStyle = 'rgba(255,255,255,0.3)';
  drawStar(ctx, cx-30, cy-30, 90, 40, 5);
  ctx.fill();
  ctx.shadowBlur = 0;

  // Rosy cheeks
  ctx.fillStyle = 'rgba(255,100,150,0.5)';
  ctx.beginPath(); ctx.ellipse(cx-80, cy+50, 50, 38, -.3, 0, Math.PI*2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(cx+80, cy+50, 50, 38, .3, 0, Math.PI*2); ctx.fill();

  // Eyes
  if (blink) {
    ctx.strokeStyle = '#1a1a2e'; ctx.lineWidth = 10; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(cx-55, cy+10); ctx.lineTo(cx-25, cy+10); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx+25, cy+10); ctx.lineTo(cx+55, cy+10); ctx.stroke();
  } else {
    ctx.fillStyle = '#1a1a2e';
    ctx.beginPath(); ctx.arc(cx-42, cy+10, 28, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(cx+42, cy+10, 28, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = '#fff';
    ctx.beginPath(); ctx.arc(cx-30, cy+2, 11, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(cx+54, cy+2, 11, 0, Math.PI*2); ctx.fill();
  }

  // Smile
  ctx.strokeStyle = '#1a1a2e'; ctx.lineWidth = 12; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.arc(cx, cy+55, 60, .2, Math.PI-.2); ctx.stroke();

  // Waving arm
  ctx.save();
  ctx.translate(cx+160, cy-20);
  ctx.rotate(wave);
  ctx.strokeStyle = '#ffd600'; ctx.lineWidth = 22;
  ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(80,-60); ctx.stroke();
  ctx.fillStyle = '#ffd600';
  ctx.beginPath(); ctx.arc(80,-60,28,0,Math.PI*2); ctx.fill();
  ctx.restore();

  // Star sparkles around
  ['#fff','#ffd600','#ff80ab'].forEach((c,i)=>{
    const ang = t*2 + i*2.1;
    const sx  = cx + 230*Math.cos(ang), sy = cy+180 + 80*Math.sin(ang);
    ctx.fillStyle = c; ctx.globalAlpha = .7;
    drawStar(ctx, sx, sy, 22, 10, 5); ctx.fill();
  });
  ctx.globalAlpha = 1;
  ctx.restore();
}

// ── Count Robot (Maths category) ──
function drawCountRobot(ctx, cx, cy, t, item) {
  const arm = Math.sin(t * 2.5) * 0.5;
  const blink = Math.sin(t * 0.7) > 0.93;
  cy += 20;
  ctx.save();

  // Shadow
  ctx.fillStyle='rgba(0,0,0,0.15)';
  ctx.beginPath();ctx.ellipse(cx,cy+340,160,40,0,0,Math.PI*2);ctx.fill();

  // Legs
  [[cx-70,cy+280],[cx+70,cy+280]].forEach(([lx,ly])=>{
    ctx.fillStyle='#455a64';
    ctx.fillRect(lx-25,ly,50,100);
    ctx.fillStyle='#37474f';
    ctx.fillRect(lx-35,ly+95,70,35);
  });

  // Body
  const bodyGrad=ctx.createLinearGradient(cx-130,cy+80,cx+130,cy+280);
  bodyGrad.addColorStop(0,'#64b5f6'); bodyGrad.addColorStop(1,'#1565c0');
  ctx.fillStyle=bodyGrad;
  pill(ctx,cx-130,cy+80,260,200,30); ctx.fill();

  // Body shine
  ctx.fillStyle='rgba(255,255,255,0.18)';
  pill(ctx,cx-100,cy+90,120,80,20); ctx.fill();

  // Screen on chest (shows number)
  ctx.fillStyle='#0d1b2a';
  pill(ctx,cx-90,cy+130,180,100,18); ctx.fill();
  ctx.fillStyle='#00e5ff';
  ctx.font='bold 70px Inter,sans-serif'; ctx.textAlign='center';
  const num=item.text.match(/\d+/)?item.text.match(/\d+/)[0]:'42';
  ctx.shadowColor='#00e5ff'; ctx.shadowBlur=20;
  ctx.fillText(num, cx, cy+205);
  ctx.shadowBlur=0;

  // Arms
  ctx.strokeStyle='#455a64'; ctx.lineWidth=40; ctx.lineCap='round';
  // left
  ctx.save();ctx.translate(cx-130,cy+150);ctx.rotate(-0.4+arm);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-100,80);ctx.stroke();
  ctx.fillStyle='#37474f';ctx.beginPath();ctx.arc(-100,80,32,0,Math.PI*2);ctx.fill();
  ctx.restore();
  // right — waving
  ctx.save();ctx.translate(cx+130,cy+150);ctx.rotate(0.4-arm);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(100,80);ctx.stroke();
  ctx.fillStyle='#37474f';ctx.beginPath();ctx.arc(100,80,32,0,Math.PI*2);ctx.fill();
  ctx.restore();

  // Head
  const headGrad=ctx.createLinearGradient(cx-120,cy-140,cx+120,cy+40);
  headGrad.addColorStop(0,'#90caf9'); headGrad.addColorStop(1,'#1976d2');
  ctx.fillStyle=headGrad;
  pill(ctx,cx-115,cy-140,230,210,30); ctx.fill();

  // Antenna
  ctx.strokeStyle='#90caf9';ctx.lineWidth=14;
  ctx.beginPath();ctx.moveTo(cx,cy-140);ctx.lineTo(cx,cy-230);ctx.stroke();
  ctx.fillStyle=Math.sin(t*4)>0?'#ff1744':'#ff8f00';
  ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=20;
  ctx.beginPath();ctx.arc(cx,cy-240,28,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;

  // Face visor
  ctx.fillStyle='#0d1b2a';
  pill(ctx,cx-90,cy-110,180,130,25);ctx.fill();
  ctx.fillStyle='rgba(100,200,255,0.15)';
  pill(ctx,cx-80,cy-100,160,110,20);ctx.fill();

  // Eyes
  if(blink){
    ctx.strokeStyle='#00e5ff';ctx.lineWidth=8;
    ctx.beginPath();ctx.moveTo(cx-55,cy-50);ctx.lineTo(cx-20,cy-50);ctx.stroke();
    ctx.beginPath();ctx.moveTo(cx+20,cy-50);ctx.lineTo(cx+55,cy-50);ctx.stroke();
  } else {
    ctx.fillStyle='#00e5ff';ctx.shadowColor='#00e5ff';ctx.shadowBlur=15;
    ctx.beginPath();ctx.arc(cx-38,cy-50,22,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(cx+38,cy-50,22,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    ctx.fillStyle='#fff';
    ctx.beginPath();ctx.arc(cx-28,cy-58,8,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(cx+48,cy-58,8,0,Math.PI*2);ctx.fill();
  }

  // Floating number bits
  ['+','×','=','2','5'].forEach((s,i)=>{
    const ang=t*1.5+i*1.26;
    const fx=cx+280*Math.cos(ang), fy=cy+100+100*Math.sin(ang);
    ctx.fillStyle='rgba(255,255,255,0.8)';ctx.font='bold 52px Inter,sans-serif';
    ctx.textAlign='center';ctx.fillText(s,fx,fy);
  });
  ctx.restore();
}

// ── Story Wizard (Stories category) ──
function drawWizard(ctx, cx, cy, t) {
  const wave = Math.sin(t*2.5)*0.4;
  const bob  = Math.sin(t*1.8)*20;
  cy += bob;
  ctx.save();

  // Shadow
  ctx.fillStyle='rgba(0,0,0,0.12)';
  ctx.beginPath();ctx.ellipse(cx,cy+390,160,40,0,0,Math.PI*2);ctx.fill();

  // Robe body
  const robeG=ctx.createLinearGradient(cx-150,cy+60,cx+150,cy+400);
  robeG.addColorStop(0,'#6a0dad');robeG.addColorStop(1,'#1a0033');
  ctx.fillStyle=robeG;
  ctx.beginPath();
  ctx.moveTo(cx-150,cy+60);ctx.lineTo(cx+150,cy+60);
  ctx.lineTo(cx+180,cy+400);ctx.lineTo(cx-180,cy+400);ctx.closePath();ctx.fill();

  // Robe stars
  ['#ffd600','#fff','#ea80fc'].forEach((c,i)=>{
    ctx.fillStyle=c; ctx.globalAlpha=.6;
    const sx=cx-100+i*100,sy=cy+150+i*70;
    drawStar(ctx,sx,sy,20,9,6);ctx.fill();
  });ctx.globalAlpha=1;

  // Belt
  ctx.fillStyle='#ffd600';
  ctx.fillRect(cx-130,cy+200,260,28);
  // Belt buckle
  ctx.fillStyle='#ff8f00';
  pill(ctx,cx-28,cy+196,56,36,8);ctx.fill();

  // Arms
  ctx.strokeStyle='#6a0dad';ctx.lineWidth=55;ctx.lineCap='round';
  // left arm
  ctx.save();ctx.translate(cx-130,cy+100);ctx.rotate(.3+wave*.3);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-90,120);ctx.stroke();ctx.restore();
  // right arm — holding wand
  ctx.save();ctx.translate(cx+130,cy+100);ctx.rotate(-.3+wave);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(100,110);ctx.stroke();
  // Wand
  ctx.strokeStyle='#5d4037';ctx.lineWidth=14;
  ctx.beginPath();ctx.moveTo(100,110);ctx.lineTo(180,20);ctx.stroke();
  // Wand tip sparkle
  ctx.fillStyle='#ffd600';ctx.shadowColor='#ffd600';ctx.shadowBlur=40;
  drawStar(ctx,180,20,40,18,5);ctx.fill();ctx.shadowBlur=0;
  // Sparkle particles
  for(let i=0;i<6;i++){
    const a=t*3+i*1.05, r=50+30*Math.sin(t*4+i);
    ctx.fillStyle='rgba(255,214,0,0.8)';
    ctx.beginPath();ctx.arc(180+r*Math.cos(a),20+r*Math.sin(a),6+4*Math.sin(t*5+i),0,Math.PI*2);ctx.fill();
  }
  ctx.restore();

  // Head
  ctx.fillStyle='#ffcc80';
  ctx.shadowColor='rgba(0,0,0,0.3)';ctx.shadowBlur=20;
  ctx.beginPath();ctx.arc(cx,cy,130,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;

  // Beard
  ctx.fillStyle='#e0e0e0';
  ctx.beginPath();ctx.ellipse(cx,cy+80,80,90,.0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#fff';ctx.font='bold 60px serif';ctx.textAlign='center';
  ctx.fillText('~~~~~',cx,cy+130);

  // Eyes
  const blink=Math.sin(t*.9)>.93;
  if(blink){
    ctx.strokeStyle='#4a148c';ctx.lineWidth=10;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(cx-55,cy-15);ctx.lineTo(cx-20,cy-15);ctx.stroke();
    ctx.beginPath();ctx.moveTo(cx+20,cy-15);ctx.lineTo(cx+55,cy-15);ctx.stroke();
  } else {
    ctx.fillStyle='#4a148c';
    ctx.beginPath();ctx.arc(cx-40,cy-20,24,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(cx+40,cy-20,24,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#fff';
    ctx.beginPath();ctx.arc(cx-28,cy-28,9,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(cx+52,cy-28,9,0,Math.PI*2);ctx.fill();
  }

  // Hat base
  ctx.fillStyle='#4a148c';
  ctx.beginPath();ctx.ellipse(cx,cy-120,150,40,0,0,Math.PI*2);ctx.fill();
  // Hat cone
  const hatG=ctx.createLinearGradient(cx,cy-120,cx,cy-450);
  hatG.addColorStop(0,'#6a0dad');hatG.addColorStop(1,'#311b92');
  ctx.fillStyle=hatG;
  ctx.beginPath();ctx.moveTo(cx-140,cy-120);ctx.lineTo(cx+140,cy-120);
  ctx.lineTo(cx+15,cy-450);ctx.lineTo(cx-15,cy-450);ctx.closePath();ctx.fill();
  // Hat stars
  ctx.fillStyle='#ffd600';ctx.globalAlpha=.8;
  [[cx-40,cy-250,18],[cx+60,cy-320,14],[cx-20,cy-390,10]].forEach(([hx,hy,hr])=>{
    drawStar(ctx,hx,hy,hr,hr*.4,5);ctx.fill();
  });ctx.globalAlpha=1;

  ctx.restore();
}

// ── Astro Kid (Science category) ──
function drawAstroKid(ctx, cx, cy, t) {
  const float = Math.sin(t*1.5)*30;
  const wave  = Math.sin(t*2.5)*0.4;
  cy -= 40 + float;
  ctx.save();

  // Planets orbiting
  [{r:280,speed:0.8,size:30,col:'#ff9800'},{r:340,speed:-0.5,size:22,col:'#7c4dff'},{r:200,speed:1.2,size:18,col:'#00bcd4'}].forEach(p=>{
    const ang=t*p.speed;
    ctx.fillStyle=p.col; ctx.globalAlpha=.7;
    ctx.beginPath();ctx.arc(cx+p.r*Math.cos(ang),cy+p.r*Math.sin(ang),p.size,0,Math.PI*2);ctx.fill();
  });ctx.globalAlpha=1;

  // Shadow
  ctx.fillStyle='rgba(0,0,0,0.10)';
  ctx.beginPath();ctx.ellipse(cx,cy+420+float,130,30,0,0,Math.PI*2);ctx.fill();

  // Suit legs
  [[cx-60,cy+270],[cx+60,cy+270]].forEach(([lx,ly])=>{
    ctx.fillStyle='#e0e0e0';ctx.fillRect(lx-30,ly,60,130);
    ctx.fillStyle='#bdbdbd';ctx.fillRect(lx-40,ly+125,80,35);
  });

  // Suit body
  const sg=ctx.createLinearGradient(cx-140,cy+60,cx+140,cy+280);
  sg.addColorStop(0,'#eeeeee');sg.addColorStop(1,'#9e9e9e');
  ctx.fillStyle=sg;
  pill(ctx,cx-140,cy+60,280,220,40);ctx.fill();

  // Suit badge on chest
  ctx.fillStyle='#1565c0'; pill(ctx,cx-55,cy+130,110,80,16);ctx.fill();
  ctx.fillStyle='#fff';ctx.font='bold 46px serif';ctx.textAlign='center';
  ctx.fillText('🚀',cx,cy+190);

  // Arms
  ctx.strokeStyle='#e0e0e0';ctx.lineWidth=50;ctx.lineCap='round';
  ctx.save();ctx.translate(cx-140,cy+120);ctx.rotate(.4+wave*.3);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-110,90);ctx.stroke();
  ctx.fillStyle='#bdbdbd';ctx.beginPath();ctx.arc(-110,90,35,0,Math.PI*2);ctx.fill();
  ctx.restore();
  ctx.save();ctx.translate(cx+140,cy+120);ctx.rotate(-.4+wave);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(110,90);ctx.stroke();
  ctx.fillStyle='#bdbdbd';ctx.beginPath();ctx.arc(110,90,35,0,Math.PI*2);ctx.fill();
  ctx.restore();

  // Helmet outer
  ctx.fillStyle='#b0bec5'; ctx.shadowColor='rgba(0,0,0,0.3)'; ctx.shadowBlur=20;
  ctx.beginPath();ctx.arc(cx,cy,160,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;

  // Visor
  const vg=ctx.createRadialGradient(cx-40,cy-40,10,cx,cy,120);
  vg.addColorStop(0,'rgba(100,200,255,0.9)');vg.addColorStop(0.7,'rgba(0,50,200,0.7)');vg.addColorStop(1,'rgba(0,0,80,0.8)');
  ctx.fillStyle=vg;
  ctx.beginPath();ctx.arc(cx,cy,110,0,Math.PI*2);ctx.fill();

  // Visor shine
  ctx.fillStyle='rgba(255,255,255,0.35)';
  ctx.beginPath();ctx.ellipse(cx-50,cy-50,65,42,-0.6,0,Math.PI*2);ctx.fill();

  // Face inside visor
  const blink=Math.sin(t*.8)>.93;
  if(blink){
    ctx.strokeStyle='#fff';ctx.lineWidth=9;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(cx-45,cy-5);ctx.lineTo(cx-15,cy-5);ctx.stroke();
    ctx.beginPath();ctx.moveTo(cx+15,cy-5);ctx.lineTo(cx+45,cy-5);ctx.stroke();
  } else {
    ctx.fillStyle='rgba(255,255,255,0.9)';
    ctx.beginPath();ctx.arc(cx-32,cy-5,22,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(cx+32,cy-5,22,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(0,50,180,0.9)';
    ctx.beginPath();ctx.arc(cx-32,cy-5,13,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(cx+32,cy-5,13,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#fff';
    ctx.beginPath();ctx.arc(cx-24,cy-12,5,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(cx+40,cy-12,5,0,Math.PI*2);ctx.fill();
  }
  ctx.strokeStyle='rgba(255,255,255,0.8)';ctx.lineWidth=10;
  ctx.beginPath();ctx.arc(cx,cy+35,40,.2,Math.PI-.2);ctx.stroke();

  // Stars scattering around
  for(let i=0;i<8;i++){
    const a=t*.6+i*.78;
    const dx=410*Math.cos(a), dy=150+200*Math.sin(a);
    ctx.fillStyle='rgba(255,255,255,'+(0.5+0.5*Math.sin(t*3+i))+')';
    drawStar(ctx,cx+dx,cy+dy,12,5,5);ctx.fill();
  }
  ctx.restore();
}

// ─── CHARACTER DISPATCHER ─────────────────────────────────────
function drawCharacter(ctx, category, cx, cy, t, item) {
  if (category==='cartoon') drawStarBuddy(ctx,cx,cy,t);
  else if(category==='maths') drawCountRobot(ctx,cx,cy,t,item);
  else if(category==='stories') drawWizard(ctx,cx,cy,t);
  else drawAstroKid(ctx,cx,cy,t);
}

// ─── BACKGROUND ELEMENTS per category ────────────────────────
function drawBg(ctx,category,t,g){
  const W=CANVAS_W,H=CANVAS_H;
  // Animated multi-stop gradient
  const shift=Math.sin(t*.3)*.5;
  const bg=ctx.createLinearGradient(0,0,W*(1+shift),H);
  bg.addColorStop(0,g[0]); bg.addColorStop(0.5,lerpColor(g[0],g[1],.5+.5*Math.sin(t*.5)));
  bg.addColorStop(1,g[1]);
  ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);

  // Big soft radial glow
  const rg=ctx.createRadialGradient(W/2,H*.4,0,W/2,H*.4,700);
  rg.addColorStop(0,'rgba(255,255,255,0.15)');rg.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=rg;ctx.fillRect(0,0,W,H);

  // Moving background shapes per category
  if(category==='cartoon'){
    // Floating clouds
    [[-200,300,1.2],[ 300,600,.9],[400,1400,1.1],[-100,1700,.8]].forEach(([ox,oy,spd],i)=>{
      const x=(ox+t*spd*40)%W, y=oy;
      ctx.fillStyle='rgba(255,255,255,0.12)';ctx.globalAlpha=1;
      ctx.beginPath();ctx.arc(x,y,90,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(x+80,y-30,70,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(x+160,y,80,0,Math.PI*2);ctx.fill();
    });
  } else if(category==='maths'){
    // Grid lines
    ctx.strokeStyle='rgba(255,255,255,0.06)';ctx.lineWidth=2;
    for(let x=0;x<W;x+=120){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
    for(let y=0;y<H;y+=120){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
    // Floating formula symbols
    ['∞','π','∑','√','%'].forEach((s,i)=>{
      const x=((i*210+t*25)%W), y=200+i*320;
      ctx.fillStyle='rgba(255,255,255,0.06)';ctx.font='bold 180px Inter,sans-serif';ctx.textAlign='center';
      ctx.fillText(s,x,y);
    });
  } else if(category==='stories'){
    // Stars in the sky feel
    for(let i=0;i<20;i++){
      const x=(i*70+Math.sin(t+i)*(20+i*5))%W;
      const y=100+i*85;
      const sz=3+5*Math.abs(Math.sin(t*2+i));
      ctx.fillStyle='rgba(255,255,255,'+(0.3+0.3*Math.sin(t*3+i))+')';
      ctx.beginPath();ctx.arc(x,y,sz,0,Math.PI*2);ctx.fill();
    }
    // Moon
    ctx.fillStyle='rgba(255,255,200,0.12)';
    ctx.beginPath();ctx.arc(900,200,120,0,Math.PI*2);ctx.fill();
  } else {
    // Science: orbiting dotted rings
    [300,400,550].forEach((r,i)=>{
      ctx.beginPath();ctx.arc(W/2,H*.38,r,0,Math.PI*2);
      ctx.strokeStyle=`rgba(255,255,255,0.06)`;ctx.lineWidth=2;ctx.stroke();
    });
    // Twinkling stars
    for(let i=0;i<30;i++){
      const x=(i*37+50)%W, y=(i*63)%H;
      const a=0.3+0.7*Math.abs(Math.sin(t*2.5+i));
      ctx.fillStyle=`rgba(255,255,255,${a})`;
      ctx.beginPath();ctx.arc(x,y,2+2*Math.abs(Math.sin(t+i)),0,Math.PI*2);ctx.fill();
    }
  }
}

// ─── MAIN FRAME RENDERER ─────────────────────────────────────
const _parts = PARTS;

export function renderKidsFrame(ctx, item, gradient, t, duration) {
  const W=CANVAS_W, H=CANVAS_H;
  const progress=Math.min(t/duration,1);

  // Background
  drawBg(ctx, item._cat||'cartoon', t, gradient);

  // Confetti particles
  ctx.save();
  for(const p of _parts){
    p.y+=p.speed; p.x+=p.drift+.4*Math.sin(t*1.5+p.phase);
    if(p.y>H+50){p.y=-50;p.x=Math.random()*W;}
    ctx.globalAlpha=.55+.35*Math.sin(t*2+p.phase);
    ctx.fillStyle=p.col;
    ctx.save();ctx.translate(p.x,p.y);ctx.rotate(t*.8+p.phase);
    if(p.shape===0){ctx.beginPath();ctx.arc(0,0,p.r*.45,0,Math.PI*2);ctx.fill();}
    else if(p.shape===1){drawStar(ctx,0,0,p.r*.55,p.r*.25,5);ctx.fill();}
    else{ctx.fillRect(-p.r*.3,-p.r*.3,p.r*.6,p.r*.6);}
    ctx.restore();
  }ctx.globalAlpha=1;ctx.restore();

  // ── Top header (wavy) ──
  ctx.save();
  ctx.fillStyle='rgba(0,0,0,0.30)';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(W,0);ctx.lineTo(W,148);
  for(let x=W;x>=0;x-=18)ctx.lineTo(x,148+22*Math.sin((x/W)*Math.PI*4+t*3));
  ctx.closePath();ctx.fill();
  ctx.fillStyle='#fff';ctx.font='bold 56px Inter,sans-serif';ctx.textAlign='center';
  ctx.shadowColor='rgba(0,0,0,.4)';ctx.shadowBlur=12;
  ctx.fillText('🎨 KidsFlix', W/2, 102);ctx.shadowBlur=0;
  ctx.restore();

  // ── Animated character ──
  drawCharacter(ctx, item._cat||'cartoon', W/2, 560, t, item);

  // ── Speech bubble ──
  const bubbleY = 1080;
  const bW=W-100, bH=200, bX=50, bR=50;
  ctx.save();
  ctx.shadowColor='rgba(0,0,0,0.3)'; ctx.shadowBlur=24;
  ctx.fillStyle='rgba(255,255,255,0.92)';
  pill(ctx,bX,bubbleY,bW,bH,bR); ctx.fill();
  // Tail
  ctx.beginPath();ctx.moveTo(W/2-40,bubbleY);ctx.lineTo(W/2+40,bubbleY);ctx.lineTo(W/2,bubbleY-55);ctx.closePath();ctx.fill();
  ctx.shadowBlur=0;
  // Bubble text
  ctx.fillStyle='#1a1a2e';ctx.font='bold 72px Inter,sans-serif';ctx.textAlign='center';
  wrapText(ctx,item.text,W/2,bubbleY+80,bW-80,82);
  ctx.restore();

  // ── Accent pill ──
  const aY=H*.73, aW=W-80;
  ctx.save();
  ctx.shadowColor='rgba(0,0,0,.3)';ctx.shadowBlur=20;
  ctx.fillStyle='rgba(0,0,0,0.35)';
  pill(ctx,40,aY,aW,138,69);ctx.fill();ctx.shadowBlur=0;
  ctx.strokeStyle='rgba(255,255,255,0.25)';ctx.lineWidth=3;
  pill(ctx,40,aY,aW,138,69);ctx.stroke();
  ctx.fillStyle='#fff';ctx.font='bold 62px Inter,sans-serif';ctx.textAlign='center';
  ctx.shadowColor='rgba(0,0,0,.3)';ctx.shadowBlur=6;
  ctx.fillText(item.accent,W/2,aY+92,aW-60);ctx.shadowBlur=0;
  ctx.restore();

  // ── Bouncing stars row ──
  ctx.save();
  [150,310,540,770,930].forEach((sx,i)=>{
    const sy=H*.87+20*Math.sin(t*3.5+i);
    ctx.font='68px serif';ctx.textAlign='center';ctx.fillText('⭐',sx,sy);
  });ctx.restore();

  // ── Progress bar ──
  const bpW=W-120,bpX=60,bpY=H-295;
  ctx.save();
  ctx.fillStyle='rgba(255,255,255,0.2)';pill(ctx,bpX,bpY,bpW,20,10);ctx.fill();
  const pg=ctx.createLinearGradient(bpX,0,bpX+bpW*progress,0);
  pg.addColorStop(0,'#ffd600');pg.addColorStop(1,'#fff');
  ctx.fillStyle=pg;pill(ctx,bpX,bpY,bpW*progress,20,10);ctx.fill();
  ctx.restore();

  // ── Bottom bar (wavy) ──
  ctx.save();
  ctx.fillStyle='rgba(0,0,0,0.38)';
  ctx.beginPath();ctx.moveTo(0,H);ctx.lineTo(W,H);ctx.lineTo(W,H-220);
  for(let x=W;x>=0;x-=18)ctx.lineTo(x,H-220-24*Math.sin((x/W)*Math.PI*3+t*2.5));
  ctx.closePath();ctx.fill();
  ctx.fillStyle='#fff';ctx.font='bold 56px Inter,sans-serif';ctx.textAlign='center';
  ctx.shadowColor='rgba(0,0,0,.4)';ctx.shadowBlur=8;
  ctx.fillText('KidsFlix • Fun & Learning 🌟',W/2,H-128);ctx.shadowBlur=0;
  ctx.fillStyle='rgba(255,255,255,0.55)';ctx.font='40px Inter,sans-serif';
  ctx.fillText('#KidsShorts  #Educational  #Fun',W/2,H-62);
  ctx.restore();
}

function lerpColor(c1,c2,t){
  const h=s=>parseInt(s.replace('#',''),16);
  const r1=(h(c1)>>16)&255,g1=(h(c1)>>8)&255,b1=h(c1)&255;
  const r2=(h(c2)>>16)&255,g2=(h(c2)>>8)&255,b2=h(c2)&255;
  return `rgb(${Math.round(r1+(r2-r1)*t)},${Math.round(g1+(g2-g1)*t)},${Math.round(b1+(b2-b1)*t)})`;
}

// ─── NURSERY MUSIC ────────────────────────────────────────────
const NOTE={C4:261.63,D4:293.66,E4:329.63,F4:349.23,G4:392,A4:440,B4:493.88,
  C5:523.25,D5:587.33,E5:659.26,F5:698.46,G5:784,A5:880,C3:130.81,D3:146.83,E3:164.81,G3:196,A3:220,_:0};

const MELODIES={
  cartoon:[ ['C4',1],['C4',1],['G4',1],['G4',1],['A4',1],['A4',1],['G4',2],['F4',1],['F4',1],['E4',1],['E4',1],['D4',1],['D4',1],['C4',2] ],
  maths:  [ ['C5',1],['G4',1],['E4',1],['G4',1],['C5',1],['E5',1],['G5',2],['E5',1],['D5',1],['C5',1],['D5',1],['E5',1],['C5',1],['G4',2] ],
  stories:[ ['G4',1.5],['A4',.5],['B4',1],['G4',1],['B4',1],['A4',2],['G4',1.5],['A4',.5],['B4',1],['G4',1],['G4',3] ],
  science:[ ['E5',1],['D5',1],['C5',1],['D5',1],['E5',1],['E5',1],['E5',2],['D5',1],['D5',1],['D5',2],['E5',1],['G5',1],['G5',2] ],
};
const BASS={cartoon:[['C3',2],['G3',2],['A3',2],['F3',2]],maths:[['C3',2],['E3',2],['G3',2],['E3',2]],
  stories:[['G3',3],['D3',3],['C3',3],['G3',3]],science:[['A3',2],['G3',2],['E3',2],['A3',2]]};

export async function generateKidsMusic(category,durationSec){
  // SR=22050 (half of CD quality) — fast to compute, sounds great for kids
  const SR=22050, total=Math.round(durationSec*SR);
  const AC=window.AudioContext||window.webkitAudioContext;
  const ctx=new AC({sampleRate:SR});
  const buf=ctx.createBuffer(2,total,SR);
  const BPM=category==='stories'?80:112;
  const beat=Math.round(SR*60/BPM);
  const mel=MELODIES[category]||MELODIES.cartoon;
  const bass=BASS[category]||BASS.cartoon;
  const THIRD=Math.pow(2,4/12);

  function synth(data,start,freq,dur,vol,type){
    if(!freq||start>=total)return;
    const end=Math.min(start+dur,total);
    const att=Math.floor(SR*.018),rel=Math.floor(dur*.2);
    const TAU=2*Math.PI;
    for(let i=start;i<end;i++){
      const idx=i-start,t=idx/SR;
      const env=idx<att?idx/att:idx>end-start-rel?(end-i)/rel:1;
      // Pure sine for bass, slight harmonics for bell (kids clarity)
      const s=type==='bass'?Math.sin(TAU*freq*t)
             :Math.sin(TAU*freq*t)*.75+Math.sin(TAU*freq*2*t)*.15;
      data[i]=(data[i]||0)+s*env*vol;
    }
  }
  for(let ch=0;ch<2;ch++){
    const d=buf.getChannelData(ch);
    let s=0,mi=0;
    while(s<total){const[n,b]=mel[mi%mel.length];synth(d,s,NOTE[n]||0,Math.round(b*beat),.30,'bell');s+=Math.round(b*beat);mi++;}
    s=0;let bi=0;
    while(s<total){const[n,b]=bass[bi%bass.length];synth(d,s,NOTE[n]||0,Math.round(b*beat),.20,'bass');s+=Math.round(b*beat);bi++;}
    // Soft limiter
    for(let i=0;i<total;i++)d[i]=Math.tanh(d[i]*1.6)*.75;
  }
  await ctx.close();return buf;
}

// ─── RECORD VIDEO — fast mode ────────────────────────────────
// Uses captureStream(0) + requestFrame() + setTimeout(0) loop
// This bypasses the 60Hz rAF throttle → ~5-8x faster encoding
export function recordKidsVideo(canvas,item,gradient,durationSec,musicBuffer){
  return new Promise(async resolve=>{
    const fps=30, totalFrames=Math.round(durationSec*fps);
    const BATCH=8; // render N frames per event-loop tick
    let frame=0;

    // Audio
    const AC=window.AudioContext||window.webkitAudioContext;
    const actx=new AC({sampleRate:22050});
    const dest=actx.createMediaStreamDestination();
    let src=null;
    if(musicBuffer){
      src=actx.createBufferSource();src.buffer=musicBuffer;src.loop=true;
      const gain=actx.createGain();gain.gain.value=.8;
      src.connect(gain);gain.connect(dest);src.start(0);
    }

    // captureStream(0) = manual frame control (no rAF lock)
    const vs=canvas.captureStream(0);
    const vt=vs.getVideoTracks()[0]; // we push frames manually
    const combined=new MediaStream();
    vs.getVideoTracks().forEach(t=>combined.addTrack(t));
    if(musicBuffer)dest.stream.getAudioTracks().forEach(t=>combined.addTrack(t));

    const chunks=[];
    let mime='video/webm;codecs=vp9,opus';
    if(!MediaRecorder.isTypeSupported(mime))mime='video/webm;codecs=vp8,opus';
    if(!MediaRecorder.isTypeSupported(mime))mime='video/webm';
    const rec=new MediaRecorder(combined,{mimeType:mime,videoBitsPerSecond:4000000});
    rec.ondataavailable=e=>{if(e.data.size>0)chunks.push(e.data);};
    rec.onstop=()=>{
      if(src){try{src.stop();}catch(e){}}
      actx.close();
      resolve(new Blob(chunks,{type:'video/webm'}));
    };
    rec.start();

    const c2d=canvas.getContext('2d');
    function tick(){
      // Render a batch of frames without yielding — fast!
      const end=Math.min(frame+BATCH,totalFrames);
      while(frame<end){
        renderKidsFrame(c2d,item,gradient,frame/fps,durationSec);
        vt.requestFrame(); // push each frame immediately
        frame++;
      }
      if(frame>=totalFrames){rec.stop();return;}
      setTimeout(tick,0); // yield to browser briefly, then continue
    }
    tick();
  });
}

// ─── BATCH GENERATE ───────────────────────────────────────────
export async function generateBatch(canvas,category,count,durationSec,onProgress){
  const items=getContent(category,count).map(it=>({...it,_cat:category}));
  const grads=items.map(()=>getGradient(category));
  onProgress({phase:'music',current:0,total:count});
  let music=null;
  try{music=await generateKidsMusic(category,Math.min(durationSec,10));}catch(e){console.warn('Music failed:',e);}
  const results=[];
  for(let i=0;i<count;i++){
    onProgress({phase:'video',current:i+1,total:count,text:items[i].text});
    const blob=await recordKidsVideo(canvas,items[i],grads[i],durationSec,music);
    results.push({id:Date.now()+i,item:items[i],gradient:grads[i],blob,category});
  }
  onProgress({phase:'done',current:count,total:count});
  return results;
}

// ─── PREVIEW SNAPSHOT ─────────────────────────────────────────
export function renderPreview(canvas,item,gradient){
  const ctx=canvas.getContext('2d');
  renderKidsFrame(ctx,{...item,_cat:item._cat||'cartoon'},gradient,2.8,12);
}
