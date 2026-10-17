# DICTO 2026-10-17 night: "start with a dome construction shape of pents and hexagons, Goldberg polyhedra, as the top mesh and the opposite
# pattern at the bottom, then every scutoid has a clear path and a place in the group — flattened out"; "not mirrored: if the top is a hex the
# bottom is a pent" (and pent top -> hex bottom), "regular-ish hexes and pents", flat layer (nothing up or down), group tiles space.
# Group = m cells inside a hexagonal prism (the prisms tile space; layers stack straight). Cells = 3D Voronoi of m seeds at different heights,
# clipped by the prism walls and the slab 0 <= z <= h: convex, flat faces; neighbours swap part-way up (Y) because the heights differ.
# Start: seeds at the cell centres of the flattened Goldberg dome (truncated icosahedron about a hexagon, azimuthal-equidistant). Search:
# every cell reaches top and bottom, top sides in {5, 6}, bottom sides = 11 - top; then regular-ish top and bottom faces and chunky cells.
# Float arithmetic. -> data/scutoid-dome-group.txt, .json
import sys, json, numpy as np
from scipy.optimize import minimize, linprog
from scipy.spatial import HalfspaceIntersection, ConvexHull
src = open('scripts/scutoid_hexlayers_poly.py').read()
for name in ('clean', 'cheb', 'poly', 'area3', 'psi'):
    i = src.index(f'def {name}('); j = src.index('\ndef ', i + 1); exec(src[i:j])
exec(open('scripts/scutoid_dome_patterns.py').read().split("top = faces(dA)")[0])
ax = np.ones(3) / 3 ** .5; e1 = np.array([1, -1, 0]) / 2 ** .5; e2 = np.cross(ax, e1)
def flat(v):
    v = v / np.linalg.norm(v); th = np.arccos(np.clip(v @ ax, -1, 1)); a = np.arctan2(v @ e2, v @ e1); return th * np.array([np.cos(a), -np.sin(a)])
cen = np.array([np.degrees(np.arccos(np.clip(N[i] @ ax / np.linalg.norm(N[i]), -1, 1))) for i in range(32)])
DOME = [i for i in range(32) if cen[i] < 95]
XY0 = np.array([flat(N[i]) for i in DOME]); TOP0 = {k: (5 if G[i] == 'P' else 6) for k, i in enumerate(DOME)}

def polyside(P):
    # sides of a convex polygon, merging near-collinear corners
    n = len(P); c = 0
    for k in range(n):
        a = P[k] - P[k - 1]; b = P[(k + 1) % n] - P[k]
        if np.linalg.norm(np.cross(a, b)) > 1e-6 * np.linalg.norm(a) * np.linalg.norm(b): c += 1
    return c

def irregular(P):
    n = len(P); ang = []; L = []
    for k in range(n):
        a = P[k - 1] - P[k]; b = P[(k + 1) % n] - P[k]; L.append(np.linalg.norm(b))
        ang.append(np.degrees(np.arccos(np.clip(a @ b / np.linalg.norm(a) / np.linalg.norm(b), -1, 1))))
    return max(abs(x - 180 * (n - 2) / n) for x in ang) / 60 + (max(L) / min(L) - 1) / 2

