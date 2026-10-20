# DICTO 2026-10-20: number audit of the Sunstar paper against the exact logs (sunstar-exact.log, sunstar-clusters.log) and arithmetic.
#   python3 audit.py <studies/2026-10-20-sunstar>
import sys, os, re
from fractions import Fraction as F
S = sys.argv[1]; txt = re.sub(r'<[^>]+>', ' ', open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paper.src.html')).read())
LOG = open(os.path.join(S, 'sunstar-exact.log')).read() + open(os.path.join(S, 'sunstar-clusters.log')).read(); bad = 0
def chk(c, m):
    global bad; print(('PASS ' if c else 'FAIL ') + m); bad += (not c)
r5 = 5 ** .5; phi = (1 + r5) / 2
chk('FAIL' not in LOG and LOG.count('PASS') == 26 and '12 PASS' in txt and '14 PASS' in txt, f'logs: {LOG.count("PASS")} PASS, no FAIL; text says 12 + 14')
chk('Dogstar = cube - 6 roofs = 6 - 2 sqrt5' in LOG and abs((6 - 2 * r5) / 64 - (3 - r5) / 32) < 1e-15 and '(3 − √5)/32' in txt and abs(1 / 8 - 6 * (1 + r5) / 192 - (3 - r5) / 32) < 1e-15, 'Dogstar (3 - sqrt5)/32 = 1/8 - 6 roofs')
chk('phi/2 exactly' in LOG and 'φ/2' in txt, 'Dogstar phi/2 at dodecahedron edge 1')
chk('(5 + √5)/32' in txt and abs((10 + 2 * r5) / 64 - (5 + r5) / 32) < 1e-15 and '(5 + √5)/8' in txt and 'packing density of the dodecahedra (5 + sqrt5)/8' in LOG and abs((10 + 2 * r5) / 16 - (5 + r5) / 8) < 1e-15, 'dodecahedron (5 + sqrt5)/32, density (5 + sqrt5)/8')
chk('[1, 12, 24, 8]' in LOG and '[1, 12, 30, 20]' in LOG and '24 of the 30 wedges and 8 of the 20 spikes' in txt and '63 bounded cells' in txt, 'stellation: 63 cells, Dogstar 1 + 12 + 24 + 8')
chk('the 6 missing wedges lie on the cube axes' in LOG, 'missing wedges on axes, spike tips at cube corners')
chk("has exactly the cell dodecahedron's 20 corners" in LOG and '24 spike tips' in LOG and '24 of their spike tips' in txt, 'great star corners; 24 tight tips')
chk('wholly inside its own cell\'s stella octangula' in LOG, 'Dogstar inside its stella')
chk('touch on exactly one rhombus' in LOG and 'meeting on 6 / 12 / 18 whole rhombi' in LOG and '18 rhombi' in txt and '12 rhombi' in txt, 'contacts 1 rhombus; 6 / 12 / 18')
U = {'(23 − 5√5)/32': (23 - 5 * r5) / 32, '(5 + √5)/8': (5 + r5) / 8, '(33 + 5√5)/32': (33 + 5 * r5) / 32, '(43 + 7√5)/32': (43 + 7 * r5) / 32, '(9 + √5)/8': (9 + r5) / 8, '(7 − √5)/8': (7 - r5) / 8}
chk('at Sunstar-Hexa cube edge 1' in LOG and all(k in txt for k in U), 'volumes at the paper unit, all in text and in the log line')
chk(abs((9 + r5) / (7 - r5) - (17 + 4 * r5) / 11) < 1e-14 and '(17 + 4√5)/11' in txt and 'ratio (17 + 4 sqrt5)/11' in LOG, 'Sunstar-Hexa : Key = (17 + 4 sqrt5)/11')
chk(abs(1 + 24 * (1 + r5) / 192 - (9 + r5) / 8) < 1e-15 and abs(1 - 24 * (1 + r5) / 192 - (7 - r5) / 8) < 1e-15 and abs(8 * (3 - r5) / 32 + 24 * (1 + r5) / 192 - (7 - r5) / 8) < 1e-15, 'Hexa 1 + 24 roofs, Key 1 - 24 roofs = 8 Dogstars + 12 double roofs')
chk('24 whole rhombi in all' in LOG and 'two rhombi (24 in all)' in txt, 'two rhombi per neighbour, 24')
chk(abs((1 + r5) / 192 + (r5 - 1) / 192 - 2 * r5 / 192) < 1e-15 and abs((5 + r5) / 32 - 6 * (r5 - 1) / 192 - 3 / 16) < 1e-15 and abs((3 - r5) / 32 + 6 * (r5 - 1) / 192 - 1 / 16) < 1e-15, 'Jewel = dodecahedron - 6 tips (sqrt5 - 1)/192; stella = Dogstar + 6 tips')
chk('4, 12 and 25 lattices' in txt and '2, 1 and 9' in txt, 'tilings as the Jewel clusters (cited)')
print('ALL PASS' if bad == 0 else f'{bad} FAIL')
