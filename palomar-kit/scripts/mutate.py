#!/usr/bin/env python3
"""Make one negative-control mutation of an entry copy, in place (used by run_negative_controls.sh).

  python3 -I mutate.py COPY_DIR V [--config entry.toml]

  V = a  change a numeral in a theorem statement of Challenge.lean (n becomes n + 1);
  V = b  weaken a definition of Challenge.lean (a Prop definition used in a theorem statement becomes `True`);
  V = c  replace the proof of a theorem in Solution.lean by `sorry`.
Each mutation is chosen automatically, or exactly from entry.toml [negative]: a_old/a_new, b_old/b_new (literal text,
must occur once), a_theorem (theorem whose statement is changed), c_theorem (theorem whose proof is removed).
Prints the theorem whose axioms should be checked (for c) on the last line as `CHECK <full name>`."""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kit  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("copy")
ap.add_argument("v", choices=["a", "b", "c"])
ap.add_argument("--config")
a = ap.parse_args()
D = Path(a.copy)
cfg = _kit.load_config(a.config)
N = cfg.get("negative", {})
comp = json.loads((D / "comparator.json").read_text(encoding="utf-8"))
thms = comp["theorem_names"]
ch_p, so_p = D / "Challenge.lean", D / "Solution.lean"
ch, so = ch_p.read_text(encoding="utf-8"), so_p.read_text(encoding="utf-8")


def literal(path: Path, text: str, old: str, new: str) -> None:
    if text.count(old) != 1:
        sys.exit(f"{path.name}: the configured text occurs {text.count(old)} times, not once: {old!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def statement_span(text: str, short: str) -> tuple[int, int]:
    """(start of `theorem short`, index of the `:=` that ends its statement) in comment-blanked text"""
    s = _kit.strip_lean_comments(text)
    m = re.search(rf"^(?:@\[[^\]]*\]\s*)?theorem {re.escape(short)}\b", s, re.M)
    if not m:
        sys.exit(f"theorem {short} not found")
    depth, i = 0, m.end()
    while i < len(s):
        c = s[i]
        if c in "([{⟨":
            depth += 1
        elif c in ")]}⟩":
            depth -= 1
        elif depth == 0 and s.startswith(":=", i):
            return m.start(), i
        i += 1
    sys.exit(f"end of the statement of {short} not found")


check = thms[0]
if a.v == "a":
    if N.get("a_old"):
        literal(ch_p, ch, N["a_old"], N["a_new"])
    else:
        order = [N["a_theorem"]] if N.get("a_theorem") else [t.rsplit(".", 1)[-1] for t in thms]
        for short in order:
            st, en = statement_span(ch, short)
            blank = _kit.strip_lean_comments(ch)
            m = re.search(r"(?<![\w.'₀-₉])\d+(?![\w.'])", blank[st:en])
            if m:
                i = st + m.start()
                n = int(m.group())
                ch_p.write_text(ch[:i] + str(n + 1) + ch[i + len(m.group()):], encoding="utf-8")
                print(f"control a: in {short}, numeral {n} -> {n + 1}")
                break
        else:
            sys.exit("no numeral in any theorem statement: set [negative] a_old / a_new in entry.toml")
elif a.v == "b":
    if N.get("b_old"):
        literal(ch_p, ch, N["b_old"], N["b_new"])
    else:
        blank = _kit.strip_lean_comments(ch)
        stmts = " ".join(blank[slice(*statement_span(ch, t.rsplit(".", 1)[-1]))] for t in thms)
        for m in re.finditer(r"^(?:noncomputable\s+)?def\s+([\w.'₀-₉]+)([^\n]*(?:\n(?!\n)[^\n]*)*?)\s:\sProp\s*:=", blank, re.M):
            name = m.group(1)
            if not re.search(rf"(?<![\w.']){re.escape(name.split('.')[-1])}(?![\w'])", stmts):
                continue
            end = blank.find("\n\n", m.end())
            end = len(ch) if end < 0 else end
            ch_p.write_text(ch[:m.end()] + " True" + ch[end:], encoding="utf-8")
            print(f"control b: definition {name} := True")
            break
        else:
            sys.exit("no Prop definition used in a theorem statement: set [negative] b_old / b_new in entry.toml")
else:
    short = N.get("c_theorem") or thms[0].rsplit(".", 1)[-1]
    check = next(t for t in thms if t.rsplit(".", 1)[-1] == short)
    st, en = statement_span(so, short)
    first_nl = so.index("\n", en) + 1
    nxt = re.search(r"^\S", so[first_nl:], re.M)
    end = first_nl + nxt.start() if nxt else len(so)
    so_p.write_text(so[:en] + ":= by\n  sorry\n\n" + so[end:].lstrip("\n"), encoding="utf-8")
    print(f"control c: proof of {short} replaced by sorry")
print(f"CHECK {check}")
