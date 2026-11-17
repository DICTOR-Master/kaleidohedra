"""Chapter 4, Theorem 4.1 made exact: DICTO's Hemi RD build (Polyhedraverse, 11 Nov 2026; world export in
studies/2026-11-11-hemi-rd-build/data/dicto-build-worldpoly.json) read in rational coordinates.
Exact reading: every stored quaternion gives, to within 1e-12 per entry, a rotation matrix with entries in {-1, 0, 1}; every stored
position is, to within 1e-12, a multiple of 1/10. The build is READ as those exact values (the export stores binary floats; the
rounding is printed). The Hemi RD's corners in its own frame are the app's record (decimal tenths, exact as fractions).
Checks (all in rational arithmetic):
 (1) each matrix is a rotation (orthogonal, det +1) and each piece has volume exactly 1 (the RD it halves: 2);
 (2) the 14 pieces have pairwise disjoint interiors (separating planes: facet normals and edge cross products);
 (3) the convex hull of the 140 corners is Z + c exactly, Z the zonohedron with generators e1, e2, e3 and the four half body
     diagonals (every corner inside Z + c, every corner of Z + c a corner of a piece), for one of the 48 axis frames;
 (4) Z: 6 squares of side 1, 12 hexagons with squared sides 1, 3/4, 3/4, 1, 3/4, 3/4 (long sides opposite), volume 15;
 (5) the six cube pyramids (base a square of Z, apex 1/2 inside) lie in Z + c and have interiors disjoint from every piece and
     from each other; 14 * 1 + 6 * 1/6 = 15 = vol Z, so pieces and pyramids fill Z + c exactly (a packing of a convex body by
     closed sets with full volume covers it).
Prints PROGRESS lines and FINAL ok only if every check passes."""
import json, sys, os, itertools, time
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q5 import Q5, v, add, sub, mul, dot, cross, det3, Body, disjoint, facets, order_face, hull_volume
t0 = time.time(); fails = []
def check(ok, what):
    print(('ok   ' if ok else 'FAIL ') + what)
    if not ok: fails.append(what)
B = json.load(open(sys.argv[1]))
LV = [(-.5, -.3, .7), (-1, .2, .2), (-.5, .7, -.3), (.5, .7, -.3), (1, .2, .2), (.5, -.3, .7), (-.5, -.3, -.3), (.5, -.3, -.3), (0, -.8, .2), (0, .2, -.8)]
LVx = [v(*(F(str(x)) for x in p)) for p in LV]
def rot(q):
    x, y, z, w = q; n = (x*x + y*y + z*z + w*w) ** .5; x, y, z, w = x/n, y/n, z/n, w/n
    return [[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]]
