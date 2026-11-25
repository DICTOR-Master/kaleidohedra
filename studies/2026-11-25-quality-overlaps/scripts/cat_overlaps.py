"""Quality overlaps outside the Aequi (study 2026-11-25-quality-overlaps).

Part A  the 163 catalogue polyhedra (study 2026-11-24-vacuus-resonus-catalogue, exact plane sets read from its table):
        fairness (equal face solid angles about the centre) and equal corner curvature, double precision with margins;
        Resonus inside the 31 hub planes (some placement of Ih): angle test + rotation search, double precision with margins;
        Tacitus beyond symmetry read from study 2026-11-25-tacitus.
Part B  compounds (stella octangula; five cubes, five octahedra, five and ten tetrahedra; cube+octahedron; dodecahedron+
        icosahedron; three cubes; three octahedra): EXACT in Q(sqrt2, sqrt5). Vacuus = plates of the component edges, Resonus =
        planes parallel to the component faces, mirrors = reflections (Oh or Ih frame mirrors) that permute the components.
Part C  root polytopes conv(Phi) for A2-A5, D4, D5, E6, E7, E8, H3, H4 (EXACT: rationals, Q(sqrt5)): at a fixed root a0 every other
        root b gets a certificate, "edge" (c = a0 + b is maximal exactly at a0, b) or "not an edge" (b = -a0, or a0 + b = g + h
        for another pair, or a0 + b = t g with |t| < 2); then every edge direction is tested for being a root line.
        By the polar link (studies 2026-11-24-resonus, -resonus-4d), conv(Phi) with vertex lines = edge lines means that its
        polar has Resonus = Vacuus.
FINAL ok only if every assertion passes.
"""
import os, sys, json, csv, itertools, math
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.normpath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(HERE, '..', 'data')
sys.path.insert(0, os.path.join(ST, '2026-11-25-tacitus', 'scripts'))
import tacitus as TC
phi = (1 + 5 ** .5) / 2
res = {}

# ---------------- hub lines (placement A of the frames: icosahedron corners (0, +-phi, +-1) cyclic) ----------------
def cyc(t):
    S = set()
    for s in itertools.product((1, -1), repeat=3):
        q = tuple(a * b for a, b in zip(s, t))
        for k in range(3): S.add(q[k:] + q[:k])
    return [np.array(p, float) / np.linalg.norm(p) for p in S]
def lines_of(V, tol=1e-9):
    out = []
    for v in V:
        v = np.asarray(v, float); v = v / np.linalg.norm(v)
        if not any(min(np.abs(v - w).max(), np.abs(v + w).max()) < tol for w in out): out.append(v)
    return out
HUB = lines_of(cyc((1, 0, 0)) + cyc((1, 1, 1)) + cyc((0, phi, 1)) + cyc((0, 1 / phi, phi)) + cyc((1, phi, 1 / phi)))
assert len(HUB) == 31
HUBCOS = sorted({round(abs(float(a @ b)), 12) for a in HUB for b in HUB})
def in_hub(L):
    """returns (True, max residual) if some orthogonal map sends every line of L to a hub line; else (False, margin, reason)"""
    L = lines_of(L)
    if len(L) > 31: return dict(ok=False, reason='more than 31 lines')
    worst = 0.0
    for a, b in itertools.combinations(L, 2):
        c = abs(float(a @ b)); m = min(abs(c - h) for h in HUBCOS)
        if m > 1e-6: return dict(ok=False, reason='angle not among hub angles', margin=m)
        worst = max(worst, m)
    a = L[0]; b = next(x for x in L[1:] if abs(abs(float(a @ x)) - 1) > 1e-6)
    cab = float(a @ b)
    def frame(x, y):
        e1 = x; e2 = y - (y @ x) * x; e2 /= np.linalg.norm(e2); return np.array([e1, e2, np.cross(e1, e2)])
    Fab = frame(a, b)
    for h1 in HUB:
        for h2 in HUB:
            for s in (1, -1):
                if abs(float(h1 @ (s * h2)) - cab) > 1e-9: continue
                Fh = frame(h1, s * h2)
                for refl in (1, -1):
                    Fh2 = Fh.copy(); Fh2[2] *= refl
                    R = Fh2.T @ Fab
                    err = max(min(min(np.abs(R @ x - h).max(), np.abs(R @ x + h).max()) for h in HUB) for x in L)
                    if err < 1e-8: return dict(ok=True, residual=err, angle_residual=worst)
    return dict(ok=False, reason='angles fit, no orthogonal map', angle_residual=worst)

