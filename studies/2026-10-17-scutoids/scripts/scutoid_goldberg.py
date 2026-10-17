# DICTO 2026-10-17: every scutoid "like a tall hexagonal prism with a pentagonal face at one end" (his Polyhedraverse Pentagon-to-UHex
# adaptor) and "close to a sphere" (each scutoid). The roundest such prism is about as tall as it is wide (hexagonal prism ψ ≈ 0.86),
# which needs ~150 cells round the shell: the Goldberg cage GP(4,0), 162 faces (12 pentagons + 150 hexagons), as the planes dual to the
# frequency-4 geodesic icosahedron. Search: one layer, inner cage = all planes at distance 1, outer cage = each Th-orbit of planes pushed
# by its own factor (overall growth about 1.28 for cells about as tall as wide). Keep the layers whose outer cage again has exactly 12
# pentagons and no other non-hexagons, with the pentagons MOVED (the 12 inner-pentagon cells become hexagons and 12 others pentagons).
# Then score every cell (sphericity, height/width). Float. -> data/scutoid-goldberg.txt / .json   (run on dicto-node)
import itertools, json, sys, numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
phi = (1 + 5 ** .5) / 2
def cyc(p): return [p, [p[1], p[2], p[0]], [p[2], p[0], p[1]]]
ICO = np.array([c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1, s2 * phi])], float)
F = [f for f in itertools.combinations(range(12), 3) if all(abs(np.linalg.norm(ICO[a] - ICO[b]) - 2) < 1e-9 for a, b in itertools.combinations(f, 2))]
assert len(F) == 20
def geodesic(n):
    P = []
    for a, b, c in F:
        for i in range(n + 1):
            for j in range(n + 1 - i):
                k = n - i - j; v = (i * ICO[a] + j * ICO[b] + k * ICO[c]) / n; P.append(v / np.linalg.norm(v))
    return np.unique(np.round(P, 9), axis=0)
FREQ = int(sys.argv[1]) if len(sys.argv) > 1 else 4
N = geodesic(FREQ); M = len(N); print('faces', M, flush=True)
# Th: cyclic permutations x sign changes
TH = [np.diag(s) @ np.eye(3)[list(p)] for p in ([0, 1, 2], [1, 2, 0], [2, 0, 1]) for s in itertools.product((1, -1), repeat=3)]
key = lambda v: tuple(np.round(v, 6)); idx = {key(v): i for i, v in enumerate(N)}
orbit = [-1] * M; orbits = []
for i in range(M):
    if orbit[i] >= 0: continue
    o = sorted({idx[key(g @ N[i])] for g in TH}); [orbit.__setitem__(j, len(orbits)) for j in o]; orbits.append(o)
pent = [i for i in range(M) if any(np.allclose(N[i], v / np.linalg.norm(v)) for v in ICO)]
print('Th orbits', [len(o) for o in orbits], 'pentagon orbit', orbit[pent[0]], flush=True)
def cage(d):
    V = np.unique(np.round(HalfspaceIntersection(np.c_[N, -d], np.zeros(3)).intersections, 9), axis=0)
    sides = np.array([(np.abs(V @ N[i] - d[i]) < 1e-7).sum() for i in range(M)]); return V, sides
d0 = np.ones(M); V0, s0 = cage(d0); assert (s0[pent] == 5).all() and (np.delete(s0, pent) == 6).all(), 'inner cage is not the Goldberg cage'
def cells(d0, d1):
    D = d1 - d0; out = []
    for i in range(M):
        r = D / D[i]; hs = np.vstack([np.r_[N[i], -d1[i]], np.r_[-N[i], d0[i]], np.c_[N - r[:, None] * N[i], -(d0 - r * d0[i])][np.arange(M) != i]])
        x0 = N[i] * (d0[i] + 0.5 * D[i])
        if not (hs[:, :3] @ x0 + hs[:, 3] < -1e-9).all(): out.append(None); continue
        out.append(np.unique(np.round(HalfspaceIntersection(hs, x0).intersections, 9), axis=0))
    return out
def psi(V): h = ConvexHull(V); return np.pi ** (1 / 3) * (6 * h.volume) ** (2 / 3) / h.area
rng = np.random.default_rng(7); keep = []
NS = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
for t in range(NS):
    g = rng.uniform(1.15, 1.45); f = rng.uniform(0.9, 1.12, len(orbits)); f[orbit[pent[0]]] = rng.uniform(0.85, 1.2)
    d1 = np.array([g * f[orbit[i]] for i in range(M)])
    if (d1 <= d0 + 0.02).any(): continue
    try: V1, s1 = cage(d1)
    except Exception: continue
    if (s1 == 0).any() or sorted(set(s1)) != [5, 6] or (s1 == 5).sum() != 12: continue
    newp = [i for i in range(M) if s1[i] == 5]
    if set(newp) & set(pent): continue
    keep.append(dict(g=g, f=f.round(4).tolist(), newp=newp))
    if len(keep) % 10 == 1: print('found', len(keep), 'at sample', t, flush=True)
print('layers with the 12 pentagons moved cleanly:', len(keep), 'of', NS, flush=True)
res = []
for k in keep[:60]:
    d1 = np.array([k['g'] * k['f'][orbit[i]] for i in range(M)]); C = cells(d0, d1)
    if any(c is None or len(c) < 4 for c in C): continue
    ps = [psi(c) for c in C]; hw = []
    for i, c in enumerate(C):
        top = c[np.abs(c @ N[i] - d1[i]) < 1e-7]; bot = c[np.abs(c @ N[i] - d0[i]) < 1e-7]
        w = np.ptp(np.r_[top, bot] - np.outer(np.r_[top, bot] @ N[i], N[i]), axis=0).max(); hw.append((d1[i] - d0[i]) / w)
    sc = [i for i in range(M) if (i in pent) or (i in k['newp'])]
    res.append(dict(k, least_psi=min(ps), scutoid_psi=(min(ps[i] for i in sc), max(ps[i] for i in sc)), hw=(min(hw), max(hw)), mean_psi=float(np.mean(ps))))
res.sort(key=lambda b: -b['least_psi'])
out = ['DICTO · dictospheres.com', f'Goldberg cage scutoid layer (frequency {FREQ}: {M} faces; 12 pentagons), the 12 pentagons moved to new cells (float)',
       f'  Th orbits of the faces: {[len(o) for o in orbits]}', f'  clean layers found: {len(keep)} of {NS} samples']
for b in res[:6]: out.append(f"  least ψ {b['least_psi']:.3f} (mean {b['mean_psi']:.3f}); the 24 scutoids ψ {b['scutoid_psi'][0]:.3f}-{b['scutoid_psi'][1]:.3f}; height/width {b['hw'][0]:.2f}-{b['hw'][1]:.2f}; growth {b['g']:.3f}")
out.append('  targets: hexagonal prism as tall as wide ψ ≈ 0.86; cube 0.806')
print('\n'.join(out), flush=True); open('data/scutoid-goldberg.txt', 'w').write('\n'.join(out) + '\n'); json.dump(res[:20], open('data/scutoid-goldberg.json', 'w'))
