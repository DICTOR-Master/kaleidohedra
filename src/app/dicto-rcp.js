// RCP v4 (DICTO's adjusted RCP, DICTO 2026-10-31, to try out beside the RCP view): the RCP perspective with the eye beyond the FAR side instead of on
// the seed's side. Polyhedraverse's 4D builds get it from krp-core (rcpBuild.js, buildRcpComplex eyeSide 'far'); the Queens world
// draws its exact model with these helpers. Plain functions, no three.js.

/** The RMS distance of points from their centre: a cell's size, as krp-core's vertex-first build matches the seed. */
export function rmsSize(P) {
  const c = P[0].map((_, i) => P.reduce((s, p) => s + p[i], 0) / P.length);
  return Math.sqrt(P.reduce((s, p) => s + p.reduce((t, x, i) => t + (x - c[i]) ** 2, 0), 0) / P.length);
}

/**
 * 4D points V seen from beyond the far side: w = V[i][0] (the axis through the seed, the seed at +w), the eye at w = −d with
 * d = margin × r, each point (frame · x) / (d + w); then the whole scaled by one factor so the seed cells (lists of indices into V)
 * keep their true 4D size. frame: three 4-vectors, the picture's x, y, z.
 */
export function farEyePoints(V, r, seedCells, frame, margin = 5) {
  const d = margin * r, P = V.map((x) => frame.map((f) => f.reduce((s, c, i) => s + c * x[i], 0) / (d + x[0])));
  const k = seedCells.reduce((s, c) => s + rmsSize(c.map((i) => V[i])), 0) / seedCells.reduce((s, c) => s + rmsSize(c.map((i) => P[i])), 0);
  return P.map((p) => p.map((x) => x * k));
}
