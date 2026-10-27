"""The six turnings, exact (DICTO 2026-10-27: 'try for the exact figures'). Companion of shadow_turnings.py.

All in Q(√5), no square roots taken. For main views A, B (exact directions a, b) the turning is the arc of directions
u = α a + β b with α, β > 0. A cell with centre n is side-on at u ∝ (n·b) a − (n·a) b; it lies inside the arc when both
coefficients have the same strict sign. Two events coincide when their (α, β) are proportional (exact test). The angle of
an event from A is given exactly as cos² = (u·a)² / ((u·u)(a·a)) and, for reading, in degrees. In each gap a direction
strictly inside (the sum of the two boundary directions, each scaled to the same 'a'-coefficient-free form) is used to
count front cells exactly and to compute the shadow hull exactly (q5.exact_hull3, shadows.describe).
Run on dicto-big-brother:  cd ~/kres-tmp/4d/scripts && ~/geom/bin/python shadow_turnings_exact.py
"""
import itertools
import json
import math

from polytopes import polytope
from q5 import Q5, ZERO, dot, exact_hull3, q5str
from shadows import Space, describe

P = polytope("600-cell")
V, cells = P["V"], P["st"]["K4"]
centre = lambda c: tuple(sum((V[i][k] for i in c), ZERO) for k in range(4))
N = [centre(c) for c in cells]
dirs = {k: d["d"] for k, d in P["dirs"].items()}
lin = lambda al, a, be, b: tuple(al * x + be * y for x, y in zip(a, b))


def unit_free_sum(p, q, a):
    """a direction strictly between directions p and q (both inside the arc): p/|p| + q/|q| needs roots, so use
    p*(q.q) ... instead: any positive combination works; take p + t q with t = 1 (p, q given with positive coefficients)."""
    return tuple(x + y for x, y in zip(p, q))


def cos2(u, a):
    x = dot(u, a)
    return x * x / (dot(u, u) * dot(a, a))


def deg(c2, sign):
    v = math.degrees(math.acos(math.copysign(math.sqrt(float(c2)), sign)))
    return round(v, 6)


out = {}
for A, B in itertools.combinations(dirs, 2):
    a, b = dirs[A], dirs[B]
    ev = []                                        # (alpha, beta) with alpha, beta > 0
    flat_all_along = 0
    for n in N:
        al, be = dot(n, b), -dot(n, a)
        sa, sb = al.sign(), be.sign()
        if sa == 0 and sb == 0:
            flat_all_along += 1; continue
        if sa != 0 and sa == sb:
            if sa < 0:
                al, be = -al, -be
            ev.append((al, be))
    uniq = []
    for al, be in ev:                              # proportional pairs are the same event
        if not any(al * b2 == a2 * be for a2, b2 in uniq):
            uniq.append((al, be))
    # order along the arc from A: by beta/alpha increasing
    uniq.sort(key=lambda p: float(p[1] / p[0]))
    bounds = [(Q5(1), Q5(0))] + uniq + [(Q5(0), Q5(1))]
    # normalise A and B ends so that 'between' combinations are valid: use alpha a + beta b directly
    evs = []
    for al, be in uniq:
        u = lin(al, a, be, b)
        c2 = cos2(u, a)
        evs.append({"u_exact": [q5str(x) for x in u], "cos2_from_A": q5str(c2), "deg_from_A": deg(c2, float(dot(u, a)))})
    gaps = []
    for (a1, b1), (a2, b2) in zip(bounds, bounds[1:]):
        # strictly inside: (a1 + a2, b1 + b2) after scaling both pairs to alpha + beta = 1 (exact)
        s1, s2 = a1 + b1, a2 + b2
        al, be = a1 / s1 + a2 / s2, b1 / s1 + b2 / s2
        u = lin(al, a, be, b)
        front = sum(1 for n in N if dot(n, u).sign() > 0)
        side = sum(1 for n in N if dot(n, u).sign() == 0)
        sp = Space(4, u, None)
        h = exact_hull3([sp.y(v) for v in V], sp.mf)
        rec, _ = describe(h, sp)
        gaps.append({"front_cells": front, "side_on_cells": side, "hull_vertices": rec["V"], "hull_faces": rec["F"],
                     "face_sizes": rec["face_sizes"]})
    c2 = cos2(b, a)
    out[f"{A} -> {B}"] = {"turn_cos2": q5str(c2), "turn_deg": deg(c2, float(dot(a, b))), "swap_events": len(uniq),
                          "cells_side_on_all_along": flat_all_along, "events": evs, "gaps": gaps}
    print(f"{A} -> {B}: turn {deg(c2, float(dot(a, b)))}° (cos² {q5str(c2)}), swap events {len(uniq)}, gaps {len(gaps)}",
          flush=True)
    for e in evs:
        print(f"   event at {e['deg_from_A']}°  cos² = {e['cos2_from_A']}", flush=True)
    for g in gaps:
        print(f"   gap: front {g['front_cells']} side-on {g['side_on_cells']} hull {g['hull_vertices']} v, {g['hull_faces']} faces {g['face_sizes']}", flush=True)
json.dump(out, open("../data/shadow_turnings_exact.json", "w"), indent=1, ensure_ascii=False)
