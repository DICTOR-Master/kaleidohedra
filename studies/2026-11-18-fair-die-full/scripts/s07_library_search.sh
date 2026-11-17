#!/bin/bash
# Protocol step 19 (prior art): full-text search of DICTO's private reference library (every PDF, pdftotext; text kept only in a
# temporary folder that is deleted at the end). Usage: s07_library_search.sh <library folder>. Prints matching files per term.
# Control: the term "Diaconis" must find the Diaconis-Keller copy added to the library on 18 Nov 2026 (else FINAL FAIL).
LIB="$1"; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
n=0; find "$LIB" -name '*.pdf' -print0 | while IFS= read -r -d '' f; do
  out="$TMP/$(echo "$f" | md5sum | cut -c1-12).txt"; pdftotext -q "$f" "$out" 2>/dev/null; echo "$f" > "$out.name"; done
echo "PDFs converted: $(ls "$TMP"/*.txt 2>/dev/null | wc -l)"
ctrl=0
for term in 'fair di(ce|e)' '14-sided|fourteen-sided|14-face' 'solid angle' 'truncated octahedr' 'tan\(π/14\)|tan\(pi/14\)' 'Diaconis' 'Rawlins'; do
  hits=$(grep -l -i -E "$term" "$TMP"/*.txt 2>/dev/null)
  echo "== term: $term : $(echo -n "$hits" | grep -c .) files"
  for h in $hits; do echo "   $(basename "$(cat "$h.name")")"; done
  if [ "$term" = "Diaconis" ] && [ -n "$hits" ]; then ctrl=1; fi
  echo "== term with 'die' or 'dice' nearby ($term):"
  for h in $hits; do grep -i -E -o ".{0,80}($term).{0,80}" "$h" | grep -i -E '\bdi(e|ce)\b' | head -2 | sed "s|^|   $(basename "$(cat "$h.name")"): |"; done
done
[ $ctrl = 1 ] && echo "control: Diaconis found" && echo "FINAL ok" || echo "FINAL FAIL (control term not found)"
