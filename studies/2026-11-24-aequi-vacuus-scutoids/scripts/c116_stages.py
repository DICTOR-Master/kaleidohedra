"""C116 -> Minana #377 in stages (26 Nov 2026; DICTO: "a new construction with an intermediate solid to divide the changes into two or
three stages"). With Claude (Anthropic).
Both are simple polyhedra (every corner on 3 faces) with 60 faces, 116 corners, 174 edges, so their duals are triangulations on the
same 60 face labels (C116's faces; Minana's faces carried over by the best T_h-equivariant pairing, data/c116/pairing.json). An edge
flip of the dual (two faces stop touching, two others start: one Y vertex in a Scutoid-Frustum layer) turns one into the other.
Rounds: each round flips a T_h-closed set of PAIRWISE INDEPENDENT edges (no two share a triangle), each flip making a neighbour pair of
Minana; the solid after each round is an intermediate stage. Greedy, largest orbit sets first. Reports rounds and flips per round.
If no improving flip exists before the target is reached, it says so (a non-improving flip would be needed)."""
import os, json, itertools
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json')))
faces, gface = d['faces'], d['gface']; sig = {int(k): v for k, v in (json.load(open(os.path.join(HERE, '../data/c116/' + os.environ['PAIRFILE']))) if os.environ.get('PAIRFILE') else d['assign']).items()}; inv = {v: k for k, v in sig.items()}
mf = d['minana_faces']
def tris_of(face_lists):
    inc = {}
    for k, f in enumerate(face_lists):
        for v in f: inc.setdefault(v, []).append(k)
    assert all(len(x) == 3 for x in inc.values()), Counter(len(x) for x in inc.values())
    return {frozenset(x) for x in inc.values()}
T0 = tris_of(faces)                                          # C116's corners = triangles of its dual
T1 = {frozenset(inv[k] for k in t) for t in tris_of(mf)}      # Minana's corners, in C116 face labels
E = lambda T: {frozenset(p) for t in T for p in itertools.combinations(t, 2)}
target = E(T1); print('triangles', len(T0), len(T1), 'edges', len(E(T0)), len(target), 'shared', len(E(T0) & target), flush=True)
def gimg(g, s): return frozenset(gface[g][x] for x in s)
# beam search over T_h-closed sets of independent flips (one orbit per move), allowing moves that do not yet improve the score
def flip1(T, x):
    ts = [t for t in T if x <= t]
    if len(ts) != 2: return None
    c, dd = [next(iter(t - x)) for t in ts]
    if any(frozenset((c, dd)) <= t2 for t2 in T for _ in [0]) and frozenset((c, dd)) in E(T): return None
    a, b = tuple(x); T = set(T); T -= set(ts); T |= {frozenset((a, c, dd)), frozenset((b, c, dd))}
    return frozenset(T)
def symmetric(T): return all(frozenset(gimg(g, t) for t in T) == T for g in range(24))
def moves(T):
    """one T_h orbit of edges flipped; independent flips side by side, touching ones one after another (in every order that works);
    kept only if the result is T_h-symmetric"""
    cur = E(T); out, seen = [], set()
    pool = cur if os.environ.get('ANY_EDGE') else cur - target
    for e in pool:
        if e in seen: continue
        o = sorted({gimg(g, e) for g in range(24)}, key=sorted); seen |= set(o)
        for start in range(min(len(o), 6)):
            T2 = T; ok = True
            for x in o[start:] + o[:start]:
                if x not in E(T2): ok = False; break
                T3 = flip1(T2, x)
                if T3 is None: ok = False; break
                T2 = T3
            if ok and symmetric(T2): out.append((len(o), T2)); break
    return out
def apply(T, mv): return mv[1]
score = lambda T: len(E(T) & target)
BEAM, DEPTH = int(os.environ.get('BEAM', 300)), int(os.environ.get('DEPTH', 30))
beam = [(score(T0), frozenset(T0), [])]; best = beam[0]; visited = {frozenset(T0)}
for depth in range(DEPTH):
    nxt = []
    for sc, T, path in beam:
        for mv in moves(T):
            T2 = apply(T, mv)
            if T2 in visited: continue
            visited.add(T2); nxt.append((score(T2), T2, path + [mv[0]]))
    if not nxt: break
    nxt.sort(key=lambda x: -x[0]); beam = nxt[:BEAM]
    if beam[0][0] > best[0]: best = beam[0]
    print(f'depth {depth + 1}: best score {beam[0][0]} / 174 (overall {best[0]}), states {len(nxt)}', flush=True)
    print(f'PROGRESS {(depth + 1) / DEPTH:.3f}', flush=True)
    if best[0] == 174: break
sc, T, path = best
print('best path: moves (flips per move)', path, 'total flips', sum(path), 'score', sc, '/ 174', flush=True)
# replay to store every intermediate
Tc = frozenset(T0)
done = sc == 174
json.dump(dict(path=path, final=[sorted(t) for t in T]), open(os.path.join(HERE, '../data/c116/flip_path_' + os.environ.get('PAIRFILE', 'pairing.json')), 'w'))
print('reached Minana:', done, flush=True)
print('FINAL ok' if done else 'FINAL FAIL (beam search did not reach Minana)')
