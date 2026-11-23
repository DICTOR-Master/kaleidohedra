#!/usr/bin/env python3
"""Johnson solids: Vacuus PILOT in floating point (24 Nov 2026). NOT exact.

Same definition as vacuus_exact.py (edge plates through O; full / shared / single sheets;
heart / inherited heart / non-heart), with O = the corner centroid (#87 convention).
Coordinates: the app registry (johnson-float-source.json, 92 solids incl. J12, J13, J17,
J51, J84 stored as deltahedra D6, D10, D16, D14, D12). Every coincidence decision is a
float test; the reported gap (largest accepted |defect| vs smallest rejected) shows how
clear each decision is. To be made exact before any release.
"""
import json, sys, itertools
import numpy as np
from scipy.spatial import ConvexHull

TOL = 1e-7
src = json.load(open(sys.argv[1]))
alias = {"D6": "J12_TRIANGULAR_BIPYRAMID", "D10": "J13_PENTAGONAL_BIPYRAMID", "D16": "J17_GYROELONGATED_SQUARE_BIPYRAMID",
         "D14": "J51_TRIAUGMENTED_TRIANGULAR_PRISM", "D12": "J84_SNUB_DISPHENOID"}

def unit(v): return v / np.linalg.norm(v)
def canon(n):
    n = unit(n); i = np.argmax(np.abs(n) > 1e-9)
    return n if n[i] > 0 else -n

def run(name, P):
    c = P.mean(0); V = P - c; n = len(V)
    scale = np.abs(V).max(); V = V / scale
    hull = ConvexHull(V)
    groups = {}
    for simp, eq in zip(hull.simplices, hull.equations):
        groups.setdefault(tuple(np.round(eq, 6)), set()).update(int(i) for i in simp)
    faces = []
    for idx in groups.values():
        idx = sorted(idx); cf = V[idx].mean(0)
        nf = unit(np.cross(V[idx[1]] - V[idx[0]], V[idx[2]] - V[idx[0]]))
        u = unit(V[idx[0]] - cf); w = np.cross(nf, u)
        poly = [i for _, i in sorted(zip([np.arctan2((V[i]-cf) @ w, (V[i]-cf) @ u) for i in idx], idx))]
        faces.append(poly)
    edges = sorted({(min(p[j], p[(j+1) % len(p)]), max(p[j], p[(j+1) % len(p)])) for p in faces for j in range(len(p))})
    assert n - len(edges) + len(faces) == 2
    L = [np.linalg.norm(V[a]-V[b]) for a, b in edges]; assert max(L) / min(L) < 1 + 1e-6, name + " edges unequal"
    def find(p):
        d = np.linalg.norm(V - p, axis=1); i = int(d.argmin()); return i if d[i] < 1e-6 else None
    neg = [find(-v) for v in V]
    cs = all(x is not None for x in neg)
    # symmetry group (orthogonal maps permuting corners, fixing the centroid)
    r = np.linalg.norm(V, axis=1)
    base = [0]
    for i in range(n):
        if np.linalg.matrix_rank(V[base + [i]], tol=1e-6) == len(base) + 1: base.append(i)
        if len(base) == 3: break
    B = V[base]; Bi = np.linalg.inv(B.T)
    G = []
    c0 = [j for j in range(n) if abs(r[j] - r[base[0]]) < 1e-6]
    for j0 in c0:
        c1 = [j for j in range(n) if abs(r[j] - r[base[1]]) < 1e-6 and abs(V[j] @ V[j0] - B[1] @ B[0]) < 1e-6]
        for j1 in c1:
            c2 = [j for j in range(n) if abs(r[j] - r[base[2]]) < 1e-6 and abs(V[j] @ V[j0] - B[2] @ B[0]) < 1e-6 and abs(V[j] @ V[j1] - B[2] @ B[1]) < 1e-6]
            for j2 in c2:
                A = V[[j0, j1, j2]].T @ Bi
                if np.abs(A @ A.T - np.eye(3)).max() > 1e-6: continue
                if all(find(A @ v) is not None for v in V): G.append(A)
    Pfix = sum(G) / len(G)
    fixdim = int(np.linalg.matrix_rank(Pfix, tol=1e-6))
    mirrors = []
    for A in G:
        if np.linalg.det(A) < 0 and abs(np.trace(A) - 1) < 1e-6:  # reflection: eigen (1,1,-1)
            w_, U = np.linalg.eigh((A + A.T) / 2); m = canon(U[:, int(np.argmin(w_))]); mirrors.append(m)
    rot = sum(1 for A in G if np.linalg.det(A) > 0)
    # plates
    plates = []; defects_in = [0.0]; defects_out = [1.0]
    for a, b in edges:
        m = canon(np.cross(V[a], V[b]))
        for p in plates:
            d = min(np.linalg.norm(p["m"] - m), np.linalg.norm(p["m"] + m))
            if d < TOL: p["e"].append((a, b)); defects_in.append(d); break
            defects_out.append(d)
        else:
            plates.append({"m": m, "e": [(a, b)]})
    rows = {}
    for p in plates:
        es = set(p["e"])
        full = cs and all((min(neg[a], neg[b]), max(neg[a], neg[b])) in es for a, b in es)
        sheet = "full" if (full and len(es) >= 2) else ("shared" if len(es) >= 2 else "single")
        s = V @ p["m"]; on = int((np.abs(s) < 1e-7).sum())
        cr = sum(1 for a, b in edges if s[a] * s[b] < 0 and abs(s[a]) > 1e-7 and abs(s[b]) > 1e-7)
        mir = any(min(np.linalg.norm(p["m"] - q), np.linalg.norm(p["m"] + q)) < 1e-6 for q in mirrors)
        k = (len(es), sheet, on + cr, mir); rows[k] = rows.get(k, 0) + 1
    sheets = {k[1] for k in rows}
    kind = "heart" if sheets == {"full"} else ("non-heart" if sheets == {"single"} else "inherited heart")
    return {"name": name, "V": n, "E": len(edges), "F": len(faces), "group_order": len(G), "rotations": rot,
            "mirrors": len(mirrors), "centrally_symmetric": cs, "unique_symmetry_centre": fixdim == 0,
            "fixed_dim": fixdim, "plates": len(plates), "kind": kind,
            "plate_classes": [{"count": c, "edges_per_plate": k[0], "sheet": k[1], "slice_sides": k[2], "mirror": k[3]}
                              for k, c in sorted(rows.items(), key=lambda kv: -kv[1])],
            "max_merged_defect": max(defects_in), "min_separate_defect": min(defects_out)}

out = []
for k, v in src.items():
    if k in ("D4", "D8", "D20"): continue
    nm = alias.get(k, k)
    r = run(nm, np.array(v["vertices"], float))
    r["J"] = int(nm.split("_")[0][1:])
    out.append(r)
out.sort(key=lambda r: r["J"])
for r in out:
    print(json.dumps(r), flush=True)
json.dump(out, open("data/johnson-pilot.json", "w"), indent=1)
print("FINAL ok", len(out))
