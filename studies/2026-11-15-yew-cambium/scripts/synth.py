#!/usr/bin/env python3
"""Synthetic conifer cross-section with KNOWN file events (control for trace.py; One tissue, yew stream, 15 Nov 2026).

A row of radial files grows outward cell by cell. Rings: each ring has C cells per file (earlywood: large, thin-walled;
latewood: radially flat, thick-walled), ring boundaries shared by all files. Per file and per cell step:
  - split with probability ps: the file divides into two daughters of half the tangential width, which widen back over K = 12 cells
    (an anticlinal division of the initial seen in the cross-section);
  - end with probability pe: the file tapers to nothing over K cells and its neighbours widen (loss of the initial);
  - each file has its own radial cell-size jitter, so tangential rows are staggered as in real wood.
Widths are absolute; each row is placed so that the files it shares with the row before move least (least squares).
Output: a grey image (bright lumina, dark walls, blur, noise, a slight rotation) and truth JSON (event list with outward
cell index, file counts). Usage: synth.py OUT_PREFIX SEED [ps pe rings cells_per_ring n_files rot_deg]"""
import sys, json, numpy as np
from scipy import ndimage as ndi

def make(seed=1, ps=0.004, pe=0.004, rings=6, C=24, n0=40, rot=7.0, K=12, wt=26.0):
    rng = np.random.default_rng(seed)
    # files: dict id -> dict(w=target width share, born, parent, ending=countdown or None, grow=countdown)
    files = [dict(id=i, w=1.0, age=K, end=None, parent=None, born=0) for i in range(n0)]
    nid = n0; events = []; rows = []           # rows: list over cell steps of [(id, width_px, radial_size_px, wall_px)]
    steps = rings * C
    for k in range(steps):
        new = []
        for f in files:
            if f['end'] is None and f['age'] >= K and k > 2 and k < steps - 3:
                u = rng.random()
                if u < ps:
                    a = dict(id=nid, w=0.5, age=0, end=None, parent=f['id'], born=k); nid += 1
                    b = dict(id=f['id'], w=0.5, age=0, end=None, parent=None, born=f['born'])
                    left = rng.random() < 0.5
                    new += [a, b] if left else [b, a]
                    events.append(dict(type='split', file=f['id'], new=a['id'], step=k)); continue
                elif u < ps + pe:
                    f['end'] = K; events.append(dict(type='end', file=f['id'], step=k + K))
            new.append(f)
        files = []
        for f in new:
            if f['end'] is not None:
                f['end'] -= 1; f['w'] = max(0.0, f['w'] * f['end'] / (f['end'] + 1))
                if f['end'] <= 0: continue
            elif f['age'] < K:
                f['age'] += 1; f['w'] = min(1.0, f['w'] + 0.5 / K)
            files.append(f)
        pos = (k % C) / C                                  # position within the ring: 0 = first earlywood cell
        early = pos < 0.65
        rs = (34.0 if early else 34.0 - 18.0 * (pos - 0.65) / 0.35)   # radial cell size (px)
        wall = (2.2 if early else 2.2 + 1.6 * (pos - 0.65) / 0.35)
        rows.append([(f['id'], f['w'], rs * (1 + 0.15 * rng.standard_normal()), wall, rs) for f in files])
    return rows, events, dict(steps=steps, rings=rings, cells_per_ring=C, n0=n0, final=len(files), wt=wt, rot=rot, seed=seed,
                              ps=ps, pe=pe, K=K)

