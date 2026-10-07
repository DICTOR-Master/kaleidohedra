// Checks src/geometry-extensions/nets.js: every solid's net lies flat
// with no two faces overlapping, each face hinged to its parent on a
// shared edge, and folding it all the way closes it back into the solid
// exactly; half-folded, every face keeps its shape (a rigid turn).
import { netOf, netSteps, SOLIDS, EKP_PIECES, EKP_ORDER, apply, mul, hullOf } from '../src/geometry-extensions/nets.js';
import { roofFoldSolids, ROOF_FOLD_KINDS, expandedWindows, EXPANDED_WINDOWS_GOLDEN } from '../src/geometry-extensions/roof-fold.js';

const EKP = roofFoldSolids();

// A solid with assembly siblings (the EKP cell's stella octangula, star
// spike + icosahedron, Pacioli's rectangles): true if another SOLIDS
// entry shares its `assembly` tag or either names the other in
// `assemblyWith` (direct finding, 2026-10-07: two different solids each
// land their net's own fold at their own canonical placement, so without
// a correction, two congruent pieces — stella's two tetrahedra — folded
// identically and rendered as one coincident shape, not an interlocking
// pair).
const hasSiblings = (id) => Object.keys(SOLIDS).some((o) => o !== id
  && ((SOLIDS[id].assembly && SOLIDS[o].assembly === SOLIDS[id].assembly) || (SOLIDS[id].assemblyWith ?? []).includes(o) || (SOLIDS[o].assemblyWith ?? []).includes(id)));

