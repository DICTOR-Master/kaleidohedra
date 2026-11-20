#!/usr/bin/env python3
"""Assemble a Palomar entry repository from a finished Lean project (generalised from the Dehn Canon and Grünbaum k = 10
assemble_entry.py). Nothing is pushed, created on GitHub or submitted.

  assemble_entry.py --config entry.toml OUTDIR [--git]

From entry.toml ([entry] and [assemble]) it writes into OUTDIR:
  Challenge.lean, Solution.lean      copies of [assemble] challenge / solution;
  <library>/**.lean                  the library modules from [assemble] library_dir (recursively). With modulize = true
                                     plain Lean files are put in Palomar's module form (`module`, `public import`,
                                     `@[expose] public section`; a leading plain comment stays first), and
                                     rename_namespace = [["Old", "Old.Library"], ...] renames a namespace in the library
                                     only (the Dehn lesson: an entry namespace equal to the library's clashes);
  lakefile.toml                      from the kit template (name, library, Mathlib v4.35.0-rc2);
  lean-toolchain, LICENSE, .gitignore  from the kit template;
  lake-manifest.json                 [assemble] lake_manifest, with its "name" set to the entry name;
  comparator.json                    from [entry] theorems / definitions (three standard axioms);
  formalization.yaml, README.md      [assemble] formalization / readme;
  scripts/                           Palomar's template check-lean-sources.py and verify-comparator.sh, plus
                                     [assemble] extra_scripts;
  .github/workflows/palomar-preflight.yml   only with --git, in a second commit (as for the three entries).
and OUTDIR/SHA256SUMS (not part of the repository).

--git: initialise OUTDIR as a git repository and commit as the author (name from [author], the GitHub no-reply address
from $PALOMAR_KIT_AUTHOR_EMAIL or the GitHub account id), with plain messages and no trailer lines:
  commit 1: [assemble] commit_message (the entry files);
  commit 2: "Palomar preflight workflow (manual dispatch only, pinned pipeline commit)".
Creating the GitHub repository and pushing need DICTO's approval; the script only prints the commands."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kit  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--config", required=True)
ap.add_argument("--git", action="store_true")
ap.add_argument("outdir")
a = ap.parse_args()
cfg = _kit.load_config(a.config)
E, A = cfg["entry"], cfg.get("assemble", {})
NAME, LIB = E["name"], E.get("library", E["name"])
_kit.check_request_id(E.get("request_id", ""))
OUT = Path(a.outdir)
OUT.mkdir(parents=True, exist_ok=True)
if a.git and (OUT / ".git").exists():
    sys.exit(f"{OUT} is already a git repository; assemble into a fresh folder")
T = _kit.TEMPLATE


def modulize(text: str, renames: list) -> str:
    """leading plain comment kept; then `module`, the imports made public, `@[expose] public section`, the rest"""
    lines = text.split("\n")
    i = 0
    if lines[0].startswith("/-") and not lines[0].startswith(("/--", "/-!")):
        while not lines[i].rstrip().endswith("-/"):
            i += 1
        i += 1
    head, rest = lines[:i], lines[i:]
    k, imports = 0, []
    while k < len(rest) and (rest[k].startswith("import ") or not rest[k].strip()):
        if rest[k].startswith("import "):
            imports.append("public " + rest[k])
        k += 1
    assert not any(l.startswith("import ") for l in rest[k:]), "an import after the leading block"
    body = rest[k:]
    for old, new in renames:
        body = [l + new[len(old):] if l in (f"namespace {old}", f"end {old}") else
                re.sub(rf"\b{re.escape(old)}\.(?!{re.escape(new[len(old) + 1:])}\.)", new + ".", l) for l in body]
    return "\n".join(head + ["module", ""] + imports + ["", "@[expose] public section", ""] + body)


# library
src_lib = _kit.cfg_path(cfg, A["library_dir"])
files = sorted(src_lib.rglob("*.lean"))
assert files, f"no .lean files under {src_lib}"
for p in files:
    rel = p.relative_to(src_lib)
    t = p.read_text(encoding="utf-8")
    if A.get("modulize"):
        t = modulize(t, A.get("rename_namespace", []))
    bad = re.findall(rf"^(?:public )?import (?!Mathlib\b|{re.escape(LIB)}\.)(\S+)", t, re.M)
    assert not bad, f"{rel}: imports outside Mathlib and {LIB}: {bad}"
    (OUT / LIB / rel).parent.mkdir(parents=True, exist_ok=True)
    (OUT / LIB / rel).write_text(t, encoding="utf-8")

# entry files
shutil.copy(_kit.cfg_path(cfg, A["challenge"]), OUT / "Challenge.lean")
shutil.copy(_kit.cfg_path(cfg, A["solution"]), OUT / "Solution.lean")
shutil.copy(_kit.cfg_path(cfg, A["formalization"]), OUT / "formalization.yaml")
shutil.copy(_kit.cfg_path(cfg, A["readme"]), OUT / "README.md")
for f in ["lean-toolchain", "LICENSE"]:
    shutil.copy(T / f, OUT / f)
shutil.copy(T / "gitignore", OUT / ".gitignore")
(OUT / "lakefile.toml").write_text(_kit.fill((T / "lakefile.toml.in").read_text(encoding="utf-8"), cfg), encoding="utf-8")
(OUT / "comparator.json").write_text(_kit.fill((T / "comparator.json.in").read_text(encoding="utf-8"), cfg),
                                     encoding="utf-8")
json.loads((OUT / "comparator.json").read_text(encoding="utf-8"))
manifest_src = _kit.cfg_path(cfg, A["lake_manifest"])
manifest = json.loads(manifest_src.read_text(encoding="utf-8"))
if manifest.get("name") == NAME:  # Lake's own formatting kept byte for byte
    shutil.copy(manifest_src, OUT / "lake-manifest.json")
else:
    manifest["name"] = NAME
    (OUT / "lake-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
(OUT / "scripts").mkdir(exist_ok=True)
for f in (T / "scripts").iterdir():
    shutil.copy(f, OUT / "scripts" / f.name)
for f in A.get("extra_scripts", []):
    shutil.copy(_kit.cfg_path(cfg, f), OUT / "scripts" / Path(f).name)

# checks that need no Lean: every comparator theorem is in the Challenge and the Solution
for full in _kit.theorem_names(cfg):
    short = full.split(".", 1)[1]
    for f in ["Challenge.lean", "Solution.lean"]:
        assert re.search(rf"^theorem {re.escape(short)}\b", (OUT / f).read_text(encoding="utf-8"), re.M), (f, short)

sums = []
for p in sorted(OUT.rglob("*")):
    if p.is_file() and not ({".lake", "logs", ".git"} & set(p.relative_to(OUT).parts)) and p.name != "SHA256SUMS":
        sums.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(OUT)}")
(OUT / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
lines = sum((OUT / LIB / p.relative_to(src_lib)).read_text(encoding="utf-8").count("\n") for p in files)
print(f"library {LIB}: {len(files)} modules, {lines} lines; entry files: {len(sums)}")

if a.git:
    who = cfg["author"]
    email = _kit.noreply_email(who["github"])
    env_git = ["git", "-C", str(OUT), "-c", f"user.name={who['name']}", "-c", f"user.email={email}"]
    (OUT / "SHA256SUMS").rename(OUT.parent / f"{OUT.name}.SHA256SUMS")
    subprocess.run(["git", "init", "-q", "-b", "main", str(OUT)], check=True)
    subprocess.run(env_git + ["add", "-A"], check=True)
    msg = A.get("commit_message", f"{E.get('title', NAME)}: Lean 4 + Mathlib Palomar entry (Challenge, Solution, "
                                  f"library {LIB})")
    subprocess.run(env_git + ["commit", "-q", "-m", msg], check=True)
    wf = OUT / ".github" / "workflows" / "palomar-preflight.yml"
    wf.parent.mkdir(parents=True, exist_ok=True)
    wf.write_text(_kit.fill((T / ".github/workflows/palomar-preflight.yml.in").read_text(encoding="utf-8"), cfg),
                  encoding="utf-8")
    subprocess.run(env_git + ["add", "-A"], check=True)
    subprocess.run(env_git + ["commit", "-q", "-m", "Palomar preflight workflow (manual dispatch only, pinned pipeline "
                              "commit)"], check=True)
    subprocess.run(["git", "-C", str(OUT), "log", "--format=%h %an %s"], check=True)
    owner, repo = who["github"] if not E.get("owner") else E["owner"], E["repo"]
    print(f"""
SHA256SUMS moved next to the repository ({OUT.name}.SHA256SUMS).
Next, ONLY after DICTO approves creating the public repository:
  gh repo create {owner}/{repo} --public --source {OUT} --push
  gh workflow run palomar-preflight.yml -R {owner}/{repo}
Then: preflight_checks.py, watch_run.sh, form_answers.py (see the kit README).""")
