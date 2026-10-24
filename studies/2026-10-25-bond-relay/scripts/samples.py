# Bond Relay, part B (exact, sample parameters): build the power cells from scratch, among fixed sites with the weights of part A,
# and check, exactly, at rational and irrational parameters:
#   B1 power cell = the app's piece (every app point inside the cell, every cell corner among the app points);
#   B2 face areas = the closed forms of part A (area^2 compared exactly);
#   B3 bond counts per piece; B4 volumes add up to the cell of the lattice; B5 faces pair up face to face (the neighbour's own cell
#   has the same polygon); B6 the corners: how many cells meet there and of which kinds (the dual weighted-Delaunay cells);
#   B7 the finite site list is enough (distance bound).
# Units: golden in half cube edges L/2 (big sites 2Z^3, small 2Z^3 + (1,1,1)); Delian in the units of krp-core tetPiece/octPiece
# (unit cubes, octet edge sqrt2; the app scales by 1/sqrt2). Output: ../data/raw/samples.json, ../data/checks/samples-checks.txt.
import json, sys, time
from fractions import Fraction as Fr
from itertools import product, permutations
from lib import QQ, Q5, Q2, Q6, C2, C6, power_cell, cell_faces, enough_sites, vadd, vsub, vmul, dot

checks, raw = [], {"golden": {}, "delian": {}}
def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail)); print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)

def key(p): return tuple(p)

def hull_volume(pts):
    """Exact volume of the convex hull of rational points (scipy picks the facets, Fractions do the sum)."""
    import numpy as np
    from scipy.spatial import ConvexHull
    h = ConvexHull(np.array([[float(z) for z in q] for q in pts])); o = pts[0]; v = Fr(0)
    for tri in h.simplices:
        a, b, cc = (vsub(pts[k], o) for k in tri)
        v += abs(a[0] * (b[1] * cc[2] - b[2] * cc[1]) - a[1] * (b[0] * cc[2] - b[2] * cc[0]) + a[2] * (b[0] * cc[1] - b[1] * cc[0])) / 6
    return v

def dual_check(label, cells, per_cell, target):
    """B8: the dual weighted-Delaunay cells (one per corner: the hull of the sites whose cells meet there). Each corner is seen by
    m cells, so sum over representative cells (x sites per lattice cell) of vol(dual)/m must be the lattice cell volume."""
    tot, shapes = Fr(0), {}
    for r, (cell, sub) in cells.items():
        for p, on in cell["corners"].items():
            S = [sub[cell["site"]][1]] + [sub[j][1] for j in on]
            ks = "+".join(sorted([sub[cell["site"]][0]] + [sub[j][0] for j in on]))
            v = hull_volume(S); tot += v / len(S) * per_cell[r]
            shapes[ks] = str(v)
    check(f"{label}: B8 dual weighted-Delaunay cells tile (sum = {target})", tot == target, json.dumps(shapes))
    return shapes

# ---------------- Golden ----------------
def golden_sites(D):
    S, R = [], int(D) + 2
    for m in product(range(-R, R + 1), repeat=3):
        for kind, off in (("big", (0, 0, 0)), ("small", (1, 1, 1))):
            c = tuple(Fr(2 * a + o) for a, o in zip(m, off))
            S.append((kind, c))
    return S

def golden_T(s, F):  # app goldenT in L/2 units: signed permutations of (1, s, 0) -> list of exact points (dedup)
    pts = set()
    for p in set(permutations((F(1), s, F(0)))):
        for sg in product((1, -1), repeat=3):
            pts.add(tuple(a * g for a, g in zip(p, sg)))
    return list(pts)

def golden_forms(s):
    one = s.F(1)
    return {("big", "big"): (s * s * 2) * (s * s * 2), ("small", "small"): ((one - s) * (one - s) * 2) * ((one - s) * (one - s) * 2),
            ("big", "small"): (one + s * 2 - s * s * 2) * (one + s * 2 - s * s * 2) * Fr(3, 4)}

def golden_vol(s, kind):
    one = s.F(1); u = s if kind == "big" else one - s
    return (one + u) * (one + u) * (one + u) * Fr(4, 3) - u * u * u * 4

GOLD = {  # x -> s = x/(1+x) (exact)
    "0": (QQ, lambda F: F(0)), "1/3": (QQ, lambda F: F(Fr(1, 4))), "1/2": (QQ, lambda F: F(Fr(1, 3))), "1": (QQ, lambda F: F(Fr(1, 2))),
    "2": (QQ, lambda F: F(Fr(2, 3))), "3": (QQ, lambda F: F(Fr(3, 4))),
    "tau": (Q5, lambda F: F(Fr(-1, 2), Fr(1, 2))),          # s = 1/tau = tau - 1 = (sqrt5 - 1)/2
    "1/tau": (Q5, lambda F: F(Fr(3, 2), Fr(-1, 2))),        # s = 1/tau^2 = 2 - tau
    "sqrt2": (Q2, lambda F: F(2, -1)),                      # s = sqrt2/(1 + sqrt2) = 2 - sqrt2
    "inf": (QQ, lambda F: F(1)),
}

