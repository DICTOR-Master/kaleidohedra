"""Helpers shared by enumerate.py and discover.py."""
import itertools
import numpy as np

def planes(S):
    out = []
    for a, b in itertools.combinations(S, 2):
        n = np.cross(a, b); n /= np.linalg.norm(n)
        if not any(abs(abs(n @ m) - 1) < 1e-9 for m in out): out.append(n)
    return out

def is_parallelohedron(S):
    if np.linalg.matrix_rank(np.array(S), 1e-9) < 3: return False
    # Venkov: every direction lies in 2 or 3 distinct planes with the others (belts of 4 or 6)
    for g in S:
        others = [h for h in S if h is not g]
        ps = []
        for h in others:
            n = np.cross(g, h); n /= np.linalg.norm(n)
            if not any(abs(abs(n @ m) - 1) < 1e-9 for m in ps): ps.append(n)
        if len(ps) not in (2, 3): return False
    return True

def canon(S):
    # Signs don't matter; canonical Gram up to permutation of |cos| with sign pattern handled by trying signs.
    n = len(S); best = None
    for perm in itertools.permutations(range(n)):
        for signs in itertools.product([1, -1], repeat=n - 1):
            sg = (1,) + signs
            G = tuple(round(sg[i] * sg[j] * float(S[perm[i]] @ S[perm[j]]), 6) for i in range(n) for j in range(i + 1, n))
            if best is None or G < best: best = G
    return best

def volume(S):
    return sum(abs(np.linalg.det(np.array(T))) for T in itertools.combinations(S, 3))

