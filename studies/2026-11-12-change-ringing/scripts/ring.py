"""Change ringing on the permutohedron: exact checks for the Permutohedron Paradigm chapter "Change, Rhythm, Harmony".
DICTO · dictospheres.com - study 2026-11-12-change-ringing.

A row is a tuple of the bells 1..n in striking order. A change exchanges the bells in some set of disjoint pairs of
neighbouring positions (swap starts i: positions i, i+1, 0-based, no two starts adjacent). The row r is the point
x(r) with x_b = (position of bell b) + 1, a corner of the permutohedron of 1..n. A one-swap change is an edge of the
permutohedron; a k-swap change joins opposite corners of a k-cube face.

Usage: python3 ring.py <study dir> [pilot]   (needs ./hamcount compiled from hamcount.c in scripts/)
Prints ok / FAIL lines, PROGRESS lines, writes data/ring.json (data/ring-pilot.json in pilot mode), ends with RING ok (exit 0) or RING FAIL (exit 1); figs.py then prints the job's FINAL line.
"""
import sys, os, json, itertools, subprocess, time, collections

STUDY = sys.argv[1]
PILOT = len(sys.argv) > 2 and sys.argv[2] == 'pilot'
SCR = os.path.join(STUDY, 'scripts'); DATA = os.path.join(STUDY, 'data')
OK = True
OUT = {}
T0 = time.time()

def check(name, cond, detail=''):
    global OK
    print(('ok   ' if cond else 'FAIL ') + name + ('  ' + str(detail) if detail != '' else ''), flush=True)
    OK = OK and bool(cond)

STEPS = 12
def progress(k, what):
    print(f'PROGRESS {k}/{STEPS} {what}  ({time.time() - T0:.1f} s)', flush=True)

# ---------------------------------------------------------------- basics
def changes(n):
    """all changes on n bells as sorted tuples of swap starts (nonempty, no two adjacent)"""
    out = []
    for k in range(1, n):
        for c in itertools.combinations(range(n - 1), k):
            if all(c[j + 1] - c[j] >= 2 for j in range(len(c) - 1)): out.append(c)
    return out

def apply(row, ch):
    r = list(row)
    for i in ch: r[i], r[i + 1] = r[i + 1], r[i]
    return tuple(r)

def change_between(a, b):
    """the change taking row a to row b, or None"""
    n = len(a); sw = []; i = 0
    while i < n:
        if a[i] == b[i]: i += 1; continue
        if i + 1 < n and a[i] == b[i + 1] and a[i + 1] == b[i]: sw.append(i); i += 2; continue
        return None
    return tuple(sw) if sw else None

SYM = '1234567890ET'
def pn_token(ch, n):
    """place notation of a change: 'x' when no place is made, else the places made"""
    fixed = [p for p in range(n) if not any(p in (i, i + 1) for i in ch)]
    return 'x' if not fixed else ''.join(SYM[p] for p in fixed)

def parse_token(tok, n):
    if tok in ('x', 'X', '-'): places = set()
    else: places = {SYM.index(c) for c in tok}
    sw = []; i = 0; implicit = []
    while i < n:
        if i in places: i += 1; continue
        if i + 1 < n and (i + 1) not in places: sw.append(i); i += 2; continue
        implicit.append(i); i += 1
    if any(p not in (0, n - 1) for p in implicit): raise ValueError(f'bad token {tok} on {n}')
    if any(p >= n for p in places): raise ValueError(f'place beyond stage: {tok} on {n}')
    if not sw: raise ValueError(f'no swap: {tok}')
    return tuple(sw)

def tokenize(part):
    toks = []; cur = ''
    for c in part:
        if c in 'xX-':
            if cur: toks.append(cur); cur = ''
            toks.append('x')
        elif c == '.':
            if cur: toks.append(cur); cur = ''
        else: cur += c
    if cur: toks.append(cur)
    return toks

def expand(notation):
    """CCCBR notation: with a comma, each part is written palindromically (a, b -> a + reverse(a)[1:] , b ...)"""
    notation = notation.strip()
    if ',' not in notation: return tokenize(notation)
    out = []
    for part in notation.split(','):
        t = tokenize(part); out += t + t[-2::-1]
    return out

def fib(k):
    a, b = 0, 1
    for _ in range(k): a, b = b, a + b
    return a

def perms(n): return list(itertools.permutations(range(1, n + 1)))

def graph(n, single_only):
    V = perms(n); idx = {r: i for i, r in enumerate(V)}
    chs = [c for c in changes(n) if (len(c) == 1 or not single_only)]
    adj = [[idx[apply(r, c)] for c in chs] for r in V]
    return V, idx, adj

def run_ham(adj, listing=False):
    src = os.path.join(SCR, 'hamcount')
    inp = f'{len(adj)}\n' + '\n'.join(f'{len(a)} ' + ' '.join(map(str, a)) for a in adj) + '\n'
    out = subprocess.run([src] + (['list'] if listing else []), input=inp, capture_output=True, text=True, check=True).stdout
    lines = out.strip().split('\n')
    cnt = int(lines[-1].split()[1])
    cyc = [list(map(int, l.split()[1:])) for l in lines[:-1]] if listing else None
    return cnt, cyc

