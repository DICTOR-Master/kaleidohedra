// Roof-fold cell: a cube of edge 2 centred at the origin, the regular
// dodecahedron made by putting Euclid's roofs on it, and the regular
// icosahedron made by reflecting the 12 roof vertices back through the cube
// faces. Copies at every translation by 2 along x, y, z form the structure;
// each roof vertex then lands on a neighbouring cell's icosahedron vertex.
// Three-free; exact claims are checked by scripts/verify-roof-fold.mjs.

export const PHI = (1 + Math.sqrt(5)) / 2;
export const ROOF_FOLD_PERIOD = 2;

const cyc = (a, b) => [[0, a, b], [a, b, 0], [b, 0, a]];
const SIGNS = [[1, 1], [1, -1], [-1, 1], [-1, -1]];

export const fold = (x) => 1 - Math.abs((((x + 1) % 4) + 4) % 4 - 2);

export function roofFoldCell() {
  const cube = [];
  for (const x of [1, -1]) for (const y of [1, -1]) for (const z of [1, -1]) cube.push([x, y, z]);
  const roof = SIGNS.flatMap(([s, t]) => cyc(s / PHI, t * PHI));
  const ico = roof.map((v) => v.map(fold));
  const dodeca = [...cube, ...roof];
  return {
    cube,
    dodeca,
    ico,
    cubeEdges: edgesOfLength(cube, 2),
    dodecaEdges: edgesOfLength(dodeca, 2 / PHI),
    icoEdges: edgesOfLength(ico, 2 / PHI ** 2),
    nodes: [[1, 1, 1], ...ico],
  };
}

export function edgesOfLength(verts, length, tol = 1e-9) {
  const out = [];
  for (let i = 0; i < verts.length; i++) {
    for (let j = i + 1; j < verts.length; j++) {
      if (Math.abs(Math.hypot(...verts[i].map((c, k) => c - verts[j][k])) - length) < tol) out.push([i, j]);
    }
  }
  return out;
}
