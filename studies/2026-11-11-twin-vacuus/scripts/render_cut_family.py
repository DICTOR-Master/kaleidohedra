# render_cut_family.py (from render_shared_angelus.py), DICTO 11 Nov 2026 ("render the OG cut family with the kites"): the Catalan pentakis
# (same five-fold corners as the OG) uncut and cut at its six-fold corners at lam = 0.95, 0.90, phi^2/3 (the OG) and 0.85; faces coloured by
# kind. Control: lam = phi^2/3 gives the OG exactly. First version: render_shared_angelus.py, DICTO 11 Nov 2026 ("render the identical level 1 Angelus"): left the OG, middle the
# Catalan pentakis scaled so its five-fold corners coincide with the OG's (s = (9 + 3 sqrt5)/2), both as solids (faces by kind); right
# their common level-1 Angelus (Vacuus of the identical level-1 twin hull), fins coloured by plane. Control: the two level-1 twin hulls are
# equal as exact point sets. First version: render_thread.py, DICTO 11 Nov 2026 ("render the Angeli thread for the Catalan pentakis"): the four Angeli
# (Vacuus of the twin hull) round the hop's 4-cycle from the Catalan pentakis dodecahedron, 2 x 2 panels, fins coloured by their plane.
# Usage: render_thread.py <ffo dir> <render.py> <logo> <out.png>. Original header: pentakis_family.py, DICTO 11 Nov 2026 ("i wonder if other pentakis produce dodecahedrons, icosahedrons and rhombicosidodecahedrons").
# The OG family's twin hulls pass exactly through the regular icosahedron (k = 2) and dodecahedron (k = 3, 7) and rhombicosidodecahedron
# patterns (k = 1, 5, 6). Do other PENTAKIS DODECAHEDRA, used as the start D_0 of the same hop (D_{k+1} = hull of the foot points of D_k's
# face planes), do the same? Starts (exact Q(sqrt5)): the Catalan pentakis dodecahedron (polar dual of the regular truncated icosahedron)
# and dodecahedra with a pyramid on each face, apex at relative heights h (apex radius = face distance * (1 + h)), h in Q(sqrt5).
# Per start and level k <= KMAX: twin hull (sqrt5 -> -sqrt5 on the exact corners), corners, faces by sides, and its kind: REGULAR
# ICOSAHEDRON / REGULAR DODECAHEDRON (exact: one edge length, regular faces), rhombicosidodecahedron pattern (60 corners; 20, 30, 12 faces;
# with the rectangles' side ratio), other. Control: the start is convex with 32 corners and 60 triangles.
# usage: python -u pentakis_family.py <five-fold-octet dir> <KMAX> <out.json>
import sys, os, json, time, itertools
ARGS = list(sys.argv); RENDER = os.path.abspath(ARGS[2]); LOGO = os.path.abspath(ARGS[3]); OUTP = os.path.abspath(ARGS[4]); KMAX = 3
here = os.path.expanduser('~/k-research/studies/2026-11-09-og-margin/scripts')
sys.argv = [ARGS[0], ARGS[1], '0', '/dev/null']; exec(open(os.path.join(here, 'exact_family.py')).read().split("t0 = time.time()")[0])
KMAX = 3
import numpy as np
from collections import Counter
from scipy.spatial import ConvexHull
from gmpy2 import mpq
PHI = R5(mpq(1, 2), mpq(1, 2)); IPHI = R5(mpq(-1, 2), mpq(1, 2)); ONE = R5(1); ZERO = R5(0)
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def signs(v):
    out = set()
    for sg in itertools.product((1, -1), repeat=3):
        out.add(tuple(x if s == 1 else -x for x, s in zip(v, sg)))
    return list(out)
