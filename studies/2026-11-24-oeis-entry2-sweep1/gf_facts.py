"""Facts for the FORMULA fields: entry 2 g.f. reduced?, recurrence start, quasi-polynomial a(8m+k); sweep 1 data line length."""
import sympy as sp
x = sp.symbols('x'); N = 1+2*x+5*x**2+4*x**3+6*x**4+6*x**5+6*x**6+4*x**7+5*x**8+2*x**9+x**10; Dn = sp.expand((1-x)**2*(1-x**8))
print('entry2 gcd(num, den) =', sp.gcd(N, Dn), '| num(1) =', N.subs(x, 1), '| den =', Dn)
a = [int(l.split()[1]) for l in open('../../papers/oeis-submissions/working/b-entry2-4H.txt')]
print('entry2 recurrence a(n)=2a(n-1)-a(n-2)+a(n-8)-2a(n-9)+a(n-10) holds for all n from', min(n for n in range(10, 201) if all(a[m] == 2*a[m-1]-a[m-2]+a[m-8]-2*a[m-9]+a[m-10] for m in range(n, 201))), 'to 200')
A, B, C = sp.symbols('A B C')
for k in range(8):
    ys = [a[8*m+k] for m in range(25)]
    s = sp.solve([A*m*m+B*m+C-ys[m] for m in (1, 2, 3)], [A, B, C])
    first = min(m0 for m0 in range(25) if all(s[A]*m*m+s[B]*m+s[C] == ys[m] for m in range(m0, 25)))
    print(f'entry2 a(8m+{k}) = {s[A]}*m^2 + {s[B]}*m + {s[C]}  (holds for m >= {first}, checked to n = 200)')
p = [int(l.split()[1]) for l in open('../../papers/oeis-submissions/working/b-sweep1-pyrochlore.txt')]
s = ','.join(map(str, p)); c = s[:261]; c = c[:c.rfind(',')]
print('sweep1 data line:', len(c), 'chars, n = 0 ..', c.count(','), ':', c)
s = ','.join(map(str, a)); c = s[:261]; c = c[:c.rfind(',')]
print('entry2 data line:', len(c), 'chars, n = 0 ..', c.count(','))
