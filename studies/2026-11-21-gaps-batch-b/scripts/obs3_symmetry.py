# Item 1 (#53 Observation 3): tau_A + tau_B against site symmetry on the twelve networks.
#
# Inputs (reused, not recomputed): the twelve networks of the relay census + the two controls of the switch-theorem study
# (exact sites, metric G, translations T), and tau_A, tau_B from study 2026-11-09-cscl-zincblende (data/likebirth.json,
# exact LP certificates, 33/33 PASS there).
# New here, all exact (Fractions):
#  (1) the symmetry group of each two-kind site set modulo T: every isometry x -> Rx + t of the lattice that maps the site
#      set to itself, keeping the kinds ("sym") or exchanging them ("swap");
#  (2) the site symmetry group of each kind (point group order and element types), centrosymmetry;
#  (3) the Voronoi cells of the union at equal weights (lam = 0), built with the relay-census engine (exact corners):
#      which neighbours are like;
#  (4) the swap corollary: if an isometry exchanges the kinds, then tau_A = tau_B <= 0, and the hand-over is a single switch
#      (at lam = 0) iff no Voronoi cell of the union at equal weights has a like neighbour;
#  (5) the distance rule: mu_K = min over like pairs of (l^2/4 - delta^2) is always >= tau_K, with equality whenever a
#      minimising pair has an inversion centre at its midpoint;
#  (6) the counterexample to "site symmetry alone decides": two networks with the same site symmetry groups and opposite types;
#  (7) the d-dimensional CsCl family (Z^d + its cube centres): tau = 2 - d (in units of the half edge) by the distance rule,
#      checked by the LP for d = 1..4.
import json, os, sys
from fractions import Fraction as Fr
from itertools import product, combinations
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(ST, "2026-10-25-relay-census", "scripts"))
sys.path.insert(0, os.path.join(ST, "2026-11-08-switch-theorem", "scripts"))
from engine import Net, Cell, gdot, vsub, vadd, solve  # noqa: E402
from networks import NETS  # noqa: E402
import extra_nets  # noqa: E402,F401

checks = []


def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)


KEYS = ["square", "honeycomb", "kagome", "bcc", "delian", "nacl", "zincblende", "hcpholes", "a15", "c15", "hbn", "sodalite"]
LABEL = {"square": "square + centres", "honeycomb": "honeycomb + centres", "kagome": "kagome + centres", "bcc": "CsCl",
         "delian": "fluorite", "nacl": "rock salt", "zincblende": "zinc blende", "hcpholes": "hcp holes", "a15": "A15",
         "c15": "C15", "hbn": "h-BN (control)", "sodalite": "sodalite (control)"}
LB = json.load(open(os.path.join(ST, "2026-11-09-cscl-zincblende", "data", "likebirth.json")))


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def inv(M):
    d = len(M); X = solve(M, [[Fr(int(i == j)) for j in range(d)] for i in range(d)])
    return X


def lattice_vectors(G, Bm, n2, K=3):
    d = len(G); out = []
    for k in product(range(-K, K + 1), repeat=d):
        v = tuple(sum(Bm[r][q] * k[q] for q in range(d)) for r in range(d))
        if gdot(G, v, v) == n2: out.append(v)
    return out


def point_group(G, T):
    """All rational R (site coordinates) with R(L) = L and R^T G R = G, L the lattice spanned by T."""
    d = len(G); Bm = [[T[q][r] for q in range(d)] for r in range(d)]  # columns = T vectors
    Binv = inv(Bm)
    gram = [[gdot(G, T[a], T[b]) for b in range(d)] for a in range(d)]
    cands = [lattice_vectors(G, Bm, gram[a][a]) for a in range(d)]
    Rs = []
    for W in product(*cands):
        if any(gdot(G, W[a], W[b]) != gram[a][b] for a in range(d) for b in range(a + 1, d)): continue
        Wm = [[W[q][r] for q in range(d)] for r in range(d)]
        R = matmul(Wm, Binv)
        Rs.append(R)
    return Rs


def apply(R, t, p):
    return tuple(sum(R[r][c] * p[c] for c in range(len(p))) + t[r] for r in range(len(p)))


