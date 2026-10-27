"""Parallel projections (shadows), projected vertex layers and hyperplane slices of the 5-, 16-, 24- and 600-cell
along the vertex-, edge-, face- and cell-first directions.  Exact in Q(sqrt5); floats only seed the hull.

Output: data/shadows.json (every solid: counts, face pattern, degree sequence, exact squared edge lengths, exact
dihedral cosines) and data/solids.pkl (exact data for the comparison step).
Run on dicto-big-brother:  ~/geom/bin/python shadows.py
"""
import json
import math
import pickle
import sys
from collections import Counter
from fractions import Fraction as Fr

import numpy as np

from q5 import Q5, ZERO, dot, sub, scal, exact_hull3, q5str
from polytopes import polytope


def frame(n, d, n0):
    """Orthogonal (unnormalised) exact basis of the complement of d (and n0) in R^n."""
    cons = [d] + ([n0] if n0 is not None else [])
    basis = []
    for k in range(n):
        v = tuple(Q5(1 if j == k else 0) for j in range(n))
        for c in cons + basis:
            v = sub(v, scal(dot(v, c) / dot(c, c), c))
        if not all(x.iszero() for x in v):
            basis.append(v)
        if len(basis) == 3:
            break
    return basis


class Space:
    """3-space orthogonal to d: exact coords y_i = p . b_i, metric diag(1/(b_i.b_i))."""

    def __init__(self, n, d, n0):
        self.B = frame(n, d, n0)
        self.w = [Q5(1) / dot(b, b) for b in self.B]
        self.mf = np.array([1.0 / math.sqrt(float(dot(b, b))) for b in self.B])

    def y(self, p):
        return tuple(dot(p, b) for b in self.B)

    def mdot(self, u, v):
        s = ZERO
        for a, b, w in zip(u, v, self.w):
            s = s + a * b * w
        return s


def describe(h, sp):
    """Combinatorial and metric record of an exact hull."""
    V, F, E = h["V"], h["faces"], h["E"]
    deg = Counter()
    for a, b in E:
        deg[a] += 1; deg[b] += 1
    L2 = {}
    for a, b in E:
        u = sub(V[a], V[b])
        L2[(a, b)] = sp.mdot(u, u)
    lvals = sorted(set(L2.values()), key=float)
    # dihedral angles
    efaces = {}
    for fi, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]):
            efaces.setdefault((min(a, b), max(a, b)), []).append(fi)
    dih = {}
    for (a, b), (f1, f2) in efaces.items():
        p, q = V[a], V[b]
        e = sub(q, p)
        ee = sp.mdot(e, e)
        perps = []
        for f in (f1, f2):
            r = next(V[t] for t in F[f] if t not in (a, b))
            u = sub(r, p)
            u = sub(u, scal(sp.mdot(u, e) / ee, e))
            perps.append(u)
        u, w = perps
        uw = sp.mdot(u, w)
        c2 = uw * uw / (sp.mdot(u, u) * sp.mdot(w, w))
        sg = uw.sign()
        ang = math.degrees(math.acos(max(-1.0, min(1.0, sg * math.sqrt(float(c2))))))
        dih[(a, b)] = (sg, c2, ang)
    dvals = sorted({(sg, c2) for sg, c2, _ in dih.values()}, key=lambda t: t[0] * math.sqrt(float(t[1])))
    fsz = Counter(len(f) for f in F)
    rec = {
        "V": len(V), "E": len(E), "F": len(F),
        "face_sizes": {str(k): v for k, v in sorted(fsz.items())},
        "all_triangles": set(fsz) == {3},
        "degrees": "".join(str(x) for x in sorted(deg.values(), reverse=True)) if max(deg.values()) < 10
        else sorted(deg.values(), reverse=True),
        "edge_len2_exact": [q5str(x) for x in lvals],
        "edge_len": [round(math.sqrt(float(x)), 6) for x in lvals],
        "edge_len_count": [sum(1 for v in L2.values() if v == x) for x in lvals],
        "edge_ratio2_exact": q5str(lvals[-1] / lvals[0]),
        "edge_ratio": round(math.sqrt(float(lvals[-1] / lvals[0])), 6),
        "dihedral_cos2_exact": [("+" if s > 0 else "-" if s < 0 else "0") + "(" + q5str(c) + ")" for s, c in dvals],
        "dihedral_deg": [round(math.degrees(math.acos(s * math.sqrt(float(c)))), 4) for s, c in dvals],
        "dihedral_count": [sum(1 for v in dih.values() if (v[0], v[1]) == t) for t in dvals],
    }
    return rec, {"L2": L2, "dih": dih, "deg": dict(deg)}


