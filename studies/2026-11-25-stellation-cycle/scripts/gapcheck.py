"""Task 2, the hits of gaps.py checked.
(c) the D5d station die (study 2026-11-19 sid 77; Theorem 8: its faces lie on D0's and RT0's planes, all exact) between the
    DICTO-Star's icosidodecahedron and the star's hull: exact in Q(sqrt5). The star's corners (#14 data, 12 digits) are recognised
    as (a + b sqrt5)/4 with small integers and then checked exactly: every edge of the 12 dodecahedra and 20 J63 caps has length 1.
(a) the two dice that fit in O ⊂ rTI (sids 6 and 63; the 4553 study): ball arithmetic on the certified depths (certify-extend
    Part 1), O and rTI exact (data/stations.json). Prints the reach t1 (fit iff t1 < 1) with its enclosure.
(d) the 131 float 'touches' of D0 ⊂ hull(Sunstar): checked to be the 8 cube corners of D0, which lie on the hull already.
-> data/gapcheck.json"""
import json, os, sys, itertools
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ST, '2026-11-24-aequi-exact-dice', 'scripts')); sys.path.insert(0, HERE)
from groups import DIRS, DFAM
from qsqrt5 import K, PHI, IPHI, dot, cross, sub, scl, cyc_signs
from flint import arb, ctx
ctx.prec = 300
src = open(os.path.join(HERE, 'exact42.py')).read().split('\nco = json.load(')[0]      # helpers only, not the run
ex = {'__file__': os.path.join(HERE, 'exact42.py')}; exec(compile(src, 'exact42-helpers', 'exec'), ex)
EX, H, solve3, A, norm_arb = ex['EX'], ex['H'], ex['solve3'], ex['A'], ex['norm_arb']
R5 = 5 ** .5
def recog(x):
    for b in range(-40, 41):
        a = round(4 * x - b * R5)
        if abs((a + b * R5) / 4 - x) < 1e-10: return K(Fr(a, 4), Fr(b, 4))
    raise ValueError(x)
def kmax(L): return max(L, key=float)
def exact_facets(V):
    """facets of conv(V), V exact: from the float hull, each facet re-made through 3 exact corners and checked exactly"""
    Vf = np.array([[float(t) for t in v] for v in V]); Hh = ConvexHull(Vf); F = {}
    for s in Hh.simplices:
        a, b, c = (V[i] for i in s); n = cross(sub(b, a), sub(c, a)); h = dot(n, a)
        if h.sign() < 0: n, h = scl(K(-1), n), K(0) - h
        key = tuple(round(float(t) / float(h), 9) for t in n)
        if key in F: continue
        assert all((h - dot(n, v)).sign() >= 0 for v in V)
        F[key] = (n, h)
    return list(F.values())
res = {}
# ---------------- (c) ----------------
SW = lambda v: (v[1], v[0], v[2])
star = json.load(open(os.path.join(ST, '..', 'papers', 'dicto-star', 'data', 'dicto-star.json')))['pieces']
IDs = [SW(tuple(recog(t) for t in v)) for v in star['icosidodecahedron']]
pieces = [[SW(tuple(recog(t) for t in v)) for v in P] for P in star['dodecahedra'] + star['tridiminishedIcosahedra_J63']]
edge_ok = True
for P in pieces:
    Pf = np.array([[float(t) for t in v] for v in P]); Hh = ConvexHull(Pf)
    for s in Hh.simplices:
        for i, j in itertools.combinations(s, 2):
            d2 = dot(sub(P[i], P[j]), sub(P[i], P[j]))
            if abs(float(d2) - 1) < 1e-6: edge_ok &= (d2 == K(1))
assert all(dot(v, v) == PHI * PHI for v in IDs), 'star icosidodecahedron: circumradius phi'
Vst = list({v for P in pieces for v in P} | set(IDs)); Fst = exact_facets(Vst)
# die 77: planes of D12/2 at h = phi^2 and C6+RT24/10 at the RT0 offsets (Theorem 8); scale 1 = RT0 depth phi
import glob
d77 = json.load(open(glob.glob(os.path.join(ST, '2026-11-19-aequi-complete', 'data', 'dice', '0077-*.json'))[0]))
assert str(d77['sid']) == '77'
q = [EX[i] for i in d77['face_directions']]; h = [H[DFAM[i]] for i in d77['face_directions']]
C77 = []
for a, b, c in itertools.combinations(range(len(q)), 3):
    x = solve3([q[a], q[b], q[c]], [h[a], h[b], h[c]])
    if x is not None and all((h[k] - dot(q[k], x)).sign() >= 0 for k in range(len(q))) and x not in C77: C77.append(x)
