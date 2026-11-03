#!/usr/bin/env python3
"""Step 1: pull every cited reference out of DICTO's papers and books.

Sources: papers/*/paper.src.html (else paper.html), the three early papers that
live in studies/*/paper/, and the book folders papers/book-*/.  Version
subfolders (v2, v3 ...) hold only PDFs, so paper.src.html is the newest text.

Each citation becomes one record in data/raw-references.json:
  {src, label, nums, kind, text}
kind = "ref"      an item of a References list (ol/ul items, [n] lines, tables)
       "checked"  one item of a "Sources checked" / prior-work paragraph
       "dataref"  a "References:" clause inside a "Data and code" paragraph
Paper numbers come from the dictospheres.com cards (title match).

Run: python3 -I scripts/extract.py   (from the study folder)
"""
import html
import json
import os
import re

HOME = os.path.expanduser("~")
KR = os.path.join(HOME, "k-research")
SITE = os.path.join(HOME, "dictospheres", "index.html")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

SKIP = {"collected", "plan-japanese-books", "plan-star-cores", "star-cores-results", "figures-draft",
        "proposed-batch-2026-10-20", "sa-batch-2026-10-20", "v3-batch-2026-10-20", "japanese", "intro-solids", "dicto-tiles"}
EXTRA = ["studies/2026-10-13-fused-shells/paper/paper.html",
         "studies/2026-10-14-axe-cleo-fuji/paper/paper-house.html",
         "studies/2026-10-14-fuji-family/paper/paper-house.html"]


def text(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return " ".join(html.unescape(s).split())


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", html.unescape(t).lower().replace("–", "-")).strip()


def site_numbers():
    h = open(SITE, encoding="utf-8").read()
    parts = re.split(r'<span class="num">#(\d+)</span>', h)
    out = {}
    for i in range(1, len(parts), 2):
        n = int(parts[i])
        t = text(parts[i + 1].split("</span>")[0])
        t = re.sub(r"\s*DOI 10\.\S+$", "", t)
        out.setdefault(n, t)
    return out


def sources():
    files = []
    for d in sorted(os.listdir(os.path.join(KR, "papers"))):
        p = os.path.join(KR, "papers", d)
        if d in SKIP or not os.path.isdir(p):
            continue
        for name in ("paper.src.html", "paper.html"):
            if os.path.exists(os.path.join(p, name)):
                files.append(f"papers/{d}/{name}")
                break
    return files + EXTRA


# Paper numbers (dictospheres.com cards, checked against each folder's Zenodo concept DOI).
# Folders not listed are companions without a number of their own, or books.
FOLDER_NUM = {
    "ekp": 8, "dodeca13": 13, "dicto-star": 14, "kagome-hulls": 17, "hexa": 18, "2026-10-14-axe-cleo-fuji": 19,
    "2026-10-14-fuji-family": 20, "chain-of-karma": 22, "spheres-of-dharma": 23, "bodhi-seed": 24, "spheroid-13-rd": 25,
    "thirteens": 26, "2026-10-13-fused-shells": 27, "tih": 28, "theaetetus": 29, "ocd-chorus": 30, "ogdoecontahedron": 31,
    "dharma-inside-out": 32, "both-cycles": 33, "progenitors": 34, "progenitors-2": 35, "golden-bodhi-pyrochlore": 36,
    "2026-10-18-bull-horns": 37, "2026-10-19-universal-pitet": 38, "2026-10-20-og-family-both-ways": 39,
    "2026-10-20-og-polytypes": 40, "2026-10-20-dicto-jewel": 41, "2026-10-20-dicto-sunstar": 42,
    "2026-10-21-kyushindo-cores": 43, "2026-10-21-aristotles-pyramid": 44, "2026-10-21-reuleaux-platonic": 45,
    "2026-10-22-platonic-mixes": 47, "2026-10-23-golden-split": 48, "2026-10-22-swept-dodecahedra": 49,
    "2026-10-23-exact-vs-dissection": 50, "2026-10-24-delian-bond": 51, "2026-10-25-web-of-bonds": 52,
    "2026-10-25-relay-census": 53, "2026-10-25-gnomon-polar": 54, "2026-10-25-david-goliath": 55,
    "2026-10-25-keyed-switch": 56, "2026-10-26-rule-of-halves": 57, "series-web-of-bonds": 58, "icosaxes-hexa": 59,
    "pyrochlore-halves": 60, "swap-rule": 61, "4d-shadows": 62, "white-queen-600": 63, "swap-crystals": 64,
    "red-queen-120": 65, "the-focus": 66, "random-stackings-faults": 67, "real-polytypes": 68, "fibonacci-stackings": 69,
    "real-materials-2": 70, "real-materials-3": 71, "real-materials-4": 72, "real-materials-5": 73, "magnets": 74,
    "two-tiles": 75, "queen-stages": 76, "face-to-face": 77, "spiked-ti": 78, "star-cores-a": 79, "star-cores-c": 80,
    "star-cores-b": 81, "hexoct-knitting": 83, "window-law": 84, "star-cores-d": 85, "2026-11-02-hexoct-family": 86,
    "dicto-vacuus": 87, "golden-truncated-triangles": 88,
}


def label_for(path, doc, nums):
    m = re.search(r"<title>(.*?)</title>", doc, re.S)
    title = text(m.group(1)) if m else path
    title = re.sub(r"\s*\(DICTO\)$", "", title)
    key = norm_title(title)
    hits = [n for n, t in nums.items() if norm_title(t) and (norm_title(t) == key or key.startswith(norm_title(t) + " ") or norm_title(t).startswith(key))]
    folder = path.split("/")[1] if path.startswith("papers/") else path.split("/")[1]
    if folder.startswith("book-"):
        return title, [], "book"
    if folder in FOLDER_NUM:
        n = FOLDER_NUM[folder]
        if nums.get(n) and norm_title(nums[n])[:12] != key[:12]:
            print(f"  note: {folder} is #{n} on the site as {nums[n]!r}, paper title {title!r}")
        return title, [n], "paper"
    return title, [], "companion"


REF_HEAD = re.compile(r"<h([1-6])[^>]*>\s*(?:[0-9.]+\s*)?(References|Bibliography|Further reading|Sources)\b[^<]*</h\1>", re.I)


def ref_blocks(doc):
    """Yield the HTML that follows each References heading, up to the next heading."""
    for m in REF_HEAD.finditer(doc):
        rest = doc[m.end():]
        nxt = re.search(r"<h[1-6][^>]*>|<section|<div class=\"plates\"", rest)
        yield rest[: nxt.start() if nxt else len(rest)]


def split_block(block):
    """Return (text, html) for each item of a reference list."""
    items = []
    lis = re.findall(r"<li[^>]*>(.*?)</li>", block, re.S)
    items += [(text(x), x) for x in lis]
    rows = re.findall(r"<tr>(.*?)</tr>", block, re.S)
    for r in rows:
        cells = re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)
        if cells and any(text(c) for c in cells):
            items.append((" | ".join(text(c) for c in cells), " | ".join(cells)))
    if not lis and not rows:
        for p in re.findall(r"<p[^>]*>(.*?)</p>", block, re.S) or [block]:
            for line in re.split(r"<br\s*/?>", p):
                for piece in re.split(r"(?=\[\d+[a-z]?\]\s)", line):
                    if text(piece):
                        items.append((text(piece), piece))
    out = []
    for t, h in items:
        t = re.sub(r"^\[\d+[a-z]?\]\s*", "", t)
        h = re.sub(r"^\s*\[\d+[a-z]?\]\s*", "", h.strip())
        if len(t) > 8:
            out.append((t, h))
    return out


