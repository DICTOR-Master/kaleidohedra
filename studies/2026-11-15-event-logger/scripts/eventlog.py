"""Event logger for time-changing cell tilings (One tissue, three scales, Step 0; DICTO 15 Nov 2026: "I want to start on the new
scutoid Earth, Sun and cosmos work ASAP"). One program for all three projects (plates, convection cells, voids).

TILING FORMAT (one JSON object per line, a "frame"; a file of frames in time order is a "tiling sequence"):
  {"t": time, "dim": 2 or 3, "surface": "sphere" | "patch" | "S3" | "space",
   "cells": [label, ...],                      # labels persist through time (same label = same cell)
   "boundaries": [[a, b], ...],                # dim 2: one entry per boundary SEGMENT (a pair may share several segments);
                                               # dim 3: one entry per contact face between cells a and b
   "junctions": [[a, b, c], ...],              # optional, dim 2: the cells meeting at each junction (corner of the map)
   "edges": [[a, b, c], ...], "corners": [[a, b, c, d], ...],   # optional, dim 3 (cells round each edge / at each corner)
   "loops": n,                                 # optional, dim 2: boundaries that are closed loops with no junction on them
   "parents": {new: {old: share}}, "heirs": {old: {new: share}}}  # optional lineage: share of the NEW cell's area that came
                                               # from each old cell / share of the OLD cell's area that went to each new cell
Labels are strings in the file (JSON keys); any hashable label works in memory.

EVENTS between consecutive frames (plain terms first; #104 names in brackets):
  dim 2: swap (two cells stop touching, two others start: the 2-2 move), birth (a three-sided cell appears at a junction: 1-3),
         death (a three-sided cell vanishes, its three neighbours meet at a new junction: 3-1), split (one cell divides in two),
         merge (two cells join), relabel (a cell's label changes, nothing else), clump (any other local change: more than one
         contact at one place and time; logged with its pattern, the rosette events of #104 Lemma 5).
  dim 3: contact gained, contact lost (separate events, Theorem 1' of #104), birth (1-4), death (4-1), split, merge, relabel, clump.
"One place" = the changed items' cells form a clique in the union of the two neighbour graphs (all mutually touching before or
after). Split vs birth and merge vs death are told apart by lineage when given (one dominant parent / heir = split / merge);
without lineage a three-sided newcomer at a former junction is a birth, a larger newcomer touching only one old cell's
neighbours is a split.

CHECKS (built in): Euler's formula per frame (sphere: junctions - boundaries + cells = 2 + loops correction; S3: corners - edges +
contacts - cells = 0); all-junctions-triple formulas on a sphere: junctions = 2(cells - 2), boundaries = 3(cells - 2);
balance per step: births + splits - deaths - merges + (clumps' own net) = change in the number of cells (swaps, contact changes,
relabels are free). The balance is recomputed from the event TYPES, so a mislabelled or missing event is caught."""
import json, itertools
from collections import Counter, defaultdict

NET = {'swap': 0, 'birth': 1, 'death': -1, 'split': 1, 'merge': -1, 'relabel': 0, 'contact gained': 0, 'contact lost': 0}


