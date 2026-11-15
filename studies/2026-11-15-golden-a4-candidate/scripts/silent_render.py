# The two golden twisted-silent 4D solids (DICTO 15 Nov 2026, for naming and for the paper "Silent Running: Twisted Silence"):
#   A = convex hull of all permutations of (phi^2, phi^2, phi^2, phi, 0)  (20 corners, in the hyperplane x1 + ... + x5 = 0 after centring)
#   B = convex hull of all permutations of (phi^2, phi^2, 1, 1, 0)        (30 corners)
# Part 1 (exact, Q(sqrt5)): facets (the 3D cells) as the faces x_S = min of the Rado inequalities sum_{i in S} x_i >= ..., kept when
# the face is 3-dimensional; edges and ridges from the facet incidences; every cell named from its corners, edges and polygons, with
# exact squared edge lengths. Cross-check: facet count of a floating-point hull (scipy). Control: the uniform truncated and cantellated
# 5-cells, perms of (2,2,2,1,0) and (2,2,1,1,0), must come out with ONE edge length.
# Part 2 (renders): (1) Schlegel view from just outside one cell (eye on the cell's axis, EYE x its distance, as #105 Figure 1),
# inner cells pulled a little apart from the centre, coloured by cell type, the outer cell as a cage; painting copied from
# studies/2026-11-15-paradigm-cover/scripts/cover.py (z-buffer, light, depth-shaded crisp edges). (2) Orthogonal projection onto the
# Coxeter plane of A4 (x -> sum x_k w^k, w = exp(2 pi i/5): 5-fold symmetric), edges coloured by length (short sqrt2, long phi sqrt2),
# shaded by depth along the second Coxeter plane.
# Run from the study folder: python scripts/silent_render.py [--pilot]   -> data/silent-cells.txt, figures/*.png
import itertools, os, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
PILOT = '--pilot' in sys.argv
# ------------------------------------------------------------------ exact arithmetic in Q(sqrt5): a + b sqrt5
class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q5(-s.a, -s.b)
    def __sub__(s, o): return s + (-(o if isinstance(o, Q5) else Q5(o)))
    def __rsub__(s, o): return Q5(o) - s
    def __mul__(s, o): o = o if isinstance(o, Q5) else Q5(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): d = s.a * s.a - 5 * s.b * s.b; assert d != 0; return Q5(s.a / d, -s.b / d)
    def __truediv__(s, o): return s * (o if isinstance(o, Q5) else Q5(o)).inv()
    def zero(s): return s.a == 0 and s.b == 0
    def sign(s):
        if s.zero(): return 0
        sa, sb = (s.a > 0) - (s.a < 0), (s.b > 0) - (s.b < 0)
        if sa >= 0 and sb >= 0: return 1
        if sa <= 0 and sb <= 0: return -1
        return sa if s.a * s.a > 5 * s.b * s.b else sb
    def __eq__(s, o): return (s - o).zero()
    def __lt__(s, o): return (s - o).sign() < 0
    def __hash__(s): return hash((s.a, s.b))
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return f'{s.b}*sqrt5'
        return f'{s.a}{"+" if s.b > 0 else "-"}{abs(s.b)}*sqrt5'
PHI = Q5(Fr(1, 2), Fr(1, 2)); PHI2 = PHI * PHI
assert PHI2 == PHI + 1
def rank(rows):
    """Exact rank of a list of Q5 vectors (Gaussian elimination)."""
    M = [list(r) for r in rows]; r = 0; n = len(M[0]) if M else 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if not M[i][c].zero()), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; inv = M[r][c].inv()
        for i in range(len(M)):
            if i != r and not M[i][c].zero():
                f = M[i][c] * inv; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
    return r
