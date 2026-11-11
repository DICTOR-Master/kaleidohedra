# The in-house panel review of "DICTO 1:2 Truncated Octahedron: The 4D Vacuus of the Permutohedron" (DICTO 11 Nov: "can we do some in
# house reviewing of paper and the Fable?"). Four expert reviewers on the local workhorse model, one after another; each report written to
# panel-<name>.md. Claude judges every point before anything changes; then Fable attacks. Prints START, PROGRESS per reviewer, FINAL.
import json, pathlib, re, html, time, urllib.request
d = pathlib.Path(__file__).parent; key = (pathlib.Path.home() / '.config/dicto/llama-key').read_text().strip()
txt = html.unescape(re.sub(r'<[^>]+>', ' ', (d / 'paper.html').read_text())); txt = re.sub(r'\s+', ' ', txt)
COMMON = ('Read this draft research paper closely. List numbered points, most serious first. For each: the exact quote, the problem '
          '(wrong / gap in a proof / unsupported / overclaim / missing credit / unclear), and a concrete fix. Do not invent facts or '
          'references; if you think prior work exists, say what to search for rather than citing something you are unsure of. Check every '
          'number you can by hand. End with a one-line verdict. Be concise and specific.')
PANEL = {
  'permutohedra': 'You are an expert on permutohedra, Coxeter groups and their face lattices (ordered set partitions, weak order, reduced '
                  'words, braid relations, generalized permutohedra). Check section 1 (the web of bonds facts and their credits) and Theorem 1: '
                  'the description of 2-faces as ordered splits, the normal-vector formula c1 = bc(b+c), c2 = -ac(a+2b+c), c3 = ab(a+b), the '
                  'count 65 = 20 + 30 + 10 + 5, the four congruence classes and the table of slice shapes.',
  'enumeration':  'You are an enumerative combinatorialist. Check Theorem 3 (the count N(n) of central hyperplanes through the ridges of the '
                  'permutohedron of 1..n) and its proof: the two-valued / three-valued split, the even-n coincidence (a,b,a) ~ (b/2,2a,b/2), the '
                  'formulas 2^(n-1)-1 and 2^(n-2)-1, and the table 3, 15, 65, 225, 770, 2443, 7761. Recompute small cases (n = 3, 4, 5) by hand. '
                  'Say whether this count is likely known (hyperplane arrangements, Coxeter arrangements, "central sections") and what to search.',
  'tilings':      'You are an expert on space tilings and convex geometry (parallelohedra, Minkowski-Venkov-McMullen, Voronoi cells of lattices, '
                  'zonotopes, truncated octahedra). Check Theorem 2 (two central slices cross in a regular hexagon; the majorization argument), '
                  'Theorem 4 (T(x) is the permutohedron of -q,-p,p,q with x = (q-p)/(2p); the isometry; x = 1/2, 1, tau) and the claims that the '
                  '1:2 truncated octahedron does not tile by translations alone, that the 1:2 and 2:1 fill space together, and the "three solids".',
  'referee':      'You are a hostile but fair journal referee. Find every overclaim, every gap, every place where "new" may not be new, every '
                  'sentence a careful reader would challenge, any wrong number, and anything essential missing (definitions, precise statements). '
                  'Judge whether the main results (the 4D Vacuus, the heart, the count N(n), DICTONIC as permutohedra) are correct, novel and significant.'}
print(f'START panel of {len(PANEL)} reviewers on the local workhorse model', flush=True)
for n, (name, role) in enumerate(PANEL.items(), 1):
    t0 = time.time()
    body = json.dumps({'model': 'workhorse', 'messages': [{'role': 'system', 'content': role + ' ' + COMMON}, {'role': 'user', 'content': 'PAPER:\n' + txt}],
                       'max_tokens': 5000, 'temperature': 0.2, 'chat_template_kwargs': {'enable_thinking': False}}).encode()
    r = urllib.request.Request('http://compute-host:8081/v1/chat/completions', data=body, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    out = json.load(urllib.request.urlopen(r, timeout=5400))['choices'][0]['message']['content'].strip()
    (d / f'panel-{name}.md').write_text(out + '\n')
    print(f'PROGRESS {n / len(PANEL):.2f} reviewer {name} done ({time.time() - t0:.0f} s, {len(out)} chars)', flush=True)
done = [p for p in PANEL if (d / f'panel-{p}.md').exists() and (d / f'panel-{p}.md').stat().st_size > 200]
print('FINAL ok' if len(done) == len(PANEL) else f'FINAL FAIL: only {done}')
