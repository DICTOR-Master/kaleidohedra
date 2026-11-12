"""Equal-speed line B (permutohedron -> Loday) for any n from gp_enum's exact vertex candidates; Conjectures 1 and 2 of the
Permutohedron Family draft; the Loday end against m_{n+2}.  DICTO · dictospheres.com - study 2026-11-12-permutohedron-associahedron-line,
13 Nov 2026.  Exact throughout (fractions.Fraction, Python integers); stdlib only.

Input: candidates file from gp_enum (each d-subset of inequalities that is a vertex on a closed s-interval [lo, hi]).
Stations: every interval end point (the only places the labelled structure can change) and the midpoint of every open stretch.
At each station: the vertices, the tight sets, the facets (affine rank of the tight vertices = d - 1), the face lattice (closure of
facet vertex sets under intersection, graded), the f-vector, Euler, simple?, generalized permutohedron? (every edge parallel to some
e_i - e_j).  Checks:
  C1  every non-interval facet S is present exactly for s < D_S (D_S = sum over block pairs k_b k_b'); interval facets always;
  C2  Omega(Pi; centre) by Warren's vertex formula on the enumerated vertices = 2^(n-1) n/(n-1)! = the flag sum;
  C3  Omega(Loday; centre) by the vertex formula = m_{n+2} (X = Loday facet values at the centre), Catalan(n) simple vertices;
  negative: a tree-dropped m_{n+2} differs.
Reported (not a control): stations that are not generalized permutohedra (an edge off the root directions), each such edge
confirmed independently by the rank of the common facet normals.
Usage: python3 gp_line_b.py n candidates.txt out.json     Prints PROGRESS k/K lines; ends with 'LINEB ok' or 'LINEB FAIL'."""
import sys, json, time, itertools
from fractions import Fraction as F
from math import comb, factorial

n = int(sys.argv[1]); CAND = sys.argv[2]; OUT = sys.argv[3]; d = n - 1
T0 = time.time(); OK = True; RES = {'n': n}
def chk(name, cond, detail=''):
    global OK
    OK = OK and bool(cond); print(('ok   ' if cond else 'FAIL ') + f'n={n}: ' + name + (f'  [{detail}]' if detail != '' else ''), flush=True)

FULLM = (1 << n) - 1
MASKS = list(range(1, FULLM)); M = len(MASKS); POS = {m: k for k, m in enumerate(MASKS)}
def elems(m): return [i + 1 for i in range(n) if (m >> i) & 1]
def lab(m): return ''.join(map(str, elems(m)))
def isint(m): e = elems(m); return e[-1] - e[0] + 1 == len(e)
def blocks(m):
    e = elems(m); out = []; cur = [e[0]]
    for a in e[1:]:
        if a == cur[-1] + 1: cur.append(a)
        else: out.append(len(cur)); cur = [a]
    return out + [len(cur)]
