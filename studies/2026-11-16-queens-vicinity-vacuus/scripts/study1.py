#!/usr/bin/env python3
"""STUDY 1 (DICTO 16 Nov 2026): re-evaluate as a Vacuus every shape found in or near the Queens.
For each shape: plates (central hyperplanes of its 2-faces, or of its edges for 3D slices/shadows), heart or non-heart,
and how many plates are mirror walls, cross walls or no wall of the Queens. All plate counts and wall matches exact in
Q(sqrt5) (see qv_lib). Output data/study1.json; final line FINAL ok only if every control passes.
usage: python3 study1.py [part ...]   parts: controls wythoff stations special koca atlas600 atlas120 hopscotch ab
"""
import sys, json, random, time, itertools
from fractions import Fraction as Fr
from qv_lib import *   # noqa: F401,F403
import qv_lib as L

OUT = {}
CHECKS = []
T0 = time.time()


def check(name, ok):
    CHECKS.append((name, bool(ok)))
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)


def show(rec):
    print(f"  {rec['name']}: V{rec['V']} plates {rec['plates']} {rec['kind']} | mirror {rec['plates_mirror']} cross "
          f"{rec['plates_cross']} none {rec['plates_none']} -> {rec['hidden']}  ({time.time() - T0:.0f}s)", flush=True)
    return rec


# ------------------------------------------------------------------ W(H4) as permutations of the 600-cell's corners
IDX = {key(v): i for i, v in enumerate(V600)}


def perm_of_reflection(a):
    return tuple(IDX[key(reflect(v, a))] for v in V600)


def group(gens):
    e = tuple(range(len(V600))); seen = {e}; todo = [e]
    while todo:
        g = todo.pop()
        for s in gens:
            h = tuple(s[i] for i in g)
            if h not in seen:
                seen.add(h); todo.append(h)
    return seen


def stabiliser(G, S):
    S = frozenset(S); return [g for g in G if frozenset(g[i] for i in S) == S]


def orbits_on(G, n, act):
    par = list(range(n))
    def f(i):
        while par[i] != i:
            par[i] = par[par[i]]; i = par[i]
        return i
    for g in G:
        for i in range(n):
            a, b = f(i), f(act(g, i))
            if a != b:
                par[a] = b
    out = {}
    for i in range(n):
        out.setdefault(f(i), []).append(i)
    return sorted(out.values(), key=lambda o: (len(o), o))


CELLKEY = {tuple(sorted(c)): i for i, c in enumerate(CELLS600)}


def cell_perm(g):
    return [CELLKEY[tuple(sorted(g[i] for i in c))] for c in CELLS600]


BASIS = None


def matrix_of(g):
    """exact 4x4 matrix M with M v_i = v_g(i) (rows of M acting on column vectors)."""
    global BASIS
    if BASIS is None:
        for comb in itertools.combinations(range(len(V600)), 4):
            if abs(np.linalg.det(np.array([fl(V600[i]) for i in comb]))) > 1e-6:
                BASIS = comb; break
    B = [V600[i] for i in BASIS]; I = [V600[g[i]] for i in BASIS]
    # M B^T = I^T  ->  for each row r of M: B r = (I_k[r])_k
    return [solve(B, tuple(I[k][r] for k in range(4))) for r in range(4)]


def apply(M, x):
    return tuple(dot(M[r], x) for r in range(4))


