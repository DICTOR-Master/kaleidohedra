#!/usr/bin/env python3
"""Radial files of tracheids in a conifer cross-section, and their events (One tissue, yew stream; DICTO 15 Nov 2026).

THE CONSTRUCTION (time = the radial coordinate of one image).
  The cambium is a sheet of cells; one cross-section cuts it in a line. Every cell the cambium leaves behind stays in place, so
  the section records that line through time: outward = later. A radial file = the chain of tracheids left by one cambial cell.
  Cut the image at outward position u (measured along the radial direction, in cells or in rings): the files present at u, in
  their order round the stem, form a ROW. The row at u is the frame "the cambium's line at time u": a 1D tiling whose cells are
  files and whose contacts are side-by-side neighbours. The sequence of rows, u increasing, is the tiling over time.
  Events of a row (plain terms):
    split  - one file becomes two side by side (an anticlinal division of the cambial cell);
    end    - a file stops and its two neighbours close up (the cambial cell is lost);
    insert - a new file appears between two that does not branch from either (intrusive growth from above or below the
             section, or a split whose junction lies outside the section);
    sideways shift - a file moves round the stem relative to its neighbours (only measurable as drift; in one row two files
             can never pass each other, so a swap is impossible in a single section: it needs the second, axial, direction).
  For the shared logger each row is drawn on a sphere: the files in a ring round the equator, closed through one cell X (the
  wood outside the window), plus two caps N and S (the cambium above and below the section). Every file then touches its two
  row neighbours and N and S; all corners are triple; Euler V - E + F = 2 holds with V = 2n, E = 3n, F = n + 2 (n = ring cells).
  A split is the logger's split (lineage: the new file's parent), an end is its merge (the neighbours close up), an insert is
  its split without lineage. Swaps cannot occur (N and S never touch), so a swap logged here would be a tracing error.

PIPELINE: image -> lumina (bright, Otsu, or a given label mask) -> cell centroids -> radial direction (strongest alignment of
neighbour links, outward sign from the ring pattern: lumina shrink slowly through latewood and jump up at the ring boundary) ->
successor links (nearest cell outward in a narrow tangential band, one-to-one) -> files (chains) -> heads and tails inside a
window bounded by two GUARD files that run the full radial length (so nothing enters or leaves through the window's sides) ->
rows at steps h -> logger (Euler + balance per step, negative control) -> counts per file per cell step, per ring.
Usage: trace.py IMAGE OUT_JSON [--mask MASK] [--dark-lumen] [--radial-deg A] [--outward +1|-1] [--steps 1,4] [--min-area 12]
       [--rings R]   (R: number of rings in the patch if known; else estimated from the lumen-size profile)"""
import sys, json, argparse, os, math
import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
LOGGER = os.path.join(HERE, '..', '..', '2026-11-15-event-logger', 'scripts')
sys.path.insert(0, os.path.abspath(LOGGER))
import eventlog as EL  # noqa: E402  (shared logger, not edited)


def lumina(img, dark=False, min_area=12, mask=None):
    from skimage import filters, measure, segmentation
    if mask is not None:
        lab = measure.label(mask > 0, connectivity=1)
    else:
        g = img.astype(float)
        if g.ndim == 3: g = g[..., :3].mean(2)
        g = ndi.gaussian_filter(g, 1.0)
        if dark: g = g.max() - g
        th = filters.threshold_otsu(g)
        lab = measure.label(g > th, connectivity=1)
    lab = segmentation.clear_border(lab)
    props = measure.regionprops(lab)
    keep = [p for p in props if p.area >= min_area]
    P = np.array([p.centroid for p in keep])            # (row, col)
    A = np.array([p.area for p in keep], float)
    return P[:, ::-1].copy(), A, lab.shape               # xy


def directions(P, k=6):
    """The two lattice directions of the cell pattern from neighbour links (angles mod 180)."""
    T = cKDTree(P); d, j = T.query(P, k + 1)
    v = P[j[:, 1:]] - P[:, None, :]
    ang = (np.degrees(np.arctan2(v[..., 1], v[..., 0])) % 180).ravel()
    h, _ = np.histogram(ang, 180, (0, 180)); h = ndi.gaussian_filter1d(h.astype(float), 2, mode='wrap')
    p1 = int(np.argmax(h)); h2 = h.copy()
    for o in range(-40, 41): h2[(p1 + o) % 180] = 0
    p2 = int(np.argmax(h2))
    def sharp(p):
        return h[p] / (h[(p + 8) % 180] + h[(p - 8) % 180] + 1e-9)
    return (p1, sharp(p1)), (p2, sharp(p2)), h


