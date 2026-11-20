"""Proper round, part 1: exact local analysis around one C1 (truncated icosahedron, edge 1, with a dodecahedron centre pyramid on
each pentagon).  Basis pi, beta = arccos(1/sqrt6) (independent over Q: packet-leads-tiling).  Angles are pairs (p,b) = p*pi + b*beta.
Sections: controls; C1 face angles at a truncated-icosahedron vertex v; face-to-face lemmas; hexagon graph; ring alphabet enumeration;
the leftover polygon L at v when a hexagon is shared with a second C1.  Run: python round_local.py  (writes data/round_local.json)"""
import itertools, json, math
from fractions import Fraction as F
import sympy as sp
import mpmath as mp
mp.mp.dps = 50
out = {}; OK = True
def pr(s): print(s, flush=True)
def chk(name, cond):
    global OK
    OK = OK and bool(cond); pr(f"  [{'pass' if cond else 'FAIL'}] {name}"); out.setdefault('checks', []).append([name, bool(cond)])
pi = sp.pi; phi = (1 + sp.sqrt(5)) / 2
be = sp.acos(1 / sp.sqrt(6)); BE = float(sp.N(be, 30))
deg = lambda v: (float(v[0]) * math.pi + float(v[1]) * BE) * 180 / math.pi
P = lambda p, b: (F(p), F(b))
add = lambda *vs: (sum(v[0] for v in vs), sum(v[1] for v in vs))
neg = lambda v: (-v[0], -v[1])
hh, r, s = P(F(3, 2), -2), P(F(3, 4), 1), P(F(2, 3), 0)          # C1 interior dihedrals: hexagon-hexagon, reflex, pyramid side-side
tq = P(F(-1, 4), 1)                                               # t' = beta - pi/4
pr("== controls (framework: ring sum 2pi, vertex areas sum 4pi)")
th = sp.acos(sp.Rational(1, 3))
chk("octet ring: 2 tetra + 2 octa dihedrals = 2pi", sp.simplify(2 * th + 2 * (pi - th) - 2 * pi) == 0)
chk("octet vertex: 8 tetra + 6 octa vertex figures = 4pi", sp.simplify(8 * (3 * th - pi) + 6 * (4 * (pi - th) - 2 * pi) - 4 * pi) == 0)
# known non-filler: regular dodecahedron alone, dihedral 2*alpha, alpha/pi irrational (packet-leads-tiling) -> n*2alpha = 2pi impossible
al = sp.atan(phi)
c2a = sp.radsimp((1 - phi**2) / (1 + phi**2))   # cos(2 alpha), alpha = arctan(phi)
assert abs(sp.N(c2a - sp.cos(2 * al), 50)) < 1e-45
mpoly = sp.minimal_polynomial(2 * c2a, sp.Symbol('x'))
chk("non-filler: dodecahedron dihedral 2alpha is not a rational multiple of pi (2cos(2alpha) not an algebraic integer: minpoly %s)" % mpoly,
    sp.Poly(mpoly).LC() != 1)
pr("== C1 at a truncated-icosahedron vertex v")
Rd = sp.sqrt(3) * phi / 2                                         # pyramid lateral edge = dodecahedron circumradius (edge 1)
cb = sp.Rational(1, 2) / Rd
chk("spike triangle base angle = 3pi/4 - beta (cos = 1/(sqrt3 phi))", sp.simplify(sp.radsimp(cb - sp.cos(3 * pi / 4 - be).rewrite(sp.sqrt))) == 0 or
    abs(sp.N(cb - sp.cos(3 * pi / 4 - be), 60)) < 1e-55)
