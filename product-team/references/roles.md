# Role briefs (paste into the Agent/SendMessage prompt; fill <…>)

Every brief must stand alone. Always include:
- the spec path and the mockup shots;
- the person's sections;
- dependencies;
- the branch / worktree / compose name;
- the files they own;
- "No push, no deploy";
- the report format (commit hash + checks + shots).

## dev-backend
"New round <round>. You are dev-backend. Spec: <path> (read all; §0 is binding). Your parts in order:
(1) §<n> API first: <endpoints>. Every endpoint needs a scope check (404 outside scope), a test (including a leak
test) and a doc entry. When it is committed, message dev-shell, dev-pages and me with the shapes.
(2) <pages you own>.
Branch <prefix>/<round>-data from <base>, worktree in the scratchpad, compose project -p <proj>-<round>-data,
logs in <dir>. You own: <files>. Ask before touching others' files. No push, no deploy.
Report: hash + suite count + checks."

## dev-shell
"You are dev-shell. FIRST: <shared primitives: layout/tokens/charts/helpers>. Commit, then message the API to
dev-pages and dev-backend. Then <your pages>. You own App/router, layout, theme tokens, shared chart primitives
and the shared helpers listed in ownership.md. Others edit only their own route lines."

## dev-pages
"You are dev-pages. Parts: <pages>. Reuse the shell primitives and helpers; do not fork them. Shared drawer and
count helpers are single-source. Code against the spec shapes until backend lands, then switch and delete the mocks."

## integrator
"You are integrator. Create <prefix>/<round> from <base> in a new worktree. Merge order: backend → shell → pages.
After each merge run the gate (`gate.sh`) and report findings with an owner. Add a gate for every bug found so it
cannot return. When green, take the acceptance shots listed in spec §acceptance into <dir>. Report: final hash,
gate summary, shots, notes for the client. No push, no deploy. Use your own compose project and log dir."

## panel-user (optional)
"You play <persona>: <duties, context>. Review the shots / mockup at <path> ONLY from your duty's point of view:
what you need to see in 5 seconds, what confuses you, what you would do next. List needs and blockers, ≤ 10 bullets.
Do not design solutions; the lead designer designs."