def uniq(P): return list(dict.fromkeys(P))
DOD = uniq([p for base in [(ONE, ONE, ONE)] for p in signs(base)] + [p for base in cyc((ZERO, PHI, IPHI)) for p in signs(base)])   # 11-11: orientation of the group G (dual of the icosahedron (0, +-1, +-phi))
assert len(DOD) == 20, len(DOD)
# five-fold directions = face normals of DOD: take whichever of (0, 1, phi) / (0, phi, 1) cyclic families are face normals
Df = np.array([fl(v) for v in DOD]); hD = ConvexHull(Df); FN = hD.equations[:, :3]
def is_normal(d):
    d = np.array([x.f() for x in d]); d /= np.linalg.norm(d); return np.abs(FN @ d - 1).min() < 1e-9
fam = None
for base in ((ZERO, ONE, PHI), (ZERO, PHI, ONE)):
    if is_normal(base): fam = base
assert fam is not None
AX = uniq([p for b in cyc(fam) for p in signs(b)]); assert len(AX) == 12
# face distance of DOD along an axis direction a: d_f = min over DOD corners of (v.a)/|a| ... exact: plane n.x = c with n = a; c = max v.a over the face = (v.a) for v on the face
a0 = AX[0]; c0 = max((dot(v, a0) for v in DOD), key=lambda x: x.f())       # n.x = c0 is the face plane for normal a0 (unnormalised)
def pentakis(hrel):
    """apex t*a with a.(t a) = c0 (1 + h): t = c0 (1 + h) / (a.a)."""
    t = c0 * (ONE + hrel) / dot(a0, a0)
    return DOD + [tuple(t * x for x in a) for a in AX]
# Catalan pentakis: polar dual of the regular truncated icosahedron (edge 2): corners even perms of (0, 1, 3phi), (1, 2+phi, 2phi), (phi, 2, 2phi+1)
TWO = R5(2); THREE = R5(3)
TIb = [(ZERO, ONE, THREE * PHI), (ONE, TWO + PHI, TWO * PHI), (PHI, TWO, TWO * PHI + ONE)]
TI = uniq([p for b in TIb for c in cyc(b) for p in signs(c)]); assert len(TI) == 60, len(TI)
def polar_dual(P):
    Pf = np.array([fl(v) for v in P]); idx = {v: i for i, v in enumerate(P)}; F, ne, _ = exact_faces(P, idx, Pf)
    return [tuple(x / d_ for x in n_) for n_, d_, _ in F.values()]           # face n.x = d  ->  dual point n/d
CAT = polar_dual(TI)
def twinf(x):
    re = float(x.a) + float(x.b) * S5
    return float(x.a) - float(x.b) * S5 if abs(re) < 1e-6 or x.b == 0 else float(x.a * x.a - 5 * x.b * x.b) / re
def twin_kind(Wk):
    idx = {v: i for i, v in enumerate(Wk)}; Wfx = np.array([fl(v) for v in Wk]); F, ne, _ = exact_faces(Wk, idx, Wfx)
    cor = sorted(set(i for mem in F for i in mem)); T = np.array([[twinf(x) for x in Wk[i]] for i in cor]); T /= np.linalg.norm(T, axis=1).max()
    h = ConvexHull(T); En = h.equations; n = len(En); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(En[f] - En[g]).max() < 1e-9: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
    sides = Counter(len(p) for p in grp.values()); V = len(h.vertices)
    E = set()
    for p in grp.values():
        ii = np.array(sorted(p)); Q = T[ii]; c = Q.mean(0); B = np.linalg.svd(Q - c)[2][:2]; q = (Q - c) @ B.T; cy = list(ii[np.argsort(np.arctan2(q[:, 1], q[:, 0]))])
        for a, b in zip(cy, cy[1:] + cy[:1]): E.add((min(a, b), max(a, b)))
    L = np.array([np.linalg.norm(T[a] - T[b]) for a, b in E]); Ls = np.unique(np.round(L / L.max(), 9))
    if V == 12 and sides == {3: 20}: kind = 'REGULAR ICOSAHEDRON' if len(Ls) == 1 else 'icosahedron pattern'
    elif V == 20 and sides == {5: 12}: kind = 'REGULAR DODECAHEDRON' if len(Ls) == 1 else 'dodecahedron pattern'
    elif V == 60 and sides == {3: 20, 4: 30, 5: 12}: kind = 'rhombicosidodecahedron ' + ('(uniform)' if len(Ls) == 1 else f'pattern, rectangles {Ls.max() / Ls.min():.6f}:1')
    elif V == 30 and sides == {3: 20, 5: 12}: kind = 'icosidodecahedron ' + ('(uniform)' if len(Ls) == 1 else 'pattern')
    else: kind = f'{V} corners, faces {dict(sorted(sides.items()))}'
    return kind, F, cor

