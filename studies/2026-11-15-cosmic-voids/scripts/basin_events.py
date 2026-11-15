"""Event logging and characterisation for any basin tiling saved per snapshot (voxel basins or Voronoi-tracer zones).
Follow-up to void_basins.py (grid or physics?, 15 Nov 2026). Same tracking rule (Wojtak, Powell & Abel 2016: minimum containment) and the
same shared event logger (studies/2026-11-15-event-logger/scripts/eventlog.py, unchanged).
Cache format (np.savez): lab (unit -> basin index; units are voxels or tracers, fixed identity across snapshots for tracers), mins (unit
index of each basin's minimum), vol (basin volume, (Mpc/h)^3), pairs (n,2 basin indices), area (wall area in native units), unit_area
((Mpc/h)^2 per native area unit), nb, optional fwall (mean field value on the wall).
Wall rules: ('faces', x) area >= x native units; ('phys', x) area >= x (Mpc/h)^2; ('eps', x) area >= x * Vbar^(2/3), Vbar = L^3 / nb.
Extra output per contact change (lost or gained): its group (alone / clumped with other contact changes / with a merge or split), wall
area in units of Vbar^(2/3) (lost: area before; gained: area after), the wall's mean field value, whether a cell of the pair takes part in
a merge or split in the same or an adjacent interval ("near a merge"), whether the same pair changes again in an adjacent interval
("flicker")."""
import os, sys, re
import numpy as np
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '2026-11-15-event-logger', 'scripts'))
import eventlog as EL

EPS_LIST = (0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05)


def parse(pat):
    return dict(zip(('born', 'died', 'lost', 'gained'), map(int, re.findall(r'\d+', pat))))


def threshold(rule, z, L):
    kind, x = rule; ua = float(z['unit_area']); nb = int(z['nb'])
    if kind == 'faces': return x
    if kind == 'phys': return x / ua
    if kind == 'eps': return x * (L ** 3 / nb) ** (2 / 3) / ua
    raise ValueError(rule)


def neighbour_curve(z, L):
    nb = int(z['nb']); a = z['area'] * float(z['unit_area']) / (L ** 3 / nb) ** (2 / 3)
    return [float(2 * np.count_nonzero(a >= e) / nb) for e in EPS_LIST]


