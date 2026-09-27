#!/usr/bin/env bash
# scripts/verify-links.sh: fail if any URL in the manuscript sources returns 4xx/5xx.
#
# URLs in build/link-allowlist.txt are skipped. Use it only for sites that
# refuse automated requests (login walls, bot checks) but load in a browser;
# each entry needs a comment saying why.

set -uo pipefail

BOOK_ROOT="${BOOK_ROOT:-book}"
ALLOW="build/link-allowlist.txt"

mapfile -t urls < <(grep -rhoE 'https?://[^ )>"`]+' "$BOOK_ROOT" \
  | sed -E 's/[.,;:]+$//' | sort -u)

fail=0
for u in "${urls[@]}"; do
  if [ -f "$ALLOW" ] && grep -qxF "$u" <(grep -v '^#' "$ALLOW" | sed 's/[[:space:]]*#.*$//'); then
    echo "skip   $u"
    continue
  fi
  code=$(curl -s -o /dev/null -L -m 40 -A "Mozilla/5.0" -w '%{http_code}' "$u" || echo 000)
  # Up to two retries: a slow or dropped first response is not a dead link.
  for wait in 3 8; do
    [[ "$code" =~ ^[23] ]] && break
    sleep "$wait"
    code=$(curl -s -o /dev/null -L -m 60 -A "Mozilla/5.0" -w '%{http_code}' "$u" || echo 000)
  done
  if [[ "$code" =~ ^[23] ]]; then
    echo "ok $code $u"
  else
    echo "FAIL $code $u"
    fail=1
  fi
done

if [ "$fail" -ne 0 ]; then
  echo "verify-links: FAILED"
  exit 1
fi
echo "verify-links: OK    ${#urls[@]} URLs checked"
