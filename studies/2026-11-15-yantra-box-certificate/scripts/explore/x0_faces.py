"""Exploration: does F = (G, H1, D) vanish on the boundary of the domain 0<=u<=1, 0<=t<=u, R<=S<=1 (R = 1/(1+u^2))?"""
import json, os, sys
import cypari2
pari = cypari2.Pari(); pari.allocatemem(2*10**9)
src = sys.argv[1]
txt = open(src).read().strip().split('\n')
F = {}
for line in txt:
    k, e = line.split(' = ', 1); F[k] = pari(e.replace('**', '^'))
G, H1, D = F['G'], F['H1'], F['D']
print('degrees u,t,S:', [[pari.poldegree(f, v) for v in ('u','t','S')] for f in (G,H1,D)])
def sub(f, v, val): return pari.substpol(f, v, val) if False else pari.subst(f, v, val)
# u = 1
for name, (v, val) in {'u=1': ('u', 1), 'u=0': ('u', 0), 't=0': ('t', 0), 't=u': ('t', pari('u')), 'S=1': ('S', 1), 'S=R': ('S', pari('1/(1+u^2)'))}.items():
    g, h, d = [pari.subst(f, v, val) for f in (G, H1, D)]
    g, h, d = [pari.numerator(x) if pari.type(x) == 't_RFRAC' else x for x in (g, h, d)]
    print(name, ': G ->', str(pari.factor(g))[:200] if g != 0 else 0, '| H1 zero:', h == 0, ' D zero:', d == 0)
    # common factors
    print('   gcd(G,H1) =', str(pari.gcd(g, h))[:200], ' gcd(G,D) =', str(pari.gcd(g, d))[:200], ' gcd(H1,D) =', str(pari.gcd(h, d))[:300])
