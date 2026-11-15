# render_nest.py (15 Nov 2026) - DICTO · dictospheres.com
# The nest pendant of the Platonic book's Chapter 10 (Filigree): the nest of #99 (Plato's Five in the Octet, Theorem 1), all five
# Platonic solids one inside the next in one octahedral cell of the octet, O > I > D > C > T, with the gap pieces of #99 §2 between
# neighbours drawn in gold: six Admiral Caps (O - I), 12 Sheriffs and 30 Lone-stars (I - D), Euclid's six roofs (D - C) and four
# copies of the octahedron's centre pyramid at 2/3 (C - T). DICTO's see-through standard: the outer stones as translucent crystal
# shells in their element colours, the innermost stone (the tetrahedron) solid, one metallic gold for every connecting piece.
# Exact coordinates in Q(sqrt5) (golden.py of study 2026-11-14-platonic-hybrid): the frame of #47 Lemma 4, icosahedron of edge 1 in
# Pacioli's position inside the octahedron of edge phi^2/sqrt2; this is #99's nest scaled by phi^2/sqrt2 (octet edge phi^2/sqrt2).
# D = face centres of I; C = the 8 corners of D on the three-fold axes; T = 4 alternate corners of C (as #99 Theorem 1).
# Exact checks first (X lines), then the figure (3 panels); imported (by ../cover-planb/packing_cover.py) it gives the pieces and checks.
# Usage: render_nest.py <outdir> [width_px]  -> PROGRESS, X, COUNT lines; FINAL ok / FINAL FAIL
import sys, os, itertools, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
MAIN = __name__ == '__main__'
if MAIN: OUTD = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 2400
import jewels_lib as J
G = J.G
from golden import V, Part, PHI, Q5
from fractions import Fraction as F
if MAIN: os.makedirs(OUTD, exist_ok=True)
FAIL = []
def X(name, ok, detail=''):
    print(('X PASS ' if ok else 'X FAIL ') + name + (f': {detail}' if detail != '' else ''), flush=True)
    if not ok: FAIL.append(name)
d2 = lambda a, b: G.dot(G.sub(a, b), G.sub(a, b))
def cen(vs): return tuple(sum((v[i] for v in vs), Q5()) / len(vs) for i in range(3))
def edge2(vs): return min(d2(a, b) for a, b in itertools.combinations(vs, 2))
def faces(vs):
    """facets of the convex hull as (plane, corner list)"""
    return [((n, c), [v for v in vs if G.dot(n, v) == c]) for n, c in G.planes_from_vertices(vs)]
def inside(pts, outer):
    P = G.planes_from_vertices(outer); return all(G.dot(n, v) <= c for n, c in P for v in pts)
# ------------------------------------------------------------------ the nest (exact)
O = list(G.OCT); I = list(G.ICO)
FI = faces(I); D = [cen(f) for _, f in FI]
C = [v for v in D if v[0] * v[0] == v[1] * v[1] == v[2] * v[2]]
T = [v for v in C if v[0] * v[1] * v[2] > 0]
gold = []
gold += [('A', [Part(t) for t in a], []) for a in G.admiral_caps()]                       # O - I: six Admiral Caps
eI = edge2(I)
for (n, c), f in faces(D):                                                               # I - D: Sheriffs (I corner over each D face)
    apex = max(I, key=lambda v: G.dot(n, v)); gold.append(('Sh', [Part(f + [apex])], []))
for a, b in itertools.combinations(I, 2):                                                # I - D: Lone-stars (I edge + 2 D corners)
    if d2(a, b) != eI: continue
    two = [cen(f) for _, f in FI if a in f and b in f]; gold.append(('Ls', [Part([a, b] + two)], []))
hc = C[0][0] if C[0][0] > 0 else -C[0][0]                                                # D - C: Euclid's six roofs
for ax in range(3):
    for s in (1, -1):
        gold.append(('R', [Part([v for v in C if v[ax] == s * hc] + [v for v in D if v not in C and v[ax] * s > hc])], []))
eC = edge2(C)
for v in C:                                                                              # C - T: four corner pyramids
    if v in T: continue
    gold.append(('P', [Part([v] + [t for t in T if d2(v, t) == eC])], []))
