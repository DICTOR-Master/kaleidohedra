"""Shadows resolved into halves, exact (DICTO 2026-10-27). For each of the four main views, the 600 cells split into
front (facing the viewer), back and side-on (flattened), decided exactly by the sign of (cell centre)·d in Q(√5).
Exact checks: front and back each tile the shadow once: the sum of the front cells' projected volumes equals the hull
volume, exactly (volumes in Q(√5), measured in the frame of shadows.Space, metric diag(sp.w)); the same for the back.
Kinds of front pieces: cells with equal sorted exact squared edge lengths in the shadow.
Run on dicto-big-brother:  cd ~/kres-tmp/4d/scripts && ~/geom/bin/python front_cells_exact.py
"""
import json

from polytopes import polytope
from q5 import Q5, ZERO, dot, exact_hull3, q5str
from shadows import Space

P = polytope("600-cell")
V, cells = P["V"], P["st"]["K4"]


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]))


out = {}
for lab, D in P["dirs"].items():
    d = D["d"]; sp = Space(4, d, None)
    Y = [sp.y(v) for v in V]
    # volume factor of the frame: coordinates y_i = p.b_i with |b_i|² = 1/w_i, so true volume = |det| * sqrt(w1 w2 w3)
    # compare volumes as det sums (common factor cancels)
    def vol(c):
        p = [Y[i] for i in c]
        a, b, e = [tuple(x - y for x, y in zip(p[k], p[0])) for k in (1, 2, 3)]
        x = det3(a, b, e)
        return x if x.sign() >= 0 else -x
    front = [c for c in cells if sum((dot(V[i], d) for i in c), ZERO).sign() > 0]
    back = [c for c in cells if sum((dot(V[i], d) for i in c), ZERO).sign() < 0]
    side = len(cells) - len(front) - len(back)
    h = exact_hull3(Y, sp.mf)
    # hull volume as a det sum: cone from the centroid of the hull vertices over each triangulated face
    hv = ZERO
    O = tuple(sum((Y[i][k] for i in range(120)), ZERO) / Q5(120) for k in range(3))
    for f in h["faces"]:
        f = list(f)
        for j in range(1, len(f) - 1):
            p = [h["V"][f[0]], h["V"][f[j]], h["V"][f[j + 1]]]
            a, b, e = [tuple(x - y for x, y in zip(q, O)) for q in p]
            x = det3(a, b, e); hv = hv + (x if x.sign() >= 0 else -x)
    fv = sum((vol(c) for c in front), ZERO); bv = sum((vol(c) for c in back), ZERO)
    def edges(c):
        L = []
        for i in range(4):
            for j in range(i + 1, 4):
                w = tuple(a - b for a, b in zip(Y[c[i]], Y[c[j]])); L.append(sp.mdot(w, w))
        return tuple(sorted(L, key=float))
    kinds = {}
    for c in front:
        kinds.setdefault(edges(c), 0); kinds[edges(c)] += 1
    out[lab] = {"front": len(front), "back": len(back), "side_on": side, "front_tiles_exactly": fv == hv,
                "back_tiles_exactly": bv == hv, "front_kinds": len(kinds), "kind_counts": sorted(kinds.values())}
    print(f"{lab}: front {len(front)}, back {len(back)}, side-on {side}; front volume = hull: {fv == hv}; "
          f"back volume = hull: {bv == hv}; kinds of front piece {len(kinds)} {sorted(kinds.values())}", flush=True)
json.dump(out, open("../data/front_cells_exact.json", "w"), indent=1)