chk("spike triangle apex angle = 2beta - pi/2", abs(sp.N(pi - 2 * (3 * pi / 4 - be) - (2 * be - pi / 2), 60)) < 1e-55)
Xc = [neg(add(hh, P(-2, 0))), neg(add(r, P(-2, 0))), neg(add(s, P(-2, 0))), neg(add(r, P(-2, 0)))]
areaX = add(*Xc, P(-2, 0))
chk(f"leftover X at v: corners {[round(deg(c),4) for c in Xc]}, area (pi-part, beta-part) = ({areaX[0]},{areaX[1]}) = 7pi/3", areaX == P(F(7, 3), 0))
out['X'] = dict(corners=[[str(x) for x in c] for c in Xc], sides_deg=[120, 69.0948, 69.0948, 120], area="7pi/3")
pr("== face-to-face lemmas (faces meet in whole faces)")
# B1: two C1 sharing a spike triangle: the triangle is isosceles (legs Rd > base 1), so base goes to base: two reflex edges on one edge
chk("B1: two C1 on one spike triangle put two reflex edges on its base: 2(3pi/4+beta) > 2pi (beta > pi/4)", 2 * deg(r) > 360 and BE > math.pi / 4)
# B2: two C1 sharing a hexagon: edge types alternate hh, r; an isometry of the hexagon either keeps the alternation (r on r) or swaps it (hh on r)
chk("B2: hexagon shared with types kept: r + r > 2pi (overlap)", 2 * deg(r) > 360)
w = add(P(2, 0), neg(hh), neg(r))
chk(f"B2: hexagon shared with types swapped: each of the 6 edges leaves a wedge 2pi - hh - r = ({w[0]},{w[1]}) = beta - pi/4 = {deg(w):.4f} deg", w == tq)
pr("== hexagon graph of C1 (hexagons adjacent across hexagon-hexagon edges)")
cyc = lambda t: [(t[0], t[1], t[2]), (t[2], t[0], t[1]), (t[1], t[2], t[0])]
icos = set()
for a_, b_ in itertools.product((1, -1), repeat=2):
    for c in cyc((0, a_, b_ * phi)): icos.add(c)
icos = [sp.Matrix(c) for c in icos]; assert len(icos) == 12
tris = [t for t in itertools.combinations(range(12), 3) if all(sp.simplify((icos[i] - icos[j]).norm() - 2) == 0 for i, j in itertools.combinations(t, 2))]
assert len(tris) == 20   # hexagons of the truncated icosahedron <-> icosahedron faces; hh edges <-> icosahedron edges
adj = {i: [j for j in range(20) if j != i and len(set(tris[i]) & set(tris[j])) == 2] for i in range(20)}
best = 0
for mask in range(1 << 20):
    if bin(mask).count('1') <= best: continue
    if all(not (mask >> j & 1) for i in range(20) if mask >> i & 1 for j in adj[i]): best = bin(mask).count('1')
chk(f"hexagon graph is cubic on 20 nodes (dodecahedral), largest independent set = {best}", all(len(v) == 3 for v in adj.values()) and best == 8)
out['hexagons'] = dict(max_shared_with_C1=best, min_K_hexagon_faces_per_C1=20 - best)
# B3: at a hh edge, both hexagons shared with C1 copies gives hh + r + r > 2pi
chk("B3: the two hexagons at a hh edge cannot both be shared with C1 copies: hh + 2r > 2pi", deg(hh) + 2 * deg(r) > 360)
pr("== ring alphabet (scope): K dihedrals are p*pi + b*beta with b in {-1,0,1}; b=+-1: p in Z/4 (the side-plane angles T, B, t', pi-t' and pi-shifts); b=0: p in Z/12")
alph = [P(F(k, 4), b) for b in (1, -1) for k in range(-4, 12)] + [P(F(k, 12), 0) for k in range(1, 24) if k != 12]
alph = [a for a in alph if 0 < deg(a) < 360 and abs(deg(a) - 180) > 1e-9]
conv = [a for a in alph if deg(a) < 180]
out['alphabet'] = dict(beta_items=[[str(a[0]), int(a[1]), round(deg(a), 4)] for a in alph if a[1] != 0], rational_step="pi/12")
def splits(target, items, first_fixed=(), maxn=4):
    """multisets of alphabet items (after the fixed ones) with exact sum = target"""
    rem = add(target, *[neg(x) for x in first_fixed]) if first_fixed else target
    res = []
    def rec(start, cur, left, n):
        if left == (0, 0): res.append(tuple(cur)); return
        if n == maxn or deg(left) <= 1e-9: return
        for i in range(start, len(items)):
            it = items[i]
            if deg(it) <= deg(left) + 1e-9: rec(i, cur + [it], add(left, neg(it)), n + 1)
    rec(0, [], rem, 0)
    return res
