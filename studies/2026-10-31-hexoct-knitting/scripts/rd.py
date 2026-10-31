#!/usr/bin/env python3
"""The rhombic dodecahedron (RD) cushion: exact checks and the knitting pattern (DICTO's idea, 31 Oct 2026).

Cubic units: FCC sites = integer points (i, j, k) with i + j + k even, unit = half the cube edge, so the ball spacing
(nearest neighbour) is sqrt(2) units. Delaunay pieces of FCC: in every unit cube the four sites form a regular tetrahedron;
the four other corners are octahedron centres (an octahedron = centre o and its six neighbours o +- e_i).
RD of scale m = Voronoi cell of the FCC of spacing m (centre at the origin): faces N.x = m for the 12 N = (+-1, +-1, 0)
(permuted); 4-valent corners m*e_i, 3-valent corners (m/2)(+-1, +-1, +-1).
Writes ../rd/*.png, ../rd/rd.json; prints every check.
Usage (dicto-big-brother): ~/geom/bin/python rd.py
"""
import os, json, math, itertools
from fractions import Fraction as F
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '../rd'); os.makedirs(OUT, exist_ok=True)
LOGO = os.path.expanduser(os.environ.get('LOGO', '~/kres-tmp/dicto-logo.png'))
GOLD_D, GOLD_L, EDGE = '#d9a521', '#f1d98a', '#1d1d24'
NN = math.sqrt(2)                       # ball spacing in cubic units
H = math.sqrt(2 / 3) * NN               # layer spacing
W_ST = math.sqrt(3) * NN / 12           # stitch width (repeat sqrt(3) ball spacings = 12 stitches)
R_ST = H / 7                            # row height (7 rows per layer)
REPORT = {}


def dot(a, b): return sum(x * y for x, y in zip(a, b))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def add(a, b): return tuple(x + y for x, y in zip(a, b))
def mul(a, s): return tuple(x * s for x in a)
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


# ---------- (a) the slice plane is a {110} plane
def check_a():
    st = (1, 1, 1)                       # stacking direction (close-packed layers are (111))
    row = (1, -1, 0)                     # a close-packed row in the (111) layer
    assert dot(st, row) == 0
    # slice plane: perpendicular to the row, i.e. normal = row = <110>: a {110} plane; it contains st
    lines = ['slice plane normal = close-packed row direction [1-10], a <110> direction: the plane is (1-10), a {110} plane',
             f'it contains the stacking direction [111]: [111].[1-10] = {dot(st, row)}',
             'in-plane horizontal direction = [1-10] x [111] ~ [-1-12] (the {11-20}/[1-100] frame of the hexagonal setting)']
    # which <111> lie in (1-10)?
    ins = [d for d in itertools.product((1, -1), repeat=3) if dot(d, row) == 0 and d[0] > 0 or (dot(d, row) == 0 and d[0] < 0 and False)]
    ins = sorted({tuple(d) if d[0] > 0 else tuple(-x for x in d) for d in itertools.product((1, -1), repeat=3) if dot(d, row) == 0})
    lines.append(f'<111> directions in (1-10): {ins}; angle between them arccos(1/3) = {math.degrees(math.acos(1/3)):.2f} deg')
    REPORT['a'] = lines
    return lines


# ---------- RD faces
def faces(m):
    out = []
    for k in range(3):
        i, j = [x for x in range(3) if x != k]
        for si in (1, -1):
            for sj in (1, -1):
                N = [0, 0, 0]; N[i] = si; N[j] = sj; N = tuple(N)
                vi = [0, 0, 0]; vi[i] = si * m; vj = [0, 0, 0]; vj[j] = sj * m
                tp = [F(0)] * 3; tp[i] = F(si * m, 2); tp[j] = F(sj * m, 2); tp[k] = F(m, 2)
                tm = list(tp); tm[k] = F(-m, 2)
                out.append(dict(N=N, V=[tuple(map(F, vi)), tuple(tp), tuple(map(F, vj)), tuple(tm)]))
    return out


ROT = [np.array(p) * np.array(s)[:, None] for p in
       [np.eye(3, dtype=int)[list(q)] for q in itertools.permutations(range(3))]
       for s in itertools.product((1, -1), repeat=3)]
