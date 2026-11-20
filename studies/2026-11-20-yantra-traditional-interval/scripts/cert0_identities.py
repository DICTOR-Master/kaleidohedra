"""Certificate 0: the identities of the arrangement on the rhombus branch, decided exactly.

At two points of the branch (u = 7/10 and u = 29/50) the 27 lines are enclosed to about 600 digits (ycert.branch at 2000 bits).
A triple of lines whose determinant ball contains 0 is a candidate identity. Each candidate is decided EXACTLY, as in #103
Proposition 11 (certified_counts.py of the #103 audit): the same determinant is computed symbolically in the model of case K
(the rhombus family u = v, generic in y = u^2, Q, S, t = b1; inputs/model.py, inputs/stage2-K.json) and must be identically zero
or a multiple of the closing numerator Fc (Huet's closing equation, which holds on every member of the family). Every other
triple is certified nonzero at both points.
Writes data/identities.json (the identity triples). Expected: 115 = 84 triples of parallel bases + 31 Huet conditions.
usage: python -u cert0_identities.py"""
import sys, os, json, time
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'inputs'))
import flint
from flint import arb, fmpq
flint.ctx.prec = 2000
import ycert as Y
import model
from sage.all__sagemath_singular import QQ, PolynomialRing

Rg = PolynomialRing(QQ, 'y,p,Q,S,t'); y, p, Qs, Ss, ts = Rg.gens(); Fd = Rg.fraction_field(); one = Fd(1)
P_ = Fd(y) / (1 + y); R_ = one / (1 + y); W3 = one / (1 + y); W7 = one / (1 + y)       # case K of the audit (u = v), x scaled by 1/u
trs = model.solve(P_, Fd(Qs), R_, Fd(Ss), W3, W7, sqrt=None, b1=Fd(ts))
Fc = Rg(json.load(open(os.path.join(ROOT, 'inputs', 'stage2-K.json')))['Fc'])
def symb_seg(n):
    k, i = n[0], int(n[1:]); W_, B_, A_ = trs['w'][i], trs['b'][i], trs['a'][i]
    if k == 'B': return ((-W_, B_), (W_, B_))
    if k == 'R': return ((W_, B_), (Fd(0), A_))
    return ((-W_, B_), (Fd(0), A_))
LS = {n: Y.lc(symb_seg(n)) for n in Y.NAMES}
def exact_identity(tr):
    d = Y.det3(*(LS[n] for n in tr))
    return d == 0 or Fc.divides(Fd(d).numerator())

TG = {fmpq(7, 10): 0.234834, fmpq(29, 50): 0.0820131}
cand_sets = []; ok = True
for uq, tg in TG.items():
    U = arb(uq)
    Sb, T, _ = Y.branch(U, tg)
    yy = Y.build(U, T, Sb)
    adm = [(nm, q) for nm, q in Y.admissibility(yy)]
    bad = [nm for nm, q in adm if not q > 0]
    L = {n: Y.lc(s) for n, s in Y.segments(yy).items()}
    cand = []; minnz = None
    for tr in Y.TRIPLES:
        d = Y.det3(*(L[n] for n in tr))
        if d.contains(0): cand.append(tr)
        else:
            m = abs(d).lower(); minnz = m if minnz is None or m < minnz else minnz
    say(f'u = {uq}: t radius {arb(T.rad()).str(3, radius=False)}, admissible (strict) {not bad} {bad}; candidates (ball contains 0) {len(cand)}; '
        f'smallest certified |det| among the others {arb(minnz).str(5, radius=False)}')
    ok = ok and not bad
    cand_sets.append(set(cand))
same = cand_sets[0] == cand_sets[1]
cands = sorted(cand_sets[0] | cand_sets[1])
base = [tr for tr in cands if all(n[0] == 'B' for n in tr)]
dec = {tr: exact_identity(tr) for tr in cands}
say(f'same candidates at both points: {same}; {len(cands)} candidates: {len(base)} triples of bases, {len(cands) - len(base)} others; '
    f'decided exactly zero (identically, or a multiple of Fc): {sum(dec.values())}')
notid = [tr for tr, v in dec.items() if not v]
if notid: say('NOT identities:', notid)
others = [tr for tr in cands if tr not in base]
say('the non-base identities:', ['-'.join(tr) for tr in others])
# the two pairs of opposite rhombus sides (u = v): parallel identically, and distinct (they cross the axis at depths 1 and 0)
def dirn(n): (p1, p2) = symb_seg(n); return (p2[0] - p1[0], p2[1] - p1[1])
par = {}
for p_, q_ in [('R3', 'L7'), ('L3', 'R7')]:
    d1, d2 = dirn(p_), dirn(q_); par[p_ + '-' + q_] = (d1[0] * d2[1] - d1[1] * d2[0]) == 0
say('opposite rhombus sides parallel identically (exact, case K):', par, '; R3 and L3 end at the apex (0, 1), R7 and L7 at (0, 0): distinct lines')
json.dump({'identities': ['-'.join(tr) for tr in cands], 'base_triples': len(base), 'huet': len(others),
           'parallel_pairs': [k for k, v in par.items() if v]},
          open(os.path.join(ROOT, 'data', 'identities.json'), 'w'), indent=0)
good = ok and same and not notid and len(cands) == 115 and len(base) == 84 and all(par.values())
print('FINAL ok' if good else f'FINAL FAIL: ok {ok}, same {same}, not identities {len(notid)}, count {len(cands)}')
