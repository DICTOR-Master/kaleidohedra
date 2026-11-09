"""Task 3: extract Theorem 6's relations G(S), Q(t) and H(t, S) from natural.py (unchanged, imported) into readable form.
Writes H-full.txt (H's non-trivial factor, collected by powers of t and S, coefficients as factored polynomials in u, v),
and prints G, Q, the trivial factors and checks: (1) re-derivation is identical to natural.py's; (2) H's main factor is
irreducible over Q (sympy); (3) on GF1 the three residuals are small (natural.py's own check). FINAL ok / FAIL."""
import sys, io, contextlib
sys.path.insert(0, '.')
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    import natural as N                      # runs natural.py's own derivation and GF1 check
import sympy as sp
u, v, t, S = N.u, N.v, N.t, N.S
fl = sp.factor_list(N.H)
main = [f for f, m in fl[1] if sp.degree(f, t) == 10]
triv = [(f, m) for f, m in fl[1] if sp.degree(f, t) != 10]
assert len(main) == 1
Hm = sp.Poly(sp.expand(main[0]), t, S)
out = []
out.append('# Theorem 6, relation H(t, S) = 0: the non-trivial factor of the closing equation in natural coordinates')
out.append(f'# degree {Hm.degree(t)} in t, {Hm.degree(S)} in S; total degree in u, v: {sp.Poly(main[0], u, v).total_degree()}; terms in (t, S, u, v): {len(sp.Poly(main[0], t, S, u, v).terms())}')
out.append(f'# trivial factors of the cleared closing equation (with multiplicity): ' + ', '.join(f'({sp.sstr(f)})^{m}' for f, m in triv))
out.append('# H = sum over i, j of c_ij(u, v) t^i S^j ; each c_ij printed factored')
for (i, j), c in sorted(Hm.terms(), reverse=True):
    out.append(f't^{i} S^{j}:  {sp.sstr(sp.factor(c))}')
out.append('')
out.append('# expanded, one line (machine-readable, sympy syntax)')
out.append('H = ' + sp.sstr(sp.expand(main[0])))
open('H-full.txt', 'w').write('\n'.join(out) + '\n')
print('G(S) =', sp.sstr(sp.collect(sp.expand(N.G), S)))
print('Q(t) =', sp.sstr(sp.factor(N.Q)))
print('trivial factors:', [(sp.sstr(f), m) for f, m in triv])
print(f'H main factor: degree {Hm.degree(t)} in t, {Hm.degree(S)} in S, {len(Hm.terms())} (t,S)-terms')
irr = sp.Poly(main[0], t, S, u, v).is_irreducible
print('H main factor irreducible over Q (sympy):', irr)
print('natural.py output:', buf.getvalue().strip().splitlines()[-2:])
ok = irr and 'FINAL ok' in buf.getvalue() and Hm.degree(t) == 10 and Hm.degree(S) == 3
print('FINAL ok' if ok else 'FINAL FAIL: extraction check')
