"""Aim 2 chunk 7, leads 1 and 2 (12 Nov 2026), exact over Q(sqrt5).
Lead 1: is the golden slice S = 4_21 cap E_perp the UNIFORM rectified 120-cell, and W = pi_perp(Voronoi) its exact polar?
  S is the polar of the window W (section-projection duality, chunk 7): S's vertices are W's facet normals, S's facets are W's vertices.
  Checks, all exact: f-vector; every vertex on one sphere; every edge the same length; every 2-face a regular polygon (equilateral and
  on the sphere, hence cyclic); every 4-vertex cell a regular tetrahedron, every 30-vertex cell an icosidodecahedron (60 equal edges,
  20 triangles + 12 pentagons, two of each at every vertex, every edge in one triangle and one pentagon); symmetry: the 60 reflections
  in the 120 roots' shadow (the H4 root system) map S onto itself, H4 (order 14400, counted as a free orbit) is transitive on S's 1200
  vertices, a vertex is fixed by exactly 4 reflections of type A1 x A2, and S's vertex set is a positive multiple of the Wythoff orbit
  o5x3o3o (ring on the node next to the 5-branch) = the uniform rectified 120-cell.
Lead 2: the golden twins. Psi(q) = phi^-1 P sigma(q) with P a coordinate permutation: if Psi maps the 240 icosian roots onto
  themselves it is an automorphism of E8 (Q-linear, orthogonal, root-preserving) which sends E_perp to E_par; then W_par = phi^-1 P W_perp
  and the two windows (and slices) are congruent in the true metric iff phi^-2 c_par = c_perp.
Controls: 600-cell and 120-cell through the same uniform test (positive); the window W itself and S with one vertex moved (negative);
  Psi without P, or with phi instead of 1/phi (negative).
Usage: python -u e8_leads.py [pilot]"""
import sys, os, time, itertools
from collections import Counter
from multiprocessing import get_context
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import e8_canon as C
from e8_canon import Q5, Fr, PHI, IPHI, key, dotg, exact_hull, incidences, e8_init, E8, ico_setup, bits, popc, solve

PILOT = 'pilot' in sys.argv[1:]
T0 = time.time()
def say(*a): print(*a, flush=True)
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def nrm(u): return dotg(u, u)
def scl(c, u): return tuple(c * x for x in u)
def sig(u): return tuple(x.sig() for x in u)

# ---------------- setup (shared by all tasks through fork) ----------------
e8_init()
Ric, Rstd, to_q = ico_setup()
BASIS = [to_q(tuple(Fr(1 if i == j else 0) for j in range(8))) for i in range(8)]
def q_of(x):
    q = [Q5(0)] * 4
    for xk, b in zip(x, BASIS):
        if xk != 0: q = [a + xk * c for a, c in zip(q, b)]
    return tuple(q)
Rq = [q_of(r) for r in Rstd]
N12 = E8['N12'] if not PILOT else E8['N12'][:2160]
Nstd = [tuple(Fr(x, 12) for x in n) for n in N12]
Nq = [q_of(n) for n in Nstd]
def dedup(P):
    d = {}
    for p in P: d.setdefault(key(p), p)
    return list(d.values())
CPAR, CPERP = Q5(1, Fr(1, 5)), Q5(1, Fr(-1, 5))

# ---------------- generic exact analysis of a 4-polytope ----------------
def faces(V, Nn, inc_f, inc_v):
    """V vertices, Nn facet normals (n.x <= 1), inc_f[f] = bitset of vertices on f, inc_v[v] = bitset of facets at v.
    edges: i, j with the meet of all facets through both = {i, j}; 2-faces: F1 cap F2 with >= 3 vertices."""
    nv = len(V); E = []
    for i in range(nv):
        for j in range(i + 1, nv):
            c = inc_v[i] & inc_v[j]
            if popc(c) < 3: continue
            g = -1
            for f in bits(c): g &= inc_f[f]
            if g == (1 << i) | (1 << j): E.append((i, j))
    F2 = set()
    nf = len(Nn)
    for a in range(nf):
        for b in range(a + 1, nf):
            g = inc_f[a] & inc_f[b]
            if popc(g) >= 3: F2.add(g)
    return E, sorted(F2)

