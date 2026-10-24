# Keyed pair as golden pair ± 8 Tricaps, and the hull-and-remainder polar (DICTO's method, 10-24), exact in Q(√5).
# Frame of #48 (icosahedron edge 1 at the origin, lattice spacing φ, Unborn centred at UC = (φ/2)(1,1,1)); reuses golden_split_exact.py.
import sys, os
from itertools import product, combinations
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'exact'))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'exact', 'golden_split_exact.py')).read()
exec(src.split("print('AXEs generated:'")[0])
exec('def hull_facets' + src.split('def hull_facets')[1].split('def poly_volume')[0])      # the exact hull-facet finder of #48              # Q5, PHI, IPHI, H, ICO, UNB, UC, helpers, check
ok_all = True
def say(label, ok):
    global ok_all; ok_all &= bool(ok); print(('PASS ' if ok else 'FAIL ') + label)
def perms(a, b):
    S = set()
    for p in set(__import__('itertools').permutations((0, 1, 2))):
        for sg in product((1, -1), repeat=3):
            v = [Z, Z, Z]; vals = (a, b, Z)
            for k in range(3): v[p[k]] = vals[k] * sg[k]
            S.add(tuple(v))
    return sorted(S, key=lambda v: tuple(float(x) for x in v))
ICOSAXES = perms(HALF, H)                         # all perms of (±1/2, ±φ/2, 0)
UNBAXES = [add(UC, q) for q in perms(IPHI * HALF, H)]   # all perms of (±1/(2φ), ±φ/2, 0) about UC
# The Tricap of the Unborn at UC in direction s: apex UC + s/2, base UC + the 3 dodecahedron neighbours of that corner (edge 1/φ)
def tricap(s):
    sx, sy, sz = s
    ap = add(UC, (HALF * sx, HALF * sy, HALF * sz))
    nb = [add(UC, (H * sx, IPHI * HALF * sy, Z * sz)), add(UC, (Z * sx, H * sy, IPHI * HALF * sz)), add(UC, (IPHI * HALF * sx, Z * sy, H * sz))]   # #48's (cyclic) orientation
    return [ap] + nb
TR = [tricap(s) for s in product((1, -1), repeat=3)]
def vol(P):
    D = det(sub(P[1], P[0]), sub(P[2], P[0]), sub(P[3], P[0])); return D * Fr(1, 6) if D.sign() >= 0 else D * Fr(-1, 6)
vt = vol(TR[0])
say('(1) every Tricap has volume 1/(12φ²) exactly: %s' % vt, all(vol(t) == vt for t in TR) and vt * 12 * PHI * PHI == 1)
U = set(UNBAXES)
say('(2a) each Tricap\'s three base corners are corners of the Unborn (so also of the Unborn Axes)', all(all(v in set(UNB) and v in U for v in t[1:]) for t in TR))
say('(2a\') each Tricap\'s apex is a corner of the cube of the Unborn\'s dodecahedron, (φ/2)(1,1,1) ± 1/2', all(all(x == H + HALF or x == H - HALF for x in t[0]) for t in TR))
def facets(P):
    F = hull_facets(P); return [(n, dot(n, P[next(iter(on))])) for on, n in F.items()]
FU = facets(UNBAXES)
def on_face_out(t, F):   # base on a facet plane of F, apex strictly outside that plane
    for n, d in F:
        if all(dot(n, v) == d for v in t[1:]) and (dot(n, t[0]) - d).sign() > 0: return True
    return False
say('(2b) each Tricap stands on a hexagon face of the Unborn Axes, apex outside: a key', all(on_face_out(t, FU) for t in TR))
# the same Tricaps seen from the icosahedron at the origin: the Unborn at UC*s sends its Tricap in direction -s
TRI = [[add(mul(Q5(1), v), (Z, Z, Z)) for v in tricap(tuple(-x for x in s))] for s in product((1, -1), repeat=3)]
TRI = [[add(v, sub(tuple(H * x for x in s), UC)) for v in tricap(tuple(-x for x in s))] for s in product((1, -1), repeat=3)]
FI = facets(ICO); FX = facets(ICOSAXES)
inside = lambda v, F: all((dot(n, v) - d).sign() <= 0 for n, d in F)
say('(2c) the 8 Tricaps facing the origin lie inside the icosahedron, each on one of its faces (corners inside or on it)', all(inside(v, FI) for t in TRI for v in t))
say('(2d) ... and their bases lie in the hexagon faces of the Icosaxes: dents', all(any(all(dot(n, v) == d for v in t[1:]) for n, d in FX) for t in TRI))
interiors_disjoint = all(not all((dot(n, sum_c) - d * 4).sign() < 0 for n, d in facets(b)) for a, b in combinations(TRI, 2) for sum_c in [tuple(sum((v[k] for v in a), Z) for k in range(3))])
say('(2e) the 8 dents are pairwise apart (no Tricap centroid inside another)', interiors_disjoint)
def tovol(P):
    F = hull_facets(P); c = P[0]; v = Q5(0)
    for on, n in F.items():
        idx = sorted(on, key=lambda i: tuple(float(x) for x in P[i]))
        # fan the facet: order corners around the facet normal
        import math
        cen = [sum(float(P[i][k]) for i in idx) / len(idx) for k in range(3)]
        nf = [float(x) for x in n]; u = [float(P[idx[0]][k]) - cen[k] for k in range(3)]
        w = [nf[1]*u[2]-nf[2]*u[1], nf[2]*u[0]-nf[0]*u[2], nf[0]*u[1]-nf[1]*u[0]]
        idx.sort(key=lambda i: math.atan2(sum((float(P[i][k])-cen[k])*w[k] for k in range(3)), sum((float(P[i][k])-cen[k])*u[k] for k in range(3))))
        for j in range(1, len(idx) - 1):
            v = v + det(sub(P[idx[0]], c), sub(P[idx[j]], c), sub(P[idx[j+1]], c)) * Fr(1, 6)
    return v if v.sign() > 0 else -v
