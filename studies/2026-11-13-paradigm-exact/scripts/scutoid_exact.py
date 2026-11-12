"""Chapter 5, Theorems 5.3 (the polar flip) and 5.4 (the cycle) made exact, in Q(sqrt5). Source: studies/2026-11-10-scutoid-linear-layer
(scutoid_sphere.py, scutoid_polar.py, scutoid_cycle.py: floating point, faces flat to 1e-13). Here every corner is exact, every
statement is decided in exact arithmetic; floating point only PROPOSES which corners share a facet of a large hull (scipy), and each
proposed facet is then verified exactly (supporting plane, closed surface: every edge on exactly two facets, Euler number 2).
Usage: python scutoid_exact.py [flip|all]   (flip = pilot: the polar part only)
 A. Solids: TI, ID, TD (standard coordinates in Q(sqrt5)); polars PD = TI°, RT = ID°, TK = TD° computed exactly; PD° = TI, TK° = TD.
 B. Theorem 5.3: every polar corner on a 5-fold or 3-fold ray; RT's 30 faces are rhombi (5,3,5,3); over each rhombus PD has the two
    triangles folded along the 3-3 diagonal, TK the two folded along the 5-5 diagonal (the flip); each side plane through the centre
    and two neighbouring rays is a mirror of the symmetry group (it maps the 32 rays to themselves). Shell PD (1) < TK (1.55) (5-fold
    radii), RT at 1.25 between: 30 cells = cone over a rhombus between PD and TK, side faces flat (exact coplanarity), equal volumes,
    equal distance multisets, sum = V(TK) - V(PD).
 C. Theorem 5.4: the scutoid move TI -> TD and its reverse TD -> TI, built as shells S (TI 1 -> ID 1.18 -> TD 1.42, circumradii to
    six digits) and A (TD -> ID -> TI at lam = 71/45 = 1.5778), every half-cell = the convex hull of its two end faces, its facets
    exactly the faces of the construction (so every face is flat), 64 half-cells per shell with pairwise disjoint interiors, inside
    the outer solid and outside the core, volumes adding exactly to the shell: each shell is filled exactly once. The move goes
    'across' (the new edge lies between the two cells that did not touch). Nesting TI < TD < lam TI, PD < TK < mu PD (mu = 155/86)
    exact: the onions fill space but the centre."""
import sys, os, itertools, time
from fractions import Fraction as F
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q5 import Q5, PHI, v, add, sub, mul, dot, cross, det3, iszero, parallel_same, centroid, Body, disjoint, facets, order_face, hull_volume
import numpy as np
from scipy.spatial import ConvexHull
MODE = sys.argv[1] if len(sys.argv) > 1 else 'all'
t0 = time.time(); fails = []
def check(ok, what):
    print(('ok   ' if ok else 'FAIL ') + what, flush=True)
    if not ok: fails.append(what)
def evenperm(p):
    out = []
    for a, b, c in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        for s in itertools.product([1, -1], repeat=3): out.append(v(s[0] * p[a], s[1] * p[b], s[2] * p[c]))
    return list(dict.fromkeys(out))
