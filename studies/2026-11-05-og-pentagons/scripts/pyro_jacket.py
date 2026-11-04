# Split the jacket (truncated octahedron minus the cut OG, gap 0) by the 14 face pyramids of the cell; count shapes.
exec(open("pyro_fill.py").read().split("for g in")[0])
exec("def same_shape" + open("octet_kit3.py").read().split("def same_shape")[1].split("O0 = ")[0].replace("> 1e-9: return None", "> 1e-4: return None").replace("atol=1e-6", "atol=1e-4").replace("< 1e-5", "< 1e-4"))
def pts(M):
    mm = M.to_mesh(); W = np.array(mm.vert_properties)[:, :3]; NS = {}
    for t in np.array(mm.tri_verts):
        a, b, c = W[t]; nn = np.cross(b - a, c - a); L = np.linalg.norm(nn)
        if L < 1e-12: continue
        for i in t: NS.setdefault(i, []).append(nn/L)
    keep = [i for i, N in NS.items() if len(N) >= 3 and np.linalg.svd(np.array(N), compute_uv=False)[-1] > 1e-3]
    return np.unique(np.round(W[keep], 9), axis=0)
M = d; C = TO(np.zeros(3), M); J = C - hull(V); print(f"cell {C.volume():.4f} cut OG {hull(V).volume():.4f} jacket {J.volume():.4f}", flush=True)
TV = pts(C); faces = [("hex", s*t, M) for t in tu for s in (1, -1)] + [("square", s*q, 2*M/math.sqrt(3)) for q in SQ for s in (1, -1)]
P = []
for kind, n, off in faces:
    F = TV[np.abs(TV @ n - off) < 1e-6]; cone = hull(np.vstack([np.zeros(3), F]))
    for p in (J ^ cone).decompose():
        if p.volume() > 1e-6: P.append((kind, p))
print("pieces", len(P), "volumes:", sorted({(k, round(p.volume(), 4)) for k, p in P}), flush=True)
cls = []
for k, p in P:
    for c in cls:
        r = same_shape(c[1], p)
        if r: c[2][r] = c[2].get(r, 0) + 1; break
    else: cls.append([k, p, {"first": 1}])
for k, p, kinds in cls:
    mir = same_shape(p, p.transform(np.array([[-1.,0,0,0],[0,1,0,0],[0,0,1,0]])), "rotation")
    print(f"  {k} piece: vol {p.volume():.4f}, corners {len(pts(p))}, copies {kinds}, own mirror by rotation: {mir}", flush=True)
print("FINAL ok")
for k, p in P[:1] + P[-1:]: print(k, "genus", p.genus(), flush=True)
