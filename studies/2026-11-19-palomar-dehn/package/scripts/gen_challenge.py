#!/usr/bin/env python3
"""Write the Palomar Challenge and Solution for candidate D1 (Hilbert's third problem with the set-defined Dehn
invariant) from the Lean sources of studies 2026-11-19-lean-dehn-1 ... -10, mechanically, so that every definition and
every theorem statement is the source text, character for character.

For each item (definition or theorem) the script copies, from its source file:
  * the `open` lines of that file,
  * the `variable` commands in scope at the item (section and namespace scopes are tracked),
  * the item itself: its doc comment, an `omit ... in` line directly before it, and its text
    (a definition up to the first blank line; a theorem up to the `:=` that ends its statement).
Items are written in source order (definitions first, then the theorems) inside `namespace DehnCanon`.
In the Challenge every proof is `sorry`; the Solution is the Challenge word for word, with only the imports added
and each `sorry` replaced by the proof that transfers the library theorem `DehnCanon.Library.<name>` (the definitions
are the same texts, so the transfer is by unfolding; assemble_entry.py puts the library in namespace
`DehnCanon.Library`, since the entry's own namespace is `DehnCanon`). Doc comments are copied too; DOC_FIX lists the one wording fix
(a reference to "study 2" removed from a doc comment).

Usage: gen_challenge.py   (writes ../Challenge/DehnCanon.lean and ../Solution/DehnCanon.lean)
"""
import re
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
STUDIES = PKG.parent.parent
NS = "DehnCanon"


def src(module):
    hits = sorted(STUDIES.glob(f"2026-11-19-lean-dehn-*/lean/{module}.lean"))
    assert len(hits) == 1, (module, hits)
    return hits[0].read_text(encoding="utf-8").split("\n")


# (file, [item keys]) in dependency order; a key is a declaration name, or "instance" for the anonymous instance
DEFS = [
    ("DehnCanon1", ["ratPi", "Angle", "DehnSpace"]),
    ("Dehn2Poly", ["sol", "IsPoly"]),
    ("Dehn2Local", ["tcone", "linSpace", "wedgeSet", "wedgeAngle", "theta", "edgeAngle", "dehnSet"]),
    ("DehnCanon2", ["ScissorsCongruent"]),
    ("Dehn2R3", ["R3", "instance", "tetN", "tetraSet", "cubeN", "cubeSet"]),
    ("Dehn4Similar", ["IsSimilarCopy"]),
    ("Dehn10Edges", ["faceIn", "IsEdge", "edges", "facetNormals", "dihedral"]),
    ("Dehn10Hilbert", ["EquiComplementable"]),
]
# (file, theorem name, proof in the Solution)
THMS = [
    ("Dehn10Hilbert", "hilbert_third_problem", "  exact DehnCanon.Library.hilbert_third_problem"),
    ("Dehn10Edges", "dehnSet_eq_edge_sum", "  exact DehnCanon.Library.dehnSet_eq_edge_sum hP hint"),
    ("DehnCanon2", "dehnSet_eq_of_scissorsCongruent", "  exact DehnCanon.Library.dehnSet_eq_of_scissorsCongruent hP hQ h"),
    ("DehnCanon2", "dehnSum_eq_of_scissors",
     "  exact DehnCanon.Library.dehnSum_eq_of_scissors hp hdp hdg hp₁ hd₁ hU₁ hp₂ hd₂ hU₂"),
    ("Dehn4Similar", "similarTetra_not_scissorsCongruent_similarCube",
     "  exact DehnCanon.Library.similarTetra_not_scissorsCongruent_similarCube hT hQ"),
]

DECL = re.compile(r"^(?:noncomputable )?(?:def|abbrev|theorem|lemma|structure) (\S+)")


def find(lines, key):
    hits = [i for i, l in enumerate(lines)
            if (key == "instance" and l.startswith("instance : ")) or
            ((m := DECL.match(l)) and m.group(1) == key)]
    assert len(hits) == 1, (key, hits)
    return hits[0]


