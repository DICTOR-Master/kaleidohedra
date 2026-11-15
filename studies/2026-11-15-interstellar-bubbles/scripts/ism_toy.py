"""Rung 5, a TOY (not a simulation of the interstellar medium): supernova-blown bubbles in a 2D periodic slice of gas.

Picture (after the three-phase picture of McKee & Ostriker 1977, ApJ 218, 148, and the superbubbles of clustered supernovae): explosion
sites appear at random places and times; each blows a hot, low-density bubble that grows (radius ~ age^0.4, the Sedov-Taylor law,
Sedov 1959 / Taylor 1950), stalls, and after a while cools and refills (radius shrinks to 0). A share of sites are clusters
(superbubbles) with a larger stall radius. Swept-up gas sits in a dense shell just outside each bubble, and the background is a
slowly changing lognormal density field (warm/cold gas). Overlapping hot regions join (bubbles merge into superbubbles), and a shell
lying inside another bubble's hot gas is gone.

Density (dimensionless, background median 1): inside any hot disc rho = EPS; elsewhere
rho = exp(SIG * G(x, t)) * (1 + SHELL * sum_i exp(-((r_i - R_i) / w_i)^2) [r_i > R_i]),  w_i = 0.15 R_i + 1 px.

CELL RULE (stated, and varied in the census): markers = connected regions (periodic, 4-adjacency) where rho < THETA, regions smaller
than AMIN pixels dropped; cells = watershed basins of log rho flooded from these markers (scikit-image), so every pixel of the slice
belongs to one cell and the dense shells and clouds are the walls. Cells are matched across frames by mutual largest overlap with
area lineage (the Sun stream's match()), so a new bubble inside a cell is a split by lineage, and joined hot regions are a merge."""
import numpy as np
from scipy import ndimage as ndi


class BubbleGas:
    def __init__(self, L=512, rate=14.0, rmed=12.0, rsig=0.4, f_cluster=0.2, cluster_boost=2.5, t_grow=3.0, t_life=10.0,
                 t_fade=5.0, eps=0.01, sig=0.5, shell=3.0, corr=6.0, key_every=20, seed=1):
        self.L, self.rate, self.rmed, self.rsig = L, rate, rmed, rsig
        self.fc, self.cb, self.tg, self.tl, self.tf = f_cluster, cluster_boost, t_grow, t_life, t_fade
        self.eps, self.sig, self.shell, self.corr, self.key_every = eps, sig, shell, corr, key_every
        self.rng = np.random.default_rng(seed)
        self.sites = []                                   # [t0, x, y, Rmax]
        self.keys = {}
        self.t = 0.0
        self.Y, self.X = np.mgrid[0:L, 0:L].astype(np.float64)

    def _key(self, k):
        if k not in self.keys:
            g = ndi.gaussian_filter(self.rng.standard_normal((self.L, self.L)), self.corr, mode='wrap')
            self.keys[k] = g / g.std()
            for old in [q for q in self.keys if q < k - 1]: del self.keys[old]
        return self.keys[k]

    def radius(self, a, R):
        if a < 0: return 0.0
        if a < self.tg: return R * (a / self.tg) ** 0.4
        if a < self.tg + self.tl: return R
        if a < self.tg + self.tl + self.tf: return R * (1 - (a - self.tg - self.tl) / self.tf)
        return 0.0

    def advance(self, dt=1.0):
        n = self.rng.poisson(self.rate * dt)
        for _ in range(n):
            R = self.rmed * np.exp(self.rsig * self.rng.standard_normal())
            if self.rng.random() < self.fc: R *= self.cb
            self.sites.append([self.t + dt * self.rng.random(), self.rng.random() * self.L, self.rng.random() * self.L, R])
        self.t += dt
        life = self.tg + self.tl + self.tf
        self.sites = [s for s in self.sites if self.t - s[0] < life]

    def density(self):
        L = self.L
        k = int(self.t // self.key_every); f = (self.t % self.key_every) / self.key_every
        G = np.cos(f * np.pi / 2) * self._key(k) + np.sin(f * np.pi / 2) * self._key(k + 1)     # keeps unit variance
        hot = np.zeros((L, L), bool); sh = np.zeros((L, L))
        for t0, x, y, Rm in self.sites:
            R = self.radius(self.t - t0, Rm)
            if R <= 0.5: continue
            w = 0.15 * R + 1.0; ext = int(R + 4 * w) + 1
            ix = (np.arange(int(x) - ext, int(x) + ext + 1)) % L; iy = (np.arange(int(y) - ext, int(y) + ext + 1)) % L
            dx = (ix - x + L / 2) % L - L / 2; dy = (iy - y + L / 2) % L - L / 2
            r = np.sqrt(dy[:, None] ** 2 + dx[None, :] ** 2)
            hot[np.ix_(iy, ix)] |= r < R
            sh[np.ix_(iy, ix)] += np.where(r >= R, np.exp(-((r - R) / w) ** 2), 0.0)
        rho = np.exp(self.sig * G) * (1 + self.shell * sh)
        rho[hot] = self.eps
        return rho, hot


def cells_from_density(rho, theta, amin, tiles):
    """The stated cell rule. Returns raw label map (1..n) or None when there is no marker."""
    mk = tiles.periodic_label(rho < theta)
    if amin > 1:
        sz = np.bincount(mk.ravel()); small = sz < amin; small[0] = False
        mk[small[mk]] = 0
        u, inv = np.unique(mk, return_inverse=True); mk = inv.reshape(mk.shape)
    if mk.max() < 2: return None
    lab = tiles.periodic_marker_watershed(np.log(rho), mk)
    u, inv = np.unique(lab, return_inverse=True)
    return (inv.reshape(lab.shape) + 1).astype(np.int64)
