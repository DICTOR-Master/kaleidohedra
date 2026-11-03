# #90 link to the web of bonds (DICTO 11-04): the sections C ∩ μC* of cube × octahedron are the CsCl power cells of #53,
# the two sublattices taking μ and 3 − μ; #48's T(x) is the section at μ = 1 + x/(1 + x). Exact (sympy).
import sympy as sp
m, x, wA, wB = sp.symbols('m x w_A w_B', real=True)
p = sp.Matrix(sp.symbols('p1:4', real=True)); b = sp.Matrix([1, 1, 1]); a2 = sp.Matrix([2, 0, 0])
# A sites 2Z^3 (weight wA), B sites 2Z^3 + (1,1,1) (weight wB). Power bisectors of A at 0:
bis_AB = sp.expand((p.dot(p) - wA) - ((p - b).dot(p - b) - wB))     # = 0 on the A|B wall
bis_AA = sp.expand((p.dot(p) - wA) - ((p - a2).dot(p - a2) - wA))
print('A|B wall:', sp.solve(bis_AB, p[0])[0], ' -> x+y+z =', sp.simplify((3 + wA - wB) / 2))
print('A|A wall: x =', sp.solve(bis_AA, p[0])[0])
mA = (3 + wA - wB) / 2; mB = (3 + wB - wA) / 2
assert sp.simplify(mA + mB - 3) == 0                                    # partner section is at 3 − μ
def vol(mu):   # |C ∩ μC*|, C = [−1,1]^3, C* = {|y|_1 <= 1}, piecewise in μ
    if mu <= 1: return sp.Rational(4, 3) * mu**3
    if mu <= 2: return sp.Rational(4, 3) * mu**3 - 4 * (mu - 1)**3
    if mu <= 3: return 8 - sp.Rational(4, 3) * (3 - mu)**3                   # cube minus 8 corners of the cut cube
    return sp.Integer(8)
phi = (1 + sp.sqrt(5)) / 2
stations = {'octahedron': 1, 'Unborn Axes': 3 - phi, 'truncated octahedron': sp.Rational(3, 2), 'Icosaxes': phi, 'cuboctahedron': 2,
            'Greater Golden Cut Cube': 4 + sp.Rational(3, 2) * sp.sqrt(2) - sp.sqrt(5) - sp.sqrt(10) / 2, 'truncated cube': 1 + sp.sqrt(2),
            'Lesser Golden Cut Cube': 4 - sp.Rational(3, 2) * sp.sqrt(2) + sp.sqrt(5) - sp.sqrt(10) / 2, 'cube': 3}
for k, mu in stations.items():
    tot = sp.nsimplify(sp.simplify(vol(mu) + vol(3 - mu)))
    assert tot == 8, (k, tot)
    print(f'{k:26s} mu={sp.nsimplify(mu)}  partner 3-mu={sp.nsimplify(sp.simplify(3 - mu))}  volumes sum {tot} (one A + one B per 2x2x2 cell)')
# #48: T(x) = signed permutations of (1, s, 0), s = x/(1+x); section corners (1, μ−1, 0): μ = 1 + s
mu_of_x = 1 + x / (1 + x)
assert sp.simplify(mu_of_x.subs(x, phi) - phi) == 0                    # Icosaxes: x = τ  -> μ = φ
assert sp.simplify(mu_of_x.subs(x, 1 / phi) - (3 - phi)) == 0          # Unborn Axes: x = 1/τ -> μ = 3 − φ
assert mu_of_x.subs(x, 1) == sp.Rational(3, 2)                           # Kelvin
assert sp.simplify(mu_of_x.subs(x, 1 / x) - (3 - mu_of_x)) == 0          # T(1/x) is the partner section 3 − μ
print('T(x) = section at mu = 1 + x/(1+x); T(1/x) at 3 - mu; Icosaxes x=tau <-> mu=phi; Unborn x=1/tau <-> 3-phi; Kelvin x=1 <-> 3/2. ALL OK')
