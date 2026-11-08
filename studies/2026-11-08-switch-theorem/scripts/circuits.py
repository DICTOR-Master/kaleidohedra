# Switch theorem, part 1: the flip formula, tested against #53 (Global Web of Bonds, relay census) by brute force.
#
# Lifted orientation test (Edelsbrunner-Shah 1996): d+2 sites p_0..p_{d+1} with weights w_i are co-power-spherical (their lifted
# points (p_i, |p_i|^2 - w_i) lie on one hyperplane) iff det[[p_i, |p_i|^2 - w_i, 1]] = 0. Expanding along the lift column,
# det = c * sum_i alpha_i (|p_i|^2 - w_i), alpha = the affine dependence of the p_i (sum alpha_i p_i = 0, sum alpha_i = 0).
# With w_A = lam, w_B = 0 this is affine in lam:  D(lam) = S0 - lam * SA,  S0 = sum alpha_i |p_i|^2,  SA = sum_{i in A} alpha_i.
# So each circuit has at most one switch value lam* = S0 / SA (none if SA = 0 and S0 != 0, every lam if both vanish).
#
# Claim tested: the interior flips of each network (#53 Table 2) are exactly the values S0/SA, inside the open coexistence range,
# of the (d+2)-sets with d+1 affinely independent sites whose power sphere at lam* is empty (no site of smaller power).
# Completeness: every site of a dual cell lies within rho of the cell's power vertex (rho = largest corner-to-own-site distance,
# #53 data), so the sites of any dual cell are pairwise within 2 rho; every (d+2)-set with pairwise squared distance <= (2 rho)^2
# is enumerated, with its lexicographically smallest site in the motif (translation invariance).
# Floats only choose candidates (tolerances 1e-9 on lam, 1e-7 on power slack); every accepted value is decided in Fractions.
# Usage: python circuits.py [net ...]
import json, os, sys, time
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RELAY = os.path.join(HERE, "..", "..", "2026-10-25-relay-census")
sys.path.insert(0, os.path.join(RELAY, "scripts"))
from engine import Net, gdot, vsub, solve  # noqa: E402
from networks import NETS  # noqa: E402
import extra_nets  # noqa: E402,F401  (adds the two control networks hbn, sodalite to NETS)

checks = []


def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)


def census_record(key):
    """Range, interior flips and rho of #53's exact walk (relay census raw data), or of our own walk for the control nets."""
    p = os.path.join(RELAY, "data", "raw", key + ".json")
    if not os.path.exists(p):
        p = os.path.join(HERE, "..", "data", key + "-walk.json")
    d = json.load(open(p))
    ivs = d["intervals"]
    lo, hi = Fr(ivs[0]["lo"]), Fr(ivs[-1]["hi"])
    flips = sorted(set(Fr(iv["lo"]) for iv in ivs[1:]))
    rho = max(s.get("rho", 0) for iv in ivs for s in iv["sites"])
    return lo, hi, flips, rho


def exact_alpha(P):
    """Affine dependence of d+2 points (Fractions): alpha_i = (-1)^i det(M without column i), M = [[p_i]; [1]]."""
    n = len(P); d = n - 2
    M = [[P[i][r] for i in range(n)] for r in range(d)] + [[Fr(1)] * n]

    def det(A):
        A = [row[:] for row in A]; m = len(A); s = Fr(1)
        for c in range(m):
            piv = next((r for r in range(c, m) if A[r][c] != 0), None)
            if piv is None: return Fr(0)
            if piv != c: A[c], A[piv] = A[piv], A[c]; s = -s
            s *= A[c][c]
            for r in range(c + 1, m):
                f = A[r][c] / A[c][c]
                for k in range(c, m): A[r][k] -= f * A[c][k]
        return s
    return [(-1) ** i * det([[row[k] for k in range(n) if k != i] for row in M]) for i in range(n)]


