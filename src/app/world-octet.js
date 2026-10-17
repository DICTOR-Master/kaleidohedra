// DICTO Icosahedral Octet (DICTO 2026-10-13; DISCOVERIES #21): Euclid's roofs moved to the icosahedron, as networks that grow with a
// Size slider, on the shared layered-world engine (Pull apart, Crystal, X-ray). Cells from src/app/octet-data.js (built and checked by
// scripts/build-octet-data.py; site rules checked by studies/2026-10-10-icosa-networks-3/octet-sites-check.py). Names by DICTO:
// Admiral Cap, Weirdstone, Tadpole, Frog Chorus, Lotus Jewel. Words: i18n octet.*.
// OCD networks (DICTO 2026-10-18; research studies/2026-10-18-ocd-octet): the Ogdoecontahedron in the octahedron of its 8 joint hexagons,
// keyed by its golden-envelope corners ("Octet with OCD"), and with a Penrose core on every edge ("Octet with OCD and Penrose cores",
// DICTO's name). Cells from src/app/ocd-octet-data.js (scripts/build-ocd-octet-data.py), already in this world's frame.
import OCTET from './octet-data.js';
import OCD_OCTET from './ocd-octet-data.js';
import { createLayeredWorld } from './world-chains.js';

const { a: A, phi: PHI } = OCTET;
const C = { ...OCTET.cells, ...OCD_OCTET.cells };
const KINDS = ['caps', 'allIco', 'frog', 'pyrochlore', 'lotusJewel', 'ocdOctet', 'ocdPenrose'];
const range = (k) => Array.from({ length: 2 * k + 1 }, (_, i) => i - k);
const near = (p, r) => Math.hypot(...p) <= r + 1e-9;
// One cell at a place, or turned inside out through its middle (the octet's other tetrahedra).
const put = (cell, t, invert = false, role = null) => cell.map(([r, V, F, E]) => [typeof role === 'function' ? role(r) : role ?? r,
  V.map((v) => v.map((x, i) => (invert ? -x : x) + t[i])), invert ? F.map((f) => [...f].reverse()) : F, ...(E ? [E] : [])]);
