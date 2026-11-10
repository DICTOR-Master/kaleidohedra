"""A geometric scutoid solid (DICTO 10 Nov: "did we get a scutoid solid … like a geometric one"). Brick-pairing layer (version a):
bottom z = 0 the hexagonal tiling; middle z = 1 the pentagon tiling (paired edges collapsed, three edge directions kept: LP);
top z = 2: each collapsed point reopens ACROSS into a horizontal edge (the scutoid move), every other edge parallel to its middle edge
(flat side faces; LP in the corner positions). A cell that gains nothing at the top goes hexagon -> pentagon with its Y-point halfway:
a scutoid. Its faces: bottom hexagon, top pentagon, lateral trapezoids / triangles, all exactly planar (checked). Output: JSON of the
solid for the renderer. Usage: python scutoid_solid.py"""
import itertools, json, numpy as np
from scipy.optimize import linprog
s3 = 3 ** .5; NX, NY = 8, 6
def centre(i, j): return np.array([i + 0.5 * (j % 2), j * s3 / 2])
ang = np.radians([90, 30, -30, -90, -150, 150])
corner = lambda c, k: c + np.array([np.cos(ang[k]), np.sin(ang[k])]) / s3
key = lambda p: tuple(np.round(p, 6))
V = {}; cells = {}
for i, j in itertools.product(range(NX), range(NY)):
    c = centre(i, j); cells[(i, j)] = [V.setdefault(key(corner(c, k)), len(V)) for k in range(6)]
P0 = np.zeros((len(V), 2))
for p, idx in V.items(): P0[idx] = p
E = {}
for ij, ids in cells.items():
    for k in range(6): E.setdefault(frozenset((ids[k], ids[(k + 1) % 6])), []).append(ij)
coll = {frozenset((cells[(i, j)][1], cells[(i, j)][2])) for i, j in cells if (i + j) % 2 == 0 and (i + 1, j) in cells}
# ---- middle: positions Q (LP): kept edges parallel to their hexagon edge, length >= f; collapsed edges zero
n = len(V); f = 0.12
def lp_positions(dirs_of, zero_edges, floor, fix, target):
    """positions x (2n) and slacks u (2n): minimise sum u = sum |x - target| (stay upright over the level below) s.t. for each edge
    (a,b) with direction d: d_perp.(x_b - x_a) = 0 (parallel: flat side faces), d.(x_b - x_a) >= floor; zero edges collapse."""
    N = 2 * n; A_eq, b_eq, A_ub, b_ub = [], [], [], []
    def row(): return np.zeros(2 * N)
    for (a, b), d in dirs_of.items():
        perp = np.array([-d[1], d[0]]); r = row(); r[2 * b:2 * b + 2] += perp; r[2 * a:2 * a + 2] -= perp; A_eq.append(r); b_eq.append(0)
        r = row(); r[2 * b:2 * b + 2] -= d; r[2 * a:2 * a + 2] += d; A_ub.append(r); b_ub.append(-floor)
    for (a, b) in zero_edges:
        for q in range(2):
            r = row(); r[2 * b + q] = 1; r[2 * a + q] = -1; A_eq.append(r); b_eq.append(0)
    tg = target.ravel()
    for k in range(N):                                  # u_k >= |x_k - target_k|
        r = row(); r[k] = 1; r[N + k] = -1; A_ub.append(r); b_ub.append(tg[k])
        r = row(); r[k] = -1; r[N + k] = -1; A_ub.append(r); b_ub.append(-tg[k])
    cvec = np.concatenate([np.zeros(N), np.ones(N)])
    res = linprog(cvec, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq) if A_eq else None, b_eq=b_eq if b_eq else None, bounds=[(None, None)] * N + [(0, None)] * N, method='highs')
    assert res.status == 0, res.message
    x = res.x[:N].reshape(-1, 2); return x, min(float(d @ (x[b] - x[a])) for (a, b), d in dirs_of.items())
dmid = {}
for e in E:
    if e in coll: continue
    a, b = sorted(e); d = P0[b] - P0[a]; dmid[(a, b)] = d / np.linalg.norm(d)
Q, tq = lp_positions(dmid, [tuple(sorted(e)) for e in coll], 0.3, 0, P0)
print(f'middle: shortest kept edge {tq:.4f}')
# ---- top: reopen each collapsed point across (T1): a = upper end, b = lower end of the vertical paired edge
nb = {v: set() for v in range(n)}
for e in E:
    a, b = tuple(e); nb[a].add(b); nb[b].add(a)
top_edges = {}
moved = {}
for e in coll:
    a, b = sorted(e, key=lambda v: -P0[v][1])               # a upper, b lower
    ua = [x for x in nb[a] if x != b]; lb = [x for x in nb[b] if x != a]
    ur = max(ua, key=lambda x: P0[x][0]); ll = min(lb, key=lambda x: P0[x][0])
    moved[(a, ur)] = (b, ur); moved[(b, ll)] = (a, ll)       # a keeps its upper-left, takes b's lower-left; b keeps lower-right, takes a's upper-right
    top_edges[(a, b)] = np.array([1.0, 0.0]) if P0[a][0] <= P0[b][0] else np.array([-1.0, 0.0])
for (a, b), d in dmid.items():
    if (a, b) in moved: a2, b2 = moved[(a, b)]; top_edges[tuple(sorted((a2, b2)))] = d if a2 < b2 else -d
    elif (b, a) in moved: b2, a2 = moved[(b, a)]; top_edges[tuple(sorted((a2, b2)))] = d if a2 < b2 else -d
    else: top_edges[(a, b)] = d
