"""DICTO 11-06: "we only need to get them all in octet and then make the adaptors out of the pieces themselves"; then "remove adaptors and
infill, or use harmonics and 3D waves with a gravel-like mix". Step 1: the octet (tetrahedra and octahedra, edge 1) as the frame; the
tetrahedra stay whole; each octahedron holds an icosahedron in Pacioli's position (edge sqrt2/phi^2, as in #47); the gap (where #47's
Admiral Caps were) is filled by GRAVEL: Platonic solids at falling sizes, placed greedily at the darkest points of the 3D wave field
first (field = solid * sin(kr)/(kr), as #96), in the octet's own orientations and the icosahedron's. Score: share of the gap filled per
step. Voxels, float: a first look, not exact. Usage: gravel.py [N] [steps]"""
import itertools, sys, time, numpy as np
from scipy.spatial import ConvexHull
t0 = time.time(); phi = (1 + 5 ** .5) / 2
N = int(sys.argv[1]) if len(sys.argv) > 1 else 96
A = np.sqrt(2)                                   # fcc cube side for octet edge 1
g = (np.arange(N) + .5) / N * A
X = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3)
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
ICO = orbit((0, 1, phi)); ICO /= 2                # edge 1
OCT = orbit((1, 0, 0)) / np.sqrt(2)               # edge 1
TET = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / (2 * np.sqrt(2))
CUBE = np.array(list(itertools.product((-.5, .5), repeat=3)))
DOD = np.vstack([orbit((1, 1, 1)), orbit((0, 1 / phi, phi))]) / (2 / phi)   # edge 1
def halfspaces(V):
    h = ConvexHull(V); return h.equations
def inside(eqs, P, c): return ((P - c) @ eqs[:, :3].T + eqs[:, 3] <= 1e-9).all(1)
def wrap(d): return d - A * np.round(d / A)
# octahedral holes of fcc (cube side A): body centre + edge midpoints
octc = [np.array([.5, .5, .5]) * A] + [np.array(p) * A for p in [(.5, 0, 0), (0, .5, 0), (0, 0, .5)]]
ice = halfspaces(ICO * (np.sqrt(2) / phi ** 2))   # Pacioli: icosahedron of edge sqrt2/phi^2 in the octahedron of edge 1 (#47 scaled)
solid = np.zeros(len(X), bool)
for c in octc:
    d = wrap(X - c); solid |= ((d @ ice[:, :3].T + ice[:, 3]) <= 0).all(1)
# the octahedra themselves (to know the gap = octahedra minus icosahedra)
oce = halfspaces(OCT)
inoct = np.zeros(len(X), bool)
for c in octc:
    d = wrap(X - c); inoct |= ((d @ oce[:, :3].T + oce[:, 3]) <= 1e-12).all(1)
gap = inoct & ~solid
print(f"N={N}: octahedra {inoct.mean():.4f} (exact {4*(np.sqrt(2)/3)/A**3:.4f}), icosahedra {solid.mean():.4f}, gap {gap.mean():.4f} of space", flush=True)
# wave field: frame (tetrahedra + icosahedra) convolved with j0, wavelength = octet edge / 2
frame = (~inoct) | solid
G = frame.reshape(N, N, N).astype(float)
k = np.fft.fftfreq(N, d=A / N) * 2 * np.pi
K = np.sqrt(sum(np.meshgrid(k, k, k, indexing='ij')[i] ** 2 for i in range(3)))
r = np.sqrt(sum(np.minimum(np.arange(N), N - np.arange(N))[:, None, None] ** 2 * 0 + 0 for _ in range(1)))
lam = 0.5; kk = 2 * np.pi / lam
xs = np.minimum(np.arange(N), N - np.arange(N)) * A / N
R = np.sqrt(xs[:, None, None] ** 2 + xs[None, :, None] ** 2 + xs[None, None, :] ** 2)
J0 = np.where(R > 0, np.sin(kk * R) / np.maximum(kk * R, 1e-12), 1.0)
Fld = np.real(np.fft.ifftn(np.fft.fftn(G) * np.fft.fftn(J0))).ravel()
# orientations: octet frame (identity) and the icosahedron's frame (identity for ICO coordinates here: same axes), plus turned copies
def rot(ax, t):
    ax = np.array(ax, float); ax /= np.linalg.norm(ax); Kx = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + np.sin(t) * Kx + (1 - np.cos(t)) * Kx @ Kx
ORI = [np.eye(3), rot((1, 1, 1), np.pi / 3), rot((0, 0, 1), np.pi / 4), rot((1, 0, 0), np.pi / 4), rot((0, 1, 0), np.pi / 4)]
SHAPES = {'T': TET, 'O': OCT, 'C': CUBE, 'I': ICO, 'D': DOD}
h = A / N
def template(V):
    out = []
    for Rm in ORI:
        W = V @ Rm.T; eq = halfspaces(W); ext = int(np.ceil(np.abs(W).max() / h)) + 1
        o = np.array(list(itertools.product(range(-ext, ext + 1), repeat=3)))
        P = o * h; ok = ((P @ eq[:, :3].T + eq[:, 3]) <= 0).all(1)
        if ok.sum() >= 4: out.append(o[ok])
    return out
free = gap.reshape(N, N, N).copy(); G0 = free.sum()
order = np.argsort(Fld[gap.ravel()]); cand = np.argwhere(gap.reshape(N, N, N))[order]
steps = int(sys.argv[2]) if len(sys.argv) > 2 else 4
tally = []
for s in range(steps):
    size = 0.5 / phi ** s                                    # gravel edge: 0.5, 0.5/phi, ...
    placed = {}
    for name, V in SHAPES.items():
        T = template(V * size)
        for a in cand:
            if not free[tuple(a)]: continue
            for t in T:
                q = (a + t) % N
                if free[q[:, 0], q[:, 1], q[:, 2]].all():
                    free[q[:, 0], q[:, 1], q[:, 2]] = False; placed[name] = placed.get(name, 0) + 1; break
    filled = 1 - free.sum() / G0; tally.append((size, placed, filled))
    print(f"step {s}: edge {size:.4f} placed {placed} -> gap filled {filled:.3f} ({time.time()-t0:.0f}s)", flush=True)
print(f"FINAL ok gap filled {tally[-1][2]:.3f} {time.time()-t0:.0f}s")
