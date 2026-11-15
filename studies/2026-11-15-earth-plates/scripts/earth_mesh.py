"""Earth's plates as a tiling sequence on a fixed fine mesh (One tissue, three scales, Section 1; DICTO 15 Nov 2026).
Replaces the boundary-noding step of ../../2026-11-15-event-logger/scripts/plates.py, whose frames failed where model polygons overlap,
leave slivers or repeat a boundary. Software, credited where used: pyGPlates (GPlates project, GPL-2.0; Müller et al. 2018, G-cubed 19,
2243-2261) resolves the plate polygons and its PlatePartitioner assigns points to them; GPlately's PlateModelManager (Mather et al. 2024,
Geoscience Data Journal 11, 3-10; GPL-2.0) downloads the models; SciPy (cKDTree, connected_components). We call their code; none is copied.

RULES (stated before counting; 15 Nov 2026):
  R1 mesh: an icosphere of LEVEL subdivisions (level 9: 2 621 442 points, spacing about 14 km). Each mesh point gets the polygon that
     the GPlates partitioner puts it in (where polygons overlap, the partitioner's own order decides: deforming networks first, then
     rigid plates). The map is the labelled mesh: a cell = a connected set of points with one label; a junction = a mesh triangle
     whose three corners carry three labels; a boundary = a chain of two-label triangles between junctions (a closed chain = loop).
     So all junctions are triple, and features narrower than the mesh spacing do not exist in the map (this is the sliver rule).
  R2 gaps (points in no polygon): rule A ('rigid') gives each such point to the nearest point of a rigid plate; rule B ('nets') first
     makes each deforming network one cell (label Z: + network) wherever it lies, as GPlates does (networks before rigid plates), then
     fills any remaining gap as in rule A; rule C ('gaps') keeps the rigid plates and makes cells of the networks only where no rigid
     plate lies (the uncovered zones, one cell per network piece), then fills what is left as in rule A. Models without deforming
     networks give the same map under A and B. The gap and overlap areas are reported for every frame.
  R3 label = reconstruction plate ID; pieces of one label that do not touch get #1, #2 ... by size. A piece that is not the largest of
     its label and has under SLIVER_KM2 of area joins the neighbouring label it shares most mesh edges with (repeated until none left).
  R4 minimum boundary length Lmin: boundaries shorter than Lmin (measured between centroids of the mesh triangles along the chain) are
     contracted to a point, shortest first, so their two junctions become one meeting of four or more cells (a contraction that would
     leave a meeting of only three cells, i.e. close a two-sided lens, is skipped); a contact made only of
     such boundaries does not count. Lmin = 0 keeps the full map.
  R5 lineage (split vs birth, merge vs death): the mesh points of a new cell are rotated back with its own plate rotation to the earlier
     frame and looked up there (parents); a vanished cell's points are rotated forward (heirs). At most 5000 points per cell.
Usage: python earth_mesh.py present MODEL RULE LEVEL                 -> present_MODEL_RULE_LLEVEL.json
       python earth_mesh.py series MODEL RULE LEVEL TMAX NPROC OUTDIR [TMIN] -> OUTDIR/MODEL_RULE.json (+ frames_*.jsonl)"""
import sys, os, json, math, time, shutil
from collections import Counter, defaultdict
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import pygplates
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-15-event-logger', 'scripts')); sys.path.insert(0, HERE)
from eventlog import Tiling, run, rebalance_log, check_tiling
from swaps import swap_list, persistent

R_KM = 6371.0
SLIVER_KM2 = 5000.0
LMINS = (0, 50, 150)
STEPS = (1, 2, 5, 10)
KS = (1, 2, 5)
LFILT = (0, 50, 150)

def icosphere(level):
    t = (1 + 5 ** .5) / 2
    V = np.array([[-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0], [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t], [t, 0, -1], [t, 0, 1],
                  [-t, 0, -1], [-t, 0, 1]], float)
    F = np.array([[0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11], [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
                  [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9], [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]], np.int64)
    V /= np.linalg.norm(V, axis=1)[:, None]
    for _ in range(level):
        nf, nv = len(F), len(V)
        E = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); E.sort(axis=1)
        u, inv = np.unique(E[:, 0] * nv + E[:, 1], return_inverse=True)
        a, b = u // nv, u % nv
        M = V[a] + V[b]; M /= np.linalg.norm(M, axis=1)[:, None]
        m = inv + nv; m01, m12, m20 = m[:nf], m[nf:2 * nf], m[2 * nf:]
        F = np.concatenate([np.c_[F[:, 0], m01, m20], np.c_[F[:, 1], m12, m01], np.c_[F[:, 2], m20, m12], np.c_[m01, m12, m20]])
        V = np.vstack([V, M])
    return V, F

