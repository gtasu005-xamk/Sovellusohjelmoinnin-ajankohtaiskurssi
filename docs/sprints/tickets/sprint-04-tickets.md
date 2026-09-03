# Sprint 4 tickets — Analytics & Progress Visualization

Backlog for Sprint 4 ([index](../README.md)). Copy tickets into your issue tracker if you like; keep the IDs (`S4-01`, …) in branch and PR titles.

## Your task for Sprint 4

The training floor from Sprint 3 is in use: members log **sessions** with planned/actual measurements, **clone** sessions for reuse, assign them to **plans** via `plan_id`, and use an in-app **calendar**. Staring at raw rows in the logbook will not tell them if they are getting fitter.

Sprint 4 is the **scoreboard**. Ship pure Python analytics over session and measurement history, authenticated `/stats/*` endpoints, a Progress page with charts, and Dashboard widgets that match the same numbers. You are not shipping new session CRUD, AI insights, or rate limits—on purpose. Later sprints assume these stats exist and stay **user-scoped** (never hang User A’s totals on User B’s wall).

Keep analytics as **pure functions** over plain data (lists / dataclasses). Routers stay thin: load the current user’s sessions + measurements, call the same functions your unit tests call. Those same numbers become the facts Sprint 5’s house coach will read.

```text
Sprint 3 data                         Sprint 4
──────────────                        ────────
Sessions (+ session_at)          →    summary / streaks
  items + measurements           →    progress time series
  (unit slugs: duration_min, …)  →    /stats/* + charts
```

**Aggregate rules (aligned with Sprint 3):**

- **Duration / distance** → from measurements by unit slug (`duration_min`, `distance_km`, …)—not fixed columns on the session
- **Session counts / calendar / streaks** → prefer sessions with **non-null** `session_at` (unscheduled program-definition rows with empty actuals usually stay out of “did I train this week?”). Prefer **actual** measurement values when aggregating; document if you fall back to planned.
- **Always user-scoped** → same ownership mindset as Sprint 3 IDOR (no global aggregates)

Say **sessions** and **measurements** in new code and docs—not “workouts.”

### What success looks like

When you finish Sprint 4, you should be able to demo:

1. Analytics unit tests pass on known fixtures (no UI required)
2. `GET /stats/summary`, `/stats/progress`, and `/stats/streaks` return auth-scoped results
3. Progress page charts update when period / granularity change
4. Dashboard widgets match `/stats/summary` for the same period

**Suggested demo flow:** seed or enter known sessions → run `pytest` for analytics → open Progress → change week/month → show Dashboard widgets match → briefly show User B does not see User A’s stats.

That demo unlocks Sprint 5 (AI insights packed from the same personal history).

### Prerequisites from Sprint 3

This backlog assumes you already have:

- Authenticated session CRUD with items + measurements
- Seeded unit catalog (exercise-level activities; Running → duration + distance; strength exercises → reps/weight `per_set`, …)
- Sprint 3 sessions with planned/actual, clone, plans via `plan_id`, calendar API/UI
- JWT + protected React layout; TanStack Query on the frontend
- Dashboard with recent sessions (you will add widgets beside it, not replace it)

If those are missing, finish or stabilize [Sprint 3 tickets](sprint-03-tickets.md) first—charts on empty or leaky data waste the week.

Sprint 1 Compose and Sprint 2 auth/catalog are still assumed underneath.

### New tools & technologies

| Tool / technology               | Role in this sprint                           |
| ------------------------------- | --------------------------------------------- |
| **pytest**                      | Unit tests for pure analytics functions       |
| **dataclasses** / **TypedDict** | Typed in-memory session/measurement inputs    |
| **Recharts**                    | Progress charts (sessions / volume over time) |
| **TanStack Query** (deeper use) | Period filters, refetch, Dashboard widgets    |

_(Carried forward: sessions/measurements API, JWT, protected UI from Sprints 2–3.)_

### What you will learn

- Implement analytics as pure, testable Python in `services/`
- Expose summary, progress, and streak metrics via layered FastAPI (`api` → `services` → `repositories`)
- Write `pytest` unit tests for aggregation logic
- Visualize progress with Recharts + TanStack Query
- Keep stats **user-scoped** (aggregate IDOR prevention)

### Backend layered architecture

Stats features follow the same call direction as health, auth, and sessions. **Outer layers may call inward; inward layers must not import outward.**

```text
api/stats.py  →  services/stats.py  →  repositories/session.py (read)
                      ↓
              services/analytics.py   ← pure functions (no FastAPI, no DB)
                      ↑
               schemas/stats.py
```

| Layer                   | Responsibility                                                      |
| ----------------------- | ------------------------------------------------------------------- |
| `api/`                  | HTTP only — auth, query params, status codes                        |
| `schemas/`              | Pydantic DTOs for stats responses                                   |
| `services/stats.py`     | Load the current user’s range; call analytics                       |
| `services/analytics.py` | Pure aggregation math (no FastAPI, no SQLAlchemy)                   |
| `repositories/`         | SQLAlchemy reads of **this user’s** sessions and measurements       |

Do **not** put aggregation math only inside route handlers. Do **not** accept another user’s id from the client when loading stats.

### Out of scope (intentionally later / already done)

| Topic                                                     | When it arrives            |
| --------------------------------------------------------- | -------------------------- |
| AI insights over these stats                              | Sprint 5                   |
| Broader API/UI test harness, rate limits, deployment docs | Sprint 6 (optional)        |
| New session/plan/calendar/clone or catalog redesign       | Sprints 2–3 (already done) |
| Replacing JWT / `localStorage`                            | optional Sprint 6 discussion |

### Week-by-week map

| Week  | Focus                                            | Ticket IDs    | Checkpoint                                       |
| ----- | ------------------------------------------------ | ------------- | ------------------------------------------------ |
| **1** | Analytics module + unit tests                    | S4-01 … S4-05 | `pytest` covers summary / progress / streaks     |
| **2** | Stats API + user scoping                         | S4-06 … S4-09 | Authenticated API matches unit-test expectations |
| **3** | Recharts, Progress page, Dashboard widgets, docs | S4-10 … S4-14 | Charts/widgets update when filters change        |

