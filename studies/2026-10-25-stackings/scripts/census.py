# Relay census, part A: walk the weight line of each two-kind network exactly (engine.py).
# For each network: w_A = lam, w_B = 0, so lam = w_A - w_B (units: the coordinates' squared length, stated per network).
# Output: ../data/raw/<net>.json and ../data/checks/<net>-checks.txt.   Usage: python census.py [net ...]
import json, sys, time
from fractions import Fraction as Fr
import sympy as sp
from engine import Net, Cell, LAM, face_alpha, cell_volume, rank, vsub, aff_eval, gdot, sym_point
from networks import NETS

def S(x): return str(x)


class Census:
    def __init__(self, key):
        self.key = key; spec = NETS[key]; self.spec = spec
        self.net = Net(spec["name"], spec["G"], spec["T"], spec["motif"], spec["w"])
        self.D2 = Fr(spec["D2"]); self.checks = []

    def check(self, name, ok, detail=""):
        self.checks.append(("PASS" if ok else "FAIL", name, detail))
        print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)

    def d2(self, c, k):
        dv = vsub(c.H[k]["c"], c.c); return gdot(self.net.G, dv, dv)

    # ---------------- one open interval
    def analyse(self, lam0):
        net = self.net
        cells = [Cell(net, i, (lam0,), self.D2) for i in range(len(net.motif))]
        if any(c.empty for c in cells):
            return {"empty": [c.kind for c in cells if c.empty]}
        lo, hi = None, None
        for c in cells:
            r = c.interval()
            if r[0] == "breakpoint":
                return {"breakpoint": lam0}
            if r[0] is not None and (lo is None or r[0] > lo): lo = r[0]
            if r[1] is not None and (hi is None or r[1] < hi): hi = r[1]
        return {"lo": lo, "hi": hi, "cells": cells, "lam0": lam0}

    def describe(self, iv):
        """Exact description of the face lattice on the open interval iv, with checks."""
        net, cells = self.net, iv["cells"]; lo, hi, l0 = iv["lo"], iv["hi"], iv["lam0"]
        tag = f"{self.key} ({S(lo)}, {S(hi)})"
        out = {"lo": S(lo), "hi": S(hi), "sample": S(l0), "sites": [], "dual": {}}
        Vtot = 0; facemap = {}
        okb = True
        for c in cells:
            ok, rho = c.bound_ok([(lo,), (hi,)]); okb &= ok
            F = c.faces(); V = cell_volume(c, F); Vtot += V
            bonds, sizes, areas, orbits, oareas = {}, [], {}, {}, {}
            for k, pts in F.items():
                kk = c.H[k]["kind"]; alpha, const2, opts = face_alpha(c, k, pts)
                bonds[kk] = bonds.get(kk, 0) + 1; sizes.append(len(pts))
                ob = f"{kk}@{S(self.d2(c, k))}"; orbits[ob] = orbits.get(ob, 0) + 1
                a2 = sp.factor(sp.expand(alpha ** 2 * const2)); oareas.setdefault(ob, set()).add(S(a2))
                areas.setdefault(kk, set()).add(S(a2))
                facemap[(c.i, c.H[k]["j"], c.H[k]["kv"])] = sp.expand(alpha ** 2 * const2)
            nV = len(c.corners); nF = len(F); nE = sum(sizes) // 2 if net.d == 3 else nV
            # corner degrees and edge lengths^2 (polynomials in lam): an edge joins two corners that share d - 1 faces
            deg = sorted(sum(1 for k in F if k in p["on"]) for p in c.corners)
            Gm = sp.Matrix(net.G); edges = set()
            for a in range(nV):
                for b in range(a + 1, nV):
                    sh = [k for k in F if k in c.corners[a]["on"] and k in c.corners[b]["on"]]
                    if len(sh) >= net.d - 1:
                        dv = sym_point(c.corners[a]["P"], net.d) - sym_point(c.corners[b]["P"], net.d)
                        edges.add(S(sp.factor(sp.expand((dv.T * Gm * dv)[0]))))
            if net.d == 3:
                self.check(f"{tag} site {c.i} ({c.kind}): Euler V - E + F = 2", nV - nE + nF == 2, f"{nV}-{nE}+{nF}")
            out["sites"].append({"i": c.i, "kind": c.kind, "bonds": dict(sorted(bonds.items())), "faces": nF, "corners": nV,
                                 "face_sizes": sorted(sizes), "area2": {k: sorted(v) for k, v in areas.items()},
                                 "volume": S(sp.factor(V)), "rho": round(rho, 4),
                                 "orbits": dict(sorted(orbits.items())), "orbit_area2": {k: sorted(v) for k, v in oareas.items()},
                                 "corner_degrees": deg, "edge_len2": sorted(edges)})
            for p in c.corners:
                ks = [c.kind] + [c.H[k]["kind"] for k in p["on"]]
                comp = "+".join(f"{ks.count(k)}{k}" for k in net.kinds if ks.count(k))
                out["dual"][comp] = out["dual"].get(comp, 0) + 1
        self.check(f"{tag}: distance bound (finite site list enough on the closed interval)", okb, f"D2={self.D2}")
        self.check(f"{tag}: cell volumes add up to the lattice cell identically in lam", sp.expand(Vtot - net.detT) == 0,
                   f"sum = {sp.factor(Vtot)}, cell = {net.detT}")
        # face to face: face (i -> j, kv) has the same measure as face (j -> i, -kv)
        okp = all(((j, i, tuple(-x for x in kv)) in facemap and sp.expand(facemap[(j, i, tuple(-x for x in kv))] - a) == 0)
                  for (i, j, kv), a in facemap.items())
        self.check(f"{tag}: every face shared face to face (same measure from both cells)", okp, f"{len(facemap)} faces")
        out["bond_types"] = sorted(set("-".join(sorted((s["kind"], k))) for s in out["sites"] for k in s["bonds"]))
        out["bond_orbits"] = sorted(set("-".join(sorted((s["kind"], k.split("@")[0]))) + "@" + k.split("@")[1] for s in out["sites"] for k in s["orbits"]))
        out["Vpoly"] = {s["kind"]: s["volume"] for s in out["sites"]}
        return out

    def stop(self, lam, iv):
        """The (closed) stop lam, at the end of the interval iv: the limit of iv's corners, plus a from-scratch cross-check."""
        net, d = self.net, self.net.d; res = {"lam": S(lam), "sites": [], "vanish": []}
        van = {c.i for c in iv["cells"] if cell_volume(c, c.faces()).subs(LAM, sp.Rational(lam)) == 0}
        for c in iv["cells"]:
            if c.i in van:
                res["vanish"].append(c.kind); res["sites"].append({"i": c.i, "kind": c.kind, "vanished": True}); continue
            pts = {}
            for p in c.corners:
                q = tuple(aff_eval(p["P"][r], (lam,)) for r in range(d))
                on = {k for k, s in enumerate(p["slack"]) if aff_eval(s, (lam,)) == 0}
                pts.setdefault(q, set()).update(on)
            bonds, sizes, orbits = {}, [], {}; nb = set(); ghost = set()
            for k in range(len(c.H)):
                f = [q for q, on in pts.items() if k in on]
                if len(f) >= d and rank([vsub(q, f[0]) for q in f[1:]]) == d - 1:
                    if c.H[k]["j"] in van:  # a plane through a vanished (point) cell that coincides with a live face: no bond
                        ghost.add((c.H[k]["j"], c.H[k]["kv"])); continue
                    kk = c.H[k]["kind"]; bonds[kk] = bonds.get(kk, 0) + 1; sizes.append(len(f)); nb.add((c.H[k]["j"], c.H[k]["kv"]))
                    ob = f"{kk}@{S(self.d2(c, k))}"; orbits[ob] = orbits.get(ob, 0) + 1
            # from scratch at lam (exact corners); must give the same corners and the same neighbours
            fresh = Cell(net, c.i, (lam,), self.D2)
            fc = {cc["p0"] for cc in fresh.corners}
            fnb = {(fresh.H[k]["j"], fresh.H[k]["kv"]) for k in fresh.faces()} - ghost
            self.check(f"{self.key} stop {S(lam)} site {c.i}: limit of the interval = power cell from scratch",
                       fc == set(pts) and fnb == nb, f"{len(pts)} corners, {len(nb)} faces")
            fk = [k for k in range(len(c.H)) if (c.H[k]["j"], c.H[k]["kv"]) in nb]
            deg = sorted(sum(1 for k in fk if k in on) for q, on in pts.items())
            res["sites"].append({"i": c.i, "kind": c.kind, "bonds": dict(sorted(bonds.items())), "faces": len(sizes), "corner_degrees": deg,
                                 "corners": len(pts), "face_sizes": sorted(sizes), "orbits": dict(sorted(orbits.items())),
                                 "ghost_planes": len(ghost)})
            # dual cells at the stop
            for q, on in pts.items():
                ks = [c.kind] + [c.H[k]["kind"] for k in on]
                comp = "+".join(f"{ks.count(k)}{k}" for k in net.kinds if ks.count(k))
                res.setdefault("dual", {}); res["dual"][comp] = res["dual"].get(comp, 0) + 1
        live = [s for s in res["sites"] if not s.get("vanished")]
        res["bond_types"] = sorted(set("-".join(sorted((s["kind"], k))) for s in live for k in s["bonds"]))
        res["bond_orbits"] = sorted(set("-".join(sorted((s["kind"], k.split("@")[0]))) + "@" + k.split("@")[1] for s in live for k in s["orbits"]))
        return res

    def step(self, b, direction, width):
        eps = width / 4 if width else Fr(1, 8)
        for _ in range(40):
            l = b + direction * eps; iv = self.analyse(l)
            if "breakpoint" in iv or "empty" in iv:
                eps /= 3; continue
            edge = iv["lo"] if direction > 0 else iv["hi"]
            if edge == b:
                return iv
            eps /= 4
        raise RuntimeError("could not step past " + str(b))

    def walk(self):
        t0 = time.time(); start = Fr(self.spec.get("start", 0))
        intervals, stops = [], []
        iv0 = self.analyse(start)
        if "breakpoint" in iv0:
            up, down = self.step(start, 1, None), self.step(start, -1, None)
            stops.append(self.stop(start, up)); intervals += [self.describe(up), self.describe(down)]
        else:
            up = down = iv0; intervals.append(self.describe(iv0))
        for direction, iv in ((1, up), (-1, down)):
            while True:
                b = iv["hi"] if direction > 0 else iv["lo"]
                assert b is not None, "unbounded interval"
                st = self.stop(b, iv); stops.append(st)
                if st["vanish"]:
                    break
                iv = self.step(b, direction, iv["hi"] - iv["lo"]); intervals.append(self.describe(iv))
                if len(intervals) > 60:
                    raise RuntimeError("too many intervals")
        intervals.sort(key=lambda r: Fr(r["lo"])); stops.sort(key=lambda r: Fr(r["lam"]))
        self.data = {"name": self.net.name, "key": self.key, "units": self.spec["units"], "kinds": self.net.kinds,
                     "lam": "w_" + self.spec["A"] + " - w_" + self.spec["B"], "intervals": intervals, "stops": stops,
                     "seconds": round(time.time() - t0, 1)}
        return self.data

    def at(self, lam):
        """The record (interval or stop) containing lam."""
        lam = Fr(lam)
        for r in self.data["stops"]:
            if Fr(r["lam"]) == lam: return r
        for r in self.data["intervals"]:
            if Fr(r["lo"]) < lam < Fr(r["hi"]): return r

    def expect(self, lam, kind, faces, sizes, bonds, label):
        r = self.at(lam); got = [s for s in r["sites"] if s["kind"] == kind]
        sig = lambda s: (s["faces"], s["face_sizes"] if self.net.d == 3 else s["corners"], s["bonds"])
        want = (faces, sorted(sizes) if self.net.d == 3 else sizes, bonds)
        self.check(f"{self.key}: at lam = {lam} every {kind} cell is the known {label}", bool(got) and all(sig(s) == want for s in got),
                   json.dumps(sig(got[0]) if got else None))

if __name__ == "__main__":
    keys = sys.argv[1:] or list(NETS)
    for key in keys:
        C = Census(key); d = C.walk()
        for e in NETS[key].get("expect", []):
            C.expect(*e)
        for f in NETS[key].get("extra_checks", []):
            f(C, d)
        d["checks"] = C.checks
        json.dump(d, open(f"../data/raw/{key}.json", "w"), indent=1, default=str)
        with open(f"../data/checks/{key}-checks.txt", "w") as fh:
            for s, n, det in C.checks:
                fh.write(f"{s} {n} {det}\n")
        npass = sum(1 for c in C.checks if c[0] == "PASS")
        print(f"== {key}: {len(d['intervals'])} intervals, {len(d['stops'])} stops, {npass}/{len(C.checks)} PASS, {d['seconds']} s", flush=True)
