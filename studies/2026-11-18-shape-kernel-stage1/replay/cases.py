"""Replay cases (shape kernel, stage 1 proper, 2026-11-18): every study run that uses a covered number module, has a stored output and
whose arguments are recorded (in a usage line, the stored log or the stored JSON).  Read by setup.py and replay.py.

A case: one script run in one study.  `copies`: studies copied into the case tree (writable; the kernel swaps are made there);
every other study is linked read-only from the studies source.  `swaps`: (module, mode, shim, names): 'defs' replaces the named
top-level definitions (replay/swap.py), 'whole' replaces the file, 'head' puts the shim before the original text from a marker line.
`log`: the stored stdout (relative to the study).  Files the run writes are compared with the stored files they overwrite."""
K10 = '2026-11-15-grunbaum-k10'; MIX = '2026-11-17-get-mixing'; AM = '2026-11-17-atoms-missing'; AM2 = '2026-11-17-atoms-missing-2'
GC = '2026-11-03-golden-cuts-beyond-plato'; SD = '2026-11-03-6d-golden-cubes'; DP = '2026-11-03-dual-pairs-dimensions'
ZS = ('zsurf_zphi.py', ['zadd', 'zsub', 'zmul', 'zneg', 'zsign', 'zfloat', 'zconj'])
EXL = ('exactlib_fields.py', ['QF', 'KC', 'AlgField', 'RF'])
CUB = ('cubes_lib_K.py', ['_s2sign', 'K', 'kstr'])
CASES = []


def case(name, group, study, script, args=(), cwd='.', log=None, copies=(), swaps=()):
    CASES.append(dict(name=name, group=group, study=study, script=script, args=list(args), cwd=cwd, log=log,
                      copies=[study] + [c for c in copies if c != study], swaps=list(swaps)))


# ---- the pilot's cases, re-run on the stage-1 kernel (G1, G2, G3)
PE = '2026-11-13-paradigm-exact'
for nm, sc, a, lg in (('hemi_exact', 'scripts/hemi_exact.py', ['../2026-11-11-hemi-rd-build/data/dicto-build-worldpoly.json'], 'data/hemi-exact.log'),
                      ('scutoid_exact', 'scripts/scutoid_exact.py', ['all'], 'data/scutoid-exact.log')):
    case(f'pilot-paradigm-exact-{nm}', 'G1', PE, sc, a, log=lg, swaps=[(f'{PE}/scripts/q5.py', 'head', 'paradigm-exact_q5_head.py', 'def facets(P):')])
FL = '2026-11-13-platonic-fans-law'
case('pilot-fans-law', 'G2', FL, 'scripts/fans_law.py', ['../2026-11-13-platonic-disc-ranking/data/registry-solids.json',
     '../2026-11-13-platonic-disc-ranking/data/disc-ranking.json', 'data/fans-law.json'], log='data/fans-law.log',
     swaps=[(f'{FL}/scripts/qf.py', 'whole', 'fans-law_qf.py', None)])
OO = '2026-10-18-ocd-octet'
case('pilot-ocd-octet-step12', 'G3', OO, 'step12_exact_faces.py', cwd='scripts', log='data/step12.log',
     swaps=[(f'{OO}/scripts/q5.py', 'whole', 'ocd-octet_q5.py', None)])

# ---- G4: K of cubes_lib.py (Q(sqrt2, sqrt5)), octet_special_exact.py (Q(k^(1/n))), pds_line.py (Q(sqrt5))
SF = '2026-10-23-shadow-forms'
case('octet-special-exact', 'G4', SF, 'octet_special_exact.py', cwd='octet', log='octet/octet-special-exact.txt',
     swaps=[(f'{SF}/octet/octet_special_exact.py', 'defs', 'octet_special_exact_K.py', ['K'])])
PD = '2026-11-12-pds-hopscotch-line'
case('pds-line-pilot', 'G4', PD, 'scripts/pds_line.py', ['--pilot'], log='data/pds-line-pilot.log',
     swaps=[(f'{PD}/scripts/pds_line.py', 'defs', 'pds_line_K.py', ['K'])])
for sc, a in [('s10_honeycomb_cubes.py', []), ('s11_star_polytopes.py', [])] + [('s9_why_not_cubes.py', [p]) for p in 'ABCDE']:
    case(f'golden-cuts-{sc[:-3]}{"-" + a[0] if a else ""}', 'G4', GC, sc, a, cwd='scripts', swaps=[(f'{GC}/scripts/cubes_lib.py', 'defs') + CUB])
for sc in ('s1_sanity_cut_project.py', 's2_field_signature.py', 's3_six_d.py', 's4_min_norm.py'):
    case(f'6d-golden-cubes-{sc[:-3]}', 'G4', SD, sc, cwd='scripts', swaps=[(f'{SD}/scripts/cubes_lib.py', 'defs') + CUB])