### How the tickets fit together

```text
Week 1                         Week 2                      Week 3
────────                       ────────                    ────────
analytics.py skeleton          GET /stats/summary          Recharts setup
Summary metrics                GET /stats/progress         Progress page charts
Progress time series           GET /stats/streaks          Period controls
Streak metrics                 User-scoped audit           Dashboard widgets
pytest fixtures                                              README / stats notes
```

Do **Must** tickets first, then **Should** (S4-14), then **Stretch** if you have time.

**How to read each ticket:** **New here** explains the concept and lists **Docs & tutorials**. **Your task** states the deliverable. **Instructions** walk through the work. **Stay in scope** keeps later-sprint features out of this ticket. **Commit** means create a new Git commit when the ticket is done (ticket ID in the message).

### Ticket index

| ID                                         | Title                     | Week | Priority | Estimate |
| ------------------------------------------ | ------------------------- | ---- | -------- | -------- |
| [S4-01](#s4-01--analytics-module-skeleton) | Analytics module skeleton | 1    | Must     | S        |
| [S4-02](#s4-02--summary-metrics)           | Summary metrics           | 1    | Must     | M        |
| [S4-03](#s4-03--progress-time-series)      | Progress time series      | 1    | Must     | L        |
| [S4-04](#s4-04--streak-metrics)            | Streak metrics            | 1    | Must     | M        |
| [S4-05](#s4-05--analytics-unit-tests)      | Analytics unit tests      | 1    | Must     | M        |
| [S4-06](#s4-06--stats-summary-endpoint)    | Stats summary endpoint    | 2    | Must     | M        |
| [S4-07](#s4-07--stats-progress-endpoint)   | Stats progress endpoint   | 2    | Must     | M        |
| [S4-08](#s4-08--stats-streaks-endpoint)    | Stats streaks endpoint    | 2    | Must     | S        |
| [S4-09](#s4-09--user-scoped-stats-queries) | User-scoped stats queries | 2    | Must     | M        |
| [S4-10](#s4-10--recharts-setup)            | Recharts setup            | 3    | Must     | S        |
| [S4-11](#s4-11--progress-page-charts)      | Progress page charts      | 3    | Must     | L        |
| [S4-12](#s4-12--period-controls)           | Period controls           | 3    | Must     | M        |
| [S4-13](#s4-13--dashboard-stat-widgets)    | Dashboard stat widgets    | 3    | Must     | M        |
| [S4-14](#s4-14--stats-readme-notes)        | Stats README notes        | 3    | Should   | S        |
| [S4-S1](#s4-s1--goal-progress-percent)     | Goal progress percent     | —    | Stretch  | M        |
| [S4-S2](#s4-s2--period-over-period)        | Period-over-period        | —    | Stretch  | M        |
| [S4-S3](#s4-s3--csv-export)                | CSV export                | —    | Stretch  | S        |

---

## S4-01 — Analytics module skeleton

| Field          | Value                                                                               |
| -------------- | ----------------------------------------------------------------------------------- |
| **Type**       | feature                                                                             |
| **Week**       | 1                                                                                   |
| **Priority**   | Must                                                                                |
| **Estimate**   | S                                                                                   |
| **Depends on** | Sprint 3 sessions + measurements in DB (and models you can shape into plain inputs) |

### New here: pure analytics vs HTTP/DB layers

**Pure analytics** means functions that take in-memory data and return numbers—no FastAPI, no SQLAlchemy `Session`, no HTTP. You pass in a list of session-shaped objects (already loaded and already scoped to one user) and get summaries, series points, or streaks back.

Why this split matters:

- Week 1 unit tests can run without Postgres or Uvicorn
- Week 2 routers stay thin: load → call analytics → return JSON
- Sprint 5 can reuse the same summaries as AI context without copying SQL

Typed inputs should represent **session + measurement** rows. Include `session_at`, intensity, activity type, and unit values such as `duration_min` / `distance_km` from Sprint 2 slugs. Callers—not this module—are responsible for filtering by the logged-in user.

**Docs & tutorials:**

- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html) — typed analytics inputs
- [typing — TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict) — alternative to dataclasses
- Layering reminder: keep routers thin (same as Sprint 1–3)

### Your task

Create a dedicated analytics module of pure Python so you can unit-test math without FastAPI or Postgres. Your deliverable is `services/analytics.py` with typed session/measurement inputs and a note that callers pass **already user-filtered** lists.

### Instructions

1. Create an analytics module under `services/` (not inside routers)—typically `backend/app/services/analytics.py`.
2. Define typed inputs (dataclasses or TypedDict) for session + measurement shaped data. Include fields you will need for later tickets: `session_at`, intensity, activity type, and measurement values keyed by unit slug.
3. Keep core functions free of FastAPI and SQLAlchemy imports so unit tests stay fast.
4. Document that callers pass **already user-filtered** lists. This module must not query the database.

### Stay in scope

- Leave summary / series / streak implementations for S4-02 … S4-04; a typed skeleton that imports cleanly is enough here.
- Leave HTTP endpoints for Week 2 (S4-06+). Do not import FastAPI in `analytics.py`.
- Leave Recharts, the Progress page, and Dashboard widgets for Week 3.
- Do not add session CRUD or change the catalog. Do not start Sprint 5 AI.
- In new names and comments, use **sessions** / **measurements**, not “workouts.”

### Hints

- Repositories load; analytics compute. If you feel the urge to `db.query(...)` here, you are in the wrong layer.
- A short module docstring that says “pure functions; no I/O” helps teammates keep it that way.

### Acceptance criteria

- [ ] Module lives under services (not inside routers)
- [ ] Input types documented briefly
- [ ] No FastAPI imports required to call core functions

### Suggested paths

`backend/app/services/analytics.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-01` in the message, for example `S4-01: short summary`. Never commit `.env` or secrets.

---

## S4-02 — Summary metrics

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 1       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S4-01   |

### New here: summarizing a period

A **summary** answers “how did this period go?” with a handful of numbers: session count, total duration, total distance, average intensity, and a per–activity-type breakdown.

Duration and distance are **not** columns on the session row. They live on **measurements**, keyed by Sprint 2 unit slugs (`duration_min`, `distance_km`, …). Sum **actual** values when present (document planned fallback if any). Session count and calendar-oriented summaries should prefer rows with **non-null** `session_at` unless you document including unscheduled rows.

Empty input must be safe: zeros or empty breakdowns, not exceptions. Decide whether missing distance measurements count as 0 in totals, and whether average intensity on an empty set is `0` or `null`—then document the choice.

**Docs & tutorials:**

- [statistics — mean](https://docs.python.org/3/library/statistics.html) — optional helper for averages
- [Python sum / generator expressions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) — aggregating measurement values

### Your task

Compute period summaries from measurement unit slugs so Dashboard widgets and `/stats/summary` share one source of truth. Your deliverable is summary functions in `analytics.py` that handle empty input safely and include a per-type breakdown.

### Instructions

1. Compute session count, total duration, total distance, and average intensity for a set of sessions.
2. Pull duration and distance from **measurements by unit slug**—not from invented session fields.
3. Include a breakdown by activity type (distance and/or session count).
4. Handle empty input safely (zeros / empty breakdowns). Document average intensity for an empty set (`0` or `null`).
5. Prefer non-null `session_at` for calendar-oriented summaries unless you document otherwise.
6. Keep the return shape JSON-friendly so Week 2 can map it to `/stats/summary` without rewriting the math.

### Stay in scope

- Leave the HTTP endpoint for S4-06. This ticket is pure functions only.
- Leave time-series buckets for S4-03 and streaks for S4-04.
- Do not query the database inside `analytics.py`.
- Do not add session CRUD or AI. Do not call domain rows “workouts.”

### Hints

- Decide whether missing distance measurements count as 0 in totals, and write that decision in a docstring.
- `statistics.mean` is optional; a simple loop is fine if you document empty-set behaviour.

### Acceptance criteria

- [ ] Empty input returns zeros / empty breakdowns safely
- [ ] Average intensity defined for empty set (0 or null—document choice)
- [ ] Per-type breakdown included
- [ ] Duration/distance come from measurement unit slugs

### Suggested paths

`backend/app/services/analytics.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-02` in the message, for example `S4-02: short summary`. Never commit `.env` or secrets.

---

## S4-03 — Progress time series

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 1       |
| **Priority**   | Must    |
| **Estimate**   | L       |
| **Depends on** | S4-01   |

### New here: bucketing by week or month

A **time series** groups values into week or month **buckets** so a chart can plot “sessions over time” or “distance over time.” Inconsistent bucket edges (one function starts weeks on Sunday, another on Monday) make Progress lines look wrong even when the totals are right.

Pick a convention and stick to it. **ISO weeks starting Monday** are a common, easy-to-explain choice (`date.isocalendar()`). Bucket using **`session_at`**; skip nulls or document how you treat unscheduled sessions.

Support at least **session count** and one volume metric (**duration** or **distance** from measurement unit slugs). Return points that Recharts can consume, for example `{ period_label, value }`.

**Docs & tutorials:**

- [datetime — timedelta / date](https://docs.python.org/3/library/datetime.html) — period math
- [ISO week date](https://docs.python.org/3/library/datetime.html#datetime.date.isocalendar) — consistent week labels

### Your task

Build week/month time series so Progress charts have honest buckets, not ad-hoc date strings. Your deliverable is series functions in `analytics.py` for session count plus at least one volume metric, with consistent week/month boundaries.

### Instructions

1. Build a time series for a chosen metric with `week` or `month` granularity.
2. Support at least session count and one volume metric (duration or distance from measurement unit slugs).
3. Align buckets to week/month boundaries consistently. Document the week-start convention (ISO Monday is recommended).
4. Bucket using `session_at` (skip nulls, or document including them).
5. Allow optional activity-type filtering at the series level, or document that filtering will be API-only in S4-07.
6. Return points as `{ period_label, value }` (or similar) ready for Recharts.

### Stay in scope

- Leave `GET /stats/progress` for S4-07. Do not add FastAPI here.
- Leave the Progress page for Week 3. A JSON-friendly list of points is enough.
- Do not hide bucketing only in SQL. Keep it in `analytics.py` so S4-05 can assert it.
- Do not add session CRUD, AI, or a second chart library.

### Hints

- Freeze dates in your head (and later in fixtures) so “week 12” means the same thing in tests and in the UI.
- Empty history → empty list of points, not a crash.

### Acceptance criteria

- [ ] Supports at least session count and one volume metric (duration or distance)
- [ ] Buckets align to week/month boundaries consistently
- [ ] Optional filter by activity type at the series level (or documented as API-only)

### Suggested paths

`backend/app/services/analytics.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-03` in the message, for example `S4-03: short summary`. Never commit `.env` or secrets.

---

## S4-04 — Streak metrics

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 1       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S4-01   |

### New here: consistency streaks

A **streak** is a simple consistency story: current and longest run of **days or weeks** with at least one session. The number is only useful if tests, API, and UI share **one definition**.

Write that definition in a docstring before you code the loop. Be explicit about:

- Calendar **days** vs **weeks**
- Whether “today” must already have a session to count
- Whether unscheduled sessions (`session_at` null) count—**prefer non-null `session_at`** unless you explicitly include them

Empty or sparse histories must return zeros, not exceptions.

**Docs & tutorials:**

- [set of dates / sorted unique days](https://docs.python.org/3/tutorial/datastructures.html#sets) — build day sets from `session_at`

### Your task

Compute current and longest streaks from a documented definition so Week 2’s `/stats/streaks` never invents a second meaning. Your deliverable is streak functions in `analytics.py` that return JSON-friendly fields and survive sparse histories.

### Instructions

1. Compute current streak and longest streak (days or weeks with ≥1 session—pick one and document it).
2. Base streaks on non-null `session_at` dates unless you explicitly include unscheduled sessions in the docstring.
3. Write the streak definition in a docstring (days vs weeks, and whether “today” must count).
4. Return structured fields suitable for JSON (e.g. `current` and `longest`).
5. Verify sparse histories and empty input do not crash (zeros, not exceptions).

### Stay in scope

- Leave `GET /stats/streaks` for S4-08.
- Leave Dashboard widgets for S4-13; this ticket is the math only.
- Do not query the database in `analytics.py`.
- Do not add AI coaching copy about streaks (Sprint 5). Do not add session CRUD.

### Hints

- Building a `set` of unique calendar dates from `session_at`, then walking consecutive days, is usually enough.
- If two sessions fall on the same day, that is still one “active” day.

### Acceptance criteria

- [ ] Definition of streak documented in docstring
- [ ] Works with sparse histories
- [ ] Returns structured fields suitable for JSON

### Suggested paths

`backend/app/services/analytics.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-04` in the message, for example `S4-04: short summary`. Never commit `.env` or secrets.

---

## S4-05 — Analytics unit tests

| Field          | Value               |
| -------------- | ------------------- |
| **Type**       | test                |
| **Week**       | 1                   |
| **Priority**   | Must                |
| **Estimate**   | M                   |
| **Depends on** | S4-02, S4-03, S4-04 |

### New here: fixture-based analytics tests

**Unit tests** with known session/measurement fixtures prove the math **before** HTTP exists. You construct a small in-memory list (plain dataclasses / dicts), call `analytics.py`, and assert numbers. No Postgres, no TestClient, no browser.

**pytest** collects functions named `test_*` and reports pass/fail. **Fixtures** are reusable known datasets—freeze dates so week/month buckets stay deterministic.

Prefer session + measurement shaped fixtures (Running-like duration/distance, strength per-set with actuals). Do not flatten everything into a legacy “workout” row; that fights Sprint 3’s model. Do not treat separate template tables as part of this sprint—Sprint 3 reuses sessions via clone.

**Docs & tutorials:**

- [pytest](https://docs.pytest.org/en/stable/) — write and run tests
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) — known session datasets

### Your task

Give graders and teammates a `pytest` suite that asserts the same numbers you will later show in charts. Your deliverable is tests over plain fixtures covering summary, series, streaks, and at least one empty-list edge case.

### Instructions

1. Add pytest fixtures with known **sessions + measurements** (not a flat legacy “workout” row). Freeze dates so bucket boundaries stay deterministic.
2. Assert summary totals, series buckets, and streaks against expected values.
3. Cover at least one edge case (empty list).
4. Include both Running-like (duration/distance from unit slugs) and strength per-set actuals if useful.
5. Document the `pytest` command/path (for example `pytest backend/tests/test_analytics.py` from the repo root, or the equivalent from `backend/`).

### Stay in scope

- Leave FastAPI `TestClient` / live Postgres API tests for optional Sprint 6. Plain fixtures are enough here.
- Do not start the Progress UI in this ticket.
- Do not add rate-limit or load tests (Sprint 6).
- Keep tests calling `analytics.py` directly—no database session required.

### Hints

- If a test needs Docker to pass, the functions are not pure enough yet—push I/O back to repositories.
- One fixture file shared by summary / series / streak tests avoids copy-paste drift.

### Acceptance criteria

- [ ] Tests run without Postgres if using plain fixtures
- [ ] At least one edge case (empty list) covered
- [ ] Command documented (`pytest` path)

### Suggested paths

`backend/tests/test_analytics.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-05` in the message, for example `S4-05: short summary`. Never commit `.env` or secrets.

---

## S4-06 — Stats summary endpoint

| Field          | Value                                    |
| -------------- | ---------------------------------------- |
| **Type**       | feature                                  |
| **Week**       | 2                                        |
| **Priority**   | Must                                     |
| **Estimate**   | M                                        |
| **Depends on** | S4-02, Sprint 2 JWT (`get_current_user`) |

### New here: thin stats router

`GET /stats/summary?from=&to=` is the HTTP face of S4-02. The router should:

1. Require auth (`Depends(get_current_user)`)
2. Parse the date range
3. Load **only the current user’s** sessions (with measurements) in that range
4. Call the same pure summary functions your tests already cover
5. Return JSON that matches a Pydantic schema (visible in OpenAPI `/docs`)

That is the same layered flow as Sprint 1 `/health` and Sprint 3 session routes: `api` → `services` → `repositories`. Aggregation does **not** belong in the route handler.

**Docs & tutorials:**

- [FastAPI — Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/) — `from` / `to`
- [FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) — `get_current_user`

### Your task

Expose period summaries over HTTP so Dashboard widgets and OpenAPI demos call one contract. Your deliverable is an authenticated `GET /stats/summary` that delegates aggregation to `analytics.py`.

### Instructions

1. Implement `GET /stats/summary?from=&to=` with auth required.
2. Load only the current user’s sessions (with measurements) in the date range via repository → stats service.
3. Call pure summary analytics; do not reimplement aggregation in the route.
4. Validate date query params; align range semantics with Sprint 3 session filters when possible.
5. Document the response in OpenAPI / `schemas/stats.py`.
6. Prefer non-null `session_at` when choosing which sessions count in the period, consistent with S4-02.

### Stay in scope

- Leave `/stats/progress` for S4-07 and `/stats/streaks` for S4-08.
- Do not add new session CRUD. This endpoint is read-only over existing history.
- Do not accept a `user_id` from the query/body—scope comes from the JWT (S4-09 will audit this).
- Do not add AI insights or rate limits.

### Hints

- Layer: `api/stats.py` → `services/stats.py` → `repositories/session.py` → `analytics.py`.
- `from` is a Python builtin; a query alias like `date_from` / `from_` is fine if you document it.

### Acceptance criteria

- [ ] Auth required
- [ ] Date range applied
- [ ] Response matches OpenAPI schema
- [ ] Aggregation delegated to pure analytics functions

### Suggested paths

`backend/app/api/stats.py`, `backend/app/services/stats.py`, `backend/app/schemas/stats.py`, `backend/app/repositories/session.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-06` in the message, for example `S4-06: short summary`. Never commit `.env` or secrets.

---

## S4-07 — Stats progress endpoint

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 2       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S4-03   |

### New here: series API for charts

`GET /stats/progress` returns the bucketed points Recharts will plot. Typical query params: **metric**, optional **`activity_type_id`**, **`granularity=week|month`**, plus a date range.

Keep metric names stable (`sessions`, `duration_min`, `distance_km`, …) and document them. Volume metric names should match **unit slugs** where they represent measurements. Invalid metric or granularity should fail clearly (`422` or `400`), not return an empty chart that looks like “no training.”

Optional `activity_type_id` filters **before** bucketing, using Sprint 2 catalog IDs—not parallel type strings.

**Docs & tutorials:**

- [FastAPI — Query validation](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/) — constrain metric / granularity
- [Pydantic Field constraints](https://docs.pydantic.dev/latest/concepts/fields/) — enums for allowed metrics

### Your task

Give the Progress page a series endpoint with validated params and user-scoped points. Your deliverable is authenticated `GET /stats/progress` that reuses S4-03 analytics and rejects bad metric/granularity values.

### Instructions

1. Implement `GET /stats/progress?metric=&activity_type_id=&granularity=week|month` (plus date range).
2. Reject invalid metric/granularity with 422/400.
3. Return series points suitable for charting (period label + value).
4. Scope to `current_user` only. Load via repository → stats service → `analytics.py`.
5. Apply optional `activity_type_id` before bucketing. Reuse Sprint 2 activity type IDs from the catalog.
6. Document allowed metric names (align volume names with unit slugs).

### Stay in scope

- Leave the Progress UI for S4-11. OpenAPI + JSON is the deliverable here.
- Do not reimplement bucketing in the router—call S4-03 functions.
- Do not add session CRUD, AI, or rate limits.
- Do not accept an arbitrary `user_id` from the client.

### Hints

- A Pydantic `Literal` or enum for metric and granularity keeps OpenAPI honest.
- Empty series (valid params, no sessions) is `200` with `[]`—not 404.

### Acceptance criteria

- [ ] Invalid metric/granularity → 422/400
- [ ] Optional activity_type_id filter works
- [ ] Series points suitable for charting (period label + value)

### Suggested paths

`backend/app/api/stats.py`, `backend/app/services/stats.py`, `backend/app/schemas/stats.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-07` in the message, for example `S4-07: short summary`. Never commit `.env` or secrets.

---

## S4-08 — Stats streaks endpoint

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 2       |
| **Priority**   | Must    |
| **Estimate**   | S       |
| **Depends on** | S4-04   |

### New here: exposing tested streak definitions

`GET /stats/streaks` must call the **same** streak functions covered in S4-05. If the UI later shows “12 days” and the tests say “12 days,” graders trust the demo. If the route invents a second loop, they will not.

Decide whether streaks are **all-history** or a **bounded window**, document it in OpenAPI, and keep the handler tiny. Base streaks on **non-null `session_at`** unless you documented otherwise in S4-04.

**Docs & tutorials:**

- [FastAPI — Response Model](https://fastapi.tiangolo.com/tutorial/response-model/) — streak DTO

### Your task

Expose the tested streak definition over HTTP so widgets never invent a second meaning of “streak.” Your deliverable is authenticated `GET /stats/streaks` that calls S4-04 functions and is documented in OpenAPI.

### Instructions

1. Implement `GET /stats/streaks` for the current user (auth required).
2. Load that user’s sessions (prefer non-null `session_at`) via repository → stats service.
3. Call the same streak functions tested in S4-05—do not rewrite the definition in the route.
4. Document the response in OpenAPI (all-history vs bounded window—pick one).

### Stay in scope

- Leave Dashboard streak widgets for S4-13 if you show them there; this ticket is the API.
- Do not add AI commentary on streaks (Sprint 5).
- Do not add session CRUD or rate limits.
- Do not accept `user_id` from the client.

### Hints

- Keep the handler tiny: auth, load, call analytics, return schema.
- If S4-04’s docstring and the OpenAPI description disagree, fix one of them now.

### Acceptance criteria

- [ ] Auth required
- [ ] Uses same streak definitions as unit-tested functions
- [ ] Documented in OpenAPI

### Suggested paths

`backend/app/api/stats.py`, `backend/app/services/stats.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-08` in the message, for example `S4-08: short summary`. Never commit `.env` or secrets.

---

## S4-09 — User-scoped stats queries

| Field          | Value                                           |
| -------------- | ----------------------------------------------- |
| **Type**       | feature                                         |
| **Week**       | 2                                               |
| **Priority**   | Must                                            |
| **Estimate**   | M                                               |
| **Depends on** | S4-06, S4-07, S4-08, Sprint 3 ownership mindset |

### New here: aggregate IDOR

**IDOR** (Insecure Direct Object Reference) in Sprint 3 meant “change the session id in the URL and see someone else’s session.” **Aggregate IDOR** is the same class of bug for stats: a global `SELECT` that summarizes **every** user’s sessions, or a query param `user_id` taken from the client.

Every stats path must filter by `current_user.id` **before** aggregation. The service layer must not accept an arbitrary `user_id` from the body or query string. Repositories should take `user_id` from the authenticated user only.

This is a privacy bug **and** a false demo: mixed-user averages look like progress that nobody actually did.

**Docs & tutorials:**

- [OWASP — Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) — same idea for aggregates
- Align with [S3-10 ownership](sprint-03-tickets.md#s3-10--ownership-enforcement)

### Your task

Audit `/stats/*` so User A’s summaries, series, and streaks ignore User B’s sessions. Your deliverable is user-scoped queries on every stats path, plus a two-user proof (manual or test) that aggregates do not leak.

### Instructions

1. Audit every stats query path (`summary`, `progress`, `streaks`) so it filters by `current_user.id` before aggregation.
2. Ensure the service layer does not accept an arbitrary `user_id` from the client body or query.
3. Pass `user_id` into repositories from the authenticated user only—never from an unchecked request field.
4. Prove with two users’ data (manual steps or a test) that A’s stats ignore B’s sessions.

### Stay in scope

- Do not add new session CRUD to “fix” scoping; filter reads instead.
- Do not add rate limits or a full API test harness (Sprint 6). A focused two-user check is enough.
- Do not start AI context packing (Sprint 5)—but the same ownership rule will apply there.
- Leave charts for Week 3; this ticket is backend scoping.

### Hints

- Optional Sprint 6 can automate more of this—leave a test hook if you can.
- Align failure style with [S3-10 ownership](sprint-03-tickets.md#s3-10--ownership-enforcement) (you should not be able to “select” another user at all).

### Acceptance criteria

- [ ] No global aggregates across users
- [ ] Manual or test proof with two users’ data
- [ ] Service layer does not accept arbitrary user_id from the client body

### Suggested paths

`backend/app/api/stats.py`, `backend/app/services/stats.py`, `backend/app/repositories/session.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-09` in the message, for example `S4-09: short summary`. Never commit `.env` or secrets.

---

## S4-10 — Recharts setup

| Field          | Value                                                 |
| -------------- | ----------------------------------------------------- |
| **Type**       | feature                                               |
| **Week**       | 3                                                     |
| **Priority**   | Must                                                  |
| **Estimate**   | S                                                     |
| **Depends on** | Sprint 3 frontend (protected routes + TanStack Query) |

### New here: Recharts

**Recharts** is a React chart library built on SVG. You pass arrays of `{ name, value }` (or similar) into components like `LineChart` / `BarChart`, and it draws axes, lines, and tooltips.

Install **one** chart library. Adding Chart.js *and* Recharts in the same sprint is extra weight with no teaching benefit. Render a Progress page **shell** with **sample data** first—then S4-11 swaps in `/stats/progress`. That way you debug “does a chart render at all?” separately from “does the API series match?”

The route should be auth-gated like other Sprint 3 pages.

**Docs & tutorials:**

- [Recharts documentation](https://recharts.org/en-US/) — LineChart / BarChart basics
- [Recharts — Getting started](https://recharts.org/en-US/guide/getting-started) — first chart

### Your task

Add Recharts and a Progress page shell with sample data so you can see a chart before wiring the stats API. Your deliverable is one chart library in `package.json` plus an auth-gated Progress route that renders a sample chart.

### Instructions

1. Add Recharts (or the agreed single library) to the frontend package.
2. Add an auth-gated Progress route and a page shell (e.g. `ProgressPage.tsx`).
3. Render a sample chart with static data (sessions over time is a good first plot).
4. Optionally add a thin wrapper under `components/charts/` so S4-11 does not dump SVG markup into the page.

### Stay in scope

- Leave live `/stats/progress` wiring for S4-11. Sample data is enough here.
- Leave period controls for S4-12 and Dashboard widgets for S4-13.
- Do not add a second heavy chart library.
- Do not add session CRUD or AI Insights UI.

### Hints

- Start with static sample data, then swap to API data in S4-11.
- If the page is blank, check the protected layout from Sprint 2—unauthenticated users should be redirected, not see a broken chart.

### Acceptance criteria

- [ ] Dependency added to frontend package
- [ ] Sample chart renders in Progress page shell
- [ ] No unrelated heavy chart libs added

### Suggested paths

`frontend/package.json`, `frontend/src/pages/ProgressPage.tsx`, `frontend/src/components/charts/`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-10` in the message, for example `S4-10: short summary`. Never commit `.env` or secrets.

---

## S4-11 — Progress page charts

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 3            |
| **Priority**   | Must         |
| **Estimate**   | L            |
| **Depends on** | S4-07, S4-10 |

### New here: charts driven by stats API

The Progress page is the visual answer to “Am I improving?” It consumes `/stats/progress` and/or the summary breakdown via **TanStack Query** (Sprint 3). Show **sessions over time** and **volume or intensity by activity type**.

Use the shared API client + Bearer token from Sprint 2. Put filter params in Query keys so S4-12 can refetch correctly. Empty data must show an **empty state**, not NaN axes or a crashed SVG.

Auth-gate the page. This is not a public marketing chart.

**Docs & tutorials:**

- [TanStack Query — useQuery](https://tanstack.com/query/latest/docs/framework/react/reference/useQuery) — fetch series
- [Recharts — LineChart](https://recharts.org/en-US/api/LineChart) — map API points to chart props

### Your task

Wire Progress charts to `/stats/progress` (and/or summary breakdown) so graders see real history, not sample arrays. Your deliverable is an auth-gated Progress page with sessions-over-time and volume/intensity-by-type charts, plus an empty state.

### Instructions

1. Build a Progress page that consumes `/stats/progress` and/or summary breakdown via TanStack Query.
2. Show sessions over time and distance/intensity by activity type.
3. Auth-gate the page; use the shared API client + Bearer token from Sprint 2.
4. Show an empty state when there is no data (empty arrays → message, not a broken chart).
5. Put filter params in Query keys (ready for S4-12).

### Stay in scope

- Leave polished period controls for S4-12 if they are not already stubbed; charts + empty state are the bar here.
- Leave Dashboard widgets for S4-13. Do not replace the Sprint 3 recent-sessions list on this ticket.
- Do not add session create/edit forms on Progress. Do not add AI Insights (Sprint 5).
- Keep language as sessions/measurements in UI copy where you can.

### Hints

- Empty arrays should render a message, not NaN axes.
- Map API `{ period_label, value }` to whatever Recharts prop names you used in S4-10.

### Acceptance criteria

- [ ] Charts consume `/stats/progress` and/or summary breakdown
- [ ] Empty data shows an empty state, not a broken chart
- [ ] Page is auth-gated

### Suggested paths

`frontend/src/pages/ProgressPage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-11` in the message, for example `S4-11: short summary`. Never commit `.env` or secrets.

---

## S4-12 — Period controls

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 3       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S4-11   |

### New here: filter controls that refetch

UI controls for **date range** and **week/month granularity** are the core Sprint 4 demo moment: change a filter, watch the chart update. That only works if:

- Control state is React state (or URL search params)
- Those values go into the `/stats/*` query string
- TanStack **Query keys include the filter params** so a change triggers a refetch (not a stale cache)

Choose sensible defaults (e.g. last 4–8 weeks). Disable or reject invalid ranges (`from > to`). Align defaults with what `/stats/*` expects.

**Docs & tutorials:**

- [TanStack Query — Query Keys](https://tanstack.com/query/latest/docs/framework/react/guides/query-keys) — include filters
- [React controlled inputs](https://react.dev/reference/react-dom/components/input#controlling-an-input-with-a-state-variable) — date/granularity controls

### Your task

Add date-range and granularity controls so changing filters refetches stats and updates charts. Your deliverable is Progress period controls with sensible defaults, Query keys that include filters, and a guard against `from > to`.

### Instructions

1. Add UI controls for date range and week/month granularity.
2. Changing controls must refetch stats and update charts.
3. Choose sensible defaults (e.g. last 4–8 weeks). Align them with what `/stats/*` expects.
4. Include filter params in TanStack Query keys.
5. Disable or reject invalid ranges (`from > to`).

### Stay in scope

- Leave Dashboard widgets for S4-13 (you may reuse the same period idea there, but this ticket is Progress).
- Do not add AI period coaching (Sprint 5).
- Do not add new session CRUD or CSV export (stretch S4-S3).
- Do not add rate-limit UX (Sprint 6).

### Hints

- Optional: keep control state in URL search params for shareable demos (React Router search).
- If charts do not move, log the Query key—missing filter fields are the usual cause.

### Acceptance criteria

- [ ] Changing controls updates charts
- [ ] Defaults are sensible (e.g. last 4–8 weeks)
- [ ] Query keys include filter params

### Suggested paths

`frontend/src/pages/ProgressPage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-12` in the message, for example `S4-12: short summary`. Never commit `.env` or secrets.

---

## S4-13 — Dashboard stat widgets

| Field          | Value                                       |
| -------------- | ------------------------------------------- |
| **Type**       | feature                                     |
| **Week**       | 3                                           |
| **Priority**   | Must                                        |
| **Estimate**   | M                                           |
| **Depends on** | S4-06, Sprint 3 Dashboard (recent sessions) |

### New here: summary widgets beside recent sessions

Dashboard **widgets** show session count, totals, and average intensity for a selected period—the same numbers as `GET /stats/summary`. They sit **beside** the Sprint 3 recent-sessions list; they do not replace it.

Mismatched numbers (widget says 5 sessions, summary API says 4) break trust in the demo. Use one shared period, show a loading state while TanStack Query fetches, and format duration/distance for humans if you like (e.g. minutes → `1h 20m`).

Prefer non-null `session_at` for “this period,” consistent with the analytics rules.

**Docs & tutorials:**

- [TanStack Query — status fields](https://tanstack.com/query/latest/docs/framework/react/guides/queries#query-status) — loading / error UI

### Your task

Add Dashboard widgets that match `/stats/summary` for the same period, without removing Sprint 3’s recent-sessions list. Your deliverable is session-count / totals / average-intensity widgets plus a loading state.

### Instructions

1. Add widgets for session count, totals, and average intensity for a selected period.
2. Fetch `/stats/summary` (shared API client + auth). Numbers must match that endpoint for the same period.
3. Show a loading state while fetching.
4. Keep the recent sessions list from Sprint 3—widgets sit beside it.
5. Prefer a single shared period control between widgets so they cannot disagree with each other.

### Stay in scope

- Do not replace the recent-sessions list with charts-only Dashboard.
- Do not add new session CRUD on the Dashboard.
- Do not add AI Insights CTA unless you are already in Sprint 5.
- Leave CSV export and period-over-period for stretch tickets.

### Hints

- One shared period control between widgets reduces “why do these two cards disagree?”
- Format duration/distance for humans (e.g. minutes → `1h 20m`) if you like.

### Acceptance criteria

- [ ] Numbers match `/stats/summary` for the same period
- [ ] Loading state while fetching
- [ ] Coexists with recent sessions list from Sprint 3

### Suggested paths

`frontend/src/pages/DashboardPage.tsx`, `frontend/src/components/StatWidgets.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-13` in the message, for example `S4-13: short summary`. Never commit `.env` or secrets.

---

## S4-14 — Stats README notes

| Field          | Value                      |
| -------------- | -------------------------- |
| **Type**       | docs                       |
| **Week**       | 3                          |
| **Priority**   | Should                     |
| **Estimate**   | S                          |
| **Depends on** | S4-05, S4-06, S4-07, S4-08 |

### New here: documenting stats for classmates

A short README section (or `docs/stats.md`) is the runbook for this sprint’s backend contract. Classmates should learn, without reading every service file:

1. The three endpoints (`/stats/summary`, `/stats/progress`, `/stats/streaks`)
2. The analytics `pytest` command
3. Your streak definition in one paragraph
4. That volumes come from **measurement unit slugs**, and that analytics is **pure Python** in `services/analytics.py`

Link OpenAPI `/docs` for response shapes. Keep it scannable—tables beat a long essay.

**Docs & tutorials:**

- [About READMEs (GitHub Docs)](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) — keep it scannable

### Your task

Write the stats notes so a classmate can run tests and call the right endpoint without digging through code. Your deliverable is a README or `docs/stats.md` section covering the three endpoints, the pytest command, and the streak definition.

### Instructions

1. Add a short README or `docs/stats.md` section explaining the three endpoints.
2. List the analytics test command.
3. Summarize your streak definition in one paragraph.
4. Note that volumes come from measurement unit slugs (Sprint 2 catalog) and that core math lives in `services/analytics.py` (no FastAPI/DB in that module).
5. Link OpenAPI `/docs` for response shapes.

### Stay in scope

- Scope the notes to **Sprint 4**: stats + tests + streak definition. A “coming next: AI insights” line is fine.
- Leave Ollama setup for Sprint 5. Leave rate limits and deployment for Sprint 6.
- Do not paste large code samples; point at paths instead.

### Hints

- A small table of endpoint → purpose → query params is easier to demo from than a paragraph.

### Acceptance criteria

- [ ] README or docs section exists
- [ ] Test command listed
- [ ] Streak definition summarized in one paragraph

### Suggested paths

`README.md`, `docs/stats.md`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-14` in the message, for example `S4-14: short summary`. Never commit `.env` or secrets.

---

## Stretch tickets

Optional extras after Must/Should. Same ticket shape; skip them if you are out of time.

## S4-S1 — Goal progress percent

| Field          | Value              |
| -------------- | ------------------ |
| **Type**       | feature            |
| **Week**       | —                  |
| **Priority**   | Stretch            |
| **Estimate**   | M                  |
| **Depends on** | S4-06, S4-09, S3-09 |

### New here: comparing totals to Sprint 3 goals

Sprint 3 **goals** are targets keyed by `unit_type_id` (not free-text metrics). A completion percentage is “this period’s total for that unit ÷ goal target.” That keeps Progress and optional Dashboard cards speaking the same catalog language as measurements.

**Docs & tutorials:**

- Reuse Goal API from [S3-09](sprint-03-tickets.md#s3-09--goals-crud-api)
- Reuse summary analytics from [S4-02](#s4-02--summary-metrics) / [S4-06](#s4-06--stats-summary-endpoint)

### Your task

Compare period totals to **active goals** and expose a simple completion percentage for Dashboard or Progress. Do not invent free-text metrics.

### Instructions

1. Reuse Goal API / model from Sprint 3 (`unit_type_id`).
2. Reuse summary analytics for the matching unit slug / unit type—do not re-sum in the route.
3. Scope to the current user only (same aggregate-IDOR rule as S4-09).

### Stay in scope

- Do not rebuild goals CRUD.
- Do not add AI commentary on goals (Sprint 5).

### Hints

- Inactive / deactivated goals should not appear as current targets unless you document otherwise.

### Acceptance criteria

- [ ] Completion percent uses active goals keyed by `unit_type_id`
- [ ] Totals come from existing summary analytics, not a new sum in the route
- [ ] Result is user-scoped (same rule as S4-09)

### Suggested paths

`backend/app/services/analytics.py`, `backend/app/api/stats.py`, Dashboard or Progress UI

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-S1` in the message, for example `S4-S1: short summary`. Never commit `.env` or secrets.

---

## S4-S2 — Period-over-period

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | —            |
| **Priority**   | Stretch      |
| **Estimate**   | M            |
| **Depends on** | S4-02, S4-06 |

### New here: previous window comparison

**Period-over-period** answers “is this 4 weeks better than the 4 weeks before?” You run the **same** analytics functions twice with different date ranges and compare. That is why Week 1 kept math in pure Python.

**Docs & tutorials:**

- [datetime arithmetic](https://docs.python.org/3/library/datetime.html#timedelta-objects) — shift windows

### Your task

Show the current window vs the previous window of the same length (e.g. this 4 weeks vs prior 4 weeks). Reuse the same analytics functions twice with different ranges.

### Instructions

1. Compute the previous window from the selected `from`/`to` (same length, immediately before).
2. Call summary (or series) analytics twice; return both results plus a simple delta if you like.
3. Keep it user-scoped; prefer non-null `session_at`.

### Stay in scope

- Do not add a second analytics module or AI “improvement” prose.

### Hints

- Derive the previous window from the selected range rather than hard-coding “last 4 weeks.”

### Acceptance criteria

- [ ] Previous window is the same length, immediately before the selected range
- [ ] Same analytics functions run twice (no duplicate math module)
- [ ] Result is user-scoped; dated slices prefer non-null `session_at`

### Suggested paths

`backend/app/services/analytics.py`, `backend/app/services/stats.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-S2` in the message, for example `S4-S2: short summary`. Never commit `.env` or secrets.

---

## S4-S3 — CSV export

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | —            |
| **Priority**   | Stretch      |
| **Estimate**   | S            |
| **Depends on** | S4-06, S4-09 |

### New here: exporting a period slice

A **CSV export** lets someone download a summary (or session/measurement slice) for the selected period. It is still a stats feature: **user-scoped**, same date rules, same unit slugs—not a dump of the whole database.

**Docs & tutorials:**

- [csv — CSV File Reading and Writing](https://docs.python.org/3/library/csv.html) — server-side export
- [MDN — Downloading files](https://developer.mozilla.org/en-US/docs/Web/API/Blob) — browser download pattern

### Your task

Allow downloading a summary (or session/measurement slice) as CSV for the selected period. Keep it user-scoped.

### Instructions

1. Add an authenticated export (API download or frontend Blob) for the current user’s selected period.
2. Reuse existing loaders + analytics; do not query all users.
3. Prefer non-null `session_at` for calendar slices unless documented.

### Stay in scope

- Leave rate limits for Sprint 6.
- No AI; no new session CRUD.

### Hints

- Set `Content-Disposition` (or an equivalent download filename) so the browser saves a `.csv`.

### Acceptance criteria

- [ ] Authenticated user can download a CSV for the selected period
- [ ] Export is user-scoped (no other users’ rows)
- [ ] Uses existing loaders / analytics, not a whole-database dump

### Suggested paths

`backend/app/api/stats.py`, Progress or Dashboard export control

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S4-S3` in the message, for example `S4-S3: short summary`. Never commit `.env` or secrets.

---

## Related

- Previous tickets: [sprint-03-tickets.md](sprint-03-tickets.md)
- Next tickets: [sprint-05-tickets.md](sprint-05-tickets.md)
- Index: [../README.md](../README.md)
