"""DICTO slot assemblies, 25 Nov 2026: every way to slot three mutually perpendicular cards (planes x = 0, y = 0, z = 0), for the
octahedron cut (each card the square on the four octahedron corners in its plane: |u| + |v| <= 1) and the cube cut (the cube's middle
square: |u|, |v| <= 1). Exhaustive exact search in a voxel model.

Model (exact for its own geometry, integer arithmetic only): unit voxels; card k is the layer x_k = 0, one voxel thick (thickness t = 1),
its region |u| + |v| <= N (octahedron cut) or max(|u|, |v|) <= N (cube cut). Two cards share the voxels of one axis; all three share the
centre voxel. A slot of width t is exactly a shared voxel given to the other card. A scheme gives every shared voxel to one card or to
none: each of the six half-axes (m = 1..N from the centre) is 'A' (all to the first card), 'B' (all to the second), 'Ai' (A owns the
inner half m <= N/2, B the outer), 'Bi', or '-' (none); the centre voxel to X, Y, Z or none. Pieces = connected parts of each card's
voxels. So every cut lies on a line where two planes meet, and no two pieces share a voxel (asserted).
Moves: straight-line translations to infinity along the 26 directions d in {-1,0,1}^3; a moving unit cube from s meets the cell r iff,
with delta = r - s and m_i = delta_i d_i: delta_i = 0 where d_i = 0, min m >= 0 and max m - min m <= 1 (exact sweep test, derived in the
README). Blocking is pairwise, so a set S of pieces can move along d iff no piece of S is blocked by a piece outside S.
Assembly: sequential (one piece at a time; greedy is complete since removing a piece only frees others) and, where that fails, the full
two-handed search (any subassembly moved as one rigid unit, recursive over all splits) before IMPOSSIBLE is written.
Usage: python schemes.py N out.json [stride]   (prints PROGRESS lines and FINAL ok)"""
import sys, json, itertools, time
import numpy as np

N = int(sys.argv[1]); OUT = sys.argv[2]; STRIDE = int(sys.argv[3]) if len(sys.argv) > 3 else 1   # stride > 1: pilot on every STRIDE-th scheme
DIRS = [d for d in itertools.product((-1, 0, 1), repeat=3) if any(d)]
CARD = 'XYZ'
HALF = [(a, s) for a in range(3) for s in (1, -1)]           # half-axes +x, -x, +y, -y, +z, -z
OPTS = ['A', 'B', 'Ai', 'Bi', '-']
def sharers(a): return [k for k in range(3) if k != a]       # cards whose planes contain axis a (A = first, B = second)

def region(k, cut):
    out = set()
    for u in range(-N, N + 1):
        for v in range(-N, N + 1):
            if (abs(u) + abs(v) if cut == 'octahedron' else max(abs(u), abs(v))) <= N:
                p = [0, 0, 0]; i, j = sharers(k); p[i], p[j] = u, v; out.add(tuple(p))
    return out

def owner_of(scheme, p):
    """card owning a shared voxel p (on an axis) under the scheme, or None"""
    nz = [i for i in range(3) if p[i]]
    if not nz: return scheme[6]
    a = nz[0]; m = abs(p[a]); s = 1 if p[a] > 0 else -1
    o = scheme[HALF.index((a, s))]; A, B = sharers(a)
    if o == 'A': return A
    if o == 'B': return B
    if o == 'Ai': return A if m <= N // 2 else B
    if o == 'Bi': return B if m <= N // 2 else A
    return None

def components(S):
    S = set(S); out = []
    while S:
        st = [S.pop()]; c = set(st)
        while st:
            p = st.pop()
            for i in range(3):
                for e in (1, -1):
                    q = list(p); q[i] += e; q = tuple(q)
                    if q in S: S.remove(q); c.add(q); st.append(q)
        out.append(c)
    return out

def pieces(scheme, cut):
    P = []
    for k in range(3):
        mine = {p for p in REG[cut][k] if sum(1 for x in p if x) == 2 or owner_of(scheme, p) == k}
        # the centre voxel is a point when t -> 0: it never joins two parts of a card (a neck of width t is not a card).
        # Parts are found without it; it then goes with the first part next to it (or stands alone, a sliver).
        cen = (0, 0, 0) in mine; comps = components(mine - {(0, 0, 0)})
        if cen:
            nb = [c for c in comps if any(q in c for q in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])]
            if nb: min(nb, key=min).add((0, 0, 0))                 # deterministic: the part with the least voxel
            else: comps.append({(0, 0, 0)})
        for c in comps: P.append((k, frozenset(c)))
    allv = [v for _, c in P for v in c]
    assert len(allv) == len(set(allv))                                    # no two pieces overlap
    return P

BC = {}
def blocked(p, q):
    """frozenset of direction indices along which piece p (moving) meets piece q"""
    key = (p, q)
    if key in BC: return BC[key]
    a = np.array(sorted(p)); b = np.array(sorted(q))
    D = np.unique((b[None, :, :] - a[:, None, :]).reshape(-1, 3), axis=0)
    out = set()
    for di, d in enumerate(DIRS):
        d = np.array(d); T = d != 0
        ok = np.all(D[:, ~T] == 0, axis=1)
        M = D[:, T] * d[T]
        ok &= (M.min(axis=1) >= 0) & (M.max(axis=1) - M.min(axis=1) <= 1)
        if ok.any(): out.add(di)
    BC[key] = frozenset(out); return BC[key]

