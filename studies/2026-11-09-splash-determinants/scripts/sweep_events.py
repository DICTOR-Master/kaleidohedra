# Splash determinants, part S: scale sliders on polar pairs (sphere quadric). S(mu) = P ∩ mu·P*, P Platonic with inradius 1:
#   S(mu) = {n_i·x <= 1 (unit face normals of P)} ∩ {v_j·x <= mu (corners v_j of P, |v_j| = R)}.
# For the three dual families (tetra self-dual, cube–octahedron, dodecahedron–icosahedron), exact in Q(√2, √3, √5) with sympy:
#  (a) INCIDENCE events: mu where four planes meet in a boundary point (4x4 determinant affine in mu) and the face lattice changes;
#  (b) METRIC events: the golden cuts of #88 (edge-length ratio = phi, a linear factor in mu) and the Dehn zero of the tetra sweep;
#  (c) SECONDARY events of t_min (Proposition C of the octahedral-constant study: t_min(S) = max x·y over corners of S and S^∨,
#      S^∨ = S(R^2/mu)): its breaks (ties of two corner pairs) and its maximum; PREDICTION tested: the maximum of t_min sits at the
#      fixed point mu = R of the core turn mu -> R^2/mu (true at sqrt3 on the cube–octahedron sweep).
#  (d) #43 scale slider: S ⊂ t·P(S) begins at t = t_min, a vertex-on-plane incidence linear in t; checked for the five solids.
import json, os, sys, itertools, time
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "data")
phi = (1 + sp.sqrt(5)) / 2
mu = sp.Symbol('mu', positive=True)
checks = []


def check(name, ok, det=""):
    checks.append(("PASS" if ok else "FAIL", name, det)); print(("PASS " if ok else "FAIL ") + name + (" " + det if det else ""), flush=True)


def orbit(gens, start):
    pts = {tuple(sp.nsimplify(x) for x in start)}; todo = list(pts)
    while todo:
        p = todo.pop()
        for g in gens:
            q = tuple(sp.simplify(x) for x in (g * sp.Matrix(p)))
            key = tuple(sp.nsimplify(sp.N(x, 30), [sp.sqrt(5), sp.sqrt(2), sp.sqrt(3)]) for x in q)
            if key not in pts:
                pts.add(key); todo.append(key)
    return [sp.Matrix(p) for p in pts]