f = lambda p: np.array([[float(x) for x in q] for q in p])
class Solid:
    """corners (exact) and facets (proposed by a float hull, each verified exactly), faces ordered counter-clockwise from outside"""
    def __init__(self, P, name):
        self.P = list(dict.fromkeys(P)); self.name = name; h = ConvexHull(f(self.P)); groups = {}
        for simp, eq in zip(h.simplices, h.equations): groups.setdefault(tuple(np.round(eq, 7)), set()).update(int(i) for i in simp)
        self.F = []
        for g in groups.values():
            g = sorted(g); a, b = self.P[g[0]], self.P[g[1]]
            c = next(self.P[k] for k in g[2:] if not iszero(cross(sub(b, a), sub(self.P[k], a))))
            nr = cross(sub(b, a), sub(c, a)); d = dot(nr, a)
            if any(dot(nr, p) > d for p in self.P): nr = tuple(-x for x in nr); d = -d
            assert all(dot(nr, p) <= d for p in self.P), 'proposed facet is not a supporting plane'
            on = [k for k in range(len(self.P)) if dot(nr, self.P[k]) == d]
            self.F.append((nr, d, order_face(self.P, on, nr)))
        E = Counter(frozenset((fc[k], fc[(k + 1) % len(fc)])) for _, _, fc in self.F for k in range(len(fc)))
        closed = all(n == 2 for n in E.values()) and len(self.P) - len(E) + len(self.F) == 2
        self.E = list(E); self.closed = closed
    def kinds(self): return dict(sorted(Counter(len(fc) for _, _, fc in self.F).items()))
    def volume(self):
        c = centroid(self.P); return sum((det3(sub(self.P[fc[0]], c), sub(self.P[fc[k]], c), sub(self.P[fc[k + 1]], c)) for _, _, fc in self.F for k in range(1, len(fc) - 1)), Q5(0)) / 6
    def contains(self, x, strict=False): return all((dot(nr, x) < d) if strict else (dot(nr, x) <= d) for nr, d, _ in self.F)
    def scaled(self, k): return Solid([mul(k, p) for p in self.P], self.name)
    def polar(self, name): return Solid([mul(Q5(1) / d, nr) for nr, d, _ in self.F], name)
TI = Solid(evenperm((0, 1, 3 * PHI)) + evenperm((1, 2 + PHI, 2 * PHI)) + evenperm((PHI, 2, 2 * PHI + 1)), 'TI')
ID = Solid(evenperm((0, 0, PHI)) + evenperm((F(1, 2), PHI / 2, PHI * PHI / 2)), 'ID')
TD = Solid(evenperm((0, 1 / PHI, 2 + PHI)) + evenperm((1 / PHI, PHI, 2 * PHI)) + evenperm((PHI, 2, PHI + 1)), 'TD')
AX = [nr for nr, d, fc in TI.F]                                       # the 32 rays: 12 five-fold (pentagons), 20 three-fold (hexagons)
AXK = [5 if len(fc) == 5 else 3 for _, _, fc in TI.F]
def axis_of(x): return next(i for i, a in enumerate(AX) if parallel_same(a, x))
def align(S):                                                          # same icosahedral frame as TI (swap x, y if needed)
    if all(any(parallel_same(nr, a) for a in AX) for nr, _, _ in S.F): return S
    S2 = Solid([(p[1], p[0], p[2]) for p in S.P], S.name); assert all(any(parallel_same(nr, a) for a in AX) for nr, _, _ in S2.F); return S2
ID, TD = align(ID), align(TD)
for S, n, k in [(TI, 60, {5: 12, 6: 20}), (ID, 30, {3: 20, 5: 12}), (TD, 60, {3: 20, 10: 12})]:
    check(S.closed and len(S.P) == n and S.kinds() == k, f'{S.name}: {len(S.P)} corners, faces {S.kinds()}, closed surface, Euler 2 (exact facets)')
PD, RT, TK = TI.polar('PD'), ID.polar('RT'), TD.polar('TK')
for S, k in [(PD, {3: 60}), (RT, {4: 30}), (TK, {3: 60})]:
    check(S.closed and len(S.P) == 32 and S.kinds() == k, f'{S.name}: 32 corners, faces {S.kinds()} (exact polar)')
check(set(PD.polar('x').P) == set(TI.P) and set(TK.polar('x').P) == set(TD.P), 'bipolar: PD° = TI and TK° = TD exactly (the polar swaps of the square)')
print('PROGRESS 0.10 solids and polars exact', flush=True)

# ---------------- B: the polar flip (Theorem 5.3)
ray = {S.name: {axis_of(p): p for p in S.P} for S in (PD, RT, TK)}
check(all(len(r) == 32 for r in ray.values()), 'every corner of PD, RT and TK lies on one of the 32 rays (12 five-fold, 20 three-fold)')
def axset(S, fc): return frozenset(axis_of(S.P[i]) for i in fc)
rh = []
for nr, d, fc in RT.F:
    ax = [axis_of(RT.P[i]) for i in fc]; kinds = [AXK[a] for a in ax]
    if kinds[0] == 3: ax = ax[1:] + ax[:1]; kinds = kinds[1:] + kinds[:1]
    sq = [dot(sub(RT.P[fc[k]], RT.P[fc[(k + 1) % 4]]), sub(RT.P[fc[k]], RT.P[fc[(k + 1) % 4]])) for k in range(4)]
    rh.append((tuple(ax), kinds == [5, 3, 5, 3] and len(set(sq)) == 1))