class Tiling:
    def __init__(self, cells, boundaries, junctions=None, dim=2, surface='sphere', t=None, edges=None, corners=None, loops=0,
                 parents=None, heirs=None):
        self.t, self.dim, self.surface, self.loops = t, dim, surface, loops
        self.cells = frozenset(cells)
        self.segments = [tuple(sorted(p)) for p in boundaries]
        self.pairs = frozenset(self.segments)
        self.junctions = None if junctions is None else [tuple(sorted(j)) for j in junctions]
        self.edges = None if edges is None else [tuple(sorted(e)) for e in edges]
        self.corners = None if corners is None else [tuple(sorted(c)) for c in corners]
        self.parents, self.heirs = parents or {}, heirs or {}
        self.nb = defaultdict(set)
        for a, b in self.pairs: self.nb[a].add(b); self.nb[b].add(a)

    def to_json(self):
        d = dict(t=self.t, dim=self.dim, surface=self.surface, cells=sorted(map(str, self.cells)),
                 boundaries=[[str(a), str(b)] for a, b in self.segments])
        if self.junctions is not None: d['junctions'] = [list(map(str, j)) for j in self.junctions]
        if self.edges is not None: d['edges'] = [list(map(str, e)) for e in self.edges]
        if self.corners is not None: d['corners'] = [list(map(str, c)) for c in self.corners]
        if self.loops: d['loops'] = self.loops
        if self.parents: d['parents'] = {str(k): {str(a): s for a, s in v.items()} for k, v in self.parents.items()}
        if self.heirs: d['heirs'] = {str(k): {str(a): s for a, s in v.items()} for k, v in self.heirs.items()}
        return json.dumps(d)

    @staticmethod
    def from_json(line):
        d = json.loads(line)
        return Tiling(d['cells'], d['boundaries'], d.get('junctions'), d.get('dim', 2), d.get('surface', 'sphere'), d.get('t'),
                      d.get('edges'), d.get('corners'), d.get('loops', 0), d.get('parents'), d.get('heirs'))


def read_frames(path):
    with open(path) as f: return [Tiling.from_json(l) for l in f if l.strip()]


def check_tiling(T):
    """Per-frame checks. Returns dict; key 'ok' is False when a check that applies fails."""
    r = dict(t=T.t, cells=len(T.cells), boundaries=len(T.segments), pairs=len(T.pairs), problems=[])
    for a, b in T.pairs:
        if a == b: r['problems'].append(f'self-contact {a}')
        if a not in T.cells or b not in T.cells: r['problems'].append(f'contact {a}-{b} names a missing cell')
    if T.dim == 2 and T.junctions is not None:
        J = len(T.junctions); r['junctions'] = J
        deg = Counter(len(j) for j in T.junctions); r['junction_degrees'] = dict(deg)
        for j in T.junctions:
            for a, b in itertools.combinations(j, 2):
                if (a, b) not in T.pairs and len(j) == 3: r['problems'].append(f'junction {j}: {a},{b} do not touch')
        if T.surface == 'sphere':
            # V - E + F = 2 for a connected map of disc cells; a junction-free loop boundary adds a face-and-edge without a vertex:
            # count each loop as one extra vertex (a loop is a circle with one 2-valent corner) so the formula still reads V-E+F=2
            chi = (J + T.loops) - len(T.segments) + len(T.cells)
            r['euler'] = chi; r['euler_ok'] = (chi == 2)
            if not r['euler_ok']: r['problems'].append(f'Euler V-E+F = {chi} != 2')
            if set(deg) <= {3} and not T.loops:
                n = len(T.cells)
                r['triple_formulas_ok'] = (J == 2 * (n - 2) and len(T.segments) == 3 * (n - 2))
                if not r['triple_formulas_ok']: r['problems'].append(f'triple-junction formulas: J={J} vs {2*(n-2)}, E={len(T.segments)} vs {3*(n-2)}')
            else:
                r['triple_formulas_ok'] = None          # not all junctions triple: the formulas do not apply
    if T.dim == 3 and T.edges is not None and T.corners is not None and T.surface == 'S3':
        chi = len(T.corners) - len(T.edges) + len(T.segments) - len(T.cells)
        r['euler'] = chi; r['euler_ok'] = (chi == 0)
        if chi != 0: r['problems'].append(f'Euler V-E+F-C = {chi} != 0')
    r['ok'] = not r['problems']
    return r


