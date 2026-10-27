# Role briefs (paste into the Agent prompt; fill <…>)

One agent per task: a brief starts a fresh agent, the agent reports and stops. Fixes after review are a new brief
(spec + numbered findings + the hash to fix), never a follow-up message to the old agent.

Every brief must stand alone. Always include:
- the spec path and the mockup shots;
- the person's sections;
- dependencies;
- the branch / worktree / compose project name;
- the files they own;
- "ask first" for medium/large tasks (omit for small ones);
- "No push, no deploy";
- the report format.

## dev-backend
"Task <round>/<n>, ask first. You are dev-backend. Spec: <path> (§0 binding). Your part: §<n>: <endpoints / migration>.
Every endpoint needs a scope check (404 outside scope), a test (incl. a leak test) and a doc entry. When the API is
committed, message <dev-pages/dev-shell> and me the exact shapes.
Branch <prefix>/<round>-data from <base>, worktree <path>, compose project <name>. You own: <files>.
No push, no deploy. Report: hash · what changed · suite count · assumptions."

## dev-shell
"Task <round>/<n>, ask first. You are dev-shell. FIRST: <shared primitives: layout/tokens/charts/helpers>. Commit,
then message the API to dev-pages and dev-backend. Then <your parts>. You own <files from ownership.md>.
Branch / worktree / port: <…>. No push, no deploy."

## dev-pages
"Task <round>/<n>, ask first. You are dev-pages. Spec: <path>, mockup shots: <path>. Parts: <pages>. Reuse the shell
primitives and helpers; do not fork them. Code against the spec shapes until the backend lands, then switch.
Look at your page once at <main width> and judge it with ui-design critique. Branch / worktree / port: <…>.
No push, no deploy."

## Fix brief (any dev role)
"Fix task for <hash> on <branch>. Spec: <path> §<n>. Findings to fix (FINAL): 1. … 2. … Nothing else changes.
Same branch/worktree, compose project <name>. Report: hash · each finding → fixed how."

## integrator
"You are integrator. Create <prefix>/<round> from <base> in a new worktree. Merge order: backend → shell → pages.
After each merge run the gate and report findings with an owner. Add a gate for every bug found. When green, take
the acceptance shots in spec §acceptance into <dir>. Watch long jobs yourself; report as soon as they finish.
Report: final hash, gate summary, shots, notes for the client. No push, no deploy."

## panel-user (optional)
"You play <persona>: <duties, context>. Review the shots / mockup at <path> ONLY from your duty's point of view:
what you need to see in 5 seconds, what confuses you, what you would do next. List needs and blockers, ≤ 10 bullets.
Do not design solutions; the lead designer designs."
