# grogan_p3.py: Grogan, "An Arithmetic Family of Aperiodic Tilings in Odd Prime Dimensions" (aiXiv 2610.01307), his child rule (eq. rule,
# §2) at p = 3, put into Kamenetsky's frame-assignment form (both use the row action (hx)_i = s_i x_{f(i)}, signs -1 on the role A, outer
# translation 4*1_A, centre translation 1): f_A(i) = mu g^{|A|} (i - z_A) over F_p, z_A = mean of A, empty role f(i) = mu i, centre
# i -> mu i. With p = 3: g = 2 (the nonsquare), mu = 1 (a square, so the centre is a plain translate).
# Checks with our own code (recount.py): (1) children partition 2C3 and are proper (his Lemma dissection); (2) |E| = |P0| equals his
# formula 2^(p+1) + (p+1)^2 - 2 = 30 (ell = ord(2) = 2); (3) is it coarsening-closed, and is it Kamenetsky's certified assignment up to a
# relabelling of the axes (his Theorem B says the closed ones are one conjugacy class)?
import itertools
from recount import *
p, g, mu = 3, 2, 1
inv_mod = lambda a: pow(a, p - 2, p)
def f_role(A):
    if not A: return tuple((mu * i) % p for i in range(p))
    z = (sum(A) * inv_mod(len(A))) % p
    return tuple((mu * pow(g, len(A), p) * (i - z)) % p for i in range(p))
FRg = {v: f_role([i for i in range(p) if v[i]]) for v in U}
print('Grogan p = 3 frames:', FRg)
CH = children(FRg); P0 = language(CH); Ps, hist = closure(CH)
print(f'partition {check_partition(CH)}; proper {all(det(h) == 1 for h, _ in CH)}; |E| = |P0| = {len(P0)} (his formula 30); closure {hist}')
FRk = {(0, 0, 0): (0, 1, 2), (0, 0, 1): (0, 2, 1), (0, 1, 0): (2, 1, 0), (0, 1, 1): (1, 2, 0), (1, 0, 0): (1, 0, 2), (1, 0, 1): (0, 1, 2), (1, 1, 0): (2, 0, 1)}
def conj(FR, s):
    """relabel axes by the permutation s: role v -> v permuted, frame f -> s f s^-1 (as index maps)"""
    si = [s.index(i) for i in range(3)]; out = {}
    for v, f in FR.items():
        v2 = tuple(v[si[i]] for i in range(3))
        out[v2] = tuple(s[f[si[i]]] for i in range(3))
    return out
same = [s for s in itertools.permutations(range(3)) if conj(FRk, s) == FRg]
print('equal to Kamenetsky\'s certified assignment after relabelling the axes by', same if same else 'NONE')
# sanity of conj: relabelled Kamenetsky assignments must also close at 44 (his Theorem B: conjugates close)
cl = [closure(children(conj(FRk, s)))[1] for s in itertools.permutations(range(3))]
print('Kamenetsky conjugates, closure histories:', cl)