def affdim(V): return rank([[x - y for x, y in zip(v, V[0])] for v in V[1:]]) if len(V) > 1 else 0
def sq(u, v): return sum(((x - y) * (x - y) for x, y in zip(u, v)), Q5(0))
def fmt(q):   # squared length a + b sqrt5 -> readable length
    tab = {(Fr(2), Fr(0)): 'sqrt2', (Fr(3), Fr(1)): 'phi*sqrt2', (Fr(1), Fr(0)): '1', (Fr(8), Fr(0)): '2*sqrt2'}
    return tab.get((q.a, q.b), f'sqrt({q})')
# ------------------------------------------------------------------ the polytope: facets, edges, ridges, cells (exact)
def analyse(seed, label, out):
    seed = tuple(x if isinstance(x, Q5) else Q5(x) for x in seed)
    V = sorted(set(itertools.permutations(seed)), key=lambda v: tuple(float(x) for x in v))
    n = len(V); facets = []
    for k in range(1, 5):
        for S in itertools.combinations(range(5), k):
            sums = [sum((v[i] for i in S), Q5(0)) for v in V]; m = min(sums)
            F = [i for i in range(n) if sums[i] == m]
            if affdim([V[i] for i in F]) == 3: facets.append((S, frozenset(F)))
    # float cross-check: scipy hull facet count (coplanar triangles merged)
    B = np.linalg.svd(np.eye(5) - np.ones((5, 5)) / 5)[0][:, :4]
    X = np.array([[float(x) for x in v] for v in V]); X = (X - X.mean(1, keepdims=True)) @ B
    h = ConvexHull(X); nf = len({tuple(np.round(e, 7)) for e in h.equations})
    assert nf == len(facets), (label, nf, len(facets))
    inc = [set(fi for fi, (_, F) in enumerate(facets) if i in F) for i in range(n)]
    edges = []
    for i, j in itertools.combinations(range(n), 2):
        common = inc[i] & inc[j]
        if len(common) >= 3 and frozenset.intersection(*[facets[f][1] for f in common]) == {i, j}: edges.append((i, j))
    ridges = set()
    for a, b in itertools.combinations(range(len(facets)), 2):
        I = facets[a][1] & facets[b][1]
        if len(I) >= 3 and affdim([V[i] for i in I]) == 2: ridges.add(I)
    lens = sorted({sq(V[i], V[j]) for i, j in edges}, key=float)
    # every 2-face of the polytope is a ridge (4D): polygons with ordered sides
    def polygon(R):
        Ed = [(i, j) for i, j in edges if i in R and j in R]; assert len(Ed) == len(R), 'ridge not a polygon'
        adj = {i: [] for i in R}
        for i, j in Ed: adj[i].append(j); adj[j].append(i)
        cyc = [min(R)]; prev = None
        while len(cyc) < len(R):
            nx = [x for x in adj[cyc[-1]] if x != prev and x not in cyc][0]; prev = cyc[-1]; cyc.append(nx)
        return [fmt(sq(V[cyc[t]], V[cyc[(t + 1) % len(cyc)]])) for t in range(len(cyc))]
    def polyname(sides):
        k = len(sides); u = sorted(set(sides))
        base = {3: 'triangle', 4: 'quadrilateral', 6: 'hexagon'}[k]
        if len(u) == 1: return {3: 'triangle', 4: 'square', 6: 'regular hexagon'}[k] + f' side {u[0]}'
        if k == 4: return f'rectangle {u[0]} x {u[1]}' if sides[0] == sides[2] else 'kite?'
        if k == 6 and sides[0::2] == [sides[0]] * 3 and sides[1::2] == [sides[1]] * 3: return f'hexagon, sides {sides[0]} and {sides[1]} in turn'
        return base + ' ' + ','.join(sides)
    cells = []
    for S, F in facets:
        Ed = [(i, j) for i, j in edges if i in F and j in F]
        polys = [polygon(R) for R in ridges if R <= F]
        el = sorted({fmt(sq(V[i], V[j])) for i, j in Ed})
        ptypes = {}
        for p in polys: ptypes[polyname(p)] = ptypes.get(polyname(p), 0) + 1
        nv, ne, nfc = len(F), len(Ed), len(polys); assert nv - ne + nfc == 2, 'Euler'
        kinds = sorted(len(p) for p in polys)
        if nv == 4 and len(el) == 1: name = 'regular tetrahedron'
        elif nv == 6 and nfc == 8 and len(el) == 1: name = 'regular octahedron'
        elif nv == 6 and nfc == 5: name = 'triangular prism' + (' (right, square sides)' if len(el) == 1 else ', golden (sides golden rectangles)')
        elif nv == 12 and kinds == [3] * 4 + [6] * 4: name = 'truncated tetrahedron' + (' (uniform)' if len(el) == 1 else ', golden (hexagon sides 1 : phi)')
        elif nv == 12 and kinds == [3] * 8 + [4] * 6: name = 'cuboctahedron' + (' (uniform)' if len(el) == 1 else ', golden (rectangles 1 : phi, triangles of two sizes)')
        else: name = f'cell with {nv} corners'
        cells.append({'S': S, 'F': sorted(F), 'name': name, 'nv': nv, 'ne': ne, 'nf': nfc, 'edges': el, 'polys': ptypes})
    out.append(f'== {label}: corners {n}, cells {len(facets)}, ridges {len(ridges)}, edges {len(edges)}; '
               f'edge lengths {", ".join(fmt(l) for l in lens)}' + (f'; ratio^2 = {lens[1] / lens[0]} (phi^2 = {PHI2})' if len(lens) == 2 else ''))
    assert n - len(edges) + len(ridges) - len(facets) == 0, 'Euler 4D'
    by = {}
    for c in cells: by.setdefault((c['name'], c['nv'], c['ne'], c['nf'], tuple(c['edges']), tuple(sorted(c['polys'].items()))), []).append(c['S'])
    for (name, nv, ne, nfc, el, pt), Ss in by.items():
        out.append(f'  {len(Ss)} x {name}: {nv} corners, {ne} edges ({", ".join(el)}), {nfc} faces: ' + '; '.join(f'{k} x {p}' for p, k in pt)
                   + f'  [cells x_S = min for |S| = {sorted({len(s) for s in Ss})}]')
    return V, X, cells, edges, lens
