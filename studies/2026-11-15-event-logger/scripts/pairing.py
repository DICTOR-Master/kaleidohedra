"""Pairing and persistence rules for swaps (2-2 neighbour exchanges), shared by every stream of "One tissue, three scales"
(DICTO, 15 Nov 2026). Post-processing on top of eventlog.py: eventlog's own behaviour and output are unchanged; this module runs
the same classify() step by step and then applies three rules whose parameters are fixed BEFORE counting and logged in the output.

THE PROBLEM. A swap is often logged in two halves: the old contact (a, b) is lost in one frame and the new contact (c, d) is gained in
a later frame (or earlier), with a four-fold meeting in between. And jittery boundaries make contacts flicker on and off. Raw swap
counts then scale with the frame rate; only net counts are stable unless a persistence / pairing rule is fixed in advance
(studies/2026-11-15-tissue-null-models).

DEFINITIONS. Time is physical (the frames' "t"; elapsed time = |t_j - t_i|), never a frame count, so the rules mean the same at every
sampling step. A contact's value at a frame is 1 if the two cells touch, 0 if not (by_segment: the number of boundaries they share).
An ELEMENTARY CHANGE is a change of one contact between two cells present in both frames that the logger attributes to a swap (its two
contacts) or to a single-contact clump (pattern "lost 1" or "gained 1", the halves). Changes inside other events (births, deaths,
splits, merges, other clumps) are left exactly as the logger gives them.

RULE T (tolerance, tol >= 0, in the frames' length unit; needs per-frame boundary lengths): before logging, a contact whose total
boundary length is below tol is removed from the frame. When it is a single boundary with exactly two junctions {a,b,c}, {a,b,d}, the
two junctions are merged into one four-fold junction {a,b,c,d} (V and E both fall by one, so Euler is unchanged); otherwise the
frame's junction list is dropped (Euler is then not checked there; the number of such frames is reported). tol = 0: off.

RULE P (persistence, P >= 0): a contact change at time t to the new value v is ACCEPTED only if the contact keeps the value v until
at least t + P, that is, its next raw change comes at a time >= t + P, or never (a change that reaches the end of the record without
reverting is accepted and counted as censored when the record ends before t + P). A change back to the last accepted value is no
change. An elementary change that is not accepted is a FLICKER and is cancelled: a back-and-forth within P (lost then regained, or
gained then lost again) cancels both halves, and a swap followed within P by its reverse cancels both swaps. A logged swap counts
only if BOTH its contacts change are accepted: its new contact survives >= P and its old contact stays lost >= P. A swap with only
one accepted change leaves that change as a half.
RULE W (pairing, W >= 0): the accepted halves that remain are paired. A lost contact (a, b) at time t_l and a gained contact (c, d) at
time t_g form ONE swap when (i) a, b, c, d are four distinct cells, (ii) c and d were both neighbours of a and of b in the last frame
before the loss (the 2-2 pattern), and (iii) |t_g - t_l| <= W. The gain may come before or after the loss. Losses are taken in time
order; each takes the admissible gain nearest in time (ties: the earlier gain); each half is used at most once. Unpaired halves stay
single-contact events.
Order: T on frames -> log -> P on the elementary changes -> W on the accepted halves. Swaps counted = accepted logged swaps + paired
halves. With P = 0 and W = 0 the swap count equals the logger's (plus halves paired at the same instant, which the logger already
joins when all four cells touch).

Use: rows, summary = pair_census(frames, W, P, tol=0, lengths=None, by_segment=False); summary['params'] records W, P, tol, units.
frames may be any iterable (streamed: two frames in memory at a time, plus sparse per-contact change lists)."""
import json
from collections import Counter, defaultdict
import eventlog as EL

ONE_LOST, ONE_GAINED = 'born 0 died 0 lost 1 gained 0', 'born 0 died 0 lost 0 gained 1'


def read_frames_with_lengths(path):
    """Frames plus per-frame boundary lengths {(a, b): [lengths]} (from an optional "lengths" field {"a|b": [..]})."""
    out = []
    with open(path) as f:
        for line in f:
            if not line.strip(): continue
            d = json.loads(line)
            L = {tuple(sorted(p.split('|'))): (v if isinstance(v, list) else [v]) for p, v in d.get('lengths', {}).items()}
            out.append((EL.Tiling.from_json(line), L))
    return out