check(len(rh) == 30 and all(ok for _, ok in rh), 'RT: 30 rhombi (equal sides, exact), corners alternately on five-fold and three-fold rays')
PDf = {axset(PD, fc) for _, _, fc in PD.F}; TKf = {axset(TK, fc) for _, _, fc in TK.F}
flip = all({frozenset((a, b, d)), frozenset((b, c, d))} <= PDf and frozenset((a, b, c)) not in PDf and
           {frozenset((a, b, c)), frozenset((a, c, d))} <= TKf and frozenset((a, b, d)) not in TKf for (a, b, c, d), _ in rh)
check(flip, 'over every rhombus (5a, 3b, 5c, 3d): PD has the triangles abd, bcd (fold along the 3-3 diagonal), TK has abc, acd (fold along the 5-5 diagonal): a diagonal flip')
def reflect(x, n): k = dot(x, n) / dot(n, n); return sub(x, mul(2 * k, n))
mirror = all(all(any(parallel_same(reflect(a, cross(AX[p], AX[q])), b) for b in AX) for a in AX)
             for (a5, b3, c5, d3), _ in rh for p, q in [(a5, b3), (b3, c5), (c5, d3), (d3, a5)])
check(mirror, 'every plane through the centre and two neighbouring corners of a rhombus is a mirror plane (maps the 32 rays to themselves)')
def r5ratio(A, B, i=0):                                              # exact ratio of the corners of A and B on five-fold ray i
    a5 = next(k for k in range(32) if AXK[k] == 5); p, q = ray[A][a5], ray[B][a5]; j = next(t for t in range(3) if q[t] != 0); return p[j] / q[j]
kTK = F(155, 100) * r5ratio('PD', 'TK'); kRT = F(125, 100) * r5ratio('PD', 'RT'); mu = F(155, 86)
TK1 = TK.scaled(kTK); RT1 = RT.scaled(kRT); PDmu = PD.scaled(mu)
check(all(TK1.contains(p, strict=True) for p in PD.P) and all(PDmu.contains(p, strict=True) for p in TK1.P),
      'nesting exact: PD (five-fold radius 1) inside TK (1.55) inside PD scaled by 155/86 (1.8023), strictly')
check(all(TK1.contains(p, strict=True) and not PD.contains(p, strict=True) for p in RT1.P), 'RT (1.25) lies between PD and TK')
def flip_cells(inner, outer, inner_tris, outer_tris):
    ri = {axis_of(p): p for p in inner.P}; ro = {axis_of(p): p for p in outer.P}; vols, shapes, flat = [], set(), True
    for (a, b, c, d), _ in rh:
        for p, q in [(a, b), (b, c), (c, d), (d, a)]:
            flat &= det3(ri[p], ri[q], ro[p]) == 0 and det3(ri[p], ri[q], ro[q]) == 0
        sv = lambda r, tris: sum((abs_q(det3(r[x], r[y], r[z])) for x, y, z in tris(a, b, c, d)), Q5(0)) / 6
        vols.append(sv(ro, outer_tris) - sv(ri, inner_tris))
        C = [ri[a], ri[b], ri[c], ri[d], ro[a], ro[b], ro[c], ro[d]]
        shapes.add(tuple(sorted(dot(sub(x, y), sub(x, y)) for x, y in itertools.combinations(C, 2))))
    return vols, shapes, flat