# ------------------------------------------------------------------ painting
GROUND = (21, 25, 33)
EDGE = np.array([240, 234, 216.]); GOLDL = (217, 165, 33)
COL = {   # Platonic cells in DICTO's element colours (T red fire, O yellow air); the golden cells in a calm teal; prisms dusty rose
    'regular tetrahedron': (205, 62, 40), 'regular octahedron': (232, 200, 82)}
def colour(name):
    if name in COL: return COL[name]
    if name.startswith('truncated tetrahedron') or name.startswith('cuboctahedron'): return (92, 168, 170)
    if name.startswith('triangular prism'): return (196, 140, 158)
    return (180, 180, 180)
def look(d, up):
    z = np.array(d, float); z /= np.linalg.norm(z); up = np.array(up, float); x = np.cross(up, z); x /= np.linalg.norm(x); y = np.cross(z, x)
    return np.array([x, y, z])
def faces_of(pts):
    h = ConvexHull(pts); F = {}
    for simp, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    out = []
    for key, idx in F.items():
        idx = list(idx); q = pts[idx]; nrm = np.array(key[:3]); c = q.mean(0); e1 = q[0] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
        out.append((q[np.argsort(np.arctan2((q - c) @ e2, (q - c) @ e1))], nrm))
    return out
def render(PC, M, size, SS, cage=None, cagecol=GOLDL, margin=0.08):
    """Z-buffer painting (from the Paradigm cover script): PC = [(faces, rgb)], orthographic view M; square canvas of `size` px with
    the model fitted inside the margin (same scale for x and y). cage = 3D segments drawn as thin lines, depth-tested."""
    allv = np.vstack([f[0] for F, _ in PC for f in F] + ([np.array(cage).reshape(-1, 3)] if cage is not None else [])) @ M.T
    lo, hi = allv.min(0), allv.max(0); inner = size * (1 - 2 * margin)
    s = inner / max(hi[0] - lo[0], hi[1] - lo[1]); ox = (size - s * (hi[0] - lo[0])) / 2; oy = (size - s * (hi[1] - lo[1])) / 2
    to_px = lambda V: np.c_[ox + s * ((V @ M.T)[:, 0] - lo[0]), oy + s * (hi[1] - (V @ M.T)[:, 1])]
    Wb = Hb = size * SS
    zb = np.full((Hb, Wb), -np.inf, np.float32); ib = np.full((Hb, Wb), -1, np.int32); nrm, cols = [], []
    for F, col in PC:
        for pts, nv in F:
            nn = M @ nv
            if nn[2] <= 1e-9: continue
            q = to_px(pts) * SS; zz = (pts @ M.T)[:, 2] * s * SS
            x0, x1 = max(0, int(q[:, 0].min())), min(Wb, int(np.ceil(q[:, 0].max())) + 1)
            y0, y1 = max(0, int(q[:, 1].min())), min(Hb, int(np.ceil(q[:, 1].max())) + 1)
            if x1 <= x0 or y1 <= y0: continue
            yy, xx = np.mgrid[y0:y1, x0:x1] + 0.5; inside = np.ones(xx.shape, bool)
            area = np.sum(q[:, 0] * np.roll(q[:, 1], -1) - np.roll(q[:, 0], -1) * q[:, 1]); sg = np.sign(area)
            for a, b in zip(q, np.roll(q, -1, axis=0)):
                inside &= sg * ((b[0] - a[0]) * (yy - a[1]) - (b[1] - a[1]) * (xx - a[0])) >= 0
            z = zz[0] - (nn[0] * (xx - q[0, 0]) - nn[1] * (yy - q[0, 1])) / nn[2]
            sub = zb[y0:y1, x0:x1]; win = inside & (z > sub)
            sub[win] = z[win]; ib[y0:y1, x0:x1][win] = len(nrm)
            nrm.append(nn); cols.append(col)
    nrm, cols = np.array(nrm), np.array(cols, float)
    fg = ib >= 0; N = np.zeros((Hb, Wb, 3), np.float32); N[fg] = nrm[ib[fg]]; C = np.zeros((Hb, Wb, 3), np.float32); C[fg] = cols[ib[fg]]
    l = np.array([-0.45, 0.62, 0.64]); l /= np.linalg.norm(l)
    diff = np.clip(N @ l, 0, 1); rim = np.clip(N @ (np.array([0.5, -0.6, 0.3]) / np.linalg.norm([0.5, -0.6, 0.3])), 0, 1)
    yy, xx = np.mgrid[0:Hb, 0:Wb].astype(np.float32)
    Lp = np.stack([(-0.15 * Wb - xx), (yy + 0.6 * Hb), np.full_like(xx, 1.2 * max(Wb, Hb))], -1)
    Lp /= np.linalg.norm(Lp, axis=-1, keepdims=True); Hv = Lp + np.array([0, 0, 1], np.float32); Hv /= np.linalg.norm(Hv, axis=-1, keepdims=True)
    spec = np.clip(np.sum(N * Hv, -1), 0, 1) ** 30
    rgb = C * (0.36 + 0.58 * diff)[..., None] + 255 * (0.20 * spec + 0.05 * rim ** 3)[..., None]
    rgb[~fg] = GROUND
    e = np.zeros((Hb, Wb), bool); e[:, :-1] |= ib[:, :-1] != ib[:, 1:]; e[:-1] |= ib[:-1] != ib[1:]
    zf = zb.copy(); zf[~fg] = -np.inf; zmax = ndimage.maximum_filter(zf, size=3)
    zl, zh = zb[fg].min(), zb[fg].max(); dz = np.clip((zmax - zl) / (zh - zl), 0, 1)
    e = ndimage.binary_dilation(e, iterations=max(1, SS))          # about 2.3 px after downsampling (standard: >= 1.5 px)
    dz = ndimage.maximum_filter(np.where(np.isfinite(dz), dz, 0), size=2 * SS)
    ea = ndimage.gaussian_filter(e.astype(np.float32), SS * 0.35) * (0.55 + 0.45 * dz)   # depth-shaded: near bright, far dimmer
    rgb = rgb * (1 - ea[..., None]) + EDGE * ea[..., None]
    if cage is not None:
        ca = np.zeros((Hb, Wb), np.float32)
        segs = [to_px(np.array(g)) * SS for g in cage]; zs = [(np.array(g) @ M.T)[:, 2] * s * SS for g in cage]
        zall = np.concatenate(zs); czl, czh = zall.min(), zall.max()
        for q, zz in zip(segs, zs):
            m = int(np.hypot(*(q[1] - q[0]))) * 2 + 2; t = np.linspace(0, 1, m)
            pts = q[0] + t[:, None] * (q[1] - q[0]); zp = zz[0] + t * (zz[1] - zz[0])
            xi, yi = pts[:, 0].astype(int), pts[:, 1].astype(int); ok = (xi >= 0) & (xi < Wb) & (yi >= 0) & (yi < Hb)
            xi, yi, zp = xi[ok], yi[ok], zp[ok]; vis = zp > zb[yi, xi]
            ca[yi[vis], xi[vis]] = np.maximum(ca[yi[vis], xi[vis]], 0.55 + 0.45 * (zp[vis] - czl) / (czh - czl + 1e-9))
        ca = ndimage.grey_dilation(ca, size=(2 * SS + 1, 2 * SS + 1)); ca = ndimage.gaussian_filter(ca, SS * 0.35)
        rgb = rgb * (1 - ca[..., None]) + np.array(cagecol, float) * ca[..., None]
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)
    return img
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(px): return ImageFont.truetype(FONT, px)
def schlegel_panel(V, X, cells, outer_name, size, SS, pull, eye_f, wv, ta=0.0, rz=0.0):
    """Schlegel view through one cell of type outer_name; inner cells pulled apart by pull x their centre."""
    oc = next(i for i, c in enumerate(cells) if c['name'] == outer_name)
    n0 = X[cells[oc]['F']].mean(0); hf = np.linalg.norm(n0); nh = n0 / hf; eye = nh * hf * eye_f
    B = []
    for e in np.eye(4):
        v = e - (e @ nh) * nh
        for b in B: v = v - (v @ b) * b
        if np.linalg.norm(v) > 1e-6 and len(B) < 3: B.append(v / np.linalg.norm(v))
    B = np.array(B)
    def sch(x): dx = x - eye; t = (hf - eye @ nh) / (dx @ nh); return B @ (eye + t * dx)
    S3 = np.array([sch(x) for x in X]); S3 /= np.linalg.norm(S3, axis=1).max()
    ho = ConvexHull(S3[cells[oc]['F']])   # a true Schlegel diagram: every corner inside the outer cell (eye close enough)
    assert np.all(S3 @ ho.equations[:, :3].T + ho.equations[:, 3] <= 1e-9), ('eye too far: not a Schlegel diagram', eye_f)
    PC = []
    for ci, c in enumerate(cells):
        if ci == oc: continue
        q = S3[c['F']]; F = faces_of(q); assert len(F) == c['nf'], (c['name'], len(F))
        sh = q.mean(0) * pull; PC.append(([(f + sh, nv) for f, nv in F], colour(c['name'])))
    # view: between a big-face normal and a small-face normal of the outer cell, weights wv
    Fo = faces_of(S3[cells[oc]['F']]); big = max(Fo, key=lambda f: len(f[0]))[1]; small = min(Fo, key=lambda f: len(f[0]))[1]
    d = wv[0] * big + wv[1] * small; d /= np.linalg.norm(d); up = small - (small @ d) * d
    if np.linalg.norm(up) < 1e-6: up = np.array([0, 0, 1.0])
    a, c = np.radians(ta), np.radians(rz)
    Rx = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]]); Rz = np.array([[np.cos(c), -np.sin(c), 0], [np.sin(c), np.cos(c), 0], [0, 0, 1]])
    M = Rz @ Rx @ look(d, up)
    allp = np.vstack([f for F_, _ in PC for f, _ in F_]); h0 = ConvexHull(S3[cells[oc]['F']])
    fac = max(1.0, np.max((allp @ h0.equations[:, :3].T) / -h0.equations[:, 3])) * 1.04
    segs = {}
    for f, nv in faces_of(S3[cells[oc]['F']] * fac):
        for a, b in zip(f, np.roll(f, -1, axis=0)): segs.setdefault(tuple(sorted((tuple(np.round(a, 9)), tuple(np.round(b, 9))))), []).append((M @ nv)[2])
    assert len(segs) == cells[oc]['ne']
    cage = [np.array(g) for g, nz in segs.items() if min(nz) < 0]   # outline and back edges only: a frame behind the cells
    return render(PC, M, size, SS, cage, cagecol=colour(outer_name)), oc