class Mesh:
    def __init__(self, level):
        self.V, F = icosphere(level); nv = len(self.V); self.F = F.astype(np.int32); nf = len(F)
        E = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); E.sort(axis=1)
        key = E[:, 0] * nv + E[:, 1]; face = np.tile(np.arange(nf), 3)
        o = np.argsort(key, kind='stable'); key, face, E = key[o], face[o], E[o]
        assert np.all(key[0::2] == key[1::2]), 'every mesh edge must have two triangles'
        self.E = E[0::2].astype(np.int32); self.EF = np.c_[face[0::2], face[1::2]].astype(np.int32)
        C = self.V[F].sum(1); C /= np.linalg.norm(C, axis=1)[:, None]
        self.DL = np.arccos(np.clip(np.sum(C[self.EF[:, 0]] * C[self.EF[:, 1]], 1), -1, 1)) * R_KM
        self.tree = cKDTree(self.V); self.vertex_km2 = 4 * math.pi * R_KM ** 2 / nv
        self.spacing_km = float(np.mean(np.linalg.norm(self.V[self.E[:, 0]] - self.V[self.E[:, 1]], axis=1)) * R_KM)
        self.MP = pygplates.MultiPointOnSphere([tuple(p) for p in self.V])

def load(model, data_dir=os.path.expanduser('~/plate-models')):
    from plate_model_manager import PlateModelManager
    m = PlateModelManager().get_model(model, data_dir=data_dir)
    rot = pygplates.RotationModel(m.get_rotation_model())
    topo = [pygplates.FeatureCollection(f) for f in m.get_topologies()]
    return rot, topo

def xyz(g):
    try: return np.asarray(g.to_xyz_array())
    except Exception: return np.array([p.to_xyz() for p in g.get_points()])

