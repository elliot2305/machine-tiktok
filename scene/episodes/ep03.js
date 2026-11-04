// Ép 3 – Michel savait tout (pop-rock) – confessionnal
const P = (x, z, o = {}) => ({ pos: [x, z], ...o });
export default {
  bpm: 128, set: 'confessionnal',
  cast: ['patate', 'michel'],
  events: [
    { t: 0, set: { set: 'confessionnal', patate: P(0, 1.0, { mood: 'angry', armsUp: true }), michel: P(0, -0.4, { y: 0.5, look: 'patate', mood: 'shock' }), shake: 1, shakeT: 0, drama: 1 } },
    { t: 10.6, set: { drama: 0, patate: P(-0.8, 1.0, { look: 'michel', mood: 'angry' }), michel: P(0.5, -0.4, { y: 0.5, look: 'patate' }) } },
    { t: 17.2, set: { frite: { pos: [-0.25, 1.4, 1.3] } } },
    { t: 21.2, set: { patate: P(-0.8, 1.0, { look: 'michel', armsUp: true }), shake: 1, shakeT: 21.2 } },
    { t: 28.1, set: { patate: undefined, frite: { pos: [0.35, 1.5, 0.2] }, michel: P(0, -0.4, { y: 0.5, look: undefined, flap: true }) } },
    { t: 31.6, set: { michel: P(0, -0.4, { y: 0.5, flap: true, talk: true }), singer: 'michel' } },
    { t: 34.8, set: { michel: P(0, -0.4, { y: 0.5, mood: 'sus', talk: true }), frite: undefined, drama: 1 } },
    { t: 38.4, set: { singer: 'patate', drama: 0, patate: P(-0.35, 0.6, { mood: 'angry', armsUp: true, look: 'michel' }), michel: P(0.3, -0.2, { y: 0.5, hop: true, flap: true, mood: 'shock', look: 'patate' }), shake: 1, shakeT: 38.4 } },
    { t: 42.9, set: { patate: P(-0.8, 1.0, { look: 'michel', cry: true }), michel: P(0.5, -0.4, { y: 0.5, look: 'patate' }) } },
    { t: 53.7, set: { patate: P(-0.8, 1.0, { look: 'michel', armsUp: true, mood: 'angry' }), shake: 1, shakeT: 53.7 } },
    { t: 58.5, set: { patate: undefined, michel: P(0, -0.4, { y: 0.5, mood: 'sus' }), singer: 'michel', drama: 1, spokenBy: 'MICHEL' } },
  ],
  shots: [
    { t: 0, from: [0, 1.7, 5.0], to: [0, 1.65, 4.3], look: [0, 1.75, 0.3], dur: 1.4, fov: 42 },
    { t: 5.2, from: [0.4, 1.4, 3.0], to: [0.2, 1.45, 2.6], aim: 'patate', aimDy: 0.1, dur: 5, fov: 40 },
    { t: 10.6, from: [0, 1.9, 6.0], to: [0, 1.7, 5.2], look: [0, 1.1, 0.2], dur: 6 },
    { t: 17.2, from: [0.9, 1.8, 2.6], to: [0.8, 1.8, 2.0], aim: 'michel', aimDy: 0.3, dur: 4, fov: 34 },
    { t: 21.2, from: [-0.2, 1.4, 3.4], to: [-0.5, 1.5, 3.0], aim: 'patate', aimDy: 0.15, dur: 1, fov: 44 },
    { t: 24.5, from: [0, 2.4, 6.4], to: [0, 2.0, 5.4], look: [0, 1.2, 0.2], dur: 4 },
    { t: 28.1, from: [0, 1.75, 2.8], to: [0, 1.75, 2.3], aim: 'michel', aimDy: 0.35, dur: 6, fov: 34 },
    { t: 34.8, from: [0, 1.8, 2.2], to: [0, 1.8, 1.7], aim: 'michel', aimDy: 0.4, dur: 3.6, fov: 30 },
    { t: 38.4, from: [0.8, 1.4, 3.2], to: [0.4, 1.4, 2.8], look: [0, 1.3, 0.2], dur: 4, fov: 40, shake: 0.4 },
    { t: 42.9, from: [0, 1.9, 6.0], to: [0, 1.7, 5.2], look: [0, 1.1, 0.2], dur: 4 },
    { t: 46.5, from: [-1.6, 1.4, 3.0], to: [-1.2, 1.4, 2.6], aim: 'patate', dur: 3, fov: 38 },
    { t: 49.6, from: [1.2, 1.7, 2.6], to: [0.9, 1.7, 2.2], aim: 'michel', aimDy: 0.3, dur: 4, fov: 36 },
    { t: 53.7, from: [0, 2.4, 6.4], to: [0, 2.0, 5.4], look: [0, 1.2, 0.2], dur: 4.8, shake: 0.3 },
    { t: 58.5, from: [0, 1.8, 2.4], to: [0, 1.8, 1.6], aim: 'michel', aimDy: 0.4, dur: 3, fov: 30 },
  ],
  stamps: [
    { t: 10.8, text: 'BALANCE !', d: 1.2 },
    { t: 34.9, text: 'UN SECRET ?!', d: 1.6, rot: 5 },
  ],
  lowers: [
    { t: 11.5, text: 'MICHEL · MEILLEUR AMI (SOI-DISANT)' },
    { t: 28.4, text: 'CONFESSIONNAL · MICHEL CRAQUE' },
  ],
  flashes: [10.6, 21.2, 28.1, 38.4, 53.7, 58.5],
};
