# contact_test.py, DICTO 12 Nov 2026 (cutting the RD bridge down). For a coarse marking scheme whose EDGE labels use only which cubes
# share a chair (e.g. CELLFRAME), ask which ways two chairs may touch under the scheme's RD rules. For every lattice-registered
# touching pose p of chair B against chair A (proper turns; Kamenetsky's all_touching_poses), build the RDs that see A or B: centre RDs
# of their 14 cubes (labels known) and every edge RD round those cubes (cubes outside A and B belong to other chairs, every way of
# grouping them is allowed). The pose is ALLOWED if some choice of edge labels and turns obeys all the scheme's pair rules between
# these RDs (SAT). Compare the allowed set P' with Kamenetsky's certified P* (44 poses) and the hierarchical language P0 (30).
# If P0 <= P' <= P*: any RD filling that splits into whole marked chairs is a P*-tiling, hence uniquely hierarchical by his Theorem A.
# Controls: every pose of P0 must be allowed (they occur); a scheme without edge information (CELL) must allow poses outside P*.
# usage: contact_test.py <level k for the rules> <scheme>
import sys, os, itertools, time
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(here, 'vendor'))
K, SCH = sys.argv[1], sys.argv[2]; ENCL = len(sys.argv) > 3 and sys.argv[3] == 'encl'
src = open(os.path.join(here, 'cut_down.py')).read(); src = src[:src.index('def sublattices')]
sys.argv = ['cut_down.py', K, '1', '/dev/null']; exec(src)
from cert3 import language
from cert6 import closure, subgroup
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
t1 = time.time()
P0, _ = language(C, verbose=False); Pstar, hist, status, _ = closure(C, subgroup(3, 'trivial'))
print(f'P0 {len(P0)}, P* {len(Pstar)} ({status}) ({time.time()-t1:.0f}s)', flush=True)
f = SCHEMES[SCH]; lab = {}; tid = {}
for x in sites:
    L, arg = canon(f(entries(x))); lab[x] = (tid.setdefault(L, len(tid)), tuple(sorted(RI[R] for R in arg)))
allowed = defaultdict(set); seen = set()
for x in sites:
    for d in NB:
        y = vadd(x, d)
        if y not in lab or (lab[x], lab[y], d) in seen: continue
        seen.add((lab[x], lab[y], d)); (a, Ra), (b, Rb) = lab[x], lab[y]
        for r in Ra:
            R = ROT[r]
            for q in Rb: allowed[(a, apply(R, d))].add((b, RI[compose(ROT[q], inverse(R))]))
print(f'{SCH}: {len(tid)} types, rules from level {K}', flush=True)
def partitions(items):
    if not items: yield []; return
    first, rest = items[0], items[1:]
    for p in partitions(rest):
        for i in range(len(p)): yield p[:i] + [[first] + p[i]] + p[i + 1:]
        yield [[first]] + p
def options(x, own):
    """possible (type, R-index tuple) at site x given the known cubes; unknown cubes grouped every way"""
    cs = cubes_of(x); unk = [c for c in cs if c not in own]; out = set()
    for part in partitions(unk):
        cid = {c: ('U', k) for k, grp in enumerate(part) for c in grp}
        E = []
        for c in cs:
            if c in own: ch, g, u = own[c]; E.append((vsub(c, x), g, u, ch))
            else: E.append((vsub(c, x), None, None, cid[c]))
        try: E2 = f(E)
        except Exception: continue
        L, arg = canon(E2)
        if L in tid: out.add((tid[L], tuple(sorted(RI[R] for R in arg))))
    return out
