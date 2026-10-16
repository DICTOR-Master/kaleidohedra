# Tests for geomcheck.py, on the polar Dharma data (each test replays one of the 2026-10-16 slips and shows the check catches it).
# Run: python3 studies/_lib/test_geomcheck.py
import json, os, sys, itertools
import numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import geomcheck as gc
ST = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-16-polar-dharma', 'data')
C = {n: np.array(V, float) for n, V in json.load(open(os.path.join(ST, 'reversed-chain.json')))}
ax = gc.icosa_axes(C['icosahedron']); G = gc.group(ax); p = gc.PHI
ok = []
def test(name):
    def wrap(f): f(); ok.append(name); print('ok', name)
    return wrap
def cyc(pts):
    out = set()
    for x, y, z in pts:
        for s in itertools.product(*[[1, -1] if c else [1] for c in (x, y, z)]):
            a = (s[0] * x, s[1] * y, s[2] * z)
            for r in range(3): out.add(tuple(round(v, 12) for v in a[r:] + a[:r]))
    return np.array(sorted(out))
@test('axes and the 60-rotation group')
def _():
    assert (len(ax['5']), len(ax['3']), len(ax['2'])) == (12, 20, 30)
@test('rule 1: of the two golden frames exactly one passes; orient() repairs the mirror one')
def _():
    V = cyc([(1, 1, p ** 3), (p * p, p, 2 * p), (2 + p, 0, p * p)])
    passes = []
    for W in (V, V[:, [1, 0, 2]]):                    # the two golden frames: exactly one may pass
        try: gc.frame(W, ax, 'RID'); passes.append(True)
        except AssertionError: passes.append(False)
    assert passes.count(True) == 1, passes
    gc.frame(gc.orient(V[:, [1, 0, 2]] if passes[0] else V, ax, 'RID'), ax, 'RID')   # orient() repairs the mirror one
@test('rule 3: the dodecahedron-in-icosidodecahedron slack reproduces 1.232241')
def _():
    grow = lambda A, B: min(-e[3] / max(A @ e[:3]) for e in ConvexHull(B).equations)
    gc.known('D in ID', grow(C['dodecahedron (inner)'], C['icosidodecahedron']), 1.232241105)
    try: gc.known('inverted formula', 1 / grow(C['dodecahedron (inner)'], C['icosidodecahedron']), 1.232241105); raise SystemExit('not caught')
    except AssertionError: pass
@test('rule 2: both orders of the truncated icosidodecahedron pair (only the reversed one fits)')
def _():
    grow = lambda A, B: min(-e[3] / max(A @ e[:3]) for e in ConvexHull(B).equations)
    T = gc.orient(cyc([(1 / p, 1 / p, 3 + p), (2 / p, p, 1 + 2 * p), (1 / p, p * p, 3 * p - 1), (2 * p - 1, 2, 2 + p), (p, 3, 2 * p)]), ax, 'TID')
    e = ConvexHull(T).equations; pl = []
    for x in e:
        if not any(np.allclose(x, y, atol=1e-9) for y in pl): pl.append(x)
    DT = gc.frame(np.array([x[:3] / -x[3] for x in pl]), ax, 'DT')
    D, ID = C['dodecahedron (inner)'], C['icosidodecahedron']
    slack = lambda X, Y: grow(Y, ID) * grow(X, Y) * grow(D, X)
    r = gc.both_orders(slack, T, DT, ('TID', 'DT'))
    gc.known('TID inside DT', r[('TID', 'DT')], 0.979666, 1e-5); gc.known('DT inside TID', r[('DT', 'TID')], 1.052459551, 1e-8)
@test('rule 4: the 120 middle pieces of the pair nest are one kind (float face counts said 103)')
def _():
    L = json.load(open(os.path.join(ST, 'polar-pair-pieces.json')))
    k = gc.kinds(L['disdyakis triacontahedron -> truncated icosidodecahedron'], G)
    assert len(k) == 1 and k[0][0] == 120, k
    k = gc.kinds(json.load(open(os.path.join(ST, 'polar-pair-rid-pieces.json')))['rhombicosidodecahedron -> deltoidal hexecontahedron'], G)
    assert sorted(c for c, _ in k) == [12, 20, 30], k
@test('rule 5 and 6: exact zero gate and labels')
def _():
    from fractions import Fraction
    gc.exact_zero('zero', Fraction(0))
    try: gc.exact_zero('nonzero', Fraction(1, 10 ** 12)); raise SystemExit('not caught')
    except AssertionError: pass
    assert gc.tag('x', True, 'tight') == '[exact, tight] x'
print(f'{len(ok)} checks passed')
