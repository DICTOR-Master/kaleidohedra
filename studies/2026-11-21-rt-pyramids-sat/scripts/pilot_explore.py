"""pilot: check templates (vertex counts, volumes, dihedrals) and list the small period lattices for RT (N = 30 det / vol(RT) integer)"""
import itertools, math, sys, json, collections
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0]); from geom import *
for kind in ['C6', 'RD', 'TET', 'GR', 'RT']:
    E, T = kind_data(kind); P = [Piece(t, E, kind != 'TET') for t in T]
    print(kind, 'templates', len(T), 'vertices', P[0].m, 'faces', len(P[0].N), 'edges', len(P[0].edges), 'vol %.6f' % P[0].volf,
          'all vols equal', np.allclose([p.volf for p in P], P[0].volf))
E = ico_basis(); Ef = zf(E)
dets = collections.Counter()
for a, b, c in itertools.combinations(range(6), 3): d = zdet3(E[a], E[b], E[c]); dets[tuple(np.abs(d)) if zsign(d) > 0 else tuple(-d)] += 1
print('|det(e_a,e_b,e_c)| as (a,b) = a + b phi:', dict(dets))
