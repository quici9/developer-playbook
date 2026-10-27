<!-- product-team: section appended to the repo's CLAUDE.md at intake. Every agent loads it, so keep it ≤ 60 lines:
     only what a developer needs on their first minute in the repo. Details stay in .claude/team/project.md. -->
## Working context (product team)

<One line: what the product is, who uses it, deploy constraints (e.g. air-gapped: no CDN, pinned deps).>

### Layout
- `<backend dir>`: <framework; how modules import; where routers / SQL / migrations live>.
- `<backend tests>`: <runner; key fixtures; where env is set before import>.
- `<frontend dir>`: <api types/queries file>, <UI primitives file>, <charts>, <pages>, <pure logic + its checks>.
- Shared helpers (use, don't fork): <time formatter>, <count helper>, <scoped link>, <drawer>.
- Ops docs: <DEPLOYMENT / RUNBOOK / API doc>; ops-impacting change → update them in the same commit.

### Commands
- Tests and build: use the `verify` skill (`bash .claude/skills/verify/verify.sh backend|frontend|check <name>`).
- Raw commands, if needed: backend `<cmd with -p $COMPOSE_PROJECT>`; checks `<cmd>`; build `<cmd>`.
- Dev server: `<cmd>` (port <n>); mock data: <how>.

### Rules (full §0 in .claude/team/project.md)
- <UI language and tone; banned words; one word per concept>.
- <Security: scope check on every endpoint, audit log, no secrets in logs>.
- Commits in English, conventional, small. Never push, never deploy.
- Don't survey the repo: read the files the brief names, then their callers.
