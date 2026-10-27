"""The White Queen 600-cell (#63), step 1: the complete atlas of the 600-cell's slices, exact in Q(√5).

For each of the four main directions (vertex-, edge-, face-, cell-first) the slice is cut at every vertex height AND at
one height inside every open interval between consecutive vertex heights (the midpoint). Between two vertex heights no
vertex crosses the cutting space, so the slice keeps one combinatorial type over the whole interval: one cut per
interval gives every type. Each slice's hull is computed exactly (q5.exact_hull3), and its face sizes, vertex count and
symmetry-relevant data are recorded. Uses the modules of study 2026-10-27-4d-shadows (run from its scripts folder).
Run on dicto-big-brother:  cd ~/kres-tmp/4d/scripts && ~/geom/bin/python atlas600.py
"""
import json
import pickle

from polytopes import polytope
from q5 import Q5, dot, exact_hull3, q5str
from shadows import Space, describe


def run():
    P = polytope("600-cell")
    V = P["V"]; n = len(V[0])
    out, keep = [], []
    for lab, D in P["dirs"].items():
        d = D["d"]
        sp = Space(n, d, P["n0"])
        heights = [dot(v, d) for v in V]
        hs = sorted(set(heights), key=float)
        cuts = [(h, True) for h in hs] + [((a + b) / Q5(2), False) for a, b in zip(hs, hs[1:])]
        for hv, at_layer in sorted(cuts, key=lambda c: float(c[0])):
            if float(hv) < -1e-12:
                continue                                  # the far half mirrors the near half (centrally symmetric)
            pts = [sp.y(v) for v, x in zip(V, heights) if x == hv]
            for a, b in P["st"]["E"]:
                ha, hb = heights[a], heights[b]
                if ((ha - hv) * (hb - hv)).sign() < 0:
                    t = (hv - ha) / (hb - ha)
                    pts.append(sp.y(tuple(x + t * (y - x) for x, y in zip(V[a], V[b]))))
            base = {"direction": lab, "height": q5str(hv), "h": float(hv), "at_vertex_layer": at_layer,
                    "tip_height": q5str(hs[-1])}
            hh = exact_hull3(pts, sp.mf)
            if hh["dim"] < 3:
                out.append({**base, "dim": hh["dim"], "V": len(pts)})
                continue
            rec, ex = describe(hh, sp)
            item = {**base, **rec}
            out.append(item); keep.append({"item": item, "fV": hh["fV"].tolist(), "faces": hh["faces"]})
        print(lab, "vertex heights", len(hs), "slices kept", sum(1 for o in out if o["direction"] == lab), flush=True)
    return out, keep


if __name__ == "__main__":
    out, keep = run()
    json.dump(out, open("../data/atlas600.json", "w"), indent=1, ensure_ascii=False)
    pickle.dump(keep, open("../data/atlas600.pkl", "wb"))
    print("slices", len(out))