def analyse(P):
    n = len(P); full = (1 << n) - 1
    blk = [[0] * n for _ in DIRS]                                         # blk[d][i] = mask of pieces blocking piece i along d
    for i in range(n):
        for j in range(n):
            if i != j:
                for di in blocked(P[i][1], P[j][1]): blk[di][i] |= 1 << j
    def movable(S, M):                                                    # direction index along which S leaves M \ S, or None
        R = M & ~S
        for di in range(len(DIRS)):
            if all(not (blk[di][i] & R) for i in range(n) if S >> i & 1): return di
        return None
    # sequential (greedy, complete for one-piece-at-a-time)
    M = full; order = []
    while M & (M - 1):
        for i in range(n):
            if M >> i & 1:
                di = movable(1 << i, M)
                if di is not None: order.append((i, di)); M &= ~(1 << i); break
        else: break
    if not (M & (M - 1)):
        last = [i for i in range(n) if M >> i & 1][0]
        return 'sequential', [(last, None)] + order[::-1]                 # assembly order: last removed goes in first
    memo = {}
    def two(M):
        if not (M & (M - 1)): return True
        if M in memo: return memo[M]
        low = M & -M; S = (M - 1) & M; res = False
        while S:
            if S & low and S != M:                                        # each split once (S holds the lowest piece)
                if (movable(S, M) is not None or movable(M & ~S, M) is not None) and two(S) and two(M & ~S): res = True; break
            S = (S - 1) & M
        memo[M] = res; return res
    return ('two-handed', None) if two(full) else ('impossible', None)

REG = {cut: [region(k, cut) for k in range(3)] for cut in ('octahedron', 'cube')}
schemes = [h + (c,) for h in itertools.product(OPTS, repeat=6) for c in (0, 1, 2, None)][::STRIDE]
res = []; t0 = time.time(); skipped = 0
for cut in ('octahedron', 'cube'):
    for si, sc in enumerate(schemes):
        P = pieces(sc, cut)
        if any(all(sum(1 for x in v if x) < 2 for v in c) for _, c in P): skipped += 1; continue   # a piece with no card body (lone centre or line voxels): a sliver, not a card piece
        kind, order = analyse(P)
        per = [sum(1 for k, _ in P if k == j) for j in range(3)]
        res.append({'cut': cut, 'half': list(sc[:6]), 'centre': None if sc[6] is None else CARD[sc[6]], 'pieces_per_card': per,
                    'outcome': 'POSSIBLE' if kind != 'impossible' else 'IMPOSSIBLE', 'search': kind,
                    'order': None if order is None else [[CARD[P[i][0]], sorted(P[i][1])[0], None if d is None else DIRS[d]] for i, d in order]})
        if si % 6250 == 0: print('PROGRESS %.3f %s %d/%d (%.0f s, cache %d)' % ((si / len(schemes) + (cut == 'cube')) / 2, cut, si, len(schemes), time.time() - t0, len(BC)), flush=True)
json.dump({'N': N, 'half_order': ['+x', '-x', '+y', '-y', '+z', '-z'], 'sharers': {'x': 'A=Y B=Z', 'y': 'A=X B=Z', 'z': 'A=X B=Y'}, 'results': res}, open(OUT, 'w'))
# summary by pieces per card (sorted) and outcome
from collections import Counter
for cut in ('octahedron', 'cube'):
    C = Counter((tuple(sorted(r['pieces_per_card'])), r['outcome']) for r in res if r['cut'] == cut)
    print(cut, 'schemes', sum(C.values()))
    for sig in sorted({s for s, _ in C}):
        print('  pieces per card %s: possible %d, impossible %d' % (sig, C[(sig, 'POSSIBLE')], C[(sig, 'IMPOSSIBLE')]))
    print('  two-handed only (sequential fails, two-handed works): %d' % sum(1 for r in res if r['cut'] == cut and r['search'] == 'two-handed'))
BY = {cut: {(tuple(r['half']), r['centre']): (r['outcome'], r['pieces_per_card']) for r in res if r['cut'] == cut} for cut in ('octahedron', 'cube')}
same = BY['octahedron'] == BY['cube']
whole = [r for r in res if r['pieces_per_card'] == [1, 1, 1]]
ok = len(whole) > 0 and all(r['outcome'] == 'IMPOSSIBLE' for r in whole)
dif = [k for k in BY['octahedron'] if BY['cube'].get(k) != BY['octahedron'][k]]
for k in dif[:12]: print('  differs', k, BY['octahedron'][k], BY['cube'].get(k))
print('skipped (sliver pieces) %d; same outcome for both cuts, scheme by scheme: %s; whole cards: %d schemes, all impossible: %s' % (skipped, same, len(whole), ok))
print('time %.0f s' % (time.time() - t0)); print('FINAL ok' if ok and same else 'FINAL FAIL')
