# Si and Ge polytypes (diamond framework = #60's pyrochlore run, the ice framework): is the volume per atom pair linear in h?
# Data: Keller, Belabbes, Furthmueller, Bechstedt, Botti, arXiv 2302.10822, Table I (PBEsol 'present' values, self-consistent;
# and the set of their ref. [46]). V = sqrt3 a^2 c/p per pair as listed (column 'V (A^3/atom pair)').
import numpy as np, json
H = {'2H': 1.0, '4H': 0.5, '6H': 1 / 3, '3C': 0.0}
SETS = {'Si present (PBEsol)': {'2H': 40.109, '4H': 40.095, '6H': 40.106, '3C': 40.152},
        'Si ref. [46]':        {'2H': 39.226, '4H': 39.228, '6H': 39.248, '3C': 39.283},
        'Ge present (PBEsol)': {'2H': 45.493, '4H': 45.516, '6H': 45.535, '3C': 45.596},
        'Ge ref. [46]':        {'2H': 44.440, '4H': 44.447, '6H': 44.473, '3C': 44.473 - 0.0}}
SETS.pop('Ge ref. [46]')   # its 3C row is not in the table extract; not used
out = {}
for name, d in SETS.items():
    h = np.array([H[k] for k in d]); v = np.array(list(d.values()))
    c = np.polyfit(h, v, 1); r = v - np.polyval(c, h)
    q = np.polyfit(h, v, 2)
    print(f'{name:22s} linear: V = {c[1]:.3f} {c[0]:+.3f} h, residuals {np.round(r, 3)}, max {np.abs(r).max():.3f} (rounding 0.0005); quadratic coeff {q[0]:+.3f}')
    out[name] = {'slope': c[0], 'intercept': c[1], 'residuals': r.tolist(), 'quadratic': q[0]}
json.dump(out, open('sige_linear.json', 'w'), indent=1)
