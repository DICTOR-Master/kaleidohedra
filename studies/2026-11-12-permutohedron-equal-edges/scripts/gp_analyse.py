"""Exact analysis of every equal-edged member found by gp_enum (one per symmetry orbit).

For each representative: rebuild its corners exactly from the 0/1 wall lengths (walking the chambers), check the walk closes,
find its faces from the fan's rays (exact support values), its edges (two faces meeting in two corners), check every edge has
squared length exactly 1, Euler, face kinds (regular or not), corner kinds; Minkowski structure: segment summands (all walls of
one root direction labelled 1), the core left when they are removed, atoms (no proper nonzero equal-edged summand, from gp_enum
sub), and an atom decomposition (exact cover of the walls). Positive controls: the seven Wythoff solids of each group and #49's
named shapes that lie in these cones are rebuilt independently and must be found and named; negative controls are in gp_setup.

Usage: gp_analyse.py DATADIR NPROC  (reads DATADIR/{A3,B3,H3}.reps and .sub; writes DATADIR/members-*.json, summary.json)
"""
import sys, os, json, time, itertools
from fractions import Fraction as Fr
import multiprocessing
Pool = multiprocessing.get_context("fork").Pool
sys.path.insert(0, os.path.dirname(__file__))
from coxeter import QF, Fan, dot, vsub, vadd, vscale, vkey, rank, matvec, cross

DATA, NPROC = sys.argv[1], int(sys.argv[2])
t0 = time.time()
checks = []


SOFT = False   # pilot only (GP_LIMIT on H3): completeness-dependent checks are reported, not counted


def chk(name, ok):
    if SOFT and not ok:
        print(f'CHECK pilot-skip {name}', flush=True)
        return
    checks.append((name, bool(ok)))
    print(f'CHECK {"ok  " if ok else "FAIL"} {name}', flush=True)


ARCH = {  # Platonic and Archimedean (non-snub), counts of n-gons
    'tetrahedron': {3: 4}, 'cube': {4: 6}, 'octahedron': {3: 8}, 'dodecahedron': {5: 12}, 'icosahedron': {3: 20},
    'cuboctahedron': {3: 8, 4: 6}, 'truncated tetrahedron': {3: 4, 6: 4}, 'truncated octahedron': {4: 6, 6: 8},
    'truncated cube': {3: 8, 8: 6}, 'rhombicuboctahedron': {3: 8, 4: 18}, 'truncated cuboctahedron': {4: 12, 6: 8, 8: 6},
    'icosidodecahedron': {3: 20, 5: 12}, 'truncated icosahedron': {5: 12, 6: 20}, 'truncated dodecahedron': {3: 20, 10: 12},
    'rhombicosidodecahedron': {3: 20, 4: 30, 5: 12}, 'truncated icosidodecahedron': {4: 30, 6: 20, 10: 12}}