def sat_for(own):
    """True if some choice of marked RDs round the chairs in own obeys every pair rule"""
    S = set()
    for c in own:
        S.add(c); S.update(vadd(c, (0, a, b)) for a in (1, -1) for b in (1, -1)); S.update(vadd(c, (a, 0, b)) for a in (1, -1) for b in (1, -1)); S.update(vadd(c, (a, b, 0)) for a in (1, -1) for b in (1, -1))
    S = sorted(S); opt = {}
    for x in S:
        ch = sorted({(a, r) for a, Rs in options(x, own) for r in Rs})      # (type, turn) choices, each once (fixed 12 Nov: a type
        opt[x] = ch                                                          # met with two turn sets had reused a variable number)
    if any(not v for v in opt.values()): return False
    vid = {}; s = Cadical153()
    for x in S:
        for a, r in opt[x]: vid[(x, a, r)] = len(vid) + 1
    top = len(vid)
    for x in S:
        lits = [vid[(x, a, r)] for a, r in opt[x]]; s.add_clause(lits)
        enc = CardEnc.atmost(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)   # (a one-literal list returns nv 0)
        for cl in enc.clauses: s.add_clause(cl)
    Sset = set(S)
    for x in S:
        for d in NB:
            y = vadd(x, d)
            if y not in Sset: continue
            for a, r in opt[x]:
                if True:
                    R = ROT[r]; ok = allowed.get((a, apply(R, d)), ())
                    s.add_clause([-vid[(x, a, r)]] + [vid[(y, b, RI[compose(ROT[q], R)])] for b, q in ok if (y, b, RI[compose(ROT[q], R)]) in vid])
    r = s.solve(); s.delete(); return r
allp = [p for p in C.all_touching_poses() if det(p[0]) == 1]
Pp = set(); t2 = time.time()
for n, p in enumerate(allp):
    own = {}
    for ch, pose in (('A', (C.id, (0, 0, 0))), ('B', p)):
        for u, c in enumerate(C.cubes(pose)): own[c] = (ch, pose[0], u)
    if sat_for(own): Pp.add(p)
    if n % 100 == 0: print(f'PROGRESS {n / len(allp):.2f} poses ({time.time()-t2:.0f}s)', flush=True)
P0p = {p for p in P0 if det(p[0]) == 1}; Psp = {p for p in Pstar if det(p[0]) == 1}
print(f'touching proper poses {len(allp)}; allowed by {SCH}: {len(Pp)}; P0 (proper) {len(P0p)} all allowed: {P0p <= Pp}; '
      f'inside P*: {Pp <= Psp}; P* proper {len(Psp)}; allowed outside P*: {len(Pp - Psp)}; P* poses refused: {len(Psp - Pp)}', flush=True)
verdict = 'CERTIFIED BY THEOREM A (given whole chairs)' if (P0p <= Pp <= Psp) else ('CONTROL FAIL (a P0 pose refused)' if not P0p <= Pp else 'NOT ENOUGH: contacts outside P* allowed')
print('VERDICT', verdict, flush=True)
if ENCL and P0p <= Pp and not Pp <= Psp:
    # Two-shell test with Kamenetsky's enclosure machinery (HCert, decoding switched off): every enclosure of the reference chair under
    # the allowed set P' that uses a contact OUTSIDE P* must be dead (no complete second shell). Every contact of a tiling lies in the
    # enclosure of one of its two chairs, so then every P'-tiling is a P*-tiling and Theorem A applies (given whole chairs).
    from cert6 import HCert
    Hc = HCert(C, subgroup(3, 'trivial'), Pp, node_limit=200000, use_prop=False)
    enc = Hc.enclosures_given(Hc.origin, []); extra = [E for E in enc if any(Hc.canon_pose(t) not in Psp for t in E)]
    print(f'enclosures under P\': {len(enc)}; using a contact outside P*: {len(extra)}', flush=True)
    live_extra = 0; t3 = time.time()
    for k, E in enumerate(extra):
        if Hc.live([Hc.origin] + list(E)): live_extra += 1
        if k % 20 == 0: print(f'PROGRESS {k / max(1, len(extra)):.2f} enclosures, live with extra so far {live_extra} ({time.time()-t3:.0f}s)', flush=True)
    print(f'live enclosures with a contact outside P*: {live_extra} of {len(extra)}; node limit hit {Hc.stats["limit"]} times', flush=True)
    print('VERDICT2', 'CERTIFIED: extra contacts never survive two shells, so every tiling is a P*-tiling (Theorem A, given whole chairs)' if live_extra == 0 and Hc.stats['limit'] == 0 else 'NOT CERTIFIED at two shells', flush=True)
print('FINAL ok' if P0p <= Pp else 'FINAL FAIL', flush=True)
