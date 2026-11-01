# Kagemusha with DICTO's notch pieces (kagemusha_variants.py), the star after step three: (1) the core-turn sequence of paper B (core =
# intersection of the hulls of the tips of each face family; turn factor t), up to 8 turns, its period (shape up to scale, 1e-6); (2) the
# star itself: corners, faces after merging coplanar neighbours (by sides), symmetry order (orthogonal maps fixing the corner set, 1e-6),
# compared with every solid of DICTO Solids v7 by corner and face counts and, where these agree, by sorted scaled distance lists.
# Kuwagata t = 2 (the star that stops at step three) and, as a cheap extra, Maedate t = 2.
# Float64: the cut-back heights come from bisection (2^-30), so exact Q(sqrt5) identification is not available for these stars.
# Usage: kuwagata_cycle.py <dataset dir> <star-cores.json> <out dir>
import json, os, sys, glob, itertools, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kagemusha_variants as KV
from star_core import core_of, shape, faces_info
from scipy.spatial import ConvexHull
DS, SC, OUT = sys.argv[1:4]
def hull_faces(C):
    CH = ConvexHull(C); CF = []
    for eq in CH.equations:
        ids = [i for i, p in enumerate(C) if abs(eq[:3] @ p + eq[3]) < 1e-8]
        c0 = C[ids].mean(0); u = C[ids[0]] - c0; w = np.cross(eq[:3], u)
        CF.append([i for _, i in sorted((np.arctan2((C[i] - c0) @ w, (C[i] - c0) @ u), i) for i in ids)])
    return [list(x) for x in {tuple(sorted(f)): f for f in CF}.values()]
def sym_order(P, tol=1e-6):
    P = P - P.mean(0); r = np.linalg.norm(P, axis=1); i1 = int(np.argmax(r)); R = r[i1]
    same = [i for i in range(len(P)) if abs(r[i] - R) < tol]
    i2 = next(i for i in same if np.linalg.norm(np.cross(P[i1], P[i])) > 1e-3)
    d12 = np.linalg.norm(P[i1] - P[i2]); B = np.array([P[i1], P[i2], np.cross(P[i1], P[i2])])
    n = 0
    for a in same:
        for b in same:
            if a == b or abs(np.linalg.norm(P[a] - P[b]) - d12) > tol: continue
            for sgn in (1, -1):
                C = np.array([P[a], P[b], sgn * np.cross(P[a], P[b])]); M = np.linalg.solve(B, C)
                if not np.allclose(M @ M.T, np.eye(3), atol=1e-6): continue
                Q = P @ M
                if all(np.min(np.linalg.norm(P - q, axis=1)) < tol for q in Q): n += 1
    return n
def faces_merged(V, F):
    FI = faces_info(V, F); key = lambda i: tuple(np.round(np.append(FI[i][1], FI[i][2]), 6))
    E = {}
    for i, f in enumerate(F):
        for k in range(len(f)): E.setdefault(tuple(sorted((f[k], f[(k + 1) % len(f)]))), []).append(i)
    par = list(range(len(F)))
    def fd(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e, (i, j) in ((e, l) for e, l in E.items() if len(l) == 2):
        if key(i) == key(j): par[fd(i)] = fd(j)
    groups = {}
    for i in range(len(F)): groups.setdefault(fd(i), []).append(i)
    sides = {}
    for g in groups.values():
        ec = {}
        for i in g:
            f = F[i]
            for k in range(len(f)): e = tuple(sorted((f[k], f[(k + 1) % len(f)]))); ec[e] = ec.get(e, 0) + 1
        corners = {v for e, c in ec.items() if c == 1 for v in e}
        # count true corners: boundary vertices where the boundary turns
        bd = [e for e, c in ec.items() if c == 1]; nb = {}
        for a, b in bd: nb.setdefault(a, []).append(b); nb.setdefault(b, []).append(a)
        turn = sum(1 for v, l in nb.items() if len(l) == 2 and np.linalg.norm(np.cross(V[l[0]] - V[v], V[l[1]] - V[v])) > 1e-9 * np.linalg.norm(V[l[0]] - V[v]) * np.linalg.norm(V[l[1]] - V[v]))
        sides[turn] = sides.get(turn, 0) + 1
    return len(groups), dict(sorted(sides.items()))
def dists(P):
    P = P - P.mean(0); D = np.linalg.norm(P[:, None] - P[None], axis=2); return np.sort(D[np.triu_indices(len(P), 1)]) / D.max()
out = {}
for variant in ('sloping',):
    r = KV.run(variant, 2.0); V = np.array(r['final']['V']); F = r['final']['F']
    used = sorted({v for f in F for v in f}); remap = {v: i for i, v in enumerate(used)}; V = V[used]; F = [[remap[v] for v in f] for f in F]
    nplanes, sides = faces_merged(V, F)
    res = dict(volume_steps=[s['volume_over_last'] for s in r['steps']], corners=len(V), faces_built=len(F), faces=nplanes, faces_by_sides=sides,
               symmetry_order=sym_order(V))
    # dataset comparison
    matches = []
    dv = dists(V)
    for fn in glob.glob(os.path.join(DS, 'solids', '*.json')):
        d = json.load(open(fn))
        if len(d['vertices']) != len(V): continue
        P = np.array([[float(x) for x in v['decimal']] for v in d['vertices']])
        same_f = len(d['faces']) == nplanes
        matches.append(dict(file=os.path.basename(fn), faces=len(d['faces']), similar=bool(same_f and np.allclose(dists(P), dv, atol=1e-6))))
    res['dataset_same_corner_count'] = matches
    # core-turn sequence
    seq = []; C, Fc = V, F
    for k in range(8):
        C2, nf = core_of(C, Fc, 2.0)
        if C2 is None: seq.append(dict(turn=k + 1, core=None, families=nf)); break
        sh = shape(C2); seq.append(dict(turn=k + 1, families=nf, corners=sh['V'], faces=sh['faces'], radii=sh['radii'][:6], edges=sh['edges'][:6]))
        C, Fc = C2, hull_faces(C2)
    shapes = [json.dumps({k: s.get(k) for k in ('corners', 'faces', 'radii', 'edges')}) for s in seq if s.get('core') is not False and 'corners' in s]
    per = None
    for i in range(len(shapes)):
        for j in range(i):
            if shapes[i] == shapes[j]: per = (j + 1, i - j); break
        if per: break
    res['core_sequence'] = seq; res['core_period'] = dict(first_turn=per[0], period=per[1]) if per else None
    out[variant] = res; print(variant, {k: v for k, v in res.items() if k not in ('core_sequence', 'dataset_same_corner_count')}, 'dataset same corner count', len(matches), 'similar', sum(m['similar'] for m in matches), flush=True)
    for s in seq: print('   ', s, flush=True)
json.dump(out, open(os.path.join(OUT, 'kuwagata-cycle-exactflat.json'), 'w'), indent=1, default=float)
