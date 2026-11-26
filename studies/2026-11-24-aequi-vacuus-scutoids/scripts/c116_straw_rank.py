"""Hollow-straw version 3, decisive test (27 Nov 2026). With Claude (Anthropic).
The pressures f_k must be equal for the three straws at each Minana corner (Minana is fixed). Solve that linear system alone:
if its solutions are only (alpha x Minana's own face functions + one common affine function), then at a core corner whose three
faces are NOT a Minana corner (the swapped ones) no straw ordering can hold, whatever the core: flat-walled straws are impossible
for that pairing, and every wall must bend at least once. Linear algebra (numerical rank, checked by SVD gap)."""
import os, sys, json
import numpy as np
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = argv
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json'))); mf = d['minana_faces']
Dm = A.build("aequus-377"); MV = np.array([[float(c) for c in v] for v in Dm["V"]])
mverts = [vs for vs, kk in Dm["faces"]]
at = {}
for t, f in enumerate(mverts):
    for v in f: at.setdefault(v, []).append(t)
rows = []
for v, ts in at.items():     # labels here are Minana faces; any pairing only relabels the unknowns, so the rank is pairing-free
    x = np.append(MV[v], 1.0)
    for j in ts[1:]:
        r = np.zeros(240); r[4 * ts[0]:4 * ts[0] + 4] = x; r[4 * j:4 * j + 4] = -x; rows.append(r)
M = np.array(rows); s = np.linalg.svd(M, compute_uv=False)
tol = 1e-9 * s[0]; rank = int((s > tol).sum()); null = 240 - rank
print('equations', M.shape[0], 'unknowns 240; rank', rank, '; solution space dimension', null, flush=True)
print('singular values around the cut:', ['%.2e' % x for x in s[rank - 3:rank + 3]], flush=True)
print('expected if only alpha x face functions + common affine: 5', flush=True)
print('RESULT:', 'flat-walled straws IMPOSSIBLE for any swapped corner (solution space = the trivial 5)' if null == 5 else f'solution space {null}: more freedom than the trivial 5, flat walls not ruled out by this test')
print('FINAL ok' if M.shape[0] == 232 else 'FINAL FAIL')
