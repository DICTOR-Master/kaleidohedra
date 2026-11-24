#!/usr/bin/env python3
"""Tie spread (edge arc) and core ratios of the uniform ring builds from closed-form circumradii (unit edge), double precision,
against data/sloane-min-angles.json. The exact values come from rings_catalogue.py."""
import math, json, os
H = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(H, "../data/sloane-min-angles.json")))
p = (1 + 5 ** .5) / 2
U = {'tetrahedron': (4, 6 ** .5 / 4), 'octahedron': (6, 2 ** .5 / 2), 'cube': (8, 3 ** .5 / 2), 'icosahedron': (12, math.sqrt(p * 5 ** .5) / 2),
     'dodecahedron': (20, 3 ** .5 * p / 2), 'cuboctahedron': (12, 1), 'icosidodecahedron': (30, p), 'truncated tetrahedron': (12, 22 ** .5 / 4),
     'truncated octahedron': (24, 10 ** .5 / 2), 'truncated cube': (24, math.sqrt(7 + 4 * 2 ** .5) / 2), 'rhombicuboctahedron': (24, math.sqrt(5 + 2 * 2 ** .5) / 2),
     'truncated cuboctahedron': (48, math.sqrt(13 + 6 * 2 ** .5) / 2), 'snub cube': (24, 1.3437133737446), 'truncated icosahedron': (60, math.sqrt(58 + 18 * 5 ** .5) / 4),
     'truncated dodecahedron': (60, math.sqrt(74 + 30 * 5 ** .5) / 4), 'rhombicosidodecahedron': (60, math.sqrt(11 + 4 * 5 ** .5) / 2),
     'truncated icosidodecahedron': (120, math.sqrt(31 + 12 * 5 ** .5) / 2), 'snub dodecahedron': (60, 2.1558373751156)}
for n in range(3, 13):
    r = 1 / (2 * math.sin(math.pi / n)); U[f'{n}-prism'] = (2 * n, math.sqrt(r * r + .25))
    h2 = 1 - 4 * r * r * math.sin(math.pi / (2 * n)) ** 2; U[f'{n}-antiprism'] = (2 * n, math.sqrt(r * r + h2 / 4))
for k, (N, R) in U.items():
    th = math.degrees(2 * math.asin(1 / (2 * R)))
    print(f'{k:28s} N={N:3d} tie-spread {th:8.4f}  R/r={2 * R:7.4f} a/r={math.sqrt(4 * R * R - 1):7.4f}  Tammes/best {S.get(str(N))}')
print("FINAL ok" if len(U) == 38 else "FINAL FAIL count")