JOHNSON = {  # face counts of the Johnson solids that can carry these face kinds (names checked by corner kinds where counts clash)
    'J1 square pyramid': {3: 4, 4: 1}, 'J2 pentagonal pyramid': {3: 5, 5: 1}, 'J3 triangular cupola': {3: 4, 4: 3, 6: 1},
    'J4 square cupola': {3: 4, 4: 5, 8: 1}, 'J5 pentagonal cupola': {3: 5, 4: 5, 5: 1, 10: 1}, 'J6 pentagonal rotunda': {3: 10, 5: 6, 10: 1},
    'J7 elongated triangular pyramid': {3: 4, 4: 3}, 'J8 elongated square pyramid': {3: 4, 4: 5},
    'J11 gyroelongated pentagonal pyramid (diminished icosahedron)': {3: 15, 5: 1},
    'J14 elongated triangular bipyramid': {3: 6, 4: 3}, 'J15 elongated square bipyramid': {3: 8, 4: 4},
    'J18 elongated triangular cupola': {3: 4, 4: 9, 6: 1}, 'J19 elongated square cupola': {3: 4, 4: 13, 8: 1},
    'J20 elongated pentagonal cupola': {3: 5, 4: 15, 5: 1, 10: 1}, 'J21 elongated pentagonal rotunda': {3: 10, 4: 10, 5: 6, 10: 1},
    'J27 triangular orthobicupola': {3: 8, 4: 6}, 'J28/J29 square ortho/gyrobicupola': {3: 8, 4: 10},
    'J30/J31 pentagonal ortho/gyrobicupola': {3: 10, 4: 10, 5: 2}, 'J32/J33 pentagonal ortho/gyrocupolarotunda': {3: 15, 4: 5, 5: 7},
    'J34 pentagonal orthobirotunda': {3: 20, 5: 12}, 'J35/J36 elongated triangular ortho/gyrobicupola': {3: 8, 4: 12},
    'J37 elongated square gyrobicupola': {3: 8, 4: 18}, 'J38/J39 elongated pentagonal ortho/gyrobicupola': {3: 10, 4: 20, 5: 2},
    'J62 metabidiminished icosahedron': {3: 10, 5: 2}, 'J63 tridiminished icosahedron': {3: 5, 5: 3},
    'J65 augmented truncated tetrahedron': {3: 8, 4: 3, 6: 3}, 'J66 augmented truncated cube': {3: 12, 4: 5, 8: 5},
    'J67 biaugmented truncated cube': {3: 16, 4: 10, 8: 4}, 'J68 augmented truncated dodecahedron': {3: 25, 4: 5, 5: 1, 10: 11},
    'J69/J70 para/metabiaugmented truncated dodecahedron': {3: 30, 4: 10, 5: 2, 10: 10},
    'J71 triaugmented truncated dodecahedron': {3: 35, 4: 15, 5: 3, 10: 9},
    'J72-J75 gyrate rhombicosidodecahedra': {3: 20, 4: 30, 5: 12},
    'J76 diminished rhombicosidodecahedron (or J77-J79)': {3: 15, 4: 25, 5: 11, 10: 1},
    'J80/J81 bidiminished rhombicosidodecahedron (or J82)': {3: 10, 4: 20, 5: 10, 10: 2},
    'J83 tridiminished rhombicosidodecahedron': {3: 5, 4: 15, 5: 9, 10: 3}}


def fan_data(name):
    F = Fan(name)
    G = F.sym_group()
    perms = [F.wall_perm(X) for X in G]
    return F, G, perms


def canon(bits, perms):
    best, stab = None, 0
    for p in perms:
        im = 0
        b, e = bits, 0
        while b:
            if b & 1:
                im |= 1 << p[e]
            b >>= 1
            e += 1
        if best is None or im < best:
            best = im
    return best


def orbit(bits, perms):
    out = set()
    for p in perms:
        im = 0
        for e in range(len(p)):
            if bits >> e & 1:
                im |= 1 << p[e]
        out.add(im)
    return out


_F = None


def init(name):
    global _F
    _F = Fan(name)


def build(bits):
    """exact corners from 0/1 wall lengths; returns (corners, closes)"""
    F = _F
    C = len(F.W)
    V = [None] * C
    V[0] = (QF(0), QF(0), QF(0))
    stack, ok = [0], True
    while stack:
        c = stack.pop()
        for i in range(3):
            d = F.nb[c][i]
            w = F.wallidx[(min(c, d), max(c, d))]
            r = F.walls[w][3] if F.walls[w][0] == c else tuple(-x for x in F.walls[w][3])
            vd = vsub(V[c], r) if bits >> w & 1 else V[c]
            if V[d] is None:
                V[d] = vd
                stack.append(d)
            elif vkey(V[d]) != vkey(vd):
                ok = False
    pts = {}
    for v in V:
        pts[vkey(v)] = v
    return list(pts.values()), ok


def ang(a, b, c):
    import math
    u = [float(x) for x in vsub(a, b)]
    v = [float(x) for x in vsub(c, b)]
    return math.degrees(math.acos(max(-1, min(1, sum(x * y for x, y in zip(u, v)) / (sum(x * x for x in u) * sum(x * x for x in v)) ** .5))))


