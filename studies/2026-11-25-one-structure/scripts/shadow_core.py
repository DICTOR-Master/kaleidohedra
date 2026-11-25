"""Exact shadow (parallel projection) of a skeleton: multiple points of the projected segments, decided exactly.

Input: exact 2D points (elements of one number field, nf.py of study 2026-11-25-plate-harmony) and segments as index pairs.
Method (certified):
- collinear segments are merged into maximal drawn pieces per line (exact line keys, exact interval ends);
- every pair of pieces on different lines is screened in double precision: intersection parameters t, u with tolerance 1e-7;
  pairs whose directions make an angle with |sin| < 1e-4 are decided exactly instead (no float decision for them);
- the float crossing points are binned on four offset grids of cell 1e-6; a point where three or more lines truly meet gives
  at least three pairs within 1e-10 of it, so it lands in one cell of at least one grid (the offsets make one grid safe in
  both coordinates);
- every cell holding at least three pairs is redone exactly: exact line intersections, grouped by exact key, and for every
  line through the point its exact status (interior of a drawn piece, or an end of one).
Float coordinates are the midpoints of 640-bit balls, so the screening error is below 1e-11 for the magnitudes here (|x| < 20),
far inside the tolerances. A pair or point that the screen keeps is always confirmed exactly; one it drops is at least 1e-7
outside a piece (parameter) and so cannot meet it.
"""
import numpy as np
import itertools, os, time
from yantra_inc import NEED_ANY, NEED_INT
from collections import defaultdict, Counter


def fl(x):
    return float(x.ball().mid())


def lt(a, af, b, bf):
    """exact a < b, decided in floats when far apart"""
    d = af - bf
    if d < -1e-9: return True
    if d > 1e-9: return False
    return (a - b).sign() < 0


def cmp(a, af, b, bf):
    d = af - bf
    if d < -1e-9: return -1
    if d > 1e-9: return 1
    return (a - b).sign()


