# Scutoid test (DICTO 2026-10-27: "the scutoids are similar to Janus c/h"). Scutoid (Gomez-Galvez et al. 2018, Nat. Commun. 9:2960):
# a cell between two parallel surfaces whose polygons on the two surfaces differ, with at least one vertex strictly between them where
# neighbours exchange (a Y junction). Here: the slab between the two layer planes of a piece's gap; for each piece, the cross-section just
# above the lower plane and just below the upper plane (sides = faces crossing; neighbours = the sites behind those faces), and every
# corner strictly inside the slab where the set of crossing faces changes. Exact (rational corners at rational lambda).
import sys, os
sys.path.insert(0, os.path.expanduser('~/kres-tmp/st57/scripts')); os.chdir(os.path.expanduser('~/kres-tmp/st57/scripts'))
from fractions import Fraction as Fr
from engine import Net, Cell, aff_eval
sys.path.insert(0, os.path.expanduser('~/kres-tmp/splash')); from splash import net_for, steps
def ltype(st, k): n = len(st); return 'c' if st[(k - 1) % n] == st[k % n] else 'h'
def crossing(c, Z, h):
    out = []
    for k in set(c.faces()):
        zs = [Z[i] for i, p in enumerate(c.corners) if k in p['on']]
        if min(zs) < h < max(zs): out.append((c.H[k]['kind'], c.H[k]['j'], tuple(c.H[k]['kv'])))
    return out
def test(label, word, s, lam, site):
    spec = net_for(word, Fr(s)); net = Net(word, spec['G'], spec['T'], spec['motif'], spec['w']); n = len(word); st = steps(word)
    c = Cell(net, site, (Fr(lam),), Fr(12)); g = site // 3
    Z = [aff_eval(p['P'][2], (Fr(lam),)) for p in c.corners]
    z0, z1 = Fr(g, n), Fr(g + 1, n); eps = Fr(1, 10 ** 6)
    if not (min(Z) < z0 + eps and max(Z) > z1 - eps): print(f'{label}: does not span its gap (z {float(min(Z)*n-g):.3f}..{float(max(Z)*n-g):.3f} in gap units): not a slab cell'); return
    lo, hi = crossing(c, Z, z0 + eps), crossing(c, Z, z1 - eps)
    inner = sorted({z for z in Z if z0 < z < z1})
    changes = 0; prev = set(lo)
    for z in inner + [z1 - eps]:
        cur = set(crossing(c, Z, z + eps if z < z1 - eps else z))
        if cur != prev: changes += 1
        prev = cur
    sl = set(lo); sh = set(hi)
    verdict = 'SCUTOID' if (len(lo) != len(hi) or sl != sh) and inner else ('prism-like (same polygon and neighbours top and bottom)' if sl == sh else 'differs but no inner corner')
    print(f'{label}: {word} s={s} lam={lam} site {site} ({ltype(st, g)} below, {ltype(st, g + 1)} above): bottom {len(lo)}-gon, top {len(hi)}-gon; '
          f'neighbours only below {len(sl - sh)}, only above {len(sh - sl)}; corners strictly inside the slab {len(inner)}; neighbour changes {changes} -> {verdict}', flush=True)
# Chucky and Fang: #57 Janus c/h octahedral pieces of ABAC at -3/8 and 5/24 (s = 1); Ganesha: mixed tetrahedral piece, s = 3/4, lam = 1/10, ACBC site 4.
# Search the mixed octahedral sites of ABAC (s = 1) for both weights, and the Ganesha site.
for lam, nm in (('-3/8', 'Chucky window'), ('5/24', 'Fang window')):
    spec = net_for('ABAC', Fr(1)); st = steps('ABAC')
    for i, (k, p) in enumerate(spec['motif']):
        g = i // 3
        if k == 'oct' and ltype(st, g) != ltype(st, g + 1): test(f'{nm} (Janus octahedral)', 'ABAC', 1, lam, i)
test('Ganesha', 'ACBC', '3/4', '1/10', 4)
test('Ganesha (mirror)', 'ACBC', '3/4', '1/10', 5)
test('pure cubic tetrahedral (control)', 'ABC', '3/4', '1/10', 1)
test('pure cubic octahedral (control)', 'ABC', '1', '5/24', 0)