def apply_tolerance(T, lengths, tol):
    """RULE T. Returns (new Tiling, junctions_dropped: bool)."""
    if not tol or lengths is None: return T, False
    short = {p for p in T.pairs if sum(lengths.get(p, lengths.get(p[::-1], [float('inf')]))) < tol}
    if not short: return T, False
    segs = [s for s in T.segments if s not in short]
    J, dropped = (None if T.junctions is None else list(T.junctions)), False
    if J is not None:
        for a, b in short:
            ends = [j for j in J if a in j and b in j]
            if T.segments.count((a, b)) == 1 and len(ends) == 2:
                J = [j for j in J if j not in ends] + [tuple(sorted(set(ends[0]) | set(ends[1])))]
            else:
                J, dropped = None, True; break
    return EL.Tiling(T.cells, segs, J, T.dim, T.surface, T.t, T.edges, T.corners, T.loops, T.parents, T.heirs,
                     T.components), dropped


def _values(T, by_segment):
    return Counter(T.segments) if by_segment else Counter({p: 1 for p in T.pairs})


def pair_census(frames, W, P, tol=0.0, lengths=None, by_segment=False, theta=0.9, units='', keep_events=False):
    """Apply rules T, P, W (see module doc) to a frame sequence. lengths: list (one dict per frame) or None; or frames may yield
    (Tiling, lengths) tuples. Returns (events, summary)."""
    return apply_rules(collect(frames, tol, lengths, by_segment, theta), W, P, units, keep_events)


def collect(frames, tol=0.0, lengths=None, by_segment=False, theta=0.9):
    """One pass over the frames (the costly part): rule T, the logger, the sparse contact timelines and the elementary changes.
    The result can be given to apply_rules() with several (W, P) without logging again."""
    times, raw = [], Counter()
    changes = defaultdict(list)              # contact -> [(frame index, old value, new value)] (all contacts: sparse timeline)
    elem = []                                # elementary changes: dict(kind, pair, i, old, new, swap_id, nbr)
    n_swaps_raw, n_jdrop, prev, prevV = 0, 0, None, None
    other_counts = Counter()
    for i, F in enumerate(frames):
        if isinstance(F, tuple): F, Lf = F
        else: Lf = lengths[i] if lengths is not None else None
        F, dr = apply_tolerance(F, Lf, tol); n_jdrop += dr
        V = _values(F, by_segment)
        times.append(F.t)
        if prev is not None:
            for p in set(V) | set(prevV):
                if V[p] != prevV[p]: changes[p].append((i, prevV[p], V[p]))
            ev = EL.classify(prev, F, theta, by_segment)
            ok, s, d = EL.balance(prev, F, ev)
            if not ok: other_counts['balance_failures'] += 1
            lk = {str(x): x for x in prev.cells | F.cells}      # the logger reports cells as strings; map back to labels
            for e in ev:
                raw[e['type']] += 1
                cs = [lk[x] for x in e['cells']]
                if e['type'] == 'swap':
                    pairs = {tuple(sorted((x, y))) for x in cs for y in cs if x != y}
                    lost = [p for p in pairs if V[p] < prevV[p]]; gained = [p for p in pairs if V[p] > prevV[p]]
                    if len(lost) == 1 and len(gained) == 1:
                        sid = n_swaps_raw; n_swaps_raw += 1
                        (a, b), (c, dd) = lost[0], gained[0]
                        elem.append(dict(kind='lost', pair=lost[0], i=i, old=prevV[lost[0]], new=V[lost[0]], swap=sid,
                                         nbr=prev.nb[a] & prev.nb[b]))
                        elem.append(dict(kind='gained', pair=gained[0], i=i, old=prevV[gained[0]], new=V[gained[0]], swap=sid))
                    else: other_counts['swap_unparsed'] += 1
                elif e['type'] == 'clump' and e['pattern'] in (ONE_LOST, ONE_GAINED) and len(cs) == 2:
                    p = tuple(sorted(cs)); a, b = p
                    if e['pattern'] == ONE_LOST:
                        elem.append(dict(kind='lost', pair=p, i=i, old=prevV[p], new=V[p], swap=None, nbr=prev.nb[a] & prev.nb[b]))
                    else:
                        elem.append(dict(kind='gained', pair=p, i=i, old=prevV[p], new=V[p], swap=None))
        prev, prevV = F, V
    return dict(times=times, raw=raw, changes=changes, elem=elem, n_jdrop=n_jdrop, other_counts=other_counts, tol=tol,
                by_segment=by_segment, theta=theta)


