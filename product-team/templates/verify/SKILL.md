---
name: verify
description: Run this repo's tests, checks and build with compact output (summary + failures only). Use instead of raw test/build commands whenever you test a change.
---
One command, short output, own compose project and teardown handled. Reads `.claude/team/gate.conf`.

- `bash .claude/skills/verify/verify.sh backend [test args]`: backend tests; no args = full suite.
  Example: `backend test_mfa.py -k replay`.
- `bash .claude/skills/verify/verify.sh frontend`: checks + build + banned terms.
- `bash .claude/skills/verify/verify.sh check <name>`: one frontend check (if the project's checks are per-file).

Use the narrow form while iterating; run the full form once before you commit.
Set `COMPOSE_PROJECT` to the name in your brief; otherwise one is derived from the worktree name.
