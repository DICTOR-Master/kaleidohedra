#!/usr/bin/env python3
"""Light preflight of an assembled Palomar entry: every check that needs no Lean build (safe on the interface machine).

  python3 -I preflight_checks.py ENTRY_DIR [--config entry.toml] [--axioms-log FILE]

Checks (FAIL blocks a submission; WARN is reported; a WARN listed in entry.toml known_warnings is shown as KNOWN):
  files        the required files exist (lakefile.toml, lean-toolchain, lake-manifest.json, Challenge.lean,
               Solution.lean, comparator.json, formalization.yaml, README.md, LICENSE, preflight workflow);
  toolchain    lean-toolchain is the kit's pin;
  challenge    Challenge.lean: FAIL above Palomar's hard cap (1,000 lines or 100 KiB); WARN "challenge-size" above the
               preferred review surface (300 lines or 32 KiB), Palomar's own warning (verify_submission.py);
  sources      Palomar's own Lean source scan (source_requirements.inspect_lean_sources: module headers, 10,000-line
               limit, no symlinks, UTF-8);
  workflow     the preflight workflow: workflow_dispatch only, pinned to the kit's PalomarSubmission commit in both
               places, request_id exactly 12 lowercase letters/digits;
  comparator   comparator.json parses, no external_kernels, permitted axioms only the three standard ones, every
               theorem named (and in entry.toml, if given) exists in Challenge.lean and Solution.lean;
  metadata     Palomar's own parser at the pinned commit (submission_contract.load_formalization_metadata with a
               pathlib.Path, normalized_provenance, declared_orcids): it must load, and must report the author's ORCID;
               the source rule (original XOR source-based) is summarised; authors and maintainers are person records;
  lean         after removing comments and strings: no `sorry`/`admit` outside Challenge.lean, no `native_decide`,
               no `axiom` declaration, no `sorryAx`, anywhere; Challenge `sorry` count reported; with --axioms-log,
               every `#print axioms` line lists only propext, Classical.choice, Quot.sound;
  privacy      no home paths, private host names (this machine's name, the ~/.ssh/config hosts, the words in
               ~/.config/palomar-kit/private-words), private IP addresses or e-mail addresses in any repository file;
               in git history: author and committer use a GitHub no-reply address, no Co-Authored-By or session
               trailers.
Exit 0 iff there is no FAIL. The last line is FINAL ok or FINAL FAIL."""
from __future__ import annotations

import argparse
import json
import os
import re
import socket
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kit  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("entry")
ap.add_argument("--config")
ap.add_argument("--axioms-log")
a = ap.parse_args()
ROOT = Path(a.entry).resolve()
cfg = _kit.load_config(a.config)
KNOWN = set(cfg["entry"].get("known_warnings", []))
results: list[tuple[str, str, str]] = []


def rec(level: str, check: str, msg: str, key: str | None = None) -> None:
    if level == "WARN" and key in KNOWN:
        level = "KNOWN"
    results.append((level, check, msg))


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


# files
REQUIRED = ["lakefile.toml", "lean-toolchain", "lake-manifest.json", "Challenge.lean", "Solution.lean",
            "comparator.json", "formalization.yaml", "README.md", "LICENSE", ".github/workflows/palomar-preflight.yml"]
missing = [f for f in REQUIRED if not (ROOT / f).is_file()]
rec("FAIL" if missing else "ok", "files", f"missing: {missing}" if missing else "all required files present")
if (ROOT / "LICENSE").is_file() and "Apache License" not in text("LICENSE"):
    rec("WARN", "files", "LICENSE is not the Apache-2.0 text")

# toolchain
if (ROOT / "lean-toolchain").is_file():
    tc = text("lean-toolchain").strip()
    rec("ok" if tc == _kit.TOOLCHAIN else "WARN", "toolchain", f"{tc}" + ("" if tc == _kit.TOOLCHAIN else
        f" (kit pin {_kit.TOOLCHAIN}; Palomar needs v4.35.0-rc2 or later)"))

# comparator.json (read early: it names the Challenge module)
comp = {}
try:
    comp = json.loads(text("comparator.json"))
except Exception as err:  # noqa: BLE001
    rec("FAIL", "comparator", f"comparator.json does not parse: {err}")
ch_mod = comp.get("challenge_module", "Challenge")
ch_path = ROOT / (ch_mod.replace(".", "/") + ".lean")

