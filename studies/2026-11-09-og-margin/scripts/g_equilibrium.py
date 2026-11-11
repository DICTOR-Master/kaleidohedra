# g_equilibrium.py, DICTO 11 Nov 2026 ("yes go ahead with G"). Is the cut share of the hop (~0.30 for the OG's generic classes, §37–38b)
# a property of the hop on fine near-round polytopes, independent of the start? Starts: (U) uniform random points on the unit sphere,
# (F) Fibonacci-spread points, each with radial noise s; (O) the OG's level 18 with its symmetry broken by a random nudge of 1e-7.
# Each start: up to 10 hops (stop at 300 000 faces). Per hop: faces F, cut share c/F (foot point not a hull corner), growth F'/F,
# R/r from O, and the identity c = F - (F' + 4 + e)/2 (e = sum over corners of P(D) of (degree - 3); generic sets have e = 0) as control.
# 11-11: pilot showed the cut share still rising at hop 9 (0.13 -> 0.315, growth 1.74 -> 1.37); this run goes to 16 hops / 4 M faces.
# usage: python -u g_equilibrium.py <five-fold-octet dir> <out.json>
import sys, os, json, time
import numpy as np
from scipy.spatial import ConvexHull
here = os.path.dirname(os.path.abspath(__file__)); OUTJ = os.path.abspath(sys.argv[2])
def hull_faces(V, tol=1e-12):
    h = ConvexHull(V); E = h.equations; n = len(E)
    a = np.repeat(np.arange(n), 3); b = h.neighbors.ravel(); same = np.abs(E[a] - E[b]).max(1) < tol
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    nc, lab = connected_components(coo_matrix((np.ones(int(same.sum())), (a[same], b[same])), shape=(n, n)), directed=False)
    Nf = np.zeros((nc, 3)); np.add.at(Nf, lab, E[:, :3]); Nf /= np.linalg.norm(Nf, axis=1)[:, None]
    Dd = np.zeros(nc); cnt = np.bincount(lab); np.add.at(Dd, lab, -E[:, 3]); Dd /= cnt
    return Nf, Dd, np.unique(h.vertices), h
def hop_series(V, tag, hops=16):
    rows = []; ok = True
    Nf, Dd, cor, h = hull_faces(V)
    for k in range(hops):
        F = len(Nf); W = Nf * Dd[:, None]                                    # foot points = candidates
        Nf2, Dd2, cor2, h2 = hull_faces(W); F2 = len(Nf2); c = F - len(cor2)
        deg = np.bincount(h2.simplices.ravel(), minlength=len(W))[cor2]     # triangles per corner ~ degree for simplicial-ish hulls
        Rr = float(np.linalg.norm(V[cor], axis=1).max() / Dd.min())
        ident = F - (F2 + 4) / 2                                            # = c when e = 0
        rows.append(dict(tag=tag, k=k, F=F, cut=c, share=c / F, growth=F2 / F, Rr=Rr, identity_gap=float(c - ident)))
        print(f'  {tag:28s} hop {k}: F {F:7d} cut {c / F:.3f} growth {F2 / F:.3f} R/r {Rr:.4f} | c - (F - (F\'+4)/2) = {c - ident:+.1f}', flush=True)
        V, Nf, Dd, cor, h = W, Nf2, Dd2, cor2, h2
        json.dump(allrows + rows, open(OUTJ, 'w'))
        if F2 > 4000000: break
    return rows
rng = np.random.default_rng(11); allrows = []; t0 = time.time()
def unit(n): x = rng.normal(size=(n, 3)); return x / np.linalg.norm(x, axis=1)[:, None]
def fib(n):
    i = np.arange(n) + .5; z = 1 - 2 * i / n; a = np.pi * (1 + 5 ** .5) * i; return np.stack([np.sqrt(1 - z * z) * np.cos(a), np.sqrt(1 - z * z) * np.sin(a), z], 1)
# 11-11 after the pilot (cut share still rising at hop 9): long runs, 16 hops, up to 4 M faces, fewer starts
for n in (2000,):
    for s in (0.001, 0.05):
        for name, base in (('U', unit(n)), ('F', fib(n))):
            V = base * (1 + s * rng.uniform(-1, 1, (n, 1)))
            allrows += hop_series(V, f'{name} n={n} noise={s}')
            print(f'PROGRESS {len(allrows) / 80:.3f}', flush=True)
# the OG's level 18, symmetry broken
sys.argv = ['x', sys.argv[1], '0', '/dev/null']; exec(open(os.path.join(here, 'og_sweep.py')).read().split('rows_out = []')[0])
V = OGf; FF = faces(V)
for k in range(18):
    M, Dd_, cor_ = FF; W = symmetrise(M * Dd_[:, None]); FF = faces(W)
M, Dd_, cor_ = FF; V18 = M * Dd_[:, None]
V18 = V18 * (1 + 1e-7 * np.random.default_rng(5).uniform(-1, 1, (len(V18), 1)))
allrows += hop_series(V18, 'OG level 18 (nudged 1e-7)')
json.dump(allrows, open(OUTJ, 'w'), indent=1)
late = [r for r in allrows if r['k'] >= 4 and r['F'] > 5000]
print(f'late hops (k >= 4, F > 5000): {len(late)}; cut share mean {np.mean([r["share"] for r in late]):.3f}, range {min(r["share"] for r in late):.3f}-{max(r["share"] for r in late):.3f}; growth mean {np.mean([r["growth"] for r in late]):.3f}')
bytag = {}
for r in late: bytag.setdefault(r['tag'].split(' ')[0] if not r['tag'].startswith('OG') else 'OG', []).append(r['share'])
print('by start kind:', {k: (round(float(np.mean(v)), 3), len(v)) for k, v in bytag.items()})
gaps = [abs(r['identity_gap']) for r in allrows if not r['tag'].startswith('OG')]
ok = max(gaps) < 1e-9 if gaps else True
print('identity c = F - (F\'+4)/2 exact for the generic starts:', ok)
print('FINAL ok' if ok else 'FINAL FAIL: growth identity violated on a generic start (degenerate corners or hull error)')
