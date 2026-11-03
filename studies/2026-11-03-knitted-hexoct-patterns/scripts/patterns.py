# Knitted HexOct: Patterns (DICTO's Knitted HexOct, spec of 2026-11-02). Builds every number, chart, table and figure of the
# pattern booklet from the spec's formulas, with exact checks, and writes paper.html, figs/*.svg and data/check.out.
# Run on dicto-big-brother with ~/geom/bin/python:  python patterns.py <out dir> <dir holding tiles.py, engine.py, stackings.py>
# (the #75 scripts of studies/2026-10-29-endless-stack-cell, as for the spec's check.py).
import itertools, math, os, sys
from fractions import Fraction as Fr
import sympy as sp

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else '.'))
FIGS, DATA = os.path.join(OUT, 'figs'), os.path.join(OUT, 'data')
os.makedirs(FIGS, exist_ok=True); os.makedirs(DATA, exist_ok=True)
LOG = []
def log(*a):
    s = ' '.join(str(x) for x in a); print(s); LOG.append(s)

# ---------------------------------------------------------------- spec §2(a): gauge rules and the sheet
N, M = 16, 14                      # node spacing a = N stitches; node rows M ridges apart (square garter gauge)
S_REF, R_REF, T_REF = 22, 22, 3.5  # reference gauge (sts and ridges per 10 cm) and sheet thickness (mm), spec §2-3
COLS, RIDGES = 4 * N, 3 * M
ROWS = 2 * RIDGES
def node_ridge(j): return (M + 1) // 2 + j * M
def node_row(j): return 2 * node_ridge(j) - 1          # the RS row of that ridge (row 1 = RS)
def node_st(i, j): return N // 2 + 1 + N * i + (N // 2) * j
assert all(node_st(i, j) == 9 + 16 * i + 8 * j for i in range(3) for j in range(3))      # spec: stitches 9 + 16i + 8j
assert [node_ridge(j) for j in range(3)] == [7, 21, 35] and [node_row(j) for j in range(3)] == [13, 41, 69]
assert M == round(0.866 * N * R_REF / S_REF) and N % 2 == 0
a_mm = 100 * N / S_REF                                   # 72.7 mm
d_mm = math.sqrt(2 / 3) * a_mm
ell_mm = lambda t: a_mm - 2 * t / (2 * math.sin(math.atan(math.sqrt(2))))   # spec: l = a - 1.22 t
assert abs(2 / (2 * math.sin(math.atan(math.sqrt(2)))) - 1.2247) < 1e-4
log(f"gauge: N={N}, M={M}, cast on {COLS}, {RIDGES} ridges = {ROWS} rows; node rows {[node_row(j) for j in range(3)]}, "
    f"node stitches {[[node_st(i, j) for i in range(3)] for j in range(3)]}")
log(f"reference sizes: a = {a_mm:.1f} mm, d = {d_mm:.1f} mm, l(t=3.5) = {ell_mm(3.5):.1f} mm")

# ---------------------------------------------------------------- spec §1: exact link geometry
POS = {'A': (Fr(0), Fr(0)), 'B': (Fr(1, 3), Fr(1, 3)), 'C': (Fr(2, 3), Fr(2, 3))}
def norm2(u, v): return u * u + u * v + v * v
def up_links(lo, hi):
    out = []
    for di, dj in itertools.product(range(-2, 3), repeat=2):
        u, v = POS[hi][0] + di - POS[lo][0], POS[hi][1] + dj - POS[lo][1]
        if norm2(u, v) == Fr(1, 3): out.append((di, dj, u, v))
    assert len(out) == 3; return out
FWD, BWD = {(0, 0), (-1, 0), (0, -1)}, {(0, 0), (1, 0), (0, 1)}
for lo, hi in [('A', 'B'), ('B', 'C')]:   # the steps used here (C -> A wraps the origin by a lattice vector)
    assert {(x[0], x[1]) for x in up_links(lo, hi)} == FWD
    assert {(x[0], x[1]) for x in up_links(hi, lo)} == BWD
d = sp.sqrt(sp.Rational(2, 3))
for lo, hi in [('A', 'B'), ('B', 'A')]:
    for _, _, u, v in up_links(lo, hi):
        h2 = sp.Rational(norm2(u, v).numerator, norm2(u, v).denominator)
        assert sp.simplify(h2 + d ** 2 - 1) == 0 and sp.simplify(sp.atan(d / sp.sqrt(h2)) - sp.atan(sp.sqrt(2))) == 0
TILT = math.degrees(math.atan(math.sqrt(2)))
log(f"links: length a, tilt atan(sqrt 2) = {TILT:.4f} deg, sheet spacing sqrt(2/3) a (exact)")
def st_r(u, v): return N * (u + v / 2), M * v               # plan offset in stitches and ridges (ideal gauge)
assert {st_r(u, v) for _, _, u, v in up_links('A', 'B')} == {(Fr(8), Fr(14, 3)), (Fr(-8), Fr(14, 3)), (Fr(0), Fr(-28, 3))}
# c / h at sheet B: links up vs links down (plan vectors)
down = {(-u, -v) for _, _, u, v in up_links('A', 'B')}       # B -> A, plan part (falling)
upc = {(u, v) for _, _, u, v in up_links('B', 'C')}
uph = {(u, v) for _, _, u, v in up_links('B', 'A')}
assert all((-u, -v) in down for u, v in upc)                 # c: each link up is the straight continuation of a link down
assert uph == down                                           # h: each link up is the mirror image (in the sheet) of a link down
log("c: 3/3 links up collinear with a link down; h: 3/3 links up mirror a link down")

def frac(x):
    x = Fr(x); s = '−' if x < 0 else '+'; x = abs(x); w, r = divmod(x.numerator, x.denominator)
    f = {Fr(1, 3): '⅓', Fr(2, 3): '⅔'}.get(Fr(r, x.denominator), '' if r == 0 else f'{r}/{x.denominator}')
    return s + (str(w) if w or not f else '') + f
def fr0(x): return '0' if x == 0 else frac(x)

# ---------------------------------------------------------------- spec §3: the two test pieces
PIECES = {'T-c': dict(word='ABC', names=['A', 'B', 'C'], kind='c'),
          'T-h': dict(word='ABA', names=['A', 'B', 'A′'], kind='h')}
EXPECT_DEG = {'ABC': [[[1, 2, 2], [2, 3, 3], [2, 3, 3]], [[4, 5, 4], [5, 6, 5], [4, 5, 4]], [[3, 3, 2], [3, 3, 2], [2, 2, 1]]],
              'ABA': [[[1, 2, 2], [2, 3, 3], [2, 3, 3]], [[6, 6, 4], [6, 6, 4], [4, 4, 2]], [[1, 2, 2], [2, 3, 3], [2, 3, 3]]]}
def lab(P, n): k, i, j = n; return f"{P['names'][k]}{1 + i + 3 * j}"
def lat(P, n): k, i, j = n; w = P['word'][k]; return (POS[w][0] + i, POS[w][1] + j, Fr(k))
def build(P):
    nodes = [(k, i, j) for k in range(3) for j in range(3) for i in range(3)]
    links = []
    for k in range(2):
        for j in range(3):
            for i in range(3):
                row = []
                for di, dj, u, v in up_links(P['word'][k], P['word'][k + 1]):
                    if 0 <= i + di < 3 and 0 <= j + dj < 3: row.append(((k, i, j), (k + 1, i + di, j + dj), u, v))
                links += sorted(row, key=lambda x: 1 + x[1][1] + 3 * x[1][2])
    deg = {n: 0 for n in nodes}
    for x in links: deg[x[0]] += 1; deg[x[1]] += 1
    assert len(nodes) == 27 and len(links) == 42 and sum(1 for x in links if x[0][0] == 0) == 21
    assert [[[deg[(k, i, j)] for i in range(3)] for j in range(3)] for k in range(3)] == EXPECT_DEG[P['word']]
    for x in links:                                           # every link: length a in the exact lattice
        p, q = lat(P, x[0]), lat(P, x[1])
        assert norm2(q[0] - p[0], q[1] - p[1]) == Fr(1, 3)
    return nodes, links, deg