# challenge size (Palomar verify_submission.py: hard caps, then the preferred review surface)
if ch_path.is_file():
    ch_bytes = ch_path.stat().st_size
    ch_lines = len(ch_path.read_text(encoding="utf-8").splitlines())
    if ch_bytes > 100 * 1024 or ch_lines > 1000:
        rec("FAIL", "challenge", f"{ch_lines} lines, {ch_bytes} bytes: over Palomar's hard cap (1,000 lines / 100 KiB)")
    elif ch_bytes > 32 * 1024 or ch_lines > 300:
        rec("WARN", "challenge", f"{ch_lines} lines, {ch_bytes} bytes: over the preferred 300 lines / 32 KiB (Palomar "
            "reports 'configured Challenge source exceeds the preferred 32 KiB / 300-line review surface')",
            "challenge-size")
    else:
        rec("ok", "challenge", f"{ch_lines} lines, {ch_bytes} bytes (preferred: at most 300 lines and 32 KiB)")

# Palomar's own parser and source scan, at the pinned commit
PS = _kit.palomar_submission_dir()
sys.path.insert(0, str(PS))
try:
    from scripts import source_requirements, submission_contract  # type: ignore  # noqa: E402
except Exception as err:  # noqa: BLE001
    rec("FAIL", "metadata", f"cannot import Palomar's parser from {PS}: {err}")
    source_requirements = submission_contract = None

if source_requirements:
    summary, issues = source_requirements.inspect_lean_sources(ROOT)
    for i in issues:
        rec("FAIL", "sources", str(i))
    if not issues:
        rec("ok", "sources", f"Palomar source scan: {summary['files_checked']} Lean files, module headers and limits ok")

# workflow
wf_path = ROOT / ".github/workflows/palomar-preflight.yml"
if wf_path.is_file():
    wf = wf_path.read_text(encoding="utf-8")
    m = re.search(r"^\s*request_id:\s*['\"]?([^'\"\s]+)", wf, re.M)
    rid = m.group(1) if m else ""
    rec("ok" if _kit.REQUEST_ID_RE.match(rid) else "FAIL", "workflow",
        f"request_id {rid!r}" + ("" if _kit.REQUEST_ID_RE.match(rid) else
                                 ": must be exactly 12 lowercase letters or digits"))
    uses = re.findall(r"submission\.yml@([0-9a-f]{40})", wf)
    pin = re.findall(r"pipeline_commit:\s*([0-9a-f]{40})", wf)
    ok = uses == [_kit.PIPELINE_COMMIT] and pin == [_kit.PIPELINE_COMMIT]
    rec("ok" if ok else "FAIL", "workflow", f"pinned to PalomarSubmission {_kit.PIPELINE_COMMIT[:7]} in uses and "
        "pipeline_commit" if ok else f"pins differ from the kit's {_kit.PIPELINE_COMMIT[:7]}: uses {uses}, "
        f"pipeline_commit {pin}")
    triggers = re.search(r"^on:\s*\n((?:\s+.*\n)+?)(?=^\S)", wf, re.M)
    trig = re.findall(r"^\s+(\w+):", triggers.group(1), re.M) if triggers else []
    rec("ok" if trig == ["workflow_dispatch"] else "WARN", "workflow", f"triggers {trig} (manual dispatch only)")
    if cfg["entry"].get("request_id") and cfg["entry"]["request_id"] != rid:
        rec("WARN", "workflow", f"request_id differs from entry.toml ({cfg['entry']['request_id']!r})")

# comparator
if comp:
    if "external_kernels" in comp:
        rec("FAIL", "comparator", "external_kernels is not a submitter field; Palomar rejects it")
    ax = comp.get("permitted_axioms", [])
    rec("ok" if set(ax) <= set(_kit.STANDARD_AXIOMS) else "FAIL", "comparator", f"permitted_axioms {ax}")
    names = comp.get("theorem_names", []) + comp.get("definition_names", [])
    if a.config and cfg["entry"].get("theorems"):
        want = _kit.theorem_names(cfg)
        if comp.get("theorem_names") != want:
            rec("FAIL", "comparator", f"theorem_names differ from entry.toml: {comp.get('theorem_names')} vs {want}")
    sol_mod = comp.get("solution_module", "Solution")
    for mod in [ch_mod, sol_mod]:
        p = ROOT / (mod.replace(".", "/") + ".lean")
        if not p.is_file():
            continue
        t = _kit.strip_lean_comments(p.read_text(encoding="utf-8"))
        ns = re.findall(r"^namespace (\S+)", t, re.M)
        for full in comp.get("theorem_names", []):
            short = full.rsplit(".", 1)[-1]
            if not re.search(rf"^(?:@\[[^\]]*\]\s*)?theorem {re.escape(short)}\b", t, re.M):
                rec("FAIL", "comparator", f"{full} not found as a theorem in {p.name}")
        miss_ns = {n.rsplit(".", 1)[0] for n in names} - set(ns)
        if miss_ns:
            rec("WARN", "comparator", f"{p.name}: namespaces {sorted(miss_ns)} of the comparator names not opened")
    rec("ok", "comparator", f"{len(comp.get('theorem_names', []))} theorems, "
        f"{len(comp.get('definition_names', []))} definitions; names checked against {ch_mod} and {sol_mod}")

