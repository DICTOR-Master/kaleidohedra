# check_equiv.py (13 Nov 2026): sanity of the keyed-RD engine on the survivors (no symmetry), to rule out an engine fault:
# (1) the fit table is symmetric: F[g, d, h] == F[h, -d, g];
# (2) it is O_h-equivariant: turning the whole filling by k maps fits to fits, F[g, d, h] == F[k g, k.d, k h]
#     (this is what licenses one torus per O_h orbit and the fixed centre orientation in keysearch's ball);
# (3) every torus (not only one per orbit) of index <= IMAX: no filling, for the first survivors.
# usage: check_equiv.py <deep48 json files> IMAX NPIECES
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); J, IMAX, NP = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.argv = ['hunt.py', 'none']; exec(open(os.path.join(here, 'hunt.py')).read().split('# ---------------------------------------------------------------- modes')[0])
S = []
for f in J.split(','): S += [H for H, v in json.load(open(f)) if v == 'SURVIVOR']
ok = True; g_, d_, h_ = np.meshgrid(range(48), range(12), range(48), indexing='ij')
for H in S:
    F = fit_table(np.array(H))
    sym = (F == F[h_, np.array(NEG)[d_], g_]).all()
    eq = all((F == F[MUL[k][g_], GD[k][d_], MUL[k][h_]]).all() for k in range(48))
    eq2 = all((F == F[MUL[g_, k], GD[k][d_], MUL[h_, k]]).all() for k in range(48))
    ok &= bool(sym) and eq
    if not (sym and eq): print('FAULT', sym, eq, eq2, H); break
print('symmetric and equivariant (k g) for all', len(S), 'survivors:', ok)
allt = sublattices(IMAX); print('all tori to index', IMAX, ':', len(allt))
for si, H in enumerate(S[:NP]):
    F = fit_table(np.array(H)); hit = None
    for n, M in allt:
        if n == 1: continue
        if sat_fill(F, list(range(48)), torus_nbr(M).tolist()): hit = n; break
    print(f'survivor {si}: every torus to index {IMAX} (no orbit reduction): {"killed %d" % hit if hit else "none fills"}', flush=True)
    ok &= hit is None
print('FINAL ok' if ok else 'FINAL FAIL', flush=True)
