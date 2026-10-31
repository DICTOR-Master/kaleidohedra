#!/usr/bin/env python3
"""Exact check of the colour areas in the slice: per layer band and per repeat, the tetrahedral (dark) and octahedral
(light) halves have equal area, and each band has area sqrt(3)*h (so the blue share = share of h layers).
Areas in (S, Z) units (S unit sqrt(3)/6, Z unit h): one repeat x one gap = 6."""
from fractions import Fraction as F
import knit, hexknit
for name, ch, n in (('4H', 'hchc', 9), ('3C', 'c', 7), ('2H', 'h', 5), ('6H', 'hcchcc', 7), ('Fibonacci', 'chcchchcchcch', 13)):
    seq, t = hexknit.from_ch(ch, n); knit.configure(seq, t)
    hv = knit.build(0, 12)
    band = {}
    for h in hv:
        k = h['layer']; kind = 'tet' if h['kind'].startswith('tet') else 'oct'
        band.setdefault(k, {'tet': F(0), 'oct': F(0)})[kind] += knit.area2(h['poly'])
    ok = all(v['tet'] == v['oct'] == (6 if 0 < k < n - 1 else 3) for k, v in band.items())
    print(name, seq, 'every band: tet area = oct area = 1/2 band (two repeats):', ok,
          'shapes per gap per repeat checked by knit.py catalogue')
