"""01: plate model sanity + controls (exact integers; SAT with CaDiCaL).
- RD / TRD reliefs agree with the exact relief of the hat-sectors study (units H/12, ball spacing 1).
- volume of every reference piece = cell volume 1/sqrt2 (exact, sympy).
- RD alone: only constant-lean words (c...c) on patches; periodic tiling found (control that must be caught).
- TRD alone: only alternating (h...h).  RD + TRD (two pieces): every word.
- an independent column check of a SAT solution (interfaces rebuilt globally) confirms exact filling.
"""
import sys, itertools, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import sympy as sp
from plates import *

t0 = time.time()
ok = True


def volume(piece):
    area = sp.sqrt(3) / 12
    unit = sp.sqrt(sp.Rational(2, 3)) / 12
    return sp.nsimplify(area * unit * sp.Rational(thickness_sum(piece), 3))


# relief values vs hat-sectors (RD scale: ball spacing sqrt2 -> multiply by sqrt2)
u_rd = sp.sqrt(2) * sp.sqrt(sp.Rational(2, 3)) / 12
chk = [sp.simplify(9 * u_rd - sp.sqrt(3) / 2), sp.simplify(6 * u_rd - 1 / sp.sqrt(3)), sp.simplify(3 * u_rd - 1 / (2 * sp.sqrt(3)))]
print('RD relief vs hat-sectors exact (centre sqrt3/2, tips 1/sqrt3, 1/(2sqrt3)):', chk)
ok &= all(c == 0 for c in chk)
for name, P in (('RD', rd_piece()), ('TRD', trd_piece())):
    v = volume(P)
    print(f'{name}: valid {valid(P)}  thickness sum {thickness_sum(P)}  volume {v}  (1/sqrt2 = {sp.sqrt(2)/2})')
    ok &= valid(P) and sp.simplify(v - sp.sqrt(2) / 2) == 0


def words_on_patch(pieces, K, R, mirrors=False):
    sts, _ = states(pieces, mirrors)
    C = compat_table(sts)
    adm = []
    for w in itertools.product((1, 2), repeat=K - 1):
        if w[0] != 1:
            continue
        cells, con = patch_contacts(w, R)
        s, model = sat_solve(len(cells), len(sts), con, C)
        if s:
            adm.append(''.join('c' if w[i] == w[i - 1] else 'h' for i in range(1, len(w))))
    return len(sts), sorted(adm)


def column_check(pieces, leans, R):
    """independent exact check: rebuild interfaces from a SAT model; every fine triangle inside the patch must see
    top(layer k cell) == bottom(layer k+1 cell) + H, and thickness > 0."""
    sts, _ = states(pieces)
    C = compat_table(sts)
    cells, con = patch_contacts(leans, R)
    s, model = sat_solve(len(cells), len(sts), con, C)
    if not s:
        return None
    where = {key: sts[model[i]] for key, i in cells.items()}
    cs = layer_cosets(leans)
    checked = 0
    for (k, X), P in where.items():
        if k == len(leans):
            continue
        for sct in range(6):
            T = [add(X, v) for v in TRI[sct]]
            Y = [p for p in T if coset(p) == cs[k + 1]][0]
            if (k + 1, Y) not in where:
                continue
            Q = where[(k + 1, Y)]
            top = dict(P[0][sct]); bot = dict(Q[1][sec([sub(p, Y) for p in T])])
            for p in T:
                if top[sub(p, X)] + 12 * k != bot[sub(p, Y)] + 12 * (k + 1):
                    return False
            checked += 1
    return checked


for name, pcs, expect in (('RD', [rd_piece()], {'ccc'}), ('TRD', [trd_piece()], {'hhh'}),
                          ('RD+TRD', [rd_piece(), trd_piece()], {''.join(w) for w in itertools.product('ch', repeat=3)})):
    n, adm = words_on_patch(pcs, 5, 2)
    print(f'{name}: {n} distinct placed states; admitted c/h words (5 layers, R=2): {adm}')
    ok &= set(adm) == expect
    sts, _ = states(pcs)
    C = compat_table(sts)
    alive, edges, conf = periodic_alive(C, len(sts), (1, 0, 1))
    w = ch_words_from_edges(edges, 4)
    print(f'   periodic (every layer uniform) tilings exist: {bool(alive)}; their c/h words of length 4: {w}')
    ok &= bool(alive)
    cc = column_check(pcs, (1, 1, 2, 1) if name == 'RD+TRD' else ((1, 1, 1, 1) if name == 'RD' else (1, 2, 1, 2)), 2)
    print(f'   independent column check: {cc} triangle contacts exact')
    ok &= bool(cc)
print(f'time {time.time()-t0:.1f}s')
print('FINAL ok' if ok else 'FINAL FAIL: a control or exact check failed')
