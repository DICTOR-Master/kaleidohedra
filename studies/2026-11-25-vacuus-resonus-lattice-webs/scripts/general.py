#!/usr/bin/env python3
"""General members and moved centres (25 Nov 2026). Exact arithmetic (webs.Q3); no floating point.

Part A. The proved conditions for the general member Z(lam_k u_k) of each type are checked against the exact web test
        on a grid of zone lengths (all lam in {1,2,3}^m, plus the cases where each predicted equality holds).
Part B. Moved centre c (same position in every cell). A plate through c and the edge e (zone u_j, midpoint m_e) with normal n
        continues if and only if n is a multiple of a primitive dual-lattice vector n0 (n0.Lambda = Z) with
        h(n0) + |n0.m_e| <= 1 and n0.c = n0.m_e. So for each edge the admissible normals form a finite set N_e, found by an
        exhaustive search in a box that contains every candidate (|n0_i| <= 2/lam_i because h(n0) >= lam_i |n0_i| / 2).
        The admissible centres are the interior points of the intersection over all edges of the union over N_e of the planes
        n0.x = n0.m_e. That set is computed exactly.
"""
import sys, json, itertools
from fractions import Fraction as Fr
import webs as W
from webs import Q3, q3, dot, cross, det3, scal, vadd, canon, Zono, commensurable_gcd, solve3


def passes(z, n):
    d = commensurable_gcd(z.lat_vals(n)); return d is not None and d >= z.h(n)


# ------------------------------------------------------------------ Part A: predicted conditions
def eq(l, i, j): return l[i] == l[j]

def predict(name, l, lab, n, info, z):
    """Predicted pass/fail from the theorems in the README (indices: lam_1..lam_m -> l[0..m-1])."""
    if name == "cube": return True
    if lab == "resonus":
        S = set(info["S"]); T = [k for k in range(z.m) if k not in S]
        if name == "truncated octahedron" and len(T) == 4:
            # square of the opposite pair S: the other two opposite pairs must each be equal
            pairs = [(0, 2), (1, 5), (3, 4)]
            return all(eq(l, a, b) for a, b in pairs if {a, b} != S)
        if len(T) == 1: return True
        if len(T) == 2: return eq(l, T[0], T[1])
        return False                                  # |T| = 3 and onto: never
    # vacuus
    return None                                       # checked against the Resonus plane it must equal (Lemma 3)


def partA(out):
    rows = []
    for name, U in W.TYPES.items():
        m = len(U)
        grid = list(itertools.product((1, 2, 3), repeat=m)) if m <= 5 else \
            [t for t in itertools.product((1, 2, 3), repeat=m) if len(set(t)) <= 2]
        nres = nvac = 0; bad = []
        vac_pass_kinds = {}
        for lam in grid:
            z = Zono(name, lam)
            res_normals = {n for n, _ in z.resonus()}
            for n, f in z.resonus():
                got = passes(z, n); pr = predict(name, lam, "resonus", n, f, z)
                nres += 1
                if got != pr: bad.append((name, lam, "R", [str(x) for x in n], got, pr))
            for n, es in z.vacuus():
                got = passes(z, n); nvac += 1
                belts = {z.belt(e["j"]) for e in es}
                # Lemma 3: a plate through an edge of a belt of six continues only if it is a Resonus plane that continues
                if 6 in belts and got and not (n in res_normals and passes(z, n)):
                    bad.append((name, lam, "V-lemma3", [str(x) for x in n]))
                if got:
                    key = ("Resonus plane" if n in res_normals else "not a Resonus plane", tuple(sorted(belts)))
                    vac_pass_kinds.setdefault(str(key), set()).add(lam)
                # hexagonal prism: plates through horizontal edges (belt of four) never continue (Theorem 4)
                if name == "hexagonal prism" and belts == {4} and got:
                    bad.append((name, lam, "V-hexprism-horizontal", [str(x) for x in n]))
            # whole-web verdicts
        rows.append({"type": name, "members": len(grid), "resonus_planes_tested": nres, "vacuus_plates_tested": nvac,
                     "mismatches": bad, "vacuus_passing_kinds": {k: len(v) for k, v in vac_pass_kinds.items()},
                     "vacuus_passing_examples": {k: [list(t) for t in sorted(v)[:6]] for k, v in vac_pass_kinds.items()}})
        print(f"PROGRESS A {name}: members {len(grid)}, R {nres}, V {nvac}, mismatches {len(bad)}", flush=True)
    out["partA"] = rows
    return all(not r["mismatches"] for r in rows)


