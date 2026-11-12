#!/bin/bash
# search_H.sh: the 12-90 search (DICTO 12 Nov). For each of the 30 subgroups H of the rotation group: contact test (with the one-shell
# test of extra contacts); if certified, the whole-chair test (R = 2). Logs in ../data/searchH-*.log. Controls: H00 (trivial, = the
# certified 90-type scheme) must certify; H29 (all 24, sharing only) must not.
cd "$(dirname "$0")"; PY=${PY:-python3}; export PY   # interpreter with pysat (set PY on the compute machine)
run() { k=$1
  $PY -W ignore -u contact_test.py 4 H$k encl > ../data/searchH-$k-contact.log 2>&1
  if grep -q "VERDICT CERTIFIED BY THEOREM A" ../data/searchH-$k-contact.log; then
    $PY -W ignore -u integrity_test.py 4 H$k 2 > ../data/searchH-$k-integrity.log 2>&1; fi
  echo "H$k done"; }
export -f run
seq -w 0 29 | xargs -P 15 -I{} bash -c 'run {}'
echo "== summary"
for k in $(seq -w 0 29); do
  t=$(grep -o "H$k: [0-9]* types" ../data/searchH-$k-contact.log | grep -o "[0-9]* types")
  c=$(grep -o "allowed outside P\*: [0-9]*" ../data/searchH-$k-contact.log)
  v=$(grep -h "^VERDICT" ../data/searchH-$k-integrity.log 2>/dev/null)
  echo "H$k | $t | $c | ${v:-no whole-chair test}"
done
ok0=$(grep -c "WHOLE CHAIRS FORCED" ../data/searchH-00-integrity.log 2>/dev/null); bad29=$(grep -c "VERDICT CERTIFIED" ../data/searchH-29-contact.log)
[ "$ok0" = 1 ] && [ "$bad29" = 0 ] && echo "FINAL ok" || echo "FINAL FAIL: controls (H00 forced $ok0, H29 certified $bad29)"