def _clusters(A, B, born, died, lost, gained):
    """Group the changed items into local events: items are linked when their cells all touch one another in A or B."""
    items = [('b', x) for x in born] + [('d', x) for x in died] + [('l', p) for p in lost] + [('g', p) for p in gained]
    cellsof = lambda it: {it[1]} if it[0] in 'bd' else set(it[1])
    touch = lambda u, v: u == v or v in A.nb[u] or v in B.nb[u]
    par = list(range(len(items)))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    bycell = defaultdict(list)
    for i, it in enumerate(items):
        for c in cellsof(it): bycell[c].append(i)
        if it[0] == 'b': [bycell[c].append(i) for c in B.nb[it[1]]]
        if it[0] == 'd': [bycell[c].append(i) for c in A.nb[it[1]]]
        if it[0] == 'l': [bycell[c].append(i) for c in A.nb[it[1][0]] & A.nb[it[1][1]]]    # a lost contact's quad corners
        if it[0] == 'g': [bycell[c].append(i) for c in B.nb[it[1][0]] & B.nb[it[1][1]]]
    for c, idx in bycell.items():
        for i, j in itertools.combinations(sorted(set(idx)), 2):
            if find(i) == find(j): continue
            U = cellsof(items[i]) | cellsof(items[j])
            if all(touch(u, v) for u, v in itertools.combinations(U, 2)): par[find(i)] = find(j)
    # lineage and relabel links: a died and a born cell are one event if lineage joins them or their neighbours are identical
    for i, x in enumerate(items):
        for j, w in enumerate(items):
            if x[0] == 'd' and w[0] == 'b':
                lin = B.parents.get(w[1], {}).get(x[1], 0) > 0 or A.heirs.get(x[1], {}).get(w[1], 0) > 0
                same = (A.nb[x[1]] - died) == (B.nb[w[1]] - born) and A.nb[x[1]]
                if lin or same: par[find(i)] = find(j)
    groups = defaultdict(list)
    for i, it in enumerate(items): groups[find(i)].append(it)
    return list(groups.values())


def _dominant(share, theta):
    if not share: return None
    k, v = max(share.items(), key=lambda kv: kv[1])
    return k if v >= theta else None


