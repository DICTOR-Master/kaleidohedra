# Exact vs cut-and-glue: builds each classical space-filler by a Kaleidohedra lattice move, exactly, beside its classical
# construction, and writes one JSON per shape to data/. DICTO's idea (2026-10-22); exact computation with Claude (Anthropic).
# DICTO · dictospheres.com
#
# The moves (krp-core e5e5dbc, src/geometry-extensions/kaleido-lattice.js; Fedorov 1885, Thm 32 p. 239 and § 83 p. 234):
#   shear   a linear map A of the FCC lattice (the app keeps only its rotation-free part S, with S^T S = A^T A, so the
#           app's solid is a rotated copy of the one built here from A); the six sliders a, b, c, alpha, beta, gamma are
#           the lengths (over sqrt 2) and angles of A(1,1,0), A(1,0,1), A(0,1,1).
#   Cell    t = 1: the four RD directions A g_i, each shifted by w = circumcentre of the -A g_i (the equal-edge cell).
#   stretch the fifth direction: the Minkowski sum with a segment s*u along a free direction u (Delone; #49).
import json, os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact import *

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data'); os.makedirs(DATA, exist_ok=True)
MARK = 'DICTO · dictospheres.com'
CREDIT = "DICTO's idea; exact computation with Claude (Anthropic)"
FEDOROV = 'Fedorov 1885: shear and stretch, Theorem 32 p. 239; zone shrinking, § 83 p. 234 (credited for the moves)'
h_ = Fr(1, 2)
G = [V(h_, h_, h_), V(h_, -h_, -h_), V(-h_, h_, -h_), V(-h_, -h_, h_)]      # RD_DIRECTIONS (krp-core), sum 0
FCC_BASIS = [V(1, 1, 0), V(1, 0, 1), V(0, 1, 1)]                          # = g1-g4, g1-g3, g1-g2
assert FCC_BASIS == [sub(G[0], G[3]), sub(G[0], G[2]), sub(G[0], G[1])]


def cell_dirs(A, t):
    """krp-core cellDirections, exact, with A in place of S (same cell up to a rotation)."""
    Sg = [matvec(A, g) for g in G]
    w = circumcentre([sc(x, -1) for x in Sg])
    return [add(x, sc(w, t)) for x in Sg], w


def lattice_params(A, scale2=1):
    """The six slider values of the lattice A*FCC: a^2, b^2, c^2 (over FCC's length sqrt 2), cos^2 and sign of alpha,
    beta, gamma, exact; plus floats in degrees. scale2 multiplies all lengths squared (uniform scale)."""
    u, v, w = [matvec(A, f) for f in FCC_BASIS]
    L2 = lambda x: dot(x, x) * scale2 / 2
    def ang(x, y):
        c2, s = corner_cos2(x, y); import math
        return {'cos2': to_str(c2), 'cos_sign': s, 'degrees': math.degrees(math.acos((1 if s >= 0 else -1) * float(c2) ** 0.5))}
    return {'a2': to_str(L2(u)), 'b2': to_str(L2(v)), 'c2': to_str(L2(w)),
            'a': float(L2(u)) ** 0.5, 'b': float(L2(v)) ** 0.5, 'c': float(L2(w)) ** 0.5,
            'alpha': ang(v, w), 'beta': ang(u, w), 'gamma': ang(u, v)}


def mat_str(A): return [vstr(r) for r in A]


def lattice_basis(V_, F_):
    """Three face-neighbour translations that generate all of them, with |det| = volume."""
    T = []
    for f in F_:
        t = sc(vsum(V_[i] for i in f), Fr(2, len(f)))
        if t not in T and sc(t, -1) not in T: T.append(t)
    vol = volume(V_, F_)
    for a, b, c in itertools.combinations(T, 3):
        d = det3(a, b, c)
        if d == 0 or abs_q(d) != vol: continue
        if all(all(x.is_int() for x in solve_coords([a, b, c], t)) for t in T): return [a, b, c]
    raise AssertionError('no lattice basis among the face-neighbour translations')


def solid_record(name, dirs, field, edge2=None):
    V_, F_, info = zonotope(dirs)
    res, fv = checks(V_, F_)
    vol = volume(V_, F_)
    assert vol == zonotope_volume(dirs), 'volume by faces must equal the zonotope formula'
    L = lattice_basis(V_, F_)
    til = tiling(V_, F_, L)
    sym = group_name(symmetry(V_))
    E2 = edge_lengths2(V_, F_)
    rec = {'mark': f'{name}, exact, 2026-10-23 · {MARK}', 'name': name, 'field': field, 'credit': CREDIT,
           'edge_directions_exact': [vstr(d) for d in dirs], 'edge_directions_float': [fl(d) for d in dirs],
           'vertices_exact': [vstr(v) for v in V_], 'vertices_float': [fl(v) for v in V_], 'faces': F_,
           'f_vector': list(fv), 'face_kinds': face_census(V_, F_), 'symmetry': sym,
           'edge_lengths_squared': [to_str(x) for x in E2], 'volume_exact': to_str(vol), 'volume_float': float(vol),
           'lattice_basis_exact': [vstr(b) for b in L], 'lattice_basis_float': [fl(b) for b in L], 'tiling': til,
           'solid_checks': res}
    if len(E2) == 1:
        e2 = E2[0]; rec['volume_at_edge_1'] = {'volume_squared_exact': to_str(vol * vol / (e2 * e2 * e2)),
                                               'float': float(vol) / float(e2) ** 1.5}
    return rec, V_, F_


def congr(rec_checks, label, P, Q):
    m = congruent(P, Q)
    rec_checks[label] = m is not None
    return m


def pts_str(P): return [vstr(p) for p in P]


def save(fname, rec):
    with open(os.path.join(DATA, fname), 'w') as f: json.dump(rec, f, indent=1, ensure_ascii=False)
    print('wrote', fname)


summary = {}
I3 = [V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)]


def mx(lattice, A, cell, fifth):
    """The move in a normal form check.py can replay: lattice 'FCC' (cell = Cell slider value) or 'cube' (the
    parallelepiped on the columns of A), shear A (exact rows), optional fifth direction (already times s)."""
    return {'lattice': lattice, 'A_rows_exact': mat_str(A), 'cell': cell, 'fifth_exact': vstr(fifth) if fifth else None}