def run():
    out = []
    solids = []
    for name in ("5-cell", "16-cell", "24-cell", "600-cell"):
        P = polytope(name)
        V = P["V"]; n = len(V[0])
        print(name, P["counts"], flush=True)
        seen_axes = []
        for lab, D in P["dirs"].items():
            d = D["d"]
            # same axis as an earlier direction? (parallel d gives the same shadow; slices then also coincide up to
            # the sign of the height)
            same = None
            for lab2, d2 in seen_axes:
                # parallel iff |d.d2|^2 == |d|^2 |d2|^2
                x = dot(d, d2)
                if x * x == dot(d, d) * dot(d2, d2):
                    same = lab2
            seen_axes.append((lab, d))
            if same:
                out.append({"polytope": name, "direction": lab, "same_axis_as": same})
                continue
            sp = Space(n, d, P["n0"])
            heights = [dot(v, d) for v in V]
            hs = sorted(set(heights), key=float)
            # 1. shadow
            pts = [sp.y(v) for v in V]
            h = exact_hull3(pts, sp.mf)
            rec, ex = describe(h, sp)
            item = {"polytope": name, "direction": lab, "kind": "shadow", "height": None, **rec}
            out.append(item); solids.append((item, h, ex, sp))
            # 2. projected layers
            for k, hv in enumerate(hs):
                lp = [sp.y(v) for v, x in zip(V, heights) if x == hv]
                hh = exact_hull3(lp, sp.mf)
                base = {"polytope": name, "direction": lab, "kind": "layer", "layer": k, "height": q5str(hv),
                        "layer_vertices": len(lp)}
                if hh["dim"] < 3:
                    out.append({**base, "dim": hh["dim"]})
                    continue
                rec, ex = describe(hh, sp)
                item = {**base, **rec}
                out.append(item); solids.append((item, hh, ex, sp))
            # 3. slices: centre and every vertex height, plus mid-heights between layers
            centre_h = dot(P["centre"], d)
            slice_hs = sorted(set(hs) | {centre_h}, key=float)
            for hv in slice_hs:
                sp_pts = [sp.y(v) for v, x in zip(V, heights) if x == hv]
                for a, b in P["st"]["E"]:
                    ha, hb = heights[a], heights[b]
                    if ((ha - hv) * (hb - hv)).sign() < 0:
                        t = (hv - ha) / (hb - ha)
                        p = tuple(x + t * (y - x) for x, y in zip(V[a], V[b]))
                        sp_pts.append(sp.y(p))
                base = {"polytope": name, "direction": lab, "kind": "slice", "height": q5str(hv),
                        "central": hv == centre_h, "at_vertex_layer": hv in hs}
                hh = exact_hull3(sp_pts, sp.mf)
                if hh["dim"] < 3:
                    out.append({**base, "dim": hh["dim"]})
                    continue
                rec, ex = describe(hh, sp)
                item = {**base, **rec}
                out.append(item); solids.append((item, hh, ex, sp))
            print(" ", lab, "layers", len(hs), flush=True)
    return out, solids


if __name__ == "__main__":
    out, solids = run()
    json.dump(out, open("data/shadows.json", "w"), indent=1)
    keep = []
    for item, h, ex, sp in solids:
        keep.append({"item": item, "V": h["V"], "faces": h["faces"], "E": h["E"], "fV": h["fV"].tolist(),
                     "w": sp.w, "L2": ex["L2"], "dih": ex["dih"], "deg": ex["deg"]})
    pickle.dump(keep, open("data/solids.pkl", "wb"))
    print("records", len(out), "solids", len(solids))