def analyse(args):
    idx, bits, orb = args
    F = _F
    P, closes = build(bits)
    d = rank([vsub(v, P[0]) for v in P[1:]]) if len(P) > 1 else 0
    res = dict(id=idx, bits=format(bits, 'x'), orbit=orb, dim=d, corners=len(P), closes=closes,
               used_roots=sorted({F.wallroot[w] for w in range(len(F.walls)) if bits >> w & 1}))
    if d < 3:
        if d == 2:
            res['polygon'] = len(P)
            c = vscale(QF(Fr(1, len(P))), tuple(sum((v[k] for v in P), QF(0)) for k in range(3)))
            res['regular'] = len({dot(vsub(v, c), vsub(v, c)).key() for v in P}) == 1
        return res
    faces = []
    for r in F.rays:
        h = max(dot(v, r) for v in P)
        S = [k for k, v in enumerate(P) if dot(v, r) == h]
        if len(S) >= 3 and rank([vsub(P[k], P[S[0]]) for k in S[1:]]) == 2:
            faces.append(S)
    edges = set()
    for a, b in itertools.combinations(range(len(faces)), 2):
        s = set(faces[a]) & set(faces[b])
        if len(s) == 2:
            edges.add(tuple(sorted(s)))
        assert len(s) <= 2
    V, E, Fn = len(P), len(edges), len(faces)
    lens = {dot(vsub(P[a], P[b]), vsub(P[a], P[b])).key() for a, b in edges}
    res.update(V=V, E=E, F=Fn, euler=V - E + Fn == 2, all_edges_1=lens == {(Fr(1), Fr(0))})
    # face kinds
    kinds = {}
    fdesc = []
    regular_all = True
    adj = {k: set() for k in range(V)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    for S in faces:
        n = len(S)
        c = vscale(QF(Fr(1, n)), tuple(sum((P[k][j] for k in S), QF(0)) for j in range(3)))
        reg = len({dot(vsub(P[k], c), vsub(P[k], c)).key() for k in S}) == 1
        regular_all &= reg
        # cyclic order via edges within the face
        Sset = set(S)
        cyc = [S[0]]
        while len(cyc) < n:
            nxt = [x for x in adj[cyc[-1]] if x in Sset and x not in cyc]
            cyc.append(nxt[0])
        angs = sorted(round(ang(P[cyc[k - 1]], P[cyc[k]], P[cyc[(k + 1) % n]]), 1) for k in range(n))
        key = f'{n}-gon regular' if reg else f'{n}-gon ' + '/'.join(f'{x:g}' for x in sorted(set(angs)))
        kinds[key] = kinds.get(key, 0) + 1
        fdesc.append(n)
    res['face_kinds'] = dict(sorted(kinds.items()))
    res['regular_faced'] = regular_all
    cnt = {}
    for n in fdesc:
        cnt[n] = cnt.get(n, 0) + 1
    res['ngon_counts'] = {str(k): v for k, v in sorted(cnt.items())}
    vconf = {}
    for k in range(V):
        conf = tuple(sorted(len(S) for S in faces if k in S))
        vconf[conf] = vconf.get(conf, 0) + 1
    res['corner_kinds'] = {'.'.join(map(str, k)): v for k, v in sorted(vconf.items())}
    DM = [[None] * V for _ in range(V)]
    for a in range(V):
        for b in range(a, V):
            x = vsub(P[a], P[b])
            DM[a][b] = DM[b][a] = dot(x, x).key()
    profs = {tuple(sorted(DM[a])) for a in range(V)}
    res['corner_profiles'] = len(profs)
    inv = sorted(DM[a][b] for a in range(V) for b in range(a + 1, V))
    res['invariant'] = str(hash(tuple(inv)))
    name = None
    if regular_all:
        for nm, c in ARCH.items():
            if cnt == c and len(profs) == 1:
                name = nm
        if name is None:
            ks = sorted(cnt)
            if len(cnt) == 2 and 4 in cnt and cnt.get(ks[-1] if ks[-1] != 4 else ks[0]) == 2:
                n = ks[-1] if ks[-1] != 4 else ks[0]
                if cnt[4] == n and len(profs) == 1:
                    name = f'{n}-gonal prism'
        if name is None:
            for nm, c in JOHNSON.items():
                if cnt == c:
                    name = nm
        if name is None:
            name = 'regular-faced, not in the table'
    res['name'] = name
    return res


def wythoff(F, S):
    p = tuple(sum((F.om[i][k] * QF(Fr(1, 2)) for i in S), QF(0)) for k in range(3))
    pts = {}
    for g in F.W:
        v = matvec(g, p)
        pts[vkey(v)] = v
    return list(pts.values())


def lbits(F, verts):
    l = F.lengths(F.support(verts))
    if not all(x == QF(0) or x == QF(1) for x in l):
        return None
    return sum(1 << e for e, x in enumerate(l) if x == QF(1))


def minkowski(A, B):
    pts = {}
    for a in A:
        for b in B:
            v = vadd(a, b)
            pts[vkey(v)] = v
    return list(pts.values())


def congruent(A, B):
    """exact: is there an isometry taking corner set A onto corner set B?"""
    if len(A) != len(B):
        return False
    def centre(P):
        n = QF(Fr(1, len(P)))
        c = tuple(sum((v[k] for v in P), QF(0)) * n for k in range(3))
        return [vsub(v, c) for v in P]
    A, B = centre(A), centre(B)
    Bset = {vkey(v) for v in B}
    a = [A[0]]
    for v in A[1:]:
        if len(a) < 3 and rank(a + [v]) == len(a) + 1:
            a.append(v)
    na = [dot(x, x) for x in a]
    ga = [dot(a[i], a[j]) for i in range(3) for j in range(3)]
    cand = [[v for v in B if dot(v, v) == na[i]] for i in range(3)]
    from coxeter import inv3
    Ai = inv3(tuple(a))          # rows a_i; Ai has columns = dual basis
    for b0 in cand[0]:
        for b1 in cand[1]:
            if dot(b0, b1) != ga[1]:
                continue
            for b2 in cand[2]:
                if dot(b0, b2) != ga[2] or dot(b1, b2) != ga[5]:
                    continue
                b = (b0, b1, b2)
                # M = sum_i b_i (dual_i)^T, dual_i = column i of Ai
                def M(x):
                    co = [sum((Ai[k][i] * x[k] for k in range(3)), QF(0)) for i in range(3)]
                    return tuple(sum((co[i] * b[i][k] for i in range(3)), QF(0)) for k in range(3))
                if all(vkey(M(v)) in Bset for v in A):
                    return True
    return False


summary = {}
for name in ['A3', 'B3', 'H3']:
    F, G, perms = fan_data(name)
    E = len(F.walls)
    reps, tot = [], [0] * 9
    for fn in sorted(os.listdir(DATA)):
        if fn.startswith(name + '.reps'):
            for line in open(os.path.join(DATA, fn)):
                p = line.split()
                if p[0] == 'R':
                    reps.append((int(p[1]), int(p[2]), int(p[3], 16)))
                elif p[0] == 'T':
                    tot = [a + int(b) for a, b in zip(tot, p[1:])]
    reps.sort(key=lambda r: (r[0], bin(r[2]).count('1'), r[2]))
    LIM = int(os.environ.get('GP_LIMIT', '0'))
    if LIM and name == 'H3':
        reps = reps[:LIM]
        SOFT = True
    chk(f'{name} orbit sizes add up to the solution count ({tot[0]})', sum(r[1] for r in reps) == tot[0])
    chk(f'{name} representatives are distinct and canonical', len({r[2] for r in reps}) == len(reps) and all(canon(r[2], perms) == r[2] for r in reps[:400]))
    # atoms from gp_enum sub (cap 3): number of members P <= Q, counting 0 and Q
    subc = {}
    for line in open(os.path.join(DATA, name + '.sub')):
        p = line.split()
        if p[0] == 'C':
            subc[int(p[1])] = p[2]
    repbits_file = [int(l.strip(), 16) for l in open(os.path.join(DATA, name + '.repbits')) if l.strip()]
    atom_of = {b: subc[i] == '2' for i, b in enumerate(repbits_file)}
    with Pool(NPROC, initializer=init, initargs=(name,)) as pool:
        out = pool.map(analyse, [(k, r[2], r[1]) for k, r in enumerate(reps)], chunksize=8)
    print(f'PROGRESS {(["A3","B3","H3"].index(name)+0.7)/3:.3f} {name} exact rebuild of {len(out)} reps ({time.time()-t0:.0f}s)', flush=True)
    byb = {r[2]: k for k, r in enumerate(reps)}
    chk(f'{name} every member rebuilds exactly (chamber walk closes)', all(m['closes'] for m in out))
    chk(f'{name} dimension from root ranks (C, float-free table) = exact corner rank', all(m['dim'] == r[0] for m, r in zip(out, reps)))
    sol = [m for m in out if m['dim'] == 3]
    chk(f'{name} every solid: Euler holds and every edge has squared length exactly 1', all(m['euler'] and m['all_edges_1'] for m in sol))
    # segment summands, core, atoms
    rootwalls = {}
    for w in range(E):
        rootwalls.setdefault(F.wallroot[w], 0)
        rootwalls[F.wallroot[w]] |= 1 << w
    atoms = [r[2] for r in reps if atom_of[r[2]] and r[2] != 0]
    atom_imgs = []
    for a in atoms:
        for im in orbit(a, perms):
            atom_imgs.append((im, byb[a]))
    for m, r in zip(out, reps):
        b = r[2]
        m['atom'] = atom_of[b] and b != 0
        segs = [k for k, rw in rootwalls.items() if b & rw == rw]
        m['segments'] = len(segs)
        core = b
        for k in segs:
            core &= ~rootwalls[k]
        cc = canon(core, perms)
        m['core'] = byb.get(cc)
        m['core_dim'] = out[m['core']]['dim'] if m['core'] is not None else -1
    # atom decomposition (one exact cover of the walls by atom images) for the solids
    def cover(b):
        if b == 0:
            return []
        low = b & -b
        for im, aid in atom_imgs:
            if im & low and im & b == im:
                rest = cover(b & ~im)
                if rest is not None:
                    return [aid] + rest
        return None
    for m, r in zip(out, reps):
        if m['dim'] == 3:
            dec = cover(r[2])
            m['atoms_in'] = sorted(dec) if dec is not None else None
    chk(f'{name} every solid splits into atoms exactly', all(m['atoms_in'] is not None for m in sol))
    # names for atoms and cores
    def label(k):
        m = out[k]
        if m['dim'] == 0:
            return 'point'
        if m['dim'] == 1:
            return 'segment'
        if m['dim'] == 2:
            return ('regular ' if m['regular'] else 'equal-edged ') + {3: 'triangle', 4: 'rhombus', 5: 'pentagon', 6: 'hexagon', 8: 'octagon', 10: 'decagon'}.get(m['polygon'], f"{m['polygon']}-gon")
        return m['name'] or f'{name}-{k}'
    for m in out:
        m['label'] = label(m['id'])
    # classes
    for m in sol:
        if m['regular_faced']:
            m['class'] = 'regular-faced (known: ' + m['name'] + ')'
        elif m['core_dim'] == 0:
            m['class'] = 'zonohedron'
        elif m['segments'] > 0:
            m['class'] = '#49 stretch: core ' + (out[m['core']]['label'] if m['core'] is not None else '?') + f" + {m['segments']} segment(s)"
        else:
            parts = [out[a] for a in m['atoms_in']]
            if any(p['dim'] == 2 and p['polygon'] == 3 for p in parts) or any(p.get('name') == 'tetrahedron' for p in parts):
                m['class'] = 'cap type (#49 corollary): ' + ' + '.join(out[a]['label'] for a in m['atoms_in'])
            else:
                m['class'] = 'beyond #49: ' + ' + '.join(out[a]['label'] for a in m['atoms_in'])
    # positive controls: Wythoff solids and #49 named shapes, built independently, must be found and named
    WN = {'A3': {(0,): 'tetrahedron', (1,): 'octahedron', (2,): 'tetrahedron', (0, 1): 'truncated tetrahedron', (1, 2): 'truncated tetrahedron',
                 (0, 2): 'cuboctahedron', (0, 1, 2): 'truncated octahedron'},
          'B3': {(0,): 'octahedron', (1,): 'cuboctahedron', (2,): 'cube', (0, 1): 'truncated octahedron', (1, 2): 'truncated cube',
                 (0, 2): 'rhombicuboctahedron', (0, 1, 2): 'truncated cuboctahedron'},
          'H3': {(0,): 'dodecahedron', (1,): 'icosidodecahedron', (2,): 'icosahedron', (0, 1): 'truncated dodecahedron', (1, 2): 'truncated icosahedron',
                 (0, 2): 'rhombicosidodecahedron', (0, 1, 2): 'truncated icosidodecahedron'}}[name]
    for S, nm in WN.items():
        b = lbits(F, wythoff(F, S))
        k = byb.get(canon(b, perms)) if b is not None else None
        chk(f'{name} positive control: Wythoff {S} built independently is found and named {nm}', k is not None and out[k]['name'] == nm)
    ctrl = []
    if name == 'A3':
        T = wythoff(F, (0,))
        Tm = [vscale(QF(-1), v) for v in T]
        O = wythoff(F, (1,))
        ctrl += [('#49: tetrahedron with four caps (T + reversed T)', minkowski(T, Tm), 'cuboctahedron')]
        for Tx, tag in ((T, 'T'), (Tm, 'reversed T')):
            b = lbits(F, minkowski(O, Tx))
            if b is not None:
                ctrl += [(f'#49: octahedron with four caps (O + {tag})', minkowski(O, Tx), 'truncated tetrahedron')]
        # three caps: T + a face triangle of the reversed T (triangle turned against the base)
        r0 = F.rays[0]
        hmax = max(dot(v, r0) for v in Tm)
        face = [v for v in Tm if dot(v, r0) == hmax]
        if len(face) != 3:
            hmin = min(dot(v, r0) for v in Tm)
            face = [v for v in Tm if dot(v, r0) != hmin]
        for tri in (face, [vscale(QF(-1), v) for v in face]):
            if lbits(F, minkowski(T, tri)) is not None:
                ctrl += [('#49: tetrahedron with three caps on a triangle (T + triangle)', minkowski(T, tri), 'J3 triangular cupola')]
                break
    if name == 'B3':
        O = wythoff(F, (0,))
        C = wythoff(F, (2,))
        TO = wythoff(F, (0, 1))
        ez = [(QF(0), QF(0), QF(0)), (QF(0), QF(0), QF(1))]
        s2 = QF(0, Fr(1, 2))
        fd = [(QF(0), QF(0), QF(0)), (s2, s2, QF(0))]
        ctrl += [('#49: octahedron stretched through a corner', minkowski(O, ez), 'J15 elongated square bipyramid'),
                 ('#49: cube stretched along a face diagonal', minkowski(C, fd), None),
                 ('truncated octahedron stretched along a four-fold axis', minkowski(TO, ez), None)]
    for desc, verts, nm in ctrl:
        b = lbits(F, verts)
        k = byb.get(canon(b, perms)) if b is not None else None
        ok = k is not None and out[k]['dim'] == 3 and (nm is None or out[k]['name'] == nm)
        chk(f'{name} positive control: {desc} is found' + (f' and named {nm}' if nm else '') +
            (f" [{out[k]['class']}; {out[k]['face_kinds']}]" if k is not None else ''), ok)
        if k is not None:
            out[k].setdefault('controls', []).append(desc)
    # congruence: distinct orbits must have distinct invariants
    invs = {}
    for m in sol:
        invs.setdefault(m['invariant'], []).append(m['id'])
    coll = [v for v in invs.values() if len(v) > 1]
    init(name)
    proved = all(congruent(build(reps[v[0]][2])[0], build(reps[w][2])[0]) for v in coll for w in v[1:])
    for v in coll:
        for w in v[1:]:
            out[w]['same_solid_as'] = v[0]
    chk(f'{name} orbits with equal distance invariants are proved congruent ({len(coll)} such groups: one solid in two orientations)', proved)
    nsolids = len(invs)
    classes = {}
    for m in sol:
        c = m['class'].split(':')[0].split(' (')[0]
        classes[c] = classes.get(c, 0) + 1
    named = sorted({m['name'] for m in sol if m['name']})
    summary[name] = dict(solutions=tot[0], solutions_by_dim=tot[1:5], orbits_by_dim=tot[5:9], solid_orbits=len(sol), distinct_solids=nsolids,
                         classes=classes, named=named, atoms=[dict(id=m['id'], label=m['label'], dim=m['dim'], V=m.get('V'), face_kinds=m.get('face_kinds')) for m in out if m['atom']])
    json.dump(out, open(os.path.join(DATA, f'members-{name}.json'), 'w'), indent=0)
    print(f'{name} SUMMARY {json.dumps(summary[name])}', flush=True)
    print(f'PROGRESS {(["A3","B3","H3"].index(name)+1)/3:.3f} {name} done ({time.time()-t0:.0f}s)', flush=True)

if 'B3' in summary and not os.environ.get('GP_LIMIT'):
    ia = {m['invariant'] for m in json.load(open(os.path.join(DATA, 'members-A3.json'))) if m['dim'] == 3}
    ib = {m['invariant'] for m in json.load(open(os.path.join(DATA, 'members-B3.json'))) if m['dim'] == 3}
    chk(f'every A3 solid reappears among the B3 solids (B3 fan refines the A3 fan): {len(ia & ib)} of {len(ia)}', ia <= ib)
json.dump(dict(summary=summary, checks=checks), open(os.path.join(DATA, 'summary.json'), 'w'), indent=1)
bad = [n for n, ok in checks if not ok]
print(f'analysis checks {len(checks)-len(bad)}/{len(checks)} ok')
if bad:
    print('ANALYSIS FAIL', bad)
    sys.exit(1)
