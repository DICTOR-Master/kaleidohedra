#!/usr/bin/env python3
"""Step 3: match each work against DICTO's reference library.

Reads data/works.json and every manifest of ~/Documents/kaleidohedra-references
(root table, papers/, history/, bridges/, expansion/, cited/); writes
data/matched.json with, per work, status = held | link | missing | own and the
library entry it matched.

Match: same arXiv id, DOI or US patent number; same Wikipedia article; or
same first author + year (±1) with title words agreeing (≥ 0.5).

Run: python3 -I scripts/match.py
"""
import json
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalise import fold, sim, words, DOI, clean_doi  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
LIB = os.path.expanduser("~/Documents/kaleidohedra-references")


def names(a):
    return a if isinstance(a, str) else ", ".join(a or [])


def surname(auth):
    a = names(auth).split(",")[0].split(" and ")[0].strip()
    toks = [t for t in re.findall(r"[^\s.]+", a) if len(t) > 1]
    return fold(toks[-1]) if toks else ""


def lib_entries():
    out = []

    def push(e, d, sect):
        blob = " ".join(str(e.get(k, "")) for k in ("url", "doi_or_url", "source_url", "venue", "edition_or_translator", "arxiv", "file", "title", "doi"))
        ids = {}
        m = re.search(r"arxiv\.org/(?:abs|pdf)/([\w./-]+?)(?:v\d+)?(?:\.pdf)?(?:$|\s)", blob) or re.search(r"arXiv[: ]+((?:\d{4}\.\d{4,5})|(?:[a-z\-]+/\d{7}))", blob)
        if e.get("arxiv"):
            ids["arxiv"] = e["arxiv"]
        elif m:
            ids["arxiv"] = m.group(1)
        dm = DOI.search(blob)
        if dm:
            ids["doi"] = clean_doi(dm.group(1))
        pm = re.search(r"US\s?(\d{7,8})|US\s?(\d{1,2},\d{3},\d{3})", blob)
        if pm:
            ids["patent"] = "US" + (pm.group(1) or pm.group(2)).replace(",", "")
        if "wikipedia" in blob.lower() or str(e.get("file", "")).startswith("Wikipedia-"):
            um = re.search(r"en\.wikipedia\.org/wiki/([^\s#]+)", blob)
            t = urllib.parse.unquote(um.group(1)).replace("_", " ") if um else re.sub(r"\s*\(.*?\)\s*$", "", e.get("title", ""))
            ids["wiki"] = fold(t).strip(" .,")
        f = e.get("file")
        held = bool(f) and os.path.exists(os.path.join(LIB, d, f))
        y = str(e.get("year", ""))[:4]
        out.append({"section": sect, "dir": d, "file": f if held else None, "title": e.get("title", ""),
                    "authors": names(e.get("authors")), "surname": surname(e.get("authors")),
                    "year": int(y) if y.isdigit() else None, "ids": ids,
                    "link": e.get("url") or e.get("doi_or_url") or e.get("source_url")})

    push({"file": "Grunbaum-2010-Bilinski-dodecahedron-v2-3-10.pdf", "authors": "Branko Grünbaum", "year": 2010,
          "title": "The Bilinski dodecahedron, and assorted parallelohedra, zonohedra, monohedra, isozonohedra and otherhedra"}, "", "root")
    push({"file": "Fedorov-1885-Nachala-ucheniya-o-figurah.pdf", "authors": "E. S. Fedorov", "year": 1885,
          "title": "Nachala ucheniya o figurah (Elements of the Theory of Figures)"}, "", "root")
    for e in json.load(open(os.path.join(LIB, "papers/MANIFEST.json")))["entries"]:
        push(e, "papers", "papers")
    for e in json.load(open(os.path.join(LIB, "history/MANIFEST.json"))):
        push(e, "history", "history")
    b = json.load(open(os.path.join(LIB, "bridges/MANIFEST.json")))
    for e in (b["entries"] if isinstance(b, dict) else b):
        push(e, "bridges", "bridges")
    for e in json.load(open(os.path.join(LIB, "expansion/MANIFEST.json")))["entries"]:
        push(e, "expansion", "expansion")
    # cited/ is this study's own output, so it is not matched against (the baseline is the library before it)
    return out


def match(w, lib):
    ids = w.get("ids", {})
    for k in ("arxiv", "doi", "patent", "wiki"):
        if k in ids:
            hits = [e for e in lib if e["ids"].get(k) and e["ids"][k].lower() == ids[k].lower()]
            if hits:
                return sorted(hits, key=lambda e: e["file"] is None)[0]
    t = w.get("title") or (w.get("forms") or [""])[0]
    best, score = None, 0.0
    for e in lib:
        if not w.get("surname") or e["surname"] != w["surname"]:
            continue
        if w.get("year") and e["year"] and abs(w["year"] - e["year"]) > 1:
            continue
        s = sim(t, e["title"]) if t else 0
        if len(words(e["title"])) >= 3:
            s = max([s] + [sim(f, e["title"]) - 0.1 for f in w.get("forms", [])])
        if w["key"].startswith("mention:") and w.get("year") == e["year"]:
            s = max(s, 0.5)       # a bare "Author YEAR" mention: author and year are all there is
        if s > score or (s == score and best and best["file"] is None and e["file"]):
            best, score = e, s
    return best if score >= 0.5 else None


def main():
    works = json.load(open(os.path.join(DATA, "works.json")))
    lib = lib_entries()
    counts = {}
    for w in works:
        if w["own"]:
            w["status"] = "own"
        else:
            e = match(w, lib)
            if e:
                w["status"] = "held" if e["file"] else "link"
                w["library"] = {k: e[k] for k in ("section", "dir", "file", "title", "authors", "year", "link")}
            else:
                w["status"] = "missing"
        counts[w["status"]] = counts.get(w["status"], 0) + 1
    # several works that meet the same library entry are one work: keep the fullest citation
    by_entry, keep = {}, []
    for w in works:
        lib_e = w.get("library")
        if not lib_e:
            keep.append(w)
            continue
        k = (lib_e["dir"], lib_e["file"] or "", lib_e["title"])
        if k in by_entry:
            a = by_entry[k]
            if a["key"].startswith("mention:") and not w["key"].startswith("mention:"):
                a, w = w, a
                by_entry[k] = a
                keep[keep.index(w)] = a
            for f in ("cites", "forms", "kinds"):
                a[f] += [x for x in w[f] if x not in a[f]]
            for kk, v in w["ids"].items():
                a["ids"].setdefault(kk, v)
        else:
            by_entry[k] = w
            keep.append(w)
    works = keep
    counts = {}
    for w in works:
        counts[w["status"]] = counts.get(w["status"], 0) + 1
    json.dump(works, open(os.path.join(DATA, "matched.json"), "w"), ensure_ascii=False, indent=1)
    print(f"library: {len(lib)} entries; works: {len(works)}", counts)


if __name__ == "__main__":
    main()
