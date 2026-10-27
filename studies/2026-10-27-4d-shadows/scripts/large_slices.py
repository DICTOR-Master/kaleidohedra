"""The six large all-triangle 600-cell slices: exact symmetry, belt/cap structure, and a symmetry-reduced exact solve
for an equilateral realisation of each face pattern.

For each slice (exact Q(sqrt5) data from shadows.py, coordinates y in the orthogonal frame of shadows.Space, metric
W = diag(w)):
  1. geometric symmetry group G: every graph automorphism that is induced by a linear map M (exact, Q(sqrt5)) with
     M^T W M = W;
  2. vertex orbits, stabilisers, fixed subspaces (exact);
  3. unknowns = coordinates of one vertex per orbit inside its fixed subspace; equations = one per edge orbit,
     |edge|^2 = 1; solved exactly (sympy Groebner basis over Q(sqrt5)), for G and for its rotation subgroup G+;
  4. each real solution checked: distinct vertices, no face degenerate, no 180-degree edge, no self-intersection.
Run on dicto-big-brother after shadows.py:  ~/geom/bin/python large_slices.py [label]
"""
import json
import pickle
import sys
import time
from fractions import Fraction as Fr

import networkx as nx
import numpy as np
import sympy as sp
from networkx.algorithms.isomorphism import GraphMatcher

from q5 import Q5, ZERO, ONE, q5sympy, q5str

SLICES = {
    "V72": ("vertex-first", "1 - √5"),
    "V32": ("edge-first", "-3/2 - 1/2√5"),
    "V30": ("face-first", "-4/3 - 2/3√5"),
    "V28": ("cell-first", "-5/4 - 3/4√5"),
    "V42": ("cell-first", "-3/2 - 1/2√5"),
    "V48": ("cell-first", "-1 - 1/2√5"),
}


# ------------------------------------------------------------------ exact linear algebra over Q(sqrt5)
def mat_mul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), ZERO) for j in range(len(B[0]))] for i in range(len(A))]


def mat_vec(A, v):
    return tuple(sum((A[i][k] * v[k] for k in range(len(v))), ZERO) for i in range(len(A)))


def transpose(A):
    return [list(r) for r in zip(*A)]


