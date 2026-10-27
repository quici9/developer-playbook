#!/usr/bin/env bash
# Setup Claude Code config trên máy mới, chạy sau khi clone repo về ~/.claude/skills.
# Chạy được trên macOS, Linux, WSL và Windows (Git Bash). Chạy lại bao nhiêu lần cũng được.
#   bash ~/.claude/skills/_config/install.sh            # cài + kiểm tra môi trường
#   bash ~/.claude/skills/_config/install.sh --check    # chỉ kiểm tra môi trường
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

# Windows (Git Bash / MSYS / Cygwin): symlink thường cần Developer Mode → dùng bản copy, chạy lại sau mỗi git pull
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) MODE=copy ;;
  *) MODE=link ;;
esac
[ "${INSTALL_MODE:-}" = copy ] && MODE=copy

place() {   # place <source> <target>
  local src=$1 t=$2
  if [ -e "$t" ] && [ ! -L "$t" ] && ! cmp -s "$src" "$t"; then
    if [ "$MODE" = copy ] && [ -f "$t.installed" ] && cmp -s "$t" "$t.installed"; then :   # our earlier copy, unchanged
    else echo "⚠️  $t khác bản trong repo và không do install.sh tạo — gộp tay rồi chạy lại"; exit 1; fi
  fi
  if [ "$MODE" = link ]; then ln -sfn "$src" "$t"; echo "✅ $t -> $src"
  else rm -f "$t"; cp "$src" "$t"; cp "$src" "$t.installed"; echo "✅ $t (bản copy — chạy lại install.sh sau git pull)"; fi
}

check() {
  echo "== Kiểm tra môi trường ($(uname -s))"
  local ok=1
  need() { if command -v "$1" >/dev/null 2>&1; then echo "  ✓ $1 $($1 --version 2>&1 | head -1)"; else echo "  ✗ $1 — $2"; ok=0; fi; }
  opt()  { if command -v "$1" >/dev/null 2>&1; then echo "  ✓ $1"; else echo "  · $1 (tuỳ chọn) — $2"; fi; }
  need git "bắt buộc"
  need node "bắt buộc cho script của product-team / ui-design (Node >= 22)"
  if command -v node >/dev/null 2>&1; then
    v=$(node -p 'process.versions.node.split(".")[0]'); [ "$v" -ge 22 ] || { echo "  ✗ Node $v < 22 — script chụp ảnh cần fetch + WebSocket có sẵn"; ok=0; }
    local cm="$DIR/../product-team/scripts/chrome.mjs"
    command -v cygpath >/dev/null 2>&1 && cm=$(cygpath -m "$cm")
    if node --input-type=module -e "const {pathToFileURL}=await import('node:url'); const m=await import(pathToFileURL(process.argv[1])); console.log('  ✓ chrome '+m.findChrome())" "$cm" 2>/dev/null; then :
    else echo "  ✗ Chrome/Chromium/Edge — cần cho chụp ảnh (hoặc đặt CHROME=/đường/dẫn)"; ok=0; fi
  fi
  opt python3 "cho handover-docs (.docx); trên Windows có thể là 'python'"
  opt docker "cho test backend trên compose project riêng"
  [ $ok = 1 ] && echo "== Môi trường đủ" || echo "== Thiếu thứ đánh dấu ✗ ở trên"
}

if [ "${1:-}" = --check ]; then check; exit 0; fi

# Windows filesystems drop the exec bit; without this, 755 scripts show as modified and block git pull
if [ "$MODE" = copy ] && git -C "$DIR/.." rev-parse --git-dir >/dev/null 2>&1; then
  git -C "$DIR/.." config core.fileMode false
fi

mkdir -p "$CLAUDE_HOME/agents"
place "$DIR/CLAUDE.md" "$CLAUDE_HOME/CLAUDE.md"
# Agent definitions used by the product-team skill (dev-backend, dev-pages, dev-shell, integrator, panel-user)
for f in "$DIR"/agents/*.md; do place "$f" "$CLAUDE_HOME/agents/$(basename "$f")"; done
check
