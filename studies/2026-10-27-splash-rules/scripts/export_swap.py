# Export the Swap Rule figure pieces (OBJ, cartesian): at d^2 = s*2/3, lam: pure cubic tet (ABC), pure hexagonal tet (AC), and a mixed
# c|h tet (lower layer c, upper h) split at its gap's mid-plane into bottom and top parts. Also prints exact volumes of the parts.
import sys, os, itertools
sys.path.insert(0, os.path.expanduser('~/kres-tmp/st57/scripts')); os.chdir(os.path.expanduser('~/kres-tmp/st57/scripts'))
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull
from engine import Net, Cell, aff_eval
sys.path.insert(0, os.path.expanduser('~/kres-tmp/splash')); from splash import net_for, steps
_h = open('exact_halves.py').read(); exec(_h[_h.index('def corners_at'):_h.index('def fp(')])
s, lam = Fr(sys.argv[1]), Fr(sys.argv[2]); OUT = os.path.expanduser('~/kres-tmp/splash/fig'); os.makedirs(OUT, exist_ok=True)
def build(word): spec = net_for(word, s); return Net(word, spec['G'], spec['T'], spec['motif'], spec['w']), spec
def cart(G, pts):
    B = np.array([[1, 0, 0], [0.5, 3 ** .5 / 2, 0], [0, 0, float(G[2][2]) ** .5]]); return np.array([[float(x) for x in p] for p in pts]) @ B
def obj(name, P, ctr):
    P = P - ctr; H = ConvexHull(P); f = open(f'{OUT}/{name}.obj', 'w')
    for v in P: f.write('v %.6f %.6f %.6f\n' % tuple(v))
    for t in H.simplices:
        a, b, c = P[t]; n = np.cross(b - a, c - a)
        if np.dot(n, a - P.mean(0)) < 0: t = t[::-1]
        f.write('f %d %d %d\n' % tuple(i + 1 for i in t))
    print(name, 'volume %.6f' % H.volume)
def ltype(st, k): n = len(st); return 'c' if st[(k - 1) % n] == st[k % n] else 'h'
for word, want, tag in (('ABC', None, 'pure-c'), ('AC', None, 'pure-h'), ('ACBC', ('c', 'h'), 'mixed')):
    net, spec = build(word); n = len(word); st = steps(word)
    for i, (k, p) in enumerate(spec['motif']):
        if k != 'tet' or i % 3 != 1: continue
        g = i // 3
        if want and (ltype(st, g), ltype(st, g + 1)) != want: continue
        c = Cell(net, i, (lam,), Fr(12))
        if c.empty: continue
        X = corners_at(c, lam); P = cart(net.G, X); ctr = P.mean(0); zc = Fr(2 * g + 1, 2 * n)
        if tag == 'mixed':
            obj('mixed-bottom', cart(net.G, half(c, lam, zc, False)), ctr); obj('mixed-top', cart(net.G, half(c, lam, zc, True)), ctr)
        else:
            obj(tag, P, ctr); obj(tag + '-bottom', cart(net.G, half(c, lam, zc, False)), ctr); obj(tag + '-top', cart(net.G, half(c, lam, zc, True)), ctr)
        print(tag, word, 'site', i, 'mid-plane height (cell fraction)', zc); break