# ============ classical helpers ============
s2 = R2 / 2                                                   # 1/sqrt 2
TO_GENS = [sc(V(1, 1, 0), s2), sc(V(1, -1, 0), s2), sc(V(1, 0, 1), s2), sc(V(1, 0, -1), s2), sc(V(0, 1, 1), s2), sc(V(0, 1, -1), s2)]
TO_PTS = sorted({tuple(sc(V(*p), s2)) for base in [(0, 1, 2)] for perm in itertools.permutations(base)
                 for sg in itertools.product((1, -1), repeat=3) for p in [tuple(a * b for a, b in zip(perm, sg))]}, key=lambda p: [float(x) for x in p])


def to_check():
    """The uniform truncated octahedron (edge 1, permutations of (0, +-1, +-2)/sqrt 2) is the zonotope of its six
    edge directions: exact vertex-set equality."""
    Vz, Fz, _ = zonotope(TO_GENS)
    return set(Vz) == set(TO_PTS) and len(TO_PTS) == 24, Vz, Fz


# ============ 2. Bain rhombic dodecahedron (#4) ============
BAIN_A = [V(1, 0, 0), V(0, 1, 0), V(0, 0, R2)]                 # diag(1, 1, sqrt 2): Towards Bain, path stop 2
bain_dirs, w = cell_dirs(BAIN_A, 1)
assert w == V(0, 0, 0), 'Bain: the four directions already have equal length, so Cell = 1 adds nothing (w = 0)'
assert bain_dirs == [matvec(BAIN_A, g) for g in G]
rec, Vb, Fb = solid_record('Bain rhombic dodecahedron (#4)', bain_dirs, 'Q(sqrt2)')
C = {}
C['solid_closed_wound_planar_convex'] = all(rec['solid_checks'].values())
C['f_vector_14_24_12'] = rec['f_vector'] == [14, 24, 12]
C['faces_4_squares_8_rhombi_60'] = rec['face_kinds'] == {'rhombus 60': 8, 'square': 4}
C['equal_edges_1'] = rec['edge_lengths_squared'] == ['1']
C['symmetry_D4h'] = rec['symmetry']['name'] == 'D4h'
C['volume_2sqrt2'] = rec['volume_exact'] == to_str(2 * R2)
C['tiles_by_translation'] = rec['tiling']['tiles']
C['lattice_is_Bain_FCC'] = abs_q(mdet(cols([matvec(BAIN_A, f) for f in FCC_BASIS]))) == volume(Vb, Fb)
# classical (a): cuboctahedron (edge 1) with an equilateral square pyramid on its top and bottom squares
CUBO = sorted({tuple(sc(V(*p), s2)) for perm in set(itertools.permutations((1, 1, 0))) for sg in itertools.product((1, -1), repeat=3)
               for p in [tuple(a * b for a, b in zip(perm, sg))]}, key=lambda p: [float(x) for x in p])
apex = [V(0, 0, R2), V(0, 0, -R2)]                            # square at z = 1/sqrt2, pyramid height 1/sqrt2
top = [p for p in CUBO if p[2] == s2] + [apex[0]]; bot = [p for p in CUBO if p[2] == -s2] + [apex[1]]
dis, W, Ps = dissection(CUBO + apex, [CUBO, top, bot])
C['classical_cuboctahedron_plus_2_pyramids_glue_to_one_convex_solid'] = dis['glued_pieces_are_the_whole']
C['pyramids_equilateral'] = all(dot(sub(apex[0], p), sub(apex[0], p)) == 1 for p in top[:-1])
congr(C, 'congruent_to_cuboctahedron_plus_2_pyramids', Vb, W[0])
# classical (b): Fedorov § 83 zone shrinking: the truncated octahedron with two perpendicular zones shrunk to 0
ok, Vto, Fto = to_check(); C['uniform_TO_is_zonotope_of_its_6_edge_directions'] = ok
perp = [(i, j) for i, j in itertools.combinations(range(6), 2) if dot(TO_GENS[i], TO_GENS[j]) == 0]
C['TO_minus_each_perpendicular_zone_pair_is_Bain_RD'] = len(perp) == 3 and all(
    congruent(Vb, zonotope([g for k, g in enumerate(TO_GENS) if k not in pr])[0]) is not None for pr in perp)
sixty = [(i, j) for i, j in itertools.combinations(range(6), 2) if dot(TO_GENS[i], TO_GENS[j]) != 0]
hp = zonotope([g for k, g in enumerate(TO_GENS) if k not in sixty[0]])
C['TO_minus_a_60_degree_zone_pair_is_a_hexagonal_prism_not_the_RD'] = len(hp[1]) == 8
rec['move'] = {'lattice': 'FCC (krp-core FCC_BASIS)', 'shear_A_exact': mat_str(BAIN_A), 'towards': 'Bain, path stop 2',
               'app_slider_values': lattice_params(BAIN_A), 'cell': 1, 'cell_shift_w_exact': vstr(w), 'stretch': None,
               'note': 'A is already symmetric, so the app applies A itself. Cell = 1 and Cell = 0 coincide here.'}
rec['classical'] = [
    {'source': 'Wikipedia, "Rhombic dodecahedron" (D4h form; link in the reference library, 2026-10-23)',
     'description': 'a cuboctahedron with square pyramids attached on the top and bottom',
     'exact_construction': 'cuboctahedron of edge 1 (permutations of (+-1, +-1, 0)/sqrt 2) and two equilateral square pyramids, apexes (0, 0, +-sqrt 2)',
     'points_exact': pts_str(CUBO + apex), 'dissection': dis},
    {'source': 'Fedorov 1885, § 83 p. 234 (zone shrinking; page image checked in the library check)',
     'description': 'truncated octahedron -> elongated dodecahedron -> rhombic dodecahedron by shrinking belts to zero',
     'exact_construction': 'uniform truncated octahedron (edge 1) with the two zones of a perpendicular pair of edge directions shrunk to 0'}]
rec['classical_credit'] = ('Bain correspondence: E. C. Bain 1924 (the stretch). Shape: first describer not found in the library; '
                           'Wikipedia lists it as the D4h form. Moves: ' + FEDOROV)
rec['move_exact'] = mx('FCC', BAIN_A, 1, None)
rec['classical_exact'] = [{'label': 'cuboctahedron + two equilateral square pyramids (Wikipedia, D4h form)', 'pieces': [pts_str(CUBO), pts_str(top), pts_str(bot)]},
                          {'label': 'truncated octahedron with a perpendicular pair of zones shrunk to 0 (Fedorov, § 83)', 'zonotope': [vstr(g) for k, g in enumerate(TO_GENS) if k not in perp[0]]}]
