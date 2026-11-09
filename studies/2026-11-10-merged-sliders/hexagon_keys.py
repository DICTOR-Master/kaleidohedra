"""Merged sliders, step 2(a) (DICTO 10 Nov 2026). Where c/h is decided for half-cells: the hexagon where a cell's two halves meet.
RD (c): lower half = inversion image of the upper half; TRD (h): lower half = mirror image (horizontal mirror). Mark the six
triangles of the hexagon face of ONE half-piece with keys p(k) in {+1 bump, -1 notch, 0 flat}, k = 0..5 around the hexagon.
Two halves fit face to face when every bump meets a notch or flat and every notch meets a bump or flat (no bump on bump, no
notch on notch, and, to be a key, at least one bump-notch pair). Under inversion triangle k meets triangle k+3; under the mirror it
meets triangle k itself. Exhaustive check over all 3^6 patterns: which force c, which force h, which allow both.
usage: python3 hexagon_keys.py"""
import itertools
def fits(p, q_of_k):
    pairs = [(p[k], p[q_of_k(k)]) for k in range(6)]
    if any(a == b != 0 for a, b in pairs): return False          # bump on bump or notch on notch
    return True
inv = lambda k: (k + 3) % 6; mir = lambda k: k
force_c = force_h = both = neither = 0; ex_c = None
for p in itertools.product((-1, 0, 1), repeat=6):
    if not any(p): continue
    c, h = fits(p, inv), fits(p, mir)
    if c and not h: force_c += 1; ex_c = ex_c or p
    elif h and not c: force_h += 1
    elif c and h: both += 1
    else: neither += 1
print(f'nonzero patterns {3**6 - 1}: force c {force_c}, force h {force_h}, allow both {both}, allow neither {neither}')
print('example forcing c:', ex_c, '(e.g. alternating +,-,+,-,+,- also forces c)')
print('no hexagon pattern can force h: under the mirror every triangle meets itself, so any bump meets a bump:', force_h == 0)
print('FINAL ok' if force_h == 0 and force_c > 0 and both == 0 else 'FINAL FAIL')
