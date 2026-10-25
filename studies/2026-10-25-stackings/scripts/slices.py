# Slice test: horizontal cross-sections of a mixed-stacking octahedral piece vs the cubic / hexagonal pieces at the same height
# above or below the site. Reports slice areas and whether each slice polygon is congruent (sorted side lengths and angles).
exec(open("halves.py").read().split("lams = ")[0])
from scipy.spatial import ConvexHull as CH
def slice_poly(V, z):
    import manifold3d as m3
    P = m3.Manifold.hull_points([list(map(float, v)) for v in V])
    cs = P.slice(float(z)); polys = cs.to_polygons()
    if not polys: return None
    pts = np.array(polys[0]); h = CH(pts); pts = pts[h.vertices]
    sides = np.sort(np.round(np.linalg.norm(np.roll(pts, -1, 0) - pts, axis=1), 6))
    return h.volume, len(pts), sides
def tag(c,o,me):
    return "CONGRUENT" if c else ("same area" if abs(o[0]-me[0])<1e-6 else "")
for word, lam in (("ABAC", 0.2083333333333333), ("ABAC", 0.1), ("ABAC", -0.25)):
    M, S = sites_of(word); i = 0; V = cellV(M, S, i, lam); pz = M[i][1][2]
    R = {}
    for rw in ("ABC", "AB"):
        RM, RS = ref[rw]; j = next(j for j, (k, p) in enumerate(RM) if k == "oct"); R[rw] = (cellV(RM, RS, j, lam), RM[j][1][2])
    zt = V[:, 2].max() - pz; zb = pz - V[:, 2].min()
    print(f"== {word} λ={lam:+.4f}: piece reaches +{zt:.4f} / −{zb:.4f}")
    for t in (0.15, 0.35, 0.6, 0.85):
        for side, sgn, ext in (("up", 1, zt), ("down", -1, zb)):
            z = sgn * t * ext; me = slice_poly(V, pz + z)
            if me is None: continue
            line = f"   {side:4s} {z:+.4f}: area {me[0]:.6f} n={me[1]}"
            for rw in ("ABC", "AB"):
                W, rz = R[rw]; o = slice_poly(W, rz + z)
                if o is None: line += f" | {rw}: none"; continue
                cong = me[1] == o[1] and np.allclose(me[2], o[2], atol=1e-5)
                line += f" | {rw}: area {o[0]:.6f} n={o[1]} {tag(cong, o, me)}"
            print(line)
