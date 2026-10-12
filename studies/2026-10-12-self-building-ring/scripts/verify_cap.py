# Exact check of the cap rule found by cap_cut.py / region_search.py (2026-10-12):
#   J2(phi^2) = J11(1) + 5 J2(1) + 5 AXE(1) + 5 FUJI(1)            (the cap of the Lotus seed at a corner)
#   J11(phi^2) = I(phi^2) minus that cap = the rest of the Lotus seed, with the cut icosahedra giving J2 / J11
# Checks: every part convex, inside the target, congruent to its kit piece (corner count + all distances to 1e-9), no two parts
# overlap (separating axes over face normals and edge cross products), volumes add up to the target's (exact value printed).
import sys, os, json, itertools, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('STEP', '1')
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cap_cut.py')).read()
exec(src[:src.index('results = {}')])
def sep(A, B, tol=1e-9):
    HA, HB = ConvexHull(A), ConvexHull(B); ax = list(HA.equations[:, :3]) + list(HB.equations[:, :3])
    def edges(H, V):
        E = set()
        for s_ in H.simplices:
            for i, j in itertools.combinations(sorted(s_), 2): E.add((i, j))
        return [V[i] - V[j] for i, j in E]
    for u in edges(HA, A):
        for v in edges(HB, B):
            w = np.cross(u, v); nn = np.linalg.norm(w)
            if nn > 1e-9: ax.append(w / nn)
    return any((A @ a).max() <= (B @ a).min() + tol or (B @ a).max() <= (A @ a).min() + tol for a in ax)
def clean(V):
    n_, d = sig(V); V = V[ConvexHull(V).vertices]; U = []
    for v in V:
        if all(np.linalg.norm(v - u) > 1e-5 for u in U): U.append(v)
    U = np.array(U)
    try: return np.vectorize(_snapc)(U)                  # corners back on the golden module (exact)
    except ValueError: return U
out = {}
base = nbrs; cap = np.vstack([A_[None], base])           # J2(phi^2): apex A, base = the 5 neighbours (edge phi^2)
rest = np.array([v for v in C12 if np.linalg.norm(v - A_) > 1e-9])   # J11(phi^2): the Lotus seed's corners without A
opp = C12[np.argmax(np.linalg.norm(C12 - A_, axis=1))]
ap = np.array([v for v in C12 if np.linalg.norm(v - A_) > 1e-9 and np.linalg.norm(v - opp) > 1e-9])   # AP(phi^2): both caps off
# the tip rule at phi^2: the band phi^2 J2 minus the tip J2(1) at A
tip = np.vstack([A_[None], A_ + (nbrs - A_) / PHI ** 2])
for label, region in (('J2(phi^2)', cap), ('J11(phi^2)', rest), ('AP(phi^2)', ap)):
    F = rc.planes(region); parts = []
    for i, V in enumerate(PVs):
        W = clip(V, F)
        if W is None or rc.vol(W) < 1e-10: continue
        W = clean(W); idn = ident(W)
        assert idn, f'{label}: a part is not a kit piece'
        parts.append((idn[0], B[i]['r'], abs(rc.vol(W) - VOL[i]) < 1e-9, W))
    tv = rc.vol(region); pv = sum(rc.vol(W) for *_, W in parts)
    inside = all(np.all(W @ F[:, :3].T + F[:, 3] <= 1e-9) for *_, W in parts)
    over = sum(not sep(parts[a][3], parts[b][3]) for a, b in itertools.combinations(range(len(parts)), 2))
    from collections import Counter
    cnt = Counter(p[0] for p in parts)
    print(f'{label}: {len(parts)} parts {dict(cnt)}')
    print(f'   from: {dict(Counter((p[1], "whole" if p[2] else "cut") for p in parts))}')
    print(f'   volume {pv:.12f} vs target {tv:.12f} (difference {pv - tv:.1e}); all inside: {inside}; overlapping pairs: {over}')
    # exact volume: J2 = (5 + sqrt5)/24, J11 = I - J2, I = 5(3 + sqrt5)/12, AXE = 1/12, FUJI from the data
    out[label] = {'credit': 'DICTO (Chain of Karma kit); cap rule found 2026-10-12', 'target': label, 'target_corners': region.tolist(),
                  'parts': [{'is': p[0], 'from_lotus_piece': p[1], 'whole_lotus_piece': bool(p[2]), 'vertices': p[3].tolist()} for p in parts],
                  'checks': {'volume_sum': pv, 'target_volume': tv, 'all_inside': bool(inside), 'overlapping_pairs': int(over),
                             'congruence': 'each part matches its kit piece: corner count and all pairwise distances to 1e-6'}}
    json.dump(out[label], open(os.path.join(rc.HERE, f'../data/cap-rule-{label.split("(")[0]}-raw.json'), 'w'), indent=1)
    unit = json.loads(json.dumps(out[label])); unit['scale'] = 'unit: target edge 1 (raw / phi^2), apex A of the Lotus seed at the origin'
    unit['target_corners'] = ((region - A_) / PHI ** 2).tolist()
    for q in unit['parts']: q['vertices'] = ((np.array(q['vertices']) - A_) / PHI ** 2).tolist()
    json.dump(unit, open(os.path.join(rc.HERE, f'../data/cap-rule-{label.split("(")[0]}-unit.json'), 'w'), indent=1)
# tip check: the J11 in the cap contains the tip J2(1) at A; J11 - J2 = the pentagonal antiprism AP
d = json.load(open(os.path.join(rc.HERE, '../data/cap-rule-J2-raw.json')))
j11 = [np.array(q['vertices']) for q in d['parts'] if q['is'].startswith('J11')][0]
tipin = np.all(tip @ rc.planes(j11)[:, :3].T + rc.planes(j11)[:, 3] <= 1e-9)
rest_ = np.array([v for v in j11 if np.min(np.linalg.norm(tip - v, axis=1)) > 1e-9 or np.linalg.norm(v - A_) > 1e-9])
apx = np.array([v for v in j11 if np.linalg.norm(v - A_) > 1e-9])
print(f'tip J2(1) at A lies in the cap\'s J11: {tipin}; J11 minus the tip = antiprism: {bool(ident(apx)) and ident(apx)[0].startswith("AP")} ({ident(apx)})')
print(f'so  phi^2 J2 = J2 (tip) + AP + 5 J2 + 5 AXE + 5 FUJI:  {rc.vol(KIT["J2"]) + rc.vol(apx) + 5 * rc.vol(KIT["J2"]) + 5 / 12 + 5 * rc.vol(KIT["FUJI"]):.12f} = {PHI ** 6 * rc.vol(KIT["J2"]):.12f}')
J2v, Iv, AXEv, FUJIv = rc.vol(KIT['J2']), rc.vol(KIT['I']), 1 / 12, rc.vol(KIT['FUJI'])
print(f'\nvolume identity: J2(phi^2) = phi^6 J2 = {PHI ** 6 * J2v:.12f};  J11 + 5 J2 + 5 AXE + 5 FUJI = {Iv - J2v + 5 * J2v + 5 * AXEv + 5 * FUJIv:.12f}')
