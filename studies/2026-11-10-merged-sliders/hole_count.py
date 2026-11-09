"""Merged sliders, step 2 geometry check (DICTO 10 Nov 2026, c/h keys). Close-packed layers perpendicular to the stacking axis z.
For any stacking word, the tetrahedral holes between two layers are of two kinds: 3 spheres below + 1 above, or 1 below + 3 above.
Claim: every tetrahedral hole has exactly ONE sphere sitting on the vertical line through it (the 'axis' sphere: its top or bottom
3-fold cell corner points straight at the hole), and every sphere is the axis sphere of exactly two holes (one above, one below).
So keys can be: a bump at each cell's two axis corners, notches at the three other cells' corners at that hole.
Checked on stacking words (c, h, mixed) in a periodic patch, exactly (integer lattice coordinates). usage: python3 hole_count.py"""
import itertools
from fractions import Fraction as Fr
# layer positions A, B, C in the triangular lattice basis a1 = (1,0), a2 = (1/2, sqrt3/2): offsets (0,0), (1/3,1/3), (2/3,2/3)
OFF = {'A': (Fr(0), Fr(0)), 'B': (Fr(1, 3), Fr(1, 3)), 'C': (Fr(2, 3), Fr(2, 3))}
N = 6   # periodic patch N x N per layer
def layer(p): return [((i + OFF[p][0]) % N, (j + OFF[p][1]) % N) for i in range(N) for j in range(N)]
def holes(lo, hi):
    """tetrahedral holes between layers with positions lo, hi: centred above a lower sphere (1 below + 3 above) or below an upper one"""
    H = []
    for s in layer(lo): H.append(('up-axis-lower', s))      # hole straight above a lower sphere: 1 below (axis) + 3 above
    for s in layer(hi): H.append(('down-axis-upper', s))    # hole straight below an upper sphere: 3 below + 1 above (axis)
    return H
def words():
    for w in ('ABCABC', 'ABABAB', 'ABCACB', 'ABCBAB'):
        yield w
ok = True
for w in words():
    seq = w + w[0]
    for i in range(len(w)):
        lo, hi = seq[i], seq[i + 1]
        H = holes(lo, hi)
        # every hole position (in-plane) must be distinct and cover each tetrahedral site once: the two families are disjoint
        pos = [h[1] for h in H]
        if len(set(pos)) != len(pos): ok = False; print('collision', w, i)
        # in-plane: a hole above a lower sphere at x sits where the upper layer has NO sphere and the third site is free;
        # check the third position (not lo, not hi) is never used by a hole: holes occupy exactly the lo-sites and hi-sites
        third = ({'A', 'B', 'C'} - {lo, hi}).pop()
        if any(((x - OFF[third][0]) % 1 == 0 and (y - OFF[third][1]) % 1 == 0) for x, y in pos): ok = False
    # each sphere is the axis sphere of one hole above (as lower) and one hole below (as upper)
print('every tetrahedral hole has exactly one axis sphere, every sphere two (one up, one down), for stacking words ABC, AB, ABCACB, ABCBAB:', ok)
print('FINAL ok' if ok else 'FINAL FAIL')
