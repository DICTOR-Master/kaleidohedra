# Network versions, midsphere screen (2026-10-12, after DICTO's ring models): for every pair of forms in the same turn, the exact
# size at which the inner one touches the outer one naturally (inner corners on outer face centres / edge midpoints / corners, or
# inner edge midpoints on outer face centres), checked that the inner one then lies inside the outer one. The outer/inner edge
# ratio is reported and flagged when it is a power of phi.
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open(__file__.replace('touch_screen.py', 'network_screen.py')).read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
def faces(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
def mids(V):
    d = min(np.linalg.norm(V[0] - w) for w in V[1:])
    return np.array([(V[a] + V[b]) / 2 for a, b in itertools.combinations(range(len(V)), 2) if abs(np.linalg.norm(V[a] - V[b]) - d) < 1e-9])
info = {}
for X in FORMS:
    V = ref[X]; F = faces(V); M = mids(V)
    info[X] = dict(V=V, cdir=V / np.linalg.norm(V, axis=1)[:, None], R=np.linalg.norm(V, axis=1).max(),
                   fdir=F[:, :3], r=-F[:, 3].max(), mdir=M / np.linalg.norm(M, axis=1)[:, None], m=np.linalg.norm(M, axis=1).min(), F=F)
    # RT has corners at two radii; R = the larger
same = lambda A, B: all(np.min(np.linalg.norm(B - a, axis=1)) < 1e-6 for a in A)
out = []
for X, Y in itertools.product(FORMS, FORMS):
    a, b = info[X], info[Y]
    for label, ok, ri, ro in [('corners on face centres', same(a['cdir'], b['fdir']), a['R'], b['r']),
                              ('corners on edge midpoints', same(a['cdir'], b['mdir']), a['R'], b['m']),
                              ('corners on corners', same(a['cdir'], b['cdir']), a['R'], b['R']),
                              ('edges touching face centres', same(a['mdir'], b['fdir']), a['m'], b['r'])]:
        if not ok: continue
        s = ro / ri                                   # scale on the inner form (outer at edge 1)
        Vin = a['V'] * s
        if not np.all(Vin @ b['F'][:, :3].T + b['F'][:, 3] <= 1e-7): continue     # must lie inside
        ratio = 1 / s; k = np.log(ratio) / np.log(PHI)
        tag = f'phi^{round(k)}' if abs(k - round(k)) < 1e-6 else ''
        out.append((X, Y, label, ratio, tag))
for X, Y, label, ratio, tag in sorted(out, key=lambda t: (t[4] == '', t[0], t[1])):
    print(f'{X:2s} inside {Y:2s}: {label:28s} outer/inner edge = {ratio:.6f} {tag}')
