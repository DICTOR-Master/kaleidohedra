# DICTO 2026-10-21: growing the B1NR + icosidodecahedron packing ("two vertical pairs, two horizontal" = how to grow it). Start: the
# float-fit B1NR with six IDs (b1nr_id.py). For every free pentagon of one ID, try a B1NR on it in every orientation (any of its six
# pentagons, five turns, either hand) and keep the clash-free ones; then list where the free sites sit round that ID (up/down
# relative to the B1NR's 3-fold axis, z), to compare with DICTO's two vertical pairs and two horizontal.
import os, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'b1nr_id.py')).read(); exec(src[:src.index("np.save(os.path.join(HERE, 'b1nr-regpent.npy')")])
k0 = 0; W0 = IDs[k0]; c0 = W0.mean(0)
used = [i for i, f in enumerate(IF) if len(f) == 5 and np.linalg.norm((W0[f].mean(0) - c0) / np.linalg.norm(W0[f].mean(0) - c0) - (-c0 / np.linalg.norm(c0))) < 0.3]
hullB = Delaunay(B); others = [B] + [W for i, W in enumerate(IDs) if i != k0]
def inside(A, P): return (Delaunay(A).find_simplex(P) >= 0).mean()
def samples(W, n=3000):
    rng = np.random.default_rng(1); S = W[rng.integers(0, len(W), (n, 4))]; w = rng.dirichlet(np.ones(4), n); return (S * w[:, :, None]).sum(1)
sites = []
for fi, f in enumerate(IF):
    if len(f) != 5 or fi in used: continue
    Q = W0[f]; out = Q.mean(0) - c0; best = None
    for g in pents:
        for rot in range(5):
            for rev in (1, -1):
                order = [g[(rot + rev * k) % 5] for k in range(5)]; R, t = kabsch(B[order], Q); Bn = B @ R.T + t
                if (Bn.mean(0) - Q.mean(0)) @ out <= 0: continue
                mis = np.sqrt(((B[order] @ R.T + t - Q) ** 2).sum(1).mean()); S = samples(Bn)
                ov = max(max(inside(A, S) for A in others), max(inside(Bn, samples(A)) for A in others))
                if best is None or (ov, mis) < best[:2]: best = (ov, mis, Bn)
    d = out / np.linalg.norm(out); sites.append((fi, best[0], best[1], d, best[2]))
print(f'ID {k0}: centre {np.round(c0, 3)}; pentagon shared with the central B1NR: {used}')
for fi, ov, mis, d, _ in sorted(sites, key=lambda s: -s[3][2]):
    print(f'  pentagon {fi:2d}: direction {np.round(d, 3)} (elevation {np.degrees(np.arcsin(d[2])):6.1f} deg) | best B1NR overlap {ov:.3f}, misfit {mis:.3f}', '  FREE' if ov < 0.005 else '')
# DICTO's reading: two vertical pairs (same side, one up one down) and two near-horizontal; check the free sites against each other
free = [s_ for s_ in sites if s_[1] < 0.005]
print('pairwise B1NR-B1NR overlap among the free sites:')
for a, b in itertools.combinations(free, 2):
    ov = max(inside(a[4], samples(b[4])), inside(b[4], samples(a[4])))
    if ov > 0.005: print(f'  {a[0]:2d} x {b[0]:2d}: {ov:.3f}')
SET = [21, 4, 22, 6, 14, 15]
ok = all(max(inside(a[4], samples(b[4])), inside(b[4], samples(a[4]))) < 0.005 for a, b in itertools.combinations([s_ for s_ in free if s_[0] in SET], 2))
print('DICTO set', SET, '(two vertical pairs 21/4 and 22/6, two near-horizontal 14, 15) clash-free together:', ok)
