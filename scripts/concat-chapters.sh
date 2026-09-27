#!/usr/bin/env bash
# scripts/concat-chapters.sh: concatenate the manuscript in canonical order.
# Output: output/manuscript.md
#
# Order: front matter, chapters, appendices. Each directory is sorted by
# filename, which is why filenames are numbered.

set -euo pipefail

BOOK_ROOT="${BOOK_ROOT:-book}"
OUT="${MANUSCRIPT_OUT:-output/manuscript.md}"
ASSET_ROOT="${ASSET_ROOT:-assets}"
SEPARATOR="${SEPARATOR:-cleardoublepage}"
mkdir -p "$(dirname "$OUT")"

: > "$OUT"

append() {
  local f="$1" sep="${2:-$SEPARATOR}"
  # Rewrite ../../assets/ so images resolve from the repo root, where pandoc runs.
  sed -E "s#\.\./\.\./assets/#${ASSET_ROOT}/#g" "$f" >> "$OUT"
  # \cleardoublepage forces recto chapter starts (blank verso when needed) in
  # the twoside paperback, and behaves like \newpage in the oneside build.
  printf '\n\n\\%s\n\n' "$sep" >> "$OUT"
}

# Front matter. The copyright page belongs on the verso of the title page, so
# the separator after the title file is \clearpage, not \cleardoublepage.
for f in "$BOOK_ROOT"/00-front-matter/*.md; do
  case "$(basename "$f")" in
    00-cover.md) append "$f" clearpage ;;
    *)           append "$f" ;;
  esac
done

for f in "$BOOK_ROOT"/01-chapters/*.md; do
  append "$f"
done

for f in "$BOOK_ROOT"/02-appendices/*.md; do
  append "$f"
done

# Drop the trailing separator (blank, blank, command, blank) to avoid an
# empty last page.
tmp="$(mktemp)"
head -n -4 "$OUT" > "$tmp" && mv "$tmp" "$OUT"

echo "concat-chapters: OK    manuscript written to $OUT"
wc -l "$OUT"
