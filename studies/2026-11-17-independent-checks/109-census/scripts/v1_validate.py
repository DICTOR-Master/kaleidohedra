"""Step 1: validate the independent tone routine on known cases."""
import sys, time
import numpy as np
from fractions import Fraction as Fr
from core import *
from universes import *

ok = True
def check(name, cond):
    global ok
    print(('PASS ' if cond else 'FAIL ') + name, flush=True)
    ok = ok and cond

t0 = time.time()
D, U, mul, conj = build_2I()
codes, cosv = exact_gram_codes(D)
print('600-cell distinct cosines:', sorted(qfloat(c) for c in cosv))
E = ToneEngine(codes, cosv, 'S3')
z = E.zeros(range(120))
print('600-cell zeros k<=20:', z)
check('600-cell rings only at 12 and 20', z == [k for k in range(1, 21) if k not in (12, 20)])

# golden sets in R^5 (centred), exact
def golden(base):
    pts = sorted(set(itertools.permutations(base)))
    n = len(pts); d = len(base)
    mean = [(Fr(sum(p[i][0] for p in pts), n), Fr(sum(p[i][1] for p in pts), n)) for i in range(d)]
    return [tuple(qsub(p[i], mean[i]) for i in range(d)) for p in pts]
p2, p1, one, zero = (1, 1), (0, 1), (1, 0), (0, 0)
X = golden((p2, p2, p2, p1, zero)); F = golden((p2, p2, one, one, zero))
for name, S, want in (('X', X, [1, 2, 5, 7]), ('F', F, [1, 2, 3, 6])):
    c, v = exact_gram_codes(S)
    zz = ToneEngine(c, v, 'S3').zeros(range(len(S)))
    print(name, len(S), 'zeros', zz)
    check(f'{name} ({len(S)} pts, R^5 centred) silent exactly {want}', zz == want)

# H4 on the 600-cell
P, info = quaternion_maps(U, U, U)
print('H4 order', len(P))
check('H4 has 14400 distinct maps', len(P) == 14400)
check('H4 preserves the exact Gram matrix', all((codes[np.ix_(p, p)] == codes).all() for p in P[::97]))

# outer automorphism alpha and twisted classes {a x alpha(a)^-1}
al = galois_alpha_2I(D, U)
hom = all(al[mul[i, j]] == mul[al[i], al[j]] for i in range(120) for j in range(120))
check('alpha is an automorphism of 2I', hom)
gens = [mul[mul[a][np.arange(120)]] for a in range(0)]
tw_perms = []
for a in range(120):
    # x -> a x alpha(a)^-1
    tw_perms.append(mul[mul[a, np.arange(120)], conj[al[a]]])
lab = orbit_labels(120, tw_perms)
sizes = sorted(np.bincount(lab))
print('twisted class sizes under alpha:', sizes)
check('twisted classes 20,20,20,30,30', sizes == [20, 20, 20, 30, 30])
sig = []
for o in range(lab.max() + 1):
    idx = np.where(lab == o)[0]
    zz = E.zeros(idx); sig.append((len(idx), zz)); print('  class', len(idx), 'zeros', zz)
want = sorted([(20, [1, 2, 5, 7]), (20, [1, 2, 5, 7]), (30, [1, 2, 3, 6]), (30, [1, 2, 3, 6])])
check('X, -X kill 1,2,5,7 and F, -F kill 1,2,3,6 inside the 600-cell',
      all(s in sig for s in want) and sum(1 for s in sig if s == (20, [1, 2, 5, 7])) == 2
      and sum(1 for s in sig if s == (30, [1, 2, 3, 6])) == 2)

# E8 shells: B(x,y)=a+b for <x,y> = a + b sqrt5
print('elapsed', round(time.time() - t0, 1))
print('FINAL ok' if ok else 'FINAL FAIL validation')