def coxeter_panel(V, edges, lens, size, SS):
    """Orthogonal projection onto the A4 Coxeter plane (5-fold); depth = the second Coxeter plane; edges by length."""
    w = np.exp(2j * np.pi * np.arange(5) / 5); P = np.array([[float(x) for x in v] for v in V]); P -= P.mean(1, keepdims=True)
    z = P @ w; dep = -np.abs(P @ w ** 2)   # 5-fold invariant: corners nearer the picture plane drawn brighter
    xy = np.c_[z.real, -z.imag]; r = np.abs(xy).max(); m = 0.08
    px = (xy / r) * (size * (0.5 - m)) + size / 2
    big = Image.new('RGB', (size * SS, size * SS), GROUND); d = ImageDraw.Draw(big)
    dl, dh = dep.min(), dep.max(); short = lens[0]
    def sq_(i, j): return sum((V[i][k] - V[j][k]) * (V[i][k] - V[j][k]) for k in range(5))
    E = sorted(edges, key=lambda e: dep[e[0]] + dep[e[1]])
    for i, j in E:
        t = ((dep[i] + dep[j]) / 2 - dl) / (dh - dl + 1e-12)   # 0 far, 1 near
        base = np.array(GOLDL if not (sq_(i, j) == short) else (150, 200, 205), float)
        col = tuple(int(c) for c in GROUND + (base - GROUND) * (0.45 + 0.55 * t))
        wdt = int(round(SS * (2.2 + 1.6 * t)))
        d.line([tuple(px[i] * SS), tuple(px[j] * SS)], fill=col, width=wdt)
    for i in np.argsort(dep):
        t = (dep[i] - dl) / (dh - dl + 1e-12); rr = SS * (2.6 + 2.0 * t)
        col = tuple(int(c) for c in GROUND + (EDGE - GROUND) * (0.5 + 0.5 * t))
        d.ellipse([px[i][0] * SS - rr, px[i][1] * SS - rr, px[i][0] * SS + rr, px[i][1] * SS + rr], fill=col)
    return big.resize((size, size), Image.LANCZOS)
