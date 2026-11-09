"""The Ammann-Beenker line and its turn (DICTO 9-10 Nov 2026, aim 1: 'the quasicrystal is the turning point of a line of crystals').
Line: canonical cut-and-project tilings from Z^4 with physical star e_k = (cos k pi/4, sin k pi/4) and internal (window) vectors
eps(t) = (-t, t), (1, 0), (-t, -t), (0, 1)  (study 2026-11-09-ab-turn, zono.py); t rational gives a periodic tiling (a crystal),
t = 1/sqrt2 the Ammann-Beenker quasicrystal.
Theorem (the turn). The rotation by 45 degrees scaled by 1/(sqrt2 t) maps eps_k(t) to +-eps_{k+1}(1/(2t)), and the 45-degree rotation
maps e_k to e_{k+1}: the shift k -> k+1 of the Z^4 basis (with signs) is a lattice automorphism carrying the scheme at t to the scheme
at 1/(2t). So the tilings at t and 1/(2t) are the same tiling turned by 45 degrees (same local patterns, same frequencies).
The turn t -> 1/(2t) has the single positive fixed point 1/sqrt2: the quasicrystal; it exchanges the Pell approximants pairwise
(2/3 <-> 3/4, 5/7 <-> 7/10, 12/17 <-> 17/24, 29/41 <-> 41/58), which close in on 1/sqrt2 from both sides.
Checks: (1) the map, exactly (symbolic t, sqrt2 exact); (2) for each Pell pair, the vertex-star frequencies of the two tilings agree
exactly (rational arithmetic, zono.py). usage: python3 ab_turn_check.py"""
import sys, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-09-ab-turn', 'scripts'))
import sympy as sp
from zono import zonogon, arrangement, area
t = sp.symbols('t', positive=True); r2 = sp.sqrt(2)
eps = lambda s: [sp.Matrix([-s, s]), sp.Matrix([1, 0]), sp.Matrix([-s, -s]), sp.Matrix([0, 1])]
Rot = sp.Matrix([[1, -1], [1, 1]]) / r2; sc = 1 / (r2 * t)
E, E2 = eps(t), eps(1 / (2 * t)); ok1 = True
for k in range(4):
    img = sp.simplify(sc * Rot * E[k]); tgt = E2[(k + 1) % 4]
    ok1 &= sp.simplify(img - tgt) == sp.zeros(2, 1) or sp.simplify(img + tgt) == sp.zeros(2, 1)
phys = [sp.Matrix([sp.cos(k * sp.pi / 4), sp.sin(k * sp.pi / 4)]) for k in range(5)]
ok1 &= all(sp.simplify(Rot * phys[k] - phys[k + 1]) == sp.zeros(2, 1) for k in range(4))
print('(1) the turn maps the scheme at t to the scheme at 1/(2t) (45-degree turn, basis shift with signs):', ok1)
fixed = sp.solve(sp.Eq(t, 1 / (2 * t)), t); print('    fixed point of t -> 1/(2t):', fixed)
def canon(star):
    b = tuple(star); best = None
    for r in range(8):
        for s_ in (1, -1):
            c = tuple(b[(s_ * d + r) % 8] for d in range(8))
            if best is None or c < best: best = c
    return ''.join('1' if x else '0' for x in best)
def freqs(tt):
    Ev = [(-tt, tt), (Fr(1), Fr(0)), (-tt, -tt), (Fr(0), Fr(1))]; W = zonogon(Ev); A = area(W); out = {}
    for P, st in arrangement(W, Ev):
        c = canon(st); out[c] = out.get(c, 0) + area(P) / A
    return out
pairs = [(Fr(2, 3), Fr(3, 4)), (Fr(5, 7), Fr(7, 10)), (Fr(12, 17), Fr(17, 24)), (Fr(29, 41), Fr(41, 58))]
ok2 = True
for a, b in pairs:
    assert b == 1 / (2 * a)
    fa, fb = freqs(a), freqs(b); same = fa == fb; ok2 &= same
    print(f'(2) t = {a} and 1/(2t) = {b}: {len(fa)} vertex stars, frequencies identical: {same};  distance from 1/sqrt2: {float(a) - 2**-0.5:+.5f}, {float(b) - 2**-0.5:+.5f}')
print('FINAL ok' if ok1 and ok2 else 'FINAL FAIL')