def analyse(label, V, Nn):
    """returns dict of exact facts (combinatorics, radii, edge lengths, 2-faces, cells)"""
    inc_f, inc_v = incidences(V, Nn)
    E, F2 = faces(V, Nn, inc_f, inc_v)
    out = {'label': label, 'f': (len(V), len(E), len(F2), len(Nn))}
    out['radii2'] = sorted({key((nrm(v),)) for v in V})
    L = Counter(key((nrm(sub(V[i], V[j])),)) for i, j in E); out['edge2'] = sorted(L.items())
    deg = Counter(); eset = set()
    for i, j in E: deg[i] += 1; deg[j] += 1; eset.add((1 << i) | (1 << j))
    out['deg'] = sorted(Counter(deg.values()).items())
    # 2-faces: sizes; every side of the polygon an edge, polygon = cycle in the edge graph
    psz = Counter(); poly_ok = True
    for g in F2:
        vs = list(bits(g)); k = len(vs)
        ne = sum(1 for a, b in itertools.combinations(vs, 2) if (1 << a) | (1 << b) in eset)
        poly_ok &= ne == k; psz[k] += 1
    out['faces2'] = sorted(psz.items()); out['faces2_are_cycles'] = poly_ok
    # cells
    cells = Counter(); cell_ok = {}
    for f in range(len(Nn)):
        vs = set(bits(inc_f[f])); ce = [(i, j) for i, j in E if i in vs and j in vs]
        cf = [g for g in F2 if g & inc_f[f] == g]
        fsz = Counter(popc(g) for g in cf)
        sig_ = (len(vs), len(ce), tuple(sorted(fsz.items())))
        cells[sig_] += 1
        if len(vs) == 30 and sig_ not in cell_ok:
            # icosidodecahedron: at each vertex 2 triangles + 2 pentagons; each edge in one triangle and one pentagon
            per_v = Counter(); per_e = Counter()
            for g in cf:
                for v in bits(g): per_v[(v, popc(g))] += 1
                for i, j in ce:
                    if g >> i & 1 and g >> j & 1: per_e[((i, j), popc(g))] += 1
            okv = all(per_v[(v, 3)] == 2 and per_v[(v, 5)] == 2 for v in vs)
            oke = all(per_e[(e, 3)] == 1 and per_e[(e, 5)] == 1 for e in ce)
            cell_ok[sig_] = okv and oke
    out['cells'] = sorted(cells.items()); out['icosidodecahedron_vertex_config'] = cell_ok
    out['E'] = E
    return out

def refl(a, aa):
    return lambda x: sub(x, scl(2 * dotg(x, a) / aa, a))

def simple_system(roots):
    import numpy as np
    g = np.random.default_rng(3).normal(size=4)
    pos = [r for r in roots if sum(x.f() * c for x, c in zip(r, g)) > 0]
    pk = {key(r) for r in pos}
    # a positive root a is simple iff its reflection maps every other positive root to a positive root (valid for H4 too)
    simple = [a for a in pos if all(key(refl(a, nrm(a))(r)) in pk for r in pos if key(r) != key(a))]
    assert len(simple) == 4, len(simple)
    return pos, simple

def orbit(x, gens):
    seen = {key(x): x}; todo = [x]
    while todo:
        y = todo.pop()
        for s in gens:
            z = s(y); k = key(z)
            if k not in seen: seen[k] = z; todo.append(z)
    return seen

def coxeter(simple):
    m = {}
    for i, j in itertools.combinations(range(4), 2):
        c2 = dotg(simple[i], simple[j]) * dotg(simple[i], simple[j]) / (nrm(simple[i]) * nrm(simple[j]))
        m[(i, j)] = 2 if c2.z() else 3 if c2 == Q5(Fr(1, 4)) else 5 if c2 == PHI * PHI / 4 else None
    return m