ROT = [R for R in ROT if round(np.linalg.det(R)) == 1]
assert len(ROT) == 24


# ---------- pieces and point classification
def classify(p):
    """('tet', cell) or ('oct', centre) for a point p (floats or Fractions) of space; None on a boundary."""
    c = tuple(math.floor(x) for x in p)
    t = tuple(x - y for x, y in zip(p, c))
    even = sum(c) % 2 == 0
    if even:
        f = [2 - (t[0] + t[1] + t[2]), t[0] + t[1] - t[2], t[0] - t[1] + t[2], -t[0] + t[1] + t[2]]
        corners = [(1, 1, 1), (0, 0, 1), (0, 1, 0), (1, 0, 0)]
    else:
        f = [t[0] + t[1] + t[2] - 1, 1 - (t[0] + t[1] - t[2]), 1 - (t[0] - t[1] + t[2]), 1 - (-t[0] + t[1] + t[2])]
        corners = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
    if min(f) > 0: return ('tet', c)
    neg = [i for i in range(4) if f[i] < 0]
    if len(neg) == 1 and all(f[i] > 0 for i in range(4) if i != neg[0]):
        return ('oct', add(c, corners[neg[0]]))
    return None


def pieces_near(m):
    R = m + 2
    rng = range(-R, R + 1)
    for c in itertools.product(rng, repeat=3):
        if sum(c) % 2 == 0:
            V = [add(c, d) for d in ((0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1))]
        else:
            V = [add(c, d) for d in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1))]
        yield 'tet', c, V
        if sum(c) % 2 == 1:
            yield 'oct', c, [add(c, d) for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]


def plane_section(V, N, m):
    pts = []
    for p, q in itertools.combinations(V, 2):
        a, b = dot(N, p) - m, dot(N, q) - m
        if a == 0: pts.append(tuple(map(F, p)))
        if b == 0: pts.append(tuple(map(F, q)))
        if (a < 0 < b) or (b < 0 < a):
            t = F(a, a - b)
            pts.append(tuple(F(x) + t * (y - x) for x, y in zip(p, q)))
    return list(set(pts))


def to2(P, b1, b2):
    return [(dot(p, b1), dot(p, b2)) for p in P]


