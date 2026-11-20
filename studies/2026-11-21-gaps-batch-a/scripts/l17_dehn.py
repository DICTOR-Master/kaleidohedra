# l17_dehn.py -- item L17 (#51: "one solid per bond that fills alone"): the Dehn screen of the pieces of the three DICTONIC BONDS and of the
# families they sit in, with dehn_mp.py (studies 2026-11-19-dehn-words / dehn-atoms, copied unchanged, sha256 396d9f2e...9217).
# Dehn invariant zero is necessary for a solid to fill space alone (Debrunner 1980); nonzero rules it out.
# Pieces are built EXACTLY (Q or Q(sqrt5), Fraction arithmetic; exact volume checks), then handed to dehn_mp at 80 digits.
# A solid glued from convex parts is screened as the disjoint union of its parts (the Dehn invariant is additive: Dehn(A u B) = Dehn(A) +
# Dehn(B) when A and B meet only on their boundaries); dehn_mp reads edges by corner index, so parts never interact.
# Lattice relation used as a control: when pieces P1..Pk with one copy of each per lattice cell fill space, the cell is scissors-congruent to
# their union (any two fundamental domains of one lattice are equidecomposable by translations), and a cube has Dehn invariant 0, so the
# Dehn invariants of one cell's pieces add to 0. dehn_mp must find ZERO for every whole cell, at every parameter.
# Parts (one per call, each under 280 s):  cal | delian | factorx | golden | keyed
# Usage: python -u l17_dehn.py <part> <out json>                      Study 2026-11-21-gaps-batch-a.
import sys, os, json, itertools, time
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
import dehn_mp as D
from mpmath import mpf, sqrt, nstr
PART, OUT = sys.argv[1:3]; T0 = time.time()
R5 = sqrt(5)
fails = []; out = []
def check(label, ok):
    print(('PASS ' if ok else 'FAIL ') + label, flush=True)
    if not ok: fails.append(label)

