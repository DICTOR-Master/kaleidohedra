# check.py: verifies the exact-vs-dissection data files exactly, from the JSON alone (DICTO · dictospheres.com, 2026-10-23).
# For every solid: closed, outward wound, planar faces, convex, Euler; f-vector, faces, edges, symmetry, exact volume;
# the Kaleidohedra move replayed from its parameters gives exactly these corners; the lattice tiles space (volume = |det|,
# no lattice vector inside P - P, face neighbours are lattice vectors); congruence by corner matching with each classical
# construction, and the classical cut-and-glue pieces really glue into one convex solid. Then it corrupts copies of the
# data in six ways and requires every corrupted copy to fail. Run: python3 check.py   (exit code 0 = all good)
import copy, glob, itertools, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact import *

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
G = [V(Fr(1, 2), Fr(1, 2), Fr(1, 2)), V(Fr(1, 2), -Fr(1, 2), -Fr(1, 2)), V(-Fr(1, 2), Fr(1, 2), -Fr(1, 2)), V(-Fr(1, 2), -Fr(1, 2), Fr(1, 2))]
FCC_BASIS = [V(1, 1, 0), V(1, 0, 1), V(0, 1, 1)]


def replay(m):
    """The move's edge directions, from its parameters only (krp-core cellDirections, exact)."""
    A = [vparse(r) for r in m['A_rows_exact']]
    if m['lattice'] == 'cube':
        dirs = [tuple(A[i][j] for i in range(3)) for j in range(3)]
    else:
        Sg = [matvec(A, g) for g in G]
        w = circumcentre([sc(x, -1) for x in Sg])
        dirs = [add(x, sc(w, m['cell'])) for x in Sg]
    if m.get('fifth_exact'): dirs.append(vparse(m['fifth_exact']))
    return A, dirs


def same_line(a, b): return iszero(cross(a, b))


def verify(rec):
    out = []
    ok = lambda label, cond: out.append((label, bool(cond)))
    try:
        Vx = [vparse(v) for v in rec['vertices_exact']]; F = rec['faces']
        res, fv = checks(Vx, F)
        for k, v in res.items(): ok(f'solid: {k}', v)
        ok('f-vector as stored', list(fv) == rec['f_vector'])
        vol = volume(Vx, F)
        ok('volume as stored (exact)', to_str(vol) == rec['volume_exact'])
        ok('float vertices match exact', all(abs(float(a) - b) < 1e-12 for v, w in zip(Vx, rec['vertices_float']) for a, b in zip(v, w)))
        ok('face kinds as stored', face_census(Vx, F) == rec['face_kinds'])
        ok('edge lengths as stored', [to_str(x) for x in edge_lengths2(Vx, F)] == rec['edge_lengths_squared'])
        ok('symmetry as stored', group_name(symmetry(Vx))['name'] == rec['symmetry']['name'])
        A, dirs = replay(rec['move_exact'])
        Vz, Fz, _ = zonotope(dirs)
        ok('the move replayed gives exactly these corners', set(Vz) == set(Vx))
        stored = [vparse(d) for d in rec['edge_directions_exact']]
        ok('edge directions as stored', len(stored) == len(dirs) and all(any(same_line(a, b) and dot(a, a) == dot(b, b) for b in dirs) for a in stored))
        ok('volume = zonotope sum of |det| over direction triples', vol == zonotope_volume(dirs))
        L = [vparse(b) for b in rec['lattice_basis_exact']]
        T = tiling(Vx, F, L)
        for k in ('volume_equals_det', 'packing', 'face_neighbours_are_lattice_vectors', 'centrally_symmetric'): ok(f'tiling: {k}', T[k])
        if rec['move_exact']['lattice'] == 'FCC' and not rec['move_exact'].get('fifth_exact'):
            M = [matvec(A, f) for f in FCC_BASIS]
            ok('tiling lattice = the sheared FCC lattice A*FCC', all(all(x.is_int() for x in solve_coords(L, m)) for m in M) and all(all(x.is_int() for x in solve_coords(M, l)) for l in L))
        if rec['move_exact']['lattice'] == 'cube':
            ok('tiling lattice = the sheared cube lattice', all(all(x.is_int() for x in solve_coords(L, d)) for d in dirs) and all(all(x.is_int() for x in solve_coords(dirs, l)) for l in L))
        e = rec.get('expected', {})
        if 'f_vector' in e: ok(f"f-vector = published ({e['source']})", list(fv) == e['f_vector'])
        if 'face_kinds' in e: ok('faces = published', face_census(Vx, F) == e['face_kinds'])
        if 'volume_exact' in e: ok('volume = published exact value', to_str(vol) == e['volume_exact'])
        if 'targets_volume_float' in e: ok('volume = TARGETS.md value (6 figures)', abs(float(vol) - e['targets_volume_float']) < 6e-6)
        if 'symmetry' in e: ok('symmetry = published', group_name(symmetry(Vx))['name'] == e['symmetry'])
        for c in rec.get('classical_exact', []):
            lab = c['label']
            if 'pieces' in c:
                pcs = [[vparse(p) for p in P] for P in c['pieces']]
                d, W, _ = dissection([p for P in pcs for p in P], pcs)
                ok(f'classical glue holds: {lab}', d['glued_pieces_are_the_whole'])
                ok(f'congruent (corner matching) to: {lab}', congruent(Vx, W[0]) is not None)
            if 'zonotope' in c:
                ok(f'congruent (corner matching) to: {lab}', congruent(Vx, zonotope([vparse(g) for g in c['zonotope']])[0]) is not None)
            if 'points' in c:
                ok(f'congruent (corner matching) to: {lab}', congruent(Vx, hull([vparse(p) for p in c['points']])[0]) is not None)
            if 'identity_points' in c:
                ok(lab, set(zonotope([vparse(g) for g in c['identity_zonotope']])[0]) == {vparse(p) for p in c['identity_points']})
            if 'zone_deletion_generators' in c:
                gens = [vparse(g) for g in c['zone_deletion_generators']]
                ok(f'congruent (corner matching) to: {lab}', all(congruent(Vx, zonotope(list(sub_))[0]) is not None for sub_ in itertools.combinations(gens, c['keep'])))
    except Exception as ex:                       # a corrupted file may not even parse; that is a failure too
        out.append((f'exception: {type(ex).__name__}: {ex}', False))
    return out