STONES = {'O': O, 'I': I, 'D': D, 'C': C, 'T': T}
# ------------------------------------------------------------------ exact checks
PHI4 = PHI * PHI * PHI * PHI                                                            # squared edges below are exact in Q(sqrt5)
X('O: 6 corners, edge^2 = phi^4/2 (edge phi^2/sqrt2)', len(O) == 6 and edge2(O) == PHI4 / 2)
X('I: 12 corners, edge 1 (Pacioli), I/O edge ratio sqrt2/phi^2', len(I) == 12 and edge2(I) * PHI * PHI * PHI * PHI / 2 == edge2(O))
X('D: 20 corners at the face centres of I, edge = (phi/3) x I edge', len(D) == 20 and edge2(D) == PHI * PHI / 9)
X('C: 8 corners of D, edge = phi x D edge', len(C) == 8 and edge2(C) == PHI * PHI * edge2(D))
X('T: 4 alternate corners of C, edge = sqrt2 x C edge', len(T) == 4 and edge2(T) == 2 * edge2(C) and all(d2(a, b) == edge2(T) for a, b in itertools.combinations(T, 2)))
X('C is the dual cube of O: its 8 corners are the face centres of O', sorted(map(str, C)) == sorted(str(cen(f)) for _, f in faces(O)))
X('nest: I in O, D in I, C in D, T in C (every corner inside, exact)', inside(I, O) and inside(D, I) and inside(C, D) and inside(T, C))
cnt = J.count(gold); print('COUNT gold', cnt, flush=True)
X('gold pieces: 6 Admiral Caps, 12 Sheriffs, 30 Lone-stars, 6 roofs, 4 pyramids', cnt == {'A': 6, 'Sh': 12, 'Ls': 30, 'R': 6, 'P': 4})
vol = lambda lab: sum((G.volume(p.verts) for pc in gold if pc[0] == lab for p in pc[1]), Q5())
vO, vI, vD, vC, vT = (G.volume(STONES[k]) for k in 'OIDCT')
X('O - I = the six Admiral Caps (exact volume)', vO - vI == vol('A'))
X('I - D = 12 Sheriffs + 30 Lone-stars (exact volume)', vI - vD == vol('Sh') + vol('Ls'))
X('D - C = Euclid\'s six roofs (exact volume)', vD - vC == vol('R'))
X('C - T = four corner pyramids (exact volume)', vC - vT == vol('P'))
X('every gold piece lies in the outer solid of its gap', all(inside(p.verts, {'A': O, 'Sh': I, 'Ls': I, 'R': D, 'P': C}[pc[0]]) for pc in gold for p in pc[1]))
sh = next(pc for pc in gold if pc[0] == 'Sh')[1][0].verts; ap = max(sh, key=lambda v: G.dot(v, v))
X('Sheriff: base edge = D edge, slant edges = sqrt3/phi x base (#99)', all(d2(ap, v) * PHI * PHI == 3 * edge2(D) for v in sh if v != ap))
pyr = next(pc for pc in gold if pc[0] == 'P')[1][0].verts
X('pyramid: trirectangular, legs = C edge = (2/3) x the legs 1/sqrt2 of O\'s centre pyramid at #99 scale',
  sorted(d2(pyr[0], v) for v in pyr[1:]) == [eC] * 3 and eC * 9 == PHI4)
for k in 'OIDCT': print(f'VOL {k} {float(G.volume(STONES[k])):.6f}', flush=True)
print('PROGRESS 0.15 checks', flush=True)
# ------------------------------------------------------------------ rendering: nested see-through shells, opaque gold and core
fl = lambda vs: np.array([[float(x) for x in v] for v in vs])
STONE = J.STONE; GOLDC = np.array([212, 160, 52.]); GOLD_EDGE = np.array([92, 64, 18.]); GROUND = np.array(J.GROUND, float)
ALPHA_F = {'O': 0.09, 'I': 0.15, 'D': 0.17, 'C': 0.17}; ALPHA_B = {'O': 0.04, 'I': 0.06, 'D': 0.07, 'C': 0.08}
SHELLS = ['O', 'I', 'D', 'C']
def look(d, up=(0, 0, 1.0)):
    z = np.array(d, float); z /= np.linalg.norm(z); x = np.cross(up, z); x /= np.linalg.norm(x); y = np.cross(z, x); return np.array([x, y, z])
