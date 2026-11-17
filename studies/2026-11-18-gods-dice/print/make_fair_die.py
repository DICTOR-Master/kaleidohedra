"""Print model of the fair 14-face die (God's Dice, test 3). DICTO, 18 Nov 2026.
P(mu) = [-1,1]^3 ∩ {|x|+|y|+|z| <= mu}, mu_f = 1 + sqrt(2 tan(pi/14) tan(2pi/7)).
Checks: corner count, face count, every face's solid angle from the centre = 4pi/14 (to 1e-12), volume.
Writes a binary STL scaled so opposite squares are SIZE_MM apart, and a preview PNG. Ends FINAL ok / FINAL FAIL."""
import sys, itertools, struct, math
import numpy as np
from scipy.spatial import ConvexHull
SIZE_MM = float(sys.argv[1]) if len(sys.argv) > 1 else 30.0
mu = 1 + math.sqrt(2*math.tan(math.pi/14)*math.tan(2*math.pi/7))
b = mu - 1
V = set()
for s in itertools.permutations([1.0, b, 0.0]):
    for sg in itertools.product([1, -1], repeat=3):
        V.add(tuple(round(c*g, 15) + 0.0 for c, g in zip(s, sg)))
V = np.array(sorted(V))
hull = ConvexHull(V)
# group triangles into faces by plane
faces = {}
for simp, eq in zip(hull.simplices, hull.equations):
    key = tuple(np.round(eq, 9))
    faces.setdefault(key, []).append(simp)
def solid_angle(tri):  # Van Oosterom–Strackee, centre at origin
    a, b_, c = tri; la, lb, lc = map(np.linalg.norm, (a, b_, c))
    num = abs(np.dot(a, np.cross(b_, c)))
    den = la*lb*lc + np.dot(a, b_)*lc + np.dot(a, c)*lb + np.dot(b_, c)*la
    return 2*math.atan2(num, den)
ok = True
print(f"mu_f = {mu:.13f}; corners {len(V)}; faces {len(faces)}")
ok &= len(V) == 24 and len(faces) == 14
for key, tris in faces.items():
    om = sum(solid_angle(V[t]) for t in tris)
    kind = "square " if max(abs(np.array(key[:3]))) > 0.99 else "hexagon"
    dev = om/(4*math.pi) - 1/14
    print(f"  {kind} normal {np.round(key[:3],4)}  p = {om/(4*math.pi):.15f}  (p - 1/14 = {dev:+.1e})")
    ok &= abs(dev) < 1e-12
print(f"volume (unit half-width 1) = {hull.volume:.12f}")
k = SIZE_MM/2
with open("fair-14-die.stl", "wb") as f:
    f.write(b"DICTO fair 14-face die, God's Dice 2026-11-18, mm".ljust(80, b" "))
    f.write(struct.pack("<I", len(hull.simplices)))
    for simp, eq in zip(hull.simplices, hull.equations):
        p = V[simp]*k; n = eq[:3]
        if np.dot(np.cross(p[1]-p[0], p[2]-p[0]), n) < 0: p = p[[0, 2, 1]]
        f.write(struct.pack("<3f", *n)); [f.write(struct.pack("<3f", *q)) for q in p]; f.write(b"\0\0")
print(f"STL: fair-14-die.stl, {len(hull.simplices)} triangles, {SIZE_MM:g} mm between opposite squares, "
      f"{hull.volume*k**3/1000:.2f} cm^3")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(6, 6)); ax = fig.add_subplot(111, projection="3d")
for key, tris in faces.items():
    sq = max(abs(np.array(key[:3]))) > 0.99
    pts = np.unique(np.concatenate([V[t] for t in tris]), axis=0)
    n = np.array(key[:3]); c = pts.mean(0); u = pts[0]-c; u /= np.linalg.norm(u); w = np.cross(n, u)
    pts = pts[np.argsort([math.atan2(np.dot(q-c, w), np.dot(q-c, u)) for q in pts])]
    ax.add_collection3d(Poly3DCollection([pts], facecolor="#c9a227" if sq else "#7a4fb0", edgecolor="k", linewidth=1.2))
ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1); ax.set_box_aspect((1, 1, 1)); ax.axis("off")
ax.view_init(22, 35)
fig.text(0.5, 0.06, f"Fair 14-face die  μ = {mu:.6f}  every face 1/14", ha="center")
fig.text(0.97, 0.02, "DICTO", ha="right", fontsize=9)
fig.savefig("fair-14-die.png", dpi=150, bbox_inches="tight")
print("FINAL ok" if ok else "FINAL FAIL")