class Shadow:
    def __init__(self, P, segs, centre_index=None):
        """P: list of (x, y) exact; segs: list of (i, j)"""
        self.P = P
        self.Pf = [(fl(x), fl(y)) for x, y in P]
        self.centre = centre_index
        self.vkeys = {}
        for i, (x, y) in enumerate(P):
            self.vkeys.setdefault((x.key(), y.key()), i)
        self.ckey = (P[centre_index][0].key(), P[centre_index][1].key()) if centre_index is not None else None
        lines = {}
        degenerate = 0
        for i, j in segs:
            (x0, y0), (x1, y1) = P[i], P[j]
            if x0 == x1 and y0 == y1:
                degenerate += 1; continue
            A = y1 - y0; B = x0 - x1
            if B:
                a = A / B; C = a * x0 + y0
                key = ("b", a.key(), C.key()); L = (a, x0.F.one, C); mode = 0      # a x + y = C, param x
                s0, s1 = (x0, self.Pf[i][0]), (x1, self.Pf[j][0])
            else:
                C = x0
                key = ("a", C.key()); L = (x0.F.one, x0.F.zero, C); mode = 1       # x = C, param y
                s0, s1 = (y0, self.Pf[i][1]), (y1, self.Pf[j][1])
            if not lt(s0[0], s0[1], s1[0], s1[1]): s0, s1 = s1, s0
            d = lines.setdefault(key, {"L": L, "mode": mode, "iv": []})
            d["iv"].append((s0, s1))
        self.degenerate = degenerate
        self.lines = []
        self.pieces = []           # (line id, (s0, s0f), (s1, s1f))
        for key, d in lines.items():
            iv = sorted(d["iv"], key=lambda t: t[0][1])
            merged = []
            for s0, s1 in iv:
                if merged and cmp(s0[0], s0[1], merged[-1][1][0], merged[-1][1][1]) <= 0:
                    if cmp(s1[0], s1[1], merged[-1][1][0], merged[-1][1][1]) > 0: merged[-1][1] = s1
                else:
                    merged.append([s0, s1])
            lid = len(self.lines)
            a, b, c = d["L"]
            self.lines.append({"key": key, "L": d["L"], "Lf": (fl(a), fl(b), fl(c)), "mode": d["mode"], "pieces": merged})
            for s0, s1 in merged: self.pieces.append((lid, s0, s1))

    # ---- geometry helpers
    def point_on(self, lid, s):
        a, b, c = self.lines[lid]["L"]
        if self.lines[lid]["mode"] == 0: return (s, c - a * s)
        return (c, s)

    def status(self, lid, X, Xf):
        """'int', 'end' or None for the exact point X on line lid"""
        ln = self.lines[lid]
        s, sf = (X[0], Xf[0]) if ln["mode"] == 0 else (X[1], Xf[1])
        for s0, s1 in ln["pieces"]:
            c0 = cmp(s, sf, s0[0], s0[1]); c1 = cmp(s, sf, s1[0], s1[1])
            if c0 == 0 or c1 == 0: return "end"
            if c0 > 0 and c1 < 0: return "int"
        return None

    def run(self):
        n = len(self.pieces)
        if n < 3:
            self.points = []; return self.points
        lid = np.array([p[0] for p in self.pieces])
        E0 = np.zeros((n, 2)); E1 = np.zeros((n, 2))
        for k, (l, s0, s1) in enumerate(self.pieces):
            a, b, c = self.lines[l]["Lf"]
            if self.lines[l]["mode"] == 0:
                E0[k] = (s0[1], c - a * s0[1]); E1[k] = (s1[1], c - a * s1[1])
            else:
                E0[k] = (c, s0[1]); E1[k] = (c, s1[1])
        D = E1 - E0
        Ln = np.hypot(D[:, 0], D[:, 1])
        I, J = np.triu_indices(n, 1)
        keep = lid[I] != lid[J]
        I, J = I[keep], J[keep]
        cr = D[I, 0] * D[J, 1] - D[I, 1] * D[J, 0]
        sinv = np.abs(cr) / (Ln[I] * Ln[J])
        near = sinv < 1e-4
        ok = ~near
        Ii, Jj, crr = I[ok], J[ok], cr[ok]
        W = E0[Jj] - E0[Ii]
        t = (W[:, 0] * D[Jj, 1] - W[:, 1] * D[Jj, 0]) / crr
        u = (W[:, 0] * D[Ii, 1] - W[:, 1] * D[Ii, 0]) / crr
        tol = 1e-7
        hit = (t > -tol) & (t < 1 + tol) & (u > -tol) & (u < 1 + tol)
        Ii, Jj, t = Ii[hit], Jj[hit], t[hit]
        X = E0[Ii] + t[:, None] * D[Ii]
        pairs_l = [(int(lid[a]), int(lid[b])) for a, b in zip(Ii, Jj)]
        # near-parallel pairs: exact
        extra = []
        for a, b in zip(I[near], J[near]):
            la, lb = int(lid[a]), int(lid[b])
            Xe = self.intersect(la, lb)
            if Xe is None: continue
            Xf = (fl(Xe[0]), fl(Xe[1]))
            if self.status(la, Xe, Xf) and self.status(lb, Xe, Xf):
                extra.append(((la, lb), Xf))
        if extra:
            X = np.vstack([X, np.array([e[1] for e in extra])])
            pairs_l += [e[0] for e in extra]
        self.n_pairs = len(pairs_l)
        cand = set()
        h = 1e-6
        for ox, oy in ((0, 0), (.5, 0), (0, .5), (.5, .5)):
            kx = np.floor(X[:, 0] / h + ox).astype(np.int64); ky = np.floor(X[:, 1] / h + oy).astype(np.int64)
            key = kx * 4000000007 + ky
            uq, inv, cnt = np.unique(key, return_inverse=True, return_counts=True)
            big = np.nonzero(cnt[inv] >= 3)[0]
            if len(big) == 0: continue
            groups = defaultdict(list)
            for k in big: groups[int(inv[k])].append(k)
            for g in groups.values(): cand.add(tuple(sorted(g)))
        pts = {}
        for g in cand:
            for k in g:
                la, lb = pairs_l[k]
                Xe = self.intersect(la, lb)
                if Xe is None: continue
                kk = (Xe[0].key(), Xe[1].key())
                d = pts.setdefault(kk, {"X": Xe, "lines": set()})
                d["lines"].update((la, lb))
        out = []
        for kk, d in pts.items():
            if len(d["lines"]) < 3: continue
            Xe = d["X"]; Xf = (fl(Xe[0]), fl(Xe[1]))
            st = {}
            for l in d["lines"]:
                s = self.status(l, Xe, Xf)
                if s: st[l] = s
            if len(st) < 3: continue
            vi = self.vkeys.get(kk)
            out.append({"X": Xe, "Xf": Xf, "status": st, "k_int": sum(1 for s in st.values() if s == "int"),
                        "k_end": sum(1 for s in st.values() if s == "end"), "vertex": vi, "centre": kk == self.ckey})
        self.points = out
        return out

    def intersect(self, la, lb):
        a1, b1, c1 = self.lines[la]["L"]; a2, b2, c2 = self.lines[lb]["L"]
        det = a1 * b2 - a2 * b1
        if not det: return None
        return ((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det)

    # ---- summaries
    def summary(self):
        pts = self.points
        strict = [p for p in pts if p["k_int"] >= 3 and not p["centre"]]
        mixed = [p for p in pts if p["k_int"] < 3 and p["k_int"] >= 1 and not p["centre"]]
        cen = [p for p in pts if p["centre"]]
        dirs = Counter()
        for ln in self.lines:
            dirs[ln["key"][:2] if ln["key"][0] == "b" else ("a",)] += 1
        maxpar = max(dirs.values()) if dirs else 0
        s = {"pieces": len(self.pieces), "lines": len(self.lines), "degenerate_segments": self.degenerate,
             "marmas": len(strict), "marma_hist": dict(sorted(Counter(p["k_int"] for p in strict).items())),
             "mixed_points": len(mixed), "centre_lines": (len(cen[0]["status"]) if cen else 0), "max_parallel": maxpar}
        s["yantra_test"] = self.yantra_test(strict, dirs)
        s["incidence"] = self.incidence() if s["yantra_test"]["pass"] else None
        return s

    def incidence(self):
        """the line-point incidence of the triple-or-more points, for the exhaustive search (yantra_sat.py)"""
        dk = {}
        dirs = [dk.setdefault(ln["key"][:2] if ln["key"][0] == "b" else ("a",), len(dk)) for ln in self.lines]
        return {"lines": len(self.lines), "dir": dirs, "points": [{str(l): st for l, st in p["status"].items()} for p in self.points]}

    def yantra_test(self, strict, dirs):
        """Necessary condition for the combinatorial Sri Yantra of yantra_search (so a failure here is a proof that the search
        has no solution): a pencil (9 or more parallel lines, or 9 or more drawn lines through one point) with 9 lines whose
        numbers of drawn triple-or-more points (the pencil point excluded) dominate the bases' needs 5, 5, 5, 4, 4, 3, 3, 1, 1,
        and whose numbers of such points inside a drawn piece dominate 5, 5, 3, 3, 3, 2, 2, 1, 1 (yantra_inc.py)."""
        on = Counter(); oi = Counter()
        for p in self.points:
            for l, st in p["status"].items():
                on[l] += 1; oi[l] += st == "int"
        pencils = []
        for dk, c in dirs.items():
            if c >= 9:
                ls = [i for i, ln in enumerate(self.lines) if (ln["key"][:2] if ln["key"][0] == "b" else ("a",)) == dk]
                pencils.append(("parallel", ls, None))
        for p in self.points:
            if len(p["status"]) >= 9: pencils.append(("point", list(p["status"]), p))
        npass = 0; best = None
        for kind, ls, p in pencils:
            cs = sorted((on[l] - (1 if p is not None else 0) for l in ls), reverse=True)
            ci = sorted((oi[l] - (1 if p is not None and p["status"].get(l) == "int" else 0) for l in ls), reverse=True)
            ok = len(cs) >= 9 and all(a >= b for a, b in zip(cs[:9], NEED_ANY)) and all(a >= b for a, b in zip(ci[:9], NEED_INT))
            npass += ok
            sc = (ok, sum(cs[:9]), len(cs))
            if best is None or sc > best[0]: best = (sc, kind, cs[:9])
        return {"pencils": len(pencils), "pass": npass, "best": None if best is None else {"kind": best[1], "top9": best[2], "lines": best[0][2]}}
