#!/usr/bin/env python3
"""4D pilot (24 Nov 2026): the Vacuus of the six regular polytopes and of the omnitruncations of
A4, B4, H4 (uniform: the corner is equidistant from the walls of its chamber).

Vacuus (#110): each 2-face (ridge) spans with O a hyperplane through O, its plate.
Corners: exact orbit of a seed under the simple reflections. Cells and 2-faces: float
convex hull (combinatorics only). Plates: grouped by float normals, then checked exactly
(one exact normal per plate; every face on it verified exactly to lie in it). Mirrors:
plate normal parallel to a root (exact check).
A4 lives in the hyperplane sum = 0 of R^5; its normals are taken inside that hyperplane.
"""
import sys, json, time, itertools
import numpy as np
import sympy as sp
from scipy.spatial import ConvexHull
from vacuus_exact import Fld

def det(M):
    n = len(M)
    if n == 1: return M[0][0]
    if n == 2: return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    s = None
    for j in range(n):
        if not M[0][j]: continue
        t = M[0][j] * det([row[:j] + row[j+1:] for row in M[1:]])
        if j % 2: t = -t
        s = t if s is None else s + t
    return s if s is not None else M[0][0] * 0

def gcross(F, vecs):
    d = len(vecs[0]); out = []
    for k in range(d):
        M = [list(v[:k]) + list(v[k+1:]) for v in vecs]
        D = det(M)
        out.append(D if k % 2 == 0 else -D)
    return tuple(x if x is not None else F.zero for x in out)

def dotx(a, b):
    s = a[0]*b[0]
    for x, y in zip(a[1:], b[1:]): s = s + x*y
    return s

def key(F, v): return tuple(F.key(x) for x in v)
def flv(F, v): return np.array([float(F.val(x)) for x in v])

def orbit(F, seed, roots):
    rr = [dotx(r, r) for r in roots]
    seen = {key(F, seed): seed}; front = [seed]
    while front:
        nf = []
        for x in front:
            for r, n2 in zip(roots, rr):
                c = 2*dotx(x, r)/n2
                if not c: continue
                y = tuple(a - c*b for a, b in zip(x, r))
                k = key(F, y)
                if k not in seen: seen[k] = y; nf.append(y)
        front = nf
    return list(seen.values())

def two_faces(P, basis):
    Q = (P - P.mean(0)) @ basis.T if basis is not None else P
    h = ConvexHull(Q); cells = {}
    for s, e in zip(h.simplices, h.equations):
        cells.setdefault(tuple(np.round(e, 7)), set()).update(int(i) for i in s)
    faces = set()
    for cell in cells.values():
        cell = sorted(cell); C = Q[cell]; C0 = C - C.mean(0)
        U = np.linalg.svd(C0)[2][:3]; X = C0 @ U.T
        h3 = ConvexHull(X); g = {}
        for s, e in zip(h3.simplices, h3.equations):
            g.setdefault(tuple(np.round(e, 7)), set()).update(int(i) for i in s)
        for poly in g.values():
            faces.add(frozenset(cell[i] for i in poly))
    return len(cells), sorted(faces, key=lambda f: sorted(f))

