"""Theorem 3 of paper #118, odd edges alone (audit 2026-11-24, items 1 and 2).
Question: do the conditions from the odd edges ALONE (interior edges with an odd number of cells round them) have a common
solution?  seams_mirror.py solved (M - I) x = -t over the holonomies of ALL loops of walls; this script solves the same kind of
equations, with the same unknowns (x0 = core position in the start cell) and the same exact arithmetic (Q(sqrt5)), but only for
the loops that go once round an odd interior edge.
Method: same patch, same wall reflections, same BFS frames g_T from the same start cell as seams_mirror.py.  For each interior
edge, the cells round it are joined in a cycle c1 -W1- c2 - ... - ck -Wk- c1 by the walls that contain the edge (interior is
decided exactly: the walls containing the edge join its cells in one closed cycle).  The loop holonomy in the start frame is
g_{c1}^{-1} W_k ... W_1 g_{c1}; for odd k it is a reflection (checked exactly) and x0 must lie on its mirror plane.
Also: (b) if the odd-edge system is consistent, which loop conditions (one non-tree wall each) make it inconsistent;
(c) the loop counts: 998 walls = tree walls + non-tree walls, and the holonomy kinds of the non-tree walls only.
Usage: python odd_edges.py"""
import json, os, sys, itertools
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
from ammann_cell import Q, dot, cross, vsub, vadd, vsc, det3
from tiling import E
patch = json.load(open(os.path.join(HERE, "../data/patch.json"))); tiles = patch["tiles"]
def P3(v6): return [sum((E[i][r]*v6[i] for i in range(6)), Q(0)) for r in range(3)]
# ---- identical to seams_mirror.py ----
def refl(n, f):
    nn = dot(n, n); M = [[(1 if r == c else 0) - (2*n[r]*n[c])/nn for c in range(3)] for r in range(3)]
    Mf = [dot(M[r], f) for r in range(3)]; return (M, vsub(f, Mf))
def comp(a, b):   # a after b
    Ma, ta = a; Mb, tb = b
    M = [[sum((Ma[r][k]*Mb[k][c] for k in range(3)), Q(0)) for c in range(3)] for r in range(3)]
    return (M, vadd([dot(Ma[r], tb) for r in range(3)], ta))
def eq(a, b): return all((x - y).sign() == 0 for r in range(3) for x, y in zip(a[0][r] + [a[1][r]], b[0][r] + [b[1][r]]))
Id = ([[Q(1) if r == c else Q(0) for c in range(3)] for r in range(3)], [Q(0)]*3)
def inv(a):
    M, t = a; Mt = [[M[c][r] for c in range(3)] for r in range(3)]
    return (Mt, vsc(-1, [dot(Mt[r], t) for r in range(3)]))
adj = {}; walls = []
for t1, t2, pts in patch["shared"]:
    X = [P3(p) for p in pts]; n = cross(vsub(X[1], X[0]), vsub(X[3], X[0])); W = refl(n, X[0])
    adj.setdefault(t1, []).append((t2, W)); adj.setdefault(t2, []).append((t1, W)); walls.append((t1, t2, W, pts))
start = min(range(len(tiles)), key=lambda i: sum(x*x for x in tiles[i]["centre"]))
g = {start: Id}; order = [start]; parent = {}
for a in order:
    for b, W in adj.get(a, []):
        if b not in g: g[b] = comp(W, g[a]); order.append(b); parent[b] = a
print(f"cells {len(tiles)}, reached {len(g)}, walls {len(walls)}, start cell {start}")
# ---- (c) loop counts: tree walls vs loops ----
tree = set()
for b, a in parent.items():   # the wall used by the BFS to reach b (first wall in patch order between a and b)
    tree.add(next(k for k, (t1, t2, W, p) in enumerate(walls) if {t1, t2} == {a, b}))
def wall_hol(k):
    t1, t2, W, p = walls[k]; return comp(inv(g[t2]), comp(W, g[t1]))
def kind(h):
    if eq(h, Id): return "identity"
    return "improper" if det3(*h[0]).sign() < 0 else "proper"