def cells(P, links):
    L = {(x[0], x[1]) for x in links}
    def tris(k):
        out = []
        for i, j in itertools.product(range(2), repeat=2):
            out.append(((k, i, j), (k, i + 1, j), (k, i, j + 1)))
            out.append(((k, i + 1, j), (k, i, j + 1), (k, i + 1, j + 1)))
        return out
    C = []
    for g in range(2):
        lo = [(g, i, j) for i in range(3) for j in range(3)]; hi = [(g + 1, i, j) for i in range(3) for j in range(3)]
        for T in tris(g):
            for n in hi:
                if all((t, n) in L for t in T): C.append(dict(kind='tet', gap=g, base=g, nodes=list(T) + [n]))
        for T in tris(g + 1):
            for n in lo:
                if all((n, t) in L for t in T): C.append(dict(kind='tet', gap=g, base=g + 1, nodes=list(T) + [n]))
        for T1 in tris(g):
            for T2 in tris(g + 1):
                ls = [(p, q) for p in T1 for q in T2 if (p, q) in L]
                if len(ls) == 6: C.append(dict(kind='oct', gap=g, lo=list(T1), hi=list(T2), links=ls))
    return C

import tiles   # #75 tiles (exact rationals)
TILE_WORD = {'T-c': 'ABC', 'T-h': 'AB'}
def tile_check(name, P, C):
    pieces, _ = tiles.tile(TILE_WORD[name], 1, Fr(-1, 8))
    assert sorted(p[0] for p in pieces) == ['oct', 'oct', 'tet', 'tet']
    found = []
    for i0, j0 in itertools.product(range(3), repeat=2):
        o = lat(P, (1, i0, j0))
        def rel(n): p = lat(P, n); return (p[0] - o[0], p[1] - o[1], p[2] - o[2])
        hit = []
        for k, up, s, Pts, J in pieces:
            S = set(Pts); m = None
            for ci, c in enumerate(C):
                if k == 'tet' and c['kind'] == 'tet' and len(S) == 4 and S == {rel(n) for n in c['nodes']}: m = ci
                if k == 'oct' and c['kind'] == 'oct':
                    tri = c['hi'] if c['gap'] == 0 else c['lo']           # the B triangle of this octahedron
                    if (c['gap'] == 0) != bool(up): continue                # up=True: top half of the gap below B
                    mids = set()
                    for p, q in c['links']:
                        a_, b_ = rel(p), rel(q); mids.add(tuple((a_[r] + b_[r]) / 2 for r in range(3)))
                    if S == {rel(n) for n in tri} | mids and len(S) == 9: m = ci
            hit.append(m)
        if all(h is not None for h in hit): found.append(((i0, j0), hit))
    assert found, name
    return found

def owner(c):   # which sheet's tile a cell (or half) belongs to
    if c['kind'] == 'tet': return [c['base']]
    return [c['gap'], c['gap'] + 1]    # lower half -> lower sheet, upper half -> upper sheet

R = {}
for name, P in PIECES.items():
    nodes, links, deg = build(P); C = cells(P, links)
    cnt = {g: dict(tet_lo=sum(1 for c in C if c['kind'] == 'tet' and c['gap'] == g and c['base'] == g),
                   tet_hi=sum(1 for c in C if c['kind'] == 'tet' and c['gap'] == g and c['base'] == g + 1),
                   oct=sum(1 for c in C if c['kind'] == 'oct' and c['gap'] == g)) for g in range(2)}
    found = tile_check(name, P, C)
    full = [lab(P, (1, i, j)) for (i, j), _ in found]
    R[name] = dict(P=P, nodes=nodes, links=links, deg=deg, C=C, cnt=cnt, full=full)
    log(f"{name} ({P['word']}): nodes 27, links 42 (21 + 21), degrees as spec check.out; cells gap 1 {cnt[0]}, gap 2 {cnt[1]}; "
        f"#75 tile of the middle sheet at lambda=-1/8 found complete as cells around {full}")

# ---------------------------------------------------------------- figures (SVG, line drawings)
GOLD, VIOL_UP, VIOL_DN, TEAL = '#d9a521', '#8a5cc2', '#b48ae0', '#2bb3a3'
def svg(w, h, body, wmm=None):
    size = f'width="{wmm}mm" height="{wmm * h / w:.2f}mm"' if wmm else f'width="{w}" height="{h}"'
    return f'<svg xmlns="http://www.w3.org/2000/svg" {size} viewBox="0 0 {w} {h}" font-family="DejaVu Sans, sans-serif">{body}</svg>'
def line(x1, y1, x2, y2, w=1.0, c='#000', dash=None, op=1):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"'
            + (f' stroke-dasharray="{dash}"' if dash else '') + (f' stroke-opacity="{op}"' if op < 1 else '') + '/>')
def text(x, y, s, size=10, anchor='middle', weight='normal', c='#000', italic=False):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{c}"'
            + (' font-style="italic"' if italic else '') + f'>{s}</text>')