pieces = []; worst_r = worst_p = 0.0
for nd in B['nodes']:
    M = rot(nd['transform']['quaternion']); Mx = [[F(round(e)) for e in row] for row in M]
    worst_r = max(worst_r, max(abs(M[i][j] - float(Mx[i][j])) for i in range(3) for j in range(3)))
    pos = nd['transform']['position']; px = [F(round(p * 10), 10) for p in pos]; worst_p = max(worst_p, max(abs(p - float(q)) for p, q in zip(pos, px)))
    MM = [[sum(Mx[k][i] * Mx[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    d = det3(*[v(*row) for row in Mx])
    check(MM == [[1, 0, 0], [0, 1, 0], [0, 0, 1]] and d == 1, f'{nd["id"]}: exact rotation {Mx}, translation {[str(p) for p in px]}')
    pieces.append([add(v(*(sum(Mx[i][j] * p[j].a for j in range(3)) for i in range(3))), v(*px)) for p in LVx])
print(f'rounding: largest |stored - exact| rotation entry {worst_r:.1e}, position {worst_p:.1e}')
check(worst_r < 1e-12 and worst_p < 1e-12, 'the stored transforms are these exact values to 1e-12')
print('PROGRESS 0.10 transforms read exactly')
H = Body(LVx); vH = H.volume()
check(len(H.F) == 8 and vH == 1, f'one Hemi RD: {len(H.F)} faces (6 + 4 + 4 + 4 + 4 + 3 + 3 corners: {sorted(len(on) for _, _, on in H.F)}), volume {vH}')
bodies = [Body(P) for P in pieces]
check(all(b.volume() == 1 for b in bodies), 'all 14 pieces have volume exactly 1')
print('PROGRESS 0.25 pieces built')
bad = [(i, j) for i, j in itertools.combinations(range(14), 2) if not disjoint(bodies[i], bodies[j])]
check(not bad, f'91 pairs of pieces: interiors disjoint (exact separating planes); overlapping pairs: {bad}')
print('PROGRESS 0.50 pieces disjoint')
h = F(1, 2)
G = [v(1, 0, 0), v(0, 1, 0), v(0, 0, 1), v(h, h, h), v(h, h, -h), v(h, -h, h), v(-h, h, h)]
pts = {tuple(sum((s * g[i] / 2 for s, g in zip(sg, G)), Q5(0)) for i in range(3)) for sg in itertools.product((1, -1), repeat=7)}
NRM = {n for a, b in itertools.combinations(G, 2) for n in [cross(a, b)]}
NRM |= {tuple(-x for x in n) for n in NRM}
PL = [(n, max(dot(n, p) for p in pts)) for n in NRM]                     # support planes in the directions of all generator-pair normals
VZ = sorted({p for p in pts if sum(1 for n, d in PL if dot(n, p) == d) >= 3}, key=lambda p: tuple(float(x) for x in p))
Zb = Body(VZ); volZ = Zb.volume()
sq = [f for f in Zb.F if len(f[2]) == 4]; hx = [f for f in Zb.F if len(f[2]) == 6]
def sides(f):
    o = order_face(Zb.P, f[2], f[0]); return [dot(sub(Zb.P[o[k]], Zb.P[o[(k + 1) % len(o)]]), sub(Zb.P[o[k]], Zb.P[o[(k + 1) % len(o)]])) for k in range(len(o))]
okhex = all(any(sides(f)[k:] + sides(f)[:k] == [1, F(3, 4), F(3, 4), 1, F(3, 4), F(3, 4)] for k in range(6)) for f in hx)
check(len(VZ) == 32 and len(sq) == 6 and len(hx) == 12 and len(Zb.F) == 18 and volZ == 15 and all(sides(f) == [1] * 4 for f in sq) and okhex,
      f'Z: {len(VZ)} corners, {len(sq)} unit squares, {len(hx)} hexagons with squared sides 1, 3/4, 3/4, 1, 3/4, 3/4 (long sides opposite), volume {volZ}')
allp = sorted({p for P in pieces for p in P}, key=lambda p: tuple(float(x) for x in p))
c = tuple(sum((p[i] for p in allp), Q5(0)) / len(allp) for i in range(3))
found = None
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        T = lambda p: tuple(sg[i] * p[perm[i]] for i in range(3))
        ZV = [add(T(p), c) for p in VZ]
        if set(ZV) <= set(allp):
            Zc = Body(ZV)
            if all(Zc.contains(p) for p in allp): found = (perm, sg, Zc); break
    if found: break
print(f'centre of the build corners: {[str(x) for x in c]}')
check(found is not None, f'conv(build) = Z + c exactly (frame {found[:2] if found else None}): every corner of the build lies in Z + c, every corner of Z + c is a corner of a piece')
print('PROGRESS 0.75 hull identified')
if found:
    Zc = found[2]; pyr = []
    for nr, d, on in Zc.F:
        if len(on) != 4: continue
        base = [Zc.P[i] for i in on]; m = tuple(sum((p[i] for p in base), Q5(0)) / 4 for i in range(3))
        # unit outward normal of an axis square: nr is a multiple of a coordinate vector
        k = [i for i in range(3) if nr[i] != 0]; assert len(k) == 1; u = [Q5(0)] * 3; u[k[0]] = Q5(1 if nr[k[0]] > 0 else -1)
        apex = sub(m, mul(F(1, 2), tuple(u))); pyr.append(Body(base + [apex]))
    check(len(pyr) == 6 and all(p.volume() == F(1, 6) for p in pyr), 'six cube pyramids (unit square base, apex 1/2 inside), volume 1/6 each')
    check(all(Zc.contains(q) for p in pyr for q in p.P), 'the pyramids lie in Z + c')
    bad = [(i, j) for i in range(6) for j in range(14) if not disjoint(pyr[i], bodies[j])] + [(i, j) for i, j in itertools.combinations(range(6), 2) if not disjoint(pyr[i], pyr[j])]
    check(not bad, f'84 pyramid-piece pairs and 15 pyramid-pyramid pairs: interiors disjoint (exact); overlapping: {bad}')
    tot = 14 + 6 * F(1, 6)
    check(tot == volZ, f'volumes: 14 * 1 + 6 * 1/6 = {tot} = vol Z = {volZ}: pieces and pyramids fill Z + c exactly')
print('PROGRESS 0.97 done')
print(f'checks failed: {len(fails)}; {time.time() - t0:.1f} s')
print('FINAL ok: Theorem 4.1 exact (build read in rational coordinates; hull = chamfered cube; build = Z less six cube pyramids)' if not fails else 'FINAL FAIL')
