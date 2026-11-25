# DICTO · dictospheres.com — the figures of "Fair Dice from Curvature" (blueprint draft, 25 Nov 2026), in the house look of #118 v2:
# scenes for the three.js renderer render3d.py of study 2026-11-21-scutoid-stand-in (used unchanged), shot at 1600 px by its
# shots.mjs, composed by its compose.py (dark warm ground, title, subtitle, swatches, DICTO mark).  With Claude (Anthropic).
#   Figure 1: four fair dice of #112 (Ih 1, Oh 1, Td 1, Th 3), each whole, see-through over its sphere of view, and pulled apart
#             into its face pyramids.  Corners from #112's 60-digit depths; every solid angle re-checked here at 70 digits.
#   Figure 2: the polar identity in 3D on the D2d shadow die (study 2026-11-24-aequi-exact-dice, Theorem 2): the cone from the
#             centre through one face and the cone of outer normals of the polar at the matching corner; EXACT check (rationals,
#             Girard's formula with exact angles) that both are the same cone, of solid angle pi/2 = 4 pi/8, for every face.
#   Figure 3: Alexandrov's condition for the face directions of Aequus CO-14 (Oh 1), kappa_i = 4 pi/14: two sets I, the region within
#             pi/2 of I shaded; its area in closed form (exact), compared with the sum of kappa_i over I.
# Usage: python fig_scenes.py scenes [pilot]  -> renders/fig*.html, renders/meta.json, scripts/fig_checks.log
#        python fig_scenes.py compose [pilot] -> figures/fig*.jpg and renders/PREVIEW-fairdice-fig*.png
import json, os, sys, itertools
from fractions import Fraction as Q
import numpy as np
import mpmath as mp
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); PAPER = os.path.normpath(os.path.join(HERE, '..'))
ST = os.environ.get('STUDIES', os.path.normpath(os.path.join(PAPER, '../../studies')))
REN = os.path.join(PAPER, 'renders'); FIG = os.path.join(PAPER, 'figures')
sys.path.insert(0, os.path.join(ST, '2026-11-24-aequi-exact-dice/scripts'))
sys.path.insert(0, os.path.join(ST, '2026-11-21-scutoid-stand-in/renders/scripts'))
from groups import DIRS, DFAM            # the 122 frame directions of #112's studies (indices 0..73 as in study 2026-11-19-aequi-complete)
from qsqrt5 import K, PHI, IPHI, cyc_signs
import render3d as R3
PILOT = 'pilot' in sys.argv[2:]
LOG = []
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)

# ---------- exact directions (as prove_shadow.py of study 2026-11-24-aequi-exact-dice) ----------
ONE, Z = K(1), K(0)
PAT = {'C6': (ONE, Z, Z), 'O8': (ONE, ONE, ONE), 'RD12': (ONE, ONE, Z), 'D12': (Z, PHI, ONE), 'I12': (Z, IPHI, PHI), 'RT24': (ONE, PHI, IPHI),
       'D12p': (Z, ONE, PHI), 'I12p': (Z, PHI, IPHI), 'RT24p': (PHI, ONE, IPHI)}
EX = []
for v, f in zip(DIRS, DFAM):
    m = [w for w in cyc_signs(PAT[f]) if np.abs(np.array([float(x) for x in w]) / np.linalg.norm([float(x) for x in w]) - v).max() < 1e-9]
    assert len(m) == 1; EX.append(m[0])
mp.mp.dps = 70
def mpk(x): return mp.mpf(x.a.numerator) / x.a.denominator + mp.mpf(x.b.numerator) / x.b.denominator * mp.sqrt(5)
def kdot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def kcross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def ksub(a, b): return tuple(x - y for x, y in zip(a, b))
def ksym(x): return sp.Rational(x.a.numerator, x.a.denominator) + sp.Rational(x.b.numerator, x.b.denominator) * sp.sqrt(5)

# ---------- colours (labels only: neutral; none of the five solid colours) ----------
KIND = [(214, 180, 106), (127, 147, 168), (201, 158, 149), (156, 116, 72), (143, 138, 128)]   # compose.py's neutral label tones
PEARL, SLATE, TEAL, INK = (226, 222, 214), (127, 147, 168), (64, 170, 160), (43, 38, 30)
EDGE = '#2b261e'
def hx(c): return '#%02x%02x%02x' % tuple(int(round(x)) for x in c)
def shade(c, k): return tuple(int(round(x * (1 + k) if k < 0 else x + (255 - x) * k)) for x in c)
DIR = [0.62, 0.48, 1.0]