def head_start(lines, i):
    """first line of the item: its doc comment and an `omit ... in` line directly before it"""
    j = i
    if lines[j - 1].rstrip().endswith("-/"):
        while not lines[j - 1].startswith("/--"):
            j -= 1
        j -= 1
    if lines[j - 1].startswith("omit ") and lines[j - 1].rstrip().endswith(" in"):
        j -= 1
    return j


def scope_vars(lines, i):
    """the `variable` commands in scope at line i (namespaces and sections tracked)"""
    stack = [[]]
    k = 0
    while k < i:
        l = lines[k]
        if l.startswith("namespace ") or l == "section" or l.startswith("section "):
            stack.append([])
        elif l == "end" or l.startswith("end "):
            stack.pop()
        elif l.startswith("variable "):
            cmd = [l]
            while k + 1 < i and lines[k + 1].startswith("  ") and lines[k + 1].strip():
                k += 1
                cmd.append(lines[k])
            stack[-1].append("\n".join(cmd))
        k += 1
    return [v for s in stack for v in s]


def opens(lines):
    return [l for l in lines if l.startswith("open ")]


def item(module, key, theorem=False):
    lines = src(module)
    i = find(lines, key)
    j = head_start(lines, i)
    if theorem:
        e = i
        while not re.search(r":=( by)?$", lines[e].rstrip()):
            e += 1
        last = re.sub(r"\s*:=( by)?$", "", lines[e].rstrip())
        body = lines[j:e] + [last + " := by", "  sorry"]
    else:
        e = i
        while e < len(lines) and lines[e].strip():
            e += 1
        body = lines[j:e]
    return dict(module=module, key=key, opens=opens(lines), vars=scope_vars(lines, j), text="\n".join(body))


def blocks(items):
    """group consecutive items with the same file and the same variables into one section"""
    out, cur = [], None
    for it in items:
        sig = (it["module"], tuple(it["vars"]))
        if cur is None or cur[0] != sig:
            cur = (sig, [it])
            out.append(cur)
        else:
            cur[1].append(it)
    text = []
    for (module, vars_), its in out:
        part = [f"-- from {module}.lean", "section", *its[0]["opens"]]
        if vars_:
            part += ["", *vars_]
        for it in its:
            part += ["", it["text"]]
        part += ["", "end"]
        text.append("\n".join(part))
    return "\n\n".join(text)


