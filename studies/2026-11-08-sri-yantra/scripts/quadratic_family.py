"""Theorem Q (quadratic Sri Yantras).  Take the leg slopes u (of t7, apex at the top point O) and
v (of t3, apex at the bottom point T) and the depths Q = b6, S = b9 all RATIONAL.  Then
P = v^2/(1+v^2), R = 1/(1+u^2) and the half-widths w3 = v/(1+v^2), w7 = u/(1+u^2) are rational
(rational points of the circle), the whole chain of Huet's conditions is rational except the one
Apollonius step, a quadratic in b1 with discriminant Delta in Q.  So every coordinate of the yantra
lies in Q(sqrt Delta) and all 18 marmas, 6 corner touches, 7 apex-on-base points and 6 circle points
hold EXACTLY.

This script (standard library only, no floats in any check):
 1. builds three named examples exactly in Q(sqrt Delta),
 2. re-proves every condition = 0 exactly (a + b sqrt Delta with a = b = 0),
 3. checks the configuration (base order, apex sides, every corner inside or on the circle) exactly,
 4. writes the exact coordinates to ../data/quadratic-examples.json."""
import json
from fractions import Fraction as Fr
from quadfield import QF
from model import solve, all_conditions, order_ok, marma_point, MARMAS, CORNERS
from math import isqrt


def rat_sqrt(q):
    q = Fr(q)
    if q < 0: return None
    n, d = isqrt(q.numerator), isqrt(q.denominator)
    return Fr(n, d) if n * n == q.numerator and d * d == q.denominator else None


def build(u, v, Q, S):
    u, v, Q, S = map(Fr, (u, v, Q, S))
    P = v * v / (1 + v * v); R = 1 / (1 + u * u)
    w3 = v / (1 + v * v); w7 = u / (1 + u * u)
    holder = {}

    def sq(z):
        r = rat_sqrt(z)
        if r is not None: holder['D'] = None; return r
        K = QF.field(z); holder['D'] = Fr(z); return K(0, 1)
    for root in (0, 1):
        tri = solve(P, Q, R, S, w3, w7, sq, root)
        if order_ok(tri, 0):
            return tri, holder['D'], root
    return None, holder.get('D'), None


def fmt(z):
    if isinstance(z, QF): return {'a': str(z.a), 'b': str(z.b), 'sqrt_of': str(z.D)}
    return {'a': str(Fr(z)), 'b': '0'}


TRAD48 = [6, 12, 17, 20, 23, 27, 30, 36, 42]  # Kaivalyasrama's 48-part grid (Chiodo 2021, Fig. 2a), depth from top

EXAMPLES = {
    # name: (u, v, Q, S, note)   placeholder names; DICTO names them
    'R1': (Fr(19, 24), Fr(2, 3), Fr(8, 15), Fr(8, 9),
           'Delta is a rational square: a fully RATIONAL yantra (found by rational_search.py; the only one in 627 million tests of rational_search2.py)'),
    'Q1': (Fr(13, 16), Fr(12, 17), Fr(29, 54), Fr(5, 6), 'small-height rationals near Huet\'s classical parameters'),
    'Q2': (Fr(4, 5), Fr(7, 10), Fr(8, 15), Fr(5, 6), 'smaller heights, a little further from Huet'),
    'Q3': (Fr(3, 4), Fr(3, 4), Fr(11, 20), Fr(11, 12),
           "on DICTO's 3-4-5 rhombus (u = v = 3/4), Q and S rational next to the degree-20 Rh345 values"),
}

if __name__ == '__main__':
    out = {}; all_ok = True
    for name, (u, v, Q, S, note) in EXAMPLES.items():
        tri, D, root = build(u, v, Q, S)
        if tri is None:
            print(name, 'NO admissible branch'); all_ok = False; continue
        conds = all_conditions(tri)
        zero = all((c.is_zero() if isinstance(c, QF) else c == 0) for _, c in conds)
        n_m = sum(1 for n, _ in conds if n.startswith('marma')) * 2
        n_c = sum(1 for n, _ in conds if n.startswith('corner')) * 2
        dev48 = max(abs(float(tri['b'][i]) - TRAD48[i - 1] / 48) for i in range(1, 10))
        print(f'{name}: u={u} v={v} Q={Q} S={S}  ({note})')
        print(f'   field Q(sqrt Delta), Delta = {D}' if D is not None else '   field Q (Delta is a square)')
        print(f'   {len(conds)} condition expressions, all exactly zero: {zero}  ({n_m} marma points, {n_c} corner touches)')
        print('   depths b1..b9 (x48):', ' '.join(f'{48 * float(tri["b"][i]):.3f}' for i in range(1, 10)),
              f'  max |b - grid/48| = {dev48:.4f}')
        all_ok = all_ok and zero
        out[name] = {'u': str(u), 'v': str(v), 'Q': str(Q), 'S': str(S), 'note': note,
                     'Delta': None if D is None else str(D), 'branch': root,
                     'b': {i: fmt(tri['b'][i]) for i in range(1, 10)},
                     'w': {i: fmt(tri['w'][i]) for i in range(1, 10)},
                     'apex': {i: fmt(tri['a'][i]) for i in range(1, 10)},
                     'marmas_right': {f'{p}{q}{r}': [fmt(c) for c in marma_point(tri, p, q, r)] for p, q, r in MARMAS},
                     'conditions_zero': zero, 'max_dev_from_48_grid': dev48}
    json.dump(out, open('../data/quadratic-examples.json', 'w'), indent=1)
    print('FINAL ok' if all_ok and len(out) == len(EXAMPLES) else 'FINAL FAIL quadratic family')
