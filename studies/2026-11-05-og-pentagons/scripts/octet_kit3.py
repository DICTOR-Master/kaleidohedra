# Cut-OG kit, part 3 (DICTO 5 Nov 2026): (a) are the 6 corner pieces one shape, is the dented tetrahedron chiral;
# (b) the gyrated octet: mirror the upper half-space across an octahedron face plane x+y+z = R (twin layer) and check overlaps + new pieces.
exec(open("octet_kit.py").read().split("OG = hull(C)")[0])
def octa(c): return hull(np.array([[R,0,0],[-R,0,0],[0,R,0],[0,-R,0],[0,0,R],[0,0,-R]]) + c)
U_all = m3.Manifold.batch_boolean(solids, m3.OpType.Add)
def pts(M): return np.unique(np.round(np.array(M.to_mesh().vert_properties)[:, :3], 7), axis=0)
def sig(M, mirror=False):
    P = pts(M); P = P*np.array([-1, 1, 1]) if mirror else P; c = P.mean(0)
    d = np.sort(np.round([np.linalg.norm(a - b) for a, b in itertools.combinations(P, 2)], 5)); return (round(M.volume(), 6), len(P), hash(d.tobytes()))
def same_shape(A, B, want=None):     # congruent by a rotation/reflection: try all orthogonal maps fixing 3 corners
    P, Q = pts(A), pts(B)
    if len(P) != len(Q) or abs(A.volume() - B.volume()) > 1e-9: return None
    cp, cq = P.mean(0), Q.mean(0); P0, Q0 = P - cp, Q - cq
    i = np.argsort(-np.linalg.norm(P0, axis=1))[:3]
    for j in itertools.permutations(range(len(Q0)), 3):
        if not np.allclose(np.linalg.norm(Q0[list(j)], axis=1), np.linalg.norm(P0[i], axis=1), atol=1e-6): continue
        X = P0[i]; Y = Q0[list(j)]
        try: Mx = np.linalg.solve(X, Y).T
        except np.linalg.LinAlgError: continue
        if not np.allclose(Mx @ Mx.T, np.eye(3), atol=1e-6): continue
        kind = "rotation" if np.linalg.det(Mx) > 0 else "reflection"
        if want and kind != want: continue
        if all(np.min(np.linalg.norm(Q0 - Mx @ p, axis=1)) < 1e-5 for p in P0): return "rotation" if np.linalg.det(Mx) > 0 else "reflection"
    return None
O0 = octa(np.zeros(3)); rest = O0 - U_all
cones = []
for v in np.eye(3).tolist() + (-np.eye(3)).tolist():
    v = np.array(v)*R; others = [w for w in (np.vstack([np.eye(3), -np.eye(3)])*R) if not np.allclose(w, v) and not np.allclose(w, -v)]
    cones.append(hull(np.vstack([np.zeros(3), v, *[ (v + w)/2 for w in others ], *[(v + w)/2*1.0 for w in others]]) ))
corner = [rest ^ hull(np.vstack([np.zeros(3), v*R, *[(v*R + w)/1.0 for w in []]])) for v in []]
# split the octahedron rest by the 6 vertex regions {x : v.x >= |w.x| for the other axes}
reg = []
for ax in range(3):
    for sgn in (1, -1):
        Hs = []
        big = 10
        P = []
        for corner_ in itertools.product((-big, big), repeat=3):
            p = np.array(corner_, float)
            P.append(p)
        box_ = m3.Manifold.cube([2*big]*3).translate([-big]*3)
        for o in range(3):
            if o == ax: continue
            for s2 in (1, -1):
                n = np.zeros(3); n[o] = s2; n[ax] = -sgn      # keep sgn*x_ax >= s2*x_o
                box_ = box_.trim_by_plane((-n).tolist(), 0.0)
        reg.append(rest ^ box_)
vols = [round(r.volume(), 6) for r in reg]; print("corner pieces volumes", vols)
print("corner corner-counts", [len(pts(r)) for r in reg]); print("corner pieces connected parts", [len(r.decompose()) for r in reg]); print("corner 0 vs others (rotation):", [same_shape(reg[0], r, "rotation") for r in reg[1:]], "(reflection):", [same_shape(reg[0], r, "reflection") for r in reg[1:]])
Tp = hull(np.array([[R,0,0],[0,R,0],[0,0,R],[R,R,R]])); Tm = hull(np.array([[R,0,0],[0,R,0],[0,0,-R],[R,R,-R]]))
tp, tm = Tp - U_all, Tm - U_all
print("dented tetrahedra:", round(tp.volume(), 6), round(tm.volume(), 6), "relation:", same_shape(tp, tm))
mir = tp.mirror([1, 0, 0]); print("dented tetrahedron = its own mirror by a ROTATION (achiral)?", same_shape(tp, mir, "rotation")); print("T+ vs T- by rotation?", same_shape(tp, tm, "rotation"))
print("FINAL ok")