def symmetry(V, roots):
    pos, simple = simple_system(roots)
    out = {'npos': len(pos), 'nsimple': len(simple)}
    Vk = {key(v) for v in V}
    R = [refl(a, nrm(a)) for a in pos]
    out['root_system_closed'] = all({key(s(r)) for r in roots} == {key(r) for r in roots} for s in R)
    out['invariant'] = all({key(s(v)) for v in V} == Vk for s in R)
    out['orbit_v0'] = len(orbit(V[0], [refl(a, nrm(a)) for a in simple]))
    st = [a for a in pos if dotg(V[0], a).z()]
    out['stab_reflections'] = len(st)
    out['stab_gram'] = sorted(Counter(key((dotg(a, b) * dotg(a, b) / (nrm(a) * nrm(b)),)) for a, b in itertools.combinations(st, 2)).items())
    # Coxeter diagram of the simple roots: cos^2 = 0 (m=2), 1/4 (m=3), phi^2/4 (m=5)
    m = coxeter(simple)
    out['coxeter'] = sorted(m.values(), key=str)
    return out, simple, m

def wythoff_check(V, roots, ring_rule):
    """vertex set of V = positive multiple of the Wythoff orbit with one ring placed by ring_rule(chain order)"""
    _, simple = simple_system(roots); m = coxeter(simple)
    # chain order: end node with a 5-bond = node 1
    adj = {i: [j for j in range(4) if j != i and m[tuple(sorted((i, j)))] != 2] for i in range(4)}
    ends = [i for i in range(4) if len(adj[i]) == 1]
    n1 = next(i for i in ends if m[tuple(sorted((i, adj[i][0])))] == 5)
    chain = [n1]
    while len(chain) < 4: chain.append(next(j for j in adj[chain[-1]] if j not in chain))
    ring = chain[ring_rule]
    v = solve([list(simple[i]) for i in range(4)], [Q5(1) if i == ring else Q5(0) for i in range(4)])
    O = orbit(tuple(v), [refl(a, nrm(a)) for a in simple])
    v0 = V[0]
    par = None
    for w in O.values():
        if all((v0[i] * w[j] - v0[j] * w[i]).z() for i, j in itertools.combinations(range(4), 2)) and dotg(v0, w).sign() > 0: par = w; break
    if par is None: return len(O), False, None
    lam = nrm(v0) / nrm(par)
    same = {key(scl(dotg(v0, par) / nrm(par), w)) for w in O.values()} == {key(x) for x in V}
    return len(O), same, lam

# ---------------- tasks ----------------
def task_slice():
    say_ = []; log = say_.append; t0 = time.time()
    Wpts = dedup([sig(q) for q in Nq])
    verts, N, _ = exact_hull(Wpts)
    Wv = [Wpts[i] for i in verts]
    log(f'window W_perp: {len(Wpts)} distinct shadows of the 19440 Voronoi vertices; hull {len(Wv)} vertices, {len(N)} facets ({time.time()-t0:.0f} s)')
    shadow = dedup([sig(q) for q in Rq])
    roots = [r for r in shadow if nrm(r) == Q5(1)]; assert len(roots) == 120   # the 240 shadows are two 600-cells (radii 1, phi) on the same 120 directions
    S = analyse('slice S = 4_21 cap E_perp (vertices = W facet normals)', [tuple(n) for n in N], Wv)
    res = {'S': S, 'log': say_}
    res['S_sym'] = symmetry([tuple(n) for n in N], roots)[0]
    res['S_wythoff'] = wythoff_check([tuple(n) for n in N], roots, 1)
    # S with one vertex moved 1/1000 outward (negative): no longer on the sphere / not invariant
    Nb = [tuple(n) for n in N]; Nb[0] = scl(Q5(Fr(1001, 1000)), Nb[0])
    res['neg_moved'] = (sorted({key((nrm(v),)) for v in Nb}) != S['radii2'], symmetry(Nb, roots)[0]['invariant'])
    W = analyse('window W_perp (negative: polar of S, not uniform)', Wv, [tuple(n) for n in N])
    res['W'] = W
    res['W_sym'] = symmetry(Wv, roots)[0]
    log(f'slice analysis done ({time.time()-t0:.0f} s)')
    return res