s1 = kmax([dot(q[k], v) / h[k] for v in IDs for k in range(len(q))])
t1 = kmax([dot(n, scl(s1, x)) / hh for x in C77 for n, hh in Fst])
inner = sum(1 for v in IDs if any(dot(q[k], v) == s1 * h[k] for k in range(len(q))))
outer = sum(1 for x in C77 if any(dot(n, scl(s1, x)) == hh for n, hh in Fst))
outer_on_star_corner = sum(1 for x in C77 if scl(s1, x) in set(Vst))
faces_touching = sorted({DFAM[d77['face_directions'][k]] for k in range(len(q)) for v in IDs if dot(q[k], v) == s1 * h[k]})
res['c'] = dict(die='4553 sid 77, D5d: C6+RT24/10 + D12/2 (2)', star_edges_exact=edge_ok, star_corners=len(Vst), star_hull_facets=len(Fst),
                die_corners=len(C77), s1='%s + %s*sqrt5' % (s1.a, s1.b), t1='%s + %s*sqrt5' % (t1.a, t1.b), closes=(t1 == K(1)), ID_corners_on_die_faces=inner, die_faces_touching_ID=faces_touching,
                die_corners_on_star_hull=outer, of_which_star_corners=outer_on_star_corner)
print('(c)', res['c'], flush=True)
# ---------------- (a) ----------------
st = json.load(open(os.path.join(HERE, '..', 'data', 'stations.json')))
def kv(v): return tuple(K(Fr(a), Fr(b)) for a, b in v)
O = [kv(v) for v in st['O']['exact']]; rTI = [kv(v) for v in st['rTI']['exact']]; FR = exact_facets(rTI)
res['a'] = []
for l in open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', 'certify-pass1.jsonl')):
    d = json.loads(l)
    if d['study'] != '2026-11-19-aequi-complete' or str(d['sid']) not in ('6', '63'): continue
    t = eval(d['tight']) if isinstance(d['tight'], str) else d['tight']
    dep = [arb(1)] + [arb(s) for s in t['enclosure']]
    die = json.load(open(glob.glob(os.path.join(ST, '2026-11-19-aequi-complete', 'data', 'dice', '%04d-*.json' % int(d['sid'])))[0]))
    idx = die['face_directions']; orb = np.repeat(np.arange(len(die['orbit_sizes'])), die['orbit_sizes'])
    Df = np.repeat([float(x) for x in die['depths_60_digits']], die['orbit_sizes'])
    hs = HalfspaceIntersection(np.hstack([DIRS[idx], -Df[:, None]]), np.zeros(3))
    # each corner from three of its planes (the face structure is certified constant on the box)
    corners = []
    for v in hs.intersections:
        I = [i for i in range(len(idx)) if abs(DIRS[idx[i]] @ v - Df[i]) < 1e-9]
        for a, b, c in itertools.combinations(I, 3):
            M = np.array([DIRS[idx[a]], DIRS[idx[b]], DIRS[idx[c]]])
            if abs(np.linalg.det(M)) > 1e-3: corners.append((a, b, c)); break
    corners = list(set(corners))
    uq = [[A(t) / norm_arb(EX[i]) for t in EX[i]] for i in idx]
    def solve(a, b, c):
        M = [uq[a], uq[b], uq[c]]; rhs = [dep[orb[a]], dep[orb[b]], dep[orb[c]]]
        det = lambda m: m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        D0 = det(M); out = []
        for col in range(3):
            Mc = [[rhs[r] if cc == col else M[r][cc] for cc in range(3)] for r in range(3)]; out.append(det(Mc) / D0)
        return out
    Vc = [solve(*c) for c in corners]
    s1 = None
    for v in O:
        va = [A(t) for t in v]
        for i in range(len(idx)):
            x = sum((uq[i][k] * va[k] for k in range(3)), arb(0)) / dep[orb[i]]
            s1 = x if s1 is None or x.mid() > s1.mid() else s1
    t1 = None
    for x in Vc:
        for n, hh in FR:
            y = s1 * sum((A(n[k]) * x[k] for k in range(3)), arb(0)) / A(hh)
            t1 = y if t1 is None or y.mid() > t1.mid() else t1
    r = dict(die='4553 sid %s, %s' % (d['sid'], d['label']), corners=len(Vc), s1=str(s1)[:40], t1=str(t1)[:40], fits_strictly=bool(t1 < 1))
    # touching: O corners on s1.P faces (float count)
    res['a'].append(r); print('(a)', r, flush=True)
