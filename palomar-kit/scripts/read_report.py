#!/usr/bin/env python3
"""Read a Palomar mechanical report without extracting anything to disk, find a submission's run, or read a public record.

  python3 -I read_report.py --run RUN_ID [--repo OWNER/REPO]   download the run's mechanical-report artifact (zip) into
                                                             memory and summarise it (default repo: the registry's
                                                             PalomarRegistry/PalomarSubmission; use the entry's own
                                                             repository for a preflight run)
  python3 -I read_report.py --zip FILE.zip                   summarise a report zip already saved
  python3 -I read_report.py --find OWNER/REPO [--limit 40]   find the registry's runs for a repository: Render runs by
                                                             title; Verify runs by reading each report's source field
  python3 -I read_report.py --entry PALOMAR-YYYY-MM-DD-NNNNNN [--version 1]
                                                             fetch the public record JSON
                                                             (https://data.palomar-registry.org/entries/<ID>-v<N>.json)
  --json   print the full report (or record) instead of the summary.

The summary: status, stage, phase, errors, warnings, execution profile and observed host, the kernels and every kernel
attempt with its status, ORCID validation, provenance, Challenge size, peak memory and total time from resource_usage.
Uses `gh` (logged in) for GitHub. Run with python3 -I: the zip is read with zipfile from memory."""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kit  # noqa: E402


