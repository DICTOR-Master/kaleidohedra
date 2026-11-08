# Switch theorem, part 2: what happens inside each dual cell at a switch point (Theorem B), tested exactly.
# For each switch point lam* (the four of #53 and the two control networks): every dual cell at lam* (sites of equal least power at
# a corner of a power cell, from the relay census engine at the exact lam*) is found, mod translation. Checks:
#  (1) every site of a dual cell is a vertex of it; no dual cell is a simplex; every edge of every dual cell is unlike;
#  (2) the dual cells fill space: their volumes, one per translation class, add up to the lattice cell;
#  (3) Theorem B prediction: just above lam* the like bonds are exactly the edges of conv(A-sites of C) over the dual cells C, and
#      just below the edges of conv(B-sites of C); compared, site by site and by squared length, with the exact walk (#53 data,
#      or our own walk for the controls) on the two neighbouring intervals; the unlike bonds on both sides are the cells' edges;
#  (4) the quadrilateral question of #53 Observation 1: is every such like bond a diagonal of a quadrilateral face of its cell?
# Convex hulls are exact (Fractions; facets from supporting planes through triples).  Usage: python switchlocal.py
import json, os, sys
from fractions import Fraction as Fr
from functools import cmp_to_key
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__))
RELAY = os.path.join(HERE, "..", "..", "2026-10-25-relay-census")
sys.path.insert(0, os.path.join(RELAY, "scripts"))
import extra_nets  # noqa: E402,F401
from engine import Net, Cell, gdot, vsub, solve, rank  # noqa: E402
from networks import NETS  # noqa: E402

checks = []


def check(name, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)


def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def dot(u, v): return sum(x * y for x, y in zip(u, v))
def det3(a, b, c): return dot(a, cross(b, c))


def hull(P):
    """Exact hull of points P (tuples, dim 1..3 inside R^2 or R^3). Returns (dim, vertices, edges, facets) on indices of P."""
    n = len(P); D = len(P[0])
    k = rank([sub(p, P[0]) for p in P[1:]]) if n > 1 else 0
    if k <= 1:
        if n == 1: return 0, [0], [], []
        # extreme points along the line
        u = next(sub(p, P[0]) for p in P[1:] if any(sub(p, P[0])))
        t = [dot(sub(p, P[0]), u) for p in P]
        a, b = t.index(min(t)), t.index(max(t)); return 1, [a, b], [frozenset((a, b))], []
    if k == 2:
        # coordinates in the plane: pick two axes on which the projection is injective
        if D == 2: Q = P
        else:
            vs = [sub(p, P[0]) for p in P[1:]]
            for ax in combinations(range(D), 2):
                if rank([tuple(v[a] for a in ax) for v in vs]) == 2:
                    Q = [tuple(p[a] for a in ax) for p in P]; break
        edges = []
        for i, j in combinations(range(n), 2):
            if Q[i] == Q[j]: continue
            e = sub(Q[j], Q[i]); s = [e[0] * (q[1] - Q[i][1]) - e[1] * (q[0] - Q[i][0]) for q in Q]
            if all(x >= 0 for x in s) or all(x <= 0 for x in s):
                on = [m for m in range(n) if s[m] == 0]
                tt = {m: dot(sub(Q[m], Q[i]), e) for m in on}
                lo, hi = min(on, key=tt.get), max(on, key=tt.get)
                edges.append(frozenset((lo, hi)))
        edges = sorted(set(edges), key=sorted)
        verts = sorted(set(v for e in edges for v in e))
        return 2, verts, edges, [list(range(n))]
    # k == 3
    facets = {}
    for i, j, l in combinations(range(n), 3):
        nv = cross(sub(P[j], P[i]), sub(P[l], P[i]))
        if not any(nv): continue
        s = [dot(nv, sub(p, P[i])) for p in P]
        if all(x >= 0 for x in s) or all(x <= 0 for x in s):
            on = frozenset(m for m in range(n) if s[m] == 0)
            facets[on] = nv
    edges, verts = set(), set()
    for i, j in combinations(range(n), 2):
        F = [f for f in facets if i in f and j in f]
        if len(F) >= 2:
            # the line ij is an edge line; keep only the two extreme points on it
            line = [m for m in F[0] if all(m in f for f in F)]
            u = sub(P[j], P[i]); tt = {m: dot(sub(P[m], P[i]), u) for m in line}
            edges.add(frozenset((min(line, key=tt.get), max(line, key=tt.get))))
    for m in range(n):
        if rank([facets[f] for f in facets if m in f]) == 3: verts.add(m)
    return 3, sorted(verts), sorted(edges, key=sorted), [sorted(f) for f in facets]