def Dof(m): b = blocks(m); return sum(b[i] * b[j] for i in range(len(b)) for j in range(i + 1, len(b)))
zE = comb(n + 1, 2)
zPi = {m: comb(bin(m).count('1') + 1, 2) for m in MASKS}
zL = {m: sum(k * (k + 1) // 2 for k in blocks(m)) for m in MASKS}
D = {m: Dof(m) for m in MASKS}
assert all(zPi[m] - zL[m] == D[m] for m in MASKS)
SMAX = max(D.values())
NORM = [tuple((1 if (m >> i) & 1 else 0) - ((m >> (n - 1)) & 1) for i in range(d)) for m in MASKS]
def bvec(s): return [zPi[m] - (0 if isint(m) else s) - (zE if (m >> (n - 1)) & 1 else 0) for m in MASKS]
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
def full(u): return tuple(u) + (zE - sum(u),)

def rank(rows):
    A = [list(r) for r in rows]; r = 0; cols = len(A[0]) if A else 0
    for c in range(cols):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = F(A[i][c], 1) / A[r][c]; A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
        if r == len(A): break
    return r
def affdim(pts):
    pts = list(pts); return rank([[a - b for a, b in zip(p, pts[0])] for p in pts[1:]]) if len(pts) > 1 else 0
def det(Mx):
    A = [list(map(F, r)) for r in Mx]; k = len(A); s = F(1)
    for c in range(k):
        p = next((i for i in range(c, k) if A[i][c] != 0), None)
        if p is None: return F(0)
        if p != c: A[c], A[p] = A[p], A[c]; s = -s
        s *= A[c][c]
        for i in range(c + 1, k):
            f = A[i][c] / A[c][c]; A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return s

# ---------- read candidates ----------
CANDS = []; ends = {F(0), F(SMAX)}
for line in open(CAND):
    v = list(map(int, line.split()))
    ms = v[:d]; dd = v[d]; P0 = v[d + 1:2 * d + 1]; P1 = v[2 * d + 1:3 * d + 1]; lo = F(v[3 * d + 1], v[3 * d + 2]); hi = F(v[3 * d + 3], v[3 * d + 4])
    CANDS.append((ms, dd, P0, P1, lo, hi)); ends.add(lo); ends.add(hi)
ends = sorted(ends)
STATIONS = sorted(set(ends) | {(a + b) / 2 for a, b in zip(ends, ends[1:])})
print(f'n={n}: {len(CANDS)} candidates, {len(ends)} interval end points {[str(e) for e in ends]}, {len(STATIONS)} stations, smax {SMAX}', flush=True)
K = len(STATIONS) + 2
def progress(k, what): print(f'PROGRESS {k}/{K} {what}  ({time.time() - T0:.1f} s)', flush=True)

def station(s):
    b = bvec(s); V = {}
    for ms, dd, P0, P1, lo, hi in CANDS:
        if lo <= s <= hi:
            u = tuple(F(p0, 1) / dd + s * F(p1, 1) / dd for p0, p1 in zip(P0, P1))
            if u not in V: V[u] = None
    V = sorted(V)
    for u in V: assert all(dot(NORM[k], u) >= b[k] for k in range(M))
    tight = [frozenset(k for k in range(M) if dot(NORM[k], u) == b[k]) for u in V]
    tv = {k: [i for i, t in enumerate(tight) if k in t] for k in range(M)}
    facets = {k: sum(1 << i for i in tv[k]) for k in range(M) if tv[k] and affdim(V[i] for i in tv[k]) == d - 1}
    # face lattice: closure of facet vertex sets under intersection; graded dims
    faces = set(facets.values()); front = list(faces)
    while front:
        nxt = []
        for f in front:
            for g in facets.values():
                h = f & g
                if h and h not in faces: faces.add(h); nxt.append(h)
        front = nxt
    faces = sorted(faces, key=lambda f: bin(f).count('1'))
    dim = {}
    for i, f in enumerate(faces):
        if bin(f).count('1') == 1: dim[f] = 0; continue
        dim[f] = 1 + max((dim[h] for h in faces[:i] if h & f == h and h != f), default=-1)
    assert all(dim[facets[k]] == d - 1 for k in facets)
    fv = [sum(1 for f in faces if dim[f] == k) for k in range(d)]
    assert fv[0] == len(V)
    euler = sum((-1) ** k * fv[k] for k in range(d)) == 1 - (-1) ** d
    vfac = [frozenset(k for k in facets if (facets[k] >> i) & 1) for i in range(len(V))]
    simple = all(len(x) == d for x in vfac)
    gp = True; badedges = []
    for f in faces:
        if dim[f] == 1:
            i, j = [k for k in range(len(V)) if (f >> k) & 1]
            dx = [a - c for a, c in zip(full(V[i]), full(V[j]))]; nz = [x for x in dx if x != 0]
            if not (len(nz) == 2 and nz[0] == -nz[1]):
                gp = False; badedges.append((i, j, dx))
    # independent confirmation that each such pair is an edge: the facets through both corners have normals of rank d - 1,
    # and no other corner lies on all of them
    conf = []
    for i, j, dx in badedges:
        com = sorted(vfac[i] & vfac[j])
        others = [k for k in range(len(V)) if k not in (i, j) and com and all((facets[c] >> k) & 1 for c in com)]
        conf.append(rank([list(NORM[c]) for c in com]) == d - 1 and not others)
    ex = None
    if badedges:
        i, j, dx = badedges[0]
        ex = dict(corner_a=[str(t) for t in full(V[i])], corner_b=[str(t) for t in full(V[j])], direction=[str(t) for t in dx],
                  facets_through_both=sorted(lab(MASKS[c]) for c in vfac[i] & vfac[j]))
    return dict(V=V, b=b, facets=facets, fv=fv, euler=euler, simple=simple, gp=gp, vfac=vfac, nongp_edges=len(badedges),
                nongp_confirmed=all(conf), nongp_example=ex)

def omega_vert(st, Y):
    tot = F(0)
    for s_ in st['vfac']:
        ks = sorted(s_); den = F(1)
        for k in ks: den *= dot(NORM[k], Y) - st['b'][k]
        tot += abs(det([NORM[k] for k in ks])) / den
    return tot

ROWS = []; C1 = True; first_bad = []
for q, s in enumerate(STATIONS):
    st = station(s)
    fac = {MASKS[k] for k in st['facets']}
    for m in MASKS:
        want = (s < D[m]) if not isint(m) else True
        if (m in fac) != want:
            C1 = False
            if len(first_bad) < 10: first_bad.append((lab(m), str(s), D[m], m in fac))
    ROWS.append(dict(s=str(s), f_vector=st['fv'], facets=len(fac), euler=st['euler'], simple=st['simple'], gp=st['gp'],
                     nongp_edges=st['nongp_edges'], nongp_confirmed=st['nongp_confirmed'], nongp_example=st['nongp_example'],
                     vanished_non_interval=sorted(lab(m) for m in MASKS if m not in fac)))
    if q == 0: PI = st
    if q == len(STATIONS) - 1: LO = st
    progress(q + 1, f's = {s}: f-vector {tuple(st["fv"])}, facets {len(fac)}, simple {st["simple"]}, gp {st["gp"]}, Euler {st["euler"]}')

# walls: stations where the structure differs from a neighbouring stretch
walls = []
for q in range(0, len(ROWS), 2):
    if q == 0: continue
    left, here = ROWS[q - 1], ROWS[q]; right = ROWS[q + 1] if q + 1 < len(ROWS) else here   # the end s = smax counts as a wall when the shape changes there
    key = lambda r: (tuple(r['f_vector']), tuple(r['vanished_non_interval']))
    if key(left) != key(here) or key(here) != key(right):
        walls.append(dict(s=here['s'], f_before=left['f_vector'], f_at=here['f_vector'], f_after=right['f_vector'],
                          vanish_here=sorted(set(here['vanished_non_interval']) - set(left['vanished_non_interval']))))
for w in walls: print(f'  wall s = {w["s"]}: {tuple(w["f_before"])} -> {tuple(w["f_at"])} (after {tuple(w["f_after"])}); facets vanishing: {", ".join(w["vanish_here"])}', flush=True)
Dvals = sorted({D[m] for m in MASKS if not isint(m)})
chk(f'C1 (Conjecture 1): every non-interval facet S present exactly for s < D_S, at all {len(STATIONS)} stations; interval facets always present', C1, first_bad)
chk(f'walls are exactly the values of D_S: {Dvals}', [w['s'] for w in walls] == [str(x) for x in Dvals], [w['s'] for w in walls])
chk('Euler relation at every station', all(r['euler'] for r in ROWS))
nongp = [(r['s'], r['nongp_edges']) for r in ROWS if not r['gp']]
print(f'  stations that are NOT generalized permutohedra (edges off the root directions e_i - e_j): {nongp}', flush=True)
for r in ROWS:
    if r['nongp_example']: print(f'    s = {r["s"]}: e.g. edge {r["nongp_example"]}', flush=True)
chk('every edge off the root directions is confirmed an edge independently (normals of the common facets have rank d - 1, no third corner on them)', all(r['nongp_confirmed'] for r in ROWS))
chk('start and end are generalized permutohedra (Pi, Loday)', ROWS[0]['gp'] and ROWS[-1]['gp'])
nonsimple = [r['s'] for r in ROWS if not r['simple']]
print(f'  non-simple stations: {nonsimple}', flush=True)
chk(f'start: n! = {factorial(n)} vertices, simple, all {M} facets', len(PI['V']) == factorial(n) and PI['simple'] and len(PI['facets']) == M)
cat = comb(2 * n, n) // (n + 1)
chk(f'end s = {SMAX}: Catalan({n}) = {cat} vertices, simple, exactly the {n * (n + 1) // 2 - 1} interval facets', len(LO['V']) == cat and LO['simple'] and {MASKS[k] for k in LO['facets']} == {m for m in MASKS if isint(m)})

# ---------- canonical forms at the centre ----------
progress(K - 1, 'canonical forms')
Y = tuple(F(n + 1, 2) for _ in range(d))
oc = F(2 ** (n - 1) * n, factorial(n - 1))
oPi = omega_vert(PI, Y)
flag = F(0)
for perm in itertools.permutations(range(1, n + 1)):
    term = F(1); S = set()
    for k in range(n - 1):
        S.add(perm[k]); term /= F(len(S) * (n + 1), 2) - comb(len(S) + 1, 2)
    flag += term
chk(f'C2 (Conjecture 2): Omega(Pi; centre) by the vertex formula = {oPi} = 2^(n-1) n/(n-1)! = {oc} = flag sum {flag}', oPi == oc == flag)
chk('control: every vertex cone of Pi is unimodular (|det| = 1)', all(abs(det([NORM[k] for k in sorted(v)])) == 1 for v in PI['vfac']))
N = n + 2
def triangulations(poly):
    if len(poly) < 3: return [frozenset()]
    a, b = poly[0], poly[-1]; out = []
    for k in range(1, len(poly) - 1):
        c = poly[k]
        for L in triangulations(poly[:k + 1]):
            for R in triangulations(poly[k:]):
                ds = set(L) | set(R)
                if k > 1: ds.add((a, c))
                if k < len(poly) - 2: ds.add((c, b))
                out.append(frozenset(ds))
    return out
TR = triangulations(list(range(1, N + 1)))
chk(f'control: Catalan({N - 2}) = {comb(2 * (N - 2), N - 2) // (N - 1)} triangulations of the {N}-gon', len(TR) == comb(2 * (N - 2), N - 2) // (N - 1) and len(set(TR)) == len(TR))
Yf = full(Y)
def Xd(i, j):   # diagonal (i, j) <-> interval [i, j - 2]
    I = sum(1 << (k - 1) for k in range(i, j - 1)); return sum(Yf[k - 1] for k in range(i, j - 1)) - zL[I]
def amp(drop=None):
    tot = F(0)
    for t, T in enumerate(sorted(TR, key=sorted)):
        if t == drop: continue
        den = F(1)
        for (i, j) in T: den *= Xd(i, j)
        tot += 1 / den
    return tot
mN = amp(); oL = omega_vert(LO, Y)
chk(f'C3: Omega(Loday; centre) by the vertex formula = {oL} = m_{N}(X = Loday facet values) = {mN}', oL == mN)
chk('negative: m_N with one tree dropped differs', amp(drop=0) != oL)
RES.update(stations=ROWS, walls=walls, D_values=Dvals, nonsimple_stations=nonsimple, omega_Pi_centre=str(oPi), closed_form=str(oc),
           omega_Loday_centre=str(oL), m_N=str(mN), N=N, candidates=len(CANDS), all_ok=OK)
json.dump(RES, open(OUT, 'w'), indent=1)
progress(K, 'json written')
print(f'n={n}: total {time.time() - T0:.1f} s', flush=True)
print('LINEB ok' if OK else 'LINEB FAIL', flush=True); sys.exit(0 if OK else 1)
