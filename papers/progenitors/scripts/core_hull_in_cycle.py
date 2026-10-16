# Progenitors step 7: do the O–H compound's core (rectified TI: the Dharma TI's 90 edge midpoints) and hull (its polar in the TI midsphere,
# rho² = 9/4) take stations in the golden O-Dharma cycle I ⊂ ID ⊂ O ⊂ TI ⊂ H ⊂ RT ⊂ I·φ³ (O at 3φ²/4)? Exact nesting and touching against every
# station. Also the 182 count: the compound has 102 + 80 faces and 80 + 102 corners; 90 kissing pairs leave 92 in core and hull. -> data/core-hull.txt
exec(open('scripts/o_dharma.py').read().split("out = ['DICTO")[0])
TIx = C[3][1]; e2 = min((dot([a[i] - b[i] for i in range(3)], [a[i] - b[i] for i in range(3)]) for a, b in itertools.combinations(TIx, 2)), key=lambda q: q.f())
core = [[(a[i] + b[i]) / 2 for i in range(3)] for a, b in itertools.combinations(TIx, 2) if dot([a[i] - b[i] for i in range(3)], [a[i] - b[i] for i in range(3)]) == e2]
rho2 = Q(Fr(9, 4)); hull = true_corners(polar(core)); hull = [[x * rho2 for x in v] for v in hull]
S = dict(C); S['core (rTI)'] = core; S['hull'] = hull
def rel(A, B):
    pl = planes_exact(B); m = [max((dot(n, a) - d for n, d in pl), key=lambda q: q.f()) for a in A]
    return all(not (x.f() > 0 and x != 0) for x in m), sum(1 for x in m if x == 0)
out = ['DICTO · dictospheres.com', 'Progenitors step 7: core (rectified TI) and hull of the O–H compound against the golden O-Dharma cycle (exact)',
       f'  core: {len(core)} corners; hull: {len(hull)} corners (polar of the core in rho² = 9/4)']
for nm in ('core (rTI)', 'hull'):
    for n, V in C:
        a_in, a_t = rel(S[nm], V); b_in, b_t = rel(V, S[nm])
        out.append(f'  {nm:11s} vs {n:5s}: {nm} inside {n} {a_in} ({a_t} corners on its faces); {n} inside {nm} {b_in} ({b_t} corners on its faces)')
print('\n'.join(out)); open('data/core-hull.txt', 'w').write('\n'.join(out) + '\n')
