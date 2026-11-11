# enclosures.py: independent recomputation of the enclosure analysis of Kamenetsky's Theorem A (paper §7-8: 33 enclosures, 18 dead,
# 15 live, each live one with exactly one compatible supertile (U), and the presence check (Pr): 14 cases, 0 failures), written from
# the paper's definitions with our own search (recount.py supplies the chair, poses, substitution and P*; none of his code).
#  - compatible(A, B): interior-disjoint, and if they touch, the relative pose lies in P*.
#  - enclosure of T: a pairwise compatible set of tiles covering all 24 panels of T; enumerated by covering the first uncovered panel.
#  - live: a patch whose tiles' panels can ALL be covered by further pairwise compatible tiles (second shell); depth-first search.
#  - U: supertiles containing T (T as any of the 8 children) whose children each are a patch tile or are disjoint from the patch and
#    compatible with every patch tile; must be exactly one per live enclosure.
#  - Pr: if that supertile is not already all in the patch, its central child U0 must be in the patch, and every enclosure of U0
#    compatible with the patch either contains all missing children or is dead.
import sys, time
from recount import *
t0 = time.time()
FR = {(0, 0, 0): (0, 1, 2), (0, 0, 1): (0, 2, 1), (0, 1, 0): (2, 1, 0), (0, 1, 1): (1, 2, 0), (1, 0, 0): (1, 0, 2), (1, 0, 1): (0, 1, 2), (1, 1, 0): (2, 0, 1)}
CH = children(FR); P, hist = closure(CH); assert P is not None and len(P) == 44
CUB = {}
def cb(A):
    if A not in CUB: CUB[A] = cubes(A)
    return CUB[A]
def compatible(A, B):
    a, b = cb(A), cb(B)
    if a & b: return False
    return (not touch(a, b)) or rel(A, B) in P
REL = sorted(P)
def covering(A, x):
    """tiles B in pose P* relative to A that contain cube x"""
    return [B for B in (absolute(A, p) for p in REL) if x in cb(B)]
def open_panels(A, occ):
    return [(c, d) for c in cb(A) for d in DIRS if tuple(a + b for a, b in zip(c, d)) not in occ]
def enclosures(T, fixed):
    """all pairwise compatible covers of T's open panels (given fixed tiles already placed), each found once"""
    out = []
    occ0 = set(cb(T)).union(*[cb(F) for F in fixed]) if fixed else set(cb(T))
    def bt(chosen, occ):
        pan = open_panels(T, occ)
        if not pan: out.append(tuple(chosen)); return
        c, d = pan[0]; x = tuple(a + b for a, b in zip(c, d))
        for B in covering(T, x):
            if all(compatible(B, Y) for Y in [T] + list(fixed) + chosen):
                bt(chosen + [B], occ | cb(B))
    bt([], occ0); return out
NODES = [0]; LIMIT = 200000
def live(patch):
    """can every open panel of every patch tile be covered by further pairwise compatible tiles?"""
    NODES[0] = 0
    def dfs(tiles, occ):
        NODES[0] += 1
        if NODES[0] > LIMIT: raise RuntimeError('node limit')
        best = None
        for A in patch:
            for c, d in open_panels(A, occ):
                x = tuple(a + b for a, b in zip(c, d))
                cands = [B for B in covering(A, x) if all(compatible(B, Y) for Y in tiles)]
                if not cands: return False
                if best is None or len(cands) < len(best): best = cands
                if len(best) == 1: break
            if best is not None and len(best) == 1: break
        if best is None: return True
        return any(dfs(tiles + [B], occ | cb(B)) for B in best)
    return dfs(list(patch), set().union(*[cb(A) for A in patch]))
INV = [(inv(h), tuple(-x for x in act(inv(h), tau))) for h, tau in CH]
def supertiles_containing(T):
    out = {}
    for k, (hi, ti) in enumerate(INV):
        S = absolute(T, (hi, ti)); K = kids(S, CH); out.setdefault(frozenset(K), (k, S, K))
    return list(out.values())
T = (ID, (0, 0, 0))
E = enclosures(T, [])
print(f'enclosures of a tile: {len(E)} (paper 33) ({time.time()-t0:.0f}s)', flush=True)
st = dict(live=0, dead=0, U_fail=0, typeA=0, Pr_checks=0, Pr_fail=0)
for n, enc in enumerate(E):
    patch = [T] + list(enc)
    if not live(patch): st['dead'] += 1; continue
    st['live'] += 1
    occ = set().union(*[cb(A) for A in patch]); pset = set(patch)
    comp = [(k, S, K) for k, S, K in supertiles_containing(T)
            if all(kd in pset or (not (cb(kd) & occ) and all(compatible(kd, Y) for Y in patch)) for kd in K)]
    if len(comp) != 1: st['U_fail'] += 1; continue
    k, S, K = comp[0]; missing = [kd for kd in K if kd not in pset]
    if not missing: st['typeA'] += 1; continue
    U0 = K[0]
    if U0 not in pset: st['Pr_fail'] += 1; continue
    st['Pr_checks'] += 1
    fixed = [Y for Y in patch if Y != U0]
    for EU in enclosures(U0, fixed):
        joint = list(dict.fromkeys(patch + list(EU)))
        if all(m in joint for m in missing): continue
        if live(joint): st['Pr_fail'] += 1; break
print(f'dead {st["dead"]} (paper 18), live {st["live"]} (paper 15); one compatible supertile in every live case: {st["U_fail"] == 0}; '
      f'already complete {st["typeA"]} (paper 1); presence checks {st["Pr_checks"]} (paper 14), failures {st["Pr_fail"]} (paper 0) ({time.time()-t0:.0f}s)', flush=True)
ok = len(E) == 33 and st['dead'] == 18 and st['live'] == 15 and st['U_fail'] == 0 and st['typeA'] == 1 and st['Pr_checks'] == 14 and st['Pr_fail'] == 0
print('FINAL ok: the enclosure analysis reproduced independently' if ok else 'FINAL FAIL', flush=True)
