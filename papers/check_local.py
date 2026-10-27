# Claim check by the local model on dicto-big-brother (run there): every factual claim of a draft with the dossier text that supports it,
# or UNSUPPORTED. Output <folder>/claims-check.md. Usage: check_local.py <paper folder> [draft file, default draft-local.md]
import json, pathlib, sys, urllib.request, re
d = pathlib.Path(sys.argv[1]); draft = (d / (sys.argv[2] if len(sys.argv) > 2 else 'draft-local.md')).read_text()
key = (pathlib.Path.home() / '.config/dicto/llama-key').read_text().strip(); dossier = (d / 'dossier.json').read_text()
system = ('You are a strict fact checker. List EVERY factual claim in the DRAFT (each number, formula, name, credit, status word such as proved/measured, '
          'and each statement of what was found). For each, quote the exact DOSSIER text that supports it, or write UNSUPPORTED if no dossier text says it, '
          'or MISMATCH if the dossier says something different (quote both). Output only a Markdown table: | claim | dossier quote | verdict (OK / UNSUPPORTED / MISMATCH) |.')
def ask(part):
    body = json.dumps({'model': 'workhorse', 'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': f'DRAFT:\n{part}\n\nDOSSIER (JSON):\n{dossier}'}],
                       'max_tokens': 24000, 'temperature': 0.0, 'chat_template_kwargs': {'reasoning_effort': 'medium'}}).encode()
    r = urllib.request.Request('http://127.0.0.1:8081/v1/chat/completions', data=body, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    c = json.load(urllib.request.urlopen(r, timeout=5400))['choices'][0]
    t = (c['message'].get('content') or '').strip()
    if not t: raise SystemExit(f"{d.name}: EMPTY answer (finish_reason {c.get('finish_reason')}): the check did not run")
    return t
# one call per section (DICTO 10-27: a whole-draft call ran out of room and returned nothing, which read as '0 claims')
parts = [p for p in re.split(r'(?m)^(?=#{1,3} )', draft) if p.strip()]
rows = [ask(p) for p in parts]
t = '\n\n'.join(rows)
(d / 'claims-check.md').write_text(t + '\n')
print(d.name, 'claims-check.md:', len(parts), 'sections,', len(re.findall(r'\| *OK *\|', t)), 'OK,', len(re.findall(r'UNSUPPORTED', t)), 'unsupported,', len(re.findall(r'MISMATCH', t)), 'mismatch')
