# Swap Rule, step 1 (DICTO 2026-10-27 "so a swap rule theorem"): find the cut that explains it. For squashed stackings (d^2 = s*2/3),
# cut each MIXED tetrahedral piece by a horizontal plane at several heights (relative to its gap: 0 = lower layer, 1 = upper layer)
# and test, exactly, whether the part below is congruent to the part below of a pure piece (cubic ABC or hexagonal AC, same s, same
# cut) and the part above likewise. Congruence: equal sorted exact squared distances of all corner pairs (#57 exact_halves method).
import sys, os, itertools
sys.path.insert(0, os.path.expanduser('~/kres-tmp/st57/scripts')); os.chdir(os.path.expanduser('~/kres-tmp/st57/scripts'))
from fractions import Fraction as Fr
from engine import Net, Cell, aff_eval, gdot, vsub
sys.path.insert(0, os.path.expanduser('~/kres-tmp/splash')); from splash import net_for, steps
_h = open('exact_halves.py').read(); exec(_h[_h.index('def corners_at'):_h.index('def cell(')])
def cell(net, i, lam): c = Cell(net, i, (lam,), Fr(12)); return None if c.empty else c
s = Fr(sys.argv[1]); lams = [Fr(x) for x in sys.argv[2].split(',')]
CUTS = [Fr(0), Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(1)]
def build(word): spec = net_for(word, s); return Net(word, spec['G'], spec['T'], spec['motif'], spec['w']), spec
def ltype(st, k): n = len(st); return 'c' if st[(k - 1) % n] == st[k % n] else 'h'     # type of layer k from steps k-1, k
REF = {'c': build('ABC'), 'h': build('AC')}
def parts(net, spec, i, lam, n):
    c = cell(net, i, lam)
    if c is None: return None
    g = i // 3; out = {}
    for u in CUTS:
        zc = (g + u) / n
        out[u] = (tuple(fp(net.G, half(c, lam, zc, False))), tuple(fp(net.G, half(c, lam, zc, True))))
    return out
for lam in lams:
    R = {}
    for t, (net, spec) in REF.items():
        n = len(spec['motif']) // 3
        for i in range(len(spec['motif'])):
            if spec['motif'][i][0] != 'tet': continue
            p = parts(net, spec, i, lam, n)
            if p: R.setdefault(t, []).append((i % 3, p))
    for word in ('ACABC', 'ACBCAC', 'ACBABC', 'ACBC'):
        net, spec = build(word); n = len(word); st = steps(word)
        for i in range(len(spec['motif'])):
            if spec['motif'][i][0] != 'tet': continue
            g = i // 3; tl, tu = ltype(st, g), ltype(st, g + 1)
            if tl == tu: continue                                   # pure context: skip
            p = parts(net, spec, i, lam, n)
            if p is None: continue
            res = []
            for u in CUTS:
                dn = [t for t in 'ch' for j, q in R.get(t, []) if j == i % 3 and q[u][0] == p[u][0]]
                up = [t for t in 'ch' for j, q in R.get(t, []) if j == i % 3 and q[u][1] == p[u][1]]
                res.append(f"cut {u}: below={''.join(sorted(set(dn))) or '-'} above={''.join(sorted(set(up))) or '-'}")
            print(f"s={s} lam={lam} {word} site {i} ({'tetX' if i % 3 == 1 else 'tetY'}) layers {tl}|{tu}: " + '; '.join(res), flush=True)