# symmetry group of the permutohedron of 1..n acting on rows: relabel the bells (permute coordinates) and/or
# read the row backwards (the point reflection x -> n+1-x)
def group(n):
    G = []
    for p in itertools.permutations(range(1, n + 1)):
        pi = dict(zip(range(1, n + 1), p))
        for rev in (False, True): G.append((pi, rev))
    return G

def act(g, row):
    pi, rev = g
    r = tuple(pi[b] for b in row)
    return r[::-1] if rev else r

def proper(g, n):
    pi, rev = g; p = [pi[b] for b in range(1, n + 1)]
    inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
    sgn = -1 if inv % 2 else 1
    return sgn * ((-1) ** (n - 1) if rev else 1) == 1

def ord_g(g, n):
    rows = [tuple(range(1, n + 1)), (2, 1) + tuple(range(3, n + 1))]
    k = 1; cur = [act(g, r) for r in rows]
    while cur != rows: cur = [act(g, r) for r in cur]; k += 1
    return k

def face_key(row, gens):
    """the face of the permutohedron through `row` spanned by the swap starts `gens`: an ordered set partition
    (blocks = runs of positions joined by the generators), as a tuple of frozensets"""
    n = len(row); blocks = []; cur = [row[0]]
    for p in range(1, n):
        if (p - 1) in gens: cur.append(row[p])
        else: blocks.append(frozenset(cur)); cur = [row[p]]
    blocks.append(frozenset(cur))
    return tuple(blocks)

def cyclic_period(word):
    N = len(word)
    for p in range(1, N + 1):
        if N % p == 0 and all(word[t] == word[(t + p) % N] for t in range(N)): return p
    return N

def word_str(word):
    p = cyclic_period(word)
    return ('(' + '.'.join(word[:p]) + f')^{len(word) // p}') if p < len(word) else '.'.join(word)

def rows_from(word_toks, n, start=None):
    r = start or tuple(range(1, n + 1)); rows = [r]; chs = []
    for t in word_toks:
        c = parse_token(t, n) if isinstance(t, str) else t
        chs.append(c); r = apply(r, c); rows.append(r)
    return rows, chs

def analyse(name, n, rows_closed, chs, G=None, want_sym=True):
    """rows_closed: rows r0..rN with rN the row after the last change (a true extent has rN == r0)."""
    N = len(chs); rows = rows_closed[:-1]
    fact = 1
    for k in range(2, n + 1): fact *= k
    closes = rows_closed[-1] == rows_closed[0]
    true = closes and len(set(rows)) == N
    extent = true and N == fact
    word = [pn_token(c, n) for c in chs]
    hist = collections.Counter(len(c) for c in chs)
    # faces: crossed (k-swap change, k >= 2: the k-cube face it crosses), turned (two consecutive one-swap changes: the 2-face)
    crossed = set(); turned_sq = set(); turned_hex = set()
    for t in range(N):
        c = chs[t]
        if len(c) >= 2: crossed.add(face_key(rows[t], set(c)))
        cprev = chs[t - 1]
        if len(c) == 1 and len(cprev) == 1 and c != cprev:
            k = face_key(rows[t], {c[0], cprev[0]})
            (turned_hex if abs(c[0] - cprev[0]) == 1 else turned_sq).add(k)
    crossed_sq = {f for f in crossed if sum(len(b) == 2 for b in f) == 2 and n - len(f) == 2}
    back = tuple(range(n, 0, -1))
    kback = rows.index(back) if back in rows else None
    res = dict(name=name, n=n, rows=N, closes=closes, true=true, extent=extent, word=word_str(word), period=cyclic_period(word),
               parts=N // cyclic_period(word), swaps_hist={str(k): v for k, v in sorted(hist.items())},
               edges_used=hist.get(1, 0), squares_crossed=len(crossed_sq), higher_cubes_crossed=len(crossed) - len(crossed_sq),
               squares_turned=len(turned_sq), hexagons_turned=len(turned_hex), backrounds_at=kback,
               backrounds_antipodal=(kback is not None and 2 * kback == N))
    if want_sym and extent:
        G = G or group(n)
        E = {frozenset((rows[t], rows[(t + 1) % N])) for t in range(N)}
        nxt = {rows[t]: rows[(t + 1) % N] for t in range(N)}
        stab = []; rot = 0
        for g in G:
            if all(frozenset((act(g, a), act(g, b))) in E for a, b in (tuple(e) for e in E)):
                stab.append(g)
                if nxt[act(g, rows[0])] == act(g, rows[1]): rot += 1
        res['symmetry_order'] = len(stab); res['symmetry_direction_preserving'] = rot
        res['central_inversion'] = any(g[1] and all(g[0][b] == b for b in g[0]) for g in stab)
        res['symmetry_type'] = dict(sorted(collections.Counter(f'{"proper" if proper(g, n) else "improper"} order {ord_g(g, n)}' for g in stab).items()))
        res['symmetry_elements'] = [(''.join(str(g[0][b]) for b in range(1, n + 1)), g[1]) for g in stab]
    return res

