# ANNNI couplings for the VOLUME of Si and Ge polytypes (DICTO 10-28, "beef" for the real-polytypes paper).
# Convention of Keller et al. (arXiv 2302.10822), checked on their energies: per atom pair, relative to 3C,
#   X(2H) = 2(J1 + J3),  X(4H) = J1 + 2J2 + J3,  X(6H) = (2/3)(J1 + 2J2 + 3J3).
# With their energy J's (Si: 10.4, -2.4, -0.68 meV/pair) this gives 19.44, 4.92, 2.37 meV/pair = 9.7, 2.5, 1.2 meV/atom = their
# Table I. A property linear in the hexagonality h has X = s h, i.e. J1 = s/2, J2 = J3 = 0; so J2, J3 measure the bend.
# Stacking faults (their Eq. 1): ISF 4(J1+J2+J3), ESF 4(J1+2J2+2J3), TSF 2(J1+2J2+3J3): with J2 = J3 = 0 these are 4J1, 4J1, 2J1,
# the 2 : 2 : 1 of #67's Theorem 2 (intrinsic : extrinsic : twin).
import numpy as np, json
from fractions import Fraction as F
M = np.array([[2, 0, 2], [1, 2, 1], [2 / 3, 4 / 3, 2]], float)
check = M @ np.array([10.4, -2.4, -0.68]); print('energy check (meV/pair):', np.round(check, 2), '-> per atom', np.round(check / 2, 2), '(their Table I: 9.7, 2.5, 1.2)')
V = {'Si (PBEsol)': {'2H': 40.109, '4H': 40.095, '6H': 40.106, '3C': 40.152},
     'Si (ref. [46])': {'2H': 39.226, '4H': 39.228, '6H': 39.248, '3C': 39.283},
     'Ge (PBEsol)': {'2H': 45.493, '4H': 45.516, '6H': 45.535, '3C': 45.596}}
EJ = {'Si (PBEsol)': (10.4, -2.4, -0.68), 'Si (ref. [46])': (11.4, -2.9, -0.75), 'Ge (PBEsol)': (16.4, -1.0, -0.38)}
out = {}
for k, d in V.items():
    x = np.array([d['2H'] - d['3C'], d['4H'] - d['3C'], d['6H'] - d['3C']])
    J = np.linalg.solve(M, x)
    rv = J[1] / J[0], J[2] / J[0]; re = EJ[k][1] / EJ[k][0], EJ[k][2] / EJ[k][0]
    print(f'{k:15s} volume J1 {J[0]:+.4f}, J2 {J[1]:+.4f}, J3 {J[2]:+.4f} A^3/pair;  J2/J1 {rv[0]:+.3f}, J3/J1 {rv[1]:+.3f};  energy J2/J1 {re[0]:+.3f}, J3/J1 {re[1]:+.3f}')
    # fault volumes (per pair) from the volume J's
    J1, J2, J3 = J
    print(f'{"":15s} fault volume changes (A^3/pair): twin {2*(J1+2*J2+3*J3):+.4f}, intrinsic {4*(J1+J2+J3):+.4f}, extrinsic {4*(J1+2*J2+2*J3):+.4f}  (law: {2*J1:+.4f} : {4*J1:+.4f} : {4*J1:+.4f})')
    out[k] = {'J_volume': J.tolist(), 'J_energy': EJ[k], 'ratios_volume': rv, 'ratios_energy': re}
json.dump(out, open('annni_volume.json', 'w'), indent=1)