def classify(A, B, theta=0.9):
    """Events between frames A and B (B later). Each event: dict(type, cells, pattern, net)."""
    born, died = B.cells - A.cells, A.cells - B.cells
    kept = A.cells & B.cells
    lost = {p for p in A.pairs - B.pairs if p[0] in kept and p[1] in kept}
    gained = {p for p in B.pairs - A.pairs if p[0] in kept and p[1] in kept}
    events = []
    for g in _clusters(A, B, born, died, lost, gained):
        kinds = Counter(k for k, _ in g)
        bs = [x for k, x in g if k == 'b']; ds = [x for k, x in g if k == 'd']
        ls = [p for k, p in g if k == 'l']; gs = [p for k, p in g if k == 'g']
        cells = sorted({x for k, x in g if k in 'bd'} | {c for k, p in g if k in 'lg' for c in p}, key=str)
        pat = f'born {len(bs)} died {len(ds)} lost {len(ls)} gained {len(gs)}'
        typ = None
        if A.dim == 2:
            if kinds == Counter(l=1, g=1):
                (a, b), (c, d) = ls[0], gs[0]
                if {c, d} <= A.nb[a] & A.nb[b] and {a, b} <= B.nb[c] & B.nb[d]: typ = 'swap'
            elif len(bs) == 1 and not ds and not gs:
                x = bs[0]; N = B.nb[x]; par = _dominant(B.parents.get(x, {}), theta)
                if par is not None and par in kept and (not ls or all(par in p for p in ls)): typ = 'split'
                elif not ls and len(N) == 3 and all(q in A.nb[p] for p, q in itertools.combinations(N, 2)) and \
                        (A.junctions is None or tuple(sorted(N)) in set(A.junctions)) and (par is None or not B.parents.get(x)):
                    typ = 'birth'
                elif not B.parents.get(x) and any(Y in kept and N - {Y} <= A.nb[Y] and all(Y in p for p in ls) for Y in N) and (len(N) != 3 or ls):
                    typ = 'split'
            elif len(ds) == 1 and not bs and not ls:
                x = ds[0]; N = A.nb[x]; heir = _dominant(A.heirs.get(x, {}), theta)
                if heir is not None and heir in kept and (not gs or all(heir in p for p in gs)): typ = 'merge'
                elif not gs and len(N) == 3 and all(q in B.nb[p] for p, q in itertools.combinations(N, 2)) and \
                        (B.junctions is None or tuple(sorted(N)) in set(B.junctions)) and not A.heirs.get(x):
                    typ = 'death'
                elif not A.heirs.get(x) and any(Y in kept and N - {Y} <= B.nb[Y] and all(Y in p for p in gs) for Y in N) and (len(N) != 3 or gs):
                    typ = 'merge'
            elif len(bs) == 2 and len(ds) == 1 and not ls and not gs:     # a cell splits and both parts get new labels
                y = ds[0]; x, w = bs
                lin = all(_dominant(B.parents.get(z, {}), theta) == y for z in bs) if B.parents.get(x) or B.parents.get(w) else \
                    (w in B.nb[x] and (B.nb[x] | B.nb[w]) - {x, w} <= A.nb[y])
                if lin: typ = 'split'
            elif len(ds) == 2 and len(bs) == 1 and not ls and not gs:     # two cells merge into a newly labelled one
                x = bs[0]; y, z = ds
                lin = all(_dominant(A.heirs.get(q, {}), theta) == x for q in ds) if A.heirs.get(y) or A.heirs.get(z) else \
                    (z in A.nb[y] and (A.nb[y] | A.nb[z]) - {y, z} <= B.nb[x])
                if lin: typ = 'merge'
            if typ is None and len(bs) == 1 and len(ds) == 1 and not ls and not gs: typ = 'relabel'
        else:
            if kinds == Counter(l=1): typ = 'contact lost'
            elif kinds == Counter(g=1): typ = 'contact gained'
            elif kinds == Counter(b=1):
                x = bs[0]; N = B.nb[x]; par = _dominant(B.parents.get(x, {}), theta)
                if par is not None and par in kept: typ = 'split'
                elif len(N) == 4 and all(q in A.nb[p] for p, q in itertools.combinations(N, 2)) and not B.parents.get(x) and \
                        (A.corners is None or tuple(sorted(N)) in set(A.corners)): typ = 'birth'
            elif kinds == Counter(d=1):
                x = ds[0]; N = A.nb[x]; heir = _dominant(A.heirs.get(x, {}), theta)
                if heir is not None and heir in kept: typ = 'merge'
                elif len(N) == 4 and all(q in B.nb[p] for p, q in itertools.combinations(N, 2)) and not A.heirs.get(x) and \
                        (B.corners is None or tuple(sorted(N)) in set(B.corners)): typ = 'death'
            elif kinds == Counter(b=1, d=1): typ = 'relabel'
        net = len(bs) - len(ds)
        if typ is not None and NET[typ] != net: typ = None              # a named event must carry its own cell change
        events.append(dict(type=typ or 'clump', cells=[str(c) for c in cells], pattern=pat, net=net))
    return events


def balance(A, B, events):
    """Births + splits - deaths - merges + clumps' net = change in cells; recomputed from event types (NET table)."""
    s = sum(NET[e['type']] if e['type'] in NET else e['net'] for e in events)
    return s == len(B.cells) - len(A.cells), s, len(B.cells) - len(A.cells)


