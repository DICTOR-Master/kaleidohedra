# Task 1c/2: which hat orientations can ONE 3D hat piece built from RD/TRD sectors take inside one layer?
# Every sector is a vertical prism over its kite (walls vertical, 01_sectors_exact.py), so the piece over a hat
# footprint is fixed by the relief at the kite tips V.  Relief types at V (units sqrt3/12): top hi = 4, lo = 2;
# bottom deep = -4, shallow = -2.  A sector type is (top, bottom) in {hi,lo} x {hi,lo}.
# Layer contexts (by the class of the honeycomb vertex V, k mod 2):
#   c-layer (RD, above != below):   class0 (hi,lo) class1 (lo,hi)    [twin: swapped]
#   h-layer (TRD, above == below):  class0 (hi,hi) class1 (lo,lo)    [twin: swapped]
# Motions that keep a layer and map kites to kites act on the plane as kite-grid isometries g; the 3D lift
# either keeps up (g a rotation/translation) or turns the piece over (h -> -h; g a reflection) when proper;
# with mirror images allowed, also g rotation + turn-over, g reflection without turn-over.
# We test ALL 4^8 sector-type patterns on the hat footprint, in all 4 layer contexts, and collect the set of
# orientations each piece reaches; then every distinct reachable set is tested by SAT (02) for R = 2..6.
import sys, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from hatgrid import *
import importlib
sat = importlib.import_module('02_orientation_sat')

t, hk = kites_of_hat()
base = [(sat.lattice_ij(c), k) for c, k in hk]
dirs = {g: [sat.transform_kite(g, centre(*ij), k)[1] for ij, k in base] for g in LIN}
CTX = {
    'c': {0: ('hi', 'lo'), 1: ('lo', 'hi')}, 'c_twin': {0: ('lo', 'hi'), 1: ('hi', 'lo')},
    'h': {0: ('hi', 'hi'), 1: ('lo', 'lo')}, 'h_twin': {0: ('lo', 'lo'), 1: ('hi', 'hi')},
}
TYPES = list(itertools.product(('hi', 'lo'), repeat=2))
flip = lambda ty: (ty[1], ty[0])

def reach(tau, ctx, mirror):
    out = []
    for g in LIN:
        need = [CTX[ctx][d % 2] for d in dirs[g]]
        up = all(n == ty for n, ty in zip(need, tau))
        over = all(n == flip(ty) for n, ty in zip(need, tau))
        if g[0] == 'r' and (up or (mirror and over)): out.append(g)
        if g[0] == 's' and (over or (mirror and up)): out.append(g)
    return frozenset(out)

reached = {}
for mirror in (False, True):
    for tau in itertools.product(TYPES, repeat=8):
        for ctx in CTX:
            r = reach(tau, ctx, mirror)
            if r:
                reached.setdefault((mirror, r), set()).add(ctx)
name = lambda S: '{' + ' '.join(f'{k}{j}' for k, j in sorted(S)) + '}'
print('distinct reachable orientation sets (mirror allowed?, set, contexts):')
for (m, S), ctxs in sorted(reached.items(), key=lambda x: (x[0][0], len(x[0][1]))):
    print(f'  mirror={m!s:5} |S|={len(S):2} {name(S)}  contexts={sorted(ctxs)}')
# natural pieces: the RD piece (fcc) and TRD piece (hcp), identity placement in context c / h
rd_tau = tuple(CTX['c'][d % 2] for d in dirs[('r', 0)])
trd_tau = tuple(CTX['h'][d % 2] for d in dirs[('r', 0)])
for lab, tau, ctx in (('RD hat piece', rd_tau, 'c'), ('TRD hat piece', trd_tau, 'h')):
    for m in (False, True):
        print(f'{lab} in its own layer, mirror={m}: reaches {name(reach(tau, ctx, m))}; in the other layer kind: '
              f'{name(reach(tau, "h" if ctx == "c" else "c", m) | reach(tau, "h_twin" if ctx == "c" else "c_twin", m))}')
# SAT on every distinct reachable set
fails = []
results = {}
for (m, S) in sorted({k for k in reached}, key=lambda x: len(x[1])):
    key = S
    if key in results: continue
    sat.SETS['X'] = sorted(S)
    rs = {R: sat.run(R, 'X') for R in (2, 4, 6)}
    results[key] = rs
    print(f'   set {name(S)} : ' + ', '.join(f'R={R} {"SAT" if v else "UNSAT"}' for R, v in rs.items()))
full = frozenset(LIN)
ok_sets = [S for S, rs in results.items() if rs[6]]
print('sets that tile the R=6 disc:', [name(S) for S in ok_sets])
cond = all(S == full for S in ok_sets) and reach(rd_tau, 'c', True) == full and len(reach(rd_tau, 'c', False)) == 6 \
       and len(reach(trd_tau, 'h', True)) == 6
print('FINAL ok' if cond else 'FINAL FAIL: unexpected reachable sets')
