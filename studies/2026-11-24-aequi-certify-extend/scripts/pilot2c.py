# Part 2(c) PILOT: fair dice with one face orbit OFF the symmetry axes. A direction v(s) moves along a mirror arc of the
# group G from axis a (s = 0) to axis b (s = 1): v(s) = normalise((1 - s) a + s b). Its G-orbit (|G|/2 directions for
# a point on one mirror) is joined to one axis orbit A at depth 1; the one fairness equation "solid angle of a face of
# the moving orbit = 4 pi / N" is solved for its depth d (all roots with log d in [-1.5, 1.5], by sign changes on a grid
# of 121 + bisection). For each s: number of fair depths, N, corners, sides, full symmetry. Double precision (pilot).
# usage: pilot2c.py out.json
import json, sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import OH, IH, closure, rot, P3, schoenflies, phi
from solve import face_omegas
from exact import combinatorics, centroid, symmetry
from scipy.optimize import brentq
TD = [g for g in OH if np.isclose(np.linalg.det(g), 1) and any(True for _ in [0])]
T = closure([P3, rot((0, 0, 1), np.pi)])
TH = closure([P3, rot((0, 0, 1), np.pi), -np.eye(3)])
TDG = closure([P3, rot((0, 0, 1), np.pi), np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1.]])])
assert len(TDG) == 24 and schoenflies(TDG) == 'Td'
def un(v): v = np.array(v, float); return v / np.linalg.norm(v)
def orbit(G, v):
    out = []
    for g in G:
        w = g @ v
        if not any(np.abs(w - x).max() < 1e-9 for x in out): out.append(w)
    return np.array(out)
FAM = [  # name, group, axis orbit (representative), arc a -> b on a mirror of G, label of the axis orbit, labels of a, b
    ('Oh: C6 + 24 on the arc C6 -> RD12', OH, (1, 0, 0), (1, 0, 0), (1, 1, 0)),
    ('Oh: C6 + 24 on the arc C6 -> O8', OH, (1, 0, 0), (1, 0, 0), (1, 1, 1)),
    ('Oh: O8 + 24 on the arc O8 -> RD12', OH, (1, 1, 1), (1, 1, 1), (1, 1, 0)),
    ('Oh: RD12 + 24 on the arc C6 -> O8', OH, (1, 1, 0), (1, 0, 0), (1, 1, 1)),
    ('Td: O8/4 + 12 on the arc O8/4 -> C6', TDG, (1, 1, 1), (1, 1, 1), (0, 0, 1)),
    ('Td: C6 + 12 on the arc O8/4 -> RD12 ... C6', TDG, (1, 0, 0), (1, 1, 1), (1, 1, -2)),
    ('Th: C6 + 12 on the arc C6 (1,0,0) -> C6 (0,1,0) (pyritohedral; D12 at s = 1/(1+phi))', TH, (1, 0, 0), (1, 0, 0), (0, 1, 0)),
    ('Th: O8 + 12 on the arc C6 (1,0,0) -> C6 (0,1,0)', TH, (1, 1, 1), (1, 0, 0), (0, 1, 0)),
    ('Ih: D12 + 60 on the arc D12 -> RT30 (0,0,1)', IH, (0, phi, 1), (0, phi, 1), (0, 0, 1)),
]
def run(fam):
    name, G, ax, a, b = fam
    A = orbit(G, un(ax)); rows = []
    for s in np.linspace(0, 1, 61)[1:-1]:
        v = un((1 - s) * np.array(a, float) + s * np.array(b, float)); M = orbit(G, v)
        if any(np.abs(M @ x).max() > 1 - 1e-9 for x in A): rows.append(dict(s=s, note='meets the axis orbit')); continue
        Nrm = np.vstack([A, M]); N = len(Nrm); T_ = 4 * np.pi / N; nA = len(A)
        def F(ld):
            try: om = face_omegas(Nrm, np.r_[np.ones(nA), np.full(len(M), np.exp(ld))])
            except Exception: return np.nan
            return om[nA:].mean() - T_
        grid = np.linspace(-1.5, 1.5, 121); fv = np.array([F(x) for x in grid]); roots = []
        for i in range(120):
            if np.isfinite(fv[i]) and np.isfinite(fv[i + 1]) and fv[i] * fv[i + 1] < 0: roots.append(brentq(F, grid[i], grid[i + 1], xtol=1e-14))
        sols = []
        for ld in roots:
            D = np.r_[np.ones(nA), np.full(len(M), np.exp(ld))]
            om = face_omegas(Nrm, D)
            if np.abs(om - T_).max() > 1e-9: continue
            V, inc, trip, faces = combinatorics(Nrm, D); cen, vol = centroid(V, faces, Nrm, D); Gs, forbs = symmetry(Nrm, D, cen)
            sols.append(dict(depth=float(np.exp(ld)), corners=len(V), sides=sorted(set((len(faces[0]),))) + sorted({len(f) for f in faces[nA:]}),
                             sym=schoenflies(Gs), orbits=len(forbs), centroid_ok=bool(np.abs(cen).max() < 1e-9),
                             maxcorner=max(len(I) for I in inc)))
        rows.append(dict(s=float(s), N=int(N), nmoving=len(M), sols=sols))
    seg = []
    for r in rows:
        if 'sols' not in r: sig = ('meets axis',)
        else: sig = (len(r['sols']),) + tuple((x['corners'], x['sym'], tuple(x['sides'])) for x in r['sols'])
        if seg and seg[-1][0] == sig: seg[-1][2] = r['s']
        else: seg.append([sig, r['s'], r['s']])
    return dict(family=name, group=schoenflies(G), rows=rows, segments=[[list(map(str, sig)), s0, s1] for sig, s0, s1 in seg])
import multiprocessing as mpc
with mpc.get_context('fork').Pool(len(FAM)) as pool: out = pool.map(run, FAM)
for o in out:
    print(o['family'], flush=True)
    for sig, s0, s1 in o['segments']: print('   s %.3f..%.3f : %s' % (s0, s1, ' '.join(sig)), flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
ok = all(o['rows'] and any('sols' in r for r in o['rows']) for o in out)
print('FINAL ok' if ok else 'FINAL FAIL: a family has no rows')
