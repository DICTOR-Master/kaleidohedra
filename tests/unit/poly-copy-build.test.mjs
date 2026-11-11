// Copy build (src/app/poly-build-record.js): the record of a hemi RD with two pieces attached, placed exactly as the app places
// them (krp-core faceAttach). Parents and faces agree with the joins; every attached face of a child lies on its parent's face
// in world coordinates (each corner on a corner, within 1e-9); the turn as stored gives the corners; the JSON round-trips.
import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { POLYHEDRA } from '../../src/krp-core/src/polyhedra/index.js';
import { facesCongruent } from '../../src/krp-core/src/polyhedra/core.js';
import { faceAttachOptions } from '../../src/krp-core/src/assembly/faceAttach.js';
import { describeAssembly } from '../../src/krp-core/src/assembly/assemblyNaming.js';
import { buildRecord, hasAttached } from '../../src/app/poly-build-record.js';

const HEMI = 'RVCMG_RD_HEMI';
const matrixOf = (n) => new THREE.Matrix4().compose(new THREE.Vector3(...n.transform.position), new THREE.Quaternion(...n.transform.quaternion), new THREE.Vector3(1, 1, 1));
function attach(nodes, connections, i, fi, id) {
  const n = nodes[i], T = POLYHEDRA[n.shape], S = POLYHEDRA[id];
  const inc = S.faces.map((_, k) => k).filter((k) => S.faces[k].length === T.faces[fi].length && facesCongruent(T.vertices, T.faces[fi], S.vertices, S.faces[k]));
  const o = faceAttachOptions(T, fi, matrixOf(n), S, inc)[0];
  assert.ok(o, `${id} on ${n.shape} face ${fi}`);
  const node = { id: `n${nodes.length + 1}`, shape: id, transform: { position: o.position.toArray(), quaternion: o.quaternion.toArray() } };
  nodes.push(node);
  connections.push({ nodeA: n.id, vertexA: fi, nodeB: node.id, vertexB: o.incomingFaceIndex, kind: 'face' });
}

function hemiBuild() {
  const nodes = [{ id: 'n1', shape: HEMI, transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }], connections = [];
  const S = POLYHEDRA[HEMI];
  const hex = S.faces.findIndex((f) => f.length === 6), rh = S.faces.findIndex((f) => f.length === 4);
  attach(nodes, connections, 0, hex, HEMI);   // hemi on hemi's hexagon: the whole RD
  attach(nodes, connections, 1, rh, HEMI);    // a third on a rhombus of the second (parent 1, not the root)
  return { nodes, connections };
}

test('a hemi RD with two attached pieces: parents and faces follow the joins', () => {
  const { nodes, connections } = hemiBuild();
  const caption = describeAssembly(nodes, connections);
  const r = buildRecord(nodes, connections, POLYHEDRA, caption);
  assert.equal(r.app, 'Polyhedraverse');
  assert.equal(r.version, 1);
  assert.equal(r.caption, caption);
  assert.match(caption, /RD-Hemi \(bare\) \+ 2× face-attached RD-Hemi \(bare\)/);
  assert.equal(r.pieces.length, 3);
  assert.deepEqual(r.pieces.map((p) => p.i), [0, 1, 2]);
  assert.deepEqual(r.pieces.map((p) => p.solid), [HEMI, HEMI, HEMI]);
  assert.deepEqual(r.pieces.map((p) => p.parent), [null, 0, 1]);
  assert.equal(r.pieces[0].parentFace, undefined);
  connections.forEach((c, k) => {
    const p = r.pieces[k + 1];
    assert.equal(p.join, 'face');
    assert.equal(p.parentFace, c.vertexA);
    assert.equal(p.face, c.vertexB);
  });
  assert.equal(hasAttached(nodes, connections), true);
  assert.equal(hasAttached(nodes.slice(0, 1), []), false);
});

test('every attached face of a child lies on its parent face in world coordinates (1e-9)', () => {
  const { nodes, connections } = hemiBuild();
  const r = buildRecord(nodes, connections, POLYHEDRA, describeAssembly(nodes, connections));
  for (const p of r.pieces) {
    if (p.parent == null) continue;
    const par = r.pieces[p.parent];
    const mine = p.faces[p.face].map((k) => p.vertices[k]), theirs = par.faces[p.parentFace].map((k) => par.vertices[k]);
    assert.equal(mine.length, theirs.length);
    for (const a of mine) {
      const d = Math.min(...theirs.map((b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2])));
      assert.ok(d < 1e-9, `piece ${p.i} face ${p.face} corner off its parent's face ${p.parentFace} by ${d}`);
    }
  }
});

test('the turn as stored gives the world corners, faces are the shape\'s own, and the JSON round-trips exactly', () => {
  const { nodes, connections } = hemiBuild();
  const r = buildRecord(nodes, connections, POLYHEDRA, 'x');
  for (const p of r.pieces) {
    const q = new THREE.Quaternion(...p.turn.quaternion), t = new THREE.Vector3(...p.turn.position);
    POLYHEDRA[p.solid].vertices.forEach((v, k) => {
      const w = new THREE.Vector3(...v).applyQuaternion(q).add(t);
      assert.ok(w.distanceTo(new THREE.Vector3(...p.vertices[k])) < 1e-12);
    });
    assert.deepEqual(p.faces, POLYHEDRA[p.solid].faces.map((f) => [...f]));
    assert.deepEqual(p.turn.quaternion, nodes[p.i].transform.quaternion);
  }
  assert.deepEqual(JSON.parse(JSON.stringify(r)), r);
});

test('a corner join is recorded as one', () => {
  const nodes = [{ id: 'a', shape: 'CUBE', transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }, { id: 'b', shape: 'D4', transform: { position: [2, 2, 2], quaternion: [0, 0, 0, 1] } }];
  const r = buildRecord(nodes, [{ nodeA: 'a', vertexA: 3, nodeB: 'b', vertexB: 1, kind: 'vertex' }], POLYHEDRA, 'c');
  assert.deepEqual([r.pieces[1].parent, r.pieces[1].join, r.pieces[1].parentCorner, r.pieces[1].corner], [0, 'corner', 3, 1]);
});