def task_controls():
    t0 = time.time()
    shadow = dedup([sig(q) for q in Rq])
    roots = [r for r in shadow if nrm(r) == Q5(1)]; assert len(roots) == 120   # the 240 shadows are two 600-cells (radii 1, phi) on the same 120 directions
    verts, N, _ = exact_hull(shadow)
    V = [shadow[i] for i in verts]
    c600 = analyse('600-cell (E_perp shadow of the roots)', V, [tuple(n) for n in N])
    c600['sym'] = symmetry(V, roots)[0]; c600['wyt'] = wythoff_check(V, roots, 3)
    c120 = analyse('120-cell (its polar)', [tuple(n) for n in N], V)
    c120['sym'] = symmetry([tuple(n) for n in N], roots)[0]; c120['wyt'] = wythoff_check([tuple(n) for n in N], roots, 0)
    # wrong ring (negative): S-type test with the ring on the 5-end node must fail for the rectified shape later; here: 600-cell vs ring 0
    c600['wyt_wrong_ring'] = wythoff_check(V, roots, 0)
    # H4 order: free orbit of a generic point under the 4 simple reflections
    _, simple = simple_system(roots)
    g = (Q5(Fr(1, 7), Fr(1, 13)), Q5(Fr(2, 11), Fr(-1, 17)), Q5(Fr(3, 19), Fr(1, 23)), Q5(Fr(-5, 29), Fr(1, 31)))
    order = len(orbit(g, [refl(a, nrm(a)) for a in simple]))
    for c in (c600, c120): c.pop('E')
    return {'c600': c600, 'c120': c120, 'H4order': order, 't': time.time() - t0}

def signed_perms():
    for p in itertools.permutations(range(4)):
        for s in itertools.product((1, -1), repeat=4):
            yield p, s
def apply_P(P, u):
    p, s = P; return tuple(u[p[i]] * s[i] for i in range(4))

def task_twin():
    t0 = time.time()
    Rk = {key(r) for r in Ric}
    good = [P for P in signed_perms() if {key(scl(IPHI, apply_P(P, sig(r)))) for r in Ric} == Rk]
    parity = Counter(sum(1 for i in range(4) for j in range(i + 1, 4) if P[0][i] > P[0][j]) % 2 for P in good)
    out = {'n_good': len(good), 'parity': sorted(parity.items())}
    neg_noP = {key(scl(IPHI, sig(r))) for r in Ric} == Rk
    neg_phi = any({key(scl(PHI, apply_P(P, sig(r)))) for r in Ric} == Rk for P in signed_perms())
    out['neg'] = (neg_noP, neg_phi)
    if not good: return out
    P = good[0]; out['P'] = P
    Psi = lambda q: scl(IPHI, apply_P(P, sig(q)))
    # Psi in standard E8 coordinates: x -> q^-1(Psi(q(x))); q as a Q-linear map Q^8 -> Q^8 (a_i, b_i)
    flat = lambda q: [c for x in q for c in (x.a, x.b)]
    Mq = [[flat(BASIS[k])[r] for k in range(8)] for r in range(8)]
    cols = [solve(Mq, flat(Psi(BASIS[k]))) for k in range(8)]
    M = [[cols[k][r] for k in range(8)] for r in range(8)]          # M x = Psi in standard coordinates
    MtM = [[sum(M[r][i] * M[r][j] for r in range(8)) for j in range(8)] for i in range(8)]
    out['orthogonal'] = all(MtM[i][j] == (1 if i == j else 0) for i in range(8) for j in range(8))
    app = lambda x: tuple(sum(M[r][k] * x[k] for k in range(8)) for r in range(8))
    Rs = {tuple(r) for r in Rstd}
    out['roots_to_roots'] = {app(r) for r in Rstd} == Rs
    out['det'] = C.det_field([list(r) for r in M])
    Rk_ = ident(); out['order'] = None
    for k in range(1, 121):
        Rk_ = [[sum(Rk_[i][t] * M[t][j] for t in range(8)) for j in range(8)] for i in range(8)]
        if Rk_ == ident(): out['order'] = k; break
    # exchanges the golden spaces: par(Psi x) = phi^-1 P perp(x), perp(Psi x) = -phi P par(x), on all roots and Voronoi vertices
    chk = all(q_of(app(x)) == Psi(q_of(x)) and sig(q_of(app(x))) == scl(-PHI, apply_P(P, q_of(x))) for x in Rstd + Nstd[::7])
    out['swaps_spaces'] = chk
    out['vor_to_vor'] = {tuple(app(n)) for n in Nstd} == {tuple(n) for n in Nstd}
    Wperp = {key(Psi(q)) for q in Nq}   # phi^-1 P (sigma q(n)) = q(Psi n)
    Wpar = {key(q) for q in Nq}
    out['Wpar_eq_image'] = Wperp == Wpar
    out['metric'] = (IPHI * IPHI * CPAR == CPERP, PHI * PHI * CPAR == CPERP)
    out['t'] = time.time() - t0
    return out