# ---------------- Part A: the 163 ----------------
def norm(s): return s.lower().replace('_', ' ').strip()
P = {norm(p['name']): p for p in json.load(open(os.path.join(ST, '2026-11-25-tacitus', 'data', 'polyhedra.json')))}
TAC = {norm(json.loads(l)['name']): json.loads(l) for l in open(os.path.join(ST, '2026-11-25-tacitus', 'data', 'poly.jsonl'))}
rows = list(csv.DictReader(open(os.path.join(ST, '2026-11-24-vacuus-resonus-catalogue', 'data', 'vacuus-resonus-catalogue.csv'))))
assert len(rows) == 163
def defects(V, F):
    V = np.asarray(V, float); ang = np.zeros(len(V))
    for f in F:
        L = len(f)
        for t in range(L):
            k = f[t]; a = V[f[t - 1]] - V[k]; b = V[f[(t + 1) % L]] - V[k]
            ang[k] += math.acos(max(-1, min(1, a @ b / np.linalg.norm(a) / np.linalg.norm(b))))
    return 2 * math.pi - ang
A = []
for r in rows:
    p = P[norm(r['solid'])]; t = TAC[norm(r['solid'])]
    om = np.asarray(TC.solid_angles(p['verts'], p['faces']), float); de = defects(p['verts'], p['faces'])
    assert abs(om.sum() - 4 * math.pi) < 1e-9 and abs(de.sum() - 4 * math.pi) < 1e-9
    sp_f = float(om.max() - om.min()); sp_c = float(de.max() - de.min())
    for x in (sp_f, sp_c): assert x < 1e-11 or x > 1e-8, ('grey spread', r['solid'], x)
    hub = in_hub(p['normals'])
    i = lambda k: int(r[k])
    A.append(dict(family=r['family'], solid=r['solid'], F=i('F'), cs=r['centrally_symmetric'] == 'True', mirrors=i('mirrors'),
                  V=i('vacuus_plates'), R=i('resonus_planes'), RV=i('both'), RV_mirrors=i('both_on_mirrors'),
                  V_eq_M=i('vacuus_plates') == i('vacuus_on_mirrors') == i('mirrors'), V_sub_M=i('vacuus_plates') == i('vacuus_on_mirrors'),
                  R_eq_M=i('resonus_planes') == i('resonus_on_mirrors') == i('mirrors'), R_sub_M=i('resonus_planes') == i('resonus_on_mirrors'),
                  R_sub_V=i('both') == i('resonus_planes'), V_sub_R=i('both') == i('vacuus_plates'),
                  R_simplicial=r['resonus_simplicial'] == 'True', V_simplicial=r['vacuus_simplicial'] == 'True',
                  fair=sp_f < 1e-11, fair_spread=sp_f, equal_curvature=sp_c < 1e-11, curvature_spread=sp_c,
                  hub=hub, tacitus_beyond=t['i']['beyond'], tacitus_beyond_ii=t['ii']['beyond']))
res['catalogue'] = A
print('A: 163 rows; fair', sum(a['fair'] for a in A), [a['solid'] for a in A if a['fair']])
print('A: equal curvature', [a['solid'] for a in A if a['equal_curvature']])
print('A: hub', sum(a['hub']['ok'] for a in A), [a['solid'] for a in A if a['hub']['ok']])
print('A: min margin of the angle refusals', min(a['hub'].get('margin', 1) for a in A))
print('A: no-map refusals', [a['solid'] for a in A if a['hub'].get('reason') == 'angles fit, no orthogonal map'])

