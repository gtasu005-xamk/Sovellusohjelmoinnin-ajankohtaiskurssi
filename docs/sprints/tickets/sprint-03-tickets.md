# Sprint 3 tickets — Sessions, clone, plans & calendar

Backlog for Sprint 3 ([index](../README.md)). Copy tickets into your issue tracker if you like; keep the IDs (`S3-01`, …) in branch and PR titles.

## Your task for Sprint 3

Sprint 2 staffed the membership desk and hung the **exercise** board. Members can walk in, but the **training floor** is still empty: no logbook, no program, no calendar, no private lockers.

Sprint 3 is where people actually train. Ship multi-exercise **WorkoutSessions** with **planned** and **actual** measurements, **session clone** for reuse, **WorkoutPlans** via `plan_id` on sessions (no junction table), an in-app **calendar**, and **period Goals** keyed by unit type. Talk about **sessions** and **measurements**, not a flat “workout” row. There is no `unit_hint` and **no** separate session-template feature.

Authentication got them through the door; **authorization** keeps User A from opening User B’s locker. Charts and the house coach still wait—you need an honest, private logbook first.

```text
UnitType ←→ ActivityType (exercise)     Sprint 2 catalog
                ↓
     WorkoutSessionItem → Measurement (planned_value, actual_value)
                ↓
          WorkoutSession ──plan_id──► WorkoutPlan
                │
                └── clone ──► new WorkoutSession (planned kept, actuals cleared)
```

**Teaching rules:**

- Activities are **individual exercises** (bench press, running, …).
- Reuse = **`POST /sessions/{id}/clone`** (deep snapshot). Editing the source does **not** change existing clones.
- Plans use **`workout_sessions.plan_id`**. There is **no** `workout_plan_sessions` table. Order members by **`session_at` ASC NULLS LAST**.
- Calendar is driven by **`session_at`** (optional `plan_id` filter)—not weekday placement rows.
- Period **Goals** (`unit_type_id`, week/month) are separate from planned set values.

### Prerequisites from Sprint 2

- JWT register / login / `me` and a protected React layout with token storage
- Alembic + models for `User`, `ActivityType`, `UnitType`, `activity_type_unit_types`
- Seeded **exercise-level** catalog (e.g. Running → duration + distance; Bench press → reps + weight `per_set`)
- Layered backend (`api` → `services` → `repositories` → `models`/`db`) and CORS allowlist

### What success looks like

1. Create a multi-exercise session with **planned** values (actuals empty or filled)
2. Assign it to a plan via **`plan_id`**; plan members ordered by `session_at`
3. **Clone** the session onto a date; planned kept, actuals cleared; fill actuals on the clone
4. Edit the source session (add an exercise)—the earlier clone is unchanged
5. Calendar month + week shows dated sessions; User B cannot open User A’s session/plan/calendar/goal
6. Dashboard shows recent sessions for the logged-in user only
7. Short IDOR demo write-up exists

**Suggested demo flow:** log in as A → create “Pull A” with planned sets → set `plan_id` → clone onto Monday → fill actuals → open Calendar → edit Pull A → confirm Monday clone unchanged → try B’s IDs (fail) → Dashboard.

### New tools & technologies

| Tool / technology | Role in this sprint |
| ----------------- | ------------------- |
| **TanStack Query** | Cache for sessions/plans/calendar |
| **Nested REST + Pydantic** | Items/measurements; clone body |
| **SQLAlchemy relationships** | Session → items → measurements; `plan_id` / `source_session_id` |
| **IDOR / object-level auth** | Ownership on every get/update/delete |
| **Calendar UI** | Month + week views over `session_at` |

### What you will learn

- Nested domain APIs with planned vs actual validation
- Clone-as-snapshot (no cascade)
- Plan membership without a junction table
- Calendar over dated sessions
- Ownership (IDOR) and TanStack Query list/forms

### Layered backend

```text
api/sessions.py   → services/sessions.py   → repositories/session.py
api/plans.py      → services/plans.py      → repositories/plan.py
api/calendar.py   → services/calendar.py   → (reuse session repo)
api/goals.py      → services/goals.py      → repositories/goal.py
```

**Naming:** SQLAlchemy `Session` (DB) ≠ `WorkoutSession` (domain). Use `db: Session` for the ORM session.

