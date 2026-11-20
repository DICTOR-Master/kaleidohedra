"""Smoke test: members() and counts at known yantras of #103 Table 3."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
mp.mp.dps = 50
import yfam as Y
phi = (1 + mp.sqrt(5)) / 2
cases = [('DICTO (Theorem 15)', mp.mpf('0.6793185887067746573886503103907545526887'), None),
         ('rhombus at 2/phi^3', mp.sqrt(2 / phi**3), None), ('Kulaichev', mp.mpf('0.75043851602221402440608465705123451034'), None),
         ('stella rhombus', 1 / mp.sqrt(2), None)]
for name, u, v in cases:
    v = (2 * mp.sqrt(5) - 4) / u if name.startswith('DICTO') else u
    t0 = time.time(); ms = Y.members(u, v)
    for y in ms:
        r = Y.regions(y); m, s = Y.counts_traditional(y)
        print(name, 'u', mp.nstr(u, 12), 'v', mp.nstr(v, 12), 'S', mp.nstr(y['S'], 12), 't', mp.nstr(y['t'], 12), 'b1', mp.nstr(y['b'][1], 10),
              '(d)', mp.nstr(Y.bindu(y)[0], 5), '| odd', r['odd'], r['rings'], 'tri', r['odd_tri'], 'marma', m, 'sandhi', s, f'{time.time()-t0:.1f}s', flush=True)
    if not ms: print(name, 'NO admissible member')
