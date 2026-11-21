"""Target 2 (#62, gap L37): every slice of the 600-cell (radius 2) along its vertex-, edge-, face- and cell-first
directions, exactly, with Normaliz + e-antic over Q(sqrt5).

Direction d = centroid of a vertex / edge / triangle / tetrahedral cell (the convention of #62, so heights h = x.d
compare directly with #62's table). The slice type can change only where the hyperplane x.d = h passes a vertex
(an incidence event), so slicing at every distinct vertex height AND at the midpoint of every interval between
consecutive heights gives every combinatorial type that occurs. Each slice = 600 facet inequalities + the equation
x.d = h, solved by Normaliz; vertices and faces are then re-checked here exactly (vertex count against an independent
edge-crossing construction, faces from exact incidences, Euler V - E + F = 2).
Output: data/slices600.json; all-triangle slices listed with h, h/(d.d) and their vertex / edge / triangle counts."""
import json, sys, time
from collections import Counter
from itertools import combinations
from qphi import QP, dot, ZERO
from polys import cell600
import nz

t0 = time.time()
V = cell600()
C = nz.hull(V); F = nz.facets(C); inc = nz.incid(F, V)
assert len(F) == 600 and all(len(x) == 4 for x in inc)
E = sorted({tuple(sorted(e)) for c in inc for e in combinations(c, 2)})
assert len(E) == 720
v0 = next(i for i, v in enumerate(V) if v == (QP(2), ZERO, ZERO, ZERO))
cell = next(c for c in inc if v0 in c)
others = [i for i in cell if i != v0]
elems = {"vertex-first": [v0], "edge-first": [v0, others[0]], "face-first": [v0, others[0], others[1]],
         "cell-first": list(cell)}


def centroid(idx):
    return tuple(sum((V[i][k] for i in idx), ZERO) / len(idx) for k in range(4))


ineq = [list(n) + [c] for n, c in F]
out = {"engine": "Normaliz 3.11.0 with e-antic (PyNormaliz 2.24), field Q(a), a^2 = a + 1", "directions": {}}
nall = 0; ok = True
dirs = list(elems.items())
for di, (lab, idx) in enumerate(dirs):
    d = centroid(idx); dd = dot(d, d)
    H = [dot(v, d) for v in V]
    hs = sorted(set(H))
    mids = [(hs[i] + hs[i + 1]) / 2 for i in range(len(hs) - 1)]
    probes = sorted([(h, "vertex height") for h in hs[1:-1]] + [(h, "interval") for h in mids], key=lambda t: t[0])
    rows = []
    for h, kind in probes:
        if h.sign() > 0: continue                      # centrally symmetric: h and -h give congruent slices
        P = nz.poly(ineq, [list(d) + [-h]])
        Vs = nz.verts(P); Fs = nz.facets(P)
        # exact recheck: vertices = original vertices at height h + crossings of edges strictly across h
        own = {V[i] for i in range(len(V)) if H[i] == h}
        for a, b in E:
            if ((H[a] - h) * (H[b] - h)).sign() < 0:
                t = (h - H[a]) / (H[b] - H[a])
                own.add(tuple(x + t * (y - x) for x, y in zip(V[a], V[b])))
        same = set(Vs) == own
        ic = nz.incid(Fs, Vs)
        sizes = Counter(len(x) for x in ic)
        # edges of the slice: pairs of vertices in >= 2 common faces
        nE = sum(1 for i, j in combinations(range(len(Vs)), 2) if sum(1 for f in ic if i in f and j in f) >= 2)
        euler = len(Vs) - nE + len(Fs)
        good = same and euler == 2
        ok &= good
        alltri = set(sizes) == {3}
        r = {"h": h.s5(), "h_over_dd": (h / dd).s5(), "h_float": round(float(h), 6), "kind": kind,
             "vertices": len(Vs), "edges": nE, "faces": len(Fs), "face_sizes": {str(k): v for k, v in sorted(sizes.items())},
             "all_triangles": alltri, "check_vertex_set": same, "euler": euler}
        rows.append(r)
        print(lab, kind, "h =", h.s5(), "V =", len(Vs), "E =", nE, "F =", len(Fs), dict(sizes),
              "ALL-TRIANGLE" if alltri else "", "" if good else "CHECK FAILED", flush=True)
    out["directions"][lab] = {"d": [x.s5() for x in d], "d.d": dd.s5(), "vertex_heights": [h.s5() for h in hs],
                              "slices": rows}
    print("PROGRESS %.2f %s done (%d probes, %.0f s)" % ((di + 1) / len(dirs), lab, len(rows), time.time() - t0), flush=True)

json.dump(out, open("../data/slices600.json", "w"), indent=1, ensure_ascii=False)
alltri = [(lab, r) for lab, D in out["directions"].items() for r in D["slices"] if r["all_triangles"]]
print("ALL-TRIANGLE SLICES (h <= 0 shown; -h congruent):")
for lab, r in alltri:
    print(" ", lab, r["kind"], "h =", r["h"], "h/(d.d) =", r["h_over_dd"], "V,E,F =", r["vertices"], r["edges"], r["faces"])
print("FINAL ok" if ok else "FINAL FAIL", flush=True)
