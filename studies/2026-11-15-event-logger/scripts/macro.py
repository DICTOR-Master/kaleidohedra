"""Macroscopic swap count: free swaps and attached swaps (One tissue, three scales; DICTO, 15 Nov 2026). Post-processing on top of
pairing.py and eventlog.py; neither is changed. Definitions fixed BEFORE any run (README, section "Macroscopic count").

WHY. With the pairing rules (pairing.py) swap counts are still step-dependent: at a coarse step a swap that falls in the same interval
as a cell vanishing, splitting, appearing or merging is absorbed into that event (a death, merge or clump). The foam literature counts
"macroscopic" swaps instead: the side-shedding swaps of a shrinking cell are counted with its vanishing (Rutenberg & McCurdy 2005:
macroscopic T1 per T2 = 0.53; Herdtle & Aref 1992: 3/2 with side-shedding included).

DEFINITIONS (time is physical, never a frame count):
- CELL EVENT: any logger event (eventlog.classify, unchanged) in which a cell vanishes or appears: death, birth, split, merge, and any
  clump with a born or died cell. A relabel (one label replaced by another, nothing else) is not a cell event. Its time is the time of
  the later frame of its interval (as for swaps in pairing.py).
- PARTICIPANTS of a cell event: its born and died cells; for a split, merge or clump also the kept partner of each born / died cell
  (the dominant parent / heir when lineage is given, else the kept neighbour Y with N(x) - {Y} inside Y's neighbours in the other
  frame, the test eventlog uses for splits and merges, taken only when exactly ONE neighbour passes it; when several pass, as when a
  four-sided cell vanishes within one coarse interval and is read as a merge, no partner is added and the event counts as a
  vanishing of x alone). RING variant (secondary, reported beside the primary): participants plus the
  neighbours of each born cell after and each died cell before.
- SWAPS: the swaps counted by pairing.py (accepted direct swaps + paired halves) with their four cells (lost pair + gained pair) and
  their time span [t, t_gain] (one instant for a direct swap).
- A swap is ATTACHED when one of its four cells is a participant of a cell event whose time lies within tau of the swap's span
  (before or after); otherwise it is FREE. tau is fixed before counting (main: tau = 2W).
- Each attached swap is assigned to ONE event: the nearest in time among those that attach it (ties: the earlier, then the first
  logged). Per event type we report the events, the swaps attached to them, and for events with a died cell the SIDES SHED: attached
  swaps before the event whose lost pair contains the died cell.
Identity checked in every run: free + attached = swaps of pairing.py.

Use: summary = macro_census(frames, W, P, taus, tol=0, lengths=None, by_segment=False, units='') (frames: list of Tiling, or of
(Tiling, lengths) tuples).  macro_from(data, cell_events, W, P, tau) reuses one logging pass for several (W, P, tau)."""
from collections import Counter, defaultdict
import eventlog as EL
import pairing as PR


def _partners(A, B, x, born, kept, theta):
    """Kept partner(s) of a born (split) or died (merge) cell x: dominant lineage if given, else eventlog's neighbourhood test."""
    if born:
        par = EL._dominant(B.parents.get(x, {}), theta)
        if par is not None and par in kept: return {par}
        N = B.nb[x]
        c = {Y for Y in N if Y in kept and N - {Y} <= A.nb[Y]}
        return c if len(c) == 1 else set()
    heir = EL._dominant(A.heirs.get(x, {}), theta)
    if heir is not None and heir in kept: return {heir}
    N = A.nb[x]
    c = {Y for Y in N if Y in kept and N - {Y} <= B.nb[Y]}
    return c if len(c) == 1 else set()


def cell_events(frames, tol=0.0, lengths=None, by_segment=False, theta=0.9):
    """One pass: the cell events of the sequence (after rule T, as pairing.collect does). Returns (times, events) with events
    dict(type, t, i, born, died, cells (primary participants), ring (ring participants))."""
    out, times, prev = [], [], None
    for i, F in enumerate(frames):
        if isinstance(F, tuple): F, Lf = F
        else: Lf = lengths[i] if lengths is not None else None
        F, _ = PR.apply_tolerance(F, Lf, tol)
        times.append(F.t)
        if prev is not None:
            A, B = prev, F
            kept = A.cells & B.cells
            lk = {str(x): x for x in A.cells | B.cells}
            for e in EL.classify(A, B, theta, by_segment):
                if e['type'] == 'relabel': continue
                cs = [lk[c] for c in e['cells']]
                born = [c for c in cs if c in B.cells - A.cells]; died = [c for c in cs if c in A.cells - B.cells]
                if not born and not died: continue
                part = set(born) | set(died)
                if e['type'] in ('split', 'merge', 'clump'):
                    for x in born: part |= _partners(A, B, x, True, kept, theta)
                    for x in died: part |= _partners(A, B, x, False, kept, theta)
                ring = set(part)
                for x in born: ring |= B.nb[x]
                for x in died: ring |= A.nb[x]
                out.append(dict(type=e['type'], t=F.t, i=i, born=born, died=died, cells=part, ring=ring))
        prev = F
    return times, out


