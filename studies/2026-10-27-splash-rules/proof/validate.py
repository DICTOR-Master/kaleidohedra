# Swap Rule proof, independent check against the census engine (DICTO 2026-10-27).
# The engine builds every power cell of a WHOLE periodic stacking from scratch (all sites within distance^2 12, exact corners). For each
# sample (s, lam), each stacking, each gap and each of its three sites, the half below and the half above the gap's mid-plane are
# compared (exact fingerprint: sorted squared distances of all corner pairs, cut points included) with the proof's model half
# K_low(role, type) of swapgeom.py (lower half; upper half = mirror role, type of the upper layer), whose corners are found here
# exactly (float halfspace intersection proposes, exact 3-plane solves decide, every corner re-checked against every plane).
# Usage: python validate.py <s> <lam1,lam2,...> [words]       prints PASS/FAIL per half and a total; a FAIL list for sharpness runs.
import sys, os, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.expanduser('~/kres-tmp/st57/scripts')); sys.path.insert(0, os.path.expanduser('~/kres-tmp/splash'))
from swapgeom import sites, row, ROLE, MIRROR, _solve, Qf
_cwd = os.getcwd(); os.chdir(os.path.expanduser('~/kres-tmp/st57/scripts'))
from engine import Net, Cell, gdot, vsub, aff_eval
from splash import net_for
_h = open('exact_halves.py').read(); exec(_h[_h.index('def corners_at'):_h.index('def cell(')])
os.chdir(_cwd)

def model_half(role, t, q, lam):
    """exact corners (x, y, zeta) of K_low(role, t) cut at zeta <= 1/2, at (q, lam)"""
    i, S = sites(role, t)
    H = []
    for j in S['K']:
        a, b = row(i, j); H.append(([a[2], a[3], a[4]], b - a[0] * q - a[1] * lam))
    H.append(([Fr(0), Fr(0), Fr(1)], q / 2))
    A = np.array([[float(x) for x in h[0]] for h in H]); bb = np.array([float(h[1]) for h in H]); nr = np.linalg.norm(A, axis=1)
    res = linprog(np.r_[0, 0, 0, -1.0], A_ub=np.c_[A, nr], b_ub=bb, bounds=[(None, None)] * 3 + [(0, None)], method='highs')
    if res.status != 0 or res.x[-1] < 1e-9: return []
    hs = HalfspaceIntersection(np.c_[A, -bb], res.x[:3]); pts = set()
    for v in hs.intersections:
        r = A @ v - bb; tight = [k for k in np.argsort(np.abs(r)) if abs(r[k]) < 1e-6 * max(1, nr[k])]
        for tri in itertools.combinations(tight, 3):
            X = _solve([H[k][0] for k in tri], [H[k][1] for k in tri])
            if X is not None: break
        assert X is not None and all(sum(h[0][r_] * X[r_] for r_ in range(3)) <= h[1] for h in H)
        pts.add((X[0], X[1], X[2] / q))
    return sorted(pts)
def fp_model(pts, q):
    return tuple(sorted(Qf((p[0] - r[0], p[1] - r[1])) + q * (p[2] - r[2]) ** 2 for p, r in itertools.combinations(pts, 2)))
def layer_type(w, k): n = len(w); return 'c' if w[(k - 1) % n] != w[(k + 1) % n] else 'h'
ROLE_OF = {0: 'oct', 1: 'tetX', 2: 'tetY'}
if __name__ == '__main__':
    s = Fr(sys.argv[1]); q = s * Fr(2, 3); lams = [Fr(x) for x in sys.argv[2].split(',')]
    words = sys.argv[3].split(',') if len(sys.argv) > 3 else ['ABC', 'AC', 'ACBC', 'ACABC', 'ACBCAC', 'ACBABC']
    ok = bad = 0; fails = []
    for lam in lams:
        M = {}
        for role in ROLE:
            for t in 'ch': M[(role, t)] = fp_model(model_half(role, t, q, lam), q)
        for w in words:
            spec = net_for(w, s); net = Net(w, spec['G'], spec['T'], spec['motif'], spec['w']); n = len(w)
            for k in range(n):
                for jr in range(3):
                    i = 3 * k + jr; role = ROLE_OF[jr]
                    c = Cell(net, i, (lam,), Fr(12)); zc = (k + Fr(1, 2)) / n
                    for up in (False, True):
                        e = tuple(fp(net.G, half(c, lam, zc, up))) if not c.empty else ()
                        key = (MIRROR[role], layer_type(w, k + 1)) if up else (role, layer_type(w, k))
                        m = M[key]
                        good = (e == m) or (len(e) <= 3 and len(m) <= 3 and e == m)
                        ok += good; bad += not good
                        if not good: fails.append(f's={s} lam={lam} {w} gap {k} {role} {"upper" if up else "lower"} half: engine {len(e)} pairs vs model {key} {len(m)} pairs')
        print(f's={s} lam={lam}: running {ok} PASS {bad} FAIL', flush=True)
    print('\n'.join(fails[:30])); print(f'TOTAL s={s}: {ok} PASS, {bad} FAIL')