# ---------- geometry helpers ----------
def die_poly(n, d):
    """corners, faces (corner lists, counter-clockwise seen from outside) and edges of {x : n_j.x <= d_j}, in floats."""
    N = len(n); V = []
    for i, j, k in itertools.combinations(range(N), 3):
        A = n[[i, j, k]]
        if abs(np.linalg.det(A)) < 1e-9: continue
        x = np.linalg.solve(A, d[[i, j, k]])
        if (n @ x <= d + 1e-9).all() and not any(np.abs(x - w).max() < 1e-7 for w in V): V.append(x)
    V = np.array(V); inc = [set(np.where(np.abs(n @ v - d) < 1e-7)[0]) for v in V]
    faces = []
    for f in range(N):
        S = [v for v in range(len(V)) if f in inc[v]]; assert len(S) >= 3, 'redundant face'
        c = V[S].mean(0); e1 = V[S[0]] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(n[f], e1)
        faces.append(sorted(S, key=lambda v: np.arctan2((V[v] - c) @ e2, (V[v] - c) @ e1)))
    edges = sorted({tuple(sorted((F[a], F[(a + 1) % len(F)]))) for F in faces for a in range(len(F))})
    assert len(V) - len(edges) + N == 2, 'Euler'
    return V, faces, edges, inc

def part(V, tris, cols, alpha=1.0, tubes=(), rad=0.004):
    return {'v': np.round(np.asarray(V, float), 6).tolist(), 't': [list(map(int, t)) for t in tris], 'c': [hx(c) for c in cols],
            'a': alpha, 'tubes': [[int(a), int(b), EDGE, None] for a, b in tubes], 'rad': rad, 'balls': []}