def classify_swaps(swaps, events, tau, key='cells'):
    """Split swaps into free and attached (see module doc). swaps: dicts with lost, gained, t, optional t_gain."""
    bycell = defaultdict(list)
    for k, e in enumerate(events):
        for c in e[key]: bycell[c].append(k)
    free, attached = [], []
    for s in swaps:
        t1 = s['t']; t2 = s.get('t_gain', t1); lo, hi = min(t1, t2), max(t1, t2)
        best = None
        for k in {k for c in set(s['lost']) | set(s['gained']) for k in bycell.get(c, ())}:
            te = events[k]['t']
            d = 0.0 if lo <= te <= hi else min(abs(te - lo), abs(te - hi))
            if d <= tau + 1e-12:
                cand = (d, te if lo <= hi else -te, k)
                if best is None or cand < best: best = cand
        if best is None: free.append(s)
        else: attached.append((s, best[2], best[0]))
    return free, attached


def per_type(events, attached, times_increasing=True):
    """Per event type: events, attached swaps, sides shed (attached swaps before a died cell's event, with that cell in the lost pair)."""
    out = defaultdict(lambda: dict(events=0, attached_swaps=0, sides_shed_before_vanishing=0, attached_before=0, attached_after=0))
    for e in events: out[e['type']]['events'] += 1
    for s, k, d in attached:
        e = events[k]; r = out[e['type']]; r['attached_swaps'] += 1
        before = (s['t'] < e['t']) if times_increasing else (s['t'] > e['t'])
        if s['t'] == e['t']: before = False
        r['attached_before' if before else 'attached_after'] += 1
        if before and set(e['died']) & set(s['lost']): r['sides_shed_before_vanishing'] += 1
    for r in out.values(): r['attached_per_event'] = round(r['attached_swaps'] / r['events'], 4) if r['events'] else None
    return dict(out)


def macro_from(data, cev, W, P, tau, units=''):
    """data = pairing.collect(...), cev = cell_events(...)[1] on the same frames. Returns summary dict."""
    swaps_ev, sm = PR.apply_rules(data, W, P, units=units, keep_events=True)
    times = data['times']; inc = len(times) < 2 or times[-1] >= times[0]
    t_first, t_last = times[0], times[-1]
    res = dict(params=dict(W=W, P=P, tau=tau, units=units, tol=data['tol'], by_segment=data['by_segment'],
                           rule='pairing.py (T, logger, P, W) -> cell events -> free / attached within tau'),
               swaps=sm['swaps'], cell_events=dict(Counter(e['type'] for e in cev)),
               vanished=sum(len(e['died']) for e in cev), appeared=sum(len(e['born']) for e in cev))
    for key in ('cells', 'ring'):
        free, att = classify_swaps(swaps_ev, cev, tau, key)
        edge = sum(1 for s in free if min(abs(s['t'] - t_first), abs(s.get('t_gain', s['t']) - t_last), abs(s['t'] - t_last),
                                          abs(s.get('t_gain', s['t']) - t_first)) < tau)
        res['primary' if key == 'cells' else 'ring'] = dict(
            free=len(free), attached=len(att), identity_ok=(len(free) + len(att) == sm['swaps']),
            free_within_tau_of_record_ends=edge, per_type=per_type(cev, att, inc))
    return res


def macro_census(frames, W, P, taus, tol=0.0, lengths=None, by_segment=False, theta=0.9, units=''):
    frames = list(frames)
    data = PR.collect(frames, tol, lengths, by_segment, theta)
    _, cev = cell_events(frames, tol, lengths, by_segment, theta)
    return {tau: macro_from(data, cev, W, P, tau, units) for tau in taus}