rec['expected'] = {'source': 'TARGETS.md (the nine; BAIN_RD), DISCOVERIES #4', 'f_vector': [14, 24, 12], 'face_kinds': {'rhombus 60': 8, 'square': 4}, 'symmetry': 'D4h', 'targets_volume_float': 2.82843}
rec['checks'] = C; save('bain-rd.json', rec); summary['bain-rd'] = C
BAIN = (Vb, Fb)

# ============ 1. Regular-hexagon elongated dodecahedron (F5, #5) ============
mu = positive_signs(bain_dirs)[1]
u5 = add(sc(bain_dirs[0], mu[0]), sc(bain_dirs[1], mu[1]))     # free direction mu1 h1 + mu2 h2 (partition 12|34)
assert all(m == 1 for m in mu) and u5 == V(1, 0, 0)
f5_dirs = bain_dirs + [u5]                                    # s = 1: |u5| = 1 = the edge
rec, Vf, Ff = solid_record('Regular-hexagon elongated dodecahedron (F5, #5)', f5_dirs, 'Q(sqrt2)')
C = {}
C['solid_closed_wound_planar_convex'] = all(rec['solid_checks'].values())
C['fedorov_counts_18_vertices_28_edges_12_faces'] = rec['f_vector'] == [18, 28, 12]
C['grunbaum_fig2b_faces_4_regular_hexagons_4_squares_4_rhombi_60'] = rec['face_kinds'] == {'regular hexagon': 4, 'rhombus 60': 4, 'square': 4}
C['equal_edges_1'] = rec['edge_lengths_squared'] == ['1']
C['volume_4sqrt2'] = rec['volume_exact'] == to_str(4 * R2)
C['symmetry_D2h'] = rec['symmetry']['name'] == 'D2h'
C['tiles_by_translation'] = rec['tiling']['tiles']
C['fifth_direction_is_free_lies_in_planes_h1h2_and_h3h4'] = det3(u5, bain_dirs[0], bain_dirs[1]) == 0 and det3(u5, bain_dirs[2], bain_dirs[3]) == 0
C['fifth_direction_equals_h1_plus_h2'] = u5 == add(bain_dirs[0], bain_dirs[1])
C['same_cell_as_krp_core_EMBLEM_DIRECTIONS'] = congruent(Vf, zonotope([V(h_, h_, h_ * R2), V(h_, -h_, h_ * R2), V(-h_, h_, h_ * R2), V(-h_, -h_, h_ * R2), V(1, 0, 0)])[0]) is not None
# classical: the uniform truncated octahedron with one zone shrunk to 0 (Fedorov § 83; Wikipedia "contraction")
C['uniform_TO_is_zonotope_of_its_6_edge_directions'] = ok
C['TO_minus_any_one_of_its_6_zones_is_congruent_to_F5'] = all(
    congruent(Vf, zonotope([g for k, g in enumerate(TO_GENS) if k != z])[0]) is not None for z in range(6))
# The stretch inserts a prism over the shadow of the Bain RD along u5: its four directions projected along x fall on two
# lines at cos^2 = 1/9 (70.53 / 109.47 degrees), so for this ED the 'square prism' wording does not apply (it fits the
# classical ED below, built on the regular RD).
pj = [V(0, d[1], d[2]) for d in bain_dirs]
C['F5_inserted_prism_is_rhombic_70.53_not_square'] = corner_cos2(pj[0], pj[2])[0] == Fr(1, 9) and iszero(cross(pj[0], pj[1]))
C['F5_minus_its_fifth_zone_is_the_Bain_RD'] = congruent(zonotope(f5_dirs[:4])[0], BAIN[0]) is not None
rec['move'] = {'lattice': 'FCC (krp-core FCC_BASIS)', 'shear_A_exact': mat_str(BAIN_A), 'towards': 'Bain, path stop 2',
               'app_slider_values': lattice_params(BAIN_A), 'cell': 1,
               'stretch': {'free_partition': '12|34', 'direction_exact': vstr(u5), 'length_s': '1',
                           'rule': 'u = mu1 h1 + mu2 h2 with sum mu_i h_i = 0 (here mu = 1, so u = h1 + h2): the line where the planes of h1, h2 and of h3, h4 meet'},
               'note': 'The fifth direction is not a live slider in the app: it is computed in krp-core (targets.js EMBLEM_DIRECTIONS, verify-kaleido.mjs "Bain ED along x") and shown in the Targets world.'}
rec['classical'] = [
    {'source': 'Grünbaum 2010, Fig. 2(b) p. 4 ("an elongated dodecahedron (with regular faces, but not Archimedean)")',
     'description': 'drawing only', 'checked': 'face kinds and counts'},
    {'source': 'Fedorov 1885, § 77 case 3 (counts) and § 83 p. 234 (zone shrinking); Wikipedia "Elongated dodecahedron": "a contraction of a uniform truncated octahedron"',
     'description': '18 vertices, 28 edges, 12 faces; the truncated octahedron with one belt shrunk to zero',
     'exact_construction': 'uniform truncated octahedron of edge 1 (permutations of (0, +-1, +-2)/sqrt 2), one of its six zones shrunk to 0',
     'points_exact': pts_str(TO_PTS)}]
rec['classical_credit'] = ('Shape known: Grünbaum 2010 Fig. 2(b) as Fedorov\'s representative; first describer not checked. '
                           'DICTO reached it independently on 2026-10-01 by the Bain stretch plus a fifth direction. Moves: ' + FEDOROV)
rec['move_exact'] = mx('FCC', BAIN_A, 1, u5)
rec['classical_exact'] = [{'label': 'uniform truncated octahedron with one zone shrunk to 0 (Fedorov, § 83; Wikipedia "contraction")', 'zonotope': [vstr(g) for g in TO_GENS[1:]]},
                          {'label': 'the uniform truncated octahedron is the zonotope of its six edge directions', 'identity_points': pts_str(TO_PTS), 'identity_zonotope': [vstr(g) for g in TO_GENS]}]
rec['expected'] = {'source': 'Fedorov 1885 § 77 (18, 28, 12); Grünbaum 2010 Fig. 2(b) (faces); library check and DISCOVERIES #5 (volume 4 sqrt 2); TARGETS ED #28 (5.65685)',
                   'f_vector': [18, 28, 12], 'face_kinds': {'regular hexagon': 4, 'rhombus 60': 4, 'square': 4}, 'volume_exact': to_str(4 * R2), 'symmetry': 'D2h', 'targets_volume_float': 5.65685}
rec['checks'] = C; save('regular-hexagon-ed.json', rec); summary['regular-hexagon-ed'] = C

