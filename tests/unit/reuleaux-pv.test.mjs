// The Reuleaux Platonic Solids in Polyhedraverse (DICTO 2026-10-23; DICTO's idea, paper #45): one body data serves the K Reuleaux world
// and the Polyhedraverse family (the film file holds no body, corners or faces); the shapes' names are the world's (rl.name.*) in every
// language; their previews are the seams; and Soft draws each body once, the same at every softness.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import FILM from '../../src/app/reuleaux-data.js';
import { REULEAUX_KEYS } from '../../src/app/world-reuleaux.js';
import { POLYHEDRA, REULEAUX_RAW, REULEAUX_ADDITION_IDS, reuleauxId } from '../../src/krp-core/src/polyhedra/index.js';
import { polyShapeName, polyShapeEdges } from '../../src/app/poly-shapes.js';
import { t } from '../../src/app/i18n.js';
import { puffedFor } from '../../src/app/soft-finish.js';

const LANGS = ['en', 'ja', 'es', 'fr', 'ko', 'zh', 'ru'];

test('one body data: the film file keeps no body, the world and Polyhedraverse read krp-core', () => {
  for (const B of FILM.bodies) for (const k of ['body', 'corners', 'faces', 'side']) assert.equal(B[k], undefined, `${B.key}.${k} only in krp-core`);
  assert.deepEqual(REULEAUX_RAW.map((B) => B.key), REULEAUX_KEYS);
  assert.deepEqual(REULEAUX_ADDITION_IDS, REULEAUX_KEYS.map(reuleauxId));
});

test('names as the Reuleaux world gives them, in every language; credit and curved-face words in every language', () => {
  for (const key of REULEAUX_KEYS) for (const L of LANGS) {
    const name = polyShapeName(reuleauxId(key), L);
    assert.equal(name, t(`rl.name.${key}`, L));
    assert.ok(name && !name.startsWith('rl.'), `${key} ${L}`);
  }
  assert.equal(polyShapeName('REULEAUX_CUBE', 'en'), 'Reuleaux cube');
  for (const L of LANGS) {
    const credit = t('pv.detail.reuleaux', L, { solid: 'x' });
    assert.ok(credit.includes('#45') && credit.includes('10.5281/zenodo.23529499') && credit.includes('DICTO'), L);
    assert.ok(t('poly.d.curvedFaces', L, { k: 3 }).includes('3'), L);
    for (const k of ['soft.title', 'soft.flat', 'soft.soft', 'soft.plain', 'soft.metallic', 'soft.ceramic', 'soft.amount']) assert.ok(!t(k, L).startsWith('soft.'), `${k} ${L}`);
  }
});

test('previews: the seams (the creases), not straight corner-to-corner edges', () => {
  for (const id of REULEAUX_ADDITION_IDS) {
    const e = polyShapeEdges(id);
    assert.equal(e.length, POLYHEDRA[id].curved.seams.length / 6);
    assert.ok(e.length > POLYHEDRA[id].edges.length * 4, 'arcs sampled finely');
  }
});

test('Soft: a curved body is one geometry at every softness, its faces its patches', () => {
  for (const id of REULEAUX_ADDITION_IDS) {
    const a = puffedFor(id, POLYHEDRA[id], 0), b = puffedFor(id, POLYHEDRA[id], 0.5);
    assert.equal(a, b);
    assert.equal(a.attributes.position.count, POLYHEDRA[id].curved.index.length);
    assert.equal(Math.max(...a.userData.faceIds), POLYHEDRA[id].faces.length - 1);
  }
  // a flat shape is puffed per softness
  assert.notEqual(puffedFor('CUBE', POLYHEDRA.CUBE, 0), puffedFor('CUBE', POLYHEDRA.CUBE, 0.3));
});
