"""B2: internal crossings of a frame, exact. For each Platonic and Archimedean polyhedron P (centre O, data/skeletons.json):
segments
- S  struts: O to every corner;
- FD face diagonals: two corners of one face that are not an edge;
- SD space diagonals: two corners on no common face;
- PL plate lines: every line through O where two Vacuus plates (planes through O and an edge) meet, clipped to P.
Collinear segments are merged into maximal pieces per line (exact keys). Every point where two or more pieces on different lines
meet is found and decided exactly: screening in double precision (distance between lines < 1e-8 and parameters inside
[-1e-7, 1 + 1e-7]; pairs with |sin| < 1e-4 decided exactly), then exact intersection in the field, grouped by exact key.
Each point: number of lines, which families, whether it is O, inside P, or on the boundary. Corners of P are left out (every
segment at a corner ends there). Writes data/internal.json."""
import os, sys, json, time, itertools
from collections import Counter, defaultdict
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "../../2026-11-25-plate-harmony/scripts")))
from nf import NF
from shadow_core import fl, cmp
import multiprocessing as mpr

CAP = int(os.environ.get("PAIRCAP", "4000000"))


def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def sub(u, v): return (u[0] - v[0], u[1] - v[1], u[2] - v[2])
def add(u, v): return (u[0] + v[0], u[1] + v[1], u[2] + v[2])
def sc(k, u): return (k * u[0], k * u[1], k * u[2])
def key(v): return tuple(x.key() for x in v)
def iszero(v): return all(not x for x in v)


def normdir(u):
    f = next(x for x in u if x)
    iv = f.inv()
    return tuple(x * iv for x in u)


def frame(row):
    F = NF(row["field"]["g"], row["field"]["eta"])
    V = [tuple(F.from_coeffs(c) for c in v) for v in row["V"]]
    O = (F.zero,) * 3
    E = {tuple(sorted(e)) for e in row["E"]}
    faces = row["faces"]
    planes = []
    for f in faces:
        n = cross(sub(V[f[1]], V[f[0]]), sub(V[f[2]], V[f[0]]))
        h = dot(n, V[f[0]])
        if h.sign() < 0: n = sc(-F.one, n); h = -h
        planes.append((n, h))
    share = defaultdict(set)
    for fi, f in enumerate(faces):
        for i in f: share[i].add(fi)
    segs = []
    for i in range(len(V)): segs.append(("S", O, V[i]))
    for i, j in itertools.combinations(range(len(V)), 2):
        if (i, j) in E: continue
        segs.append(("FD" if share[i] & share[j] else "SD", V[i], V[j]))
    vac = {}
    for i, j in E:
        n = normdir(cross(V[i], V[j])); vac.setdefault(key(n), n)
    vac = list(vac.values())
    lines = {}
    for a, b in itertools.combinations(vac, 2):
        u = cross(a, b)
        if iszero(u): continue
        u = normdir(u); lines.setdefault(key(u), u)
    for u in lines.values():
        def reach(w):
            best = None
            for n, h in planes:
                d = dot(n, w)
                if d.sign() > 0:
                    t = h / d
                    if best is None or (t - best).sign() < 0: best = t
            return best
        t1 = reach(u); t0 = reach(sc(-F.one, u))
        segs.append(("PL", sc(-t0, u), sc(t1, u)))
    return F, V, O, planes, segs, len(vac), len(lines)


