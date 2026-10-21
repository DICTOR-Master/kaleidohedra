# DICTO 2026-10-21 (neck version): DICTO's pieces are joined by BOTTLE-NECK bridges, three parallel rings, the outer two clicked into
# the two pentagons, the middle one holding them 'one narrow ring apart' (gap G, in ring sides) and free to turn about the neck.
# Earlier: the B1NR + icosidodecahedron network, rigid version ("the B1NRs act as cube and octahedral packing bridges" = six
# ways out round each ID; "from one angle the IDs are in triangular formation, from another in square formation"). Float fit.
# Growth rule: every B1NR shares all 6 of its pentagons with IDs; every ID shares 3 OPPOSITE PAIRS of its pentagons with B1NRs (its
# existing links, plus the opposite pairs whose both ends take a B1NR without clashing). New pieces that land on an existing piece
# are merged (the network closes up there). Reports clashes, merges, choices, and the lattice the ID centres form.
import os, sys, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'b1nr_id.py')).read(); exec(src[:src.index("np.save(os.path.join(HERE, 'b1nr-regpent.npy')")])
RMAX = float(sys.argv[1]) if len(sys.argv) > 1 else 7.0
G = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2
TURNS = np.radians(np.arange(0, 360, 15))
IPF = [f for f in IF if len(f) == 5]
P = [('B', B.copy())] + [('I', W) for W in IDs]              # pieces: (kind, corners)
cen = lambda k: P[k][1].mean(0)
def pent_centres(k):
    kind, W = P[k]; F = pents if kind == 'B' else IPF; return [W[f].mean(0) for f in F]
def samples(W, n=1500):
    rng = np.random.default_rng(1); S = W[rng.integers(0, len(W), (n, 4))]; w = rng.dirichlet(np.ones(4), n); return (S * w[:, :, None]).sum(1)
def clashes(W, skip=()):
    S = samples(W); D = Delaunay(W); c = W.mean(0)
    for k, (kind, A) in enumerate(P):
        if k in skip or np.linalg.norm(A.mean(0) - c) > 5: continue
        if (Delaunay(A).find_simplex(S) >= 0).mean() > .005 or (D.find_simplex(samples(A)) >= 0).mean() > .005: return k
    return None
def same(W, kind):                                           # an existing piece with the same corners?
    for k, (kd, A) in enumerate(P):
        if kd == kind and np.linalg.norm(A.mean(0) - W.mean(0)) < .3:
            d = np.sqrt((np.min(np.linalg.norm(W[:, None] - A[None], axis=2), axis=1) ** 2).mean()); return k, d
    return None, None
def occupied(Q, kind_other):                                 # is a pentagon (centre Q) already shared with a piece of the other kind?
    for k, (kd, A) in enumerate(P):
        if kd == kind_other and np.linalg.norm(A.mean(0) - Q) < 4:
            if min(np.linalg.norm(c - Q) for c in pent_centres(k)) < .12 + G: return k
    return None
def axis_turn(W, c, n, a):                                   # turn corners W about the axis through c along n
    n = n / np.linalg.norm(n); K_ = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]]); R = np.eye(3) + np.sin(a) * K_ + (1 - np.cos(a)) * K_ @ K_
    return (W - c) @ R.T + c
def unit_n(Q, out):
    n = np.linalg.svd(Q - Q.mean(0))[2][-1]; return n if n @ out > 0 else -n
def place(base, F, Q, out, kind):                            # base piece with its pentagon F set across a neck from pentagon Q
    n = unit_n(Q, out); c = Q.mean(0) + G * n; best = None
    for rev in (1, -1):
        order = [F[(rev * j) % 5] for j in range(5)]; R, t = kabsch(base[order], Q); W0_ = base @ R.T + t
        if (W0_.mean(0) - Q.mean(0)) @ n <= 0: W0_ = 2 * Q.mean(0) - W0_                       # make sure it sits outside
        W0_ = W0_ + G * n
        for a in TURNS:
            W = axis_turn(W0_, c, n, a); cl = clashes(W); key = (cl is not None, a)
            if best is None or key < best[0]: best = (key, W)
    return best[1], best[0][0]
