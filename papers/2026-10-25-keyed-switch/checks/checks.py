# #56 exact checks (census engine, sympy): the twinned (gyrated) octet's weight walk — piece volumes (Cartesian, hcp edge 1)
# at the octet, at the equal-volume point (Sonsam/Lahdeli), at 5/24 (Ian Dury + 60° rhombohedron) and at 3/8 (Blockhead);
# the ordinary octet's equal-volume point (Samson/Delilah); pieces per cell. Run from this folder.
import sys
from fractions import Fraction as Fr
import sympy as sp
sys.path.insert(0, '../../../studies/2026-10-25-relay-census/scripts')
from engine import Net, Cell, LAM, cell_volume
from networks import NETS
out, fails = [], 0
def chk(name, ok, detail=''):
    global fails; fails += (not ok); s = ('PASS ' if ok else 'FAIL ') + name + (' ' + detail if detail else ''); print(s); out.append(s)
def vols(key, l0):
    spec = NETS[key]; net = Net(spec['name'], spec['G'], spec['T'], spec['motif'], spec['w'])
    cells = [Cell(net, i, (Fr(l0),), Fr(spec['D2'])) for i in range(len(net.motif))]
    det = sp.sqrt(sp.Matrix(spec['G']).det())
    return [(c.kind, sp.expand(cell_volume(c, c.faces()) * det)) for c in cells], cells
# ordinary octet: equal-volume point
V, _ = vols('delian', Fr(-1, 50)); vt = next(v for k, v in V if k == 'tet'); vo = next(v for k, v in V if k == 'oct')
r = sp.nsimplify(sp.Rational(3, 8) - sp.cbrt(4) / 4)
chk('octet walk: Samson = Delilah exactly at lam = 3/8 − ∛4/4', sp.simplify(vt.subs(LAM, r) - vo.subs(LAM, r)) == 0, f'(volume {sp.nsimplify(sp.simplify(vo.subs(LAM, r)))})')
# twinned octet
V, cells = vols('hcpholes', Fr(1, 300))
vt = next(v for k, v in V if k == 'tet'); vo = next(v for k, v in V if k == 'oct')
chk('twinned: all four tet sites have the same volume polynomial', len({sp.simplify(v) for k, v in V if k == 'tet'}) == 1)
p = sp.Poly(sp.expand((vt - vo) * 6144 / sp.sqrt(2)), LAM)
chk('twinned: Sonsam = Lahdeli where 1536λ³ + 5184λ² − 3384λ + 11 = 0', sp.simplify(p.as_expr() / 3 + (1536*LAM**3 + 5184*LAM**2 - 3384*LAM + 11)) == 0 or sp.simplify(p.as_expr() + 3*(1536*LAM**3 + 5184*LAM**2 - 3384*LAM + 11)) == 0, str(p.as_expr()))
root = [x for x in sp.Poly(1536*LAM**3 + 5184*LAM**2 - 3384*LAM + 11, LAM).nroots(n=30) if abs(sp.im(x)) < 1e-20 and -sp.Rational(1, 8) < sp.re(x) < sp.Rational(5, 24)]
chk('twinned: exactly one root inside the octet–5/24 stretch', len(root) == 1, f'λ ≈ {float(sp.re(root[0])):.12f}')
chk('twinned: the cubic has no rational root (irreducible)', sp.Poly(1536*LAM**3 + 5184*LAM**2 - 3384*LAM + 11, LAM).is_irreducible)
vs = sp.N(vo.subs(LAM, sp.re(root[0])), 30)
chk('Sonsam and Lahdeli volume = √2/6 (the average: 6 pieces share the cell volume √2)', abs(vs - sp.sqrt(2) / 6) < 1e-25, f'{float(vs):.12f}')
chk('cell volume of the twinned net = √2 (2 oct + 4 tet pieces)', sp.simplify(2 * vo + 4 * vt - sp.sqrt(2)) == 0)
for c in cells:
    if c.kind in ('oct', 'tet') and c.i in (0, 2):
        F = c.faces(); sz = sorted(len(f) for f in F.values())
        chk(f'Sonsam/Lahdeli stretch: {c.kind} piece has {len(c.corners)} corners, faces {sz}', True)
iv = [c.interval() for c in cells]; lo = max(x[0] for x in iv); hi = min(x[1] for x in iv)
chk('the stretch is exactly (−1/8, 5/24)', (lo, hi) == (Fr(-1, 8), Fr(5, 24)), f'{lo}, {hi}')
iand = sp.nsimplify(sp.simplify(vt.subs(LAM, sp.Rational(5, 24)))); rho = sp.nsimplify(sp.simplify(vo.subs(LAM, sp.Rational(5, 24))))
chk('at 5/24: Ian Dury volume', True, f'{iand} = {float(iand):.9f}')
chk('at 5/24: 60° rhombohedron of edge 1/3 has volume (1/3)³/√2', sp.simplify(rho - sp.Rational(1, 27) / sp.sqrt(2)) == 0, f'{rho}')
V2, cells2 = vols('hcpholes', Fr(3, 10))
vt2 = next(v for k, v in V2 if k == 'tet'); vo2 = next(v for k, v in V2 if k == 'oct')
iv2 = [c.interval() for c in cells2]; lo2 = max(x[0] for x in iv2 if x[0] is not None); hi2 = min(x[1] for x in iv2 if x[1] is not None)
chk('next stretch is (5/24, 3/8)', (lo2, hi2) == (Fr(5, 24), Fr(3, 8)), f'{lo2}, {hi2}')
chk('continuity at 5/24 (Ian Dury from both sides)', sp.simplify(vt2.subs(LAM, sp.Rational(5, 24)) - vt.subs(LAM, sp.Rational(5, 24))) == 0)
blk = sp.simplify(vt2.subs(LAM, sp.Rational(3, 8))); oct38 = sp.simplify(vo2.subs(LAM, sp.Rational(3, 8)))
chk('at 3/8 the oct pieces vanish', oct38 == 0)
chk('Blockhead volume = √2/4 (four per cell of volume √2)', sp.simplify(blk - sp.sqrt(2) / 4) == 0, f'{blk}')
print(f'{len(out) - fails} PASS, {fails} FAIL'); out.append(f'{len(out) - fails} PASS, {fails} FAIL')
open('checks.txt', 'w').write('\n'.join(out) + '\n')