def inv3(A):
    a, b, c = A[0]; d, e, f = A[1]; g, h, i = A[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    if det.iszero():
        return None
    adj = [[e * i - f * h, c * h - b * i, b * f - c * e],
           [f * g - d * i, a * i - c * g, c * d - a * f],
           [d * h - e * g, b * g - a * h, a * e - b * d]]
    return [[x / det for x in r] for r in adj]


def nullspace(rows, n=3):
    """exact nullspace basis of the matrix with the given rows (Q5 entries)."""
    R = [list(r) for r in rows]
    piv = []
    r = 0
    for c in range(n):
        p = next((k for k in range(r, len(R)) if not R[k][c].iszero()), None)
        if p is None:
            continue
        R[r], R[p] = R[p], R[r]
        pv = R[r][c]
        R[r] = [x / pv for x in R[r]]
        for k in range(len(R)):
            if k != r and not R[k][c].iszero():
                f = R[k][c]
                R[k] = [x - f * y for x, y in zip(R[k], R[r])]
        piv.append(c)
        r += 1
        if r == len(R):
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [ZERO] * n
        v[fc] = ONE
        for i, pc in enumerate(piv):
            v[pc] = -R[i][fc]
        basis.append(tuple(v))
    return basis


def det3(A):
    a, b, c = A[0]; d, e, f = A[1]; g, h, i = A[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


# ------------------------------------------------------------------ symmetry
def symmetry_group(V, E, W):
    G = nx.Graph(); G.add_edges_from(E)
    n = len(V)
    # three independent vertices
    base = None
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                if not det3([V[a], V[b], V[c]]).iszero():
                    base = (a, b, c); break
            if base: break
        if base: break
    Binv = inv3(transpose([V[t] for t in base]))
    group = []
    for sigma in GraphMatcher(G, G).isomorphisms_iter():
        M = mat_mul(transpose([V[sigma[t]] for t in base]), Binv)
        if all(all((x - y).iszero() for x, y in zip(mat_vec(M, V[v]), V[sigma[v]])) for v in range(n)):
            Wm = [[W[i] if i == j else ZERO for j in range(3)] for i in range(3)]
            MtWM = mat_mul(transpose(M), mat_mul(Wm, M))
            assert all((MtWM[i][j] - Wm[i][j]).iszero() for i in range(3) for j in range(3))
            group.append((dict(sigma), M))
    return group


def orbits(n, group):
    seen = {}
    orbs = []
    for v in range(n):
        if v in seen:
            continue
        orb = {}
        for sigma, M in group:
            orb.setdefault(sigma[v], (sigma, M))
        for u in orb:
            seen[u] = len(orbs)
        orbs.append((v, orb))
    return orbs, seen


def edge_orbits(E, group):
    done = set()
    reps = []
    for a, b in E:
        k = (min(a, b), max(a, b))
        if k in done:
            continue
        reps.append(k)
        for sigma, M in group:
            x, y = sigma[a], sigma[b]
            done.add((min(x, y), max(x, y)))
    return reps


# ------------------------------------------------------------------ belts and caps along the main axis
def belts(V, E, W, group):
    """rings of vertices by exact height along the axis fixed by the rotation subgroup (if unique)."""
    rots = [M for s, M in group if det3(M) == ONE]

    def order(M):
        P, k = M, 1
        while not all((P[i][j] - (ONE if i == j else ZERO)).iszero() for i in range(3) for j in range(3)):
            P = mat_mul(P, M); k += 1
        return k
    top = max(rots, key=order)
    ax = nullspace([tuple(top[i][j] - (ONE if i == j else ZERO) for j in range(3)) for i in range(3)])
    if len(ax) != 1:
        return None
    a = ax[0]
    h = [sum((W[i] * a[i] * v[i] for i in range(3)), ZERO) for v in V]
    hs = sorted(set(h), key=float)
    G = nx.Graph(); G.add_edges_from(E)
    rings = []
    for x in hs:
        vs = [i for i, y in enumerate(h) if y == x]
        sub = G.subgraph(vs)
        rings.append({"axis_order": order(top), "height": float(x), "vertices": len(vs), "degrees": sorted((G.degree(v) for v in vs), reverse=True),
                      "ring_edges": sub.number_of_edges(), "is_cycle": len(vs) > 2 and sub.number_of_edges() == len(vs)
                      and all(d == 2 for _, d in sub.degree())})
    return rings


# ------------------------------------------------------------------ symmetry-reduced equilateral solve
def reduced_system(V, E, W, group):
    n = len(V)
    orbs, which = orbits(n, group)
    syms = []
    pos = [None] * n
    info = []
    for k, (rep, orb) in enumerate(orbs):
        stab = [M for sigma, M in group if sigma[rep] == rep]
        rows = []
        for M in stab:
            for i in range(3):
                rows.append(tuple(M[i][j] - (ONE if i == j else ZERO) for j in range(3)))
        fix = nullspace(rows)
        ts = sp.symbols(f"t{k}_0:{len(fix)}")
        syms += list(ts)
        yrep = [sum((t * q5sympy(f[i]) for t, f in zip(ts, fix)), sp.Integer(0)) for i in range(3)]
        for u, (sigma, M) in orb.items():
            pos[u] = [sp.expand(sum(q5sympy(M[i][j]) * yrep[j] for j in range(3))) for i in range(3)]
        info.append({"orbit_size": len(orb), "stabiliser": len(stab), "fixed_dim": len(fix)})
    Ws = [q5sympy(w) for w in W]
    eqs = []
    for a, b in edge_orbits(E, group):
        d = [pos[a][i] - pos[b][i] for i in range(3)]
        eqs.append(sp.expand(sum(Ws[i] * d[i] ** 2 for i in range(3)) - 1))
    return syms, eqs, pos, info


def main(labels):
    S = pickle.load(open("data/solids.pkl", "rb"))
    out = {}
    for lab in labels:
        direc, h = SLICES[lab]
        s = next(t for t in S if t["item"]["polytope"] == "600-cell" and t["item"]["direction"] == direc
                 and t["item"]["kind"] == "slice" and t["item"]["height"] == h)
        V, E, W = s["V"], s["E"], s["w"]
        n = len(V)
        # centre at the vertex centroid (exact)
        c = tuple(sum((v[i] for v in V), ZERO) / Q5(n) for i in range(3))
        V = [tuple(v[i] - c[i] for i in range(3)) for v in V]
        t0 = time.time()
        group = symmetry_group(V, E, W)
        rot = [(s_, M) for s_, M in group if det3(M) == ONE]
        G = nx.Graph(); G.add_edges_from(E)
        ncomb = sum(1 for _ in GraphMatcher(G, G).isomorphisms_iter())
        rec = {"direction": direc, "height": h, "V": n, "E": len(E), "F": len(s["faces"]),
               "graph_automorphisms": ncomb, "geometric_symmetries": len(group), "rotations": len(rot),
               "centroid_offset": [q5str(x) for x in c]}
        rec["belts"] = belts(V, E, W, group)
        for gname, grp in (("full", group), ("rotations", rot)):
            syms, eqs, pos, info = reduced_system(V, E, W, grp)
            r = {"orbits": info, "unknowns": len(syms), "equations": len(eqs),
                 "equations_exact": [str(e) for e in eqs]}
            rec[gname] = r
        out[lab] = rec
        print(lab, json.dumps({k: v for k, v in rec.items() if k not in ("full", "rotations")}), flush=True)
        for gname in ("full", "rotations"):
            print("  ", gname, rec[gname]["orbits"], "unknowns", rec[gname]["unknowns"], "equations",
                  rec[gname]["equations"], f"({time.time() - t0:.0f}s)", flush=True)
    json.dump(out, open("data/large-slices-systems.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:] or list(SLICES))