def hull2(pts):
    pts = sorted(set(pts))
    if len(pts) < 3: return pts
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def area2(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2


def clip(poly, a, b, c):
    """keep a*x + b*y <= c"""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0: out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    out = hull2(out)
    return out if len(out) >= 3 and area2(out) != 0 else None


def face_sections(face, m):
    """Exact section polygons of the pieces with the face rhombus, in integer face coordinates (b1, b2)."""
    N = face['N']; V4 = face['V']
    b1 = tuple(int(x) for x in sub(V4[0], V4[2]))                 # long diagonal (integer)
    b2 = cross(N, b1)
    R2 = to2(V4, b1, b2)
    cen = (sum(p[0] for p in R2) / 4, sum(p[1] for p in R2) / 4)
    edges = []
    for i in range(4):
        p, q = R2[i], R2[(i + 1) % 4]
        a, b = q[1] - p[1], -(q[0] - p[0]); c = a * p[0] + b * p[1]
        if a * cen[0] + b * cen[1] > c: a, b, c = -a, -b, -c
        edges.append((a, b, c))
    res = []
    for kind, key, V in pieces_near(m):
        if not any(dot(N, v) > m for v in V) or not any(dot(N, v) < m for v in V): continue
        S = plane_section(V, N, m)
        if len(S) < 3: continue
        P = hull2(to2(S, b1, b2))
        if len(P) < 3 or area2(P) == 0: continue
        for e in edges:
            P = clip(P, *e)
            if P is None: break
        if P is None: continue
        res.append(dict(kind=kind, key=key, poly=P))
    tot = sum(area2(r['poly']) for r in res)
    assert tot == abs(area2(R2)), (tot, area2(R2))
    return res, R2, b1, b2


# ---------- the face frame for knitting: up = a <111> edge direction, right = up x N (seen from outside)
def frame(face, up):
    N = np.array(face['N'], float); N /= np.linalg.norm(N)
    u = np.array(up, float); u /= np.linalg.norm(u)
    r = np.cross(u, N)
    return u, r


def check_b_c(m):
    lines = []
    fs = faces(m)
    # (b) every face plane N.x = m is a {110} lattice plane through ball centres
    for f in fs:
        N = f['N']
        assert all(dot(N, v) == m for v in f['V'])
    lines.append(f'all 12 RD faces lie in planes N.x = m with N a <110> direction: {{110}} planes; the plane N.x = m '
                 f'contains FCC sites (e.g. m e_i) for every integer m, so it is a lattice plane like the knitted slice')
    # corners are ball centres when m = 4n
    ok = all(sum(int(x) for x in v) % 2 == 0 and all(x.denominator == 1 for x in v) for f in fs for v in f['V'])
    lines.append(f'm = {m}: all rhombus corners are ball centres: {ok}')
    # edges along <111>
    f0 = fs[0]
    e = [sub(f0['V'][(i + 1) % 4], f0['V'][i]) for i in range(4)]
    lines.append('edge vectors of one face: ' + ', '.join(str(tuple(int(2 * x) / 2 for x in v)) for v in e) + ' : all along <111>')
    # sections: shapes, symmetry
    secs, R2, b1, b2 = face_sections(f0, m)
    kinds = {}
    for s in secs: kinds[s['kind']] = kinds.get(s['kind'], 0) + 1
    lines.append(f'face sections (m={m}): {kinds}; covered area = rhombus area exactly')
    # symmetry under the face's two in-plane mirrors (z -> -z type and the swap), for face N=(1,1,0)-type
    N = f0['N']
    k = [i for i in range(3) if N[i] == 0][0]
    i, j = [x for x in range(3) if x != k]
    def M1(p):
        q = list(p); q[k] = -q[k]; return tuple(q)
    def M2(p):
        q = list(p); q[i], q[j] = N[i] * N[j] * p[j], N[i] * N[j] * p[i]; return tuple(q)
    def canon(s, M):
        return None
    # check the colour function is mirror symmetric on a fine rational grid of the face
    bad = 0; tot = 0
    for a in range(1, 4 * m * 6):
        for b in range(-4 * m * 6, 4 * m * 6):
            # point = V0 + (a/24m)*(V1-V0) + (b/24m)*(V3-V0)
            P0, P1, P3 = f0['V'][0], f0['V'][1], f0['V'][3]
            s, t = F(a, 24 * m), F(b, 24 * m)
            if not (0 < t < 1 and 0 < s < 1): continue
            p = tuple(P0[x] + s * (P1[x] - P0[x]) + t * (P3[x] - P0[x]) for x in range(3))
            c0 = classify(p); c1 = classify(M1(p)); c2 = classify(M2(p))
            if c0 is None or c1 is None or c2 is None: continue
            tot += 1
            if not (c0[0] == c1[0] == c2[0]): bad += 1
    lines.append(f'colour (tet/oct) symmetric under both diagonal mirrors of the face: {bad == 0} ({tot} exact sample points)')
    # (c) seams: along every edge, the piece on both faces next to the edge is the same 3D piece
    adj = 0; badseam = 0
    for f in fs:
        for g in fs:
            if f is g: continue
            sh = [v for v in f['V'] if v in g['V']]
            if len(sh) != 2: continue
            adj += 1
            p, q = sh
            cf = tuple(sum(v[x] for v in f['V']) / 4 for x in range(3))
            cg = tuple(sum(v[x] for v in g['V']) / 4 for x in range(3))
            for a in range(1, 60):
                t = F(a, 60)
                x = tuple(p[y] + t * (q[y] - p[y]) for y in range(3))
                eps = F(1, 10**7)
                xf = tuple(x[y] + eps * (cf[y] - x[y]) for y in range(3))
                xg = tuple(x[y] + eps * (cg[y] - x[y]) for y in range(3))
                kf, kg = classify(xf), classify(xg)
                if kf is None or kg is None or classify(x) is None: continue   # skip points on piece boundaries
                if kf != kg: badseam += 1
    lines.append(f'seams: {adj // 2} edges; points where the two faces next to a seam show different 3D pieces: {badseam}')
    return lines, secs, R2


def rotations_to(N0, N):
    return [R for R in ROT if tuple(R @ np.array(N0)) == tuple(N)]


def net_and_orientations(m=1):
    """Reference face F0 (a belt face for [111]) with up = [111]; every face gets up = R up0 for a rotation R (F0 -> F)."""
    fs = faces(4)
    N0 = (1, -1, 0); up0 = np.array((1, 1, 1))
    F0 = [f for f in fs if f['N'] == N0][0]
    ups = {}
    for f in fs:
        Rs = rotations_to(N0, f['N'])
        cand = [tuple(R @ up0) for R in Rs]
        # both rotations give +-same axis; pick the one pointing 'up' (positive [111] component), or the first
        cand.sort(key=lambda u: -(u[0] + u[1] + u[2]))
        ups[f['N']] = cand[0]
    return fs, ups


def face2d(face, up):
    u, r = frame(face, up)
    V = [np.array([float(x) for x in v]) for v in face['V']]
    c = sum(V) / 4
    return [(float(np.dot(v - c, r)), float(np.dot(v - c, u))) for v in V]


def unfold(fs, ups):
    """Net: spanning tree over shared edges, faces laid flat. Returns 2D polygons (in the face frame of each face) + arrows."""
    idx = {f['N']: i for i, f in enumerate(fs)}
    belt = [f for f in fs if sum(f['N']) == 0]
    # order belt around [111]
    ax = np.array((1, 1, 1)) / math.sqrt(3)
    ref = np.array((1, -1, 0)) / math.sqrt(2); ref2 = np.cross(ax, ref)
    belt.sort(key=lambda f: math.atan2(np.dot(f['N'], ref2), np.dot(f['N'], ref)))
    placed = {}
    def shared(f, g): return [v for v in f['V'] if v in g['V']]
    def place(f, g, Pg):
        """place face f next to placed face g (2D vertices Pg in g['V'] order) across their shared edge"""
        a, b = shared(f, g)
        A2, B2 = np.array(Pg[g['V'].index(a)]), np.array(Pg[g['V'].index(b)])
        Fv = [np.array([float(x) for x in v]) for v in f['V']]
        A3, B3 = Fv[f['V'].index(a)], Fv[f['V'].index(b)]
        e3 = (B3 - A3) / np.linalg.norm(B3 - A3)
        e2 = (B2 - A2) / np.linalg.norm(B2 - A2); n2 = np.array((-e2[1], e2[0]))
        gc = np.mean(Pg, axis=0)
        side = -np.sign(np.dot(gc - A2, n2))
        N = np.array(f['N'], float); N /= np.linalg.norm(N)
        w3 = np.cross(N, e3)
        fc = np.mean(Fv, axis=0)
        sgn = np.sign(np.dot(fc - A3, w3))
        P = []
        for v in Fv:
            d = v - A3
            P.append(tuple(A2 + np.dot(d, e3) * e2 + side * sgn * np.dot(d, w3) * n2))
        return P
    # first belt face in its own frame
    f0 = belt[0]
    placed[f0['N']] = face2d(f0, ups[f0['N']])
    for k in range(1, 6):
        placed[belt[k]['N']] = place(belt[k], belt[k - 1], placed[belt[k - 1]['N']])
    tops = [f for f in fs if sum(f['N']) == 2]; bots = [f for f in fs if sum(f['N']) == -2]
    for grp in (tops, bots):
        for f in grp:
            g = [b for b in belt if len(shared(f, b)) == 2]
            # attach to the first belt face (in belt order) that shares an edge and keeps the net free of overlap
            for b in sorted(g, key=lambda b: belt.index(b)):
                P = place(f, b, placed[b['N']])
                placed[f['N']] = P
                break
    return placed, belt


def lift(face, P2, b1, b2, m):
    A = np.array([b1, b2, face['N']], float)
    return [tuple(np.linalg.solve(A, np.array([float(x), float(y), float(m)]))) for x, y in P2]


def chart_face(n, ups, fs):
    """Raster chart of the reference face (N0 = (1,-1,0), up = [111]) for m = 4n."""
    m = 4 * n
    fs = faces(m)
    f0 = [f for f in fs if f['N'] == (1, -1, 0)][0]
    u, r = frame(f0, (1, 1, 1))
    V3 = [np.array([float(x) for x in v]) for v in f0['V']]
    co = [(float(np.dot(v, r)), float(np.dot(v, u))) for v in V3]
    # origin: lowest corner on the left vertical side
    xmin = min(c[0] for c in co)
    left = [i for i, c in enumerate(co) if abs(c[0] - xmin) < 1e-9]
    o = min(left, key=lambda i: co[i][1])
    O3 = V3[o]
    R2 = [((c[0] - co[o][0]) / W_ST, (c[1] - co[o][1]) / R_ST) for c in co]     # in stitches / rows
    ncol = int(round(max(p[0] for p in R2))); nrow = int(round(max(p[1] for p in R2)))
    def inside(x, y, tol=1e-7):
        sgn = None
        for i in range(4):
            p, q = R2[i], R2[(i + 1) % 4]
            c = (q[0] - p[0]) * (y - p[1]) - (q[1] - p[1]) * (x - p[0])
            if abs(c) < tol * 100: continue
            s_ = c > 0
            if sgn is None: sgn = s_
            elif s_ != sgn: return False
        return True
    def p3(x, y): return O3 + x * W_ST * r + y * R_ST * u
    sub = [-3 / 8, -1 / 8, 1 / 8, 3 / 8]
    grid = {}
    ties = 0
    for j in range(nrow + 1):
        for c in range(ncol + 1):
            if not inside(c, j): continue
            v = {}
            for a in sub:
                for b in sub:
                    k = classify(tuple(p3(c + a, j + b)))
                    if k is None: continue
                    v[k[0]] = v.get(k[0], 0) + 1
            if v.get('tet', 0) > v.get('oct', 0): col = 'D'
            elif v.get('oct', 0) > v.get('tet', 0): col = 'L'
            else: col = 'D'; ties += 1
            grid[(j, c)] = col
    # balls: FCC sites in the face plane
    balls = []
    for j in range(nrow + 1):
        for c in range(ncol + 1):
            if (j, c) not in grid: continue
            q = p3(c, j); qi = np.round(q)
            if np.allclose(q, qi, atol=1e-6) and int(qi.sum()) % 2 == 0:
                onedge = not inside(c, j, tol=-1) or any(abs(((R2[(i+1)%4][0]-R2[i][0])*(j-R2[i][1])-(R2[(i+1)%4][1]-R2[i][1])*(c-R2[i][0]))) < 1e-6 for i in range(4))
                balls.append((j, c, onedge))
    return dict(grid=grid, R2=R2, ncol=ncol, nrow=nrow, balls=balls, ties=ties, m=m)


def runs(seq):
    out = []
    for x in seq:
        if out and out[-1][1] == x: out[-1][0] += 1
        else: out.append([1, x])
    return out


def rows_table(ch):
    g = ch['grid']; rows = []
    prev = None
    for j in range(ch['nrow'] + 1):
        cols = sorted(c for (jj, c) in g if jj == j)
        if not cols: continue
        lo, hi = cols[0], cols[-1]
        assert cols == list(range(lo, hi + 1))
        rs = (len(rows) % 2 == 0)
        order = range(hi, lo - 1, -1) if rs else range(lo, hi + 1)
        rr = runs([g[(j, c)] for c in order])
        sh = ''
        if prev:
            dl, dr = prev[0] - lo, hi - prev[1]      # + = stitches added at left / right
            parts = []
            if dr: parts.append(f"{'add' if dr > 0 else 'remove'} {abs(dr)} at right")
            if dl: parts.append(f"{'add' if dl > 0 else 'remove'} {abs(dl)} at left")
            sh = ', '.join(parts)
        bob = [c - lo + 1 for (jj, c, e) in ch['balls'] if jj == j and not e]
        rows.append(dict(row=len(rows) + 1, side='RS' if rs else 'WS', first=lo, last=hi, sts=hi - lo + 1,
                         runs=[(k, 'DG' if x == 'D' else 'LG') for k, x in rr], shaping=sh, bobbles=bob))
        prev = (lo, hi)
    return rows


def draw_chart(ch, path, n):
    g = ch['grid']; stw, sth = 1.25, 1.0
    NR, NC = ch['nrow'] + 1, ch['ncol'] + 1
    fig = plt.figure(figsize=(7.0, 7.0 * (NR + 3) / (NC * stw + 8)), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1])
    for (j, c), col in g.items():
        ax.add_patch(Rectangle((c * stw, j * sth), stw, sth, fc=GOLD_D if col == 'D' else GOLD_L, ec='#3a3a3a', lw=0.3))
    for j, c, e in ch['balls']:
        if e: ax.plot((c + 0.5) * stw, (j + 0.5) * sth, 'o', ms=4.0, mfc='white', mec='#1d1d24', mew=0.8)
        else: ax.plot((c + 0.5) * stw, (j + 0.5) * sth, 'o', ms=5.5, mfc='#1d1d24', mec='white', mew=0.8)
    R2 = ch['R2']
    ax.add_patch(MPoly([((x + 0.5) * stw, (y + 0.5) * sth) for x, y in R2], closed=True, fill=False, ec='#b00020', lw=1.0))
    rr = sorted({j for (j, c) in g}); fs_ = max(3.5, 6.5 - 0.03 * NR)
    for k, j in enumerate(rr):
        if NR <= 60 or k % 2 == 0:
            ax.text(-0.4, (j + 0.5) * sth, str(k + 1), ha='right', va='center', fontsize=fs_)
            ax.text(NC * stw + 0.4, (j + 0.5) * sth, str(k + 1), ha='left', va='center', fontsize=fs_)
    for c in range(NC):
        if NC <= 20 or c % 2 == 0:
            ax.text((c + 0.5) * stw, -0.5, str(c + 1), ha='center', va='top', fontsize=fs_ * 0.85)
    ax.set_xlim(-3.5, NC * stw + 3.5); ax.set_ylim(-2, NR * sth + 0.5); ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(path); plt.close(fig)