def fit_B(Q, out): return place(B, pents[0], Q, out, 'B')
def fit_I(Q, out): return place(I, IP, Q, out, 'I')[0]
def closes(Q, out, kind_other):                              # an existing piece already across a neck from pentagon Q?
    n = unit_n(Q, out); target = Q.mean(0) + G * n
    for k, (kd, A) in enumerate(P):
        if kd != kind_other or np.linalg.norm(A.mean(0) - target) > 4: continue
        F = pents if kd == 'B' else IPF
        for f in F:
            m = np.linalg.norm(A[f].mean(0) - target)
            if m < .35:
                ang = np.degrees(np.arccos(min(1, abs(unit_n(A[f], A[f].mean(0) - A.mean(0)) @ n)))); log['close'].append((round(float(m), 3), round(float(ang), 1))); return k
    return None
log = {'merge': [], 'clash': [], 'choice': [], 'close': []}
def add(kind, W):
    k, d = same(W, kind)
    if k is not None: log['merge'].append(round(float(d), 3)); return k
    c = clashes(W)
    if c is not None: log['clash'].append((kind, P[c][0], round(float(np.linalg.norm(W.mean(0))), 2))); return None
    P.append((kind, W)); return len(P) - 1
done = set(); queue = list(range(len(P)))
while queue:
    k = queue.pop(0)
    if k in done or np.linalg.norm(cen(k)) > RMAX: continue
    done.add(k); kind, W = P[k]; c = cen(k)
    if kind == 'B':
        for f in pents:
            Q = W[f]; out = Q.mean(0) - c
            if occupied(Q.mean(0) + G * unit_n(Q, out), 'I') is None and closes(Q, out, 'I') is None:
                n = add('I', fit_I(Q, out)); queue += [n] if n is not None else []
    else:
        PC = [W[f].mean(0) for f in IPF]; opp = {i: int(np.argmin([np.linalg.norm(PC[j] + PC[i] - 2 * c) for j in range(12)])) for i in range(12)}
        axes = sorted({tuple(sorted((i, opp[i]))) for i in range(12)}); linked = [a for a in axes if any(occupied(PC[i], 'B') is not None for i in a)]
        cand = []
        for a in axes:
            if a in linked: continue
            fits = [fit_B(W[IPF[i]], PC[i] - c) for i in a]
            if all(not cl for _, cl in fits): cand.append((a, fits))
        need = 3 - len(linked); log['choice'].append((len(linked), len(cand)))
        for a, fits in cand[:max(need, 0)]:
            for Bn, _ in fits:
                n = add('B', Bn); queue += [n] if n is not None else []
        for a in linked:                                       # the other end of each linked axis
            for i in a:
                if occupied(PC[i], 'B') is None:
                    Bn, cl = fit_B(W[IPF[i]], PC[i] - c); n = add('B', Bn); queue += [n] if n is not None else []
nB = sum(1 for kd, _ in P if kd == 'B'); nI = len(P) - nB
print(f'grown to radius {RMAX}: {nB} B1NRs, {nI} IDs; merges {len(log["merge"])} (corner rms up to {max(log["merge"] or [0])}), clashes {len(log["clash"])}')
print('clashes (new kind, hit kind, radius):', log['clash'][:12])
from collections import Counter
print('closures (neck offset, angle deg):', log['close'][:10])
print('ID choices (linked axes, free opposite pairs):', Counter(log['choice']))
C = np.array([cen(k) for k in range(len(P)) if P[k][0] == 'I']); C0 = C[np.argmin(np.linalg.norm(C, axis=1))]
D = sorted({tuple(np.round(c - C0, 2)) for c in C if 0 < np.linalg.norm(c - C0) < 4.2}, key=lambda v: np.linalg.norm(v))
print('ID neighbours of the innermost ID (vector, length):', [(v, round(float(np.linalg.norm(v)), 3)) for v in D])
np.save(os.path.join(HERE, f'network-neck-{G}.npy'), np.array([(0 if kd == 'B' else 1, W) for kd, W in P], dtype=object), allow_pickle=True)
