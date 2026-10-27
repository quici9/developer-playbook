#!/usr/bin/env bash
# Setup Claude Code config trên máy mới, chạy sau khi clone repo về ~/.claude/skills
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -e "$HOME/.claude/CLAUDE.md" ] && [ ! -L "$HOME/.claude/CLAUDE.md" ]; then
  echo "⚠️  ~/.claude/CLAUDE.md đã tồn tại (không phải symlink) — gộp tay rồi chạy lại"
  exit 1
fi
ln -sfn "$DIR/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
echo "✅ ~/.claude/CLAUDE.md -> $DIR/CLAUDE.md"

# Agent definitions used by the product-team skill (dev-backend, dev-pages, dev-shell, integrator, panel-user)
mkdir -p "$HOME/.claude/agents"
for f in "$DIR"/agents/*.md; do
  t="$HOME/.claude/agents/$(basename "$f")"
  if [ -e "$t" ] && [ ! -L "$t" ] && ! cmp -s "$f" "$t"; then
    echo "⚠️  $t khác bản trong repo (không phải symlink) — gộp tay rồi chạy lại"; exit 1
  fi
  ln -sfn "$f" "$t"
  echo "✅ $t -> $f"
done