# ------------------------------------------------------------------ parts
def part_controls():
    r600 = show(vacuus4(V600, '600-cell (White Queen; Schlafli 1852)'))
    r120 = show(vacuus4(C600, '120-cell (Red Queen; Schlafli 1852)'))
    check('control 600-cell: 60 plates, all mirror walls, heart', r600['plates'] == 60 and r600['plates_mirror'] == 60 and r600['kind'] == 'heart' and r600['F3'] == 600)
    check('control 120-cell: 60 plates, all mirror walls, heart', r120['plates'] == 60 and r120['plates_mirror'] == 60 and r120['kind'] == 'heart' and r120['F3'] == 120)
    # negative control 1: every corner of the 600-cell moved by a small exact rational step (a perturbed member)
    rnd = random.Random(16112026)
    Vp = [tuple(x + Q5(Fr(rnd.randint(-40, 40), 1000)) for x in v) for v in V600]
    rp = show(vacuus4(Vp, 'perturbed 600-cell (control)'))
    check('negative control perturbed 600-cell: mostly no wall (>90% of plates)', rp['plates_none'] > 0.9 * rp['plates'])
    # negative control 2: the 600-cell turned by a generic exact rational rotation (Cayley transform)
    K = [[Fr(0), Fr(1, 3), Fr(-2, 7), Fr(1, 5)], [Fr(-1, 3), Fr(0), Fr(1, 4), Fr(-3, 11)], [Fr(2, 7), Fr(-1, 4), Fr(0), Fr(2, 9)], [Fr(-1, 5), Fr(3, 11), Fr(-2, 9), Fr(0)]]
    Iq = [[Q5(1 if i == j else 0) for j in range(4)] for i in range(4)]
    IpK = [[Iq[i][j] + Q5(K[i][j]) for j in range(4)] for i in range(4)]
    ImK = [[Iq[i][j] - Q5(K[i][j]) for j in range(4)] for i in range(4)]
    # Q = (I-K)(I+K)^-1 ; rotate v -> Q v : solve (I+K) y = v, then x = (I-K) y
    def rot(v):
        y = solve(IpK, v); return tuple(sum((ImK[i][j] * y[j] for j in range(4)), ZERO) for i in range(4))
    Vr = [rot(v) for v in V600]
    check('rotation is exact and orthogonal', all(dot(a, a) == dot(b, b) for a, b in zip(Vr[:10], V600[:10])) and dot(Vr[0], Vr[1]) == dot(V600[0], V600[1]))
    rr = show(vacuus4(Vr, 'turned 600-cell (control)'))
    check('negative control turned 600-cell: heart, 60 plates, none on the Queens walls', rr['plates'] == 60 and rr['plates_none'] == 60 and rr['kind'] == 'heart')
    OUT['controls'] = [r600, r120, rp, rr]


WY = [((1, 0, 0, 0), '120-cell'), ((0, 1, 0, 0), 'rectified 120-cell'), ((0, 0, 1, 0), 'rectified 600-cell'),
      ((0, 0, 0, 1), '600-cell'), ((1, 1, 0, 0), 'truncated 120-cell'), ((1, 0, 1, 0), 'cantellated 120-cell'),
      ((1, 0, 0, 1), 'runcinated 120-cell'), ((0, 1, 1, 0), 'bitruncated 120-cell'), ((0, 1, 0, 1), 'cantellated 600-cell'),
      ((0, 0, 1, 1), 'truncated 600-cell'), ((1, 1, 1, 0), 'cantitruncated 120-cell'), ((1, 1, 0, 1), 'runcitruncated 120-cell'),
      ((1, 0, 1, 1), 'runcitruncated 600-cell'), ((0, 1, 1, 1), 'cantitruncated 600-cell'), ((1, 1, 1, 1), 'omnitruncated 120-cell')]
KNOWN_V = {'120-cell': 600, 'rectified 120-cell': 1200, 'rectified 600-cell': 720, '600-cell': 120, 'truncated 120-cell': 2400,
           'cantellated 120-cell': 3600, 'runcinated 120-cell': 2400, 'bitruncated 120-cell': 3600, 'cantellated 600-cell': 3600,
           'truncated 600-cell': 1440, 'cantitruncated 120-cell': 7200, 'runcitruncated 120-cell': 7200,
           'runcitruncated 600-cell': 7200, 'cantitruncated 600-cell': 7200, 'omnitruncated 120-cell': 14400}