def run(frames, theta=0.9):
    """Log a whole sequence. Returns (rows, summary). rows: one per event with t0, t1."""
    rows, checks, bad_bal = [], [check_tiling(F) for F in frames], []
    for A, B in zip(frames, frames[1:]):
        ev = classify(A, B, theta)
        ok, s, d = balance(A, B, ev)
        if not ok: bad_bal.append((A.t, B.t, s, d))
        for e in ev: rows.append(dict(t0=A.t, t1=B.t, **e))
    counts = Counter(r['type'] for r in rows)
    clumps = Counter(r['pattern'] for r in rows if r['type'] == 'clump')
    summary = dict(frames=len(frames), counts=dict(counts), clump_patterns=dict(clumps),
                   frames_failing=[c for c in checks if not c['ok']][:20], n_frames_failing=sum(not c['ok'] for c in checks),
                   balance_failures=bad_bal[:20], n_balance_failures=len(bad_bal),
                   triple_formulas=Counter(str(c.get('triple_formulas_ok')) for c in checks))
    summary['triple_formulas'] = dict(summary['triple_formulas'])
    summary['ok'] = summary['n_frames_failing'] == 0 and not bad_bal
    return rows, summary


def rebalance_log(frames, rows):
    """Recheck the balance from a (possibly edited) event log: used by the negative control."""
    by = defaultdict(list)
    for r in rows: by[(r['t0'], r['t1'])].append(r)
    fails = []
    for A, B in zip(frames, frames[1:]):
        ok, s, d = balance(A, B, by[(A.t, B.t)])
        if not ok: fails.append((A.t, B.t, s, d))
    return fails


def from_triangles(tris, t=None, **kw):
    """Sphere tiling dual to a triangulated sphere: cells = vertices, boundaries = edges, junctions = triangles (all triple)."""
    tris = [tuple(sorted(x)) for x in tris]
    E = sorted({p for a, b, c in tris for p in ((a, b), (a, c), (b, c))})
    return Tiling({v for x in tris for v in x}, E, tris, 2, 'sphere', t, **kw)


def from_tets(tets, t=None, **kw):
    """3-sphere tiling dual to a triangulated 3-sphere: cells = vertices, contacts = edges, edges = triangles, corners = tets."""
    tets = [tuple(sorted(x)) for x in tets]
    F = sorted({f for q in tets for f in itertools.combinations(q, 3)})
    E = sorted({e for q in tets for e in itertools.combinations(q, 2)})
    return Tiling({v for q in tets for v in q}, E, None, 3, 'S3', t, edges=F, corners=tets, **kw)


def run_stream(frames, theta=0.9, keep_rows=False):
    """As run(), but for an iterator of frames (memory: two frames at a time). Also performs the negative control on the first
    step with a cell change: that step's first such event retyped as a swap must fail the balance. Returns (rows, summary)."""
    rows, counts, clumps, nfail, fails, bad_bal, triple, neg, nfr = [], Counter(), Counter(), 0, [], [], Counter(), None, 0
    prev = None
    for B in frames:
        nfr += 1
        c = check_tiling(B); triple[str(c.get('triple_formulas_ok'))] += 1
        if not c['ok']:
            nfail += 1
            if len(fails) < 20: fails.append(c)
        if prev is not None:
            ev = classify(prev, B, theta)
            ok, s, d = balance(prev, B, ev)
            if not ok: bad_bal.append((prev.t, B.t, s, d))
            if neg is None and any(e['net'] for e in ev):
                bad = [dict(e) for e in ev]; i = next(i for i, e in enumerate(bad) if e['net']); bad[i]['type'] = 'swap'
                neg = not balance(prev, B, bad)[0]
            for e in ev:
                counts[e['type']] += 1
                if e['type'] == 'clump': clumps[e['pattern']] += 1
                if keep_rows: rows.append(dict(t0=prev.t, t1=B.t, **e))
        prev = B
    summary = dict(frames=nfr, counts=dict(counts), clump_patterns=dict(clumps), frames_failing=fails, n_frames_failing=nfail,
                   balance_failures=bad_bal[:20], n_balance_failures=len(bad_bal), triple_formulas=dict(triple), neg_control_caught=neg)
    summary['ok'] = nfail == 0 and not bad_bal
    return rows, summary
