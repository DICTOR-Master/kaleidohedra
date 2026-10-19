# SA batch print + check job (dicto-node). For each paper: fetch the latest published PDF from Zenodo, take its file name and footer title,
# reprint the edited source with the same name and footer (new version), and diff the two texts page by page.
import json, os, re, socket, subprocess, urllib.request, difflib
from pypdf import PdfReader
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
H = os.path.expanduser('~/sa-batch'); K = H + '/k'; os.makedirs(H + '/old', exist_ok=True); os.makedirs(H + '/new', exist_ok=True)
plan = json.load(open(H + '/plan.json')); rep = []
def split(pdf):  # (body text, footer line) per page; the footer is the line "<title> · DICTO · dictospheres.com · ..."
    out = []
    for p in PdfReader(pdf).pages:
        L = (p.extract_text() or '').split('\n'); F = [x for x in L if re.match(r'.+? · DICTO · dictospheres\.com · ', x) or re.match(r'DICTO · .+? · DICTO DOI', x)]
        out.append((re.sub(r'\s+', ' ', ' '.join(x for x in L if x not in F)).strip(), F[0] if F else ''))
    return out
def get(url):
    for k in range(5):
        try: return urllib.request.urlopen(url, timeout=300).read()
        except Exception as e: err = e
    raise err
for r in plan:
    rec = json.loads(get(f"https://zenodo.org/api/records/{r['latest']}"))
    pdfs = [f for f in rec['files'] if f['key'].endswith('.pdf')]; assert len(pdfs) >= 1, r['src']
    pdfs = [x for x in pdfs if not x['key'].endswith('-nets.pdf')]; assert len(pdfs) == 1, r['src']; f = pdfs[0]; name = f['key']; old = f"{H}/old/{r['concept']}-{name}"
    if not os.path.exists(old): data = get(f['links']['self']); open(old, 'wb').write(data)
    os_ = split(old); ot = [x[0] for x in os_]; fo = next((x[1] for x in os_ if x[1]), ''); foot = re.match(r'(.+?) · DICTO · dictospheres\.com', fo) or re.match(r'DICTO · (.+?) · DICTO DOI', fo); title = foot.group(1).strip() if foot else None
    assert r['src'].endswith('build_house.py') or (title and len(title) < 80), (r['src'], fo)
    src = r['src']; d = os.path.dirname(src)
    if src.endswith('build_house.py'):
        subprocess.run(['python3', 'build_house.py'], cwd=f'{K}/{d}', check=True, capture_output=True)
        subprocess.run(['node', 'print.mjs', 'paper-house.html', name], cwd=f'{K}/{d}', check=True, capture_output=True)
        new = f'{K}/{d}/{name}'
    else:
        dd = d.replace('papers/', '', 1)
        if src.endswith('collected.html'):
            open(f'{K}/papers/collected/paper.html', 'w').write(open(f'{K}/{src}').read())
        subprocess.run(['node', 'print.mjs', dd, name, title or '?', f"10.5281/zenodo.{r['doi_in_src']}", str(r['new_version'])], cwd=f'{K}/papers', check=True, capture_output=True)
        new = f'{K}/{d}/{name}'
    ns_ = split(new); nt = [x[0] for x in ns_]; subprocess.run(['cp', new, f"{H}/new/{r['concept']}-{name}"])
    # diff: words changed, page counts
    ow, nw = ' '.join(ot).split(), ' '.join(nt).split(); sm = difflib.SequenceMatcher(None, ow, nw, autojunk=False)
    ch = [(' '.join(ow[a:b]), ' '.join(nw[c:dd_])) for tag, a, b, c, dd_ in sm.get_opcodes() if tag != 'equal']
    rep.append(dict(src=src, name=name, title=title, pages_old=len(ot), pages_new=len(nt), changes=ch, sa=('CC BY-SA 4.0' in ' '.join(nt)), foot_old=fo, foot_new=next((x[1] for x in ns_ if x[1]), ''), old_by=sum(x.count('CC BY 4.0') for x in nt)))
    json.dump(rep, open(H + '/report.json', 'w'), indent=1, ensure_ascii=False)
    print(f"{src[:50]:50} {name[:36]:36} pages {len(ot)}->{len(nt)} changes {len(ch)} SA {rep[-1]['sa']} oldBY {rep[-1]['old_by']}", flush=True)
json.dump(rep, open(H + '/report.json', 'w'), indent=1, ensure_ascii=False); print('done', len(rep))