KNOWN_C = {'120-cell': 120, 'rectified 120-cell': 720, 'rectified 600-cell': 720, '600-cell': 600, 'truncated 120-cell': 720,
           'cantellated 120-cell': 1920, 'runcinated 120-cell': 2640, 'bitruncated 120-cell': 720, 'cantellated 600-cell': 1440,
           'truncated 600-cell': 720, 'cantitruncated 120-cell': 1920, 'runcitruncated 120-cell': 2640,
           'runcitruncated 600-cell': 2640, 'cantitruncated 600-cell': 1440, 'omnitruncated 120-cell': 2640}


def part_wythoff():
    res = []
    for lam, nm in WY:
        V = wythoff(lam)
        r = vacuus4(V, f'{nm} {lam}')
        r['seed'] = lam; show(r); res.append(r)
        check(f'{nm}: {KNOWN_V[nm]} corners, {KNOWN_C[nm]} cells, Euler 0', r['V'] == KNOWN_V[nm] and r['F3'] == KNOWN_C[nm] and r['euler'] == 0)
    OUT['wythoff'] = res


def chain_components(J):
    J = sorted(J); comps = [[J[0]]]
    for j in J[1:]:
        if j == comps[-1][-1] + 1:
            comps[-1].append(j)
        else:
            comps.append([j])
    return comps


def part_stations():
    """Exact law for the whole Wythoff family (every seed, not only the uniform ones): which face types lie on mirror walls
    and which on cross walls. Face type J = 2 nodes; its plate is span(x, alpha_J). A wall with normal w (w = sum c_i alpha_i,
    c_i = w.omega_i) contains it iff w.alpha_j = 0 (j in J) and sum_{i in R} lambda_i c_i = 0 over the ringed nodes R."""
    dirs = {'mirror': [canon(v) for v in {key(canon(v)): canon(v) for v in V600}.values()],
            'cross': [canon(c) for c in {key(canon(c)): canon(c) for c in C600}.values()]}
    rows = []; mirror_law_ok = True
    for lam, nm in WY:
        R = [i for i in range(4) if lam[i]]
        for J in itertools.combinations(range(4), 2):
            if not all(any(i in R for i in comp) for comp in chain_components(J)):
                continue
            row = {'shape': nm, 'seed': lam, 'face_type': [j + 1 for j in J]}
            for kind, D in dirs.items():
                uni, fam, sta = 0, 0, []
                for w in D:
                    if not all(dot(w, ALPHA[j]).iszero() for j in J):
                        continue
                    c = [dot(w, OMEGA[i]) for i in range(4)]
                    cR = [c[i] for i in R]
                    if all(x.iszero() for x in cR):
                        fam += 1; uni += 1
                    else:
                        sg = {x.sign() for x in cR if not x.iszero()}
                        if sum(cR, ZERO).iszero():
                            uni += 1
                        if len(sg) == 2:
                            # a station: seeds with sum lambda_i c_i = 0 (one ratio when |R| = 2)
                            if len(R) == 2:
                                ratio = -cR[1] / cR[0]   # lambda_R0 : lambda_R1 = ratio : 1 ... solve l0 c0 + l1 c1 = 0 -> l0/l1 = -c1/c0
                                sta.append(ratio)
                            else:
                                sta.append('codim-1 family')
                row[kind] = {'walls_all_seeds': fam, 'walls_uniform_seed': uni,
                             'stations': sorted({str(s) if isinstance(s, str) else q5str(s) for s in sta})}
                if kind == 'mirror':
                    # Mirror Law (#107 Theorem 1): on mirrors iff a root of the unringed nodes is orthogonal to alpha_J
                    law = any(all(dot(w, ALPHA[j]).iszero() for j in J) and all(dot(w, OMEGA[i]).iszero() for i in R) for w in D)
                    mirror_law_ok &= (law == (fam > 0)) and not sta
            rows.append(row)
    check('Mirror Law reproduced for every face type of the 15 (and roots never give stations)', mirror_law_ok)
    OUT['stations'] = rows
    for r in rows:
        if r['cross']['walls_uniform_seed'] or r['cross']['stations'] or r['cross']['walls_all_seeds']:
            print('  cross:', r['shape'], 'type', r['face_type'], r['cross'], flush=True)