# orient each top edge direction with the vertex order (a < b): direction of x_b - x_a
dtop = {}
for (a, b), d in top_edges.items():
    if (a, b) in [tuple(sorted(e)) for e in coll]:
        # the new horizontal edge: from the left new vertex to the right one
        L, R = (a, b) if P0[a][0] <= P0[b][0] else (b, a); dtop[(min(L, R), max(L, R))] = np.array([1.0, 0.0]) if L < R else np.array([-1.0, 0.0])
    else: dtop[(a, b)] = d
T, tt = lp_positions(dtop, [], 0.25, 0, Q)
print(f'top: shortest edge {tt:.4f}')
# ---- top cell polygons after the T1 moves (a = upper end, b = lower end of each paired vertical edge)
cen = {ij: np.mean([P0[v] for v in ids], 0) for ij, ids in cells.items()}
topc = {ij: list(ids) for ij, ids in cells.items()}
for e in coll:
    a, b = sorted(e, key=lambda v: -P0[v][1])
    owners = [ij for ij, ids in cells.items() if a in ids or b in ids]
    for ij in owners:
        ids = cells[ij]; ha, hb = a in ids, b in ids; L = topc[ij]
        if ha and hb:                                  # A (left) keeps a, B (right) keeps b
            left = cen[ij][0] < P0[a][0]
            L.remove(b if left else a)
        elif ha:                                       # C (above): a gets b beside it, on the side of its right neighbour
            k = L.index(a); nxt, prv = L[(k + 1) % len(L)], L[k - 1]
            L.insert(k + 1 if P0[nxt][0] > P0[prv][0] else k, b)
        elif hb:                                       # D (below): b gets a beside it, on the side of its left neighbour
            k = L.index(b); nxt, prv = L[(k + 1) % len(L)], L[k - 1]
            L.insert(k + 1 if P0[nxt][0] < P0[prv][0] else k, a)
counts = {ij: len(L) for ij, L in topc.items() if 1 <= ij[0] <= NX - 2 and 1 <= ij[1] <= NY - 2}
print('top side counts (interior cells):', {k: list(counts.values()).count(k) for k in sorted(set(counts.values()))})
pick = next(ij for ij in sorted(counts) if counts[ij] == 5 and 2 <= ij[0] <= NX - 3 and 2 <= ij[1] <= NY - 3 and sum(frozenset((cells[ij][k], cells[ij][(k + 1) % 6])) in coll for k in range(6)) == 1)
ids = cells[pick]
def pts(seq, pos, z):
    out = []
    for v in seq:
        p = tuple(np.round(pos[v], 9))
        if not out or p != tuple(np.round(out[-1][:2], 9)): out.append(np.array([*pos[v], z]))
    if len(out) > 1 and np.allclose(out[0], out[-1]): out.pop()
    return out
bot = pts(ids, P0, 0.0); mid = pts(ids, Q, 1.0); top = pts(topc[pick], T, 2.0)
print(f'scutoid cell {pick}: bottom {len(bot)}-gon, middle {len(mid)}-gon, top {len(top)}-gon')
# faces: lower lateral (bottom edge -> middle edge, a vanished edge gives a triangle), upper lateral (middle -> top), bottom, top
faces = [list(range(len(bot)))]
V3 = [list(p) for p in bot] + [list(p) for p in mid] + [list(p) for p in top]
ob, om, ot = 0, len(bot), len(bot) + len(mid)
midkey = [tuple(np.round(Q[v], 9)) for v in ids]; mk = [tuple(np.round(p[:2], 9)) for p in mid]
for k in range(6):
    u, w = ids[k], ids[(k + 1) % 6]; iu, iw = mk.index(midkey[k]), mk.index(midkey[(k + 1) % 6])
    faces.append([ob + k, ob + (k + 1) % 6] + ([om + iw, om + iu] if iu != iw else [om + iu]))
topkey = [tuple(np.round(T[v], 9)) for v in topc[pick]]; tk = [tuple(np.round(p[:2], 9)) for p in top]
# upper lateral: middle corner sequence of this cell -> top corner sequence (same cyclic order; match by vertex id)
midids = []
for v in ids:
    kk = tuple(np.round(Q[v], 9))
    if not midids or tuple(np.round(Q[midids[-1]], 9)) != kk: midids.append(v)
if tuple(np.round(Q[midids[0]], 9)) == tuple(np.round(Q[midids[-1]], 9)): midids.pop()
# the merged mid corner (a=b) maps to whichever of a, b the cell keeps on top
tops = topc[pick]
mapm = [next((x for x in (v, ) + tuple(w for w in ids if tuple(np.round(Q[w], 9)) == tuple(np.round(Q[v], 9))) if x in tops)) for v in midids]
for k in range(len(midids)):
    a1, a2 = mapm[k], mapm[(k + 1) % len(midids)]
    faces.append([om + k, om + (k + 1) % len(midids), ot + tops.index(a2), ot + tops.index(a1)])
faces.append([ot + q for q in range(len(top))][::-1])
def planar(F):
    P = np.array([V3[q] for q in F]);
    if len(P) < 4: return 0.0
    nrm = np.cross(P[1] - P[0], P[2] - P[0]); nrm /= np.linalg.norm(nrm); return float(np.abs((P - P[0]) @ nrm).max())
worst = max(planar(F) for F in faces)
print(f'faces {len(faces)}; largest distance of a corner from its face plane {worst:.2e} (every face flat)')
json.dump({'V': V3, 'F': faces, 'bottom_n': len(bot), 'top_n': len(top)}, open('scutoid-solid.json', 'w'))
print('FINAL ok' if worst < 1e-9 and len(bot) == 6 and len(top) == 5 else 'FINAL FAIL')