def abs_q(x): return x if x.sign() >= 0 else -x
PDtris = lambda a, b, c, d: [(a, b, d), (b, c, d)]; TKtris = lambda a, b, c, d: [(a, b, c), (a, c, d)]
vf, shf, flf = flip_cells(PD, TK1, PDtris, TKtris)
check(flf, 'forward flip shell: all 120 side faces flat (four corners coplanar with the centre, exact)')
check(len(set(vf)) == 1 and vf[0].sign() > 0 and len(shf) == 1, f'forward flip shell: 30 cells, one volume {float(vf[0]):.10f} (exact, all equal), one distance multiset (congruent)')
check(sum(vf, Q5(0)) == TK1.volume() - PD.volume(), f'forward flip shell: 30 volumes add to V(TK) - V(PD) = {float(TK1.volume() - PD.volume()):.10f} exactly')
r5 = 1 / float(np.linalg.norm(f([ray['PD'][next(k for k in range(32) if AXK[k] == 5)]])[0]))
print(f'control: at five-fold radius 1 for PD the forward shell volume is {float(TK1.volume() - PD.volume()) * r5 ** 3:.10f} (source study, float: 6.4660211935); one cell {float(vf[0]) * r5 ** 3:.4f} (0.2155)', flush=True)
vb, shb, flb = flip_cells(TK1, PDmu, TKtris, PDtris)
check(flb and len(set(vb)) == 1 and vb[0].sign() > 0 and len(shb) == 1 and sum(vb, Q5(0)) == PDmu.volume() - TK1.volume(),
      f'back flip shell (TK -> RT -> PD x 155/86): faces flat, 30 congruent cells of volume {float(vb[0]):.10f}, adding to the shell exactly')
check(shf != shb, 'the forward and back flip cells are two different shapes')
print('PROGRESS 0.30 polar flip exact (Theorem 5.3)', flush=True)
if MODE == 'flip':
    print(f'pilot (flip part) {time.time() - t0:.1f} s; checks failed {len(fails)}')
    print('FINAL ok (pilot: polar flip)' if not fails else 'FINAL FAIL'); sys.exit()

