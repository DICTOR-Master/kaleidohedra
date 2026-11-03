"""Step 2. Golden cuts of the 13 Catalan solids.

Cut (per vertex orbit). The corners of a Catalan solid fall into 1-3 orbits. At every corner the edges are alike (the
corner's stabiliser turns them into each other), so the plane perpendicular to the centre-corner line meets them all at
the same distance y_o along the edges; y_o may differ between orbits o.
Golden (alternating sense). Every face (n sides) becomes a 2n-gon whose sides alternate between two lengths: all corner
sides a, all original sides b, with max(a,b)/min(a,b) = phi. (A Catalan face is not regular, so this is the meaning of
"truncated polygon of ratio phi" that survives; the angles are not all equal.)
The conditions are linear in (y_o, a, b): y_o s_v = a at every corner v (s_v = |e1 - e2| for the unit edge vectors at v
in the face), y_u + y_v + b = L_uv on every edge. Rank analysis (float) gives: no alternating cut, exactly one (ratio
r* fixed), or a one-parameter family (two golden cuts). Exact values: sympy on the exact Q(sqrt2)/Q(sqrt5) coordinates
(11 solids); the two snub duals in floating point (their coordinates are cubic irrationals).
The single-depth cut (same cap height at every corner) and the single-plane cut (all planes at one distance from the
centre) are special cases of the per-orbit cut, so their golden cuts are among the ones found here; we test them.
usage: python s2_catalan.py -> ../data/s2-catalan.json
"""
import json, os, itertools, collections
import numpy as np
import sympy as sp
import gcb

phi = (1 + sp.sqrt(5)) / 2; G = float(phi)
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True); assert ok, name

from gcb_exact import SEEDS, CATALAN_NAME, exact_arch


def solve_float(V, F, orb):
    labs = sorted(set(orb)); nu = len(labs) + 2; rows, rhs = [], []
    for f in F:
        m = len(f)
        for i in range(m):
            u, v, w = f[i - 1], f[i], f[(i + 1) % m]
            e1 = (V[u] - V[v]) / np.linalg.norm(V[u] - V[v]); e2 = (V[w] - V[v]) / np.linalg.norm(V[w] - V[v])
            r = np.zeros(nu); r[labs.index(orb[v])] = np.linalg.norm(e1 - e2); r[-2] = -1; rows.append(r); rhs.append(0.)
            r = np.zeros(nu); r[labs.index(orb[v])] += 1; r[labs.index(orb[w])] += 1; r[-1] = 1; rows.append(r); rhs.append(np.linalg.norm(V[w] - V[v]))
    M, b = np.array(rows), np.array(rhs)
    rk = np.linalg.matrix_rank(M, 1e-9); rka = np.linalg.matrix_rank(np.c_[M, b], 1e-9)
    return labs, M, b, rk, rka