def polygon_order(Q, idx):
    c = tuple(sum(Q[i][r] for i in idx) / len(idx) for r in range(2))
    def half(v): return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1
    def cmp(a, b):
        u, v = sub(Q[a], c), sub(Q[b], c)
        if half(u) != half(v): return half(u) - half(v)
        cr = u[0] * v[1] - u[1] * v[0]
        return -1 if cr > 0 else (1 if cr < 0 else 0)
    return sorted(idx, key=cmp_to_key(cmp))


def volume(P, dim, facets, verts):
    """Exact coordinate volume (area in 2D) of conv(P)."""
    if len(P[0]) == 2:
        o = polygon_order(P, verts)
        return abs(sum(P[o[q]][0] * P[o[(q + 1) % len(o)]][1] - P[o[(q + 1) % len(o)]][0] * P[o[q]][1] for q in range(len(o)))) / 2
    cen = tuple(sum(P[v][r] for v in verts) / len(verts) for r in range(3)); vol = Fr(0)
    for f in facets:
        nv = next(cross(sub(P[b], P[a]), sub(P[c], P[a])) for a, b, c in combinations(f, 3) if any(cross(sub(P[b], P[a]), sub(P[c], P[a]))))
        ax = next(a for a in range(3) if nv[a] != 0)
        keep = [a for a in range(3) if a != ax]
        Q = {m: tuple(P[m][a] for a in keep) for m in f}
        o = polygon_order(Q, [m for m in f])
        for q in range(1, len(o) - 1):
            vol += abs(det3(sub(P[o[0]], cen), sub(P[o[q]], cen), sub(P[o[q + 1]], cen))) / 6
    return vol


def lattice_coeffs(net, v):
    X = solve([[net.T[q][r] for q in range(net.d)] for r in range(net.d)], [[x] for x in v])
    return tuple(X[r][0] for r in range(net.d))


def canon(net, pts):
    """Translation class of a finite set of sites: translate its lexicographically smallest site into the motif."""
    p = min(pts)
    for _, m in net.motif:
        t = lattice_coeffs(net, sub(p, m))
        if all(x.denominator == 1 for x in t):
            L = sub(p, m); return tuple(sorted(sub(q, L) for q in pts))
    raise AssertionError("site not in the net")


def kind_of(net, p):
    for k, m in net.motif:
        if all(x.denominator == 1 for x in lattice_coeffs(net, sub(p, m))): return k
    raise AssertionError


def walk_record(key):
    p = os.path.join(RELAY, "data", "raw", key + ".json")
    if not os.path.exists(p): p = os.path.join(HERE, "..", "data", key + "-walk.json")
    return json.load(open(p))


CASES = [("square", Fr(0)), ("honeycomb", Fr(-1, 2)), ("nacl", Fr(0)), ("delian", Fr(-1, 8)), ("hbn", Fr(0)), ("sodalite", Fr(0))]


