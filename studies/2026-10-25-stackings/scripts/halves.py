# Half-and-half check (DICTO 2026-10-25): an octahedral site sits half-way between two layers. Cut its cell by the horizontal plane
# through the site. Claim: in a mixed stacking each half is congruent to the same half of the cubic (ABC) or of the hexagonal (AB)
# piece at the same λ, chosen by the layer on that side. Tested on ABAC and ABCACB octahedral sites at the stops (−3/8, 5/24) and at
# sample λ on every stretch. Congruence by sorted pairwise corner distances of each half.
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open("congruent2.py").read().split("allp = []")[0])
def halves(V, pz):
    import manifold3d as m3
    P = m3.Manifold.hull_points([list(map(float, v)) for v in V])
    up = P.trim_by_plane([0, 0, 1], float(pz)); dn = P.trim_by_plane([0, 0, -1], float(-pz))
    pts = lambda m: np.unique(np.round(np.array(m.to_mesh().vert_properties)[:, :3] - np.array([0, 0, pz]), 7), axis=0)
    return pts(up), pts(dn), up.volume(), dn.volume()
def fps(W): return fp(W - W.mean(0))
ref = {}
for word in ("ABC", "AB"):
    M, S = sites_of(word); ref[word] = (M, S)
lams = [-0.375, -0.3, -0.2, -0.125, -0.05, 0.003266957, 0.1, 0.2083333333333333, 0.25, 0.33]
ok = bad = 0; NONE = "NONE"
for word in ("ABAC", "ABCACB"):
    M, S = sites_of(word)
    for lam in lams:
        lib = {}
        for rw in ("ABC", "AB"):
            RM, RS = ref[rw]
            for j, (k, p) in enumerate(RM):
                if k != "oct": continue
                V = cellV(RM, RS, j, lam)
                if V is None: continue
                u, d, vu, vd = halves(V, p[2]); lib.setdefault((rw, "up"), fps(u)); lib.setdefault((rw, "down"), fps(d))
        for i, (k, p) in enumerate(M):
            if k != "oct": continue
            V = cellV(M, S, i, lam)
            if V is None: continue
            u, d, vu, vd = halves(V, p[2]); fu, fd = fps(u), fps(d)
            mu = [key for key, f in lib.items() if key[1] == "up" and len(f) == len(fu) and np.allclose(f, fu, atol=2e-5)]
            md = [key for key, f in lib.items() if key[1] == "down" and len(f) == len(fd) and np.allclose(f, fd, atol=2e-5)]
            good = bool(mu) and bool(md); ok += good; bad += (not good)
            if not good or lam in (-0.375, 0.2083333333333333):
                print(f"{word} λ={lam:+.4f} oct site {i}: corners {len(V)}, upper half = {[m[0] for m in mu] or NONE}, lower half = {[m[0] for m in md] or NONE}")
print(f"halves matched: {ok}, unmatched: {bad}")
