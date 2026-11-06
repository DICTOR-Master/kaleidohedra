"""Rung 1 gaps filled with gravel (DICTO 11-06 "keep climbing, fill the gaps then rung 2"; earlier "remove adaptors and infill or use
harmonics and 3D waves with a gravel-like mix"). Frame: the 1/1 approximant (icosahedra edge 1 on bcc, a = 2phi^2/3; periodic cube with
2 clusters). Gap = everything outside the icosahedra (17.93%). Gravel: tetrahedra, octahedra, cubes, icosahedra, dodecahedra at falling
sizes (edge 0.5 / phi^k), tried in the frame's own orientations (cubic + icosahedral share one frame here) and turned copies, placed
greedily at the darkest points of the 3D wave field first (field = solid * sin(kr)/(kr)). Score: share of the gap filled per step.
Voxels, float. Heartbeat per step, FINAL line. Usage: rung1_gravel.py [N] [steps] [golden]
DICTO 11-06 "can we grow golden skin inside": mode golden = #96's growth, golden rhombohedra (edges along 3 of the icosahedra's six
5-fold axes, prolate and oblate) in phi-steps (edge 0.16, /phi, ...), darkest wave points first; the leftover is the golden skin."""
import itertools, sys, time, numpy as np
from scipy.spatial import ConvexHull
t0 = time.time(); phi = (1 + 5 ** .5) / 2
N = int(sys.argv[1]) if len(sys.argv) > 1 else 72; steps = int(sys.argv[2]) if len(sys.argv) > 2 else 4
A = 2 * phi ** 2 / 3
g = (np.arange(N) + .5) / N * A
X = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3)
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
ICO = orbit((0, 1, phi)) / 2; OCT = orbit((1, 0, 0)) / np.sqrt(2)
TET = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / (2 * np.sqrt(2)); CUBE = np.array(list(itertools.product((-.5, .5), repeat=3)))
DOD = np.vstack([orbit((1, 1, 1)), orbit((0, 1 / phi, phi))]) / (2 / phi)
def eqs(V): return ConvexHull(V).equations
def wrap(d): return d - A * np.round(d / A)
eI = eqs(ICO); solid = np.zeros(len(X), bool)
for c in (np.zeros(3), np.ones(3) * A / 2):
    d = wrap(X - c); solid |= ((d @ eI[:, :3].T + eI[:, 3]) <= 0).all(1)
gap = ~solid
print(f"N={N}: icosahedra {solid.mean():.4f} (exact 0.8207), gap {gap.mean():.4f}", flush=True)
G = solid.reshape(N, N, N).astype(float)
xs = np.minimum(np.arange(N), N - np.arange(N)) * A / N
R = np.sqrt(xs[:, None, None] ** 2 + xs[None, :, None] ** 2 + xs[None, None, :] ** 2)
kk = 2 * np.pi / (A / 2)
J0 = np.where(R > 0, np.sin(kk * R) / np.maximum(kk * R, 1e-12), 1.0)
F = np.real(np.fft.ifftn(np.fft.fftn(G) * np.fft.fftn(J0))).ravel()
def rot(ax, t):
    ax = np.array(ax, float); ax /= np.linalg.norm(ax); K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
ORI = [np.eye(3), rot((0, 0, 1), np.pi / 2), rot((1, 1, 1), np.pi / 3), rot((0, 0, 1), np.pi / 4), rot((1, 0, 0), np.pi / 4)]
SH = {'T': TET, 'O': OCT, 'C': CUBE, 'I': ICO, 'D': DOD}; h = A / N
GOLD = len(sys.argv) > 3 and sys.argv[3] == 'golden'
ax5 = []
for p in ICO:
    u = p / np.linalg.norm(p)
    if not any(abs(abs(u @ q) - 1) < 1e-6 for q in ax5): ax5.append(u)
RH = []
for tri in itertools.combinations(range(6), 3):
    for sg in itertools.product((1, -1), repeat=2):
        E = np.array([ax5[tri[0]], sg[0] * ax5[tri[1]], sg[1] * ax5[tri[2]]]); RH.append(E)
def rh_template(E, e):
    Ev = e * E; cor = np.array([sum(Ev[k] * b for k, b in enumerate(bits)) for bits in itertools.product((0, 1), repeat=3)])
    ext = int(np.ceil(np.abs(cor).max() / h)) + 1; o = np.array(list(itertools.product(range(-ext, ext + 1), repeat=3)))
    co = (o * h) @ np.linalg.inv(Ev); ok = np.all((co >= 0) & (co < 1), axis=1); return o[ok]
def templates(V):
    out = []
    for Rm in ORI:
        W = V @ Rm.T; e = eqs(W); ext = int(np.ceil(np.abs(W).max() / h)) + 1
        o = np.array(list(itertools.product(range(-ext, ext + 1), repeat=3))); ok = ((o * h) @ e[:, :3].T + e[:, 3] <= 0).all(1)
        if ok.sum() >= 4: out.append(o[ok])
    return out
free = gap.reshape(N, N, N).copy(); G0 = free.sum()
cand = np.argwhere(free)[np.argsort(F[gap])]
for s in range(steps):
    size = (0.16 if GOLD else 0.5) / phi ** s; placed = {}
    for name, V in ({'rhomb': None}.items() if GOLD else SH.items()):
        for t in ([rh_template(E, size) for E in RH] if GOLD else templates(V * size)):
            if len(t) < 4: continue
            for a in cand:
                if not free[tuple(a)]: continue
                q = (a + t) % N
                if free[q[:, 0], q[:, 1], q[:, 2]].all(): free[q[:, 0], q[:, 1], q[:, 2]] = False; placed[name] = placed.get(name, 0) + 1
    print(f"HEARTBEAT step {s}: edge {size:.4f} placed {placed} -> gap filled {1 - free.sum()/G0:.3f} ({time.time()-t0:.0f}s)", flush=True)
print(f"FINAL ok gap filled {1 - free.sum()/G0:.3f}; space filled {solid.mean() + (1-free.sum()/G0)*gap.mean():.4f} {time.time()-t0:.0f}s")