# metadata: Palomar's own parser
if submission_contract and (ROOT / "formalization.yaml").is_file():
    try:
        data = submission_contract.load_formalization_metadata(ROOT / "formalization.yaml")
        prov = submission_contract.normalized_provenance(data)
        orcids = submission_contract.declared_orcids(data, prov)
        want = cfg["author"]["orcid"]
        rec("ok" if want in orcids else "FAIL", "metadata",
            f"Palomar parser: result_origin {prov.get('result_origin')}, repository_role {prov.get('repository_role')}, "
            f"{len(prov.get('mathematical_sources', []))} sources, {len(prov.get('related_formalizations', []))} "
            f"related formalizations, ORCID {orcids}" + ("" if want in orcids else f" (author's ORCID {want} missing)"))
        srcs = data.get("sources", []) or []
        rels = [(s.get("type"), s.get("relationship")) for s in srcs]
        orig = [r for r in rels if r[0] == "original-proof"]
        based = [r for r in rels if r[1] in ("formalizes", "adapts", "independently-proves")]
        if orig and based:
            rec("FAIL", "metadata", "source rule: an original-proof source together with formalizes/adapts/"
                "independently-proves sources (exactly one of original or source-based)")
        else:
            rec("ok", "metadata", "source rule: " + ("ORIGINAL (one original-proof source)" if orig else
                f"SOURCE-BASED ({len(based)} formalizes/adapts/independently-proves)"))
        bad_types = sorted({s.get("type") for s in srcs} - {"paper", "book", "web discussion", "folklore",
                                                             "original-proof", "other"})
        if bad_types:
            rec("FAIL", "metadata", f"source types outside Palomar's list: {bad_types}")
        people = (data["project"].get("authors") or []) + (data["project"].get("responsible_maintainers") or [])
        if not all(isinstance(p, dict) and p.get("orcid") and p.get("github") for p in people):
            rec("WARN", "metadata", "authors / responsible_maintainers should be person records {name, orcid, github}")
    except Exception as err:  # noqa: BLE001
        rec("FAIL", "metadata", f"Palomar parser rejects formalization.yaml: {type(err).__name__}: {err}")

