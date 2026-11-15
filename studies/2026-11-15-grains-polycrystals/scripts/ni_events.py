"""Contact events between consecutive states of the public Ni HEDM grain maps (Bhattacharya et al., Science 374 (2021) 189;
data archive of G. S. Rohrer, CMU; we read the posted Dream.3D files and use Dream.3D's own neighbour lists and shared areas).
Only intervals whose states share the sample orientation (found by ni_register.py: intervals 0-1 and 4-5) are used.
Matching: a grain of state i is the grain of state i+1 within RADIUS of its shifted centroid with the smallest misorientation
(cubic symmetry), accepted below 1 degree. Interior grains only (Dream.3D SurfaceFeatures = 0 in both states).
Sets: 'deep' (all neighbours interior; biased to small grains) and 'interior'. Counts: interior grains that vanish, contacts gained / lost between matched interior grains (area thresholds 0 and AMIN um^2),
mean faces, and the steady-state identity net = f_v - <F>/2. Usage: ni_events.py DATADIR SCRIPTDIR OUT.json"""
import sys, json, h5py, numpy as np
sys.path.insert(0, sys.argv[2]); from ni_register import mats, OPS
D, OUT = sys.argv[1], sys.argv[3]; G = 'DataContainers/ImageDataContainer/CellFeatureData/'
RADIUS = 30.0; AMIN = 50.0
def feat(i):
    f = h5py.File(f'{D}/An{i}new6.dream3d', 'r')
    nn = f[G + 'NumNeighbors2'][:, 0]; nl = f[G + 'NeighborList2'][:]; sa = f[G + 'SharedSurfaceAreaList2'][:]
    off = np.concatenate([[0], np.cumsum(nn)]); assert off[-1] == len(nl)
    con = {}
    for g in range(1, len(nn)):
        for j in range(off[g], off[g + 1]):
            h = int(nl[j])
            if h > 0 and h != g: con[(min(g, h), max(g, h))] = max(con.get((min(g, h), max(g, h)), 0), float(sa[j]))
    return dict(q=f[G + 'AvgQuats'][:], c=f[G + 'Centroids'][:], d=f[G + 'EquivalentDiameters'][:, 0], surf=f[G + 'SurfaceFeatures'][:, 0],
                nn=nn, con=con, n=len(nn))
res = {}
for i, FULL in ((0, False), (4, False), (0, True), (4, True)):
    A, B = feat(i), feat(i + 1)
    Ma, Mb = mats(A['q'], False), mats(B['q'], False)
    # translation from the 300 largest grains (as in ni_register.py)
    big = np.argsort(-A['d'][1:])[:300] + 1; pairs = []
    for a in big:
        tr = np.einsum('sij,bji->bs', OPS, np.einsum('ij,bkj->bik', Ma[a], Mb[1:])).max(1)
        ang = np.degrees(np.arccos(np.clip((tr - 1) / 2, -1, 1))); b = ang.argmin() + 1
        if ang[b - 1] < 0.5: pairs.append(B['c'][b] - A['c'][a])
    shift = np.median(pairs, 0)
    match, mis = {}, []
    for a in range(1, A['n']):
        if A['d'][a] <= 0: continue
        dist = np.linalg.norm(B['c'][1:] - (A['c'][a] + shift), axis=1); cand = np.nonzero(dist < RADIUS + A['d'][a])[0] + 1
        if not len(cand): continue
        tr = np.einsum('sij,bji->bs', OPS, np.einsum('ij,bkj->bik', Ma[a], Mb[cand])).max(1)
        ang = np.degrees(np.arccos(np.clip((tr - 1) / 2, -1, 1))); k = ang.argmin()
        if ang[k] < 1.0: match[a] = int(cand[k]); mis.append(ang[k])
    inv = {}
    for a, b in match.items(): inv.setdefault(b, []).append(a)
    many = sum(len(v) > 1 for v in inv.values())
    intA = {a for a in range(1, A['n']) if A['surf'][a] == 0 and A['d'][a] > 0}
    intB = {b for b in range(1, B['n']) if B['surf'][b] == 0 and B['d'][b] > 0}
    # interior grains of A whose contacts are all with interior grains (so their whole neighbourhood is seen)
    deep = intA if FULL else {a for a in intA if all((h in intA) for (x, y) in A['con'] if a in (x, y) for h in (x, y))}
    vanished = [a for a in deep if a not in match]
    unmatchedB = [b for b in intB if b not in inv]
    r = dict(shift_um=shift.round(2).tolist(), matched=len(match), median_misorientation=float(np.median(mis)), B_grains_with_several_A=many,
             interior_A=len(intA), deep_A=len(deep), vanished_deep=len(vanished), interior_B_unmatched=len(unmatchedB),
             faces_vanished_mean=float(np.mean([A['nn'][a] for a in vanished])) if vanished else None,
             vanished_faces_hist={str(k): int(v) for k, v in zip(*np.unique([A['nn'][a] for a in vanished], return_counts=True))} if vanished else {},
             vanished_diam_over_mean=float(np.mean([A['d'][a] for a in vanished]) / np.mean([A['d'][a] for a in deep])) if vanished else None,
             meanF_deep_A=float(np.mean([A['nn'][a] for a in deep])),
             meanF_interior_B=float(np.mean([B['nn'][b] for b in intB])))
    for amin in (0.0, AMIN):
        cA = {p for p, s in A['con'].items() if s > amin}; cB = {p for p, s in B['con'].items() if s > amin}
        ok = {a for a in deep if a in match and match[a] in intB and len(inv[match[a]]) == 1}
        gained = lost = 0
        for (x, y) in cA:
            if x in ok and y in ok and tuple(sorted((match[x], match[y]))) not in cB: lost += 1
        okB = {match[a]: a for a in ok}
        for (x, y) in cB:
            if x in okB and y in okB and tuple(sorted((okB[x], okB[y]))) not in cA: gained += 1
        nv = max(1, len(vanished))
        r[f'amin{amin:g}'] = dict(tracked_grains=len(ok), gained=gained, lost=lost, gained_per_vanished=gained / nv, lost_per_vanished=lost / nv,
                                  net_per_vanished=(gained - lost) / nv,
                                  identity_fv_minus_halfF=(r['faces_vanished_mean'] - r['meanF_deep_A'] / 2) if vanished else None)
    r['set'] = 'all interior grains' if FULL else 'deep interior (all neighbours interior)'
    res[f'{i}-{i + 1} {"interior" if FULL else "deep"}'] = r
    print(i, json.dumps(r))
json.dump(res, open(OUT, 'w'), indent=1)
print('NI_OK')