def render(rows, meta, rng):
    wt = meta['wt']; C = meta['cells_per_ring']
    total = max(sum(r[1] for r in row) for row in rows) * wt      # the circumference grows: widths are absolute (no renormalisation)
    # rows carry (id, w, jittered radial size, wall, nominal size). Ring boundaries are shared by all files: within each ring a
    # file's jittered sizes are rescaled so that they cover the same radial span as the nominal sizes of the steps it is present.
    jit, nom = {}, {}
    for k, row in enumerate(rows):
        for fid, w, rs, wall, rn in row:
            key = (fid, k // C); jit[key] = jit.get(key, 0.0) + rs; nom[key] = nom.get(key, 0.0) + rn
    ring_start, acc = [], 0.0
    for k, row in enumerate(rows):
        if k % C == 0: ring_start.append(acc)
        acc += row[0][4]
    # Tangential placement: in every row the files sit side by side with their widths; each row is shifted so that the files it
    # shares with the row before move least (least squares). File boundaries are then lines x(r) through the rows' nominal
    # radial centres, shared by neighbouring files, so two files never overlap and every radial wall is continuous.
    rnom, acc = [], 0.0
    for k, row in enumerate(rows): rnom.append(acc + row[0][4] / 2); acc += row[0][4]
    rnom = np.array(rnom)
    prevc, bounds = {}, {}                                   # bounds[fid] = list of (k, left, right)
    for k, row in enumerate(rows):
        rel, x = {}, 0.0
        for fid, w, rs, wall, rn in row: rel[fid] = (x, x + w * wt); x += w * wt
        shared = [f for f in rel if f in prevc]
        off = float(np.mean([prevc[f] - (rel[f][0] + rel[f][1]) / 2 for f in shared])) if shared else (total - x) / 2
        for f, (l, rr) in rel.items(): bounds.setdefault(f, []).append((k, l + off, rr + off))
        prevc = {f: (rel[f][0] + rel[f][1]) / 2 + off for f in rel}
    rpos = {}; cells = []
    for k, row in enumerate(rows):
        ring = k // C
        nom_before = sum(rows[j][0][4] for j in range(ring * C, k))
        for fid, w, rs, wall, rn in row:
            key = (fid, ring)
            if (fid, ring, 'c') not in rpos: rpos[(fid, ring, 'c')] = nom_before
            r0 = ring_start[ring] + rpos[(fid, ring, 'c')]
            sz = rs * nom[key] / jit[key]
            rpos[(fid, ring, 'c')] += sz
            cells.append((fid, k, r0, r0 + sz, wall))
    xmin = min(l for v in bounds.values() for _, l, _ in v)
    H = int(acc) + 60; Wd = int(max(rr for v in bounds.values() for _, _, rr in v) - xmin) + 40
    img = np.zeros((H, Wd), np.float32) + 0.15               # wall grey
    out = []
    for fid, k, r0, r1, wall in cells:
        B = np.array(bounds[fid]); kk = rnom[B[:, 0].astype(int)]
        ys = np.arange(int(round(r0 + 20 + wall)), int(round(r1 + 20 - wall)))
        if len(ys) == 0: continue
        # boundaries step at the nominal row edges (nearest row of this file), so a daughter and its parent never overlap
        ii = np.clip(np.abs((ys - 20)[:, None] - kk[None, :]).argmin(1), 0, len(kk) - 1)
        lft = B[ii, 1] - xmin + 20 + wall; rgt = B[ii, 2] - xmin + 20 - wall
        for y, a_, b_ in zip(ys, lft, rgt):
            if b_ - a_ >= 1: img[y, int(round(a_)):int(round(b_))] = 0.9
        xm = float(np.interp((r0 + r1) / 2, kk, (B[:, 1] + B[:, 2]) / 2) - xmin + 20)
        out.append((xm - 1, xm + 1, r0, r1, wall, fid, k))
    cells = out
    img = ndi.gaussian_filter(img, 1.2) + 0.06 * rng.standard_normal(img.shape).astype(np.float32)
    sh0 = img.shape
    img = ndi.rotate(img, meta['rot'], reshape=True, order=1, mode='constant', cval=0.15)
    # carry the cell centres into the rotated picture (convention of scipy.ndimage.rotate, checked on a single bright pixel:
    # q = R (p - c0) + c1 with R = [[cos, sin], [-sin, cos]] on (x, y), c0 / c1 the centres before / after)
    th = np.radians(meta['rot']); Rm = np.array([[np.cos(th), np.sin(th)], [-np.sin(th), np.cos(th)]])
    c0 = np.array([(sh0[1] - 1) / 2, (sh0[0] - 1) / 2]); c1 = np.array([(img.shape[1] - 1) / 2, (img.shape[0] - 1) / 2])
    rc = []
    for x0, x1, r0, r1, wall, fid, k in cells:
        q = Rm @ (np.array([(x0 + x1) / 2, (r0 + r1) / 2 + 20]) - c0) + c1
        rc.append((q[0] - 1, q[0] + 1, q[1] - 20 - 0.0, q[1] - 20, wall, fid, k))
    return np.clip(img, 0, 1), rc

if __name__ == '__main__':
    out, seed = sys.argv[1], int(sys.argv[2])
    kw = {}
    names = ['ps', 'pe', 'rings', 'C', 'n0', 'rot']
    for n, v in zip(names, sys.argv[3:]): kw[n] = float(v) if n in ('ps', 'pe', 'rot') else int(v)
    rows, events, meta = make(seed, **kw)
    img, cells = render(rows, meta, np.random.default_rng(seed + 1000))
    # event positions in the unrotated frame (pixel x, y of the lumen centre): split = first cell of the new file; end = last
    # cell of the ending file
    first, last = {}, {}
    for x0, x1, r0, r1, wall, fid, k in cells:
        c = ((x0 + x1) / 2, (r0 + r1) / 2 + 20)
        if fid not in first: first[fid] = c
        last[fid] = c
    for e in events:
        e['xy'] = first[e['new']] if e['type'] == 'split' else last.get(e['file'])
    from PIL import Image
    Image.fromarray((img * 255).astype(np.uint8)).save(out + '.png')
    file_steps = sum(len(r) for r in rows)
    truth = dict(meta=meta, events=events, n_split=sum(e['type'] == 'split' for e in events),
                 n_end=sum(e['type'] == 'end' for e in events), file_cells=file_steps,
                 note='outward = +y before rotation by rot degrees (counter-clockwise, scipy.ndimage.rotate)')
    json.dump(truth, open(out + '.truth.json', 'w'), indent=1)
    print(f"SYNTH_OK {out}.png {img.shape} splits {truth['n_split']} ends {truth['n_end']} files {meta['n0']}->{meta['final']}")