def part_special():
    res = []
    S24 = [i for i, v in enumerate(V600) if all(x.b == 0 for x in v)]        # (+-2,0,0,0), (+-1,+-1,+-1,+-1)
    check('inscribed 24-cell: 24 corners', len(S24) == 24)
    r = show(vacuus4([V600[i] for i in S24], '24-cell inscribed in the 600-cell (one of 25)')); res.append(r)
    snub = [V600[i] for i in range(120) if i not in S24]
    r = show(vacuus4(snub, 'snub 24-cell (Gosset 1900) = 600-cell minus an inscribed 24-cell'))
    check('snub 24-cell: 96 corners, 144 cells', r['V'] == 96 and r['F3'] == 144); res.append(r)
    # grand antiprism: remove two completely orthogonal decagons
    v0 = V600[0]; e2 = ST600['edge2']
    u = next(V600[j] for j in range(120) if dot(sub(V600[j], v0), sub(V600[j], v0)) == e2)
    plane = [i for i, w in enumerate(V600) if all(x.iszero() for x in cross4(v0, u, w))]
    perp = [i for i, w in enumerate(V600) if dot(w, v0).iszero() and dot(w, u).iszero()]
    check('two orthogonal decagons', len(plane) == 10 and len(perp) == 10)
    ga = [V600[i] for i in range(120) if i not in plane and i not in perp]
    r = show(vacuus4(ga, 'grand antiprism (Conway and Guy 1965)'))
    check('grand antiprism: 100 corners, 320 cells, 720 two-faces', r['V'] == 100 and r['F3'] == 320 and r['F2'] == 720); res.append(r)
    # diminished 600-cells (Dutour Sikiric and Myrvold 2008: an independent set of corners removed)
    adj = ST600['adj']
    r = show(vacuus4(V600[1:], 'one-diminished 600-cell')); res.append(r)
    rnd = random.Random(2008)
    for size in (2, 6, 12, 18):
        for t in range(2):
            S = set(); cand = list(range(120)); rnd.shuffle(cand)
            for i in cand:
                if len(S) < size and not (adj[i] & S):
                    S.add(i)
            r = show(vacuus4([V600[i] for i in range(120) if i not in S], f'{size}-diminished 600-cell (random independent set {t})'))
            r['removed'] = sorted(S); res.append(r)
    # a centrally symmetric diminishing: remove an antipodal pair
    j = IDX[key(neg(V600[0]))]
    r = show(vacuus4([V600[i] for i in range(120) if i not in (0, j)], 'bi-diminished 600-cell (antipodal pair)')); res.append(r)
    dim = [x for x in res if 'diminished' in x['name'] or 'snub' in x['name']]
    check('every diminished 600-cell tested has all plates on mirror walls', all(x['plates_none'] == 0 and x['plates_cross'] == 0 for x in dim))
    # a 600-cell inscribed in the 120-cell: closure of two 120-cell corners at 36 degrees under self-reflection
    c0 = C600[0]; cc = dot(c0, c0)
    is36 = lambda a, b: dot(a, b).sign() > 0 and dot(a, b) * dot(a, b) * 4 == cc * cc * PHI * PHI
    near = [c for c in C600 if is36(c, c0)]
    print('  120-cell corners at 36 degrees from one corner:', len(near), flush=True)
    ck = {key(c) for c in C600}
    S = None
    for a, b, c in itertools.combinations(near, 3):
        if not (is36(a, b) and is36(a, c) and is36(b, c)):
            continue
        T = {key(x): x for x in (c0, a, b, c)}; grow = True; bad = False
        while grow and not bad:
            grow = False; Lst = list(T.values())
            for p_ in Lst:
                for q_ in Lst:
                    y = reflect(q_, p_); k = key(y)
                    if k not in T:
                        if k not in ck or len(T) >= 120:
                            bad = True; break
                        T[k] = y; grow = True
                if bad: break
        if not bad and len(T) == 120:
            S = T; break
    ins = list(S.values())
    check('inscribed 600-cell: 120 corners, all corners of the 120-cell', len(ins) == 120 and all(key(x) in ck for x in ins))
    r = show(vacuus4(ins, '600-cell inscribed in the 120-cell (classical; credit not traced here)')); res.append(r)
    OUT['special'] = res