cwd0 = os.getcwd(); sys.argv = ['x', '.', '.', LOGO]; exec(open(RENDER).read().split('def plate(')[0])
import colorsys
from PIL import Image, ImageDraw, ImageFont
def pcol(j):
    h = (j * 0.618033988749895) % 1.0; s_ = 0.55 + 0.25 * ((j * 7) % 3) / 2; v = 0.62 + 0.28 * ((j * 5) % 4) / 3
    return np.array(colorsys.hsv_to_rgb(h, s_, v))

def hop(W):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W]); F, ne, _ = exact_faces(W, idx, Wfx)
    feet = {}
    for n_, d_, _ in F.values():
        s_ = d_ / dot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
    return list(feet)
def conj(x): return R5(x.a, -x.b)
def twin_hull_exact(W):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W]); F, ne, _ = exact_faces(W, idx, Wfx)
    cor = sorted(set(i for mem in F for i in mem)); T = [tuple(conj(x) for x in W[i]) for i in cor]
    Tf = np.array([[twinf(x) for x in W[i]] for i in cor]); h = ConvexHull(Tf / np.linalg.norm(Tf, axis=1).max()); return [T[i] for i in h.vertices]
OGW = [tuple(cv(x) for x in v) for v in OG]; S9 = R5(mpq(9, 2), mpq(3, 2)); CATs = [tuple(S9 * x for x in v) for v in CAT]

def solid_panel(W, title):
    P = np.array([fl(v) for v in W]); P /= np.linalg.norm(P, axis=1).max(); h = ConvexHull(P); En = h.equations; n = len(En); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(En[f] - En[g]).max() < 1e-9: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), []).append(f)
    M = rot(20, 24); Pv = P @ M.T; C = Canvas(1.08); KC = {3: '#d4af37', 4: '#8e5bd6', 6: '#2bb3a3', 5: '#e07b39'}   # triangles gold, kites purple, pentagons orange, hexagons teal
    for gi, fs in enumerate(grp.values()):                                  # one id per whole face: outlines only on true face edges (11-11)
        k_ = len(set(int(j) for f in fs for j in h.simplices[f])); col = rgb(KC.get(k_, '#8a8f9c'))
        for f in fs:
            tri = Pv[h.simplices[f]]; C.tri(tri, shade(col, En[f, :3] @ M.T), gi)
    C.outlines(); kinds = Counter(len(set(int(j) for f in fs for j in h.simplices[f])) for fs in grp.values())
    return C.image(), title, f'{len(h.vertices)} corners, faces {dict(sorted(kinds.items()))}'
def angelus_panel(H):
    T = np.array([[twinf(x) if False else x.f() for x in v] for v in H]); T /= np.linalg.norm(T, axis=1).max(); h = ConvexHull(T); En = h.equations; n = len(En); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(En[f] - En[g]).max() < 1e-9: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
    faces = []
    for pts in grp.values():
        ii = np.array(sorted(pts)); Q = T[ii]; c = Q.mean(0); B = np.linalg.svd(Q - c)[2][:2]; q = (Q - c) @ B.T; faces.append(list(ii[np.argsort(np.arctan2(q[:, 1], q[:, 0]))]))
    E = sorted({(min(a, b), max(a, b)) for f in faces for a, b in zip(f, f[1:] + f[:1])}); planes = {}
    for i, (a, b) in enumerate(E):
        nn = np.cross(T[a], T[b]); nn /= np.linalg.norm(nn); nn *= np.sign(nn[np.argmax(np.abs(nn) > 1e-9)]); planes.setdefault(tuple(np.round(nn, 7)), []).append(i)
    pidx = {i: j for j, ids in enumerate(planes.values()) for i in ids}
    M = rot(20, 24); Wv = T @ M.T; C = Canvas(1.08); O = np.zeros(3)
    for i, (a, b) in enumerate(E):
        tri = np.array([O, Wv[a], Wv[b]]); C.tri(tri, shade(pcol(pidx[i]), np.cross(tri[1], tri[2])), i)
    NF = []
    for f in faces:
        nv = np.zeros(3)
        for j in range(len(f)): nv += np.cross(Wv[f[j]], Wv[f[(j + 1) % len(f)]])
        NF.append(nv)
    C.outlines(); C.ghost(Wv, faces, NF, 0.08)
    return C.image(), 'their common level-1 Angelus', f'{len(E)} fins, {len(planes)} fin planes, apex 12.87° and 34.12° (identical from both)'

