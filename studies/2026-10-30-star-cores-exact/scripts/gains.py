# Study 1 gains: minimal polynomial of each exact radius gain and the factored field norm (for study 5, the primes). Usage: gains.py <study1.json>
import json, sys, sympy as sp
x = sp.Symbol('x'); s5 = sp.sqrt(5)
for r in json.load(open(sys.argv[1])):
    sq = 'gain_radius' not in r or r['gain_radius'] is None; g = sp.sympify(r['gain_radius_squared'] if sq else r['gain_radius'])
    mp = sp.minimal_polynomial(g, x); N = sp.Poly(mp, x).all_coeffs()
    norm = sp.Rational(N[-1], N[0]) * (-1) ** (len(N) - 1)
    print(f"{r['solid'][:26]:26} {'r^2' if sq else 'r  '} {str(g)[:50]:50} minpoly {mp}  norm {norm} = {sp.factorrat(norm)}")
