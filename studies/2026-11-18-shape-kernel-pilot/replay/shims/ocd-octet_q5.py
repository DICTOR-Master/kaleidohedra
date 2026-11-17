# q5.py for the replay of 2026-10-18-ocd-octet: the Q(sqrt5) pair arithmetic now comes from the shape kernel (kernel/pairs.py);
# the vector helpers, save/load and MARK below are the original module's lines, unchanged.
from fractions import Fraction as Fr
import json, os
from kernel.pairs import Z, ONE, PHI, q, qs_, qa, qs, qm, qn, qr, qinv, qd, qf, sgn
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
vadd = lambda u, v: [qa(a, b) for a, b in zip(u, v)]; vsub = lambda u, v: [qs(a, b) for a, b in zip(u, v)]
vmul = lambda u, s: [qm(a, s) for a in u]
dot = lambda u, v: qa(qa(qm(u[0], v[0]), qm(u[1], v[1])), qm(u[2], v[2]))
def cross(u, v): return [qs(qm(u[1], v[2]), qm(u[2], v[1])), qs(qm(u[2], v[0]), qm(u[0], v[2])), qs(qm(u[0], v[1]), qm(u[1], v[0]))]
def det3(a, b, c): return dot(a, cross(b, c))
def save(name, obj): json.dump(obj, open(os.path.join(DATA, name), 'w'), indent=1, ensure_ascii=False); print('saved data/' + name)
def load(name): return json.load(open(os.path.join(DATA, name)))
MARK = 'DICTO · dictospheres.com'
