# Cutaway of the complete golden fill around the original OG (DICTO 5 Nov 2026): OG (teal), its golden skin (orange: the bricks it touches,
# minus the OG), whole golden rhombohedra (gold). Half of space removed (above a plane through the OG centre) to see inside.
import json, itertools, numpy as np, manifold3d as m3, matplotlib, sys; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
O = np.array(json.load(open("/home/dicto/study-runs/og-pent/og/data/network.json"))["ocd"]); O = O - O.mean(0)
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float).tolist()); OG = hull(O)
m = int(sys.argv[1]) if len(sys.argv) > 1 else 12
env = np.load(f"touch-m{m}.npy"); D = np.load("skin-m3.npz") if False else None
import importlib.util
r = np.linalg.norm(O, axis=1); tips = O[r > r.max() - 1e-6]; ax = []
for p in tips/np.linalg.norm(tips, axis=1)[:, None]:
    if not any(abs(abs(p @ q) - 1) < 1e-6 for q in ax): ax.append(p)
ax = np.array(ax); tri = next(q for q in itertools.combinations(range(6), 3) if all(abs(abs(ax[i] @ ax[j]) - 1/5**0.5) < 1e-6 for i, j in itertools.combinations(q, 2)))
E = np.array([ax[k] for k in tri])
for k in (1, 2):
    if E[0] @ E[k] < 0: E[k] = -E[k]
t = 1.390323; a = t/m; U = np.array(list(itertools.product((0, 1), repeat=3)), float)
brick = lambda b: (np.array(b, float) + U) @ (a*E)
Env = m3.Manifold.batch_boolean([hull(brick(b)) for b in env], m3.OpType.Add); Skin = Env - OG
cut = lambda M: M.trim_by_plane([0, 0, -1], -0.0)                  # keep z <= 0
envset = {tuple(b) for b in env}; lo, hi = env.min(0) - 1, env.max(0) + 1
whole = [b for b in itertools.product(*[range(l, h + 1) for l, h in zip(lo, hi)]) if b not in envset and np.linalg.norm(brick(b).mean(0)) < r.max()*1.25]
W = m3.Manifold.batch_boolean([hull(brick(b)) for b in whole], m3.OpType.Add)
def tris(M):
    mm = M.to_mesh(); V = np.array(mm.vert_properties)[:, :3]; return V[np.array(mm.tri_verts)]
def shade(T, col):
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
    k = 0.4 + 0.6*np.abs(n @ (np.array([0.4, -0.5, 0.75])/np.linalg.norm([0.4, -0.5, 0.75]))); return [tuple(np.array(col)*x) for x in k]
fig = plt.figure(figsize=(14, 7), facecolor="white")
for i, (title, parts) in enumerate((("the OG in its golden skin (cut open)", [(cut(OG), (0.30, 0.64, 0.65)), (cut(Skin), (0.95, 0.55, 0.20))]),
                                     ("with the whole golden rhombohedra around (cut open)", [(cut(OG), (0.30, 0.64, 0.65)), (cut(Skin), (0.95, 0.55, 0.20)), (cut(W), (0.85, 0.68, 0.20))]))):
    axx = fig.add_subplot(1, 2, i + 1, projection="3d")
    for M, col in parts:
        T = tris(M); axx.add_collection3d(Poly3DCollection(T, facecolors=shade(T, col), edgecolors="none"), autolim=False)
    R = r.max()*1.15; axx.set_xlim(-R, R); axx.set_ylim(-R, R); axx.set_zlim(-R, R); axx.set_box_aspect((1, 1, 1)); axx.axis("off"); axx.view_init(28, 35)
    axx.set_title(title, fontsize=10)
fig.text(0.5, 0.03, f"Complete fill around the original OG: OG (teal) + one golden skin (orange) + one golden rhombohedron (gold), brick edge t/{m}.\nFiner bricks: the skin halves with the brick edge and can be made as thin as wished, never zero (Dehn).  DICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=9, color="#333")
plt.savefig(f"golden-skin-m{m}.png", dpi=125, bbox_inches="tight"); print("FINAL ok")
