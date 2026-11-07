#!/usr/bin/env python3
"""Hygiene (DICTO 2026-11-07: "keep unread drafts clear, and remove/delete unneeded transitional files ... otherwise we will need a
512gb clearout of rubbish"). Run daily by cron, and by zen_new.py / zen_newversion.py right after every release (--folder).

  tidy.py                 daily sweep (this machine + dicto-big-brother)
  tidy.py --folder DIR    after a release of DIR: delete every DRAFT*.pdf of that paper here and on dicto-big-brother
  tidy.py --dry           report only

Rules:
 1. A DRAFT*.pdf is transitional: deleted once its paper is released (--folder), and anywhere when older than 14 days.
 2. papers-to-read/read-earlier: DRAFT files are deleted at once (the published PDF is the record); everything else after 14 days.
 3. papers-to-read (top) holds only what waits for DICTO; items older than 1 day are reported as stale (DICTO 11-07: stale content).
 4. Runjob scratch (<data>.txt/.json + .part/.FAILED, untracked) older than 2 days is deleted; /tmp scratch of ours on dicto-big-brother older than 2 days too.
Never touches .git, memory folders, published PDFs (dicto-*.pdf), data files or sources, nor ANY file tracked by git."""
import os, sys, time, subprocess, glob
DRY = '--dry' in sys.argv; NOW = time.time(); DAY = 86400
HOME = os.path.expanduser('~'); READ = os.path.join(HOME, 'Documents', 'papers-to-read'); EARLIER = os.path.join(READ, 'read-earlier')
ROOTS = [os.path.join(HOME, 'k-research'), os.path.join(HOME, 'kaleidohedra')]
log = []
def tracked(p):   # never delete a file git tracks (11-07: "*.part" also matched source files named style.part)
    d = os.path.dirname(p)
    r = subprocess.run(['git', '-C', d, 'ls-files', '--error-unmatch', os.path.basename(p)], capture_output=True)
    return r.returncode == 0
def rm(p, why):
    if os.path.isfile(p) and tracked(p): log.append(f'KEEP {p} (tracked by git)'); return
    log.append(f'delete {p} ({why})')
    if not DRY:
        try: os.remove(p)
        except IsADirectoryError: subprocess.run(['rm', '-rf', p])
        except FileNotFoundError: pass
def walk(root, pat):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in ('.git', 'node_modules', 'memory')]
        for f in files:
            if glob.fnmatch.fnmatch(f, pat): yield os.path.join(d, f)
def remote(cmd):
    return subprocess.run(['ssh', '-o', 'ConnectTimeout=10', 'dicto-big-brother', cmd], capture_output=True, text=True).stdout
if '--folder' in sys.argv:
    folder = os.path.abspath(sys.argv[sys.argv.index('--folder') + 1]); name = os.path.basename(folder)
    for p in [q for pat in ('DRAFT*.pdf', '*draft*.pdf') for q in glob.glob(os.path.join(folder, pat))]: rm(p, 'released')
    out = remote(f'find ~/kaleidohedra-check/papers/{name} -maxdepth 1 -iname "*draft*.pdf" {"-print" if DRY else "-print -delete"}')
    log += [f'delete dicto-big-brother:{l} (released)' for l in out.split()]
    for p in glob.glob(os.path.join(READ, f'DRAFT*')):
        pass   # drafts in the reading folder are moved by the release step itself (read ok = read)
else:
    for r in ROOTS:
        for p in [q for pat in ('DRAFT*.pdf', '*draft*.pdf', '*Draft*.pdf') for q in walk(r, pat)]:
            if NOW - os.path.getmtime(p) > 14 * DAY: rm(p, 'draft older than 14 days')
        for pat in ('*.txt.part', '*.json.part', '*.txt.FAILED', '*.json.FAILED'):   # runjob writes <data file>.part / .FAILED only
            for p in walk(r, pat):
                if NOW - os.path.getmtime(p) > 2 * DAY: rm(p, 'runjob scratch older than 2 days')
    if os.path.isdir(EARLIER):
        for f in os.listdir(EARLIER):
            p = os.path.join(EARLIER, f)
            if f.startswith('DRAFT'): rm(p, 'read draft (published PDF is the record)')
            elif NOW - os.path.getmtime(p) > 14 * DAY: rm(p, 'read-earlier item older than 14 days')
    out = remote(f'find ~/kaleidohedra-check/papers -iname "*draft*.pdf" -mtime +14 {"-print" if DRY else "-print -delete"}; '
                 f'find /tmp -maxdepth 1 -user $USER \\( -name "*.png" -o -name "*.pdf" -o -name "*.json" -o -name "zz-*" \\) -mtime +2 {"-print" if DRY else "-print -delete"} 2>/dev/null')
    log += [f'delete dicto-big-brother:{l}' for l in out.split()]
    if os.path.isdir(READ):
        stale = [f for f in os.listdir(READ) if f != 'read-earlier' and NOW - os.path.getmtime(os.path.join(READ, f)) > 1 * DAY]
        waiting = [f for f in os.listdir(READ) if f != 'read-earlier']
        log.append(f'reading folder: {len(waiting)} waiting' + (f'; STALE (> 1 day: answered → move to read-earlier; waiting → ask DICTO): {", ".join(stale)}' if stale else ''))
print('\n'.join(log) or 'nothing to tidy')
print(f"FINAL ok ({'dry run' if DRY else 'tidied'}: {sum(1 for l in log if l.startswith('delete'))} deletions)")
