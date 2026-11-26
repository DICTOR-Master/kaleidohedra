"""C116 -> Minana #377 with divided faces (26 Nov 2026; DICTO: "option 2 divided faces at the long changes"). With Claude (Anthropic).
Dual picture: faces = vertices of a triangulation, corners = triangles. Moves, each applied to a whole T_h orbit at once, the result
required to be T_h-symmetric (a floor):
  swap   an edge (dual edge flip: two faces stop touching, two start);
  divide a face v into v and a copy v' (dual vertex split along two of v's neighbours a, b: v keeps one arc of neighbours, v' the
         other, v and v' touch, both touch a and b): the piece branches;
  rejoin a copy v' into v (dual edge contraction; allowed when v and v' share exactly two neighbours).
Score of a floor = Minana neighbour pairs present (a copy counts as its face) - 2 x copies; goal: no copies and all 174 pairs.
Beam search from floor 1 of the local pairing (132/174). Prints the best path as a list of moves."""
import os, json, itertools
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json')))
faces, gface = d['faces'], d['gface']; mf = d['minana_faces']
sig = {int(k): v for k, v in json.load(open(os.path.join(HERE, '../data/c116/pairing_local.json'))).items()}; inv = {v: k for k, v in sig.items()}
def tris_of(fl):
    inc = {}
    for k, f in enumerate(fl):
        for v in f: inc.setdefault(v, []).append(k)
    assert all(len(x) == 3 for x in inc.values()); return {frozenset(x) for x in inc.values()}
T0 = frozenset(tris_of(faces)); T1 = {frozenset(inv[k] for k in t) for t in tris_of(mf)}
def base(x): return x if isinstance(x, int) else base(x[1])
def edges(T): return {frozenset(p) for t in T for p in itertools.combinations(t, 2)}
target = edges(T1)
def g_on(g, x): return gface[g][x] if isinstance(x, int) else ('s', g_on(g, x[1]), frozenset(g_on(g, y) for y in x[2]))
def gT(g, T): return frozenset(frozenset(g_on(g, x) for x in t) for t in T)
def symmetric(T): return all(gT(g, T) == T for g in range(1, 24))
def verts(T): return {x for t in T for x in t}
PEN = float(os.environ.get('PEN', 2))   # cost of one divided face in the beam ranking (26 Nov: 2 dropped the 168-pair branch)
def score(T):
    be = {frozenset(map(base, e)) for e in edges(T) if base(min(e, key=str)) != base(max(e, key=str))}
    ncopy = sum(1 for v in verts(T) if not isinstance(v, int))
    return len(be & target) - PEN * ncopy, ncopy
def link(T, v):   # neighbours of v in cyclic order
    ts = [t for t in T if v in t]; nb = {}
    for t in ts:
        a, b = [x for x in t if x != v]; nb.setdefault(a, []).append(b); nb.setdefault(b, []).append(a)
    start = next(iter(nb)); cyc = [start]; prev = None
    while True:
        nx = [y for y in nb[cyc[-1]] if y != prev]
        if not nx: return None
        nxt = nx[0] if len(nx) == 1 or nx[0] != cyc[-1] else nx[1]
        if nxt == start: return cyc
        prev = cyc[-1]; cyc.append(nxt)
        if len(cyc) > len(nb): return None
def flip(T, e):
    ts = [t for t in T if e <= t]
    if len(ts) != 2: return None
    c, dd = [next(iter(t - e)) for t in ts]
    if frozenset((c, dd)) in edges(T): return None
    a, b = tuple(e); return (T - set(ts)) | {frozenset((a, c, dd)), frozenset((b, c, dd))}
def split(T, v, i, j):
    cyc = link(T, v)
    if cyc is None: return None
    k = len(cyc); a, b = cyc[i], cyc[j]
    arc2 = [cyc[(i + t) % k] for t in range((j - i) % k + 1)]          # a .. b, goes to the copy
    inner = set(arc2[1:-1]); w = ('s', v, frozenset(arc2))
    if not inner: return None
    T2 = set()
    for t in T:
        if v in t and (t - {v}) <= set(arc2) and (t - {v}) & inner: T2.add(frozenset(x if x != v else w for x in t))
        else: T2.add(t)
    T2 |= {frozenset((v, w, a)), frozenset((v, w, b))}
    return frozenset(T2)