tree_kinds = Counter(kind(wall_hol(k)) for k in tree)
loop_walls = [k for k in range(len(walls)) if k not in tree]
loop_kinds = Counter(kind(wall_hol(k)) for k in loop_walls)
print(f"(c) tree walls {len(tree)} (holonomy kinds {dict(tree_kinds)}); loops (non-tree walls) {len(loop_walls)}: {dict(loop_kinds)}")
print(f"    all 998 counted together as in seams_mirror.py: identity {tree_kinds['identity'] + loop_kinds['identity']}, "
      f"improper {loop_kinds['improper']}, proper {loop_kinds['proper']}")
counts_ok = (len(tree) == 401 and tree_kinds == Counter(identity=401) and len(loop_walls) == 597
             and loop_kinds == Counter(identity=27, improper=368, proper=202))
print(f"    597 = 27 + 368 + 202: {counts_ok}")
# ---- interior edges, exactly ----
edges = {}
for T, t in enumerate(tiles):
    n, A = t["n"], t["A"]
    for k in range(3):
        l = A[k]; o1, o2 = [A[q] for q in range(3) if q != k]
        for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
            v = list(n); v[o1] += a; v[o2] += b; w = list(v); w[l] += 1
            edges.setdefault((tuple(v), tuple(w)), set()).add(T)
wall_of_edge = {}
for k, (t1, t2, W, pts) in enumerate(walls):
    P = [tuple(p) for p in pts]
    for i in range(4):
        u, v = P[i], P[(i + 1) % 4]
        e = (u, v) if (u, v) in edges else (v, u)
        wall_of_edge.setdefault(e, []).append(k)
def cycle(e):
    cells = edges[e]; ws = wall_of_edge.get(e, [])
    if len(ws) != len(cells) or len(cells) < 3: return None
    nb = {c: [] for c in cells}
    for k in ws:
        t1, t2 = walls[k][0], walls[k][1]
        if t1 not in nb or t2 not in nb: return None
        nb[t1].append((t2, k)); nb[t2].append((t1, k))
    if any(len(x) != 2 for x in nb.values()): return None
    c0 = min(cells); seq = [c0]; wk = []; prev_w = None; c = c0
    while True:
        nxt, k = next((d, k) for d, k in nb[c] if k != prev_w)
        wk.append(k); prev_w = k
        if nxt == c0: break
        seq.append(nxt); c = nxt
    return (seq, wk) if len(seq) == len(cells) else None
interior = {e: cyc for e in edges if (cyc := cycle(e)) is not None}
deg = Counter(len(c[0]) for c in interior.values())
print(f"interior edges (exact cycle test) {len(interior)}: {dict(sorted(deg.items()))}")
print(f"    agrees with seams_mirror.py (814; 3:364 4:239 5:156 6:13 7:30 8:10 9:2): "
      f"{len(interior) == 814 and deg == Counter({3: 364, 4: 239, 5: 156, 6: 13, 7: 30, 8: 10, 9: 2})}")
def edge_hol(e):
    seq, wk = interior[e]; H = Id; c = seq[0]
    for k in wk:
        H = comp(walls[k][2], H)
    return comp(inv(g[seq[0]]), comp(H, g[seq[0]])), H, seq[0]
# ---- the odd-edge system ----
def rows_of(h):
    M, t = h; return [[M[r][c] - (1 if r == c else 0) for c in range(3)] + [-t[r]] for r in range(3)]
def solve(R):
    R = [list(r) for r in R]; rk = 0; piv = []
    for c in range(3):
        p_ = next((k for k in range(rk, len(R)) if R[k][c].sign() != 0), None)
        if p_ is None: continue
        R[rk], R[p_] = R[p_], R[rk]; pv = R[rk][c]; R[rk] = [x/pv for x in R[rk]]
        for k in range(len(R)):
            if k != rk and R[k][c].sign() != 0:
                f = R[k][c]; R[k] = [a - f*b for a, b in zip(R[k], R[rk])]
        piv.append(c); rk += 1
    incons = any(all(x.sign() == 0 for x in r[:3]) and r[3].sign() != 0 for r in R)
    return rk, piv, incons, R[:rk]
