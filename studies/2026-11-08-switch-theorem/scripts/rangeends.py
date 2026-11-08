# Switch theorem, part 3: the ends of the coexistence range (Theorem C, #53 Observation 4), exact.
# For a site a of kind A (weight lam), its cell is nonempty iff lam >= m_a,  m_a = min over x in V_A(a) of
#   f_a(x) = max_b (|x - a|^2 - |x - b|^2)   (b over the B sites; V_A(a) = Voronoi cell of a among the A sites),
# a linear programme. f_a(a) = -d_a^2 (d_a = nearest unlike distance), and m_a = -d_a^2 iff a lies in the convex hull of its
# nearest unlike neighbours. The same for B with the sign reversed (upper end +m_b... = d_b^2 iff b in the hull of its nearest A).
# Here: (1) the hull test, exactly, for every motif site of all twelve networks; (2) the LP, solved by floats and certified
# exactly (exact primal vertex from its tight constraints, exact feasibility against a larger site list, exact non-negative dual
# multipliers on the tight constraints); (3) the ends compared with the exact walks (#53 data; our walks for the controls).
import json, os, sys
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__))
RELAY = os.path.join(HERE, "..", "..", "2026-10-25-relay-census")
sys.path.insert(0, os.path.join(RELAY, "scripts"))
import extra_nets  # noqa: E402,F401
from engine import Net, gdot, vsub, solve, rank  # noqa: E402
from networks import NETS  # noqa: E402

checks = []


def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)


def in_hull(x, S):
    """Exact: is x in conv(S)? (Caratheodory: some simplex of at most d+1 points of S contains x.)"""
    d = len(x)
    for k in range(1, d + 2):
        for T in combinations(S, k):
            # solve sum mu_i T_i = x, sum mu_i = 1 (least-determined systems via exact elimination on independent rows)
            M = [[T[i][r] for i in range(k)] for r in range(d)] + [[Fr(1)] * k]; rhs = [x[r] for r in range(d)] + [Fr(1)]
            # pick k independent rows
            rows = []
            for r in range(d + 1):
                if rank([tuple(M[q]) for q in rows + [r]]) == len(rows) + 1: rows.append(r)
                if len(rows) == k: break
            if len(rows) < k: continue
            X = solve([M[r] for r in rows], [[rhs[r]] for r in rows])
            if X is None: continue
            mu = [X[i][0] for i in range(k)]
            if all(m >= 0 for m in mu) and all(sum(M[r][i] * mu[i] for i in range(k)) == rhs[r] for r in range(d + 1)):
                return True
    return False


def lp_min(net, i, R2):
    """m_i = min_x max_{unlike b} (|x-c|^2 - |x-b|^2) over x in V_same(c); exact certificate. Returns (m, x*)."""
    ki, c = net.motif[i]; d = net.d; G = net.G
    near = net.sites_near(i, R2)
    rows, rhs, tag = [], [], []
    # variables (x, t). unlike b: 2 x.G(b - c) + |c|^2 - |b|^2 - t <= 0 ; like a': 2 x.G(a' - c) <= |a'|^2 - |c|^2
    for j, kv, p in near:
        g = [2 * sum(G[r][s] * (p[s] - c[s]) for s in range(d)) for r in range(d)]
        if net.motif[j][0] != ki:
            rows.append(g + [Fr(-1)]); rhs.append(gdot(G, p, p) - gdot(G, c, c)); tag.append(("u", p))
        else:
            rows.append(g + [Fr(0)]); rhs.append(gdot(G, p, p) - gdot(G, c, c)); tag.append(("l", p))
    Af = np.array([[float(v) for v in r] for r in rows]); bf = np.array([float(v) for v in rhs])
    res = linprog(np.r_[np.zeros(d), 1.0], A_ub=Af, b_ub=bf, bounds=[(None, None)] * (d + 1), method="highs")
    assert res.status == 0
    z = res.x; sl = bf - Af @ z
    tight = [k for k in np.argsort(sl) if sl[k] < 1e-7]
    for T in combinations(tight, d + 1):
        X = solve([rows[k] for k in T], [[rhs[k]] for k in T])
        if X is None: continue
        zx = [X[r][0] for r in range(d + 1)]
        if not all(sum(a * b for a, b in zip(rows[k], zx)) <= rhs[k] for k in range(len(rows))): continue
        # dual: sum_k y_k rows_k = -(0,..,0,1) i.e. objective gradient, y >= 0 on tight set
        TT = [k for k in tight if sum(a * b for a, b in zip(rows[k], zx)) == rhs[k]]
        for U in combinations(TT, d + 1):
            Y = solve([[rows[k][r] for k in U] for r in range(d + 1)], [[Fr(0)] for _ in range(d)] + [[Fr(-1)]])
            if Y is not None and all(Y[q][0] >= 0 for q in range(d + 1)):
                # y >= 0 with sum y_k rows_k = -(0, ..., 0, 1): KKT certificate for min t
                return zx[d], tuple(zx[:d])
    raise AssertionError("no exact certificate")


