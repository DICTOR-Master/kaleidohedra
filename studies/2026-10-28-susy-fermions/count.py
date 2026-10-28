# Supersymmetric lattice fermions (Fendley, Schoutens, de Boer 2003) and close-packed stackings (DICTO idea 10-28).
# A periodic stacking of N layers <-> its cyclic type string (h = 'fermion' on the site, c = empty). The FSdB chain allows any
# string with no two adjacent fermions (hard cores). A type string is a real periodic stacking when it CLOSES: the step signs close
# (even number of h) and the positions close (sum of steps = 0 mod 3). Compare, for each N and fermion number f: hard-core strings
# (FSdB states), and those that are periodic stackings.
from itertools import product
from collections import Counter
def closes(t):
    n = len(t); s = [1]
    for k in range(1, n): s.append(s[-1] if t[k] == 'c' else -s[-1])
    sign_ok = (s[-1] == s[0]) == (t[0] == 'c')        # layer 0 sits between step n-1 and step 0
    return sign_ok and sum(s) % 3 == 0
out = {}
for N in range(2, 16):
    hc, st = Counter(), Counter()
    for t in product('ch', repeat=N):
        if any(t[k] == 'h' and t[(k + 1) % N] == 'h' for k in range(N)): continue
        f = t.count('h'); hc[f] += 1
        if closes(t): st[f] += 1
    W = sum((-1) ** f * c for f, c in hc.items())
    print(f'N={N:2d}  hard-core states by f: {dict(sorted(hc.items()))} (total {sum(hc.values())}, Witten index {W});  of these periodic stackings: {dict(sorted(st.items()))}; FSdB ground f = {(N + 1) // 3}')
    out[N] = {'hardcore': dict(hc), 'stackings': dict(st), 'witten': W}
import json; json.dump(out, open('counts.json', 'w'), indent=1)