# lean
lean_files = [p for p in ROOT.rglob("*.lean") if not ({".lake", ".git"} & set(p.relative_to(ROOT).parts))]
lean_bad = []
ch_sorry = 0
for p in lean_files:
    rel = p.relative_to(ROOT).as_posix()
    t = _kit.strip_lean_comments(p.read_text(encoding="utf-8"))
    is_ch = p.resolve() == ch_path.resolve()
    n_sorry = len(re.findall(r"(?<![\w.'])(sorry|admit)(?![\w'])", t))
    if is_ch:
        ch_sorry = n_sorry
    elif n_sorry:
        lean_bad.append(f"{rel}: {n_sorry} sorry/admit")
    for pat, what in [(r"(?<![\w.])native_decide(?![\w'])", "native_decide"), (r"(?<![\w.])sorryAx(?![\w'])", "sorryAx"),
                      (r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*axiom\s", "axiom declaration")]:
        k = len(re.findall(pat, t, re.M))
        if k:
            lean_bad.append(f"{rel}: {k} {what}")
for b in lean_bad:
    rec("FAIL", "lean", b)
if not lean_bad:
    rec("ok", "lean", f"{len(lean_files)} Lean files: no sorry outside the Challenge, no native_decide, no axiom "
        f"declarations; Challenge has {ch_sorry} sorry ({len(comp.get('theorem_names', []))} theorems)")
if a.axioms_log:
    lines = [l for l in Path(a.axioms_log).read_text(encoding="utf-8").splitlines() if "depends on axioms" in l]
    extra = []
    for l in lines:
        got = set(re.findall(r"[\w.]+", l.split("depends on axioms", 1)[1]))
        extra += sorted(got - set(_kit.STANDARD_AXIOMS))
    rec("ok" if lines and not extra else "FAIL", "lean", f"--axioms-log: {len(lines)} theorems; "
        + (f"non-standard axioms {sorted(set(extra))}" if extra else "only the three standard axioms"))
else:
    rec("note", "lean", "#print axioms needs a build: run it on the compute host and pass its output with --axioms-log")

# privacy
private = {socket.gethostname()}
ssh = Path.home() / ".ssh" / "config"
if ssh.is_file():
    for l in ssh.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"\s*(Host|HostName)\s+(.*)", l, re.I)
        if m:
            private |= {w for w in m.group(2).split() if "*" not in w and "?" not in w}
words_file = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "palomar-kit" / "private-words"
if words_file.is_file():
    private |= {w.strip() for w in words_file.read_text(encoding="utf-8").splitlines() if w.strip()}
private |= {w for w in os.environ.get("PALOMAR_KIT_PRIVATE_WORDS", "").split(",") if w}
private = {w for w in private if len(w) >= 6 and not re.fullmatch(r"[\d.]+", w)}
PATTERNS = [
    (re.compile(r"/home/[A-Za-z0-9_.-]+|/Users/[A-Za-z0-9_.-]+|[A-Za-z]:\\Users\\|/tmp/claude-\d+"), "home path"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"), "e-mail address"),
    (re.compile(r"\b(?:192\.168|10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b"), "private IP address"),
]
if private:
    PATTERNS.append((re.compile("|".join(re.escape(w) for w in sorted(private, key=len, reverse=True)), re.I),
                     "private host name"))
is_git = (ROOT / ".git").exists()
if is_git:
    listed = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                            capture_output=True, text=True, check=True).stdout.split("\0")
    repo_files = [ROOT / f for f in listed if f and (ROOT / f).is_file()]
else:
    repo_files = [p for p in ROOT.rglob("*") if p.is_file()
                  and not ({".lake", ".git", "logs"} & set(p.relative_to(ROOT).parts)) and p.name != "SHA256SUMS"]
hits = []
for p in repo_files:
    try:
        t = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    for rx, what in PATTERNS:
        for m in rx.finditer(t):
            line = t.count("\n", 0, m.start()) + 1
            hits.append(f"{p.relative_to(ROOT)}:{line}: {what}")  # the match itself is not printed
for h in hits[:30]:
    rec("FAIL", "privacy", h)
if len(hits) > 30:
    rec("FAIL", "privacy", f"... and {len(hits) - 30} more")
if not hits:
    rec("ok", "privacy", f"{len(repo_files)} files: no home paths, host names, private IPs or e-mail addresses "
        f"({len(private)} private words checked)")
if is_git:
    log = subprocess.run(["git", "-C", str(ROOT), "log", "--format=%H%x1f%ae%x1f%ce%x1f%an%x1f%B%x1e"],
                         capture_output=True, text=True).stdout
    commits = [c.strip("\n").split("\x1f") for c in log.split("\x1e") if c.strip()]
    bad = []
    for h, ae, ce, an, body in commits:
        if not ae.endswith("@users.noreply.github.com") or not ce.endswith("@users.noreply.github.com"):
            bad.append(f"{h[:7]}: author/committer address is not a GitHub no-reply address")
        if re.search(r"^(Co-Authored-By|Claude-Session|Signed-off-by):|Generated with", body, re.I | re.M):
            bad.append(f"{h[:7]}: trailer line in the message")
        if an != cfg["author"]["name"]:
            bad.append(f"{h[:7]}: author name {an!r}, not {cfg['author']['name']!r}")
    for b in bad:
        rec("FAIL", "privacy", "git history " + b)
    if not bad:
        rec("ok", "privacy", f"git history: {len(commits)} commits, author {cfg['author']['name']}, no-reply "
            "addresses, no trailers")

print(f"Palomar preflight (light) of {ROOT.name}; PalomarSubmission {_kit.PIPELINE_COMMIT[:7]}")
for level, check, msg in results:
    print(f"  {level:5} {check:10} {msg}")
nf = sum(1 for r in results if r[0] == "FAIL")
nw = sum(1 for r in results if r[0] == "WARN")
nk = sum(1 for r in results if r[0] == "KNOWN")
print(f"{nf} FAIL, {nw} WARN, {nk} known warning(s)")
print("FINAL ok" if nf == 0 else "FINAL FAIL")
sys.exit(1 if nf else 0)
