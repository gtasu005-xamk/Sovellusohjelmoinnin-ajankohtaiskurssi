# Sprint 6 tickets — Testing, Security & Deployment Readiness (optional)

Backlog for Sprint 6 ([index](../README.md)). Keep IDs in branch/PR titles. When a ticket is done, create a **new Git commit** with the ticket ID in the message (see **Commit** on each ticket).

**This sprint is optional.** Sprints 1–5 already opened the gym: building, membership desk, training floor, lockers, scoreboard, and a house coach. The core course demo is complete. Sprint 6 is an **inspection before handoff**—tests, a security note, a time limit on the coach, and a runbook for the next staff. Only pick up these tickets if you have time after Sprint 5.

Priorities below (**Must** / **Should** / **Stretch**) apply *within* Sprint 6 if you take it—they are not required for the core course.

### New tools & technologies

| Tool / technology | Role in this sprint |
| ----------------- | ------------------- |
| **pytest** + FastAPI **TestClient** / httpx | Broader API tests (auth, ownership, stats, mocked AI) |
| **Vitest** | Minimal frontend unit tests |
| **Rate limiting** (e.g. SlowAPI or custom) | Protect `/ai/insights` from abuse |
| **`docs/security.md`** / **`docs/deployment.md`** | Written security checklist and deploy runbook |
| **GitHub Actions** (stretch) | CI smoke on push/PR |
| **Playwright** (stretch) | Browser smoke for a happy path |

*(Carried forward: full S1–5 stack; this sprint hardens and documents it.)*

