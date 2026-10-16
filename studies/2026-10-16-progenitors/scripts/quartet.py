# Progenitors step 2 (DICTO: "maybe the truncated icosahedron has a place"): the quartet TI, H (Hecatodihedron), O (Ogdoecontahedron), PD, with
# TI ⊂ H and O ⊂ PD as given and TI ↔ PD, H ↔ O dual. For every cyclic order of the four, each solid scaled to the least size that holds the
# previous one (exact in Q(sqrt5)): the gain per round, whether it is a power of φ, and which corners touch. -> data/quartet.txt
exec(open('scripts/pair_chain.py').read().split("s, ts = contain(H, O)")[0])
TI = true_corners(st['truncated icosahedron']); PDv = true_corners(polar(TI))
S = {'TI': TI, 'H': H, 'O': O, 'PD': PDv}
P3 = Q(2, 1)
def phipow(x):                      # k if x = φ^k exactly (|k| <= 12), else None
    y = Q(1); phi = Q(Fr(1, 2), Fr(1, 2))
    for k in range(0, 13):
        if y == x: return k
        y = y * phi
    y = Q(1)
    for k in range(1, 13):
        y = y / phi
        if y == x: return -k
    return None
from fractions import Fraction as Fr
out = ['DICTO · dictospheres.com', 'Progenitors step 2: the quartet TI, H, O, PD in every cyclic order, each scaled to the least size holding the previous (exact)']
for perm in itertools.permutations(['H', 'O', 'PD']):
    order = ['TI'] + list(perm); g = Q(1); steps = []
    for a, b in zip(order, order[1:] + order[:1]):
        k, tch = contain(S[a], S[b]); steps.append(f'{a} ⊂ {k.f():.4f}·{b} ({tch} touch)'); g = g * k
    kp = phipow(g)
    out.append(f'  {" ⊂ ".join(order)} ⊂ TI: gain {g!r} = {g.f():.6f}' + (f' = φ^{kp}' if kp is not None else ' (not a power of φ)'))
    out.append('      ' + '; '.join(steps))
print('\n'.join(out)); open('data/quartet.txt', 'w').write('\n'.join(out) + '\n')
