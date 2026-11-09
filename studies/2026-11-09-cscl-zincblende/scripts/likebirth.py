# #53 Observation 3 (which networks switch): the like-bond births read off the sites by a linear programme (Proposition D).
#
# For a site a of kind K, let f_a(x) = max over unlike sites b of (|x-a|^2 - |x-b|^2) (affine in x for each b: a convex
# piecewise-affine function), and U_a(l) = {x : f_a(x) <= l}, the cell a would have against the unlike sites alone.
# Claim (Proposition D): inside the open coexistence range, the A cells have an A-A facet  <=>  lam > tau_A, and the B cells have a
# B-B facet  <=>  -lam > tau_B, where
#     tau_K = min over like pairs (a, a') of  min_x max(f_a(x), f_a'(x))        (an LP for each pair).
# So A-A bonds live on (tau_A, hi], B-B bonds on [lo, -tau_B); the hand-over is gradual iff tau_A < -tau_B, a single switch iff
# tau_A = -tau_B in the open range, and tau_A > -tau_B is impossible (it would give an interval of switch points; Theorem B).
# Here: tau_A, tau_B for all twelve networks of the switch-theorem study (exact LP certificates; a proved bound on which pairs can
# matter), compared with the bond lives of the exact walks. Also the "midpoint value" l^2/4 - delta^2 (l = like distance,
# delta = distance from the bond midpoint to the nearest unlike site), which equals the pair's LP value whenever the midpoint
# is a centre of symmetry of the two-kind site set (then a minimiser can be taken at the midpoint, by convexity).
import json, os, sys, math
from fractions import Fraction as Fr
from itertools import combinations, product
import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
RELAY = os.path.join(HERE, "..", "..", "2026-10-25-relay-census")
SWITCH = os.path.join(HERE, "..", "..", "2026-11-08-switch-theorem")
sys.path.insert(0, os.path.join(RELAY, "scripts")); sys.path.insert(0, os.path.join(SWITCH, "scripts"))
from engine import Net, Cell, gdot, vsub, vadd, solve  # noqa: E402
from networks import NETS  # noqa: E402
import extra_nets  # noqa: E402,F401
checks = []


def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)


def exact_lp(rows, rhs, d):
    """min t over (x, t) s.t. rows.(x,t) <= rhs; floats find the vertex, exact primal vertex + exact non-negative dual certify it."""
    Af = np.array([[float(v) for v in r] for r in rows]); bf = np.array([float(v) for v in rhs])
    res = linprog(np.r_[np.zeros(d), 1.0], A_ub=Af, b_ub=bf, bounds=[(None, None)] * (d + 1), method="highs")
    assert res.status == 0, res.message
    z = res.x; sl = bf - Af @ z
    tight = [k for k in np.argsort(sl) if sl[k] < 1e-7]
    for T in combinations(tight, d + 1):
        X = solve([rows[k] for k in T], [[rhs[k]] for k in T])
        if X is None: continue
        zx = [X[r][0] for r in range(d + 1)]
        if not all(sum(a * b for a, b in zip(rows[k], zx)) <= rhs[k] for k in range(len(rows))): continue
        TT = [k for k in tight if sum(a * b for a, b in zip(rows[k], zx)) == rhs[k]]
        for U in combinations(TT, d + 1):
            Y = solve([[rows[k][r] for k in U] for r in range(d + 1)], [[Fr(0)] for _ in range(d)] + [[Fr(-1)]])
            if Y is not None and all(Y[q][0] >= 0 for q in range(d + 1)):
                return zx[d], tuple(zx[:d])
    raise AssertionError("no exact certificate")


def all_sites(net, centre, R2):
    """All sites (kind, coords) within G-distance^2 R2 of the point centre."""
    TG = np.array([[float(gdot(net.G, a, b)) for b in net.T] for a in net.T])
    K = int(np.ceil(np.sqrt(float(R2) / np.linalg.eigvalsh(TG).min()))) + 3
    # integer translation range around centre
    Tm = np.array([[float(x) for x in v] for v in net.T]).T
    k0 = np.round(np.linalg.solve(Tm, np.array([float(x) for x in centre]))).astype(int)
    out = []
    for kv in product(*[range(k0[q] - K, k0[q] + K + 1) for q in range(net.d)]):
        t = tuple(sum(kv[q] * net.T[q][r] for q in range(net.d)) for r in range(net.d))
        for k, c in net.motif:
            p = vadd(c, t); dv = vsub(p, centre)
            if gdot(net.G, dv, dv) <= R2: out.append((k, p))
    return out


