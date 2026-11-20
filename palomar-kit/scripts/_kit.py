"""Shared constants and helpers of the Palomar submission kit (imported by the kit's Python scripts).

Kit-wide pins, taken from the three entries that went through Palomar (Kulaichev Yantra, Dehn Canon, Grünbaum k = 10):
  PIPELINE_COMMIT  the PalomarSubmission commit their preflight workflows were pinned to;
  TOOLCHAIN, MATHLIB_REV  the Lean toolchain and Mathlib tag they were built with.
Change a pin only after checking the new value against Palomar's current documentation, and record why in CHECKLIST.md.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
TEMPLATE = KIT / "template"

PIPELINE_COMMIT = "14aa8d6b3c2f14a8540605e37144560b9a00e7e7"
PALOMAR_SUBMISSION_URL = "https://github.com/PalomarRegistry/PalomarSubmission.git"
PALOMAR_SUBMISSION_REPO = "PalomarRegistry/PalomarSubmission"
TOOLCHAIN = "leanprover/lean4:v4.35.0-rc2"
MATHLIB_REV = "v4.35.0-rc2"
STANDARD_AXIOMS = ["propext", "Quot.sound", "Classical.choice"]
REQUEST_ID_RE = re.compile(r"^[0-9a-z]{12}$")
PUBLIC_RECORD_URL = "https://data.palomar-registry.org/entries/{id}-v{version}.json"

DEFAULT_AUTHOR = {"name": "DICTO", "orcid": "0009-0001-2620-2036", "github": "DICTOR-Master"}


def load_config(path: str | Path | None) -> dict:
    """entry.toml as a dict, with `_dir` (the folder of the file, against which its relative paths resolve)"""
    if path is None:
        return {"entry": {}, "author": dict(DEFAULT_AUTHOR), "_dir": Path.cwd()}
    p = Path(path).resolve()
    cfg = tomllib.loads(p.read_text(encoding="utf-8"))
    cfg.setdefault("entry", {})
    cfg["author"] = {**DEFAULT_AUTHOR, **cfg.get("author", {})}
    cfg["_dir"] = p.parent
    return cfg


def cfg_path(cfg: dict, value: str) -> Path:
    """a path from entry.toml, resolved against the folder of entry.toml; ~ and $VARS are expanded"""
    v = Path(os.path.expandvars(os.path.expanduser(value)))
    return v if v.is_absolute() else (cfg["_dir"] / v).resolve()


def theorem_names(cfg: dict) -> list[str]:
    e = cfg["entry"]
    return [f"{e['name']}.{t}" if not t.startswith(e["name"] + ".") else t for t in e.get("theorems", [])]


def definition_names(cfg: dict) -> list[str]:
    e = cfg["entry"]
    return [f"{e['name']}.{t}" if not t.startswith(e["name"] + ".") else t for t in e.get("definitions", [])]


def noreply_email(github: str) -> str:
    """the GitHub no-reply address of the author: $PALOMAR_KIT_AUTHOR_EMAIL if set, else built from the account id that
    GitHub reports for the login (so no address is ever written into the kit)"""
    env = os.environ.get("PALOMAR_KIT_AUTHOR_EMAIL")
    if env:
        return env
    uid = subprocess.run(["gh", "api", f"users/{github}", "--jq", ".id"], capture_output=True, text=True, check=True)
    return f"{uid.stdout.strip()}+{github}@users.noreply.github.com"


def palomar_submission_dir(commit: str = PIPELINE_COMMIT) -> Path:
    """a checkout of PalomarSubmission at `commit`: $PALOMAR_SUBMISSION_DIR if set (must be at that commit), else a
    cached clone under ${XDG_CACHE_HOME:-~/.cache}/palomar-kit/ (made on first use)"""
    env = os.environ.get("PALOMAR_SUBMISSION_DIR")
    if env:
        d = Path(env)
    else:
        cache = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "palomar-kit"
        d = cache / f"PalomarSubmission-{commit[:12]}"
        if not (d / ".git").exists():
            cache.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "clone", "-q", PALOMAR_SUBMISSION_URL, str(d)], check=True)
            subprocess.run(["git", "-C", str(d), "checkout", "-q", commit], check=True)
    head = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if head != commit:
        sys.exit(f"PalomarSubmission checkout {d} is at {head or '?'}, not the pinned {commit}")
    return d


def strip_lean_comments(text: str) -> str:
    """Lean source with comments (line, block, doc; nested) and string literals blanked, line structure kept"""
    out, i, n, depth = [], 0, len(text), 0
    while i < n:
        if depth:
            if text.startswith("/-", i):
                depth += 1; out.append("  "); i += 2
            elif text.startswith("-/", i):
                depth -= 1; out.append("  "); i += 2
            else:
                out.append("\n" if text[i] == "\n" else " "); i += 1
        elif text.startswith("/-", i):
            depth = 1; out.append("  "); i += 2
        elif text.startswith("--", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i)); i = j
        elif text[i] == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append('"' + " " * (min(j, n) - i - 1) + '"'); i = j + 1
        else:
            out.append(text[i]); i += 1
    return "".join(out)


def fill(text: str, cfg: dict) -> str:
    """replace the template tokens @NAME@, @TITLE@, @LIBRARY@, @REQUEST_ID@, @THEOREM1@, @THEOREMS@, @DEFINITIONS@"""
    import json
    e = cfg["entry"]
    thms = theorem_names(cfg)
    rep = {
        "@NAME@": e["name"], "@TITLE@": e.get("title", e["name"]), "@LIBRARY@": e.get("library", e["name"]),
        "@REQUEST_ID@": e.get("request_id", "xxxxxxxxxxxx"),
        "@THEOREM1@": (e.get("theorems") or ["main_theorem"])[0].split(".")[-1],
        "@THEOREMS@": json.dumps(thms, indent=4).replace("\n]", "\n  ]"),
        "@DEFINITIONS@": json.dumps(definition_names(cfg)),
    }
    for k, v in rep.items():
        text = text.replace(k, v)
    return text


def check_request_id(rid: str) -> None:
    if not REQUEST_ID_RE.match(rid or ""):
        sys.exit(f"request_id {rid!r} must be exactly 12 lowercase letters or digits (Palomar's SUBMISSION_ID_RE)")
