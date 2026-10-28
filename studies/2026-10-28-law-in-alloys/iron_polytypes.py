# Fe-Mn step 2 (DICTO 10-28): six iron polytypes, non-magnetic DFT (Tsumuraya, Watanabe, Sawaguchi, arXiv 2010.07118 v4, Table I-II,
# NM rows: same method for all six). V0 Bohr^3/atom, dE meV/atom (relative to AFM-II hcp; differences only are used).
# Sequences from their Table I; their 10H "ABC-BC-B-A-CA-C" = ABCBCBACAC = the Mg LPSO 10H (types cchhh x2, h = 3/5; their
# table prints 0.3, which does not match their own hc string cchhh: a misprint).
import numpy as np
D = {'3C': ('ABC', 69.2, 106), '2H': ('AB', 68.7, 27), '4H': ('ABCB', 69.1, 82), '6H1': ('ABCACB', 69.2, 80),
     '6H2': ('ABCBCB', 69.0, 59), '10H': ('ABCBCBACAC', 69.0, 60)}
STEP = {('A','B'):1,('B','C'):1,('C','A'):1,('B','A'):-1,('C','B'):-1,('A','C'):-1}
def corr(w):                                   # per-layer <s_i s_i+n>, n = 1, 2, 3, cyclic
    n = len(w); s = [STEP[(w[i], w[(i+1) % n])] for i in range(n)]
    return [sum(s[i]*s[(i+k) % n] for i in range(n)) / n for k in (1, 2, 3)]
def hex_(w): n = len(w); return sum(w[i-1] == w[(i+1) % n] for i in range(n)) / n
rows = [(k, hex_(w), corr(w), V, E) for k, (w, V, E) in D.items()]
for k, h, c, V, E in rows: print(f'{k:4s} {D[k][0]:11s} h = {h:.3f}  <ss+n> = {np.round(c, 3)}')
for name, col in (('volume V0 (Bohr^3)', 3), ('energy (meV/atom)', 4)):
    y = np.array([r[col] for r in rows]); h = np.array([r[1] for r in rows])
    a, b = np.polyfit(h, y, 1); res = y - (a*h + b)
    print(f'\n{name}: law fit (linear in h) slope {a:.2f}, residuals', dict(zip([r[0] for r in rows], np.round(res, 2))))
    A = np.array([[1] + [-x for x in r[2]] for r in rows]); J, *_ = np.linalg.lstsq(A, y, rcond=None)
    print(f'  ANNNI to 3rd neighbour: E0 {J[0]:.2f}, J1 {J[1]:.2f}, J2 {J[2]:.2f}, J3 {J[3]:.2f}; residuals', np.round(y - A @ J, 2),
          f' |J2/J1| = {abs(J[2]/J[1]):.2f}')