# ============ 3. The elongated dodecahedron as a type (classical equilateral ED, Bain ED along z, F7) ============
ed = {'mark': f'The elongated dodecahedron as a type: the stretch family, exact, 2026-10-23 · {MARK}', 'credit': CREDIT,
      'family': ('Every RD-type cell Z(h1..h4) with sum mu_i h_i = 0, mu_i > 0, has exactly three free directions (besides its '
                 'own four): u_{ij|kl} = mu_i h_i + mu_j h_j, the line shared by the planes of h_i, h_j and of h_k, h_l. '
                 'Z(h1..h4, s u) is an elongated dodecahedron for every s > 0 (stretch = Minkowski sum with a segment; Delone '
                 'free direction; #49). Any fifth direction outside these three lines leaves a belt of 8 faces (Venkov), so no '
                 'tiling. Parameters: lattice (six sliders), Cell t, partition ij|kl, stretch s.'),
      'members': {}}
# (a) classical equilateral ED = regular RD + square prism of height = edge (Polyhedraverse ED; Polytope Wiki / MathWorld)
rd_dirs, w0 = cell_dirs([V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)], 1)
assert w0 == V(0, 0, 0)
muR = positive_signs(rd_dirs)[1]; uR = add(rd_dirs[0], rd_dirs[1])
assert all(m == 1 for m in muR) and uR == V(1, 0, 0)
sR = R3 / 2                                                   # = the RD edge, so all edges equal
ced_dirs = rd_dirs + [sc(uR, sR)]
rec, Vc, Fc = solid_record('Equilateral elongated dodecahedron (regular RD + square prism)', ced_dirs, 'Q(sqrt3)')
C = {}
C['solid_closed_wound_planar_convex'] = all(rec['solid_checks'].values())
C['fedorov_counts_18_28_12'] = rec['f_vector'] == [18, 28, 12]
C['equal_edges'] = len(rec['edge_lengths_squared']) == 1
C['tiles_by_translation'] = rec['tiling']['tiles']
C['symmetry_D4h'] = rec['symmetry']['name'] == 'D4h'
hh = R3 / 2                                                   # elongatedDodecahedronVerts(1, 1): h = sqrt3 * 1/2
PV = ([V(0, 0, 1 + hh / 2), V(0, 0, -(1 + hh / 2))] + [V(x * h_, y * h_, z * h_ + z * hh / 2) for x in (1, -1) for y in (1, -1) for z in (1, -1)]
      + [p for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)] for p in (V(x, y, hh / 2), V(x, y, -hh / 2))])
congr(C, 'congruent_to_Polyhedraverse_elongatedDodecahedronVerts(1,1)', Vc, PV)
# the classical cut-and-glue: RD halves (cut at the equator) capping a square prism
RDV = [V(0, 0, 1), V(0, 0, -1), V(1, 0, 0), V(-1, 0, 0), V(0, 1, 0), V(0, -1, 0)] + [V(x * h_, y * h_, z * h_) for x in (1, -1) for y in (1, -1) for z in (1, -1)]
up = [add(p, V(0, 0, hh / 2)) for p in RDV if p[2] >= 0]; dn = [add(p, V(0, 0, -hh / 2)) for p in RDV if p[2] <= 0]
prism = [V(x, y, z) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)] for z in (hh / 2, -hh / 2)]
dis, W, Ps = dissection(PV, [up, prism, dn])
C['classical_RD_halves_plus_square_prism_glue_to_one_convex_solid'] = dis['glued_pieces_are_the_whole']
C['prism_cross_section_is_a_square'] = all(dot(sub(a, b), sub(a, b)) == 2 for a, b in [(prism[0], prism[4]), (prism[4], prism[2]), (prism[2], prism[6]), (prism[6], prism[0])])
rec['move'] = {'lattice': 'FCC', 'shear_A_exact': mat_str([V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)]), 'app_slider_values': lattice_params([V(1, 0, 0), V(0, 1, 0), V(0, 0, 1)]),
               'cell': 1, 'stretch': {'free_partition': '12|34', 'direction_exact': vstr(uR), 'length_s': to_str(sR), 'note': 's = the RD edge sqrt3/2 (app scale), so every edge is equal'}}
rec['classical'] = [{'source': 'Polyhedraverse ED (krp-core elongated-dodecahedron.js, after Polytope Wiki / MathWorld): "take a Rhombic Dodecahedron, cut it through its own equator ... insert a square prism of height h"',
                     'exact_construction': 'elongatedDodecahedronVerts(1, 1), h = sqrt3/2', 'points_exact': pts_str(PV), 'dissection': dis}]
rec['move_exact'] = mx('FCC', I3, 1, sc(uR, sR))
rec['classical_exact'] = [{'label': 'Polyhedraverse elongatedDodecahedronVerts(1, 1)', 'points': pts_str(PV)},
                          {'label': 'RD cut at its equator, halves capping a square prism (Polytope Wiki / MathWorld, per krp-core)', 'pieces': [pts_str(up), pts_str(prism), pts_str(dn)]}]
rec['expected'] = {'source': 'Fedorov 1885 § 77 case 3', 'f_vector': [18, 28, 12], 'symmetry': 'D4h'}
rec['wikipedia_volume_note'] = 'Wikipedia "Elongated dodecahedron" (read 2026-10-23) gives V = 6 a^3 with no definition of a; at edge 1 this ED has volume_at_edge_1 above and the regular-hexagon ED 4 sqrt 2; neither is 6. Reported, not changed.'
rec['checks'] = C; ed['members']['classical_equilateral_ED'] = rec; summary['ed-classical'] = C
# (b) Bain ED along z (TARGETS #23): the other kind of free line of the Bain RD
uz = add(bain_dirs[0], bain_dirs[3]); assert uz == V(0, 0, R2)
bz_dirs = bain_dirs + [V(0, 0, 1)]
rec, _, _ = solid_record('Bain ED along z (TARGETS #23)', bz_dirs, 'Q(sqrt2)')
C = {'solid_closed_wound_planar_convex': all(rec['solid_checks'].values()), 'fedorov_counts_18_28_12': rec['f_vector'] == [18, 28, 12],
     'faces_8_rhombi_60_4_hexagons_135_135_90': rec['face_kinds'] == {'equilateral hexagon 135/135/90': 4, 'rhombus 60': 8},
     'volume_2sqrt2_plus_2_(TARGETS 4.82843)': rec['volume_exact'] == to_str(2 + 2 * R2), 'tiles_by_translation': rec['tiling']['tiles']}