def label_mesh(mesh, rot, topo, t, rule):
    """Per-vertex labels (strings via names list) after rules R1-R3, plus frame information."""
    rts, nets = [], []
    pygplates.resolve_topologies(topo, rot, rts, float(t), resolve_topology_types=pygplates.ResolveTopologyType.boundary)
    pygplates.resolve_topologies(topo, rot, nets, float(t), resolve_topology_types=pygplates.ResolveTopologyType.network)
    nv = len(mesh.V); keys, kidx, pidof = [], {}, {}
    def key_of(rt, is_net):
        f = rt.get_feature(); pid = f.get_reconstruction_plate_id()
        k = ('Z:' + f.get_feature_id().get_string()[-8:]) if is_net else str(pid)
        if k not in kidx: kidx[k] = len(keys); keys.append(k); pidof[k] = pid
        return kidx[k]
    def assign(polys, is_net, lab, overwrite):
        if not polys: return
        pp = pygplates.PlatePartitioner(polys, rot); inside = []
        pp.partition_geometry(mesh.MP, inside)
        for rt, geoms in inside:
            k = key_of(rt, is_net)
            for g in geoms:
                idx = mesh.tree.query(xyz(g))[1]
                lab[idx if overwrite else idx[lab[idx] < 0]] = k
    rigid = np.full(nv, -1, np.int32); assign(rts, False, rigid, True)
    gap_rigid = float(np.mean(rigid < 0))
    area_rigid = sum(rt.get_resolved_boundary().get_area() for rt in rts) / (4 * math.pi)
    area_nets = sum(n.get_resolved_boundary().get_area() for n in nets) / (4 * math.pi)
    lab = rigid.copy()
    if rule in ('nets', 'gaps') and nets:
        netlab = np.full(nv, -1, np.int32); assign(nets, True, netlab, True)
        put = (netlab >= 0) if rule == 'nets' else (netlab >= 0) & (lab < 0)
        lab[put] = netlab[put]
    gap = float(np.mean(lab < 0))
    if gap > 0:
        have = np.nonzero(lab >= 0)[0]; miss = np.nonzero(lab < 0)[0]
        lab[miss] = lab[have[cKDTree(mesh.V[have]).query(mesh.V[miss])[1]]]
    info = dict(time=t, polygons=len(rts), networks=len(nets), gap_rigid_frac=round(gap_rigid, 5), gap_after_rule_frac=round(gap, 5),
                overlap_rigid_frac=round(area_rigid - (1 - gap_rigid), 5), network_area_frac=round(area_nets, 5))
    # R3: pieces and slivers
    E0, E1 = mesh.E[:, 0], mesh.E[:, 1]; nmin = SLIVER_KM2 / mesh.vertex_km2; merged = 0
    for it in range(20):
        same = lab[E0] == lab[E1]
        comp = connected_components(coo_matrix((np.ones(same.sum(), np.int8), (E0[same], E1[same])), shape=(nv, nv)), directed=False)[1]
        size = np.bincount(comp); clab = np.zeros(len(size), np.int32); clab[comp] = lab
        big = {}
        for c in np.argsort(-size):
            big.setdefault(clab[c], c)
        isbig = np.zeros(len(size), bool); isbig[list(big.values())] = True
        sl = (~isbig) & (size < nmin)
        if not sl.any(): break
        d = ~same; cu, cv = comp[E0[d]], comp[E1[d]]; lu, lv = lab[E0[d]], lab[E1[d]]
        cc = np.concatenate([cu, cv]); ll = np.concatenate([lv, lu]); m = sl[cc]
        cnt = Counter(zip(cc[m].tolist(), ll[m].tolist())); best = {}
        for (c, l), n in cnt.items():
            if n > best.get(c, (0, -1))[0]: best[c] = (n, l)
        newl = clab.copy()
        for c, (n, l) in best.items(): newl[c] = l
        lab = newl[comp]; merged += len(best)
    info['sliver_pieces_merged'] = merged
    lost_labels = sorted(set(keys) - {keys[i] for i in np.unique(lab)})
    info['labels_below_resolution'] = lost_labels
    # cell names
    order = np.argsort(-size); names, cname = [], {}
    per = Counter(clab[c] for c in range(len(size)))
    rank = Counter()
    for c in order:
        k = keys[clab[c]]; rank[k] += 1
        cname[c] = k if per[clab[c]] == 1 else f'{k}#{rank[k]}'
    uc = np.unique(comp); cidx = {c: i for i, c in enumerate(uc)}
    names = [cname[c] for c in uc]
    cell = np.searchsorted(uc, comp).astype(np.int32)
    pids = {n: pidof[n.split('#')[0]] for n in names}
    return cell, names, pids, info