ring = {}
for name, items in (("convex K", conv), ("non-convex K", alph)):
    R = {}
    # reflex edge r, hexagon side shared with C1' (contributes hh): the K on the spike triangle and any others fill 2pi - r - hh
    R['r | hexagon on C1'] = splits(add(P(2, 0), neg(r), neg(hh)), items)
    # reflex edge r, hexagon side a K face: K_tri + K_hex + others fill 2pi - r (count pairs (K_tri, K_hex) and the rest)
    rr = splits(add(P(2, 0), neg(r)), items, maxn=4); R['r | hexagon on K'] = [x for x in rr if len(x) >= 2]
    # hh edge with one hexagon shared with C1' (contributes r): rest fills 2pi - hh - r
    R['hh | one hexagon on C1'] = splits(add(P(2, 0), neg(hh), neg(r)), items)
    rr = splits(add(P(2, 0), neg(hh)), items, maxn=4); R['hh | both hexagons on K'] = [x for x in rr if len(x) >= 2]
    rr = splits(add(P(2, 0), neg(s)), items, maxn=4); R['s | both spike triangles on K'] = [x for x in rr if len(x) >= 2]
    ring[name] = {k: dict(count=len(v), beta_signatures=sorted({tuple(sorted(int(i[1]) for i in x)) for x in v}),
                          examples=[[round(deg(i), 4) for i in x] for x in v[:6]]) for k, v in R.items()}
    for k, v in R.items(): pr(f"  {name:13s} {k:32s}: {len(v)} fillings; beta signatures {ring[name][k]['beta_signatures'][:8]}")
    if name == "convex K":
        forced = R['r | hexagon on C1'] == [(tq,)] and R['hh | one hexagon on C1'] == [(tq,)]
        chk("FORCED (both alphabets): where a hexagon is shared with C1', each wedge is ONE K edge of dihedral t' = beta - pi/4 (20.9052 deg)", forced)
    else:
        chk("same with non-convex K", R['r | hexagon on C1'] == [(tq,)] and R['hh | one hexagon on C1'] == [(tq,)])
out['rings'] = ring
pr("== the leftover L at v when hexagon H1 at v is shared with C1' (types swapped)")
TV = set()
for b in [(0, 1, 3 * phi), (1, 2 + phi, 2 * phi), (phi, 2, 2 * phi + 1)]:
    for sg in itertools.product((1, -1), repeat=3):
        t = tuple(sg[i] * b[i] for i in range(3))
        for c in cyc(t): TV.add(tuple(sp.nsimplify(x / 2) for x in c))
TVn = [mp.matrix([mp.mpf(sp.N(x, 60)) for x in v]) for v in TV]; assert len(TVn) == 60
nrm = lambda u: mp.sqrt(sum(x * x for x in u))
def unit(u): n = nrm(u); return u / n
def dot(u, v): return sum(u[i] * v[i] for i in range(3))
def cross(u, v): return mp.matrix([u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]])
v0 = TVn[0]
nb = sorted([q for q in TVn if abs(nrm(q - v0) - 1) < mp.mpf(10) ** -40], key=lambda q: float(q[0] + 2 * q[1] + 3 * q[2]))
assert len(nb) == 3
# pentagon at v0: its centre direction; apex = dodecahedron centre
pdirs = []
for a_, b_ in itertools.product((1, -1), repeat=2):
    for c in cyc((0, a_, b_ * phi)): pdirs.append(unit(mp.matrix([mp.mpf(sp.N(x, 60)) for x in c])))
pd = max(pdirs, key=lambda d: dot(d, v0))
pent = sorted([q for q in TVn if abs(dot(q, pd) - dot(v0, pd)) < mp.mpf(10) ** -40], key=lambda q: 0)
cen = sum(pent, mp.matrix([0, 0, 0])) / 5
hgt = mp.sqrt(mp.mpf(sp.N(Rd ** 2, 60)) - nrm(v0 - cen) ** 2)
apex = cen + hgt * pd
inpent = [q for q in nb if abs(dot(q, pd) - dot(v0, pd)) < mp.mpf(10) ** -40]; hhn = [q for q in nb if q not in inpent][0]
e_hh, e_r1, e_r2, e_s = unit(hhn - v0), unit(inpent[0] - v0), unit(inpent[1] - v0), unit(apex - v0)
# H1 = hexagon containing v0, hhn, inpent[0]; normal
hex1 = [q for q in TVn if abs(dot(cross(hhn - v0, inpent[0] - v0), q - v0)) < mp.mpf(10) ** -40]
assert len(hex1) == 6
hc = sum(hex1, mp.matrix([0, 0, 0])) / 6; hn = unit(hc)
def refl(x): return x - 2 * dot(x - hc, hn) * hn            # reflection in the H1 plane
def rot60(x):                                                # rotation by 60 deg about the H1 axis
    y = x - hc; a_ = dot(y, hn) * hn; b_ = y - a_; c_ = cross(hn, b_)
    return hc + a_ + b_ * mp.cos(mp.pi / 3) + c_ * mp.sin(mp.pi / 3)
