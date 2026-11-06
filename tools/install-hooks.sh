#!/bin/sh
# Install the research pre-commit guard into this repository's hooks folder (shared by all worktrees).
h=$(git rev-parse --git-common-dir)/hooks; cp "$(dirname "$0")/pre-commit" "$h/pre-commit"; chmod +x "$h/pre-commit"; echo "installed $h/pre-commit"
