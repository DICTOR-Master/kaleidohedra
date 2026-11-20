#!/usr/bin/env python3
"""Print the answers for Palomar's submission form (submit.palomar-registry.org), each in its own block to copy.

  python3 -I form_answers.py ENTRY_DIR [--config entry.toml] [--commit SHA]

Fields: repository, commit (the full 40-character sha: --commit, else the entry's HEAD; it must be the commit whose
preflight run passed), Comparator configuration path, relationship to the work (from the preflight workflow's
authorization_relationship), existing entry id (only when entry.toml existing_entry is set: a new version of a
registered entry), and Notes (formalization.yaml project.description, as one paragraph).
Nothing is sent: DICTO fills the form with his own GitHub login."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kit  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("entry")
ap.add_argument("--config")
ap.add_argument("--commit")
a = ap.parse_args()
ROOT = Path(a.entry).resolve()
cfg = _kit.load_config(a.config)
E = cfg["entry"]


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout.strip()


owner = E.get("owner", cfg["author"]["github"])
repo = E.get("repo")
if not repo:
    m = re.search(r"github\.com[/:]([^/]+)/([^/.\s]+)", git("remote", "get-url", "origin"))
    owner, repo = (m.group(1), m.group(2)) if m else (owner, ROOT.name)
commit = a.commit or git("rev-parse", "HEAD")
if not re.fullmatch(r"[0-9a-f]{40}", commit or ""):
    sys.exit(f"commit {commit!r} is not a full 40-character sha")
if a.commit and git("cat-file", "-t", commit) != "commit":
    print(f"warning: {commit} is not in the local clone; check it is the pushed commit", file=sys.stderr)
pushed = git("branch", "-r", "--contains", commit)
if (ROOT / ".git").exists() and not pushed:
    print("warning: the commit is not on any remote-tracking branch of the local clone (not pushed, or not fetched)",
          file=sys.stderr)
wf = (ROOT / ".github/workflows/palomar-preflight.yml")
rel = "I am a responsible author or maintainer"
if wf.is_file():
    m = re.search(r'"authorization_relationship"\s*:\s*"([^"]+)"', wf.read_text(encoding="utf-8"))
    rel = m.group(1) if m else rel
comp = json.loads((ROOT / "comparator.json").read_text(encoding="utf-8"))
meta = yaml.safe_load((ROOT / "formalization.yaml").read_text(encoding="utf-8"))
notes = " ".join(str(meta["project"]["description"]).split())

fields = [
    ("Repository", f"https://github.com/{owner}/{repo}"),
    ("Commit", commit),
    ("Comparator configuration", "comparator.json"),
    ("Relationship", rel),
]
if E.get("existing_entry"):
    fields.append(("Existing entry (new version)", E["existing_entry"]))
fields.append(("Notes", notes))
print(f"# Palomar form answers: {meta['project']['name']}  ({len(comp.get('theorem_names', []))} theorems)\n")
for k, v in fields:
    print(f"{k}:\n```\n{v}\n```\n")
