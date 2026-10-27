#!/usr/bin/env bash
# Render a page at several widths and color schemes for visual review.
# Usage: shot.sh <file.html|url> <out-dir> [widths] [schemes]
#   widths  default "1440 390"     schemes default "dark light"
# Dev-time tool only: needs Playwright + Chromium already cached on the dev machine.
set -euo pipefail

target="${1:?usage: shot.sh <file.html|url> <out-dir> [widths] [schemes]}"
out="${2:?out-dir required}"
widths="${3:-1440 390}"
schemes="${4:-dark light}"

if [[ "$target" != http://* && "$target" != https://* && "$target" != file://* ]]; then
  [[ -f "$target" ]] || { echo "not found: $target" >&2; exit 1; }
  target="file://$(cd "$(dirname "$target")" && pwd)/$(basename "$target")"
fi

if npx --no-install playwright --version >/dev/null 2>&1; then
  pw=(npx --no-install playwright)
else
  echo "Playwright not available. On an internet-connected dev machine run:" >&2
  echo "  npx playwright@latest install chromium" >&2
  exit 1
fi

mkdir -p "$out"
name="$(basename "${target%%\?*}")"
name="${name%.html}"
[[ -n "$name" ]] || name="page"

for w in $widths; do
  h=900; [[ "$w" -lt 800 ]] && h=844
  for s in $schemes; do
    f="$out/${name}-${w}-${s}.png"
    "${pw[@]}" screenshot --full-page --wait-for-timeout=300 \
      --viewport-size="${w},${h}" --color-scheme="$s" "$target" "$f" >/dev/null
    echo "$f"
  done
done
