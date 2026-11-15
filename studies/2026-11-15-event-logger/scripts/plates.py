"""Earth's plates as a tiling sequence (One tissue, three scales, Step 1). Reads a published plate model with pyGPlates (GPlates
project, GPL-2.0; Müller et al. 2018, G-cubed 19, 2243) through the model download of GPlately (Mather et al. 2024, Geoscience Data
Journal 11, 3-10, doi:10.1002/gdj3.185; GPL-2.0) and its PlateModelManager. The plate model itself: Müller et al. 2019, Tectonics 38,
1884-1907 (CC BY 4.0 data, EarthByte). We call their code; no code of theirs is copied here.
RULES (stated, fixed before counting):
  * plates = the model's resolved topological plate polygons (ResolveTopologyType.boundary); deforming networks are ignored (they
    overlay the rigid plate polygons, which alone cover the sphere);
  * label = reconstruction plate ID (persistent through time); two polygons with one plate ID in one frame get suffixes #1, #2;
  * boundaries = maximal chains of shared sub-segments between junctions (consecutive sub-segments shared by the same two plates
    are one boundary); a junction = a point where three or more plates meet; a closed boundary without a junction = a loop;
  * lineage for split / merge vs birth / death: 40 000 near-uniform points; a newborn plate's points are rotated back with its own
    rotation to the earlier time and located there (parents); a vanishing plate's points are rotated forward (heirs).
Usage: python plates.py present MODEL            -> plates_present_MODEL.json
       python plates.py series MODEL STEP TMAX   -> plates_series_MODEL_STEP.json (+ _frames.jsonl, _events.json)"""
import sys, os, json, math, itertools, time as _time
from collections import Counter, defaultdict
import numpy as np
import pygplates
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eventlog import Tiling, run, rebalance_log, check_tiling
from plate_model_manager import PlateModelManager

def load(model, data_dir=os.path.expanduser('~/plate-models')):
    m = PlateModelManager().get_model(model, data_dir=data_dir)
    rot = pygplates.RotationModel(m.get_rotation_model())
    topo = [pygplates.FeatureCollection(f) for f in m.get_topologies()]
    return rot, topo, m

SNAP = 1e-4      # radians (640 m): sub-segment ends closer than this are one point; ends this close to another sub-segment split it

