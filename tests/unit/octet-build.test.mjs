// The buildable Icosahedral Octet Lattice (DICTO 2026-10-13) builds exactly the octet: growing from one cell over its face
// neighbours reaches every piece of the octet world's network view (size 2), with the same roles, in all five versions.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cellAt, neighbours, OCTET_BUILD_KINDS } from '../../src/app/world-octet-build.js';
import { OCTET_VIEWS } from '../../src/app/world-octet.js';

const key = (V) => V.map((p) => p.map((c) => c.toFixed(4)).join(',')).sort().join(';');
for (const kind of OCTET_BUILD_KINDS) {
  test(`building the ${kind} octet gives its network, piece for piece`, () => {
    const want = new Map(OCTET_VIEWS[kind].views.network(2).map(([r, V]) => [key(V), r]));
    const seen = new Set(['0,0,0']), queue = [[0, 0, 0]], got = new Map();
    while (queue.length) {
      const q = queue.shift();
      const pcs = cellAt(kind, q).pieces;
      if (!pcs.every(([, V]) => want.has(key(V)))) continue;
      for (const [r, V] of pcs) got.set(key(V), r);
      for (const n of neighbours(kind, q)) if (!seen.has(n.join())) { seen.add(n.join()); queue.push(n); }
    }
    assert.equal(got.size, want.size);
    for (const [k, r] of got) assert.equal(want.get(k), r);
  });
}
