"""DICTO's decision 1 (17 Nov 2026): grow past nine by repeating the 7 -> 9 step exactly.  This script states
the step by chain roles, checks that it rebuilds t8 and t4 exactly from the seven-triangle yantra, and then
applies it once more to the nine-triangle yantra.  Exact arithmetic on R1 (in Q) and Q3 (in Q(sqrt Delta)).

The step (roles from the free end of the chain C = [..., C5, C4, C3, C2, C1], C1 the end, a down triangle):
  new up U:   apex on C1's base;  its base on the level where C5's leg meets C4's leg      [marma (C5, U, C4) = (3,8,9)]
              its leg through the point where C5's leg meets the base G just above U's base [marma (C5, G, U) = (3,7,8)]
              and C1's leg, C5's base, U's leg must meet in one point                       [marma (C1, C5, U) = (1,3,8)]
  new down D: apex on U's base;  its base on the level where C1's leg meets C2's leg      [marma (C1, D, C2) = (1,4,6)]
              its leg through the point where C4's leg meets C2's base                     [marma (D, C2, C4) = (4,6,9)]
              and D's corner must lie on U's leg                                           [corner touch (D, D, U) = (4,4,8)]
  7 -> 9: C = [t3, t9, t2, t6, t1], G = t7, U = t8, D = t4.   9 -> 11: C = [t2, t6, t1, t8, t4].
usage: python3 step_check.py <study dir>"""
import sys, os, json
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yarr import QF

ST = sys.argv[1] if len(sys.argv) > 1 else '.'
DOWN = {1, 2, 3, 4, 5}


def load(name):
    e = json.load(open(os.path.join(ST, 'data', 'input', 'quadratic-examples.json')))[name]
    if e['Delta'] is None:
        g = lambda z: Fr(z['a'])
    else:
        QF.D = Fr(e['Delta']); g = lambda z: QF(Fr(z['a']), Fr(z.get('b', '0')))
    return {i: (g(e['b'][str(i)]), g(e['w'][str(i)]), g(e['apex'][str(i)])) for i in range(1, 10)}


def legx(T, i, d):                       # right leg of triangle i at depth d
    b, w, a = T[i]
    return w * (d - a) / (b - a)


def leg_meet(T, i, j):                   # depth where the right legs of i and j meet
    bi, wi, ai = T[i]; bj, wj, aj = T[j]
    si, sj = wi / (bi - ai), wj / (bj - aj)          # x = s (d - a)
    return (si * ai - sj * aj) / (si - sj)


def step(T, C, G):
    C5, C4, C3, C2, C1 = C[-5:]
    aU = T[C1][0]
    bU = leg_meet(T, C5, C4)
    p2 = (legx(T, C5, T[G][0]), T[G][0])               # C5's leg on G's base
    sU = p2[0] / (p2[1] - aU)
    wU = sU * (bU - aU)
    r1 = sU * (T[C5][0] - aU) - legx(T, C1, T[C5][0])  # (C1, C5, U) concurrent?
    aD = bU
    bD = leg_meet(T, C1, C2)
    p = (legx(T, C4, T[C2][0]), T[C2][0])              # C4's leg on C2's base
    sD = p[0] / (p[1] - aD)
    wD = sD * (bD - aD)
    r2 = sU * (bD - aU) - wD                           # D's corner on U's leg?
    return (bU, wU, aU), (bD, wD, aD), r1, r2


ok = True
for name in ('R1', 'Q3'):
    T = load(name)
    T7 = {i: T[i] for i in (1, 2, 3, 5, 6, 7, 9)}
    U, D, r1, r2 = step(T7, [3, 9, 2, 6, 1], 7)
    rebuilt = (U == T[8] or all(x == y for x, y in zip(U, T[8]))) and all(x == y for x, y in zip(D, T[4]))
    print(f"{name}: 7 -> 9 by the step rebuilds t8 and t4 exactly: {rebuilt}; closing residuals zero: {not r1 and not r2}")
    ok = ok and rebuilt and not r1 and not r2
    # 9 -> 11: C5 = t2, C4 = t6.  Corner touch (2,6,6) puts t6's corner on t2's leg, so the two legs meet AT
    # t6's corner, on t6's base: the new up triangle's base would lie on the line of t6's base.
    bU = leg_meet(T, 2, 6)
    same = (bU == T[6][0])
    print(f"{name}: 9 -> 11: t2's leg meets t6's leg at depth b6 exactly (new base on t6's base line): {same}")
    ok = ok and same
print("FINAL ok" if ok else "FINAL FAIL")