def resolve(rot, topo, t):
    rts, sbs = [], []
    pygplates.resolve_topologies(topo, rot, rts, float(t), sbs, resolve_topology_types=pygplates.ResolveTopologyType.boundary)
    fid = lambda rt: rt.get_feature().get_feature_id().get_string()
    pidof = lambda rt: rt.get_feature().get_reconstruction_plate_id()
    # polygons with one plate ID that share a boundary (overlapping or abutting pieces) are one cell; separate pieces get #1, #2
    grp = {fid(rt): fid(rt) for rt in rts}
    def gf(x):
        while grp[x] != x: grp[x] = grp[grp[x]]; x = grp[x]
        return x
    for sb in sbs:
        for ss in sb.get_shared_sub_segments():
            srt = ss.get_sharing_resolved_topologies()
            for a_, b_ in itertools.combinations(srt, 2):
                if pidof(a_) == pidof(b_): grp[gf(fid(a_))] = gf(fid(b_))
    groups_of = defaultdict(list)
    for rt in rts:
        if gf(fid(rt)) not in groups_of[pidof(rt)]: groups_of[pidof(rt)].append(gf(fid(rt)))
    lab = {}
    for rt in rts:
        gs = groups_of[pidof(rt)]
        lab[fid(rt)] = str(pidof(rt)) if len(gs) == 1 else f'{pidof(rt)}#{gs.index(gf(fid(rt))) + 1}'
    L = lambda rt: lab[rt.get_feature().get_feature_id().get_string()]
    node_of, nodes, subs, share = {}, [], [], Counter()
    def node(p):
        x = np.array(p.to_xyz()); key = tuple(np.round(x, 9))
        for dk in [(0, 0, 0)]:
            if key in node_of: return node_of[key]
        for j, y in enumerate(nodes):
            if np.linalg.norm(x - y) < SNAP: node_of[key] = j; return j
        node_of[key] = len(nodes); nodes.append(x); return node_of[key]
    nets = []
    pygplates.resolve_topologies(topo, rot, nets, float(t), resolve_topology_types=pygplates.ResolveTopologyType.network)
    other = Counter()
    def across(g, P):
        # the cell on the far side of a sub-segment used by plate P alone: a plate whose polygon lies there (boundary not shared
        # as one feature), else the deforming network covering that point (its gap cell), else 'gap'
        arc = max(g.get_segments(), key=lambda a: a.get_arc_length())
        if arc.is_zero_length(): return None
        a, b = np.array(arc.get_start_point().to_xyz()), np.array(arc.get_end_point().to_xyz())
        mid = (a + b) / np.linalg.norm(a + b); nrm = np.array(arc.get_great_circle_normal().to_xyz())
        for sgn in (1, -1):
            q = mid + sgn * 2e-4 * nrm; q = pygplates.PointOnSphere(*(q / np.linalg.norm(q)))
            if P.get_resolved_boundary().is_point_in_polygon(q): continue
            for rt in rts:
                if rt is not P and rt.get_resolved_boundary().is_point_in_polygon(q): other['plate'] += 1; return L(rt)
            for nt in nets:
                if nt.get_resolved_boundary().is_point_in_polygon(q):
                    other['network'] += 1; f = nt.get_feature(); netname[f'N:{f.get_feature_id().get_string()}'] = f.get_name(); return f'N:{f.get_feature_id().get_string()}'
            other['gap'] += 1; return 'gap'
        return None
    netname = {}; skipped = Counter()
    raw = []                                  # (points as unit vectors, sharing topologies)
    for sb in sbs:
        for ss in sb.get_shared_sub_segments():
            srt = ss.get_sharing_resolved_topologies()
            share[len(srt)] += 1
            g = ss.get_resolved_geometry()
            if g is None: skipped['no geometry'] += 1; continue
            P = np.array([p.to_xyz() for p in g.get_points()])
            if len(P) < 2: skipped['one point'] += 1; continue
            raw.append((P, srt))
    # NODING: a sub-segment end lying inside another sub-segment (a T-junction: the boundary of one polygon ends on the side of
    # another without being shared as one feature) splits that sub-segment there
    ends = np.array([P[k] for P, _ in raw for k in (0, -1)])
    pieces, tsplits = [], 0
    for P, srt in raw:
        cuts = []                                         # (arc index, fraction along, point)
        A, B = P[:-1], P[1:]
        n = np.cross(A, B); nn = np.linalg.norm(n, axis=1); ok = nn > 1e-12
        n[ok] /= nn[ok][:, None]
        d = np.abs(ends @ n.T)                            # distance of each end from each arc's great circle
        for e, k in zip(*np.nonzero((d < SNAP) & ok[None, :])):
            x = ends[e]
            if min(np.linalg.norm(x - P[0]), np.linalg.norm(x - P[-1])) < SNAP: continue
            if np.dot(np.cross(A[k], x), n[k]) > 0 and np.dot(np.cross(x, B[k]), n[k]) > 0 and np.linalg.norm(x - A[k]) > 1e-9:
                cuts.append((k, float(np.dot(x - A[k], B[k] - A[k])), tuple(np.round(x, 12))))
        cuts = sorted(set(cuts)); tsplits += len(cuts)
        cur, last = [P[0]], 0
        for k, _, x in cuts:
            cur += [P[q] for q in range(last + 1, k + 1)] + [np.array(x)]; pieces.append((np.array(cur), srt)); cur, last = [np.array(x)], k
        cur += [P[q] for q in range(last + 1, len(P))]; pieces.append((np.array(cur), srt))
    seen2 = {}
    for P, srt in pieces:
        plates = frozenset(L(rt) for rt in srt)
        if len(srt) == 1:
            g = pygplates.PolylineOnSphere([pygplates.PointOnSphere(*(p / np.linalg.norm(p))) for p in P]) if len(P) > 1 else None
            o = across(g, srt[0]) if g is not None else None
            if o is None: skipped['far side not found'] += 1; continue
            plates = frozenset((L(srt[0]), o))
        if len(plates) != 2: skipped[f'shared by {len(plates)}'] += 1
        a, b = node(pygplates.PointOnSphere(*(P[0] / np.linalg.norm(P[0])))), node(pygplates.PointOnSphere(*(P[-1] / np.linalg.norm(P[-1]))))
        ln = sum(np.arccos(np.clip(np.sum(P[:-1] * P[1:], 1), -1, 1))) * 6371.0
        if a == b and ln < 2: skipped['zero-length piece'] += 1; continue
        key2 = (min(a, b), max(a, b), plates)
        if key2 in seen2 and abs(seen2[key2] - ln) < 0.1 * max(ln, 1) + 1: skipped['coincident duplicate'] += 1; continue
        seen2[key2] = ln
        subs.append((a, b, plates, ln))
    # deforming-zone cells = connected regions not covered by any rigid plate polygon (bounded by sub-segments whose far side is a
    # network or nothing); one cell per connected region, labelled Z: + the network covering most of its boundary (stated rule)
    gz = [i for i, (a, b, pl, _) in enumerate(subs) if any(c.startswith('N:') or c == 'gap' for c in pl)]
    up = {}
    def f(x):
        while up.setdefault(x, x) != x: up[x] = up[up[x]]; x = up[x]
        return x
    for i in gz: up[f(subs[i][0])] = f(subs[i][1])
    comp = defaultdict(list)
    for i in gz: comp[f(subs[i][0])].append(i)
    zl, used_names = {}, Counter()
    for r, idx in sorted(comp.items(), key=lambda kv: -len(kv[1])):
        dom = Counter(c for i in idx for c in subs[i][2] if c.startswith('N:') or c == 'gap').most_common(1)[0][0]
        used_names[dom] += 1; lab_ = 'Z:' + dom[2:] if dom != 'gap' else 'Z:gap'
        if used_names[dom] > 1: lab_ += f'#{used_names[dom]}'
        netname[lab_] = netname.get(dom, 'uncovered gap'); zl[r] = lab_
        for i in idx:
            a, b, pl, ln = subs[i]
            subs[i] = (a, b, frozenset(zl[r] if (c.startswith('N:') or c == 'gap') else c for c in pl), ln)
    for k in [k for k in netname if k.startswith('N:')]: del netname[k]
    inc = defaultdict(list)
    for i, (a, b, pl, _) in enumerate(subs): inc[a].append(i); inc[b].append(i)
    nplates = {n: frozenset().union(*[subs[i][2] for i in inc[n]]) for n in inc}
    isj = {n: len(nplates[n]) >= 3 for n in inc}
    # chains between junctions
    used, segments, loops, lengths, chain_ends = set(), [], 0, [], []
    for i, (a, b, pl, ln) in enumerate(subs):
        if i in used or len(pl) != 2: continue
        chain, ends = [i], []
        used.add(i)
        for start in (a, b):
            n, prev = start, i
            while not isj[n]:
                nxt = [j for j in inc[n] if j != prev and j not in used and subs[j][2] == pl]
                if not nxt: break
                j = nxt[0]; used.add(j); chain.append(j); prev = j
                n = subs[j][1] if subs[j][0] == n else subs[j][0]
                if n == start: break
            ends.append(n)
        closed = not isj[ends[0]] and not isj[ends[1]]
        if closed: loops += 1
        segments.append(tuple(sorted(pl))); chain_ends.append(tuple(ends)); lengths.append(sum(subs[j][3] for j in chain))
    junctions = [tuple(sorted(nplates[n])) for n in inc if isj[n]]
    cyc = {}
    for c in set(x for pl in segments for x in pl):
        upc = {}
        def fc(x):
            while upc.setdefault(x, x) != x: upc[x] = upc[upc[x]]; x = upc[x]
            return x
        for (e0, e1), pl in zip(chain_ends, segments):
            if c in pl: upc[fc(('n', e0))] = fc(('n', e1))
        cyc[c] = len({fc(x) for x in list(upc)})
    jdeg = Counter(len(inc[n]) for n in inc if isj[n])
    cells = sorted(set(L(rt) for rt in rts) | {c for _, _, pl, _ in subs for c in pl})
    names = {L(rt): rt.get_feature().get_name() for rt in rts}; names.update(netname)
    info = dict(time=t, plates=len(cells), polygons=len(rts), subsegments=len(subs), t_splits=tsplits, sharing=dict(share), junction_node_degrees=dict(jdeg),
                odd_subsegments=sum(v for k, v in share.items() if k != 2), far_side_of_unshared=dict(other), skipped=dict(skipped), cycles_per_cell=dict(Counter(cyc.values())), multi_cycle_cells={c: k for c, k in cyc.items() if k != 1}, deforming_cells=len(netname), boundary_length_km=round(sum(lengths)))
    T = Tiling(cells, segments, junctions, 2, 'sphere', t, loops=loops)
    T._debug = (subs, nodes, nplates, inc)
    return T, rts, L, names, info