def draw_face_exact(n, path):
    m = 4 * n
    fs = faces(m); f0 = [f for f in fs if f['N'] == (1, -1, 0)][0]
    secs, R2, b1, b2 = face_sections(f0, m)
    u, r = frame(f0, (1, 1, 1))
    fig = plt.figure(figsize=(3.2, 3.6), dpi=220); ax = fig.add_axes([0, 0, 1, 1])
    def to(P3): return [(float(np.dot(p, r)), float(np.dot(p, u))) for p in map(np.array, P3)]
    for s in secs:
        P3 = lift(f0, s['poly'], b1, b2, m)
        ax.add_patch(MPoly(to(P3), closed=True, fc=GOLD_D if s['kind'] == 'tet' else GOLD_L, ec=EDGE, lw=0.8))
    for v in itertools.product(range(-m, m + 1), repeat=3):
        if sum(v) % 2 == 0 and dot(f0['N'], v) == m:
            cnd = classify(tuple(F(x) for x in v))
            pts = to([v])[0]
            # inside the rhombus?
            V = to([tuple(float(x) for x in w) for w in f0['V']])
            from matplotlib.path import Path
            if Path(V).contains_point(pts, radius=1e-6) or Path(V).contains_point(pts, radius=-1e-6):
                ax.plot(*pts, 'o', ms=4, mfc='#1d1d24', mec='white', mew=0.6)
    V = to([tuple(float(x) for x in w) for w in f0['V']])
    ax.add_patch(MPoly(V, closed=True, fill=False, ec='#b00020', lw=1.3))
    xs = [p[0] for p in V]; ys = [p[1] for p in V]
    ax.set_xlim(min(xs) - 0.2, max(xs) + 0.2); ax.set_ylim(min(ys) - 0.2, max(ys) + 0.2); ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(path); plt.close(fig)