VI, VU = tovol(ICOSAXES), tovol(UNBAXES)
say('(3a) Icosaxes volume 1 + 2√5/3 exactly: %s' % VI, VI == Q5(1, Fr(2, 3)))
say('(3b) Unborn Axes volume 1 + √5/3 exactly: %s' % VU, VU == Q5(1, Fr(1, 3)))
say('(3c) Lotus Jewel Axes = Icosaxes − 8 Tricaps: volume √5 exactly', VI - vt * 8 == Q5(0, 1))
say('(3d) Dodecaxes = Unborn Axes + 8 Tricaps: volume 2 exactly', VU + vt * 8 == Q5(2))
# (4) polars of the golden pair (about each centre): square faces at distance (1+x)s, hexagons at (1+2x)s/√3 -> pyramid height x/(1+x)
def pyr_height(P, cen):
    # polar about cen: facet n.x = d gives corner n/(d - n.cen). Square facet n = (a,0,0): apex at |a|/d' on the axis;
    # hexagon facet n = (±m,±m,±m): polar cube corner, half edge |m|/e'. Height in half cube edges = |a| e' / (d' |m|) - 1.
    F = [(n, d - dot(n, cen)) for n, d in facets(P)]
    n, d = [(n, d) for n, d in F if sum(1 for x in n if x != Z) == 1][0]
    m, e = [(n, d) for n, d in F if sum(1 for x in n if x != Z) == 3][0]
    a = [x for x in n if x != Z][0]; a = a if a.sign() > 0 else -a; mm = m[0] if m[0].sign() > 0 else -m[0]
    return a * e, d * mm          # (1 + height) = first / second
def ratio_eq(num, den, val): return num == den * val
n1, d1 = pyr_height(ICOSAXES, (Z, Z, Z)); n2, d2 = pyr_height(UNBAXES, UC)
say('(4a) polar of the Icosaxes: a cube with face pyramids of height 1/φ (in half cube edges)', ratio_eq(n1, d1, Q5(1) + IPHI) and len(facets(ICOSAXES)) == 14)
say('(4b) polar of the Unborn Axes: pyramids of height 1/φ² ; and 1/φ + 1/φ² = 1 (Kepler\'s rhombic dodecahedron)', ratio_eq(n2, d2, Q5(1) + IPHI * IPHI) and IPHI + IPHI * IPHI == 1 and len(facets(UNBAXES)) == 14)
# (5) polar of a Tricap about its centroid: corner i = n_i / (d_i - n_i.g); lateral and base edges of the polar
t = TR[0]; g = tuple(sum((v[k] for v in t), Z) * Fr(1, 4) for k in range(3))
F5 = facets(t); poles = [mul(Q5(1) * 1, n) for n, d in F5]
P5 = []
for n, d in F5:
    h = d - dot(n, g); P5.append((n, h))
def dist2(a, b):   # |a/ha - b/hb|^2 compared without dividing: returns numerator/denominator pair is messy; use squared edge via common scaling
    (na, ha), (nb, hb) = a, b
    v = sub(mul(hb, na), mul(ha, nb)); return dot(v, v), (ha * hb) * (ha * hb)
E2 = [dist2(a, b) for a, b in combinations(P5, 2)]
def eq_ratio(x, y): return x[0] * y[1] == y[0] * x[1]
groups = []
for e in E2:
    for gp in groups:
        if eq_ratio(gp[0], e): gp.append(e); break
    else: groups.append([e])
say('(5a) the Tricap\'s polar is a three-sided pyramid: its 6 edges come in two lengths, 3 and 3', sorted(len(gp) for gp in groups) == [3, 3])
long_, short = (groups[0][0], groups[1][0]) if float(groups[0][0][0]) / float(groups[0][0][1]) > float(groups[1][0][0]) / float(groups[1][0][1]) else (groups[1][0], groups[0][0])
# long²/short² = 5 + 2√5 = tan²72°
say('(5b) long edge : short edge = tan 72°, i.e. squared ratio 5 + 2√5', long_[0] * short[1] == short[0] * long_[1] * Q5(5, 2))
print('ALL PASS' if ok_all else 'SOME FAIL')
