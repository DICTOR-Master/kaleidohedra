exec(open("gyro_kit2.py").read().split("print(\"PER-CELL")[0])
# twin connectors: for face-sharing pairs (an octahedron and its mirror image across the twin layer), across each of the 3 shared edges,
# the hull of the two pentagons facing that edge
twin = []
for (ca, A, OA, TA), (cb, B, OB, TB) in itertools.combinations(cells, 2):
    sh = [p for p in OA if np.min(np.linalg.norm(OB - p, axis=1)) < 1e-9]
    if len(sh) != 3: continue
    for e0, e1 in itertools.combinations(sh, 2):
        m = (e0 + e1)/2
        def pentq(c, P, T):
            e = (m - c)/np.linalg.norm(m - c); Ut = (T - c)/np.linalg.norm(T - c, axis=1)[:, None]; u = Ut[np.argmax(Ut @ e)]
            return P[np.abs((P - c) @ u - 0.63932) < 2e-3], u
        QA, ua = pentq(ca, A, TA); QB, ub = pentq(cb, B, TB)
        twin.append((hull(np.vstack([QA, QB])), len(QA), len(QB), float(ua @ ub)))
print("twin connectors:", len(twin), "pentagon sizes", {(t[1], t[2]) for t in twin}, "axis dot products", sorted({round(t[3], 4) for t in twin}))
print("twin connector volumes", sorted({round(t[0].volume(), 6) for t in twin}), "(octet connector 0.018887)")
T_all = m3.Manifold.batch_boolean([t[0] for t in twin], m3.OpType.Add)
print("overlap of twin connectors with cut OGs + octet connectors:", round((T_all ^ U_all).volume(), 8), "; among themselves:", round(sum(t[0].volume() for t in twin) - T_all.volume(), 8))
ALL = U_all + T_all; ref = R*np.array([.5, .5, 0])
def on_plane(P): return sum(abs(p @ n - d0) < 1e-9 for p in P) >= 3
for c, A, O, _ in cells:
    if on_plane(O) and np.linalg.norm(c - ref) < 1.3*R:
        rest = hull(O) - ALL; print("  twin-layer octahedron rest", round(rest.volume(), 5), "pieces", sorted(round(p.volume(), 5) for p in rest.decompose() if p.volume() > 1e-9)); break
for (c, A, O, _) in cells[:len(up)]:
    for sg in itertools.product((1, -1), repeat=3):
        T = np.vstack([[c + R*np.eye(3)[i]*sg[i] for i in range(3)], c + R*np.array(sg, float)])
        if on_plane(T) and np.linalg.norm(c - ref) < 1.3*R:
            rest = hull(T) - ALL; v = round(rest.volume(), 5)
            if v > .2: print("  twin-layer tetrahedron rest", v, "pieces", sorted(round(p.volume(), 5) for p in rest.decompose() if p.volume() > 1e-9)); break
    else: continue
    break
print("octet values: corner piece 0.07826 (x6 = 0.46956), dented tetrahedron 0.39725; FINAL ok")
