// The Hexagonality Law panel (DICTO 2026-10-29, decisions 1A–5A; src/app/hexlaw-panel.js, hexlaw-data.js): seven papers, every
// buildable dot's word has its own h, every dot of a law line with no scatter in the source lies on it (#66, #71a, #74), and a dot
// of a standard polytype opens that polytype, whatever the rotation of its word.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { LAW_CHARTS } from '../../src/app/hexlaw-data.js';
import { LAW_PAPERS, hexShare, chartSvg } from '../../src/app/hexlaw-panel.js';
import { presetOf, setWord, currentWord, resetLayers } from '../../src/app/world-stackings.js';

test('seven papers, ten charts', () => {
  assert.deepEqual(LAW_PAPERS, [66, 68, 70, 71, 72, 73, 74]); assert.equal(LAW_CHARTS.length, 10);
});
test('every buildable dot sits at its own word\'s h', () => {
  for (const c of LAW_CHARTS) for (const s of c.series) for (const p of s.points) if (p.word) {
    const [n, d] = hexShare(p.word); assert.ok(Math.abs(n / d - p.h) < 1e-6, `${c.key} ${p.label}`);
  }
});
test('exact laws: the dots lie on the line', () => {
  for (const key of ['c66', 'c71a', 'c74']) for (const s of LAW_CHARTS.find((c) => c.key === key).series) for (const p of s.points) {
    const [[x0, y0], [x1, y1]] = s.line; assert.ok(Math.abs(y0 + ((p.h - x0) * (y1 - y0)) / (x1 - x0) - p.y) < 1e-5, `${key} ${p.label}`);
  }
});
test('standard polytypes are found in any rotation; other stackings build into the kind on show', () => {
  assert.equal(presetOf('ABCB'), '4H'); assert.equal(presetOf('ABABCBCAC'), '9R'); assert.equal(presetOf('ABCBAB'), null);
  assert.ok(setWord('3C', 'ABCBAB')); assert.equal(currentWord('3C'), 'ABCBAB'); assert.deepEqual(hexShare('ABCBAB'), [2, 3]);
  assert.ok(!setWord('3C', 'ABBA')); resetLayers('3C'); assert.equal(currentWord('3C'), 'ABC');
});
test('every chart draws, with the gold ring only on h charts', () => {
  for (const c of LAW_CHARTS) { const s = chartSvg(c, [1, 2], 'en'); assert.ok(s.startsWith('<svg')); assert.equal(s.includes('law-own'), c.x === 'h' && c.key !== 'c73b'); }
});
