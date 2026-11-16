"""Assemble the local Palomar entry (nothing is pushed or submitted): writes the directory given as argument with
  Challenge.lean, Solution.lean (Challenge word for word with proofs; the proofs transfer the library theorems by definitional
  unfolding), the library YantraCert in Palomar's module layout (`module`, `public import`, `@[expose] public section`),
  lakefile.toml, lean-toolchain, lake-manifest.json, comparator.json, formalization.yaml, LICENSE, scripts/, README.md.
Usage: c14_palomar_entry.py OUTDIR [LIBDIR]   (LIBDIR: a directory holding YantraCert/ with every library file, generated
       ones included; default the study's lean/)"""
import os, re, shutil, sys, json
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D_ = lambda *p: os.path.join(HERE, *p)
OUT = sys.argv[1]; LIB = sys.argv[2] if len(sys.argv) > 2 else D_('lean')
LOOP = os.environ.get('TEMPLATE') or os.path.join(os.path.dirname(HERE), '2026-11-14-lean-loop-equality', 'entry')  # a built Palomar template entry
os.makedirs(OUT, exist_ok=True)
from lean_module import modulize   # `module` first, public imports, an exposed public section (idempotent: the study's
                                   # sources are committed in this form since 16 Nov 2026 and are then copied unchanged)
# library: exactly the import closure of YantraCert.Main (unused generated modules, e.g. KTest_28, stay out)
def lib_path(m): return os.path.join(LIB, *m.split('.')) + '.lean'
todo, keep = ['YantraCert.Main'], set()
while todo:
    m = todo.pop()
    if m in keep: continue
    keep.add(m)
    todo += re.findall(r'^(?:public )?import (YantraCert\S*)', open(lib_path(m)).read(), re.M)
n = 0
for m in sorted(keep):
    dst = os.path.join(OUT, *m.split('.')) + '.lean'; os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w').write(modulize(open(lib_path(m)).read())); n += 1
# Challenge
ch = open(D_('lean', 'Challenge', 'KulaichevYantra.lean')).read()
open(os.path.join(OUT, 'Challenge.lean'), 'w').write(modulize(ch))
# Solution
proofs = {
 'kulaichev_unique': '''  obtain ⟨z, hz, hu⟩ := YantraCert.Y.kulaichev_unique
  refine ⟨⟨z.b, z.w, z.a⟩, hz, fun y hy => ?_⟩
  have e := hu ⟨y.b, y.w, y.a⟩ hy
  cases y; cases z; simp only [YantraCert.Y.Yantra.mk.injEq] at e; obtain ⟨rfl, rfl, rfl⟩ := e; rfl''',
 'kulaichev_slope': '''  exact YantraCert.Y.kulaichev_slope ⟨y.b, y.w, y.a⟩ h'''}
sol = ch
for k, pr in proofs.items():
    sol = re.sub(r'(theorem ' + k + r'[\s\S]*?:= by\n)  sorry', lambda m: m.group(1) + pr, sol, count=1)
assert 'sorry' not in sol
sol = modulize(sol)
sol = sol.replace('public import Mathlib\n', 'public import Mathlib\npublic import YantraCert.Main\n', 1)
assert 'public import YantraCert.Main' in sol
sol = sol.replace('/-!\n# Kulaichev', '/-!\n# Proved solution: Kulaichev', 1)
open(os.path.join(OUT, 'Solution.lean'), 'w').write(sol)
# project files
open(os.path.join(OUT, 'lakefile.toml'), 'w').write('''name = "KulaichevYantra"
version = "0.1.0"
defaultTargets = ["YantraCert", "Challenge", "Solution"]

[[require]]
name = "mathlib"
git = "https://github.com/leanprover-community/mathlib4.git"
rev = "v4.35.0-rc2"

[[lean_lib]]
name = "YantraCert"
globs = ["YantraCert.+"]

[[lean_lib]]
name = "Challenge"
roots = ["Challenge"]

[[lean_lib]]
name = "Solution"
roots = ["Solution"]
''')
for f in ('lean-toolchain', 'lake-manifest.json', 'LICENSE'):
    shutil.copy(os.path.join(LOOP, f), os.path.join(OUT, f))
os.makedirs(os.path.join(OUT, 'scripts'), exist_ok=True)
for f in ('check-lean-sources.py', 'verify-comparator.sh'):
    shutil.copy(os.path.join(LOOP, 'scripts', f), os.path.join(OUT, 'scripts', f))
json.dump({'challenge_module': 'Challenge', 'solution_module': 'Solution',
           'theorem_names': ['KulaichevYantra.kulaichev_unique', 'KulaichevYantra.kulaichev_slope'], 'definition_names': [],
           'permitted_axioms': ['propext', 'Quot.sound', 'Classical.choice'], 'enable_nanoda': True},
          open(os.path.join(OUT, 'comparator.json'), 'w'), indent=2)
shutil.copy(D_('lean', 'palomar', 'formalization.yaml'), os.path.join(OUT, 'formalization.yaml'))
shutil.copy(D_('lean', 'palomar', 'README.md'), os.path.join(OUT, 'README.md'))
print('library files:', n)
_need = ['comparator.json', 'formalization.yaml', 'README.md', 'lakefile.toml']
_miss = [f for f in _need if not os.path.exists(os.path.join(OUT, f))]
# every YantraCert import of every written file must resolve to a written file
for root, dirs, files in os.walk(OUT):
    for f in files:
        if f.endswith('.lean') and '.lake' not in root:
            for m in re.findall(r'^public import (YantraCert\S*)|^import (YantraCert\S*)', open(os.path.join(root, f)).read(), re.M):
                m = m[0] or m[1]
                if not os.path.exists(os.path.join(OUT, *m.split('.')) + '.lean'): _miss.append(m)
print('FINAL ok' if n > 0 and not _miss else f'FINAL FAIL (missing {sorted(set(_miss))[:10]}, files {n})')
