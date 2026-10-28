# Perovskites step 1 (DICTO 10-28): BaRuO3 polytypes, volume per formula unit against the hexagonality of the BaO3 stacking.
# Cells (room temperature, ambient): 3C a = 4.0059 A (Jin et al., PNAS 105, 7115 (2008), Table 1); 4H a = 5.729, c = 9.500 A, Z = 4
# and 9R a = 5.755, c = 21.621 A, Z = 9 (as quoted in arXiv 2107.07165 from refs 10-12 there); 6H a ~ 5.71, c ~ 14 A, Z = 6 (Longo
# et al. 1968, quoted second-hand in a Cornell thin-film paper; two-figure c, flagged). Interfaces (Jin et al.): 9R CFFCFFCFF,
# 4H CFCF, 6H FCCFCC, 3C CCC -> share of face-sharing (F) = h = 2/3, 1/2, 1/3, 0 (#71 Theorem (ii)).
import numpy as np
P = {'3C': (0, 4.0059**3, 'precise'), '6H': (1/3, 3**.5/2*5.71**2*14.0/6, 'approximate (c ~ 14 A)'),
     '4H': (1/2, 3**.5/2*5.729**2*9.500/4, 'precise'), '9R': (2/3, 3**.5/2*5.755**2*21.621/9, 'precise')}
for k, (h, V, q) in P.items(): print(f'{k}: h = {h:.3f}  V = {V:.2f} A^3 per BaRuO3  ({q})')
h3 = [P[k][0] for k in ('3C', '4H', '9R')]; v3 = [P[k][1] for k in ('3C', '4H', '9R')]
s, b = np.polyfit(h3, v3, 1)
print(f'\nlaw line through the three precise phases: V = {b:.2f} + {s:.2f} h  (A^3)')
for k, (h, V, q) in P.items(): print(f'  {k}: line {b + s*h:.2f}, measured {V:.2f}, off {100*(V - b - s*h)/V:+.2f}%')
print('\nface-sharing clusters (runs of h layers + 1): 3C none; 6H dimers + single octahedra; 4H dimers; 9R trimers; 2H endless chains.'
      '\nPair count = h is linear; the cluster sizes are not (they depend on runs, i.e. farther neighbours).')
print(f'\npressure: if V is a straight line in h with slope {s:.1f} A^3 > 0, then P*V favours lower h at first order (#70 Proposition):'
      '\nthe observed synthesis sequence 9R (ambient) -> 4H (3 GPa) -> 6H (5 GPa) -> 3C (18 GPa) (Jin et al.) runs down h step by step.')
