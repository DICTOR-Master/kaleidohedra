#!/usr/bin/env python3
"""Start a new Palomar entry from the kit template (step 2 of the kit README).
  new_entry.py --config entry.toml OUTDIR
writes into OUTDIR (which must not exist): lakefile.toml, lean-toolchain, Challenge.lean, Solution.lean, comparator.json,
formalization.yaml, README.md, LICENSE, .gitignore, scripts/ (Palomar's template check-lean-sources.py and
verify-comparator.sh), .github/workflows/palomar-preflight.yml (pinned pipeline commit, the entry's request_id).
The library folder (entry.library) is created empty. Nothing is committed, created on GitHub or submitted."""
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kit  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--config", required=True)
ap.add_argument("outdir")
a = ap.parse_args()
cfg = _kit.load_config(a.config)
_kit.check_request_id(cfg["entry"].get("request_id", ""))
out = Path(a.outdir)
if out.exists():
    sys.exit(f"{out} exists; choose a new folder")
T = _kit.TEMPLATE
for src, dst in [("lakefile.toml.in", "lakefile.toml"), ("Challenge.lean.in", "Challenge.lean"),
                 ("Solution.lean.in", "Solution.lean"), ("comparator.json.in", "comparator.json"),
                 ("formalization.yaml.in", "formalization.yaml"), ("README.md.in", "README.md"),
                 (".github/workflows/palomar-preflight.yml.in", ".github/workflows/palomar-preflight.yml")]:
    (out / dst).parent.mkdir(parents=True, exist_ok=True)
    (out / dst).write_text(_kit.fill((T / src).read_text(encoding="utf-8"), cfg), encoding="utf-8")
for f in ["lean-toolchain", "LICENSE"]:
    shutil.copy(T / f, out / f)
shutil.copy(T / "gitignore", out / ".gitignore")
shutil.copytree(T / "scripts", out / "scripts")
(out / cfg["entry"].get("library", cfg["entry"]["name"])).mkdir()
print(f"new entry skeleton in {out}; next: write the library and the Challenge, then `lake update` on the compute host")
