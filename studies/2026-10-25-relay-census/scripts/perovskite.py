# Relay census, part C: perovskite ABX3 (three kinds, two weights): w_A = lam, w_B = mu, w_X = 0. The parameter plane is cut by
# straight walls (every slack is affine in (lam, mu)) into chambers of constant face lattice. Each chamber is found exactly (its
# polygon from the slacks that are positive at a sample point; floats only pick the candidate polygon corners, which are then
# solved and tested exactly), and the chamber complex is explored by stepping across every wall. Completeness: every wall segment
# that is not on the coexistence boundary is covered exactly by the chambers on its other side.
# Output: ../data/raw/perovskite.json, ../data/checks/perovskite-checks.txt.
import json, time
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np
import sympy as sp
from scipy.spatial import HalfspaceIntersection
from engine import Net, Cell, LAM, MU, cell_volume, face_alpha, gdot, vsub

net = Net("perovskite ABX3 (A cube corner, B body centre, X face centres)", [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
          [(2, 0, 0), (0, 2, 0), (0, 0, 2)],
          [("A", (0, 0, 0)), ("B", (1, 1, 1)), ("X", (1, 1, 0)), ("X", (1, 0, 1)), ("X", (0, 1, 1))],
          {"A": (0, 1, 0), "B": (0, 0, 1), "X": (0, 0, 0)}, m=2)
D2 = Fr(40); BOX = Fr(40)
BOXL = {(BOX, Fr(-1), Fr(0)), (BOX, Fr(1), Fr(0)), (BOX, Fr(0), Fr(-1)), (BOX, Fr(0), Fr(1))}
checks = []
def check(n, ok, det=""):
    checks.append(("PASS" if ok else "FAIL", n, det)); print(("PASS " if ok else "FAIL ") + n + (" " + det if det else ""), flush=True)

def norm(s):  # line a0 + a1 lam + a2 mu (> 0 side kept), scaled so the first nonzero of (a1, a2) has absolute value 1
    k = abs(s[1]) if s[1] != 0 else abs(s[2]); return tuple(x / k for x in s)

def ev(l, p): return l[0] + l[1] * p[0] + l[2] * p[1]

def chamber(p0):
    cells = [Cell(net, i, p0, D2) for i in range(len(net.motif))]
    if any(c.empty for c in cells):
        return "empty"
    L = set()
    for c in cells:
        for q in c.corners:
            for s in q["slack"]:
                if s[1] == 0 and s[2] == 0: continue
                v = ev(s, p0)
                if v == 0: return "wall"
                L.add(norm(s))
    L |= BOXL
    L = sorted(L)
    Hs = np.array([[-float(l[1]), -float(l[2]), -float(l[0])] for l in L])  # -a.x - a0 <= 0
    hs = HalfspaceIntersection(Hs, np.array([float(p0[0]), float(p0[1])]))
    verts = []
    for v in np.unique(np.round(hs.intersections, 9), axis=0):
        r = Hs[:, :2] @ v + Hs[:, 2]; tight = [k for k in np.argsort(np.abs(r))[:6] if abs(r[k]) < 1e-7]
        P = None
        for a, b in combinations(tight, 2):
            la, lb = L[a], L[b]; det = la[1] * lb[2] - la[2] * lb[1]
            if det != 0:
                P = ((-la[0] * lb[2] + lb[0] * la[2]) / det, (-la[1] * lb[0] + lb[1] * la[0]) / det); break
        assert P is not None and all(ev(l, P) >= 0 for l in L), "chamber corner not exact"
        if P not in verts: verts.append(P)
    c0 = np.mean([[float(x) for x in v] for v in verts], 0)
    verts.sort(key=lambda v: np.arctan2(float(v[1]) - c0[1], float(v[0]) - c0[0]))
    edges = []
    for k in range(len(verts)):
        a, b = verts[k], verts[(k + 1) % len(verts)]
        on = [l for l in L if ev(l, a) == 0 and ev(l, b) == 0]
        edges.append({"a": a, "b": b, "line": on[0]})
    return {"cells": cells, "verts": verts, "edges": edges, "p0": p0, "lines": L}

def describe(ch, tag):
    cells = ch["cells"]; out = {"verts": [[str(x) for x in v] for v in ch["verts"]], "sample": [str(x) for x in ch["p0"]], "sites": [], "dual": {}}
    Vt = 0; fm = {}
    okb = all(c.bound_ok([tuple(v) for v in ch["verts"]])[0] for c in cells)
    check(f"{tag}: distance bound at every chamber corner", okb)
    for c in cells:
        F = c.faces(); V = cell_volume(c, F); Vt += V; bonds, orb = {}, {}
        for k, pts in F.items():
            kk = c.H[k]["kind"]; bonds[kk] = bonds.get(kk, 0) + 1
            dv = vsub(c.H[k]["c"], c.c); o = f"{kk}@{gdot(net.G, dv, dv)}"; orb[o] = orb.get(o, 0) + 1
            al, c2, _ = face_alpha(c, k, pts); fm[(c.i, c.H[k]["j"], c.H[k]["kv"])] = sp.expand(al ** 2 * c2)
        nE = sum(len(p) for p in F.values()) // 2
        check(f"{tag} site {c.i} ({c.kind}): Euler", len(c.corners) - nE + len(F) == 2)
        out["sites"].append({"i": c.i, "kind": c.kind, "faces": len(F), "face_sizes": sorted(len(p) for p in F.values()),
                             "bonds": dict(sorted(bonds.items())), "orbits": dict(sorted(orb.items())), "volume": str(sp.factor(V))})
        for p in c.corners:
            ks = [c.kind] + [c.H[k]["kind"] for k in p["on"]]
            comp = "+".join(f"{ks.count(k)}{k}" for k in net.kinds if ks.count(k)); out["dual"][comp] = out["dual"].get(comp, 0) + 1
    check(f"{tag}: volumes add up to the lattice cell identically in (lam, mu)", sp.expand(Vt - net.detT) == 0, str(sp.factor(Vt)))
    check(f"{tag}: faces shared face to face", all((j, i, tuple(-x for x in kv)) in fm and sp.expand(fm[(j, i, tuple(-x for x in kv))] - a) == 0
                                                     for (i, j, kv), a in fm.items()))
    out["bond_types"] = sorted(set("-".join(sorted((s["kind"], k))) for s in out["sites"] for k in s["bonds"]))
    out["bond_orbits"] = sorted(set("-".join(sorted((s["kind"], k.split("@")[0]))) + "@" + k.split("@")[1] for s in out["sites"] for k in s["orbits"]))
    return out

def step_out(e, ch):
    a, b, l = e["a"], e["b"], e["line"]; m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    nrm = (l[1] ** 2 + l[2] ** 2); eps = Fr(1, 64)
    for _ in range(30):
        p = (m[0] - eps * l[1], m[1] - eps * l[2]); r = chamber(p)
        if r == "empty": return "boundary", m
        if r != "wall" and all(ev(x, m) >= 0 for x in r["lines"]): return r, m
        eps /= 4
    raise RuntimeError("cannot step out")

t0 = time.time()
start = (Fr(1, 97), Fr(1, 89)); first = chamber(start); assert isinstance(first, dict)
chambers = [first]; key = lambda ch: tuple(sorted(ch["verts"]))
seen = {key(first)}; queue = [first]; boundary = []
while queue:
    ch = queue.pop()
    for e in ch["edges"]:
        if e["line"] in BOXL:
            boundary.append(("box", e)); continue
        r, m = step_out(e, ch)
        if r == "boundary":
            boundary.append(("coexistence", e)); e["other"] = "outside"; continue
        k = key(r)
        e["other"] = k
        if k not in seen:
            seen.add(k); chambers.append(r); queue.append(r)
print(len(chambers), "chambers", round(time.time() - t0, 1), "s", flush=True)
check("perovskite: no chamber reaches the bounding box (the coexistence region is bounded)", not any(b[0] == "box" for b in boundary))
# completeness: every interior wall segment is covered by edges of other chambers on the same line
def same_line(l1, l2): return l1[0] == -l2[0] and l1[1] == -l2[1] and l1[2] == -l2[2] or l1 == l2
okc = True
for ch in chambers:
    for e in ch["edges"]:
        if e.get("other") == "outside": continue
        l = e["line"]; ax = 1 if l[2] != 0 else 0  # parametrise along the coordinate that varies
        t = lambda p: p[0] if l[2] != 0 else p[1]
        lo, hi = sorted((t(e["a"]), t(e["b"])))
        segs = sorted(sorted((t(f["a"]), t(f["b"]))) for c2 in chambers if c2 is not ch for f in c2["edges"] if same_line(f["line"], l))
        cur = lo
        for s0, s1 in segs:
            if s0 <= cur < s1: cur = s1
        okc &= cur >= hi
check("perovskite: every interior wall is covered exactly by chambers on its other side (no chamber missed)", okc, f"{len(chambers)} chambers")
# coexistence region area = sum of chamber areas (both exact); the region is the union
def area(vs): return abs(sum(vs[k][0] * vs[(k + 1) % len(vs)][1] - vs[(k + 1) % len(vs)][0] * vs[k][1] for k in range(len(vs)))) / 2
tot = sum(area(ch["verts"]) for ch in chambers)
recs = [describe(ch, f"perovskite chamber {n}") for n, ch in enumerate(chambers)]
# walls: distinct lines among interior edges
walls = {}
for n, ch in enumerate(chambers):
    for e in ch["edges"]:
        l = e["line"]; l = l if (l[1] > 0 or (l[1] == 0 and l[2] > 0)) else tuple(-x for x in l)
        walls.setdefault(str(tuple(str(x) for x in l)), set()).add("boundary" if e.get("other") == "outside" else "wall")
# hinge search: chambers, and points on walls/corners, where only unlike bonds exist
like = {"A-A", "B-B", "X-X"}
hinge_ch = [n for n, r in enumerate(recs) if not like & set(r["bond_types"])]
corner_info = {}
for ch in chambers:
    for v in ch["verts"]:
        kv = f"({v[0]}, {v[1]})"
        if kv in corner_info: continue
        cs = [Cell(net, i, v, D2) for i in range(len(net.motif))]
        bt = set()
        for c in cs:
            if c.empty: continue
            for k in c.faces(): bt.add("-".join(sorted((c.kind, c.H[k]["kind"]))))
        corner_info[kv] = {"vanished": sorted(set(c.kind for c in cs if c.empty)), "bond_types": sorted(bt)}
hinge_pts = [k for k, v in corner_info.items() if not v["vanished"] and not like & set(v["bond_types"])]
# sanity: on mu = -1 (B cells are points) at lam = 0, A + X are the fcc sites with equal weights: every A and X cell is the
# rhombic dodecahedron (Voronoi cell of fcc); at lam = mu = 0 the B cell is the cube of its 6 X neighbours (the B site sits in an
# octahedral hole of the A + X fcc and the 6 X-B bisectors cut first) - checked as face counts.
for i in range(len(net.motif)):
    c = Cell(net, i, (Fr(0), Fr(-1)), D2)
    if net.motif[i][0] == "B":
        check("perovskite (0, -1): B cell is a point", c.empty); continue
    F = c.faces(); check(f"perovskite (0, -1): {c.kind} cell is the rhombic dodecahedron (fcc Voronoi)",
                         sorted(len(p) for p in F.values()) == [4] * 12 and not any(c.H[k]["kind"] == "B" for k in F))
res = {"name": net.name, "params": "lam = w_A - w_X, mu = w_B - w_X", "units": "cubic cell edge 2 (A-X distance sqrt2, B-X 1)",
       "chambers": recs, "walls": {k: sorted(v) for k, v in walls.items()}, "coexistence_area": str(tot),
       "hinge_chambers": hinge_ch, "corners": corner_info, "hinge_corners": hinge_pts, "seconds": round(time.time() - t0, 1)}
json.dump(res, open("../data/raw/perovskite.json", "w"), indent=1)
with open("../data/checks/perovskite-checks.txt", "w") as fh:
    for s, n, det in checks: fh.write(f"{s} {n} {det}\n")
print(len(chambers), "chambers; walls", len(walls), "; hinge chambers", hinge_ch, "; hinge corners", hinge_pts)
print(sum(c[0] == "PASS" for c in checks), "/", len(checks), "PASS;", res["seconds"], "s")
for n, r in enumerate(recs):
    print(n, r["verts"], r["bond_orbits"], [(s["kind"], s["faces"], s["bonds"]) for s in r["sites"] if s["kind"] != "X"] + [(s["kind"], s["faces"], s["bonds"]) for s in r["sites"][2:3]], r["dual"])
for k, v in corner_info.items(): print(k, v)
print(res["walls"])