odd = [e for e in interior if len(interior[e][0]) % 2]
planes = []; all_refl = True
for e in odd:
    h, H, c1 = edge_hol(e)
    M = h[0]; MM = comp(h, h)
    rk_, _, _, _ = solve([r[:3] + [Q(0)] for r in rows_of(h)])
    # a reflection: det -1, h^2 = id, M - I of rank 1, and the local map H fixes both ends of the edge
    ends = [P3(list(v)) for v in e]
    fixes = all(all((a - b).sign() == 0 for a, b in zip(vadd([dot(H[0][r], p) for r in range(3)], H[1]), p)) for p in ends)
    isrefl = det3(*M).sign() < 0 and eq(MM, Id) and rk_ == 1 and fixes
    all_refl &= isrefl
    r0 = next(r for r in rows_of(h) if any(x.sign() != 0 for x in r[:3]))
    planes.append(r0)   # one equation a.x = b (written a.x - b with b = -t-part: row = [a | b] meaning a.x = b)
print(f"odd interior edges {len(odd)}; every odd-edge holonomy is a reflection whose mirror contains the edge (exact): {all_refl}")
rk, piv, incons, Rred = solve(planes)
if incons:
    print(f"(a) ODD EDGES ALONE: rank {rk}, EMPTY (inconsistent)")
else:
    sol = {3: "a single point", 2: "a line", 1: "a plane", 0: "all of space"}[rk]
    print(f"(a) ODD EDGES ALONE: CONSISTENT, rank {rk}; common solution set = {sol}")
    for r in Rred: print("    reduced equation:", " + ".join(f"({r[c]})*x{c}" for c in range(3) if r[c].sign() != 0), "=", r[3])
# distinct mirror planes (normalised)
def normal_form(r):
    c = next(c for c in range(4) if r[c].sign() != 0); return tuple(str(x/r[c]) for x in r)
distinct = {normal_form(r) for r in planes}
print(f"    distinct mirror planes among the odd edges: {len(distinct)}")
# certificate for the inconsistent case: <= 4 planes (rank of A plus one)
if incons:
    basis = []
    for i, r in enumerate(planes):
        if solve([planes[j][:3] + [Q(0)] for j in basis + [i]])[0] > len(basis): basis.append(i)
        if len(basis) == rk: break
    j = next(i for i in range(len(planes)) if solve([planes[k] for k in basis + [i]])[2])
    cert = basis + [j]
    # try to shrink: drop any plane that keeps it inconsistent
    for i in list(cert):
        if len(cert) > 2 and solve([planes[k] for k in cert if k != i])[2]: cert.remove(i)
    print(f"    certificate: {len(cert)} odd edges whose mirror planes have no common point:")
    for k in cert: print("     edge", odd[k], "cells", len(interior[odd[k]][0]), "plane", planes[k])
# ---- (b) loop conditions that break a consistent odd-edge system ----
if not incons:
    breakers = [k for k in loop_walls if solve(planes + rows_of(wall_hol(k)))[2]]
    bk = Counter(kind(wall_hol(k)) for k in breakers)
    print(f"(b) single loop conditions (non-tree walls) that make the odd-edge system inconsistent: {len(breakers)} of "
          f"{len(loop_walls)} ({dict(bk)})")
    if breakers:
        k = breakers[0]; t1, t2, W, p = walls[k]
        print(f"    smallest added set: 1 loop, e.g. wall {k} between cells {t1} and {t2} ({kind(wall_hol(k))})")
# ---- side line: all interior edges (odd and even) ----
erows = [r for e in interior for r in rows_of(edge_hol(e)[0])]
rk2, _, inc2, _ = solve(erows)
print(f"side: all {len(interior)} edge loops (odd and even): rank {rk2}, {'EMPTY' if inc2 else 'consistent'}")
allrows = [r for k in loop_walls for r in rows_of(wall_hol(k))]
rk3, _, inc3, _ = solve(allrows)
print(f"check: all {len(loop_walls)} loops as in seams_mirror.py: rank {rk3}, {'EMPTY (reproduces the original)' if inc3 else 'consistent'}")
ok = counts_ok and all_refl and len(interior) == 814 and inc3
print("FINAL ok" if ok else "FINAL FAILED (see above)")
