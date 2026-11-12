# refine_snip.py, 12 Nov 2026 (aim 3, EXACT keying; DICTO "go ahead with exact keying"). exec'd by keyed_rd.py, contact_test.py and
# integrity_test.py right after they build lab/tid.
# Why: cancel-keying (bump meets dent) makes "fit" an equivalence closure: two faces that fit a common partner fit each other's
# partners. So fit = allowed exactly is possible only if the allowed face relation is a union of complete blocks; that is a property of
# the TYPES, not of the bump layout. So we refine the types: a refined label also records, on chosen faces, the type of the neighbour
# across that face and the neighbour's relative turn, in the RD's own canonical frame, minimised over the RD's own symmetric frames
# (the refined frames are those attaining the minimum: a subset of the base frames, so the base frame and chair picture stay valid).
# Modes: REFINE=n  -> n rounds, every face recorded (colour refinement);
#        REFINE_SPEC=file.json -> list of rounds, each {type id: [canonical faces to record]} (targeted; keyed_rd.py writes the next
#        round: the faces of every fit-class that holds an extra fit).
# Only sites whose 12 neighbours are labelled keep a label (the patch shrinks by one shell per round).
# A refined marking maps onto the coarse one (forget the record), so every tiling by refined types is a tiling by the coarse types:
# a certified coarse marking stays certified. The tests are rerun anyway (control).
# Output: lab (refined), tid (refined key -> id), BASEL (refined id -> BASE label L, for the chair picture).
import os as _os, json as _json, hashlib as _hl
_dg = lambda o: _hl.sha1(repr(o).encode()).hexdigest()[:16]      # content key of a type: the same at every level of the patch
if _os.environ.get('REFINE_SPEC'):
    _ROUNDS = [{k: [tuple(f) for f in v] for k, v in r.items()} for r in _json.load(open(_os.environ['REFINE_SPEC']))]
else:
    _ROUNDS = [None] * int(_os.environ.get('REFINE', '0'))
BASEL = {a: L for L, a in tid.items()}
KEY = {a: _dg(L) for L, a in tid.items()}                         # spec rounds name types by KEY (12 Nov: level-independent)
for _round, _spec in enumerate(_ROUNDS):
    _new = {}; _ntid = {}; _nbase = {}
    for x, (a, Ra) in lab.items():
        nbs = {d: vadd(x, d) for d in NB}
        if not all(y in lab for y in nbs.values()): continue
        faces = NB if _spec is None else _spec.get(KEY[a], [])
        best = None; arg = []
        for r in Ra:
            R = ROT[r]; Ri = inverse(R)
            k = tuple(sorted((f, KEY[lab[nbs[apply(Ri, f)]][0]], min(RI[compose(ROT[q], inverse(R))] for q in lab[nbs[apply(Ri, f)]][1])) for f in faces))
            if best is None or k < best: best, arg = k, [r]
            elif k == best: arg.append(r)
        key = _dg((KEY[a], best)); i = _ntid.setdefault(key, len(_ntid)); _nbase[i] = BASEL[a]
        _new[x] = (i, tuple(sorted(arg)))
    lab = _new; BASEL = _nbase; KEY = {i: key for key, i in _ntid.items()}
    tid = {('R', _round + 1, i): i for key, i in _ntid.items()}      # ids for the RULES type_labels check (same order in every script)
    print(f'REFINE round {_round + 1}: {len(tid)} types on {len(lab)} labelled sites', flush=True)