rec['move'] = {'lattice': 'FCC', 'towards': 'Bain, path stop 2', 'cell': 1, 'stretch': {'free_partition': '14|23', 'direction_exact': vstr(V(0, 0, 1)), 'length_s': '1'}}
rec['move_exact'] = mx('FCC', BAIN_A, 1, V(0, 0, 1))
rec['expected'] = {'source': 'TARGETS ED #23 (BAIN_ED)', 'f_vector': [18, 28, 12], 'face_kinds': {'equilateral hexagon 135/135/90': 4, 'rhombus 60': 8}, 'targets_volume_float': 4.82843}
rec['checks'] = C; ed['members']['bain_ED_along_z_TARGETS_23'] = rec; summary['ed-bain-z'] = C
# Bain RD: the third free line (13|24) is the y axis, the same cell as F5 turned 90 degrees
C = {'bain_third_free_line_gives_F5_again': congruent(zonotope(bain_dirs + [V(0, 1, 0)])[0], Vf) is not None}
summary['ed-bain-y'] = C

# (c) F7: DICTO's skewed EDs on DICTO FCC
B15 = []
for k in range(3):
    e = [q(0)] * 3; e[k] = q(1); B15.append(tuple(e))
    for s1 in (1, -1):
        for s2_ in (1, -1):
            v = [q(0)] * 3; v[k] = q(h_); v[(k + 1) % 3] = PHI * s1 / 2; v[(k + 2) % 3] = s2_ / (2 * PHI); B15.append(tuple(v))
assert all(dot(b, b) == 1 for b in B15)
C72 = (R5 - 1) / 4                                            # cos 72
def lang(a, b):
    d = abs_q(dot(a, b))
    return {q(Fr(1, 2)): 60, C72: 72, (R5 + 1) / 4: 36, q(0): 90}.get(d)
def dicto_cell():                                             # krp-core dicto-fcc.js cellDirectionsBlueFrame, exact
    for a, b, c, d in itertools.combinations(range(15), 4):
        S = [B15[a], B15[b], B15[c], B15[d]]
        if any(det3(S[i], S[j], S[k]) == 0 for i, j, k in itertools.combinations(range(4), 3)): continue
        if sorted(lang(S[i], S[j]) or 0 for i, j in itertools.combinations(range(4), 2)) == [60, 60, 60, 72, 72, 72]: return S
D4 = dicto_cell()
hD, muD = positive_signs(D4)
rec, Vd, Fd = solid_record("DICTO skewed RD (F1, the RD of DICTO FCC)", hD, 'Q(sqrt5)')
C = {'solid_closed_wound_planar_convex': all(rec['solid_checks'].values()), 'f_vector_14_24_12': rec['f_vector'] == [14, 24, 12],
     'volume_phi2': rec['volume_exact'] == to_str(PHI * PHI), 'tiles_by_translation': rec['tiling']['tiles'],
     'faces_6_rhombi_60_6_rhombi_72': rec['face_kinds'] == {'rhombus 60': 6, 'rhombus 72.00': 6}}
AD = matmul(cols([sub(hD[0], hD[3]), sub(hD[0], hD[2]), sub(hD[0], hD[1])]), minv(cols(FCC_BASIS)))
cdD, wD = cell_dirs(AD, 1)
C['cell_1_of_this_shear_is_DICTO_RD_exactly'] = cdD == hD
rec['move'] = {'lattice': 'FCC', 'towards': 'DICTO FCC, path stop 2', 'shear_A_exact (one labelling)': mat_str(AD), 'app_slider_values (edge 1)': lattice_params(AD), 'cell': 1}
rec['dependency_mu_exact'] = [to_str(x) for x in muD]
rec['move_exact'] = mx('FCC', AD, 1, None)
rec['expected'] = {'source': 'DISCOVERIES #1 (volume phi^2)', 'f_vector': [14, 24, 12], 'face_kinds': {'rhombus 60': 6, 'rhombus 72.00': 6}, 'volume_exact': to_str(PHI * PHI)}
rec['checks'] = C; ed['members']['dicto_skewed_RD_F1'] = rec; summary['dicto-rd'] = C
f7 = {}
for part in [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]:
    (i, j), (k, l) = part
    u = add(sc(hD[i], muD[i]), sc(hD[j], muD[j]))
    blue = [b for b in B15 if iszero(cross(b, u))]
    key = f'{i + 1}{j + 1}|{k + 1}{l + 1}'
    entry = {'free_line_exact': vstr(u), 'free_line_float': fl(u), 'angles_to_h_deg': [round(__import__('math').degrees(__import__('math').acos(abs(float(dot(u, h)) / float(dot(u, u)) ** .5))), 4) for h in hD],
             'is_a_blue_line (icosahedral 2-fold axis)': bool(blue)}
    if blue:
        b = blue[0]; dirs = hD + [b]
        r, Ve, Fe = solid_record(f'DICTO skewed ED on free line {key}', dirs, 'Q(sqrt5)')
        r['move'] = {'lattice': 'FCC', 'towards': 'DICTO FCC, path stop 2', 'cell': 1, 'stretch': {'free_partition': key, 'direction_exact': vstr(b), 'length_s': '1'}}
        r['move_exact'] = mx('FCC', AD, 1, b)
        entry['solid'] = r
    f7[key] = entry