# ---------------- (d) ----------------
G = json.load(open(os.path.join(HERE, '..', 'data', 'gaps.json')))['d']['touching']
cube = np.array(list(itertools.product((1, -1), repeat=3)), float)
phi = (1 + R5) / 2
def rot5(k):
    a = np.array([0, phi, 1.]); a /= np.linalg.norm(a); t = 2 * np.pi * k / 5; Km = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(t) * Km + (1 - np.cos(t)) * Km @ Km
pinch = 0; other_d = []
D0 = np.array([s for s in itertools.product((1, -1), repeat=3)], float)
Is = np.array([np.roll((0, a * phi, b), kk) for a in (1, -1) for b in (1, -1) for kk in range(3)], float)
D0full = np.vstack([D0, np.array([np.roll((0, a / phi, b * phi), kk) for a in (1, -1) for b in (1, -1) for kk in range(3)], float)])
sun = [D0full]
for i in range(3):
    for sg in (1, -1):
        c = np.zeros(3); c[i] = 2 * sg; sun += [c + Is / phi ** 2, c + D0]
Hs = ConvexHull(np.vstack(sun)); GD = (Hs.equations[:, :3], -Hs.equations[:, 3], None)
gd = json.load(open(os.path.join(HERE, '..', 'data', 'gaps.json')))
for t1, srcs, sid, label, k, s1 in G:
    if srcs == '4553':
        die = json.load(open(glob.glob(os.path.join(ST, '2026-11-19-aequi-complete', 'data', 'dice', '%04d-*.json' % int(sid)))[0]))
        idx, sizes, deps = die['face_directions'], die['orbit_sizes'], [float(x) for x in die['depths_60_digits']]
    else:
        b = srcs.split()[1]; dd = [x for x in json.load(open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', 'dice%s-new.json' % b))) if str(x['sid']) == sid][0]
        ev = lambda x: eval(x) if isinstance(x, str) else x; idx, sizes, deps = ev(dd['idx']), ev(dd['sizes']), [float(x) for x in ev(dd['depths'])]
    U = DIRS[idx] @ rot5(k).T; Dd = np.repeat(deps, sizes)
    V = HalfspaceIntersection(np.hstack([U, -Dd[:, None]]), np.zeros(3)).intersections * s1
    n, hh, _ = GD
    outer = [v for v in V if abs((v @ n.T / hh).max() - 1) < 1e-9]
    inner = [(D0[a], U[b]) for a in range(8) for b in range(len(U)) if abs(D0[a] @ U[b] / Dd[b] / s1 - 1) < 1e-9]
    ax3 = all(abs(np.abs(v).max() - 3) < 1e-7 and abs(np.sort(np.abs(v))[1] - np.sort(np.abs(v))[0]) < 1e-7 for v in outer)   # on x = +-3 with |y| = |z| (cyclic)
    o8 = all(np.allclose(np.abs(u), 1 / 3 ** .5) for p, u in inner) and len(inner) > 0
    pinch += bool(outer) and ax3 and o8
    if not (bool(outer) and ax3 and o8) and len(other_d) < 6:
        other_d.append(dict(die=(srcs, sid, label, k), outer=[v.round(6).tolist() for v in outer][:3], outer_facets=[(n[j] / hh[j]).round(6).tolist() for v in outer[:1] for j in range(len(hh)) if abs(v @ n[j] / hh[j] - 1) < 1e-9],
                            inner=[(p.tolist(), u.round(4).tolist()) for p, u in inner][:3]))
res['d'] = dict(touch_candidates=len(G), touching_through_the_octahedron=pinch,
                explanation='every inner contact is a three-fold face of the die through a cube corner of D0 (planes +-x +-y +-z = 3), and every outer contact is a die corner on a square face x = +-3 of the Sunstar hull with |y| = |z| (cyclic): it lies on the line where two of those planes meet, e.g. (x + y + z = 3) and (x - y - z = 3) meet in x = 3, y = -z. So the contacts come from the regular octahedron |x| + |y| + |z| <= 3 on D0s cube corners, whose edges-lines through (+-3,0,0) lie in the hull faces')
res['d']['others_sample'] = other_d
print('(d)', res['d'])
json.dump(res, open(os.path.join(HERE, '..', 'data', 'gapcheck.json'), 'w'), indent=1, default=str)
ok = res['c']['star_edges_exact'] and res['c']['closes'] and all(r['fits_strictly'] for r in res['a']) and pinch == len(G)
print('FINAL ok' if ok else 'FINAL FAIL (see above)')
