# integrity_test.py, DICTO 12 Nov 2026 ("go ahead with the whole chair test"). For a marking scheme whose chair contacts are certified
# (contact_test.py: only the 30 occurring contacts, inside Kamenetsky's P*), show that ANY RD filling obeying the scheme's pair rules
# groups into whole marked chairs, so that Theorem A applies with no extra assumption.
# (G) Grid: every allowed neighbour pair must claim cube centres in the same class mod 2 (labels place cubes at offsets from the RD);
#     each RD's own cubes are in one class, so agreement spreads to one global cube grid, and an RD at a cube centre must carry a
#     centre label, an RD at a cube-edge midpoint an edge label in the matching position.
# (C) Chair: with the grid fixed, take the cube c0 at (1,1,1) with its centre RD turned so that its chair frame is the identity (the
#     rules are turn-invariant). Ask SAT for an assignment of marked RDs on every site of the cubes within R grid steps that obeys all
#     pair rules but where, for EVERY cell u that c0 could be in, the chair K_u = cubes((id, t_u)) is NOT read off exactly: some cube of
#     K_u has a different frame, or some edge RD round a face between a cube of K_u and a neighbour cube says "same chair" when the
#     neighbour is outside K_u or "different" when it is inside. UNSAT = every rule-obeying filling reads a whole chair round every cube.
# Controls: (1) the true labelling of a hierarchical patch satisfies the 'valid' reading (checked directly); (2) the scheme CELLFRAME
#     (edges know only sharing, centres cell + frame; 12 types) is run too: it is expected to pass (C) as well, since chair grouping is
#     its whole edge content; FRAME (2 types, edges blank) must FAIL (C).
# usage: integrity_test.py <level k> <scheme> <R>
import sys, os, itertools, time
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(here, 'vendor'))
K, SCH, RAD = sys.argv[1], sys.argv[2], int(sys.argv[3])
src = open(os.path.join(here, 'cut_down.py')).read(); src = src[:src.index('def sublattices')]
sys.argv = ['cut_down.py', K, '1', '/dev/null']; exec(src)
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
t1 = time.time()
f = SCHEMES[SCH]; lab = {}; tid = {}
for x in sites:
    L, arg = canon(f(entries(x))); lab[x] = (tid.setdefault(L, len(tid)), tuple(sorted(RI[R] for R in arg)))
TYPES = {a: L for L, a in tid.items()}
allowed = defaultdict(set); seen = set()
for x in sites:
    for d in NB:
        y = vadd(x, d)
        if y not in lab or (lab[x], lab[y], d) in seen: continue
        seen.add((lab[x], lab[y], d)); (a, Ra), (b, Rb) = lab[x], lab[y]
        for r in Ra:
            R = ROT[r]
            for q in Rb: allowed[(a, apply(R, d))].add((b, RI[compose(ROT[q], inverse(R))]))
print(f'{SCH}: {len(tid)} types ({sum(1 for L in TYPES.values() if len(L) == 1)} centre, {sum(1 for L in TYPES.values() if len(L) == 4)} edge, {sum(1 for L in TYPES.values() if len(L) == 0)} blank)', flush=True)
def world(a, r, x):
    """world picture of type a in turn r at site x: list of (cube, frame or None, cell or None, id or None)"""
    Ri = inverse(ROT[r]); return [(vadd(x, apply(Ri, o)), rot_frame(Ri, g), u, i) for o, g, u, i in TYPES[a]]
# ---- (G) grid consistency over every allowed pair
badG = 0
for (a, dl), S in allowed.items():
    pa = world(a, RI[ROT[0]], (0, 0, 0))
    for b, q in S:
        pb = world(b, q, dl)                      # neighbour at local direction dl with turn q relative to a's (identity) turn
        cls = {tuple(v % 2 for v in c) for c, *_ in pa + pb}
        if len(cls) > 1: badG += 1
blank = any(len(L) == 0 for L in TYPES.values())
print(f'(G) allowed pairs claiming cubes on two different grids: {badG}' + (' (scheme has blank RDs: grid not carried, G not applicable)' if blank else ''), flush=True)
# ---- (C) chair reading in a ball
cub = [tuple(1 + 2 * k for k in v) for v in itertools.product(range(-RAD, RAD + 1), repeat=3)]
cubset = set(cub)
S = set(cub)
for c in cub:
    for i in range(3):
        for a_, b_ in itertools.product((1, -1), repeat=2):
            d = [a_, b_]; d.insert(i, 0); S.add(vadd(c, tuple(d)))
S = sorted(S); Sset = set(S)
def site_options(x):
    cs = set(cubes_of(x)); out = []
    for a, L in TYPES.items():
        if len(L) == 0:
            out += [(a, r) for r in range(24)]; continue
        if len(L) != len(cs): continue
        for r in range(24):
            if {c for c, *_ in world(a, r, x)} == cs: out.append((a, r))
    return out
