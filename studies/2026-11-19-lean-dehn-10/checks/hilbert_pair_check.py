#!/usr/bin/env python3
"""Independent check of the pair of tetrahedra of Lean study 10 (Dehn10Hilbert.lean), from the corners alone.
Plain Python, no packages. Prints edge lengths, interior dihedral angles, volumes and altitudes."""
import math
from itertools import combinations

A, B, C = (0, 0, 0), (1, 0, 0), (0, 1, 0)
TETS = {"cornerTet (apex D = (0,0,1))": (A, B, C, (0, 0, 1)),
        "orthoTet  (apex D' = (0,1,1))": (A, B, C, (0, 1, 1))}

def sub(p, q): return tuple(x - y for x, y in zip(p, q))
def dot(p, q): return sum(x * y for x, y in zip(p, q))
def cross(p, q): return (p[1]*q[2]-p[2]*q[1], p[2]*q[0]-p[0]*q[2], p[0]*q[1]-p[1]*q[0])
def norm(p): return math.sqrt(dot(p, p))

def dihedral(P, Q, R, S):
    """interior dihedral angle at the edge PQ of the tetrahedron PQRS"""
    e = sub(Q, P)
    def perp(X):
        w = sub(X, P)
        t = dot(w, e) / dot(e, e)
        return tuple(wi - t * ei for wi, ei in zip(w, e))
    r, s = perp(R), perp(S)
    return math.acos(dot(r, s) / (norm(r) * norm(s)))

names = {math.pi/2: "pi/2", math.pi/3: "pi/3", math.pi/4: "pi/4", math.acos(1/math.sqrt(3)): "arccos(1/sqrt 3)"}
def name(x):
    for v, n in names.items():
        if abs(x - v) < 1e-12: return n
    return repr(x)

for label, T in TETS.items():
    print(label)
    for i, j in combinations(range(4), 2):
        k, l = [m for m in range(4) if m not in (i, j)]
        L2 = dot(sub(T[i], T[j]), sub(T[i], T[j]))
        print(f"  edge {i}{j}: length^2 = {L2}, angle = {name(dihedral(T[i], T[j], T[k], T[l]))}")
    vol6 = abs(dot(sub(T[1], T[0]), cross(sub(T[2], T[0]), sub(T[3], T[0]))))
    n = cross(sub(B, A), sub(C, A))
    print(f"  6 * volume = {vol6};  altitude over ABC = {abs(dot(sub(T[3], A), n)) / norm(n)}")
phi = math.acos(1/math.sqrt(3))
print("2*arccos(1/sqrt 3) - (pi - arccos(1/3)) =", 2*phi - (math.pi - math.acos(1/3)))
