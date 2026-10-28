# Zircaloy step (DICTO 10-28): from hydrogen_sites.py, usable tetrahedral sites per metal atom = 2 - h (one H per face-sharing pair,
# Switendick's 2.1 A H-H limit). So a hydride MH_x with hydrogen in tetrahedral sites needs local hexagonality h <= 2 - x.
# Distances (ideal close packing, a = metal-metal distance): face-sharing tetra pair 0.408a, edge-sharing tetra pair 0.707a.
for metal, a in (('Ti', 2.95), ('Zr', 3.23)):
    print(f'{metal}: a = {a} A: face-sharing pair {0.408*a:.2f} A (forbidden), edge-sharing pair {0.707*a:.2f} A '
          f'({"allowed" if 0.707*a > 2.1 else "at the limit"})')
for name, x in (('gamma-ZrH (fct)', 1.0), ('delta-ZrH1.5', 1.5), ('delta-ZrH1.66', 1.66), ('epsilon-ZrH2 / delta-TiH2', 2.0)):
    print(f'{name:26s} x = {x:4.2f}: needs local h <= {2 - x:.2f}' + ('  (hcp itself, h = 1, allows it)' if 2 - x >= 1 else ''))