def stone_faces(k): return [(n, poly) for n, poly in J.piece_faces((k, [Part(STONES[k])], []))]
def tri_raster(s, Wd, Ht):
    """yield (ya, yb, xa, xb, mask, z) for the fan triangles of projected polygon s (columns x, y, z)"""
    for k in range(1, len(s) - 1):
        (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = s[0], s[k], s[k + 1]
        xa, xb = int(max(0, np.floor(min(x0, x1, x2)))), int(min(Wd - 1, np.ceil(max(x0, x1, x2))))
        ya, yb = int(max(0, np.floor(min(y0, y1, y2)))), int(min(Ht - 1, np.ceil(max(y0, y1, y2))))
        if xb < xa or yb < ya: continue
        Xg, Yg = np.meshgrid(np.arange(xa, xb + 1) + 0.5, np.arange(ya, yb + 1) + 0.5)
        dd = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(dd) < 1e-12: continue
        a = ((y1 - y2) * (Xg - x2) + (x2 - x1) * (Yg - y2)) / dd; b = ((y2 - y0) * (Xg - x2) + (x0 - x2) * (Yg - y2)) / dd; c = 1 - a - b
        m = (a >= -1e-9) & (b >= -1e-9) & (c >= -1e-9)
        if m.any(): yield ya, yb, xa, xb, m, a * z0 + b * z1 + c * z2
def render(gold_pieces, Rm, Wpx, Hpx, extra_gold=(), stones=('O', 'I', 'D', 'C', 'T'), scale=None, ground=None):
    SS = 3; Wd, Ht = Wpx * SS, Hpx * SS
    pts = np.vstack([fl(O)] + [p for _, _, p, _ in extra_gold]) @ Rm.T
    sc = scale * SS if scale else min(Wd * 0.88 / np.ptp(pts[:, 0]), Ht * 0.90 / np.ptp(pts[:, 1]))
    mx, my = (pts[:, 0].max() + pts[:, 0].min()) / 2, (pts[:, 1].max() + pts[:, 1].min()) / 2
    def proj(p):
        q = np.asarray(p) @ Rm.T; return np.column_stack([Wd / 2 + (q[:, 0] - mx) * sc, Ht / 2 - (q[:, 1] - my) * sc, q[:, 2]])
    yy = np.linspace(0, 1, Ht)[:, None, None]
    img = np.zeros((Ht, Wd, 3)) + (GROUND * (1.08 - 0.16 * yy) if ground is None else np.array(ground, float)); zb = np.full((Ht, Wd), -1e9)
    L = np.array([-0.40, 0.58, 0.71]); L /= np.linalg.norm(L); Hh = L + np.array([0, 0, 1.0]); Hh /= np.linalg.norm(Hh)
    L2 = np.array([0.6, -0.2, 0.5]); L2 /= np.linalg.norm(L2)
    def shade_gold(n):
        nv = Rm @ n; nv = nv if nv[2] >= 0 else -nv; d = max(0.0, nv @ L); d2_ = max(0.0, nv @ L2)
        env = 0.5 + 0.5 * abs(nv[1])                                  # metal: a sky-to-floor reflection by the normal's tilt
        col = GOLDC * (0.34 + 0.46 * d + 0.16 * d2_ + 0.22 * env)
        return np.clip(col + np.array([255, 232, 170]) * (0.20 * max(0.0, nv @ Hh) ** 16), 0, 255)
    def shade_stone(n, k, front=True):
        nv = Rm @ n; d = max(0.0, (nv if nv[2] >= 0 else -nv) @ L); base = np.array(STONE[k], float)
        sp = 0.30 * max(0.0, nv @ Hh) ** 40 if front else 0.0
        return np.clip(base * (0.55 + 0.55 * d) + 255 * sp, 0, 255)
    # 1. opaque: gold pieces and the core (the tetrahedron); gold sits a hair behind a stone face it touches
    opaque = [('g', n, poly) for pc in gold_pieces for n, poly in J.piece_faces(pc)] + [('b', n, poly) for _, n, poly, _ in extra_gold]
    if 'T' in stones: opaque += [('T', n, poly) for n, poly in stone_faces('T')]
    for lab, n, poly in opaque:
        col = shade_gold(n) if lab in 'gb' else shade_stone(n, 'T'); s = proj(poly)
        for ya, yb, xa, xb, m, z in tri_raster(s, Wd, Ht):
            z = z - (2e-3 if lab in 'gb' else 0.0)
            sub = zb[ya:yb + 1, xa:xb + 1]; put = m & (z > sub); sub[put] = z[put]; img[ya:yb + 1, xa:xb + 1][put] = col
    EW = max(2, int(Wpx / 700)) * SS
    offs = [(dx, dy) for dx in range(-EW // 2, EW // 2 + 1) for dy in range(-EW // 2, EW // 2 + 1) if dx * dx + dy * dy <= (EW / 2) ** 2]
    def edge_mask(segs, eps=0.02, thin=False):
        acc = np.zeros((Ht, Wd), bool); off = offs[::2] if thin else offs
        for a, b in segs:
            s = proj(np.array([a, b])); Ln = np.hypot(*(s[1, :2] - s[0, :2])); nn = max(2, int(Ln * 2))
            t = np.linspace(0, 1, nn)[:, None]; p = s[0] * (1 - t) + s[1] * t
            xi = np.clip(p[:, 0].astype(int), 0, Wd - 1); yi = np.clip(p[:, 1].astype(int), 0, Ht - 1); vis = p[:, 2] >= zb[yi, xi] - eps
            for dx, dy in off: acc[np.clip(yi[vis] + dy, 0, Ht - 1), np.clip(xi[vis] + dx, 0, Wd - 1)] = True
        return acc
    def segs_of(polys):
        E = {}
        for poly in polys:
            for a, b in zip(poly, np.roll(poly, -1, 0)): E.setdefault(tuple(sorted([tuple(np.round(a, 6)), tuple(np.round(b, 6))])), (a, b))
        return list(E.values())
    img[edge_mask(segs_of([p for lab, _, p in opaque if lab == 'g']))] = GOLD_EDGE          # gold edges dark (tinted by the shells later)
    if 'T' in stones: img[edge_mask(segs_of([p for lab, _, p in opaque if lab == 'T']))] = np.array([250, 214, 196.])
    # 2. see-through shells, exact order for nested convex shells: back faces outer to inner, then front faces inner to outer
    view = Rm[2]
    sh = [k for k in SHELLS if k in stones]
    passes = [(k, False) for k in sh] + [(k, True) for k in sh[::-1]]
    for k, front in passes:
        for n, poly in stone_faces(k):
            if (n @ view > 0) != front: continue
            col = shade_stone(n, k, front); al = (ALPHA_F if front else ALPHA_B)[k]; s = proj(poly)
            for ya, yb, xa, xb, m, z in tri_raster(s, Wd, Ht):
                sub = zb[ya:yb + 1, xa:xb + 1]; put = m & (z >= sub - 1e-3)
                blk = img[ya:yb + 1, xa:xb + 1]; blk[put] = blk[put] * (1 - al) + col * al
    # 3. shell edges, light in the stone's own colour: back edges faint, front (and outline) edges clear
    for k in sh:
        fs = stone_faces(k); base = np.array(STONE[k], float); light = np.clip(base * 1.25 + 40, 0, 255)
        E = {}
        for n, poly in fs:
            fr = n @ view > 0
            for a, b in zip(poly, np.roll(poly, -1, 0)):
                key = tuple(sorted([tuple(np.round(a, 6)), tuple(np.round(b, 6))])); E[key] = (a, b, E.get(key, (0, 0, False))[2] or fr)
        for fr in (False, True):
            m = edge_mask([(a, b) for a, b, f in E.values() if f == fr], eps=0.01, thin=not fr); w = 0.95 if fr else 0.40
            img[m] = img[m] * (1 - w) + light * w
    return Image.fromarray(img.clip(0, 255).astype(np.uint8)).resize((Wpx, Hpx), Image.LANCZOS)
def centre(pc): return np.mean([fl(p.verts).mean(0) for p in pc[1]], 0)
if MAIN:
    hO = float(PHI * PHI / 2)                                    # top corner of O at (0, 0, hO): the pendant hangs from it
    bail = J.hoop((0.0, 0.0, hO + 0.36), R=0.18, wy=0.07, th=0.035)
    Rm = look((0.80, -0.42, 0.36)) @ J.rot(2, np.radians(8))
    front = lambda pc: centre(pc) @ Rm[2] > 0
    kept = [pc for pc in gold if not front(pc)]
    print('COUNT panel (b) gold kept', J.count(kept), 'of', J.count(gold), flush=True)
    pw, ph = W // 3, int(W * 0.52)
    _p = np.vstack([fl(O)] + [p for _, _, p, _ in bail]) @ Rm.T
    SC = min(pw * 0.88 / np.ptp(_p[:, 0]), ph * 0.90 / np.ptp(_p[:, 1]))     # one scale for all three panels
    a = render(gold, Rm, pw, ph, extra_gold=bail, scale=SC); print('PROGRESS 0.40 panel a', flush=True)
    b = render(kept, Rm, pw, ph, extra_gold=bail, scale=SC); print('PROGRESS 0.65 panel b', flush=True)
    c = render([], Rm, pw, ph, extra_gold=bail, scale=SC); print('PROGRESS 0.85 panel c', flush=True)
    canvas = Image.new('RGB', (W, ph + int(W * 0.035)), tuple(int(x) for x in GROUND))
    labs = []
    for i, p in enumerate((a, b, c)):
        canvas.paste(p, (i * pw, 0)); labs.append((i * pw + int(W * 0.012), int(W * 0.008), '(' + 'abc'[i] + ')'))
    J.finish(canvas, labs, os.path.join(OUTD, 'nest-pendant.png'))
    print('PROGRESS 0.98 done', flush=True)
    print('FINAL ok' if not FAIL else 'FINAL FAIL: ' + '; '.join(FAIL))
