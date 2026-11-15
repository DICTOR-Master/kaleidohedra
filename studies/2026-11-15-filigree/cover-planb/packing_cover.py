# packing_cover.py (15 Nov 2026) - DICTO · dictospheres.com
# Plan-B cover picture for The Platonic Solids: the nest of #99 in its place in the packing. One cube of the octet (the face-centred
# cubic cell, side 2 in lattice units, corners of the octet at the integer points with even sum) is exactly one whole octahedron at its
# centre, eight whole tetrahedra (one in each eighth of the cube) and twelve quarter octahedra along its edges (8 = 4/3 + 8/3 + 12/3).
# Every octahedron of the octet holds the nest O > I > D > C > T, and every tetrahedron the same nest at half size through its midpoint
# octahedron (#99, Theorem 1). Drawn: the central octahedron's nest with its gold (the 58 pieces of Chapter 10's nest pendant; the
# gold pieces whose centres lie in front of the nest's centre left out), the eight tetrahedra as red see-through crystal, each holding
# its half-size nest (stones only), the twelve quarter octahedra as yellow see-through crystal; the cells nearest the viewer (the
# tetrahedron in the front eighth and the three quarter octahedra on the edges at the front corner) left out so the centre shows.
# Pieces: ../scripts/render_nest.py (exact nest in Q(sqrt5), checks run at import); lattice unit u = phi^2/2 (the octahedron's
# corners at distance u from its centre). Usage: packing_cover.py OUT.png [width height]  -> X lines, FINAL ok / FINAL FAIL
import sys, os, itertools, numpy as np
from fractions import Fraction as Fr
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
import render_nest as N
J = N.J; fl = N.fl
OUT = sys.argv[1]; Wpx = int(sys.argv[2]) if len(sys.argv) > 2 else 2400; Hpx = int(sys.argv[3]) if len(sys.argv) > 3 else 2200
FAIL = list(N.FAIL)
def X(name, ok, detail=''):
    print(('X PASS ' if ok else 'X FAIL ') + name + (f': {detail}' if detail != '' else ''), flush=True)
    if not ok: FAIL.append(name)
# ------------------------------------------------------------------ the cube of the octet (integers)
E3 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
cen0 = (1, 1, 1)
octa = lambda c: [tuple(c[k] + s * e[k] for k in range(3)) for e in E3 for s in (1, -1)]
tets = [[tuple(a[k] + d[k] for k in range(3)) for d in itertools.product((0, 1), repeat=3) if (sum(a) + sum(d)) % 2 == 0]
        for a in itertools.product((0, 1), repeat=3)]
edge_c = [c for c in itertools.product((0, 1, 2), repeat=3) if sorted(c).count(1) == 1 and sum(c) % 2 == 1]
quarters = []
for c in edge_c:
    ax = c.index(1); inward = [(k, 1 if c[k] == 0 else -1) for k in range(3) if k != ax]
    quarters.append((c, [v for v in octa(c) if all((v[k] - c[k]) * s >= 0 for k, s in inward)]))
def vol(P):
    a, b, c, d = [np.array(p, dtype=object) for p in P]
    m = [[Fr(int(x)) for x in b - a], [Fr(int(x)) for x in c - a], [Fr(int(x)) for x in d - a]]
    det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    return abs(det) / 6
X('cube of the octet: 1 octahedron + 8 tetrahedra + 12 quarter octahedra (each a tetrahedron of 4 corners)',
  len(tets) == 8 and len(quarters) == 12 and all(len(q) == 4 for _, q in quarters))
X('volumes add up exactly to the cube, 8 = 4/3 + 8 x 1/3 + 12 x 1/3',
  Fr(4, 3) + sum(vol(t) for t in tets) + sum(vol(q) for _, q in quarters) == 8 and all(vol(t) == Fr(1, 3) for t in tets))
X('every tetrahedron has edge sqrt2 (the octahedron\'s) and its midpoint octahedron is axis-parallel, radius 1/2, about its centroid',
  all(all(sum((a[k] - b[k]) ** 2 for k in range(3)) == 2 for a, b in itertools.combinations(t, 2)) for t in tets)
  and all(sorted(tuple(Fr(a[k] + b[k], 2) - Fr(sum(v[k] for v in t), 4) for k in range(3)) for a, b in itertools.combinations(t, 2))
          == sorted(tuple(Fr(s, 2) * e[k] for k in range(3)) for e in E3 for s in (1, -1)) for t in tets))