def run(ri):
    row = ROWS[ri]
    t0 = time.time()
    F, V, O, planes, segs, nvac, npl = frame(row)
    # merge collinear segments: line key = (direction normalised, moment p x u)
    L = {}
    for fam, p, q in segs:
        u = normdir(sub(q, p)); m = cross(p, u)
        k = (key(u), key(m))
        # parameter along u: s = (x . u) / (u . u) up to a positive factor; use x . u
        s0, s1 = dot(p, u), dot(q, u)
        a, b = (s0, fl(s0)), (s1, fl(s1))
        if cmp(a[0], a[1], b[0], b[1]) > 0: a, b = b, a
        d = L.setdefault(k, {"u": u, "m": m, "p": p, "iv": [], "fams": set()})
        d["iv"].append((a, b, fam)); d["fams"].add(fam)
    lines = []; pieces = []
    for k, d in L.items():
        iv = sorted(d["iv"], key=lambda t: t[0][1])
        merged = []
        for a, b, fam in iv:
            if merged and cmp(a[0], a[1], merged[-1][1][0], merged[-1][1][1]) <= 0:
                if cmp(b[0], b[1], merged[-1][1][0], merged[-1][1][1]) > 0: merged[-1][1] = b
                merged[-1][2].add(fam)
            else:
                merged.append([a, b, {fam}])
        lid = len(lines)
        u = d["u"]; uu = dot(u, u)
        # a point of the line: the foot from O, f = (u x m) / (u . u)
        foot = sc(uu.inv(), cross(u, d["m"]))
        lines.append({"u": u, "uu": uu, "foot": foot, "fams": d["fams"], "pieces": merged, "O": iszero(d["m"])})
        for a, b, fams in merged:
            pa = add(foot, sc(a[0] / uu, u)); pb = add(foot, sc(b[0] / uu, u))
            pieces.append((lid, pa, pb, fams, a, b))
    n = len(pieces)
    E0 = np.array([[fl(x) for x in p[1]] for p in pieces]); E1 = np.array([[fl(x) for x in p[2]] for p in pieces])
    D = E1 - E0; Ln = np.linalg.norm(D, axis=1)
    lid = np.array([p[0] for p in pieces])
    c0 = np.array([lines[p[0]]["O"] for p in pieces])     # two lines through O meet only at O: such pairs are skipped
    CI, CJ, CX = [], [], []; nearpar = []
    tot = 0
    for i0 in range(0, n, 400):
        I = np.arange(i0, min(n, i0 + 400))[:, None]; J = np.arange(n)[None, :]
        mask = (J > I) & (lid[J] != lid[I]) & ~(c0[I] & c0[J])
        Ii, Jj = np.nonzero(mask); Ii = Ii + i0
        if len(Ii) == 0: continue
        cr = np.cross(D[Ii], D[Jj]); crn = np.linalg.norm(cr, axis=1)
        sinv = crn / (Ln[Ii] * Ln[Jj])
        near = sinv < 1e-4
        nearpar += list(zip(Ii[near], Jj[near]))
        ok = ~near
        Ii, Jj, cr, crn = Ii[ok], Jj[ok], cr[ok], crn[ok]
        W = E0[Jj] - E0[Ii]
        dist = np.abs(np.einsum("ij,ij->i", W, cr)) / crn
        keep = dist < 1e-8
        Ii, Jj, cr, W = Ii[keep], Jj[keep], cr[keep], W[keep]
        cc = np.einsum("ij,ij->i", cr, cr)
        t = np.einsum("ij,ij->i", np.cross(W, D[Jj]), cr) / cc
        s = np.einsum("ij,ij->i", np.cross(W, D[Ii]), cr) / cc
        tol = 1e-7
        hit = (t > -tol) & (t < 1 + tol) & (s > -tol) & (s < 1 + tol)
        CI.append(Ii[hit].astype(np.int32)); CJ.append(Jj[hit].astype(np.int32)); CX.append(E0[Ii[hit]] + t[hit][:, None] * D[Ii[hit]])
        tot += int(hit.sum())
        if tot > CAP: break
    if tot > CAP:
        return {"polyhedron": row["name"], "capped": True, "candidate_pairs_over": CAP, "segments": len(segs), "secs": round(time.time() - t0, 1)}
    CI = np.concatenate(CI) if CI else np.zeros(0, np.int32); CJ = np.concatenate(CJ) if CJ else np.zeros(0, np.int32)
    CX = np.concatenate(CX) if CX else np.zeros((0, 3))
    vk = {key(v) for v in V}
    pts = {}
    def status(l, X):
        ln = lines[l]
        s = dot(X, ln["u"]); sf = fl(s)
        for a, b, fams in ln["pieces"]:
            c0 = cmp(s, sf, a[0], a[1]); c1 = cmp(s, sf, b[0], b[1])
            if c0 == 0 or c1 == 0: return ("end", fams)
            if c0 > 0 and c1 < 0: return ("int", fams)
        return None
    def inter(la, lb):
        A, Bq = lines[la], lines[lb]
        u, v = A["u"], Bq["u"]; p, q = A["foot"], Bq["foot"]
        w = cross(u, v)
        if iszero(w): return None
        if dot(sub(q, p), w): return None          # skew
        s = dot(cross(sub(q, p), v), w) / dot(w, w)
        return add(p, sc(s, u))
    def online(l, X):
        return iszero(cross(sub(X, lines[l]["foot"]), lines[l]["u"]))
    def record(X, la, lb):
        k = key(X)
        if k in vk: return
        d = pts.setdefault(k, {"X": X, "lines": set()})
        d["lines"].update((la, lb))
    # group the float points by a 1e-6 grid; one exact point per group, the other pairs checked by exact incidence (a group cut
    # by a cell wall gives the same exact key twice, merged below)
    g = np.floor(CX / 1e-6).astype(np.int64)
    order = np.lexsort((g[:, 2], g[:, 1], g[:, 0]))
    gs = g[order]
    brk = np.nonzero(np.any(gs[1:] != gs[:-1], axis=1))[0] + 1
    starts = np.concatenate([[0], brk]) if len(order) else np.zeros(0, int)
    ends = np.concatenate([brk, [len(order)]]) if len(order) else np.zeros(0, int)
    for a0, a1 in zip(starts, ends):
        X0 = None
        for idx in order[a0:a1]:
            la, lb = int(lid[CI[idx]]), int(lid[CJ[idx]])
            if X0 is not None and online(la, X0) and online(lb, X0):
                record(X0, la, lb); continue
            X = inter(la, lb)
            if X is None: continue
            if X0 is None: X0 = X
            record(X, la, lb)
    for a, b in nearpar:
        la, lb = int(lid[a]), int(lid[b])
        X = inter(la, lb)
        if X is not None: record(X, la, lb)
    hist = Counter(); comp = Counter(); where = Counter(); Oinfo = None
    top = []
    for k, d in pts.items():
        X = d["X"]
        st = {l: status(l, X) for l in d["lines"]}
        st = {l: s for l, s in st.items() if s}
        if len(st) < 2: continue
        m = len(st)
        if iszero(X): continue
        mx = max(((dot(n, X) - h).sign() for n, h in planes))
        loc = "inside" if mx < 0 else "boundary"
        fams = tuple(sorted(Counter("+".join(sorted(s[1])) for s in st.values()).items()))
        hist[(loc, m)] += 1
        comp[(loc, m, fams)] += 1
    stO = [status(l, O) for l, ln in enumerate(lines) if ln["O"]]
    stO = [x for x in stO if x]
    Oinfo = {"lines": len(stO), "families": dict(Counter(f for s_ in stO for f in sorted(s_[1])))}
    out = {"polyhedron": row["name"], "capped": False, "corners": len(V), "segments": dict(Counter(f for f, p, q in segs)),
           "vacuus_plates": nvac, "plate_lines": npl, "lines": len(lines), "pieces": n,
           "centre": Oinfo,
           "inside_points_by_lines": {str(m): c for (loc, m), c in sorted(hist.items()) if loc == "inside"},
           "boundary_points_by_lines": {str(m): c for (loc, m), c in sorted(hist.items()) if loc == "boundary"},
           "inside_marmas": sum(c for (loc, m), c in hist.items() if loc == "inside" and m >= 3),
           "patterns": [{"where": loc, "lines": m, "families": dict(f), "points": c} for (loc, m, f), c in sorted(comp.items(), key=lambda t: (t[0][0], -t[0][1], -t[1]))],
           "secs": round(time.time() - t0, 1)}
    return out


if __name__ == "__main__":
    procs = int(os.environ.get("PROCS", "3"))
    ROWS = [r for r in json.load(open(os.path.join(STUDY, "data/skeletons.json"))) if r["family"] in ("Platonic", "Archimedean")]
    only = os.environ.get("ONLY")
    if only: ROWS = [r for r in ROWS if r["name"] in only.split(",")]
    order = sorted(range(len(ROWS)), key=lambda i: -len(ROWS[i]["V"]))
    res = []
    with mpr.get_context("fork").Pool(procs) as pool:
        for i, r in enumerate(pool.imap_unordered(run, order)):
            res.append(r)
            print(f"PROGRESS {(i + 1) / len(order):.3f} {r['polyhedron']} capped={r['capped']} centre={r.get('centre')} inside={r.get('inside_points_by_lines')} "
                  f"boundary={r.get('boundary_points_by_lines')} ({r['secs']} s)", flush=True)
    json.dump(res, open(os.path.join(STUDY, "data/internal.json" if not only else "data/internal-pilot.json"), "w"), indent=1)
    if len(res) == len(order): print("FINAL ok internal", flush=True)