def soup(tris, cols, alpha=1.0):
    """triangles given by coordinates (k, 3, 3) -> a part (no shared corners); for rods and patches that must show through glass."""
    T = np.asarray(tris, float).reshape(-1, 3)
    return {'v': np.round(T, 6).tolist(), 't': [[3 * i, 3 * i + 1, 3 * i + 2] for i in range(len(T) // 3)], 'c': [hx(c) for c in cols],
            'a': alpha, 'tubes': [], 'rad': 0.004, 'balls': []}

def rod(a, b, r, seg=10):
    """an opaque thin prism from a to b (edges inside see-through shells: the renderer hides tubes behind glass)."""
    a, b = np.asarray(a, float), np.asarray(b, float); d = b - a; d /= np.linalg.norm(d)
    p = np.cross(d, [0.31, 0.77, 0.55]); p /= np.linalg.norm(p); q = np.cross(d, p); out = []
    ring = [r * (np.cos(t) * p + np.sin(t) * q) for t in np.linspace(0, 2 * np.pi, seg + 1)]
    for k in range(seg):
        out += [[a + ring[k], b + ring[k], b + ring[k + 1]], [a + ring[k], b + ring[k + 1], a + ring[k + 1]]]
    return out

def ball(c, r, lev=2):
    """a small opaque icosphere (corner markers that must show through glass)."""
    t = (1 + 5 ** .5) / 2
    P = [np.array(v, float) for v in [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
                                      (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]]
    F = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2),
         (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    T = [[P[i] / np.linalg.norm(P[i]) for i in f] for f in F]
    for _ in range(lev):
        T2 = []
        for a, b, c2 in T:
            m = [(x + y) / np.linalg.norm(x + y) for x, y in ((a, b), (b, c2), (c2, a))]
            T2 += [[a, m[0], m[2]], [m[0], b, m[1]], [m[2], m[1], c2], [m[0], m[1], m[2]]]
        T = T2
    return [[np.asarray(c) + r * v for v in t] for t in T]

def icosphere(lev):
    T = ball((0, 0, 0), 1.0, 0); T = [[np.asarray(v) for v in t] for t in T]
    for _ in range(lev):
        T2 = []
        for a, b, c2 in T:
            m = [(x + y) / np.linalg.norm(x + y) for x, y in ((a, b), (b, c2), (c2, a))]
            T2 += [[a, m[0], m[2]], [m[0], b, m[1]], [m[2], m[1], c2], [m[0], m[1], m[2]]]
        T = T2
    return T

def arc(a, b, r, k=40):
    a, b = np.asarray(a, float), np.asarray(b, float); a /= np.linalg.norm(a); b /= np.linalg.norm(b)
    w = np.arccos(np.clip(a @ b, -1, 1)); P = [(np.sin((1 - t) * w) * a + np.sin(t * w) * b) / np.sin(w) for t in np.linspace(0, 1, k + 1)]
    return [r * p for p in P]

def extent(parts, dirv, m=1.08):
    x, y, _ = R3.basis(dirv); P = np.vstack([np.asarray(p['v']) for p in parts])
    return float(m * max(np.abs(P @ x).max(), np.abs(P @ y).max()))

def subdivide(a, b, c, m):
    """the flat triangle abc cut into m*m small triangles."""
    P = lambda i, j: a + (b - a) * i / m + (c - a) * j / m; out = []
    for i in range(m):
        for j in range(m - i):
            out.append([P(i, j), P(i + 1, j), P(i, j + 1)])
            if i + j < m - 1: out.append([P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)])
    return out

def clip(poly, nrm):
    """split a convex polygon (list of 3-vectors) by the plane nrm.x = 0 -> (part with nrm.x >= 0, part with nrm.x <= 0)."""
    pos, neg = [], []; L = len(poly)
    for i in range(L):
        a, b = poly[i], poly[(i + 1) % L]; sa, sb = nrm @ a, nrm @ b
        if sa >= 0: pos.append(a)
        if sa <= 0: neg.append(a)
        if (sa > 0 and sb < 0) or (sa < 0 and sb > 0):
            t = sa / (sa - sb); x = a + t * (b - a); pos.append(x); neg.append(x)
    return pos, neg

# ---------- exact spherical polygons (Girard) ----------
def sph_area_exact(P):
    """P: exact K-vectors, corners of a convex spherical polygon in cyclic order -> its area, a sympy expression (exact)."""
    m = len(P); S = [tuple(ksym(x) for x in p) for p in P]; tot = 0; angs = []
    for i in range(m):
        a, b, c = S[i - 1], S[i], S[(i + 1) % m]
        u = sp.Matrix(b).cross(sp.Matrix(a)); w = sp.Matrix(b).cross(sp.Matrix(c))
        cs = sp.nsimplify(sp.radsimp(sp.simplify(u.dot(w) / sp.sqrt(u.dot(u) * w.dot(w)))))
        al = sp.acos(cs); angs.append(al); tot += al
    return sp.simplify(tot - (m - 2) * sp.pi), angs

def cyclic(P):
    """cyclic order (float) of exact vectors around their mean direction."""
    F = np.array([[float(x) for x in p] for p in P]); F /= np.linalg.norm(F, axis=1)[:, None]; c = F.mean(0); c /= np.linalg.norm(c)
    e1 = F[0] - (F[0] @ c) * c; e1 /= np.linalg.norm(e1); e2 = np.cross(c, e1)
    return sorted(range(len(P)), key=lambda i: np.arctan2(F[i] @ e2, F[i] @ e1))

def mp_solid_angle(P):
    """area of the spherical polygon over the corners P (mp vectors, cyclic) by Van Oosterom and Strackee (1983), fan from P[0]."""
    def d3(a, b, c): return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
    def dt(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    tot = mp.mpf(0)
    for i in range(1, len(P) - 1):
        a, b, c = P[0], P[i], P[i + 1]; la, lb, lc = mp.sqrt(dt(a, a)), mp.sqrt(dt(b, b)), mp.sqrt(dt(c, c))
        tot += 2 * mp.atan2(abs(d3(a, b, c)), la * lb * lc + dt(a, b) * lc + dt(a, c) * lb + dt(b, c) * la)
    return tot

# =====================================================================================================================
# Figure 1: four fair dice of #112
DICE = [('0003-Ih-O8-I12-20-D12', 'Aequus DI-32, Ih 1', 'Ih'), ('0010-Oh-C6-O8', 'Aequus CO-14, Oh 1', 'Oh'),
        ('0019-Td-C6-O8-4', 'Aequus TC-10, Td 1', 'Td'), ('0026-Th-O8-D12', 'Aequus OD-20, Th 3', 'Th')]
GON = {3: 'triangles', 4: 'squares', 5: 'pentagons', 6: 'hexagons', 7: 'heptagons', 8: 'octagons', 10: 'decagons'}

def load_die(tag):
    D = json.load(open(os.path.join(ST, '2026-11-19-aequi-complete/data/dice', tag + '.json')))
    idx = D['face_directions']; orb = sum(([j] * s for j, s in enumerate(D['orbit_sizes'])), [])
    dep60 = [mp.mpf(D['depths_60_digits'][j]) for j in orb]
    nm = [[mpk(x) for x in EX[i]] for i in idx]; nm = [[x / mp.sqrt(sum(y * y for y in v)) for x in v] for v in nm]
    n = np.array([[float(x) for x in v] for v in nm]); d = np.array([float(x) for x in dep60])
    return D, idx, orb, nm, dep60, n, d

def check_die(nm, dep, V, faces, inc):
    """every face's solid angle at 70 digits, from the 60-digit depths: corners re-solved in mp on three of their planes."""
    N = len(nm); Vm = []
    for v, I in zip(V, inc):
        I = sorted(I)
        for tri in itertools.combinations(I, 3):
            A = mp.matrix([nm[i] for i in tri])
            if abs(mp.det(A)) > mp.mpf('1e-6'): break
        x = mp.lu_solve(A, mp.matrix([dep[i] for i in tri])); Vm.append([x[0], x[1], x[2]])
        res = max(abs(sum(nm[i][k] * x[k] for k in range(3)) - dep[i]) for i in I)
        assert res < mp.mpf('1e-55'), res
    Om = [mp_solid_angle([Vm[v] for v in F]) for F in faces]
    return max(abs(o - 4 * mp.pi / N) for o in Om), abs(sum(Om) - 4 * mp.pi)

def fig1():
    scenes, meta = [], []
    for tag, name, grp in (DICE[1:2] if PILOT else DICE):
        D, idx, orb, nm, dep, n, d = load_die(tag)
        V, faces, edges, inc = die_poly(n, d); N = len(n)
        assert len(V) == D['corners'], (len(V), D['corners'])
        err, tot = check_die(nm, dep, V, faces, inc)
        log(f'Figure 1 {name}: N={N}, corners {len(V)}, max |Omega_k - 4pi/N| = {mp.nstr(err, 3)}, |sum - 4pi| = {mp.nstr(tot, 3)} (70 digits)')
        assert err < mp.mpf('1e-50')
        col = [KIND[orb[f]] for f in range(N)]
        # A: whole
        tris, cols = [], []
        for f, F in enumerate(faces):
            for a in range(1, len(F) - 1): tris.append([F[0], F[a], F[a + 1]]); cols.append(col[f])
        A = part(V, tris, cols, 1.0, edges, 0.0045)
        # B: see-through, over the sphere of view: each face's central projection, edges of the cells as rods
        rs = 0.62 * d.min(); pt, pc = [], []
        for f, F in enumerate(faces):
            c = V[F].mean(0)
            for a in range(len(F)):
                for t in subdivide(c, V[F[a]], V[F[(a + 1) % len(F)]], 10):
                    pt.append([rs * p / np.linalg.norm(p) for p in t]); pc.append(shade(col[f], 0.12))
        rods = []
        for a, b in edges:
            P = arc(V[a], V[b], rs * 1.004, 24)
            for p, q in zip(P[:-1], P[1:]): rods += rod(p, q, 0.006 * rs, 6)
        B = [part(V, tris, cols, 0.30, edges, 0.0045), soup(pt, pc), soup(rods, [INK] * len(rods)), soup(ball((0, 0, 0), 0.03 * rs), [INK] * 320)]
        # C: pulled apart into the N face pyramids (apex at the centre), each moved out along the ray through its face centre
        C = []
        for f, F in enumerate(faces):
            c = V[F].mean(0); sh = 0.95 * c; P = [np.zeros(3)] + [V[v] for v in F]
            tt = [[0, 1 + a, 1 + (a + 1) % len(F)] for a in range(len(F))] + [[1, 1 + a, 2 + a] for a in range(1, len(F) - 1)]
            cc = [shade(col[f], -0.32)] * len(F) + [col[f]] * (len(F) - 2)
            tb = [(0, 1 + a) for a in range(len(F))] + [(1 + a, 1 + (a + 1) % len(F)) for a in range(len(F))]
            C.append(part(np.array(P) + sh, tt, cc, 1.0, tb, 0.0040))
        EAB = extent([A], DIR); EC = extent(C, DIR)
        scenes += [{'E': EAB, 'dir': DIR, 'parts': [A]}, {'E': EAB, 'dir': DIR, 'parts': B}, {'E': EC, 'dir': DIR, 'parts': C}]
        kinds = [(KIND[j], f"{s} {GON[int(D['faces_by_orbit'][j].split('×')[1].split('-')[0])]}") for j, s in enumerate(D['orbit_sizes'])]
        meta.append(dict(name=name, grp=grp, N=N, corners=len(V), depths=[mp.nstr(mp.mpf(x), 12, strip_zeros=True).rstrip('.0') if mp.mpf(x) == 1 else mp.nstr(mp.mpf(x), 12) for x in D['depths_60_digits']],
                         kinds=kinds, err=mp.nstr(err, 2), orbits=D['orbits']))
    R3.write(os.path.join(REN, 'fig1.html'), scenes); return meta

# =====================================================================================================================
# Figure 2: the polar identity on the D2d shadow die (study 2026-11-19-aequi-complete row 787; exact by Theorem 2 of 2026-11-24-aequi-exact-dice)
IDX2 = [14, 16, 18, 22, 15, 17, 19, 20]

def kdet(a, b, c): return kdot(a, kcross(b, c))

def fig2():
    q = [EX[i] for i in IDX2]; N = len(q); h = [ONE] * N            # die {x : q_j.x <= 1}; all depths equal (catalogue ratios 1, 1)
    for v in q: assert DFAM[IDX2[q.index(v)]] == 'RD12'
    # exact corners of the die
    V = []
    for i, j, k in itertools.combinations(range(N), 3):
        dt = kdet(q[i], q[j], q[k])
        if dt.sign() == 0: continue
        M = [[q[i][c] for c in range(3)], [q[j][c] for c in range(3)], [q[k][c] for c in range(3)]]
        cols_ = [[M[0][c], M[1][c], M[2][c]] for c in range(3)]
        x = []
        for r in range(3):
            cc = [list(col_) for col_ in cols_]; cc[r] = [h[i], h[j], h[k]]
            x.append(kdet(tuple(cc[0]), tuple(cc[1]), tuple(cc[2])) / dt)
        x = tuple(x)
        if all((h[m] - kdot(q[m], x)).sign() >= 0 for m in range(N)) and x not in V: V.append(x)
    inc = [{m for m in range(N) if (h[m] - kdot(q[m], v)).sign() == 0} for v in V]
    log(f'Figure 2: D2d die (row 787), N = {N} faces, {len(V)} corners (exact rationals)')
    p = [tuple(x / h[j] for x in q[j]) for j in range(N)]                 # polar corners n_j/d_j = q_j/h_j
    # polar facets, exactly: planes through three polar corners with every polar corner on one side
    facets = {}
    for a, b, c in itertools.combinations(range(N), 3):
        m = kcross(ksub(p[b], p[a]), ksub(p[c], p[a]))
        if all(x.sign() == 0 for x in m): continue
        c0 = kdot(m, p[a])
        if c0.sign() == 0: continue                                          # plane through the centre: no facet
        if c0.sign() < 0: m = tuple(-x for x in m); c0 = -c0
        assert c0.sign() > 0
        sg = {(kdot(m, p[e]) - c0).sign() for e in range(N)}
        if 1 in sg: continue
        key = frozenset(e for e in range(N) if (kdot(m, p[e]) - c0).sign() == 0)
        facets[key] = tuple(x / c0 for x in m)                            # facet {y : u.y = 1}
    log(f'  polar: {N} corners, {len(facets)} facets (exact); die corners {len(V)}: facets <-> corners {len(facets) == len(V)}')
    assert len(facets) == len(V)
    allok = True; res = []
    for k in range(N):
        Fk = [v for v in range(len(V)) if k in inc[v]]
        nk = [u for key, u in facets.items() if k in key]                 # outer normals of the polar at its corner p_k
        same = len(nk) == len(Fk) and all(any(all(x.sign() == 0 for x in ksub(u, V[v])) for v in Fk) for u in nk)
        # u is the facet normal scaled to u.y = 1, the die corner v has p_j.v = 1 on its faces: same vector, exactly
        o = cyclic([V[v] for v in Fk]); Pk = [V[Fk[i]] for i in o]
        Om, angs = sph_area_exact(Pk)
        oc = cyclic(nk); Nk = [nk[i] for i in oc]
        Ka, _ = sph_area_exact(Nk)
        Omn = mp_solid_angle([[mpk(x) for x in P] for P in Pk])
        ok = same and sp.simplify(Om - 4 * sp.pi / N) == 0 and sp.simplify(Ka - 4 * sp.pi / N) == 0 and abs(Omn - mp.pi / 2) < mp.mpf('1e-65')
        allok &= ok; res.append((k, len(Fk), str(Om), str(Ka), [str(a) for a in angs], ok))
        log(f'  face {k}: {len(Fk)} corners, solid angle {Om} (angles {", ".join(str(a) for a in angs)}), curvature at n_k/d_k {Ka},'
            f' same cone exactly: {same}, 70-digit check {mp.nstr(Omn - mp.pi / 2, 3)} -> {ok}')
    assert allok
    # scene: face 0
    k = 4; Vf = np.array([[float(x) for x in v] for v in V]); pf = np.array([[float(x) for x in v] for v in p])
    nf = np.array([[float(x) for x in v] for v in q]); nf /= np.linalg.norm(nf, axis=1)[:, None]
    Vd, faces, edges, _ = die_poly(nf, np.array([1 / np.linalg.norm([float(x) for x in v]) for v in q]))
    assert np.abs(np.sort(Vd, 0) - np.sort(Vf, 0)).max() < 1e-12
    Vf = Vd; Fk = faces[k]
    tris, cols = [], []
    for f, F in enumerate(faces):
        if f == k: continue
        for a in range(1, len(F) - 1): tris.append([F[0], F[a], F[a + 1]]); cols.append(PEARL)
    die = part(Vf, tris, cols, 0.30, edges, 0.004)
    cone_t, cone_c, rods = [], [], []
    for a in range(len(Fk)):
        A_, B_ = Vf[Fk[a]], Vf[Fk[(a + 1) % len(Fk)]]
        cone_t.append([np.zeros(3), A_, B_]); cone_c.append(TEAL); rods += rod(np.zeros(3), A_, 0.008) + rod(A_, B_, 0.008)
    c = Vf[Fk].mean(0)
    for a in range(len(Fk)): cone_t.append([c, Vf[Fk[a]], Vf[Fk[(a + 1) % len(Fk)]]]); cone_c.append(shade(TEAL, 0.35))
    S1 = [die, soup(cone_t, cone_c), soup(rods, [INK] * len(rods)), soup(ball((0, 0, 0), 0.035), [INK] * 320)]
    # the polar: facets as polygons, see-through; the normal cone at p_k = p_k + the same cone
    pe = set()
    for key, u in facets.items():
        S = sorted(key); uf = np.array([float(x) for x in u]); cc_ = pf[S].mean(0); e1 = pf[S[0]] - cc_; e2 = np.cross(uf, e1)
        S = sorted(S, key=lambda v: np.arctan2((pf[v] - cc_) @ e2, (pf[v] - cc_) @ e1))
        for a in range(len(S)): pe.add(tuple(sorted((S[a], S[(a + 1) % len(S)]))))
    ptri, pcol = [], []
    for key, u in facets.items():
        S = sorted(key); uf = np.array([float(x) for x in u]); cc_ = pf[S].mean(0); e1 = pf[S[0]] - cc_; e2 = np.cross(uf, e1)
        S = sorted(S, key=lambda v: np.arctan2((pf[v] - cc_) @ e2, (pf[v] - cc_) @ e1))
        for a in range(1, len(S) - 1): ptri.append([S[0], S[a], S[a + 1]]); pcol.append(shade(SLATE, 0.35))
    pol = part(pf, ptri, pcol, 0.30, sorted(pe), 0.004)
    nt, nc, nr = [], [], []
    for a in range(len(Fk)):
        A_, B_ = pf[k] + Vf[Fk[a]], pf[k] + Vf[Fk[(a + 1) % len(Fk)]]
        nt.append([pf[k], A_, B_]); nc.append(TEAL); nr += rod(pf[k], A_, 0.008) + rod(A_, B_, 0.008)
    c2 = pf[k] + c
    for a in range(len(Fk)): nt.append([c2, pf[k] + Vf[Fk[a]], pf[k] + Vf[Fk[(a + 1) % len(Fk)]]]); nc.append(shade(TEAL, 0.35))
    S2 = [pol, soup(nt, nc), soup(nr, [INK] * len(nr)), soup(ball(pf[k], 0.05), [TEAL] * 320), soup(ball((0, 0, 0), 0.035), [INK] * 320)]
    ax = c / np.linalg.norm(c); up = np.array([0, 1.0, 0]); side = np.cross(ax, up); side /= np.linalg.norm(side)
    dv = list(side + 0.12 * ax + 0.30 * up)
    E = max(extent(S1, dv), extent(S2, dv))
    R3.write(os.path.join(REN, 'fig2.html'), [{'E': E, 'dir': dv, 'parts': S1}, {'E': E, 'dir': dv, 'parts': S2}])
    return dict(N=N, corners=len(V), facets=len(facets), face=k, face_corners=len(Fk), Omega=res[k][2], angles=res[k][4])

# =====================================================================================================================
# Figure 3: Alexandrov's condition on the 14 face directions of Aequus CO-14 (C6 + O8), kappa_i = 4 pi/14
def fig3():
    dirs = [EX[i] for i in range(14)]; N = 14; kap = 4 * sp.pi / N
    sets = [('three cube directions', [i for i in range(14) if DFAM[i] == 'C6' and sum(float(x) for x in dirs[i]) > 0]),
            ('the seven directions about (1, 1, 1)', [i for i in range(14) if sum(float(x) for x in dirs[i]) > 0])]
    scenes, meta = [], []
    for title, I in sets:
        # complement of the region: C = {x : n_i.x <= 0 for i in I}; its corners are the cross products of pairs, exactly
        cand = []
        for i, j in itertools.combinations(I, 2):
            w = kcross(dirs[i], dirs[j])
            for s in (1, -1):
                ws = tuple(s * x for x in w)
                if all(x.sign() == 0 for x in ws): continue
                if all(kdot(dirs[m], ws).sign() <= 0 for m in I):
                    wf = np.array([float(x) for x in ws]); wf /= np.linalg.norm(wf)
                    if not any(np.abs(wf - np.array([float(x) for x in c]) / np.linalg.norm([float(x) for x in c])).max() < 1e-12 for c in cand): cand.append(ws)
        o = cyclic(cand); Cp = [cand[i] for i in o]
        aC, angs = sph_area_exact(Cp); area = sp.simplify(4 * sp.pi - aC); sk = sp.simplify(len(I) * kap)
        okn = abs(float(area) - (4 * np.pi - mc_area(dirs, I))) < 5e-3
        holds = bool(sp.N(area - sk, 50) > 0)
        log(f'Figure 3, I = {title} ({len(I)}): complement = spherical {len(Cp)}-gon, area {aC} (angles {", ".join(map(str, angs))});'
            f' region within pi/2 of I: area {area} = {sp.N(area, 20)}; sum of kappa over I = {sk} = {sp.N(sk, 20)}; condition holds: {holds};'
            f' sampling check {okn}')
        assert okn and holds
        # sphere: icosphere cut exactly along the great circles n_i.x = 0 (i in I), each piece in or out of the region
        T = icosphere(5); tris, cols = [], []
        nI = [np.array([float(x) for x in dirs[i]]) for i in I]; nI = [v / np.linalg.norm(v) for v in nI]
        for t in T:
            polys = [list(t)]
            for nv in nI:
                nxt = []
                for P in polys:
                    s = [nv @ x for x in P]
                    if min(s) < -1e-12 and max(s) > 1e-12:
                        a, b = clip(P, nv); nxt += [x for x in (a, b) if len(x) >= 3]
                    else: nxt.append(P)
                polys = nxt
            for P in polys:
                P = [x / np.linalg.norm(x) for x in P]; c = sum(P) / len(P)
                inside = any(nv @ c > 0 for nv in nI)
                for a in range(1, len(P) - 1): tris.append([P[0], P[a], P[a + 1]]); cols.append(SLATE if inside else PEARL)
        rods = []
        Cf = [np.array([float(x) for x in c]) for c in Cp]
        for a in range(len(Cf)):
            P = arc(Cf[a], Cf[(a + 1) % len(Cf)], 1.003, 60)
            for p, q in zip(P[:-1], P[1:]): rods += rod(p, q, 0.007, 6)
        balls = []
        for i in range(14):
            v = np.array([float(x) for x in dirs[i]]); v /= np.linalg.norm(v)
            balls.append((soup(ball(v * 1.0, 0.055 if i in I else 0.035), [TEAL if i in I else INK] * 320)))
        parts = [soup(tris, cols), soup(rods, [INK] * len(rods))] + balls
        for dv in ([0.75, 0.55, 1.0], [-0.75, -0.55, -1.0]):
            scenes.append({'E': 1.12, 'dir': dv, 'parts': parts})
        meta.append(dict(title=title, n=len(I), cgon=len(Cp), comp=str(aC), area=str(area), area_f=float(area), sk=str(sk), sk_f=float(sk)))
    R3.write(os.path.join(REN, 'fig3.html'), scenes); return meta

def mc_area(dirs, I, M=400000):
    """independent check of the complement's area by a fixed quasi-random sample (Fibonacci sphere)."""
    k = np.arange(M) + 0.5; z = 1 - 2 * k / M; r = np.sqrt(1 - z * z); th = np.pi * (3 - 5 ** .5) * k
    X = np.c_[r * np.cos(th), r * np.sin(th), z]; nI = np.array([[float(x) for x in dirs[i]] for i in I])
    return 4 * np.pi * np.mean((X @ nI.T <= 0).all(1))

# =====================================================================================================================
if __name__ == '__main__':
    os.makedirs(REN, exist_ok=True)
    if sys.argv[1] == 'scenes':
        meta = {'fig2': fig2()}
        if not PILOT: meta['fig3'] = fig3()
        meta['fig1'] = fig1()
        json.dump(meta, open(os.path.join(REN, 'meta.json'), 'w'), indent=1)
        LOG.append('FINAL ok'); open(os.path.join(HERE, 'fig_checks.log'), 'w').write('\n'.join(LOG) + '\n'); print('FINAL ok')
    else:   # compose
        import types
        from PIL import Image
        src = open(os.path.join(ST, '2026-11-21-scutoid-stand-in/renders/scripts/compose.py')).read()
        Cp = types.ModuleType('compose_defs'); Cp.__dict__['__file__'] = os.path.join(REN, 'x')
        exec(src[:src.index('s = lambda')], Cp.__dict__)          # the house compose functions only, not its own figures
        Cp.OUT = REN; Cp.MARK = 'DICTO · dictospheres.com'
        meta = json.load(open(os.path.join(REN, 'meta.json'))); sh_ = lambda f, i: os.path.join(REN, 'shots', f, f'p{i}.png')
        made = []
        def done(png, jpg, prev):
            im = Image.open(os.path.join(REN, png)).convert('RGB'); im.save(os.path.join(FIG, jpg), quality=90, optimize=True)
            w = 2000; im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(os.path.join(REN, prev), optimize=True); made.append(jpg)
        # Figure 2
        m = meta['fig2']; assert m['Omega'] == 'pi/2', m
        Cp.figure('fig2.png', 'The polar identity (Lemma 3): one cone, seen twice',
                  f"A fair die from #112's data set: the rhombic dodecahedron's planes with 4 of the 12 left out · {m['N']} faces, {m['corners']} corners ·"
                  f" exact: every face is seen from the centre under π/2 = 4π/{m['N']}",
                  [(sh_('fig2', 0), 'the die', 'the cone from the centre through one face'),
                   (sh_('fig2', 1), 'its polar (corners at the points n/d)', 'the cone of outer normals at the matching corner')],
                  [(PEARL, 'die faces'), (shade(SLATE, 0.35), 'polar faces'), (TEAL, 'the cone: solid angle π/2 = curvature π/2')], cell=760)
        done('fig2.png', 'fig2-polar.jpg', 'PREVIEW-fairdice-fig2-polar.png')
        if not PILOT:
            m3 = meta['fig3']
            assert m3[0]['area'] == '7*pi/2' and m3[0]['sk'] == '6*pi/7' and m3[0]['comp'] == 'pi/2', m3[0]
            assert m3[1]['area'] == '-3*acos(1/3) + 5*pi' and m3[1]['sk'] == '2*pi' and m3[1]['comp'] == '-pi + 3*acos(1/3)', m3[1]
            Cp.figure('fig3.png', "Alexandrov's condition on the 14 face directions of Aequus CO-14, Oh 1",
                      'Each direction carries κ = 4π/14 · highlighted: a set I · shaded: the directions within π/2 of some direction in I ·'
                      ' the condition asks that its area exceed the sum of κ over I · areas exact',
                      [[(sh_('fig3', 0), 'I = 3 cube directions', f"shaded area 7π/2 ≈ {m3[0]['area_f']:.4f} > Σκ = 6π/7 ≈ {m3[0]['sk_f']:.4f}"),
                        (sh_('fig3', 1), 'the same, from the far side', 'unshaded: one octant, area π/2')],
                       [(sh_('fig3', 2), 'I = the 7 directions about (1, 1, 1)', f"shaded area 5π − 3 arccos(1/3) ≈ {m3[1]['area_f']:.4f} > Σκ = 2π ≈ {m3[1]['sk_f']:.4f}"),
                        (sh_('fig3', 3), 'the same, from the far side', 'unshaded: a spherical triangle, area 3 arccos(1/3) − π')]],
                      [(TEAL, 'directions in I'), (INK, 'the other directions'), (SLATE, 'within π/2 of I'), (PEARL, 'farther than π/2 from all of I')], cell=560)
            done('fig3.png', 'fig3-alexandrov.jpg', 'PREVIEW-fairdice-fig3-alexandrov.png')
        for i, d in enumerate(meta['fig1']):
            kt = ', '.join(t for _, t in d['kinds'])
            Cp.figure(f"fig1-{d['grp']}.png", f"{d['name']}: a fair die of symmetry {d['grp']}",
                      f"{kt} · every face is seen from the centre under 4π/{d['N']} · depths {' : '.join(d['depths'])}"
                      f" (#112, to 60 digits; checked here: each face within {d['err']} of 4π/{d['N']})",
                      [(sh_('fig1', 3 * i), 'whole', f"{d['N']} faces, {d['corners']} corners"),
                       (sh_('fig1', 3 * i + 1), 'see-through', "each face's shadow on a sphere about the centre"),
                       (sh_('fig1', 3 * i + 2), 'pulled apart', f"the {d['N']} pyramids on the faces, apex at the centre")],
                      [(tuple(c), t) for c, t in d['kinds']], cell=560)
            done(f"fig1-{d['grp']}.png", f"fig1-{d['grp']}.jpg", f"PREVIEW-fairdice-fig1-{d['grp']}.png")
        print('composed', made); print('FINAL ok')
