// A fresh start (DICTO's rule, app audit 2026-10-22): the pure parts of the "Continue where you left off / Start fresh" check.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildOf, listsEmpty, sameStores, asksItself } from '../../src/app/fresh-start.js';

test('a build is compared without names, dates and versions', () => {
  const a = { worldName: 'Rhombiverse', version: 1, cells: { '0,0,0': { material: 'stone' } }, meta: { createdAt: 'x', lastModified: 'y' } };
  const b = { worldName: 'Other', version: 2, cells: { '0,0,0': { material: 'stone' } }, meta: {} };
  assert.equal(buildOf(a), buildOf(b));
  assert.notEqual(buildOf(a), buildOf({ ...b, cells: {} }));
  assert.notEqual(buildOf({ view: { mix: 'DI' } }), buildOf({ view: { mix: '' } }));
});
test('empty piece lists hold nothing; a world snapshot is not judged by them', () => {
  assert.equal(listsEmpty({ worldName: 'BCC Lattice', cells: {}, meta: {} }), true);
  assert.equal(listsEmpty({ pieces: {} }), true);
  assert.equal(listsEmpty({ cells: { '0,0,0': {} } }), false);
  assert.equal(listsEmpty({ nodes: [], connections: [], view: {} }), true);
  assert.equal(listsEmpty({ version: 2, view: { mix: 'D' } }), false, 'no lists: compare it');
});
test('one space asks once; kits and polytopes ask themselves', () => {
  assert.equal(sameStores(['main', 'bcc'], ['bcc', 'main']), true);
  assert.equal(sameStores(['worldpoly'], ['main']), false);
  assert.equal(sameStores(['main'], null), false);
  assert.equal(sameStores([], []), false);
  assert.equal(asksItself('tool:polyKit:antonius.block'), true);
  assert.equal(asksItself('tool:polytope:CUBE|TESSERACT'), true);
  assert.equal(asksItself('tool:platonicMixWorld'), false);
  assert.equal(asksItself(null), false);
});