def mod_T(net, p):
    """Reduce p modulo the lattice of T (exact): coordinates in the T basis taken mod 1."""
    d = net.d; Tm = [[net.T[q][r] for q in range(d)] for r in range(d)]
    X = solve(Tm, [[x] for x in p]); f = [X[r][0] - (X[r][0].numerator // X[r][0].denominator) for r in range(d)]
    return tuple(sum(net.T[q][r] * f[q] for q in range(d)) for r in range(d))


def space_group(net):
    sites = {mod_T(net, c): k for k, c in net.motif}
    kinds = sorted(set(sites.values()))
    other = {kinds[0]: kinds[1], kinds[1]: kinds[0]}
    ops = {"sym": [], "swap": []}
    k0, p0 = net.motif[0]
    for R in point_group(net.G, net.T):
        Rp0 = apply(R, (0,) * net.d, p0)
        for s, ks in sites.items():
            t = vsub(s, Rp0)
            typ = "sym" if ks == k0 else "swap"
            ok = True
            for q, kq in sites.items():
                img = mod_T(net, apply(R, t, q))
                if img not in sites or sites[img] != (kq if typ == "sym" else other[kq]): ok = False; break
            if ok: ops[typ].append((R, mod_T(net, t)))
    return ops, sites


def eltype(R):
    d = len(R)
    det = round(float(np.linalg.det(np.array([[float(x) for x in r] for r in R]))))
    tr = sum(R[i][i] for i in range(d))
    return (det, int(tr))


# element types -> names. 3D: (det, trace): 1 (1,3), 2 (1,-1), 3 (1,0), 4 (1,1), 6 (1,2), -1 (-1,-3), m (-1,1), -3 (-1,0),
# -4 (-1,-1), -6 (-1,-2). 2D: 1 (1,2), 2 (1,-2), 3 (1,-1), 4 (1,0), 6 (1,1), m (-1,0).
N3 = {(1, 3): "1", (1, -1): "2", (1, 0): "3", (1, 1): "4", (1, 2): "6", (-1, -3): "-1", (-1, 1): "m", (-1, 0): "-3",
      (-1, -1): "-4", (-1, -2): "-6"}
N2 = {(1, 2): "1", (1, -2): "2", (1, -1): "3", (1, 0): "4", (1, 1): "6", (-1, 0): "m"}
# point groups by their element-type counts (the ones that occur; an unknown signature is a FAIL, not a guess)
PG = {
    # 2D
    (("1", 1), ("2", 1), ("4", 2), ("m", 4)): "4mm (D4)", (("1", 1), ("3", 2), ("m", 3)): "3m (D3)",
    (("1", 1), ("2", 1), ("3", 2), ("6", 2), ("m", 6)): "6mm (D6)", (("1", 1), ("2", 1), ("m", 2)): "2mm (D2)",
    # 3D
    (("-1", 1), ("-3", 8), ("-4", 6), ("1", 1), ("2", 9), ("3", 8), ("4", 6), ("m", 9)): "m-3m (Oh)",
    (("-4", 6), ("1", 1), ("2", 3), ("3", 8), ("m", 6)): "-43m (Td)",
    (("-1", 1), ("-3", 2), ("1", 1), ("2", 3), ("3", 2), ("m", 3)): "-3m (D3d)",
    (("-6", 2), ("1", 1), ("2", 3), ("3", 2), ("m", 4)): "-6m2 (D3h)",
    (("1", 1), ("3", 2), ("m", 3)): "3m (C3v)",
    (("-4", 2), ("1", 1), ("2", 3), ("m", 2)): "-42m (D2d)",
    (("-1", 1), ("1", 1), ("2", 3), ("m", 3)): "mmm (D2h)",
    (("-1", 1), ("-4", 2), ("1", 1), ("2", 5), ("4", 2), ("m", 5)): "4/mmm (D4h)",
    (("1", 1), ("2", 1), ("m", 2)): "mm2 (C2v)",
    (("1", 1), ("m", 1)): "m (Cs)",
    (("-1", 1), ("-3", 8), ("1", 1), ("2", 3), ("3", 8), ("m", 3)): "m-3 (Th)",
}


def pg_name(Rs, d):
    names = N2 if d == 2 else N3
    cnt = {}
    for R in Rs:
        n = names[eltype(R)]; cnt[n] = cnt.get(n, 0) + 1
    sig = tuple(sorted(cnt.items()))
    return PG.get(sig, "UNKNOWN " + str(sig)), sig


def site_group(net, ops, p):
    return [R for R, t in ops if mod_T(net, vsub(apply(R, t, p), p)) == (0,) * net.d]


def voronoi_like_faces(net, key):
    """At lam = 0 (equal weights): for each motif site, the numbers of like and unlike Voronoi neighbours (exact engine)."""
    spec = NETS[key]; out = {}
    D2 = spec["D2"]
    for i, (k, c) in enumerate(net.motif):
        E = Cell(net, i, (Fr(0),), D2)
        ok, rho = E.bound_ok([(Fr(0),)]); assert ok, "distance bound fails"
        F = E.faces()
        like = sum(1 for q in F if E.H[q]["kind"] == k); unlike = len(F) - like
        out.setdefault(k, set()).add((like, unlike))
    return {k: sorted(v) for k, v in out.items()}


def cscl_d(d):
    """Z^d (even, edge 2) + cube centres; the LP value of the nearest like pair and the midpoint value l^2/4 - delta^2."""
    # like pair a = 0, a' = 2 e1; unlike sites: all (odd)^d near the pair; f_a(x) = max_b |x-a|^2 - |x-b|^2 (affine in x)
    from scipy.optimize import linprog
    a = (0,) * d; a2 = (2,) + (0,) * (d - 1)
    U = [tuple(v) for v in product(*[(-3, -1, 1, 3, 5)] + [(-3, -1, 1, 3)] * (d - 1))]
    rows, rhs = [], []
    for p in (a, a2):
        for b in U:
            g = [2 * (b[s] - p[s]) for s in range(d)]
            rows.append(g + [-1]); rhs.append(sum(x * x for x in b) - sum(x * x for x in p))
    res = linprog(np.r_[np.zeros(d), 1.0], A_ub=np.array(rows, float), b_ub=np.array(rhs, float),
                  bounds=[(None, None)] * (d + 1), method="highs")
    # exact value at the midpoint m = e1: f_a(m) = max_b (1 - |m-b|^2) = 1 - (d - 1)
    m = (1,) + (0,) * (d - 1)
    fm = max(max(sum((x - y) ** 2 for x, y in zip(m, p)) - sum((x - y) ** 2 for x, y in zip(m, b)) for b in U) for p in (a, a2))
    # exact dual certificate: the LP value is >= fm because the midpoint is an inversion centre of the two-kind set and
    # max(f_a, f_a') is convex and symmetric under that inversion (Jensen); so LP value = fm exactly. Float LP as a cross-check.
    return Fr(fm), res.fun


if __name__ == "__main__":
    rows = []
    for key in KEYS:
        spec = NETS[key]; net = Net(spec["name"], spec["G"], spec["T"], spec["motif"], spec["w"])
        A, B = spec["A"], spec["B"]
        ops, sites = space_group(net)
        nT = len([1 for R, t in ops["sym"]])
        cen = any(eltype(R) == ((-1, -3) if net.d == 3 else (1, -2)) for R, t in ops["sym"])
        # inversion in 2D is the 2-fold rotation (det 1, trace -2)
        pA = next(c for k, c in net.motif if k == A); pB = next(c for k, c in net.motif if k == B)
        gA = site_group(net, ops["sym"], pA); gB = site_group(net, ops["sym"], pB)
        nA, sigA = pg_name(gA, net.d); nB, sigB = pg_name(gB, net.d)
        # all sites of one kind have the same site group (one orbit)? count orbits
        orbit_ok = True
        for K in (A, B):
            reps = [c for k, c in net.motif if k == K]
            orb = {mod_T(net, apply(R, t, reps[0])) for R, t in ops["sym"]}
            orbit_ok &= all(mod_T(net, c) in orb for c in reps)
        swap = len(ops["swap"]) > 0
        tA, tB = Fr(LB[key]["tau"][A]), Fr(LB[key]["tau"][B]); typ = LB[key]["type"]
        lo, hi = (Fr(x) for x in LB[key]["range"])
        vor = voronoi_like_faces(net, key)
        like0 = any(l > 0 for K in vor for (l, u) in vor[K])
        # distance rule
        mu = {}; midec = {}
        for K in (A, B):
            P = LB[key]["pairs"][K]
            mu[K] = min(Fr(p["midpoint_value"]) for p in P)
            midec[K] = any(p["midpoint_inversion"] and Fr(p["tau"]) == Fr(LB[key]["tau"][K]) for p in P)
        check(f"{key}: mu_K >= tau_K for both kinds (midpoint is feasible)", mu[A] >= tA and mu[B] >= tB,
              f"mu = ({mu[A]}, {mu[B]}), tau = ({tA}, {tB})")
        if midec[A]:
            check(f"{key}: distance rule decides kind {A}: mu = tau", mu[A] == tA)
        if midec[B]:
            check(f"{key}: distance rule decides kind {B}: mu = tau", mu[B] == tB)
        n_sites = {K: sum(1 for k, c in net.motif if k == K) for K in (A, B)}
        if swap:
            check(f"{key}: swap corollary part 1, tau_A = tau_B", tA == tB, f"{tA}, {tB}")
            pred = "switch" if not like0 else "gradual"
            check(f"{key}: swap corollary, type predicted from the equal-weight Voronoi cells = type of the walk", pred == typ,
                  f"like faces at lam=0: {vor}; predicted {pred}, census {typ}")
            check(f"{key}: swap: equal counts of the two kinds", n_sites[A] == n_sites[B])
        else:
            pred = "(no swap)"
        check(f"{key}: each kind is one orbit of the symmetry group", orbit_ok)
        check(f"{key}: site groups named", "UNKNOWN" not in nA + nB, f"{A}: {nA}; {B}: {nB}")
        rows.append(dict(key=key, label=LABEL[key], d=net.d, A=A, B=B, counts=n_sites, range=[str(lo), str(hi)],
                         sym_ops_mod_T=nT, swap_ops_mod_T=len(ops["swap"]), centrosymmetric=cen,
                         site_group={A: nA, B: nB}, site_order={A: len(gA), B: len(gB)},
                         tau={A: str(tA), B: str(tB)}, tau_sum=str(tA + tB), type=typ,
                         mu={A: str(mu[A]), B: str(mu[B])}, distance_rule_decides={A: midec[A], B: midec[B]},
                         voronoi_lam0={K: [list(x) for x in v] for K, v in vor.items()}, swap_prediction=pred))
        print(f"  {LABEL[key]}: |sym/T| = {nT}, |swap/T| = {len(ops['swap'])}, centro {cen}; site groups {A}: {nA} "
              f"({len(gA)}), {B}: {nB} ({len(gB)}); tau = ({tA}, {tB}), sum {tA + tB}, {typ}; mu = ({mu[A]}, {mu[B]}); "
              f"Voronoi lam=0 (like, unlike) {vor}", flush=True)

    # ---- controls that fail: the swap corollary's conclusion without its hypothesis
    by = {r["key"]: r for r in rows}
    hc = by["honeycomb"]
    check("control (expected to break the swap corollary's conclusion without a swap): honeycomb + centres has like "
          "neighbours at lam = 0 and yet a single switch (at -1/2); the hypothesis is needed",
          any(l > 0 for K in hc["voronoi_lam0"] for (l, u) in hc["voronoi_lam0"][K]) and hc["type"] == "switch" and hc["swap_ops_mod_T"] == 0)
    fl = by["delian"]
    check("control: fluorite has no swap and tau_A != tau_B (the swap identity tau_A = tau_B fails without a swap)",
          fl["swap_ops_mod_T"] == 0 and fl["tau"]["tet"] != fl["tau"]["oct"])
    # ---- site symmetry alone does not decide
    pairs = []
    for r1, r2 in combinations(rows, 2):
        if r1["d"] == r2["d"] and sorted(r1["site_group"].values()) == sorted(r2["site_group"].values()) \
                and (r1["type"] == "switch") != (r2["type"] == "switch"):
            pairs.append((r1["label"], r2["label"], sorted(r1["site_group"].values()), r1["type"], r2["type"]))
    for p in pairs: print("  same site groups, opposite type:", p)
    check("site symmetry alone does not decide the type: CsCl and rock salt both have site groups m-3m (Oh) for both kinds, "
          "both centrosymmetric with a kind swap, and CsCl is gradual (tau sum -2), rock salt a switch (0)",
          any({"CsCl", "rock salt"} == {p[0], p[1]} for p in pairs))
    # ---- the d-dimensional CsCl family
    for d in (1, 2, 3, 4):
        fm, lpv = cscl_d(d)
        check(f"CsCl in dimension {d}: like-pair value l^2/4 - delta^2 = 2 - d, float LP agrees", fm == 2 - d and abs(lpv - (2 - d)) < 1e-9,
              f"exact midpoint {fm}, float LP {lpv:.12f}")
    check("square + centres is the d = 2 member (tau = 0, switch) and CsCl the d = 3 member (tau = -1, gradual), in the units "
          "of the census (half edge 1)", by["square"]["tau"] == {"corner": "0", "centre": "0"} and by["bcc"]["tau"] == {"big": "-1", "small": "-1"})

    json.dump(rows, open(os.path.join(HERE, "..", "data", "obs3_symmetry.json"), "w"), indent=1)
    with open(os.path.join(HERE, "..", "data", "obs3_symmetry-checks.txt"), "w") as fh:
        for s_, n, det in checks: fh.write(f"{s_} {n} {det}\n")
    nf = sum(1 for c in checks if c[0] == "FAIL")
    print(f"{len(checks) - nf}/{len(checks)} PASS")
    print("FINAL ok" if checks and nf == 0 else f"FINAL FAIL: {nf} of {len(checks)} checks failed")