def fpieces(net, a, Ub):
    """rows for t >= 2 x.G(b - a) + |a|^2 - |b|^2  (b in Ub):  2 G(b-a).x - t <= |b|^2 - |a|^2."""
    d = net.d; rows, rhs = [], []
    for b in Ub:
        g = [2 * sum(net.G[r][s] * (b[s] - a[s]) for s in range(d)) for r in range(d)]
        rows.append(g + [Fr(-1)]); rhs.append(gdot(net.G, b, b) - gdot(net.G, a, a))
    return rows, rhs


def f_exact(net, a, x, U):
    return max(gdot(net.G, vsub(x, a), vsub(x, a)) - gdot(net.G, vsub(x, b), vsub(x, b)) for b in U)


def covering_r2(net, kind):
    """Squared covering radius of the sites of one kind (max corner distance of its Voronoi cell), exact corners from the engine."""
    mot = [(k, c) for k, c in net.motif if k == kind]
    sub = Net("sub", net.G, net.T, mot, {kind: (0, 0)})
    best = Fr(0)
    for i in range(len(mot)):
        D2 = Fr(16) * max(gdot(net.G, v, v) for v in net.T)
        E = Cell(sub, i, (Fr(0),), D2)
        ok, rho = E.bound_ok([(Fr(0),)])
        assert ok
        for c in E.corners:
            dv = vsub(c["p0"], mot[i][1]); best = max(best, gdot(net.G, dv, dv))
    return best


def is_site(net, kind, p):
    Tm = [[net.T[q][r] for q in range(net.d)] for r in range(net.d)]
    for k, c in net.motif:
        if k != kind: continue
        X = solve(Tm, [[x] for x in vsub(p, c)])
        if X is not None and all(X[r][0].denominator == 1 for r in range(net.d)): return True
    return False


def walk(key):
    p = os.path.join(RELAY, "data", "raw", key + ".json")
    if not os.path.exists(p): p = os.path.join(SWITCH, "data", key + "-walk.json")
    return json.load(open(p))


KEYS = ["square", "honeycomb", "kagome", "bcc", "delian", "nacl", "zincblende", "hcpholes", "a15", "c15", "hbn", "sodalite"]


def tau(net, K, Ukind, R2cov):
    """tau_K: min over like pairs of the pair LP. Pairs with l^2/4 - R2cov >= current best are provably irrelevant
    (f_a(x) >= |x-a|^2 - R2cov, and one of a, a' is at distance >= l/2 from x)."""
    best, arg = None, None; recs = []; mids = []
    Ksites = [(i, c) for i, (k, c) in enumerate(net.motif) if k == K]
    r2 = max(gdot(net.G, v, v) for v in net.T)
    lmin2 = min(gdot(net.G, vsub(p, c), vsub(p, c)) for _, c in Ksites for k, p in all_sites(net, c, 4 * r2) if k == K and p != c)
    # the nearest like pair has LP value <= lmin2/4 (its midpoint value), so only pairs with l^2 <= lmin2 + 4 R2cov can matter
    L2 = sorted(set(gdot(net.G, vsub(p, c), vsub(p, c)) for _, c in Ksites
                    for k, p in all_sites(net, c, lmin2 + 4 * R2cov) if k == K and p != c))
    for l2 in L2:
        if best is not None and l2 / 4 - R2cov >= best: break
        for i, a in Ksites:
            for k, a2 in all_sites(net, a, l2):
                if k != K or a2 == a or gdot(net.G, vsub(a2, a), vsub(a2, a)) != l2: continue
                m = tuple((x + y) / 2 for x, y in zip(a, a2))
                R2u = l2 / 4 + 4 * R2cov + 4
                U = [p for kk, p in all_sites(net, m, R2u) if kk == Ukind]
                r1, h1 = fpieces(net, a, U); r2, h2 = fpieces(net, a2, U)
                t, x = exact_lp(r1 + r2, h1 + h2, net.d)
                # exact feasibility against every unlike site that could matter: term <= t iff |x-b|^2 >= |x-a|^2 - t
                need = max(gdot(net.G, vsub(x, a), vsub(x, a)), gdot(net.G, vsub(x, a2), vsub(x, a2))) - t
                Ubig = [p for kk, p in all_sites(net, x, need + 1) if kk == Ukind]
                assert max(f_exact(net, a, x, Ubig), f_exact(net, a2, x, Ubig)) == t, "LP optimum not exact on the full site set"
                dmid = min(gdot(net.G, vsub(m, p), vsub(m, p)) for p in Ubig + U)
                inv = all(is_site(net, kk, tuple(2 * mm - pp for mm, pp in zip(m, p)))
                          for kk, p in all_sites(net, m, R2u))
                recs.append(dict(l2=str(l2), a=[str(v) for v in a], a2=[str(v) for v in a2], tau=str(t), argmin=[str(v) for v in x],
                                 midpoint_value=str(l2 / 4 - dmid), midpoint_inversion=inv))
                if inv:
                    mids.append(t == l2 / 4 - dmid)
                if best is None or t < best: best, arg = t, recs[-1]
    return best, arg, recs, mids


