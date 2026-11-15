#!/usr/bin/env python3
"""export_dicto.py (15 Nov 2026) - DICTO · dictospheres.com
Collects DICTO's solids for the McCooey comparison into one file, corners as 40-digit decimals where an exact build exists.
Groups:
  cone      every 3D equal-edged solid of the A3 / B3 / H3 permutohedron cones (study 2026-11-12-permutohedron-equal-edges),
            rebuilt exactly from its 0/1 wall labels with that study's own coxeter.py (Q(sqrt2) / Q(sqrt5)); its kind kept
            (the 369 new atoms and the 54 sums of atoms are marked)
  silent    the DICTO silent zonohedron: signed permutations of (a, a+1, a+2), a = -1 + sqrt(1 + sqrt(5/6)) (sympy, exact)
  golden-og Lesser / Greater Golden OG (#91), rebuilt exactly with study 2026-11-03-dual-pairs-dimensions dp_lib (Q(sqrt2, sqrt5))
  og-family the DICTO OG and its eight steps (#39) from that study's float file; the further steps (Hamlet, Ophelia, #80; the
            pedal steps 5-11, #43) and the Universal PiTet cycle (#38) recomputed in double precision (T: v.x <= v.v; P: foot
            points), with corner / face counts checked against the Concordance
  registry  the 389-solid app registry the disc-ranking study read (double precision)
  hybrid    the hybrid kit (study 2026-11-14-platonic-hybrid): cap, roof plate Z, roof R, Admiral Cap (exact Q(sqrt5))
usage (compute host, venv with numpy/scipy/sympy/mpmath): export_dicto.py K_RESEARCH_ROOT OUT.json"""
import sys, os, json, time, itertools
import numpy as np
import mpmath as mp
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, HalfspaceIntersection

mp.mp.dps = 50
ROOT, OUT = sys.argv[1], sys.argv[2]
T0 = time.time()
CHECKS = []


def check(name, ok, detail=''):
    CHECKS.append((name, bool(ok)))
    print(f'CHECK {"ok  " if ok else "FAIL"} {name} {detail}', flush=True)


def s40(x):
    return mp.nstr(x, 40, strip_zeros=False) if x != 0 else '0'


def frac(x):
    return mp.mpf(x.numerator) / x.denominator


solids = []


def add(sid, name, group, V, precision, source, **kw):
    d = {'id': sid, 'name': name, 'group': group, 'precision': precision, 'source': source,
         'V': [[s40(c) if precision == 'exact' else repr(float(c)) for c in v] for v in V]}
    d.update(kw)
    solids.append(d)


# ---------------- cone solids (A3, B3, H3)
EE = os.path.join(ROOT, 'studies/2026-11-12-permutohedron-equal-edges')
sys.path.insert(0, os.path.join(EE, 'scripts'))
import coxeter
from coxeter import QF, Fan, vsub, vkey
for name, D in (('A3', 2), ('B3', 2), ('H3', 5)):
    QF.D = D
    F = Fan(name)
    QF.D = D
    mem = json.load(open(os.path.join(EE, f'data/raw/members-{name}.json')))
    C = len(F.W)
    n = 0
    for m in mem:
        if m.get('dim') != 3:
            continue
        bits = int(m['bits'], 16)
        V = [None] * C
        V[0] = (QF(0), QF(0), QF(0))
        stack, ok = [0], True
        while stack:
            c = stack.pop()
            for i in range(3):
                d = F.nb[c][i]
                w = F.wallidx[(min(c, d), max(c, d))]
                r = F.walls[w][3] if F.walls[w][0] == c else tuple(-x for x in F.walls[w][3])
                vd = vsub(V[c], r) if bits >> w & 1 else V[c]
                if V[d] is None:
                    V[d] = vd
                    stack.append(d)
                elif vkey(V[d]) != vkey(vd):
                    ok = False
        pts = {}
        for v in V:
            pts[vkey(v)] = v
        P = [[frac(x.a) + frac(x.b) * mp.sqrt(D) for x in v] for v in pts.values()]
        if not ok or len(P) != m['V']:
            check(f'cone {m["label"]} rebuild', False, f'{len(P)} vs {m["V"]}')
        add(m['label'], m.get('name') or m['label'], 'cone', P, 'exact', 'study 2026-11-12-permutohedron-equal-edges',
            kind=m.get('kind'), cone=name, faces_desc=m.get('face_kinds'))
        n += 1
    print(f'PROGRESS {0.1 + 0.15 * ("A3", "B3", "H3").index(name):.2f} cone {name}: {n} solids ({time.time() - T0:.0f} s)', flush=True)