def extract(mesh, cell, names, lmins=LMINS):
    """Map of the labelled mesh: {Lmin: Tiling}, plus chain statistics."""
    F, E, EF = mesh.F, mesh.E, mesh.EF
    fc = cell[F]; nd = (fc[:, 0] != fc[:, 1]).astype(int) + (fc[:, 1] != fc[:, 2]) + (fc[:, 0] != fc[:, 2])
    isJ = nd == 3
    b = cell[E[:, 0]] != cell[E[:, 1]]
    de, dl = EF[b], mesh.DL[b]; pa = np.sort(np.c_[cell[E[b, 0]], cell[E[b, 1]]], axis=1)
    jA, jB = isJ[de[:, 0]], isJ[de[:, 1]]
    nf = len(F)
    inter = ~jA & ~jB
    g = coo_matrix((np.ones(inter.sum(), np.int8), (de[inter, 0], de[inter, 1])), shape=(nf, nf))
    fcomp = connected_components(g, directed=False)[1]
    # chain ids: components of non-junction boundary faces, then direct junction-junction edges
    bf = np.unique(de[~jA | ~jB].ravel()); bf = bf[~isJ[bf]]
    ck = np.unique(fcomp[bf]); cid = -np.ones(fcomp.max() + 1, np.int64); cid[ck] = np.arange(len(ck))
    nchain = len(ck)
    length = np.zeros(nchain); pair = np.zeros((nchain, 2), np.int64); ends = [[] for _ in range(nchain)]
    ii = cid[fcomp[de[inter, 0]]]; np.add.at(length, ii, dl[inter]); pair[ii] = pa[inter]
    half = jA ^ jB
    for (f0, f1), L, p, a in zip(de[half], dl[half], pa[half], jA[half]):
        jf, of = (f0, f1) if a else (f1, f0)
        c = cid[fcomp[of]]; length[c] += L; pair[c] = p; ends[c].append(int(jf))
    both = jA & jB
    for (f0, f1), L, p in zip(de[both], dl[both], pa[both]):
        length = np.append(length, L); pair = np.vstack([pair, p]); ends.append([int(f0), int(f1)])
    loops = [i for i, e in enumerate(ends) if len(e) == 0]
    assert all(len(e) in (0, 2) for e in ends), 'a boundary chain must have 0 or 2 ends'
    jf = np.nonzero(isJ)[0]; jid = {f: i for i, f in enumerate(jf)}
    up = list(range(len(jf)))
    def find(x):
        while up[x] != x: up[x] = up[up[x]]; x = up[x]
        return x
    for e in ends:
        if e: up[find(jid[e[0]])] = find(jid[e[1]])
    components = len({find(i) for i in range(len(jf))}) + len(loops)
    out = {}
    nm = np.array(names, dtype=object)
    for L in lmins:
        upL = list(range(len(jf)))
        def fl(x):
            while upL[x] != x: upL[x] = upL[upL[x]]; x = upL[x]
            return x
        keep = np.ones(len(ends), bool)
        gcells = {jid[f]: set(fc[f].tolist()) for f in jf}
        for i in np.argsort(length):
            if length[i] >= L: break
            if not ends[i]: continue
            u, v = fl(jid[ends[i][0]]), fl(jid[ends[i][1]])
            if u != v and len(gcells[u] | gcells[v]) > 3:          # never contract to a meeting of only three cells (a lens)
                upL[u] = v; keep[i] = False; gcells[v] |= gcells[u]
        groups = defaultdict(set)
        for f in jf: groups[fl(jid[f])].update(nm[fc[f]].tolist())
        segs = [tuple(nm[pair[i]].tolist()) for i in range(len(ends)) if keep[i]]
        out[L] = Tiling(names, segs, [tuple(sorted(s)) for s in groups.values()], 2, 'sphere', None, loops=len(loops), components=components)
    plen = defaultdict(list)
    for i in range(len(ends)): plen['|'.join(sorted(nm[pair[i]].tolist()))].append(round(float(length[i]), 1))
    stats = dict(chains=len(ends), loops=len(loops), components=components, shortest_km=round(float(length.min()), 1) if len(length) else None,
                 chains_under={L: int(np.sum(length < L)) for L in lmins if L}, boundary_km=round(float(length.sum())))
    return out, stats, dict(plen)

def rot_matrix(R):
    """3x3 matrix of a pyGPlates FiniteRotation, from the images of the three axes."""
    return np.array([(R * pygplates.PointOnSphere(*e)).to_xyz() for e in np.eye(3)]).T

# ---- workers (fork: the mesh and the model are inherited from the parent) ----
G = {}
def frame_job(t):
    mesh, rot, topo, rule, work = G['mesh'], G['rot'], G['topo'], G['rule'], G['work']
    t0 = time.time()
    cell, names, pids, info = label_mesh(mesh, rot, topo, t, rule)
    maps, stats, plen = extract(mesh, cell, names)
    np.savez_compressed(os.path.join(work, f'{t}.npz'), cell=cell.astype(np.uint16 if len(names) < 65000 else np.int32))
    info.update(stats); info['cells'] = len(names); info['seconds'] = round(time.time() - t0, 1)
    for L, T in maps.items(): T.t = t
    fj = {L: T.to_json() for L, T in maps.items()}
    d = json.loads(fj[0]); d['lengths'] = plen; fj[0] = json.dumps(d)
    return t, fj, names, pids, info