ed['members']['dicto_free_lines'] = f7
C = {}
found = {k: v['solid'] for k, v in f7.items() if 'solid' in v}
C['exactly_two_of_the_three_free_lines_are_blue_lines'] = len(found) == 2
want16 = {'equilateral hexagon 144/144/72': 2, 'regular hexagon': 2, 'rhombus 60': 4, 'rhombus 72.00': 4}
want18 = {'equilateral hexagon 144/108/108': 4, 'rhombus 60': 6, 'rhombus 72.00': 2}
m16 = [k for k, r in found.items() if r['face_kinds'] == want16 and r['volume_exact'] == to_str(PHI * PHI + 2)]
m18 = [k for k, r in found.items() if r['face_kinds'] == want18 and r['volume_exact'] == to_str(PHI * PHI * PHI + Fr(1, 2))]
C['one_is_TARGETS_16_(4 rh60, 4 rh72, 2 hex 144/144/72, 2 regular hexagons; volume phi^2+2)'] = len(m16) == 1
C['other_is_TARGETS_18_(6 rh60, 2 rh72, 4 hex 144/108/108; volume phi^3+1/2)'] = len(m18) == 1
C['both_fedorov_counts_18_28_12'] = all(r['f_vector'] == [18, 28, 12] for r in found.values())
C['both_equal_edges_1'] = all(r['edge_lengths_squared'] == ['1'] for r in found.values())
C['both_tile_by_translation'] = all(r['tiling']['tiles'] for r in found.values())
C['both_closed_wound_planar_convex'] = all(all(r['solid_checks'].values()) for r in found.values())
ed['F7_partitions'] = {'ED16': m16, 'ED18': m18}
for k_ in m16: f7[k_]['solid']['expected'] = {'source': 'TARGETS ED #16; DISCOVERIES #7 (phi^2 + 2)', 'f_vector': [18, 28, 12], 'face_kinds': want16, 'volume_exact': to_str(PHI * PHI + 2), 'targets_volume_float': 4.61803}
for k_ in m18: f7[k_]['solid']['expected'] = {'source': 'TARGETS ED #18; DISCOVERIES #7 (phi^3 + 1/2)', 'f_vector': [18, 28, 12], 'face_kinds': want18, 'volume_exact': to_str(PHI * PHI * PHI + Fr(1, 2)), 'targets_volume_float': 4.73607}
ed['checks_F7'] = C; summary['ed-F7'] = C
ed['classical_credit'] = 'Elongated dodecahedron (elongated hexaparallelohedron): Fedorov 1885, § 77 case 3; zone shrinking § 83. Free directions: Delone 1929 (via Garber 2019, Def. 2.13). ' + FEDOROV
save('elongated-dodecahedron-type.json', ed)

# ============ 4. Bilinski dodecahedron ============
F6 = [V(0, 1, PHI), V(0, -1, PHI), V(1, PHI, 0), V(-1, PHI, 0), V(PHI, 0, 1), V(PHI, 0, -1)]   # the six 5-fold axes
e2B = dot(F6[0], F6[0]); assert e2B == PHI + 2
Bg = F6[:4]
hB, muB = positive_signs(Bg)
# choose the labelling (which h goes with which RD direction g) giving the most equal lattice lengths
best = None; seen = set()
for perm in itertools.permutations(range(4)):
    h = [hB[p] for p in perm]
    A = matmul(cols([sub(h[0], h[3]), sub(h[0], h[2]), sub(h[0], h[1])]), minv(cols(FCC_BASIS)))
    lp = lattice_params(A)
    key = tuple(sorted([lp['a2'], lp['b2'], lp['c2']]) + sorted([lp['alpha']['cos2'], lp['beta']['cos2'], lp['gamma']['cos2']]))
    seen.add(tuple([lp['a2'], lp['b2'], lp['c2'], lp['alpha']['cos2'], lp['beta']['cos2'], lp['gamma']['cos2']]))
    score = (len({lp['a2'], lp['b2'], lp['c2']}), [lp['a'], lp['b'], lp['c']])
    if best is None or score < best[0]: best = (score, perm, A)
_, permB, AB = best
hB = [hB[p] for p in permB]; muB = positive_signs(hB)[1]
cdB, wB = cell_dirs(AB, 1)
assert cdB == hB, 'Cell = 1 of the shear A_B must give the Bilinski directions exactly'
rec, VB, FB = solid_record('Bilinski dodecahedron', hB, 'Q(sqrt5)')
C = {}
C['solid_closed_wound_planar_convex'] = all(rec['solid_checks'].values())
C['f_vector_14_24_12'] = rec['f_vector'] == [14, 24, 12]
C['twelve_congruent_golden_rhombi (cos^2 = 1/5: diagonals in ratio phi)'] = rec['face_kinds'] == {'golden rhombus': 12}
C['equal_edges'] = rec['edge_lengths_squared'] == [to_str(PHI + 2)]
C['symmetry_D2h'] = rec['symmetry']['name'] == 'D2h'
C['tiles_by_translation'] = rec['tiling']['tiles']
C['shear_then_cell_1_gives_it_exactly'] = cdB == hB
C['equal_edge_cell_is_unique (circumcentre of 4 non-coplanar points)'] = det3(*[sub(sc(matvec(AB, G[i]), -1), sc(matvec(AB, G[0]), -1)) for i in (1, 2, 3)]) != 0
# Cell = 0 (the RD only sheared) is an affine image of Kepler's K; B is not (Grünbaum 2010 p. 6): an affine map keeps the
# ratios of the dependency coefficients, which are 1:1:1:1 for K.
C['dependency_mu_not_all_equal_so_B_is_not_an_affine_image_of_K'] = len(set(muB)) > 1
c0 = [matvec(AB, g) for g in G]; V0, F0, _ = zonotope(c0)
C['cell_0_is_not_B (needs Cell = 1)'] = congruent(V0, VB) is None
C['cell_1_volume_equals_lattice_det (app: fills space, no red band)'] = volume(VB, FB) == abs_q(mdet(cols([matvec(AB, f) for f in FCC_BASIS])))
# classical (a): Grünbaum's zone deletion T -> F -> B
VT, FT, _ = zonotope(F6)
rT, fvT = checks(VT, FT)
C['T_is_Keplers_triacontahedron (32 V, 60 E, 30 golden rhombi, closed convex)'] = fvT == (32, 60, 30) and all(rT.values()) and face_census(VT, FT) == {'golden rhombus': 30}
VF, FF, _ = zonotope(F6[:5]); rF, fvF = checks(VF, FF)
C['T_minus_one_zone_is_Fedorovs_rhombic_icosahedron (22 V, 40 E, 20 golden rhombi)'] = fvF == (22, 40, 20) and face_census(VF, FF) == {'golden rhombus': 20}
C['T_minus_any_two_zones_(all 15 pairs)_is_congruent_to_the_Kaleidohedra_B'] = all(
    congruent(VB, zonotope([g for k, g in enumerate(F6) if k not in pr])[0]) is not None for pr in itertools.combinations(range(6), 2))
# classical (b): Hafner-Zitko, glued from golden rhombohedra: the zonotopal tilings of B by its four parallelepipeds
def kind(T3):
    a, b, c = T3; s = (dot(a, b) * dot(a, c) * dot(b, c)).sign()
    return 'acute (prolate) golden rhombohedron' if s > 0 else 'obtuse (oblate) golden rhombohedron'
tilings = []
for deltas in itertools.product((1, -1), repeat=4):
    pieces = []
    for m in range(4):
        T3 = [hB[k] for k in range(4) if k != m]
        off = sc(hB[m], Fr(deltas[m], 2))
        pieces.append(([add(p, off) for p in zonotope(T3)[0]], kind(T3)))
    d, W, Ps = dissection(VB, [p for p, _ in pieces])
    if d['glued_pieces_are_the_whole']: tilings.append((deltas, d, [k for _, k in pieces], [p for p, _ in pieces]))