def draw_3d(n, ups, path, view=(0.5, -0.85, 0.15)):
    """Orthographic view of the cushion: only the faces turned to the viewer (a convex body), crisp edges."""
    m = 4 * n
    fs = faces(m)
    d = np.array(view, float); d /= np.linalg.norm(d)
    ex = np.cross((0, 0, 1), d); ex /= np.linalg.norm(ex); ey = np.cross(d, ex)
    P = lambda q: (float(np.dot(q, ex)), float(np.dot(q, ey)))
    fig = plt.figure(figsize=(4.4, 4.4), dpi=220); ax = fig.add_axes([0, 0, 1, 1])
    for f in fs:
        if np.dot(f['N'], d) <= 0: continue
        secs, R2, b1, b2 = face_sections(f, m)
        for s_ in secs:
            Q = lift(f, s_['poly'], b1, b2, m)
            ax.add_patch(MPoly([P(np.array(q)) for q in Q], closed=True, fc=GOLD_D if s_['kind'] == 'tet' else GOLD_L,
                               ec=EDGE, lw=0.5, joinstyle='miter'))
        ax.add_patch(MPoly([P(np.array([float(x) for x in v])) for v in f['V']], closed=True, fill=False, ec='#7a1010', lw=1.6))
    for v in itertools.product(range(-m, m + 1), repeat=3):
        if sum(v) % 2: continue
        vv = np.array(v, float)
        on = [f for f in fs if dot(f['N'], v) == m and np.dot(f['N'], d) > 0]
        if not on: continue
        if max(abs(dot(g['N'], v)) for g in fs) > m: continue
        ax.plot(*P(vv), 'o', ms=3.2, mfc='#1d1d24', mec='white', mew=0.5, zorder=5)
    ax.set_xlim(-1.45 * m, 1.45 * m); ax.set_ylim(-1.45 * m, 1.45 * m); ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(path); plt.close(fig)


