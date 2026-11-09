# DICTO 11-09 (Mandalaspheres, Kaleidohedra app): on the Cleo sphere the yantra lines look as if they run on as great circles across
# the whole network; maybe exact with a slight scale change. Each yantra line is a great circle (gnomonic). For scale factor lam
# (yantra size / Cleo incircle size) and both orientations (top to a face corner = app, or to an edge), find line pairs from DIFFERENT
# yantras whose great circles nearly coincide (pole angle), and the lam where they coincide exactly. FINAL ok.
import json, math, itertools, sys
import numpy as np
sys.path.insert(0, '../../2026-11-08-tetra-yantra')
V = json.load(open('../../2026-11-08-tetra-yantra/golden_family.json'))['GF1']
f = lambda d: {int(k): float(v['a']) for k, v in d.items()}
b, w, a = f(V['b']), f(V['w']), f(V['apex'])
phi = (1 + 5 ** .5) / 2
I = [np.array(p, float) for c in [(0, 1, phi), (1, phi, 0), (phi, 0, 1)] for p in itertools.product(*[(x, -x) if x else (0,) for x in c])]
I = [v / np.linalg.norm(v) for v in I]
E = min(np.linalg.norm(I[i] - I[j]) for i, j in itertools.combinations(range(12), 2))
faces = [t for t in itertools.combinations(range(12), 3) if all(abs(np.linalg.norm(I[x] - I[y]) - E) < 1e-9 for x, y in itertools.combinations(t, 2))]
c0 = sum(I[k] for k in faces[0]); c0 /= np.linalg.norm(c0)
m0 = I[faces[0][0]] + I[faces[0][1]]; m0 /= np.linalg.norm(m0); RHO = math.acos(np.dot(c0, m0))
ANTI = {i: next(j for j, u in enumerate(faces) if np.allclose(sum(I[k] for k in u), -sum(I[k] for k in faces[i]))) for i in range(20)}
lines = []
for i in range(1, 10):
    L, R, A = (-w[i], b[i]), (w[i], b[i]), (0, a[i]); lines += [(L, R, i, 'base'), (L, A, i, 'side'), (R, A, i, 'side')]
def poles(lam, orient):
    sc = lam * math.tan(RHO) / 0.5; out = []
    for fi, t in enumerate(faces):
        cen = sum(I[k] for k in t); cen /= np.linalg.norm(cen)
        tgt = I[t[0]] if orient == 'corner' else -I[t[0]]
        up = tgt - np.dot(tgt, cen) * cen; up /= np.linalg.norm(up); rt = np.cross(up, cen)
        P = lambda x, y: cen + (x * sc) * rt + ((0.5 - y) * sc) * up
        for li, (p, q, i, kind) in enumerate(lines):
            n = np.cross(P(*p), P(*q)); out.append((fi, li, n / np.linalg.norm(n)))
    return out
def near(lam, orient, tol):
    Ps = poles(lam, orient); res = []
    for (f1, l1, n1), (f2, l2, n2) in itertools.combinations(Ps, 2):
        if f1 == f2 or ANTI[f1] == f2: continue
        ang = math.degrees(math.acos(min(1, abs(float(np.dot(n1, n2))))))
        if ang < tol: res.append((ang, f1, l1, f2, l2))
    return res
for orient in ('corner', 'edge'):
    print(f'== orientation: top to a face {orient}' + ('  (as in the app)' if orient == 'corner' else ''))
    for lam in (1.0,):
        r = near(lam, orient, 3.0); r.sort()
        print(f' lam 1.000: pairs within 3 deg: {len(r)}; closest: ' + ', '.join(f'{x[0]:.3f} (t{lines[x[2]][2]} {lines[x[2]][3]} / t{lines[x[4]][2]} {lines[x[4]][3]})' for x in r[:6]))
    # scan lam: best exact coincidences (pairs below 0.01 deg)
    best = []
    for lam in np.linspace(0.5, 2.0, 1501):
        r = near(lam, orient, 0.02)
        if r: best.append((len(r), lam, min(x[0] for x in r), sorted(set((lines[x[2]][2], lines[x[2]][3], lines[x[4]][2], lines[x[4]][3]) for x in r))[:4]))
    best.sort(key=lambda x: x[1])
    for n_, lam, mn, kinds in best: print(f' lam {lam:.3f}: {n_} pairs within 0.05 deg (min {mn:.4f}); kinds {kinds}')
print('FINAL ok' if len(faces) == 20 and len(ANTI) == 20 else 'FINAL FAIL: face set or antipodes wrong')