def run_golden():
    D = 4
    S = golden_sites(D)
    for name, (F, sf) in GOLD.items():
        t0 = time.time(); s = sf(F)
        w = {"big": (s * 2 - 1) * Fr(1, 2), "small": -(s * 2 - 1) * Fr(1, 2)}  # w_big - w_small = 2s - 1 (units (L/2)^2)
        reps = {"big": (Fr(0),) * 3, "small": (Fr(1),) * 3}
        cells, faces, vols = {}, {}, {}
        for kind, c in reps.items():
            sub = [x for x in S if dot(vsub(x[1], c), vsub(x[1], c)) <= D * D]
            i = sub.index((kind, c))
            cell = power_cell(i, sub, w, F); cells[kind] = (cell, sub)
            ok, rho = enough_sites(cell, sub, w, D); check(f"golden x={name} {kind}: B7 site list enough", ok, f"rho={rho:.4f} D={D}")
            fc, vol = cell_faces(cell, F); faces[kind] = fc; vols[kind] = vol
            app = [vadd(c, p) for p in golden_T(s if kind == "big" else F(1) - s, F)]
            inside = all(all((b - dot(n, p)).sign() >= 0 for _, n, b in cell["planes"]) for p in app)
            cs = set(cell["corners"]); covered = cs <= set(app)
            check(f"golden x={name} {kind}: B1 power cell = app T", inside and covered, f"{len(cs)} corners")
        # B2/B3: bonds by type
        forms = golden_forms(s); rec = {}
        for kind in reps:
            cell, sub = cells[kind]; cnt = {}
            for j, (poly, a2, n) in faces[kind].items():
                kk = sub[j][0]; typ = tuple(sorted((kind, kk)))
                cnt[typ] = cnt.get(typ, 0) + 1
                f = forms[typ]
                if not (a2 == f):
                    check(f"golden x={name} {kind}->{kk}: B2 area^2", False, f"{a2} vs {f}")
                rec.setdefault(kind, {}).setdefault("-".join(typ), float(a2) ** 0.5)
            rec.setdefault(kind, {})["counts"] = {"-".join(k): v for k, v in sorted(cnt.items())}
        check(f"golden x={name}: B2 every face area = closed form", not any(c[0] == "FAIL" and "B2" in c[1] and f"x={name} " in c[1] for c in checks))
        # B4 volume: one big + one small fill the cube of side 2 (= L^3)
        check(f"golden x={name}: B4 vol(big) + vol(small) = 8 (L^3)", (vols["big"] + vols["small"]) == 8, f"{float(vols['big']):.6f} + {float(vols['small']):.6f}")
        check(f"golden x={name}: B4 volumes = (4/3)(1+u)^3 - 4u^3", vols["big"] == golden_vol(s, "big") and vols["small"] == golden_vol(s, "small"))
        # B5 face to face: neighbour's own cell (a translate of the representative of its kind) has the same polygon
        okp = True
        for kind in reps:
            cell, sub = cells[kind]; c = sub[cell["site"]][1]
            for j, (poly, a2, n) in faces[kind].items():
                kj, cj = sub[j]; shift = vsub(cj, reps[kj]); cellj, subj = cells[kj]
                back = vsub(c, shift)  # where site i sits relative to j's representative
                jj = [k for k, x in enumerate(subj) if x[1] == back]
                fj = faces[kj].get(jj[0]) if jj else None
                if fj is None or set(vadd(p, shift) for p in fj[0]) != set(poly):
                    okp = False
        check(f"golden x={name}: B5 every face shared face to face", okp)
        # B6 corners: kinds of the cells meeting at each corner
        deg = {}
        for kind in reps:
            cell, sub = cells[kind]
            for p, on in cell["corners"].items():
                ks = sorted([kind] + [sub[j][0] for j in on]); deg.setdefault(kind, {}).setdefault("+".join(ks), 0)
                deg[kind]["+".join(ks)] += 1
        rec["corners"] = deg; rec["dual cells (sites: volume)"] = dual_check(f"golden x={name}", cells, {"big": 1, "small": 1}, 8)
        rec["seconds"] = round(time.time() - t0, 2)
        raw["golden"][name] = rec
        print(name, json.dumps(rec), flush=True)