def show(res):
    keys = ['symmetry_type', 'name', 'rows', 'true', 'extent', 'word', 'period', 'parts', 'swaps_hist', 'squares_crossed', 'higher_cubes_crossed',
            'squares_turned', 'hexagons_turned', 'backrounds_at', 'backrounds_antipodal', 'symmetry_order', 'symmetry_direction_preserving', 'central_inversion']
    print('  ' + '; '.join(f'{k}={res[k]}' for k in keys if k in res), flush=True)

# ---------------------------------------------------------------- 1. the change graph and the permutohedron
progress(0, 'changes and faces')
for n in range(2, 13):
    check(f'number of changes on {n} bells = F({n + 1}) - 1 = {fib(n + 1) - 1}', len(changes(n)) == fib(n + 1) - 1, len(changes(n)))
OUT['changes_count'] = {n: len(changes(n)) for n in range(2, 13)}
for n in (3, 4, 5, 6):
    V = perms(n)
    # faces of the permutohedron as ordered set partitions; count 2-faces by kind via face_key over all rows and generator pairs
    sq = set(); hx = set(); ed = set()
    for r in V:
        for i in range(n - 1):
            ed.add(face_key(r, {i}))
            for j in range(i + 1, n - 1):
                (hx if j == i + 1 else sq).add(face_key(r, {i, j}))
    fact = len(V)
    exp_e = (n - 1) * fact // 2; exp_h = (n - 2) * fact // 6; exp_s = ((n - 2) * (n - 3) // 2) * fact // 4
    check(f'P{n}: {len(V)} corners, edges {len(ed)} = (n-1)n!/2, hexagons {len(hx)} = (n-2)n!/6, squares {len(sq)} = C(n-2,2)n!/4',
          (len(ed), len(hx), len(sq)) == (exp_e, exp_h, exp_s))
    OUT.setdefault('faces', {})[n] = dict(corners=len(V), edges=len(ed), hexagons=len(hx), squares=len(sq))
check('truncated octahedron: 24 corners, 36 edges, 8 hexagons, 6 squares', OUT['faces'][4] == dict(corners=24, edges=36, hexagons=8, squares=6))
check('4D permutohedron: 120 corners, 240 edges, 60 hexagons + 90 squares = 150 two-faces', OUT['faces'][5] == dict(corners=120, edges=240, hexagons=60, squares=90))
# geometry: a one-swap change moves the point by sqrt2 (an edge); a k-swap change by sqrt(2k) between opposite corners of a k-cube face
for n in (4, 5, 6):
    good = True
    for r in perms(n):
        for c in changes(n):
            s = apply(r, c)
            x = {b: r.index(b) + 1 for b in r}; y = {b: s.index(b) + 1 for b in s}
            d2 = sum((x[b] - y[b]) ** 2 for b in r)
            # opposite corners of the face: the face's corners are the 2^k rows from subsets of the swaps
            face_rows = {apply(r, sub) for k in range(len(c) + 1) for sub in itertools.combinations(c, k)}
            if d2 != 2 * len(c) or len(face_rows) != 2 ** len(c) or face_key(r, set(c)) != face_key(s, set(c)): good = False
    check(f'n={n}: every k-swap change moves the point by sqrt(2k) to the opposite corner of a k-cube face', good)

# ---------------------------------------------------------------- 2. controls for the Hamiltonian-cycle counter
progress(1, 'Hamiltonian counter controls')
def cyc_graph(m): return [[(i - 1) % m, (i + 1) % m] for i in range(m)]
cube = [[v ^ 1, v ^ 2, v ^ 4] for v in range(8)]
K4 = [[w for w in range(4) if w != v] for v in range(4)]
def lcf(m, pat):
    adj = [[(i - 1) % m, (i + 1) % m] for i in range(m)]
    for i in range(m): adj[i].append((i + pat[i % len(pat)]) % m)
    return adj
dodeca = lcf(20, [10, 7, 4, -4, -7, 10, -4, 7, -7, 4])
petersen = [[(i + 1) % 5, (i - 1) % 5, i + 5] if i < 5 else [5 + (i - 5 + 2) % 5, 5 + (i - 5 - 2) % 5, i - 5] for i in range(10)]
for nm, g, want in (('hexagon', cyc_graph(6), 1), ('K4', K4, 3), ('cube', cube, 6), ('dodecahedron (Hamilton)', dodeca, 30), ('Petersen (none)', petersen, 0)):
    check(f'control: Hamiltonian cycles of the {nm} = {want}', run_ham(g)[0] == want, run_ham(g)[0])
check('control: dodecahedron graph is 3-regular on 20 vertices', all(len(set(a)) == 3 for a in dodeca))