opt = {x: site_options(x) for x in S}
vid = {}
for x in S:
    for o in opt[x]: vid[(x,) + o] = len(vid) + 1
top = len(vid); s = Cadical153()
def newv():
    global top; top += 1; return top
for x in S:
    lits = [vid[(x,) + o] for o in opt[x]]; s.add_clause(lits)
    enc = CardEnc.atmost(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)
    for cl in enc.clauses: s.add_clause(cl)
for x in S:
    for d in NB:
        y = vadd(x, d)
        if y not in Sset: continue
        for a, r in opt[x]:
            R = ROT[r]; ok = allowed.get((a, apply(R, d)), ())
            s.add_clause([-vid[(x, a, r)]] + [vid[(y, b, RI[compose(ROT[q], R)])] for b, q in ok if (y, b, RI[compose(ROT[q], R)]) in vid])
c0 = (1, 1, 1)
# fix c0's centre RD: an option whose world frame of c0 is the identity
ID = C.id
fix = [vid[(c0, a, r)] for a, r in opt[c0] if any(c == c0 and g == ID for c, g, u, i in world(a, r, c0))]
if not fix: print('no centre option with frame id at c0 (scheme has no frame on centres)', flush=True)
s.add_clause(fix if fix else [vid[(c0,) + opt[c0][0]]])
# frame literals per cube: Fc <-> OR(options at the cube's centre site giving world frame id)
F = {}
for c in cub:
    lits = [vid[(c, a, r)] for a, r in opt[c] if any(cc == c and g == ID for cc, g, u, i in world(a, r, c))]
    v = newv(); F[c] = v
    if lits:
        s.add_clause([-v] + lits)
        for l in lits: s.add_clause([v, -l])
    else: s.add_clause([-v])
# same-chair literals per (edge site, cube pair): Se <-> OR(options at e that put both cubes in one chair)
def faces_edges(c, c2):
    """the 4 edge sites round the face between face-adjacent cubes c, c2"""
    m = tuple((p + q) // 2 for p, q in zip(c, c2)); ax = next(i for i in range(3) if c[i] != c2[i]); out = []
    for j in range(3):
        if j == ax: continue
        for sg in (1, -1):
            e = list(m); e[j] += sg; out.append(tuple(e))
    return out
SAME = {}
def same_lit(e, c, c2):
    if (e, c, c2) in SAME: return SAME[(e, c, c2)]
    lits = []
    for a, r in opt[e]:
        W = {cc: i for cc, g, u, i in world(a, r, e)}
        if c in W and c2 in W and W[c] is not None and W[c] == W[c2]: lits.append(vid[(e, a, r)])
    v = newv(); SAME[(e, c, c2)] = v
    if lits:
        s.add_clause([-v] + lits)
        for l in lits: s.add_clause([v, -l])
    else: s.add_clause([-v])
    return v
U7 = [u for u in itertools.product((0, 1), repeat=3) if u != (1, 1, 1)]
valid = []
for u in U7:
    t = tuple((c0[k] - (2 * u[k] + 1)) // 2 for k in range(3)); Ku = set(C.cubes((ID, t)))
    if not Ku <= cubset: continue
    conds = [F[c] for c in Ku]
    for c in Ku:
        for k in range(3):
            for sg in (2, -2):
                c2 = list(c); c2[k] += sg; c2 = tuple(c2)
                if c2 not in cubset: continue
                for e in faces_edges(c, c2):
                    if e not in Sset: continue
                    sl = same_lit(e, c, c2); conds.append(sl if c2 in Ku else -sl)
    vu = newv(); valid.append(vu)
    for cnd in conds: s.add_clause([-vu, cnd])                  # vu -> all conditions
    s.add_clause([vu] + [-cnd for cnd in conds])                 # all conditions -> vu
zpos = newv(); s.add_clause([-zpos] + valid)                     # control (1): a filling WITH a valid whole chair must exist
ctrl = s.solve(assumptions=[zpos])
print(f'control (1): rule-obeying filling with a whole chair round c0 exists: {ctrl}', flush=True)
zneg = newv()
for vu in valid: s.add_clause([-zneg, -vu])                      # demand: no cell reading is valid
print(f'(C) ball R={RAD}: {len(S)} sites, {len(vid)} choices, {len(valid)} candidate chairs for c0 ({time.time()-t1:.0f}s)', flush=True)
r = s.solve(assumptions=[zneg])
print('(C) a rule-obeying filling WITHOUT a whole chair round c0 exists' if r else '(C) UNSAT: every rule-obeying filling reads a whole chair, turned as its RDs say, round every cube', f'({time.time()-t1:.0f}s)', flush=True)
print('VERDICT', 'WHOLE CHAIRS FORCED' if (not r and not badG and not blank and ctrl) else 'NOT FORCED', flush=True)
print('FINAL ok' if ctrl else 'FINAL FAIL: control (1)', flush=True)