### Out of scope

| Topic | When |
| ----- | ---- |
| Progress charts / aggregations | Sprint 4 |
| AI insights | Sprint 5 |
| Full automated test suite | Sprint 6 (optional) |
| Google Calendar sync / invites | Never Must |
| `session_templates` / `is_template` / `workout_plan_sessions` | **Do not build** |

### Week-by-week map

| Week | Focus | Ticket IDs | Checkpoint |
| ---- | ----- | ---------- | ---------- |
| **1** | Models + APIs (sessions, clone, plans, calendar, ownership) | S3-01 … S3-12 | OpenAPI happy path + IDOR fails |
| **2** | TanStack Query + session UI + clone in UI | S3-13 … S3-17 | Designer + clone from UI |
| **3** | Plans UI, calendar UI, dashboard, IDOR docs | S3-18 … S3-23 | Two-account + calendar demo |

### Ticket index

| ID | Title | Week | Priority | Estimate |
| -- | ----- | ---- | -------- | -------- |
| [S3-01](#s3-01--session-models-and-migration) | Session models and migration | 1 | Must | L |
| [S3-02](#s3-02--goal-model-and-migration) | Goal model and migration | 1 | Must | M |
| [S3-03](#s3-03--plan-model-and-migration) | Plan model and migration | 1 | Must | M |
| [S3-04](#s3-04--sessions-crud-api) | Sessions CRUD API | 1 | Must | L |
| [S3-05](#s3-05--session-measurements-planned-and-actual) | Session measurements (planned/actual) | 1 | Must | L |
| [S3-06](#s3-06--session-filters) | Session filters | 1 | Must | M |
| [S3-07](#s3-07--clone-session-api) | Clone session API | 1 | Must | L |
| [S3-08](#s3-08--plans-crud-and-attach-api) | Plans CRUD and attach API | 1 | Must | L |
| [S3-09](#s3-09--activity-types-api) | Activity types API | 1 | Must | M |
| [S3-10](#s3-10--goals-crud-api) | Goals CRUD API | 1 | Must | M |
| [S3-11](#s3-11--ownership-enforcement) | Ownership enforcement | 1 | Must | M |
| [S3-12](#s3-12--calendar-api) | Calendar API | 1 | Must | M |
| [S3-13](#s3-13--tanstack-query-setup) | TanStack Query setup | 2 | Must | S |
| [S3-14](#s3-14--sessions-list-and-filters-ui) | Sessions list and filters UI | 2 | Must | L |
| [S3-15](#s3-15--session-designer-planned-and-actual) | Session designer (planned + actual) | 2 | Must | L |
| [S3-16](#s3-16--edit-delete-and-clone-session-ui) | Edit, delete, and clone session UI | 2 | Must | M |
| [S3-17](#s3-17--activity-type-selector) | Activity type selector | 2 | Must | M |
| [S3-18](#s3-18--plans-ui) | Plans UI | 3 | Must | L |
| [S3-19](#s3-19--calendar-ui) | Calendar UI (month + week) | 3 | Must | L |
| [S3-20](#s3-20--dashboard-recent-sessions) | Dashboard recent sessions | 3 | Must | M |
| [S3-21](#s3-21--empty-and-error-states) | Empty and error states | 3 | Should | S |
| [S3-22](#s3-22--idor-demo-documentation) | IDOR demo documentation | 3 | Must | S |
| [S3-23](#s3-23--optional-goals-ui) | Optional Goals UI | 3 | Stretch | M |
| [S3-S1](#s3-s1--pagination) | Pagination | — | Stretch | S |
| [S3-S2](#s3-s2--ownership-api-tests) | Ownership API tests | — | Stretch | M |
| [S3-S3](#s3-s3--add-models-to-sqladmin) | Add models to SQLAdmin | — | Stretch | S |
| [S3-S4](#s3-s4--planned-vs-actual-adherence-preview) | Planned vs actual adherence preview | — | Stretch | M |

---

## S3-01 — Session models and migration

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | Sprint 2 complete |

### New here: sessions with planned and actual measurements

A **WorkoutSession** is one training outing (or unscheduled program definition) with several **exercises**. Values live on measurements as **`planned_value`** and **`actual_value`** (both nullable). Optional **`plan_id`** and **`source_session_id`** support plans and clone provenance.

| Table | Purpose |
| ----- | ------- |
| `workout_sessions` | `user_id`, `name`, `session_at` (nullable), `status`, `notes`, `intensity`, **`plan_id`** (nullable FK → plans, ON DELETE SET NULL), **`source_session_id`** (nullable FK → `workout_sessions`, ON DELETE SET NULL), timestamps |
| `workout_session_items` | `session_id`, `activity_type_id`, `sort_order`, notes |
| `workout_session_measurements` | `session_item_id`, `unit_type_id`, **`planned_value`**, **`actual_value`**, `set_index` |

You may add `plan_id` in this migration with a deferred FK, or add it in S3-03 once `workout_plans` exists—document which approach you use. Prefer one migration batch for S3-01…S3-03 if possible.

**Docs:** [SQLAlchemy relationships](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html), [Alembic create revision](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script)

### Your task

Add session/item/measurement models + migration. No single `value` column—use planned and actual.

### Instructions

1. Create the three tables/models as above (wire `plan_id` when plans exist).
2. Index `(user_id, session_at)` and later `(plan_id, session_at)`.
3. Status check: `planned` \| `in_progress` \| `completed`; intensity 1–10 or null.
4. Do **not** add `is_template` or template tables.

### Stay in scope

Leave CRUD APIs for S3-04+, clone for S3-07, plans for S3-03/S3-08.

### Acceptance criteria

- [ ] Migration applies on a fresh DB
- [ ] Measurements have planned and actual columns
- [ ] No `workout_plan_sessions` / template tables

### Suggested paths

`backend/app/models/workout_session*.py`, `backend/alembic/versions/`

### Commit

`S3-01: short summary`

---

## S3-02 — Goal model and migration

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S3-01 (same batch OK) |

### New here: period goals

**Goals** are week/month targets by **`unit_type_id`** (and optional `activity_type_id`) for Sprint 5 AI—not planned set prescriptions on a session.

### Your task

Add `goals` table: `user_id`, `unit_type_id`, `target_value`, `period` (`week`\|`month`), `activity_type_id` nullable, `active`, `created_at`.

### Instructions

1. Model + migration with FK checks.
2. Keep payloads tiny; UI can wait until S3-23.

### Stay in scope

Leave Goals CRUD for S3-10; do not confuse with `planned_value`.

### Acceptance criteria

- [ ] Goal model migrated
- [ ] Period constrained to week/month

### Suggested paths

`backend/app/models/goal.py`

### Commit

`S3-02: short summary`

---

## S3-03 — Plan model and migration

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S3-01 |

### New here: plans without a junction

**WorkoutPlan** is a named program. Sessions belong via **`workout_sessions.plan_id`**. Optional `start_date` / `length_weeks` are **metadata** only (not a recurrence engine).

**Do not** create `workout_plan_sessions`.

### Your task

Add `workout_plans` (`user_id`, `name`, `notes`, optional `start_date`, `length_weeks`, timestamps) and ensure sessions can reference `plan_id`.

### Instructions

1. Model + migration.
2. Relationship: plan → sessions; order in queries by `session_at` NULLS LAST.
3. Document: one session → at most one plan.

### Stay in scope

Leave attach API for S3-08; calendar for S3-12/S3-19.

### Acceptance criteria

- [ ] Plans table exists
- [ ] No plan↔session junction table
- [ ] `plan_id` on sessions works

### Suggested paths

`backend/app/models/workout_plan.py`

### Commit

`S3-03: short summary`

---

## S3-04 — Sessions CRUD API

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | S3-01, JWT |

### Your task

Layered `/sessions` CRUD scoped to `current_user`. Nested create/update may include items + measurements. Support optional `plan_id` on write (must own the plan).

### Instructions

1. `GET/POST /sessions`, `GET/PATCH/DELETE /sessions/{id}`.
2. Always scope by `user_id`; cross-user → 404 or 403 (same convention as S3-11).
3. Keep services for rules; repositories for queries.

### Stay in scope

Measurement validation details in S3-05; filters in S3-06; clone in S3-07.

### Acceptance criteria

- [ ] Owner CRUD works in OpenAPI
- [ ] Nested items round-trip
- [ ] Foreign session id fails closed

### Suggested paths

`backend/app/api/sessions.py`, `services/sessions.py`, `repositories/session.py`, `schemas/session.py`

### Commit

`S3-04: short summary`

---

## S3-05 — Session measurements (planned and actual)

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | S3-04, Sprint 2 links |

### New here: planned vs actual

Each measurement may carry **`planned_value`**, **`actual_value`**, or both. Reject a measurement payload where **both** are null. Validate `unit_type_id` against the item’s activity links; if `per_set`, require `set_index`.

### Your task

Persist and validate planned/actual on create/update; round-trip on GET.

### Instructions

1. Wire schemas with both fields.
2. Catalog validation in services.
3. Document: clone (S3-07) copies planned and clears actual.

### Stay in scope

Leave designer UI for S3-15.

### Acceptance criteria

- [ ] Planned-only, actual-only, and both work
- [ ] Invalid unit rejected
- [ ] Per-set `set_index` enforced when required

### Suggested paths

Same as S3-04

### Commit

`S3-05: short summary`

---

## S3-06 — Session filters

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S3-04 |

### Your task

`GET /sessions` query params: `from`, `to`, `status`, `activity_type_id`, `unscheduled`, **`plan_id`**. Always AND with `user_id`. Invalid range (`from` > `to`) → 400.

### Acceptance criteria

- [ ] Filters documented in OpenAPI
- [ ] Cannot widen access beyond current user

### Suggested paths

`backend/app/api/sessions.py`, `repositories/session.py`

### Commit

`S3-06: short summary`

---

## S3-07 — Clone session API

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | S3-05 |

### New here: clone as snapshot

`POST /sessions/{id}/clone` creates a **new** session owned by the caller:

- Deep-copy items and measurements (new row IDs)
- **Keep `planned_value`**
- **Set `actual_value` to null**
- Set `source_session_id` to the source
- Optional body: `session_at`, `name`, optional `plan_id` (if omitted, **do not** inherit source `plan_id`)
- Later edits to the source **must not** change the clone

### Your task

Implement clone in `services/`; prove isolation in a manual OpenAPI check.

### Stay in scope

Leave clone UI for S3-16; calendar perform uses this endpoint.

### Acceptance criteria

- [ ] Clone keeps planned, clears actuals
- [ ] `source_session_id` set
- [ ] Editing source does not alter clone content
- [ ] Cross-user clone source → fail closed

### Suggested paths

`backend/app/api/sessions.py`, `services/sessions.py`

### Commit

`S3-07: short summary`

---

## S3-08 — Plans CRUD and attach API

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | S3-03, S3-04 |

### Your task

CRUD `/plans`. Attach/detach by setting/clearing **`session.plan_id`** (thin `POST/DELETE /plans/{id}/sessions/{session_id}` allowed). Detail lists members **ordered by `session_at` NULLS LAST**. Reject attaching another user’s session.

### Stay in scope

No junction table; no `sequence` / `week_offset` / `weekday`.

### Acceptance criteria

- [ ] Plan CRUD works
- [ ] Attach/detach via `plan_id`
- [ ] Members ordered by `session_at`
- [ ] Cross-user attach fails

### Suggested paths

`backend/app/api/plans.py`, `services/plans.py`

### Commit

`S3-08: short summary`

---

## S3-09 — Activity types API

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | Sprint 2 catalog |

### Your task

Authenticated `GET /activity-types` (system + own custom) with unit links. Optional custom create scoped to user. No `unit_hint`.

### Acceptance criteria

- [ ] Unit links returned
- [ ] Custom types scoped to creator

### Suggested paths

`backend/app/api/activity_types.py`

### Commit

`S3-09: short summary`

---

## S3-10 — Goals CRUD API

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S3-02 |

### Your task

Owner-scoped `/goals` CRUD; validate `unit_type_id`; filter by `active`. UI optional (S3-23).

### Acceptance criteria

- [ ] Owner-only CRUD in OpenAPI
- [ ] `unit_type_id` validated

### Suggested paths

`backend/app/api/goals.py`

### Commit

`S3-10: short summary`

---

## S3-11 — Ownership enforcement

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S3-04, S3-08, S3-10 |

### New here: IDOR

Centralize “get session/plan/goal for current user or raise.” Prefer consistent **404** (or 403)—document in S3-22. Apply to get/update/delete, attach, and clone source.

### Acceptance criteria

- [ ] Cross-user access fails for sessions, plans, goals
- [ ] Convention documented for S3-22

### Suggested paths

`backend/app/services/sessions.py`, `plans.py`, `goals.py`

### Commit

`S3-11: short summary`

---

## S3-12 — Calendar API

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 1 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S3-04, S3-06 |

### New here: calendar by `session_at`

`GET /calendar?from=&to=&plan_id?` returns the current user’s sessions with non-null `session_at` in range (optional plan filter). No generated weekday slots—**dated sessions are the source of truth**.

### Your task

Owner-scoped calendar list DTO (id, name, session_at, status, plan_id, …). Invalid range → 400.

### Stay in scope

Leave month/week UI for S3-19; clone remains S3-07.

### Acceptance criteria

- [ ] Returns only current user’s dated sessions
- [ ] Optional `plan_id` filter
- [ ] No foreign data

### Suggested paths

`backend/app/api/calendar.py`, `services/calendar.py`

### Commit

`S3-12: short summary`

---

## S3-13 — TanStack Query setup

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 2 |
| **Priority** | Must |
| **Estimate** | S |
| **Depends on** | Sprint 2 auth client |

### Your task

Install TanStack Query; wrap with `QueryClientProvider`; document keys e.g. `['sessions', filters]`, `['plans', id]`, `['calendar', from, to, planId]`.

### Acceptance criteria

- [ ] Provider wraps app
- [ ] At least one query used
- [ ] Key convention written down

### Suggested paths

`frontend/src/api/queryClient.ts`, `frontend/src/main.tsx`

### Commit

`S3-13: short summary`

---

## S3-14 — Sessions list and filters UI

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 2 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | S3-06, S3-13 |

### Your task

Protected sessions list with filters (date, status, unscheduled, plan, activity). Show name, `session_at` or Unscheduled, status, exercise summary. Link to detail/edit.

### Acceptance criteria

- [ ] List loads for logged-in user
- [ ] Filters hit the API
- [ ] No other user’s sessions

### Suggested paths

`frontend/src/pages/SessionsPage.tsx`

### Commit

`S3-14: short summary`

---

## S3-15 — Session designer (planned and actual)

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 2 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | S3-05, S3-09, S3-13 |

### Your task

Form for metadata + ordered exercises + measurement inputs from unit links. Support **planned** and **actual** fields (and leaving either empty when allowed). Allow null `session_at`. Optional `plan_id` assign.

### Acceptance criteria

- [ ] Multi-exercise session save works
- [ ] Per-set planned/actual for a strength exercise
- [ ] `session_at` optional

### Suggested paths

`frontend/src/pages/SessionFormPage.tsx`, measurement editor component

### Commit

`S3-15: short summary`

---

## S3-16 — Edit, delete, and clone session UI

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 2 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S3-07, S3-15 |

### Your task

Edit/delete with confirm; **Clone** action calling S3-07 (pick date / name). Invalidate query keys. Show clear message on 404/403. Demo: clone → edit source → clone unchanged.

### Acceptance criteria

- [ ] Edit/delete work
- [ ] Clone from UI keeps planned, clears actuals
- [ ] Isolation visible after editing source

### Suggested paths

`frontend/src/pages/SessionFormPage.tsx`

### Commit

`S3-16: short summary`

---

## S3-17 — Activity type selector

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 2 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S3-09, S3-13 |

### Your task

Shared selector listing system + custom exercises with unit summary from API links (no `unit_hint`). Use in the designer.

### Acceptance criteria

- [ ] Used by session designer
- [ ] Reflects API unit links

### Suggested paths

`frontend/src/components/ActivityTypeSelect.tsx`

### Commit

`S3-17: short summary`

---

## S3-18 — Plans UI

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 3 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | S3-08, S3-13 |

### Your task

List/create/edit/delete plans; attach/detach owned sessions via `plan_id`; show members ordered by `session_at` with an unscheduled section for nulls. Optional display of `start_date` / `length_weeks` metadata. No drag-reorder junction UI.

### Acceptance criteria

- [ ] Plan builder works end-to-end
- [ ] Only own sessions attachable
- [ ] Order follows `session_at`

### Suggested paths

`frontend/src/pages/PlansPage.tsx`, `PlanDetailPage.tsx`

### Commit

`S3-18: short summary`

---

## S3-19 — Calendar UI

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 3 |
| **Priority** | Must |
| **Estimate** | L |
| **Depends on** | S3-12, S3-07, S3-13 |

### New here: full in-app calendar

**Must:** month view **and** week view over `GET /calendar`. Show dated sessions; optional plan filter. From a day/session, **clone** onto a chosen date (reuse S3-07). Visual distinction for statuses as you like. No Google sync.

### Acceptance criteria

- [ ] Month and week views work
- [ ] Only current user’s sessions
- [ ] Clone-onto-date from calendar works

### Suggested paths

`frontend/src/pages/CalendarPage.tsx`

### Commit

`S3-19: short summary`

---

## S3-20 — Dashboard recent sessions

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 3 |
| **Priority** | Must |
| **Estimate** | M |
| **Depends on** | S3-04, S3-13 |

### Your task

Protected dashboard of recent dated sessions (prefer non-null `session_at`); links to edit; empty state when none.

### Acceptance criteria

- [ ] Only current user’s sessions
- [ ] Empty state when none

### Suggested paths

`frontend/src/pages/DashboardPage.tsx`

### Commit

`S3-20: short summary`

---

## S3-21 — Empty and error states

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 3 |
| **Priority** | Should |
| **Estimate** | S |
| **Depends on** | S3-14, S3-18, S3-19 |

### Your task

Empty copy (“Create your first session”) and error banners for failed saves / forbidden responses on sessions, plans, and calendar.

### Acceptance criteria

- [ ] Empty and error states visible without silent failures

### Suggested paths

Shared alert/empty components on list pages

### Commit

`S3-21: short summary`

---

## S3-22 — IDOR demo documentation

| Field | Value |
| ----- | ----- |
| **Type** | docs |
| **Week** | 3 |
| **Priority** | Must |
| **Estimate** | S |
| **Depends on** | S3-11 |

### Your task

Short classmate-facing write-up (e.g. `docs/idor-demo.md`): two users, try foreign session/plan/goal/calendar ids, expected 404/403, document your choice.

### Acceptance criteria

- [ ] Steps reproducible from `/docs`
- [ ] Status convention stated

### Suggested paths

`docs/idor-demo.md`

### Commit

`S3-22: short summary`

---

## S3-23 — Optional Goals UI

| Field | Value |
| ----- | ----- |
| **Type** | feature |
| **Week** | 3 |
| **Priority** | Stretch |
| **Estimate** | M |
| **Depends on** | S3-10, S3-13 |

### Your task

Simple UI to create/list/deactivate period goals by `unit_type_id`. Label them **period goals**, not planned sets.

### Acceptance criteria

- [ ] Owner can manage period goals in the UI

### Suggested paths

`frontend/src/pages/GoalsPage.tsx`

### Commit

`S3-23: short summary`

---

## S3-S1 — Pagination

| Field | Value |
| ----- | ----- |
| **Priority** | Stretch |
| **Estimate** | S |

Add page/limit (or cursor) to session list; document in OpenAPI; wire UI controls.

### Commit

`S3-S1: short summary`

---

## S3-S2 — Ownership API tests

| Field | Value |
| ----- | ----- |
| **Priority** | Stretch |
| **Estimate** | M |

Automated tests: User B cannot read/update A’s session/plan/goal; clone isolation; calendar scoped.

### Commit

`S3-S2: short summary`

---

## S3-S3 — Add models to SQLAdmin

| Field | Value |
| ----- | ----- |
| **Priority** | Stretch |
| **Estimate** | S |

Register session/plan/goal models in `/admin` for demos.

### Commit

`S3-S3: short summary`

---

## S3-S4 — Planned vs actual adherence preview

| Field | Value |
| ----- | ----- |
| **Priority** | Stretch |
| **Estimate** | M |

Small owner-scoped summary comparing planned vs actual for a period (feeds Sprint 4 thinking). Keep pure logic testable.

### Commit

`S3-S4: short summary`