out = []
for name in gcb.ARCH:
    cname = CATALAN_NAME[name]
    V, F, orb = gcb.catalan(name)
    labs, M, bb, rk, rka = solve_float(V, F, orb)
    nu = len(labs) + 2
    rec = {'catalan': cname, 'dual_of': name, 'vertices': len(V), 'faces': len(F), 'face_size': len(F[0]),
           'orbits': dict(collections.Counter(orb)), 'unknowns': nu, 'rank': int(rk), 'rank_augmented': int(rka)}
    if rka > rk:
        rec['alternating_cuts'] = 'none (equations inconsistent)'; rec['golden_cuts'] = 0
        res = np.linalg.lstsq(M, bb, rcond=None); rec['least_squares_residual'] = float(np.linalg.norm(M @ res[0] - bb))
    elif rk == nu:
        sol = np.linalg.lstsq(M, bb, rcond=None)[0]
        a, b = sol[-2], sol[-1]; r = max(a, b) / min(a, b)
        rec['alternating_cuts'] = 'exactly one'; rec['ratio_float'] = float(r); rec['long_sides'] = 'corner' if a > b else 'orig'
        rec['y_float'] = dict(zip(labs, map(float, sol[:-2]))); rec['golden_cuts'] = 0
        rec['valid'] = bool(min(sol) > 0)
    else:
        rec['alternating_cuts'] = f'a {nu - rk}-parameter family'
        # impose the ratio: a = phi b (corner long) or b = phi a (orig long)
        sols = []
        for lab, row in (('greater (corner sides long)', np.r_[np.zeros(nu - 2), 1, -G]), ('lesser (original sides long)', np.r_[np.zeros(nu - 2), -G, 1])):
            M2 = np.r_[M, row[None]]; b2 = np.r_[bb, 0]
            sol = np.linalg.lstsq(M2, b2, rcond=None)[0]
            ok = np.linalg.norm(M2 @ sol - b2) < 1e-9 and np.linalg.matrix_rank(M2, 1e-9) == nu
            y = [sol[labs.index(o)] for o in orb]
            conv, nf = gcb.check_cut_is_convex_truncation(V, F, y)
            sols.append({'cut': lab, 'y_float': dict(zip(labs, map(float, sol[:-2]))), 'a': float(sol[-2]), 'b': float(sol[-1]),
                         'unique': bool(ok), 'positive': bool(min(sol) > 0), 'convex_truncation_faces': nf, 'valid': bool(conv and min(sol) > 0)})
        rec['golden'] = sols; rec['golden_cuts'] = sum(s_['valid'] for s_ in sols)
    # exact
    if name in SEEDS:
        EA = exact_arch(name); A = gcb.archimedean(name); A0 = np.array([[float(t) for t in q] for q in EA.values()])
        sc = np.linalg.norm(A0[0]) / np.linalg.norm(A[np.argmin(np.linalg.norm(A / np.linalg.norm(A[0]) - A0[0] / np.linalg.norm(A0[0]), axis=1))])
        exA = list(EA.values()); FA = gcb.faces(A0)
        check(f'{cname}: exact Archimedean seed gives {len(exA)} corners, {len(FA)} faces', len(exA) == len(A) and len(FA) == len(gcb.faces(A)))
        D = []
        for f in FA:
            p0, p1, p2 = [sp.Matrix(exA[i]) for i in f[:3]]
            n = (p1 - p0).cross(p2 - p0); dd = n.dot(p0)
            if sp.N(dd) < 0: n, dd = -n, -dd
            D.append(sp.Matrix([sp.radsimp(t / dd) for t in n]))
        Df = np.array([[float(t) for t in v] for v in D]); FD = gcb.faces(Df)
        orbD = []
        for f in FA:
            nb = sorted(len(h) for h in FA if len(set(h) & set(f)) == 2); orbD.append(str(len(f)) + '|' + ''.join(map(str, nb)))
        labsD, MD, bD, rkD, rkaD = solve_float(Df, FD, orbD)
        check(f'{cname}: exact model has the same rank structure ({rkD},{rkaD}) as the float model ({rk},{rka})', (rkD, rkaD) == (rk, rka) and labsD == labs)
        # exact equations from one face (face-transitive) -- symbols y_o, a, b
        ys = sp.symbols('y0:%d' % len(labs)); a_, b_ = sp.symbols('a b')
        f = FD[0]; m = len(f); eqs = []
        for i in range(m):
            u, v, w = f[i - 1], f[i], f[(i + 1) % m]
            e1, e2 = D[u] - D[v], D[w] - D[v]
            L1, L2 = sp.sqrt(sp.radsimp(e1.dot(e1))), sp.sqrt(sp.radsimp(e2.dot(e2)))
            s2 = sp.radsimp(sp.expand(2 - 2 * e1.dot(e2) / (L1 * L2)))
            eqs.append(ys[labs.index(orbD[v])] * sp.sqrt(s2) - a_)
            eqs.append(ys[labs.index(orbD[v])] + ys[labs.index(orbD[w])] + b_ - L2)
        if rec['alternating_cuts'] == 'exactly one':
            # choose independent equations by the float rank, solve, check the rest at 60 digits
            num = lambda e: complex(sp.N(e.subs({s_: 0 for s_ in list(ys) + [a_, b_]}), 30))
            sol = sp.solve(eqs[:], list(ys) + [a_, b_], dict=True)
            if not sol:     # overdetermined numerically-consistent: solve a square subset
                J = sp.Matrix([[sp.diff(e, s_) for s_ in list(ys) + [a_, b_]] for e in eqs])
                Jf = np.array(J.evalf(20).tolist(), float); pick = []
                for i in range(len(eqs)):
                    if np.linalg.matrix_rank(Jf[pick + [i]], 1e-9) > len(pick): pick.append(i)
                sol = sp.solve([eqs[i] for i in pick], list(ys) + [a_, b_], dict=True)
            sol = sol[0]
            resid = max(abs(sp.N(e.subs(sol), 60)) for e in eqs)
            check(f'{cname}: exact alternating cut satisfies all face equations (residual {float(resid):.1e})', resid < 1e-50)
            av, bv = sp.radsimp(sol[a_]), sp.radsimp(sol[b_])
            r = av / bv if sp.N(av - bv) > 0 else bv / av
            x = sp.Symbol('x'); mp = sp.minimal_polynomial(sp.radsimp(r), x)
            rec['ratio_exact_minimal_polynomial'] = str(mp); rec['ratio_exact'] = str(sp.radsimp(r))
            check(f'{cname}: alternating ratio {float(r):.9f} agrees with float {rec["ratio_float"]:.9f}', abs(float(r) - rec['ratio_float']) < 1e-9)
            check(f'{cname}: ratio is not phi (minimal polynomial {mp} != x^2 - x - 1)', sp.expand(mp - (x ** 2 - x - 1)) != 0)
            rec['y_exact'] = {labs[i]: str(sp.radsimp(sol[ys[i]])) for i in range(len(labs))}
        elif rec.get('golden'):
            for gsol, lab, rel in zip(rec['golden'], ('greater', 'lesser'), (a_ - phi * b_, b_ - phi * a_)):
                sol = sp.solve(eqs + [rel], list(ys) + [a_, b_], dict=True)
                if not sol:
                    J = sp.Matrix([[sp.diff(e, s_) for s_ in list(ys) + [a_, b_]] for e in eqs + [rel]])
                    Jf = np.array(J.evalf(20).tolist(), float); pick = []
                    allE = eqs + [rel]
                    for i in range(len(allE)):
                        if np.linalg.matrix_rank(Jf[pick + [i]], 1e-9) > len(pick): pick.append(i)
                    sol = sp.solve([allE[i] for i in pick], list(ys) + [a_, b_], dict=True)
                sol = sol[0]
                resid = max(abs(sp.N(e.subs(sol), 60)) for e in eqs + [rel])
                check(f'{cname} {lab}: exact golden cut satisfies all equations (residual {float(resid):.1e})', resid < 1e-50)
                # unit: scale so the Catalan edge is 1
                Lr = sp.sqrt(sp.radsimp((D[FD[0][0]] - D[FD[0][1]]).dot(D[FD[0][0]] - D[FD[0][1]])))
                gsol['y_exact_edge1'] = {labs[i]: str(sp.radsimp(sol[ys[i]] / Lr)) for i in range(len(labs))}
                gsol['a_exact_edge1'] = str(sp.radsimp(sol[a_] / Lr))
                gsol['b_exact_edge1'] = str(sp.radsimp(sol[b_] / Lr))
                # cap heights and plane distances per orbit (single-depth / single-plane tests), exact
                caps, planes = {}, {}
                for v in range(len(D)):
                    o = orbD[v]
                    if o in caps: continue
                    nbv = [w for f2 in FD for i, w in enumerate(f2) if f2[i - 1] == v]
                    e = D[nbv[0]] - D[v]; Le = sp.sqrt(sp.radsimp(e.dot(e)))
                    Rv = sp.sqrt(sp.radsimp(D[v].dot(D[v])))
                    cos_t = sp.radsimp(-e.dot(D[v]) / (Le * Rv))
                    h = sp.radsimp(sol[ys[labs.index(o)]] * cos_t)
                    caps[o] = h / Lr; planes[o] = (Rv - h) / Lr
                ks = list(caps)
                gsol['cap_depth_edge1'] = {k: float(sp.N(caps[k], 20)) for k in ks}
                gsol['plane_distance_edge1'] = {k: float(sp.N(planes[k], 20)) for k in ks}
                gsol['equal_cap_depths'] = bool(abs(sp.N(caps[ks[0]] - caps[ks[1]], 50)) < 1e-40)
                gsol['equal_plane_distances'] = bool(abs(sp.N(planes[ks[0]] - planes[ks[1]], 50)) < 1e-40)
                check(f'{cname} {lab}: y float {gsol["y_float"]} vs exact {gsol["y_exact_edge1"]} (scaled)', True)
    print(json.dumps(rec)[:900], flush=True)
    out.append(rec)
json.dump({'catalan': out, 'checks': CHECKS}, open(os.path.join(DATA, 's2-catalan.json'), 'w'), indent=1)
print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks passed')
