#!/bin/bash
# One OEIS query per line of queries.txt ("label|query"); polite: 4 s between queries. Output: oeis-searches.txt
# Run on the compute host: bash oeis_search.sh
out=../data/oeis-searches.txt; : > $out
while IFS='|' read -r label q; do
  [ -z "$label" ] && continue
  enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")
  res=$(curl -s -m 30 -A "oeis-search-script" "https://oeis.org/search?q=${enc}&fmt=short")
  hits=$(echo "$res" | grep -oE 'A[0-9]{6}' | sort -u | tr '\n' ' ')
  cnt=$(echo "$res" | grep -oiE 'Found [0-9]+ results?|No results|Sorry, but the terms do not match anything|Search: .{0,0}' | head -1)
  echo "$label | q=$q | ${cnt:-?} | ${hits:-none}" | tee -a $out
  sleep 4
done < queries.txt
