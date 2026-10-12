# Search an exact kit complex (Chain of Karma step 1 or 2) for copies of a target region whose cut leaves only kit pieces
# (2026-10-12). Targets: phi^m * J2, phi^m * FUJI (the whole pyramid), and DICTO's rings (band minus the point-mirrored hole) for
# J2 and FUJI, in all 120 turns of the frame, with the apex (pyramids) or a floor corner (rings) on a complex vertex. A placement
# is accepted if every complex piece meeting the target meets it in a kit piece (any type, golden size; a cut icosahedron may
# give J2, J11, the antiprism, ...) and the parts add up to the target's volume. Exact geometry: the complex is snapped to the
# golden module; corners are compared to 1e-6.
import sys, os, json, itertools, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('STEP', sys.argv[1] if len(sys.argv) > 1 else '1')
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cap_cut.py')).read()
exec(src[:src.index('# the Lotus seed')])
TGT = os.environ.get('TGTS', 'J2,FUJI,ringJ2,ringFUJI').split(','); MS = [int(x) for x in os.environ.get('MS', '1,2,3').split(',')]
tree2 = cKDTree(PC)
CH = rc.planes(np.vstack(PVs))           # the complex is convex (an icosahedron): a target must lie inside it
def subtract(parts, M):
    FM = rc.planes(M); out = []
    for P_ in parts:
        cells = [P_]
        for e in FM:
            new = []
            for Q in cells:
                a = clip(Q, e[None, :]); b = clip(Q, -e[None, :])
                new += [x for x in (a, b) if x is not None and rc.vol(x) > 1e-10]
            cells = new
        out += [Q for Q in cells if not np.all(Q.mean(0) @ FM[:, :3].T + FM[:, 3] < -1e-9)]
    return out
found = []
t0 = time.time()
for tg in TGT:
    P_ = tg.replace('ring', '')
    if P_ not in ('J2', 'FUJI', 'AXE', 'CLEO'): continue
    r = rc.ring(P_); apex = r['apex']; big = np.vstack([r['floor'], apex[None]])
    for m in MS:
        s = PHI ** (m - 1)                              # target built from phi*P scaled by phi^(m-1): phi^m * P
        if tg.startswith('ring'):
            reg0 = (r['band'] - apex) * s; holes0 = [(r['hole'] - apex) * s]; anchor_idx = 0     # anchor: a floor corner
        else:
            reg0 = (big - apex) * s; holes0 = []; anchor_idx = len(big) - 1                       # anchor: the apex
        tvol = rc.vol(reg0) - sum(rc.vol(h) for h in holes0)
        seen = set(); hits = 0; tested = 0
        for g in G:
            R0 = reg0 @ g.T; H0 = [h @ g.T for h in holes0]
            key = tuple(sorted(map(tuple, np.round(R0 - R0[anchor_idx], 6))))
            if key in seen: continue
            seen.add(key)
            F0 = rc.planes(R0); rad = np.linalg.norm(R0 - R0[anchor_idx], axis=1).max()
            if H0: HLO_, HHI_ = (H0[0] @ AX.T).min(0), (H0[0] @ AX.T).max(0); HT = AX; FH0 = rc.planes(H0[0])
            for p in pts:
                t = p - R0[anchor_idx]
                if not np.all((R0 + t) @ CH[:, :3].T + CH[:, 3] <= 1e-9): continue
                F = F0.copy(); F[:, 3] = F0[:, 3] - F0[:, :3] @ t
                cen = R0.mean(0) + t
                near = tree2.query_ball_point(cen, rad + PR.max())
                if not near: continue
                near = np.array(near)
                # classify by exact separating axes: wholly inside the region, wholly outside, or straddling (clip only those)
                Wn = PV[near]; RL, RH = ((R0 + t) @ AX.T).min(0), ((R0 + t) @ AX.T).max(0)
                outside = np.any((PHI_[near] <= RL + 1e-9) | (PLO[near] >= RH - 1e-9), axis=1)
                inside = np.all(np.einsum('nvk,fk->nvf', Wn, F[:, :3]) + F[:, 3] <= 1e-9, axis=(1, 2))
                tested += 1
                parts, names, ok = [], [], True
                for i, ins, outs in zip(near, inside, outside):
                    if outs: continue
                    if ins: W = PVs[i]
                    else:
                        W = clip(PVs[i], F)
                        if W is None: continue
                    sub = [W]
                    if H0:
                        hlo, hhi = HLO_ + HT @ t, HHI_ + HT @ t; wl, wh = (W @ AX.T).min(0), (W @ AX.T).max(0)
                        if np.any((wh <= hlo + 1e-9) | (wl >= hhi - 1e-9)): sub = [W]                     # clear of the hole
                        elif np.all(W @ FH0[:, :3].T + (FH0[:, 3] - FH0[:, :3] @ t) <= 1e-9): sub = []     # inside the hole
                        else: sub = subtract([W], H0[0] + t)
                    for x in sub:
                        idn = ident(x) if not (ins and not H0) else [B[i]['r']]
                        if not idn: ok = False; break
                        parts.append((i, x)); names.append(idn[0])
                    if not ok: break
                if not ok: continue
                if abs(sum(rc.vol(x) for _, x in parts) - tvol) > 1e-7: continue          # complex does not cover the region here
                if len(parts) < 2: continue                                               # the target inside one piece: trivial
                hits += 1
                from collections import Counter
                if hits <= 3: print(f'   {tg} phi^{m}: CLEAN at turn {G.index(g) if False else "?"}, anchor {np.round(p, 4)}: {len(names)} parts {dict(Counter(names))}', flush=True)
                found.append({'target': tg, 'm': m, 'anchor': p.tolist(), 'parts': [{'is': n_, 'from': B[i]['r'], 'vertices': x.tolist()} for n_, (i, x) in zip(names, parts)]})
        print(f'{tg} at phi^{m} (volume {tvol:.6f}): {len(seen)} turns, {tested} placements inside the complex, clean {hits} ({time.time() - t0:.0f}s)', flush=True)
json.dump(found, open(os.path.join(rc.HERE, f'../data/region-search-step{os.environ["STEP"]}{os.environ.get("OUTTAG", "")}.json'), 'w'))
print('done', len(found))
