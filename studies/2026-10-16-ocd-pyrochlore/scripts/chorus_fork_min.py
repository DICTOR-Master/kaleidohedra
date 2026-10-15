# Step 30b: is the fork really a tie? Exact minimum five-fold silencing (integer program over whole rings, float clash test) on the
# patch round each of the four departure points, solved twice: with the core target's ring forced silent (Fibonacci) and forced
# kept (thinned). Equal minima = a true tie; otherwise the smaller decides. Also lists every copy the rival clashes with.
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
exec(open('scripts/chorus_rules.py').read().split("out = [f'(30) rules")[0])
def orbits(LP):
    oid = -np.ones(len(LP), int); k = 0
    for i in range(len(LP)):
        if oid[i] >= 0: continue
        for s in range(5):
            qq = np.linalg.matrix_power(R72, s) @ LP[i]; j = int(np.argmin(np.linalg.norm(LP - qq, axis=1)))
            if np.linalg.norm(LP[j] - qq) < 1e-6: oid[j] = k
        k += 1
    return oid, k
out = ['(30b) minimum five-fold silencing on each patch (integer program, whole rings, float clash test): target ring forced silent vs forced kept']
for h, p, q in dep:
    XT = add(sc(b1, Q(p)), sc(b2, Q(q))); xT = f(XT); tT = np.linalg.norm(xT - (xT @ ax) * ax)
    LP = patch(h, tT + 5.0); iT = int(np.argmin(np.linalg.norm(LP - xT, axis=1)))
    oid, no = orbits(LP); rows = []; forced = set()
    for i in range(len(LP)):
        dd = np.linalg.norm(LP - LP[i], axis=1); cand = np.where((dd < rmax) & (dd > 1e-9))[0]
        for j in cand[gf(LP[cand] - LP[i]) < 1 - 1e-9]:
            if j <= i: continue
            if oid[i] == oid[j]: forced.add(oid[i])
            else: rows.append((oid[i], oid[j]))
    rows = sorted(set(tuple(sorted(r)) for r in rows))
    A = np.zeros((len(rows), no))
    for r, (a, b) in enumerate(rows): A[r, a] = 1; A[r, b] = 1
    res = {}
    for want in (1, 0):
        lb = np.zeros(no); ub = np.ones(no)
        for o in forced: lb[o] = 1
        lb[oid[iT]] = ub[oid[iT]] = want
        r_ = milp(np.ones(no), constraints=[LinearConstraint(A, 1, np.inf)], integrality=np.ones(no), bounds=Bounds(lb, ub))
        res[want] = int(round(r_.fun)) if r_.success else None
    dd = np.linalg.norm(LP - LP[iT], axis=1); near = np.where((dd < rmax) & (dd > 1e-9))[0]; riv = [int(j) for j in near if gf(LP[j] - LP[iT]) < 1 - 1e-9]
    parts = []
    for j in riv:
        d2 = np.linalg.norm(LP - LP[j], axis=1); c2 = np.where((d2 < rmax) & (d2 > 1e-9))[0]; c2 = [int(k) for k in c2 if gf(LP[k] - LP[j]) < 1 - 1e-9]
        parts.append(f'rival h {LP[j] @ ax:.3f} clashes with {len(c2)}: ' + '; '.join(f'h {LP[k] @ ax:.3f} rho {np.linalg.norm(LP[k] - (LP[k] @ ax) * ax):.4f}{" (target)" if k == iT else ""}{" (ring self-clashes)" if oid[k] in forced else ""}' for k in c2))
    verdict = 'TIE' if res[1] == res[0] else ('Fibonacci cheaper' if res[1] < res[0] else 'thinned cheaper')
    out.append(f'  height {h:.3f}: {no} rings, {len(rows)} clashing ring pairs, {len(forced)} self-clashing rings; minimum with target silent {res[1]}, with target kept {res[0]} rings -> {verdict}')
    out += ['      ' + s_ for s_ in parts]
print('\n'.join(out)); open('data/chorus-fork-min.txt', 'w').write('\n'.join(out) + '\n')
