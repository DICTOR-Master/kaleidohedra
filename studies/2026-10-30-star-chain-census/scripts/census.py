# Star Chain Census (DICTO 10-30: "have we done these steps with all newly discovered/identified solids?"). For every convex solid of the
# dataset DICTO Solids: Exact Geometry v5: centre it (mean of corners; flag if that is not a centre of symmetry), and for t = phi and t = 2
# run the star step of #78: spikes over the faces with tips at t times the foot of the perpendicular from the centre (flag a foot outside
# its face), hull of the tips, exact fill of both layers by corner pyramids and edge tetrahedra (by volume), and the star chain S0 -> S1 ->
# ... up to 8 steps, recording whether a shape repeats (period) and whether a hull has the shape of any solid of the dataset.
# Usage: ~/geom/bin/python scripts/census.py <dataset solids dir> <out.json>
import sys, os, json, glob, itertools, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
SOL, OUT = sys.argv[1], sys.argv[2]
def read_off(p):
    L = [l.split('#')[0].strip() for l in open(p)]; L = [l for l in L if l]
    assert L[0].upper().startswith('OFF'); n = int(L[1].split()[0]); return np.array([[float(x) for x in L[2 + i].split()[:3]] for i in range(n)])
def facelist(Q):
    hq = ConvexHull(Q); V = Q[hq.vertices]; out = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = (eq, [i for i, p in enumerate(V) if abs(eq[:3] @ p + eq[3]) < 1e-7 * max(1, np.abs(V).max())])
    return V, list(out.values())
def shape(V):
    W = V / np.linalg.norm(V, axis=1).max(); d = np.linalg.norm(W[:, None] - W[None], axis=2); m = d[d > 1e-9].min()
    return (len(W), tuple(sorted({round(x, 4) for x in d[(d > 1e-9) & (d < 1.7 * m)].ravel()})), tuple(sorted({round(x, 5) for x in np.linalg.norm(W, axis=1)})))
def in_face(p, Vf, n):
    c = Vf.mean(0); a = Vf[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
    ang = np.arctan2((Vf - c) @ b, (Vf - c) @ a); R = Vf[np.argsort(ang)]
    q = p - c; sgn = [np.cross(R[i] - c, R[(i + 1) % len(R)] - c) @ n for i in range(len(R))]
    return all(np.cross(R[i] - p, R[(i + 1) % len(R)] - p) @ n >= -1e-9 for i in range(len(R)))
def step(V0, t):
    V, FL = facelist(V0); vol = lambda Q: ConvexHull(Q).volume
    tips = [t * (-eq[3]) * eq[:3] for eq, _ in FL]; TP = np.array(tips)
    feet_inside = all(in_face(-eq[3] * eq[:3], V[ids], eq[:3]) for eq, ids in FL)
    fa = {v: [fi for fi, (_, ids) in enumerate(FL) if v in ids] for v in range(len(V))}
    def is_edge(a, b):
        fs = [fi for fi in fa[a] if fi in fa[b]]
        if len(fs) != 2: return False
        m = (V[a] + V[b]) / 2; return all(abs(FL[f][0][:3] @ m + FL[f][0][3]) < 1e-7 * max(1, np.abs(V).max()) for f in fs)
    E = [e for e in itertools.combinations(range(len(V)), 2) if is_edge(*e)]
    try:
        star = vol(V) + sum(vol(np.vstack([V[ids], tips[fi]])) for fi, (_, ids) in enumerate(FL)); VH = vol(TP)
        L1 = sum(vol(np.vstack([V[v]] + [tips[f] for f in fa[v]])) for v in range(len(V))) + sum(vol(np.vstack([V[a], V[b]] + [tips[f] for f in fa[a] if f in fa[b]])) for a, b in E)
        L2 = sum(vol(np.vstack([t * V[v]] + [tips[f] for f in fa[v]])) for v in range(len(V))) + sum(vol(np.vstack([t * V[a], t * V[b]] + [tips[f] for f in fa[a] if f in fa[b]])) for a, b in E)
        ok1 = abs(L1 - (VH - star)) < 1e-7 * VH; ok2 = abs(L2 - (t ** 3 * vol(V) - VH)) < 1e-7 * VH
        star_in = bool(np.all(np.vstack([V] + tips) @ np.array([eq[:3] for eq in ConvexHull(TP).equations]).T + np.array([eq[3] for eq in ConvexHull(TP).equations]) <= 1e-7 * np.abs(TP).max()))
    except Exception as ex:
        return TP, dict(error=str(ex)[:120], feet_inside=feet_inside)
    return TP, dict(corners=len(V), faces=len(FL), feet_inside=feet_inside, star_over=round(star / vol(V), 6), hull_over=round(VH / vol(V), 6),
                    star_inside_hull=star_in, layer1_exact=bool(ok1), layer2_exact=bool(ok2))
solids = []
for js in sorted(glob.glob(os.path.join(SOL, '*.json'))):
    m = json.load(open(js)); off = js[:-5] + '.off'
    if not m.get('convex') or not os.path.exists(off): continue
    V = read_off(off); c = V.mean(0); V = V - c
    solids.append((m.get('name', os.path.basename(js)), os.path.basename(off), V))
lib = {shape(ConvexHull(V).points[ConvexHull(V).vertices]): n for n, _, V in solids}
res = []
for name, f, V in solids:
    row = dict(name=name, file=f, corners=len(ConvexHull(V).vertices))
    # centre of symmetry check: reflection through the centre maps the corner set to itself
    W = V[ConvexHull(V).vertices]; row['centrally_symmetric'] = bool(all(np.min(np.linalg.norm(W + w, axis=1)) < 1e-7 * np.abs(W).max() for w in W))
    for tn, t in [('phi', phi), ('2', 2.0)]:
        S = V; chain = []; shapes = [shape(W)]; period = None
        for n in range(8):
            try: S2, info = step(S, t)
            except Exception as ex: chain.append(dict(error=str(ex)[:120])); break
            sh = shape(S2[ConvexHull(S2).vertices]); info['hull_shape_is'] = lib.get(sh); info['repeats_step'] = [k for k, s0 in enumerate(shapes) if s0 == sh]
            chain.append(info); shapes.append(sh)
            if info['repeats_step'] and period is None: period = (n + 1) - info['repeats_step'][0]; break
            S = S2
        row[tn] = dict(period=period, steps=chain)
    res.append(row); print(name, row['corners'], 'sym' if row['centrally_symmetric'] else 'NOSYM', 'phi period', row['phi']['period'], '2 period', row['2']['period'],
                       'L ok', all(s.get('layer1_exact') and s.get('layer2_exact') for s in row['phi']['steps']), flush=True)
    json.dump(res, open(OUT, 'w'), indent=1, default=str)