def lineage_job(args):
    tA, tB = args                                        # tA older (larger age)
    mesh, rot, work, meta = G['mesh'], G['rot'], G['work'], G['meta']
    nA, nB = meta[tA]['names'], meta[tB]['names']
    born, died = set(nB) - set(nA), set(nA) - set(nB)
    par, her = {}, {}
    if not born and not died: return (tA, tB), par, her
    cA = np.load(os.path.join(work, f'{tA}.npz'))['cell']; cB = np.load(os.path.join(work, f'{tB}.npz'))['cell']
    def trace(cfrom, nfrom, x, tfrom, tto, cto, nto, pid):
        v = np.nonzero(cfrom == nfrom.index(x))[0]
        if len(v) == 0: return {}
        v = v[np.linspace(0, len(v) - 1, min(5000, len(v))).astype(int)]
        M = rot_matrix(rot.get_rotation(float(tto), int(pid), float(tfrom)))
        idx = mesh.tree.query(mesh.V[v] @ M.T)[1]
        c = Counter(nto[i] for i in cto[idx]); n = sum(c.values())
        return {k: round(m / n, 4) for k, m in c.items()}
    for x in born: par[x] = trace(cB, nB, x, tB, tA, cA, nA, meta[tB]['pids'][x])
    for y in died: her[y] = trace(cA, nA, y, tA, tB, cB, nB, meta[tA]['pids'][y])
    return (tA, tB), par, her

