# DICTO 2026-10-20: number audit of the DICTO Jewel paper against the exact logs (jewel-exact.log, cluster-exact.log) and arithmetic.
#   python3 audit.py <studies/2026-10-20-dicto-jewel>
import sys, os, re
from fractions import Fraction as F
S = sys.argv[1]; txt = re.sub(r'<[^>]+>', ' ', open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paper.src.html')).read())
LOG = open(os.path.join(S, 'jewel-exact.log')).read() + open(os.path.join(S, 'cluster-exact.log')).read(); bad = 0
def chk(c, m):
    global bad; print(('PASS ' if c else 'FAIL ') + m); bad += (not c)
s3 = F(1, 64); r5 = 5 ** .5
chk('FAIL' not in LOG and LOG.count('PASS') == 29, f'logs: {LOG.count("PASS")} PASS, no FAIL')
chk('carved roof = roof 1/3|1/3 - roof and stella -1/3|1/3 = 2/3 exactly' in LOG and F(2, 3) * s3 == F(1, 96) and '1/96' in txt, 'carved roof 2/3 raw = 1/96')
chk(abs((1 + r5) / 3 / 64 - (1 + r5) / 192) < 1e-15 and '(1 + √5)/192' in txt and '(√5 − 1)/192' in txt, 'roof (1+sqrt5)/192, roof-and-stella (sqrt5-1)/192')
chk('10|2 = 14.472136' in LOG and abs((10 + 2 * r5) / 64 - (5 + r5) / 32) < 1e-15 and '(5 + √5)/32' in txt, 'dodecahedron (5+sqrt5)/32')
chk(12 * s3 == F(3, 16) and 4 * s3 == F(1, 16) and 8 * s3 == F(1, 8) and F(1, 8) + 6 * F(1, 96) == F(3, 16) and F(1, 16) + 6 * F(1, 96) == F(1, 8), 'Jewel 3/16 = 1/8 + 6/96; stella cell 1/16 + 6/96 = 1/8')
chk('38 corners' in LOG and '38 − 96 + 60 = 2' in txt and 'side^2 = 6|-2' in LOG and abs((r5 - 1) / 4 - 1 / (1 + r5)) < 1e-15, 'Jewel 38 corners, Euler, side (sqrt5-1)/4 = 1/(2 phi)')
chk('cos 108 = (1 - sqrt5)/4 exactly' in LOG and abs((1 - r5) / 4 - __import__('math').cos(__import__('math').radians(108))) < 1e-15, 'cos 108 = (1 - sqrt5)/4')
chk('pyritohedral' in LOG and 'no mirror across (111)' in LOG, 'symmetry')
chk('228 faces (192 triangles + 36 rhombi)' in LOG and '228 faces' in txt and '3/4' in txt, 'tetrahedral cluster 228 = 192 + 36, 3/4')
chk('288 faces (240 triangles + 48 rhombi)' in LOG and 6 * F(3, 16) == F(9, 8) and 6 * F(3, 16) + F(1, 16) == F(19, 16) and '9/8' in txt and '19/16' in txt, 'octahedral cluster 288 = 240 + 48; 9/8, 19/16')
chk('on 12 lattices of index 12' in LOG and '12 lattices of index 12' in txt, '12 lattices')
chk('18 windows, 12 along its edges and 6 along the short diagonals' in LOG and 8 * F(3, 16) + F(1, 16) == F(25, 16), 'rhombohedron 18 windows, 25/16')
chk('Jewel Cube 5/4, Jewel Cube Key 3/4' in LOG and 1 + 24 * F(1, 96) == F(5, 4) and 1 - 24 * F(1, 96) == F(3, 4) and 8 * F(1, 16) + 12 * 2 * F(1, 96) == F(3, 4), 'Cube 5/4, Key 3/4 = 8 stellas + 12 double roofs')
chk('share exactly 2 whole windows' in LOG and '24 whole windows in all' in LOG, 'two windows per neighbour, 24 in all')
chk('(2,0,0) -> (2/3,-4/3,-4/3)' in LOG and '(1/3, −2/3, −2/3)' in txt, '(111) mirror: (1,0,0) -> (1/3,-2/3,-2/3) in cell units')
L = open(os.path.join(S, 'lalvani-edges.log')).read(); chk('window edges on axes 48/48; other edges on axes 0/48' in L, 'Lalvani edges 48/48 on, 0/48 off')
print('ALL PASS' if bad == 0 else f'{bad} FAIL')
