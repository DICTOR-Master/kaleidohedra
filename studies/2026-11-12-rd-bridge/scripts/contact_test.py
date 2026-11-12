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
exec(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'refine_snip.py')).read())   # REFINE=n: exact-keying refinement (12 Nov)
allowed = defaultdict(set); seen = set()
for x in lab:
    for d in NB:
        y = vadd(x, d)
        if y not in lab or (lab[x], lab[y], d) in seen: continue
        seen.add((lab[x], lab[y], d)); (a, Ra), (b, Rb) = lab[x], lab[y]
        for r in Ra:
            R = ROT[r]
            for q in Rb: allowed[(a, apply(R, d))].add((b, RI[compose(ROT[q], inverse(R))]))
if os.environ.get('RULES'):                 # 12 Nov: rules = the fitting relation of the keyed RD (bumps and dents), not the marking's
    import json as _j; _K = _j.load(open(os.environ['RULES']))
    assert _K['type_labels'] == [repr(L) for L in tid], 'keyed file made from another type list'
    allowed = defaultdict(set)
    for a, e, b, q in _K['fit_relation']: allowed[(a, tuple(e))].add((b, q))
    print(f"RULES from {os.environ['RULES']}: {len(_K['fit_relation'])} fitting face pairs (keyed geometry)", flush=True)
print(f'{SCH}: {len(tid)} types, rules from level {K}', flush=True)
import itertools as _it
def partitions(items):
    if not items: yield []; return
    first, rest = items[0], items[1:]
    for p in partitions(rest):
        for i in range(len(p)): yield p[:i] + [[first] + p[i]] + p[i + 1:]
        yield [[first]] + p
TYPES = BASEL   # base label per (possibly refined) type
def options(x, own):
    """possible (type, R-index) at site x: every type label and turn whose world picture agrees with the known cubes (12 Nov: generic;
    the first version enumerated groupings of the unknown cubes and so handled sharing-only edge labels alone). A label entry
    (o, g, u, i) seen from turn R (world -> canonical) sits at cube x + R^-1(o) with chair frame R^-1 g; known cubes must match frame,
    cell and grouping (known chairs A and B never share an id with each other or with unknown cubes)."""
    cs = set(cubes_of(x)); out = set()
    for a, L in TYPES.items():
        if len(L) != len(cs) and not (len(L) == 0): continue
        for r, R in enumerate(ROT):
            Ri = inverse(R); ok = True; idmap = {}; used = set(); cub = set()
            for o, g, u, i in L:
                c = vadd(x, apply(Ri, o)); cub.add(c)
                if c not in cs: ok = False; break
                if c in own:
                    ch, gw, uw = own[c]
                    if g is not None and ((gw not in rot_frame(Ri, g)) if is_coset(g) else (compose(Ri, g) != gw)): ok = False; break
                    if u is not None and u != uw: ok = False; break
                    if i is not None:
                        if idmap.setdefault(i, ch) != ch: ok = False; break
                elif i is not None:
                    if idmap.setdefault(i, ('U', i)) != ('U', i): ok = False; break
            if ok and L and cub != cs: ok = False
            if ok and L:
                # a known chair's cubes at this site must all carry the same id
                ids = {}
                for o, g, u, i in L:
                    c = vadd(x, apply(Ri, o))
                    if c in own and i is not None and ids.setdefault(own[c][0], i) != i: ok = False; break
            if ok: out.add((a, (r,)))
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
    # Test per extra contact (12 Nov: enumerating all enclosures under 99 poses ran > 35 min silently): place chair E in the extra pose
    # beside the reference chair T and ask Kamenetsky's live() for a complete, pairwise-admissible first shell round BOTH T and E. If an
    # extra contact occurred in any tiling, that tiling would supply such a shell, so DEAD for every extra pose means no tiling obeying
    # the scheme uses a contact outside P*: it is a P*-tiling, and Theorem A applies (given whole chairs). A node-limit hit counts as live.
    Hc = HCert(C, subgroup(3, 'trivial'), Pp, node_limit=200000, use_prop=False)
    extra = sorted(Pp - Psp); live_extra = []; t3 = time.time()
    for k, e in enumerate(extra):
        if Hc.live([Hc.origin, e]): live_extra.append(e)
        print(f'PROGRESS {(k + 1) / len(extra):.2f} extra contacts, live so far {len(live_extra)} ({time.time()-t3:.0f}s)', flush=True)
    ctrl = [p for p in sorted(P0p)[:5] if not Hc.live([Hc.origin, p])]
    print(f'control: occurring contacts found live {5 - len(ctrl)} of 5', flush=True)
    print(f'extra contacts that survive a full shell round both chairs: {len(live_extra)} of {len(extra)}; node limit hit {Hc.stats["limit"]} times', flush=True)
    print('VERDICT2', 'CERTIFIED: no contact outside P* survives one full shell, so every tiling is a P*-tiling (Theorem A, given whole chairs)' if not live_extra and Hc.stats['limit'] == 0 and not ctrl else 'NOT CERTIFIED at this depth: ' + str(live_extra[:5]), flush=True)
print('FINAL ok' if P0p <= Pp else 'FINAL FAIL', flush=True)