def circ(x, y, r, fill='#000', stroke='none', w=1):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'
def poly(pts, fill='none', stroke='#000', w=0.8, fop=1, dash=None):
    return (f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="{fill}" fill-opacity="{fop}" stroke="{stroke}" '
            f'stroke-width="{w}" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
def save(name, s): open(os.path.join(FIGS, name), 'w').write(s)

# --- stitch charts: one square = 1 stitch x 1 ridge (2 rows); stitch 1 at the right (RS view, cast-on edge at the bottom)
GHOST = {0: 'circle', 1: 'diamond', 2: 'square'}
def chart(name, k):
    P = R[name]['P']; s = 10; X0, Y0 = 46, 34; W = X0 + COLS * s + 70; H = Y0 + RIDGES * s + 46
    X = lambda st: X0 + (COLS - st) * s + s / 2         # centre of stitch column st (continuous)
    Y = lambda rg: Y0 + (RIDGES - rg) * s + s / 2       # centre of ridge rg (continuous)
    b = [f'<rect x="{X0}" y="{Y0}" width="{COLS * s}" height="{RIDGES * s}" fill="#fff" stroke="#000" stroke-width="1.2"/>']
    for c in range(1, COLS):
        b.append(line(X0 + c * s, Y0, X0 + c * s, Y0 + RIDGES * s, 1.0 if c % 8 == 0 else 0.35, '#000' if c % 8 == 0 else '#999'))
    for r in range(1, RIDGES):
        b.append(line(X0, Y0 + r * s, X0 + COLS * s, Y0 + r * s, 1.0 if r % 7 == 0 else 0.35, '#000' if r % 7 == 0 else '#999'))
    for st in [1] + list(range(8, COLS + 1, 8)):
        b.append(text(X(st), Y0 + RIDGES * s + 13, str(st), 8.5)); b.append(text(X(st), Y0 - 5, str(st), 8.5))
    for rg in [1] + list(range(7, RIDGES + 1, 7)):
        b.append(text(X0 - 5, Y(rg) + 3, str(rg), 8.5, 'end'))
    b.append(text(X0 - 26, Y0 + RIDGES * s / 2, 'ridge', 9, 'middle'))
    b.append(text(X0 + COLS * s / 2, Y0 + RIDGES * s + 27, 'stitch (counted from the start of the RS row, stitch 1 at the right) · cast-on edge at the bottom', 9))
    for j in range(3):
        b.append(line(X0 + COLS * s + 2, Y(node_ridge(j)), X0 + COLS * s + 8, Y(node_ridge(j)), 1))
        b.append(text(X0 + COLS * s + 10, Y(node_ridge(j)) + 3.5, f'row {node_row(j)} (RS)', 8.5, 'start', 'bold'))
    # other sheets' nodes in their final places, exactly (ideal gauge): ghosts
    o = lat(P, (k, 0, 0))
    for k2 in range(3):
        if k2 == k: continue
        for i, j in itertools.product(range(3), repeat=2):
            p = lat(P, (k2, i, j)); du, dv = p[0] - o[0], p[1] - o[1]; ds, dr = st_r(du, dv)
            st, rg = node_st(0, 0) + ds, node_ridge(0) + dr
            if not (0.5 <= st <= COLS + 0.5 and 0.5 <= rg <= RIDGES + 0.5): continue
            x, y = X(float(st)), Y(float(rg)); r_ = 3.4
            if GHOST[k2] == 'circle': b.append(circ(x, y, r_, 'none', '#555', 1.1))
            elif GHOST[k2] == 'diamond': b.append(poly([(x, y - 4.4), (x + 4.4, y), (x, y + 4.4), (x - 4.4, y)], 'none', '#555', 1.1))
            else: b.append(poly([(x - 3.3, y - 3.3), (x + 3.3, y - 3.3), (x + 3.3, y + 3.3), (x - 3.3, y + 3.3)], 'none', '#555', 1.1))
            b.append(text(x + 5, y - 4, lab(P, (k2, i, j)), 6.5, 'start', c='#555'))
    for i, j in itertools.product(range(3), repeat=2):
        st, rg = node_st(i, j), node_ridge(j)
        b.append(f'<rect x="{X(st) - s / 2:.1f}" y="{Y(rg) - s / 2:.1f}" width="{s}" height="{s}" fill="#000"/>')
        b.append(text(X(st), Y(rg) - 7.5, lab(P, (k, i, j)), 8.5, 'middle', 'bold'))
    save(f'chart-{name}-{k}.svg', svg(W, H, ''.join(b)))

# --- 3D view of a finished piece (knitter's frame: stitch numbers increase to the left, ridges away from you)
def xyz(P, n):
    u, v, k = lat(P, n); return (-(float(u) + float(v) / 2), float(v) * math.sqrt(3) / 2, float(k) * math.sqrt(2 / 3))
def sheet_rect(P, k):
    u0, v0, _ = lat(P, (k, 0, 0)); pts = []
    for st, rg in [(0.5, 0.5), (COLS + 0.5, 0.5), (COLS + 0.5, RIDGES + 0.5), (0.5, RIDGES + 0.5)]:
        dv = (rg - node_ridge(0)) / M; du = (st - node_st(0, 0)) / N - dv / 2
        u, v = float(u0) + du, float(v0) + dv
        pts.append((-(u + v / 2), v * math.sqrt(3) / 2, k * math.sqrt(2 / 3)))
    return pts
def hull_faces(pts):
    faces = []; n = len(pts)
    for a_, b_, c_ in itertools.combinations(range(n), 3):
        A, B, Cc = (pts[t] for t in (a_, b_, c_))
        nx = (B[1] - A[1]) * (Cc[2] - A[2]) - (B[2] - A[2]) * (Cc[1] - A[1]); ny = (B[2] - A[2]) * (Cc[0] - A[0]) - (B[0] - A[0]) * (Cc[2] - A[2])
        nz = (B[0] - A[0]) * (Cc[1] - A[1]) - (B[1] - A[1]) * (Cc[0] - A[0]); ln = math.sqrt(nx * nx + ny * ny + nz * nz)
        if ln < 1e-9: continue
        sd = [(p[0] - A[0]) * nx + (p[1] - A[1]) * ny + (p[2] - A[2]) * nz for p in pts]
        if all(x <= 1e-7 * ln for x in sd) or all(x >= -1e-7 * ln for x in sd):
            on = frozenset(t for t in range(n) if abs(sd[t]) <= 1e-7 * ln)
            if on not in [f for f in faces]: faces.append(on)
    out = []
    for f in faces:
        f = list(f); cx = [sum(pts[t][r] for t in f) / len(f) for r in range(3)]
        # order around the centroid in the face plane
        A = pts[f[0]]; e = [A[r] - cx[r] for r in range(3)]
        nrm = None
        for t in f[1:]:
            q = [pts[t][r] - cx[r] for r in range(3)]
            cr = (e[1] * q[2] - e[2] * q[1], e[2] * q[0] - e[0] * q[2], e[0] * q[1] - e[1] * q[0])
            if math.sqrt(sum(x * x for x in cr)) > 1e-9: nrm = cr; break
        f2 = (nrm[1] * e[2] - nrm[2] * e[1], nrm[2] * e[0] - nrm[0] * e[2], nrm[0] * e[1] - nrm[1] * e[0])
        ang = lambda t: math.atan2(sum((pts[t][r] - cx[r]) * f2[r] for r in range(3)), sum((pts[t][r] - cx[r]) * e[r] for r in range(3)))
        out.append([pts[t] for t in sorted(f, key=ang)])
    return out

def view3d(name, mode, fname, W=820, H=560, phi=-28, theta=27, scale=118):
    P = R[name]['P']; links = R[name]['links']; C = R[name]['C']
    cp, sp_, ct, st_ = math.cos(math.radians(phi)), math.sin(math.radians(phi)), math.cos(math.radians(theta)), math.sin(math.radians(theta))
    allp = [p for k in range(3) for p in sheet_rect(P, k)]
    def proj0(p):
        x1 = p[0] * cp + p[1] * sp_; y1 = -p[0] * sp_ + p[1] * cp
        return x1, -(p[2] * ct + y1 * st_), y1 * ct - p[2] * st_
    xs = [proj0(p)[0] for p in allp]; ys = [proj0(p)[1] for p in allp]
    sc = min((W - 120) / (max(xs) - min(xs)), (H - 60) / (max(ys) - min(ys)))
    ox, oy = (W + 60 - sc * (max(xs) + min(xs))) / 2, (H - sc * (max(ys) + min(ys))) / 2
    def pr(p): x, y, z = proj0(p); return (ox + sc * x, oy + sc * y)
    depth = lambda p: proj0(p)[2]
    b = []
    for k in range(3):
        rect = sheet_rect(P, k)
        b.append(poly([pr(p) for p in rect], '#e9e6df', '#777', 0.9, 0.55))
        fx, fy = pr(rect[1]); b.append(text(fx - 6, fy + 4, f"sheet {P['names'][k]}", 11, 'end', 'bold', '#444'))
        # sheet threads between neighbouring nodes (the fabric carries them)
        for i, j in itertools.product(range(3), repeat=2):
            for di, dj in [(1, 0), (0, 1), (-1, 1)]:
                if 0 <= i + di < 3 and 0 <= j + dj < 3:
                    b.append(line(*pr(xyz(P, (k, i, j))), *pr(xyz(P, (k, i + di, j + dj))), 0.7, '#999', '3 2'))
        for i, j in itertools.product(range(3), repeat=2):
            b.append(circ(*pr(xyz(P, (k, i, j))), 3.0, '#000'))
            if (i, j) in [(0, 0), (2, 0), (0, 2), (2, 2)] or (mode == 'cells' and (i, j) == (1, 1)):
                x, y = pr(xyz(P, (k, i, j))); b.append(text(x + 5, y + 12, lab(P, (k, i, j)), 9, 'start', 'bold', '#222'))
        if k == 2: break
        items = []
        for x in links:
            if x[0][0] != k: continue
            p, q = xyz(P, x[0]), xyz(P, x[1])
            items.append(((depth(p) + depth(q)) / 2 - 1e-3, line(*pr(p), *pr(q), 2.2, TEAL)))
        if mode == 'cells':
            for c in C:
                if c['gap'] != k: continue
                if c['kind'] == 'tet' and c['base'] == 1:
                    for f in hull_faces([xyz(P, n) for n in c['nodes']]):
                        items.append((sum(depth(p) for p in f) / len(f), poly([pr(p) for p in f], GOLD, '#6b5310', 0.7, 0.42)))
                if c['kind'] == 'oct':
                    tri = c['hi'] if k == 0 else c['lo']
                    pts = [xyz(P, n) for n in tri]
                    for p_, q_ in c['links']:
                        a_, b2 = xyz(P, p_), xyz(P, q_); pts.append(tuple((a_[r] + b2[r]) / 2 for r in range(3)))
                    col = VIOL_DN if k == 0 else VIOL_UP
                    for f in hull_faces(pts):
                        items.append((sum(depth(p) for p in f) / len(f), poly([pr(p) for p in f], col, '#3c2366', 0.7, 0.42)))
        for _, it in sorted(items, key=lambda t: -t[0]): b.append(it)
    save(fname, svg(W, H, ''.join(b)))

# --- c against h: section along a row (horizontal = ridges) and plan at one node of B, in the knitter's frame
def ch_fig(name):
    me = PIECES[name]['kind']; U = 78; p = math.sqrt(3) / 2; dd = math.sqrt(2 / 3); b = []
    OFF = {'A': 0, 'B': 1 / 3, 'C': 2 / 3}
    def panel(x0, word, kind, names):
        ymin, ymax = -0.15, 2.65
        X = lambda t: x0 + 34 + (t - ymin) * p * U; Z = lambda k: 214 - k * dd * U
        hi = kind == me
        if hi: b.append(f'<rect x="{x0 + 4}" y="22" width="{(ymax - ymin) * p * U + 62}" height="232" fill="none" stroke="{TEAL}" stroke-width="2.2" rx="6"/>')
        for k, L in enumerate(word):
            b.append(line(X(ymin), Z(k), X(ymax), Z(k), 1.6, '#000')); b.append(text(X(ymin) - 7, Z(k) + 4, names[k], 12, 'end', 'bold'))
        for k in range(2):
            lo, h_ = word[k], word[k + 1]; sgn = 1 if abs((OFF[h_] - OFF[lo]) % 1 - 1 / 3) < 1e-9 else -1
            for r in range(-2, 5):
                t = r + OFF[lo]
                for dt, w in ((sgn / 3, 2.4), (-2 * sgn / 3, 1.0)):
                    if ymin <= t <= ymax and ymin <= t + dt <= ymax: b.append(line(X(t), Z(k), X(t + dt), Z(k + 1), w, TEAL if hi else '#9ab'))
        t0 = 1 + OFF[word[0]]; s2 = 1 / 3 if kind == 'c' else -1 / 3
        b.append(line(X(t0), Z(0), X(t0 + 1 / 3), Z(1), 3.6, '#000')); b.append(line(X(t0 + 1 / 3), Z(1), X(t0 + 1 / 3 + s2), Z(2), 3.6, '#000'))
        for k, L in enumerate(word):
            for r in range(-2, 5):
                t = r + OFF[L]
                if ymin <= t <= ymax: b.append(circ(X(t), Z(k), 3.0))
        title = f"{'T-c' if kind == 'c' else 'T-h'}: B is {kind}, links {'run straight on' if kind == 'c' else 'turn back'}"
        b.append(text(X((ymin + ymax) / 2), 40, title, 11, 'middle', 'bold'))
        b.append(text(X((ymin + ymax) / 2), 247, 'ridges → (towards the bind-off edge)', 9.5))
        return X, Z
    Wp = 2.8 * p * U + 70
    X, Z = panel(0, 'ABC', 'c', ['A', 'B', 'C']); panel(Wp + 14, 'ABA', 'h', ['A', 'B', 'A′'])
    b.append(line(X(2.45) + 14, Z(0), X(2.45) + 14, Z(1), 0.8)); b.append(text(X(2.45) + 17, (Z(0) + Z(1)) / 2 + 4, 'd', 10, 'start', italic=True))
    # plans
    def plan(cx, cy, kind):
        hi = kind == me; Rr = 64; out = []
        if hi: out.append(f'<rect x="{cx - 130}" y="{cy - 114}" width="260" height="194" fill="none" stroke="{TEAL}" stroke-width="2.2" rx="6"/>')
        dn = [(-u, -v) for _, _, u, v in up_links('A', 'B')]
        up = [(u, v) for _, _, u, v in up_links('B', 'C' if kind == 'c' else 'A')]
        V = lambda u, v: (cx - Rr * (float(u) + float(v) / 2), cy - Rr * float(v) * p)
        for i, j in itertools.product(range(-2, 3), repeat=2):
            x, y = V(i, j)
            if math.hypot(x - cx, y - cy) < 1.15 * Rr: out.append(circ(x, y, 2.2, '#aaa'))
        for u, v in dn: out.append(line(cx, cy, *V(u, v), 1.5, '#000', '4 3'))
        for u, v in up:
            ex, ey = V(u, v); out.append(line(cx, cy, ex, ey, 2.6, TEAL if hi else '#9ab')); out.append(circ(ex, ey, 4.2, 'none', '#000', 1.2))
            ds, dr = st_r(u, v); out.append(text(ex + (ex - cx) * 0.55, ey + (ey - cy) * 0.55 + 3, f'{fr0(ds)} st, {fr0(dr)} r', 8.5, 'middle', c='#333'))
        out.append(circ(cx, cy, 4.4))
        out.append(text(cx, cy - 98, f"plan at a node of B ({kind}):", 10.5, 'middle', 'bold'))
        out.append(text(cx, cy - 85, f"links up {'opposite' if kind == 'c' else 'over'} the links down", 10.5, 'middle', 'bold'))
        return ''.join(out)
    b.append(plan(Wp / 2, 386, 'c')); b.append(plan(Wp + 14 + Wp / 2, 386, 'h'))
    b.append(text(Wp + 7, 484, 'black: one pair of links followed through sheet B · thick line: two links (in front of and behind the section) · thin line: one link', 8.4))
    b.append(text(Wp + 7, 497, 'dashed: links down to A · ring: top end of a link up', 8.4))
    b.append(text(Wp + 7, 510, 'st = stitches (+ towards higher stitch numbers) · r = ridges (+ towards the bind-off edge)', 8.4))
    save(f'ch-{name}.svg', svg(2 * Wp + 14, 516, ''.join(b)))

# --- card template, true scale at the reference gauge (print at 100 %)
def card():
    a = a_mm; base, hgt = a / math.sqrt(3), math.sqrt(2 / 3) * a; b = []; top = max(hgt, ell_mm(T_REF)); x0, y0 = 8, 6 + top
    b.append(poly([(x0, y0), (x0 + base, y0), (x0 + base, y0 - hgt)], '#faf6ea', '#000', 0.35))
    r = 11; ang = math.radians(TILT)
    b.append(f'<path d="M {x0 + r:.2f} {y0:.2f} A {r} {r} 0 0 0 {x0 + r * math.cos(ang):.2f} {y0 - r * math.sin(ang):.2f}" fill="none" stroke="#000" stroke-width="0.3"/>')
    b.append(text(x0 + 13.5, y0 - 4.2, f'{TILT:.1f}°', 3.3, 'start'))
    b.append(text(x0 + base / 2, y0 + 4.2, f'a/√3 = {base:.1f} mm (lies on the sheet)', 3.1))
    b.append(text(x0 + base + 1.5, y0 - hgt / 2, f'd = {hgt:.1f} mm', 3.1, 'start'))
    b.append(f'<text font-size="3.1" text-anchor="middle" transform="translate({x0 + base / 2 - 3.5:.2f},{y0 - hgt / 2 - 1:.2f}) rotate({-TILT:.2f})">a = {a:.1f} mm (link)</text>')
    # cord strip and 50 mm control bar
    xs = x0 + base + 28; ell = ell_mm(T_REF)
    b.append(poly([(xs, y0), (xs + 8, y0), (xs + 8, y0 - ell), (xs, y0 - ell)], '#faf6ea', '#000', 0.35))
    b.append(f'<text font-size="3.1" text-anchor="middle" transform="translate({xs + 5:.2f},{y0 - ell / 2:.2f}) rotate(-90)">cord strip ℓ = {ell:.1f} mm (t = {T_REF} mm)</text>')
    xb = xs + 22
    b.append(line(xb, y0, xb, y0 - 50, 0.6)); b.append(line(xb - 1.5, y0, xb + 1.5, y0, 0.4)); b.append(line(xb - 1.5, y0 - 50, xb + 1.5, y0 - 50, 0.4))
    b.append(f'<text font-size="3.1" text-anchor="middle" transform="translate({xb + 4:.2f},{y0 - 25:.2f}) rotate(-90)">50 mm: check the print</text>')
    W = xb + 10
    save('card.svg', svg(W, top + 13, ''.join(b), wmm=round(W, 2)))
    return round(W, 2)

for name in PIECES:
    for k in range(3): chart(name, k)
    view3d(name, 'structure', f'piece-{name}.svg', theta=22, phi=-22); view3d(name, 'cells', f'cells-{name}.svg'); ch_fig(name)
CARD_W = card()
open(os.path.join(DATA, 'check.out'), 'w').write('\n'.join(LOG) + '\n')

# ---------------------------------------------------------------- the booklet
a_cm, d_cm = a_mm / 10, d_mm / 10
SHEET_W, SHEET_H = COLS * 10 / S_REF, RIDGES * 10 / R_REF
THICK = 2 * d_cm + T_REF / 10
def fig(src, cap, w=None):
    st = f' style="width:{w}"' if w else ''
    return f'<figure><img src="figs/{src}"{st} alt=""><figcaption>{cap}</figcaption></figure>'

def sheet_rows(P, k):
    nm = P['names'][k]; out = [f'<li>Cast on {COLS} sts (long-tail). Mark the side facing you as the RS (Row 1 is a RS row).</li>']
    prev = 0
    for j in range(3):
        r = node_row(j)
        out.append(f'<li><b>Rows {prev + 1}–{r - 1}:</b> knit.</li>')
        parts, pos = [], 0
        for i in range(3):
            st = node_st(i, j); parts.append(f'K{st - pos - 1}' if st - pos - 1 else ''); parts.append(f'NK [{lab(P, (k, i, j))}]'); pos = st
        parts.append(f'K{COLS - pos}')
        out.append(f'<li><b>Row {r} (RS, node row {j + 1}, ridge {node_ridge(j)}):</b> {", ".join(x for x in parts if x)}. ({COLS} sts)</li>')
        prev = r
    out.append(f'<li><b>Rows {prev + 1}–{ROWS}:</b> knit. ({RIDGES} ridges)</li>')
    out.append(f'<li>Bind off knitwise on the next RS row. Label the sheet “{nm}” on a tag at the cast-on edge.</li>')
    return '<ol class="rows">' + ''.join(out) + '</ol>'

def node_table(P, k):
    rows = ''.join(f'<tr><td><b>{lab(P, (k, i, j))}</b></td><td class="n">{node_row(j)}</td><td class="n">{node_ridge(j)}</td><td class="n">{node_st(i, j)}</td>'
                   f'<td class="n">{R_name_deg(P, k, i, j)}</td></tr>' for j in range(3) for i in range(3))
    return ('<table class="nt"><tr><th>node</th><th class="n">row</th><th class="n">ridge</th><th class="n">stitch</th><th class="n">links</th></tr>'
            + rows + '</table>')
def R_name_deg(P, k, i, j):
    for nm, r in R.items():
        if r['P'] is P: return r['deg'][(k, i, j)]

def link_table(name):
    P = R[name]['P']; L = R[name]['links']; ell = ell_mm(T_REF)
    def half(g):
        rows = []
        for n, x in enumerate(L):
            if x[0][0] != g: continue
            ds, dr = st_r(x[2], x[3])
            rows.append(f'<tr><td class="n">{n + 1}</td><td><b>{lab(P, x[0])}</b></td><td><b>{lab(P, x[1])}</b></td><td>{fr0(ds)} st, {fr0(dr)} r</td></tr>')
        lo, hi = P['names'][g], P['names'][g + 1]
        return (f'<table class="lt"><tr><th colspan="4">Gap {g + 1}: sheet {lo} → sheet {hi} ({"forward" if g == 0 or P["kind"] == "c" else "backward"} step)</th></tr>'
                '<tr><th class="n">link</th><th>from</th><th>to</th><th>top end lies</th></tr>' + ''.join(rows) + '</table>')
    return f'<div class="two">{half(0)}{half(1)}</div>'

def by_target(name, g):
    P = R[name]['P']; L = R[name]['links']; out = []
    for j in range(3):
        for i in range(3):
            t = (g + 1, i, j); src = [f'{lab(P, x[0])} (link {n + 1})' for n, x in enumerate(L) if x[1] == t]
            out.append(f'<b>{lab(P, t)}</b> ← {", ".join(src) if src else "none"}')
    return '; '.join(out)

def pattern(name):
    P = R[name]['P']; r = R[name]; kind = P['kind']; nm = P['names']; cnt = r['cnt']
    top = nm[2]; shift = lat(P, (2, 0, 0)); ds, dr = st_r(shift[0], shift[1])
    hshift = math.sqrt(float(norm2(shift[0], shift[1]))) * a_cm
    word = '-'.join(nm)
    g2 = 'forward' if kind == 'c' else 'backward'
    nb = sum(1 for c in r['C'] if c['kind'] == 'tet' and c['base'] == 1)
    nb_oct_dn = sum(1 for c in r['C'] if c['kind'] == 'oct' and c['gap'] == 0); nb_oct_up = sum(1 for c in r['C'] if c['kind'] == 'oct' and c['gap'] == 1)
    ntet = sum(1 for c in r['C'] if c['kind'] == 'tet'); noct = sum(1 for c in r['C'] if c['kind'] == 'oct')
    h = [f'<h1 class="brk pat">Pattern {name}: {word} (middle sheet {kind})</h1>']
    h.append(f'''<h2>What you are making</h2>
<p>A three-dimensional HexOct structure, not a flat fabric: three knitted sheets held one above another, joined by 42 knitted cords (links).
Each sheet is one close-packed layer: its 9 marked node stitches lie on a triangular lattice of spacing <i>a</i>. Each node is linked to the
3 nodes of the next sheet that its ball would touch. When the sheets are pulled apart until every cord is taut, the cords stand at
{TILT:.1f}° to the sheets, the sheets lie <i>d</i> = √(2/3)&nbsp;<i>a</i> apart, and sheets and cords close off tetrahedra and
octahedra in space. The middle sheet B is <b>{kind}</b>: {"each cord up from a B node runs on in a straight line from a cord coming down into it (stacking A-B-C)" if kind == "c" else "each cord up from a B node is the mirror image of a cord coming down into it: the bond turns back (stacking A-B-A)"}.
The cells around B are the pieces of the HexOct {kind}-tile (#75, at λ = −1/8). The chart of each sheet only places the node stitches; there is no colourwork.</p>
<table class="sz"><tr><th>at {S_REF} sts and {R_REF} ridges per 10 cm (N = {N}, M = {M})</th><th class="n"></th></tr>
<tr><td>node spacing <i>a</i> (= link length, node to node)</td><td class="n">{a_cm:.2f} cm</td></tr>
<tr><td>sheet spacing <i>d</i> = √(2/3)&nbsp;<i>a</i> (mid-plane to mid-plane)</td><td class="n">{d_cm:.2f} cm</td></tr>
<tr><td>each sheet ({COLS} sts × {RIDGES} ridges)</td><td class="n">{SHEET_W:.1f} × {SHEET_H:.1f} cm</td></tr>
<tr><td>node patch in each sheet (A1 to A9)</td><td class="n">{3 * a_cm:.1f} × {math.sqrt(3) * a_cm:.1f} cm</td></tr>
<tr><td>height of the piece (2<i>d</i> + one sheet thickness {T_REF / 10:.2f} cm)</td><td class="n">{THICK:.1f} cm</td></tr>
<tr><td>top sheet {top} over sheet A: {"node C1 lies " + fr0(ds) + " st and " + fr0(dr) + " ridges from A1" if kind == "c" else "node A′1 lies straight over A1"}</td><td class="n">{f"{hshift:.1f} cm sideways" if kind == "c" else "0 cm sideways"}</td></tr>
<tr><td>cells closed by sheets and cords</td><td class="n">{ntet} tetrahedra, {noct} octahedra</td></tr></table>
<p><b>How it stands.</b> Each sheet is laced into a flat rigid frame. Hang the piece by the top frame and the lower frames settle where all
cords are taut: that is the only place where the sheets are farthest apart, the exact HexOct place (self-centring, spec §1). Then four
posts of length <i>d</i> at the frame corners let it stand on a table. {"Sheet C ends up moved on sideways again, the same way as B over A." if kind == "c" else "Sheet A′ ends up straight over sheet A."}</p>''')
    h.append(fig(f'piece-{name}.svg', f'Figure {name}.1. The finished piece {name}, tensioned, seen from the front (cast-on edges towards you) and above. '
                 f'Grey: the three sheets ({COLS} sts × {RIDGES} ridges); dots: node stitches; dashed: the sheet between neighbouring nodes; teal: the 42 cords, each of length <i>a</i> at {TILT:.1f}°.', '60%'))
    h.append(f'''<h2>Materials for {name}</h2><ul>
<li>DK-weight mercerised cotton (firm, low stretch): 3 balls of 50 g (about 100 m each), one colour.</li>
<li>Contrast thread (any smooth thread in a strong colour): 27 lengths of 15 cm.</li>
<li>Needles: 3.5 mm pair; 3.0 mm double-pointed needles (DPNs), two.</li>
<li>42 safety pins with paper tags; tapestry needle; card for the cord strip and the angle template (finishing page).</li>
<li>Three flat rigid frames, opening about 32 × 22 cm (canvas stretchers, glassless picture frames or stiff card with a window); eight posts of length <i>d</i> (about {d_cm:.1f} cm). Alternatives (spec §4): spacer blocks or stuffing; optional non-stretch core cord, about {42 * (ell_mm(T_REF) + 40) / 1000:.1f} m.</li></ul>''')
    # sheets
    h.append(f'<h1 class="brk">{name}: the three sheets</h1>')
    h.append(f'''<p>Knit all three sheets the same way, in garter stitch, with the 9 node stitches at the same places; only the labels differ.
Do not stretch or block the sheets. Where a sheet lies in the finished piece (A, B or {top}) is not knitted in: the cords set it.
Each chart shows the sheet from the RS, cast-on edge at the bottom, one square = 1 stitch × 1 ridge; black squares are the node
stitches (worked NK). Outlined marks show where the nodes of the other two sheets lie above or below this sheet in the finished
piece ({"○" if True else ""} sheet A, ◇ sheet B, □ sheet {top}), at the exact offsets: B is {fr0(N // 2)} st and {frac(Fr(M, 3))} ridges from A;
{top} is {fr0(ds)} st and {fr0(dr)} ridges from A.</p>''')
    for k in range(3):
        cls = ' class="brk"' if k == 1 else ''
        h.append(f'<h2{cls}>Sheet {nm[k]}</h2><div class="sheet"><div>{sheet_rows(P, k)}</div><div>{node_table(P, k)}</div></div>')
        h.append(fig(f'chart-{name}-{k}.svg', f'Chart {name}-{nm[k]}. Sheet {nm[k]}, {COLS} sts × {RIDGES} ridges ({ROWS} rows). '
                     f'Node stitches {nm[k]}1–{nm[k]}9 on rows {node_row(0)}, {node_row(1)}, {node_row(2)}.', '100%'))
    # links
    h.append(f'<h1 class="brk">{name}: the 42 links</h1>')
    h.append(f'''<p><b>Cord length.</b> Every link is a 3-stitch i-cord of the same free length ℓ = <i>a</i> − 1.22&nbsp;<i>t</i>, measured between the
two sheet faces (<i>t</i> = sheet thickness; measure it on a sheet with a ruler under light pressure). At the reference gauge
<i>a</i> = {a_mm:.1f} mm: ℓ = {ell_mm(3.0):.1f} mm for <i>t</i> = 3.0 mm, {ell_mm(3.5):.1f} mm for 3.5 mm, {ell_mm(4.0):.1f} mm for 4.0 mm.
Cut a card strip of length ℓ. Knit the first cord to the strip under a light, even pull and count its rows; knit every other cord to the
same row count. Equal counts make equal links.</p>
<p><b>To work one cord (from node X of the lower sheet).</b> Lay the lower sheet RS up, cast-on edge towards you. With a 3.0 mm DPN, on the
RS, pick up and knit 3 sts: the node stitch X and the stitch on each side of it in the same ridge. *Slide the sts to the other end of the
DPN, pull the yarn across the back, K3; repeat from * to the row count. Do not bind off: put the 3 live sts on a safety pin and tag it
with the link number and target node Y.</p>
{link_table(name)}
<p class="small">“Top end lies” is where the top of the cord ends up, seen from above, counted from its foot X:
st = stitches (+ towards higher stitch numbers), r = ridges (+ towards the bind-off edge). It is a check, not an instruction: the cords
find these places themselves when tensioned. Links whose target would lie outside the 3 × 3 node patch are left out; that is why
corner nodes have fewer than 3.</p>
<p class="small"><b>Received by each node of sheet B:</b> {by_target(name, 0)}.<br><b>Received by each node of sheet {top}:</b> {by_target(name, 1)}.</p>''')
    h.append(f'<h2 class="brk">{name}: c against h at sheet B</h2>')
    h.append(fig(f'ch-{name}.svg', f'Figure {name}.2. This pattern is the boxed panel{"s" if True else ""}. Top: section seen along a row of nodes '
                 f'(from the side edge), sheets as horizontal lines. Bottom: plan at one node of sheet B, as seen from above on the RS. '
                 + ('In T-c (c) the cords up from B go on in the same direction as the cords coming in from A (forward step A→B→C): a pair of links followed through B is one straight line.'
                    if kind == 'c' else
                    'In T-h (h) the cords up from B go back the way the cords from A came (forward step A→B, then backward step B→A′): a pair of links followed through B folds back like a chevron, and A′ lies over A.'), '90%'))
    h.append(f'''<h2>Joining order</h2><ol>
<li>Knit sheets A, B and {top} (charts above). Check each: 9 node stitches, contrast thread in each.</li>
<li>Lace sheet A into its frame, RS up, cast-on edge towards you. Lace firmly but do not stretch: each of the triangles A1-A2-A4, A2-A4-A5, … must measure <i>a</i> = {a_cm:.1f} cm on all three sides (node centre to node centre).</li>
<li>Work links 1–21 from sheet A (table, gap 1), in order, all to the same row count. Pin and tag each.</li>
<li>Lace sheet B into its frame the same way (RS up, cast-on edge towards you) and hold it over sheet A, about <i>d</i> = {d_cm:.1f} cm above.</li>
<li>Sew each of links 1–21 to its target node of B: from above, with the tapestry needle, pass each of the 3 live stitches through the node stitch or one of its two neighbours in the ridge and fasten off on the RS. Work node by node, B1 to B9 (list “received by”).</li>
<li>Work links 22–42 from the RS of sheet B (table, gap 2: {g2} step), pin and tag.</li>
<li>Lace sheet {top} into its frame, RS up, cast-on edge towards you; sew links 22–42 to its nodes, {top}1 to {top}9.</li>
<li>Weave in all ends; remove the contrast threads or leave them as node marks.</li></ol>
<h2>Finishing: tension the piece</h2>
<p>Hang the piece by the frame of sheet {top} (two strings from a hook or a rod), sheets horizontal, and let frames B and A hang on the
cords. Each frame sinks until all of its cords are taut. Taut cords of equal length allow the greatest spacing only when the sheet sits
exactly in its place over the one below (spec §1: any sideways shift <i>t</i> lowers the spacing to at most √(2/3&nbsp;<i>a</i>² − <i>t</i>²));
so a hanging sheet centres itself. Tap the frames lightly so that they settle. Measure the spacing at the four corners of each frame
(expect <i>d</i> = {d_cm:.1f} cm between the sheets' mid-planes) and cut four posts to the measured length for each gap. Set the posts
between the frame corners, outside the node patch, and stand the piece on a table. If a cord is slack while the others are taut, it is
too long: unpick its sewn end and work it again to the row count.</p>''')
    h.append(f'<figure><img src="figs/card.svg" style="width:{CARD_W}mm" alt=""><figcaption>Card template (link angle and sheet spacing) and cord strip, true size for '
             f'<i>a</i> = {a_mm:.1f} mm (print at 100 %; the bar must measure 50 mm). For another <i>a</i>: a right triangle with legs '
             f'0.577&nbsp;<i>a</i> (on the sheet) and 0.816&nbsp;<i>a</i> (upright); its slanted edge is <i>a</i> and its foot angle {TILT:.1f}°. '
             'Cut it from card and use the long leg to check the sheet spacing at the same time.</figcaption></figure>')
    # check your work
    deg = r['deg']
    degtab = ''.join(f'<tr><td>sheet {nm[k]}</td>' + ''.join(f'<td class="n">{deg[(k, i, j)]}</td>' for j in range(3) for i in range(3)) + f'<td class="n">{sum(deg[(k, i, j)] for i in range(3) for j in range(3))}</td></tr>' for k in range(3))
    h.append(f'<h1 class="brk">{name}: check your work</h1>')
    h.append(f'''<table class="sz"><tr><th>count</th><th class="n">expected</th></tr>
<tr><td>node stitches (9 per sheet)</td><td class="n">27</td></tr>
<tr><td>links (gap 1 + gap 2)</td><td class="n">42 (21 + 21)</td></tr>
<tr><td>gap 1 (A–B): tetrahedra on A · tetrahedra hanging from B · octahedra</td><td class="n">{cnt[0]["tet_lo"]} · {cnt[0]["tet_hi"]} · {cnt[0]["oct"]}</td></tr>
<tr><td>gap 2 (B–{top}): tetrahedra on B · tetrahedra hanging from {top} · octahedra</td><td class="n">{cnt[1]["tet_lo"]} · {cnt[1]["tet_hi"]} · {cnt[1]["oct"]}</td></tr></table>
<table class="dg"><tr><th>links per node</th>{"".join(f"<th class='n'>{t}</th>" for t in range(1, 10))}<th class="n">sum</th></tr>{degtab}</table>
<p><b>The cells.</b> Every closed cell has all its edges of length <i>a</i>: a sheet edge between neighbouring nodes or a cord. A
tetrahedron is 3 nodes of one sheet and the one node of the next sheet linked to all three (3 cords). An octahedron is a triangle of
3 nodes below and the opposite triangle above, joined by 6 cords. In the HexOct tiles of #75 at λ = −1/8, sheet B's {kind}-tile is:
the tetrahedra standing on B and hanging from B (gold), the upper halves of the octahedra of gap 1 and the lower halves of the
octahedra of gap 2, cut at the gaps' mid-planes (violet; each half has 3 nodes and the midpoints of its 6 cords). This piece holds
{nb} tetrahedral pieces and {nb_oct_dn + nb_oct_up} octahedral halves of sheet B; around node {", ".join(r["full"])} the four pieces
of one whole {kind}-tile are all closed (checked against tiles.py of #75). {"The octahedra of gap 2 are set aside from those of gap 1 (c)." if kind == "c" else "The octahedra of gap 2 sit straight over those of gap 1 (h)."}</p>''')
    h.append(fig(f'cells-{name}.svg', f'Figure {name}.3. The tensioned piece with the cells of sheet B coloured as its HexOct {kind}-tile pieces (#75, λ = −1/8): '
                 'gold, tetrahedral pieces; violet, octahedral halves (lighter: below B, darker: above B); teal, the cords. '
                 f'Cells of sheets A and {top} are left open.', '80%'))
    h.append(f'''<h2>Measure it</h2><ul>
<li><b>Link length.</b> Node centre to node centre along each cord: <i>a</i> = {a_cm:.1f} cm (the same as the node spacing in a sheet). Free cord between the sheet faces: ℓ.</li>
<li><b>Sheet spacing.</b> Mid-plane to mid-plane at each frame corner: <i>d</i> = √(2/3)&nbsp;<i>a</i> = 0.8165&nbsp;<i>a</i> = {d_cm:.1f} cm (face to face {d_cm - T_REF / 10:.1f} cm).</li>
<li><b>Link angle.</b> Stand the card template on the lower sheet, upright, its long leg vertical, its slanted edge along a cord: the cord lies on the edge, at {TILT:.2f}° to the sheet (arctan √2).</li>
<li><b>Position of the top sheet.</b> Hang a plumb line (thread and a small weight) from node {top}1: it meets sheet A {"at " + fr0(ds) + " st and " + fr0(dr) + " ridges from A1, " + f"{hshift:.1f} cm away" if kind == "c" else "on A1 itself"}. From B1 it meets sheet A at +8 st and +4⅔ ridges from A1 ({a_cm / math.sqrt(3):.1f} cm).</li></ul>''')
    return '\n'.join(h)

# gauge table
def gauge_table():
    rows = []
    for q in [Fr(85, 100), Fr(90, 100), Fr(95, 100), Fr(1), Fr(105, 100), Fr(110, 100), Fr(115, 100)]:
        m = round(0.866 * N * float(q)); err = m / (math.sqrt(3) / 2 * N * float(q)) - 1
        rows.append(f'<tr><td class="n">{float(q):.2f}</td><td class="n">{m}</td><td class="n">{err * 100:+.1f} %</td></tr>')
    return ('<table class="gt"><tr><th class="n">R / S</th><th class="n">M (N = 16)</th><th class="n">row spacing error</th></tr>' + ''.join(rows) + '</table>')

CSS = '''table{border-collapse:collapse;font-size:7.8pt;margin:1.5mm 0;width:100%} td,th{border-bottom:1px solid #ddd;padding:0.5mm 1.1mm;text-align:left;vertical-align:top} td.n,th.n{text-align:right}
body,p,li{font-size:8.9pt;line-height:1.38} h1{font-size:17pt} h1.pat{font-size:15pt;margin-top:0} h1.brk{font-size:13pt;margin-top:0} .logo{width:22mm}
h2{font-size:11pt;margin:3mm 0 1mm} h2,h1{break-after:avoid} ol,ul{margin:1mm 0 1mm 5mm;padding-left:3mm} li{margin:0.4mm 0}
figure{margin:2mm 0;break-inside:avoid;text-align:center} figure img{width:100%;display:block;margin:0 auto} figcaption{font-size:7.8pt;line-height:1.33;color:#333;margin-top:1mm;text-align:left}
.brk{break-before:page} .status{border:1px solid #b8962e;background:#faf6ea;padding:2mm 3mm;font:8pt "DejaVu Sans",sans-serif;margin:0 0 3mm}
.two{display:grid;grid-template-columns:1fr 1fr;gap:4mm} .two table{font-size:7.6pt} .small{font-size:7.9pt}
.sheet{display:grid;grid-template-columns:1.55fr 1fr;gap:4mm;break-inside:avoid} ol.rows li{font-size:8.4pt} table.nt{font-size:7.4pt}
table.sz{width:auto;min-width:60%} table.gt{width:auto} table.dg td,table.dg th{padding:0.4mm 1.2mm} .abbr td:first-child{font-weight:bold;white-space:nowrap}'''

contents = ''.join(f'<li>{t}</li>' for t in ['Materials, gauge, abbreviations',
    'Pattern T-c (A-B-C, middle sheet c): what you are making · the three sheets with charts · the 42 links · c against h · joining · finishing · check your work',
    'Pattern T-h (A-B-A′, middle sheet h): the same parts'])
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Knitted HexOct: Patterns</title><link rel="stylesheet" href="../paper.css">
<style>{CSS}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Knitted HexOct: Patterns</h1>
<p class="sub">Two test pieces, T-c and T-h: three knitted sheets and 42 knitted links that stand in space as the HexOct structure</p>
<div class="meta"><b>DICTO</b> · dictospheres.com · 3 November 2026 · study 2026-11-03-knitted-hexoct-patterns · pattern, not published</div>
<div class="status"><b>Status.</b> Pattern, not published; no DOI. Not yet test-knitted. Built from the Knitted HexOct specification (study
2026-11-02-knitted-hexoct); every number, chart and table is generated by scripts/patterns.py and checked there (27 nodes, 42 links,
node positions, link geometry, cells against the #75 tiles).</div>
<p>DICTO proposed the Knitted HexOct: a multi-layer knitted fabric whose sheets are close-packed layers and whose links join each node
to the 3 nodes of the next sheet that its ball touches, so that c and h are carried by the links. These patterns make the two smallest
pieces that show c against h. Each piece is the structure itself in three dimensions: the sheets are layers A, B, C (or A, B, A′),
the knitted links are the bonds between them, and the cells closed off by sheets and links are tetrahedra and octahedra, the pieces of
the HexOct c-tile or h-tile. There is no colourwork: the charts only tell you where the node stitches are.</p>
<h2>Contents</h2><ol>{contents}</ol>
<h2>Materials (both pieces)</h2><ul>
<li>Yarn: DK-weight mercerised cotton, firm and low-stretch, about 210 m per piece: 3 balls of 50 g (about 100 m) per piece, 5 balls for both.</li>
<li>Needles: 3.5 mm pair (sheets); 3.0 mm double-pointed needles (DPNs), two (links).</li>
<li>Contrast thread for the node marks: 27 lengths of 15 cm per piece.</li>
<li>42 safety pins with paper tags per piece; tapestry needle; ruler; card for the cord strip and the angle template.</li>
<li>To hold the shape: three flat rigid frames per piece (opening about 32 × 22 cm) and four posts per gap; or, as alternatives (spec §4), spacer blocks between the sheets, stuffing in the cells, or stiffened cords (starch, glue, or a non-stretch core cord inside each i-cord).</li></ul>
<h2>Gauge</h2>
<p>Knit a garter-stitch swatch of 30 sts × 40 ridges on 3.5 mm needles (one ridge = 2 rows). Lay it flat without stretching and measure
<b>S</b> = stitches per 10 cm and <b>R</b> = ridges per 10 cm.</p>
<ul><li><b>N</b>, the node spacing in stitches: {N} (must be even, so that every second node row can shift by half a spacing). Then
<i>a</i> = 10&nbsp;N/S cm.</li>
<li><b>M</b>, the node-row spacing in ridges: the whole number nearest 0.866 × N × R/S. With a square garter gauge (R = S), M = {M}: the
node rows come out 14/16 = 0.875&nbsp;<i>a</i> apart instead of 0.866&nbsp;<i>a</i>, +1.0 %.</li>
<li>Sheet: cast on 4N sts, work 3M ridges. Node rows: the RS row of ridges ⌈M/2⌉, ⌈M/2⌉ + M, ⌈M/2⌉ + 2M. Node stitch (i, j), i = 0, 1, 2 along the
row, j = 0, 1, 2 the node row: stitch N/2 + 1 + N&nbsp;i + (N/2)&nbsp;j.</li></ul>
<div class="two"><div>{gauge_table()}<p class="small">For a more exact triangle, larger N: N = 30, M = 26 gives the row spacing to 0.07 %, but <i>a</i> ≈ 14 cm (spec §4).</p></div>
<div><p class="small">The patterns below are written for <b>N = {N}, M = {M}</b> (cast on {COLS}, {RIDGES} ridges, node rows {node_row(0)}, {node_row(1)},
{node_row(2)}). Sizes are given at the reference gauge {S_REF} sts and {R_REF} ridges per 10 cm: <i>a</i> = {a_cm:.2f} cm,
<i>d</i> = {d_cm:.2f} cm. With your own S, scale every size by {S_REF}/S. If your M differs, recompute the node rows from the formula;
the node stitches depend on N only.</p></div></div>
<h2>Abbreviations</h2>
<table class="abbr" style="width:auto">
<tr><td>K, Kn</td><td>knit; knit n stitches</td></tr>
<tr><td>NK [X]</td><td>node knit: knit the next stitch with the yarn and a 15 cm contrast thread held together; leave both thread ends hanging. This stitch is node X.</td></tr>
<tr><td>RS, WS</td><td>right side, wrong side (mark the RS: garter looks the same on both)</td></tr>
<tr><td>st(s); r</td><td>stitch(es); ridge (2 rows of garter)</td></tr>
<tr><td>DPN</td><td>double-pointed needle</td></tr>
<tr><td>i-cord</td><td>3 sts on a DPN: knit 3, slide the sts to the other end, pull the yarn across the back, repeat</td></tr>
<tr><td><i>a</i>, <i>d</i>, ℓ, <i>t</i></td><td>node spacing; sheet spacing √(2/3)&nbsp;<i>a</i>; free cord length <i>a</i> − 1.22&nbsp;<i>t</i>; sheet thickness</td></tr>
<tr><td>A1…A9, B1…B9, C1…C9, A′1…A′9</td><td>nodes: sheet letter, then 1 + i + 3j (node row 1: 1–3, row 2: 4–6, row 3: 7–9)</td></tr>
<tr><td>gap 1, gap 2</td><td>the space between sheets 1 and 2, and between sheets 2 and 3</td></tr></table>
{pattern("T-c")}
{pattern("T-h")}
</body></html>'''
open(os.path.join(OUT, 'paper.html'), 'w').write(html)
print('written', OUT)
