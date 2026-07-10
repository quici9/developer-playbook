# developer-playbook

Bộ skills + cấu hình Claude Code cá nhân, đồng bộ giữa các máy.

## Setup máy mới

```bash
git clone https://github.com/quici9/developer-playbook.git ~/.claude/skills
bash ~/.claude/skills/_config/install.sh   # symlink CLAUDE.md toàn cục
```

## Cấu trúc

- `<tên-skill>/SKILL.md` — 16 skills cho phát triển hệ thống security / air-gapped,
  Claude Code tự quét và load theo ngữ cảnh
- `_config/CLAUDE.md` — chỉ dẫn toàn cục (symlink về `~/.claude/CLAUDE.md`)
- Symlink `paperclip*` do tool tự tạo trên từng máy — đã gitignore

## Duy trì

Sửa skill xong: `git add -A && git commit && git push` — máy khác `git pull`.
