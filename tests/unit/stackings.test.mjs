// The Stackings World (DICTO 2026-10-26; src/app/stackings-geometry.js): the pieces it computes equal paper #57's exact volumes
// (k-research studies/2026-10-25-stackings/appendix.json) for the pure and mixed stackings at λ inside every stretch; each column fills
// its period exactly; octahedral halves follow the rule of halves; and the census corollary (studies/2026-10-26-rule-of-halves-census)
// holds: the tetrahedral / octahedral split of space depends only on the hexagonality.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { PRESETS, validWord, layerTypes, stackingPieces, census, LAM_LO, LAM_HI } from '../../src/app/stackings-geometry.js';

const R2 = Math.SQRT2;
// #57 appendix volumes (exact), by stretch: tet c / tet h, oct cc / hh / mixed (c over h = h over c)
const STRETCHES = [
  [-11 / 24, -3 / 8, { tetC: () => 0, tetH: (l) => (R2 * (24 * l + 11) ** 3) / 6144, octCC: () => R2 / 2, octHH: (l) => (-R2 * (13824 * l ** 3 + 19008 * l ** 2 + 8712 * l - 205)) / 3072,
    octMix: (l) => (-R2 * (13824 * l ** 3 + 19008 * l ** 2 + 8712 * l - 1741)) / 6144 }],
  [-3 / 8, -1 / 8, { tetC: (l) => (R2 * (8 * l + 3) ** 3) / 96, tetH: (l) => (R2 * (24 * l + 11) ** 3) / 6144, octCC: (l) => (-R2 * (512 * l ** 3 + 576 * l ** 2 + 216 * l + 3)) / 48,
    octHH: (l) => (-R2 * (13824 * l ** 3 + 19008 * l ** 2 + 8712 * l - 205)) / 3072, octMix: (l) => (-R2 * (46592 * l ** 3 + 55872 * l ** 2 + 22536 * l - 13)) / 6144 }],
  [-1 / 8, 5 / 24, { tetC: (l) => (R2 * (512 * l ** 3 - 576 * l ** 2 + 216 * l + 69)) / 384, tetH: (l) => (-R2 * (1536 * l ** 3 + 5184 * l ** 2 - 3384 * l - 1013)) / 6144,
    octCC: (l) => (-R2 * (8 * l - 3) ** 3) / 192, octHH: (l) => (R2 * (1536 * l ** 3 + 5184 * l ** 2 - 3384 * l + 523)) / 3072, octMix: (l) => (-R2 * (6656 * l ** 3 - 14400 * l ** 2 + 6840 * l - 955)) / 6144 }],
  [5 / 24, 3 / 8, { tetC: (l) => (R2 * (512 * l ** 3 - 576 * l ** 2 + 216 * l + 69)) / 384, tetH: (l) => (R2 * (8 * l + 1) * (64 * l ** 2 - 80 * l + 37)) / 256,
    octCC: (l) => (-R2 * (8 * l - 3) ** 3) / 192, octHH: (l) => (-R2 * (8 * l - 3) ** 3) / 128, octMix: (l) => (-5 * R2 * (8 * l - 3) ** 3) / 768 }],
];
const close = (a, b, msg) => assert.ok(Math.abs(a - b) < 1e-7, `${msg}: ${a} vs ${b}`);

test('presets are valid words with the expected h/c sequences', () => {
  for (const w of Object.values(PRESETS)) assert.ok(validWord(w), w);
  assert.deepEqual(layerTypes('ABC'), ['c', 'c', 'c']);
  assert.deepEqual(layerTypes('AB'), ['h', 'h']);
  assert.deepEqual(layerTypes('ABAC'), ['c', 'h', 'c', 'h']);
  assert.ok(!validWord('AAB') && !validWord('ABA') && !validWord('A'));
});

for (const word of ['ABC', 'AB', 'ABAC', 'ABCACB', 'ABACACBCB']) {
  test(`${word}: every piece has #57's exact volume; the column fills its period`, () => {
    const types = layerTypes(word), n = word.length;
    for (const [lo, hi, V] of STRETCHES) for (const f of [0.3, 0.7]) {
      const l = lo + f * (hi - lo), P = stackingPieces(word, l);
      close(P.reduce((s, p) => s + p.volume, 0), (n * R2) / 2, `${word} λ=${l} column`);
      for (const p of P.filter((q) => q.role === 'tet')) close(p.volume, p.type === 'c' ? V.tetC(l) : V.tetH(l), `${word} λ=${l} tet ${p.type}`);
      for (let k = 0; k < n; k++) {   // the octahedral piece of gap k: bottom half (layer k) + top half (layer k+1)
        const v = P.filter((q) => q.role !== 'tet' && q.gap === k).reduce((s, q) => s + q.volume, 0), b = types[k], t = types[(k + 1) % n];
        close(v, b === t ? (b === 'c' ? V.octCC(l) : V.octHH(l)) : V.octMix(l), `${word} λ=${l} oct gap ${k} (${b} below, ${t} above)`);
      }
    }
  });
}

test('rule of halves: a half depends only on its own layer', () => {
  for (const l of [-0.4, -0.25, 0, 0.1, 0.3]) {
    const half = (word, role, type) => stackingPieces(word, l).find((p) => p.role === role && p.type === type)?.volume ?? 0;
    for (const role of ['octBottom', 'octTop']) {
      close(half('ABAC', role, 'c'), half('ABC', role, 'c'), `λ=${l} ${role} c`);
      close(half('ABAC', role, 'h'), half('AB', role, 'h'), `λ=${l} ${role} h`);
    }
  }
});

test('census: the space split depends only on the hexagonality, not the order', () => {
  // valid words of length 8 starting with A; two with the same number of h layers but different hh neighbour pairs (h/c counts only)
  const words = [];
  const grow = (w) => { if (w.length === 8) { if (validWord(w)) words.push(w); return; } for (const x of 'ABC') if (x !== w[w.length - 1]) grow(w + x); };
  grow('A');
  const key = (w) => { const t = layerTypes(w); return [t.filter((x) => x === 'h').length, t.filter((x, k) => x === 'h' && t[(k + 1) % t.length] === 'h').length]; };
  let w1, w2;
  for (const a of words) { for (const b of words) { const [ha, pa] = key(a), [hb, pb] = key(b); if (ha === hb && pa !== pb) { w1 = a; w2 = b; break; } } if (w1) break; }
  assert.ok(w1 && w2, 'found two orders with equal hexagonality');
  for (const l of [LAM_LO + 0.03, -0.25, 0, 0.3, LAM_HI - 0.01]) close(census(w1, l).octShare, census(w2, l).octShare, `λ=${l} ${w1} vs ${w2}`);
});
