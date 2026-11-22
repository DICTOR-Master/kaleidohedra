#!/usr/bin/env python3
"""Write the Palomar Challenge and Solution of the DehnPackets entry from the Lean library, mechanically, so that every
definition and every theorem statement is the library text, character for character (the method of the Dehn Canon and
Dehn-Hadwiger 4D entries' gen_challenge.py).

For each item the script copies, from its library file (the folder made by prep_library.py), the item itself: its doc
comment and its text (a definition up to the first blank line; a theorem up to the `:=` that ends its statement).
Items are grouped by file, in dependency order, each group in a `section` with that file's own `open` lines
(the library's namespaces `DehnCanon.Library`, `Packets`, `PacketsGen` dropped, as the Challenge imports Mathlib
only) and the file's `variable` commands in scope at the item (Lean keeps in a definition only the variables it uses);
consecutive files with the same `open` lines and no variables (the eight generated solids) share one section.
The one text change: the qualifier `DehnCanon.Library.` is dropped (in `ConvexTiling`). In the Challenge every proof is
`sorry`; the Solution is the Challenge word for word, with the library imported and each `sorry` replaced by one line
that applies the library theorem (definitions are the same texts, so the transfer is by unfolding; a `ConvexTiling`
is rebuilt from its fields as the library's structure).

Usage: gen_challenge.py   (reads ../library; writes ../Challenge/DehnPackets.lean and ../Solution/DehnPackets.lean)
"""
import re
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
LIBDIR = PKG / "library"
NS = "DehnPackets"
SOLIDS = ["pyrD", "ti", "pyrI", "td", "dh", "ih", "to", "tco"]
GEN = {"pyrD": "GenPyrD", "ti": "GenTI", "pyrI": "GenPyrI", "td": "GenTD", "dh": "GenDH", "ih": "GenIH",
       "to": "GenTO", "tco": "GenTCO"}
DEFS = [
    ("Canon/Dehn2Poly", ["sol", "IsPoly"]),
    ("Canon/Dehn2Local", ["tcone", "linSpace", "wedgeSet", "wedgeAngle"]),
    ("Canon/Dehn2R3", ["R3"]),
    ("Angles", ["α", "β", "γ"]),
    ("Lemma2", ["ConvexTiling", "EdgeAngle"]),
    ("Pieces", ["SimilarCopy"]),
] + [(GEN[s], [f"{s}N", f"{s}B", f"{s}Set"]) for s in SOLIDS] + [("Copies", ["RationalAngles"])]
L = "Packets."
TILING = "⟨T.P, T.poly, T.nonempty_interior, T.cover, T.disjoint, T.locallyFinite⟩"
THMS = [
    ("Angles", "lemma3", f"  exact {L}lemma3 q a b c h"),
    ("Lemma2", "lemma2", f"  exact {L}lemma2 (T := {TILING}) hx h1"),
    ("Copies", "theorem4a_copies", f"  exact {L}theorem4a_copies {TILING} hk i"),
    ("Copies", "theorem4b_copies", f"  exact {L}theorem4b_copies {TILING} hk i"),
]
ORDER = ["Canon/Dehn2Poly", "Canon/Dehn2Local", "Canon/Dehn2R3", "Angles", "Lemma2", "Pieces"] + \
        [GEN[s] for s in SOLIDS] + ["Copies"]
TEXT_FIX = [("DehnCanon.Library.", "")]
DECL = re.compile(r"^(?:noncomputable )?(?:def|abbrev|theorem|lemma|structure) (\S+)")
LIBNS = re.compile(r"\b(DehnCanon\.Library|DehnCanon|Packets|PacketsGen)\b")


def src(module):
    return (LIBDIR / f"{module}.lean").read_text(encoding="utf-8").split("\n")


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
    assert not lines[j - 1].startswith("omit "), lines[j - 1]
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
    """the file's top-level open lines; an open of a library namespace is dropped (every name it opens is defined in
    the Challenge's own namespace)"""
    out = []
    for l in lines:
        if l.startswith("open "):
            if LIBNS.search(l):
                continue
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
    return dict(module=module, key=key, opens=opens(lines), vars=scope_vars(lines, j), text="\n".join(body),
                theorem=theorem)


items = [item(m, k) for m, ks in DEFS for k in ks] + [item(m, k, True) for m, k, _ in THMS]
items.sort(key=lambda it: (ORDER.index(it["module"]), find(src(it["module"]), it["key"])))
parts = []
cur_mod, cur_vars, cur_opens = None, [], None
for it in items:
    if it["module"] != cur_mod and cur_mod is not None and it["opens"] == cur_opens and not cur_vars \
            and not it["vars"]:
        parts.append("")
        parts.append(f"-- from {it['module'].split('/')[-1]}.lean")
        cur_mod = it["module"]
        parts.append(it["text"])
        continue
    if it["module"] != cur_mod:
        if cur_mod is not None:
            parts.append("\nend")
            parts.append("")
        parts.append(f"-- from {it['module'].split('/')[-1]}.lean")
        parts.append("section")
        parts += it["opens"]
        cur_mod, cur_vars, cur_opens = it["module"], [], it["opens"]
    if it["vars"][:len(cur_vars)] != cur_vars:
        raise SystemExit(f"variables of {it['key']} do not extend the section's")
    new = it["vars"][len(cur_vars):]
    if new:
        parts.append("")
        parts += new
        cur_vars = it["vars"]
    parts.append("")
    parts.append(it["text"])
parts.append("\nend")
body = "\n".join(parts)
for old, new in TEXT_FIX:
    body = body.replace(old, new)
assert not re.search(r"\b(DehnCanon|PacketsGen)\b|\bPackets\.", body), "a library name left in the Challenge"
HEADER = (PKG / "scripts" / "challenge_header.md").read_text(encoding="utf-8").rstrip("\n")
challenge = f"""module

public import Mathlib

@[expose] public section

{HEADER}

namespace {NS}

{body}

end {NS}
"""
(PKG / "Challenge" / f"{NS}.lean").write_text(challenge, encoding="utf-8")

solution = challenge.replace("public import Mathlib\n", "public import Mathlib\npublic import Packets.Copies\n", 1)
for module, key, proof in THMS:
    it = next(x for x in items if x["key"] == key)
    stmt = it["text"]
    for old, new in TEXT_FIX:
        stmt = stmt.replace(old, new)
    assert solution.count(stmt) == 1, key
    solution = solution.replace(stmt, stmt[: -len("  sorry")] + proof.lstrip("\n"), 1)
assert "sorry" not in re.sub(r"(?s)/-.*?-/", "", solution)
(PKG / "Solution" / f"{NS}.lean").write_text(solution, encoding="utf-8")
n = challenge.count("\n")
print(f"Challenge: {n} lines, {len(challenge.encode())} bytes; Solution: {solution.count(chr(10))} lines")
