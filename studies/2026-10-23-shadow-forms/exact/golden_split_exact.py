# Golden split of the AXE, exact in Q(sqrt5): cone every AXE from the point at t = 1/phi on its axis (from the midpoint of its long
# edge, shared by two icosahedra, to the midpoint of its short edge, shared by two Unborns); each of its 4 pyramids joins the piece
# whose face it sits on. Claim: icosahedron + 12 pyramids and Unborn + 12 pyramids are both convex (union volume = hull volume),
# both truncated octahedra (8 hexagons, 6 squares), volumes sum to phi^3. Exact arithmetic only; floats used just to order face corners.
from fractions import Fraction as Fr
from itertools import combinations, product
import math
class Q5:
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def _c(o): return o if isinstance(o, Q5) else Q5(o)
    def __add__(s, o): o = Q5._c(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = Q5._c(o); return Q5(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return Q5._c(o) - s
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): o = Q5._c(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __eq__(s, o): o = Q5._c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) * (1 if a * a > 5 * b * b else -1)
    def __repr__(s): return f'({s.a} + {s.b}√5)'
PHI = Q5(Fr(1, 2), Fr(1, 2)); IPHI = PHI - 1; H = PHI * Fr(1, 2); T = IPHI   # T = 1/phi
add = lambda u, v: tuple(x + y for x, y in zip(u, v)); sub = lambda u, v: tuple(x - y for x, y in zip(u, v))
mul = lambda k, u: tuple(k * x for x in u); dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
cross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
det = lambda a, b, c: dot(a, cross(b, c))
cyc = lambda p: [p, (p[2], p[0], p[1]), (p[1], p[2], p[0])]
Z = Q5(0); HALF = Q5(Fr(1, 2))
ICO = [q for s1 in (1, -1) for s2 in (1, -1) for q in cyc((Z, s1 * HALF, s2 * H))]
UC = (H, H, H)
UNB = [add(UC, q) for s1 in (1, -1) for s2 in (1, -1) for q in cyc((s1 * H, s2 * IPHI * Fr(1, 2), Z))]
AXE0 = [(-HALF, H, Z), (HALF, H, Z), (Z, H + IPHI * Fr(1, 2), H), (Z, H - IPHI * Fr(1, 2), H)]
fails = 0
def check(label, ok):
    global fails; fails += not ok; print(('PASS ' if ok else 'FAIL ') + label)
# all AXEs near the origin cell: cyclic turns and sign flips of AXE0, then lattice slides
key = lambda V: frozenset(V)
AX = {}
for k in range(3):
    for sg in product((1, -1), repeat=3):
        V = [tuple(sg[i] * (cyc(v)[k][i]) for i in range(3)) for v in AXE0]
        for sl in product((-1, 0, 1), repeat=3):
            W = [add(v, mul(PHI, tuple(Q5(x) for x in sl))) for v in V]
            AX[key(W)] = W
print('AXEs generated:', len(AX))
def padded(base):
    S = set(base); pyr = []
    for W in AX.values():
        for f in combinations(range(4), 3):
            if all(W[i] in S for i in f):
                o = [i for i in range(4) if i not in f][0]
                long_mid = mul(HALF, add(W[0], W[1])); short_mid = mul(HALF, add(W[2], W[3]))
                p = add(long_mid, mul(T, sub(short_mid, long_mid)))
                pyr.append(([W[i] for i in f], p))
    return pyr
def hull_facets(P):
    F = {}
    for a, b, c in combinations(range(len(P)), 3):
        n = cross(sub(P[b], P[a]), sub(P[c], P[a]))
        if all(x == 0 for x in n): continue
        d = [dot(n, sub(q, P[a])).sign() for q in P]
        if all(x <= 0 for x in d) or all(x >= 0 for x in d):
            on = frozenset(i for i, x in enumerate(d) if x == 0)
            F[on] = n if all(x <= 0 for x in d) else mul(-1, n)
    return F
def poly_volume(P, F):   # fan each facet from its first corner, cone from the centroid-ish point P[0]
    c = P[0]; v = Q5(0)
    for on, n in F.items():
        idx = list(on); cen = [sum(float(P[i][k]) for i in idx) / len(idx) for k in range(3)]
        nf = [float(x) for x in n]; u = [float(P[idx[0]][k]) - cen[k] for k in range(3)]
        w = [nf[1] * u[2] - nf[2] * u[1], nf[2] * u[0] - nf[0] * u[2], nf[0] * u[1] - nf[1] * u[0]]
        ang = lambda i: math.atan2(sum((float(P[i][k]) - cen[k]) * w[k] for k in range(3)), sum((float(P[i][k]) - cen[k]) * u[k] for k in range(3)))
        idx.sort(key=ang)
        for j in range(1, len(idx) - 1):
            v = v + det(sub(P[idx[0]], c), sub(P[idx[j]], c), sub(P[idx[j + 1]], c))
    return v * Fr(1, 6) if v.sign() > 0 else v * Fr(-1, 6)
results = {}
for name, base in [('icosahedron', ICO), ('Unborn', UNB)]:
    pyr = padded(base)
    check(f'{name}: 12 AXE faces lie on it, so it takes 12 pyramids (found {len(pyr)})', len(pyr) == 12)
    PB = list(base); FB = hull_facets(PB); vb = poly_volume(PB, FB)
    vp = sum((abs_ := det(sub(f[0], p), sub(f[1], p), sub(f[2], p))) * (Fr(1, 6) if abs_.sign() > 0 else Fr(-1, 6)) for f, p in pyr)
    union = vb + vp
    P = list(dict.fromkeys(list(base) + [p for _, p in pyr])); F = hull_facets(P); vh = poly_volume(P, F)
    check(f'{name} + 12 pyramids is convex: union volume {union} = hull volume {vh} (exact)', union == vh)
    corners = set(i for on in F for i in on)
    sizes = sorted(len(on) for on in F)
    check(f'{name} + pyramids: {len(corners)} corners (want 24), {len(F)} faces (want 14): {sizes.count(6)} hexagons, {sizes.count(4)} squares',
          len(corners) == 24 and len(F) == 14 and sizes.count(6) == 8 and sizes.count(4) == 6)
    e2 = set()
    for on in F:
        idx = list(on)
        for a, b in combinations(idx, 2):
            # an edge = a pair shared by exactly two facets
            if sum(1 for o2 in F if a in o2 and b in o2) == 2: e2.add((len(on), dot(sub(P[a], P[b]), sub(P[a], P[b]))))
    print('   squared edge lengths by face size:', sorted((k, repr(v), float(v)) for k, v in e2))
    hexes = []
    for on in F:
        if len(on) == 6:
            idx = list(on); hexes.append(tuple(sorted((dot(sub(P[a], P[b]), sub(P[a], P[b])) for a, b in combinations(idx, 2)), key=float)))
    check(f'{name}: its 8 hexagons are congruent to each other (all 15 corner-to-corner distances match)', len(set(hexes)) == 1)
    # Koca 2015 eq. (49) / Polytope Wiki semi-uniform truncated octahedron: corners = full orbit of (p, q, 0) under all sign changes and orders
    C = [P[i] for i in sorted(corners)]
    p_, q_ = (HALF, H) if name == 'icosahedron' else (IPHI * Fr(1, 2), H)
    orbit = {tuple(sg[k] * perm[k] for k in range(3)) for perm in {(p_, q_, Z), (p_, Z, q_), (q_, p_, Z), (q_, Z, p_), (Z, p_, q_), (Z, q_, p_)}
             for sg in product((1, -1), repeat=3)}
    rel = {sub(c, (Z, Z, Z) if name == 'icosahedron' else UC) for c in C}
    check(f'{name} + pyramids: its 24 corners are exactly the orbit of ({p_}, {q_}, 0) under all sign changes and orders (full octahedral symmetry; Koca 2015 eq. 49 with x = {"φ" if name == "icosahedron" else "φ²"})', rel == orbit)
    apices = {sub(p, (Z, Z, Z) if name == 'icosahedron' else UC) for _, p in pyr}
    own = {sub(q, (Z, Z, Z) if name == 'icosahedron' else UC) for q in base}
    mirror = {(y, x, z) for x, y, z in own}
    check(f'{name}: the 12 AXE pyramid tips are exactly the corners of its mirror image (x <-> y)', apices == mirror)
    results[name] = (union, e2, hexes[0])
    unused = [q for q in base if P.index(q) not in corners]
    print(f'   {name}: {len(unused)} of its own corners are no longer corners (they lie in faces)')
tot = results['icosahedron'][0] + results['Unborn'][0]
check(f'volumes {results["icosahedron"][0]} + {results["Unborn"][0]} = {tot} = phi^3 {PHI * PHI * PHI}', tot == PHI * PHI * PHI)
hexa = lambda r: sorted(float(v) for k, v in r[1] if k == 6)
check('the hexagons of both pieces have the same side lengths (squared: 1/2 and (3 - √5)/4)', set(results['icosahedron'][1]) & set(results['Unborn'][1]) and
      {v for k, v in results['icosahedron'][1] if k == 6} == {v for k, v in results['Unborn'][1] if k == 6})
check('the hexagon of the padded icosahedron is congruent to that of the padded Unborn (all 15 corner distances)', results['icosahedron'][2] == results['Unborn'][2])
# Lotus Jewel network: the 8 Tricaps (exact volume (3 - √5)/24 each, axe-gap study) move from the icosahedron side to the dodecahedron side
VT8 = Q5(Fr(3, 24), Fr(-1, 24)) * 8
big_k = results['icosahedron'][0] - VT8; small_k = results['Unborn'][0] + VT8
check(f'Lotus Jewel network, golden split: big keyed piece (Jewel + 12 pyramids) volume {big_k} = √5', big_k == Q5(0, 1))
check(f'small keyed piece (dodecahedron + 12 pyramids) volume {small_k} = 2', small_k == Q5(2))
print('ALL PASS' if fails == 0 else f'{fails} FAIL')
