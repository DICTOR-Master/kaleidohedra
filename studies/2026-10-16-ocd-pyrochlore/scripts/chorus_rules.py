# Step 30 (DICTO: "find a rule that keeps the spine pure Fibonacci"). Candidate silencing rules are tested where the ring-clash
# window and the canonical window disagree (the first four plane points with t_c <= t < L: heights 12.81, -22.71, 34.77, -44.66)
# and on the whole radius-10 build. Every rule is the chorus's greedy five-fold silencing (float clash test, whole rings) with a
# different priority:
#   A  most clashes first, ties to the copy farther from the centre (the chorus as built);
#   B  most clashes first, ties to the copy nearer the axis;
#   C  most clashes first, ties to the ring nearest to clashing with itself (smallest ring margin g = gauge of X - R72 X);
#   D  ring margin first (smallest g silenced first among clashing copies), clash count only as tie-break.
# Clash counts at every decision that touches a target or its rival are logged (this checks the step-29 statement that the two
# rings tie). Patches: all sites of all five voices with |height - h| < 7 and distance from the axis < t + 5 (exact sites).
import sys, itertools, numpy as np
exec(open('scripts/chorus_window_why.py').read().split('out2 = []')[0])           # steps 26-28 setup (radius-10 build, exact)
i0 = next(i for i in Pl if wk[i] != -1)
q_ = R72 @ Pf[i0]; j0 = int(np.argmin(np.linalg.norm(Pf - q_, axis=1)))
if np.linalg.norm(Pf[j0] - q_) > 1e-6: q_ = np.linalg.matrix_power(R72, 4) @ Pf[i0]; j0 = int(np.argmin(np.linalg.norm(Pf - q_, axis=1)))
Dx = sub(sites[i0][1], sites[j0][1]); gg = max((dot(n, Dx) / (Q(2) * d) for _, n, d in PO), key=lambda q: q.f())
tc2 = (tr[i0] * tr[i0] / dot(w, w)) / (gg * gg)
dep = []
for p in range(-80, 81):
    for q in range(-80, 81):
        t = tb1 * Q(p) + tb2 * Q(q)
        if 0 < t.f() < Lw.f() and (t * t / dot(w, w) - tc2).f() >= 0: dep.append(((hb1 * Q(p) + hb2 * Q(q)).f() / vv.f() ** .5, p, q))
dep.sort(key=lambda x: abs(x[0])); dep = dep[:4]
ax = f(v) / np.linalg.norm(f(v))
n_f = np.array([f(n) / np.linalg.norm(f(n)) for _, n, d in PO]); d_f = np.array([d.f() / np.linalg.norm(f(n)) for _, n, d in PO])
gf = lambda D_: np.max((D_ @ n_f.T) / (2 * d_f), axis=-1)
rmax = 2 * np.linalg.norm(Of, axis=1).max() + 1e-6
bases = []
for k in range(5):
    for a, b, c in itertools.combinations(cubes[k], 3):
        M = np.array([Bf[a], Bf[b], Bf[c]]).T
        if abs(np.linalg.det(M)) > 1e-6 and all(np.allclose(np.linalg.solve(M, Bf[i]), np.round(np.linalg.solve(M, Bf[i])), atol=1e-6) for i in cubes[k]): break
    bases.append((M, a, b, c))
def patch(hc, RW, HW=7.0):
    loc = []
    for k, (M, a, b, c) in enumerate(bases):
        Mi = np.linalg.inv(M); ctr = hc * ax; rad = np.hypot(HW, RW) + 1; lim = np.abs(Mi).sum(axis=1) * rad; c0 = Mi @ ctr
        for ijk in itertools.product(*[range(int(np.floor(c0[r] - lim[r])), int(np.ceil(c0[r] + lim[r])) + 1) for r in range(3)]):
            x = M @ np.array(ijk, float); z = x @ ax; rho = np.linalg.norm(x - z * ax)
            if abs(z - hc) >= HW or rho >= RW: continue
            onaxis = rho < 1e-9
            if not (onaxis or wedge(x) == k): continue
            if onaxis and any(np.allclose(x, y) for y in loc): continue
            loc.append(x)
    return np.array(loc)
def margin(LP):                                       # ring margin: gauge of the difference to the 72-degree turned copy
    m = gf(LP - LP @ R72.T); m[np.linalg.norm(LP - np.outer(LP @ ax, ax), axis=1) < 1e-9] = np.inf   # an axis copy is its own ring
    return m
