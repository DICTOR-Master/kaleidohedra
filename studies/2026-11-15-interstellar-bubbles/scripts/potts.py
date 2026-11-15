"""Cellular Potts foam on a periodic grid, 2D or 3D: rungs 1-4 of the foam ladder (DICTO 15 Nov 2026: "simplest most basic foam and
bubbles upwards").

Model (credited at the point of use): the large-Q Potts model of a coarsening soap froth, each bubble a domain of one label, energy =
number of unlike neighbour pairs (Glazier, Gross & Stavans 1987 used it for 2D froth; Anderson, Srolovitz, Grest & Sahni 1984 for grain
growth; Glazier 1993 in 3D), with the area-constraint term of the cellular Potts model (Graner & Glazier 1992) for (a) the liquid of a
wet foam (rung 2) and (b) bubbles fed with gas after they nucleate (rung 4). Interactions reach the 8 (2D) or 26 (3D) nearest sites to
reduce lattice anisotropy. Updates: Metropolis at temperature T with "copy a neighbour's label" proposals, applied to the 2^d parity
sub-lattices in turn (no two sites of a sub-lattice interact), so the sweep is vectorised. Time unit: one Monte Carlo step (MCS) =
one attempt per site.

Energy H = sum over neighbour pairs J(a, b) + sum over constrained labels lam_l (A_l - target_l)^2,
J(a, a) = 0, J(bubble, bubble') = 1, J(bubble, liquid) = Jbl, liquid = label 0 (only in wet runs).
The area term uses the areas at the start of each sub-lattice sweep (a standard approximation for parallel updates)."""
import numpy as np
from scipy.spatial import cKDTree
import itertools


def voronoi_labels(shape, n, rng):
    """Periodic Voronoi label map of n random seeds (labels 1..n)."""
    pts = rng.random((n, len(shape))) * np.array(shape)
    grid = np.stack(np.meshgrid(*[np.arange(s) + 0.5 for s in shape], indexing='ij'), -1).reshape(-1, len(shape))
    tree = cKDTree(pts, boxsize=np.array(shape, float))
    _, idx = tree.query(grid)
    return (idx + 1).reshape(shape).astype(np.int64)


class Potts:
    def __init__(self, lab, T=0.3, Jbl=None, rng=None, nmax=None):
        self.lab = lab.astype(np.int64)
        self.d = lab.ndim
        self.T, self.Jbl = T, Jbl                        # Jbl None = dry foam
        self.rng = rng or np.random.default_rng(0)
        self.offs = [o for o in itertools.product((-1, 0, 1), repeat=self.d) if any(o)]
        self.subs = list(itertools.product((0, 1), repeat=self.d))
        n = int(nmax or (self.lab.max() + 1))
        self.lam = np.zeros(n); self.target = np.zeros(n)
        self.t = 0

    def grow(self, n):
        if n > len(self.lam):
            k = max(n, 2 * len(self.lam))
            self.lam = np.concatenate([self.lam, np.zeros(k - len(self.lam))])
            self.target = np.concatenate([self.target, np.zeros(k - len(self.target))])

    def _J(self, x, y):
        if self.Jbl is None: return (x != y).astype(np.float64)
        return np.where(x == y, 0.0, np.where((x == 0) | (y == 0), self.Jbl, 1.0))

    def sweep(self):
        lab = self.lab
        for s in self.subs:
            sl = tuple(slice(a, None, 2) for a in s)
            nb = np.stack([np.roll(lab, tuple(-o for o in off), axis=tuple(range(self.d)))[sl] for off in self.offs])
            old = lab[sl]
            k = self.rng.integers(0, len(self.offs), size=old.shape)
            cand = np.take_along_axis(nb, k[None], 0)[0]
            m = cand != old
            if not m.any(): continue
            o, c, N = old[m], cand[m], nb[:, m]
            dE = self._J(c[None], N).sum(0) - self._J(o[None], N).sum(0)
            if self.lam.any():
                A = np.bincount(lab.ravel(), minlength=len(self.lam)).astype(np.float64)
                dE += self.lam[o] * (-2 * (A[o] - self.target[o]) + 1) + self.lam[c] * (2 * (A[c] - self.target[c]) + 1)
            acc = (dE <= 0) | (self.rng.random(dE.shape) < np.exp(-np.clip(dE, 0, 50) / max(self.T, 1e-9)))
            if self.T <= 0: acc = (dE < 0) | ((dE == 0) & (self.rng.random(dE.shape) < 0.5))
            sub = old.copy(); idx = np.flatnonzero(m)[acc]
            sub.ravel()[idx] = c[acc]
            lab[sl] = sub
        self.t += 1
