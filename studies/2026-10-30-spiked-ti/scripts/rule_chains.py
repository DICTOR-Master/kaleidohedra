# TI Star: follow DICTO's growth rule (each corner gives a face plane of the next) from TI, from the icosahedron Ip of the pentagon
# tips and from the dodecahedron Dh of the hexagon tips, for six steps each, and place every solid of the chains among the solids of
# the turn and of the next turn (scaled by s): inside / outside / touching (corners on faces).
import json, itertools, os, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
h = ConvexHull(P); F = []; seen = set()
for eq in h.equations:
    k = tuple(np.round(eq, 7))
    if k in seen: continue
    seen.add(k); F.append([i for i, p in enumerate(P) if abs(eq[:3] @ p + eq[3]) < 1e-8])
VT = h.volume
def grow(Q):
    V = Q[ConvexHull(Q).vertices]; r = np.linalg.norm(V, axis=1)
    W = HalfspaceIntersection(np.hstack([V / r[:, None], -r[:, None]]), np.zeros(3)).intersections; return W[ConvexHull(W).vertices]
def planes(Q):
    hq = ConvexHull(Q); u = {}
    for eq in hq.equations: u.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(u.values()))
def kind(Q):
    V = Q[ConvexHull(Q).vertices]; c = {}
    for eq in planes(Q):
        n = sum(1 for p in V if abs(eq[:3] @ p + eq[3]) < 1e-7); c[n] = c.get(n, 0) + 1
    return f"{len(V)} corners {dict(sorted(c.items()))}"
def rel(A, B):
    pb = planes(B); d = A @ pb[:, :3].T + pb[:, 3]
    if np.all(d <= 1e-9): return 'inside' + (' (touching)' if np.any(np.abs(d) < 1e-9) else '')
    pa = planes(A); d2 = B @ pa[:, :3].T + pa[:, 3]
    if np.all(d2 <= 1e-9): return 'contains' + (' (touching)' if np.any(np.abs(d2) < 1e-9) else '')
    return 'crosses'
out = {}
for SCN, s in [('phi', phi), ('2', 2.0)]:
    tip = [s * P[f].mean(0) for f in F]
    pen = np.array([t for t, f in zip(tip, F) if len(f) == 5]); hexa = np.array([t for t, f in zip(tip, F) if len(f) == 6])
    core = HalfspaceIntersection(np.vstack([planes(pen), planes(hexa)]), np.zeros(3)).intersections; core = core[ConvexHull(core).vertices]
    turn = {'TI': P, 'core': core, 'Ip': pen, 'Dh': hexa, 'K': np.vstack([pen, hexa]), 's·TI': s * P}
    ref = dict(turn); ref.update({k + ' (next turn)': v * s for k, v in turn.items() if k != 'TI'})
    chains = {}
    for start in ['TI', 'Ip', 'Dh']:
        Q = turn[start]; rows = []
        for step in range(1, 7):
            G = grow(Q); g = ConvexHull(G).volume / VT
            lin = (ConvexHull(G).volume / ConvexHull(Q).volume) ** (1 / 3)
            # the solid two steps back, scaled, to measure the factor per two steps
            rows.append(dict(step=step, solid=kind(G), volume_over_TI=round(g, 6),
                             relations={k: rel(G, v) for k, v in ref.items()}))
            Q = G
        two = (ConvexHull(grow(grow(turn[start]))).volume / ConvexHull(turn[start]).volume) ** (1 / 3)
        chains[start] = dict(linear_factor_per_two_steps=round(two, 9), steps=rows)
    out[SCN] = chains
json.dump(out, open('data/rule-chains.json', 'w'), indent=1, ensure_ascii=False)
for SCN, ch in out.items():
    print('== s =', SCN)
    for st, c in ch.items():
        print(' from', st, 'factor per two steps', c['linear_factor_per_two_steps'])
        for r in c['steps'][:3]:
            inside = [k for k, v in r['relations'].items() if v.startswith('inside')]; cont = [k for k, v in r['relations'].items() if v.startswith('contains')]
            touch = [k for k, v in r['relations'].items() if 'touching' in v]
            print('   step', r['step'], r['solid'], r['volume_over_TI'], '| inside', inside[:3], '| contains', cont, '| touching', touch)
