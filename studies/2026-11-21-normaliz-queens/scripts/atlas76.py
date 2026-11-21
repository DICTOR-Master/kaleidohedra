"""Target 3b (#76, gap L26): the exact atlas of the five stages between the 600-cell and the 120-cell in Q(sqrt5),
with Normaliz + e-antic. Each stage is the sweep member S(mu) = P ∩ mu P* (circumradius-1 600-cell P; stations.py
shows these equal #76's Table 1 builds corner for corner). Directions: #76/#62's vertex-, edge-, face-, cell-first
(centroids of a corner, an edge, a triangle, a cell of P). Slices at every corner height of S(mu) and halfway between,
from the centre to the tip (S(mu) is centrally symmetric), as in #76; the last slice is the tip element.
Each 3D slice: Normaliz from the 720 facet inequalities + x.d = h; corners, edges (Normaliz f-vector), faces by sides
(exact incidences); Euler check. Shadows: Normaliz hull of the projected corners. Patterns as #76: (V, E, F, faces by sides).
Usage: python3 atlas76.py [workers]   -> data/atlas76.json"""
import json, sys, time
from collections import Counter
import multiprocessing as mp   # spawn, not fork: forked workers deadlocked in Normaliz/OpenMP (run 2, 0% CPU)
from fractions import Fraction as Fr
from itertools import combinations
from qphi import QP, dot, ZERO, ONE, PHI, SQRT5
from polys import cell600
import nz

def q(a, b=0): return QP(Fr(a)) + QP(Fr(b)) * SQRT5
STAGES = [("600-cell", None), ("truncated 600-cell", q(Fr(9, 12), Fr(1, 12))), ("rectified 600-cell", (2 + PHI) / 4),
          ("bitruncated", q(Fr(11, 20), Fr(3, 20))), ("rectified 120-cell", PHI * PHI / 3),
          ("truncated 120-cell", q(Fr(15, 38), Fr(8, 38))), ("120-cell", "end")]
V = [tuple(x / 2 for x in v) for v in cell600()]
F = nz.facets(nz.hull(V))
N = [tuple(x / (-c) for x in n) for n, c in F]
inc = [[i for i, v in enumerate(V) if dot(n, v) == ONE] for n in N]
r2 = 1 / dot(N[0], N[0])
v0 = 0; cell = next(c for c in inc if v0 in c); oth = [i for i in cell if i != v0]
ELEM = {"v": [v0], "e": [v0, oth[0]], "f": [v0, oth[0], oth[1]], "c": list(cell)}
def cen(idx): return tuple(sum((V[i][k] for i in idx), ZERO) / len(idx) for k in range(4))
DIRS = {k: cen(x) for k, x in ELEM.items()}


def stage_ineq(mu):
    if mu is None: return [[-x for x in n] + [ONE] for n in N]                        # 600-cell
    if isinstance(mu, str): return [[-x for x in v] + [r2] for v in V]                         # 120-cell = r^2 P*
    return [[-x for x in n] + [ONE] for n in N] + [[-x for x in v] + [mu] for v in V]