for sc, a in ([('s1_sweeps.py', [p]) for p in ('co', 'di', 'tt')] + [('s2_di_lattice.py', []), ('s3_tt.py', []), ('s4_og_dharma.py', []),
              ('s4b_og_lattice.py', [])] + [('s4c_relatives.py', [p]) for p in 'LG'] + [('s5_fourd.py', [])]
              + [('s6_cycles.py', [p]) for p in ('co', 'di', 'tt')] + [('s7_hyper.py', []), ('s8_rd_to.py', [])]):
    case(f'dual-pairs-{sc[:-3]}{"-" + a[0] if a else ""}', 'G4', DP, sc, a, cwd='scripts', swaps=[(f'{DP}/scripts/cubes_lib.py', 'defs') + CUB])

# ---- G5 + G6: get-mixing (mixlib.py Q in the golden basis, zsurf.py Z[phi])
MSW = [(f'{MIX}/scripts/mixlib.py', 'defs', 'mixlib_Q.py', ['Q']), (f'{MIX}/scripts/zsurf.py', 'defs') + ZS]
KI = ['../' + K10, 'data/inchbald-source.json']
for nm, sc, a, lg in [('pilot_lib', 'pilot_lib.py', KI, 'pilot_lib'), ('layers', 'layers.py', KI + ['data/layers.json'], 'layers'),
                      ('pilot-patch', 'patch.py', KI + ['data/layers.json', 'ABAAB', '3', 'data/pilot-patch.json'], 'pilot-patch'),
                      ('patch-abc', 'patch.py', KI + ['data/layers.json', 'ACBCCABBA', '4', 'data/patch-abc.json'], 'patch-abc'),
                      ('patch-fibonacci', 'patch.py', KI + ['data/layers.json', 'ABAABABAABAAB', '4', 'data/patch-fibonacci.json'], 'patch-fibonacci'),
                      ('free-patch-A2', 'free_patch.py', KI + ['7', '3', 'data/free-patch-A2.json', 'A2'], 'free-patch-A2'),
                      ('free-patch-AB', 'free_patch.py', KI + ['7', '3', 'data/free-patch-AB.json', 'AB'], 'free-patch-AB'),
                      ('decorated', 'decorated_lattice.py', KI + ['data/layers.json', 'data/decorated.json'], 'decorated'),
                      ('decorated-sft', 'decorated_sft.py', KI + ['data/decorated.json', 'data/decorated-sft.json'], 'decorated-sft')]:
    case(f'get-mixing-{nm}', 'G5+G6', MIX, 'scripts/' + sc, a, log=f'data/{lg}.log', swaps=MSW)

# ---- G6: grunbaum-k10 (zsurf.py), get-palomar (getgeom.py and the k10 zsurf.py)
KSW = [(f'{K10}/scripts/zsurf.py', 'defs') + ZS]
for nm, sc, a, lg in [('vclass3', 'vclass3.py', ['data/vclass3.json'], 'vclass3'), ('search6-pilot', 'k10_search.py', ['6', '3', 'data/search6-pilot.json'], 'search6-pilot'),
                      ('cover6', 'cover_surface.py', ['data/search6.json', 'data/cover6.json'], 'cover6'),
                      ('cover-gnomon', 'cover_surface.py', ['data/gnomon.json', 'data/cover-gnomon.json'], 'cover-gnomon'),
                      ('verify', 'verify_k10.py', ['data/tile12.json', 'data/search6.json', 'data/verify.json'], 'verify'),
                      ('gnomon-sources', 'gnomon_source.py', [], 'gnomon-sources')]:
    case(f'grunbaum-k10-{nm}', 'G6', K10, 'scripts/' + sc, a, log=f'data/{lg}.log', swaps=KSW)
GP = '2026-11-17-get-palomar'
case('get-palomar-gen_data', 'G6', GP, 'gen_data.py', cwd='scripts', copies=[K10],
     swaps=KSW + [(f'{GP}/scripts/getgeom.py', 'defs', 'getgeom_zphi.py', ['zadd', 'zsub', 'zneg', 'zmul', 'zsign'])])

# ---- G7 (and G2: exactlib QF): atoms-missing, atoms-missing-2 (exactlib.py QF, KC, AlgField, RF)
for nm in ('build_keyed', 'build_bodhi_frog', 'build_closed', 'build_dharma2', 'build_icosa', 'build_julias', 'build_narcissus', 'build_star_og'):
    case(f'atoms-missing-2-{nm}', 'G7+G2', AM2, nm + '.py', cwd='scripts', log=f'scripts/{nm}.log', swaps=[(f'{AM2}/scripts/exactlib.py', 'defs') + EXL])
for nm, a, lg in [('build_dharma', [], 'build_dharma'), ('build_early', [], 'build_early'), ('build_hexoct', [], 'build_hexoct'),
                  ('build_octet', ['gbpc', 'bull', 'keyed', 'dented', 'w', 'tetartoid', 'mg', 'fill1', 'fill2', 'fill34'], 'build_octet')] + \
                 [('build_mine', [p], f'build_mine_{p}') for p in ('shield', 'xy', 'towers', 'polar')]:
    case(f'atoms-missing-{lg}', 'G7+G2', AM, nm + '.py', a, cwd='scripts', log=f'scripts/{lg}.log', swaps=[(f'{AM}/scripts/exactlib.py', 'defs') + EXL])