def greedy(LP, rule, watch=()):
    N = len(LP); nb = [[] for _ in range(N)]
    for i in range(N):
        dd = np.linalg.norm(LP - LP[i], axis=1); cand = np.where((dd < rmax) & (dd > 1e-9))[0]
        if len(cand): nb[i] = list(cand[gf(LP[cand] - LP[i]) < 1 - 1e-9])
    ring = []
    for i in range(N):
        r = [i]
        for s in range(1, 5):
            qq = np.linalg.matrix_power(R72, s) @ LP[i]; j = int(np.argmin(np.linalg.norm(LP - qq, axis=1)))
            if np.linalg.norm(LP[j] - qq) < 1e-6: r.append(j)
        ring.append(r)
    mg = margin(LP); dc = np.linalg.norm(LP, axis=1); rho = np.linalg.norm(LP - np.outer(LP @ ax, ax), axis=1)
    alive = np.ones(N, bool); log = []
    while True:
        cnt = {i: sum(alive[j] for j in nb[i]) for i in np.where(alive)[0]}; cnt = {i: c for i, c in cnt.items() if c}
        if not cnt: break
        key = {'A': lambda i: (cnt[i], dc[i]), 'B': lambda i: (cnt[i], -rho[i]), 'C': lambda i: (cnt[i], -mg[i]),
               'D': lambda i: (-mg[i], cnt[i])}[rule]
        i = max(cnt, key=key)
        if any(set(ring[i]) & set(ring[wj]) for wj in watch):
            log.append((int(i), {int(w_): (cnt.get(w_, 0), round(float(mg[w_]), 4)) for w_ in watch}))
        for j in ring[i]: alive[j] = False
    return alive, log
out = [f'(30) rules: A as built (ties to farther from centre), B (ties to nearer the axis), C (ties to the ring nearest self-clash), D (ring margin first)',
       f'    departure points (t_c <= t < L), nearest first: {[(round(h, 3), p, q) for h, p, q in dep]}']
ok = {r: True for r in 'ABCD'}
for h, p, q in dep:
    XT = add(sc(b1, Q(p)), sc(b2, Q(q))); xT = f(XT); tT = np.linalg.norm(xT - (xT @ ax) * ax)
    LP = patch(h, tT + 5.0); iT = int(np.argmin(np.linalg.norm(LP - xT, axis=1))); assert np.linalg.norm(LP[iT] - xT) < 1e-6
    dd = np.linalg.norm(LP - LP[iT], axis=1); near = np.where((dd < rmax) & (dd > 1e-9))[0]; riv = [int(j) for j in near if gf(LP[j] - LP[iT]) < 1 - 1e-9]
    mg = margin(LP)
    out.append(f'  height {h:.3f} (t {tT:.4f}): patch {len(LP)} sites; target ring margin {mg[iT]:.4f}; rivals (overlapping the target, float): '
               + ', '.join(f'h {LP[j] @ ax:.3f} rho {np.linalg.norm(LP[j] - (LP[j] @ ax) * ax):.4f} margin {mg[j]:.4f}' for j in riv))
    for rule in 'ABCD':
        alive, log = greedy(LP, rule, watch=[iT] + riv)
        res = 'SILENCED (Fibonacci)' if not alive[iT] else 'kept (thinned)'; ok[rule] &= not alive[iT]
        first = log[0] if log else None
        out.append(f'      rule {rule}: target {res}; silenced {int((~alive).sum())}; first decision touching them: removed site {first[0] if first else "-"}'
                   f' {"(target ring)" if first and first[0] == iT else ""}; (clash count, margin) then: {first[1] if first else "-"}')
out.append('  rules that keep the spine Fibonacci at all four points: ' + ', '.join(r for r in 'ABCD' if ok[r]))
# the radius-10 build under each rule: same silences as built? (the built run is the reference; its kept set is exact-checked)
P10 = Pf; built = silent
for rule in 'ABCD':
    alive, _ = greedy(P10, rule)
    out.append(f'  radius-10 build under rule {rule}: silenced {int((~alive).sum())} (built 385); same silent set as built: {bool(np.array_equal(~alive, built))}'
               + ('' if np.array_equal(~alive, built) else f'; differ at {int(np.sum((~alive) != built))} sites'))
print('\n'.join(out)); open('data/chorus-rules.txt', 'w').write('\n'.join(out) + '\n')
