# Fable, FLOAT independent check of data/gbpc-build.json (2026-10-16): random points in one bcc cell; fraction free, covered by tiles (all lattice translates), covered twice, and covered while inside an RT.
import sys, io, os, contextlib, json, numpy as np
os.chdir('/home/dicto/kaleidohedra/studies/2026-10-16-ocd-pyrochlore')
src = open('scripts/golden_fill.py').read().split('# ---- all bodies')[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
Nn = np.array([fl(n) for n, d in RT['H']]); Dd = np.array([d.f() for n, d in RT['H']])
L = np.array([fl(b) for b in LB]).T
D = json.load(open('data/gbpc-build.json'))
rng = np.random.default_rng(0); n = 200000
X = rng.random((n, 3)) @ L.T
sh = [L @ np.array(m) for m in np.array(np.meshgrid(*[range(-4, 5)] * 3, indexing='ij')).reshape(3, -1).T]
sh = [s for s in sh if np.linalg.norm(s) < 6]
inRT = np.zeros(n, bool)
for s in sh: inRT |= np.all((X - s) @ Nn.T <= Dd, axis=1)
cnt = np.zeros(n, int)
for T in D['tiles']:
    W = np.array(T['edges']); IB = np.linalg.inv(W); p = np.array(T['corner'])
    for s in sh:
        t = (X - p - s) @ IB
        cnt += np.all((t > 0) & (t < 1), axis=1)
cv = abs(np.linalg.det(L))
txt = f'DICTO · dictospheres.com\nFLOAT Monte Carlo, {n} points in one cell: free {1 - inRT.mean():.4f}, tiles {(cnt > 0).mean():.4f}, covered twice {(cnt > 1).mean():.6f}, tile points inside an RT {(inRT & (cnt > 0)).mean():.6f}; tiles / free = {(cnt > 0).mean() / (1 - inRT.mean()):.4f}\n'; print(txt); open('data/gbpc-build-check.txt', 'w').write(txt)
print('cell', cv, 'free frac', 1 - inRT.mean(), 'tile frac', (cnt > 0).mean(), 'multi', (cnt > 1).mean(), 'tile in RT', (inRT & (cnt > 0)).mean())
print('sum tile vol / cell', sum(abs(np.linalg.det(np.array(T['edges']))) for T in D['tiles']) / cv)
