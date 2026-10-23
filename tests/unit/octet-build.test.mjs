// The buildable Icosahedral Octet Lattice (DICTO 2026-10-13) builds exactly the octet: growing from one cell over its face
// neighbours reaches every piece of the octet world's network view (size 2), with the same roles, in all seven versions (the
// simple cubic ones with the pieces their cells share: Tricaps and AXE, DICTO 2026-10-23).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cellAt, neighbours, buildPieces, OCTET_BUILD_KINDS } from '../../src/app/world-octet-build.js';
import { OCTET_VIEWS } from '../../src/app/world-octet.js';

const key = (V) => V.map((p) => p.map((c) => c.toFixed(4)).join(',')).sort().join(';');
for (const kind of OCTET_BUILD_KINDS) {
  test(`building the ${kind} octet gives its network, piece for piece`, () => {
    const want = new Map(OCTET_VIEWS[kind].views.network(2).map(([r, V]) => [key(V), r]));
    const seen = new Set(['0,0,0']), queue = [[0, 0, 0]], built = [];
    while (queue.length) {
      const q = queue.shift();
      if (!cellAt(kind, q).pieces.every(([, V]) => want.has(key(V)))) continue;
      built.push(q);
      for (const n of neighbours(kind, q)) if (!seen.has(n.join())) { seen.add(n.join()); queue.push(n); }
    }
    const got = new Map(buildPieces(kind, built).map(([r, V]) => [key(V), r]));
    assert.equal(got.size, want.size);
    for (const [k, r] of got) assert.equal(want.get(k), r);
  });
}
