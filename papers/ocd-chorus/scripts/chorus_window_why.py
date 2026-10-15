# Step 28 ("next": why the canonical window). Exact in Q(sqrt5). For each core-plane site with transverse distance t < 1.6,
# test it against its four ring-mates (the same site turned by 72k degrees about the axis, which are sites of the other voices):
# overlap (some pair has every face separation < 0), touch (best separation exactly 0) or apart. If overlap <=> t < L_can and
# touch at t = L_can, the Fibonacci window is the self-clash threshold of five-fold rings.
import sys, numpy as np
exec(open('scripts/chorus_canonical.py').read().split("print('\\n'.join(out)); open('data/chorus-canonical.txt'")[0])
out2 = []
R72f = R72
Pf_ = np.array([x for x, _ in sites])
def sep(X, Y):
    Dx = sub(X, Y); best = max((dot(n, Dx) - Q(2) * d for _, n, d in PO), key=lambda q: q.f()); return best
rows = []
for i in sorted([i for i in Pl if wk[i] != -1 and tr[i].f() / dot(w, w).f() ** .5 < 1.6], key=lambda i: tr[i].f()):
    t = tr[i].f() / dot(w, w).f() ** .5
    mates = []
    for s_ in range(1, 5):
        q = np.linalg.matrix_power(R72f, s_) @ Pf_[i]; j = int(np.argmin(np.linalg.norm(Pf_ - q, axis=1)))
        if np.linalg.norm(Pf_[j] - q) < 1e-6: mates.append(j)
    seps = [sep(sites[i][1], sites[j][1]) for j in mates]
    worst = min(seps, key=lambda q: q.f()) if seps else None
    state = 'no mates in build' if worst is None else ('OVERLAP' if worst.f() < 0 and worst != Q(0) else ('TOUCH (exact 0)' if worst == Q(0) else 'apart'))
    rows.append((t, silent[i], state, worst))
    out2.append(f'  t = {t:.5f}  {"silent" if silent[i] else "kept  "}  ring-mates found {len(mates)}/4  vs nearest ring-mate: {state}' + (f'  (best face separation {worst})' if worst is not None and state != 'OVERLAP' else ''))
Lc = Lw.f() / dot(w, w).f() ** .5
ok = all(((t < Lc - 1e-9) == (st == 'OVERLAP')) for t, _, st, _ in rows if st != 'no mates in build')
edge = [st for t, _, st, _ in rows if abs(t - Lc) < 1e-6]
out2.insert(0, f'(28) core-plane sites vs their own five-fold ring-mates (exact); canonical L = {Lc:.6f}')
out2.append(f'  overlap exactly when t < L: {ok}; the copy at t = L: {edge}')
print('\n'.join(out2)); open('data/chorus-window-why.txt', 'w').write('\n'.join(out2) + '\n')
# Critical distance: a ring-mate pair differs by D = X - R72 X, purely transverse and proportional to t (all plane sites lie on one
# ray), so overlap <=> gauge g(D) = max n.D/(2d) < 1, and g = t * gamma. t_c = t / g(D), exact and the same for every plane site.
tcs = []
for i in [i for i in Pl if wk[i] != -1 and tr[i].f() / dot(w, w).f() ** .5 < 1.6]:
    q = np.linalg.matrix_power(R72f, 1) @ Pf_[i]; j = int(np.argmin(np.linalg.norm(Pf_ - q, axis=1)))
    if np.linalg.norm(Pf_[j] - q) > 1e-6:
        q = np.linalg.matrix_power(R72f, 4) @ Pf_[i]; j = int(np.argmin(np.linalg.norm(Pf_ - q, axis=1)))
    Dx = sub(sites[i][1], sites[j][1]); g = max((dot(n, Dx) / (Q(2) * d) for _, n, d in PO), key=lambda q: q.f())
    tcs.append((tr[i] * tr[i] / dot(w, w)) / (g * g))                     # t_c^2, exact
same = all(x == tcs[0] for x in tcs); tc2 = tcs[0]; L2 = Lw * Lw / dot(w, w)
msg = [f'  critical distance (ring-mates just touch): t_c^2 = {tc2} (t_c = {tc2.f() ** .5:.6f}); same for every plane site: {same}',
       f'  canonical L = {L2.f() ** .5:.6f}; largest silent t = 1.113132; t_c inside the gap between them: {1.113132 < tc2.f() ** .5 < L2.f() ** .5}; t_c == L exactly: {tc2 == L2}']
print('\n'.join(msg)); open('data/chorus-window-why.txt', 'a').write('\n'.join(msg) + '\n')
# Where would the ring-clash chain (window [0, t_c)) first differ from the canonical Fibonacci chain ([0, L))? Plane lattice points
# with t_c <= t < L, exact, nearest to the centre by height.
tcw = Q(0)
diff = []
for p in range(-150, 151):
    for q in range(-150, 151):
        t = tb1 * Q(p) + tb2 * Q(q)
        if not (0 < t.f() < Lw.f()): continue
        tt = t * t / dot(w, w)
        if (tt - tc2).f() >= 0: diff.append(((hb1 * Q(p) + hb2 * Q(q)).f() / vv.f() ** .5, tt.f() ** .5))
diff.sort(key=lambda x: abs(x[0]))
msg = [f'  plane points with t_c <= t < L (kept under ring-clash, but in the canonical chain): nearest heights {[(round(h, 3), round(t, 4)) for h, t in diff[:4]]}',
       f'  -> the ring-clash chain equals the canonical Fibonacci chain for |height| < {abs(diff[0][0]):.3f}; the build reaches |height| < 10']
print('\n'.join(msg)); open('data/chorus-window-why.txt', 'a').write('\n'.join(msg) + '\n')