def ident(): return [[Fr(1 if i == j else 0) for j in range(8)] for i in range(8)]

def run(name):
    return name, {'slice': task_slice, 'controls': task_controls, 'twin': task_twin}[name]()

def main():
    OK = True
    def check(m, c):
        nonlocal OK
        OK &= bool(c); say(('ok   ' if c else 'FAIL ') + m)
    say(f'chunk 7 leads 1, 2: pilot={PILOT}; setup {time.time()-T0:.0f} s; {len(Nq)} Voronoi vertices mapped')
    check('icosian map on all 240 roots (exact)', {key(q) for q in Rq} == {key(q) for q in Ric})
    res = {}
    with get_context('fork').Pool(3) as pool:
        for i, (n, r) in enumerate(pool.imap_unordered(run, ['slice', 'controls', 'twin'])):
            res[n] = r; say(f'PROGRESS {(i + 1) / 3:.2f} {n} ({time.time()-T0:.0f} s)')
    c = res['controls']; c6, c1 = c['c600'], c['c120']
    for k in ('c600', 'c120'):
        say(f"control {c[k]['label']}: f = {c[k]['f']}, radii2 {c[k]['radii2']}, edge2 {c[k]['edge2']}, degree {c[k]['deg']}, 2-faces {c[k]['faces2']}, cells {c[k]['cells']}, symmetry {c[k]['sym']}, Wythoff {c[k]['wyt']}")
    check(f"H4 order: free orbit of a generic point under the 4 simple reflections = {c['H4order']} (expect 14400)", c['H4order'] == 14400)
    check('POS 600-cell: f = (120, 720, 1200, 600), one radius, one edge length, 2-faces triangles, cells regular tetrahedra, H4-transitive, stabilizer H3 (15 reflections), Wythoff o5o3o3x',
          c6['f'] == (120, 720, 1200, 600) and len(c6['radii2']) == 1 and len(c6['edge2']) == 1 and c6['faces2'] == [(3, 1200)] and c6['sym']['invariant']
          and c6['sym']['orbit_v0'] == 120 and c6['sym']['stab_reflections'] == 15 and c6['wyt'][1])
    check('POS 120-cell: f = (600, 1200, 720, 120), one radius, one edge length, pentagons, 20-vertex cells, H4-transitive, stabilizer A3 (6), Wythoff x5o3o3o',
          c1['f'] == (600, 1200, 720, 120) and len(c1['radii2']) == 1 and len(c1['edge2']) == 1 and c1['faces2'] == [(5, 720)] and c1['sym']['orbit_v0'] == 600
          and c1['sym']['stab_reflections'] == 6 and c1['wyt'][1])
    check('NEG 600-cell against the wrong ring (5-end node): not its Wythoff orbit', not c6['wyt_wrong_ring'][1])
    s = res['slice']
    for line in s['log']: say(line)
    S, W = s['S'], s['W']
    say(f"slice S: f = {S['f']}, radii2 {S['radii2']}, edge2 {S['edge2']}, degree {S['deg']}, 2-faces {S['faces2']} (cycles {S['faces2_are_cycles']}), cells {S['cells']}, icosidodecahedron vertex/edge config {S['icosidodecahedron_vertex_config']}")
    say(f"slice S symmetry: {s['S_sym']}; Wythoff o5x3o3o: orbit {s['S_wythoff'][0]}, equal to S up to scale {s['S_wythoff'][1]}, |v0|^2/|wythoff point|^2 = {s['S_wythoff'][2]}")
    say(f"window W: f = {W['f']}, radii2 {W['radii2']}, edge2 {W['edge2']}, degree {W['deg']}, 2-faces {W['faces2']}, cells {W['cells']}; symmetry {s['W_sym']}")
    if not PILOT:
        check('LEAD 1 S: f-vector (1200, 3600, 3120, 720) of the rectified 120-cell', S['f'] == (1200, 3600, 3120, 720))
        check('LEAD 1 S: all 1200 vertices on one sphere and all 3600 edges of one length (exact in Q(sqrt5))', len(S['radii2']) == 1 and len(S['edge2']) == 1)
        check('LEAD 1 S: every vertex has degree 6 (vertex figure a triangular prism: 5 cells)', S['deg'] == [(6, 1200)])
        check('LEAD 1 S: 2-faces 2400 triangles + 720 pentagons, each a cycle of edges; equilateral and on the sphere => regular', S['faces2'] == [(3, 2400), (5, 720)] and S['faces2_are_cycles'])
        check('LEAD 1 S: cells 600 regular tetrahedra (4 vertices, 6 equal edges) + 120 icosidodecahedra (30 vertices, 60 edges, 20 triangles + 12 pentagons, 3.5.3.5 at every vertex)',
              S['cells'] == [((4, 6, ((3, 4),)), 600), ((30, 60, ((3, 20), (5, 12))), 120)] and all(S['icosidodecahedron_vertex_config'].values()))
        ss = s['S_sym']
        check('LEAD 1 S: the 60 H4 reflections map S onto itself; H4 transitive on the 1200 vertices; a vertex fixed by exactly 4 reflections (A1 x A2: cos^2 = 0 for 3 pairs, 1/4 for 3 pairs)',
              ss['root_system_closed'] and ss['invariant'] and ss['orbit_v0'] == 1200 and ss['stab_reflections'] == 4
              and ss['stab_gram'] == [(((Fr(0), Fr(0)),), 3), (((Fr(1, 4), Fr(0)),), 3)])
        check('LEAD 1 S = positive multiple of the Wythoff orbit o5x3o3o (uniform rectified 120-cell), exact', s['S_wythoff'][0] == 1200 and s['S_wythoff'][1])
        check('LEAD 1 W: the window has two vertex radii and more than one edge length (it is the dual, not a uniform polytope); 1200 cells of 5 vertices',
              len(W['radii2']) == 2 and len(W['edge2']) > 1 and W['f'][3] == 1200)
        check('NEG S with one vertex moved 1/1000: off the sphere and no longer H4-invariant', s['neg_moved'][0] and not s['neg_moved'][1])
    t = res['twin']
    say(f"twin: {t}")
    check(f"LEAD 2: Psi = phi^-1 P sigma maps the 240 icosian roots onto themselves for {t['n_good']} signed permutations P (parity {t['parity']})", t['n_good'] > 0)
    check('NEG Psi without P (phi^-1 sigma) and Psi with phi instead of phi^-1 do NOT preserve the roots', not t['neg'][0] and not t['neg'][1])
    if t['n_good']:
        check(f"LEAD 2: Psi in standard E8 coordinates is an orthogonal rational matrix (det {t['det']}, order {t['order']}) mapping the 240 roots onto themselves: an automorphism of E8",
              t['orthogonal'] and t['roots_to_roots'])
        check('LEAD 2: Psi maps the Voronoi vertices onto themselves and swaps the golden spaces: par(Psi x) = phi^-1 P perp(x), perp(Psi x) = -phi P par(x) (exact)', t['vor_to_vor'] and t['swaps_spaces'])
        check('LEAD 2: phi^-1 P maps the 19440 shadows in E_perp exactly onto those in E_par, so W_par = phi^-1 P W_perp', t['Wpar_eq_image'])
        check('LEAD 2: phi^-2 c_par = c_perp exactly (phi^-1 P is an isometry E_perp -> E_par in the true metric); NEG phi^2 c_par != c_perp', t['metric'][0] and not t['metric'][1])
    say(f'total {time.time()-T0:.0f} s')
    say('FINAL ok' if OK else 'FINAL FAIL: see the FAIL lines above')

if __name__ == '__main__':
    main()