def gh(*args: str, binary: bool = False):
    r = subprocess.run(["gh", *args], capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode()


def report_from_zip_bytes(data: bytes) -> dict:
    z = zipfile.ZipFile(io.BytesIO(data))
    names = [n for n in z.namelist() if n.endswith(".json")]
    if not names:
        sys.exit(f"no JSON in the artifact: {z.namelist()}")
    return json.loads(z.read("mechanical-report.json" if "mechanical-report.json" in names else names[0]))


def run_report(run_id: str, repo: str) -> dict | None:
    arts = json.loads(gh("api", f"repos/{repo}/actions/runs/{run_id}/artifacts"))["artifacts"]
    arts = [x for x in arts if x["name"].startswith("mechanical-report")]
    if not arts:
        return None
    if arts[0]["expired"]:
        sys.exit(f"run {run_id}: artifact {arts[0]['name']} has expired")
    return report_from_zip_bytes(gh("api", f"repos/{repo}/actions/artifacts/{arts[0]['id']}/zip", binary=True))


def gib(kib: float) -> str:
    return f"{kib / 1024 / 1024:.2f} GiB"


def summary(d: dict) -> None:
    src = d.get("source", {})
    print(f"status {d.get('status')}  stage {d.get('stage')}  phase {d.get('phase')}  checked {d.get('checked_at')}")
    print(f"source {src.get('repository')} @ {src.get('commit')}")
    sub = d.get("submission") or {}
    if sub:
        print(f"submission {json.dumps(sub)[:300]}")
    if d.get("existing_id"):
        print(f"existing entry {d['existing_id']}")
    vp = d.get("verification_profile") or {}
    host = vp.get("observed_host", {})
    print(f"profile {d.get('execution_profile')}; host {host.get('effective_cpus')} CPUs, "
          f"{host.get('memory_bytes', 0) / 2**30:.1f} GiB")
    ch = d.get("challenge", {})
    print(f"challenge {ch.get('path')}: {ch.get('lines')} lines, {ch.get('bytes')} bytes, trust {ch.get('trust_level')}")
    for e in d.get("errors", []):
        print(f"ERROR {json.dumps(e)[:500]}")
    for w in d.get("warnings", []):
        print(f"WARNING {w if isinstance(w, str) else json.dumps(w)[:500]}")
    print("kernels: " + ", ".join(k.get("name", "?") for k in d.get("kernels", [])) + " (and Lean's own kernel)")
    for k in d.get("kernel_attempts", []):
        print(f"  attempt {k.get('name')}: {k.get('status')} ({k.get('reason')}), exit {k.get('exit_code')}, "
              f"budget {k.get('budget_seconds')} s; {str(k.get('detail', '')).splitlines()[0][:200]}")
    tail = str(d.get("comparator_log_tail", "")).strip().splitlines()
    if tail:
        print("comparator log tail: " + " | ".join(tail[-4:])[:400])
    ov = d.get("orcid_validation") or {}
    recs = ov.get("records", [])
    print(f"orcid_validation: {len(recs)} record(s)" + "".join(f"\n  {json.dumps(r)[:300]}" for r in recs))
    pv = d.get("provenance") or {}
    print(f"provenance: {pv.get('result_origin')}, {pv.get('repository_role')}, "
          f"{len(pv.get('mathematical_sources', []))} sources, maintainers {pv.get('responsible_maintainers')}")
    ru = d.get("resource_usage") or []
    if ru:
        peak = max(ru, key=lambda r: r.get("max_rss_kib") or 0)
        slow = max(ru, key=lambda r: r.get("elapsed_seconds") or 0)
        total = sum(r.get("elapsed_seconds") or 0 for r in ru)
        print(f"resources: {len(ru)} phases, {total / 60:.1f} min in all; peak {gib(peak.get('max_rss_kib') or 0)} "
              f"({peak.get('phase')}); longest {slow.get('elapsed_seconds')} s ({slow.get('phase')})")
    print(f"workflow {d.get('workflow_url')}")


def find(repo_full: str, limit: int) -> None:
    runs = json.loads(gh("run", "list", "-R", _kit.PALOMAR_SUBMISSION_REPO, "-L", str(limit), "--json",
                         "databaseId,displayTitle,status,conclusion,createdAt,workflowName"))
    want = repo_full.lower()
    for r in runs:
        title = r["displayTitle"]
        hit = want in title.lower()
        if not hit and title.startswith("Verify submission") and r["status"] == "completed":
            try:
                rep = run_report(str(r["databaseId"]), _kit.PALOMAR_SUBMISSION_REPO)
            except subprocess.CalledProcessError:
                rep = None
            hit = bool(rep) and str(rep.get("source", {}).get("repository", "")).lower() == want
            if hit:
                title += f"  [{rep.get('source', {}).get('commit', '')[:7]}, report status {rep.get('status')}]"
        if hit:
            print(f"{r['databaseId']}  {r['createdAt']}  {r['status']}/{r['conclusion'] or '-'}  {title}")
    print(f"(searched the last {limit} runs of {_kit.PALOMAR_SUBMISSION_REPO}; runs still in progress have no report "
          "yet; the entry's own preflight runs: gh run list -R OWNER/REPO)")


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--run")
g.add_argument("--zip")
g.add_argument("--find")
g.add_argument("--entry")
ap.add_argument("--repo", default=_kit.PALOMAR_SUBMISSION_REPO)
ap.add_argument("--limit", type=int, default=40)
ap.add_argument("--version", type=int, default=1)
ap.add_argument("--json", action="store_true")
a = ap.parse_args()

if a.find:
    find(a.find, a.limit)
elif a.entry:
    url = _kit.PUBLIC_RECORD_URL.format(id=a.entry, version=a.version)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "palomar-kit"}), timeout=30) as f:
        rec = json.load(f)
    if a.json:
        print(json.dumps(rec, indent=1, ensure_ascii=False))
    else:
        print(f"{rec.get('id')} v{rec.get('version')}: {rec.get('title')}")
        print(f"status {rec.get('status')}; registered {rec.get('registered_at')}; first registered "
              f"{rec.get('first_registered_on')}")
        for k in ["source", "review", "verification", "trust"]:
            print(f"{k}: {json.dumps(rec.get(k), ensure_ascii=False)[:400]}")
        print(f"record {url}")
else:
    rep = report_from_zip_bytes(Path(a.zip).read_bytes()) if a.zip else run_report(a.run, a.repo)
    if rep is None:
        sys.exit(f"run {a.run}: no mechanical-report artifact (yet)")
    print(json.dumps(rep, indent=1, ensure_ascii=False) if a.json else "", end="")
    if not a.json:
        summary(rep)