| ID | Title | Week | Priority | Estimate |
| -- | ----- | ---- | -------- | -------- |
| [S6-01](#s6-01--api-test-harness) | API test harness | 1 | Must | M |
| [S6-02](#s6-02--auth-api-tests) | Auth API tests | 1 | Must | M |
| [S6-03](#s6-03--ownership-and-stats-tests) | Ownership and stats tests | 1 | Must | L |
| [S6-04](#s6-04--mocked-ai-tests) | Mocked AI tests | 1 | Must | M |
| [S6-05](#s6-05--frontend-unit-tests) | Frontend unit tests | 1 | Must | M |
| [S6-06](#s6-06--document-test-commands) | Document test commands | 1 | Must | S |
| [S6-07](#s6-07--rate-limit-ai-insights) | Rate limit AI insights | 2 | Must | M |
| [S6-08](#s6-08--secrets-and-jwt-review) | Secrets and JWT review | 2 | Must | S |
| [S6-09](#s6-09--ownership-and-cors-review) | Ownership and CORS review | 2 | Must | S |
| [S6-10](#s6-10--securitymd) | security.md | 2 | Must | M |
| [S6-11](#s6-11--seed-script) | Seed script | 3 | Must | L |
| [S6-12](#s6-12--deploymentmd) | deployment.md | 3 | Must | M |
| [S6-13](#s6-13--readme-polish-and-demo-script) | README polish and demo script | 3 | Must | M |
| [S6-14](#s6-14--final-demo-rehearsal-fixes) | Final demo rehearsal fixes | 3 | Should | M |
| [S6-S1](#s6-s1--ci-workflow) | CI workflow | — | Stretch | M |
| [S6-S2](#s6-s2--playwright-smoke) | Playwright smoke | — | Stretch | L |
| [S6-S3](#s6-s3--security-headers) | Security headers | — | Stretch | S |
| [S6-S4](#s6-s4--optional-ollama-integration-test) | Optional Ollama integration test | — | Stretch | M |

---

## S6-01 — API test harness

| Field | Value |
| ----- | ----- |
| **Type** | test |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | Sprint 5 complete (full API surface) |

### Why this matters

Without a shared harness, every test reinvents DB setup and auth. A solid `conftest` makes the rest of Week 1 fast and keeps CI-ready commands boring and reliable.

### What you should do

1. Set up pytest with httpx `AsyncClient` or Starlette `TestClient`.
2. Choose a test DB strategy (SQLite or disposable Postgres) and document it.
3. Provide fixtures for the app client and user creation.

### Hints

- Prefer overriding `get_db` / settings so tests never touch your personal Docker volumes by accident.
- Keep fixture names obvious (`client`, `auth_headers`, `user_a`, `user_b`).

### Acceptance criteria

- [ ] Tests can boot the app against a test DB
- [ ] Fixtures for client and user creation exist
- [ ] Strategy documented (SQLite vs Postgres)

### Suggested paths

`backend/tests/conftest.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-01` in the message, for example `S6-01: short summary`. Never commit `.env` or secrets.

---

## S6-02 — Auth API tests

| Field | Value |
| ----- | ----- |
| **Type** | test |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S6-01 |

### Why this matters

Auth is the gate for everything else. Automated register/login/me coverage catches regressions before demo day.

### What you should do

1. Cover successful register and login.
2. Assert duplicate register is handled; bad login returns 401.
3. Assert `/auth/me` without token → 401 and with token → 200.

### Hints

- Reuse the same password-hashing path as production—do not bypass with raw SQL inserts unless necessary.
- Clear DB state between tests or use unique emails per test.

### Acceptance criteria

- [ ] Duplicate register handled
- [ ] Bad login → 401
- [ ] `/auth/me` without token → 401; with token → 200

### Suggested paths

`backend/tests/test_auth.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-02` in the message, for example `S6-02: short summary`. Never commit `.env` or secrets.

---

## S6-03 — Ownership and stats tests

| Field | Value |
| ----- | ----- |
| **Type** | test |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | S6-01, Sprint 3 ownership, Sprint 4 stats |

### Why this matters

Two-user fixtures prove IDOR prevention and user-scoped analytics—the security story you claimed in earlier sprints.

### What you should do

1. Create User A and User B with separate sessions.
2. Assert B cannot read/update A’s session (and plan) by id; cover clone source access and calendar if present.
3. Assert stats for A ignore B’s sessions; cover at least one filter/list case.
4. Optionally assert clone isolation (edit source → prior clone unchanged).

### Hints

- Assert status codes match your documented 404/403 choice from Sprint 3.
- Seed enough dated sessions (`session_at` set) that a date filter can isolate rows; include a plan via `plan_id` if testing attach.

### Acceptance criteria

- [ ] User B cannot read/update User A’s session
- [ ] Stats for A ignore B’s sessions
- [ ] At least one filter/list case covered

### Suggested paths

`backend/tests/test_sessions_ownership.py`, `backend/tests/test_stats.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-03` in the message, for example `S6-03: short summary`. Never commit `.env` or secrets.

---

## S6-04 — Mocked AI tests

| Field | Value |
| ----- | ----- |
| **Type** | test |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S6-01, Sprint 5 `/ai/insights` |

### Why this matters

Default tests must not require a running Ollama. Mock the provider so success and failure paths stay green on any machine.

### What you should do

1. Override/fake `AIProvider` for `/ai/insights` tests.
2. Assert success returns structured fields (`summary`, `strengths`, `recommendations`, `caveats`).
3. Assert provider failure maps to the expected HTTP error; keep real Ollama optional/skipped.

### Hints

- Dependency overrides on the FastAPI app are usually cleaner than patching HTTP.
- Mark any live Ollama test with `pytest.mark.integration` and skip if unreachable.

### Acceptance criteria

- [ ] Success returns structured fields
- [ ] Provider failure maps to expected HTTP error
- [ ] No real Ollama required for default CI path

### Suggested paths

`backend/tests/test_ai_insights.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-04` in the message, for example `S6-04: short summary`. Never commit `.env` or secrets.

---

## S6-05 — Frontend unit tests

| Field | Value |
| ----- | ----- |
| **Type** | test |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | Sprint 2–3 frontend helpers |

### Why this matters

A few Vitest checks prove the frontend toolchain runs without a backend—token helpers and validation are high value for little cost.

### What you should do

1. Add Vitest (or your agreed runner) and a `package.json` test script.
2. Write at least two meaningful tests (e.g. token storage and form validation helpers).
3. Ensure tests do not require a running API.

### Hints

- Prefer pure helpers over full-page render tests for this ticket.
- Keep config minimal; Playwright is a stretch later.

### Acceptance criteria

- [ ] At least two meaningful tests pass
- [ ] Test script in `package.json`
- [ ] Does not require a running backend

### Suggested paths

`frontend/src/auth/token.test.ts`, Vitest config

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-05` in the message, for example `S6-05: short summary`. Never commit `.env` or secrets.

---

## S6-06 — Document test commands

| Field | Value |
| ----- | ----- |
| **Type** | docs |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | S |
| **Depends on** | S6-01, S6-05 |

### Why this matters

If commands are not written down, graders and classmates cannot verify your suite. Documentation is part of the harness.

### What you should do

1. Add a README section with exact backend and frontend test commands.
2. Note any required env vars for tests.
3. Mention optional Ollama integration mark/skip behavior.

### Hints

- Copy-paste commands from a clean checkout on your machine once before committing.
- Call out working directories (`backend/` vs `frontend/`).

### Acceptance criteria

- [ ] README section lists exact commands
- [ ] Notes any required env for tests
- [ ] Mentions optional Ollama integration mark/skip

### Suggested paths

`README.md`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-06` in the message, for example `S6-06: short summary`. Never commit `.env` or secrets.

---

## S6-07 — Rate limit AI insights

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 2 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | Sprint 5 `POST /ai/insights` |

### Why this matters

Insights calls are expensive (CPU/time). Rate limiting reduces spam and accidental hammering during demos and multi-user use.

### What you should do

1. Rate-limit `POST /ai/insights` (SlowAPI or a simple in-memory limiter).
2. Return 429 (or a documented equivalent) when exceeded.
3. Document limit values; leave other routes unaffected (or document separately).

### Hints

- Key limits by user id when authenticated, not only by IP, if practical.
- Make limits generous enough for a live demo walkthrough.

### Acceptance criteria

- [ ] Excess requests return 429 (or documented equivalent)
- [ ] Limit values documented
- [ ] Other routes unaffected (or separately documented)

### Suggested paths

`backend/app/api/ai.py`, `backend/app/core/rate_limit.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-07` in the message, for example `S6-07: short summary`. Never commit `.env` or secrets.

---

## S6-08 — Secrets and JWT review

| Field | Value |
| ----- | ----- |
| **Type** | chore |
| **Week** | 2 |
| **Priority** | Must |
| **Estimate** | S |
| **Depends on** | Sprint 2 JWT settings |

### Why this matters

Committed secrets and eternal JWTs are common course-project footguns. A short review before handoff prevents embarrassing leaks.

### What you should do

1. Verify secrets live only in `.env` (not committed); `.env.example` uses placeholders.
2. Confirm JWT expiry is sensible and documented.
3. Scan current tracked files for accidental real secrets.

### Hints

- Rotate any secret that was ever committed—even for a school project.
- Prefer a strong random `JWT_SECRET` in real `.env`, never in examples.

### Acceptance criteria

- [ ] No real secrets in git history of current files
- [ ] `.env.example` uses placeholders
- [ ] JWT expiry documented

### Suggested paths

`.env.example`, `backend/app/core/config.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-08` in the message, for example `S6-08: short summary`. Never commit `.env` or secrets.

---

## S6-09 — Ownership and CORS review

| Field | Value |
| ----- | ----- |
| **Type** | chore |
| **Week** | 2 |
| **Priority** | Must |
| **Estimate** | S |
| **Depends on** | S6-03, Sprint 2 CORS |

### Why this matters

A final pass across workouts, goals, stats, and insights catches routes added late without ownership checks, and confirms CORS is still locked down.

### What you should do

1. Walk routers and note a checklist of ownership-reviewed routes (PR note or `security.md`).
2. Confirm CORS allowlist still defaults to the frontend origin.
3. Fix findings or explicitly accept them with a written reason.

### Hints

- Include AI context building: it must never pull another user’s rows.
- Wildcard CORS is a demo-day smell—document if you temporarily loosen it.

### Acceptance criteria

- [ ] Checklist of routes reviewed (note in PR or security.md)
- [ ] CORS still locked to frontend origin in default config
- [ ] Findings fixed or explicitly accepted

### Suggested paths

`docs/security.md` (notes), routers

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-09` in the message, for example `S6-09: short summary`. Never commit `.env` or secrets.

---

## S6-10 — security.md

| Field | Value |
| ----- | ----- |
| **Type** | docs |
| **Week** | 2 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S6-07, S6-08, S6-09 |

### Why this matters

Security writing shows you understand trade-offs (including localStorage JWT vs XSS). Graders look for honesty that matches the code.

### What you should do

1. Write `docs/security.md` covering hashing, JWT, IDOR, ORM/validation, CORS, secrets, localStorage XSS trade-off, and AI rate limits.
2. Make sure the doc matches implemented behavior.
3. Link it from the root README.

### Hints

- Explain why you chose localStorage for easier debugging and what risk that accepts.
- Point to tests that prove ownership where possible.

### Acceptance criteria

- [ ] File exists and matches implemented behavior
- [ ] XSS trade-off for localStorage JWT explained honestly
- [ ] Linked from README

### Suggested paths

`docs/security.md`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-10` in the message, for example `S6-10: short summary`. Never commit `.env` or secrets.

---

## S6-11 — Seed script

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 3 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | Workouts, goals, activity types APIs |

### Why this matters

Fresh Compose + empty DB makes Progress and Insights look broken. A seed script creates a demo user with realistic history so the full walkthrough works.

### What you should do

1. Create `backend/scripts/seed.py` that inserts a demo user, varied workouts/goals, and activity types if needed.
2. Make it idempotent or document safe re-run behavior.
3. Document demo credentials for your team and anyone grading the demo.

### Hints

- Spread workouts across dates so charts and streaks look intentional.
- Print the login email/password at the end of a successful seed run.

### Acceptance criteria

- [ ] Idempotent or safe to re-run with documented behavior
- [ ] Demo credentials documented for your team (and anyone who grades your demo)
- [ ] Data sufficient for Progress + Insights demos

### Suggested paths

`backend/scripts/seed.py`, `backend/app/services/seed.py`, `backend/app/repositories/`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-11` in the message, for example `S6-11: short summary`. Never commit `.env` or secrets.

---

## S6-12 — deployment.md

| Field | Value |
| ----- | ----- |
| **Type** | docs |
| **Week** | 3 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | Compose + env setup from earlier sprints |

### Why this matters

Deployment notes turn “works on my laptop” into something another person can host: API + DB containers, secrets, migrations, and what not to expose.

### What you should do

1. Write `docs/deployment.md` for deploying API + DB with containers.
2. Cover env/secrets, migrations, Ollama local vs optional remote, and cloud LLM as future config only.
3. Warn what must not be exposed publicly without auth; link from README.

### Hints

- Keep cloud LLM as “stub / future”—do not invent billing setup.
- Mention ports, reverse proxy basics, and never committing production secrets.

### Acceptance criteria

- [ ] `docs/deployment.md` exists
- [ ] Covers env/secrets, migrations, and what not to expose publicly without auth
- [ ] Linked from README

### Suggested paths

`docs/deployment.md`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-12` in the message, for example `S6-12: short summary`. Never commit `.env` or secrets.

---

## S6-13 — README polish and demo script

| Field | Value |
| ----- | ----- |
| **Type** | docs |
| **Week** | 3 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S6-06, S6-10, S6-11, S6-12 |

### Why this matters

The README is the final demo script. A classmate should run seed → login → workouts → progress → insights without asking you for private steps.

### What you should do

1. Polish root README: short architecture blurb, sprint index link, full demo path.
2. Link tests, `security.md`, `deployment.md`, and `docs/sprints/`.
3. Verify ports and commands against a clean environment.

### Hints

- Order the demo path the way you will present on demo day.
- Remove obsolete commands that no longer match the repo.

### Acceptance criteria

- [ ] A classmate can demo from the README without asking you for extra steps
- [ ] Links to `docs/sprints/`, `security.md`, `deployment.md`
- [ ] Ports and commands accurate

### Suggested paths

`README.md`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-13` in the message, for example `S6-13: short summary`. Never commit `.env` or secrets.

---

## S6-14 — Final demo rehearsal fixes

| Field | Value |
| ----- | ----- |
| **Type** | chore |
| **Week** | 3 |
| **Priority** | Should |
| **Estimate** | M |
| **Depends on** | S6-13 |

### Why this matters

Peer dry-runs catch broken links, seed failures, and flaky tests before graders do. Rehearsal is the last quality gate.

### What you should do

1. Have at least one classmate run the full demo from your README.
2. File and fix blockers (links, seed, flaky tests).
3. List remaining known issues and optional stretch leftovers as future work.

### Hints

- Time the walkthrough; cut steps that always confuse people.
- Prefer fixing seed/docs over last-minute feature work.

### Acceptance criteria

- [ ] At least one classmate dry-run completed
- [ ] Blockers fixed or listed as known issues
- [ ] Stretch leftovers optionally listed as future work

### Suggested paths

issue notes / README “Known issues”

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-14` in the message, for example `S6-14: short summary`. Never commit `.env` or secrets.

---

## Stretch tickets

Optional extras after Must/Should. Same ticket shape; skip them if you are out of time. Rate limits stay Must (S6-07), not stretch.

## S6-S1 — CI workflow

| Field          | Value   |
| -------------- | ------- |
| **Type**       | chore   |
| **Week**       | —       |
| **Priority**   | Stretch |
| **Estimate**   | M       |
| **Depends on** | S6-06   |

### New here: tests on every PR

**CI** runs your documented test commands on each push/PR so a broken import or failing pytest is caught before demo day. This is the same idea as Sprint 1 smoke CI, widened to the Sprint 6 harness (backend + frontend unit tests). Keep live Ollama optional/skipped so classmates without a GPU stay green.

**Docs & tutorials:**

- [Understanding GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions) — workflows, jobs, runners
- [GitHub Actions quickstart](https://docs.github.com/en/actions/writing-workflows/quickstart) — first workflow YAML
- [Building and testing Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python) — install deps and run pytest
- [Building and testing Node.js](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-nodejs) — frontend unit tests

### Your task

Add a GitHub Actions (or similar) workflow that runs the documented backend and frontend tests on each PR. Reuse the commands from S6-06.

### Instructions

1. Add a workflow YAML that checks out the repo and installs backend + frontend deps.
2. Run the same test commands documented in the README (S6-06).
3. Skip or exclude live Ollama tests so the default job stays green without a model.
4. Confirm a failing test fails the job.

### Stay in scope

- Leave Playwright for S6-S2.
- Do not require Docker-in-CI or a real Ollama instance for the default job.
- Rate limits stay Must S6-07, not this ticket.

### Hints

- Set working directories to `backend/` and `frontend/` so imports and Vitest resolve.
- If you already have Sprint 1 smoke CI, extend that workflow rather than adding a second unused file.

### Acceptance criteria

- [ ] Workflow runs on push/PR
- [ ] Documented backend tests run
- [ ] Documented frontend unit tests run
- [ ] Default job does not require a live Ollama instance

### Suggested paths

`.github/workflows/ci.yml`, `README.md`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-S1` in the message, for example `S6-S1: short summary`. Never commit `.env` or secrets.

---

## S6-S2 — Playwright smoke

| Field          | Value   |
| -------------- | ------- |
| **Type**       | test    |
| **Week**       | —       |
| **Priority**   | Stretch |
| **Estimate**   | L       |
| **Depends on** | S6-06   |

### New here: browser smoke

**Playwright** drives a real browser: login → create a **session** → open Progress. That catches UI regressions the API suite misses (wrong route, missing token header, empty Progress). Keep the path short—one happy path is enough.

**Docs & tutorials:**

- [Playwright — Introduction](https://playwright.dev/docs/intro) — install and first test
- [Playwright — Authentication](https://playwright.dev/docs/auth) — login once, reuse storage state
- [Playwright — Running tests](https://playwright.dev/docs/running-tests) — local + CI later

### Your task

Automate login → create session → open Progress as a browser smoke test. Say **session**, not workout—the domain from Sprint 3 still applies.

### Instructions

1. Add Playwright in the frontend (or a small e2e folder) with one smoke spec.
2. Log in (seed user or register in-test), create a session, then open Progress.
3. Assert the Progress page loads for that user (a chart, empty state, or period controls—pick one and document it).
4. Document the command next to the other test commands from S6-06.

### Stay in scope

- One happy path is enough; do not automate Insights/Ollama in this smoke.
- Leave CI wiring of Playwright as optional (S6-S1 can stay API + Vitest only).
- Rate limits stay Must S6-07.

### Hints

- Prefer the seed user from S6-11 if it exists, so the test does not depend on a unique register each run.
- Base URL should match the documented frontend URL (Compose or Vite).

### Acceptance criteria

- [ ] Spec covers login → create session → open Progress
- [ ] Command is documented
- [ ] Test does not require a live Ollama instance

### Suggested paths

`frontend/e2e/smoke.spec.ts` (or `frontend/tests/e2e/`), `README.md`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-S2` in the message, for example `S6-S2: short summary`. Never commit `.env` or secrets.

---

## S6-S3 — Security headers

| Field          | Value   |
| -------------- | ------- |
| **Type**       | chore   |
| **Week**       | —       |
| **Priority**   | Stretch |
| **Estimate**   | S       |
| **Depends on** | S6-10   |

### New here: response headers as a baseline

Browser **security headers** are a cheap extra layer: `X-Content-Type-Options: nosniff` stops MIME sniffing; `Referrer-Policy` limits what the next site sees. They do not replace ownership checks, CORS, or hashing—they belong in `docs/security.md` next to those choices.

**Docs & tutorials:**

- [MDN — X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options) — `nosniff`
- [MDN — Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) — what to send on navigation
- [OWASP Secure Headers](https://owasp.org/www-project-secure-headers/) — practical header set
- [Starlette CORSMiddleware](https://www.starlette.io/middleware/#corsmiddleware) — you already use middleware; headers are the same pattern

### Your task

Add basic security headers middleware (at least `X-Content-Type-Options` and `Referrer-Policy`) and document them in `security.md`.

### Instructions

1. Add middleware (or equivalent) that sets at least `X-Content-Type-Options` and `Referrer-Policy` on API responses.
2. Confirm in `/docs` or a simple GET that the headers are present.
3. Document the chosen values in `docs/security.md` (S6-10) so they match the code.

### Stay in scope

- Do not treat headers as a substitute for IDOR tests, CORS, or `/ai/insights` rate limits (S6-07).
- Leave a full CSP / HSTS production matrix for later unless you already serve HTTPS.

### Hints

- A tiny middleware class that sets two headers is enough; you do not need a new package.

### Acceptance criteria

- [ ] API responses include `X-Content-Type-Options` and `Referrer-Policy`
- [ ] Values are documented in `docs/security.md`
- [ ] Existing CORS / auth behavior still works

### Suggested paths

`backend/app/main.py`, `docs/security.md`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-S3` in the message, for example `S6-S3: short summary`. Never commit `.env` or secrets.

---

## S6-S4 — Optional Ollama integration test

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | test         |
| **Week**       | —            |
| **Priority**   | Stretch      |
| **Estimate**   | M            |
| **Depends on** | S6-01, S6-04, Sprint 5 Ollama (S5-03) |

### New here: skippable live test

An integration test that talks to a **real** Ollama instance is useful—and harmful if it fails CI for classmates without a GPU or pulled model. **Skip cleanly** when Ollama is unreachable. Mocked AI coverage stays in [S6-04](#s6-04--mocked-ai-tests); this ticket is the optional live path only.

**Docs & tutorials:**

- [pytest — skip](https://docs.pytest.org/en/stable/how-to/skipping.html) — conditional skip
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md) — generate/chat smoke call

### Your task

Add an optional live Ollama test that skips when the runtime is down; do not fail CI for missing GPU/model.

### Instructions

1. Call a real Ollama instance from a pytest (or similar) test.
2. Skip cleanly when unreachable (`pytest.skip`).
3. Do not mark the job required for classmates without a model.

### Stay in scope

- Mocked `/ai/insights` tests stay in S6-04; do not require Ollama for the default pytest path.
- Rate limits are S6-07, not this ticket.

### Hints

- Mark the test `pytest.mark.integration` so default `pytest` can exclude it.

### Acceptance criteria

- [ ] Live test calls a real Ollama instance
- [ ] Unreachable runtime → skip, not fail
- [ ] Default test / CI path does not require a pulled model

### Suggested paths

`backend/tests/test_ollama_integration.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S6-S4` in the message, for example `S6-S4: short summary`. Never commit `.env` or secrets.

---

## Related

- Previous tickets: [sprint-05-tickets.md](sprint-05-tickets.md)
- Index: [../README.md](../README.md)