# ---------------- Delian ----------------
def odd(p): return (sum(int(x) for x in p) % 2) == 1

def delian_sites(D):
    S, R = [], int(D) + 2
    for m in product(range(-R, R + 2), repeat=3):
        S.append(("tet", tuple(Fr(a) + Fr(1, 2) for a in m)))
        if sum(m) % 2 == 1:
            S.append(("oct", tuple(Fr(a) for a in m)))
    return S

def tet_piece(k, t, F):  # krp-core delian-bond.js tetPiece, exact
    C = [vadd(k, d) for d in product((0, 1), repeat=3)]
    even = [p for p in C if not odd(p)]; octs = [p for p in C if odd(p)]; q = tuple(Fr(x) + Fr(1, 2) for x in k)
    third = Fr(1, 3)
    if (t - third).sign() <= 0:
        return [tuple(F(qi) + (F(vi) - qi) * (t * 3) for qi, vi in zip(q, v)) for v in even]
    a = (F(1) - t) * Fr(3, 2)
    out = [tuple(F(x) for x in v) for v in even]
    for o in octs:
        for v in even:
            if sum((x - y) ** 2 for x, y in zip(v, o)) == 1:
                out.append(tuple(F(oi) + a * (vi - oi) for oi, vi in zip(o, v)))
    return out

def oct_piece(c, t, F):  # krp-core octPiece, exact
    AX = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    tips = [tuple(F(ci + g * e) for ci, e in zip(c, ax)) for ax in AX for g in (1, -1)]
    if (t - Fr(1, 3)).sign() >= 0:
        a = (F(1) - t) * Fr(3, 2)
        return [tuple(a * (g * e) + ci for ci, e in zip(c, ax)) for ax in AX for g in (1, -1)]
    out = list(tips); s3 = t * 3
    for sg in product((-1, 1), repeat=3):
        q = tuple(Fr(ci) + Fr(g, 2) for ci, g in zip(c, sg))
        near = [vadd(c, (sg[0], 0, 0)), vadd(c, (0, sg[1], 0)), vadd(c, (0, 0, sg[2]))]
        for v in near:
            out.append(tuple(F(qi) + (F(vi) - qi) * s3 for qi, vi in zip(q, v)))
    return out

def delian_forms(t):
    one = t.F(1); a = (one - t) * Fr(3, 2)
    left = (t - Fr(1, 3)).sign() <= 0
    ot = (t * t * t * t) * Fr(243, 4) if left else (a * a * a * a) * Fr(3, 4)
    oo = (one - t * t * 9) * (one - t * t * 9) * Fr(1, 2)
    tt = (one - a * a) * (one - a * a)
    return {("oct", "tet"): ot, ("oct", "oct"): oo, ("tet", "tet"): tt}

def delian_vols(t):
    one = t.F(1); a = (one - t) * Fr(3, 2)
    if (t - Fr(1, 3)).sign() <= 0:
        return t * t * t * 9, one * 2 - t * t * t * 18
    return one - a * a * a * Fr(2, 3), a * a * a * Fr(4, 3)

DEL = {
    "0": (QQ, lambda F: F(0)), "1/6": (QQ, lambda F: F(Fr(1, 6))), "1/4": (QQ, lambda F: F(Fr(1, 4))), "1/3": (QQ, lambda F: F(Fr(1, 3))),
    "1/2": (QQ, lambda F: F(Fr(1, 2))), "2/3": (QQ, lambda F: F(Fr(2, 3))), "1": (QQ, lambda F: F(1)),
    "equilateralRd": (Q6, lambda F: F(Fr(-1, 5), Fr(2, 15))),                 # (2 sqrt6 - 3)/15
    "half": (C6, lambda F: F(1, Fr(-1, 3))),                                  # 1 - cbrt6/3
    "delian": (C2, lambda F: F(1, 0, Fr(-1, 3))),                             # 1 - (2/3) 2^(-1/3) = 1 - 2^(2/3)/3
    "equilateralCube": (Q2, lambda F: F(Fr(5, 3), Fr(-2, 3))),                # 5/3 - (2/3) sqrt2
}

