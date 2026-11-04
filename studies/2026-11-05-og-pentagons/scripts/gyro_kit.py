# Cut-OG kit in the GYRATED octet (DICTO 5 Nov 2026). Twin layer = the plane x+y+z = R (an octahedron face plane).
# Above it the octet with cut OGs; below it the mirror image of everything above (octahedron meets octahedron, tetrahedron meets
# tetrahedron across the layer). Connectors across every edge shared by two octahedra whose cut OGs show parallel facing pentagons.
# Reports: overlaps, which shared edges get no connector, and the leftover pieces of every cell touching the twin layer.
exec(open("octet_kit.py").read().split("cen = [")[0])
n = np.array([1., 1, 1])/math.sqrt(3); d0 = R/math.sqrt(3)
def M(P): P = np.asarray(P, float); return P - 2*np.outer(P @ n - d0, n)
OCT = np.array([[R,0,0],[-R,0,0],[0,R,0],[0,-R,0],[0,0,R],[0,0,-R]])
up = [R*np.array(v, float) for v in itertools.product(range(-3, 4), repeat=3) if sum(v) % 2 == 0 and sum(v) >= 2 and max(map(abs, v)) <= 3]
up = [c for c in up if np.linalg.norm(c - R*np.array([.5, .5, 0])) < 3.2*R]
cells = [(c, C + c, OCT + c, TIPS + c) for c in up] + [(M([c])[0], M(C + c), M(OCT + c), M(TIPS + c)) for c in up]   # (centre, cut OG corners, octahedron corners)
solids = [hull(o) for _, o, _, _ in cells]; conn = 0; noconn = []
for (ca, A, OA, TA), (cb, B, OB, TB) in itertools.combinations(cells, 2):
    sh = [p for p in OA if np.min(np.linalg.norm(OB - p, axis=1)) < 1e-9]
    if len(sh) != 2: continue
    m = (sh[0] + sh[1])/2
    def facing(c, P, T):
        e = (m - c)/np.linalg.norm(m - c); Ut = (T - c)/np.linalg.norm(T - c, axis=1)[:, None]; u = Ut[np.argmax(Ut @ e)]
        Q = P[np.abs((P - c) @ u - 0.63932) < 2e-3]; return Q, u, 0
    QA, na, _ = facing(ca, A, TA); QB, nb, _ = facing(cb, B, TB)
    flatA = np.linalg.svd(QA - QA.mean(0))[1][-1]; flatB = np.linalg.svd(QB - QB.mean(0))[1][-1]
    if len(QA) == 5 and len(QB) == 5 and flatA < 1e-6 and flatB < 1e-6 and abs(na @ nb + 1) < 1e-6:
        solids.append(hull(np.vstack([QA, QB]))); conn += 1
    else: noconn.append((np.round(m, 3), round(float(na @ nb), 4), float(flatA), float(flatB)))
U_all = m3.Manifold.batch_boolean(solids, m3.OpType.Add); tot = sum(s.volume() for s in solids)
print(f"cells {len(cells)} (half mirrored), connectors {conn}, shared edges without parallel pentagons {len(noconn)}; overlap volume {tot - U_all.volume():.2e}", flush=True)
for x in noconn[:6]: print("   no connector at edge midpoint", x[0], "pentagon normals dot", x[1], "flatness", f"{x[2]:.1e} {x[3]:.1e}")
# cells touching the twin layer: octahedra whose face lies on the plane, tetrahedra with a face on it (upper and mirrored)
def on_plane(P): return sum(abs(p @ n - d0) < 1e-9 for p in P) >= 3
ks = {}
for c, A, O, _ in cells:
    if not on_plane(O) or np.linalg.norm(c - R*np.array([.5, .5, 0])) > 1.3*R: continue
    rest = hull(O) - U_all
    for p in rest.decompose():
        if p.volume() > 1e-9: k = ("octahedron", round(p.volume(), 5)); ks[k] = ks.get(k, 0) + 1
tets = []
for (c, A, O, _) in cells[:len(up)]:
    for s in itertools.product((1, -1), repeat=3):
        F = [c + R*np.eye(3)[i]*s[i] for i in range(3)]; apex = c + R*np.array(s, float)
        T = np.vstack([F, apex])
        if on_plane(T) and np.linalg.norm(c - R*np.array([.5, .5, 0])) < 1.3*R: tets += [T, M(T)]
seen = set()
for T in tets:
    key = tuple(np.round(np.sort(T, axis=0).ravel(), 5))
    if key in seen: continue
    seen.add(key); rest = hull(T) - U_all
    for p in rest.decompose():
        if p.volume() > 1e-9: k = ("tetrahedron", round(p.volume(), 5)); ks[k] = ks.get(k, 0) + 1
print("leftover pieces in cells on the twin layer (kind, volume): count"); [print("  ", k, v) for k, v in sorted(ks.items())]
print("octet values for comparison: corner piece 0.07826, dented tetrahedron 0.39725"); print("FINAL ok")