def job(arg):
    si, dk = arg
    lab, mu = STAGES[si]; d = DIRS[dk]
    t0 = time.time()
    ineq = stage_ineq(mu)
    S = nz.poly(ineq); SV = nz.verts(S)
    H = [dot(p, d) for p in SV]
    hs = sorted(set(H))
    probes = [(h, "corner height") for h in hs if h.sign() <= 0] + \
             [((hs[i] + hs[i + 1]) / 2, "between") for i in range(len(hs) - 1) if ((hs[i] + hs[i + 1]) / 2).sign() <= 0]
    probes.sort(key=lambda t: t[0])
    rows = []
    for h, kind in probes:
        P = nz.poly(ineq, [list(d) + [-h]])
        Vs = nz.verts(P)
        fvec = P.FVector()
        if len(Vs) <= 2 or len(fvec) < 5:
            rows.append({"h": h.s5(), "kind": kind, "tip": True, "vertices": fvec[1] if len(fvec) > 2 else len(Vs), "normaliz_vertex_rows": len(Vs), "f_vector": fvec}); continue
            # (engine caveat: on 2-dimensional tips Normaliz 3.11.0 listed 11 vertex rows for a pentagon; the f-vector is used)
        Fs = nz.facets(P); ic = nz.incid(Fs, Vs)
        sizes = Counter(len(x) for x in ic)
        nV, nE, nF = fvec[1], fvec[2], fvec[3]          # PyNormaliz f-vector: [1, f0, f1, f2, 1] for a 3-polytope
        r = {"h": h.s5(), "kind": kind, "vertices": len(Vs), "edges": nE, "faces": len(Fs),
             "faces_by_sides": {str(k): v for k, v in sorted(sizes.items())},
             "euler": len(Vs) - nE + len(Fs), "fvector_consistent": (nV == len(Vs) and nF == len(Fs))}
        if r["euler"] != 2 or not r["fvector_consistent"]:
            # lower-dimensional tip (a polygon) is not an error
            r["note"] = "not a 3D slice" if len(fvec) < 5 else "CHECK"
        rows.append(r)
    # shadow: projection along d onto d-perp (exact; lies in a 3-space)
    dd = dot(d, d)
    proj = [tuple(x - (dot(p, d) / dd) * y for x, y in zip(p, d)) for p in SV]
    Sh = nz.hull(proj); shV = nz.verts(Sh); shF = nz.facets(Sh); shf = Sh.FVector()
    shadow = {"vertices": len(shV), "faces": len(shF), "edges": shf[2], "euler": len(shV) - shf[2] + len(shF),
              "faces_by_sides": {str(k): v for k, v in sorted(Counter(len(x) for x in nz.incid(shF, shV)).items())}}
    pats = {json.dumps([r.get("vertices"), r.get("edges"), r.get("faces"), r.get("faces_by_sides")]) for r in rows}
    return {"stage": lab, "dir": dk, "stage_vertices": len(SV), "slices": len(rows), "patterns": len(pats),
            "rows": rows, "shadow": shadow, "seconds": round(time.time() - t0, 1)}


if __name__ == "__main__":
    w = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    tasks = [(si, dk) for si in range(len(STAGES)) for dk in "vefc"]
    out = {}; t0 = time.time(); bad = 0
    with mp.get_context("spawn").Pool(w) as pool:
        for i, r in enumerate(pool.imap_unordered(job, tasks)):
            out.setdefault(r["stage"], {})[r["dir"]] = r
            bad += sum(1 for x in r["rows"] if x.get("note") == "CHECK") + (r["shadow"]["euler"] != 2)
            print("PROGRESS %.2f %s %s: %d slices, %d patterns, shadow %d/%d (%.0f s)" % ((i + 1) / len(tasks), r["stage"], r["dir"],
                  r["slices"], r["patterns"], r["shadow"]["vertices"], r["shadow"]["faces"], r["seconds"]), flush=True)
    json.dump(out, open("../data/atlas76.json", "w"), indent=1, ensure_ascii=False)
    print("TABLE stage: slices v.e.f.c (all) | patterns v.e.f.c | shadows corners/faces v.e.f.c")
    for lab, _ in STAGES:
        D = out[lab]
        s = [D[k]["slices"] for k in "vefc"]; p = [D[k]["patterns"] for k in "vefc"]
        sh = ["%d/%d" % (D[k]["shadow"]["vertices"], D[k]["shadow"]["faces"]) for k in "vefc"]
        print("TABLE", lab, ":", "·".join(map(str, s)), sum(s), "|", "·".join(map(str, p)), "|", " · ".join(sh))
    print("checks failing:", bad, "time", round(time.time() - t0), "s")
    print("FINAL ok" if bad == 0 else "FINAL FAIL", flush=True)
