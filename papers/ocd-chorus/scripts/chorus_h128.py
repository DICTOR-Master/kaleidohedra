# Step 29 (DICTO: "yes run the 12.8 check"). Exact in Q(sqrt5). The ring-clash rule (window [0, t_c)) and the canonical Fibonacci
# chain (window [0, L)) first differ at the core-plane site with height 12.812, t = 1.1553: its ring does not clash with itself.
# Is it silenced by some OTHER neighbour? Build every site in a cylinder around the axis at that height (all five voices, wedges as
# before), list every copy that overlaps the target exactly, say whether each of those is forced silent (its own five-fold ring
# clashes with itself), and run the same greedy five-fold silencing as the chorus on the patch.
import sys, itertools, numpy as np
exec(open('scripts/chorus_window_why.py').read().split('out2 = []')[0])           # step 27/28 setup (no files written)
# t_c^2, as in step 28
i0 = next(i for i in Pl if wk[i] != -1)
q_ = R72 @ Pf[i0]; j0 = int(np.argmin(np.linalg.norm(Pf - q_, axis=1)))
if np.linalg.norm(Pf[j0] - q_) > 1e-6: q_ = np.linalg.matrix_power(R72, 4) @ Pf[i0]; j0 = int(np.argmin(np.linalg.norm(Pf - q_, axis=1)))
Dx = sub(sites[i0][1], sites[j0][1]); gg = max((dot(n, Dx) / (Q(2) * d) for _, n, d in PO), key=lambda q: q.f())
tc2 = (tr[i0] * tr[i0] / dot(w, w)) / (gg * gg)
# the departure points (t_c <= t < L) nearest the centre, exact 3D position
dep = []
for p in range(-60, 61):
    for q in range(-60, 61):
        t = tb1 * Q(p) + tb2 * Q(q)
        if not (0 < t.f() < Lw.f()): continue
        if (t * t / dot(w, w) - tc2).f() >= 0: dep.append(((hb1 * Q(p) + hb2 * Q(q)).f() / vv.f() ** .5, p, q))
dep.sort(key=lambda x: abs(x[0])); hT, pT, qT = dep[0]
XT = add(sc(b1, Q(pT)), sc(b2, Q(qT))); xT = f(XT)
ax = f(v) / np.linalg.norm(f(v)); rhoT = np.linalg.norm(xT - (xT @ ax) * ax)
out = [f'(29) target: core-plane site at height {hT:.4f}, transverse {rhoT:.4f} (plane coords {pT}, {qT}); wedge {wedge(xT)} (core wedge {k0})']
# all sites of all voices in the cylinder |height - hT| < HW, rho < RW (exact), wedge rule as in the chorus
HW, RW = 7.0, rhoT + 5.0
def inpatch(x): z = x @ ax; return abs(z - hT) < HW and np.linalg.norm(x - z * ax) < RW
loc = []
for k in range(5):
    for a, b, c in itertools.combinations(cubes[k], 3):
        M = np.array([Bf[a], Bf[b], Bf[c]]).T
        if abs(np.linalg.det(M)) > 1e-6 and all(np.allclose(np.linalg.solve(M, Bf[i]), np.round(np.linalg.solve(M, Bf[i])), atol=1e-6) for i in cubes[k]): break
    Mi = np.linalg.inv(M)
    # integer box covering the patch: corners of the cylinder's bounding box mapped to lattice coordinates
    ctr = hT * ax; rad = np.hypot(HW, RW) + 1
    lim = np.abs(Mi).sum(axis=1) * rad; c0 = Mi @ ctr
    rng = [range(int(np.floor(c0[r] - lim[r])), int(np.ceil(c0[r] + lim[r])) + 1) for r in range(3)]
    for ijk in itertools.product(*rng):
        x = M @ np.array(ijk, float)
        if not inpatch(x): continue
        onaxis = np.linalg.norm(x - (x @ ax) * ax) < 1e-9
        if not (onaxis or wedge(x) == k): continue
        if onaxis and any(np.allclose(x, y) for y, _ in loc): continue
        loc.append((x, add(add(sc(bond[a], Q(ijk[0])), sc(bond[b], Q(ijk[1]))), sc(bond[c], Q(ijk[2])))))
