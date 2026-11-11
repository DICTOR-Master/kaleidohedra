# The panel review of "Scutoids in Four Dimensions" (DICTO 10 Nov: "getting dBB multipanel expert to review it first", then Fable).
# Four expert reviewers on the local workhorse model, one after another; each report written to panel-<name>.md. Claude judges every
# point before anything changes. Prints START, PROGRESS per reviewer, FINAL.
import json, pathlib, re, html, time, urllib.request
d = pathlib.Path(__file__).parent; key = (pathlib.Path.home() / '.config/dicto/llama-key').read_text().strip()
txt = html.unescape(re.sub(r'<[^>]+>', ' ', (d / 'paper.html').read_text())); txt = re.sub(r'\s+', ' ', txt)
COMMON = ('Read this draft research paper closely. List numbered points, most serious first. For each: the exact quote, the problem '
          '(wrong / gap in a proof / unsupported / overclaim / missing credit / unclear), and a concrete fix. Do not invent facts or '
          'references; if you think prior work exists, say what to search for rather than citing something you are unsure of. '
          'End with a one-line verdict. Be concise and specific.')
PANEL = {
  'polytopes': 'You are an expert in the combinatorics of convex polytopes (h-vectors, Dehn-Sommerville, simple polytopes, shellings, '
               'Morse-type arguments, bistellar flips). Check Theorem 1 and its proof line by line (the claim that passing a corner of index '
               '1, 2, 3 is a birth, a pure swap, a death; that two cells share at most one 2-face; that the counts are h1, h2, h3), Theorem 2 '
               '(simplicity of the 120-cell, truncated 120-cell, bitruncated 600-cell; the h-vector formulas; non-simplicity of the truncated '
               '600-cell) and the remarks on higher dimensions and non-simple polytopes. Say exactly what is classical and must be credited.',
  'geometry':  'You are an expert in computational geometry: power diagrams (weighted Voronoi), regular subdivisions, secondary fans, '
               'exact computation. Check section 2 (Theorem 3): is the proof by exact two-parameter computation sound as described (planes '
               'linear in s and lambda, corners rational, slack non-negativity on whole cells via the two boundary walls, Bernstein sign tests), '
               'what assumptions are hidden (finite neighbourhood, the six stacking words), and whether the "each wall is a swap" reading is right.',
  'scutoids':  'You are a biophysicist who works on epithelial packing and scutoids (Gomez-Galvez et al. 2018 and follow-ups). Check that the '
               'paper describes scutoids and the T1 / apico-basal transition fairly and accurately, whether calling the polytope events '
               '"scutoid swaps" and the 4D cells "4D scutoids" is justified or overreaching, and what the biology community would object to.',
  'referee':   'You are a hostile but fair journal referee. Find every overclaim, every gap, every place where "new" may not be new, every '
               'sentence a careful reader would challenge, and anything essential that is missing (definitions, conditions such as genericity, '
               'precise statements). Judge whether the main claim (the scutoid reading of simple 4-polytopes, swaps = h2) is novel and significant.'}
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
