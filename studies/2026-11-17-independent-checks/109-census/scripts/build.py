"""Independent census, stage A: subgroup catalogue -> orbit partitions -> candidate sets.
usage: python build.py WORLD [pilot]
Writes data/partitions-WORLD.pkl and data/masks-WORLD.pkl."""
import sys, os, time, pickle, itertools
import numpy as np
import multiprocessing as mp
Pool = mp.get_context("fork").Pool
from core import *
from engine import *
from worlds import world

name = sys.argv[1]; pilot = len(sys.argv) > 2 and sys.argv[2] == 'pilot'
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
t0 = time.time()
def log(*a):
    print(f'[{time.time()-t0:7.1f}s]', *a, flush=True)

W = world(name); G = W.G
log('world', name, 'group order', G.N, 'points', W.n, 'distinct cosines', len(W.cosv))

def part_of(gens):
    return components(W.n, [W.PU[g] for g in gens])

def work_pairs(chunk):
    out = {}
    for g, h in chunk:
        for gens in variants(G, [g, h]):
            lab = part_of(gens)
            out.setdefault(lab.tobytes(), ('pair', g, h))
    return out

def qid(i, j, b):
    if name == 'snub':
        g = W.lab2id[i, j, b]
        return int(W.G.try_id(W.G_h4.P[g][None])[0])
    return int(W.lab2id[i, j, b])

if __name__ == '__main__':
    parts = {}          # bytes(labels) -> provenance
    tw_lists = []       # list of lists of twisted classes (each class an index array)
    # ---- two-generated subgroups (includes cyclic), with rotation parts and -I
    reps, pairs = G.pair_reps()
    log('conjugacy classes', len(reps), 'pair representatives', len(pairs))
    if pilot:
        pairs = pairs[:: max(1, len(pairs) // 2000)]
    chunks = [pairs[i::96] for i in range(96)]
    with Pool(24) as pool:
        for d in pool.imap_unordered(work_pairs, chunks):
            for k, v in d.items(): parts.setdefault(k, v)
    log('partitions after two-generated', len(parts))
    # ---- reflection subgroups
    rs, R = reflection_subgroups(G)
    log('reflections', len(R), 'reflection subgroup classes', len(rs), sorted(len(s) for s in rs))
    for S in rs:
        for gens in variants(G, S):
            parts.setdefault(part_of(gens).tobytes(), ('refl', len(S)))
    log('partitions after reflection', len(parts))
    # ---- quaternion families
    qn = len(W.qU)
    # snub: its symmetry group conjugates 2I only by 2T, so subgroups are taken up to 2T-conjugacy
    conjugators = None if name != 'snub' else sorted(set(range(120)) - set(W.S.tolist()))
    subs = subgroups_of_unit_group(W.qmul, W.qconj, qn, conjugators)
    e = int(np.where(np.all(np.isclose(W.qU, [1, 0, 0, 0]), axis=1))[0][0])
    log('subgroup classes of the unit group', len(subs), [len(s) for s in subs])
    nfam = 0
    for L in subs:
        for Rr in subs:
            gens = {qid(l, r, 0) for l in L for r in Rr} - {-1}
            for gg in variants(G, sorted(gens)):
                parts.setdefault(part_of(gg).tobytes(), ('LxR', len(L), len(Rr))); nfam += 1
        gens = ({qid(l, r, 0) for l in L for r in L} | {qid(e, e, 1)}) - {-1}
        for gg in variants(G, sorted(gens)):
            parts.setdefault(part_of(gg).tobytes(), ('LxL.2', len(L)))
        # diagonal .2
        gens = ({qid(l, l, 0) for l in L} | {qid(e, e, 1)}) - {-1}
        for gg in variants(G, sorted(gens)):
            parts.setdefault(part_of(gg).tobytes(), ('diag.2', len(L)))
    log('partitions after [LxR], [LxL].2, diag.2', len(parts))
    # ---- graph (diagonal / twisted diagonal) groups for every automorphism
    naut = 0
    for L in subs:
        auts = automorphisms(L, W.qmul, W.qconj)
        naut += len(auts)
        for f in auts:
            if name == 'snub':
                H = W.G_h4
                gens = [int(W.lab2id[a, f[a], 0]) for a in L]
                lab = components(120, [H.P[g] for g in gens])
                cl = [np.where(lab == o)[0] for o in range(lab.max() + 1)]
                pos = -np.ones(120, int); pos[W.S] = np.arange(96)
                inside = [pos[c] for c in cl if (pos[c] >= 0).all()]
                if inside: tw_lists.append(('tw', len(L), inside))
                gens2 = {qid(a, f[a], 0) for a in L} - {-1}
                for gg in variants(G, sorted(gens2)):
                    parts.setdefault(part_of(gg).tobytes(), ('graph', len(L)))
                continue
            gens = sorted({qid(a, f[a], 0) for a in L} - {-1})
            lab = part_of(gens)
            if name in ('600', '24', 'snub'):
                tw_lists.append(('tw', len(L), [np.where(lab == o)[0] for o in range(lab.max() + 1)]))
            for gg in variants(G, gens):
                parts.setdefault(part_of(gg).tobytes(), ('graph', len(L)))
    log('automorphisms used', naut, 'partitions total', len(parts), 'twisted partitions', len(tw_lists))
    # ---- candidate sets: orbits, unions of two orbits, unions of twisted classes
    masks = {}
    def add(idx, tag):
        m = np.zeros(W.n, bool); m[idx] = True
        masks.setdefault(np.packbits(m).tobytes(), tag)
    npairs = 0
    for k, prov in parts.items():
        lab = np.frombuffer(k, np.int32); no = lab.max() + 1
        orbs = [np.where(lab == o)[0] for o in range(no)]
        for o in orbs: add(o, 'orbit')
        for a, b in itertools.combinations(range(no), 2):
            add(np.concatenate([orbs[a], orbs[b]]), 'union2'); npairs += 1
    log('masks from orbits + unions of two orbits', len(masks), 'raw unions', npairs)
    for tag, nL, cl in tw_lists:
        k = len(cl)
        sizes = range(1, k + 1) if k <= 9 else range(1, 4)
        for r in sizes:
            for comb in itertools.combinations(range(k), r):
                add(np.concatenate([cl[c] for c in comb]), 'twunion')
    log('masks incl. twisted unions', len(masks))
    pickle.dump({'parts': parts, 'tw': tw_lists}, open(os.path.join(DATA, f'partitions-{name}.pkl'), 'wb'))
    pickle.dump(masks, open(os.path.join(DATA, f'masks-{name}.pkl'), 'wb'))
    log('FINAL ok')
