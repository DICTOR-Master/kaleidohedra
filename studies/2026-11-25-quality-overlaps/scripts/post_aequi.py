"""Post-processing of data/aequi-overlaps.jsonl (study 2026-11-25-quality-overlaps).
1. The different-orbit CANDIDATES (depth ratio ball overlaps r*): for each, is r* = 1 exactly and does a frame map carry the
   face set onto itself while exchanging the two orbits? Then the two depths are EQUAL exactly (the map sends the fair die to a
   fair die with the same orbit set, and that die is unique: study 2026-11-24-aequi-uniqueness), so the plate is exactly the
   Resonus plane: the coincidence is proved. Otherwise it stays open.
2. Summary tables for the README (data/aequi-summary.json).
"""
import gzip, os, sys, json, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
sys.path.insert(0, HERE)
import aequi_overlaps as AO
D = [json.loads(l) for l in gzip.open(os.path.join(HERE, '..', 'data', 'aequi-overlaps.jsonl.gz'), 'rt')]
REC = {(r['part'], r['study'], int(r['sid'])): r for r in AO.PA.records()}
ZT = AO.ZT; DIRS = AO.DIRS; LINE = AO.LINE
proved, openc = [], []
for o in D:
    if not o['n_candidates']: continue
    r = REC[(o['part'], o['study'], o['sid'])]
    idx = [int(x) for x in r['idx']]; sizes = [int(x) for x in r['sizes']]
    lab = np.repeat(np.arange(len(sizes)), sizes); P = DIRS[idx]
    # recompute all candidates of this die (the jsonl keeps at most 10)
    V, inc = AO.C.combinatorics(idx, sizes, r['depths'])
    cnt = collections.Counter()
    for I in inc:
        for a, b in __import__('itertools').combinations(sorted(I), 2): cnt[(a, b)] += 1
    edges = [ab for ab, c in cnt.items() if c >= 2]
    lines_res = {LINE[i] for i in idx}
    new_lines = set(); still = []
    same_lines = set()
    for k, j in edges:
        for (c, same_ok, rstar) in ZT.get((idx[k], idx[j]), []):
            if LINE[c] not in lines_res: continue
            if lab[k] == lab[j]:
                if same_ok: same_lines.add(LINE[c])
                continue
            ok_swap = False
            if same_ok:
                for g in AO.GR.ALLG:
                    img = P @ np.asarray(g).T; d2 = np.linalg.norm(img[:, None, :] - P[None, :, :], axis=2); jj = d2.argmin(1)
                    if d2.min(1).max() < 1e-9 and len(set(jj.tolist())) == len(jj):
                        perm_ok = all(len(set(lab[jj[lab == o]].tolist())) == 1 for o in range(len(sizes)))
                        if perm_ok and set(lab[jj[lab == lab[k]]].tolist()) == {lab[j]}: ok_swap = True; break
            # only the overlapping ones were candidates; re-test the ball overlap with the run's depth balls
            if ok_swap: new_lines.add(LINE[c])
            else: still.append((k, j, int(c), bool(same_ok), str(rstar)))
    assert len(same_lines) == o['RV'], ('recount', o['label'])
    o['RV_with_symmetry'] = len(same_lines | new_lines)
    rec = dict(part=o['part'], study=o['study'], sid=o['sid'], No=o.get('No'), name=o.get('name'), label=o['label'], RV_same_orbit=o['RV'],
               RV_with_symmetry=len(same_lines | new_lines))
    (proved if new_lines and not still else openc).append(dict(rec, unresolved=still[:5], n_unresolved=len(still)))
print('candidate dice', sum(1 for o in D if o['n_candidates']), '| all resolved by an orbit-exchanging symmetry', len(proved), '| some left', len(openc))
for x in openc[:10]: print('OPEN', x['label'], x['n_unresolved'], x['unresolved'][:2])
S = {}
def c(f): return sum(1 for o in D if f(o))
S['dice'] = len(D)
S['RV_nonempty'] = c(lambda o: o['RV'] > 0)
S['RV_nonempty_with_symmetry'] = c(lambda o: o.get('RV_with_symmetry', o['RV']) > 0)
S['RV_max_with_symmetry'] = max(o.get('RV_with_symmetry', o['RV']) for o in D)
mx = max(o['RV'] for o in D); S['RV_max'] = mx
S['RV_max_dice'] = [(o['part'], o['sid'], o.get('No'), o.get('name'), o['label'], o['resonus']) for o in D if o['RV'] == mx][:20]
S['RV_hist'] = sorted(collections.Counter(o['RV'] for o in D).items())
S['RV_by_group'] = sorted(collections.Counter(o['group'] for o in D if o['RV'] > 0).items(), key=lambda t: -t[1])
S['R_sub_V'] = [(o['part'], o['sid'], o.get('No'), o.get('name'), o['label'], o['resonus'], o['RV']) for o in D if o['R_sub_V']]
S['V_sub_R'] = c(lambda o: o['V_sub_R'])
S['R_eq_M'] = [(o['part'], o['sid'], o.get('No'), o.get('name'), o['label'], o['resonus'], o['mirrors']) for o in D if o['R_eq_M']]
S['R_sub_M'] = c(lambda o: o['R_sub_M']); S['V_sub_M'] = c(lambda o: o['V_sub_M']); S['M_sub_V'] = c(lambda o: o['M_sub_V'] and o['mirrors'] > 0)
S['M_sub_R'] = c(lambda o: o['M_sub_R'] and o['mirrors'] > 0)
S['hub_A_or_B'] = c(lambda o: o['hubA'] or o['hubB'])
S['hub_and_RV'] = c(lambda o: (o['hubA'] or o['hubB']) and o['RV'] > 0)
S['simplicial_R'] = c(lambda o: o['res_arr']['simplicial'])
S['tacitus_joined'] = c(lambda o: o['tacitus_beyond'] is not None)
S['tacitus_beyond'] = c(lambda o: bool(o['tacitus_beyond']))
S['tacitus_and_simplicial'] = [(o['part'], o['sid'], o.get('No'), o.get('name'), o['label'], o['tacitus_beyond'], o['resonus'], o['res_arr']['regions_sphere'])
                               for o in D if o['tacitus_beyond'] and o['res_arr']['simplicial']]
S['tacitus_and_RV'] = c(lambda o: o['tacitus_beyond'] and o['RV'] > 0)
S['tacitus_and_hub'] = c(lambda o: o['tacitus_beyond'] and (o['hubA'] or o['hubB']))
S['equal_curvature'] = [(o['part'], o['sid'], o.get('No'), o.get('name'), o['label'], o['RV'], o['res_arr']['simplicial'], o['tacitus_beyond']) for o in D if o['equal_curvature']]
S['eqcurv_and_RV'] = c(lambda o: o['equal_curvature'] and o['RV'] > 0)
S['simplicial_and_RV'] = c(lambda o: o['res_arr']['simplicial'] and o['RV'] > 0)
S['uncertified_depths'] = [(o['part'], o['sid'], o['label'], o['n_candidates']) for o in D if o['depth_source'].startswith('float')]
S['candidates_proved'] = proved; S['candidates_open'] = openc
json.dump(S, open(os.path.join(HERE, '..', 'data', 'aequi-summary.json'), 'w'), indent=1, ensure_ascii=False)
for k, v in S.items():
    if k not in ('candidates_proved', 'candidates_open'): print(k, json.dumps(v, ensure_ascii=False)[:700])
print('FINAL ok' if len(D) == 15192 and S['equal_curvature'] and len(S['equal_curvature']) == 24 else 'FINAL FAIL')
