#!/bin/bash
# One watched job (dbb job packets-fit): regenerate the truncated icosidodecahedron with the exact-code generator,
# build the reference project, refresh the entry library (Canon imports renamed), regenerate Challenge and Solution,
# then the kit checks (run_checks.sh: namespace build, axioms, comparator, negative controls, standard profile) and the
# split con-ron kernel timing at the namespace profile.
# FINAL ok iff run_checks passes (FINAL ok), the standard profile passes, and con-ron takes at most 15 min.
REF=$HOME/lean/palomar-packets; ENT=$HOME/lean/packets-entry
PKG=$HOME/k-research/studies/2026-11-22-palomar-packets/package; KIT=$HOME/k-research/palomar-kit/scripts
export PATH=$HOME/.elan/bin:$PATH
echo "PROGRESS 0.01 start"
(cd "$REF/gen" && python3 gen_pieces.py tid 2> tid.err) || { echo "TID generation failed"; tail -3 "$REF/gen/tid.err"; exit 1; }
grep -a "wrote\|faces" "$REF/gen/tid.err"
echo "PROGRESS 0.05 TID generated"
cd "$REF" || exit 1
lake build Packets 2>&1 | tee /tmp/fit-ref.log | grep -a --line-buffered "Built Packets\|^error" | \
  while IFS= read -r l; do echo "PROGRESS 0.1 reference $l"; done
if grep -aq "^error" /tmp/fit-ref.log; then grep -a "^error" -A8 /tmp/fit-ref.log | head -40; exit 1; fi
echo "reference warnings:"; grep -a "^warning" /tmp/fit-ref.log | sed 's/:[0-9]*:[0-9]*:/:/' | sort | uniq -c | head
echo "PROGRESS 0.15 reference built"
# entry library: the reference Packets files, Canon imports renamed; the vendored Canon stays
mkdir -p "$PKG/library/Canon"
rm -f "$PKG/library"/*.lean
cp "$ENT"/Packets/Canon/*.lean "$PKG/library/Canon/"
for f in "$REF"/Packets/*.lean; do
  sed 's/^public import DehnCanon\./public import Packets.Canon./; s/^import DehnCanon\./import Packets.Canon./' \
    "$f" > "$PKG/library/$(basename "$f")"
done
python3 "$PKG/scripts/gen_challenge.py" || { echo "gen_challenge failed"; exit 1; }
rm -f "$ENT"/Packets/*.lean
cp "$PKG"/library/*.lean "$ENT/Packets/"
cp "$PKG/Challenge/DehnPackets.lean" "$ENT/Challenge.lean"
cp "$PKG/Solution/DehnPackets.lean" "$ENT/Solution.lean"
wc -l "$ENT/Challenge.lean" "$ENT"/Packets/Gen*.lean | tail -12
echo "PROGRESS 0.2 entry assembled"
bash "$PKG/scripts/run_checks.sh" "$ENT" "$PKG/entry.toml" 2>&1 | tee /tmp/fit-checks.log | \
  awk '/^PROGRESS/ { $2 = sprintf("%.2f", 0.2 + 0.7 * $2); print "PROGRESS " $2 " checks:" substr($0, index($0, $3) - 1); fflush(); next }
       /^FINAL/ { print "checks " $0; fflush(); next } { print; fflush() }'
grep -aq "^FINAL ok" /tmp/fit-checks.log && chk=1 || chk=0
grep -aq "^STANDARD PROFILE ok" /tmp/fit-checks.log && std=1 || std=0
echo "PROGRESS 0.92 kit checks done (checks $chk, standard $std)"
cd "$ENT" || exit 1
ENTRY=$ENT PROFILE=namespace STEP=export TMO=3600 bash "$KIT/fit_check.sh" | tail -3
ENTRY=$ENT PROFILE=namespace STEP=kernel K=con-ron TMO=3600 bash "$KIT/fit_check.sh" | tail -3
line=$(grep -a "kernel" logs/fit/SUMMARY.tsv | grep -a "con-ron" | tail -1); echo "con-ron: $line"
wall=$(printf '%s\n' "$line" | sed -n 's/.*wall \([0-9:.]*\).*/\1/p')
secs=$(printf '%s\n' "$wall" | awk -F: '{ if (NF == 3) print $1*3600 + $2*60 + $3; else print $1*60 + $2 }')
echo "con-ron seconds: ${secs:-unknown}"
cr=0; [ -n "$secs" ] && awk -v s="$secs" 'BEGIN { exit !(s <= 900) }' && cr=1
cat logs/fit/SUMMARY.tsv
echo "PROGRESS 1 done (checks $chk, standard $std, con-ron<=15min $cr)"
if [ $chk = 1 ] && [ $std = 1 ] && [ $cr = 1 ]; then echo "FINAL ok"; else echo "FINAL FAIL"; fi