nc = sum(1 for s in solids if s['group'] == 'cone')
na = sum(1 for s in solids if s.get('kind', '').startswith('new atom'))
ns = sum(1 for s in solids if s.get('kind', '').startswith('sum of atoms'))
check('cone solids rebuilt: 17 + 103 orbits + 4427 = 4547, new atoms 2 + 2 + 367 = 371 rows (369 distinct: A3 pair = B3 pair), sums 54',
      nc == 4547 and na == 371 and ns == 54, f'{nc} {na} {ns}')

# ---------------- the DICTO silent zonohedron
a = -1 + mp.sqrt(1 + mp.sqrt(mp.mpf(5) / 6))
check('silent zonohedron a* ~ 0.383066', abs(a - mp.mpf('0.383066')) < 1e-6, mp.nstr(a, 12))
Z = set()
for p in itertools.permutations((a, a + 1, a + 2)):
    for sg in itertools.product((1, -1), repeat=3):
        Z.add(tuple(s * x for s, x in zip(sg, p)))
add('SILENT', 'DICTO silent zonohedron', 'silent', sorted(Z), 'exact', 'study 2026-11-14-forced-fixed-points (named 14 Nov 2026)')
check('silent zonohedron: 48 corners', len(Z) == 48)

# ---------------- Golden OGs (#91)
DP = os.path.join(ROOT, 'studies/2026-11-03-dual-pairs-dimensions/scripts')
sys.path.insert(0, DP)
cwd = os.getcwd()
os.chdir(DP)
import dp_lib
from dp_lib import Pair, platonic, x_golden, planes_of, hull3, vertices_H
P_ = Pair('dodecahedron', platonic()['dodecahedron'][0])


def kval(x):
    a_, b_, c_, d_ = x.v
    return frac(a_) + frac(b_) * mp.sqrt(2) + frac(c_) * mp.sqrt(5) + frac(d_) * mp.sqrt(10)


for which, lab, sid in ((1, 'Lesser Golden OG', 'GOLDEN_OG_L'), (0, 'Greater Golden OG', 'GOLDEN_OG_G')):
    x = x_golden(3)[which]
    mu = P_.mu_Ps(x)
    Hm = P_.Hull(mu)
    C_, F_, Pl_ = planes_of(Hm)
    Cq = hull3(vertices_H(Pl_ + [(v, P_.rho2) for v in P_.V]))[0]
    Cq, Fq = hull3(Cq)
    add(sid, lab, 'golden-og', [[kval(c) for c in v] for v in Cq], 'exact', 'study 2026-11-03-dual-pairs-dimensions, #91')
    check(f'{lab}: 102 corners, 80 faces (OG combinatorics)', len(Cq) == 102 and len(Fq) == 80, f'{len(Cq)} {len(Fq)}')
os.chdir(cwd)
print(f'PROGRESS 0.60 golden OGs ({time.time() - T0:.0f} s)', flush=True)


# ---------------- OG family (#39) + further steps (#80, #43) + Universal PiTet cycle (#38)
def faces_of(V, tol=1e-9):
    """merged face planes of the hull (unit normal n, offset d)"""
    h = ConvexHull(V)
    pl = []
    for e in h.equations:
        n, d = e[:3], -e[3]
        if not any(np.allclose(n, q[0], atol=tol) and abs(d - q[1]) < tol for q in pl):
            pl.append((n, d))
    return pl


