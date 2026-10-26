#!/bin/bash
# Generic integration gate. Run from the worktree root: gate.sh [--backend] [--no-browser] [--conf PATH]
# Reads .claude/team/gate.conf (see templates/gate.conf). Steps: build · checks · dist mock probe ·
# banned-term grep (comment-only hits ignored, allowlist by file + exact string) · (browser) pages-check ·
# (--backend) backend suite on its own compose project. Exit 0 only if every step passes.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
CONF=.claude/team/gate.conf; BACKEND=0; BROWSER=1
while [ $# -gt 0 ]; do case $1 in --backend) BACKEND=1;; --no-browser) BROWSER=0;; --conf) CONF=$2; shift;; esac; shift; done
[ -f "$CONF" ] || { echo "no $CONF (run the product-team intake first)"; exit 2; }
# shellcheck disable=SC1090
. "$CONF"
ROOT=$(pwd); rc=0
LOG=${GATE_LOG_DIR:-${TMPDIR:-/tmp}/gate-$(basename "$ROOT")}; mkdir -p "$LOG"
echo "== tip $(git log --oneline -1 2>/dev/null)"
[ -z "$(git status --short 2>/dev/null)" ] && echo "tree clean" || echo "TREE DIRTY"

echo "== build"
if (cd "$FRONTEND_DIR" && eval "$BUILD_CMD") > "$LOG/build.log" 2>&1; then echo "ok"; else echo "BUILD FAILED (see $LOG/build.log)"; tail -15 "$LOG/build.log"; rc=1; fi

if [ -n "${CHECK_CMD:-}" ]; then
  echo "== checks"
  if (cd "$FRONTEND_DIR" && eval "$CHECK_CMD") > "$LOG/checks.log" 2>&1; then echo "ok"; else echo "CHECKS FAILED"; tail -20 "$LOG/checks.log"; rc=1; fi
fi

if [ -n "${DIST_PROBE:-}" ] && [ -d "${DIST_DIR:-}" ]; then
  echo "== dist mock probe"
  n=$(grep -rlE "$DIST_PROBE" "$DIST_DIR" | wc -l | tr -d ' ')
  echo "files with mock code: $n"; [ "$n" = 0 ] || rc=1
fi

if [ -n "${BANNED:-}" ]; then
  echo "== banned terms in UI strings"
  nnew=0; nallow=0; ncomm=0
  ALLOW=""; [ -f "${ALLOWLIST_FILE:-}" ] && ALLOW=$(grep -v '^#' "$ALLOWLIST_FILE")
  while IFS= read -r hit; do
    [ -z "$hit" ] && continue
    file=${hit%%:*}; rest=${hit#*:}; text=${rest#*:}
    t=$(printf '%s' "$text" | sed -E 's/^[[:space:]]+//')
    case "$t" in "//"*|"/*"*|"*"*|"{/*"*|"#"*) ncomm=$((ncomm+1)); continue;; esac
    ok=0
    while IFS=$'\t' read -r af as; do [ -n "$af" ] && [ "$file" = "$af" ] && [[ "$text" == *"$as"* ]] && ok=1; done <<< "$ALLOW"
    if [ $ok = 1 ]; then nallow=$((nallow+1)); else nnew=$((nnew+1)); echo "   BANNED ${hit:0:200}"; fi
  done < <(grep -rnE "$BANNED" "$SRC_GLOB" | grep -vE "${SRC_EXCLUDE:-^$}")
  echo "hits: $nnew banned · $nallow allowlisted · $ncomm comment-only"
  [ $nnew = 0 ] || rc=1
fi

if [ $BROWSER = 1 ] && [ -f "${PAGES_FILE:-}" ]; then
  echo "== pages (no-hscroll, console, 404, redirects) @ $DEV_URL"
  if node "$HERE/pages-check.mjs" "$DEV_URL" "$PAGES_FILE" "${WIDTHS:-1280,1920}" "${THEMES:-light}" "${THEME_STORAGE:-}" "${EXTRA_QUERY:-}" > "$LOG/pages.log" 2>&1; then
    tail -1 "$LOG/pages.log"
  else rc=1; grep -v '^ok' "$LOG/pages.log" | head -30; fi
fi

if [ $BACKEND = 1 ] && [ -n "${BACKEND_TEST_CMD:-}" ]; then
  echo "== backend suite"
  PROJ=${GATE_COMPOSE_PROJECT:-gate-$(basename "$ROOT")}; export PROJ
  if eval "$BACKEND_TEST_CMD" > "$LOG/backend.log" 2>&1; then grep -E "passed|failed" "$LOG/backend.log" | tail -1; else echo "BACKEND FAILED"; tail -20 "$LOG/backend.log"; rc=1; fi
  docker compose -p "$PROJ" down -v > /dev/null 2>&1 || true
fi

echo "== gate rc=$rc"; exit $rc
