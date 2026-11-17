# DICTO 2026-10-18 octet study: shared exact arithmetic in Q(sqrt5): numbers a + b*sqrt5 as Fraction pairs (as gbpc scripts).
from fractions import Fraction as Fr
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
Z = (Fr(0), Fr(0)); ONE = (Fr(1), Fr(0)); PHI = (Fr(1, 2), Fr(1, 2))
def q(s): a, b = s.split('|'); return (Fr(a), Fr(b))
def qs_(x): return f'{x[0]}|{x[1]}'
qa = lambda x, y: (x[0] + y[0], x[1] + y[1]); qs = lambda x, y: (x[0] - y[0], x[1] - y[1])
qm = lambda x, y: (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
qn = lambda x: (-x[0], -x[1]); qr = lambda r: (Fr(r), Fr(0))
def qinv(x): n = x[0] * x[0] - 5 * x[1] * x[1]; return (x[0] / n, -x[1] / n)
qd = lambda x, y: qm(x, qinv(y))
qf = lambda x: float(x[0]) + float(x[1]) * 5 ** .5
def sgn(x):
    a, b = x
    if b == 0: return (a > 0) - (a < 0)
    if a == 0: return (b > 0) - (b < 0)
    if a > 0 and b > 0: return 1
    if a < 0 and b < 0: return -1
    s = 1 if a * a > 5 * b * b else -1
    return s if a > 0 else -s
vadd = lambda u, v: [qa(a, b) for a, b in zip(u, v)]; vsub = lambda u, v: [qs(a, b) for a, b in zip(u, v)]
vmul = lambda u, s: [qm(a, s) for a in u]
dot = lambda u, v: qa(qa(qm(u[0], v[0]), qm(u[1], v[1])), qm(u[2], v[2]))
def cross(u, v): return [qs(qm(u[1], v[2]), qm(u[2], v[1])), qs(qm(u[2], v[0]), qm(u[0], v[2])), qs(qm(u[0], v[1]), qm(u[1], v[0]))]
def det3(a, b, c): return dot(a, cross(b, c))
def save(name, obj): json.dump(obj, open(os.path.join(DATA, name), 'w'), indent=1, ensure_ascii=False); print('saved data/' + name)
def load(name): return json.load(open(os.path.join(DATA, name)))
MARK = 'DICTO · dictospheres.com'