def walk_range(key):
    p = os.path.join(RELAY, "data", "raw", key + ".json")
    if not os.path.exists(p): p = os.path.join(HERE, "..", "data", key + "-walk.json")
    r = json.load(open(p)); return Fr(r["intervals"][0]["lo"]), Fr(r["intervals"][-1]["hi"])


KEYS = ["square", "honeycomb", "kagome", "bcc", "delian", "nacl", "zincblende", "hcpholes", "a15", "c15", "hbn", "sodalite"]
if __name__ == "__main__":
    out = {}
    for key in KEYS:
        spec = NETS[key]; net = Net(spec["name"], spec["G"], spec["T"], spec["motif"], spec["w"]); A, B = spec["A"], spec["B"]
        lo, hi = walk_range(key); ends = {A: [], B: []}; rec = []
        for i, (ki, c) in enumerate(net.motif):
            nb = net.sites_near(i, Fr(spec["D2"]))
            un = [(gdot(net.G, vsub(p, c), vsub(p, c)), p) for j, kv, p in nb if net.motif[j][0] != ki]
            d2 = min(x for x, _ in un); S = [p for x, p in un if x == d2]
            inside = in_hull(c, S)
            m, xs = lp_min(net, i, Fr(spec["D2"]))
            m2, _ = lp_min(net, i, 2 * Fr(spec["D2"]))        # larger site list: same optimum
            ok = (m == m2) and (m <= -d2) and ((m == -d2) == inside)   # m <= f(c) = -d^2 always
            check(f"{key} site {i} ({ki}): LP min = {m}, -d^2 = {-d2}, in hull of its {len(S)} nearest unlike: {inside}", ok,
                  f"minimiser {tuple(str(v) for v in xs)}")
            ends[ki].append(m); rec.append(dict(i=i, kind=ki, d2=str(d2), n_nearest=len(S), in_hull=inside, m=str(m),
                                               argmin=[str(v) for v in xs]))
        pred_lo, pred_hi = max(ends[A]), -max(ends[B])
        check(f"{key}: range predicted ({pred_lo}, {pred_hi}) = exact walk ({lo}, {hi})", (pred_lo, pred_hi) == (lo, hi))
        out[key] = dict(sites=rec, range=[str(pred_lo), str(pred_hi)])
    json.dump(out, open(os.path.join(HERE, "..", "data", "rangeends.json"), "w"), indent=1)
    with open(os.path.join(HERE, "..", "data", "rangeends-checks.txt"), "w") as fh:
        for s, n, det in checks: fh.write(f"{s} {n} {det}\n")
    nf = sum(1 for c in checks if c[0] == "FAIL")
    print(f"{len(checks) - nf}/{len(checks)} PASS")
    print('FINAL ok' if checks and nf == 0 else f'FINAL FAIL: {nf} of {len(checks)} checks failed')
