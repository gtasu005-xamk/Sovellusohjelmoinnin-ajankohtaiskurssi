# Sprint 4 report — Analytics & progress

Copy this file to `docs/reports/sprint-04.md` in **your** repo and fill the blanks. Keep it a process log: no pasted source, no secrets, no `.env` values.

| Field | Your answer |
| ----- | ----------- |
| **Dates** | |
| **Names** | |
| **Repo URL** | |
| **Branch** | |

Tickets: [sprint-04-tickets.md](../tickets/sprint-04-tickets.md) · Index: [../README.md](../README.md)

## Sprint goal

From the tickets: turn stored sessions into stats and charts you can explain. You are done when stats endpoints match known fixtures; analytics unit tests pass without the full UI; Progress shows sessions over time and distance/intensity by activity; Dashboard period widgets match the API.

In your words (2–3 sentences): did you meet that, and what is still rough?

## Tickets

For **each** ticket fill **Status** and **PR / commit**.

Fill **Demonstration** only where this template includes that section. Follow the numbered steps exactly. Store images under `docs/reports/images/sprint-04/` using the suggested filename. Crop tokens.

For **every** ticket: set **Used AI?** to `Yes` or `No`. Write the sprint-level **AI usage** reflection at the end of this report (not under each ticket).

Skip stretch tickets you did not do. Stretch: Status, PR, and Used AI? for each stretch you did; add a Demonstration only where listed below.

### S4-01 — Analytics module skeleton (Must)

- **Status:** Done / deferred (why):
- **PR / commit:**
- **Used AI?** Yes / No

### S4-02 — Summary metrics (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S4-03 — Progress time series (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S4-04 — Streak metrics (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S4-05 — Analytics unit tests (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** From the documented working directory, run `pytest` for the analytics unit tests (pure Python—no UI required).
  2. **Capture:** Terminal screenshot of the test run.
  3. **Must show:** Analytics-related tests **passed** (summary / progress / streaks coverage as in your tickets).
  4. **Must not show:** Secrets in the environment dump.
  5. **Save as:** `docs/reports/images/sprint-04/s4-05-pytest.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S4-06 — Stats summary endpoint (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Authorize in `/docs`. Call `GET /stats/summary` for a **known** period where you already know expected totals from fixtures or seeded sessions.
  2. **Capture:** Screenshot of the `/docs` response JSON.
  3. **Must show:** Successful summary response for that period (counts/totals visible).
  4. **Must not show:** Full JWT; crop Authorize.
  5. **Save as:** `docs/reports/images/sprint-04/s4-06-summary.png`
  6. **Caption (1–2 sentences):** (state the period and expected numbers briefly)
- **Used AI?** Yes / No

### S4-07 — Stats progress endpoint (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** In `/docs`, call `GET /stats/progress` with period/granularity params you support.
  2. **Capture:** Screenshot of the time-series (or bucketed) JSON response.
  3. **Must show:** Progress payload with series/points for the authenticated user.
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-04/s4-07-progress-api.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S4-08 — Stats streaks endpoint (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** In `/docs`, call `GET /stats/streaks`.
  2. **Capture:** Screenshot of the streaks JSON.
  3. **Must show:** Streak metrics returned for the authenticated user (document whether null `session_at` rows are excluded).
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-04/s4-08-streaks.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S4-09 — User-scoped stats queries (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** As User A, call a stats endpoint and note totals. As User B (different account with different sessions), call the same endpoint. Confirm User A’s response does **not** include User B’s sessions (and vice versa).
  2. **Capture:** Two screenshots (A and B) or one collage; emails only in the caption.
  3. **Must show:** Aggregate IDOR prevented—User B’s data absent from User A’s stats.
  4. **Must not show:** Tokens or passwords.
  5. **Save as:** `docs/reports/images/sprint-04/s4-09-scoped-stats.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S4-10 — Recharts setup (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S4-11 — Progress page charts (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Log in, open Progress for a **known** period whose numbers you can explain (same fixtures as tests or a hand-counted set).
  2. **Capture:** Screenshot of the Progress charts.
  3. **Must show:** Charts rendered for that period (sessions over time and/or distance/intensity by activity as implemented).
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-04/s4-11-progress.png`
  6. **Caption (1–2 sentences):** (state expected numbers for the period)
- **Used AI?** Yes / No

### S4-12 — Period controls (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** On Progress, change period and/or granularity. Confirm charts refetch and update.
  2. **Capture:** Two screenshots (before and after the control change) or a single shot with the control and updated chart.
  3. **Must show:** Period/granularity control changing the displayed data.
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-04/s4-12-period.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S4-13 — Dashboard stat widgets (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open Dashboard for the **same** period you used on Progress. Compare widget numbers to Progress / `/stats/summary`.
  2. **Capture:** Screenshot of Dashboard widgets.
  3. **Must show:** Period widgets (session count, totals, average intensity, or your implemented set) matching the same period as Progress.
  4. **Must not show:** Tokens or another user’s stats.
  5. **Save as:** `docs/reports/images/sprint-04/s4-13-dashboard.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S4-14 — Stats README notes (Should)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the README (or `docs/stats.md`) section that documents stats endpoints, tests, and how to interpret periods/`session_at`.
  2. **Capture:** Screenshot of that documentation.
  3. **Must show:** Classmate-facing notes for stats/test commands or endpoint contract.
  4. **Must not show:** Secrets.
  5. **Save as:** `docs/reports/images/sprint-04/s4-14-readme.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### Stretch (only if you did them)

For each stretch below that you completed: Status, PR / commit, Used AI? Add Demonstration when the extra UI or download is visible ([S4-S1](../tickets/sprint-04-tickets.md#s4-s1--goal-progress-percent), [S4-S2](../tickets/sprint-04-tickets.md#s4-s2--period-over-period), [S4-S3](../tickets/sprint-04-tickets.md#s4-s3--csv-export)).

#### S4-S1 — Goal progress percent (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Show goal progress percent in UI or `/docs`.
  2. **Capture:** Screenshot of the percent / progress display.
  3. **Must show:** Goal progress visible for the logged-in user.
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-04/s4-s1-goal-progress.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

#### S4-S2 — Period over period (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Show period-over-period comparison in UI or API response.
  2. **Capture:** Screenshot of the comparison.
  3. **Must show:** Two periods compared with clear labels.
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-04/s4-s2-pop.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

#### S4-S3 — CSV export (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Trigger CSV export; show the download dialog or open the file header rows (no secrets).
  2. **Capture:** Screenshot of download UI or CSV opened with sample rows.
  3. **Must show:** Export produced a CSV for the user’s stats/sessions as documented.
  4. **Must not show:** Tokens in the URL.
  5. **Save as:** `docs/reports/images/sprint-04/s4-s3-csv.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

## How we worked

Sprint 4 is **three weeks**.

- **Week 1** (analytics module + unit tests):
- **Week 2** (`/stats/summary`, `/stats/progress`, `/stats/streaks`):
- **Week 3** (Progress charts, period controls, Dashboard widgets):
- Who did what:
- One blocker and how you unblocked it:

## Decisions

Two to four technical choices with why (for example how you define a streak, which `session_at` rows count).

1.
2.

## What we learned

Note what you actually used. Tools this sprint: pytest, dataclasses / TypedDict, Recharts, TanStack Query (period filters). Sprint 4 Must is **pure Python** in the API—not pandas.

- What clicked:
- One thing you would do differently:

## Carry-over

Deferred Must/Should, stretch leftovers, risks for [Sprint 5 tickets](../tickets/sprint-05-tickets.md) (Ollama insights).

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

