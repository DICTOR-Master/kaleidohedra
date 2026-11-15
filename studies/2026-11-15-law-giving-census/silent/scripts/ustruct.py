#!/usr/bin/env python3
"""Orbit-space structure of the silent loci (exact, sympy): the invariant harmonics h_{k,i} as polynomials in the basic invariants
u_2..u_n on the unit sphere (u_1 = |v|^2 = 1); Groebner bases of the design systems {h_k : k <= t}; which coordinates each h involves."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sympy as sp
import sil

def sym(H, P, U, s):
    return sp.expand(sum((sp.Rational(str(c.a)) + sp.Rational(str(c.b))*s)*sp.prod([U[i]**e[i] for i in range(len(e))]) for e, c in P.items()))

def polys(name, kmax):
    H = sil.H(name); s = sp.sqrt(H.D); U = sp.symbols(f'u1:{H.n + 1}')
    out = {}
    for k in H.degrees(kmax):
        out[k] = [sym(H, h, U, s).subs(U[0], 1) for h in H.harm[k]]
    return H, U, out

if __name__ == '__main__':
    name = sys.argv[1]; kmax = int(sys.argv[2])
    H, U, P = polys(name, kmax)
    for k, ps in P.items():
        for i, p in enumerate(ps):
            pp = sp.Poly(p, *U[1:])
            print(f'h{k}.{i}: degrees in {U[1:]} = {pp.degree_list()}, terms {len(pp.terms())}')