def draw_net(path, n=1):
    m = 4 * n
    fs, ups = net_and_orientations()
    placed, belt = unfold(fs, ups)
    order = belt + [f for f in fs if sum(f['N']) == 2] + [f for f in fs if sum(f['N']) == -2]
    fig = plt.figure(figsize=(7.0, 5.0), dpi=220); ax = fig.add_axes([0, 0, 1, 1])
    fsm = faces(m)
    for num, f in enumerate(order, 1):
        P = np.array(placed[f['N']])
        V3 = np.array([[float(x) for x in v] for v in f['V']])
        # affine map 3D face -> 2D net from three corners
        A = np.c_[V3[:3] - V3[0]]
        M, *_ = np.linalg.lstsq(V3[1:3] - V3[0], P[1:3] - P[0], rcond=None)
        def T(q): return P[0] + (np.array(q) - V3[0]) @ M
        # pattern (m = 4n face scaled to the net's unit face)
        fm = [g for g in fsm if g['N'] == f['N']][0]
        secs, R2, b1, b2 = face_sections(fm, m)
        for s in secs:
            Q = np.array(lift(fm, s['poly'], b1, b2, m)) * (4 / m)
            ax.add_patch(MPoly([T(q) for q in Q], closed=True, fc=GOLD_D if s['kind'] == 'tet' else GOLD_L, ec=EDGE, lw=0.3))
        ax.add_patch(MPoly(P, closed=True, fill=False, ec='#7a1010', lw=1.2))
        c = P.mean(axis=0)
        up = np.array(ups[f['N']], float); up /= np.linalg.norm(up)
        d = (T(V3.mean(axis=0) + up * 1.6) - T(V3.mean(axis=0)))
        ax.annotate('', xy=c + d, xytext=c - d, arrowprops=dict(arrowstyle='-|>', color='#b00020', lw=1.4))
        ax.text(*(c + np.array((0.55, -0.1))), str(num), fontsize=8, weight='bold', color='#1d1d24')
    allp = np.vstack([np.array(p) for p in placed.values()])
    ax.set_xlim(allp[:, 0].min() - 0.5, allp[:, 0].max() + 0.5); ax.set_ylim(allp[:, 1].min() - 0.5, allp[:, 1].max() + 0.5)
    ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(path); plt.close(fig)
    return [(num, f['N'], ups[f['N']]) for num, f in enumerate(order, 1)]


