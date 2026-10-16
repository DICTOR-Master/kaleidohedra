# Progenitors step 3 (option 2): can classical stations absorb the factor 3? Cycles through all of TI, H, O, PD plus any of I, ID, D, RT
# (each at most once, any order), every solid at the least size that holds the previous one; exact gain per round, kept if a power of φ.
# All solids in one frame (Dharma stations; O and PD as polars of H and TI). -> data/golden-search.txt
exec(open('scripts/pair_chain.py').read().split("s, ts = contain(H, O)")[0])
from fractions import Fraction as Fr
S = {'TI': true_corners(st['truncated icosahedron']), 'H': H, 'O': O}
S['PD'] = true_corners(polar(S['TI']))
for n, m in (('I', 'icosahedron'), ('ID', 'icosidodecahedron'), ('D', 'dodecahedron'), ('RT', 'rhombic triacontahedron')): S[n] = true_corners(st[m])
R = {}
for a in S:
    for b in S:
        if a != b: R[(a, b)] = contain(S[a], S[b])        # (least k with a ⊂ k·b, corners touching)
phi = Q(Fr(1, 2), Fr(1, 2)); PW = {}
y = Q(1)
for k in range(0, 25): PW[(y.a, y.b)] = k; y = y * phi
y = Q(1)
for k in range(1, 25): y = y / phi; PW[(y.a, y.b)] = -k
hits = []; n_cyc = 0
extras = ['I', 'ID', 'D', 'RT']
for m in range(0, 5):
    for ex in itertools.combinations(extras, m):
        for perm in itertools.permutations(['H', 'O', 'PD'] + list(ex)):
            order = ['TI'] + list(perm); n_cyc += 1; g = Q(1)
            for a, b in zip(order, order[1:] + order[:1]): g = g * R[(a, b)][0]
            k = PW.get((g.a, g.b))
            if k is not None: hits.append((len(order), k, order, g))
out = ['DICTO · dictospheres.com', f'Progenitors step 3: {n_cyc} cycles through TI, H, O, PD (+ any of I, ID, D, RT), each at least size; golden closures (gain = φ^k exactly): {len(hits)}']
for L, k, order, g in sorted(hits, key=lambda h: (h[0], h[1])):
    steps = '; '.join(f'{a}⊂{R[(a, b)][0].f():.4f}·{b} ({R[(a, b)][1]})' for a, b in zip(order, order[1:] + order[:1]))
    out.append(f'  {" ⊂ ".join(order)} ⊂ TI: gain φ^{k} = {g!r}\n      {steps}')
out.append('Pairwise least scales (a ⊂ k·b):')
for (a, b), (k, t) in sorted(R.items()): out.append(f'  {a} ⊂ {k!r} · {b}  ({k.f():.5f}; {t} touch)')
print('\n'.join(out[:40])); open('data/golden-search.txt', 'w').write('\n'.join(out) + '\n')