if __name__ == "__main__":
    out = {}
    for key in KEYS:
        spec = NETS[key]; net = Net(spec["name"], spec["G"], spec["T"], spec["motif"], spec["w"]); A, B = spec["A"], spec["B"]
        W = walk(key); lo, hi = Fr(W["intervals"][0]["lo"]), Fr(W["intervals"][-1]["hi"])
        AA, BB = f"{A}-{A}", f"{B}-{B}"
        has = lambda iv, t: any(bt == t or bt.startswith(t + "@") for bt in iv["bond_types"])
        ivA = [iv for iv in W["intervals"] if has(iv, AA)]; ivB = [iv for iv in W["intervals"] if has(iv, BB)]
        birthA = min(Fr(iv["lo"]) for iv in ivA) if ivA else None      # A-A alive on (birthA, hi) inside the range
        deathB = max(Fr(iv["hi"]) for iv in ivB) if ivB else None      # B-B alive on (lo, deathB)
        RA, RB = covering_r2(net, A), covering_r2(net, B)
        tA, argA, recA, midA = tau(net, A, B, RB)
        tB, argB, recB, midB = tau(net, B, A, RA)
        predA = max(tA, lo) if tA < hi else None; predB = min(-tB, hi) if -tB > lo else None
        okA = (predA == birthA); okB = (predB == deathB)
        if predA is not None and predB is not None:
            typ = "gradual" if tA < -tB else ("switch" if tA == -tB else "IMPOSSIBLE")
        else:
            typ = "one like bond only"
        wtyp = ("gradual" if (birthA is not None and deathB is not None and birthA < deathB) else
                "switch" if (birthA is not None and birthA == deathB) else "one like bond only")
        check(f"{key}: tau_{A} = {tA} (A-A born at {birthA} in the walk), tau_{B} = {tB} (B-B dies at {deathB}); "
              f"type from tau: {typ}, from the walk: {wtyp}", okA and okB and typ == wtyp,
              f"range ({lo}, {hi}); minimising pairs: {A} l^2 = {argA['l2']} at x = {argA['argmin']}, {B} l^2 = {argB['l2']} at x = {argB['argmin']}")
        check(f"{key}: tau_A + tau_B = {tA + tB} <= 0", tA + tB <= 0 or typ == "one like bond only")
        if midA or midB:
            check(f"{key}: midpoint rule l^2/4 - delta^2 = pair LP value for every inversion-symmetric like pair "
                  f"({sum(midA) + sum(midB)}/{len(midA) + len(midB)})", all(midA + midB))
        out[key] = dict(range=[str(lo), str(hi)], tau={A: str(tA), B: str(tB)}, type=typ, walk_type=wtyp,
                        covering_r2={A: str(RA), B: str(RB)}, pairs={A: recA, B: recB})
    json.dump(out, open(os.path.join(HERE, "..", "data", "likebirth.json"), "w"), indent=1)
    with open(os.path.join(HERE, "..", "data", "likebirth-checks.txt"), "w") as fh:
        for s_, n, det in checks: fh.write(f"{s_} {n} {det}\n")
    nf = sum(1 for c in checks if c[0] == "FAIL")
    print(f"{len(checks) - nf}/{len(checks)} PASS")
    print('FINAL ok' if checks and nf == 0 else f'FINAL FAIL: {nf} of {len(checks)} checks failed')