def trd_check():
    """Voronoi cell of hcp (2H): faces and which lie in slice planes."""
    from scipy.spatial import Voronoi
    h = math.sqrt(2 / 3)
    P = []
    for L, z in (('A', 0), ('B', 1), ('A', 2), ('B', -1), ('A', -2)):
        for a in range(-3, 4):
            for b in range(-3, 4):
                x = a + b / 2 + (0.5 if L == 'B' else 0); y = b * math.sqrt(3) / 2 + (math.sqrt(3) / 6 if L == 'B' else 0)
                P.append((x, y, z * h))
    P = np.array(P); i0 = int(np.argmin(np.linalg.norm(P, axis=1)))
    vor = Voronoi(P)
    out = []
    for (p, q), rv in zip(vor.ridge_points, vor.ridge_vertices):
        if i0 not in (p, q) or -1 in rv: continue
        other = q if p == i0 else p
        nrm = P[other] - P[i0]
        V = vor.vertices[rv]
        # merge coplanar duplicates: count distinct vertices
        Vu = np.unique(np.round(V, 9), axis=0)
        c = Vu.mean(axis=0); nn = nrm / np.linalg.norm(nrm)
        e1 = Vu[0] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(nn, e1)
        ang = np.argsort([math.atan2(np.dot(v - c, e2), np.dot(v - c, e1)) for v in Vu]); Vo = Vu[ang]
        sides = [round(float(np.linalg.norm(Vo[(i + 1) % len(Vo)] - Vo[i])), 4) for i in range(len(Vo))]
        out.append(dict(normal=np.round(nrm, 4).tolist(), nvert=len(Vu), vertical=abs(nrm[2]) < 1e-9, sides=sides,
                        plane_offset=round(float(np.dot(c, nn)), 4)))
    return out


