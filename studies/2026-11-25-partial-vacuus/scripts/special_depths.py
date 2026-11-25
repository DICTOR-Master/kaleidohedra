# DICTO · partial Vacuus, part 1: special depths (25 Nov 2026). With Claude (Anthropic). Exact (sympy, Q(sqrt5)).
# Idea (DICTO, 25 Nov): "the excavated dodecahedron is kind of a vacuus"; "depth doesn't go all the way to center"; "a true vacuus or
# resonus barely exists". A PARTIAL VACUUS of a polyhedron P: every face dug in as a pyramid pit with its apex on the face's axis at
# distance a from the centre (a = 0: the Vacuus pyramids; a = face distance: the solid). A depth is SPECIAL when the pits' walls lie in
# the face planes of another solid Q centred at O (then the pits stop exactly on Q). Test, for each P and each candidate Q in the same
# symmetry frame: the wall through an edge e of P and the apex on the axis of a face f containing e is a face plane of Q (scaled freely).
# Wall plane = span of e's endpoints u, v and the apex a*n_f (n_f unit face normal). Its normal m = (u - a n_f) x (v - a n_f); Q's face
# normals are fixed directions; the wall is a Q face plane iff m is parallel to a Q normal (for some a > 0) and the scale is consistent.
import sympy as sp, itertools, json
f5 = sp.sqrt(5); ph = (1 + f5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def signs(v):
    out = []
    for s in itertools.product((1, -1), repeat=3):
        w = tuple(sp.nsimplify(a * b) for a, b in zip(s, v))
        if w not in out: out.append(w)
    return out
SOL = {
 'tetrahedron': [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)],
 'octahedron': [w for v in cyc((1, 0, 0)) for w in signs(v)],
 'cube': signs((1, 1, 1)),
 'icosahedron': [w for v in cyc((0, 1, ph)) for w in signs(v)],
 'dodecahedron': signs((1, 1, 1)) + [w for v in cyc((0, ph, 1 / ph)) for w in signs(v)],
}
def hull(V):
    """faces found in floating point (sign test), normals kept exact."""
    import numpy as np
    Vf = np.array([[float(x) for x in v] for v in V]); V = [sp.Matrix(v) for v in V]; F = {}
    for i, j, k in itertools.combinations(range(len(V)), 3):
        nf = np.cross(Vf[j] - Vf[i], Vf[k] - Vf[i])
        if np.linalg.norm(nf) < 1e-9: continue
        sv = (Vf - Vf[i]) @ nf
        if (sv <= 1e-9).all() or (sv >= -1e-9).all():
            on = frozenset(int(m) for m in np.where(np.abs(sv) < 1e-9)[0])
            if on in F: continue
            n = (V[j] - V[i]).cross(V[k] - V[i])
            if (sv >= -1e-9).all(): n = -n
            F[on] = n
    return V, F
def unit_dir(n):
    n = sp.Matrix(n); return n / sp.sqrt(n.dot(n))
res = []
for P, VP in SOL.items():
    V, F = hull(VP)
    faces = list(F.items())
    # one face f and one of its edges (by symmetry enough for the regular solids)
    (on, nf) = faces[0]; nf = unit_dir(nf); dist = sp.simplify(nf.dot(V[list(on)[0]]))
    pts = list(on); cen = sum((V[i] for i in pts), sp.zeros(3, 1)) / len(pts)
    # an edge of f: two vertices of f adjacent on the hull (share two faces)
    e = next((a, b) for a, b in itertools.combinations(pts, 2) if sum(1 for o, _ in faces if a in o and b in o) == 2)
    u, v = V[e[0]], V[e[1]]
    a = sp.symbols('a', positive=True)
    m = (u - a * nf).cross(v - a * nf)
    for Q, VQ in SOL.items():
        VQm, FQ = hull(VQ)
        sols = set()
        for _, nq in FQ.items():
            c = m.cross(nq)   # parallel <=> cross = 0
            eqs = [sp.simplify(x) for x in c if sp.simplify(x) != 0]
            if not eqs: continue
            s = sp.solve(eqs[0], a)
            for r in s:
                r = sp.nsimplify(sp.simplify(r))
                if r.is_real and r > 0 and r < dist and all(sp.simplify(x.subs(a, r)) == 0 for x in c):
                    sols.add(r)
        # every wall of every pit must be a face plane of Q (one scale): check all faces f and all their edges
        import numpy as np
        QN = [np.array([float(x) for x in unit_dir(nq)]) for nq in FQ.values()]
        def all_walls(r):
            dws = set()
            for on2, nf2 in faces:
                n2 = np.array([float(x) for x in unit_dir(nf2)]); ap = float(r) * n2
                p2 = list(on2)
                for a1, b1 in itertools.combinations(p2, 2):
                    if sum(1 for o, _ in faces if a1 in o and b1 in o) != 2: continue
                    U = np.array([float(x) for x in V[a1]]); W = np.array([float(x) for x in V[b1]])
                    w = np.cross(U - ap, W - ap); w /= np.linalg.norm(w)
                    if not any(abs(abs(w @ q) - 1) < 1e-9 for q in QN): return False
                    dws.add(round(abs(w @ U), 9))
            return len(dws) == 1
        for r in sorted(sols, key=lambda x: float(x)):
            if not all_walls(r):
                print(f'{P:13s} on {Q:13s}: one wall at {float(r/dist):.6f} lies on a {Q} face plane, but not every wall (rejected)'); continue
            frac = sp.nsimplify(sp.simplify(r / dist))
            # the wall plane's distance from O fixes Q's scale: Q face plane through u
            wall_n = unit_dir(m.subs(a, r)); wall_d = sp.simplify(abs(wall_n.dot(u)))
            res.append(dict(P=P, Q=Q, apex_over_face_distance=str(frac), apex_over_face_distance_float=float(frac), Q_inradius_over_P_face_distance=str(sp.nsimplify(sp.simplify(wall_d / dist)))))
            print(f'{P:13s} pits stop on {Q:13s} faces: apex at {sp.simplify(frac)} = {float(frac):.6f} of the face distance; Q inradius / P face distance = {float(wall_d/dist):.6f}', flush=True)
json.dump(res, open('special_depths.json', 'w'), indent=1)
ok = any(r['P'] == 'dodecahedron' and r['Q'] == 'icosahedron' and abs(r['apex_over_face_distance_float'] - (5 - 2 * 5 ** 0.5)) < 1e-12 for r in res)
print('control: excavated dodecahedron found at 5 - 2 sqrt5:', ok)
print('FINAL ok' if ok else 'FINAL FAIL (control)')