def rejoin(T, w):
    v = w[1]; ts = [t for t in T if v in t and w in t]
    if len(ts) != 2: return None
    nv = {x for t in T if v in t for x in t} - {v}; nw = {x for t in T if w in t for x in t} - {w}
    if len(nv & nw) != 2: return None
    return frozenset(frozenset(x if x != w else v for x in t) for t in T if not (v in t and w in t))
def orbit_apply(T, op, item):
    imgs = []
    for g in range(24):
        im = (g_on(g, item[0]),) + tuple(item[1:]) if op != 'flip' else frozenset(g_on(g, x) for x in item[0])
        if im not in imgs: imgs.append(im)
    T2 = set(T)
    for im in imgs:
        if op == 'flip':
            if not im <= {x for t in T2 for x in t} or im not in edges(T2): return None
            r = flip(frozenset(T2), im)
        elif op == 'rejoin': r = rejoin(frozenset(T2), im[0])
        if r is None: return None
        T2 = set(r)
    T2 = frozenset(T2)
    return T2 if symmetric(T2) else None
def moves(T):
    out = []; seen = set()
    for e in edges(T):
        k = frozenset(frozenset(g_on(g, x) for x in e) for g in range(24))
        if k in seen: continue
        seen.add(k); r = orbit_apply(T, 'flip', (e,))
        if r: out.append(('swap', r))
    for w in verts(T):
        if not isinstance(w, int):
            r = orbit_apply(T, 'rejoin', (w,))
            if r: out.append(('rejoin', r))
    vs, seenv = sorted((v for v in verts(T) if isinstance(v, int)), key=str), set()
    for v in vs:
        if v in seenv: continue
        orb = {g_on(g, v) for g in range(24)}; seenv |= orb
        cyc = link(T, v)
        if cyc is None: continue
        k = len(cyc)
        for i in range(k):
            for j in range(k):
                if (j - i) % k < 2 or (i - j) % k < 2: continue
                T2 = set(T); ok = True
                for g in range(24):   # split every image, using the image of the same arc
                    pass
                # apply the same split to every image of v: carry the arc by g
                arc = frozenset(cyc[(i + t) % k] for t in range((j - i) % k + 1))
                T2 = frozenset(T); done = set()
                for g in range(24):
                    vg = g_on(g, v); ag = frozenset(g_on(g, x) for x in arc)
                    if (vg, ag) in done: continue
                    done.add((vg, ag)); cg = link(T2, vg)
                    if cg is None: ok = False; break
                    kk = len(cg); idx = [p for p in range(kk) if cg[p] in ag]
                    ends = [p for p in idx if cg[(p - 1) % kk] not in ag or cg[(p + 1) % kk] not in ag]
                    if len(ends) != 2 or len(idx) != len(ag): ok = False; break
                    p0 = next(p for p in ends if cg[(p - 1) % kk] not in ag); p1 = next(p for p in ends if p != p0)
                    r = split(T2, vg, p0, p1)
                    if r is None: ok = False; break
                    T2 = r
                if ok and symmetric(T2): out.append(('divide', T2))
    return out
# floor 1 (from the local pairing's first symmetric round) is found by the same search
BEAM, DEPTH = int(os.environ.get('BEAM', 200)), int(os.environ.get('DEPTH', 16))
beam = [(score(T0), T0, [])]; best = beam[0]; visited = {T0}
for depth in range(DEPTH):
    nxt = []
    for sc, T, path in beam:
        for kind, T2 in moves(T):
            if T2 in visited: continue
            visited.add(T2); nxt.append((score(T2), T2, path + [kind]))
    if not nxt: break
    nxt.sort(key=lambda x: (-x[0][0], x[0][1])); beam = nxt[:BEAM]
    done = [x for x in nxt if x[0][1] == 0 and x[0][0] == 174]
    if beam[0][0] > best[0]: best = beam[0]
    print(f'depth {depth + 1}: best (score, copies) {beam[0][0]}, path {beam[0][2]}, states {len(nxt)}', flush=True)
    print(f'PROGRESS {(depth + 1) / DEPTH:.3f}', flush=True)
    if done: best = done[0]; break
sc, T, path = best
ok = sc[1] == 0 and sc[0] == 174
print('best path:', path, 'score', sc, '| reached Minana with no divided faces left:', ok, flush=True)
json.dump(dict(path=path, score=list(sc)), open(os.path.join(HERE, '../data/c116/divided_path.json'), 'w'))
print('FINAL ok' if ok else 'FINAL FAIL (no path found within the search bounds)')