HEADER = """/-!
# Hilbert's third problem, with the Dehn invariant of a set

**Informal statement.** In Euclidean 3-space, a convex polytope is a bounded intersection of finitely many closed
half-spaces (`IsPoly`). Two sets are *scissors congruent* (`ScissorsCongruent`) when the first is the union of
finitely many convex polytopes with pairwise disjoint interiors that, each moved by an isometry of the space
(reflections allowed), fill the second, again with pairwise disjoint interiors. They are *equicomplementable*
(`EquiComplementable`) when congruent sets of convex polytopes can be added to both, with disjoint interiors, so that
the two enlarged solids are scissors congruent.

The Dehn invariant `dehnSet P` is defined from the set `P` alone, in `ℝ ⊗[ℚ] (ℝ / ℚπ)`. At a point `x` of `P` the
directions that stay in `P` form a cone (`tcone`); the directions `v` with `v` and `-v` both in it span a space
(`linSpace`). Where that space is a line `K`, the angle at `x` is `2π · area(cone ∩ unit disc of K^⊥) / area(unit disc
of K^⊥)` (`wedgeAngle`), taken modulo rational multiples of `π`; elsewhere the class is `0` (`theta`, `edgeAngle`).
Then `dehnSet P` is the sum over the angle classes `θ` of (1-dimensional Hausdorff measure of the points with class
`θ`) ⊗ `θ`. The edges (`IsEdge`: exposed faces that are segments with two different ends), the outward unit normals of
the facets through an edge (`facetNormals`) and the interior dihedral angle (`dihedral`) are also defined from the set.

1. `hilbert_third_problem`: **Hilbert's third problem in Hilbert's words.** There are two tetrahedra `A B C D` and
   `A B C D'` on one and the same base triangle, with apexes at the same distance 1 from its plane and the same
   volume 1/6, that are neither scissors congruent nor equicomplementable.
2. `dehnSet_eq_edge_sum`: for every convex polytope with interior points, `dehnSet P` is the classical sum over the
   edges of (length) ⊗ (interior dihedral angle modulo ℚπ): Dehn's invariant in Jessen's tensor form.
3. `dehnSet_eq_of_scissorsCongruent`: **the bridge.** Scissors-congruent convex polytopes have the same `dehnSet`
   (in every 3-dimensional real inner product space).
4. `dehnSum_eq_of_scissors`: the bridge for finite unions of convex polytopes (polyhedra that need not be convex):
   the total invariant over the pieces does not depend on the dissection and is kept by scissors congruence.
5. `similarTetra_not_scissorsCongruent_similarCube`: **Dehn's theorem.** No similar copy of the regular tetrahedron
   `tetraSet` is scissors congruent to a similar copy of the cube `cubeSet 1`.

**Sources.** D. Hilbert, Mathematische Probleme, *Nachr. Ges. Wiss. Göttingen* (1900) 253–297, problem 3 (English by
M. W. Newson, *Bull. Amer. Math. Soc.* 8 (1902) 437–479); M. Dehn, Ueber den Rauminhalt, *Math. Ann.* 55 (1901)
465–478; B. Jessen, *Math. Scand.* 22 (1968) 241–256 (the tensor form). The pair of tetrahedra is that of M. Aigner and
G. M. Ziegler, *Proofs from THE BOOK*, chapter "Hilbert's third problem" (their T₁ and T₂), placed on one base.

**Scope.** Dimension 3. The pieces of a dissection are convex polytopes, finitely many, moved by isometries
(reflections included). The edge sum is for convex polytopes with interior points. Sydler's converse is not stated.

Every definition and statement below is copied, character for character, from the Lean development (studies
2026-11-19-lean-dehn-1 to -10; in this entry its namespace is `DehnCanon.Library`); the comment before each group
names its file.
-/"""


# doc-comment fixes for the Challenge (statements and definitions are never changed)
DOC_FIX = {"the Dehn invariant `dehnSet P` of study 2, defined": "the Dehn invariant `dehnSet P`, defined"}


def main():
    defs = [item(m, k) for m, ks in DEFS for k in ks]
    thms = [item(m, k, theorem=True) for m, k, _ in THMS]
    body = blocks(defs) + "\n\n" + blocks(thms)
    for a, b in DOC_FIX.items():
        assert body.count(a) == 1, a
        body = body.replace(a, b)
    challenge = "\n".join([
        "module", "", "public import Mathlib", "", "@[expose] public section", "", HEADER, "",
        f"namespace {NS}", "", body, "", f"end {NS}", ""])
    sol_body = body
    for (m, k, proof) in THMS:
        pat = re.compile(r"(theorem " + re.escape(k) + r"\b[\s\S]*?:= by\n)  sorry")
        sol_body, n = pat.subn(lambda mm: mm.group(1) + proof, sol_body, count=1)
        assert n == 1, k
    assert "sorry" not in sol_body
    solution = "\n".join([
        "module", "", "public import Mathlib", "public import DehnCanon.Dehn10Hilbert",
        "public import DehnCanon.Dehn10Edges", "", "@[expose] public section", "",
        HEADER.replace("# Hilbert's third problem, with the Dehn invariant of a set",
                       "# Hilbert's third problem, with the Dehn invariant of a set (proved)", 1), "",
        f"namespace {NS}", "", sol_body, "", f"end {NS}", ""])
    (PKG / "Challenge").mkdir(exist_ok=True)
    (PKG / "Solution").mkdir(exist_ok=True)
    (PKG / "Challenge" / "DehnCanon.lean").write_text(challenge, encoding="utf-8")
    (PKG / "Solution" / "DehnCanon.lean").write_text(solution, encoding="utf-8")
    print("Challenge:", challenge.count("\n"), "lines,", len(challenge.encode()), "bytes; theorems:",
          ", ".join(k for _, k, _ in THMS))


if __name__ == "__main__":
    main()