def part_koca():
    gens = [perm_of_reflection(a) for a in ALPHA]
    G = group(gens)
    check('W(H4) has order 14400', len(G) == 14400)
    S24 = [i for i, v in enumerate(V600) if all(x.b == 0 for x in v)]
    v0 = V600[0]; e2 = ST600['edge2']
    u = next(j for j in range(120) if dot(sub(V600[j], v0), sub(V600[j], v0)) == e2)
    dec = [i for i, w in enumerate(V600) if all(x.iszero() for x in cross4(v0, V600[u], w))] + \
          [i for i, w in enumerate(V600) if dot(w, v0).iszero() and dot(w, V600[u]).iszero()]
    # A2+A2': a hexagon of roots in a plane whose orthogonal plane holds another hexagon
    hexa = None
    for j in range(120):
        if dot(V600[j], v0) == Q5(2):           # 60 degrees (|v|^2 = 4)
            pl = [i for i, w in enumerate(V600) if all(x.iszero() for x in cross4(v0, V600[j], w))]
            pp = [i for i, w in enumerate(V600) if dot(w, v0).iszero() and dot(w, V600[j]).iszero()]
            if len(pl) == 6 and len(pp) == 6:
                hexa = pl + pp; break
    # A4: simple roots a1..a4 with a_i.a_{i+1} = -2, others 0; its 20 roots by closure
    A4 = None
    for a2 in range(120):
        if dot(V600[a2], v0) != Q5(-2):
            continue
        for a3 in range(120):
            if dot(V600[a3], V600[a2]) != Q5(-2) or not dot(V600[a3], v0).iszero():
                continue
            for a4 in range(120):
                if dot(V600[a4], V600[a3]) == Q5(-2) and dot(V600[a4], v0).iszero() and dot(V600[a4], V600[a2]).iszero():
                    rs = set()
                    for gg in (v0, V600[a2], V600[a3], V600[a4]):
                        rs |= {key(x) for x in orbit(gg, [V600[a2], V600[a3], V600[a4], v0], cap=200)}
                    if len(rs) == 20:
                        A4 = [IDX[k] for k in rs]; break
            if A4: break
        if A4: break
    subs = {'W(H3)xZ2, order 240 (stabiliser of a corner pair)': [0, IDX[key(neg(v0))]],
            'Aut(A4) = W(A4)xZ2, order 240 (stabiliser of an A4 root system)': A4,
            'W(D4):C3, order 576 (stabiliser of an inscribed 24-cell)': S24,
            '[W(H2)xW(H2)]:Z4, order 400 (stabiliser of two orthogonal decagons)': dec,
            '[W(A2)xW(A2)]:Z4, order 144 (stabiliser of two orthogonal hexagons)': hexa}
    want = [240, 240, 576, 400, 144]
    res = []
    for (nm, S), order in zip(subs.items(), want):
        H = stabiliser(G, S)
        check(f'{nm}: order {order}', len(H) == order)
        o600 = orbits_on(H, 120, lambda g, i: g[i])
        cps = [cell_perm(g) for g in H]
        o120 = orbits_on(cps, 600, lambda g, i: g[i])
        ent = {'subgroup': nm, 'order': len(H), 'orbits_600cell_corners': [len(o) for o in o600],
               'orbits_120cell_corners': [len(o) for o in o120], 'hulls': []}
        print(nm, 'orbits on 600-cell corners', ent['orbits_600cell_corners'], 'on 120-cell corners', ent['orbits_120cell_corners'], flush=True)
        for src, orbs, VV in (('600-cell corners', o600, V600), ('120-cell corners', o120, C600)):
            for o in orbs:
                P = [VV[i] for i in o]
                if len(o) < 5 or np.linalg.matrix_rank(np.array([fl(p) for p in P]), tol=1e-9) < 4:
                    continue
                # an orbit not centred on 0 is still read with plates through the Queens' centre 0
                r = vacuus4(P, f'{nm.split(",")[0]} orbit of {len(o)} {src}', need_euler=True)
                r['orbit'] = o; show(r); ent['hulls'].append(r)
        # a generic orbit of the subgroup (its own symmetry only)
        Ms = [matrix_of(g) for g in H]
        x = (Q5(Fr(7, 5)), Q5(Fr(2, 7)), Q5(Fr(3, 11)), Q5(Fr(5, 13)))
        P = list({key(apply(M, x)): apply(M, x) for M in Ms}.values())
        r = show(vacuus4(P, f'{nm.split(",")[0]} generic orbit ({len(P)} points)')); ent['generic'] = r
        res.append(ent)
    OUT['koca'] = res


