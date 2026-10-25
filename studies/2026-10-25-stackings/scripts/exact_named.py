# #57 data: exact volumes (ℚ(√2)) of Chucky (ABAC oct, λ = −3/8) and Fang (ABAC oct, λ = 5/24), the cubic and hexagonal octahedral
# pieces at the same λ, and the exact check that each named piece is the mean of the two (half-volumes).
import sympy as sp
from fractions import Fraction as Fr
from engine import Net, Cell, LAM, cell_volume
from stackings import net_for
def vol_poly(word, i, l0):
    spec = net_for(word); net = Net(word, spec['G'], spec['T'], spec['motif'], spec['w'])
    c = Cell(net, i, (Fr(l0),), Fr(12)); det = sp.sqrt(sp.Matrix(spec['G']).det())
    return sp.expand(cell_volume(c, c.faces()) * det)
out = []
for name, lam, near in (('Chucky', Fr(-3, 8), [Fr(-1, 4), Fr(-7, 16)]), ('Fang', Fr(5, 24), [Fr(1, 10), Fr(1, 4)])):
    vals = {}
    for word, i in (('ABAC', 0), ('ABC', 0), ('AB', 0)):
        for s in near:                      # the stop value from a polynomial of an adjacent stretch (continuity)
            try:
                v = sp.nsimplify(sp.simplify(vol_poly(word, i, s).subs(LAM, sp.Rational(lam.numerator, lam.denominator)))); vals.setdefault(word, set()).add(v)
            except Exception as e: pass
    m = {w: sorted(v, key=str) for w, v in vals.items()}
    out.append(f"{name} (λ = {lam}): ABAC {m.get('ABAC')}, cubic {m.get('ABC')}, hexagonal {m.get('AB')}")
    try:
        a = list(vals['ABAC'])[0]; c = list(vals['ABC'])[0]; h = list(vals['AB'])[0]
        out.append(f"   mean check: {name} − (cubic + hexagonal)/2 = {sp.simplify(a - (c + h) / 2)}")
    except Exception as e: out.append(f"   mean check not possible: {e}")
open('../exact_named.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
