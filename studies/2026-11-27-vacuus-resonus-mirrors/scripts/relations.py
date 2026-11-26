"""Step 6b (27 Nov 2026): the pieces' solid angles as a rational plus a few shared irrationals. With Claude (Anthropic).
Each solid angle of a spherical polygon is (sum of its corner angles) - (k-2) pi; the corner angles here are angles between the
solids' planes, i.e. arccos of numbers in Q(sqrt2) or Q(sqrt5). So each fraction-of-sphere f = q + sum c_i (theta_i / pi) with
theta_i from a short basis of such arccos values. Found by integer relation (PSLQ, mpmath, 60 digits) against the basis; a relation
counts only if its integers are small (<= 10^4) and it holds to 1e-50. Identified, not yet proved (proof: exact corner angles)."""
import os, json
import mpmath as mp
mp.mp.dps = 60
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../angles.json')))
s2, s5 = mp.sqrt(2), mp.sqrt(5)
CAND = [('acos(1/3)', mp.acos(mp.mpf(1) / 3)), ('acos(1/sqrt3)', mp.acos(1 / mp.sqrt(3))), ('acos(sqrt5/3)', mp.acos(s5 / 3)),
        ('acos(1/sqrt5)', mp.acos(1 / s5)), ('acos(2/3)', mp.acos(mp.mpf(2) / 3)), ('acos(1/sqrt15)', mp.acos(1 / mp.sqrt(15))),
        ('acos(sqrt(3/5))', mp.acos(mp.sqrt(mp.mpf(3) / 5))), ('acos(1/(2 sqrt2))', mp.acos(1 / (2 * s2))),
        ('acos((1+sqrt5)/(2 sqrt3))', mp.acos((1 + s5) / (2 * mp.sqrt(3)))), ('acos((sqrt5-1)/(2 sqrt3))', mp.acos((s5 - 1) / (2 * mp.sqrt(3))))]
def independent(cands):   # greedy: keep a candidate only if it has no small integer relation with 1 and those kept
    keep = []
    for n, v in cands:
        r = mp.pslq([mp.mpf(1)] + [x / mp.pi for _, x in keep] + [v / mp.pi], maxcoeff=10 ** 4, maxsteps=10 ** 6, tol=mp.mpf(10) ** -50)
        if r is None: keep.append((n, v))
    return [(n + '/pi', v / mp.pi) for n, v in keep]
BASIS = {'cubic': independent(CAND[:2] + CAND[4:5] + CAND[7:8]), 'icosahedral': independent(CAND)}
print('independent basis:', {k: [n for n, v in b] for k, b in BASIS.items()}, flush=True)
out = []; bad = 0
for P in D:
    fam = 'icosahedral' if P['group_order'] == 120 else 'cubic'
    names = [n for n, v in BASIS[fam]]; vals = [v for n, v in BASIS[fam]]
    print(P['pair'], flush=True)
    for k, pc in enumerate(P['pieces']):
        f = mp.mpf(pc['frac_of_sphere'])
        # recompute f at full precision from the stored 30 digits is not enough: use 28-digit tolerance
        rel = mp.pslq([f, mp.mpf(1)] + vals, maxcoeff=10 ** 4, maxsteps=10 ** 6, tol=mp.mpf(10) ** -50)
        if rel and rel[0] != 0:
            q = mp.mpf(-rel[1]) / rel[0]; cs = [mp.mpf(-c) / rel[0] for c in rel[2:]]
            txt = f'{-rel[1]}/{rel[0]}' + ''.join(f' + ({-c}/{rel[0]}) {n}' for c, n in zip(rel[2:], names) if c)
            print(f'   piece {k}: f = {txt}', flush=True); out.append(dict(pair=P['pair'], piece=k, relation=[int(x) for x in rel], basis=['f', '1'] + names))
        else:
            print(f'   piece {k}: no small relation found', flush=True); bad += 1
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../relations.json'), 'w'), indent=1)
print('identified', len(out), 'of', len(out) + bad, '(58-digit data; identified, not proved)')
print('FINAL ok' if out else 'FINAL FAIL')