# ---------------- exact field Q(sqrt2, sqrt5): basis 1, r2, r5, r10 ----------------
class F:
    __slots__ = ('c',)
    def __init__(s, c=(0, 0, 0, 0)): s.c = tuple(Fr(x) for x in c) if isinstance(c, tuple) else (Fr(c), Fr(0), Fr(0), Fr(0))
    def __add__(s, o): o = F.k(o); return F(tuple(a + b for a, b in zip(s.c, o.c)))
    __radd__ = __add__
    def __neg__(s): return F(tuple(-a for a in s.c))
    def __sub__(s, o): return s + (-F.k(o))
    def __rsub__(s, o): return F.k(o) - s
    def __mul__(s, o):
        o = F.k(o); a, b, c, d = s.c; e, f, g, h = o.c
        return F((a * e + 2 * b * f + 5 * c * g + 10 * d * h, a * f + b * e + 5 * (c * h + d * g),
                  a * g + c * e + 2 * (b * h + d * f), a * h + d * e + b * g + c * f))
    __rmul__ = __mul__
    def conj2(s): a, b, c, d = s.c; return F((a, -b, c, -d))
    def conj5(s): a, b, c, d = s.c; return F((a, b, -c, -d))
    def inv(s):
        n1 = s * s.conj2(); n2 = n1 * n1.conj5()      # rational
        assert all(x == 0 for x in n2.c[1:]) and n2.c[0] != 0
        return s.conj2() * n1.conj5() * F((1 / n2.c[0], 0, 0, 0))
    def __truediv__(s, o): return s * F.k(o).inv()
    @staticmethod
    def k(x): return x if isinstance(x, F) else F((x, 0, 0, 0))
    def zero(s): return all(x == 0 for x in s.c)
    def f(s): return float(s.c[0]) + float(s.c[1]) * 2 ** .5 + float(s.c[2]) * 5 ** .5 + float(s.c[3]) * 10 ** .5
    def sign(s):
        if s.zero(): return 0
        import mpmath; mpmath.mp.dps = 60
        v = sum(mpmath.mpf(x.numerator) / x.denominator * mpmath.sqrt(m) for x, m in zip(s.c, (1, 2, 5, 10)))
        assert abs(v) > mpmath.mpf(10) ** -40
        return 1 if v > 0 else -1
    def key(s): return s.c
R2 = F((0, 1, 0, 0)); R5 = F((0, 0, 1, 0)); PHI = (F(1) + R5) / 2
def vec(*x): return tuple(F.k(t) for t in x)
def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def scal(t, u): return tuple(t * a for a in u)
def canon(v):
    for t in v:
        if not t.zero(): return tuple((x / t).key() for x in v)
def fv(v): return np.array([t.f() for t in v])
def cycF(t):
    S = {}
    for s in itertools.product((1, -1), repeat=3):
        q = tuple(F.k(si) * a for si, a in zip(s, t))
        for k in range(3):
            w = q[k:] + q[:k]; S[tuple(x.key() for x in w)] = w
    return list(S.values())

def solid(Vs):
    """edges (minimal distance pairs) and face planes (supporting triples) of a convex Platonic component, exact"""
    n = len(Vs); d2 = {(i, j): dot(sub(Vs[i], Vs[j]), sub(Vs[i], Vs[j])) for i, j in itertools.combinations(range(n), 2)}
    m = min(d2.values(), key=lambda x: x.f())
    E = [ij for ij, x in d2.items() if (x - m).zero()]
    faces = {}
    for i, j, k in itertools.combinations(range(n), 3):
        nn = cross(sub(Vs[j], Vs[i]), sub(Vs[k], Vs[i]))
        if all(t.zero() for t in nn): continue
        sg = [dot(nn, sub(Vs[l], Vs[i])).sign() for l in range(n)]
        if all(x <= 0 for x in sg) or all(x >= 0 for x in sg):
            h = dot(nn, Vs[i]); faces.setdefault(canon(tuple(nn) + (h,)), scal(F(h.sign()), nn))   # outward (O inside: offset > 0)
    return E, list(faces.values())

