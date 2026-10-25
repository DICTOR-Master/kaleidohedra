# Web of bonds of the keyed DICTONIC pair (all keyed: Lotus Jewel Axes + Dodecaxes), exact in Q(√5), with the golden pair at x = τ
# (Icosaxes + Unborn Axes) through the same code as the control. Frame of #48 / the polar study: icosahedron edge 1 at the origin,
# lattice spacing φ (Icosaxes at φZ³, Unborn Axes at UC + φZ³, UC = (φ/2)(1,1,1)). Reuses keyed_polar_exact.py (its Tricaps, in the
# corrected cyclic orientation of #48). A bond = a shared boundary region of positive area. Each piece's boundary is a signed sum of
# convex polygons (Lotus: Icosaxes faces − 8 Tricap bases + 8×3 Tricap side faces turned inward; Dodecaxes: Unborn Axes faces − 8 bases
# + 8×3 side faces); the shared area of two pieces is Σ s_a s_b area(a ∩ b) over coplanar, oppositely facing polygons.
import sys, os, io, contextlib
from itertools import product, combinations
from fractions import Fraction as Fr
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
POLAR = os.environ.get('POLAR', os.path.join(HERE, '..', '..', '2026-10-23-shadow-forms', 'polar', 'keyed_polar_exact.py'))
src = open(POLAR).read().replace("os.path.dirname(os.path.abspath(__file__))", repr(os.path.dirname(os.path.abspath(POLAR))))
with contextlib.redirect_stdout(io.StringIO()) as buf: exec(src)
assert 'ALL PASS' in buf.getvalue(), buf.getvalue()
import math
def inv(q): n = q.a * q.a - 5 * q.b * q.b; return Q5(q.a / n, -q.b / n)
ok_all = True; npass = 0
def say(label, ok):
    global ok_all, npass; ok_all &= bool(ok); npass += bool(ok); print(('PASS ' if ok else 'FAIL ') + label)
S5 = sp.sqrt(5)
sym = lambda q: sp.Rational(q.a.numerator, q.a.denominator) + sp.Rational(q.b.numerator, q.b.denominator) * S5
def order(P, n):   # corners of a convex planar polygon in turn about n (floats only to sort)
    cen = [sum(float(p[k]) for p in P) / len(P) for k in range(3)]; nf = [float(x) for x in n]
    u = [float(P[0][k]) - cen[k] for k in range(3)]; w = [nf[1]*u[2]-nf[2]*u[1], nf[2]*u[0]-nf[0]*u[2], nf[0]*u[1]-nf[1]*u[0]]
    return sorted(P, key=lambda p: math.atan2(sum((float(p[k])-cen[k])*w[k] for k in range(3)), sum((float(p[k])-cen[k])*u[k] for k in range(3))))
def faces_of(P):   # facets of the hull of P: (outward normal, corners in turn)
    return [(n, order([P[i] for i in on], n)) for on, n in hull_facets(P).items()]
def avec(poly):    # area vector ½ Σ v_i × v_{i+1}
    A = (Z, Z, Z)
    for i in range(len(poly)): A = add(A, cross(poly[i], poly[(i + 1) % len(poly)]))
    return mul(HALF, A)
def clip(poly, n, a, b):   # keep the part of poly on the left of edge a→b (about normal n)
    m = cross(n, sub(b, a)); out = []
    val = [dot(m, sub(p, a)) for p in poly]
    for i in range(len(poly)):
        p, q, vp, vq = poly[i], poly[(i + 1) % len(poly)], val[i], val[(i + 1) % len(poly)]
        if vp.sign() >= 0: out.append(p)
        if vp.sign() * vq.sign() < 0: out.append(add(p, mul(vp * inv(vp - vq), sub(q, p))))
    return out
def inter(P, Q, n):   # P, Q convex, coplanar, both turning positively about n
    R = P
    for i in range(len(Q)):
        if len(R) < 3: return []
        R = clip(R, n, Q[i], Q[(i + 1) % len(Q)])
    return R