def fib_points(n=40000):
    i = np.arange(n) + 0.5; z = 1 - 2 * i / n; r = np.sqrt(1 - z * z); th = math.pi * (1 + 5 ** .5) * i
    return [pygplates.PointOnSphere(float(a), float(b), float(c)) for a, b, c in zip(r * np.cos(th), r * np.sin(th), z)]

def partition(rot, rts, L, pts, t):
    pp = pygplates.PlatePartitioner(rts, rot)
    out = []
    for p in pts:
        r = pp.partition_point(p); out.append(L(r) if r is not None else None)
    return out

def lineage(rot, topo, A, B, pts):
    """parents of B's newborn plates (traced back to A's time) and heirs of A's vanished plates (traced forward)."""
    born, died = B.cells - A.cells, A.cells - B.cells
    if not born and not died: return {}, {}
    _, rA, LA, _, _ = resolve(rot, topo, A.t); _, rB, LB, _, _ = resolve(rot, topo, B.t)
    pid = lambda lab: int(lab.split('#')[0])
    par, her = {}, {}
    if born:
        own = partition(rot, rB, LB, pts, B.t)
        for x in born:
            mine = [p for p, o in zip(pts, own) if o == x]
            if not mine: continue
            R = rot.get_rotation(float(A.t), pid(x), float(B.t))
            back = partition(rot, rA, LA, [R * p for p in mine], A.t)
            c = Counter(back); par[x] = {k: v / len(mine) for k, v in c.items() if k is not None}
    if died:
        own = partition(rot, rA, LA, pts, A.t)
        for y in died:
            mine = [p for p, o in zip(pts, own) if o == y]
            if not mine: continue
            R = rot.get_rotation(float(B.t), pid(y), float(A.t))
            fwd = partition(rot, rB, LB, [R * p for p in mine], B.t)
            c = Counter(fwd); her[y] = {k: v / len(mine) for k, v in c.items() if k is not None}
    return par, her

