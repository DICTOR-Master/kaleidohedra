# Step 24 (DICTO: "test whether the core has a nameable shape"). Uses the exact radius-8 chorus (data/chorus-exact-r8.json).
# (1) the silent copies near the axis: positions along the axis, angles, spacings; (2) the empty channel: grid points within
# rho < 2.5 of the axis not inside any kept copy; its cross-section profile, outline and repeat along the axis. Float readout of exact sites.
import sys, io, os, contextlib, json, numpy as np
from scipy.spatial import ConvexHull
DATA = sys.argv[1] if len(sys.argv) > 1 else 'data/chorus-exact-r8.json'
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
os.chdir(here)
Of = np.array([[x.f() for x in v] for v in dict(rev)['dual of the Hecatodihedron']])
E = ConvexHull(Of).equations; N, d = E[:, :3], -E[:, 3]                       # inside: N.x <= d
D = json.load(open(DATA)); K = np.array(D['sites']); S = np.array(D['silenced']); R = D['RAD']
a5, e1, e2, th0 = np.array(D['a5']), np.array(D['e1']), np.array(D['e2']), D['th0']; phi = (1 + 5 ** .5) / 2
cyl = lambda X: (X @ e1, X @ e2, X @ a5)
out = [f'radius {R} run: {len(K)} kept, {len(S)} silent; OCD circumradius {np.linalg.norm(Of, axis=1).max():.4f}, inradius {d.min() / np.linalg.norm(N, axis=1).max():.4f}']
# (1) silent copies near the axis
sx, sy, sz = cyl(S); rho = np.hypot(sx, sy); ang = np.degrees(np.arctan2(sy, sx) - th0) % 72
core = rho < 1.05
out.append(f'silent copies within 1.05 of the axis: {int(core.sum())}')
for r0 in sorted(set(np.round(rho[core], 4))):
    m = core & (np.abs(rho - r0) < 1e-3)
    zs = np.sort(sz[m]); out.append(f'  ring at distance {r0:.4f} from the axis: {int(m.sum())} copies, angles within each 72° wedge {sorted(set(np.round(ang[m], 2)))}, heights {list(np.round(zs, 4))}')
zc = np.sort(sz[core]); gz = np.unique(np.round(np.diff(np.unique(np.round(zc, 4))), 4))
out.append(f'  distinct height gaps between core silences: {list(gz)}' + (f'; ratios to smallest {list(np.round(gz / gz.min(), 4))}' if len(gz) > 1 else ''))
# kept copies nearest the axis: who walls the channel
kx, ky, kz = cyl(K); kr = np.hypot(kx, ky)
out.append(f'kept copies nearest the axis: distances {sorted(set(np.round(kr, 4)))[:6]}')
# (2) the empty channel on a grid
zmax = R - 3.0; h = 0.05
xs = np.arange(-2.5, 2.5 + 1e-9, h); zs = np.arange(-zmax, zmax + 1e-9, h)
X, Y = np.meshgrid(xs, xs, indexing='ij'); disk = np.hypot(X, Y) <= 2.5
near = K[kr < 2.5 + 1.2]
area, free_r, outline = [], [], []
for z in zs:
    pts = (X[disk, None] * e1 + Y[disk, None] * e2) + z * a5
    pts = pts.reshape(-1, 3); inside = np.zeros(len(pts), bool)
    for s in near[np.abs(near @ a5 - z) < 1.2]:
        inside |= np.all((pts - s) @ N.T <= d + 1e-12, axis=1)
    empty = ~inside; area.append(empty.sum() * h * h)
    pr = np.hypot(X[disk], Y[disk]); free_r.append(pr[inside].min() if inside.any() else 2.5)
    # outline: free radius by direction (36 sectors)
    pa = np.degrees(np.arctan2(Y[disk], X[disk]) - th0) % 360
    outline.append([pr[inside & (np.abs(((pa - a0 + 180) % 360) - 180) < 5)].min() if (inside & (np.abs(((pa - a0 + 180) % 360) - 180) < 5)).any() else 2.5 for a0 in range(0, 360, 10)])
area = np.array(area); free_r = np.array(free_r); outline = np.array(outline)
out.append(f'empty channel (grid {h}, within 2.5 of the axis, |z| < {zmax:g}): cross-section area min {area.min():.3f}, mean {area.mean():.3f}, max {area.max():.3f}')
out.append(f'  clear radius (largest empty disc on the axis): min {free_r.min():.3f}, mean {free_r.mean():.3f}, max {free_r.max():.3f}; is the axis itself ever covered? {bool((free_r < h).any())}')
# outline symmetry: average over z of outline by direction, folded mod 72 and mod 36
ol = outline.mean(0); out.append(f'  mean clear radius by direction (0, 10, ..., 350 deg from the first boundary): {list(np.round(ol, 2))}')
out.append(f'  five-fold variation (std over the 5 copies of each direction): {np.mean([np.std(ol[i::7]) for i in range(7)]):.3f}  (direction-to-direction std {np.std(ol):.3f})')
# repeat along the axis: autocorrelation of the area profile
a = area - area.mean(); ac = np.correlate(a, a, 'full')[len(a) - 1:]; ac /= ac[0]
peaks = [i for i in range(2, len(ac) - 1) if ac[i] > ac[i - 1] and ac[i] >= ac[i + 1] and ac[i] > 0.3]
out.append(f'  area profile self-similarity: correlation peaks at shifts {[round(p * h, 3) for p in peaks[:8]]} (values {[round(ac[p], 2) for p in peaks[:8]]})')
print('\n'.join(out)); tag = os.path.basename(DATA).replace('chorus-exact-', '').replace('.json', '')
open(f'data/chorus-core-{tag}.txt', 'w').write('\n'.join(out) + '\n')
np.savez(f'data/chorus-core-{tag}.npz', zs=zs, area=area, free_r=free_r, outline=outline)