def turn(poly, n):   # make poly turn positively about n
    return poly if dot(avec(poly), n).sign() > 0 else poly[::-1]
def area_q(poly, n):   # exact area as (A·n, |n|²): area = A·n / |n|
    return dot(avec(poly), n), dot(n, n)
# ---- the pieces ----
FI = faces_of(ICOSAXES); FU = faces_of(UNBAXES)
hexI = [(n, P) for n, P in FI if len(P) == 6]; hexU = [(n, P) for n, P in FU if len(P) == 6]
def tri_parts(T):   # Tricap [apex, b1, b2, b3] -> (base, [3 sides]) with the Tricap's outward normals
    F = faces_of(T); base = [(n, P) for n, P in F if T[0] not in P]; sides = [(n, P) for n, P in F if T[0] in P]
    return base[0], sides
def shift(f, c): n, P = f; return (n, [add(p, c) for p in P])
def lotus(c, keyed=True):   # signed faces (sign, outward normal of the piece, corners in turn about it)
    out = [(1, n, P) for n, P in FI]
    if keyed:
        for T in TRI:
            (nb, B), S = tri_parts(T)
            out.append((-1, nb, turn(B, nb)))                              # base sits in the Icosaxes' hexagon; piece normal = Tricap's
            out += [(1, mul(-1, n), turn(P, mul(-1, n))) for n, P in S]    # side faces, now facing into the dent
    return [(s, n, [add(p, c) for p in P]) for s, n, P in out]
def dodec(c, keyed=True):
    out = [(1, n, P) for n, P in FU]
    if keyed:
        for T in TR:
            (nb, B), S = tri_parts(T)
            out.append((-1, mul(-1, nb), turn(B, mul(-1, nb))))           # base sits in the Unborn Axes' hexagon; piece normal = − Tricap's
            out += [(1, n, P) for n, P in S]
    return [(s, n, [add(p, sub(c, UC)) for p in P]) for s, n, P in out]
def coplanar_opp(fa, fb):
    (_, na, Pa), (_, nb, Pb) = fa, fb
    return all(x == 0 for x in cross(na, nb)) and dot(na, nb).sign() < 0 and dot(na, Pb[0]) == dot(na, Pa[0])
def coplanar_same(fa, fb):
    (_, na, Pa), (_, nb, Pb) = fa, fb
    return all(x == 0 for x in cross(na, nb)) and dot(na, nb).sign() > 0 and dot(na, Pb[0]) == dot(na, Pa[0])
def shared(A, B):   # list of (A·n, |n|²) terms, signed
    terms = []
    for fa in A:
        for fb in B:
            if coplanar_opp(fa, fb):
                R = inter(fa[2], turn(fb[2], fa[1]), fa[1])
                if len(R) >= 3:
                    an, nn = area_q(R, fa[1])
                    if an.sign() != 0: terms.append((fa[0] * fb[0], an, nn))
    return terms
def symarea(terms): return sp.nsimplify(sp.simplify(sum(s * sym(an) / sp.sqrt(sym(nn)) for s, an, nn in terms))) if terms else sp.Integer(0)
def surface(A): return sp.simplify(sum(s * sym(area_q(P, n)[0]) / sp.sqrt(sym(area_q(P, n)[1])) for s, n, P in A))
def cluster(keyed):
    pcs = {}
    for m in product((-1, 0, 1), repeat=3):
        pcs[('L' if keyed else 'I', m)] = lotus(mul(PHI, tuple(Q5(x) for x in m)), keyed)
    for m in product((-2, -1, 0, 1), repeat=3):
        c = add(UC, mul(PHI, tuple(Q5(x) for x in m)))
        if max(abs(float(x) - float(PHI) / 4) for x in c) < 1.9 * float(PHI): pcs[('D' if keyed else 'U', m)] = dodec(c, keyed)
    return pcs
def web(keyed, centres):
    pcs = cluster(keyed); res = {}
    for k0 in centres:
        bonds = {}
        for k, B in pcs.items():
            if k == k0: continue
            t = shared(pcs[k0], B)
            if t:
                a = symarea(t)
                if a != 0: bonds[k] = a
        res[k0] = (bonds, surface(pcs[k0]))
    return res
