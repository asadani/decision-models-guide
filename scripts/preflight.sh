#!/usr/bin/env bash
# scripts/preflight.sh: confirm the book toolchain is present.
set -euo pipefail

missing=()
for cmd in pandoc pdflatex curl make python; do
  command -v "$cmd" >/dev/null 2>&1 || missing+=("$cmd")
done

if [ ${#missing[@]} -gt 0 ]; then
  echo "preflight: FATAL missing required tools: ${missing[*]}"
  exit 1
fi
echo "preflight: OK    pandoc, pdflatex, curl, make, python present."