C['B_is_glued_from_four_golden_rhombohedra (exact dissection found)'] = len(tilings) >= 1
comp = sorted(tilings[0][2]) if tilings else []
C['two_acute_and_two_obtuse'] = comp.count('acute (prolate) golden rhombohedron') == 2 and comp.count('obtuse (oblate) golden rhombohedron') == 2
Ha = next(zonotope(list(t))[0] for t in itertools.combinations(F6, 3) if kind(t).startswith('acute'))
Ho = next(zonotope(list(t))[0] for t in itertools.combinations(F6, 3) if kind(t).startswith('obtuse'))
C['the_four_pieces_are_Grunbaums_Ha_and_Ho'] = all(congruent(p, Ha if k.startswith('acute') else Ho) is not None for p, k in zip(tilings[0][3], tilings[0][2])) if tilings else False
volHa = volume(*zonotope(list(next(t for t in itertools.combinations(F6, 3) if kind(t).startswith('acute'))))[:2])
volHo = volume(*zonotope(list(next(t for t in itertools.combinations(F6, 3) if kind(t).startswith('obtuse'))))[:2])
C['volume_B = 2 Ha + 2 Ho'] = volume(VB, FB) == 2 * volHa + 2 * volHo
k2 = Fr(3, 4) / e2B                                           # scale to the app's RD edge sqrt3/2
rec['move'] = {'lattice': 'FCC (krp-core FCC_BASIS)', 'shear_A_exact (lengths at edge sqrt(phi+2))': mat_str(AB),
               'app_slider_values (scaled to the app edge sqrt3/2)': lattice_params(AB, k2),
               'app_slider_values (raw, edge sqrt(phi+2))': lattice_params(AB),
               'cell': 1, 'cell_shift_w_exact': vstr(wB), 'stretch': None,
               'labelling': f'h_i = the five-fold vectors in order {permB}; {len(seen)} distinct slider settings over the 24 labellings give the same solid',
               'note': 'Reached by the six sliders (not a Towards path); the app sliders step 0.005 and 0.1 degree, so the app shows a close approximation; the exact values are these.'}
rec['dependency_mu_exact'] = [to_str(x) for x in muB]
lpB = lattice_params(AB)
C['sliders_are_plain_FCC_with_gamma_36: a=b=c, alpha=beta=60, cos gamma = phi/2'] = (
    lpB['a2'] == lpB['b2'] == lpB['c2'] and lpB['alpha']['cos2'] == lpB['beta']['cos2'] == '1/4' and lpB['alpha']['cos_sign'] == lpB['beta']['cos_sign'] == 1
    and lpB['gamma']['cos2'] == to_str(PHI * PHI / 4) and lpB['gamma']['cos_sign'] == 1)
# The same move with lengths a = b = c = 1 (scale is free): basis (sqrt2-length) vectors at 60, 60, 36 degrees -> Cell = 1 -> B scaled
c36 = PHI / 2
# Build any exact basis with Gram 2*[[1, cg, cb], [cg, 1, ca], [cb, ca, 1]] is not possible in Q(sqrt5) (Cholesky leaves the field),
# so the scale-free check is done on the Gram matrix: Gram(A_B * FCC_BASIS) = (a^2 * 2) * [[1, phi/2, 1/2], [phi/2, 1, 1/2], [1/2, 1/2, 1]].
uB, vB, wB2 = [matvec(AB, f) for f in FCC_BASIS]
g0 = dot(uB, uB)
C['Gram_of_the_Bilinski_lattice_basis_is_|u|^2 [[1, phi/2, 1/2], [phi/2, 1, 1/2], [1/2, 1/2, 1]]'] = (
    dot(vB, vB) == g0 and dot(wB2, wB2) == g0 and dot(uB, vB) == g0 * PHI / 2 and dot(uB, wB2) == g0 / 2 and dot(vB, wB2) == g0 / 2)
rec['classical'] = [
    {'source': 'Grünbaum 2010, pp. 5-6, Fig. 4: zone deletion T -> F -> B (after Fedorov); Coxeter (quoted by Senechal 2004): remove a zone and bring the two pieces together',
     'exact_construction': 'rhombic triacontahedron = zonotope of the six five-fold axes (0, +-1, phi), (+-1, phi, 0), (phi, 0, +-1); two zones deleted', 'generators_exact': pts_str(F6)},
    {'source': 'Hafner and Zitko 2002, Introduction: "could be made by gluing appropriate number of rhombohedra" (no count given)',
     'result': f'{len(tilings)} exact gluings of B from its four golden rhombohedra; each uses {comp}',
     'gluing_offsets (delta_m: piece without h_m shifted by delta_m h_m / 2)': [list(t[0]) for t in tilings],
     'dissection': tilings[0][1] if tilings else None},
    {'source': 'Grünbaum 2010, pp. 8-9', 'description': 'B is affinely a Dirichlet-Voronoi tile of a lattice affine to fcc',
     'agreement': 'the move shows the lattice of B is a linear image of FCC (the shear A); Cell = 1 is what turns K into B, since B is not an affine image of K'}]
rec['volume_pieces'] = {'Ha (acute)': to_str(volHa), 'Ho (obtuse)': to_str(volHo)}
rec['classical_credit'] = 'Bilinski 1960 (not read; link only). Zone deletion: Fedorov 1885 / Grünbaum 2010. Gluing: Hafner and Zitko 2002. Moves: ' + FEDOROV
rec['move_exact'] = mx('FCC', AB, 1, None)
rec['classical_exact'] = [{'label': 'rhombic triacontahedron with any two of its six zones deleted (Grünbaum Fig. 4; all 15 pairs)', 'zone_deletion_generators': [vstr(g) for g in F6], 'keep': 4},
                          {'label': 'four golden rhombohedra glued (Hafner and Zitko 2002)', 'pieces': [pts_str(p) for p in tilings[0][3]]}]
rec['expected'] = {'source': 'Grünbaum 2010 (isozonohedron: 12 congruent golden rhombi); D2h', 'f_vector': [14, 24, 12], 'face_kinds': {'golden rhombus': 12}, 'symmetry': 'D2h'}
rec['checks'] = C; save('bilinski-dodecahedron.json', rec); summary['bilinski'] = C

