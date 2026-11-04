#!/usr/bin/env python3
"""Calibrations for methods.py — every method must reproduce known answers before a study may use it. Run: python3 test_methods.py"""
import os, sys, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import methods as M
L = M.Ledger(); phi = M.PHI
# harmonic fingerprint, 3D: classical Steinhardt–Nelson–Ronchetti values
CO = M.perms((1, 1, 0)); ICO = M.cyclic([0, 1, phi])
J27 = [(math.cos(k*math.pi/3), math.sin(k*math.pi/3), 0) for k in range(6)]
for k in range(3):
    a = math.pi/6 + k*2*math.pi/3; e = math.atan(math.sqrt(2)); J27 += [(math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), s*math.sin(e)) for s in (1, -1)]
BCC = np.vstack([M.perms((1, 1, 1))/math.sqrt(3), M.perms((1, 0, 0))*2/math.sqrt(3)])
L.check('Q4, Q6 of the fcc shell = 0.191, 0.575', abs(M.Q3d(CO, 4) - .1909) < 1e-3 and abs(M.Q3d(CO, 6) - .5745) < 1e-3)
L.check('Q4, Q6 of the hcp shell = 0.097, 0.485', abs(M.Q3d(J27, 4) - .0972) < 1e-3 and abs(M.Q3d(J27, 6) - .4848) < 1e-3)
L.check('Q4, Q6 of the bcc shell = 0.036, 0.511', abs(M.Q3d(BCC, 4) - .0364) < 1e-3 and abs(M.Q3d(BCC, 6) - .5107) < 1e-3)
L.check('icosahedron: Q4 = 0, Q6 = 0.663', M.Q3d(ICO, 4) < 1e-9 and abs(M.Q3d(ICO, 6) - .6633) < 1e-3)
L.check('#94: Q4 of the sweep vanishes at Icosaxes (mu = phi)', M.Q3d(M.sweep_cube_octa(phi), 4) < 1e-9)
L.check('W6 of icosahedron and dodecahedron: -0.1698 and +0.1698', abs(M.W6(ICO) + .1698) < 1e-3 and abs(M.W6(np.vstack([M.perms((1, 1, 1)), M.cyclic([0, 1/phi, phi])])) - .1698) < 1e-3)
# harmonic fingerprint, 4D: spherical designs
tess = np.array(list(itertools.product((1, -1), repeat=4)), float)
c600 = np.unique(np.round(np.vstack([tess/2, M.perms((1, 0, 0, 0)), M.even_perms((phi/2, .5, 1/(2*phi), 0))]), 12), axis=0)
L.check('600-cell has 120 corners and is silent in degrees 2..11, sounds at 12', len(c600) == 120 and max(M.Q4d(c600, l) for l in range(2, 12)) < 1e-4 and M.Q4d(c600, 12) > .2)
L.check('tesseract silent at 2, 3; sounds at 4', M.Q4d(tess, 2) < 1e-4 and M.Q4d(tess, 3) < 1e-4 and M.Q4d(tess, 4) > .1)
# overlap test
cube = M.perms((.5, .5, .5), True)
L.check('unit cubes: touching faces do not overlap; shifted by half overlap 0.5', M.overlap(cube, cube + [1, 0, 0]) == 0.0 and abs(M.overlap(cube, cube + [.5, 0, 0]) - .5) < 1e-9)
# forced-sector candidates: the cube's centre pyramid round its lateral edge closes the cube (3 pieces at 120 deg)
C6 = np.array([np.zeros(3), (.5, .5, .5), (.5, -.5, .5), (.5, -.5, -.5), (.5, .5, -.5)])
cs = M.sector_candidates(C6, 0, 1, 2*math.pi/3)
cube_pyr = []
for f in range(3):
    for s in (1, -1):
        n = np.zeros(3); n[f] = s
        base = [v for v in M.perms((.5, .5, .5)) if abs(v @ n - .5) < 1e-9]
        cube_pyr.append(np.array([np.zeros(3), *base]))
L.check('sector candidates round a C6 lateral edge include two pyramids of the same cube', all(any(any(M.same_piece(c, q) for q in cube_pyr) for c in sec) for sec in cs))
# sweep sections
L.check('sweep: mu = 2 gives the cuboctahedron, mu = 1 the octahedron', len(M.sweep_cube_octa(2.0)) == 12 and len(M.sweep_cube_octa(1.0)) == 6)
sys.exit(0 if L.summary() else 1)