def stage2x(caches, k, rule, a_of, L):
    idx = list(range(0, len(caches), k))
    if idx[-1] != len(caches) - 1: idx.append(len(caches) - 1)
    prev = None; pid_prev = None; next_pid = 0
    tot = Counter(); pats = Counter(); deg = []; nbs = []; bal_fail = 0; derived = Counter()
    recs = []                       # per contact change: (interval, pair, group, kind, area_eps, fwall)
    mergecells = []                 # per interval: set of cell labels in merge/split/birth/death events
    pairchg = []                    # per interval: set of pairs changed
    for j in idx:
        z = np.load(caches[j]); lab = z['lab'].ravel(); mins = z['mins']; vol = z['vol']; nb = int(z['nb'])
        keep = z['area'] >= threshold(rule, z, L)
        pairs = z['pairs'][keep]; area = z['area'][keep] * float(z['unit_area']) / (L ** 3 / nb) ** (2 / 3)
        fw = z['fwall'][keep] if 'fwall' in z.files else np.full(len(pairs), np.nan)
        if prev is None:
            pid = np.arange(nb); next_pid = nb; parents, heirs = {}, {}
        else:
            plab, pmins, pvol = prev
            fA = lab[pmins]; gB = plab[mins]
            pid = np.full(nb, -1, np.int64); parents, heirs = {}, {}
            cands = {}
            for A, B in enumerate(fA): cands.setdefault(int(B), []).append(A)
            for B in range(nb):
                c = cands.get(B)
                if c:
                    A = int(gB[B]) if int(gB[B]) in c else max(c, key=lambda a: pvol[a])
                    pid[B] = pid_prev[A]
                else:
                    pid[B] = next_pid; next_pid += 1
                    parents[str(pid[B])] = {str(pid_prev[int(gB[B])]): 1.0}
            kept = set(pid.tolist())
            for A in range(len(pmins)):
                if pid_prev[A] not in kept: heirs[str(pid_prev[A])] = {str(pid[fA[A]]): 1.0}
        cells = [str(x) for x in pid]
        bnd = [(str(pid[a]), str(pid[b])) for a, b in pairs]
        info = {tuple(sorted(p)): (float(ar), float(f)) for p, ar, f in zip(bnd, area, fw)}
        Tn = EL.Tiling(cells, bnd, dim=3, surface='space', t=float(a_of[j]), parents=parents)
        deg.append(2 * len(Tn.pairs) / nb); nbs.append(nb)
        if prev is not None:
            Tp.heirs = heirs
            ev = EL.classify(Tp, Tn)
            ok, _, _ = EL.balance(Tp, Tn, ev)
            if not ok: bal_fail += 1
            tot.update(Counter(e['type'] for e in ev))
            iv = len(mergecells); mc = set(); chg = set()
            lost = {p for p in Tp.pairs - Tn.pairs if p[0] in Tn.cells and p[1] in Tn.cells}
            gained = {p for p in Tn.pairs - Tp.pairs if p[0] in Tp.cells and p[1] in Tp.cells}
            for e in ev:
                P = parse(e['pattern']); cs = set(e['cells'])
                if e['type'] == 'clump': pats[e['pattern']] += 1
                ch = P['lost'] + P['gained']
                if e['type'] in ('contact gained', 'contact lost'): g = 'alone'
                elif P['born'] == 0 and P['died'] == 0: g = 'clumped'
                else: g = 'merge'; mc |= cs
                derived[{'alone': 'contact changes, alone', 'clumped': 'contact changes, clumped with other contact changes',
                         'merge': 'contact changes, with a merge/split/birth/death'}[g]] += ch
                derived['cells died (merge or death)'] += P['died']; derived['cells born (split or birth)'] += P['born']
                if g == 'clumped': derived[f'clump size {min(ch, 6)}{"+" if ch >= 6 else ""}'] += 1
                for p in lost:
                    if p[0] in cs and p[1] in cs: recs.append((iv, p, g, 'lost') + infop[p]); chg.add(p)
                for p in gained:
                    if p[0] in cs and p[1] in cs: recs.append((iv, p, g, 'gained') + info[p]); chg.add(p)
            mergecells.append(mc); pairchg.append(chg)
        prev = (lab, mins, vol); pid_prev = pid; Tp = Tn; infop = info
    # characterise
    nI = len(mergecells); grp = defaultdict(list)
    for iv, p, g, kind, ar, f in recs:
        near = any(p[0] in mergecells[t] or p[1] in mergecells[t] for t in (iv - 1, iv, iv + 1) if 0 <= t < nI)
        flick = any(p in pairchg[t] for t in (iv - 1, iv + 1) if 0 <= t < nI)
        grp[g].append((ar, f, near, flick, kind == 'lost'))
    char = {}
    for g, v in grp.items():
        a = np.array(v, float)
        char[g] = dict(n=len(v), median_area_eps=float(np.median(a[:, 0])), frac_area_below_0p01=float(np.mean(a[:, 0] < 0.01)),
                       frac_area_below_0p03=float(np.mean(a[:, 0] < 0.03)),
                       mean_wall_field=float(np.nanmean(a[:, 1])) if np.isfinite(a[:, 1]).any() else None,
                       frac_near_merge=float(np.mean(a[:, 2])), frac_flicker=float(np.mean(a[:, 3])), frac_lost=float(np.mean(a[:, 4])))
    cc = sum(derived[x] for x in ('contact changes, alone', 'contact changes, clumped with other contact changes',
                                  'contact changes, with a merge/split/birth/death'))
    died = derived['cells died (merge or death)']
    return dict(k=k, rule=list(rule), snapshots_used=len(idx), counts=dict(tot), top_clump_patterns=dict(pats.most_common(12)),
                derived=dict(derived), contact_changes_total=cc, per_basin_per_step=cc / (len(idx) - 1) / np.mean(nbs),
                fraction_alone=derived['contact changes, alone'] / cc if cc else None,
                fraction_clumped=derived['contact changes, clumped with other contact changes'] / cc if cc else None,
                contact_changes_per_merge=cc / died if died else None, balance_failures=bal_fail,
                basins_first_last=(nbs[0], nbs[-1]), mean_contacts_first_last=(deg[0], deg[-1]), mean_contacts_mean=float(np.mean(deg)),
                characterisation=char)
