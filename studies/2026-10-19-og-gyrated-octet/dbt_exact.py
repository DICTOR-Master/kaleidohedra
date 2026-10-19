# DICTO Belted Triacontahedron (DBT), exact in Q(sqrt5): a rhombic triacontahedron (inradius 2/3, #37 frame; it began as the golden
# envelope) truncated at its two three-fold corners on (1,1,1) by x+y+z = +-R, R = (1+sqrt5)/3. Every number is exact unless marked float.
import json, itertools, math
from fractions import Fraction as Fr
S5 = math.sqrt(5)
class Q:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): o = q(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = q(o); return Q(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return q(o) - s
    def __neg__(s): return Q(-s.a, -s.b)
    def __mul__(s, o): o = q(o); return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = q(o); n = o.a * o.a - 5 * o.b * o.b; return s * Q(o.a / n, -o.b / n)
    def sign(s):
        if s.b == 0: return (s.a > 0) - (s.a < 0)
        if s.a == 0: return (s.b > 0) - (s.b < 0)
        if (s.a > 0) == (s.b > 0): return 1 if s.a > 0 else -1
        # a and b of opposite sign: compare a^2 with 5 b^2
        big_a = s.a * s.a > 5 * s.b * s.b
        return (1 if s.a > 0 else -1) if big_a else (1 if s.b > 0 else -1)
    def __eq__(s, o): o = q(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b) * S5
    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return f'{s.b}*sqrt5'
        return f'{s.a} {"+" if s.b > 0 else "-"} {abs(s.b)}*sqrt5'
def q(x): return x if isinstance(x, Q) else Q(x)
def parse(t): a, b = t.split('|'); return Q(Fr(a), Fr(b))
dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
sub = lambda u, v: tuple(x - y for x, y in zip(u, v))
cross = lambda u, v: (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
det = lambda a, b, c: dot(a, cross(b, c))
PHI = Q(Fr(1, 2), Fr(1, 2)); R = Q(Fr(1, 3), Fr(1, 3)); I = PHI - 1  # 1/phi
ok = lambda c, msg: print(('PASS ' if c else 'FAIL ') + msg)

D = json.load(open('../2026-10-18-ocd-octet/data/step1-ocd-exact.json'))
V = [tuple(parse(c) for c in v) for v in D['V']]
assert D['R'] == '1/3|1/3'
r2 = [dot(v, v) for v in V]; top = max(r2, key=Q.f); U = [v for v, x in zip(V, r2) if x == top]
ok(len(U) == 12, f'OG has 12 outermost corners (radius^2 {top}) on the five-fold axes')

# the 30 two-fold unit vectors in this frame: (+-1,0,0) perms and cyclic perms of (+-phi, +-1/phi, +-1)/2 (this frame)
two = set()
for i in range(3):
    for s in (1, -1):
        e = [Q(0)] * 3; e[i] = Q(s); two.add(tuple(e))
for sx, sy, sz in itertools.product((1, -1), repeat=3):
    base = (PHI * sx / 2, I * sy / 2, Q(Fr(sz, 2)))
    for k in range(3): two.add(tuple(base[(j + k) % 3] for j in range(3)))
ok(len(two) == 30 and all(dot(n, n) == 1 for n in two), '30 exact unit two-fold vectors')
# the envelope's faces are perpendicular to u_i + u_j for neighbouring five-fold corners; match each to an exact unit vector
d2 = sorted({dot(u, w).f() for u, w in itertools.combinations(U, 2)}, reverse=True)[0]
pairs = [(u, w) for u, w in itertools.combinations(U, 2) if abs(dot(u, w).f() - d2) < 1e-12]
N = []
for u, w in pairs:
    s = tuple(x + y for x, y in zip(u, w)); m = [n for n in two if all(c == 0 for c in cross(n, s)) and dot(n, s).sign() > 0]
    assert len(m) == 1; N.append(m[0])
ok(len(set(N)) == 30, 'each of the 30 neighbour pairs u_i+u_j is exactly parallel to one two-fold unit vector')
n3 = (Q(1), Q(1), Q(1))
PL = [(n, Q(Fr(2, 3))) for n in N] + [(n3, R), (tuple(-x for x in n3), R)]   # n.x <= c

def corners(planes):
    pts = set()
    for (n1, c1), (n2, c2), (n3_, c3) in itertools.combinations(planes, 3):
        dd = det(n1, n2, n3_)
        if dd == 0: continue
        x = tuple((c1 * a + c2 * b + c3 * c) / dd for a, b, c in zip(cross(n2, n3_), cross(n3_, n1), cross(n1, n2)))
        if all((c - dot(n, x)).sign() >= 0 for n, c in planes): pts.add(x)
    return pts
def solid(planes, P):
    P = list(P); faces = []
    for n, c in planes:
        on = [p for p in P if dot(n, p) == c]
        if len(on) < 3: continue
        # order round the face centre (float angle; face is convex)
        cf = [sum(p[i].f() for p in on) / len(on) for i in range(3)]; nf = [x.f() for x in n]
        e1 = [on[0][i].f() - cf[i] for i in range(3)]; e2 = [nf[1] * e1[2] - nf[2] * e1[1], nf[2] * e1[0] - nf[0] * e1[2], nf[0] * e1[1] - nf[1] * e1[0]]
        on.sort(key=lambda p: math.atan2(sum((p[i].f() - cf[i]) * e2[i] for i in range(3)), sum((p[i].f() - cf[i]) * e1[i] for i in range(3))))
        faces.append((n, c, on))
    vol = Q(0)
    for n, c, on in faces:
        for k in range(1, len(on) - 1): vol = vol + det(on[0], on[k], on[k + 1]) / 6
    return faces, vol

RTc = corners(PL[:30]); RTf, RTv = solid(PL[:30], RTc)
P = corners(PL); F, vol = solid(PL, P)
ok(len(RTc) == 32 and len(RTf) == 30, f'envelope = rhombic triacontahedron: 32 corners, 30 faces; volume {RTv} = {RTv.f():.6f}')
nE = sum(len(on) for _, _, on in F) // 2
ok(len(P) - nE + len(F) == 2, f'DBT: {len(P)} corners, {nE} edges, {len(F)} faces (Euler 2)')
gone = RTc - P
ok(P <= RTc and len(gone) == 2 and all(dot(p, p) == dot(n3, p) * dot(n3, p) / 3 for p in gone),
   'no new corners: the DBT keeps 30 of the envelope corners and loses exactly the two on the (1,1,1) axis')
pole = [p for p in gone if dot(n3, p).sign() > 0][0]
ok(all((dot(n3, p) - R).sign() <= 0 for p in RTc - gone), 'every other envelope corner lies on or inside the cuts')
cut = [p for p in P if dot(n3, p) == R]
kinds = {}
for n, c, on in F:
    e2 = [dot(sub(on[i], on[(i + 1) % len(on)]), sub(on[i], on[(i + 1) % len(on)])) for i in range(len(on))]
    if len(on) == 4: k = 'rhombus' if len(set(e2)) == 1 else 'quad?'
    elif len(on) == 3: k = 'equilateral triangle' if len(set(e2)) == 1 else 'half-rhombus (isosceles)' if len(set(e2)) == 2 else 'triangle?'
    else: k = f'{len(on)}-gon?'
    kinds[k] = kinds.get(k, 0) + 1
ok(kinds == {'rhombus': 24, 'half-rhombus (isosceles)': 6, 'equilateral triangle': 2}, f'faces {kinds}')
tri = [on for n, c, on in F if n == n3][0]; s2 = dot(sub(tri[0], tri[1]), sub(tri[0], tri[1]))
print(f'      pole triangle side^2 = {s2} (side {math.sqrt(s2.f()):.6f}); its corners = the three five-fold-type envelope corners next-but-one to the pole')
# each half-rhombus is a rhombus of the envelope halved along its long diagonal
halves = 0
for n, c, on in F:
    if len(on) != 3 or n in (n3, tuple(-x for x in n3)): continue
    full = [o for m, cc, o in RTf if m == n][0]; d = [x for x in full if x not in on]
    if len(d) == 1 and d[0] in gone:
        halves += 1
ok(halves == 6, 'each half-rhombus = an envelope rhombus with its pole corner cut off along a diagonal (cut runs on diagonals)')
# long vs short diagonal: the cut diagonal against the rhombus' other diagonal
n, c, on = [f for f in F if len(f[2]) == 3 and f[0] != n3 and f[0] != tuple(-x for x in n3)][0]
full = [o for m, cc, o in RTf if m == n][0]; d = [x for x in full if x not in on][0]; opp = [x for x in on if x not in cut][0]
cutd = dot(sub(*[x for x in on if x in cut]), sub(*[x for x in on if x in cut])); other = dot(sub(d, opp), sub(d, opp))
ok((cutd - other).sign() > 0 and cutd / other == PHI * PHI, f'the cut diagonal is the LONG one (ratio^2 = phi^2 = {cutd / other})')
key = (RTv - vol) / 2
ok(key == Q(Fr(-44, 81), Fr(20, 81)), f'DBT volume {vol} = {vol.f():.6f}; each removed corner {key} = {key.f():.6f}')
# the removed corner is the pyramid pole + pole triangle; compare with the golden rhombohedron spanned by the pole's three edges
nb = [p for p in RTc if p != pole and any(len(on) == 4 and pole in on and p in on and (on.index(p) - on.index(pole)) % 4 in (1, 3) for _, _, on in RTf)]
ok(len(nb) == 3, 'pole has three envelope edges')
rh = abs(det(*[sub(p, pole) for p in nb]).f()); rhq = det(*[sub(p, pole) for p in nb]); rhq = rhq if rhq.sign() > 0 else -rhq
print(f'      rhombohedron on the pole edges: volume {rhq} = {rhq.f():.6f}; removed corner / rhombohedron = {key / rhq}')
ok(key / rhq == Q(Fr(1, 6)), 'removed corner = 1/6 of that golden rhombohedron (a tetrahedron on three of its edges)')
obl = sum(1 for a, b in itertools.combinations([sub(p, pole) for p in nb], 2) if dot(a, b).sign() < 0)
print(f'      edge pairs at the pole with obtuse angle: {obl} of 3 ->', 'oblate' if obl == 3 else 'prolate' if obl == 0 else 'mixed')
# symmetry D3d: 3-fold about (1,1,1), inversion, a 2-fold across it
Ps = set(P)
ok({(p[1], p[2], p[0]) for p in P} == Ps, 'three-fold turn about (1,1,1) maps the DBT to itself')
ok({tuple(-x for x in p) for p in P} == Ps, 'inversion maps the DBT to itself')
perp = [n for n in two if dot(n, n3) == 0 and n[0].sign() >= 0]
half = [n for n in perp if {tuple(2 * dot(n, p) * n[i] - p[i] for i in range(3)) for p in P} == Ps]
ok(len(half) == 3, f'half-turns about the {len(half)} golden two-fold axes perpendicular to (1,1,1) map the DBT to itself -> D3d (order 12): {[[str(x) for x in n] for n in half]}')
ok({(p[1], p[0], p[2]) for p in P} != Ps, 'the mirror x<->y does NOT (so not a larger group via that plane)')
# the OG inside: every OG corner within all 32 planes; which touch
inside = all((c - dot(n, v)).sign() >= 0 for v in V for n, c in PL)
touch = sum(1 for v in V if any(dot(n, v) == c for n, c in PL))
ok(inside, f'OG lies inside the DBT; OG corners on its surface: {touch}')
# float only: area and sphericity
def area(on):
    s = [0.0, 0.0, 0.0]
    for k in range(1, len(on) - 1):
        cr = cross(sub(on[k], on[0]), sub(on[k + 1], on[0])); s = [s[i] + cr[i].f() for i in range(3)]
    return 0.5 * math.sqrt(sum(x * x for x in s))
A = sum(area(on) for _, _, on in F)
print(f'      float: surface {A:.6f}, sphericity {math.pi ** (1 / 3) * (6 * vol.f()) ** (2 / 3) / A:.4f}')
json.dump({'mark': 'DICTO · dictospheres.com · CC BY-SA 4.0', 'note': 'DICTO Belted Triacontahedron, exact a|b = a + b*sqrt5',
           'V': [[f'{x.a}|{x.b}' for x in p] for p in sorted(P, key=lambda p: [x.f() for x in p])],
           'volume': f'{vol.a}|{vol.b}', 'removed_corner': f'{key.a}|{key.b}', 'envelope_volume': f'{RTv.a}|{RTv.b}'},
          open('dbt-exact.json', 'w'), indent=1)
print('wrote dbt-exact.json')
