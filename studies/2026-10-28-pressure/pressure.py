# Pressure and the stacking variants (DICTO queue item 2, 10-28). At pressure P the enthalpy E + PV of a polytype adds P times its
# volume; in the ANNNI expansion (convention of Keller et al. 2023: X(2H) = 2(J1+J3), X(4H) = J1+2J2+J3, X(6H) = (2/3)(J1+2J2+3J3),
# per pair relative to 3C) the volume couplings J^V add P J^V to the energy couplings. If the volume were exactly linear in the
# hexagonality (the Hexagonality Law's form) only J1 would shift. First-order estimate: couplings at P=0, volumes at P=0.
# 1 GPa * 1 A^3 = 6.2415 meV.
import numpy as np, json
M = np.array([[2, 0, 2], [1, 2, 1], [2 / 3, 4 / 3, 2]], float); K = 6.2415
def couplings(x2H, x4H, x6H): return np.linalg.solve(M, np.array([x2H, x4H, x6H]))
vol = lambda a, cp: np.sqrt(3) / 2 * a * a * cp
SETS = {
 'SiC (GGA+vdW, Kawanishi-Mizoguchi)': dict(E=(15.0, 2.7, 1.3), V={'3C': vol(3.079, 2.514), '2H': vol(3.074, 2.529), '4H': vol(3.076, 2.521), '6H': vol(3.077, 2.519)}),
 'Si (PBEsol, Keller et al.)': dict(E=(19.4, 4.9, 2.4), V={'3C': 40.152, '2H': 40.109, '4H': 40.095, '6H': 40.106}),
 'Ge (PBEsol, Keller et al.)': dict(E=(32.0, 14.2, 9.0), V={'3C': 45.596, '2H': 45.493, '4H': 45.516, '6H': 45.535}),
}
out = {}
for name, d in SETS.items():
    JE = couplings(*d['E']); V = d['V']; JV = couplings(V['2H'] - V['3C'], V['4H'] - V['3C'], V['6H'] - V['3C'])
    # stability of 3C against 6H and 4H: 3C is the lowest while J1+2J2+3J3 > 0 (3C/6H) and J1+2J2+J3 > 0 (3C/4H); and 2H: J1+J3 > 0
    rows = {}
    for lab, c in (('3C vs 6H', [1, 2, 3]), ('3C vs 4H', [1, 2, 1]), ('3C vs 2H', [1, 0, 1])):
        e, v = np.dot(c, JE), np.dot(c, JV) * K       # meV/pair and meV/pair per GPa
        Pc = -e / v if v < 0 else float('inf')
        rows[lab] = (round(e, 3), round(v, 4), None if Pc == float('inf') else round(Pc, 1))
    lin = abs(JV[1]) + abs(JV[2]); share = abs(JV[0]) / (abs(JV[0]) + lin)
    print(f'{name}\n  energy J (meV/pair) {np.round(JE, 3)}; volume J (A^3/pair) {np.round(JV, 4)}; nearest share of volume couplings {share:.2f}')
    for lab, (e, v, Pc) in rows.items():
        print(f'    {lab}: margin {e} meV/pair at P=0, changes by {v} meV/pair per GPa' + (f' -> closes at about {Pc} GPa' if Pc else ' -> pressure favours 3C'))
    out[name] = {'JE': JE.tolist(), 'JV': JV.tolist(), 'margins': rows}
json.dump(out, open('pressure.json', 'w'), indent=1)
