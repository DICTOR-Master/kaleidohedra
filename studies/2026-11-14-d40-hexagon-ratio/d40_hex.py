# D40 (DICTO GTI) hexagon side ratio, exact in Q(sqrt5).
# Construction (paper #38): ID of circumradius phi; T(S) = {x : v.x <= v.v for every corner v of S}; RT = T(ID), GTI = T(RT).
# Every number is a + b*sqrt5 with rational a, b (class Q below); signs are decided exactly. Floats are used only to
# order the corners of a face round its centre, never for a length, a comparison of lengths, or a plane test.
import json, os, sys, itertools, math
from fractions import Fraction as F

class Q:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = F(a); s.b = F(b)
    def __add__(s, o): o = q(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q(-s.a, -s.b)
    def __sub__(s, o): return s + (-q(o))
    def __rsub__(s, o): return q(o) - s
    def __mul__(s, o): o = q(o); return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s):
        n = s.a * s.a - 5 * s.b * s.b
        assert n != 0
        return Q(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * q(o).inv()
    def __rtruediv__(s, o): return q(o) * s.inv()
    def sign(s):  # exact sign of a + b sqrt5
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        d = a * a - 5 * b * b  # compare |a| with |b| sqrt5
        return (1 if a > 0 else -1) if d > 0 else ((1 if b > 0 else -1) if d < 0 else 0)
    def __eq__(s, o): o = q(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b) * math.sqrt(5)
    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return f'{s.b}*sqrt5'
        return f'{s.a} + {s.b}*sqrt5'
def q(x): return x if isinstance(x, Q) else Q(x)

R5 = Q(0, 1); PHI = Q(F(1, 2), F(1, 2))
def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def sub(u, v): return tuple(x - y for x, y in zip(u, v))
def cross(u, v): return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
def cyc(p): return [p, (p[1], p[2], p[0]), (p[2], p[0], p[1])]

def T(corners):
    """Corners of {x : v.x <= v.v for all corners v}: every triple of planes, solved exactly, kept if feasible."""
    planes = [(v, dot(v, v)) for v in corners]
    out = set()
    for (n1, c1), (n2, c2), (n3, c3) in itertools.combinations(planes, 3):
        det = dot(n1, cross(n2, n3))
        if det.sign() == 0: continue
        x = tuple((c1 * a + c2 * b + c3 * c) / det for a, b, c in zip(cross(n2, n3), cross(n3, n1), cross(n1, n2)))
        if all((dot(n, x) - c).sign() <= 0 for n, c in planes): out.add(x)
    return sorted(out, key=lambda p: tuple(c.f() for c in p))

def hull_faces(V):
    """Faces of the convex hull of V: maximal sets of corners on a supporting plane (exact), ordered round the face."""
    faces = {}
    for i, j, k in itertools.combinations(range(len(V)), 3):
        n = cross(sub(V[j], V[i]), sub(V[k], V[i]))
        if all(c.sign() == 0 for c in n): continue
        s = [dot(n, sub(p, V[i])).sign() for p in V]
        if all(t <= 0 for t in s) or all(t >= 0 for t in s):
            key = frozenset(m for m, t in enumerate(s) if t == 0)
            faces[key] = n
    res = []
    for key, n in faces.items():
        idx = list(key); c = [sum(V[m][t].f() for m in idx) / len(idx) for t in range(3)]
        nf = [x.f() for x in n]; e1 = [V[idx[0]][t].f() - c[t] for t in range(3)]
        e2 = [nf[1]*e1[2]-nf[2]*e1[1], nf[2]*e1[0]-nf[0]*e1[2], nf[0]*e1[1]-nf[1]*e1[0]]
        ang = lambda m: math.atan2(sum((V[m][t].f()-c[t])*e2[t] for t in range(3)), sum((V[m][t].f()-c[t])*e1[t] for t in range(3)))
        res.append(sorted(idx, key=ang))
    return res

def sides2(V, face): return [dot(sub(V[face[i]], V[face[(i+1) % len(face)]]), sub(V[face[i]], V[face[(i+1) % len(face)]])) for i in range(len(face))]

def report_hexagons(name, V):
    fs = hull_faces(V); by = {}
    for f in fs: by.setdefault(len(f), []).append(f)
    print(f'{name}: {len(V)} corners, faces by sides', {k: len(v) for k, v in sorted(by.items())}, flush=True)
    E = len({frozenset((f[i], f[(i+1) % len(f)])) for f in fs for i in range(len(f))})
    assert len(V) - E + len(fs) == 2, 'Euler fails'
    pats = set()
    for f in by.get(6, []):
        s = sides2(V, f)
        alt = s[0] == s[2] == s[4] and s[1] == s[3] == s[5]
        pats.add((alt, tuple(sorted(set(s), key=lambda x: x.f()))))
    assert len(pats) == 1, f'hexagons not all alike: {pats}'
    alt, ls = pats.pop()
    sh, lo = (ls[0], ls[-1])  # one length only = regular hexagon, ratio 1
    return dict(faces={k: len(v) for k, v in by.items()}, alternate=alt, short2=sh, long2=lo, ratio2=lo / sh, faceslist=fs)

def is_square_of(r2, r):  # r > 0 and r*r == r2
    return r.sign() > 0 and r * r == r2

PROG = 6
print('PROGRESS 0/6 start', flush=True)
# 1. ID of circumradius phi (frame of #38): (+-phi,0,0) cyclic, (+-1/2, +-phi/2, +-phi^2/2) cyclic
ID = []
for s in (1, -1): ID += cyc((s * PHI, Q(0), Q(0)))
for s1, s2, s3 in itertools.product((1, -1), repeat=3): ID += cyc((Q(F(s1, 2)), s2 * PHI / 2, s3 * PHI * PHI / 2))
assert len(set(ID)) == 30 and all(dot(v, v) == PHI * PHI for v in ID)
print('PROGRESS 1/6 ID built: 30 corners, circumradius^2 =', PHI * PHI, flush=True)
RT = T(ID); assert len(RT) == 32, len(RT)
print('PROGRESS 2/6 RT = T(ID): 32 corners', flush=True)
GTI = T(RT)
print('PROGRESS 3/6 GTI = T(RT):', len(GTI), 'corners; circumradius^2 set', sorted({str(dot(v, v)) for v in GTI}), flush=True)
g = report_hexagons('GTI = T(T(ID))', GTI)
r = 1 + 3 * R5 / 5
print(f"  hexagon sides alternate: {g['alternate']}; short^2 = {g['short2']}, long^2 = {g['long2']}")
print(f"  ratio^2 (long/short) = {g['ratio2']}  ~ {math.sqrt(g['ratio2'].f()):.12f}")
ok_census = is_square_of(g['ratio2'], r); ok_phi = is_square_of(g['ratio2'], PHI)
print(f'  long/short == 1 + 3*sqrt5/5 exactly: {ok_census};  long/short == phi exactly: {ok_phi}')
for nm, sq in (('short', g['short2']), ('long', g['long2'])):
    for cand in (Q(5, -2), Q(-1, 1), Q(3, -1), Q(-3, 1)):
        if is_square_of(sq, cand): print(f'  {nm} side = {cand}')
# which edges are which: short = pentagon-hexagon edges, long = hexagon-hexagon edges
fs = g['faceslist']; pent_edges = {frozenset((f[i], f[(i+1) % 5])) for f in fs if len(f) == 5 for i in range(5)}
pe2 = {dot(sub(GTI[a], GTI[b]), sub(GTI[a], GTI[b])) for a, b in map(tuple, pent_edges)}
print(f'  pentagon side^2 = {pe2} (pentagons regular: {len(pe2) == 1}); short side is the pentagon side: {pe2 == {g["short2"]}}')
print('PROGRESS 4/6 GTI hexagons measured', flush=True)

# 2. compare with the DICTO Solids dataset file (exact vertex strings 'a + (b)*sqrt(5)')
import sympy as sp
def parse(s):
    e = sp.expand(sp.sympify(s)); b = e.coeff(sp.sqrt(5)); a = sp.expand(e - b * sp.sqrt(5))
    assert a.is_Rational and b.is_Rational, s
    return Q(F(str(a)), F(str(b)))
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset-gti-vertices.json')))['vertices']
DV = sorted({tuple(parse(c) for c in v) for v in D}, key=lambda p: tuple(c.f() for c in p))
assert len(DV) == 60
print('  dataset corners parse check (float agreement):', all(abs(Q.f(parse(c)) - eval(c.replace('sqrt(5)', '5**0.5'))) < 1e-12 for v in D for c in v))
same = set(DV) == set(GTI)
print(f'  dataset dicto-gti.json corners == T(T(ID)) corners exactly: {same}')
print(f'  dataset corners also corners of T(T(ID)): {len(set(DV) & set(GTI))} of 60; dataset circumradius^2 set {sorted({str(dot(v, v)) for v in DV})}')
# the dataset may hold the same solid in another orientation: test the 48 coordinate permutations with signs, and similarity by edge lengths
perm_hit = None
for pm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        if {tuple(sg[t] * v[pm[t]] for t in range(3)) for v in DV} == set(GTI): perm_hit = (pm, sg)
print(f'  dataset == T(T(ID)) after a signed coordinate permutation: {perm_hit}')
for i in range(3): print('   sample dataset corner', DV[i], '| sample T(T(ID)) corner', GTI[i])
dg = report_hexagons('dataset dicto-gti.json', DV)
same_shape = dg['ratio2'] == g['ratio2'] and dg['short2'] == g['short2'] and dg['long2'] == g['long2']
print(f"  dataset hexagons: short^2 = {dg['short2']}, long^2 = {dg['long2']}; same edge lengths and ratio as T(T(ID)): {same_shape}")
print('PROGRESS 5/6 dataset compared', flush=True)

# 3. controls: icosahedron of edge 1 cut at x along every edge (x < 1/2). Hexagon sides: x (shared with the corner pentagon)
#    and 1 - 2x (shared with a neighbouring hexagon). Positive: x = 1/3 gives ratio 1 (Archimedean).
#    #38's own description: x = 1/(2 + phi) gives (1-2x)/x = phi. Golden Ladder Table 4.3: x = 5/(15 + 3 sqrt5).
ICO = []
for s1, s2 in itertools.product((1, -1), repeat=2): ICO += cyc((Q(0), Q(F(s1, 2)), s2 * PHI / 2))
IE = [(u, v) for u, v in itertools.combinations(ICO, 2) if dot(sub(u, v), sub(u, v)) == 1]; assert len(IE) == 30
def cut(x): return [tuple(a + x * (b - a) for a, b in zip(u, v)) for p, w in IE for u, v in ((p, w), (w, p))]
res = {}
for nm, x in (('x = 1/3 (Archimedean)', Q(F(1, 3))), ('x = 1/(2+phi) (#38 text)', 1 / (2 + PHI)), ('x = 5/(15+3 sqrt5) (Golden Ladder)', 5 / (15 + 3 * R5))):
    h = report_hexagons('icosahedron cut at ' + nm, cut(x)); res[nm] = h
    print(f"  ratio^2 = {h['ratio2']}; = 1: {h['ratio2'] == 1}; = phi^2: {is_square_of(h['ratio2'], PHI)}; = (1+3sqrt5/5)^2: {is_square_of(h['ratio2'], r)}")
# similarity of the GTI with the Golden Ladder cut (same edge-length ratio and same face counts; both are Ih truncations of an icosahedron)
gl = res['x = 5/(15+3 sqrt5) (Golden Ladder)']; p38 = res['x = 1/(2+phi) (#38 text)']
sim_gl = gl['ratio2'] == g['ratio2']; sim_38 = p38['ratio2'] == g['ratio2']
print(f'  GTI similar to icosahedron cut at 5/(15+3 sqrt5): {sim_gl}; similar to cut at 1/(2+phi): {sim_38}')
k = (g['long2'] / gl['long2']); print(f'  scale^2 GTI : Golden Ladder cut = {k}')
print('PROGRESS 6/6 controls done', flush=True)

checks = dict(census_ratio=ok_census, not_phi=not ok_phi, dataset_same_shape=same_shape, control_archimedean=res['x = 1/3 (Archimedean)']['ratio2'] == 1,
              control_38_cut_is_phi=is_square_of(p38['ratio2'], PHI), gti_is_GL_cut=sim_gl, gti_not_38_cut=not sim_38,
              hexagons_alternate=g['alternate'])
print('CHECKS', checks)
if all(checks.values()):
    print('FINAL ok: D40 = T(T(ID)) has hexagons with alternating sides (5-2sqrt5) and (sqrt5-1); long/short = 1 + 3sqrt5/5 exactly, not phi')
else:
    print('FINAL FAIL', [k for k, v in checks.items() if not v]); sys.exit(1)