LP = np.array([x for x, _ in loc]); NL = len(LP)
iT = int(np.argmin(np.linalg.norm(LP - xT, axis=1))); assert np.linalg.norm(LP[iT] - xT) < 1e-6 and loc[iT][1] == XT
out.append(f'    patch: {NL} sites with |height - {hT:.3f}| < {HW}, distance from the axis < {RW:.2f} (exact, all five voices)')
def best(X, Y): Dx = sub(X, Y); return max((dot(n, Dx) - Q(2) * d for _, n, d in PO), key=lambda q: q.f())
def state(X, Y): b_ = best(X, Y); return 'touch' if b_ == Q(0) else ('overlap' if b_.f() < 0 else 'apart')
rmax = 2 * np.linalg.norm(Of, axis=1).max() + 1e-6
def ring(i):
    r = []
    for s in range(1, 5):
        qq = np.linalg.matrix_power(R72, s) @ LP[i]; j = int(np.argmin(np.linalg.norm(LP - qq, axis=1)))
        r.append(j if np.linalg.norm(LP[j] - qq) < 1e-6 else None)
    return r
def forced(i): return any(j is not None and state(loc[i][1], loc[j][1]) == 'overlap' for j in ring(i))
rT = ring(iT)
out.append(f'    target ring-mates in the patch: {sum(j is not None for j in rT)}/4; vs ring-mates: {[state(XT, loc[j][1]) for j in rT if j is not None]}')
nb = [j for j in range(NL) if j != iT and np.linalg.norm(LP[j] - LP[iT]) < rmax]
hits = [(j, state(XT, loc[j][1])) for j in nb]; ov = [j for j, s in hits if s == 'overlap']; to = [j for j, s in hits if s == 'touch']
out.append(f'    nearby copies (centres within {rmax:.3f}): {len(nb)}; overlapping the target EXACTLY: {len(ov)}; touching exactly: {len(to)}')
for j in ov:
    zj = LP[j] @ ax; rj = np.linalg.norm(LP[j] - zj * ax)
    out.append(f'      overlaps: height {zj:.4f}, distance from axis {rj:.4f}, wedge {wedge(LP[j]) if rj > 1e-9 else "axis"}; '
               f'its own ring clashes with itself (forced silent): {forced(j)}')
# the chorus's greedy five-fold silencing on the patch (float gauge, as in chorus_exact_big)
n_f = np.array([f(n) / np.linalg.norm(f(n)) for _, n, d in PO]); d_f = np.array([d.f() / np.linalg.norm(f(n)) for _, n, d in PO])
gf = lambda D_: np.max((D_ @ n_f.T) / (2 * d_f), axis=-1)
alive = np.ones(NL, bool)
while True:
    cnt = {}
    for i in np.where(alive)[0]:
        gx = gf(LP - LP[i]); gx[i] = 9; gx[~alive] = 9
        for j in np.where(gx < 1 - 1e-9)[0]: cnt[i] = cnt.get(i, 0) + 1
    if not cnt: break
    i = max(cnt, key=lambda i: (cnt[i], np.linalg.norm(LP[i])))
    for qq in [np.linalg.matrix_power(R72, s) @ LP[i] for s in range(5)]:
        dd = np.linalg.norm(LP - qq, axis=1); j = int(np.argmin(dd))
        if dd[j] < 1e-6: alive[j] = False
out.append(f'    greedy five-fold silencing on the patch: silenced {int((~alive).sum())} of {NL}; target {"SILENCED" if not alive[iT] else "KEPT"}')
# exact check of the kept copies around the target
kept_ov = [j for j in ov if alive[j]]
out.append(f'    after silencing, kept copies overlapping the target: {len(kept_ov)}; overlapping neighbours silenced: {sum(not alive[j] for j in ov)}/{len(ov)}')
# core-plane check on the patch: the plane sites in the patch, silent vs the two windows
nP_ = cross(v, X0)
pl = [i for i in range(NL) if (np.linalg.norm(LP[i] - (LP[i] @ ax) * ax) < 1e-9 or wedge(LP[i]) == k0) and dot(nP_, loc[i][1]) == Q(0)]
rows = []
for i in sorted(pl, key=lambda i: LP[i] @ ax):
    t = dot(loc[i][1], w); tt = (t * t / dot(w, w)).f() ** .5; inL = 0 <= t.f() < Lw.f(); inC = 0 <= t.f() and (t * t / dot(w, w) - tc2).f() < 0
    if tt < 1.6 and abs(LP[i] @ ax - hT) < HW - 2.5:
        rows.append(f'      h {LP[i] @ ax:8.4f}  t {tt:.4f}  canonical {"silent" if inL else "kept  "}  ring-clash {"silent" if inC else "kept  "}  patch greedy {"silent" if not alive[i] else "kept"}')
out.append('    core-plane sites near the target (interior of the patch):'); out += rows
print('\n'.join(out)); open('data/chorus-h128.txt', 'w').write('\n'.join(out) + '\n')
