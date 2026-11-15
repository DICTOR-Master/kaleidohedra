"""Where do the polygon counts of c and h first differ?  Classify every cycle through a site by its vertical profile.
A cycle crosses the vertical bonds of bilayer j an even number of times (they are the only bonds between sheet j and
sheet j+1); the profile is the tuple of those numbers for the bilayers it uses, relative to the root bilayer.
Also: cycles that stay in two neighbouring sheets (one bilayer's vertical bonds only) -- these see only that bilayer's
c/h letter: two sheets joined at an h bilayer are eclipsed (hexagonal prisms), at a c bilayer staggered.
Usage: diag.py L  -> per profile counts for c^inf and h^inf at both sites, and their differences, lengths 6..L.
"""
import sys, time
sys.setrecursionlimit(10000)
import rings
from collections import Counter
L = int(sys.argv[1]); T0 = time.time()
res = {}
for w in 'ch':
    net, roots, kr = rings.make_net(w, L)
    for u, r in enumerate(roots):
        cnt = Counter()
        for c in rings.cycles_through(net.nb, r, L):
            prof = Counter()
            for i in range(len(c)):
                a, b = c[i], c[(i + 1) % len(c)]
                ka, ia, ja, ua = net.coords(a); kb, ib, jb, ub = net.coords(b)
                if ka == kb: prof[ka - kr] += 1          # vertical bond of bilayer ka
            key = (len(c), tuple(sorted(prof.items())))
            cnt[key] += 1
        res[(w, u)] = cnt
        print(f'# {w} u{u} done ({time.time() - T0:.0f} s)', flush=True)
for u in (0, 1):
    keys = sorted(set(res[('c', u)]) | set(res[('h', u)]))
    print(f'PROFILE site u={u}: length, vertical bonds used per bilayer (offset: count), cycles in c^inf, in h^inf, difference h-c')
    for k in keys:
        a, b = res[('c', u)].get(k, 0), res[('h', u)].get(k, 0)
        if a != b or k[0] >= L - 2: print(f'  {k[0]:3d} {str(dict(k[1])):40s} {a:9d} {b:9d} {b - a:+d}' + ('   <-- differs' if a != b else ''))
    for l in range(6, L + 1, 2):
        print(f'  total l={l}: c {sum(v for k, v in res[("c", u)].items() if k[0] == l)} h {sum(v for k, v in res[("h", u)].items() if k[0] == l)}')
print('DIAG done', f'({time.time() - T0:.0f} s)')