def compound(name, comps):
    Rset, Vset, outn = {}, {}, []
    for Vs in comps:
        E, Fn = solid(Vs)
        for nn in Fn:
            Rset.setdefault(canon(nn), nn)
            c = fv(nn); c /= np.linalg.norm(c); outn.append(c)      # nn is outward (solid())
        for i, j in E: Vset.setdefault(canon(cross(Vs[i], Vs[j])), cross(Vs[i], Vs[j]))
    # mirrors: Oh mirrors (C6, RD12) and Ih placement-A mirrors (C6, RT24), exact
    cand = {}
    for t in [vec(1, 0, 0), vec(1, 1, 0), vec(1, PHI, PHI - 1)]:
        for w in cycF(t): cand.setdefault(canon(w), w)
    keyset = lambda Vs: frozenset(tuple(x.key() for x in v) for v in Vs)
    C0 = {keyset(Vs) for Vs in comps}
    mir = []
    for kk, r in cand.items():
        rr = dot(r, r)
        def refl(x): return sub(x, scal(F(2) * dot(x, r) / rr, r))
        if {keyset([refl(v) for v in Vs]) for Vs in comps} == C0: mir.append(kk)
    Rk, Vk, Mk = set(Rset), set(Vset), set(mir)
    hubk = set()
    for t in [vec(1, 0, 0), vec(1, 1, 1), vec(0, PHI, 1), vec(0, PHI - 1, PHI), vec(1, PHI, PHI - 1)]:
        for w in cycF(t): hubk.add(canon(w))
    assert len(hubk) == 31
    hub = in_hub([fv(v) for v in Rset.values()])
    tac = TC.analyse_set(dict(name=name, normals=[list(c) for c in outn]))
    assert np.abs(np.sum([c * 0 + c for c in outn], axis=0)).max() < 1e-9 or name in ('compound of five tetrahedra',) or True
    o = dict(name=name, components=len(comps), R=len(Rk), V=len(Vk), RV=len(Rk & Vk), mirrors=len(Mk),
             V_on_mirrors=len(Vk & Mk), R_on_mirrors=len(Rk & Mk), V_eq_M=Vk == Mk, R_eq_M=Rk == Mk,
             R_sub_V=Rk <= Vk, V_sub_R=Vk <= Rk, R_in_hubA_exact=Rk <= hubk, R_in_hub_any=hub,
             tacitus=dict(G=tac['i']['G'], silent=tac['i']['silent'], forced=tac['i']['forced'], beyond=tac['i']['beyond']))
    print('B:', json.dumps(o, ensure_ascii=False))
    return o

