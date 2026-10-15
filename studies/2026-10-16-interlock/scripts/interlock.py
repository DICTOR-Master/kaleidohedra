# Interlock step 2 (run on dicto-node, ~/plotenv): the common refinement of the two cycles. Every piece P of the original turn
# (cone cut, convex) is intersected with every piece Q of the flipped cycle (turns 0 and 1, which together cover the original turn
# exactly in the ends setting). Each nonempty P ∩ Q is convex and lies in one layer of each cycle: the interlock pieces.
# Checks: for every P, the volumes of its parts add back to vol(P); kinds counted by symmetry orbit (geomcheck).
import json, sys, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else '../_lib'); import geomcheck as gc
p3 = ((1 + 5 ** .5) / 2) ** 3
SET = sys.argv[2] if len(sys.argv) > 2 else 'ends'          # 'middle': rho^2 = 3 phi^2/4, the flipped cycle x3, turns -1 and 0 cover ours
K, TURNS = (1.0, (0, 1)) if SET == 'ends' else (3.0, (-1, 0))
OP = json.load(open('data/orig-pieces.json')); FP = json.load(open('data/flip-ends-pieces.json'))
C = {n: np.array(V) for n, V in json.load(open('data/orig-chain.json'))}
G = gc.group(gc.icosa_axes(C['icosahedron']))
orig = [(li, k, np.array(V)) for li, (lay, L) in enumerate(OP.items()) for k, V in enumerate(L)]
flip = [(t, li, k, np.array(V) * K * p3 ** t) for t in TURNS for li, (lay, L) in enumerate(FP.items()) for k, V in enumerate(L)]
def hs(V): return ConvexHull(V).equations                     # n.x + d <= 0 inside
def meet(A, B):
    H = np.vstack([A, B]); nrm = np.linalg.norm(H[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if r.status != 0 or r.x[3] < 1e-7: return None
    V = HalfspaceIntersection(H, r.x[:3]).intersections; V = np.unique(np.round(V, 10), axis=0)
    return V if len(V) >= 4 and ConvexHull(V).volume > 1e-11 else None
Of = [(li, k, V, hs(V), V.mean(0), np.linalg.norm(V - V.mean(0), axis=1).max(), ConvexHull(V).volume) for li, k, V in orig]
Ff = [(t, li, k, V, hs(V), V.mean(0), np.linalg.norm(V - V.mean(0), axis=1).max()) for t, li, k, V in flip]
pieces, worst = [], 0.0
for oi, (li, k, V, Ho, c, r, vol) in enumerate(Of):
    s = 0.0
    for t, lj, kk, W, Hf, cf, rf in Ff:
        if np.linalg.norm(c - cf) > r + rf + 1e-9: continue
        X = meet(Ho, Hf)
        if X is None: continue
        v = ConvexHull(X).volume; s += v; pieces.append({'o': [li, k], 'f': [t, lj, kk], 'v': X.tolist(), 'vol': v})
    worst = max(worst, abs(s - vol) / vol)
    if oi % 40 == 0: print('orig piece', oi, 'of', len(Of), 'parts so far', len(pieces), flush=True)
kinds = gc.kinds([np.array(q['v']) for q in pieces], G)
out = [f'interlock ({SET} setting): {len(pieces)} pieces from {len(Of)} original pieces x {len(Ff)} flipped pieces',
       f'check: every original piece is the sum of its parts, worst relative error {worst:.2e}',
       f'kinds by symmetry orbit: {len(kinds)}; counts {sorted((c for c, _ in kinds), reverse=True)}']
by = {}
for q in pieces: by.setdefault((q['o'][0], q['f'][0], q['f'][1]), 0); by[(q['o'][0], q['f'][0], q['f'][1])] += 1
out.append('pieces per (original layer, flipped turn, flipped layer): ' + ', '.join(f'{k}: {v}' for k, v in sorted(by.items())))
print('\n'.join(out)); open(f'data/interlock-{SET}.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'pieces': pieces, 'orig_layers': list(OP), 'flip_layers': list(FP)}, open(f'data/interlock-{SET}.json', 'w'))
