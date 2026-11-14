#!/bin/sh
# README.md -> paper/paper.html -> DRAFT PDF on the compute host with the house pipeline (print.mjs)
set -e
cd "$(dirname "$0")"
mkdir -p paper
python3 scripts/md2html.py README.md paper/paper.html
D=chat-handoff-triage
rsync -a --delete --exclude '*.pdf' paper/ compute-host-2:kaleidohedra-papers/$D/
rsync -a ../../papers/paper.css ../../papers/dicto-logo.png ../../papers/print.mjs ../../papers/figcheck.mjs compute-host-2:kaleidohedra-papers/
ssh compute-host-2 "cd ~/kaleidohedra-papers && node print.mjs $D DRAFT-chat-handoff-triage.pdf 'Chat handoff: triage and quick tests' draft"
rsync -a compute-host-2:kaleidohedra-papers/$D/DRAFT-chat-handoff-triage.pdf paper/