u = float(N.PHI * N.PHI / 2)
P3 = lambda p: (np.array(p, float) - np.array(cen0, float)) * u
# ------------------------------------------------------------------ view and what is left out
Rm = N.look((0.80, -0.42, 0.36)) @ J.rot(2, np.radians(8)); vz = Rm[2]
front_corner = max(itertools.product((0, 2), repeat=3), key=lambda c: P3(c) @ vz)
tet_drawn = [t for t in tets if not all(abs(v[k] - front_corner[k]) <= 1 for v in t for k in range(3))]
q_drawn = [(c, q) for c, q in quarters if sum(abs(c[k] - front_corner[k]) for k in range(3)) != 1]
print('front corner', front_corner, '; tetrahedra drawn', len(tet_drawn), '; quarter octahedra drawn', len(q_drawn), flush=True)
X('left out: the front tetrahedron and the three quarter octahedra at the front corner', len(tet_drawn) == 7 and len(q_drawn) == 9)
kept = [pc for pc in N.gold if N.centre(pc) @ vz <= 0]
# ------------------------------------------------------------------ painting (as render_nest.render, for many cells)
STONE = J.STONE; GOLDC = np.array([212, 160, 52.]); GOLD_EDGE = np.array([92, 64, 18.]); GROUND = np.array([20, 15, 11.])
def hull_faces(pts): return [(n, poly) for n, o, poly in J.hull_faces(np.asarray(pts, float))]
nest_faces = {k: N.stone_faces(k) for k in 'OIDCT'}
def nest(cpos, s, alpha_scale):
    return [(k, [(n, poly * s + cpos) for n, poly in nest_faces[k]], alpha_scale) for k in 'OIDC']
cells = []                                                      # (centre, [(stone key, faces, alpha scale)] outer to inner)
cells.append((np.zeros(3), nest(np.zeros(3), 1.0, 1.0)))
opaque = [('g', n, poly) for pc in kept for n, poly in J.piece_faces(pc)] + [('T', n, poly) for n, poly in nest_faces['T']]
for t in tet_drawn:
    c = P3(np.mean(np.array(t, float), 0))
    cells.append((c, [('Tc', hull_faces([P3(v) for v in t]), 0.8)] + nest(c, 0.5, 0.8)))
    opaque += [('T', n, poly * 0.5 + c) for n, poly in nest_faces['T']]
for cq, q in q_drawn:
    cells.append((P3(np.mean(np.array(q, float), 0)), [('Oc', hull_faces([P3(v) for v in q]), 0.8)]))
ALPHA_F = {'O': 0.09, 'I': 0.15, 'D': 0.17, 'C': 0.17, 'Tc': 0.10, 'Oc': 0.10}; ALPHA_B = {'O': 0.04, 'I': 0.06, 'D': 0.07, 'C': 0.08, 'Tc': 0.05, 'Oc': 0.05}
COL = dict(STONE); COL['Tc'] = STONE['T']; COL['Oc'] = STONE['O']
SS = 3; Wd, Ht = Wpx * SS, Hpx * SS
allp = np.vstack([P3(c) for c in itertools.product((0, 2), repeat=3)]) @ Rm.T
sc = min(Wd * 0.90 / np.ptp(allp[:, 0]), Ht * 0.92 / np.ptp(allp[:, 1]))
mx, my = (allp[:, 0].max() + allp[:, 0].min()) / 2, (allp[:, 1].max() + allp[:, 1].min()) / 2
def proj(p):
    q = np.asarray(p) @ Rm.T; return np.column_stack([Wd / 2 + (q[:, 0] - mx) * sc, Ht / 2 - (q[:, 1] - my) * sc, q[:, 2]])
img = np.zeros((Ht, Wd, 3)) + GROUND; zb = np.full((Ht, Wd), -1e9)
L = np.array([-0.40, 0.58, 0.71]); L /= np.linalg.norm(L); Hh = L + np.array([0, 0, 1.0]); Hh /= np.linalg.norm(Hh)
L2 = np.array([0.6, -0.2, 0.5]); L2 /= np.linalg.norm(L2)
def shade_gold(n):
    nv = Rm @ n; nv = nv if nv[2] >= 0 else -nv; d = max(0.0, nv @ L); d2_ = max(0.0, nv @ L2); env = 0.5 + 0.5 * abs(nv[1])
    return np.clip(GOLDC * (0.34 + 0.46 * d + 0.16 * d2_ + 0.22 * env) + np.array([255, 232, 170]) * (0.20 * max(0.0, nv @ Hh) ** 16), 0, 255)
