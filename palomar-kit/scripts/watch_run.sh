#!/bin/bash
# Wait for one Palomar run to finish, then read its mechanical report (no extraction to disk).
#   RUN=<run id> [REPO=PalomarRegistry/PalomarSubmission] bash watch_run.sh
#   FIND=<owner>/<repo> bash watch_run.sh       list the registry's runs for that repository first (read_report.py --find)
#   PREFLIGHT=<owner>/<repo> bash watch_run.sh  the entry's own latest preflight run (workflow palomar-preflight.yml)
# Waiting uses `gh run watch` with a 120 s interval (GitHub's API, not the registry's site). On this interface machine
# run it as a logged background job with a heartbeat, never as a foreground loop; it ends with FINAL ok when the run
# succeeded and the report status is pass.
KIT=$(cd "$(dirname "$0")" && pwd); REPO=${REPO:-PalomarRegistry/PalomarSubmission}
if [ -n "$FIND" ]; then python3 -I "$KIT/read_report.py" --find "$FIND" --limit "${LIMIT:-60}"; exit $?; fi
if [ -n "$PREFLIGHT" ]; then REPO=$PREFLIGHT
  RUN=$(gh run list -R "$REPO" --workflow palomar-preflight.yml -L 1 --json databaseId --jq '.[0].databaseId'); fi
RUN=${RUN:?set RUN, FIND or PREFLIGHT}
echo "watching run $RUN of $REPO"
gh run watch "$RUN" -R "$REPO" --interval 120 --exit-status > /dev/null; s=$?
gh run view "$RUN" -R "$REPO" --json status,conclusion,displayTitle,url --jq '"\(.displayTitle): \(.status)/\(.conclusion) \(.url)"'
python3 -I "$KIT/read_report.py" --run "$RUN" --repo "$REPO" | tee /dev/stderr | grep -q "^status pass" && [ $s -eq 0 ] \
  && echo "FINAL ok" || echo "FINAL FAIL (run exit $s; see the report above)"
