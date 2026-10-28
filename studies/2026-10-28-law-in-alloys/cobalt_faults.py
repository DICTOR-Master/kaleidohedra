# Cobalt step (DICTO 10-28). Four fault energies of hcp cobalt (Aas, Szunyogh, Evans, Chantrell, arXiv 1304.1353, LSDA SKKR-ASA,
# per fault, error ~0.1-0.2 meV): I1 16, I2 48, E 62, T2 39 meV (40, 122, 160, 100 mJ/m^2). Sequences as given there.
# (1) Law test: under the law (two-layer roles) a fault's energy = (number of layers it turns cubic) x one constant.
# (2) ANNNI fit, same convention as #68: E/layer = -sum_n J_n <s_i s_i+n>, s = +1 for steps A->B->C->A, -1 the other way.
import numpy as np
SEQ = {'I1': 'BABABCBCB', 'I2': 'ABAB|CACA', 'E': 'ABABCABAB', 'T2': 'ABABCBABA'}
EV = {'I1': 16, 'I2': 48, 'E': 62, 'T2': 39}
def ext(core, pad=40):
    s = core.replace('|', '')
    for _ in range(pad): s = s[1] + s                # prepend: keeps ...ABAB pattern (x y x y)
    for _ in range(pad): s = s + s[-2]
    return s
STEP = {('A','B'):1,('B','C'):1,('C','A'):1,('B','A'):-1,('C','B'):-1,('A','C'):-1}
def counts(s):
    st = [STEP[(s[i], s[i+1])] for i in range(len(s)-1)]
    c = [sum(st[i]*st[i+n] for i in range(len(st)-n)) for n in (1, 2, 3)]
    nc = sum(1 for i in range(1, len(s)-1) if s[i-1] != s[i+1])
    return np.array(c), nc
rows = []
for k, core in SEQ.items():
    s = ext(core)
    ref = ''.join('AB'[i % 2] for i in range(len(s)))
    (cf, ncf), (cr, ncr) = counts(s), counts(ref)
    dc = cf - cr; ncub = ncf - ncr
    rows.append((k, dc, ncub)); print(f'{k}: {s[38:51]}  cubic layers made {ncub}  change in <s s+n> sums (n=1,2,3) {dc}')
print('\nLaw test (energy per cubic layer, should be one constant):')
for k, dc, n in rows: print(f'  {k}: {EV[k]} meV / {n} = {EV[k]/n:.1f} meV')
A = np.array([-dc for _, dc, _ in rows], float); b = np.array([EV[k] for k, _, _ in rows], float)
J, res, *_ = np.linalg.lstsq(A, b, rcond=None)
print('\nANNNI fit (meV): J1 = %.2f, J2 = %.2f, J3 = %.2f' % tuple(J))
for (k, _, _), p in zip(rows, A @ J): print(f'  {k}: computed {EV[k]} meV, fit {p:.1f} meV')
print('X(fcc) - X(hcp) per layer = -2(J1+J3) = %.1f meV ; J2/J1 = %.2f' % (-2*(J[0]+J[2]), J[1]/J[0]))
