#!/usr/bin/env python3
"""Palomar source rules, checked over every Lean file committed in this repository (16 Nov 2026).

Rules (PalomarPolicy CONTRIBUTING.md, "Lean source requirements", and submit.palomar-registry.org/llms.txt):
  1. every regular committed `.lean` file uses the module system: `module` is its first token, after any ordinary
     comments (`--` lines and plain `/- -/` blocks; doc comments `/-! -/` and `/-- -/` are commands and must come after);
     `lakefile.lean` is exempt from this rule only;
  2. every such file has at most 10,000 physical lines (LF / CRLF each end one line; an unterminated last line counts,
     a final newline adds none);
  3. no committed `.lean` file is a symbolic link;
  4. every Challenge has at most 1,000 lines and 100 KiB. Challenges: the `challenge_module` of each committed
     comparator.json (resolved in its project folder), and every committed `Challenge.lean` or `Challenge/*.lean`.
The header scanner follows PalomarSubmission/scripts/source_requirements.py, as copied in the Palomar template's
scripts/check-lean-sources.py (the loop-equality and Kyushindo entries of this repository carry that copy).
Usage: python3 scripts/palomar_source_check.py      prints every violation, then FINAL ok or FINAL FAIL."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

COMMENT_MARKER = re.compile(r"/-|-/")
ID_LETTER_LIKE = (
    r"α-κμ-ωΑ-ΟΡ-΢Τ-Ω"
    r"ϊ-ϻἀ-῾℀-⅏\U0001d49c-\U0001d59f"
    r"À-ÖØ-öø-ſ"
)
ID_FIRST = rf"A-Za-z_{ID_LETTER_LIKE}"
ID_REST = rf"{ID_FIRST}0-9'!?₀-₉ₐ-ₜᵢ-ᵪⱼ"
IDENTIFIER_CONTINUATION = re.compile(rf"[{ID_REST}]|\.[{ID_FIRST}«]")
MAX_LINES, CH_LINES, CH_BYTES = 10_000, 1_000, 100 * 1024


def has_module_header(text):
    """`module` as the first token after blanks, `--` comments and plain block comments (Lean's header parser)"""
    i = 0
    while i < len(text):
        if text[i] in " \r\n":
            i += 1
        elif text.startswith("--", i):
            end = text.find("\n", i + 2)
            i = len(text) if end < 0 else end + 1
        elif text.startswith("/-", i) and not text.startswith(("/--", "/-!"), i):
            i += 3
            depth = 1
            while depth:
                m = COMMENT_MARKER.search(text, i)
                if m is None:
                    break
                depth += 1 if m.group() == "/-" else -1
                i = m.end()
            if depth:
                return False
        else:
            return text.startswith("module", i) and IDENTIFIER_CONTINUATION.match(text, i + 6) is None
    return False


def physical_lines(text):
    return text.count("\n") + int(bool(text) and not text.endswith("\n"))


def main():
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    staged = subprocess.check_output(["git", "-C", str(root), "ls-files", "-s", "-z"], text=True).split("\0")
    entries = [(e.split(" ", 1)[0], e.split("\t", 1)[1]) for e in staged if "\t" in e]
    lean = [(mode, p) for mode, p in entries if p.endswith(".lean") and "/.lake/" not in f"/{p}"]
    bad, worst = [], (0, "")
    for mode, p in lean:
        path = root / p
        if mode == "120000" or path.is_symlink():
            bad.append(f"{p}: a symbolic link (refused)"); continue
        if not path.is_file():
            bad.append(f"{p}: tracked but missing from the working tree"); continue
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            bad.append(f"{p}: not valid UTF-8"); continue
        n = physical_lines(text)
        worst = max(worst, (n, p))
        if path.name != "lakefile.lean" and not has_module_header(text):
            bad.append(f"{p}: does not start with `module`")
        if n > MAX_LINES:
            bad.append(f"{p}: {n} lines (> {MAX_LINES})")
    # Challenges
    tracked = {p for _, p in entries}
    challenges = {p for _, p in lean if Path(p).name == "Challenge.lean" or Path(p).parent.name == "Challenge"}
    for p in sorted(t for t in tracked if Path(t).name == "comparator.json"):
        try:
            mod = json.load(open(root / p)).get("challenge_module")
        except Exception as e:
            bad.append(f"{p}: unreadable ({e})"); continue
        if mod:
            c = str(Path(p).parent / (mod.replace(".", "/") + ".lean"))
            if c in tracked: challenges.add(c)
            else: bad.append(f"{p}: challenge_module {mod} has no committed source {c}")
    for c in sorted(challenges):
        data = (root / c).read_bytes(); n = physical_lines(data.decode("utf-8", "replace"))
        print(f"challenge {c}: {n} lines, {len(data)} bytes")
        if n > CH_LINES or len(data) > CH_BYTES:
            bad.append(f"{c}: Challenge over {CH_LINES} lines or {CH_BYTES} bytes ({n} lines, {len(data)} bytes)")
    print(f"tracked .lean files: {len(lean)}; challenges: {len(challenges)}; longest file: {worst[0]} lines ({worst[1]})")
    for b in bad:
        print("VIOLATION " + b)
    print("FINAL ok" if not bad else f"FINAL FAIL ({len(bad)} violations)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
