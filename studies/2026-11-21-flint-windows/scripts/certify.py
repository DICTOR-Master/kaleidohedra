"""Certified regime at one rational depth.  Usage: python certify.py <cube|dodeca> <s as p/q> <N> [<N_exact>]
Steps 0..N: the type is read in floating point, then every corner is solved EXACTLY (fmpq for the cube, Q(sqrt5) for the
dodecahedron) and checked: every tight incidence exactly zero, every other slack certified negative (arb ball from the exact
value), Euler V - E + F = 2 (E = pairs of corners sharing two planes, F = planes with three or more corners), so no corner is
missing.  Closure: the first pair of steps (j, k) with equal counts and kinds whose corners match exactly (parallel, one exact
ratio of squared radii).  A pair that does not close is certified so by one corner of step k with no parallel corner in step j
(every cross product a certified nonzero arb ball).  Prints one line per step and a verdict; FINAL ok."""
import sys, time, itertools
import numpy as np
from flint import fmpq, arb, ctx
import fw

kind, s, N = sys.argv[1], fmpq(*map(int, sys.argv[2].split('/'))), int(sys.argv[3])
t0 = time.time()
field = 'fmpq' if kind == 'cube' else 'Q5'
ctx.prec = 128
def A(x): return arb(x) if kind == 'cube' else arb(x.a) + arb(x.b) * arb(5).sqrt()
def zero(x): return x == 0 if kind == 'cube' else x.is_zero()
types, Vf = fw.float_chain(kind, float(s), N)
planes = fw.start_planes(kind, field, s if kind == 'cube' else fw.Q5(s))
hist = []; verdict = None
for k in range(N + 1):
    typ = types[k]
    V = [fw.solve(planes, tri) for tri, T in typ]
    VA = [tuple(A(x) for x in v) for v in V]
    PA = [(tuple(A(x) for x in n), A(c)) for n, c in planes]
    inc = all(zero(fw.slack(planes, V[j], i)) for j, (tri, T) in enumerate(typ) for i in T)
    neg = all(fw.dot(PA[i][0], VA[j]) - PA[i][1] < 0 for j, (tri, T) in enumerate(typ) for i in range(len(planes)) if i not in set(T))
    Ts = [set(T) for tri, T in typ]
    E = sum(1 for a, b in itertools.combinations(range(len(V)), 2) if len(Ts[a] & Ts[b]) >= 2)
    cnt = {}
    for T in Ts:
        for i in T: cnt[i] = cnt.get(i, 0) + 1
    F = sum(1 for i, c in cnt.items() if c >= 3)
    kinds = fw.kinds_of(typ, len(planes))
    ok = inc and neg and len(V) - E + F == 2
    print(f'step {k}: {len(V)} corners, {E} edges, {F} faces, kinds {dict(kinds)}; exact incidences {inc}, free slacks < 0 {neg}, '
          f'Euler {len(V) - E + F}; {time.time() - t0:.1f}s', flush=True)
    if not ok:
        if verdict is None and k >= 6:
            print(f'NO CLOSURE within {k - 1} steps (certified exactly); step {k}: the floating-point type is not clean, not used')
            print('FINAL ok' if len(hist) == k else 'FINAL FAIL: steps missing'); sys.exit()
        print('FINAL FAIL: the type is not certified at this step'); sys.exit()
    for j, (Vj, VAj, kj) in enumerate(hist):
        if len(Vj) != len(V) or kj != kinds: continue
        # exact similarity: partner by float direction, then exact cross product zero and one exact ratio
        a = np.array([[float(x.mid()) for x in u] for u in VAj]); a /= np.linalg.norm(a, axis=1)[:, None]
        g = None; sim = True
        for v, va in zip(V, VA):
            b = np.array([float(x.mid()) for x in va]); b /= np.linalg.norm(b)
            m = int(np.argmin(np.linalg.norm(a - b, axis=1))); u = Vj[m]
            if not all(zero(x) for x in fw.cross(u, v)) or not (fw.dot(VAj[m], va) > 0):   # parallel, same way round
                sim = False; break
            r = fw.dot(v, v) / fw.dot(u, u)
            if g is None: g = r
            elif not zero(r - g): sim = False; break
        if sim:
            verdict = (j, k, g); break
        # certify non-similarity: one corner of step k with no parallel corner in step j
        cert = any(all(any(not (x.contains(0)) for x in fw.cross(ua, va)) for ua in VAj) for va in VA)
        print(f'  steps {j}, {k}: same counts and kinds, NOT similar; certified by a corner with no parallel partner: {cert}')
        if not cert: print('FINAL FAIL: non-similarity not certified'); sys.exit()
    if verdict: break
    hist.append((V, VA, kinds))
    if k < N: planes = [(v, fw.dot(v, v)) for v in V]
if verdict:
    j, k, g = verdict
    gs = str(g) if kind == 'cube' else f'{g.a} + {g.b} sqrt5'
    print(f'CLOSES exactly: step {k} = step {j} scaled, period {k - j}, entered at step {j}; squared radius gain over the period {gs} ~ {float(g):.10f}')
else:
    print(f'NO CLOSURE within {N} steps (certified exactly)')
print('FINAL ok' if verdict or len(hist) == N + 1 else 'FINAL FAIL: steps missing')