NAME = {'I': 'Icosaxes', 'U': 'Unborn Axes', 'L': 'Lotus Jewel Axes', 'D': 'Dodecaxes'}
def report(res):
    tab = {}
    for k0, (bonds, surf) in res.items():
        kinds = {}
        for k, a in bonds.items(): kinds.setdefault((k[0], a), []).append(k[1])
        print(f'{NAME[k0[0]]} at {k0[1]}: surface {surf} ≈ {float(surf):.10f}')
        for (kk, a), ms in sorted(kinds.items(), key=lambda z: (z[0][0], -float(z[0][1]))):
            print(f'   {len(ms)} × {NAME[kk]}, shared area {a} ≈ {float(a):.10f}')
        tab[k0[0]] = {(kk, a): len(ms) for (kk, a), ms in kinds.items()}
        say(f'{NAME[k0[0]]}: surface = sum of its shared regions (the pieces fill space): {sp.simplify(surf - sum(bonds.values())) == 0}', sp.simplify(surf - sum(bonds.values())) == 0)
    return tab
O3 = (0, 0, 0); U0 = (0, 0, 0)
print('== golden pair at x = τ (control, same code) ==')
g = report(web(False, [('I', O3), ('U', U0)]))
hexA = (sp.sqrt(3) + 3 * sp.sqrt(15)) / 16
say('control: Icosaxes = 8 hexagons (√3 + 3√15)/16 with Unborn Axes + 6 squares 1/2 with Icosaxes (study 2026-10-25-web-of-bonds)',
    sorted(g['I'].values()) == [6, 8] and all(sp.simplify(a - (hexA if kk == 'U' else sp.Rational(1, 2))) == 0 for kk, a in g['I']))
say('control: Unborn Axes = 8 hexagons with Icosaxes + 6 squares 1/(2φ²) with Unborn Axes',
    sorted(g['U'].values()) == [6, 8] and all(sp.simplify(a - (hexA if kk == 'I' else 1 / (2 * ((1 + S5) / 2) ** 2))) == 0 for kk, a in g['U']))
# ---- the keyed network: validity of the signed boundaries ----
L0 = lotus((Z, Z, Z)); D0 = dodec(UC)
def inside_poly(p, P, n): return all(dot(cross(n, sub(P[(i + 1) % len(P)], P[i])), sub(p, P[i])).sign() >= 0 for i in range(len(P)))
def bases_in_hex(F, hexes):
    ok = True
    for s, n, P in F:
        if s < 0: ok &= sum(1 for hn, HP in hexes if coplanar_same((1, n, P), (1, hn, HP)) and all(inside_poly(p, turn(HP, hn), hn) for p in P)) == 1
    return ok
say('each Tricap base lies inside one hexagon of its piece (so hexagon − base is a true region)', bases_in_hex(L0, hexI) and bases_in_hex(D0, hexU))
def no_self_overlap(F):   # no two positive faces of one piece overlap in a common plane (side faces not on the hull, not on each other)
    pos = [f for f in F if f[0] > 0]
    for a, b in combinations(pos, 2):
        if coplanar_same(a, b) or coplanar_opp(a, b):
            R = inter(a[2], turn(b[2], a[1]), a[1])
            if len(R) >= 3 and dot(avec(R), a[1]).sign() != 0: return False
    return True