def shade_stone(n, k, front=True):
    nv = Rm @ n; d = max(0.0, (nv if nv[2] >= 0 else -nv) @ L); base = np.array(COL[k], float)
    return np.clip(base * (0.55 + 0.55 * d) + (255 * 0.30 * max(0.0, nv @ Hh) ** 40 if front else 0.0), 0, 255)
for lab, n, poly in opaque:
    col = shade_gold(n) if lab == 'g' else shade_stone(n, 'T')
    for ya, yb, xa, xb, m, z in N.tri_raster(proj(poly), Wd, Ht):
        z = z - (2e-3 if lab == 'g' else 0.0); sub = zb[ya:yb + 1, xa:xb + 1]; put = m & (z > sub); sub[put] = z[put]; img[ya:yb + 1, xa:xb + 1][put] = col
EW = max(2, int(Wpx / 700)) * SS
offs = [(dx, dy) for dx in range(-EW // 2, EW // 2 + 1) for dy in range(-EW // 2, EW // 2 + 1) if dx * dx + dy * dy <= (EW / 2) ** 2]
def edge_mask(segs, eps=0.02, thin=False):
    acc = np.zeros((Ht, Wd), bool); off = offs[::2] if thin else offs
    for a, b in segs:
        s = proj(np.array([a, b])); nn = max(2, int(np.hypot(*(s[1, :2] - s[0, :2])) * 2))
        t = np.linspace(0, 1, nn)[:, None]; p = s[0] * (1 - t) + s[1] * t
        xi = np.clip(p[:, 0].astype(int), 0, Wd - 1); yi = np.clip(p[:, 1].astype(int), 0, Ht - 1); vis = p[:, 2] >= zb[yi, xi] - eps
        for dx, dy in off: acc[np.clip(yi[vis] + dy, 0, Ht - 1), np.clip(xi[vis] + dx, 0, Wd - 1)] = True
    return acc
def segs_of(polys):
    E = {}
    for poly in polys:
        for a, b in zip(poly, np.roll(poly, -1, 0)): E.setdefault(tuple(sorted([tuple(np.round(a, 6)), tuple(np.round(b, 6))])), (a, b))
    return list(E.values())
img[edge_mask(segs_of([p for lab, _, p in opaque if lab == 'g']))] = GOLD_EDGE
img[edge_mask(segs_of([p for lab, _, p in opaque if lab == 'T']), thin=True)] = np.array([250, 214, 196.])
# see-through: cells far to near; inside a cell, back faces outer to inner, then front faces inner to outer (exact for nested shells)
cells.sort(key=lambda c: c[0] @ vz)
for cpos, shells in cells:
    for (k, fs, asc), front in [(sh, False) for sh in shells] + [(sh, True) for sh in shells[::-1]]:
        for n, poly in fs:
            if (n @ vz > 0) != front: continue
            col = shade_stone(n, k, front); al = (ALPHA_F if front else ALPHA_B)[k] * asc
            for ya, yb, xa, xb, m, z in N.tri_raster(proj(poly), Wd, Ht):
                sub = zb[ya:yb + 1, xa:xb + 1]; put = m & (z >= sub - 1e-3); blk = img[ya:yb + 1, xa:xb + 1]; blk[put] = blk[put] * (1 - al) + col * al
for cpos, shells in cells:                                      # edges, light in each stone's colour: back faint, front clear
    for k, fs, asc in shells:
        light = np.clip(np.array(COL[k], float) * 1.25 + 40, 0, 255); E = {}
        for n, poly in fs:
            fr = n @ vz > 0
            for a, b in zip(poly, np.roll(poly, -1, 0)):
                key = tuple(sorted([tuple(np.round(a, 6)), tuple(np.round(b, 6))])); E[key] = (a, b, E.get(key, (0, 0, False))[2] or fr)
        small = asc < 1 and k not in ('Tc', 'Oc')
        for fr in (False, True):
            m = edge_mask([(a, b) for a, b, f in E.values() if f == fr], eps=0.01, thin=(not fr) or small)
            w = (0.95 if fr else 0.40) * (0.75 if small else 1.0); img[m] = img[m] * (1 - w) + light * w
Image.fromarray(img.clip(0, 255).astype(np.uint8)).resize((Wpx, Hpx), Image.LANCZOS).save(OUT)
print('saved', OUT, (Wpx, Hpx), flush=True)
print('FINAL ok' if not FAIL else 'FINAL FAIL: ' + '; '.join(FAIL))
