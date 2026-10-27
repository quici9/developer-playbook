#!/bin/bash
# Compact test runner for agents (product-team template). Prints the summary and the failures only.
# Reads .claude/team/gate.conf: FRONTEND_DIR, BUILD_CMD, CHECK_CMD, BACKEND_TEST_CMD (uses $PROJ and $ARGS),
# SRC_GLOB, SRC_EXCLUDE, BANNED, and optionally CHECK_ONE_CMD (uses $NAME).
set -u -o pipefail
ROOT=$(git rev-parse --show-toplevel) || exit 2
cd "$ROOT" || exit 2
CONF=.claude/team/gate.conf
[ -f "$CONF" ] || { echo "no $CONF"; exit 2; }
# shellcheck disable=SC1090
. "$CONF"
PROJ=${COMPOSE_PROJECT:-verify-$(basename "$ROOT" | tr 'A-Z' 'a-z')}; export PROJ
short() { grep -E "^(FAIL|FAILED|ERROR)|[Ee]rror|assert|^E |passed|failed" | tail -40; }
case "${1:-}" in
  backend)
    shift; ARGS="$*"; export ARGS
    [ -n "${BACKEND_TEST_CMD:-}" ] || { echo "BACKEND_TEST_CMD not set in $CONF"; exit 2; }
    out=$(eval "$BACKEND_TEST_CMD" 2>&1); rc=$?
    docker compose -p "$PROJ" down -v >/dev/null 2>&1 || true
    if [ $rc = 0 ]; then echo "$out" | tail -1; else echo "$out" | short; fi
    exit $rc ;;
  frontend)
    rc=0
    if [ -n "${CHECK_CMD:-}" ]; then
      out=$( (cd "$FRONTEND_DIR" && eval "$CHECK_CMD") 2>&1) && echo "checks ok" || { echo "$out" | short; rc=1; }
    fi
    out=$( (cd "$FRONTEND_DIR" && eval "$BUILD_CMD") 2>&1) && echo "build ok" || { echo "$out" | grep -iE "error" | head -20; rc=1; }
    if [ -n "${BANNED:-}" ]; then
      hits=$(grep -rnE "$BANNED" "$SRC_GLOB" | grep -vE "${SRC_EXCLUDE:-^$}" | head -20)
      [ -z "$hits" ] && echo "banned terms ok" || { echo "banned terms (check comments/allowlist):"; echo "$hits"; rc=1; }
    fi
    exit $rc ;;
  check)
    NAME=${2:?check name}; export NAME
    [ -n "${CHECK_ONE_CMD:-}" ] || { echo "CHECK_ONE_CMD not set; use: verify.sh frontend"; exit 2; }
    out=$( (cd "$FRONTEND_DIR" && eval "$CHECK_ONE_CMD") 2>&1); rc=$?
    echo "$out" | grep -vE "^ok" | tail -30; echo "rc=$rc"; exit $rc ;;
  *) echo "usage: verify.sh backend [args] | frontend | check <name>"; exit 2 ;;
esac