DIRS = None


def dirs4():
    from polytopes import polytope
    P = polytope('600-cell')
    check('polytopes.py 600-cell matches qv_lib frame', [key(v) for v in P['V']] == [key(v) for v in V600])
    return {lab: D['d'] for lab, D in P['dirs'].items()}


def atlas(V, E, label):
    res = []; dd = dirs4()
    for lab, d in dd.items():
        hs = sorted({dot(v, d) for v in V}, key=float)
        cuts = sorted([(h, True) for h in hs] + [((a + b) / Q5(2), False) for a, b in zip(hs, hs[1:])], key=lambda c: float(c[0]))
        for hv, at in cuts:
            if hv.sign() < 0:
                continue
            pts = slice_points(V, E, d, hv)
            ent = {'direction': lab, 'height': q5str(hv), 'at_vertex_layer': at, 'points': len(pts)}
            if len(pts) < 4 or np.linalg.matrix_rank(np.array([fl(p) for p in pts]) - fl(pts[0]), tol=1e-9) < 3:
                ent['dim'] = '<3'; res.append(ent); continue
            centre = scal(hv / dot(d, d), d)
            r = vacuus3(pts, d, centre, f'{label} {lab} slice h={q5str(hv)}')
            ent.update(r); res.append(ent)
        sh = shadow_points(V, d)
        r = vacuus3(sh, d, tuple(ZERO for _ in range(4)), f'{label} {lab} shadow')
        r['direction'] = lab; r['shadow'] = True; res.append(r)
    n3 = [x for x in res if 'plates' in x]
    print(f'{label}: {len([x for x in res if not x.get("shadow")])} slices ({len([x for x in res if x.get("dim") == "<3"])} below 3D), 4 shadows;',
          'hidden', sum(x['hidden'] == 'hidden' for x in n3), 'partly', sum(x['hidden'] == 'partly hidden' for x in n3),
          'not', sum(x['hidden'] == 'not hidden' for x in n3), f'({time.time() - T0:.0f}s)', flush=True)
    return res


def part_atlas600():
    res = atlas(V600, ST600['E'], '600-cell')
    check('#63 atlas: 62 slice types of the 600-cell reproduced', len([x for x in res if not x.get('shadow')]) == 62)
    OUT['atlas600'] = res