# ---------------------------------------------------------------- 3. all extents on 3 and 4 bells
progress(2, 'all extents on 3 and 4 bells')
V3, idx3, P3 = graph(3, True); _, _, R3 = graph(3, False)
OUT['ham'] = {'P3': run_ham(P3)[0], 'R3': run_ham(R3)[0]}
check('3 bells: the change graph is the hexagon; one extent (plain hunt on three)', OUT['ham'] == {'P3': 1, 'R3': 1})
V4, idx4, P4 = graph(4, True); _, _, R4 = graph(4, False)
cP4, cycP4 = run_ham(P4, True)
cR4 = run_ham(R4)[0]
check('R4 cycle count small enough to list (<= 400000)', cR4 <= 400000, cR4)
cycR4 = run_ham(R4, True)[1] if cR4 <= 400000 else []
OUT['ham'].update({'P4': cP4, 'R4': cR4})
def ham_py(adj):
    # independent count: directed Hamiltonian cycles through vertex 0, halved
    n = len(adj); cnt = 0; used = [False] * n; used[0] = True
    def go(v, d):
        nonlocal cnt
        if d == n: cnt += (0 in adj[v]); return
        for w in adj[v]:
            if not used[w]: used[w] = True; go(w, d + 1); used[w] = False
    go(0, 1); return cnt // 2
check('independent Python count agrees: P4', ham_py(P4) == cP4, ham_py(P4))
check('independent Python count agrees: R4', ham_py(R4) == cR4)
print(f'  Hamiltonian cycles: truncated octahedron P4 {cP4}; change graph R4 {cR4}', flush=True)
check('every P4 cycle is also an R4 cycle (count P4 <= R4)', cP4 <= cR4)
G4 = group(4)
# the full automorphism groups of P4 and R4 (backtracking), against the 48 symmetries of the permutohedron
def automorphisms(adj):
    n = len(adj); A = [set(a) for a in adj]; order = []; seen = {0}; q = [0]
    while q:
        v = q.pop(0); order.append(v)
        for w in adj[v]:
            if w not in seen: seen.add(w); q.append(w)
    cnt = 0; img = {}
    def bt(k):
        nonlocal cnt
        if k == n: cnt += 1; return
        v = order[k]
        for c in range(n):
            if c in img.values() or len(A[c]) != len(A[v]): continue
            if all(((w in A[v]) == (img[w] in A[c])) for w in img):
                img[v] = c; bt(k + 1); del img[v]
    bt(0); return cnt
aP4 = automorphisms(P4); aR4 = automorphisms(R4)
OUT['aut'] = {'P4': aP4, 'R4': aR4}
check('the automorphism group of the truncated-octahedron graph has order 48', aP4 == 48, aP4)
check('the 48 symmetries (relabel bells, read backwards) are automorphisms of R4', all(
    all(idx4[act(g, V4[w])] in set(R4[idx4[act(g, V4[v])]]) for v in range(24) for w in R4[v]) for g in G4))
print(f'  automorphisms of the change graph R4: {aR4}', flush=True)

def cycle_info(cyc, V):
    rows = [V[i] for i in cyc] + [V[cyc[0]]]
    chs = [change_between(rows[t], rows[t + 1]) for t in range(len(cyc))]
    return rows, chs

def canon(cyc, V, idx, G):
    N = len(cyc); best = None
    E = [(V[cyc[t]], V[cyc[(t + 1) % N]]) for t in range(N)]
    for g in G:
        key = tuple(sorted(tuple(sorted((idx[act(g, a)], idx[act(g, b)]))) for a, b in E))
        if best is None or key < best: best = key
    return best