img = lambda x: rot60(refl(x))
# C1' edge directions at v0: images of C1 edges at the vertex u that maps to v0
src = min(TVn, key=lambda q: nrm(img(q) - v0)); assert nrm(img(src) - v0) < mp.mpf(10) ** -40
nbs = [q for q in TVn if abs(nrm(q - src) - 1) < mp.mpf(10) ** -40]
pd2 = max(pdirs, key=lambda d: dot(d, src)); pent2 = [q for q in TVn if abs(dot(q, pd2) - dot(src, pd2)) < mp.mpf(10) ** -40]
cen2 = sum(pent2, mp.matrix([0, 0, 0])) / 5; apex2 = cen2 + hgt * pd2
ins2 = [q for q in nbs if q in pent2]; hh2 = [q for q in nbs if q not in pent2][0]
E2 = dict(hh=unit(img(hh2) - v0), r1=unit(img(ins2[0]) - v0), r2=unit(img(ins2[1]) - v0), s=unit(img(apex2) - v0))
coinc = lambda a_, b_: nrm(a_ - b_) < mp.mpf(10) ** -30
pr(f"  C1' hh edge on a C1 reflex edge: {any(coinc(E2['hh'], e) for e in (e_r1, e_r2))};  C1' reflex edge on the C1 hh edge: {any(coinc(E2[k], e_hh) for k in ('r1','r2'))}")
# L corners: C1 rays e_r (not in H1), e_s, then the shared ray e_r(H1), C1' rays, ...
eH = e_r1 if any(coinc(E2['hh'], e) for e in (e_r1,)) else e_r2      # C1 reflex ray in H1 (carries C1' hh)
eO = e_r2 if eH is e_r1 else e_r1
c2r = [E2[k] for k in ('r1', 'r2') if not coinc(E2[k], e_hh)][0]
Lrays = [eO, e_s, eH, c2r, E2['s'], e_hh]
ang = lambda a_, b_: mp.acos(dot(a_, b_)) * 180 / mp.pi
sides = [ang(Lrays[i], Lrays[(i + 1) % 6]) for i in range(6)]
pr("  L rays: C1 reflex, C1 spike edge, shared ray (C1 reflex + C1' hh), C1' reflex, C1' spike edge, shared ray (C1 hh + C1' reflex)")
pr("  L sides (deg): " + ", ".join(mp.nstr(x, 10) for x in sides))
Lc = [neg(add(r, P(-2, 0))), neg(add(s, P(-2, 0))), tq, neg(add(r, P(-2, 0))), neg(add(s, P(-2, 0))), tq]
aL = add(*Lc, P(-4, 0))
chk(f"L corners {[round(deg(c),4) for c in Lc]}: area = ({aL[0]},{aL[1]}) = 2pi/3", aL == P(F(2, 3), 0))
# which sides of L can be the top (or bottom) face side of ONE scutoid vertex figure equal to L: L must lie in the closed hemisphere
hemi = []
for i in range(6):
    nn = unit(cross(Lrays[i], Lrays[(i + 1) % 6]))
    sg = [dot(nn, Lrays[j]) for j in range(6) if j not in (i, (i + 1) % 6)]
    one = all(x > mp.mpf(10) ** -20 for x in sg) or all(x < -mp.mpf(10) ** -20 for x in sg)
    hemi.append(dict(side=i, face=['spike triangle', 'spike triangle', "C1' hexagon", "C1' spike triangle", "C1' spike triangle", 'C1 hexagon'][i],
                     L_in_one_hemisphere=bool(one), min_abs_margin=float(min(abs(x) for x in sg))))
    pr(f"  side {i} ({hemi[-1]['face']}): L in one closed hemisphere: {one} (smallest |margin| {float(min(abs(x) for x in sg)):.4f})")
out['L'] = dict(corners_deg=[round(deg(c), 4) for c in Lc], sides_deg=[float(x) for x in sides], area="2pi/3", hemisphere_test=hemi)
json.dump(out, open('data/round_local.json', 'w'), indent=1)
pr("FINAL ok" if OK else "FINAL FAIL")