def census(frames_json, lin, times, step, L, by_segment=True):
    fr = [Tiling.from_json(frames_json[t][L]) for t in times]
    for A, B in zip(fr, fr[1:]):
        p, h = lin.get((A.t, B.t), ({}, {}))
        B.parents = dict(p); A.heirs = dict(h)
    rows, summ = run(fr, by_segment=by_segment)
    sw = swap_list(fr, rows)
    i = next((i for i, r in enumerate(rows) if r['net'] != 0), None); neg = None
    if i is not None:
        bad = [dict(r) for r in rows]; bad[i]['type'] = 'swap'; neg = len(rebalance_log(fr, bad)) >= 1
    per100 = defaultdict(Counter)
    for r in rows: per100[int((r['t0'] - 1e-9) // 100) * 100][r['type']] += 1
    pers = {k: persistent(fr, sw, k) for k in KS}
    lens = None
    if L == 0:
        lens = [{tuple(p.split('|')): v for p, v in json.loads(frames_json[t][0]).get('lengths', {}).items()} for t in times]
    lf = {f'k{k}_l{lm}': persistent(fr, sw, k, lm, lens)[0] for k in KS for lm in LFILT} if lens else None
    return dict(step=step, Lmin=L, by_segment=by_segment, frames=len(fr), counts=summ['counts'], clump_patterns=summ['clump_patterns'],
                frames_failing=summ['n_frames_failing'], failing_detail=summ['frames_failing'][:5], balance_failures=summ['n_balance_failures'],
                neg_control_caught=neg, swaps_direct=sum(s['via'] == 'direct' for s in sw), swaps_fourfold=sum(s['via'] == 'four-fold' for s in sw),
                swaps_persistent={k: v[0] for k, v in pers.items()}, swaps_persistent_lengthfilter=lf, swaps_persistent_censored={k: v[1] for k, v in pers.items()},
                per100={f'{k}-{k + 100} Ma': dict(v) for k, v in sorted(per100.items())},
                swap_times=[[fr[s['iA']].t, fr[s['iB']].t, s['via']] for s in sw]), rows

if __name__ == '__main__':
    mode, model, rule, level = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    t0 = time.time(); mesh = Mesh(level); rot, topo = load(model)
    print(f'mesh level {level}: {len(mesh.V)} points, spacing {mesh.spacing_km:.1f} km, built in {time.time() - t0:.0f} s', flush=True)
    if mode == 'present':
        tt = float(sys.argv[5]) if len(sys.argv) > 5 else 0
        cell, names, pids, info = label_mesh(mesh, rot, topo, tt, rule)
        maps, stats, _ = extract(mesh, cell, names)
        res = {}
        for L, T in maps.items():
            c = check_tiling(T)
            res[L] = dict(cells=len(T.cells), junctions=len(T.junctions), boundaries=len(T.segments), pairs=len(T.pairs), loops=T.loops,
                          components=T.components, euler=c.get('euler'), ok=c['ok'], triple=c.get('triple_formulas_ok'),
                          junction_degrees=c.get('junction_degrees'))
        out = dict(model=model, rule=rule, level=level, time=tt, spacing_km=mesh.spacing_km, info=info, stats=stats, maps=res, cells=names)
        print(json.dumps({k: out[k] for k in ('info', 'stats', 'maps')}, default=str), flush=True)
        json.dump(out, open(f'present_{model}_{rule}_L{level}_{int(tt)}.json', 'w'), indent=1, default=str)
        print('FINAL ok' if all(r['ok'] for r in res.values()) else 'FINAL FAIL check', flush=True)
        sys.exit(0)
    tmax, nproc, outdir = int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
    tmin = int(sys.argv[8]) if len(sys.argv) > 8 else 0            # youngest age (models such as Domeier & Torsvik 2014 end at 250 Ma)
    work = os.path.join(outdir, f'work_{model}_{rule}'); os.makedirs(work, exist_ok=True)
    G.update(mesh=mesh, rot=rot, topo=topo, rule=rule, work=work)
    import multiprocessing as mp
    times = list(range(tmax, tmin - 1, -1))
    frames_json, meta, infos = {}, {}, {}
    with mp.get_context('fork').Pool(nproc) as pool:
        for n, (t, fj, names, pids, info) in enumerate(pool.imap_unordered(frame_job, times)):
            frames_json[t] = fj; meta[t] = dict(names=names, pids=pids); infos[t] = info
            if n % 10 == 0: print(f'PROGRESS {0.7 * n / len(times):.3f} frames {n}/{len(times)} (t={t}: {info["cells"]} cells, {info["seconds"]} s)', flush=True)
    G['meta'] = meta
    def series_times(s):
        ts = list(range(tmax, tmin - 1, -s))
        return ts + [tmin] if ts[-1] != tmin else ts
    pairs = sorted({(a, b) for s in STEPS for a, b in zip(series_times(s), series_times(s)[1:])})
    lin = {}
    with mp.get_context('fork').Pool(nproc) as pool:
        for n, (k, p, h) in enumerate(pool.imap_unordered(lineage_job, pairs)):
            lin[k] = (p, h)
            if n % 50 == 0: print(f'PROGRESS {0.7 + 0.2 * n / len(pairs):.3f} lineage {n}/{len(pairs)}', flush=True)
    for L in LMINS:                                       # 1 Myr frames WITH lineage (parents from t+1, heirs to t-1), for recounts
        with open(os.path.join(outdir, f'frames_{model}_{rule}_L{L}.jsonl'), 'w') as f:
            for t in times:
                d = json.loads(frames_json[t][L])
                p = lin.get((t + 1, t), ({}, {}))[0]; h = lin.get((t, t - 1), ({}, {}))[1]
                if p: d['parents'] = p
                if h: d['heirs'] = h
                f.write(json.dumps(d) + '\n')
    results, n = [], 0
    for s in STEPS:
        ts = series_times(s)
        for L in LMINS:
            r, rows = census(frames_json, lin, ts, s, L)
            results.append(r); n += 1
            if s == 1: json.dump(rows, open(os.path.join(outdir, f'events_{model}_{rule}_L{L}.json'), 'w'), indent=0)
            print(f'PROGRESS {0.9 + 0.1 * n / (len(STEPS) * len(LMINS) + 1):.3f} census step {s} Lmin {L}: {r["counts"]} persistent {r["swaps_persistent"]}', flush=True)
    pair_rule, _ = census(frames_json, lin, times, 1, 0, by_segment=False)
    out = dict(model=model, rule=rule, level=level, spacing_km=mesh.spacing_km, tmax=tmax, plates_by_time={t: infos[t]['cells'] for t in times},
               census=results, pair_rule_step1_L0=pair_rule, infos=[infos[t] for t in times])
    json.dump(out, open(os.path.join(outdir, f'{model}_{rule}.json'), 'w'), indent=1, default=str)
    shutil.rmtree(work)
    ok = all(r['frames_failing'] == 0 and r['balance_failures'] == 0 and r['neg_control_caught'] for r in results)
    print(json.dumps([{k: r[k] for k in ('step', 'Lmin', 'counts', 'swaps_persistent', 'frames_failing', 'balance_failures', 'neg_control_caught')} for r in results], default=str), flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL frames, balance or control', flush=True)