# ---------------- C: the scutoid move and its reverse as exact shells (Theorem 5.4)
R0 = float(np.linalg.norm(f(TI.P[:1])[0]))
def scale_to(S, r): return Solid([mul(F(round(r * R0 / float(np.linalg.norm(f(S.P[:1])[0])) * 10 ** 6), 10 ** 6), p) for p in S.P], S.name)
lam = F(71, 45)
TI0 = TI; ID1 = scale_to(ID, 1.18); TD1 = scale_to(TD, 1.42); ID2 = scale_to(ID, 0.95 * 1.42 / 0.90); TI2 = TI.scaled(lam)
print('circumradii (TI = 1):', [round(float(np.linalg.norm(f(S.P[:1])[0])) / R0, 6) for S in (TI0, ID1, TD1, ID2, TI2)], flush=True)
def shell(core, mid, out, tag, prog):
    big_c = max(len(fc) for _, _, fc in core.F); big_o = max(len(fc) for _, _, fc in out.F)
    def shrink_map(S, big):                                          # each corner -> the mid corner on the ray of its big-big edge
        faces_at = {}
        for i, (_, _, fc) in enumerate(S.F):
            for u in fc: faces_at.setdefault(u, []).append(i)
        m = {}
        for e in S.E:
            u, w = tuple(e); fs = [i for i in faces_at[u] if w in S.F[i][2]]
            if all(len(S.F[i][2]) == big for i in fs):
                mid_i = [k for k, p in enumerate(mid.P) if parallel_same(p, add(S.P[u], S.P[w]))]; assert len(mid_i) == 1
                m[u] = m.get(u, mid_i[0]); m[w] = m.get(w, mid_i[0]); assert m[u] == mid_i[0] and m[w] == mid_i[0]
        return m, faces_at
    hh, fa_c = shrink_map(core, big_c); po, fa_o = shrink_map(out, big_o)
    ok_maps = len(hh) == len(core.P) and len(po) == len(out.P)
    face_on = lambda S, n: next(fc for nr, d, fc in S.F if parallel_same(nr, n))
    halves, kinds, ok_faces, ok_sep = [], Counter(), True, True
    for nr, d, fc in core.F:
        g = face_on(mid, nr); o = face_on(out, nr)
        ok_faces &= {hh[u] for u in fc} == set(g) and {po[t] for t in o} == set(g)
        lowP = [core.P[u] for u in fc] + [mid.P[k] for k in g]
        lowF = {frozenset(core.P[u] for u in fc), frozenset(mid.P[k] for k in g)} | {frozenset((core.P[u], core.P[w], mid.P[hh[w]], mid.P[hh[u]])) for u, w in zip(fc, fc[1:] + fc[:1])}
        upP = [mid.P[k] for k in g] + [out.P[t] for t in o]
        upF = {frozenset(mid.P[k] for k in g), frozenset(out.P[t] for t in o)} | {frozenset((mid.P[po[t]], mid.P[po[s]], out.P[s], out.P[t])) for t, s in zip(o, o[1:] + o[:1])}
        for P, Fc in [(lowP, lowF), (upP, upF)]:
            Bd = Body(P); got = {frozenset(Bd.P[i] for i in on) for _, _, on in Bd.F}
            ok_faces &= got == Fc                                    # the hull's facets are exactly the faces of the construction
            ok_sep &= all(dot(nr, x) >= d for x in Bd.P) and all(out.contains(x) for x in Bd.P)
            halves.append(Bd)
        kinds[(len(fc), len(g), len(o))] += 1
    print(f'PROGRESS {prog:.2f} {tag}: 64 half-cells built', flush=True)
    vols = [b.volume() for b in halves]
    bad = [(i, j) for i, j in itertools.combinations(range(len(halves)), 2) if not disjoint(halves[i], halves[j])]
    across = True                                                    # the move goes across: new edge between the two cells that did not touch
    for e in core.E:
        u, w = tuple(e)
        if hh.get(u) != hh.get(w): continue
        small = [next(core.F[i][0] for i in fa_c[x] if len(core.F[i][2]) < big_c) for x in (u, w)]
        t, s = [t for t in range(len(out.P)) if po[t] == hh[u]]
        bigo = [out.F[i][0] for i in fa_o[t] if s in out.F[i][2]]
        across &= len(bigo) == 2 and all(any(parallel_same(a, b) for b in bigo) for a in small)
    tot = sum(vols, Q5(0)); shellv = out.volume() - core.volume()
    check(ok_maps and ok_faces, f'{tag}: cells {dict(kinds)}; every half-cell is the convex hull of its two end faces and its facets are exactly the faces of the construction (every face flat, exact)')
    check(across, f'{tag}: each shrunk edge reopens across: the new edge lies on the two faces grown from the cells that did not touch')
    check(ok_sep and all(x.sign() > 0 for x in vols), f'{tag}: every half-cell inside the outer solid and outside the core (exact planes), every volume positive')
    check(not bad, f'{tag}: {len(halves) * (len(halves) - 1) // 2} pairs of half-cells, interiors disjoint (exact separating planes); overlapping {bad[:5]}')
    check(tot == shellv, f'{tag}: the 64 volumes add to V(out) - V(core) = {float(shellv):.10f} exactly: the shell is filled exactly once')
    per = {}
    for (k, fc), a, b in zip([(None, fc) for _, _, fc in core.F], vols[0::2], vols[1::2]): per.setdefault(len(fc), set()).add(a + b)
    check(all(len(s) == 1 for s in per.values()), f'{tag}: cells of one kind have one volume each ({ {k: round(float(next(iter(s))), 10) for k, s in per.items()} })')
    return kinds
kS = shell(TI0, ID1, TD1, 'S (TI -> ID -> TD)', 0.55)
kA = shell(TD1, ID2, TI2, 'A (TD -> ID -> TI x 71/45)', 0.85)
check(all(TD1.contains(p, strict=True) for p in TI0.P) and all(TI2.contains(p, strict=True) for p in TD1.P),
      'nesting exact: TI inside TD inside TI x 71/45, strictly; S and A share the TD surface corner for corner (the same exact solid)')
check(set(kS) == {(5, 5, 10), (6, 3, 3)} and set(kA) == {(10, 5, 5), (3, 3, 6)}, 'four scutoid shapes per period: 5-5-10, 6-3-3 (S) and 10-5-5, 3-3-6 (A)')
print('PROGRESS 0.97 done', flush=True)
print(f'checks failed: {len(fails)}; {time.time() - t0:.1f} s')
print('FINAL ok: Theorems 5.3 and 5.4 certified exactly in Q(sqrt5)' if not fails else 'FINAL FAIL')
