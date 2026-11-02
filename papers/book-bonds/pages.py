# Page numbers for the contents: reads the typeset PDF and writes pages.json (chapter and back-matter start pages), then re-run assemble.py and print.
# Usage: python3 pages.py <pdf> pages.json
import subprocess, json, re, sys
pdf, out = sys.argv[1], sys.argv[2]
n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
keys = {f'ch{i}': f'Chapter {i}. ' for i in range(1, 13)}
keys.update({'epilogue': 'Epilogue. From the walk to the law', 'app': 'Appendix. Sources by chapter', 'refs': 'Papers referred to, not in this book', 'index': 'Index', 'about': 'About the author'})
res = {}
for p in range(4, n + 1):
    t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', pdf, '-'], capture_output=True, text=True).stdout
    first = '\n'.join(l.strip() for l in t.splitlines() if l.strip())[:120]
    for k, v in keys.items():
        if k not in res and first.startswith(v): res[k] = p
json.dump(res, open(out, 'w'), indent=0); print(res, len(res))