CHECK_P = re.compile(r"<p[^>]*>\s*(?:<b>)?\s*(Sources checked|Prior[- ]art (?:sources|check)[^<]*)(.*?)</p>", re.S | re.I)
APPX = re.compile(r"<h[2-4][^>]*>[^<]*Sources checked[^<]*</h[2-4]>\s*(.*?)(?=<h[1-6]|<section|$)", re.S | re.I)
DATAREF = re.compile(r"References?:\s*(.*?)(?:</p>|$)", re.S)


def split_checked(t):
    t = re.sub(r"\([^()]*\bquer(?:y|ies)\b[^()]*\)", " ", t)            # "(ask-library, 22 queries, ...)"
    t = re.sub(r"ask-library:?\s*(\"[^\"]*\"[;,]?\s*)+", " ", t)
    parts = re.split(r";\s+|\.\s+(?=[A-Z][a-z]+(?: [a-z]+)*:)|(?<=:)\s+(?=[A-Z])", t)
    out = []
    for p in parts:
        p = p.strip(" .;:")
        p = re.sub(r"^(?:Read|Web|Web, read|Abstract only|History|Library|Reference library|Read in full|Also|Search summaries, not read in full|Not checked)[^:]{0,40}:\s*", "", p)
        if len(p) > 6:
            out.append(p)
    return out


def main():
    nums = site_numbers()
    recs = []
    for path in sources():
        doc = open(os.path.join(KR, path), encoding="utf-8").read()
        title, n, kind_src = label_for(path, doc, nums)
        base = {"src": path, "label": title, "nums": n, "type": kind_src}
        for block in ref_blocks(doc):
            for it, raw in split_block(block):
                recs.append(dict(base, kind="ref", text=it, html=raw))
        for m in CHECK_P.finditer(doc):
            for it in split_checked(text(m.group(2))):
                recs.append(dict(base, kind="checked", text=it))
        for m in APPX.finditer(doc):
            blk = m.group(1)
            if "Sources checked" in blk[:40]:
                continue
            for it in split_checked(text(blk)):
                recs.append(dict(base, kind="checked", text=it))
        for m in re.finditer(r"<b>Data and code\.?</b>(.*?)</p>", doc, re.S):
            d = DATAREF.search(m.group(1))
            if d:
                for it in re.split(r";\s+", text(d.group(1))):
                    if len(it) > 6:
                        recs.append(dict(base, kind="dataref", text=it.strip(" .")))
    # one record per (src, kind, text)
    seen, uniq = set(), []
    for r in recs:
        k = (r["src"], r["text"])
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    os.makedirs(OUT, exist_ok=True)
    json.dump(uniq, open(os.path.join(OUT, "raw-references.json"), "w"), ensure_ascii=False, indent=1)
    by = {}
    for r in uniq:
        by.setdefault(r["kind"], 0)
        by[r["kind"]] += 1
    print(f"{len(sources())} sources, {len(uniq)} citations", by)
    for p in sources():
        c = sum(1 for r in uniq if r["src"] == p)
        lab = next((r for r in uniq if r["src"] == p), None)
        print(f"  {c:4d}  {p}  {lab and lab['nums']}")


if __name__ == "__main__":
    main()
