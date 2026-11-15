"""Macroscopic swaps by the Rutenberg-McCurdy rule, without a time window (One tissue, three scales; DICTO, 15 Nov 2026).
Post-processing on top of pairing.py and eventlog.py; neither is changed. Rules fixed BEFORE any run (README, section
"Rutenberg-McCurdy count").

SOURCE. A. D. Rutenberg and M. B. McCurdy, "Scaling state of dry two-dimensional froths: universal angle-deviations and structure",
Phys. Rev. E 73, 011403 (2006), arXiv cond-mat/0502287 (free version read in full, section III C and Fig. 7). Their definition, quoted:
"We count T1 events distinctly if all bubbles involved are bigger than l^2, and count T2n events if the bubble has n sides as it
shrinks past the scale of l^2", with l = sqrt(rc L(t)), the geometric mean of the microscopic scale rc (the distance at which two
vertices enter a T1; the Plateau-border size) and the mean bubble size L(t) ~ sqrt(<A>). "Any side-shedding that occurs at
microscopic scales should simply be counted as the details of the associated T2 process." So their rule is an AREA rule on all
the bubbles of a T1, not a rule on later vanishing: a side shed while the bubble is still larger than l^2 counts as macroscopic.

Two counts are given here, both without a time window:
RULE SS (side-shedding, combinatorial; the rule asked for in the plan): a counted swap is SIDE-SHEDDING when a cell x of its lost
  pair later vanishes, at the first frame after the loss in which x is absent (time T_x), and x gains no contact in any counted swap
  between the loss and T_x (t_loss < t_gain < T_x). Macroscopic (SS) = counted swaps - side-shedding swaps.
  SS_any (reported beside it): the same without the no-regain condition.
RULE RM (the paper's own area rule; needs cell areas per frame): a counted swap is MICROSCOPIC when one of its four cells has area
  below l^2(t) = rc * sqrt(A_box / N(t)) in any frame from the frame before its first change to the frame of its last change (frames
  where the cell exists). Macroscopic (RM) = counted swaps - microscopic swaps. rc is in the frames' length unit (foam: pixels).
  Also: the side number of each vanishing cell "as it shrinks past l^2" = its neighbour count in the first frame of its final
  stretch below l^2 (for the 3/4/5-sided proportions, Rutenberg-McCurdy 9 / 84 / 7 %).
Counted swaps = pairing.py swaps (accepted direct swaps + paired halves) under the given W, P (W = P = 0: the logger's swaps).
Times are physical and must increase along the frames. T2 = vanished cells (pairing.vanished_appeared).

Use: data = pairing.collect(frames); res = rm_count(frames, data, W, P, areas=None, box=None, rcs=(1,))."""
from bisect import bisect_right
from collections import Counter, defaultdict
import pairing as PR


def vanish_times(frames):
    """cell -> sorted list of times at which it is absent after being present (first absent frame)."""
    out = defaultdict(list)
    for A, B in zip(frames, frames[1:]):
        for x in A.cells - B.cells: out[x].append(B.t)
    return out


def side_shedding(swaps, frames):
    """Classify swaps (dicts with lost, gained, t, optional t_gain; t = time of the loss) by RULE SS. Returns per-swap flags
    (ss, ss_any) and the shed-to-vanish delays of the SS swaps."""
    van = vanish_times(frames)
    gains = defaultdict(list)
    for s in swaps:
        tg = s.get('t_gain', s['t'])
        for c in s['gained']: gains[c].append(tg)
    for g in gains.values(): g.sort()
    flags, delays, alive_end = [], [], 0
    for s in swaps:
        tl = s['t']; ss = ss_any = False; best = None; noregain_alive = False
        for x in s['lost']:
            vt = van.get(x, [])
            k = bisect_right(vt, tl)
            g = gains.get(x, [])
            j = bisect_right(g, tl)
            if k == len(vt):                                   # x does not vanish after the loss (record ends)
                if j == len(g): noregain_alive = True
                continue
            T = vt[k]; ss_any = True
            if j == len(g) or g[j] >= T:                       # no gain of x strictly between the loss and its vanishing
                ss = True; d = T - tl; best = d if best is None else min(best, d)
        if ss: delays.append(best)
        if not ss and noregain_alive: alive_end += 1
        flags.append((ss, ss_any))
    return flags, delays, alive_end


