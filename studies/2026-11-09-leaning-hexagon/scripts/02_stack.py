"""02: leaning sides on plate pieces: controls, Lemma S, the subset property, and the scan.

Controls (must come out as in the vertical model): RD -> only ccc, TRD -> only hhh, RD+TRD -> all 8 words, each
with a periodic tiling found (the periodic control must be caught); leaning versions: sheared RD -> ccc + periodic.
Lemma S (exact): two cells with different corner lines meet across an interface only where the contact is flat
(all six contact heights equal).  Subset: every leaning contact is a vertical-model contact.
Scan: every relief that tiles in the vertical model x lean menu x centre lean x (proper / with mirror copies):
  V       vertical sides;
  shear   all six sides lean one way, u in {(1,0), (1,1), (2,1)} (lattice directions D, coarse, generic), centre u or 0;
  stripe  the four-side lean that fills layers (01): corners lean +-D0 + u, u = mu*D0 (mu = -4..4) and the u found in
          01 to need mirror copies, centre lean in {-2..2}^2.
Battery: patch SAT (5 layers, radius 2, every lean word, in-layer contacts, one drift per interface) then periodic
tilings with in-plane period lattice of index <= 3, any vertical period and skew, via the finite layer graph.
"""
import sys, time, json, itertools, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pieces import *
import multiprocessing as mp
Pool = mp.get_context("fork").Pool

t0 = time.time()
PILOT = 'pilot' in sys.argv
ok = True
OUT = os.path.join(HERE, '..', 'data')

REL = reliefs()
print(f'reliefs: {len(REL)}: {sorted(REL)}')
# vertical-model check that every relief tiles
for name, P in REL.items():
    r = battery([P], patch=(4, 2), maxidx=3)
    if not r['verdict'].startswith('PERIODIC'):
        print('   relief does not tile in the vertical model:', name, r['verdict'])
        ok = False


def words(res):
    return ''.join(sorted(res.get('patch_words', [])))


# ---------------------------------------------------------------- controls
Z6 = shear((0, 0))
for name, pcs, expect in (('RD', [make(*rd_piece(), Z6)], {'ccc'}), ('TRD', [make(*trd_piece(), Z6)], {'hhh'}),
                          ('RD+TRD', [make(*rd_piece(), Z6), make(*trd_piece(), Z6)],
                           {''.join(w) for w in itertools.product('ch', repeat=3)}),
                          ('RD sheared (1,0)', [make(*rd_piece(), shear((1, 0)), (1, 0))], {'ccc'}),
                          ('RD sheared (2,1)', [make(*rd_piece(), shear((2, 1)), (2, 1))], {'ccc'})):
    r = lean_battery(pcs, patch=(5, 2), maxidx=1)
    print(f'control {name}: states {r["states"]}, words {r["patch_words"]}, verdict {r["verdict"]}')
    ok &= set(r['patch_words']) == expect and r['verdict'].startswith('PERIODIC')

# ---------------------------------------------------------------- Lemma S and subset property
lemS_bad = 0
lemS_flat = 0
sub_bad = 0
for name, P in REL.items():
    for u in ((1, 0), (1, 1), (2, 1)):
        for wc in (u, (0, 0)):
            sts, _ = states_l([make(*P, shear(u), wc)], True)
            C = inter_table(sts)
            Cv = inter_table(sts, vertical=True)
            for d, Cd in C.items():
                for s in range(6):
                    for il in range(len(sts)):
                        m = Cd[s][il]
                        if m & ~Cv[(0, 0)][s][il]:
                            sub_bad += 1
                        for iu in range(len(sts)):
                            if m >> iu & 1 and dict(sts[il][2]) [D[0]] != dict(sts[iu][2])[D[0]]:
                                # different shears: the contact must be flat
                                T_ = [TRI[(s - 1) % 6], TRI[s]]
                                hs = {dict(sts[il][0][sec(T)])[v] for T in T_ for v in T}
                                if len(hs) != 1:
                                    lemS_bad += 1
                                else:
                                    lemS_flat += 1
print(f'Lemma S: contacts between different shears: {lemS_flat} flat, {lemS_bad} not flat; subset violations {sub_bad}')
ok &= lemS_bad == 0 and sub_bad == 0

# ---------------------------------------------------------------- scan
STRIPE_U = [scal(mu, D[0]) for mu in range(-4, 5)]
prof = json.load(open(os.path.join(OUT, '01_profiles.json')))
for rec in prof:
    if rec['class'].startswith('P4') and rec['mirrors']['tori'] and not rec['proper']['tori']:
        w = [tuple(x) for x in rec['w']]
        # write as stripe(u) in doubled units: 2w_s = EPS_s D0 + u ; keep if consistent
        u = sub(scal(2, w[0]), scal(EPS[0], D[0]))
        if all(add(scal(EPS[s], D[0]), u) == scal(2, w[s]) for s in range(6)):
            STRIPE_U.append(u)
        else:
            # other stripe orientation: record the lean itself (doubled)
            STRIPE_U.append(('raw', tuple(scal(2, x) for x in w)))