let failures = 0;
function check(label, ok, extra = '') {
  console.log(`${ok ? 'OK  ' : 'FAIL'} ${label}${extra ? `  (${extra})` : ''}`);
  if (!ok) failures++;
}
const near = (a, b, e = 1e-6) => Math.abs(a - b) < e;
const dist = (a, b) => Math.hypot(...a.map((v, i) => v - b[i]));
for (const id of Object.keys(SOLIDS)) {
  const net = netOf(id, 5);
  const F = net.faces.length;
  const flat = net.at(0).map((M, i) => net.faces[i].pts.map((p) => apply(M, p)));
  check(`${net.label}: ${F} faces, all flat on the screen at t = 0`, flat.every((P) => P.every((p) => near(p[2], 0))));
  check(`${net.label}: no two faces of the flat net overlap`, net.overlapCount === 0);
  const T1 = net.at(1);
  // Folded: each face back in its place on the solid (up to the one rigid
  // placement of the first face), so shared edges meet.
  const M0 = T1[net.tree.order[0]];
  const closed = net.faces.every((f, i) => f.pts.every((p) => dist(apply(T1[i], p), apply(M0, p)) < 1e-6));
  check(`${net.label}: folded (t = 1) it closes into the solid`, closed);
  if (hasSiblings(id)) {
    // Composed with net.align, folded (t = 1) must land back on this
    // solid's own true vertices exactly (not just some congruent copy of
    // them), the property an assembly's pieces share a frame by.
    const trueT = T1.map((Ti) => mul(net.align, Ti));
    const onTrueVerts = net.faces.every((f, i) => f.pts.every((p) => dist(apply(trueT[i], p), p) < 1e-6));
    check(`${net.label}: aligned, it folds onto its own true vertices (an assembly sibling)`, onTrueVerts);
  }
  if (EKP_PIECES[id]) {
    // An EKP piece, aligned and scaled to cell units, lands on its own
    // corners in the cell (roof-fold.js), so all of them fold into one whole.
    const { kind, index, cell } = EKP_PIECES[id];
    const faces = kind === 'stella' ? EKP.stella.faces.slice(4 * index, 4 * index + 4) : kind === 'rects' ? [EKP.rects.faces[index]] : kind === 'star' ? [...EKP.star.faces.slice(0, 3), EKP.ico.faces[0]] : EKP[kind].faces;
    const corners = faces.flat();
    const s = cell / net.scale;
    const landed = net.faces.flatMap((f, i) => f.pts.map((p) => apply(mul(net.align, T1[i]), p).map((x) => x * s)));
    check(`${net.label}: folded into the EKP cell's frame, on the ${kind}'s own corners`, landed.every((p) => corners.some((q) => dist(p, q) < 1e-6)) && corners.every((q) => landed.some((p) => dist(p, q) < 1e-6)));
  }
  const T5 = net.at(0.5);
  const rigid = net.faces.every((f, i) => f.pts.every((p, j) => f.pts.every((q, k) => near(dist(apply(T5[i], p), apply(T5[i], q)), dist(p, q)))));
  const hinged = net.tree.order.slice(1).every((i) => {
    const node = net.tree.nodes[i];
    const P = node.parent;
    // The hinge's ends sit on both faces at every fold.
    return [0, 0.3, 0.7, 1].every((t) => { const T = net.at(t); return [node.a, node.a.map((v, d) => v + node.d[d] * 5)].every((q) => dist(apply(T[i], q), apply(T[P], q)) < 1e-6); });
  });
  check(`${net.label}: half folded, faces keep their shape and stay hinged`, rigid && hinged);
  // Every face's outline is complete once built: each of its sides is an
  // edge it owns or its hinge to its parent (the parent's).
  const has = (list, a, b) => list.some(([p, q]) => (dist(p, a) < 1e-9 && dist(q, b) < 1e-9) || (dist(p, b) < 1e-9 && dist(q, a) < 1e-9));
  const closedOutlines = net.faces.every((f, i) => f.pts.every((a, j) => {
    const b = f.pts[(j + 1) % f.pts.length];
    const parent = net.tree.nodes[i].parent;
    return has(net.owned[i], a, b) || (parent >= 0 && has(net.owned[parent], a, b));
  }));
  check(`${net.label}: every face's outline is complete once built`, closedOutlines);
  const steps = netSteps(net);
  const edges = steps.flatMap((s) => s.edges);
  const sides = net.faces.reduce((s, f) => s + f.pts.length, 0);
  // Every step's edge is a real edge of the solid: its length matches one
  // of the lengths the solid's own faces actually have (most solids have
  // only one; the EKP assembly pieces have two, a short and a long).
  const realLengths = [...new Set(net.faces.flatMap((f) => f.pts.map((p, i) => dist(p, f.pts[(i + 1) % f.pts.length]))).map((d) => Math.round(d * 1e6)))];
  const isRealEdge = (a, b) => realLengths.some((d) => near(dist(a, b), d / 1e6));
  check(`${net.label}: the build follows the net, first face by sides then a face a tap (${steps.length} taps), every edge n`, steps.length === net.faces[net.tree.order[0]].pts.length + F - 1 && edges.length === sides - (F - 1) && edges.every(([a, b]) => isRealEdge(a, b)));
}
check(`EKP wrap order ${EKP_ORDER.join(', ')} follows ROOF_FOLD_KINDS`, EKP_ORDER.length === Object.keys(EKP_PIECES).length && EKP_ORDER.every((id, i) => i === 0 || ROOF_FOLD_KINDS.indexOf(EKP_PIECES[EKP_ORDER[i - 1]].kind) <= ROOF_FOLD_KINDS.indexOf(EKP_PIECES[id].kind)) && EKP_ORDER[0] === 'pacioli1' && EKP_ORDER.at(-1) === 'dodeca');
// Buildable (study 10a): the expanded windows at the golden push unfold into a flat net, no two faces overlapping.
{
  const V = [];
  for (const f of expandedWindows(EXPANDED_WINDOWS_GOLDEN)) for (const p of f) if (!V.some((q) => dist(p, q) < 1e-9)) V.push(p);
  const net = netOf({ label: 'Expanded windows', make: () => hullOf(V) }, 5);
  const T1 = net.at(1), M0 = T1[net.tree.order[0]];
  const closes = net.faces.every((f, i) => f.pts.every((p) => dist(apply(T1[i], p), apply(M0, p)) < 1e-6));
  check(`expanded windows (study 10a): a flat net of all ${net.faces.length} faces, no overlaps, folds closed (${netSteps(net).length} taps)`, net.faces.length === 74 && net.overlapCount === 0 && closes);
}
console.log(`\n${failures} failure${failures === 1 ? '' : 's'}.`);
process.exit(failures ? 1 : 0);