// Octahedra at (a/2)n, n with even sum; corners of the truss at odd sum; tetrahedra at (a/4)s, s odd, turned when sum(s) = 1 mod 4.
function octSites(r) {
  const out = [], k = Math.ceil(r / (A / 2));
  for (const x of range(k)) for (const y of range(k)) for (const z of range(k)) {
    const p = [x, y, z].map((c) => (c * A) / 2);
    if (near(p, r)) out.push({ p, even: (x + y + z) % 2 === 0 });
  }
  return out;
}
function tetSites(r) {
  const out = [], k = Math.ceil(r / (A / 4)) | 1;
  const odd = range(k).filter((c) => Math.abs(c) % 2 === 1);
  for (const x of odd) for (const y of odd) for (const z of odd) {
    const p = [x, y, z].map((c) => (c * A) / 4);
    if (near(p, r)) out.push({ p, s: [x, y, z], invert: (((x + y + z) % 4) + 4) % 4 === 1 });
  }
  return out;
}
// Pyrochlore inside the octet: one tetrahedron of each turn at every corner, mirror images through it (1 in 8 of the tetrahedra).
export const pyro = (s) => [[1, 1, 1], [3, 3, 3]].some((b) => { const d = s.map((c, i) => c - b[i]); return d.every((c) => ((c % 4) + 4) % 4 === 0) && d.reduce((t, c) => t + c / 4, 0) % 2 === 0; });
const R = (size) => size * (A / 2) * 1.01;
const network = (tetCell, octCell = 'oct', turned = null) => (size) => [
  ...octSites(R(size)).filter((o) => o.even).flatMap((o) => put(C[octCell], o.p)),
  ...tetSites(R(size)).flatMap((t) => put(C[tetCell], t.p, t.invert, t.invert ? turned : null)),
];
export const OCTET_VIEWS = {
  caps: { maxSize: 4, views: { network: network('tet'), cell: [...put(C.oct, [0, 0, 0]), ...put(C.tet, [A / 4, A / 4, A / 4])] } },
  allIco: { maxSize: 3, views: { network: network('tetIco'), octahedron: put(C.oct, [0, 0, 0]), tetrahedron: put(C.tetIco, [0, 0, 0]) } },
  frog: { maxSize: 2, views: {
    network: (size) => [
      ...octSites(R(size)).filter((o) => o.even).flatMap((o) => put(C.oct.slice(0, 1), o.p)),
      ...tetSites(R(size)).flatMap((t) => put(C.tetIco.slice(0, 1), t.p, t.invert)),
      ...octSites(R(size)).filter((o) => !o.even).flatMap((o) => put(C.frog, o.p)),
    ],
    star: put(C.frog, [0, 0, 0]),
  } },
  pyrochlore: { maxSize: 4, views: {
    network: (size) => {
      const r = R(size) * 2;
      return [
        ...octSites(r).filter((o) => o.even).flatMap((o) => put(C.oct, o.p, false, 'octGlass')),
        ...tetSites(r).flatMap((t) => (pyro(t.s) ? put(C.tet, t.p, t.invert, t.invert ? 'pyroDown' : 'pyroUp') : put(C.tet, t.p, t.invert, 'tetGlass'))),
      ];
    },
    alone: (size) => tetSites(R(size) * 2).filter((t) => pyro(t.s)).flatMap((t) => put(C.tet, t.p, t.invert, t.invert ? 'pyroDown' : 'pyroUp')),
  } },
  ocdOctet: { maxSize: 3, views: { network: network('ocdTet', 'ocdOct'), cell: [...put(C.ocdOct, [0, 0, 0]), ...put(C.ocdTet, [A / 4, A / 4, A / 4])] } },
  // the turned tetrahedra (the octet's other tetrahedra) are the mirror images here: teal
  ocdPenrose: { maxSize: 3, views: {
    network: network('ocdTetPenrose', 'ocdOctPenrose', (r) => (r === 'ocdTetL' ? 'ocdTetR' : r)),
    cell: [...put(C.ocdOctPenrose, [0, 0, 0]), ...put(C.ocdTetPenrose, [A / 4, A / 4, A / 4]), ...put(C.ocdTetPenrose, [-A / 4, -A / 4, -A / 4], true, (r) => (r === 'ocdTetL' ? 'ocdTetR' : r))],
  } },
  lotusJewel: { maxSize: 3, views: {
    network: (size) => {
      const out = [], k = size, r = size * PHI * 1.01;
      for (const x of range(k)) for (const y of range(k)) for (const z of range(k)) {
        const p = [x, y, z].map((c) => c * PHI);
        if (near(p, r)) out.push(...put(C.lotusJewel, p));
        const q = p.map((c) => c + PHI / 2);
        if (near(q, r)) out.push(...put(C.voidDodeca, q));
      }
      return out;
    },
    jewel: put(C.lotusJewel, [0, 0, 0]),
  } },
};
const DATA = OCTET_VIEWS;
const GLASS = { ocdOctet: new Set(['ocdCapPlain']), ocdPenrose: new Set(['ocdCap', 'midRest']), caps: new Set(['ico']), allIco: new Set(['ico', 'icoSmall']), frog: new Set(['ico', 'icoSmall']), pyrochlore: new Set(['octGlass', 'tetGlass']), lotusJewel: new Set(['voidDodeca']) };

export function createOctetWorld({ scene, fitView }) {
  return createLayeredWorld({ scene, fitView, name: 'octet', data: DATA, kinds: KINDS, glassRoles: GLASS, prefix: 'octet',
    defaultParts: { caps: 'network', allIco: 'network', frog: 'network', pyrochlore: 'network', lotusJewel: 'network', ocdOctet: 'network', ocdPenrose: 'network' } });
}

/** Points whose convex hull previews a network in the DICTO menu (one cell). */
export function octetPreviewPoints(kind) {
  const first = { caps: C.oct, allIco: C.tetIco, frog: C.oct.slice(0, 1), pyrochlore: C.tet, lotusJewel: C.lotusJewel, ocdOctet: C.ocdOct.slice(0, 1), ocdPenrose: C.ocdOct.slice(0, 1) }[kind] ?? [];
  return first.flatMap((p) => p[1]);
}
