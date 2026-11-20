#!/usr/bin/env python3
"""Write the Palomar Challenge and Solution of the DehnHadwiger4D entry from the Lean sources, mechanically, so that
every definition and every theorem statement is the source text, character for character (the method of the Dehn
Canon entry's gen_challenge.py, study 2026-11-19-palomar-dehn).

For each item the script copies, from its source file, the item itself: its doc comment, an `omit ... in` line
directly before it, and its text (a definition up to the first blank line; a theorem up to the `:=` that ends its
statement). To keep the Challenge within 300 lines the items share two sections: the first file's (`open Real
TensorProduct`), and one for all the others, with the union of their `open` lines (the development's own namespace
`DehnCanon` dropped, since the Challenge imports Mathlib only) and one `variable` line for the space `E` (Lean keeps in
each declaration only the variables it uses). A comment names the source file before each run of items from it. Items are written in source order inside
`namespace DehnHadwiger4D`. In the Challenge every proof is `sorry`; the Solution is the Challenge word for word, with
the library imported and each `sorry` replaced by one line that applies the library theorem (the definitions are the
same texts, so the transfer is by unfolding). DOC_FIX lists the doc-comment wording fixes (no Lean text changes).

Usage: gen_challenge.py   (writes ../Challenge/DehnHadwiger4D.lean and ../Solution/DehnHadwiger4D.lean)
"""
import re
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
STUDY = PKG.parent
STUDIES = STUDY.parent
NS = "DehnHadwiger4D"


def src(module):
    if module.startswith("DH"):
        p = STUDY / "lean" / "DehnHadwiger" / f"{module}.lean"
        return p.read_text(encoding="utf-8").split("\n")
    hits = sorted(STUDIES.glob(f"2026-11-19-lean-dehn-*/lean/{module}.lean"))
    assert len(hits) == 1, (module, hits)
    return hits[0].read_text(encoding="utf-8").split("\n")


DEFS = [
    ("DehnCanon1", ["ratPi", "Angle", "DehnSpace"]),
    ("Dehn2Poly", ["sol", "IsPoly"]),
    ("Dehn2Local", ["tcone", "linSpace", "wedgeSet", "wedgeAngle"]),
    ("DehnCanon2", ["ScissorsCongruent"]),
    ("Dehn4Similar", ["IsSimilarCopy"]),
    ("DH1Def", ["thetaH", "ridgeAngle", "dehnHadwiger"]),
    ("DH6Cells", ["R4", "zvec", "tessZ", "cell16Z", "cell24Z", "tesseract", "cell16", "cell24"]),
    ("DH7Cell5", ["fiveN", "cell5"]),
    ("DH8Cell120", ["gval", "gvec", "cell120Z", "cell120"]),
    ("DH11Cell600Defs", ["orders", "orbit", "cell600Z", "cell600"]),
]
L = "DehnHadwiger."
THMS = [
    ("DH3Bridge", "dehnHadwiger_eq_of_scissorsCongruent", f"  exact {L}dehnHadwiger_eq_of_scissorsCongruent hP hQ h"),
    ("DH3Bridge", "dehnHadwigerSum_eq_of_scissors",
     f"  exact {L}dehnHadwigerSum_eq_of_scissors hp hdp hdg hp₁ hd₁ hU₁ hp₂ hd₂ hU₂"),
    ("DH6Cells", "dehnHadwiger_tesseract", f"  exact {L}dehnHadwiger_tesseract"),
    ("DH6Cells", "dehnHadwiger_cell16", f"  exact {L}dehnHadwiger_cell16"),
    ("DH6Cells", "dehnHadwiger_cell24", f"  exact {L}dehnHadwiger_cell24"),
    ("DH7Cell5", "arccos_quarter_not_ratPi", f"  exact {L}arccos_quarter_not_ratPi"),
    ("DH7Cell5", "dehnHadwiger_cell5_eq", f"  exact {L}dehnHadwiger_cell5_eq"),
    ("DH7Cell5", "dehnHadwiger_cell5_ne_zero", f"  exact {L}dehnHadwiger_cell5_ne_zero"),
    ("DH8Cell120", "dehnHadwiger_cell120", f"  exact {L}dehnHadwiger_cell120"),
    ("DH13Cell600", "dehnHadwiger_cell600_eq", f"  exact {L}dehnHadwiger_cell600_eq"),
    ("DH14Cell600Area", "dehnHadwiger_cell600_ne_zero", f"  exact {L}dehnHadwiger_cell600_ne_zero"),
    ("DH9Results", "similarCell5_not_scissorsCongruent", f"  exact {L}similarCell5_not_scissorsCongruent hT hQ"),
    ("DH15Results600", "similarCell600_not_scissorsCongruent", f"  exact {L}similarCell600_not_scissorsCongruent hT hQ"),
    ("DH15Results600", "similarCell5_not_scissorsCongruent_similarCell600",
     f"  exact {L}similarCell5_not_scissorsCongruent_similarCell600 hT hQ"),
]
VAR_E = "variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]"
# ScissorsCongruent sits in a section of DehnCanon2.lean with `[Fact (finrank ℝ E = 3)]`, which the definition does
# not use (Lean leaves it out of the definition's type); the Challenge shows only the variables it uses.
VARS_OVERRIDE = {("DehnCanon2", "ScissorsCongruent"): [VAR_E], ("Dehn4Similar", "IsSimilarCopy"): [VAR_E]}
DOC_FIX = [
    ("/-- The angle of the cone `T` around the line `K`: 2π × area(T ∩ unit disc of Kᗮ) / area(unit disc of Kᗮ). -/",
     "/-- The angle of the cone `T` around `K` (`Kᗮ` a plane): 2π × area(T ∩ unit disc of Kᗮ) / area(unit disc of Kᗮ). -/"),
]
DECL = re.compile(r"^(?:noncomputable )?(?:def|abbrev|theorem|lemma|structure) (\S+)")