def group(x, m):
    R, h = abs(x[0]), abs(x[1]) + 1e-6; S = np.array(x[2:2 + 3 * m]).reshape(m, 3); S[:, 2] *= h
    W = []
    for k in range(6):
        a = np.pi / 3 * k; W.append([np.cos(a), np.sin(a), 0])
    W = np.array(W); wb = np.full(6, R * 3 ** .5 / 2)   # hexagon, circumradius R, a flat edge facing each wall normal
    cells = []
    for k in range(m):
        s = S[k]; A = [S[j] - s for j in range(m) if j != k]; b = [(S[j] @ S[j] - s @ s) / 2 for j in range(m) if j != k]
        A = np.r_[np.array(A), W, [[0, 0, 1], [0, 0, -1]]]; b = np.r_[b, wb, h, 0]
        P = poly(A, b)
        if P is None: return None
        top = bot = None
        for f in P['faces']:
            if f[0][2] > 1 - 1e-9: top = f[2]
            elif f[0][2] < -1 + 1e-9: bot = f[2]
        cells.append(dict(P=P, top=top, bot=bot, nt=polyside(top) if top is not None else 0, nb=polyside(bot) if bot is not None else 0,
                          psi=psi(P['vol'], sum(area3(f[2]) for f in P['faces'])), vol=P['vol']))
    return dict(cells=cells, R=R, h=h, S=S)

def score(x, m, want):
    try: g = group(x, m)
    except Exception: return 50.0, None
    if g is None: return 50.0, None
    pen = 0.0; irr = 0.0
    for k, c in enumerate(g['cells']):
        if c['top'] is None or c['bot'] is None: pen += 3; continue
        if area3(c['top']) < 0.15 or area3(c['bot']) < 0.15: pen += 1
        nt, nb = c['nt'], c['nb']
        pen += abs(nt - want.get(k, nt)) * 0.5 if want else 0
        pen += (nt not in (5, 6)) + (nb not in (5, 6)) + abs(nt + nb - 11)
        irr = max(irr, irregular(c['top']), irregular(c['bot']))
    vols = [c['vol'] for c in g['cells']]; uneven = max(vols) / min(vols) - 1
    least = min(c['psi'] for c in g['cells'])
    return pen * 1.0 + 0.3 * irr + 0.3 * uneven - least, g

if __name__ == '__main__':
    tries = int(sys.argv[1]) if len(sys.argv) > 1 else 12; rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    m = len(DOME); out = ['DICTO · dictospheres.com', f'Flattened Goldberg dome group: {m} cells in a hexagonal prism; top = dome pattern, bottom = every cell swapped 5<->6 (float)']
    best = (1e9, None, None)
    for t in range(tries):
        sc = np.sqrt(m / (np.pi * (XY0 ** 2).sum(1).max())) * rng.uniform(.9, 1.1)   # dome spread to about area 1 per cell
        R0 = (2 * m / (3 * 3 ** .5)) ** .5
        x0 = np.r_[R0, rng.uniform(.8, 1.4), np.c_[XY0 * sc + rng.normal(0, .05, XY0.shape), rng.uniform(0, 1, m)].ravel()]
        want = TOP0 if t % 2 == 0 else {}
        f = lambda x: score(x, m, want)[0]
        r = minimize(f, x0, method='Powell', options=dict(maxfev=6000, xtol=1e-4, ftol=1e-6))
        v, g = score(r.x, m, want)
        line = None
        if g is not None:
            ok = all(c['top'] is not None and c['bot'] is not None and {c['nt'], c['nb']} == {5, 6} for c in g['cells'])
            line = dict(t=t, keep_dome_top=bool(want), valid=ok, value=float(v), least_psi=float(min(c['psi'] for c in g['cells'])),
                        sides=[(c['nt'], c['nb']) for c in g['cells']], R=float(g['R']), h=float(g['h']))
            print(json.dumps(line), flush=True)
            if ok and v < best[0]: best = (v, r.x, line)
    if best[1] is None: out.append('  no valid group found (every cell swapping 5<->6)')
    else:
        out.append(f"  best: least ψ {best[2]['least_psi']:.3f}, layer height {best[2]['h']:.3f}, hexagon circumradius {best[2]['R']:.3f} (cell area ≈ 1); sides (top, bottom) {best[2]['sides']}")
        json.dump(dict(x=list(map(float, best[1])), m=m, **best[2]), open('data/scutoid-dome-group.json', 'w'))
    print('\n'.join(out)); open('data/scutoid-dome-group.txt', 'w').write('\n'.join(out) + '\n')
