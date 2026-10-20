# DICTO 2026-10-20 (float): symmetries of the DICTO Jewel, built as in studies/2026-10-19-og-gyrated-octet/jewel_twin.py (its corners).
# Tests centre symmetry, the 120 deg turn about (1,1,1), the half-turns/coordinate sign changes, and the mirror across the (111) layer.
#   python3 jewel_symmetry.py <studies/2026-10-19-og-gyrated-octet>
import sys, os, numpy as np
exec(open(os.path.join(sys.argv[1], 'jewel_twin.py')).read().split("V = np.array(verts)")[0])
V = np.array(verts)
same = lambda A, B: len(A) == len(B) and all(np.min(np.linalg.norm(B - a, axis=1)) < 1e-9 for a in A)
CYC = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]]); MIR = np.eye(3) - 2 / 3 * np.ones((3, 3))
print('corners', len(V), '| centre-symmetric', same(-V, V), '| 120 deg about (1,1,1)', same(V @ CYC.T, V),
      '| half-turns', all(same(V * np.array(s), V) for s in [(1, -1, -1), (-1, 1, -1), (-1, -1, 1)]),
      '| mirror across the (111) layer', same(V @ MIR.T, V), '| 60 deg turn = mirror image', same(V @ MIR.T, V @ np.array([[2, -1, 2], [2, 2, -1], [-1, 2, 2]]).T / 3))