def apply_rules(data, W, P, units='', keep_events=False):
    """Rules P and W on collected data (see module doc). Returns (events, summary)."""
    times, raw, changes, n_jdrop, other_counts = data['times'], data['raw'], data['changes'], data['n_jdrop'], data['other_counts']
    tol, by_segment, theta = data['tol'], data['by_segment'], data['theta']
    elem = [dict(e) for e in data['elem']]
    n = len(times)
    el = lambda i, j: abs(times[j] - times[i])
    # RULE P: accepted switches per contact (sparse timeline)
    accepted, censored_at = set(), set()
    for p, ch in changes.items():
        deb = ch[0][1]
        for k, (i, old, new) in enumerate(ch):
            if new == deb: continue
            nxt = ch[k + 1][0] if k + 1 < len(ch) else None
            if nxt is None or el(i, nxt) >= P:
                if (new > old) == (new > deb): accepted.add((p, i))
                if nxt is None and el(i, n - 1) < P: censored_at.add((p, i))
                deb = new
    for e in elem: e['ok'] = (e['pair'], e['i']) in accepted
    by_swap = defaultdict(list)
    for e in elem:
        if e['swap'] is not None: by_swap[e['swap']].append(e)
    swaps_ok, swaps_one_side, swaps_cancelled, halves, censored = 0, 0, 0, [], 0
    events = []
    for sid, es in by_swap.items():
        oks = [e['ok'] for e in es]
        if all(oks):
            swaps_ok += 1
            censored += any((e['pair'], e['i']) in censored_at for e in es)
            if keep_events: events.append(dict(type='swap', via='direct', t=times[es[0]['i']], lost=es[0]['pair'], gained=es[1]['pair']))
        elif any(oks): swaps_one_side += 1; halves += [e for e in es if e['ok']]
        else: swaps_cancelled += 1
    single = [e for e in elem if e['swap'] is None]
    flicker_halves = sum(not e['ok'] for e in single)
    halves += [e for e in single if e['ok']]
    # RULE W: pair the accepted halves
    L = sorted([e for e in halves if e['kind'] == 'lost'], key=lambda e: e['i'])
    G = sorted([e for e in halves if e['kind'] == 'gained'], key=lambda e: e['i'])
    used, paired, gaps = set(), 0, Counter()
    for l in L:
        a, b = l['pair']; best = None
        for gi, g in enumerate(G):
            if gi in used: continue
            c, d = g['pair']
            if len({a, b, c, d}) < 4 or not ({c, d} <= l['nbr']): continue
            dt = el(l['i'], g['i'])
            if dt > W: continue
            key = (dt, g['i'])
            if best is None or key < best[0]: best = (key, gi)
        if best is not None:
            used.add(best[1]); paired += 1; l['paired'] = True
            g = G[best[1]]; gaps[round(el(l['i'], g['i']), 9)] += 1
            censored += ((l['pair'], l['i']) in censored_at or (g['pair'], g['i']) in censored_at)
            if keep_events: events.append(dict(type='swap', via='paired', t=times[l['i']], t_gain=times[g['i']], lost=l['pair'], gained=g['pair']))
    lost_left = sum(not l.get('paired') for l in L); gained_left = len(G) - len(used)
    summary = dict(
        params=dict(W=W, P=P, tol=tol, units=units, by_segment=by_segment, theta=theta,
                    rule='T on frames -> eventlog.classify -> P on elementary contact changes -> W pairing of accepted halves'),
        frames=n, step=(abs(times[1] - times[0]) if n > 1 else None),
        raw_counts=dict(raw), raw_one_lost=sum(e['kind'] == 'lost' and e['swap'] is None for e in elem),
        raw_one_gained=sum(e['kind'] == 'gained' and e['swap'] is None for e in elem),
        swaps=swaps_ok + paired, swaps_direct=swaps_ok, swaps_paired=paired, pair_gaps=dict(sorted(gaps.items())),
        swaps_cancelled_flicker=swaps_cancelled, swaps_one_side_only=swaps_one_side, halves_cancelled_flicker=flicker_halves,
        halves_left_lost=lost_left, halves_left_gained=gained_left, swaps_censored=censored,
        frames_junctions_dropped_by_tol=n_jdrop, balance_failures=other_counts['balance_failures'],
        swap_unparsed=other_counts['swap_unparsed'])
    return events, summary


def vanished_appeared(frames):
    """Cells that disappeared / appeared over the sequence (all event types)."""
    v = a = 0
    for A, B in zip(frames, frames[1:]):
        v += len(A.cells - B.cells); a += len(B.cells - A.cells)
    return v, a