def uniq(P, tol=1e-9):
    out = []
    for p in P:
        if not any(np.linalg.norm(p - q) < tol for q in out):
            out.append(p)
    return np.array(out)


def T(V):
    V = np.asarray(V)
    hs = np.hstack([V, -np.sum(V * V, axis=1)[:, None]])
    W = uniq(HalfspaceIntersection(hs, np.zeros(3)).intersections)
    h = ConvexHull(W)
    return W[np.unique(h.vertices)]


def Pd(V):
    return uniq(np.array([d * n for n, d in faces_of(V)]))


fam = json.load(open(os.path.join(ROOT, 'studies/2026-10-19-five-fold-octet/data/og-family-solids.json')))
want = {'DICTO TQHD': 162, 'DICTO TQP': 140, 'DICTO TQH': 132, 'DICTO TPH': 80, 'DICTO OG': 102, 'DICTO KRE': 92,
        'DICTO PHE': 180, 'DICTO TPP': 212, 'DICTO DPHP': 270}
S = fam['solids']
for k in fam['order']:
    V = np.array(S[k]['v'])
    check(f'{k}: {want[k]} corners in the float file', len(V) == want[k], str(len(V)))
    add(k.replace(' ', '_'), k, 'og-family', V, 'double', 'study 2026-10-19-five-fold-octet, #39', F=S[k].get('f'))
OG = np.array(S['DICTO OG']['v'])
up = [OG]
for i in range(6):
    up.append(T(up[-1]))
dn = [OG]
for i in range(11):
    dn.append(Pd(dn[-1]))
# controls: recomputed steps agree with the float file (same frame)
for i, k in enumerate(['DICTO KRE', 'DICTO PHE', 'DICTO TPP', 'DICTO DPHP'], 1):
    A, B = up[i], np.array(S[k]['v'])
    ok = len(A) == len(B) and max(min(np.linalg.norm(B - a, axis=1)) for a in A) < 1e-7
    check(f'control: T^{i}(OG) = {k} of the float file', ok, f'{len(A)} corners')
for i, k in enumerate(['DICTO TPH', 'DICTO TQH', 'DICTO TQP', 'DICTO TQHD'], 1):
    A, B = dn[i], np.array(S[k]['v'])
    ok = len(A) == len(B) and max(min(np.linalg.norm(B - a, axis=1)) for a in A) < 1e-7
    check(f'control: P^{i}(OG) = {k} of the float file', ok, f'{len(A)} corners')
for i, nm, nv, nf in ((5, 'Hamlet', 452, 270), (6, 'Ophelia', 642, 440)):
    f = len(faces_of(up[i]))
    check(f'{nm}: T^{i}(OG) has {nv} corners, {nf} faces (Concordance)', len(up[i]) == nv and f == nf, f'{len(up[i])} {f}')
    add(nm.upper(), nm, 'og-family', up[i], 'double', 'recomputed T^%d(OG), #80' % i)
for i, nm, nf in ((5, 'DICTO TQP-252', 252), (6, 'DICTO TQ-320', 320), (7, 'DICTO TQP-402', 402), (8, 'DICTO TQ-500', 500),
                  (9, 'DICTO TQD-732', 732), (10, 'DICTO TQHD-662', 662), (11, 'DICTO TQP-672', 672)):
    f = len(faces_of(dn[i]))
    check(f'{nm}: P^{i}(OG) has {nf} faces (Concordance)', f == nf, str(f))
    add(nm.replace(' ', '_'), nm, 'og-family', dn[i], 'double', 'recomputed P^%d(OG), #43' % i)
# Universal PiTet cycle from the icosidodecahedron of circumradius phi
ph = (1 + 5 ** 0.5) / 2
ID = set()
for p in [(0, 0, ph), (0.5, ph / 2, ph * ph / 2)]:
    for c in range(3):
        q = p[c:] + p[:c]
        for sg in itertools.product((1, -1), repeat=3):
            ID.add(tuple(round(s * x, 12) + 0.0 for s, x in zip(sg, q)))
