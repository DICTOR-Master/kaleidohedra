# Render the golden fill inside DICTO's Bull-horns OG adaptor (DICTO 5 Nov 2026): the adaptor (faint amber), the whole golden rhombohedra
# coloured by growth step, and one view with the six OGs that bite the adaptor.
import json, itertools, numpy as np, manifold3d as m3, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import HalfspaceIntersection
DD = json.load(open("/home/dicto/study-runs/og-pent/step10-input.json")); VV = np.array(DD["V"]); aa = 4*DD["R"]/3
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float).tolist())
h0 = np.array([aa/2, 0, 0]); holes = [np.array(q)*aa/2 for q in itertools.product(range(-5, 6), repeat=3) if sum(x % 2 for x in q) in (1, 2)]
hh = [np.r_[p - h0, -(p - h0) @ ((p + h0)/2)] for p in holes if 1e-9 < np.linalg.norm(p - h0) < 3*aa]
cellM = hull(HalfspaceIntersection(np.array(hh), h0).intersections)
sites = [np.array(q)*aa/2 for q in itertools.product(range(-4, 5), repeat=3) if len({x % 2 for x in q}) == 1]
OGM = hull(VV); bite = [p for p in sites if np.linalg.norm(p - h0) < 2.2*aa and (cellM ^ OGM.translate(list(p))).volume() > 1e-9]
Room = cellM - m3.Manifold.batch_boolean([OGM.translate(list(p)) for p in bite], m3.OpType.Add)
T = np.load("bh-tiles-s3.npy"); st = T[:, 0].astype(int); C = T[:, 1:].reshape(-1, 8, 3) - h0
def tris(M):
    mm = M.to_mesh(); V = np.array(mm.vert_properties)[:, :3] - h0; return V[np.array(mm.tri_verts)]
L = np.array([0.4, -0.5, 0.75]); L /= np.linalg.norm(L)
def shade(Tr, col, alpha=1):
    n = np.cross(Tr[:, 1] - Tr[:, 0], Tr[:, 2] - Tr[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
    return [tuple(np.array(col)*(0.45 + 0.55*abs(x))) + (alpha,) for x in n @ L]
cols = [(0.72, 0.50, 0.04), (0.85, 0.65, 0.13), (0.95, 0.82, 0.45)]
faces = []; fcol = []
for k, Cc in zip(st, C):
    for i in range(3):
        j, l = [x for x in range(3) if x != i]
        for s in (0, 1):
            idx = lambda b: Cc[b[0]*4 + b[1]*2 + b[2]]
            q = []
            for dj, dl in ((0, 0), (1, 0), (1, 1), (0, 1)):
                b = [0, 0, 0]; b[i] = s; b[j] = dj; b[l] = dl; q.append(idx(b))
            faces.append(q); fcol.append(cols[min(k, 2)])
FA = np.array(faces); n = np.cross(FA[:, 1] - FA[:, 0], FA[:, 2] - FA[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
fc = [tuple(np.array(c)*(0.45 + 0.55*abs(x))) for c, x in zip(fcol, n @ L)]
R = np.abs(tris(Room)).max()*0.95
fig = plt.figure(figsize=(15, 7.4), facecolor="white")
for i, (el, az) in enumerate(((25, 30), (70, 120))):
    ax = fig.add_subplot(1, 3, i + 1, projection="3d")
    ax.add_collection3d(Poly3DCollection(list(FA), facecolors=fc, edgecolors=(0.3, 0.2, 0, 0.25), linewidths=0.15), autolim=False)
    Tr = tris(Room); ax.add_collection3d(Poly3DCollection(Tr, facecolors=shade(Tr, (1.0, 0.72, 0.30), 0.07), edgecolors="none"), autolim=False)
    ax.set_xlim(-R, R); ax.set_ylim(-R, R); ax.set_zlim(-R, R); ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(el, az)
ax = fig.add_subplot(1, 3, 3, projection="3d")
ax.add_collection3d(Poly3DCollection(list(FA), facecolors=fc, edgecolors="none"), autolim=False)
for p in bite:
    Tr = tris(OGM.translate(list(p))); ax.add_collection3d(Poly3DCollection(Tr, facecolors=shade(Tr, (0.30, 0.64, 0.65), 0.18), edgecolors="none"), autolim=False)
R2 = R*2.2; ax.set_xlim(-R2, R2); ax.set_ylim(-R2, R2); ax.set_zlim(-R2, R2); ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(25, 30)
fig.text(0.36, 0.93, "Golden rhombohedra inside DICTO's Bull-horns OG adaptor (faint amber): 994 whole bricks in three φ-steps (dark → pale), 48.7% of the adaptor", ha="center", fontsize=11)
fig.text(0.83, 0.93, "with the six OGs (teal) that bite it", ha="center", fontsize=10)
fig.text(0.5, 0.04, "The rest of the adaptor is golden bricks trimmed by the OG walls; only they carry the OG's Dehn invariant.  DICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=9, color="#333")
plt.savefig("bh-golden-fill.png", dpi=125, bbox_inches="tight"); print("FINAL ok")