# ---- exact Q(sqrt5) arithmetic (as in shadow-forms/exact/golden_split_exact.py) ----
class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def _c(o): return o if isinstance(o, Q5) else Q5(o)
    def __add__(s, o): o = Q5._c(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = Q5._c(o); return Q5(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return Q5._c(o) - s
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): o = Q5._c(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = Q5._c(o); n = o.a * o.a - 5 * o.b * o.b; return Q5((s.a * o.a - 5 * s.b * o.b) / n, (s.b * o.a - s.a * o.b) / n)
    def __rtruediv__(s, o): return Q5._c(o) / s
    def __eq__(s, o): o = Q5._c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        return (1 if a > 0 else -1) * (1 if a * a > 5 * b * b else -1)
    def mp(s): return mpf(s.a.numerator) / s.a.denominator + mpf(s.b.numerator) / s.b.denominator * R5
    def __repr__(s): return f'{s.a} + {s.b}*sqrt5' if s.b else f'{s.a}'
add = lambda u, v: tuple(x + y for x, y in zip(u, v)); sub = lambda u, v: tuple(x - y for x, y in zip(u, v))
mul = lambda k, u: tuple(k * x for x in u); dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
cross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
det = lambda a, b, c: dot(a, cross(b, c))
def tomp(P): return [[x.mp() if isinstance(x, Q5) else mpf(x.numerator) / x.denominator for x in p] for p in P]

def hull_exact(P):
    """facets of a convex hull, exact: (set of on-facet indices, outward normal)"""
    F = {}
    for a, b, c in itertools.combinations(range(len(P)), 3):
        n = cross(sub(P[b], P[a]), sub(P[c], P[a]))
        if all(Q5._c(x) == 0 for x in n): continue
        d = [Q5._c(dot(n, sub(q, P[a]))).sign() for q in P]
        if all(x <= 0 for x in d) or all(x >= 0 for x in d):
            on = frozenset(i for i, x in enumerate(d) if x == 0)
            if on not in F: F[on] = n if all(x <= 0 for x in d) else mul(-1, n)
    return F
def volume(P):
    """exact volume of a convex point set: cone from an interior point over fan-triangulated facets (corner order from the facet's own
    exact angular sort is not needed: the facet is split by its centroid into triangles in float order, volumes added exactly)"""
    F = hull_exact(P); c = tuple(sum((Q5._c(p[k]) for p in P), Q5(0)) / len(P) for k in range(3)); v = Q5(0)
    import math
    for on, n in F.items():
        idx = list(on); cen = [sum(float(Q5._c(P[i][k]).mp()) for i in idx) / len(idx) for k in range(3)]
        nf = [float(Q5._c(x).mp()) for x in n]; u = [float(Q5._c(P[idx[0]][k]).mp()) - cen[k] for k in range(3)]
        w = [nf[1] * u[2] - nf[2] * u[1], nf[2] * u[0] - nf[0] * u[2], nf[0] * u[1] - nf[1] * u[0]]
        idx.sort(key=lambda i: math.atan2(sum((float(Q5._c(P[i][k]).mp()) - cen[k]) * w[k] for k in range(3)), sum((float(Q5._c(P[i][k]).mp()) - cen[k]) * u[k] for k in range(3))))
        for j in range(1, len(idx) - 1):
            v = v + Q5._c(det(sub(P[idx[0]], c), sub(P[idx[j]], c), sub(P[idx[j + 1]], c)))
    return v * Fr(1, 6) if v.sign() > 0 else v * Fr(-1, 6)
def vertices_from_halfspaces(H):
    """corners of {x : n.x <= d for (n, d) in H}, exact (Fractions): every triple of planes, kept if inside all"""
    V = []
    for (n1, d1), (n2, d2), (n3, d3) in itertools.combinations(H, 3):
        M = [list(n1), list(n2), list(n3)]; dt = det(*M)
        if dt == 0: continue
        x = tuple(det(*[[(d1, d2, d3)[r] if k == j else M[r][k] for k in range(3)] for r in range(3)]) / dt for j in range(3))
        if all(dot(n, x) <= d for n, d in H) and x not in V: V.append(x)
    return V

def screen(name, parts, note='', want=None):
    """Dehn invariant of the union of convex parts (lists of exact points), by dehn_mp.dehn on their disjoint union"""
    V, F = [], []
    for P in parts:
        Pm = tomp(P); f = D.hull_faces(Pm); F += [[i + len(V) for i in fc] for fc in f]; V += Pm
    r = D.dehn(V, F, name); r['note'] = note; r['parts'] = len(parts)
    if want: r['want'] = want; check(f"{name}: {r['verdict']} (want {want}); dihedrals {r['distinct_dihedrals']}, independent {r['independent_mod_pi']}, max coefficient sum {r['max_coefficient_sum']}", r['verdict'] == want)
    else: print(f"     {name}: {r['verdict']}; dihedrals {r['distinct_dihedrals']}, independent mod pi {r['independent_mod_pi']}, rational {r['rational_pi_dihedrals_deg']}, max coefficient sum {r['max_coefficient_sum']}, {round(time.time() - T0)} s", flush=True)
    out.append(r); json.dump(out, open(OUT, 'w'), indent=1); return r

if PART == 'cal':
    # dehn_mp's own calibration, unchanged (11 solids: zero cube, RD, TO, RT, both golden rhombohedra, RD centre pyramid; nonzero T, O, I, D)
    CAL = D.CAL + [('RD centre pyramid over one rhombus', [D.M(0, 0, 0), D.M(2, 0, 0), D.M(1, 1, 1), D.M(0, 2, 0), D.M(1, 1, -1)], 'ZERO')]
    for nm, V, want in CAL:
        r = D.dehn(V, D.hull_faces(V), nm); r['want'] = want; out.append(r)
        check(f'calibration {nm}: {r["verdict"]} (want {want})', r['verdict'] == want)
    # union mode controls: two cubes side by side = a brick (zero); tetrahedron + octahedron (nonzero); 2 tetrahedra + 1 octahedron of the
    # octet (one cell of the octet: zero, the lattice relation)
    cube = [tuple(Fr(x) for x in v) for v in itertools.product((0, 1), repeat=3)]
    screen('union control: two unit cubes (a brick)', [cube, [add(v, (Fr(1), Fr(0), Fr(0))) for v in cube]], want='ZERO')
    T1 = [(Fr(1), Fr(0), Fr(0)), (Fr(0), Fr(1), Fr(0)), (Fr(0), Fr(0), Fr(1)), (Fr(1), Fr(1), Fr(1))]
    OCT = [tuple(Fr(s) if i == k else Fr(0) for i in range(3)) for k in range(3) for s in (1, -1)]
    screen('union control: one tetrahedron + one octahedron of the octet', [T1, OCT], want='NONZERO')
    screen('union control: one octet cell, 2 tetrahedra + 1 octahedron (the lattice relation)', [T1, [mul(-1, v) for v in T1], OCT], want='ZERO')

if PART == 'delian':
    # #51 frame: octet edge sqrt2, octahedron |x|+|y|+|z| <= 1 at the origin, the tetrahedron (1,0,0),(0,1,0),(0,0,1),(1,1,1), centre (1/2,1/2,1/2).
    # O(t) = RD n IS {+-x+-y+-z <= 3(1 - t)/2}; T(t): for t <= 1/3 the tetrahedron scaled 3t about its centre; for t >= 1/3 the cube [0,1]^3
    # with its 4 octahedron-centre corners cut: x+y+z >= a, (1-x)+(1-y)+z >= a, (1-x)+y+(1-z) >= a, x+(1-y)+(1-z) >= a, a = 3(1 - t)/2.
    RD = [((Fr(s1), Fr(s2), Fr(0)), Fr(1)) for s1 in (1, -1) for s2 in (1, -1)]
    RD = [(tuple(n[p[i]] for i in range(3)), d) for n, d in RD for p in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]]
    def O_(t):
        return vertices_from_halfspaces(RD + [((Fr(a), Fr(b), Fr(c)), Fr(3) * (1 - t) / 2) for a in (1, -1) for b in (1, -1) for c in (1, -1)])
    cT = (Fr(1, 2),) * 3
    def T_(t):
        if t <= Fr(1, 3): return [add(cT, mul(3 * t, sub(v, cT))) for v in [(Fr(1), Fr(0), Fr(0)), (Fr(0), Fr(1), Fr(0)), (Fr(0), Fr(0), Fr(1)), (Fr(1), Fr(1), Fr(1))]]
        a = Fr(3) * (1 - t) / 2; one = Fr(1)
        H = [((one, 0, 0), one), ((-one, 0, 0), 0), ((0, one, 0), one), ((0, -one, 0), 0), ((0, 0, one), one), ((0, 0, -one), 0),
             ((-one, -one, -one), -a), ((one, one, -one), 2 - a), ((one, -one, one), 2 - a), ((-one, one, one), 2 - a)]
        return vertices_from_halfspaces([(tuple(Fr(x) for x in n), Fr(d)) for n, d in H])
    VT = Fr(1, 3)      # the octet tetrahedron's volume at edge sqrt2 (= sqrt2^3 sqrt2/12); octahedron 4/3
    for t in (Fr(1, 10), Fr(1, 5), Fr(1, 3), Fr(2, 5), Fr(1, 2), Fr(3, 5), Fr(4, 5), Fr(9, 10)):
        O, T = O_(t), T_(t); vO, vT = volume(O), volume(T)
        a = Fr(3) * (1 - t) / 2
        wantT = 27 * t ** 3 * VT if t <= Fr(1, 3) else (3 - 2 * a ** 3) * VT
        wantO = (6 - 54 * t ** 3) * VT if t <= Fr(1, 3) else 4 * a ** 3 * VT
        check(f'Delian t = {t}: exact volumes T(t) {vT}, O(t) {vO} as #51 Main theorem; 2 T + O = 2 octet tetrahedra + 1 octahedron = 2', vT == wantT and vO == wantO and 2 * vT + vO == 2)
        screen(f'Delian T(t), t = {t}', [T], 'tetrahedron piece')
        screen(f'Delian O(t), t = {t}', [O], 'octahedron piece')
        screen(f'Delian cell 2 T(t) + O(t), t = {t}', [T, [sub((Fr(1), Fr(1), Fr(1)), v) for v in T], O], 'lattice relation', want='ZERO')
    screen('Delian t = 0: O(0) = the rhombic dodecahedron', [O_(Fr(0))], 'end', want='ZERO')
    screen('Delian t = 1: T(1) = the cube', [T_(Fr(1))], 'end', want='ZERO')
    # the Delian bond itself, t_D = 1 - (2/3) 2^(-1/3), is not in Q(sqrt5): Samson and Delilah were screened in dehn-atoms (D71 Samson
    # NONZERO, Delilah NONZERO); the exact argument below covers every t.

if PART == 'factorx':
    # #48 Theorem 4: T(x) = hull of the signed orders of (1 + x, x, 0); the golden pair x = tau (Icosaxes) and its partner T(1/x) scaled by x
    # (Unborn Axes at x = tau); Kelvin's cell x = 1; the DICTO 1:2 and 2:1 Truncated Octahedra x = 1/2, 2. One of each per bcc cell.
    phi = Q5(Fr(1, 2), Fr(1, 2))
    def TX(x, s=Q5(1)):
        x = Q5._c(x); s = Q5._c(s); return list({tuple(sg[i] * s * v[p[i]] for i in range(3)) for p in itertools.permutations(range(3)) for sg in itertools.product((1, -1), repeat=3) for v in [(1 + x, x, Q5(0))]})
    for nm, x in (('x = 1/3', Q5(Fr(1, 3))), ('x = 1/2 (DICTO 1:2 Truncated Octahedron)', Q5(Fr(1, 2))), ('x = 1/tau', phi - 1), ('x = 1 (Kelvin)', Q5(1)),
                  ('x = tau (Icosaxes)', phi), ('x = 2 (DICTO 2:1 Truncated Octahedron)', Q5(2)), ('x = 3', Q5(3))):
        screen(f'factor x: T({nm})', [TX(x)], want='ZERO' if x == 1 else 'NONZERO')
        screen(f'factor x: cell T(x) + x T(1/x), {nm}', [TX(x), [add(v, (Q5(10),) * 3) for v in TX(1 / x, x)]], 'lattice relation', want='ZERO')

if PART in ('golden', 'keyed'):
    # the AXE network of #48 (exact, from shadow-forms/exact/golden_split_exact.py): icosahedra of edge 1 at phi Z^3, Unborns at the cube
    # centres, six AXEs per cell; cone every AXE from p(s) = long-edge midpoint + s (short-edge midpoint - long-edge midpoint)
    PHI = Q5(Fr(1, 2), Fr(1, 2)); IPHI = PHI - 1; H = PHI * Fr(1, 2); HALF = Q5(Fr(1, 2)); Z = Q5(0)
    cyc = lambda p: [p, (p[2], p[0], p[1]), (p[1], p[2], p[0])]
    ICO = [q for s1 in (1, -1) for s2 in (1, -1) for q in cyc((Z, s1 * HALF, s2 * H))]
    UC = (H, H, H)
    UNB = [add(UC, q) for s1 in (1, -1) for s2 in (1, -1) for q in cyc((s1 * H, s2 * IPHI * Fr(1, 2), Z))]
    AXE0 = [(-HALF, H, Z), (HALF, H, Z), (Z, H + IPHI * Fr(1, 2), H), (Z, H - IPHI * Fr(1, 2), H)]
    AX = {}
    for k in range(3):
        for sg in itertools.product((1, -1), repeat=3):
            Vv = [tuple(sg[i] * (cyc(v)[k][i]) for i in range(3)) for v in AXE0]
            for sl in itertools.product((-1, 0, 1), repeat=3):
                Wv = [add(v, mul(PHI, tuple(Q5(x) for x in sl))) for v in Vv]; AX[frozenset(Wv)] = Wv
    def pyramids(base, s):
        S = set(base); pyr = []
        for Wv in AX.values():
            for f in itertools.combinations(range(4), 3):
                if all(Wv[i] in S for i in f):
                    lm = mul(HALF, add(Wv[0], Wv[1])); sm = mul(HALF, add(Wv[2], Wv[3])); p = add(lm, mul(s, sub(sm, lm)))
                    pyr.append([Wv[i] for i in f] + [p])
        return pyr
    # the six AXEs of one cell (to check the cell volume) and the dodecahedron D of edge 1/phi at the cube centre, its 8 Tricaps
    D_ = [add(UC, v) for v in [tuple(Q5(Fr(s, 2)) for s in sg) for sg in itertools.product((1, -1), repeat=3)]] + \
         [add(UC, q) for s1 in (1, -1) for s2 in (1, -1) for q in cyc((Z, s1 * H, s2 * IPHI * Fr(1, 2)))]
    cube_c = D_[:8]
    def nbrs(v, P):
        d = sorted(P, key=lambda w: dot(sub(v, w), sub(v, w)).mp())
        return [w for w in d[1:4]]
    TRICAPS = [[c] + nbrs(c, D_) for c in cube_c]
    vI, vU, vD = volume(ICO), volume(UNB), volume(D_); vTc = [volume(T) for T in TRICAPS]
    check(f'exact volumes: icosahedron {vI}, Unborn {vU} = (3 + 7 sqrt5)/12, dodecahedron (edge 1/phi) {vD}, Tricap {vTc[0]} = (3 - sqrt5)/24 (all 8 equal), D = Unborn + 8 Tricaps',
          vU == Q5(Fr(3, 12), Fr(7, 12)) and all(v == Q5(Fr(3, 24), Fr(-1, 24)) for v in vTc) and vD == vU + 8 * vTc[0] and len(D_) == 20 and all(u in set(D_) for u in UNB))
    svals = [('1/10', Q5(Fr(1, 10))), ('1/5', Q5(Fr(1, 5))), ('3/10', Q5(Fr(3, 10))), ('2/5', Q5(Fr(2, 5))), ('1/2', Q5(Fr(1, 2))),
             ('3/5', Q5(Fr(3, 5))), ('1/phi (golden)', IPHI), ('7/10', Q5(Fr(7, 10))), ('4/5', Q5(Fr(4, 5))), ('9/10', Q5(Fr(9, 10)))]
    sel = [x for x in svals if x[0] in os.environ.get('SVALS', ','.join(n for n, _ in svals)).split(',')]
    for sn, s in sel:
        pI, pU = pyramids(ICO, s), pyramids(UNB, s)
        vol = vI + vU + sum((volume(P) for P in pI + pU), Q5(0))
        check(f's = {sn}: 12 + 12 pyramids; cell volume I(s) + U(s) = {vol} = phi^3 (exact)', len(pI) == 12 and len(pU) == 12 and vol == PHI * PHI * PHI)
        if PART == 'golden':
            screen(f'golden walk: padded icosahedron I(s), s = {sn}', [ICO] + pI, 'icosahedron + 12 AXE pyramids' + (' = Icosaxes' if sn.startswith('1/phi') else ''))
            screen(f'golden walk: padded Unborn U(s), s = {sn}', [UNB] + pU, 'Unborn + 12 AXE pyramids' + (' = Unborn Axes' if sn.startswith('1/phi') else ''))
            screen(f'golden walk: cell I(s) + U(s), s = {sn}', [ICO] + pI + [UNB] + pU, 'lattice relation', want='ZERO')
        else:
            screen(f'keyed walk: Dodecaxes(s) = dodecahedron + 12 AXE pyramids, s = {sn}', [D_] + pU, 'D = Unborn + 8 Tricaps' + (' = Dodecaxes' if sn.startswith('1/phi') else ''))
            screen(f'keyed walk: the same as Unborn + 8 Tricaps + 12 pyramids, s = {sn}', [UNB] + TRICAPS + pU, 'consistency (same solid, other parts)')
            if sn.startswith('1/phi'):
                for k in range(1, 8):
                    screen(f'keyed variants at the golden cut: Unborn Axes + {k} Tricap keys', [UNB] + TRICAPS[:k] + pU, 'k of the 8 keys on the small piece; the big piece is Icosaxes minus k keys (lattice relation)')
print('FINAL ok' if not fails else 'FINAL FAIL: ' + '; '.join(fails))