def frame_coords(P, deg):
    a = math.radians(deg); er = np.array([math.cos(a), math.sin(a)]); et = np.array([-er[1], er[0]])
    return P @ er, P @ et


def ring_profile(r, A, cell):
    """Mean lumen area in radial bins of one cell spacing; ring boundaries = abrupt rises."""
    lo, hi = r.min(), r.max(); nb = max(4, int((hi - lo) / cell))
    idx = np.clip(((r - lo) / (hi - lo + 1e-9) * nb).astype(int), 0, nb - 1)
    m = np.array([A[idx == i].mean() if np.any(idx == i) else np.nan for i in range(nb)])
    m = np.where(np.isnan(m), np.nanmean(m), m)
    return m


def outward_sign(r, A, cell):
    """Latewood -> earlywood is an abrupt rise in lumen size; earlywood -> latewood is gradual. Outward is the direction in
    which the largest steps are rises. Returns +1 or -1 and the score (sum of cubed differences, normalised)."""
    m = ring_profile(r, A, cell); d = np.diff(m) / (np.std(m) + 1e-9)
    s = float(np.sum(d ** 3))
    return (1 if s >= 0 else -1), s, m


def count_rings(m):
    """Rings = abrupt rises from the lower third to the upper third of the profile within 3 bins."""
    lo, hi = np.nanpercentile(m, 33), np.nanpercentile(m, 67); n = 0; last = -10
    for i in range(len(m) - 1):
        if m[i] < lo and np.max(m[i + 1:i + 4]) > hi and i - last > 4: n += 1; last = i
    return n


def link(r, t, A, dt):
    """Successor of each cell: the nearest cell outward whose tangential offset is within 0.45 dt (dt = file spacing), and
    no farther than 2.5 typical radial spacings; one-to-one (a contested successor goes to the tangentially closer cell)."""
    n = len(r); order = np.argsort(r)
    T = cKDTree(np.c_[r, t])
    cand = {}
    # typical radial spacing from nearest outward neighbour in band
    for i in range(n):
        js = T.query_ball_point([r[i], t[i]], 3.0 * dt)
        best = None
        for j in js:
            dr = r[j] - r[i]; dtt = abs(t[j] - t[i])
            if dr <= 0.15 * math.sqrt(A[i]) or dtt > 0.45 * dt: continue
            if best is None or dr < best[0]: best = (dr, dtt, j)
        if best: cand[i] = best
    drs = np.array([b[0] for b in cand.values()]); drmed = float(np.median(drs)) if len(drs) else dt
    succ = {}; claimed = {}
    for i, (dr, dtt, j) in sorted(cand.items(), key=lambda kv: kv[1][1]):
        if dr > 2.5 * drmed * max(1.0, math.sqrt(A[i] / np.median(A))): continue
        if j in claimed: continue
        claimed[j] = i; succ[i] = j
    return succ, drmed


def chains(n, succ):
    pred = {j: i for i, j in succ.items()}
    out = []
    for i in range(n):
        if i in pred: continue
        c = [i]
        while c[-1] in succ: c.append(succ[c[-1]])
        out.append(c)
    return out