ID = np.array(sorted(ID))
cyc = [ID]
for i in range(4):
    cyc.append(T(cyc[-1]))
check('PiTet cycle: ID 30 -> RT 32 -> golden TI 60 -> Q 32 -> ID 30 (#38)', [len(c) for c in cyc] == [30, 32, 60, 32, 30],
      str([len(c) for c in cyc]))
add('PITET_GOLDEN_TI', 'Universal PiTet golden truncated icosahedron (T^2 of the icosidodecahedron)', 'og-family', cyc[2], 'double', '#38')
add('PITET_Q', 'Universal PiTet Q, pentakis type (T^3 of the icosidodecahedron)', 'og-family', cyc[3], 'double', '#38')
print(f'PROGRESS 0.80 OG family ({time.time() - T0:.0f} s)', flush=True)

# ---------------- registry (389)
reg = json.load(open(os.path.join(ROOT, 'studies/2026-11-13-platonic-disc-ranking/data/registry-solids.json')))
for s in reg:
    add('REG:' + s['id'], s['name'], 'registry', s['V'], 'double', 'app registry (disc-ranking study)', F=s['F'])
check('registry: 389 solids', sum(1 for s in solids if s['group'] == 'registry') == 389)

# ---------------- hybrid kit (exact Q(sqrt5))
sys.path.insert(0, os.path.join(ROOT, 'studies/2026-11-14-platonic-hybrid/scripts'))
import golden as G


def q5(x):
    return frac(x.a) + frac(x.b) * mp.sqrt(5)


cap = G.caps8()[0][1]
add('HYB_CAP', 'hybrid cap (dodecahedron minus octahedron, one octant)', 'hybrid', [[q5(c) for c in v] for v in cap], 'exact',
    'study 2026-11-14-platonic-hybrid')
R = G.ROOFS[(2, 1)]
add('HYB_ROOF_R', "Euclid's roof R on the cube of edge phi", 'hybrid', [[q5(c) for c in v] for v in R], 'exact', 'study 2026-11-14-platonic-hybrid')
# Z: box phi x phi x 1/2 over the cube face z = phi/2, minus the roof standing on that face (ridge on the top face)
hf, half = G.HF, G.HALF
box = [G.V(x, y, z) for x in (-hf, hf) for y in (-hf, hf) for z in (hf, hf + half)]
ridge = [v for v in R if v[2] != hf]
Zc = box + ridge
add('HYB_PLATE_Z', 'hybrid roof plate Z (box minus roof; non-convex)', 'hybrid', [[q5(c) for c in v] for v in Zc], 'exact',
    'study 2026-11-14-platonic-hybrid', convex=False)
check('Z: ridge ends lie on the top face of the box (roof height 1/2)', all(v[2] == hf + half for v in ridge) and len(ridge) == 2)
ac = G.admiral_caps()[0]
acV = {tuple(v) for t in ac for v in t}
add('HYB_ADMIRAL_CAP', 'Admiral Cap (two tetrahedra; non-convex)', 'hybrid', [[q5(c) for c in v] for v in acV], 'exact',
    'study 2026-11-14-platonic-hybrid', convex=False)
check('Admiral Cap: 5 corners', len(acV) == 5)

json.dump({'made': time.strftime('%Y-%m-%d'), 'solids': solids}, open(OUT, 'w'))
groups = {}
for s in solids:
    groups[s['group']] = groups.get(s['group'], 0) + 1
print('groups', groups, flush=True)
bad = [c for c in CHECKS if not c[1]]
print(f'checks {len(CHECKS) - len(bad)}/{len(CHECKS)}, {time.time() - T0:.0f} s', flush=True)
print('FINAL ok' if not bad else 'FINAL FAIL', flush=True)
