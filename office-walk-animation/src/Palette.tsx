/**
 * Palette.tsx — 16-bit limited colour palette shared across all components.
 * All colours hand-picked for a retro SNES/GBA RPG feel.
 */

export const PAL = {
  // Sky sunset gradient stops
  skyTop:    '#12022a',
  skyMid:    '#6b1808',
  skyOrange: '#c43e14',
  skyYellow: '#f5900f',
  sunYellow: '#ffe04d',

  // Office environment
  ceil:      '#1a1230',
  ceilLight: '#fff8c0',
  wall:      '#1e1636',
  wallStripe:'#261e42',

  // Window
  winFrame:  '#7a5230',
  winGlass:  '#3a6aaa',
  winSky:    '#5588cc',
  winCloud:  '#c4d8f0',

  // Floor
  floor:     '#3c2410',
  floorLine: '#503018',
  floorShine:'#5a3820',

  // Furniture
  desk:      '#5c3a18',
  deskTop:   '#7a5228',
  monitor:   '#080814',
  screen:    '#0a24cc',
  screenLine:'#2244ff',
  plant:     '#1a7a1e',
  plantDark: '#104e12',
  pot:       '#8b4513',
  potDark:   '#5a2d0c',
  wb:        '#e8e8dc',
  wbFrame:   '#7a7a7a',
  wbBar1:    '#3399ff',
  wbBar2:    '#ff4444',
  wbBar3:    '#44cc44',

  // Character
  skin:      '#f5c090',
  skinSh:    '#c88a60',
  hair:      '#3d1e00',
  shirt:     '#1555bb',
  shirtSh:   '#0a3388',
  tie:       '#cc1a1a',
  tieHi:     '#ff4444',
  trouser:   '#28374a',
  trouserSh: '#18242e',
  shoe:      '#0a0a0a',
  paper:     '#f0f0d8',
  paperLine: '#c8c8b0',

  // HUD
  hudBg:     '#010810',
  hudBorder: '#2255aa',
  hudBorderHi:'#44aaff',
  hudText:   '#e8f0ff',
  hudSub:    '#6688bb',
  heartFull: '#ff2244',
  heartSh:   '#990020',
  heartEmpty:'#2a0c14',
  xpFill:    '#22ee44',
  xpBg:      '#0a1e0e',
  xpBorder:  '#44bb66',
  taskText:  '#ffdd44',

  // Crowd
  crowd:   ['#cc3344','#3355cc','#33aa44','#cc8822','#882299','#44aaaa','#cc4422'],
  crowdSh: ['#881a22','#182288','#1a6624','#885500','#4a1166','#1a6666','#882200'],
  signBg:   '#f5f0d8',
  signBrd:  '#8b7050',
  goColor:  '#cc2200',
  oopsColor:'#ff7700',

  // Effects
  minus:    '#ff2244',
  minusBg:  '#1a0008',
  black:    '#000000',
  white:    '#ffffff',
  transparent: 'none',
};

/** Scale factor: 1 art pixel = S×S real pixels */
export const S = 6;