P = CATs; idx = {v: i for i, v in enumerate(P)}; Pf = np.array([fl(v) for v in P]); F, ne, _ = exact_faces(P, idx, Pf)
r2c = {}
for v in P: r2c.setdefault(dot(v, v), []).append(v)
SIX = [v for r, vs in r2c.items() if len(vs) == 20 for v in vs]
EDG = set()
for mem in F:
    mm = sorted(mem); Q = Pf[mm]; c = Q.mean(0); B = np.linalg.svd(Q - c)[2][:2]; q = (Q - c) @ B.T; cy = [mm[i] for i in np.argsort(np.arctan2(q[:, 1], q[:, 0]))]
    for a, b in zip(cy, cy[1:] + cy[:1]): EDG.add((min(a, b), max(a, b)))
nb = {i: set() for i in range(len(P))}
for a, b in EDG: nb[a].add(b); nb[b].add(a)
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def cut(lam):
    pts = [v for v in P if v not in set(SIX)]
    for v in SIX:
        i = idx[v]; d = lam * dot(v, v)
        for j in nb[i]:
            w = P[j]; t = (d - dot(v, v)) / dot(v, sub(w, v)); pts.append(tuple(a + t * (b - a) for a, b in zip(v, w)))
    return list(dict.fromkeys(pts))
LS = [('uncut: the Catalan pentakis', None), ('cut at 0.95', R5(mpq(19, 20))), ('cut at 0.90', R5(mpq(9, 10))), ('cut at φ²/3: the OG (kites appear)', R5(mpq(1, 2), mpq(1, 6))), ('cut at 0.85', R5(mpq(17, 20)))]
panels = []; ok = True
for title, lam in LS:
    W = P if lam is None else cut(lam)
    if lam is not None and lam == R5(mpq(1, 2), mpq(1, 6)): ok &= set(W) == set(OGW)
    panels.append(solid_panel(W, title))
os.chdir(cwd0)
G = PX + 40; im = Image.new('RGB', (len(panels) * G - 40, PX + 200), 'white'); dr = ImageDraw.Draw(im)
try: ft = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 34); fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 23)
except Exception: ft = fs = ImageFont.load_default()
dr.text((24, 14), 'The OG cut family: the Catalan pentakis cut at its six-fold corners; the OG is the cut where the cuts touch', fill=(30, 30, 40), font=ft)
for j, (img, t1, t2) in enumerate(panels):
    x = j * G; im.paste(img, (x, 150)); dr.text((x + 24, 70), t1, fill=(50, 50, 60), font=fs); dr.text((x + 24, 102), t2, fill=(100, 100, 110), font=fs)
lg = Image.open(LOGO).convert('RGBA'); hh = 70; lg = lg.resize((int(lg.width * hh / lg.height), hh)); im.paste(lg, (im.width - lg.width - 8, im.height - hh - 8), lg)
dr.text((24, im.height - 38), 'DICTO · dictospheres.com · triangles gold, kites purple, pentagons orange, hexagons teal · depth = fraction of the six-fold corner radius', fill=(120, 110, 90), font=fs)
im.save(OUTP, dpi=(300, 300)); print('FINAL ok' if ok else 'FINAL FAIL: the phi^2/3 cut is not the OG')
