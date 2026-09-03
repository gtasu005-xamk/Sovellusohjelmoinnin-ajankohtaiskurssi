# Sprint 6 report — Testing, security & deployment (optional)

**This sprint is optional.** Fill this report only if you took Sprint 6. Copy this file to `docs/reports/sprint-06.md` in **your** repo. Keep it a process log: no pasted source, no secrets, no `.env` values. Say **session**, not workout.

| Field | Your answer |
| ----- | ----------- |
| **Dates** | |
| **Names** | |
| **Repo URL** | |
| **Branch** | |

Tickets: [sprint-06-tickets.md](../tickets/sprint-06-tickets.md) · Index: [../README.md](../README.md)

## Sprint goal

From the tickets: harden the project for handoff. You are done when documented test commands pass (backend + basic frontend); `docs/security.md` and `docs/deployment.md` match the code; seed creates a demo user with realistic **sessions**; `/ai/insights` is rate-limited; the README covers seed → login → sessions → progress → insights.

In your words (2–3 sentences): did you meet that, and what is still rough?

## Tickets

For **each** ticket fill **Status** and **PR / commit**.

Fill **Demonstration** only where this template includes that section. Follow the numbered steps exactly. Store images under `docs/reports/images/sprint-06/` using the suggested filename. Crop secrets.

For **every** ticket: set **Used AI?** to `Yes` or `No`. Write the sprint-level **AI usage** reflection at the end of this report (not under each ticket).

Skip stretch tickets you did not do. Stretch: Status, PR, and Used AI? for each stretch you did; add a Demonstration only where listed below.

### S6-01 — API test harness (Must)

