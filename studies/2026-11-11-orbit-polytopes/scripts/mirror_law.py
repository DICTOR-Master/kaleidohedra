"""THE MIRROR LAW (proof in the README): for a Wythoff polytope with seed x (labels lambda_i = alpha_i . x, ringed set S = support),
the central (d-1)-space of a face of type J (|J| = d-2: edges in 3D, 2-faces in 4D) is span(x, alpha_J); it is a mirror iff some root r is
orthogonal to x and to alpha_J; since every root's simple-root coefficients share one sign and r . x = sum lambda_l c_l, r . x = 0
forces r into the root subsystem of the UNRINGED nodes. CRITERION: on a mirror iff the unringed subsystem has a root orthogonal to alpha_J.
This script checks the criterion against the direct test (normal of span(x, alpha_J) compared with all mirrors) for every 0/1 seed of
A3, B3, H3, A4, B4, F4, H4 and every face type J (faces exist iff every component of J contains a ringed node)."""
import itertools, sys
import numpy as np
sys.argv = ['x', '--no-h4']
src = open('vacuus_middles.py').read().split('res = {}')[0]
exec(src)
s5 = 5 ** .5; phi = (1 + s5) / 2
A3 = [unit([1, -1, 0, 0]), unit([0, 1, -1, 0]), unit([0, 0, 1, -1])]
B3d = [unit([1, -1, 0]), unit([0, 1, -1]), unit([0, 0, 1])]
def h3_roots():
    from scipy.optimize import nnls
    V = [np.eye(3)[i] * sg for i in range(3) for sg in (1, -1)]
    for c in range(3):                                    # even (cyclic) permutations of (phi, 1, 1/phi)/2 with all signs
        for sg in itertools.product((1, -1), repeat=3):
            b = np.array([phi, 1, 1 / phi]) / 2 * np.array(sg); V.append(np.roll(b, c))
    V = np.array(V); f = np.array([1, .37, .113]); pos = [v for v in V if v @ f > 0]; P = np.array(pos); simple = []
    for i, v in enumerate(pos):
        c, r = nnls(np.delete(P, i, axis=0).T, v)
        if r > 1e-7: simple.append(unit(v))
    assert len(simple) == 3 and len(V) == 30, (len(simple), len(V))
    return simple
H3d = h3_roots()
def chain_any(R):
    d = len(R); n = len(R)
    m = lambda a, b: int(round(np.pi / (np.pi - np.arccos(np.clip(a @ b, -1, 1))))) if abs(a @ b) > 1e-9 else 2
    deg = [sum(m(R[i], R[j]) > 2 for j in range(n) if j != i) for i in range(n)]
    order = [min(range(n), key=lambda i: (deg[i], -max(m(R[i], R[j]) for j in range(n) if j != i)))]
    while len(order) < n: order.append(next(j for j in range(n) if j not in order and m(R[order[-1]], R[j]) > 2))
    return [R[i] for i in order], [m(R[order[i]], R[order[i + 1]]) for i in range(n - 1)]
def roots_of(R):
    dim = len(R[0]); gens = [np.eye(dim) - 2 * np.outer(r, r) for r in R]; out = [r for r in R]; fr = list(out)
    while fr:
        nf = []
        for v in fr:
            for g in gens:
                w = g @ v
                if min(np.linalg.norm(np.array(out) - w, axis=1)) > 1e-7: out.append(w); nf.append(w)
        fr = nf
    return np.array(out)
def basis_reduce(R):
    """express roots in their own span (A3 lives in R^4 with sum 0)"""
    M = np.array(R); U = np.linalg.svd(M)[2][:len(R)]
    return [unit(U @ r) for r in R]
groups = [('A3', basis_reduce(A3)), ('B3', B3d), ('H3', H3d), ('A4', A4), ('B4', B4), ('F4', F4), ('H4', H4)]
bad = 0; lines = 0
for name, R0 in groups:
    R, bonds = chain_any(list(R0)); n = len(R); Rm = np.array(R); ROOTS = roots_of(R)
    assert len(ROOTS) in {'A3': [12], 'B3': [18], 'H3': [30], 'A4': [20], 'B4': [32], 'F4': [48], 'H4': [120]}[name], (name, len(ROOTS))
    adj = lambda i, j: abs(R[i] @ R[j]) > 1e-9
    for lab in itertools.product((0, 1), repeat=n):
        if not any(lab): continue
        S = {i for i in range(n) if lab[i]}; x = np.linalg.solve(Rm, np.array(lab, float))
        T = [i for i in range(n) if i not in S]; RT = roots_of([R[i] for i in T]) if T else np.zeros((0, n))
        for J in itertools.combinations(range(n), n - 2):
            comps = []                                  # components of J in the Coxeter graph
            for j in J:
                hit = [c for c in comps if any(adj(j, k) for k in c)]
                new = {j}.union(*hit) if hit else {j}
                comps = [c for c in comps if c not in hit] + [new]
            if not all(c & S for c in comps): continue    # not a face of dimension n-2
            span = np.array([x] + [R[j] for j in J]); nrm = np.linalg.svd(span)[2][-1]
            direct = bool(np.abs(ROOTS @ nrm).max() > 1 - 1e-7)
            crit = bool(len(RT) and any(all(abs(r @ R[j]) < 1e-9 for j in J) for r in RT))
            bad += direct != crit; lines += 1
            if direct != crit: print('MISMATCH', name, lab, J)
    print(f'{name} chain {bonds}: all seeds and face types checked', flush=True)
print(f'{lines} (seed, face type) cases, mismatches {bad}')
print('FINAL ok' if bad == 0 else 'FINAL FAIL')
