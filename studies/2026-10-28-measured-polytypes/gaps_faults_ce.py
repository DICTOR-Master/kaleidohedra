# Three add-ons for the real-polytypes paper (DICTO 10-28: "those three and it's a wrap").
import numpy as np, json
M = np.array([[2, 0, 2], [1, 2, 1], [2 / 3, 4 / 3, 2]], float)     # X(2H), X(4H), X(6H) relative to 3C, ANNNI (Keller et al. convention)
out = {}
# 1. SiC band gaps (eV, room temperature, two decimals as summarised in the literature: 3C 2.36, 6H 3.02, 4H 3.23; 2H 3.33)
g = {'3C': 2.36, '6H': 3.02, '4H': 3.23, '2H': 3.33}
J = np.linalg.solve(M, np.array([g['2H'] - g['3C'], g['4H'] - g['3C'], g['6H'] - g['3C']]))
h = np.array([0, 1 / 3, .5, 1]); y = np.array([g['3C'], g['6H'], g['4H'], g['2H']]); c = np.polyfit(h, y, 1); r = y - np.polyval(c, h)
print(f'SiC gap: J1 {J[0]:+.3f}, J2 {J[1]:+.3f}, J3 {J[2]:+.3f} eV; J2/J1 {J[1]/J[0]:+.2f}; straight-line residuals {np.round(r, 3)} eV')
out['SiC gap'] = {'J': J.tolist(), 'residuals': r.tolist()}
# 2. Stacking-fault energies against the law's 2 : 2 : 1 (intrinsic : extrinsic : twin), Keller et al. Table II (mJ/m^2)
for k, (i, e, t) in {'Si (PBEsol)': (36.5, 21.2, 8.9), 'Si (ref. [46])': (39.3, 20.6, 8.4), 'Ge (PBEsol)': (69.4, 63.3, 30.8), 'Ge (ref. [46])': (69.7, 62.2, 30.0)}.items():
    print(f'{k:15s} fault energies ISF : ESF : TSF = {i/t:.2f} : {e/t:.2f} : 1   (nearest-layer case 2 : 2 : 1)')
    out['faults ' + k] = [i / t, e / t]
# 3. Cerium at 20 C (Wikipedia, Cerium): gamma fcc a = 5.1612 A (h = 0); beta dhcp a = 3.6811, c = 11.857 A (ABAC, h = 1/2)
Vg = 5.1612 ** 3 / 4; Vb = np.sqrt(3) / 2 * 3.6811 ** 2 * 11.857 / 4
print(f'Ce: fcc {Vg:.2f}, dhcp {Vb:.2f} A^3/atom, +{100*(Vb/Vg-1):.2f}% from h = 0 to h = 1/2 (two stackings: a line cannot be tested)')
out['Ce'] = {'fcc': Vg, 'dhcp': Vb}
json.dump(out, open('gaps_faults_ce.json', 'w'), indent=1)