def sheet(panels, legend, title, out):
    """Panels side by side on the ground, a caption line under each, a legend row, the DICTO mark bottom right."""
    P = panels[0][0].size[0]; f = P / 1300; pad = int(50 * f); top = int(150 * f); cap = int(70 * f)
    ft, fc, fl, fm = font(int(44 * f)), font(int(30 * f)), font(int(29 * f)), font(int(26 * f)); lh = int(46 * f); sw = int(30 * f)
    Wd = len(panels) * P + (len(panels) + 1) * pad
    probe = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    rows, x = 1, pad                      # legend rows needed (same wrapping as below)
    for col, txt in legend:
        if col == 'BR': rows += 1; x = pad; continue
        wdt = (sw + int(12 * f) if col is not None else 0) + probe.textlength(txt, font=fl)
        if x + wdt > Wd - pad: rows += 1; x = pad
        x += wdt + int(40 * f)
    Hd = top + P + cap + rows * lh + int(110 * f)
    im = Image.new('RGB', (Wd, Hd), GROUND); d = ImageDraw.Draw(im)
    for k, line in enumerate(title): d.text((pad, int(28 * f) + k * int(56 * f)), line, font=ft if k == 0 else fc, fill=(236, 230, 214) if k == 0 else (200, 196, 186))
    for k, (p, c) in enumerate(panels):
        x = pad + k * (P + pad); im.paste(p, (x, top)); assert d.textlength(c, font=fc) < P, ('caption too long', c)
        d.text((x + (P - d.textlength(c, font=fc)) / 2, top + P + int(12 * f)), c, font=fc, fill=(200, 196, 186))
    y = top + P + cap + int(14 * f); x = pad
    for col, txt in legend:
        if col == 'BR': x = pad; y += lh; continue
        wdt = (sw + int(12 * f) if col is not None else 0) + d.textlength(txt, font=fl)
        if x + wdt > Wd - pad: x = pad; y += lh
        if col is not None: d.rectangle([x, y + int(3 * f), x + sw, y + int(3 * f) + sw], fill=col); x += sw + int(12 * f)
        d.text((x, y), txt, font=fl, fill=(220, 214, 200)); x += d.textlength(txt, font=fl) + int(40 * f)
    mk = 'DICTO · dictospheres.com'; d.text((Wd - pad - d.textlength(mk, font=fm), Hd - int(56 * f)), mk, font=fm, fill=(150, 150, 150))
    im.save(out); return im
