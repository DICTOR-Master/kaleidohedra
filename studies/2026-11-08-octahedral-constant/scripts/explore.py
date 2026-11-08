# explore.py -- numerical pilot (float): min over unit u, w of F(u, w) = max_{g in O} (g u).w
# for the octahedral rotation group O (24 signed permutation matrices of det +1).
# Case B of the proof: a, b in the chamber T = {x1 >= x2 >= x3 >= 0}, F_B(a, b) = max over the
# 24 improper h in O_h of a.(h b). Which improper h are needed near the minimum?
import itertools, numpy as np

def group():
    P, I = [], []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product([1, -1], repeat=3):
            M = np.zeros((3, 3))
            for i, j in enumerate(perm):
                M[j, i] = sg[i]
            (P if round(np.linalg.det(M)) == 1 else I).append(M)
    return np.array(P), np.array(I)

PROP, IMPR = group()
assert len(PROP) == 24 and len(IMPR) == 24
c = 1 / np.sqrt(3)
rng = np.random.default_rng(1)

# 1. global: random u, w on the sphere
U = rng.normal(size=(400000, 3)); U /= np.linalg.norm(U, axis=1)[:, None]
W = rng.normal(size=(400000, 3)); W /= np.linalg.norm(W, axis=1)[:, None]
F = np.einsum('gij,nj,ni->ng', PROP, U, W).max(axis=1)
print('random pairs: min F =', F.min(), ' 1/sqrt3 =', c, ' margin', F.min() - c)

# 2. case B on the chamber, with local polishing
def chamber(n):
    x = np.abs(rng.normal(size=(n, 3))); x = -np.sort(-x, axis=1)
    return x / np.linalg.norm(x, axis=1)[:, None]
A, B = chamber(400000), chamber(400000)
V = np.einsum('hij,nj,ni->nh', IMPR, B, A)
FB = V.max(axis=1)
k = FB.argmin()
print('case B: min F_B =', FB[k], 'at a =', A[k], 'b =', B[k])
# which improper elements attain the max at the 2000 smallest values
idx = np.argsort(FB)[:2000]
used = set(V[idx].argmax(axis=1))
print('improper elements attaining the max near the minimum:', len(used))
for h in sorted(used):
    print('  ', IMPR[h].astype(int).tolist())
# 3. case A sanity: identity gives a.b >= 1/sqrt3 on the chamber
print('case A: min a.b on chamber pairs =', np.einsum('ni,ni->n', A, B).min())
ok = F.min() >= c - 1e-9 and FB[k] >= c - 1e-9
print('FINAL ok' if ok else 'FINAL FAIL: a sample fell below 1/sqrt3')