def census(cycs, V, idx, G, label):
    orbits = collections.defaultdict(list); crosscnt = collections.Counter(); periods = collections.Counter(); anti = 0
    for k, cyc in enumerate(cycs):
        orbits[canon(cyc, V, idx, G)].append(k)
        rows, chs = cycle_info(cyc, V)
        crosscnt[sum(len(c) >= 2 for c in chs)] += 1
        periods[cyclic_period([pn_token(c, 4) for c in chs])] += 1
        back = (4, 3, 2, 1); anti += (2 * [V[i] for i in cyc].index(back) == len(cyc))
    symorders = collections.Counter()
    # orbit size = number of cycles in the orbit (all Hamiltonian cycles are listed), so |stab| = |G| / orbit size
    for key, members in orbits.items(): symorders[len(G) // len(members)] += 1
    check(f'{label}: orbit sizes divide 48', all(len(G) % len(m) == 0 for m in orbits.values()))
    return orbits, dict(cycles=len(cycs), orbits=len(orbits), orbits_by_symmetry_order=dict(sorted(symorders.items())),
                        cycles_by_cross_changes=dict(sorted(crosscnt.items())), cycles_by_word_period=dict(sorted(periods.items())),
                        cycles_backrounds_antipodal=anti)

progress(3, 'orbits of the 4-bell extents')
orbP4, censP4 = census(cycP4, V4, idx4, G4, 'P4')
orbR4, censR4 = census(cycR4, V4, idx4, G4, 'R4')
OUT['census4'] = {'P4': censP4, 'R4': censR4}
print('  P4 census', censP4, flush=True); print('  R4 census', censR4, flush=True)
check('P4 cycles are exactly the R4 cycles with no cross change', censR4['cycles_by_cross_changes'].get(0, 0) == cP4)
# the most symmetric extents
def best_reps(orbits, cycs, V):
    top = max(48 // len(m) for m in orbits.values())
    out = []
    for key, m in orbits.items():
        if 48 // len(m) == top:
            rows, chs = cycle_info(cycs[m[0]], V)
            out.append(analyse(f'most symmetric, orbit of {len(m)}', 4, rows, chs, G4))
    return top, out
topP4, repsP4 = best_reps(orbP4, cycP4, V4); topR4, repsR4 = best_reps(orbR4, cycR4, V4)
print(f'  highest symmetry order: P4 {topP4} ({len(repsP4)} orbits); R4 {topR4} ({len(repsR4)} orbits)', flush=True)
for r in repsP4 + repsR4: show(r)
OUT['most_symmetric'] = {'P4': repsP4, 'R4': repsR4}
# full row lists of the most symmetric cycles for the figures
def rows_of(orbits, cycs, V, top):
    return [[''.join(map(str, V[i])) for i in cycs[m[0]]] for key, m in orbits.items() if 48 // len(m) == top]
OUT['most_symmetric_rows'] = {'P4': rows_of(orbP4, cycP4, V4, topP4), 'R4': rows_of(orbR4, cycR4, V4, topR4)}

def sjt(n):
    """plain changes (Steinhaus-Johnson-Trotter order) as a list of one-swap changes"""
    perm = list(range(1, n + 1)); dirs = [-1] * n; rows = [tuple(perm)]; chs = []
    while True:
        mob = None
        for i in range(n):
            j = i + dirs[perm[i] - 1]
            if 0 <= j < n and perm[j] < perm[i] and (mob is None or perm[i] > perm[mob]): mob = i
        if mob is None: break
        j = mob + dirs[perm[mob] - 1]; perm[mob], perm[j] = perm[j], perm[mob]; chs.append((min(mob, j),)); rows.append(tuple(perm))
        for k in range(n):
            if perm[k] > perm[j]: dirs[perm[k] - 1] *= -1
    last = change_between(rows[-1], rows[0])
    return rows + [rows[0]], chs + [last]

# ---------------------------------------------------------------- 4. methods: the CCCBR collection, stages 3-6
progress(4, 'CCCBR collection')
tsv = os.path.join(DATA, 'cccbr-methods-stage3-6.tsv')
meth = []
for line in open(tsv):
    if line.startswith('#') or line.startswith('id\t'): continue
    f = line.rstrip('\n').split('\t'); meth.append(dict(zip(['id', 'stage', 'cls', 'flags', 'hunts', 'lol', 'title', 'notation', 'lead_head'], f)))
if PILOT: meth = [m for m in meth if m['stage'] in ('3', '4')] + [m for m in meth if m['stage'] == '5'][:200]
skipped = collections.Counter(); parsed = 0; lh_ok = 0; lh_bad = []
plain_course = {}
stats = collections.defaultdict(lambda: collections.Counter())
minimus_extents = []
EXT_NAMES = collections.defaultdict(list)
SKIP_BY_STAGE = collections.Counter()
for m in meth:
    n = int(m['stage'])
    try:
        toks = expand(m['notation']); chs = [parse_token(t, n) for t in toks]
    except Exception as e:
        skipped[str(e).split(':')[0]] += 1; SKIP_BY_STAGE[n] += 1; continue
    if len(chs) != int(m['lol']): lh_bad.append((m['title'], 'length')); continue
    parsed += 1
    r = tuple(range(1, n + 1))
    for c in chs: r = apply(r, c)
    if ''.join(map(str, r)) == m['lead_head']: lh_ok += 1
    else: lh_bad.append((m['title'], ''.join(map(str, r)), m['lead_head'])); continue
    # plain course: repeat the lead until rounds
    rows = [tuple(range(1, n + 1))]; allch = []
    for _ in range(200):
        for c in chs: allch.append(c); rows.append(apply(rows[-1], c))
        if rows[-1] == rows[0]: break
    N = len(allch); fact = len(perms(n)) if n <= 6 else None
    true = rows[-1] == rows[0] and len(set(rows[:-1])) == N
    st = stats[n]; st['methods'] += 1; st['true plain course'] += true
    if true and N == fact:
        st['plain course is an extent'] += 1
        if all(len(c) == 1 for c in allch): st['extent using edges only'] += 1
        if n != 4: EXT_NAMES[n].append(m['title'] + (' [edges only]' if all(len(c) == 1 for c in allch) else ''))
        if n == 4:
            cyc = [idx4[x] for x in rows[:-1]]
            minimus_extents.append((m['title'], m['cls'], m['flags'], canon(cyc, V4, idx4, G4), rows, allch))
OUT['cccbr'] = dict(parsed=parsed, lead_heads_match=lh_ok, lead_head_mismatch=lh_bad[:20], skipped=dict(skipped),
                    by_stage={n: dict(c) for n, c in sorted(stats.items())},
                    skipped_by_stage=dict(sorted(SKIP_BY_STAGE.items())), extent_names={n: v if n != 5 else (v if len(v) <= 12 else [x for x in v if 'edges only' in x] + [f'... {len(v)} in all']) for n, v in sorted(EXT_NAMES.items())})
print('  CCCBR', OUT['cccbr'], flush=True)
check('every parsed CCCBR method gives the lead head the collection lists', not lh_bad and parsed > 0, f'{lh_ok} of {parsed}')
# Minimus extents: which orbits of R4 Hamiltonian cycles carry a named method
orbit_names = collections.defaultdict(list)
for title, cls, flags, key, rows, allch in minimus_extents:
    check(f'{title}: plain course is a Hamiltonian cycle of R4 (in the enumeration)', key in orbR4)
    orbit_names[key].append(title)
OUT['minimus_named_orbits'] = dict(named_orbits=len(orbit_names), of=len(orbR4), methods=len(minimus_extents),
                                   groups=sorted([sorted(v) for v in orbit_names.values()], key=lambda v: (-len(v), v)),
                                   edges_only=[t for t, c, f, k, rows, allch in minimus_extents if all(len(x) == 1 for x in allch)])
print('  Minimus extents by orbit:', OUT['minimus_named_orbits'], flush=True)
per_orb = collections.Counter(); per_named = collections.Counter()
for key, members in orbR4.items():
    rows, chs = cycle_info(cycR4[members[0]], V4); p = cyclic_period([pn_token(c, 4) for c in chs])
    per_orb[p] += 1; per_named[p] += key in orbit_names
OUT['minimus_named_orbits']['orbits_by_period'] = dict(sorted(per_orb.items())); OUT['minimus_named_orbits']['named_orbits_by_period'] = dict(sorted(per_named.items()))
print('  orbits by word period', dict(per_orb), 'named', dict(per_named), flush=True)
top_named = {}
for key, members in orbR4.items():
    if 48 // len(members) == topR4:
        rows, chs = cycle_info(cycR4[members[0]], V4)
        top_named[word_str([pn_token(c, 4) for c in chs])] = orbit_names.get(key, [])
pc_rows, pc_chs = sjt(4); pc_key = canon([idx4[r] for r in pc_rows[:-1]], V4, idx4, G4)
OUT['top_orbits_named'] = top_named; OUT['plain_changes_4_orbit_symmetry'] = 48 // len(orbR4[pc_key]); OUT['plain_changes_4_named_as'] = orbit_names.get(pc_key, [])
print('  most symmetric orbits and their CCCBR names:', top_named, '; plain changes on 4 in orbit named', OUT['plain_changes_4_named_as'], flush=True)
min_an = {}
for title, cls, flags, key, rows, allch in minimus_extents:
    a = analyse(title, 4, rows, allch, G4); a['orbit_size'] = len(orbR4[key]); a['class'] = cls; a['flags'] = flags
    min_an[title] = a
OUT['minimus_analyses'] = min_an
pbm = min_an.get('Plain Bob Minimus')
check('control (CCCBR): Plain Bob Minimus plain course = 24 rows, a true extent, lead head 1342', pbm is not None and pbm['extent'] and pbm['rows'] == 24)
if pbm: show(pbm)

# ---------------------------------------------------------------- 5. named extents on 4, 5, 6 bells
progress(5, 'plain hunt, plain changes, broken controls')
named = {}
for n in (4, 5, 6):
    rows, chs = sjt(n)
    check(f'plain changes on {n}: the closing step is one swap', chs[-1] is not None and len(chs[-1]) == 1)
    a = analyse(f'Plain changes on {n} (Steinhaus-Johnson-Trotter order)', n, rows, chs, want_sym=(n <= 5)); named[a['name']] = a; show(a)
    check(f'plain changes on {n} are an extent using edges only (a Hamiltonian cycle of the permutohedron)', a['extent'] and a['edges_used'] == a['rows'])
def plain_hunt(n):
    toks = (['x', '1' + SYM[n - 1]] if n % 2 == 0 else [SYM[n - 1], '1']) * n
    return rows_from(toks, n)
for n in (4, 5, 6):
    rows, chs = plain_hunt(n)
    a = analyse(f'Plain hunt on {n}', n, rows, chs, want_sym=False); named[a['name']] = a; show(a)
    check(f'plain hunt on {n}: true, {2 * n} rows, backrounds after {n} changes (antipodal)', a['true'] and a['rows'] == 2 * n and a['backrounds_at'] == n)
# broken methods that must fail as tours
for nm, n, toks in (('broken: Plain Bob Minimus with lead end 14 (= plain hunt)', 4, ['x', '14'] * 4 * 3),
                    ('broken: Plain Bob Minimus with lead end x (two crosses in a row repeat a row)', 4, ['x', '14', 'x', '14', 'x', '14', 'x', 'x'] * 3),
                    ('broken: Plain Bob Doubles plain course rung for 120 rows', 5, ['5', '1', '5', '1', '5', '1', '5', '1', '5', '125'] * 12)):
    rows, chs = rows_from(toks, n); a = analyse(nm, n, rows, chs, want_sym=False); named[nm] = a
    check(f'negative control fails as an extent: {nm}', not a['extent'], f'rows {a["rows"]}, true {a["true"]}')

# ---------------------------------------------------------------- 6. Doubles: all extents with calls
progress(6, 'Doubles callings')
def lead_rows(start, toks, n):
    r = start; rows = []; chs = []
    for t in toks:
        c = parse_token(t, n); rows.append(r); chs.append(c); r = apply(r, c)
    return rows, chs, r
def search(n, nleads, lead_of, calls, cap_s, first_only=False, label=''):
    """all callings (strings over `calls`) of nleads leads whose rows are all distinct and come round exactly at the end"""
    fact = len(perms(n)); found = []; t0 = time.time(); timed_out = False; nodes = 0
    seen = set()
    def dfs(start, calling):
        nonlocal timed_out, nodes
        nodes += 1
        if time.time() - t0 > cap_s: timed_out = True; return
        if len(calling) == nleads:
            if start == tuple(range(1, n + 1)): found.append(''.join(calling))
            return
        for c in calls:
            rows, chs, nxt = lead_rows(start, lead_of(c), n)
            if any(r in seen for r in rows) or len(set(rows)) < len(rows): continue
            if nxt == tuple(range(1, n + 1)) and len(calling) + 1 < nleads: continue
            for r in rows: seen.add(r)
            calling.append(c); dfs(nxt, calling); calling.pop()
            for r in rows: seen.discard(r)
            if timed_out or (first_only and found): return
    dfs(tuple(range(1, n + 1)), [])
    print(f'  {label}: {len(found)} callings found, {nodes} nodes, {time.time() - t0:.1f} s, timed out {timed_out}', flush=True)
    return found, timed_out
def callings_summary(found, calls):
    by = collections.Counter(''.join(sorted(set(f) - {'P'})) or 'none' for f in found)
    mincalls = min((sum(ch != 'P' for ch in f) for f in found), default=None)
    rot = set()
    for f in found: rot.add(min(f[i:] + f[:i] for i in range(len(f))))
    return dict(callings=len(found), by_calls_used=dict(sorted(by.items())), fewest_calls=mincalls, up_to_rotation=len(rot))
def full_rows(found_calling, lead_of, n):
    rows = [tuple(range(1, n + 1))]; chs = []
    for c in found_calling:
        rs, cs, nxt = lead_rows(rows[-1], lead_of(c), n); chs += cs; rows += rs[1:] + [nxt]
    return rows, chs
G5 = group(5)
DOUB = {
  'Plain Bob Doubles': (lambda c: ['5', '1', '5', '1', '5', '1', '5', '1', '5', {'P': '125', 'B': '145', 'S': '123'}[c]], 'PBS', 12),
  'Grandsire Doubles': (lambda c: ['3', '1', '5', '1', '5', '1', '5', '1'] + {'P': ['5', '1'], 'B': ['3', '1'], 'S': ['3', '123']}[c], 'PBS', 12),
  # Stedman: a lead of two sixes; the call letter covers both six ends of the lead: P plain, S single at the 2nd change ("5" -> "345")
  # of the lead only, T at the 8th only, U at both
  'Stedman Doubles': (lambda c: ['3', '1', '345' if c in 'SU' else '5', '3', '1', '3', '1', '3', '345' if c in 'TU' else '5', '1', '3', '1'], 'PSTU', 10),
}
check('CCCBR notation: Plain Bob Doubles lead = 5.1.5.1.5,125 expanded', expand('5.1.5.1.5,125') == DOUB['Plain Bob Doubles'][0]('P'))
check('CCCBR notation: Grandsire Doubles lead = 3,1.5.1.5.1 expanded', expand('3,1.5.1.5.1') == DOUB['Grandsire Doubles'][0]('P'))
check('CCCBR notation: Stedman Doubles lead = 3.1.5.3.1.3,1 expanded', expand('3.1.5.3.1.3,1') == DOUB['Stedman Doubles'][0]('P'))
OUT['doubles'] = {}; FOUND = {}
for nm, (lead_of, calls, nleads) in DOUB.items():
    rows, chs = rows_from([t for _ in range(60) for t in lead_of('P')], 5)
    k = next(t for t in range(1, len(rows)) if rows[t] == rows[0])
    print(f'  {nm}: plain course {k} rows', flush=True)
    found, to = search(5, nleads, lead_of, calls, 900 if not PILOT else 60, label=nm)
    FOUND[nm] = found
    summ = callings_summary(found, calls); summ['plain_course_rows'] = k; summ['timed_out'] = to
    if found:
        # the extent with fewest calls, first in alphabetical order, analysed in full
        best = sorted(found, key=lambda f: (sum(ch != 'P' for ch in f), f))[0]
        rows, chs = full_rows(best, lead_of, 5)
        a = analyse(f'{nm}, calling {best}', 5, rows, chs, G5); show(a); summ['example'] = a; summ['example_calling'] = best
        cyc_keys = set()
        for f in found:
            rows, chs = full_rows(f, lead_of, 5)
            cyc_keys.add(frozenset(frozenset(p) for p in zip(rows[:-1], rows[1:])))
        summ['distinct_cycles'] = len(cyc_keys)
    OUT['doubles'][nm] = summ
    print(f'  {nm}:', {k: v for k, v in summ.items() if k != "example"}, flush=True)
pb = OUT['doubles']['Plain Bob Doubles']; gs = OUT['doubles']['Grandsire Doubles']; sd = OUT['doubles']['Stedman Doubles']
check('Plain Bob Doubles plain course = 40 rows', pb['plain_course_rows'] == 40)
check('Grandsire Doubles plain course = 30 rows', gs['plain_course_rows'] == 30)
check('Stedman Doubles plain course = 60 rows', sd['plain_course_rows'] == 60)
check('control (Wenham): Grandsire Doubles P B P B P S repeated is an extent', 'PBPBPSPBPBPS' in FOUND['Grandsire Doubles'])
check('Grandsire Doubles has no extent with bobs only', not gs['timed_out'] and 'B' not in gs['by_calls_used'])
for nm in DOUB: check(f'{nm}: search finished within its cap', not OUT['doubles'][nm]['timed_out'])

# ---------------------------------------------------------------- 7. Minor: Plain Bob Minor
progress(7, 'Plain Bob Minor')
pbmin = lambda c: ['x', '16'] * 5 + ['x', {'P': '12', 'B': '14', 'S': '1234'}[c]]
check('CCCBR notation: Plain Bob Minor lead = -16-16-16,12 expanded', expand('-16-16-16,12') == pbmin('P'))
OUT['minor'] = {}
for label, calls in (('bobs only', 'PB'), ('bobs and singles', 'PBS')):
    found, to = search(6, 60, pbmin, calls, 600 if not PILOT else 30, first_only=True, label=f'Plain Bob Minor {label}')
    ent = dict(found=found[:1], timed_out=to)
    if found:
        rows, chs = full_rows(found[0], pbmin, 6); a = analyse(f'Plain Bob Minor, {label}, calling {found[0]}', 6, rows, chs, want_sym=False)
        ent['analysis'] = a; show(a); check(f'Plain Bob Minor {label}: the found calling is a true 720', a['extent'])
    OUT['minor'][label] = ent

# ---------------------------------------------------------------- 8. geodesics between rounds and backrounds
progress(8, 'geodesics')
STANLEY = {3: 2, 4: 16, 5: 768, 6: 292864}
OUT['geodesics'] = {}
for n in (3, 4, 5, 6):
    for nm, single in (('P', True), ('R', False)):
        V, idx, adj = graph(n, single)
        dist = [-1] * len(V); ways = [0] * len(V); dist[0] = 0; ways[0] = 1; q = [0]
        for v in q:
            for w in adj[v]:
                if dist[w] < 0: dist[w] = dist[v] + 1; q.append(w)
                if dist[w] == dist[v] + 1: ways[w] += ways[v]
        b = idx[tuple(range(n, 0, -1))]
        far = max(dist)
        OUT['geodesics'][f'{nm}{n}'] = dict(distance=dist[b], geodesics=ways[b], diameter=far, farthest=[''.join(map(str, V[i])) for i in range(len(V)) if dist[i] == far][:3])
        print(f'  {nm}{n}: rounds->backrounds distance {dist[b]}, geodesics {ways[b]}, eccentricity of rounds {far}', flush=True)
    check(f'control (Stanley 1984): {STANLEY[n]} shortest edge paths rounds -> backrounds on P{n}, length C(n,2)',
          OUT['geodesics'][f'P{n}'] == dict(OUT['geodesics'][f'P{n}'], distance=n * (n - 1) // 2, geodesics=STANLEY[n]))
    check(f'R{n}: backrounds is the farthest row, at distance n = {n}', OUT['geodesics'][f'R{n}']['distance'] == n == OUT['geodesics'][f'R{n}']['diameter'])

# ---------------------------------------------------------------- 9. the extents of the figures
progress(9, 'figure data')
fig = {}
rows, chs = rows_from(expand('-14-14,12') * 3, 4); fig['Plain Bob Minimus'] = [''.join(map(str, r)) for r in rows]
rows, chs = sjt(4); fig['Plain changes on 4'] = [''.join(map(str, r)) for r in rows]
rows, chs = plain_hunt(4); fig['Plain hunt on 4'] = [''.join(map(str, r)) for r in rows]
for title, cls, flags, key, rows_, allch in minimus_extents:
    if title in ('Double Court Place Minimus', 'Double Bob Minimus', 'Plain Bob Minimus'): fig['CCCBR ' + title] = [''.join(map(str, r)) for r in rows_]
fig['most symmetric P4'] = OUT['most_symmetric_rows']['P4']; fig['most symmetric R4'] = OUT['most_symmetric_rows']['R4']
# rhythm strips: the swap positions of each change, as 0/1 columns
strips = {}
for nm, (rows_, chs_) in (('Plain Bob Minimus', rows_from(expand('-14-14,12') * 3, 4)), ('Plain changes on 4', sjt(4))):
    strips[nm] = [list(c) for c in chs_]
for nm in DOUB:
    if OUT['doubles'][nm].get('example_calling'):
        rows_, chs_ = full_rows(OUT['doubles'][nm]['example_calling'], DOUB[nm][0], 5); strips[nm] = [list(c) for c in chs_]
rows_, chs_ = sjt(5); strips['Plain changes on 5'] = [list(c) for c in chs_]
fig['strips'] = strips
OUT['figures'] = fig
OUT['named'] = named
progress(10, 'write')
name = 'ring-pilot.json' if PILOT else 'ring.json'
json.dump(OUT, open(os.path.join(DATA, name), 'w'), indent=1, default=lambda o: sorted(o) if isinstance(o, (set, frozenset)) else str(o))
progress(12, 'done')
print(f'time {time.time() - T0:.1f} s')
print('RING ok (all checks passed)' if OK else 'RING FAIL'); sys.exit(0 if OK else 1)