def microscopic(swaps, frames, areas, box, rc):
    """RULE RM flags per swap. areas[i]: dict cell -> area in frame i; box: total area."""
    tix = {F.t: i for i, F in enumerate(frames)}
    ell2 = [rc * (box / len(F.cells)) ** 0.5 for F in frames]
    flags = []
    for s in swaps:
        i1, i2 = tix[s['t']], tix[s.get('t_gain', s['t'])]
        lo, hi = max(0, min(i1, i2) - 1), max(i1, i2)
        cells = set(s['lost']) | set(s['gained'])
        small = any(areas[i].get(c, float('inf')) < ell2[i] for i in range(lo, hi + 1) for c in cells)
        flags.append(small)
    return flags, ell2


def sides_at_ell(frames, areas, ell2):
    """Side number of each vanishing cell when it shrinks past l^2 for the last time (first frame of its final stretch below l^2).
    Cells that vanish without ever being below l^2 in a frame are counted under 'never below'."""
    out = Counter()
    last = {}
    for i, (A, B) in enumerate(zip(frames, frames[1:])):
        for x in A.cells - B.cells:
            j = i
            if not areas[j].get(x, float('inf')) < ell2[j]: out['never below'] += 1; continue
            while j - 1 >= 0 and x in frames[j - 1].cells and areas[j - 1].get(x, float('inf')) < ell2[j - 1]: j -= 1
            out[len(frames[j].nb[x])] += 1
    return dict(sorted(out.items(), key=lambda kv: str(kv[0])))


def rm_count(frames, data, W, P, areas=None, box=None, rcs=(1.0,), units=''):
    times = [F.t for F in frames]
    assert all(b > a for a, b in zip(times, times[1:])), 'times must increase'
    swaps, sm = PR.apply_rules(data, W, P, units=units, keep_events=True)
    van, app = PR.vanished_appeared(frames)
    flags, delays, alive_end = side_shedding(swaps, frames)
    n = len(swaps); ss = sum(f[0] for f in flags); ssa = sum(f[1] for f in flags)
    delays.sort()
    q = lambda p: delays[min(len(delays) - 1, int(p * len(delays)))] if delays else None
    res = dict(params=dict(W=W, P=P, units=units, tol=data['tol'], by_segment=data['by_segment'], rcs=list(rcs),
                           rule='pairing.py (T, logger, P, W) -> SS: lost-pair cell vanishes later with no gain between; RM: any cell < rc*sqrt(<A>)'),
               swaps=n, vanished=van, appeared=app,
               SS=dict(side_shedding=ss, macroscopic=n - ss, identity_ok=(ss + (n - ss) == n and ss <= ssa <= n),
                       side_shedding_any=ssa, macroscopic_any=n - ssa, not_ss_lost_cell_alive_at_end_no_regain=alive_end,
                       shed_to_vanish_delay_quartiles=[q(0.25), q(0.5), q(0.75)]),
               per_vanished=dict(total=round(n / van, 4) if van else None,
                                 SS_macroscopic=round((n - ss) / van, 4) if van else None,
                                 SS_side_shedding=round(ss / van, 4) if van else None,
                                 SS_any_macroscopic=round((n - ssa) / van, 4) if van else None))
    if areas is not None:
        res['RM'] = {}
        for rc in rcs:
            mf, ell2 = microscopic(swaps, frames, areas, box, rc)
            mic = sum(mf)
            both = sum(1 for a, b in zip(mf, flags) if a and b[0])
            res['RM'][str(rc)] = dict(microscopic=mic, macroscopic=n - mic,
                                      macroscopic_per_vanished=round((n - mic) / van, 4) if van else None,
                                      microscopic_and_SS=both, ell2_first_last=[round(ell2[0], 3), round(ell2[-1], 3)],
                                      sides_at_ell2=sides_at_ell(frames, areas, ell2))
    return res