if __name__ == '__main__':
    mode, model = sys.argv[1], sys.argv[2]
    rot, topo, m = load(model)
    if mode == 'present':
        T, rts, L, names, info = resolve(rot, topo, 0)
        chk = check_tiling(T)
        nbr = Counter(len(T.nb[c]) for c in T.cells)
        out = dict(model=model, info=info, check=chk, mean_neighbours=2 * len(T.pairs) / len(T.cells),
                   mean_boundaries_per_plate=2 * len(T.segments) / len(T.cells), neighbour_numbers=dict(sorted(nbr.items())),
                   nonTriple=[[names.get(c, c) for c in j] for j in T.junctions if len(j) != 3], frame=json.loads(T.to_json()),
                   names=names)
        print(json.dumps({k: out[k] for k in ('info', 'check', 'mean_neighbours', 'mean_boundaries_per_plate', 'neighbour_numbers', 'nonTriple')}, indent=1, default=str))
        json.dump(out, open(f'plates_present_{model}.json', 'w'), indent=1, default=str)
        print('FINAL ok' if chk.get('euler_ok') else 'FINAL FAIL Euler', flush=True)
    else:
        step, tmax = int(sys.argv[3]), int(sys.argv[4])
        times = list(range(tmax, -1, -step))
        if times[-1] != 0: times.append(0)
        frames, infos = [], []
        for i, t in enumerate(times):
            T, rts, L, names, info = resolve(rot, topo, t); frames.append(T); infos.append(info)
            if i % 10 == 0: print(f'PROGRESS {0.6 * i / len(times):.3f} resolve {t} Ma: {info["plates"]} plates', flush=True)
        pts = fib_points()
        for i, (A, B) in enumerate(zip(frames, frames[1:])):
            p, h = lineage(rot, topo, A, B, pts); B.parents.update(p); A.heirs.update(h)
            if i % 10 == 0: print(f'PROGRESS {0.6 + 0.4 * i / len(times):.3f} lineage {A.t}->{B.t} Ma', flush=True)
        rows, summ = run(frames)
        with open(f'plates_series_{model}_{step}_frames.jsonl', 'w') as f:
            for T in frames: f.write(T.to_json() + '\n')
        json.dump(rows, open(f'plates_series_{model}_{step}_events.json', 'w'), indent=1)
        per100 = defaultdict(Counter)
        for r in rows: per100[f'{int((r["t0"] - 1e-9) // 100) * 100}-{int((r["t0"] - 1e-9) // 100) * 100 + 100} Ma'][r['type']] += 1
        i = next((i for i, r in enumerate(rows) if r['net'] != 0), None); neg = None
        if i is not None:
            bad = [dict(r) for r in rows]; bad[i]['type'] = 'swap'; neg = len(rebalance_log(frames, bad)) == 1
        out = dict(model=model, step=step, times=[times[0], times[-1]], plates_by_time={T.t: len(T.cells) for T in frames}, summary=summ,
                   per100={k: dict(v) for k, v in sorted(per100.items())}, neg_control_caught=neg,
                   euler_fail_times=[c['t'] for c in summ['frames_failing']], infos=infos)
        json.dump(out, open(f'plates_series_{model}_{step}.json', 'w'), indent=1, default=str)
        print(json.dumps({k: out[k] for k in ('summary', 'per100', 'neg_control_caught')}, indent=1, default=str)[:4000], flush=True)
        print('FINAL ok' if summ['n_balance_failures'] == 0 and neg else 'FINAL FAIL balance or control', flush=True)
