// The theorem block's exact bond sizes (dictonic-theorem.js, from study 2026-10-25-bond-relay) agree with the app's own web of
// bonds (webOf over the pieces the world draws) at sample points of both loops, and the per-kind bond types match.
import test from 'node:test';
import assert from 'node:assert/strict';
import { BOND_AREAS } from '../../src/app/dictonic-theorem.js';
import { DICTONIC_VIEWS } from '../../src/app/world-dictonic.js';

const PHI = (1 + Math.sqrt(5)) / 2;
// distinct sizes (two kinds may share one size, e.g. big–big = small–small at Kelvin), compared to 1e-7
const distinct = (xs) => xs.filter((a) => a > 1e-9).sort((a, b) => a - b).reduce((d, a) => (d.length && a - d[d.length - 1] < 1e-7 ? d : [...d, a]), []);
const same = (a, b, msg) => { assert.equal(a.length, b.length, msg); a.forEach((v, i) => assert.ok(Math.abs(v - b[i]) < 1e-7, `${msg}: ${v} vs ${b[i]}`)); };
const sizesOf = (web) => distinct(web.map((w) => w[2]));
const exact = (o) => distinct(Object.values(o));
test('golden bond sizes = exact formulas', () => {
  for (const x of [0.3, 1, PHI, 1 / PHI, 3]) same(sizesOf(DICTONIC_VIEWS.golden.web(2, { param: x })), exact(BOND_AREAS.golden(x)), `x = ${x}`);
});
test('Delian bond sizes = exact formulas', () => {
  for (const t of [0.1, 0.25, 1 / 3, 0.47, 0.8]) same(sizesOf(DICTONIC_VIEWS.delian.web(2, { param: t })), exact(BOND_AREAS.delian(t)), `t = ${t}`);
});
test('the octet is the one Delian point with a single bond kind and both pieces', () => {
  for (let i = 1; i < 100; i++) { const t = i / 100, n = Object.values(BOND_AREAS.delian(t)).filter((a) => a > 1e-12).length; assert.equal(n, 2, `t = ${t}`); }
  assert.equal(Object.values(BOND_AREAS.delian(1 / 3)).filter((a) => a > 1e-12).length, 1);
});