def records():
    for path in sorted(glob.glob(os.path.join(DATA, '*.json'))):
        name = os.path.basename(path)
        if name == 'build-summary.json': continue
        d = json.load(open(path))
        if 'vertices_exact' in d: yield name, d
        for k, m in d.get('members', {}).items():
            if 'vertices_exact' in m: yield f'{name}:{k}', m
            elif k == 'dicto_free_lines':
                for part, e in m.items():
                    if 'solid' in e: yield f'{name}:free line {part}', e['solid']


def corruptions(rec):
    """Six deliberate corruptions; each must make verify() fail."""
    def c1(r): v = r['vertices_exact'][0]; v[0] = to_str(parse(v[0]) + Fr(1, 7))
    def c2(r): r['faces'][0] = r['faces'][0][::-1]
    def c3(r): r['lattice_basis_exact'][0] = vstr(sc(vparse(r['lattice_basis_exact'][0]), 2))
    def c4(r): a = r['move_exact']['A_rows_exact']; a[0][0] = to_str(parse(a[0][0]) + Fr(1, 5))
    def c5(r): r['volume_exact'] = to_str(parse(r['volume_exact']) + Fr(1, 1000))
    def c6(r):
        cl = r.get('classical_exact', [])
        for c in cl:
            if 'pieces' in c: p = c['pieces'][0][0]; p[0] = to_str(parse(p[0]) + Fr(1, 9)); return
            if 'zonotope' in c: g = c['zonotope'][0]; g[0] = to_str(parse(g[0]) + Fr(1, 9)); return
            if 'points' in c: p = c['points'][0]; p[0] = to_str(parse(p[0]) + Fr(1, 9)); return
            if 'zone_deletion_generators' in c: g = c['zone_deletion_generators'][0]; g[0] = to_str(parse(g[0]) + Fr(1, 9)); return
        r['face_kinds'] = dict(r['face_kinds'], extra=1)          # no classical construction: corrupt the face list instead
    return [('vertex moved by 1/7', c1), ('one face wound backwards', c2), ('lattice vector doubled', c3),
            ('shear matrix entry changed by 1/5', c4), ('stored volume changed by 1/1000', c5), ('classical construction point moved by 1/9', c6)]


def main():
    total = passed = 0; caught = tried = 0
    for name, rec in records():
        res = verify(rec)
        bad = [l for l, o in res if not o]
        total += len(res); passed += len(res) - len(bad)
        print(f'{name}: {len(res) - len(bad)} of {len(res)} checks pass')
        for l in bad: print('   FAIL', l)
        for label, f in corruptions(rec):
            r2 = copy.deepcopy(rec); f(r2)
            fails = [l for l, o in verify(r2) if not o]
            tried += 1; caught += bool(fails)
            print(f'   corrupted ({label}): {"caught, " + str(len(fails)) + " checks fail, e.g. " + fails[0] if fails else "NOT CAUGHT"}')
    # rule 7: the congruence test on a known counterexample, and the DICTO RD = affine image of Bilinski claim
    A6 = [V(x, 0, 0) for x in (0, 1, 4, 10, 12, 17)]; B6 = [V(x, 0, 0) for x in (0, 1, 8, 11, 13, 17)]
    dl = lambda S: sorted(float(dot(sub(a, b), sub(a, b))) for a, b in itertools.combinations(S, 2))
    extra = [('control: homometric point sets share sorted distance lists', dl(A6) == dl(B6)),
             ('control: corner matching rejects them (not congruent)', congruent(A6, B6) is None)]
    ed = json.load(open(os.path.join(DATA, 'elongated-dodecahedron-type.json')))
    bil = json.load(open(os.path.join(DATA, 'bilinski-dodecahedron.json')))
    Lm = [vparse(r) for r in ed['F1_is_an_affine_image_of_Bilinski']['linear_map_exact']]
    F1 = {vparse(v) for v in ed['members']['dicto_skewed_RD_F1']['vertices_exact']}
    extra.append(('DICTO skewed RD (F1) = L(Bilinski B) for the stored linear map L', {matvec(Lm, vparse(v)) for v in bil['vertices_exact']} == F1))
    for l, o in extra:
        total += 1; passed += o; print(f'{"OK  " if o else "FAIL"} {l}')
    print(f'\nTOTAL: {passed} of {total} checks pass; corrupted copies caught: {caught} of {tried}')
    sys.exit(0 if passed == total and caught == tried else 1)


if __name__ == '__main__':
    main()
