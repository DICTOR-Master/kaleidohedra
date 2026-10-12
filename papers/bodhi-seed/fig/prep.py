# Data for the Bodhi seed figures: solids and both kits (studies/2026-10-12-bodhi-pieces/data), each piece as hull triangles +
# feature edges; Diadem L/R told apart by the sign of the turn (det +1 or -1) taking a reference B5 onto each.
import json, itertools, os, numpy as np
from scipy.spatial import ConvexHull
D = os.path.expanduser('~/kaleidohedra/studies/2026-10-12-bodhi-pieces/data/')
S = json.load(open(D + 'bodhi-seed-solids.json')); KA = json.load(open(D + 'bodhi-kit-A-all-pieces.json')); KB = json.load(open(D + 'bodhi-kit-B-all-pieces.json'))
def poly(V):
    V = np.array(V, float); H = ConvexHull(V); eq = H.equations; tris = H.simplices.tolist()
    from collections import defaultdict
    adj = defaultdict(list)
    for t, (a, b, c) in enumerate(tris):
        for e in ((a, b), (b, c), (a, c)): adj[tuple(sorted(e))].append(t)
    ed = [list(e) for e, ts in adj.items() if len(ts) == 2 and np.linalg.norm(eq[ts[0], :3] - eq[ts[1], :3]) > 1e-6]
    return {'v': np.round(V, 6).tolist(), 't': tris, 'e': ed}
ref = np.array(KB['B5'][0], float); rc = ref - ref.mean(0)
def hand(W):
    W = np.array(W, float); wc = W - W.mean(0)
    for perm in itertools.permutations(range(len(W)), 3):
        A = rc[[0, 1, 2]].T; B = wc[list(perm)].T
        try: M = B @ np.linalg.inv(A)
        except np.linalg.LinAlgError: continue
        if np.allclose(M @ M.T, np.eye(3), atol=1e-6) and all(np.min(np.linalg.norm(wc - x, axis=1)) < 1e-6 for x in rc @ M.T):
            return 'L' if np.linalg.det(M) > 0 else 'R'
    return '?'
out = {'outer': poly(S['outer']), 'copies': [poly(c) for c in S['copies']], 'centre': poly(S['centre'])}
out['A'] = [[k, poly(W)] for k in KA for W in KA[k]]
out['B'] = [[('B5' + hand(W)) if k == 'B5' else k, poly(W)] for k in KB for W in KB[k]]
from collections import Counter; print(Counter(k for k, _ in out['B']))
json.dump(out, open(os.path.expanduser('~/kaleidohedra/papers/bodhi-seed/fig/bodhi-data.json'), 'w'), separators=(',', ':'))
