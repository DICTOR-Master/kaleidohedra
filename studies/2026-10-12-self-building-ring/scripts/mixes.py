# Which mixes of kit pieces (type x size phi^k) can make up a ring at all? (2026-10-12)
# Necessary conditions (hadwiger.py): the refined edge invariant H (2 components in Q(sqrt5), orientation-free because all kit
# edges lie on the 15 two-fold axes, one class) must sum to H(ring) = 0, and the volumes to 3 vol(P). Integer program: fewest
# pieces; then a list of distinct small mixes (no-good cuts), and for each type/size whether it can appear at all.
import sys, os, json, itertools, numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.optimize import milp, LinearConstraint, Bounds
PHI = (1 + 5 ** .5) / 2
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/hadwiger-rows.json')))
RING = sys.argv[1] if len(sys.argv) > 1 else 'J2'
KMIN = int(os.environ.get('KMIN', '-5')); KMAX = int(os.environ.get('KMAX', '0')); NSOL = int(os.environ.get('NSOL', '15'))
types = sorted(set(k.split('|')[0] for k in D['rows']))
Hrow = {}
for k, v in D['rows'].items():
    t = k.split('|')[0]
    h = {kk: (float(Fraction(p)) + float(Fraction(q)) * PHI) for kk, (p, q) in v.items()}
    Hrow.setdefault(t, h)
    assert all(abs(Hrow[t].get(kk, 0) - h.get(kk, 0)) < 1e-9 for kk in set(h) | set(Hrow[t])), f'{t}: H depends on the turn?'
comps = sorted(set(kk for h in Hrow.values() for kk in h))
print(f'H is the same in all turns for every piece; components {comps}')
for t in types: print(f'  H({t}) = ' + ', '.join(f'{Hrow[t].get(c, 0):+.6f}' for c in comps) + f'; volume {D["volumes"][t]:.9f}')
# conjugate embedding: an element p + q phi of Q(sqrt5) is zero iff p + q phi = 0 and p + q phibar = 0; we use exact (p, q)
def pq(t, c):
    for k, v in D['rows'].items():
        if k.split('|')[0] == t:
            p, q = v.get(c, ['0', '0']); return Fraction(p), Fraction(q)
def times_phi(p, q, k):
    for _ in range(abs(k)):
        p, q = (q, p + q) if k > 0 else (q - p, p)
    return p, q
def vpq(t):
    """volume as p + q phi (rational), found from the float by a small search"""
    x = D['volumes'][t]
    for den in (12, 24, 48, 60, 120, 240):
        for q in range(-400, 401):
            p = x * den - q * PHI
            if abs(p - round(p)) < 1e-7: return Fraction(round(p), den), Fraction(q, den)
    raise ValueError(t)
cols = [(t, k) for t in types for k in range(KMIN, KMAX + 1)]
A, names = [], []
for c in comps:
    for part in (0, 1):
        A.append([float(times_phi(*pq(t, c), k)[part]) for t, k in cols]); names.append(f'H{c}[{part}]')
for part in (0, 1):
    A.append([float(times_phi(*vpq(t), 3 * k)[part]) for t, k in cols]); names.append(f'vol[{part}]')
A = np.array(A); ringvol = times_phi(*vpq(RING), 0); b = np.r_[np.zeros(2 * len(comps)), 3 * float(ringvol[0]), 3 * float(ringvol[1])]
print(f'\n{RING} ring: {len(cols)} columns (types {types}, sizes phi^{KMIN}..phi^{KMAX})')
cons = [LinearConstraint(A, b - 1e-9, b + 1e-9)]
sols = []
for it in range(NSOL):
    res = milp(np.ones(len(cols)), constraints=cons, integrality=np.ones(len(cols)), bounds=Bounds(0, 400), options={'time_limit': 300})
    if res.x is None: print('no (more) mixes:', res.message); break
    x = np.round(res.x).astype(int); used = {f'{cols[i][0]}@phi^{cols[i][1]}': int(x[i]) for i in np.where(x > 0)[0]}
    print(f'  mix {it + 1}: {int(x.sum())} pieces: {used}', flush=True); sols.append(used)
    # no-good cut on the support: exclude this exact count vector  (sum over support of x_i <= total-1 OR others >0): use support cut
    sup = np.where(x > 0)[0]; row = np.zeros(len(cols)); row[sup] = 1; row[np.setdiff1d(np.arange(len(cols)), sup)] = -1
    cons.append(LinearConstraint(row[None, :], -np.inf, len(sup) - 1))
# which (type, size) can appear in some mix at all (LP over reals is enough to say "cannot")
can = []
for i, (t, k) in enumerate(cols):
    res = milp(-np.eye(len(cols))[i], constraints=[LinearConstraint(A, b - 1e-9, b + 1e-9)], integrality=np.ones(len(cols)), bounds=Bounds(0, 400), options={'time_limit': 60})
    if res.x is not None and res.x[i] > .5: can.append(f'{t}@phi^{k}')
print(f'\n{RING} ring: piece sizes that occur in at least one balanced mix: {can}')
json.dump({'mixes': sols, 'possible': can}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/mixes-{RING}-k{KMIN}..{KMAX}.json'), 'w'), indent=1)