def part_atlas120():
    st = structure(C600)
    check('120-cell edges 1200', len(st['E']) == 1200)
    res = atlas(C600, st['E'], '120-cell')
    check('Red Queen atlas: 124 slice patterns of the 120-cell reproduced', len([x for x in res if not x.get('shadow')]) == 124)
    OUT['atlas120'] = res


def mu_of(x0):
    """Hopscotch parameter of the H4 seed x0 (pds-hopscotch-line frame: 600-cell radius 1, S(mu) = facets & corner planes mu)."""
    w1, w4 = OMEGA[0], OMEGA[3]
    return dot(w1, w4) * dot(w4, x0) / (dot(w4, w4) * dot(w1, x0))


def part_hopscotch():
    res = []
    stage = {(0, 0, 0, 1): '600-cell', (0, 0, 1, 0): 'rectified 600-cell', (0, 1, 0, 0): 'rectified 120-cell', (1, 0, 0, 0): '120-cell'}
    mus = {nm: mu_of(tuple(sum((Q5(l) * OMEGA[i][k] for i, l in enumerate(lam)), ZERO) for k in range(4))) for lam, nm in stage.items()}
    for nm, m in mus.items():
        print('  stage', nm, 'mu =', q5str(m), float(m), flush=True)
    check('Hopscotch frame: mu(600-cell) = 1 and mu(120-cell) = r^2 = phi^4/8', mus['600-cell'] == ONE and mus['120-cell'] == PHI * PHI * PHI * PHI / Q5(8))
    for lam in ((0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 0), (0, 2, 1, 0), (1, 2, 0, 0), (2, 1, 0, 0), (0, 0, 1, 1), (0, 1, 1, 0), (1, 1, 0, 0)):
        x0 = tuple(sum((Q5(l) * OMEGA[i][k] for i, l in enumerate(lam)), ZERO) for k in range(4))
        V = orbit(x0)
        r = show(vacuus4(V, f'S(mu) seed {lam}, mu = {float(mu_of(x0)):.6f}'))
        r['seed'] = lam; r['mu'] = q5str(mu_of(x0)); res.append(r)
    # the cross-wall stations found by part_stations, built and measured directly
    st = []
    for lam, nm in (((ZERO, ZERO, IPHI, ONE), 'truncated 600-cell type at the station lambda3:lambda4 = 1/phi'),
                    ((ZERO, Q5(-2, 1), ZERO, ONE), 'cantellated 600-cell type at the station lambda2:lambda4 = sqrt5 - 2')):
        x0 = tuple(sum((l * OMEGA[i][k] for i, l in enumerate(lam)), ZERO) for k in range(4))
        V = orbit(x0)
        r = show(vacuus4(V, f'{nm}, mu = {q5str(mu_of(x0))} = {float(mu_of(x0)):.9f}'))
        r['mu'] = q5str(mu_of(x0)); st.append(r)
    check('station of the truncated-600-cell hop: its 2400 triangles leave the 1200 no-wall plates for cross walls',
          st[0]['plates_none'] == 0 and st[0]['plates_cross'] > 0 and st[0]['V'] == 1440)
    check('station of the cantellated 600-cell family: the 2-3 faces on cross walls', st[1]['plates_cross'] > 0)
    OUT['hopscotch'] = res
    OUT['hopscotch_stations'] = st


