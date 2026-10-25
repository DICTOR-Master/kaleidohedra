"""One-off helper: find DOIs on Crossref by bibliographic query (output pasted into crossref_check.py after inspection)."""
import json, sys, urllib.request, urllib.parse
qs = sys.argv[1:]
import time
for q in qs:
    time.sleep(3)
    u = "https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(q)
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "k-research (mailto:none)"}), timeout=30))
    print("==", q)
    for it in r["message"]["items"]:
        print("  ", it.get("DOI"), "|", (it.get("title") or [""])[0][:90], "|", (it.get("container-title") or [""])[0][:40], it.get("volume"), it.get("page"), it.get("issued", {}).get("date-parts"))
