# Cross-sections through the OG centre of the complete golden fill at three brick sizes (DICTO 5 Nov 2026): OG teal, skin orange, golden bricks gold.
import json, itertools, numpy as np, manifold3d as m3, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
O = np.array(json.load(open("/home/dicto/study-runs/og-pent/og/data/network.json"))["ocd"]); O = O - O.mean(0)
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float).tolist()); OG = hull(O); r = np.linalg.norm(O, axis=1)
tips = O[r > r.max() - 1e-6]; ax = []
for p in tips/np.linalg.norm(tips, axis=1)[:, None]:
    if not any(abs(abs(p @ q) - 1) < 1e-6 for q in ax): ax.append(p)
ax = np.array(ax); tri = next(q for q in itertools.combinations(range(6), 3) if all(abs(abs(ax[i] @ ax[j]) - 1/5**0.5) < 1e-6 for i, j in itertools.combinations(q, 2)))
E = np.array([ax[k] for k in tri])
for k in (1, 2):
    if E[0] @ E[k] < 0: E[k] = -E[k]
t = 1.390323; U = np.array(list(itertools.product((0, 1), repeat=3)), float)
def polys(M):
    try: return [np.array(p) for p in M.slice(0.0).to_polygons()]
    except Exception: return []
fig, axs = plt.subplots(1, 3, figsize=(15, 5.6), facecolor="white")
for axp, m in zip(axs, (8, 12, 24)):
    a = t/m; env = {tuple(b) for b in np.load(f"touch-m{m}.npy")}; brick = lambda b: (np.array(b, float) + U) @ (a*E)
    allb = list(env); lo = np.min(allb, 0) - 2; hi = np.max(allb, 0) + 2
    for b in itertools.product(*[range(l, h + 1) for l, h in zip(lo, hi)]):
        C = brick(b)
        if C[:, 2].min() > 0 or C[:, 2].max() < 0 or np.linalg.norm(C.mean(0)[:2]) > r.max()*1.3: continue
        Mb = hull(C); inside = b in env
        for P in polys(Mb - OG if inside else Mb):
            axp.add_patch(Polygon(P, closed=True, fc="#f08c33" if inside else "#d9ad3c", ec="#6b4a12", lw=0.25))
    for P in polys(OG): axp.add_patch(Polygon(P, closed=True, fc="#4fa3a5", ec="#1e4f50", lw=0.6))
    R = r.max()*1.25; axp.set_xlim(-R, R); axp.set_ylim(-R, R); axp.set_aspect("equal"); axp.axis("off")
    axp.set_title(f"brick edge t/{m}", fontsize=10)
fig.text(0.5, 0.02, "Sections through the OG: OG (teal), its golden skin (orange) and whole golden rhombohedra (gold). A complete fill at every size;\nthe skin halves with the brick edge and never vanishes (exact Dehn invariant).  DICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=9, color="#333")
plt.savefig("golden-skin-sections.png", dpi=125, bbox_inches="tight"); print("FINAL ok")