def analyse(P, A, shape, radial_deg=None, outward=None, steps=(1, 4), rings=None):
    res = {}
    (p1, s1), (p2, s2), h = directions(P)
    if radial_deg is None:
        # radial = the sharper of the two alignment peaks (files are straighter than tangential rows)
        radial_deg = p1 if s1 >= s2 else p2
    res['peaks'] = dict(p1=p1, sharp1=round(s1, 3), p2=p2, sharp2=round(s2, 3), radial_deg=radial_deg)
    r, t = frame_coords(P, radial_deg)
    T = cKDTree(np.c_[r, t]); d, j = T.query(np.c_[r, t], 7)
    vt = np.abs(t[j[:, 1:]] - t[:, None]); vr = np.abs(r[j[:, 1:]] - r[:, None])
    tang = vt[(vt > 2 * vr)]; dt = float(np.median(tang)) if len(tang) else float(np.median(d[:, 1]))
    rad = vr[(vr > 2 * vt)]; dr0 = float(np.median(rad)) if len(rad) else dt
    sgn, score, prof = outward_sign(r, A, dr0)
    if outward is not None: sgn = outward
    res['outward'] = dict(sign=sgn, score=round(score, 3), forced=outward is not None)
    r = r * sgn
    succ, drmed = link(r, t, A, dt)
    ch = chains(len(r), succ)
    # gap closing: a chain tail and a chain head in line (outward gap up to 4 radial spacings, tangential offset up to 0.5 of a
    # file spacing (0.6), measured after extrapolating the tail's own drift) are one file with a missed or merged lumen between them
    # (the usual tracking step of closing gaps; one-to-one, nearest first)
    heads0 = {c[0]: c for c in ch}; cand = []
    for c in ch:
        i = c[-1]; drift = (t[c[-1]] - t[c[-3]]) / max(r[c[-1]] - r[c[-3]], 1e-9) if len(c) >= 3 else 0.0
        for c2 in ch:
            j = c2[0]
            if c2 is c: continue
            dr = r[j] - r[i]
            if 0 < dr <= 4 * drmed and abs(t[j] - (t[i] + drift * dr)) <= 0.6 * dt:
                cand.append((dr + 2 * abs(t[j] - t[i] - drift * dr), i, j))
    used_t, used_h, joins = set(), set(), 0
    for _, i, j in sorted(cand):
        if i in used_t or j in used_h: continue
        used_t.add(i); used_h.add(j); succ[i] = j; joins += 1
    ch = chains(len(r), succ)
    res['spacing'] = dict(tangential_px=round(dt, 2), radial_px=round(drmed, 2), cells=len(r), links=len(succ), files=len(ch), gap_joins=joins)
    # files as arrays; chains of fewer than MINLEN cells are lumen fragments or debris, not files: left out of rows and events
    MINLEN = 3
    res['fragments_dropped'] = dict(chains=sum(len(c) < MINLEN for c in ch), cells=sum(len(c) for c in ch if len(c) < MINLEN))
    ch = [c for c in ch if len(c) >= MINLEN]
    F = [dict(r=r[c], t=t[c], ids=c) for c in ch]
    rmin, rmax = r.min(), r.max()
    margin = 1.5 * drmed
    # guard files: long files (radial span at least 70% of the longest) far apart round the stem; the window is the radial span
    # common to the two guards, and everything between them. Nothing can enter or leave the window through its sides.
    spans = np.array([f['r'][-1] - f['r'][0] for f in F]); smax = spans.max()
    full = [k for k in range(len(F)) if spans[k] >= 0.7 * smax]
    res['full_length_files'] = len(full)
    if len(full) < 2:
        res['ok'] = False; res['why'] = 'fewer than two long files: no guarded window'
        res['chain_lengths'] = np.percentile([len(f['r']) for f in F], [50, 90, 99, 100]).tolist()
        return res, dict(F=F, heads=[], tails=[], L=None, R=None)
    tm = {k: float(np.median(F[k]['t'])) for k in full}
    best = None
    for L_ in full:
        for R_ in full:
            if tm[R_] <= tm[L_]: continue
            a, b = max(F[L_]['r'][0], F[R_]['r'][0]), min(F[L_]['r'][-1], F[R_]['r'][-1])
            if b - a < 0.5 * smax: continue
            score = (b - a) * (tm[R_] - tm[L_])
            if best is None or score > best[0]: best = (score, L_, R_)
    if best is None:
        res['ok'] = False; res['why'] = 'no pair of long files with a common span of half the longest'
        return res, dict(F=F, heads=[], tails=[], L=None, R=None)
    _, L, R = best
    r0, r1 = max(F[L]['r'][0], F[R]['r'][0]) + 0.5 * drmed, min(F[L]['r'][-1], F[R]['r'][-1]) - 0.5 * drmed

    def tat(f, u):
        return float(np.interp(u, f['r'], f['t']))

    def inside(f, u):
        return f['r'][0] <= u <= f['r'][-1] and tat(F[L], u) < tat(f, u) < tat(F[R], u)
    # heads / tails inside the window, classified
    heads, tails = [], []
    TT = cKDTree(np.c_[r, t])
    def wood_beyond(u, tt, sgn):
        # the traced wood continues past this point (outward for a tail, inward for a head): at least 3 cells 0.5 to 3 radial
        # spacings beyond, within 2 file spacings round the stem. Else the file meets the edge of the picture, not an event.
        js = TT.query_ball_point([u + sgn * 1.75 * drmed, tt], 2.5 * dt)
        return sum(1 for j in js if 0.5 * drmed < sgn * (r[j] - u) < 3 * drmed and abs(t[j] - tt) < 2 * dt) >= 3
    for k, f in enumerate(F):
        if k in (L, R) or len(f['r']) < 1: continue
        u0, u1 = f['r'][0], f['r'][-1]
        if r0 < u0 < r1 and tat(F[L], u0) < f['t'][0] < tat(F[R], u0) and wood_beyond(u0, f['t'][0], -1):
            # parent: a file that is present just inward of the head and tangentially adjacent (within one file spacing)
            par = None; best = 1e9
            for q, g in enumerate(F):
                if q == k or not (g['r'][0] < u0 - 0.3 * drmed and g['r'][-1] >= u0): continue
                dd = abs(tat(g, u0 - 0.5 * drmed) - f['t'][0])
                if dd < 0.9 * dt and dd < best: best, par = dd, q
            heads.append(dict(file=k, u=float(u0), parent=par))
        if r0 < u1 < r1 and tat(F[L], u1) < f['t'][-1] < tat(F[R], u1) and wood_beyond(u1, f['t'][-1], +1):
            tails.append(dict(file=k, u=float(u1)))
    # JUMP (sideways shift seen in one section): a tail and a head of different files within 1.5 radial spacings and 1.2 file
    # spacings tangentially, the head not branching from the tail's own file: the file continues one place over. Counted as one
    # jump, not as an end plus a new file. (In a synthetic pattern without shifts every jump is a tracing error.)
    pairs = sorted((abs(F[hd['file']]['r'][0] - tl['u']) / drmed + abs(F[hd['file']]['t'][0] - F[tl['file']]['t'][-1]) / dt, a, b)
                   for a, tl in enumerate(tails) for b, hd in enumerate(heads)
                   if abs(F[hd['file']]['r'][0] - tl['u']) <= 1.5 * drmed and abs(F[hd['file']]['t'][0] - F[tl['file']]['t'][-1]) <= 1.2 * dt)
    ut, uh, jumps = set(), set(), []
    for _, a, b in pairs:
        if a in ut or b in uh: continue
        ut.add(a); uh.add(b); jumps.append((a, b))
    res['jumps'] = len(jumps); tails_all, heads_all = list(tails), list(heads)
    jump_heads = {heads[b]['file'] for a, b in jumps}; jump_tails = {tails[a]['file'] for a, b in jumps}
    heads = [h for h in heads if h['file'] not in jump_heads]; tails = [x for x in tails if x['file'] not in jump_tails]
    alias = {}
    def root(k):
        while k in alias: k = alias[k]
        return k
    for a, b in sorted(jumps, key=lambda ab: tails_all[ab[0]]['u']):   # the file continues one place over: join the chains
        ta, hb = root(tails_all[a]['file']), heads_all[b]['file']
        if ta == hb or F[hb] is None: continue
        F[ta] = dict(r=np.r_[F[ta]['r'], F[hb]['r']], t=np.r_[F[ta]['t'], F[hb]['t']], ids=list(F[ta]['ids']) + list(F[hb]['ids']))
        F[hb] = None; alias[hb] = ta
    for h in heads:
        h['file'] = root(h['file'])
        if h['parent'] is not None: h['parent'] = root(h['parent'])
    for x in tails: x['file'] = root(x['file'])
    if L in alias or R in alias: res['why'] = 'a guard file was joined'
    res['window'] = dict(r0=round(r0, 1), r1=round(r1, 1), span_cells=round((r1 - r0) / drmed, 1), guard_files=[L, R])
    # rows (frames) at steps h (in radial cell spacings)
    out_rows = {}
    for h in steps:
        us = np.arange(r0, r1, h * drmed)
        frames = []; prev_present = set(); nfiles = []
        for i, u in enumerate(us):
            pres = [k for k, f in enumerate(F) if f is not None and k not in (L, R) and inside(f, u)]
            pres.sort(key=lambda k: tat(F[k], u))
            ring = ['X', f'f{L}'] + [f'f{k}' for k in pres] + [f'f{R}']
            nfiles.append(len(ring) - 1)
            cells = ring + ['N', 'S']
            n = len(ring)
            bnd = [[ring[a], ring[(a + 1) % n]] for a in range(n)] + [[c, 'N'] for c in ring] + [[c, 'S'] for c in ring]
            jun = [[ring[a], ring[(a + 1) % n], cap] for a in range(n) for cap in ('N', 'S')]
            parents = {}
            for hd in heads:
                k = hd['file']
                if k in pres and k not in prev_present and hd['parent'] is not None and f"f{hd['parent']}" in ring:
                    parents[f'f{k}'] = {f"f{hd['parent']}": 1.0}
            frames.append(EL.Tiling(cells, bnd, jun, 2, 'sphere', float((u - r0) / drmed), parents=parents))
            prev_present = set(pres)
        rows, summ = EL.run(frames)
        neg = None
        for A_, B_ in zip(frames, frames[1:]):
            ev = EL.classify(A_, B_)
            if any(e['net'] for e in ev):
                bad = [dict(e) for e in ev]; ii = next(i for i, e in enumerate(bad) if e['net']); bad[ii]['type'] = 'swap'
                neg = not EL.balance(A_, B_, bad)[0]; break
        summ['neg_control_caught'] = neg
        summ.pop('frames_failing', None)
        file_steps = float(np.sum(nfiles[:-1]) * h) if len(nfiles) > 1 else 0.0
        out_rows[h] = dict(frames=len(frames), logger=summ, file_cell_steps=file_steps)
    res['heads'] = dict(total=len(heads), with_parent=sum(hd['parent'] is not None for hd in heads),
                        no_parent=sum(hd['parent'] is None for hd in heads))
    res['tails'] = len(tails)
    nf = [sum(1 for k, f in enumerate(F) if f is not None and inside(f, u)) for u in np.arange(r0, r1, drmed)]
    file_cells = float(np.sum(nf))
    res['file_cells_in_window'] = file_cells
    res['mean_files_in_row'] = float(np.mean(nf)) if nf else 0
    res['per_file_per_cell'] = dict(jump=len(jumps) / max(file_cells, 1), split=len([x for x in heads if x['parent'] is not None]) / max(file_cells, 1),
                                    insert=len([x for x in heads if x['parent'] is None]) / max(file_cells, 1),
                                    end=len(tails) / max(file_cells, 1))
    nr = rings if rings is not None else count_rings(prof)
    res['rings'] = dict(n=nr, estimated=rings is None, profile_bins=len(prof))
    if nr:
        cpr = (r1 - r0) / drmed / max(nr, 1) if nr else None
        res['cells_per_ring'] = cpr
        res['per_file_per_ring'] = {k: v * cpr for k, v in res['per_file_per_cell'].items()}
    res['steps'] = {str(k): v for k, v in out_rows.items()}
    res['ok'] = all(v['logger']['ok'] for v in out_rows.values())
    return res, dict(F=F, heads=heads, tails=tails, L=L, R=R)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('image'); ap.add_argument('out')
    ap.add_argument('--mask'); ap.add_argument('--dark-lumen', action='store_true')
    ap.add_argument('--radial-deg', type=float); ap.add_argument('--outward', type=int)
    ap.add_argument('--steps', default='1,4'); ap.add_argument('--min-area', type=int, default=12)
    ap.add_argument('--rings', type=int); ap.add_argument('--figure')
    a = ap.parse_args()
    from PIL import Image
    img = np.array(Image.open(a.image))
    mask = np.array(Image.open(a.mask)) if a.mask else None
    P, A, shape = lumina(img, a.dark_lumen, a.min_area, mask)
    res, geo = analyse(P, A, shape, a.radial_deg, a.outward, tuple(float(s) for s in a.steps.split(',')), a.rings)
    res['image'] = os.path.basename(a.image); res['image_shape'] = list(img.shape)
    if a.figure and geo:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 8 * img.shape[0] / img.shape[1]))
        ax.imshow(img if img.ndim == 2 else img[..., :3], cmap='gray'); ax.set_axis_off()
        for k, f in enumerate(geo['F']):
            if f is None: continue
            xy = P[f['ids']]
            ax.plot(xy[:, 0], xy[:, 1], '-', lw=0.8, color='#ffbf00' if k in (geo['L'], geo['R']) else '#3a7bd5')
        for hd in geo['heads']:
            x, y = P[geo['F'][hd['file']]['ids'][0]]
            ax.plot(x, y, 'o', ms=5, color='#2ca02c' if hd['parent'] is not None else '#9467bd')
        for tl in geo['tails']:
            x, y = P[geo['F'][tl['file']]['ids'][-1]]
            ax.plot(x, y, 'x', ms=6, color='#d62728')
        fig.savefig(a.figure, dpi=110, bbox_inches='tight'); plt.close(fig)
    json.dump(res, open(a.out, 'w'), indent=1, default=float)
    print(('TRACE_OK ' if res.get('ok') else 'TRACE_FAIL ') + json.dumps(dict(cells=res.get('spacing'), heads=res.get('heads'),
          tails=res.get('tails'), rings=res.get('rings'), ok=res.get('ok'), why=res.get('why')), default=float))


if __name__ == '__main__':
    main()