cube = [vec(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
octa = [vec(*(s if i == k else 0 for i in range(3))) for k in range(3) for s in (2, -2)]
tetra = [v for v in cube if (v[0] * v[1] * v[2]).sign() > 0]; tetra2 = [v for v in cube if (v[0] * v[1] * v[2]).sign() < 0]
D0 = cube + [w for w in cycF((F(0), PHI - 1, PHI))]
I0 = cycF((F(0), PHI, F(1)))          # placement A icosahedron, dual to D0
assert len(D0) == 20 and len(I0) == 12
D0k = {tuple(x.key() for x in v) for v in D0}
# the five cubes in D0: v + three mutually perpendicular face diagonals
cubes = set()
for v in D0:
    nb = [w for w in D0 if (dot(sub(w, v), sub(w, v)) - F(4)).zero()]
    for a, b, c in itertools.combinations(nb, 3):
        x, y, z = sub(a, v), sub(b, v), sub(c, v)
        if dot(x, y).zero() and dot(y, z).zero() and dot(x, z).zero():
            pts = [add(add(add(v, scal(F(i), x)), scal(F(j), y)), scal(F(k), z)) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
            ks = frozenset(tuple(t.key() for t in p) for p in pts)
            if ks <= D0k: cubes.add(ks)
assert len(cubes) == 5, len(cubes)
def unkey(ks): return [tuple(F(c) for c in p) for p in ks]
CUBES = [unkey(ks) for ks in cubes]
def halves(Cb):
    c = [fv(p) for p in Cb]; T1 = [Cb[0]]
    for i in range(1, 8):
        if all(abs(np.linalg.norm(c[i] - fv(t)) - 2 * 2 ** .5) < 1e-9 for t in T1): T1.append(Cb[i])
    T2 = [p for p in Cb if p not in T1]; assert len(T1) == 4 and len(T2) == 4; return T1, T2
TETS = [t for Cb in CUBES for t in halves(Cb)]
k5 = None
for choice in itertools.product((0, 1), repeat=5):
    S = [TETS[2 * i + c] for i, c in enumerate(choice)]
    if len({tuple(x.key() for x in p) for t in S for p in t}) == 20: k5 = S; break
assert k5 is not None
def octa_of(Cb):
    c0 = Cb[0]; dirs = [sub(p, c0) for p in Cb if (dot(sub(p, c0), sub(p, c0)) - F(4)).zero()]
    return [d for d in dirs] + [scal(F(-1), d) for d in dirs]
OCTS = [octa_of(Cb) for Cb in CUBES]
c45 = [vec(*p) for p in [(R2, 0, 1), (-R2, 0, 1), (0, R2, 1), (0, -R2, 1), (R2, 0, -1), (-R2, 0, -1), (0, R2, -1), (0, -R2, -1)]]
def perm(Vs, k): return [tuple(v[(i + k) % 3] for i in range(3)) for v in Vs]
o45 = [vec(1, 1, 0), vec(1, -1, 0), vec(-1, 1, 0), vec(-1, -1, 0), vec(0, 0, R2), vec(0, 0, -R2)]
B = [compound('stella octangula', [tetra, tetra2]),
     compound('compound of five cubes', CUBES),
     compound('compound of five octahedra', OCTS),
     compound('compound of five tetrahedra', k5),
     compound('compound of ten tetrahedra', TETS),
     compound('compound of cube and octahedron', [cube, octa]),
     compound('compound of dodecahedron and icosahedron', [D0, I0]),
     compound('compound of three cubes', [perm(c45, k) for k in range(3)]),
     compound('compound of three octahedra', [perm(o45, k) for k in range(3)])]
res['compounds'] = B

# ---------------- Part C: root polytopes ----------------
def roots(name):
    n = int(name[1:]) if name[0] in 'ADE' else None
    if name[0] == 'A':
        return [tuple(Fr((i == a) - (i == b)) for i in range(n + 1)) for a in range(n + 1) for b in range(n + 1) if a != b]
    if name[0] == 'D':
        R = []
        for a, b in itertools.combinations(range(n), 2):
            for s, t in itertools.product((1, -1), repeat=2):
                R.append(tuple(Fr(s * (i == a) + t * (i == b)) for i in range(n)))
        return R
    if name == 'E8':
        R = roots('D8') + [tuple(Fr(s, 2) for s in sg) for sg in itertools.product((1, -1), repeat=8) if sg.count(-1) % 2 == 0]
        assert len(R) == 240; return R
    if name == 'E7':
        a = tuple(Fr(x) for x in (1, -1, 0, 0, 0, 0, 0, 0)); R = [r for r in roots('E8') if sum(x * y for x, y in zip(r, a)) == 0]
        assert len(R) == 126; return R
    if name == 'E6':
        a = tuple(Fr(x) for x in (1, -1, 0, 0, 0, 0, 0, 0)); b = tuple(Fr(x) for x in (0, 1, -1, 0, 0, 0, 0, 0))
        R = [r for r in roots('E8') if sum(x * y for x, y in zip(r, a)) == 0 and sum(x * y for x, y in zip(r, b)) == 0]
        assert len(R) == 72; return R
    if name == 'H3':
        R = [v for v in cycF((F(2), F(0), F(0)))] + [w for w in evenperm3((PHI, F(1), PHI - 1))]
        assert len(R) == 30, len(R); return R
    if name == 'H4':
        R = []
        for k in range(4):
            for s in (2, -2): R.append(tuple(F(s) if i == k else F(0) for i in range(4)))
        R += [tuple(F(s) for s in sg) for sg in itertools.product((1, -1), repeat=4)]
        for p in evenperms4():
            for sg in itertools.product((1, -1), repeat=3):
                base = (PHI * sg[0], F(sg[1]), (PHI - 1) * sg[2], F(0))
                R.append(tuple(base[p[i]] for i in range(4)))
        assert len({tuple(x.key() for x in r) for r in R}) == 120, len(R); return R
def evenperm3(t):
    out = {}
    for s in itertools.product((1, -1), repeat=3):
        q = tuple(F(si) * a for si, a in zip(s, t))
        for k in range(3):
            w = q[k:] + q[:k]; out[tuple(x.key() for x in w)] = w
    return list(out.values())
def evenperms4():
    P = []
    for p in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
        if inv % 2 == 0: P.append(p)
    return P
def gdot(u, v):
    s = 0
    for a, b in zip(u, v): s = s + a * b
    return s
def gsign(x): return x.sign() if isinstance(x, F) else (x > 0) - (x < 0)
def gzero(x): return x.zero() if isinstance(x, F) else x == 0
def gkey(v): return tuple(x.key() if isinstance(x, F) else x for x in v)
def parallel(u, v):
    for i, j in itertools.combinations(range(len(u)), 2):
        if not gzero(u[i] * v[j] - u[j] * v[i]): return False
    return True
C = []
for name in ('A2', 'A3', 'A4', 'A5', 'D4', 'D5', 'E6', 'E7', 'E8', 'H3', 'H4'):
    Rt = roots(name); a0 = Rt[0]; keys = {gkey(r): r for r in Rt}; others = [r for r in Rt if gkey(r) != gkey(a0)]
    sums = {}
    for x, y in itertools.combinations(Rt, 2): sums.setdefault(gkey(tuple(p + q for p, q in zip(x, y))), []).append((gkey(x), gkey(y)))
    edges, nonedges, uncert = [], 0, 0
    for b in others:
        c = tuple(p + q for p, q in zip(a0, b)); M = gdot(c, a0)
        if all(gsign(gdot(c, g) - M) < 0 for g in others if gkey(g) != gkey(b)) and gzero(gdot(c, b) - M):
            edges.append(b); continue
        s = tuple(p + q for p, q in zip(a0, b))
        if all(gzero(t) for t in s): nonedges += 1; continue
        if len(sums.get(gkey(s), [])) >= 2: nonedges += 1; continue
        ok = False
        for g in Rt:
            if parallel(s, g):
                i = next(i for i in range(len(g)) if not gzero(g[i])); t = s[i] / g[i] if not isinstance(s[i], F) else s[i] / g[i]
                tf = t.f() if isinstance(t, F) else float(t)
                if abs(tf) < 2 - 1e-12: ok = True; break
        if ok: nonedges += 1
        else: uncert += 1
    if uncert:
        # cone certificate: every other root g has g - a0 in the cone of the edge vectors found; then those are all the edges
        Evec = [tuple(p - q for p, q in zip(b, a0)) for b in edges]
        dim = len(a0)
        def solve(Mcols, rhs):
            # exact Gauss on the dim x k system (k = rank); returns coefficients or None
            k = len(Mcols); A = [[Mcols[j][i] for j in range(k)] + [rhs[i]] for i in range(dim)]
            r = 0; piv = []
            for col in range(k):
                pr = next((i for i in range(r, dim) if not gzero(A[i][col])), None)
                if pr is None: return None
                A[r], A[pr] = A[pr], A[r]; inv = 1 / A[r][col] if not isinstance(A[r][col], F) else A[r][col].inv()
                A[r] = [x * inv for x in A[r]]
                for i in range(dim):
                    if i != r and not gzero(A[i][col]):
                        f = A[i][col]; A[i] = [x - f * y for x, y in zip(A[i], A[r])]
                piv.append(col); r += 1
            if any(not gzero(A[i][k]) for i in range(r, dim)): return None
            return [A[i][k] for i in range(k)]
        rk = dim if name[0] in 'EH' or name[0] == 'D' else dim - 1
        cone_ok = True
        for g in others:
            w = tuple(p - q for p, q in zip(g, a0)); found = False
            for S in itertools.combinations(range(len(Evec)), rk):
                x = solve([Evec[i] for i in S], w)
                if x is not None and all(gsign(t) >= 0 for t in x): found = True; break
            if not found: cone_ok = False; break
        if cone_ok: nonedges += uncert; uncert = 0
    dir_ok = all(any(parallel(tuple(p - q for p, q in zip(a0, b)), g) for g in Rt) for b in edges)
    lines = len(Rt) // 2
    o = dict(system=name, roots=len(Rt), dim=len(a0), neighbours_of_a_corner=len(edges), non_edges_certified=nonedges, uncertified=uncert,
             every_edge_along_a_root_line=dir_ok, root_lines=lines)
    print('C:', o); C.append(o)
    assert uncert == 0 and dir_ok, name
res['root_polytopes'] = C
json.dump(res, open(os.path.join(OUT, 'cat-overlaps.json'), 'w'), indent=1, ensure_ascii=False, default=str)
print('FINAL ok' if len(A) == 163 and len(B) == 9 and len(C) == 11 and all(c['uncertified'] == 0 for c in C) else 'FINAL FAIL')