if __name__ == '__main__':
    SS = 1 if PILOT else 3; SIZE = 700 if PILOT else 1300
    os.makedirs('figures', exist_ok=True); os.makedirs('data', exist_ok=True)
    out = []
    print('PROGRESS 0.00 start', flush=True)
    # controls: the uniform members have one edge length and the uniform cell names
    _, _, cu, _, lu = analyse((2, 2, 2, 1, 0), 'CONTROL uniform truncated 5-cell, perms of (2,2,2,1,0)', out)
    assert len(lu) == 1 and sorted(c['name'] for c in cu) == ['regular tetrahedron'] * 5 + ['truncated tetrahedron (uniform)'] * 5
    _, _, cu, _, lu = analyse((2, 2, 1, 1, 0), 'CONTROL uniform cantellated 5-cell, perms of (2,2,1,1,0)', out)
    assert len(lu) == 1 and sorted(c['name'] for c in cu) == ['cuboctahedron (uniform)'] * 5 + ['regular octahedron'] * 5 + ['triangular prism (right, square sides)'] * 10
    print('PROGRESS 0.15 controls ok', flush=True)
    A = analyse((PHI2, PHI2, PHI2, PHI, Q5(0)), 'A: perms of (phi^2, phi^2, phi^2, phi, 0)', out)
    Bs = analyse((PHI2, PHI2, Q5(1), Q5(1), Q5(0)), 'B: perms of (phi^2, phi^2, 1, 1, 0)', out)
    assert len(A[0]) == 20 and len(A[2]) == 10 and len(A[3]) == 40 and len(Bs[0]) == 30 and len(Bs[2]) == 20 and len(Bs[3]) == 90, ('\n'.join(out), [len(t) for t in A[:4]], [len(t) for t in Bs[:4]])
    txt = '\n'.join(out); print(txt, flush=True)
    open('data/silent-cells.txt', 'w').write('# exact cell analysis (Q(sqrt5)), scripts/silent_render.py; DICTO · dictospheres.com\n' + txt + '\n')
    print('PROGRESS 0.30 exact analysis written', flush=True)
    E = os.environ.get
    SOL = {'A': (A, 'truncated tetrahedron, golden (hexagon sides 1 : phi)', '(φ², φ², φ², φ, 0)', 'golden truncated tetrahedron'),
           'B': (Bs, 'cuboctahedron, golden (rectangles 1 : phi, triangles of two sizes)', '(φ², φ², 1, 1, 0)', 'golden cuboctahedron')}
    made = []
    if PILOT:   # Schlegel views only, small: a grid of pull x view weight x tilt per solid
        os.makedirs('figures/pilot', exist_ok=True); grid = []
        for tag in 'AB':
            for pl in [float(t) for t in E('PULLS', '0.8,1.4').split(',')]:
                for ws in [float(t) for t in E('WSS', '0.55,1.6').split(',')]:
                    for ta in [float(t) for t in E('TAS', '0,25').split(',')]:
                        for ey in [float(t) for t in E('EYES', '1.18').split(',')]: grid.append((tag, pl, ws, ta, ey))
        grid = [g for g in grid if g[0] in E('TAGS', 'AB')]
        for k, (tag, pl, ws, ta, ey) in enumerate(grid):
            (V, X, cells, edges, lens), outer, _, _ = SOL[tag]
            try: sp, _ = schlegel_panel(V, X, cells, outer, 520, 1, pl, ey, (1.0, ws), ta)
            except AssertionError as ex: print('SKIP', tag, ey, ex, flush=True); continue
            o = f'figures/pilot/{tag}-p{pl}-w{ws}-t{ta}-e{ey}.png'; sp.save(o); made.append(o)
            print(f'PROGRESS {0.30 + 0.70 * (k + 1) / len(grid):.2f} pilot {o}', flush=True)
    else:
        for k, tag in enumerate('AB'):
            (V, X, cells, edges, lens), outer, seed, oname = SOL[tag]
            pl, ws, ta, rz, ey = (float(E(f'{v}_{tag}', dflt)) for v, dflt in (('PULL', 0.8), ('WS', 0.55), ('TA', 0), ('RZ', 0), ('EYE', 1.18)))
            sp, oc = schlegel_panel(V, X, cells, outer, SIZE, SS, pl, ey, (1.0, ws), ta, rz)
            cp = coxeter_panel(V, edges, lens, SIZE, SS)
            sp.save(f'figures/silent-{tag}-schlegel.png'); cp.save(f'figures/silent-{tag}-coxeter.png')
            names = {}
            for c in cells: names[c['name']] = names.get(c['name'], 0) + 1
            legend = [(colour(nm), f'{cnt} {nm}') for nm, cnt in sorted(names.items(), key=lambda t: -t[1])]
            legend += [('BR', ''), (None, 'Right, edges:'), ((150, 200, 205), 'short sqrt2'), (GOLDL, 'long phi·sqrt2 (ratio phi : 1)')]
            legend = [(c, t.replace('phi', 'φ').replace('sqrt2', '√2')) for c, t in legend]
            title = [f'Twisted-silent solid {tag}: all permutations of {seed}',
                     f'{len(V)} corners, {len(edges)} edges, {len(cells)} cells; two edge lengths, √2 and φ√2']
            sheet([(sp, f'Schlegel view through one {oname}, cells pulled apart'),
                   (cp, 'Orthogonal projection on the 5-fold (Coxeter) plane')], legend, title, f'figures/RENDER-silent-{tag}.png')
            made.append(f'figures/RENDER-silent-{tag}.png'); print(f'PROGRESS {0.30 + 0.70 * (k + 1) / 2:.2f} {tag}', flush=True)
    ok = all(os.path.exists(m) for m in made)
    print('FINAL ok' if ok else 'FINAL FAIL', flush=True)