def analyse4(name, F, V, roots_all, extra=None, basis=None):
    t0 = time.time()
    P = np.array([flv(F, v) for v in V]); n = len(V)
    ncell, faces = two_faces(P, basis)
    vk = {key(F, v): i for i, v in enumerate(V)}
    neg = [vk.get(key(F, tuple(-x for x in v))) for v in V]
    cs = all(x is not None for x in neg)
    fset = set(faces)
    groups = {}
    for f in faces:
        idx = sorted(f)[:3]
        vecs = [P[i] for i in idx] + ([extra[1]] if extra else [])
        M = np.array(vecs); nn = np.linalg.svd(M)[2][-1]
        if extra is None:
            pass
        nn = nn / np.linalg.norm(nn); j = int(np.argmax(np.abs(nn) > 1e-9)); nn = nn if nn[j] > 0 else -nn
        groups.setdefault(tuple(np.round(nn, 8)), []).append(f)
    Rf = np.array([flv(F, r) for r in roots_all]); Rf = Rf / np.linalg.norm(Rf, axis=1)[:, None]
    rows = {}
    for gk, fs in groups.items():
        f0 = sorted(fs[0])
        # exact normal from three corners of the first face that span a plane with O
        nrm = None
        for tri in itertools.combinations(f0, 3):
            vecs = [V[i] for i in tri] + ([extra[0]] if extra else [])
            nrm = gcross(F, vecs)
            if any(nrm): break
        for f in fs:
            for i in f:
                assert not dotx(nrm, V[i]), name + ": face not on plate (exact)"
        full = cs and all(frozenset(neg[i] for i in f) in set(fs) for f in fs)
        sheet = "full" if (full and len(fs) >= 2) else ("shared" if len(fs) >= 2 else "single")
        nf = np.array(gk); hit = np.where(np.abs(np.abs(Rf @ (nf / np.linalg.norm(nf))) - 1) < 1e-6)[0]
        mirror = False
        if len(hit):
            r = roots_all[int(hit[0])]
            mirror = all(not (nrm[a]*r[b] - nrm[b]*r[a]) for a in range(len(r)) for b in range(len(r)))
        sides = tuple(sorted(len(f) for f in fs))
        k = (len(fs), sides, sheet, mirror); rows[k] = rows.get(k, 0) + 1
    sheets = {k[2] for k in rows}
    kind = "heart" if sheets == {"full"} else ("non-heart" if sheets == {"single"} else "inherited heart")
    out = {"name": name, "corners": n, "cells": ncell, "two_faces": len(faces), "centrally_symmetric": cs,
           "plates": len(groups), "kind": kind, "plates_on_mirrors": sum(c for k, c in rows.items() if k[3]),
           "classes": [{"count": c, "faces_per_plate": k[0], "face_sides": "+".join(map(str, k[1])) if len(k[1]) <= 12 else f"{len(k[1])} faces", "sheet": k[2], "mirror": k[3]}
                       for k, c in sorted(rows.items(), key=lambda kv: -kv[1])],
           "secs": round(time.time() - t0, 1)}
    print(json.dumps(out), flush=True)
    return out

def weights(F, simple):
    """seed v with v.alpha_j = c_j: solve Gram system exactly (within span of the simple roots)."""
    G = [[dotx(a, b) for b in simple] for a in simple]
    def solve(c):
        # v = sum x_i alpha_i with G x = c  (Cramer)
        D = det(G); xs = []
        for i in range(len(simple)):
            Gi = [row[:i] + [c[r]] + row[i+1:] for r, row in enumerate(G)]
            xs.append(det(Gi) / D)
        return tuple(sum((x*a[t] for x, a in zip(xs, simple)), F.zero) for t in range(len(simple[0])))
    return solve

