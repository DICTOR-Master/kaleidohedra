"""Lean text of the 600-cell data from gen600.py's /tmp/gen600.json, as flat 8-integer records (`Q8`): L8_0..L8_9
(the 600 normals, 60 per list), V8_0..V8_3 (the 120 corners doubled, 30 per list), recs600 (per facet: four corner
indices into the corners, then the four neighbour indices into the normals). Writes /tmp/DH11Lists.txt."""
import json
d = json.load(open('/tmp/gen600.json'))


def q8(v):
    return "⟨" + ", ".join(f"{c[0]}, {c[1]}" for c in v) + "⟩"


def lst(name, typ, items, per, doc):
    rows = [", ".join(items[i:i + per]) for i in range(0, len(items), per)]
    return f"set_option maxHeartbeats 1000000 in\n/-- {doc} -/\ndef {name} : {typ} :=\n  [" + ",\n    ".join(rows) + "]\n"


out = []
L = [q8(v) for v in d['L']]
V = [q8(v) for v in d['V']]
for c in range(10):
    out.append(lst(f"L8_{c}", "List Q8", L[60 * c:60 * c + 60], 4, f"Normals {60 * c} to {60 * c + 59} (generated)."))
for c in range(4):
    out.append(lst(f"V8_{c}", "List Q8", V[30 * c:30 * c + 30], 4,
                   f"Corners {30 * c} to {30 * c + 29}, doubled: the corner is `(1/2) • gvec w.toZ` (generated)."))
R = ["[" + ", ".join(str(x) for x in r[0] + r[1]) + "]" for r in d['recs']]
out.append(lst("recs600", "List (List ℕ)", R, 6,
               "For the facet `k`: its four corners (indices into the corners) and, opposite each, the neighbouring facet "
               "(index into the normals) (generated)."))
open('/tmp/DH11Lists.txt', 'w').write("\n".join(out))

# --- symmetry and index tables (appended) ---
from collections import deque
full = [tuple(tuple(c) for c in v) for v in d['full']]
Lt = [tuple(tuple(c) for c in v) for v in d['L']]
Vt = [tuple(tuple(c) for c in v) for v in d['V']]
Li = {v: k for k, v in enumerate(Lt)}
Vi = {v: k for k, v in enumerate(Vt)}
idx = [Li[v] for v in full]
pos = [full.index(v) for v in Lt]


def neg(c):
    return (-c[0], -c[1])


GENS = [lambda v: (neg(v[0]), v[1], v[2], v[3]),      # flip coordinate 0
        lambda v: (v[1], v[2], v[0], v[3]),           # 3-cycle of coordinates 0, 1, 2
        lambda v: (v[0], v[2], v[3], v[1])]           # 3-cycle of coordinates 1, 2, 3
tabs = [[Li[g(v)] for v in Lt] for g in GENS]
# words: for each corner c a word w (list of generator numbers, applied left to right) with w(V[c]) = a representative
words, repOf = [None] * len(Vt), [None] * len(Vt)
# forward BFS from every corner to a representative found earlier
reps = []
for c in range(len(Vt)):
    seen = {c: []}
    q = deque([c])
    found = None
    while q:
        u = q.popleft()
        if u in reps or (not reps and u == c and False):
            found = u
            break
        for gi, g in enumerate(GENS):
            w = Vi[g(Vt[u])]
            if w not in seen:
                seen[w] = seen[u] + [gi]
                q.append(w)
    if found is None:
        reps.append(c)
        words[c], repOf[c] = [], c
    else:
        words[c], repOf[c] = seen[found], found
assert len(reps) <= 6, reps


def wapply(word, v):
    for gi in word:
        v = GENS[gi](v)
    return v


assert all(wapply(words[c], Vt[c]) == Vt[repOf[c]] for c in range(len(Vt)))
nl = lambda xs, per: ",\n    ".join(", ".join(str(x) for x in xs[i:i + per]) for i in range(0, len(xs), per))
extra = []
extra.append("/-- For each entry of `cell600Z`, in order, its number in the 600 normals (generated). -/\ndef idx600 : List ℕ :=\n  [" + nl(idx, 30) + "]\n")
extra.append("/-- For each of the 600 normals, a place where it occurs in `cell600Z` (generated). -/\ndef pos600 : List ℕ :=\n  [" + nl(pos, 30) + "]\n")
for gi in range(3):
    extra.append(f"/-- The image of each normal under the generator `gen {gi}` (generated). -/\ndef tab{gi} : List ℕ :=\n  [" + nl(tabs[gi], 30) + "]\n")
extra.append("/-- For each corner, a word in the generators taking it to a representative corner (generated). -/\ndef words120 : List (List ℕ) :=\n  [" + nl(["[" + ", ".join(map(str, w)) + "]" for w in words], 12) + "]\n")
extra.append("/-- The representative of each corner (generated). -/\ndef rep120 : List ℕ :=\n  [" + nl(repOf, 30) + "]\n")
extra.append(f"/-- The representative corners (generated). -/\ndef reps120 : List ℕ := [{', '.join(map(str, reps))}]\n")
open('/tmp/DH11Lists.txt', 'a').write("\n" + "\n".join(extra))
print("reps", reps, "max word", max(len(w) for w in words))