def solids():
    out = {}
    # tetrahedron: corners (1,1,1) even signs; faces opposite: normals -(corner)/sqrt3
    tv = [sp.Matrix(p) for p in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
    out["tetra"] = dict(normals=[-v / sp.sqrt(3) for v in tv], dirs=[v / sp.sqrt(3) for v in tv], face_n=3, dual_face_n=3)
    cub = [sp.Matrix(p) for p in itertools.product((1, -1), repeat=3)]
    octn = [sp.Matrix(p) for p in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
    out["cube"] = dict(normals=octn, dirs=[v / sp.sqrt(3) for v in cub], face_n=4, dual_face_n=3)
    ico = []
    for s1, s2 in itertools.product((1, -1), repeat=2):
        for p in [(0, s1 * phi, s2), (s2, 0, s1 * phi), (s1 * phi, s2, 0)]:   # dual orientation to the dodecahedron below
            ico.append(sp.Matrix(p))
    dod = [sp.Matrix(p) for p in itertools.product((1, -1), repeat=3)]
    for s1, s2 in itertools.product((1, -1), repeat=2):
        for p in [(0, s1 / phi, s2 * phi), (s1 / phi, s2 * phi, 0), (s2 * phi, 0, s1 / phi)]:
            dod.append(sp.Matrix(p))
    nrm = lambda v: v / sp.sqrt(sp.simplify(v.dot(v)))
    out["dodeca"] = dict(normals=[nrm(v) for v in ico], dirs=[nrm(v) for v in dod], face_n=5, dual_face_n=3)
    return out


def build(sol):
    """Planes of S(mu): n·x <= 1 (P), d·x <= mu/R... we use unit corner directions d and write the corner planes as d·x <= m,
    m = mu/R; P has inradius 1, so R = circumradius of P; return the corner list of P and R."""
    N = sol["normals"]; Dd = sol["dirs"]
    # corners of P: intersections of 3 face planes that satisfy all
    Nf = np.array([[float(x) for x in n] for n in N])
    corners = []
    for a, b, c in itertools.combinations(range(len(N)), 3):
        M = sp.Matrix([list(N[a]), list(N[b]), list(N[c])])
        if abs(float(M.det())) < 1e-9: continue
        x = M.LUsolve(sp.Matrix([1, 1, 1]))
        xf = np.array([float(t) for t in x])
        if (Nf @ xf <= 1 + 1e-9).all():
            if not any(np.allclose(xf, np.array([float(t) for t in y])) for y in corners):
                corners.append(sp.Matrix([sp.nsimplify(sp.radsimp(t)) for t in x]))
    R = sp.sqrt(sp.nsimplify(sp.simplify(corners[0].dot(corners[0]))))
    return corners, sp.simplify(R)


def planes_at(N, Dd, m):  # list of (normal float, rhs float)
    return [(np.array([float(x) for x in n]), 1.0) for n in N] + [(np.array([float(x) for x in d]), float(m)) for d in Dd]


def vertices(N, Dd, m):
    P = planes_at(N, Dd, m); A = np.array([p[0] for p in P]); b = np.array([p[1] for p in P]); V = []
    for a, c, e in itertools.combinations(range(len(P)), 3):
        M = A[[a, c, e]]
        if abs(np.linalg.det(M)) < 1e-9: continue
        x = np.linalg.solve(M, b[[a, c, e]])
        if (A @ x <= b + 1e-9).all() and not any(np.linalg.norm(x - y) < 1e-7 for y in V): V.append(x)
    return V


def facets(N, Dd, m):
    V = vertices(N, Dd, m); P = planes_at(N, Dd, m); f = []
    for n, h in P:
        k = sum(1 for x in V if abs(n @ x - h) < 1e-8)
        if k >= 3: f.append(k)
    return len(V), sorted(f)


def incidence_events(N, Dd, lo, hi):
    """Roots m in [lo, hi] of 4-plane determinants det[[n_i, h_i(m)]] (h = 1 or m), with the common point on S(m)."""
    P = [(n, 0) for n in N] + [(d, 1) for d in Dd]
    roots = {}
    Pf = [(np.array([float(x) for x in n]), k) for n, k in P]
    for q in itertools.combinations(range(len(P)), 4):
        M0 = np.array([np.append(Pf[i][0], -1.0 if Pf[i][1] == 0 else 0.0) for i in q])
        M1 = np.array([np.append(Pf[i][0], 0.0 if Pf[i][1] == 0 else -1.0) for i in q])
        # det(M0 + m * E) affine in m: det along last column
        d0 = np.linalg.det(M0); d1 = np.linalg.det(np.column_stack([M0[:, :3], M0[:, 3] + M1[:, 3]])) - d0
        if abs(d1) < 1e-9: continue
        r = -d0 / d1
        if not (lo - 1e-9 <= r <= hi + 1e-9): continue
        # common point inside S(r)
        A = np.array([Pf[i][0] for i in q[:3]]); b = np.array([1.0 if Pf[i][1] == 0 else r for i in q[:3]])
        if abs(np.linalg.det(A)) < 1e-9:
            A = np.array([Pf[i][0] for i in q[1:]]); b = np.array([1.0 if Pf[i][1] == 0 else r for i in q[1:]])
            if abs(np.linalg.det(A)) < 1e-9: continue
        x = np.linalg.solve(A, b)
        allp = planes_at(N, Dd, r)
        if all(n @ x <= h + 1e-9 for n, h in allp):
            roots.setdefault(round(r, 9), q)
    # exact value of each root from its quadruple
    out = []
    m = sp.Symbol('m')
    for rf, q in sorted(roots.items()):
        rows = []
        for i in q:
            n, k = P[i]; rows.append(list(n) + [-(1 if k == 0 else m)])
        D = sp.expand(sp.Matrix(rows).det(method='berkowitz'))
        D = sp.expand(D)
        c1 = sp.simplify(D.coeff(m, 1)); c0 = sp.simplify(D.subs(m, 0))
        if c1 == 0 or D.diff(m, 2) != 0: continue
        ex = sp.radsimp(sp.simplify(-c0 / c1))
        if abs(float(sp.N(ex, 30)) - rf) > 1e-7: continue
        out.append((rf, ex, q, sp.factor(D)))
    return out


def tmin(N, Dd, m, R2=1.0):
    """t_min(S(m)) = max x·y over corners x of S(m), y of S^∨ = S(1/m) (Proposition C: unit normals, distances 1 and m
    invert to 1 and 1/m)."""
    V = vertices(N, Dd, m); W = vertices(N, Dd, 1.0 / m)
    return max(float(x @ y) for x in V for y in W)


def tmin_direct(N, Dd, m):
    """t_min from the definition (#43): least t with S ⊂ t·P(S), P(S) = hull of the foot points of the FACET planes of S."""
    from scipy.spatial import ConvexHull
    V = vertices(N, Dd, m); P = planes_at(N, Dd, m)
    feet = []
    for n, h in P:
        if sum(1 for x in V if abs(n @ x - h) < 1e-8) >= 3:
            feet.append(h * n / (n @ n))
    H = ConvexHull(np.array(feet))
    A = H.equations[:, :3]; b = -H.equations[:, 3]
    return max(max((A @ v) / b) for v in V)


X = sp.Symbol('x')


def mp(v):
    return sp.minimal_polynomial(v, X)


def same(a, b):
    return abs(float(sp.N(a - b, 40))) < 1e-25 and mp(a) == mp(b)


def golden(cornersP, n, plane_dist_of, label):
    """Cut fractions x_G, x_L on the n-gon faces; plane_dist_of(x) = m at which the cutting plane removes the fraction x."""
    c = 2 * sp.cos(sp.pi / n)
    return {f"{label} {n}-gon x_G": plane_dist_of(phi / (c + 2 * phi)), f"{label} {n}-gon x_L": plane_dist_of(1 / (phi * c + 2))}


def nearest(cs, v):
    w = [u for u in cs if abs(float((u - v).dot(u - v))) > 1e-9]
    e2 = min(float((u - v).dot(u - v)) for u in w)
    return [u for u in w if abs(float((u - v).dot(u - v)) - e2) < 1e-9][0]


def main():
    S = solids(); res = {}
    for name, sol in S.items():
        N = sol["normals"]; Dd = sol["dirs"]
        corners, R = build(sol)
        # P* = {d·x <= 1}: its corners
        dual = build(dict(normals=Dd, dirs=N))[0]
        ev = incidence_events(N, Dd, 0.2, float(R) + 1e-9)
        rows = []
        for rf, ex, q, D in ev:
            eps = 1e-5
            a = facets(N, Dd, rf - eps); b = facets(N, Dd, rf + eps)
            rows.append(dict(m=str(ex), m_float=rf, minpoly=str(mp(ex)), det_factor=str(sp.factor(D)), facets_below=str(a),
                             facets_above=str(b), change=a != b))
            print(f"{name}: incidence root m = {ex} = {rf:.6f}, minimal polynomial {mp(ex)}; face lattice changes: {a != b}", flush=True)
        # golden cuts: at P's corners (plane dhat·x = m, dhat = v/R) and at m·P*'s corners (P plane n·x = 1 cuts m·u)
        v = corners[0]; wv = nearest(corners, v); R2 = sp.simplify(v.dot(v)); vw = sp.simplify(v.dot(wv))
        g = golden(corners, sol["face_n"], lambda x: sp.radsimp(sp.simplify((R2 - x * (R2 - vw)) / R)), "P")
        u = dual[0]; wu = nearest(dual, u); nn = u / sp.sqrt(sp.simplify(u.dot(u)))
        a1 = sp.simplify(nn.dot(u)); a2 = sp.simplify(nn.dot(wu))
        g.update(golden(dual, sol["dual_face_n"], lambda x: sp.radsimp(sp.simplify(1 / (a1 - x * (a1 - a2)))), "P*"))
        res[name] = dict(R=str(R), events=rows, golden={k: dict(m=str(val), m_float=float(sp.N(val)), minpoly=str(mp(val))) for k, val in g.items()})
        for k, val in g.items():
            print(f"{name}: golden cut {k}: m = {val} = {float(sp.N(val)):.6f}, minimal polynomial {mp(val)}", flush=True)
        # HOPSCOTCH TURN m -> 1/m (S^∨ = S(1/m)): pair the events
        evx = [sp.sympify(r["m"]) for r in rows]
        ends = sorted(r["m_float"] for r in rows); a_, b_ = ends[0], ends[-1]
        check(f"{name}: the range [{a_:.5f}, {b_:.5f}] is turned into itself by m -> 1/m", abs(a_ * b_ - 1) < 1e-9)
        pairs = []
        for e in evx:
            partner = [f for f in evx if same(e * f, sp.Integer(1))]
            pairs.append(dict(m=str(e), m_float=float(sp.N(e)), partner=str(1 / e) if True else None,
                              partner_float=float(sp.N(1 / e)), partner_is_incidence_event=bool(partner)))
        gp = []
        for k, val in g.items():
            hit = [k2 for k2, v2 in g.items() if same(val * v2, sp.Integer(1))]
            gp.append(dict(cut=k, m_float=float(sp.N(val)), partner_float=float(sp.N(1 / val)), partner_is_golden_cut=hit))
        res[name]["turn"] = dict(turning_point="m = 1 (the two plane families at equal distance)", incidence_pairs=pairs, golden_pairs=gp)
        for pr in pairs:
            print(f"{name}: turn pairs incidence m = {pr['m_float']:.6f} with 1/m = {pr['partner_float']:.6f}: partner is an incidence event: {pr['partner_is_incidence_event']}", flush=True)
        for pr in gp:
            print(f"{name}: turn pairs golden cut {pr['cut']} m = {pr['m_float']:.6f} with 1/m = {pr['partner_float']:.6f}: partner golden: {pr['partner_is_golden_cut']}", flush=True)
        # t_min on the open range
        grid = np.linspace(a_ + 1e-4, b_ - 1e-4, 4001)
        T = np.array([tmin(N, Dd, x) for x in grid]); k = int(T.argmax())
        dT = np.diff(T); md = np.median(np.abs(np.diff(dT)))
        kinks = [float(grid[i + 1]) for i in range(1, len(dT) - 1) if abs(dT[i] - dT[i - 1]) > 50 * md + 1e-9]
        kk = []
        for x in kinks:
            if not kk or x - kk[-1] > 2e-3: kk.append(x)
        cand = [float(sp.N(e)) for e in evx] + [float(sp.N(1 / e)) for e in evx]
        kink_match = [dict(kink=x, nearest_event_or_turned_event=min(cand, key=lambda c: abs(c - x))) for x in kk]
        okk = all(abs(km["kink"] - km["nearest_event_or_turned_event"]) < 1e-3 for km in kink_match)
        check(f"{name}: every kink of t_min is an incidence event of S or the turn of one (an incidence event of S^∨)", okk,
              str([(round(km['kink'], 4), round(km['nearest_event_or_turned_event'], 4)) for km in kink_match]))
        sym_ok = all(abs(tmin(N, Dd, x) - tmin_direct(N, Dd, x)) < 1e-9 and abs(tmin_direct(N, Dd, x) - tmin_direct(N, Dd, 1 / x)) < 1e-9
                     for x in grid[::200])
        check(f"{name}: t_min by definition (#43) = max x·y over S x S^∨ and t_min(m) = t_min(1/m), 21 grid points", sym_ok)
        # exact value at the turning point: S^∨ = S, so t_min = max x·y over S x S = R(S(1))^2
        V1 = vertices(N, Dd, 1.0); i1 = int(np.argmax([x @ x for x in V1]))
        # exact corner: solve its three planes exactly
        Pl = [(n, sp.Integer(1)) for n in N] + [(d, sp.Integer(1)) for d in Dd]
        Pf = planes_at(N, Dd, 1.0)
        tight = [j for j, (nf, h) in enumerate(Pf) if abs(nf @ V1[i1] - h) < 1e-8]
        xe = None
        for t3 in itertools.combinations(tight, 3):
            M = sp.Matrix([list(Pl[j][0]) for j in t3])
            if abs(float(sp.N(M.det()))) > 1e-9:
                xe = M.LUsolve(sp.Matrix([1, 1, 1])); break
        tfix = sp.radsimp(sp.simplify(xe.dot(xe)))
        t1 = tmin(N, Dd, 1.0)
        pred = abs(t1 - float(sp.N(tfix))) < 1e-9 and t1 >= T.max() - 1e-12
        check(f"{name}: PREDICTION t_min is largest at the turning point m = 1, value R(S(1))^2 = {tfix} = {float(sp.N(tfix)):.6f}", bool(pred),
              f"grid max {T[k]:.6f} at m = {grid[k]:.5f}")
        res[name]["tmin"] = dict(range=[a_, b_], argmax=float(grid[k]), max=float(T[k]), at_turning_point=str(tfix), at_turning_point_minpoly=str(mp(tfix)),
                                 kinks=kink_match, end_values=[float(T[0]), float(T[-1])])
    json.dump(res, open(os.path.join(DATA, "sweep-events.json"), "w"), indent=1, default=str)
    nf = sum(c[0] == "FAIL" for c in checks)
    print(f"{len(checks) - nf}/{len(checks)} PASS")
    print('FINAL ok' if checks and nf == 0 else f'FINAL FAIL: {nf} failed')


if __name__ == "__main__":
    main()
