# Render: the regular-triangle cut OG on the pyrochlore (diamond) network, and one bcc cell exploded. DICTO 5 Nov 2026.
exec(open("pyro_fill.py").read().split("for g in")[0])
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
def faces(P):
    hh = ConvexHull(P); pl = {}
    for eq, s in zip(hh.equations, hh.simplices): pl.setdefault(tuple(np.round(eq, 5)), (eq, set()))[1].update(s)
    out = []
    for eq, f in pl.values():
        f = list(f); c = P[f].mean(0); n = eq[:3]; e1 = P[f[0]] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
        f.sort(key=lambda i: math.atan2((P[i] - c) @ e2, (P[i] - c) @ e1)); out.append(P[f])
    return out
col = {3: "#d4a020", 5: "#c0392b", 6: "#4fa3a5"}
def tris(M):
    mm = M.to_mesh(); W = np.array(mm.vert_properties)[:, :3]; return [W[t] for t in np.array(mm.tri_verts)]
M = d; m = [M*t for t in tu]; OGF = faces(V)
fig = plt.figure(figsize=(15, 8), facecolor="white")
ax = fig.add_subplot(1, 2, 1, projection="3d")
nodes = [np.zeros(3)] + [2*m[i] for i in range(4)] + [2*m[0] - 2*m[j] for j in (1, 2, 3)]
for c in nodes:
    ax.add_collection3d(Poly3DCollection([f + c for f in OGF], facecolors=[col[len(f)] for f in OGF], edgecolors="#333", linewidths=.2, alpha=.35), autolim=False)
S = {tuple(np.round(a + s*m[i], 4)) for a in nodes for b in nodes for i in range(4) for s in (1, -1) if np.linalg.norm((a + s*2*m[i]) - b) < 1e-4}
S = np.array(sorted(S)); ax.scatter(*S.T, s=110, c="#111", edgecolors="white", linewidths=1.2, depthshade=False, zorder=10)
for a in nodes:
    for b in nodes:
        if 1e-6 < np.linalg.norm(a - b) < 2*M + 1e-4: ax.plot(*np.array([a, b]).T, color="#111", lw=1.6, zorder=9)
r = 3.0*M; cc = np.mean(nodes, 0); ax.set_xlim(cc[0]-r, cc[0]+r); ax.set_ylim(cc[1]-r, cc[1]+r); ax.set_zlim(cc[2]-r, cc[2]+r)
ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(20, 35)
ax.set_title("Cut OGs on the diamond network\nlines = bonds · dots = joints = pyrochlore sites", fontsize=12)
ax = fig.add_subplot(1, 2, 2, projection="3d")
C = TO(np.zeros(3), M); TV = np.array(C.to_mesh().vert_properties)[:, :3]; J = C - hull(V)
facesTO = [("hex+", t, M) for t in tu] + [("hex-", -t, M) for t in tu] + [("sq", s*q, 2*M/math.sqrt(3)) for q in SQ for s in (1, -1)]
E = 0.55
ax.add_collection3d(Poly3DCollection(OGF, facecolors=[col[len(f)] for f in OGF], edgecolors="#333", linewidths=.25, alpha=.95), autolim=False)
pc = {"hex+": "#e8b04a", "hex-": "#8a5a2b", "sq": "#7a5fb0"}
for k, n, off in facesTO:
    F = TV[np.abs(TV @ n - off) < 1e-6]; cone = hull(np.vstack([np.zeros(3), F]))
    for p in (J ^ cone).decompose():
        if p.volume() < 1e-6: continue
        ax.add_collection3d(Poly3DCollection([t + E*M*n for t in tris(p)], facecolors=pc[k], edgecolors="none", alpha=.85), autolim=False)
off = 3.2*M*np.array(SQ[0])
ax.add_collection3d(Poly3DCollection([f + off for f in faces(TV)], facecolors="#d8d8d8", edgecolors="#777", linewidths=.6, alpha=.45), autolim=False)
r = 2.3*M; ax.set_xlim(-r + off[0]/2, r + off[0]/2); ax.set_ylim(-r + off[1]/2, r + off[1]/2); ax.set_zlim(-r + off[2]/2, r + off[2]/2)
ax.set_box_aspect((1, 1, 1)); ax.axis("off"); ax.view_init(20, 35)
ax.set_title("One cell pulled apart\nrings gold / brown = left / right · squares purple\ngrey = a whole truncated octahedron (the empty cells)", fontsize=12)
fig.text(.5, .03, "Every other truncated octahedron of the bcc packing holds a cut OG touching it on 8 hexagons; the others stay whole.\nDICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=9, color="#444")
plt.savefig("og-pyrochlore.png", dpi=120, bbox_inches="tight"); print("FINAL ok")