say('no Tricap side face lies on another face of its piece (Lotus Jewel Axes, Dodecaxes)', no_self_overlap(L0) and no_self_overlap(D0))
print('== keyed network (all keyed) ==')
kr = web(True, [('L', O3), ('D', U0)])
k = report(kr)
# the expected keyed bond: hexagon − base triangle + 3 Tricap side faces
(nb, B), Sd = tri_parts(TR[0])
tri_area = sp.simplify(sym(area_q(turn(B, nb), nb)[0]) / sp.sqrt(sym(dot(nb, nb))))
side_area = [sp.simplify(sym(area_q(turn(P, n), n)[0]) / sp.sqrt(sym(dot(n, n)))) for n, P in Sd]
keyhex = sp.simplify(hexA - tri_area + sum(side_area))
print(f'Tricap base (equilateral) area {sp.nsimplify(tri_area)} ≈ {float(tri_area):.10f}; side faces {[sp.nsimplify(x) for x in side_area]} ≈ {float(side_area[0]):.10f}')
print(f'keyed hexagon = hexagon − base + 3 sides = {sp.nsimplify(keyhex)} ≈ {float(keyhex):.10f}')
say('Lotus Jewel Axes: 8 keyed hexagons with Dodecaxes (hexagon − base + 3 side faces) + 6 squares 1/2 with Lotus Jewel Axes, nothing else',
    sorted(k['L'].values()) == [6, 8] and all(sp.simplify(a - (keyhex if kk == 'D' else sp.Rational(1, 2))) == 0 for kk, a in k['L']))
say('Dodecaxes: 8 keyed hexagons with Lotus Jewel Axes + 6 squares 1/(2φ²) with Dodecaxes, nothing else',
    sorted(k['D'].values()) == [6, 8] and all(sp.simplify(a - (keyhex if kk == 'L' else 1 / (2 * ((1 + S5) / 2) ** 2))) == 0 for kk, a in k['D']))
gb = web(False, [('I', O3), ('U', U0)])
REN = {'I': 'L', 'U': 'D'}
same_adj = all(set(kr[(REN[a], O3)][0]) == {(REN[x], m) for x, m in gb[(a, O3)][0]} for a in 'IU')
say('same adjacency as the golden pair: the same neighbours, bond for bond (no bond born or lost)', same_adj)
sI, sL = gb[('I', O3)][1], kr[('L', O3)][1]; sU, sD = gb[('U', U0)][1], kr[('D', U0)][1]
d8 = sp.simplify(8 * (sum(side_area) - tri_area))
say(f'surfaces: Lotus Jewel Axes − Icosaxes = Dodecaxes − Unborn Axes = 8(3 sides − base) = {sp.nsimplify(d8)} ≈ {float(d8):.10f}',
    sp.simplify(sL - sI - d8) == 0 and sp.simplify(sD - sU - d8) == 0)
print(f'surfaces: Icosaxes {sp.nsimplify(sI)}, Unborn Axes {sp.nsimplify(sU)}, Lotus Jewel Axes {sp.nsimplify(sL)}, Dodecaxes {sp.nsimplify(sD)}')
# closed forms: φ = (1+√5)/2, tan 36° = √(5 − 2√5)
ph = (1 + S5) / 2; t36 = sp.sqrt(5 - 2 * S5)
say('closed forms: Tricap base √3/4, side face (tan 36°)/4, keyed hexagon 3√3/(8φ) + (3/4) tan 36°, golden hexagon (√3/16)(1 + 3√5)',
    sp.simplify(tri_area - sp.sqrt(3) / 4) == 0 and all(sp.simplify(x - t36 / 4) == 0 for x in side_area) and sp.simplify(keyhex - (3 * sp.sqrt(3) / (8 * ph) + 3 * t36 / 4)) == 0)
say('closed forms: surfaces Icosaxes 3 + (√3/2)(1+3√5), Unborn Axes 3/φ² + (√3/2)(1+3√5), Lotus Jewel Axes 3 + 3√3/φ + 6 tan 36°, Dodecaxes 3/φ² + 3√3/φ + 6 tan 36°',
    all(sp.simplify(a - b) == 0 for a, b in [(sI, 3 + sp.sqrt(3) * (1 + 3 * S5) / 2), (sU, 3 / ph**2 + sp.sqrt(3) * (1 + 3 * S5) / 2),
        (sL, 3 + 3 * sp.sqrt(3) / ph + 6 * t36), (sD, 3 / ph**2 + 3 * sp.sqrt(3) / ph + 6 * t36)]))
print('ALL PASS' if ok_all else 'SOME FAIL', f'({npass} checks passed)')
