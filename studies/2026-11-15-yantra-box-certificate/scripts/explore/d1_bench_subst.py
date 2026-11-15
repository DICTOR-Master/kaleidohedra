"""Bench for the kernel normaliser: main H~ composed with the chart W map must equal c p^18 H_W (b1_charts).  Writes
lean/bench/BenchSubst.lean.  Uses Sage only to find the constant c."""
import json, os
from sage.all__sagemath_singular import QQ, PolynomialRing
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D_ = lambda *p: os.path.join(HERE, *p)
main = json.load(open(D_('data', 'polys-utr.json'))); W = json.load(open(D_('data', 'polys-utr-W.json')))
R = PolynomialRing(QQ, 'p,q,r'); p, q, r = R.gens()
def dec(P, gens): return sum(QQ(c) * gens[0]**e[0] * gens[1]**e[1] * gens[2]**e[2] for e, c in P)
H = dec(main['F']['H1'], (p, q, r)); HW = dec(W['F']['H1'], (p, q, r))
comp = H(p, p**4 * (1 + p**4 * (q - 4)), 1 + p + p**2 * (r - 4))
c = comp / (p**18 * HW); print('c =', c)
assert c in QQ
def zp(P):
    s = '.nil'
    for e, cc in reversed(sorted(P, key=lambda t: tuple(t[0]))):
        cc = int(cc); lit = f'(.ofNat {cc})' if cc >= 0 else f'(.negSucc {-cc - 1})'
        s = f'(.cons {lit} {e[0]} {e[1]} {e[2]} {s})'
    return s
c = QQ(c); num, den = c.numerator(), c.denominator()
src = f'''import YantraCert.ZPoly
set_option maxRecDepth 200000
namespace YantraCert.BenchSubst
open YantraCert
noncomputable def H : ZP := {zp(main['F']['H1'])}
noncomputable def HW : ZP := {zp(W['F']['H1'])}
noncomputable def X : ZP := (.cons 1 1 0 0 .nil)
noncomputable def Y : ZP := (.cons (.negSucc 3) 8 0 0 (.cons 1 8 1 0 (.cons 1 4 0 0 .nil)))
noncomputable def Z : ZP := (.cons 1 0 0 0 (.cons 1 1 0 0 (.cons (.negSucc 3) 2 0 0 (.cons 1 2 0 1 .nil))))
theorem ok : ZP.eqv (ZP.mul (ZP.const {den}) (ZP.subst X Y Z H)) (ZP.mul (ZP.const {num}) (ZP.mul (ZP.cons 1 18 0 0 .nil) HW)) = true := by decide +kernel
end YantraCert.BenchSubst
'''
os.makedirs(D_('lean', 'bench'), exist_ok=True)
open(D_('lean', 'bench', 'BenchSubst.lean'), 'w').write(src)
print('terms', len(main['F']['H1']), len(W['F']['H1']))
