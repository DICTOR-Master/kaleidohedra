# DICTO · dictospheres.com — exact rechecks, for this paper, of the Part 2 results of study 2026-11-20-600cell-5cell-zero
# (checks/part2_queens.py there) that §6 states: the five left cap sets against the right ones, the centres of each set on a
# regular 600-cell, the right stabiliser 2T and the 1440 rotations, the tip 600-cell turned by right multiplication and the
# hull, the plates of the capped solid on the 600-cell's 60 mirrors, the caps hidden, the tips on mirrors and cross walls,
# and the compound of five tetrahedra at a corner. Exact arithmetic in Q(√5) only (exact4d.py).
# Usage: import part2; part2.run() -> dict of results (audit.py prints and checks them).
from itertools import combinations
import exact4d as X
from exact4d import Q5, Fr, PHI


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def run():
    P = X.six()['600-cell']; V = P.V; idx = {v: i for i, v in enumerate(V)}; cells = P.cells; cid = {c: k for k, c in enumerate(cells)}
    R = {}
    left = X.caps(P)
    # right orbits
    seen, right = set(), []
    for k, c in enumerate(cells):
        if k in seen: continue
        o = sorted(set(cid[frozenset(idx[X.qmul(V[i], g)] for i in c)] for g in V)); seen |= set(o); right.append(o)
    R['left_sizes'] = sorted(len(o) for o in left); R['right_sizes'] = sorted(len(o) for o in right)
    R['meet'] = sorted({len(set(a) & set(b)) for a in left for b in right})
    R['ten_distinct'] = len({frozenset(o) for o in left + right}) == 10
    cen = [tuple(sum((V[i][j] for i in c), Q5()) for j in range(4)) for c in cells]
    cc = X.dot(cen[0], cen[0]); R['cc'] = cc                           # |sum of 4 corners|² = 16 |centroid|²
    # the centres of each of the ten sets lie on a regular 600-cell: the same inner products as the 600-cell's corners × cc
    gramP = {X.dot(V[0], v) for v in V}
    ok600 = True
    for o in left + right:
        c0 = cen[o[0]]; g = {X.dot(c0, cen[k]) / cc for k in o}
        nb = sum(1 for k in o if X.dot(c0, cen[k]) / cc == PHI / 2)
        ok600 &= (g == gramP and nb == 12)
    R['sets_on_600cells'] = ok600
    # right stabiliser of left set 0 (r with F·r in the set for every F of it): order 24; 1440 = 120 · 24 / 2
    S = set(left[0])
    stab = [g for g in V if all(cid[frozenset(idx[X.qmul(V[i], g)] for i in cells[k])] in S for k in S)]
    R['stab_order'] = len(stab); R['rotations'] = 120 * len(stab) // 2
    R['stab_real_parts'] = sorted(float(g[0]) for g in stab)
    # the tip 600-cell: unit tips = P · ĉ; turn: cos² of the angle from a corner to the nearest cell centre
    best = max((X.dot(V[0], c) * X.dot(V[0], c) / cc for c in cen), key=float); R['turn_cos2'] = best
    # tips' inradius² (radius √2 times the unit 600-cell's inradius² = cc/16): 2 cc/16 > 1, so P is inside: hull = tip 600-cell
    R['tip_inradius2'] = 2 * cc / 16
    V600 = Q5(25) / 4 * PHI * PHI * PHI; solid = V600 + 120 * X.R5 / 96; hull = V600 * 4      # hull edge √2 a: volume × (√2)⁴
    R['hull_ratio'] = solid / hull
    # plates: the 3-space through the centre and a triangle; on a mirror (normal a corner) or a cross wall (normal a centre)
    half = []
    for v in V:
        neg = tuple(-x for x in v)
        if neg not in half: half.append(v)
    mirrors = half                                                     # 60 normals, one of each ± pair
    hc = []
    for c in cen:
        neg = tuple(-x for x in c)
        if neg not in hc: hc.append(c)
    walls = hc                                                         # 300 cross-wall normals
    R['n_mirrors'], R['n_walls'] = len(mirrors), len(walls)
    R['overlap'] = any(X.dot(m, m) * X.dot(w, w) == X.dot(m, w) * X.dot(m, w) for m in mirrors for w in walls)

    def on(pts, normals): return [n for n, m in enumerate(normals) if all(X.dot(m, p) == 0 for p in pts)]
    orb = left[0]; T = {k: X.tip(P, k) for k in orb}
    old = [[V[i] for i in s] for s in P.ridges]
    sides = []
    for k in orb:
        c = sorted(cells[k])
        for u, v in combinations(c, 2): sides.append((k, (u, v), [T[k], V[u], V[v]]))
    per_m = [0] * 60; per_m_side = [0] * 60; bad = 0
    for t in old:
        m = on(t, mirrors); w = on(t, walls)
        if len(m) != 1 or w: bad += 1
        else: per_m[m[0]] += 1
    opp_ok = True
    for k, (u, v), t in sides:
        m = on(t, mirrors); w = on(t, walls)
        if len(m) != 1 or w: bad += 1; continue
        per_m_side[m[0]] += 1
        wx = [i for i in cells[k] if i not in (u, v)]; e = X.sub(V[wx[0]], V[wx[1]])
        mm = mirrors[m[0]]; opp_ok &= (X.dot(mm, mm) * X.dot(e, e) == X.dot(mm, e) * X.dot(mm, e))   # mirror ⟂ opposite edge wx
    R['plates_bad'] = bad; R['per_mirror'] = (sorted(set(per_m)), sorted(set(per_m_side)))
    R['side_mirror_perp_opposite_edge'] = opp_ok
    # each cap: its 10 two-face plates on 10 different mirrors (4 base triangles + 6 sides)
    hid = True
    for k in orb:
        c = sorted(cells[k]); ms = set()
        for tri in combinations(c, 3): ms |= set(on([V[i] for i in tri], mirrors))
        for u, v in combinations(c, 2): ms |= set(on([T[k], V[u], V[v]], mirrors))
        hid &= len(ms) == 10
    R['caps_hidden'] = hid
    R['tip_on'] = sorted({(len(on([t], mirrors)), len(on([t], walls))) for t in T.values()})
    # the tip 600-cell's triangles: on cross walls of P, 20 on each of 60
    TT = list(T.values()); a2t = 2 * P.a2
    adj = {i: set() for i in range(120)}
    for i, j in combinations(range(120), 2):
        d = X.sub(TT[i], TT[j])
        if X.dot(d, d) == a2t: adj[i].add(j); adj[j].add(i)
    tris = [(i, j, k) for i in range(120) for j in adj[i] if j > i for k in adj[i] & adj[j] if k > j]
    wc = {}
    badt = 0
    for t in tris:
        w = on([TT[i] for i in t], walls); m = on([TT[i] for i in t], mirrors)
        if len(w) != 1 or m: badt += 1
        else: wc[w[0]] = wc.get(w[0], 0) + 1
    R['tip_triangles'] = (len(tris), badt, len(wc), sorted(set(wc.values())))
    # at corner 0: the 20 cells split by left set into 5 sets of 4, face centres of each a regular tetrahedron
    star = [k for k, c in enumerate(cells) if 0 in c]
    groups = {}
    for k in star:
        g = [n for n, o in enumerate(left) if k in set(o)][0]; groups.setdefault(g, []).append(k)
    reg = True
    for g, ks in groups.items():
        d = {X.dot(X.sub(cen[a], cen[b]), X.sub(cen[a], cen[b])) for a, b in combinations(ks, 2)}
        reg &= len(ks) == 4 and len(d) == 1
    rgroups = {}
    for k in star:
        g = [n for n, o in enumerate(right) if k in set(o)][0]; rgroups.setdefault(g, []).append(k)
    R['corner'] = (len(star), sorted(len(v) for v in groups.values()), reg,
                   not ({frozenset(v) for v in groups.values()} & {frozenset(v) for v in rgroups.values()}))
    return R


if __name__ == '__main__':
    for k, v in run().items(): print(k, v)