def run(key, L):
    spec = NETS[key]; net = Net(spec["name"], spec["G"], spec["T"], spec["motif"], spec["w"]); A, B = spec["A"], spec["B"]
    d = net.d; D2 = Fr(spec["D2"])
    cells = {}            # canon -> list of sites
    at_site = {}          # motif i -> list of dual cells (absolute coordinates) at the corners of its power cell
    for i, (ki, ci) in enumerate(net.motif):
        cell = Cell(net, i, (L,), D2); at_site[i] = []
        for c in cell.corners:
            pts = sorted(set([ci] + [cell.H[k]["c"] for k in c["on"]]))
            at_site[i].append(pts); cells.setdefault(canon(net, pts), pts)
    # (1) shape of every dual cell
    ok_vert = ok_bip = ok_simp = True; vol = Fr(0); shapes = []
    info = {}
    for key_c, pts in cells.items():
        kinds = [kind_of(net, p) for p in pts]
        dim, verts, edges, facets = hull(pts)
        ok_vert &= (dim == d and len(verts) == len(pts))
        ok_simp &= len(pts) > d + 1
        ok_bip &= all(kinds[a] != kinds[b] for a, b in map(sorted, edges))
        vol += volume(pts, dim, facets, verts)
        shapes.append(f"{len(pts)} sites ({kinds.count(A)} {A} + {kinds.count(B)} {B}), {len(edges)} edges, "
                      f"{len(facets) if d == 3 else len(verts)} {'faces' if d == 3 else 'sides'}")
        info[key_c] = (pts, kinds, facets)
    T = abs(sp_det([list(v) for v in net.T]))
    check(f"{key} at {L}: every site of every dual cell is a vertex of it", ok_vert)
    check(f"{key} at {L}: no dual cell is a simplex", ok_simp)
    check(f"{key} at {L}: every edge of every dual cell joins unlike sites (bipartite)", ok_bip)
    check(f"{key} at {L}: dual cells, one per translation class, fill the lattice cell", vol == T, f"{vol} vs {T}; cells: {sorted(set(shapes))}")
    # (3) Theorem B prediction vs the exact walk
    rec = walk_record(key)
    above = next(r for r in rec["intervals"] if Fr(r["lo"]) == L); below = next(r for r in rec["intervals"] if Fr(r["hi"]) == L)
    stop = next(r for r in rec["stops"] if Fr(r["lam"]) == L)
    quad_yes = quad_no = 0; pred_all = True
    for i, (ki, ci) in enumerate(net.motif):
        for side, X, r in (("above", A, above), ("below", B, below)):
            site = next(s for s in r["sites"] if s["i"] == i)
            want_like = {o: n for o, n in site["orbits"].items() if o.split("@")[0] == ki}
            want_unlike = {o: n for o, n in site["orbits"].items() if o.split("@")[0] != ki}
            got_like = {}
            if ki == X:
                ends = set()
                for pts in at_site[i]:
                    S = [p for p in pts if kind_of(net, p) == X]
                    if len(S) < 2: continue
                    _, _, eS, _ = hull(S)
                    for a, b in map(sorted, eS):
                        if ci in (S[a], S[b]):
                            q = S[b] if S[a] == ci else S[a]
                            if q in ends: continue
                            ends.add(q)
                            # quadrilateral face of this dual cell containing both ends?
                            facets = hull(pts)[3] if d == 3 else [list(range(len(pts)))]
                            inq = any(len(f) == 4 and ci in [pts[m] for m in f] and q in [pts[m] for m in f] for f in facets)
                            quad_yes += inq; quad_no += (not inq)
                for q in ends:
                    o = f"{ki}@{gdot(net.G, sub(q, ci), sub(q, ci))}"; got_like[o] = got_like.get(o, 0) + 1
            st = next(s for s in stop["sites"] if s["i"] == i)
            unl = set()
            for pts in at_site[i]:
                _, _, eC, _ = hull(pts)
                for a, b in map(sorted, eC):
                    if ci in (pts[a], pts[b]): unl.add(pts[b] if pts[a] == ci else pts[a])
            got_unlike = {}
            for q in unl:
                o = f"{kind_of(net, q)}@{gdot(net.G, sub(q, ci), sub(q, ci))}"; got_unlike[o] = got_unlike.get(o, 0) + 1
            ok = (got_like == want_like) and (want_unlike == st["orbits"] == got_unlike)
            pred_all &= ok
            if not ok:
                print(f"   mismatch {key} site {i} {ki} {side}: predicted like {got_like} walk like {want_like}; "
                      f"unlike walk {want_unlike} vs stop {st['orbits']}", flush=True)
    check(f"{key} at {L}: like bonds on each side = edges of conv(A-sites) above, conv(B-sites) below; unlike bonds = cell edges",
          pred_all, f"like bonds counted at motif sites: {quad_yes} are diagonals of a quadrilateral face, {quad_no} are not")
    return dict(lam=str(L), cells=sorted(set(shapes)), quad_diagonal=quad_yes, not_quad=quad_no)


def sp_det(M):
    import sympy as sp
    return Fr(str(sp.Matrix(M).det()))


if __name__ == "__main__":
    out = {key: run(key, L) for key, L in CASES}
    json.dump(out, open(os.path.join(HERE, "..", "data", "switchlocal.json"), "w"), indent=1)
    with open(os.path.join(HERE, "..", "data", "switchlocal-checks.txt"), "w") as fh:
        for s, n, det in checks: fh.write(f"{s} {n} {det}\n")
    for k, v in out.items(): print(k, v)
    nf = sum(1 for c in checks if c[0] == "FAIL")
    print(f"{len(checks) - nf}/{len(checks)} PASS")
    print('FINAL ok' if checks and nf == 0 else f'FINAL FAIL: {nf} of {len(checks)} checks failed')