- **Status:** Done / deferred (why):
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Run the documented command that collects or lists API tests (`pytest --collect-only` or your harness equivalent).
  2. **Capture:** Terminal screenshot of collection (or first successful harness run).
  3. **Must show:** Test harness discovering API tests without requiring a manual UI click.
  4. **Must not show:** Database passwords in the command line.
  5. **Save as:** `docs/reports/images/sprint-06/s6-01-harness.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S6-02 — Auth API tests (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Run documented auth API tests (`pytest` path for register/login/me or equivalent).
  2. **Capture:** Terminal showing those tests passed.
  3. **Must show:** Auth-related tests green.
  4. **Must not show:** Secrets or full JWTs printed by debug logs—rerun with quieter logging if needed.
  5. **Save as:** `docs/reports/images/sprint-06/s6-02-auth-tests.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S6-03 — Ownership and stats tests (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Run ownership and stats-scoping tests.
  2. **Capture:** Terminal showing those tests passed.
  3. **Must show:** Cross-user / stats scope tests green.
  4. **Must not show:** Secrets.
  5. **Save as:** `docs/reports/images/sprint-06/s6-03-ownership-stats.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S6-04 — Mocked AI tests (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Run mocked `/ai/insights` (or provider) tests **without** live Ollama.
  2. **Capture:** Terminal showing mocked AI tests passed.
  3. **Must show:** Insights tests green with a mock/stub provider (no requirement that Ollama is running).
  4. **Must not show:** Real API keys.
  5. **Save as:** `docs/reports/images/sprint-06/s6-04-mocked-ai.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S6-05 — Frontend unit tests (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Run Vitest (or your documented frontend unit runner) from `frontend/`.
  2. **Capture:** Terminal showing frontend unit tests passed.
  3. **Must show:** Frontend unit test run green.
  4. **Must not show:** Secrets.
  5. **Save as:** `docs/reports/images/sprint-06/s6-05-vitest.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S6-06 — Document test commands (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the README section that lists exact commands to run backend and frontend tests.
  2. **Capture:** Screenshot of that section.
  3. **Must show:** Copy-pasteable test commands a classmate can run after clone.
  4. **Must not show:** Secrets.
  5. **Save as:** `docs/reports/images/sprint-06/s6-06-test-docs.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S6-07 — Rate limit AI insights (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Call `POST /ai/insights` repeatedly (or via a small script) until the documented rate limit triggers. Show the error/status in `/docs` or the UI.
  2. **Capture:** Screenshot of the rate-limit response (HTTP status and message your API returns).
  3. **Must show:** Limit enforced after too many calls (status/body matching your docs).
  4. **Must not show:** Tokens; crop Authorize.
  5. **Save as:** `docs/reports/images/sprint-06/s6-07-rate-limit.png`
  6. **Caption (1–2 sentences):** (state the limit you configured)
- **Used AI?** Yes / No

### S6-08 — Secrets and JWT review (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S6-09 — Ownership and CORS review (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S6-10 — security.md (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open `docs/security.md`. Scroll to the heading and the `localStorage` JWT XSS trade-off (and other checklist items you documented).
  2. **Capture:** Screenshot of those sections.
  3. **Must show:** `docs/security.md` exists with the localStorage JWT trade-off written in plain language.
  4. **Must not show:** Real production secrets pasted as “examples.”
  5. **Save as:** `docs/reports/images/sprint-06/s6-10-security-md.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S6-11 — Seed script (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Run the demo seed. Log in as the demo user (email only in the report). Open sessions (or Dashboard) showing realistic seeded **sessions**.
  2. **Capture:** Screenshot of seed command success **and** UI after login with sessions visible.
  3. **Must show:** Seed created a usable demo user with session history.
  4. **Must not show:** Demo password in the screenshot if avoidable; never paste production secrets. Email is enough to identify the user.
  5. **Save as:** `docs/reports/images/sprint-06/s6-11-seed.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S6-12 — deployment.md (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open `docs/deployment.md` covering Compose deploy, env/secrets, migrations, and what not to expose.
  2. **Capture:** Screenshot of the main headings/sections.
  3. **Must show:** Deployment runbook for API + DB (Compose-oriented), including env and exposure warnings.
  4. **Must not show:** Real cloud credentials.
  5. **Save as:** `docs/reports/images/sprint-06/s6-12-deployment-md.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S6-13 — README polish and demo script (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the README full demo path: seed → login → sessions → progress → insights (and Compose).
  2. **Capture:** Screenshot of that demo script / checklist section.
  3. **Must show:** End-to-end classmate demo path documented in one place.
  4. **Must not show:** Real secrets.
  5. **Save as:** `docs/reports/images/sprint-06/s6-13-readme-demo.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S6-14 — Final demo rehearsal fixes (Should)

- **Status:**
- **PR / commit:**
- **Demonstration:** (only if you did this ticket)
  1. **Do this:** Either paste short dry-run notes from a classmate following the README, or capture a short screenshot sequence of the full happy path.
  2. **Capture:** Notes image or collage of the path (login → sessions → progress → insights).
  3. **Must show:** Evidence you rehearsed the full demo and fixed blockers (notes or screenshots).
  4. **Must not show:** Tokens or passwords.
  5. **Save as:** `docs/reports/images/sprint-06/s6-14-rehearsal.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### Stretch (only if you did them)

For each stretch below that you completed: Status, PR / commit, Used AI? Add Demonstration for [S6-S1](../tickets/sprint-06-tickets.md#s6-s1--ci-workflow), [S6-S2](../tickets/sprint-06-tickets.md#s6-s2--playwright-smoke), [S6-S3](../tickets/sprint-06-tickets.md#s6-s3--security-headers), and [S6-S4](../tickets/sprint-06-tickets.md#s6-s4--optional-ollama-integration-test) (`pytest` skip or pass).

#### S6-S1 — CI workflow (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the Git host Actions (or equivalent) run for your CI workflow.
  2. **Capture:** Screenshot of a green / successful workflow.
  3. **Must show:** CI job success on push/PR as documented.
  4. **Must not show:** Secrets in logs.
  5. **Save as:** `docs/reports/images/sprint-06/s6-s1-ci.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

#### S6-S2 — Playwright smoke (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Run the Playwright smoke (login → create a **session** → open Progress, or your documented path).
  2. **Capture:** Terminal or HTML report showing the smoke passed.
  3. **Must show:** Browser smoke path green.
  4. **Must not show:** Passwords in trace screenshots—use a throwaway demo user and crop.
  5. **Save as:** `docs/reports/images/sprint-06/s6-s2-playwright.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

#### S6-S3 — Security headers (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Inspect response headers on a document or API response (DevTools Network or `curl -I`).
  2. **Capture:** Screenshot of the security-related headers you added.
  3. **Must show:** Documented headers present (names visible).
  4. **Must not show:** Cookies with session secrets if avoidable—crop values.
  5. **Save as:** `docs/reports/images/sprint-06/s6-s3-headers.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

#### S6-S4 — Optional Ollama integration test (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Run the documented integration test; show skip (Ollama down) or pass (Ollama up).
  2. **Capture:** Terminal screenshot of skip or pass.
  3. **Must show:** Documented skip/pass behavior without requiring graders to have Ollama.
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-06/s6-s4-pytest.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

## How we worked

Sprint 6 is **three weeks**.

- **Week 1** (API + frontend test breadth):
- **Week 2** (rate limit, security review, `security.md`):
- **Week 3** (seed, `deployment.md`, README polish, rehearsal):
- Who did what:
- One blocker and how you unblocked it:

## Decisions

Two to four technical choices with why (for example test DB strategy, rate-limit library, what you put in `deployment.md`).

1.
2.

## What we learned

Note what you actually used. Tools this sprint: pytest + TestClient / httpx, Vitest, rate limiting, `docs/security.md` / `docs/deployment.md`. Stretch if you did them: GitHub Actions, Playwright.

- What clicked:
- One thing you would do differently:

## Carry-over

Known issues, stretch leftovers, and notes for course handoff / demo day.

## AI usage (sprint-level reflection)

Mark **Used AI?** under each ticket above (`Yes` / `No`). Do **not** write per-ticket reflections there.

Here, cover your **overall** AI use during this sprint (Cursor, ChatGPT, Copilot, local coding assistants, etc.). Product Insights via Ollama in Sprint 5 does **not** count unless you also used an AI assistant to write code.

If you marked **No** on every ticket, write a short note that you did not use AI coding assistants this sprint (you may still answer verification / independence questions briefly).

- **Where AI helped most this sprint** (themes, ticket IDs, or areas—not a ticket-by-ticket dump):
- **What I typically accepted from AI suggestions:**
- **What I typically rejected or reworked, and why:**
- **How I verified AI-assisted work** (tests, `/docs`, manual demos, reviews):
- **What I can now explain or do independently** that I relied on AI for earlier:
- **Anything I would do differently with AI next sprint:**

Do not paste secrets, full JWTs, or `.env` values.