# DICTO's skewed RD (F1) has the same dependency coefficients (phi, phi, 1, 1) as B: then a linear map carries B onto F1.
def affine_map(hs, ht):
    for perm in itertools.permutations(range(4)):
        t = [ht[p] for p in perm]
        L = matmul(cols(t[:3]), minv(cols(hs[:3])))
        if matvec(L, hs[3]) == t[3]: return L, perm
    return None, None
LBD, pBD = affine_map(hB, hD)
C2 = {'F1_dependency_equals_B_dependency (phi, phi, 1, 1 up to order)': sorted(map(float, muD)) == sorted(map(float, muB)),
      'a_linear_map_carries_the_four_B_directions_onto_F1s (so F1 = L(B), an affine image of Bilinski B)': LBD is not None,
      'and_F1_is_not_an_affine_image_of_Keplers_K (mu not all equal)': len(set(muD)) > 1,
      'zonotope_check: L applied to Bs corners gives F1s corners': LBD is not None and {matvec(LBD, v) for v in VB} == set(Vd)}
ed['F1_is_an_affine_image_of_Bilinski'] = {'linear_map_exact': mat_str(LBD) if LBD else None, 'pairing (B direction i -> F1 direction perm[i])': list(pBD) if pBD else None, 'checks': C2}
save('elongated-dodecahedron-type.json', ed)
summary['F1-affine-to-B'] = C2

# ============ 5. 60-degree rhombohedron (worked example) ============
RA = [sc(V(0, 1, 1), s2), sc(V(1, 0, 1), s2), sc(V(1, 1, 0), s2)]      # images of the cube's edges e1, e2, e3
rec, Vr, Fr6 = solid_record('60-degree rhombohedron', RA, 'Q(sqrt2)')
C = {}
C['solid_closed_wound_planar_convex'] = all(rec['solid_checks'].values())
C['f_vector_8_12_6'] = rec['f_vector'] == [8, 12, 6]
C['six_rhombi_60'] = rec['face_kinds'] == {'rhombus 60': 6}
C['equal_edges_1'] = rec['edge_lengths_squared'] == ['1']
C['volume_1_over_sqrt2'] = rec['volume_exact'] == to_str(R2 / 2)
C['symmetry_D3d'] = rec['symmetry']['name'] == 'D3d'
C['tiles_by_translation'] = rec['tiling']['tiles']
OCT = [V(s2, 0, 0), V(-s2, 0, 0), V(0, s2, 0), V(0, -s2, 0), V(0, 0, s2), V(0, 0, -s2)]
ap = [V(s2, s2, s2), V(-s2, -s2, -s2)]
t1 = [OCT[0], OCT[2], OCT[4], ap[0]]; t2 = [OCT[1], OCT[3], OCT[5], ap[1]]
C['tetrahedra_regular_edge_1'] = all(dot(sub(a, b), sub(a, b)) == 1 for t in (t1, t2) for a, b in itertools.combinations(t, 2))
dis, W, Ps = dissection(OCT + ap, [OCT, t1, t2])
C['classical_octahedron_plus_2_tetrahedra_glue_to_one_convex_solid'] = dis['glued_pieces_are_the_whole']
congr(C, 'congruent_to_Maurolicos_tetrahedron_octahedron_tetrahedron', Vr, W[0])
C['same_as_app_FCC_basis_parallelepiped (plain FCC sliders)'] = congruent(Vr, [sc(p, s2) for p in zonotope(FCC_BASIS)[0]]) is not None
rec['move'] = {'lattice': 'simple cubic (Z^3)', 'shear_A_exact (columns = images of e1, e2, e3)': mat_str(cols(RA)),
               'lattice_params': {'a=b=c': '1', 'alpha=beta=gamma': '60 degrees (cos = 1/2)'},
               'note': 'a = b = c, all angles 60: the sheared cube lattice is the FCC lattice itself, and the rhombohedron is the parallelepiped on the app\'s FCC_BASIS (plain FCC sliders), scaled to edge 1. TARGETS: RHOMBOHEDRON_60.'}
rec['classical'] = [{'source': 'Lagarias and Zong 2012, Notices AMS 59, p. 1542, Fig. 2 (Maurolico, 16th c.)',
                     'description': 'gluing two regular tetrahedra to diagonally opposite faces of a regular octahedron; six congruent faces, each a 60-120 degree rhombus',
                     'exact_construction': 'octahedron +-e_i/sqrt2 (edge 1), tetrahedron apexes +-(1,1,1)/sqrt2', 'points_exact': pts_str(OCT + ap), 'dissection': dis}]
rec['classical_credit'] = 'Maurolico (16th century), per Lagarias and Zong 2012. Moves: ' + FEDOROV
rec['move_exact'] = mx('cube', cols(RA), None, None)
rec['classical_exact'] = [{'label': 'tetrahedron + octahedron + tetrahedron (Maurolico, per Lagarias and Zong 2012)', 'pieces': [pts_str(OCT), pts_str(t1), pts_str(t2)]}]
rec['expected'] = {'source': 'Lagarias and Zong 2012 (six 60-120 rhombi); TARGETS (RHOMBOHEDRON_60, 0.707107)', 'f_vector': [8, 12, 6], 'face_kinds': {'rhombus 60': 6}, 'symmetry': 'D3d', 'targets_volume_float': 0.707107}
rec['checks'] = C; save('rhombohedron-60.json', rec); summary['rhombohedron-60'] = C

# ============ negative control for the congruence test (rule 7) ============
A6 = [V(x, 0, 0) for x in (0, 1, 4, 10, 12, 17)]; B6 = [V(x, 0, 0) for x in (0, 1, 8, 11, 13, 17)]
dl = lambda S: sorted(float(dot(sub(a, b), sub(a, b))) for a, b in itertools.combinations(S, 2))
summary['congruence-test-control'] = {'homometric_sets_have_equal_sorted_distance_lists': dl(A6) == dl(B6),
                                      'corner_matching_rejects_them': congruent(A6, B6) is None,
                                      'corner_matching_accepts_a_rotated_copy': congruent(Vb, [V(p[1], -p[0], p[2]) for p in Vb]) is not None}

with open(os.path.join(DATA, 'build-summary.json'), 'w') as f:
    json.dump({'mark': f'exact-vs-dissection build summary, 2026-10-23 · {MARK}', 'checks': summary}, f, indent=1, ensure_ascii=False)
bad = [(s, k) for s, c in summary.items() for k, v in c.items() if v is not True]
n = sum(len(c) for c in summary.values())
print(f'{n - len(bad)} of {n} build checks passed')
for b in bad: print('  FAILED', b)