def main():
    a = check_a()
    for l in a: print('(a)', l)
    res = {}
    for n in (1, 2, 3):
        m = 4 * n
        lines, secs, R2 = check_b_c(m)
        for l in lines: print(f'(b,c) n={n}', l)
        res[n] = lines
    REPORT['bc'] = res
    fs, ups = net_and_orientations()
    tables = {}
    for n in (1, 2, 3):
        ch = chart_face(n, ups, fs)
        draw_chart(ch, os.path.join(OUT, f'chart-n{n}.png'), n)
        rows = rows_table(ch)
        cnt = {'DG': 0, 'LG': 0}
        for r in rows:
            for k, c in r['runs']: cnt[c] += k
        nb = sum(len(r['bobbles']) for r in rows)
        tables[n] = dict(m=ch['m'], ncol=ch['ncol'] + 1, nrows=len(rows), rows=rows, counts=cnt, bobbles=nb, ties=ch['ties'],
                         edge_balls=sum(1 for b in ch['balls'] if b[2]), R2=ch['R2'])
        print(f'n={n}: face chart {ch["ncol"] + 1} sts wide x {len(rows)} rows; per face DG {cnt["DG"]} LG {cnt["LG"]}, '
              f'bobbles {nb}, balls on edges {tables[n]["edge_balls"]}, ties {ch["ties"]}; corners (sts, rows) '
              + ' '.join(f'({x:.3f},{y:.3f})' for x, y in ch['R2']))
        draw_face_exact(n, os.path.join(OUT, f'face-exact-n{n}.png'))
    draw_3d(2, ups, os.path.join(OUT, 'rd-3d-n2.png'))
    draw_3d(1, ups, os.path.join(OUT, 'rd-3d-n1.png'))
    net = draw_net(os.path.join(OUT, 'net.png'))
    print('net order (face number, normal, knitting up):', net)
    trd = trd_check()
    kinds = {}
    for f in trd: kinds[(f['vertical'], f['nvert'])] = kinds.get((f['vertical'], f['nvert']), 0) + 1
    print('2H Voronoi cell faces (vertical?, corners): count', kinds)
    for f in trd: print('   ', 'vertical' if f['vertical'] else 'slanted ', 'sides', f['sides'], 'distance', f['plane_offset'])
    REPORT['trd'] = trd
    json.dump(dict(report=REPORT, tables=tables, net=net), open(os.path.join(OUT, 'rd.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