def part_ab():
    """A and B (the golden twisted solids) as orbits of W(A4) on the 600-cell's corners (Koca et al. 2006 list 120 = 20 + 20+ + 20- + 30+ + 30-)."""
    gens = [perm_of_reflection(a) for a in ALPHA]
    G = group(gens)
    v0 = V600[0]
    # an A4 root system as in part_koca
    for a2 in range(120):
        if dot(V600[a2], v0) != Q5(-2): continue
        for a3 in range(120):
            if dot(V600[a3], V600[a2]) != Q5(-2) or not dot(V600[a3], v0).iszero(): continue
            for a4 in range(120):
                if dot(V600[a4], V600[a3]) == Q5(-2) and dot(V600[a4], v0).iszero() and dot(V600[a4], V600[a2]).iszero():
                    sr = [v0, V600[a2], V600[a3], V600[a4]]
                    rs = set()
                    for g0 in sr:
                        rs |= {key(x) for x in orbit(g0, sr, cap=200)}
                    if len(rs) == 20:
                        break
            else: continue
            break
        else: continue
        break
    W = group([perm_of_reflection(a) for a in sr])
    check('W(A4) generated by the four A4 roots has order 120', len(W) == 120)
    o = orbits_on(W, 120, lambda g, i: g[i])
    print('  W(A4) orbits on the 600-cell corners:', [len(x) for x in o], flush=True)
    # compare with A (perms of (phi^2,phi^2,phi^2,phi,0)) and B (perms of (phi^2,phi^2,1,1,0)) by their Gram spectra up to scale
    def spec(P):
        P = np.array([fl(p) for p in P]); P = P - P.mean(0); g = P @ P.T; g = g / np.max(np.diag(g)); return np.sort(np.round(g.ravel(), 7))
    p = (1 + 5 ** .5) / 2
    A5 = np.array(sorted(set(itertools.permutations((p * p, p * p, p * p, p, 0)))))
    B5 = np.array(sorted(set(itertools.permutations((p * p, p * p, 1, 1, 0)))))
    def spec5(S):
        S = S - S.mean(0); g = S @ S.T; g = g / np.max(np.diag(g)); return np.sort(np.round(g.ravel(), 7))
    sA, sB = spec5(A5), spec5(B5)
    found = {'A': [], 'B': []}
    rec = []
    for x in o:
        P = [V600[i] for i in x]
        s = spec(P)
        tag = 'A' if len(x) == 20 and np.allclose(s, sA) else ('B' if len(x) == 30 and np.allclose(s, sB) else None)
        r = vacuus4(P, f'W(A4) orbit of {len(x)} corners' + (f' = solid {tag}' if tag else ''))
        r['matches'] = tag; r['orbit'] = x; show(r); rec.append(r)
        if tag: found[tag].append(r)
    check('solid A appears twice (A and -A) among the W(A4) orbits, solid B twice', len(found['A']) == 2 and len(found['B']) == 2)
    # A, B plates (centred on their own centroid, as the walls study did, they coincide with the origin-centred plates
    # since the W(A4) orbits are centred at 0: check)
    ctr = all(not any(sum((V600[i][k] for i in x), ZERO).a or sum((V600[i][k] for i in x), ZERO).b for k in range(4)) for x in o)
    check('every W(A4) orbit is centred at the Queens centre', ctr)
    a, b = found['A'][0], found['B'][0]
    check('A: 30 plates, all mirror walls; B: 80 plates, 40 mirror + 40 cross (walls study reproduced in this frame)',
          (a['plates'], a['plates_mirror']) == (30, 30) and (b['plates'], b['plates_mirror'], b['plates_cross']) == (80, 40, 40))
    OUT['ab'] = rec


if __name__ == '__main__':
    parts = sys.argv[1:] or ['controls', 'wythoff', 'stations', 'special', 'koca', 'atlas600', 'atlas120', 'hopscotch', 'ab']
    for p_ in parts:
        print(f'== part {p_}', flush=True)
        globals()['part_' + p_]()
        print(f'PROGRESS {(parts.index(p_) + 1) / len(parts):.2f} {p_}', flush=True)
    tag = '-'.join(parts) if len(parts) < 9 else 'all'
    json.dump({'out': OUT, 'checks': CHECKS}, open(os.path.join(HERE, '..', 'data', f'study1-{tag}.json'), 'w'), indent=1, default=str)
    bad = [c for c in CHECKS if not c[1]]
    print('checks', len(CHECKS), 'failed', bad)
    print('FINAL ok' if CHECKS and not bad else 'FINAL FAIL')