def run_delian():
    D = 3
    S = delian_sites(D)
    reps = {"oct": ("oct", (Fr(1), Fr(0), Fr(0))), "tet0": ("tet", (Fr(1, 2),) * 3), "tet1": ("tet", (Fr(3, 2), Fr(1, 2), Fr(1, 2)))}
    def rep_of(kind, c):
        if kind == "oct": return "oct"
        return "tet1" if (sum(int(x - Fr(1, 2)) for x in c) % 2) else "tet0"
    for name, (F, tf) in DEL.items():
        t0 = time.time(); t = tf(F)
        w = {"tet": (t * 2 - 1) * Fr(3, 4), "oct": F(0)}  # w_tet - w_oct = (3/4)(2t - 1)
        cells, faces, vols = {}, {}, {}
        for r, (kind, c) in reps.items():
            sub = [x for x in S if dot(vsub(x[1], c), vsub(x[1], c)) <= D * D]
            i = sub.index((kind, c))
            cell = power_cell(i, sub, w, F); cells[r] = (cell, sub)
            ok, rho = enough_sites(cell, sub, w, D); check(f"delian t={name} {r}: B7 site list enough", ok, f"rho={rho:.4f} D={D}")
            fc, vol = cell_faces(cell, F); faces[r] = fc; vols[r] = vol
            if kind == "oct":
                app = oct_piece((1, 0, 0), t, F) if (t - 1).sign() < 0 else []
            else:
                k = (0, 0, 0) if r == "tet0" else (1, 0, 0)
                app = tet_piece(k, t, F) if t.sign() > 0 else []
            cs = set(cell["corners"])
            if not app:  # the app draws no piece here: the power cell must be a single point (zero volume)
                check(f"delian t={name} {r}: B1 app draws none, power cell is a point", len(cs) == 1 and vol.iszero(), f"{len(cs)} corner(s)")
                continue
            inside = all(all((b - dot(n, p)).sign() >= 0 for _, n, b in cell["planes"]) for p in app)
            check(f"delian t={name} {r}: B1 power cell = app piece", inside and cs <= set(app), f"{len(cs)} corners")
        forms = delian_forms(t); rec = {}; bad = 0
        for r in reps:
            cell, sub = cells[r]; cnt = {}; kind = reps[r][0]
            for j, (poly, a2, n) in faces[r].items():
                kk = sub[j][0]; typ = tuple(sorted((kind, kk)))
                cnt[typ] = cnt.get(typ, 0) + 1
                if not (a2 == forms[typ]):
                    bad += 1; print("area mismatch", name, r, kk, a2, forms[typ])
                rec.setdefault(r, {}).setdefault("-".join(typ), float(a2) ** 0.5)
            rec.setdefault(r, {})["counts"] = {"-".join(k): v for k, v in sorted(cnt.items())}
        check(f"delian t={name}: B2 every face area = closed form", bad == 0)
        vt, vo = delian_vols(t)
        tot = vols["oct"] * 4 + vols["tet0"] * 4 + vols["tet1"] * 4
        check(f"delian t={name}: B4 4 oct + 8 tet = 8 (cube of side 2)", tot == 8, f"{float(vols['tet0']):.6f}, {float(vols['oct']):.6f}")
        check(f"delian t={name}: B4 volumes = closed form", vols["tet0"] == vt and vols["tet1"] == vt and vols["oct"] == vo)
        okp = True
        for r in reps:
            cell, sub = cells[r]; c = sub[cell["site"]][1]
            for j, (poly, a2, n) in faces[r].items():
                kj, cj = sub[j]; rj = rep_of(kj, cj); shift = vsub(cj, reps[rj][1]); cellj, subj = cells[rj]
                back = vsub(c, shift); jj = [k for k, x in enumerate(subj) if x[1] == back]
                fj = faces[rj].get(jj[0]) if jj else None
                if fj is None or set(tuple(F(0) + x for x in vadd(p, shift)) for p in fj[0]) != set(poly):
                    okp = False
        check(f"delian t={name}: B5 every face shared face to face", okp)
        deg = {}
        for r in reps:
            cell, sub = cells[r]; kind = reps[r][0]
            for p, on in cell["corners"].items():
                ks = "+".join(sorted([kind] + [sub[j][0] for j in on])); deg.setdefault(r, {}).setdefault(ks, 0); deg[r][ks] += 1
        rec["corners"] = deg; rec["dual cells (sites: volume)"] = dual_check(f"delian t={name}", cells, {"oct": 4, "tet0": 4, "tet1": 4}, 8)
        rec["seconds"] = round(time.time() - t0, 2)
        raw["delian"][name] = rec
        print(name, json.dumps(rec), flush=True)

if __name__ == "__main__":
    T0 = time.time()
    run_golden(); run_delian()
    raw["seconds_total"] = round(time.time() - T0, 1)
    json.dump(raw, open("../data/raw/samples.json", "w"), indent=1)
    with open("../data/checks/samples-checks.txt", "w") as f:
        for c in checks: f.write("  ".join(c) + "\n")
        f.write(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL, {raw['seconds_total']} s\n")
    print(f"{sum(c[0] == 'PASS' for c in checks)} PASS, {sum(c[0] == 'FAIL' for c in checks)} FAIL, total {raw['seconds_total']} s")