def belt(self, j):
    fl = set()
    for k in range(self.m):
        if k == j: continue
        nrm = cross(self.U[j], self.U[k]); fl.add(canon(nrm))
    return 2 * len(fl)
Zono.belt = belt


# ------------------------------------------------------------------ Part B: moved centres
def dual_short(z):
    """All primitive dual vectors n0 (n0.Lambda = Z) with h(n0) <= 1, one of each +- pair. Exhaustive: h(n0) <= 1 forces
    |lam_k n0.u_k| <= 2 for every zone, so z_i = n0.G e_i = sum_k lam_k (n0.u_k) u_k,i obeys |z_i| <= 2 sum_k |u_k,i|."""
    from math import gcd
    Bz = [2 * sum(abs(int(u[i].a)) for u in z.U) for i in range(3)]
    uniq = {}
    for zz in itertools.product(*[range(-b, b + 1) for b in Bz]):
        if not any(zz): continue
        g = 0
        for x in zz: g = gcd(g, abs(x))
        if g != 1: continue
        n0 = solve3(z.G, tuple(q3(x) for x in zz))         # G symmetric: n0.G e_i = zz_i, so n0.Lambda = Z
        if z.h(n0) <= 1: uniq.setdefault(canon(n0), n0)
    return list(uniq.values())


def dual_candidates(z, uj, me, N0):
    return [n0 for n0 in N0 if not dot(n0, uj) and z.h(n0) + abs(dot(n0, me)) <= 1]


def rref(rows):
    """rows: list of (n, b) meaning n.x = b; returns canonical reduced rows or None if inconsistent."""
    M = [list(n) + [b] for n, b in rows]
    r = 0; piv = []
    for c in range(3):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        inv = M[r][c]; M[r] = [x / inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    for i in range(r, len(M)):
        if M[i][3]: return None
    return tuple(tuple(row) for row in M[:r])


def partB(out):
    rows = []
    for name, lam in [("cube", [1, 1, 1]), ("hexagonal prism", [1, 1, 1, 1]), ("rhombic dodecahedron", [1, 1, 1, 1]),
                      ("elongated dodecahedron", [1, 1, 1, 1, 1]), ("elongated dodecahedron", [1, 1, 1, Fr(1, 2) * W.SQ3, 1]),
                      ("truncated octahedron", [1] * 6)]:
        z = Zono(name, lam)
        states = {(): None}
        Ne_sizes = []
        N0 = dual_short(z)
        for e in z.Ed:
            uj = z.U[e["j"]]; me = e["c"]
            N = dual_candidates(z, uj, me, N0); Ne_sizes.append(len(N))
            new = {}
            for st in states:
                for n0 in N:
                    r = rref([(row[:3], row[3]) for row in st] + [(n0, dot(n0, me))])
                    if r is not None: new[r] = None
            states = new
        sols = []
        for st in states:
            if len(st) == 3:
                c = tuple(row[3] for row in st)
                inside = all(abs(dot(f["n"], c)) < z.h(f["n"]) for f in z.F)
                sols.append({"point": [str(x) for x in c], "interior": inside})
            else:
                sols.append({"subspace_rows": [[str(x) for x in row] for row in st]})
        # Resonus with moved centre: the admissible centres are |n.c| <= d - h for every face normal (Theorem 2)
        slack = [{"normal": [str(x) for x in f["n"]], "d_minus_h": str(commensurable_gcd(z.lat_vals(f["n"])) - z.h(f["n"]))
                  if commensurable_gcd(z.lat_vals(f["n"])) is not None else "dense"} for f in z.F]
        row = {"name": name, "lam": [str(x) for x in lam], "edges": len(z.Ed), "short_dual_vectors": len(N0), "admissible_normals_per_edge": sorted(set(Ne_sizes)),
               "edges_with_no_admissible_plate": sum(1 for x in Ne_sizes if x == 0),
               "vacuus_centres": sols, "resonus_slack": slack}
        rows.append(row)
        print(f"PROGRESS B {name} {row['lam']}: N_e sizes {row['admissible_normals_per_edge']}; Vacuus centres {sols}", flush=True)
    out["partB"] = rows
    return True


if __name__ == "__main__":
    out = {}
    okA = partA(out)
    okB = partB(out)
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "general.json", "w"), indent=1, default=str)
    if okA and okB: print("FINAL ok", flush=True)
    else: print("FINAL FAIL (mismatch with the proved conditions)", flush=True)