LEANS = [('V', shear((0, 0)), (0, 0))]
for u in ((1, 0), (1, 1), (2, 1)):
    for wc in (u, (0, 0)):
        LEANS.append((f'shear{u}', shear(u), wc))
for u in STRIPE_U:
    w = stripe(u) if not (isinstance(u, tuple) and u and u[0] == 'raw') else u[1]
    for wc in itertools.product(range(-2, 3), repeat=2):
        LEANS.append((f'stripe{u if u[0] != "raw" else "raw"}', w, wc))
if 'box2' in sys.argv:
    # second scan: every lean class of the larger box (01 box2) that fills a layer, as it is (no rescaling)
    LEANS = [('V', shear((0, 0)), (0, 0))]
    for rec in json.load(open(os.path.join(OUT, '01_profiles_box2.json'))):
        if not (rec['proper']['tori'] or rec['mirrors']['tori']):
            continue
        w = tuple(tuple(x) for x in rec['w'])
        if rec['class'].startswith('P1'):
            if w[0] != (0, 0):
                for wc in (w[0], (0, 0)):
                    LEANS.append((f'shear{w[0]}', w, wc))
        else:
            lab = 'stripe' if rec['stripe_type'] else 'pattern2D'
            for wc in itertools.product(range(-2, 3), repeat=2):
                LEANS.append((f'{lab}{tuple(rec["lam"])}', w, wc))
TASKS = [(rn, li, mir) for rn in sorted(REL) for li in range(len(LEANS)) for mir in (False, True)]
if PILOT:
    TASKS = TASKS[::max(1, len(TASKS) // 150)]
print(f'lean menu {len(LEANS)} (by type: { {k: sum(1 for l in LEANS if l[0].startswith(k)) for k in ("V", "shear", "stripe", "pattern2D")} }); tasks {len(TASKS)}')


def run(task):
    rn, li, mir = task
    lab, w, wc = LEANS[li]
    P = make(*REL[rn], w, wc)
    t = time.time()
    r = lean_battery([P], mirrors=mir, patch=(5, 2), maxidx=3)
    r.update({'relief': rn, 'lean': lab, 'w': w, 'wc': wc, 'mirrors': mir, 'sec': round(time.time() - t, 2)})
    return r


res = []
with Pool(22) as pool:
    for k, r in enumerate(pool.imap_unordered(run, TASKS, chunksize=4)):
        res.append(r)
        if k % 500 == 0:
            print(f'  heartbeat {k}/{len(TASKS)} {time.time()-t0:.0f}s', flush=True)
json.dump(res, open(os.path.join(OUT, '02_scan_pilot.json' if PILOT else
                                 ('02_scan_box2.json' if 'box2' in sys.argv else '02_scan.json')), 'w'), default=list)
summ = {}
for r in res:
    key = (r['lean'].split('(')[0] if r['lean'] != 'V' else 'V', r['mirrors'], r['verdict'].split('-')[0],
           words(r) if r['verdict'] != 'NO PATCH' else '')
    summ[key] = summ.get(key, 0) + 1
print('lean type, mirrors, verdict, patch words (length 3): count')
for k, c in sorted(summ.items()):
    print('  ', k, c)
cands = [r for r in res if r['verdict'] in ('CANDIDATE', 'UNDECIDED')]
print('CANDIDATE / UNDECIDED:', len(cands))
for r in cands[:20]:
    print('   ', r['relief'], r['lean'], r['wc'], r['mirrors'], r['verdict'], r['patch_words'], r.get('skipped'))
# periodic word sets and in-plane lattices
pw = {}
for r in res:
    if r['verdict'].startswith('PERIODIC'):
        pw[(r['lean'].split('(')[0], r['verdict'], ' '.join(r['periodic_words']))] = \
            pw.get((r['lean'].split('(')[0], r['verdict'], ' '.join(r['periodic_words'])), 0) + 1
print('periodic: lean type, smallest period lattice, words of length 4 of those tilings: count')
for k, c in sorted(pw.items()):
    print('  ', k, c)
# stripe pieces that tile: is every layer forced non-uniform?  (index-1 lattice never alive for stripes)
stripe_unif = [r for r in res if r['lean'][:6] in ('stripe', 'patter') and r['verdict'] == 'PERIODIC-1']
print('stripe pieces with a uniform periodic layer (must be 0: a stripe layer is never uniform):', len(stripe_unif))
ok &= len(stripe_unif) == 0
print(f'max battery time {max(r["sec"] for r in res):.1f}s; total {time.time()-t0:.0f}s')
print('FINAL ok' if ok else 'FINAL FAIL: a control, Lemma S, the subset property or the stripe check failed')