def find(lines, key):
    hits = [i for i, l in enumerate(lines) if (m := DECL.match(l)) and m.group(1) == key]
    assert len(hits) == 1, (key, hits)
    return hits[0]


def head_start(lines, i):
    j = i
    if lines[j - 1].rstrip().endswith("-/"):
        while not lines[j - 1].startswith("/--"):
            j -= 1
        j -= 1
    if lines[j - 1].startswith("omit ") and lines[j - 1].rstrip().endswith(" in"):
        j -= 1
    return j


def scope_vars(lines, i):
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
    out = []
    for l in lines:
        if l.startswith("open "):
            l = re.sub(r" DehnCanon\b", "", l)
            if l.strip() not in ("open", "open scoped"):
                out.append(l)
    return out


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
    vars_ = VARS_OVERRIDE.get((module, key), scope_vars(lines, j))
    return dict(module=module, key=key, opens=opens(lines), vars=vars_, text="\n".join(body))


OPEN_REST = ["open scoped RealInnerProductSpace Pointwise", "open Set MeasureTheory Measure Module TensorProduct"]
VAR_REST = ("variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]\n"
            "  [MeasurableSpace E] [BorelSpace E]")


def blocks(items, first):
    """`first`: the items of DehnCanon1.lean in their own section with that file's opens"""
    text = []
    if first:
        part = [f"-- from {first[0]['module']}.lean", "section", *first[0]["opens"]]
        for it in first:
            part += ["", it["text"]]
        text.append("\n".join(part + ["", "end"]))
    for it in first + items:
        if it in first:
            continue
        for o in it["opens"]:
            toks, pool = o.split()[1:], OPEN_REST[0].split()[1:] if o.startswith("open scoped") else OPEN_REST[1].split()[1:]
            assert set(toks) <= set(pool), (it["key"], o)
    part, cur = ["section", *OPEN_REST, "", VAR_REST], None
    for it in items:
        if it["module"] != cur:
            part += ["", f"-- from {it['module']}.lean"]
            cur = it["module"]
        else:
            part += [""]
        part += [it["text"]]
    text.append("\n".join(part + ["", "end"]))
    return "\n\n".join(text)


HEADER = (PKG / "scripts" / "challenge_header.md").read_text(encoding="utf-8").rstrip("\n")

defs = [item(m, k) for m, ks in DEFS for k in ks]
thms = [item(m, k, theorem=True) for m, k, _ in THMS]
first = [d for d in defs if d["module"] == "DehnCanon1"]
body = blocks(defs[len(first):] + thms, first)
for old, new in DOC_FIX:
    assert body.count(old) == 1, old
    body = body.replace(old, new)
challenge = f"""module

public import Mathlib

@[expose] public section

{HEADER}

namespace {NS}

{body}

end {NS}
"""
assert "DehnCanon." not in body and "sorry" in body
(PKG / "Challenge" / f"{NS}.lean").write_text(challenge, encoding="utf-8")

solution = challenge.replace("public import Mathlib\n",
                             "public import Mathlib\npublic import DehnHadwiger.DH15Results600\n", 1)
for module, key, proof in THMS:
    it = item(module, key, theorem=True)
    stated = it["text"]
    assert solution.count(stated) == 1, key
    solution = solution.replace(stated, stated[: -len("  sorry")] + proof)
assert "sorry" not in solution.split(f"namespace {NS}", 1)[1]
(PKG / "Solution" / f"{NS}.lean").write_text(solution, encoding="utf-8")
n = challenge.count("\n")
print(f"Challenge: {n} lines, {len(challenge.encode())} bytes; {len(THMS)} theorems")