def run(key):
    spec = NETS[key]; t0 = time.time()
    net = Net(spec["name"], spec["G"], spec["T"], spec["motif"], spec["w"])
    d = net.d; A = spec["A"]
    lo, hi, flips, rho = census_record(key)
    Dp2 = Fr((2 * rho * 1.001) ** 2).limit_denominator(1000) + Fr(1, 100)
    span = float(max(abs(lo), abs(hi)))
    Rcl = 2 * rho + np.sqrt(rho ** 2 + 2 * span) + 0.5   # cloud radius for the emptiness test (asserted per candidate)
    Gf = np.array([[float(x) for x in r] for r in net.G])
    found = {}   # exact lam* -> list of circuits
    ncand = nfloat = 0
    for i, (ki, ci) in enumerate(net.motif):
        near = [(j, kv, c) for j, kv, c in net.sites_near(i, Dp2) if tuple(c) > tuple(ci)]
        cloud = [(j, kv, c) for j, kv, c in net.sites_near(i, Fr(Rcl ** 2).limit_denominator(100))] + [(i, (0,) * d, ci)]
        Xc = np.array([[float(x) for x in c] for _, _, c in cloud]); Ac = np.array([net.motif[j][0] == A for j, _, _ in cloud])
        Xn = np.array([[float(x) for x in c] for _, _, c in near]); An = np.array([net.motif[j][0] == A for j, _, _ in near])
        x0 = np.array([float(x) for x in ci])
        # adjacency: pairwise squared distance <= Dp2
        diff = Xn[:, None, :] - Xn[None, :, :]
        D2 = np.einsum("abi,ij,abj->ab", diff, Gf, diff)
        adj = D2 <= float(Dp2) + 1e-9
        idx = list(range(len(near)))
        combos = []

        def grow(cur, cand):
            if len(cur) == d + 1:
                combos.append(tuple(cur)); return
            for t, v in enumerate(cand):
                grow(cur + [v], [u for u in cand[t + 1:] if adj[v, u]])
        grow([], idx)
        if not combos: continue
        C = np.array(combos)                                   # (k, d+1)
        P = np.concatenate([np.broadcast_to(x0, (len(C), 1, d)), Xn[C]], axis=1)    # (k, d+2, d)
        isA = np.concatenate([np.full((len(C), 1), ki == A), An[C]], axis=1)
        M = np.concatenate([P.transpose(0, 2, 1), np.ones((len(C), 1, d + 2))], axis=1)  # (k, d+1, d+2)
        alpha = np.stack([(-1) ** q * np.linalg.det(np.delete(M, q, axis=2)) for q in range(d + 2)], axis=1)
        sq = np.einsum("kpi,ij,kpj->kp", P, Gf, P)
        S0 = (alpha * sq).sum(1); SA = (alpha * isA).sum(1)
        scale = np.abs(alpha).sum(1)
        ok = (scale > 1e-9) & (np.abs(SA) > 1e-9 * scale)
        with np.errstate(divide="ignore", invalid="ignore"):
            lam = np.where(ok, S0 / np.where(ok, SA, 1), np.nan)
        sel = np.where(ok & (lam > float(lo) - 1e-9) & (lam < float(hi) + 1e-9))[0]
        ncand += len(C)
        for k in sel:
            L = lam[k]; w = np.where(isA[k], L, 0.0)
            # power vertex: 2 (p_q - p_0)^T G c = (|p_q|^2 - w_q) - (|p_0|^2 - w_0)
            Aq = 2 * (P[k, 1:] - P[k, 0]) @ Gf; bq = (sq[k, 1:] - w[1:]) - (sq[k, 0] - w[0])
            c, *_ = np.linalg.lstsq(Aq, bq, rcond=None)
            pi = (c - P[k, 0]) @ Gf @ (c - P[k, 0]) - w[0]
            dv = Xc - c; pw = np.einsum("ai,ij,aj->a", dv, Gf, dv) - np.where(Ac, L, 0.0)
            if pw.min() - pi < -1e-7: continue
            nfloat += 1
            key_f = round(L, 7)
            found.setdefault(key_f, []).append((i, [near[q] for q in C[k]], c, pi))
    # exact decision, one float root at a time
    exact = {}
    for key_f, cands in sorted(found.items()):
        for i, rest, cf, pif in cands:
            pts = [(i, (0,) * d, net.motif[i][1])] + rest
            Pq = [c for _, _, c in pts]; kinds = [net.motif[j][0] for j, _, _ in pts]
            al = exact_alpha(Pq)
            S0 = sum(a * gdot(net.G, p, p) for a, p in zip(al, Pq)); SA = sum(a for a, k in zip(al, kinds) if k == A)
            if SA == 0: continue
            L = S0 / SA
            if not (lo < L < hi): continue
            w = [L if k == A else Fr(0) for k in kinds]
            # exact power vertex from d+1 independent sites of the circuit
            sol = None
            for sub in combinations(range(d + 2), d + 1):
                p0 = Pq[sub[0]]
                Am = [[2 * x for x in [sum(net.G[r][s] * (Pq[q][s] - p0[s]) for s in range(d)) for r in range(d)]] for q in sub[1:]]
                bm = [[(gdot(net.G, Pq[q], Pq[q]) - w[q]) - (gdot(net.G, p0, p0) - w[sub[0]])] for q in sub[1:]]
                X = solve(Am, bm)
                if X is not None:
                    sol = tuple(X[r][0] for r in range(d)); break
            if sol is None: continue
            dv0 = vsub(sol, Pq[0]); pi = gdot(net.G, dv0, dv0) - w[0]
            allpw = [gdot(net.G, vsub(sol, q), vsub(sol, q)) - wq for q, wq in zip(Pq, w)]
            assert all(x == pi for x in allpw), "circuit not co-power-spherical at its root"
            # the cloud covers the ball of every site that could undercut pi
            rad = float(np.sqrt(max(float(pi) + float(max(abs(lo), abs(hi))), 0)))
            dist0 = float(np.sqrt(float(gdot(net.G, vsub(sol, net.motif[i][1]), vsub(sol, net.motif[i][1])))))
            assert dist0 + rad < Rcl - 0.25, "cloud too small"
            cloud = net.sites_near(i, Fr(Rcl ** 2).limit_denominator(100)) + [(i, (0,) * d, net.motif[i][1])]
            empty = all(gdot(net.G, vsub(sol, c), vsub(sol, c)) - (L if net.motif[j][0] == A else 0) >= pi for j, _, c in cloud)
            if empty:
                on = sorted((net.motif[j][0], tuple(str(x) for x in c)) for j, _, c in cloud
                            if gdot(net.G, vsub(sol, c), vsub(sol, c)) - (L if net.motif[j][0] == A else 0) == pi)
                exact.setdefault(L, dict(circuit=[(k, [str(x) for x in p]) for k, p in zip(kinds, Pq)],
                                         alpha=[str(a) for a in al], S0=str(S0), SA=str(SA), vertex=[str(x) for x in sol],
                                         power=str(pi), cell_sites=len(on),
                                         cell_kinds={k: sum(1 for kk, _ in on if kk == k) for k in sorted(set(kk for kk, _ in on))}))
                break
    got = sorted(exact)
    print(f"{key}: {ncand} (d+2)-sets, {nfloat} float candidates with empty power sphere, exact roots {[str(x) for x in got]}; "
          f"#53 flips {[str(x) for x in flips]}; {time.time() - t0:.1f} s", flush=True)
    for L in got:
        e = exact[L]
        print(f"   lam* = {L}: circuit {e['circuit']} alpha {e['alpha']} S0 = {e['S0']} SA = {e['SA']}; "
              f"dual cell {e['cell_sites']} sites {e['cell_kinds']}", flush=True)
    check(f"{key}: the empty-sphere circuit roots in ({lo}, {hi}) are exactly the flips of the exact walk", got == flips,
          f"roots {[str(x) for x in got]} flips {[str(x) for x in flips]}")
    return {str(L): exact[L] for L in got}


if __name__ == "__main__":
    keys = sys.argv[1:] or ["square", "honeycomb", "kagome", "bcc", "delian", "nacl", "zincblende", "hcpholes", "a15", "c15", "hbn", "sodalite"]
    out = {}
    for key in keys:
        out[key] = run(key)
    tag = "-".join(keys) if len(keys) < 4 else "all"
    json.dump(out, open(os.path.join(HERE, "..", "data", f"circuits-{tag}.json"), "w"), indent=1)
    with open(os.path.join(HERE, "..", "data", f"circuits-{tag}-checks.txt"), "w") as fh:
        for s, n, det in checks: fh.write(f"{s} {n} {det}\n")
    nf = sum(1 for c in checks if c[0] == "FAIL")
    print(f"{len(checks) - nf}/{len(checks)} PASS")
    print('FINAL ok' if checks and nf == 0 else f'FINAL FAIL: {nf} of {len(checks)} checks failed')