def main():
    res = []
    # ---- A4 in R^5 ----
    F = Fld(); o = F.one; z = F.zero
    e = lambda i: tuple(o if k == i else z for k in range(5))
    sA = [tuple(a - b for a, b in zip(e(i), e(i+1))) for i in range(4)]
    rootsA = [tuple(a - b for a, b in zip(e(i), e(j))) for i in range(5) for j in range(5) if i != j]
    ones = (o,)*5
    B = np.linalg.svd(np.vstack([np.ones(5)]))[2][1:]  # orthonormal basis of sum = 0
    solve = weights(F, sA)
    for nm, c in (("5-cell", (o, z, z, z)), ("A4 omnitruncation (4D permutohedron)", (o, o, o, o))):
        V = orbit(F, solve(c), sA)
        res.append(analyse4(nm, F, V, rootsA, extra=(ones, np.ones(5)), basis=B))
    # ---- B4 ----
    F = Fld(sp.sqrt(2)); o = F.one; z = F.zero; s2 = F.c(sp.sqrt(2))
    e = lambda i: tuple(o if k == i else z for k in range(4))
    sB = [tuple(a - b for a, b in zip(e(0), e(1))), tuple(a - b for a, b in zip(e(1), e(2))), tuple(a - b for a, b in zip(e(2), e(3))), e(3)]
    rootsB = []
    for i in range(4):
        for sgn in (o, -o): rootsB.append(tuple(sgn if k == i else z for k in range(4)))
        for j in range(i+1, 4):
            for a, b in itertools.product((o, -o), repeat=2):
                rootsB.append(tuple(a if k == i else (b if k == j else z) for k in range(4)))
    solve = weights(F, sB)
    rootsF4 = rootsB + [tuple(s) for s in itertools.product((o, -o), repeat=4)]  # the 24-cell's own group is F4
    for nm, seed, rr in (("tesseract", (o, o, o, o), rootsB), ("16-cell", (o, z, z, z), rootsB), ("24-cell", (o, o, z, z), rootsF4)):
        V = orbit(F, seed, sB)
        res.append(analyse4(nm, F, V, rr))
    V = orbit(F, solve((s2, s2, s2, o)), sB)
    res.append(analyse4("B4 omnitruncation", F, V, rootsB))
    json.dump(res, open("data/four-d.json", "w"), indent=1)
    # ---- H4 ----
    F = Fld(sp.sqrt(5)); o = F.one; z = F.zero; h = o/2
    phi = F.c((1 + sp.sqrt(5))/2); ip = phi - o
    R = []
    for i in range(4):
        for sgn in (o, -o): R.append(tuple(sgn if k == i else z for k in range(4)))
    for sg in itertools.product((h, -h), repeat=4): R.append(sg)
    base = (phi*h, h, ip*h, z)
    evens = [p for p in itertools.permutations(range(4)) if sum(1 for a in range(4) for b in range(a+1, 4) if p[a] > p[b]) % 2 == 0]
    for p in evens:
        v = tuple(base[p[k]] for k in range(4))
        for sg in itertools.product((1, -1), repeat=4):
            w = tuple(x if s == 1 else -x for x, s in zip(v, sg))
            if all(not (s == -1 and not x) for x, s in zip(v, sg)): R.append(w)
    R = list({key(F, r): r for r in R}.values()); assert len(R) == 120
    Rf = np.array([flv(F, r) for r in R]); c5 = (1 + 5**.5)/4
    a1 = 0; simple = None
    for a2 in range(120):
        if abs(Rf[a1] @ Rf[a2] + c5) > 1e-9: continue
        for a3 in range(120):
            if abs(Rf[a2] @ Rf[a3] + .5) > 1e-9 or abs(Rf[a1] @ Rf[a3]) > 1e-9: continue
            for a4 in range(120):
                if abs(Rf[a3] @ Rf[a4] + .5) > 1e-9 or abs(Rf[a1] @ Rf[a4]) > 1e-9 or abs(Rf[a2] @ Rf[a4]) > 1e-9: continue
                simple = [R[a1], R[a2], R[a3], R[a4]]; break
            if simple: break
        if simple: break
    G = [[dotx(a, b) for b in simple] for a in simple]
    assert G[0][1] == -phi/2 and G[1][2] == -h and G[2][3] == -h and all(G[i][i] == o for i in range(4))
    solve = weights(F, simple)
    for nm, c in (("120-cell", (o, z, z, z)), ("600-cell", (z, z, z, o)), ("H4 omnitruncation", (o, o, o, o))):
        V = orbit(F, solve(c), simple)
        print("PROGRESS", nm, len(V), "corners", flush=True)
        res.append(analyse4(nm, F, V, R))
        json.dump(res, open("data/four-d.json", "w"), indent=1)
    print("FINAL ok", len(res))

if __name__ == "__main__":
    main()
