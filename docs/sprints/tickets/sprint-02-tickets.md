# Sprint 2 tickets — Auth & database design

Backlog for Sprint 2 ([index](../README.md)). Copy tickets into your issue tracker if you like; keep the IDs (`S2-01`, …) in branch and PR titles.

## Your task for Sprint 2

The gym from Sprint 1 has lights and a front door. It still does not know *who* walked in, and the walls are blank—nobody can tell whether “Running” means minutes, kilometres, or both.

Sprint 2 is the **membership desk and the activity board**. Ship ORM models and Alembic migrations, a seeded unit/activity catalog, SQLAdmin at `/admin`, JWT register/login/`me`, and a Login/Register UI that stores the token. Sprint 3 assumes users exist, passwords are hashed, JWT protects API routes, and activities already declare which units they accept. If those pieces are missing, the training-floor logbook has nothing to attach to.

Activities do **not** store a single measurement hint. Measurement kinds live in **`unit_types`**, and each activity links to **one or more** units (for example Running → duration + distance; Bench press → reps + weight per set). **Activities are individual exercises** (bench press, hammer curl, running)—not a single coarse “Gym” type. SQLAdmin login (env username/password) is **separate** from JWT app-user auth. Keep secrets in config, never store plain-text passwords, and verify JWT on every protected API route.

Next chapter: people actually train—sessions with planned/actual values, clone, plans (`plan_id`), calendar, and lockers that only they can open. Leave that for Sprint 3.

### Prerequisites from Sprint 1

This backlog assumes you already have:

- Compose stack with `db`, `api`, and (ideally) `web`
- `DATABASE_URL` / env settings wired so the API can reach Postgres
- FastAPI `/health` and a React shell with routing

If those are missing, finish or stabilize [Sprint 1 tickets](sprint-01-tickets.md) first.

### What success looks like

When you finish Sprint 2, you should be able to demo:

1. Migrations create `User`, `ActivityType`, `UnitType`, and `activity_type_unit_types`; system units and **exercise-level** activity types are seeded with links (for example Running has duration + distance; Bench press has reps + weight `per_set`)
2. `/admin` works with env-based login and shows unit types, activity types, and links
3. `POST /auth/register`, `POST /auth/login`, and `GET /auth/me` work
4. Passwords are hashed with bcrypt; JWT protects `/auth/me`
5. In the UI you can register, log in, see your profile, and log out

**Suggested demo flow:** open `/admin` → show unit types + activity↔unit links (Running has duration and distance; a strength exercise has per-set reps/weight) → register in the UI → log out / in → show profile from `/auth/me` → optionally inspect the new user in SQLAdmin.

### New tools & technologies

| Tool / technology | Role in this sprint |
| ----------------- | ------------------- |
| **SQLAlchemy** | ORM models, engine, DB sessions |
| **Alembic** | Versioned schema migrations |
| **psycopg** | PostgreSQL driver for SQLAlchemy |
| **SQLAdmin** | Browser UI at `/admin` for Postgres tables |
| **bcrypt** (or passlib) | Password hashing / verify |
| **JWT** (PyJWT or python-jose) | Access tokens after login |
| **FastAPI security** (`HTTPBearer` / OAuth2-style) | Protect `/auth/me` and later routes |
| **CORSMiddleware** | Allow the SPA origin to call the API |
| **`localStorage`** | Store JWT in the browser (learning choice) |

*(Carried forward from Sprint 1: FastAPI, Compose, React, React Router.)*

### What you will learn

- Keep growing the **layered** backend (`api` → `services` → `repositories` → `models`/`db`)
- Model users, activity types, and **unit types** (M:N) in PostgreSQL with Alembic migrations
- Seed system units, activity types, and their links
- Use SQLAdmin to view and manage Postgres data from FastAPI
- Implement register / login / `me` with bcrypt and JWT
- Lock **CORS** to your frontend origin
- Build Login / Register UI with token storage and a protected layout

### Layered backend (carry forward from Sprint 1)

Auth and data features follow the same call direction as health:

```text
api/auth.py  →  services/auth.py  →  repositories/user.py  →  models/user.py
                     ↑
              schemas/auth.py (DTOs at the edges)
```

| Put this here                                    | Not here                      |
| ------------------------------------------------ | ----------------------------- |
| HTTP status / `Depends`                          | `api/` only — not in services |
| Hash password, issue JWT, register rules         | `services/`                   |
| `SELECT` / `INSERT` user by email                | `repositories/`               |
| ORM `User` / `ActivityType` / `UnitType` classes | `models/`                     |
| Engine / `SessionLocal` / `get_db`               | `db/`                         |
| Pydantic request/response bodies                 | `schemas/`                    |

`admin.py` remains an allowed exception: SQLAdmin views may bind directly to models + engine.

### Two login systems (keep them separate)

| System           | Audience                      | How you authenticate                                           | Typical URL                |
| ---------------- | ----------------------------- | -------------------------------------------------------------- | -------------------------- |
| **SQLAdmin**     | You / demos inspecting the DB | Env `SQLADMIN_USERNAME` / `SQLADMIN_PASSWORD` + session cookie | `/admin`                   |
| **JWT app auth** | End users of the tracker      | Register / login API → Bearer token in the SPA                 | UI `/login`, API `/auth/*` |

A JWT from the app will **not** open SQLAdmin, and the admin password will **not** call `/auth/me`. Your README (S2-18) should spell this out.

### Out of scope (intentionally later)

| Topic                                            | When it arrives                 |
| ------------------------------------------------ | ------------------------------- |
| Sessions, WorkoutPlans, measurements             | Sprint 3                        |
| Goals (model + API; UI optional)                 | Sprint 3                        |
| Progress charts / analytics UI                   | Sprint 4                        |
| AI insights (e.g. Ollama)                        | Sprint 5                        |
| Full automated test suite / production hardening | Sprint 6 (optional; partial stretch here) |

### Week-by-week map

| Week  | Focus                                                         | Ticket IDs    | Checkpoint                                                              |
| ----- | ------------------------------------------------------------- | ------------- | ----------------------------------------------------------------------- |
| **1** | Engine/session, models (incl. units), Alembic, seed, SQLAdmin | S2-01 … S2-07 | Migrate + seed → units + exercise activities with links; `/admin` shows them |
| **2** | bcrypt, JWT, register/login/`me`, CORS                        | S2-08 … S2-13 | Auth works in OpenAPI; `/auth/me` needs a valid token                   |
| **3** | Register/Login UI, protected layout, logout, docs             | S2-14 … S2-18 | Full UI happy path without curl; README covers both logins              |

### How the tickets fit together

```text
Week 1                         Week 2                      Week 3
────────                       ────────                    ────────
Engine + Base + get_db()       hash / verify password      Register page
User + ActivityType + UnitType JWT + get_current_user      Login + localStorage token
Alembic + initial migration    POST register / login       Protected layout
Seed units + activities+links  GET /auth/me                Profile display + logout
SQLAdmin at /admin             CORS allowlist              README: JWT + /admin
```

Concepts from Sprint 1 (Compose, env settings, FastAPI routers, React Router, layered packages) are assumed. This file focuses on the **unit/activity catalog**, **ORM + migrations**, **SQLAdmin**, **JWT auth**, and the **auth UI**.

Do **Must** tickets first, then **Should** (S2-18), then **Stretch** if you have time.

**How to read each ticket:** **New here** explains the concept and lists **Docs & tutorials**. **Your task** states the deliverable. **Instructions** walk through the work. **Stay in scope** keeps later-sprint features out of this ticket. **Commit** means create a new Git commit when the ticket is done (ticket ID in the message).

### Ticket index

| ID                                                       | Title                                    | Week | Priority | Estimate |
| -------------------------------------------------------- | ---------------------------------------- | ---- | -------- | -------- |
| [S2-01](#s2-01--sqlalchemy-engine-session-and-base)      | SQLAlchemy engine, session, and Base     | 1    | Must     | M        |
| [S2-02](#s2-02--user-model)                              | User model                               | 1    | Must     | M        |
| [S2-03](#s2-03--activity-type-model)                     | ActivityType model                       | 1    | Must     | M        |
| [S2-04](#s2-04--unit-type-model-and-activity-links)      | UnitType model and activity links        | 1    | Must     | M        |
| [S2-05](#s2-05--alembic-setup-and-initial-migration)     | Alembic setup and initial migration      | 1    | Must     | L        |
| [S2-06](#s2-06--seed-system-catalog)                     | Seed system catalog (units + activities) | 1    | Must     | M        |
| [S2-07](#s2-07--sqladmin-ui-for-postgres)                | SQLAdmin UI for Postgres                 | 1    | Must     | L        |
| [S2-08](#s2-08--password-hashing-helpers)                | Password hashing helpers                 | 2    | Must     | S        |
| [S2-09](#s2-09--jwt-helpers-and-current-user-dependency) | JWT helpers and current user             | 2    | Must     | M        |
| [S2-10](#s2-10--register-endpoint)                       | Register endpoint                        | 2    | Must     | M        |
| [S2-11](#s2-11--login-endpoint)                          | Login endpoint                           | 2    | Must     | M        |
| [S2-12](#s2-12--me-endpoint)                             | Me endpoint                              | 2    | Must     | S        |
| [S2-13](#s2-13--cors-lockdown)                           | CORS lockdown                            | 2    | Must     | S        |
| [S2-14](#s2-14--register-page)                           | Register page                            | 3    | Must     | M        |
| [S2-15](#s2-15--login-page-and-token-storage)            | Login page and token storage             | 3    | Must     | M        |
| [S2-16](#s2-16--protected-layout)                        | Protected layout                         | 3    | Must     | M        |
| [S2-17](#s2-17--user-display-and-logout)                 | User display and logout                  | 3    | Must     | S        |
| [S2-18](#s2-18--auth--sqladmin-readme-notes)             | Auth + SQLAdmin README notes             | 3    | Should   | S        |
| [S2-S1](#s2-s1--stronger-password-rules)                 | Stronger password rules                  | —    | Stretch  | S        |
| [S2-S2](#s2-s2--email-normalization)                     | Email normalization                      | —    | Stretch  | S        |
| [S2-S3](#s2-s3--api-test-register--login--me)            | API test: register → login → me          | —    | Stretch  | M        |
| [S2-S4](#s2-s4--keep-sqladmin-views-in-sync)             | Keep SQLAdmin views in sync              | —    | Stretch  | S        |

---

## S2-01 — SQLAlchemy engine, session, and Base

| Field          | Value                                                |
| -------------- | ---------------------------------------------------- |
| **Type**       | feature                                              |
| **Week**       | 1                                                    |
| **Priority**   | Must                                                 |
| **Estimate**   | M                                                    |
| **Depends on** | Sprint 1 complete (`DATABASE_URL`, Compose Postgres) |

### New here: ORM, SQLAlchemy engine, and sessions

An **ORM** (Object-Relational Mapper) lets you work with database rows as Python objects instead of writing raw SQL for every read/write. **SQLAlchemy** is the standard ORM for this course.

Key pieces you create once and reuse everywhere:

| Piece                          | Role                                                                                      |
| ------------------------------ | ----------------------------------------------------------------------------------------- |
| **Engine**                     | Connection pool to Postgres, built from `DATABASE_URL`                                    |
| **`Session` / `SessionLocal`** | Short-lived unit of work: query, add, commit, close                                       |
| **`Base`**                     | Declarative base class; your models inherit from it so tables register in `Base.metadata` |
| **`get_db()`**                 | FastAPI **dependency** that yields a session per request and closes it afterward          |

**`pool_pre_ping=True`:** before using a pooled connection, SQLAlchemy checks it is still alive—useful when Postgres restarts under Compose.

**Sync vs async:** keep **sync** SQLAlchemy unless your team already chose async end-to-end. Mixing styles early adds confusion without much benefit for this sprint.

**Driver note:** with Postgres you typically use a URL like `postgresql+psycopg://user:pass@db:5432/dbname` and depend on `psycopg[binary]`.

**Docs & tutorials:**

- [SQLAlchemy 2.0 tutorial](https://docs.sqlalchemy.org/en/20/tutorial/) — engine, connections, and ORM overview
- [Engines and connections](https://docs.sqlalchemy.org/en/20/core/engines.html) — `create_engine` and `DATABASE_URL`
- [Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html) — `Session` / `sessionmaker`
- [FastAPI — SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/) — `Depends` + `get_db` pattern
- [psycopg 3](https://www.psycopg.org/psycopg3/docs/) — Postgres driver used with SQLAlchemy

### Your task

Create the shared SQLAlchemy engine, session factory, and declarative `Base` that every later model and route will use. Auth, SQLAdmin, and Sprint 3 sessions all need one engine and `get_db()`—creating a new engine inside every request is fragile and hard to test. Your deliverable is `Base`, `SessionLocal`, and a FastAPI-ready `get_db()` that reads `DATABASE_URL` from settings.

### Instructions

1. Add a declarative `Base` in `backend/app/db/base.py` (or equivalent). Models in later tickets will inherit from this class so tables register on `Base.metadata`.
2. Create an engine from settings/`DATABASE_URL` with `pool_pre_ping=True`. Keep the URL only in settings/env—never hard-code passwords in `session.py`.
3. Add `SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)` (or equivalent) in `backend/app/db/session.py`.
4. Implement `get_db()` as a generator: `yield` a session, `finally` close it—so FastAPI can inject `db: Session = Depends(get_db)`.
5. Add `sqlalchemy` and `psycopg[binary]` to `backend/requirements.txt` if they are not already present. Reinstall into the API image / venv.
6. If you built `/health/db` in Sprint 1 stretch, point that ping at this shared engine instead of a one-off connection.
7. Check your work: from `backend/`, import `app.db.session` (or start the API) and confirm it loads without error. A later ticket will apply migrations against this engine.

### Stay in scope

- Leave ORM table models for S2-02 … S2-04.
- Leave Alembic, seed, and SQLAdmin for S2-05 … S2-07.
- Leave JWT and auth routes for Week 2.

### Hints

- Import model modules before migrations/`create_all` so metadata is populated (empty metadata → empty migrations).
- Keep **sync** SQLAlchemy unless the whole team already committed to async.

### Acceptance criteria

- [ ] Shared engine and session factory exist
- [ ] `get_db()` (or equivalent) yields and closes sessions
- [ ] DB URL comes from settings/env

### Suggested paths

`backend/app/db/base.py`, `backend/app/db/session.py`, `backend/requirements.txt`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-01` in the message, for example `S2-01: short summary`. Never commit `.env` or secrets.

---

## S2-02 — User model

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 1       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S2-01   |

### New here: ORM models and table mapping

An **ORM model** is a Python class mapped to a database table. Columns become attributes; SQLAlchemy translates `session.query(User)` / `select(User)` into SQL.

Important design choices for `User`:

- **Primary key (`id`):** UUID or integer—pick one style and reuse it on later tables.
- **Unique `email`:** enforced in the database (`unique=True` / unique constraint), not only in Python—race conditions need the DB constraint.
- **`password_hash` only:** never a column named `password` that stores plain text. Hashing helpers come in S2-08; the column exists now.
- **`__str__` / `__repr__`:** optional for Python, very helpful for SQLAdmin list labels later this week.

Timestamps: prefer timezone-aware UTC (`created_at`) so demos across machines stay consistent.

**Docs & tutorials:**

- [ORM Declared Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#declarative-mapping) — map classes to tables
- [Table configuration with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html) — columns, types, constraints
- [FastAPI — Create the database models](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models) — model layout in a FastAPI app
- [Constraints and Indexes](https://docs.sqlalchemy.org/en/20/core/constraints.html) — unique constraints (e.g. on `email`)

### Your task

Define the `User` ORM model so later tickets can register accounts and attach sessions to a real identity. Getting columns and uniqueness right now avoids a painful migration later. Your deliverable is a `users` table mapping with unique email and `password_hash` only—no plain-text password column.

### Instructions

1. Add `backend/app/models/user.py` inheriting from `Base`.
2. Include at least: `id`, `email` (unique), `password_hash`, `display_name`, `created_at`. Map it to a clear table name (e.g. `users`).
3. Store credentials only as `password_hash`. Leave hashing helpers for S2-08; the column is enough here.
4. Add a readable `__str__` (helps SQLAdmin list views in S2-07).
5. Import the model from `backend/app/models/__init__.py` (or Alembic’s `env.py` later) so `Base.metadata` sees it.
6. Check your work: import `User` from the package and confirm it has no `password` column—only `password_hash`.

### Stay in scope

- Leave password hashing helpers for S2-08.
- Leave register/login routes for S2-10 / S2-11.
- Leave sessions, plans, and goals for Sprint 3.

### Hints

- Put models under `backend/app/models/` and import them from a package `__init__` or Alembic’s `env.py` so metadata sees them.
- Email length: a reasonable `String(255)` (or similar) is enough for demos.
- Pick UUID or integer PKs now and reuse that style on `ActivityType` and `UnitType`.

### Acceptance criteria

- [ ] Model maps to a users table
- [ ] Email is unique at the database level
- [ ] Password is stored only as `password_hash`

### Suggested paths

`backend/app/models/user.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-02` in the message, for example `S2-02: short summary`. Never commit `.env` or secrets.

---

## S2-03 — ActivityType model

| Field          | Value                                |
| -------------- | ------------------------------------ |
| **Type**       | feature                              |
| **Week**       | 1                                    |
| **Priority**   | Must                                 |
| **Estimate**   | M                                    |
| **Depends on** | S2-02 (same migration batch is fine) |

### New here: reference data and system vs custom rows

**Activity types** are the catalog of **individual exercises** (running, bench press, hammer curl, …). Sprint 3 attaches **session items** to these types. Modeling **system** vs **custom** now prepares user-defined exercises without redesigning the table later.

Measurement kinds are **not** columns on this table. They live in **`UnitType`**, linked many-to-many in **S2-04**, so one activity can support several units (Running → duration + distance; Bench press → reps + weight).

Typical fields:

| Field       | Meaning                                                        |
| ----------- | -------------------------------------------------------------- |
| `name`      | Human label (“Running”)                                        |
| `slug`      | Stable machine id (`running`)—URL-safe, used in seeds and APIs |
| `is_system` | `True` for built-in seeded types                               |
| `user_id`   | `NULL` for system types; set for custom types owned by a user  |

**Uniqueness:** system slugs should be unique globally; custom types often use unique `(user_id, slug)`. Add that constraint now or document it clearly for Sprint 3.

**Docs & tutorials:**

- [SQLAlchemy relationships](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html) — optional `user_id` foreign keys and related objects
- [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#unique-constraint) — composite uniqueness like `(user_id, slug)`
- [PostgreSQL UNIQUE](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS) — how the DB enforces uniqueness

### Your task

Add the `ActivityType` ORM model so Sprint 3 sessions have a catalog to attach to, instead of hard-coded strings in the frontend. Keep measurement kinds off this table—units arrive in S2-04. Your deliverable is an `activity_types` mapping that can express system vs custom rows.

### Instructions

1. Add `backend/app/models/activity_type.py` with fields: `name`, `slug`, `is_system`, and optional `user_id` for custom types.
2. Mark system rows as `is_system=True` and `user_id=NULL`.
3. Document (or add) uniqueness: global unique slugs for system types; unique `(user_id, slug)` for custom types (add the constraint now or write it down for Sprint 3).
4. Add a readable `__str__` (helps SQLAdmin list views in S2-07).
5. Leave room for a relationship to unit links—you will wire it in S2-04.
6. Import the model so `Base.metadata` includes it (same pattern as `User`).

### Stay in scope

- Leave the unit catalog and M:N link table for S2-04.
- Leave a single-unit hint column off this model—measurement kinds belong on `UnitType`.
- Leave session items and custom-activity APIs for Sprint 3.

### Hints

- Keep slugs lowercase and URL-safe (`running`, `bench_press`, `hammer_curl`, …).
- The system exercise types themselves are seeded in S2-06; this ticket is the table shape.

### Acceptance criteria

- [ ] System vs custom is expressible
- [ ] No single-unit hint column on activity types
- [ ] Ready for unique `(user_id, slug)` on customs (add now or document for Sprint 3)

### Suggested paths

`backend/app/models/activity_type.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-03` in the message, for example `S2-03: short summary`. Never commit `.env` or secrets.

---

## S2-04 — UnitType model and activity links

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 1       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S2-03   |

### New here: measurement catalog and M:N links

A **unit type** is a reusable measurement kind: duration, distance, reps, weight, and so on. Activities **declare which units they accept** through a junction table.

| Table                      | Role                                                                             |
| -------------------------- | -------------------------------------------------------------------------------- |
| `unit_types`               | Catalog: `name`, `slug`, optional `unit_label` (`min`, `km`, `kg`), `is_system`  |
| `activity_type_unit_types` | Link: `activity_type_id`, `unit_type_id`, `sort_order`, `is_required`, `per_set` |

**`per_set`:** when `True`, Sprint 3 logs values with a `set_index` (reps/weight per set). Cardio units usually have `per_set=False` (one value per session item).

Example links after seed:

- Running / cycling (and similar cardio) → `duration_min` + `distance_km`
- Strength exercises (e.g. `bench_press`, `barbell_curl`, `hammer_curl`, `incline_curl`, `face_pull`) → `reps` + `weight_kg` (both `per_set=True`)
- Optional catch-all `other` → e.g. `duration_min` only

Do **not** seed a single coarse `gym` activity as the strength story—Sprint 3 demos need per-exercise types.
- Other → `duration_min`

**Docs & tutorials:**

- [Many-to-many relationships](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many) — activities ↔ units via a link table
- [Association Object](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object) — extra columns on the link (`sort_order`, `per_set`, …)
- [Foreign Key](https://docs.sqlalchemy.org/en/20/core/constraints.html#foreign-key) — `activity_type_id` / `unit_type_id` references

### Your task

Add `UnitType` and the activity↔unit association so one activity can accept several measurements. Strength work needs reps and weight; a run needs time and distance—one column on the activity cannot express that. Your deliverable is `unit_types` plus `activity_type_unit_types` with `sort_order`, `is_required`, and `per_set`. This is the foundation Sprint 3 session measurements will read.

### Instructions

1. Add `UnitType` in `backend/app/models/unit_type.py` mapped to `unit_types` (`name`, `slug`, optional `unit_label`, `is_system`).
2. Add `ActivityTypeUnitType` in `backend/app/models/activity_type_unit_type.py` with `activity_type_id`, `unit_type_id`, `sort_order`, `is_required`, and `per_set`.
3. Put a unique constraint on `(activity_type_id, unit_type_id)` so the same pair cannot be linked twice.
4. Wire relationships from `ActivityType` / `UnitType` to the link rows (association object, not a bare secondary table—you need the extra columns).
5. Add a thin repository if useful (`backend/app/repositories/unit_type.py`): find unit by slug; create link if missing. Keep it thin.
6. Include both tables in the same Alembic revision batch as S2-05 (or immediately after). Confirm the models import and appear on `Base.metadata`.

### Stay in scope

- Leave seed rows (the four units, six activities, and their links) for S2-06.
- Leave session measurement tables for Sprint 3.
- Leave a single-unit hint column off `ActivityType`—use this M:N catalog instead.

### Hints

- Seeded system unit slugs will be: `duration_min`, `distance_km`, `reps`, `weight_kg`.
- Keep repositories thin: find unit by slug; create link if missing.

### Acceptance criteria

- [ ] `unit_types` and `activity_type_unit_types` exist in the schema
- [ ] An activity can link to multiple unit types
- [ ] `per_set` and `sort_order` are expressible on the link

### Suggested paths

`backend/app/models/unit_type.py`, `backend/app/models/activity_type_unit_type.py`, `backend/app/repositories/unit_type.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-04` in the message, for example `S2-04: short summary`. Never commit `.env` or secrets.

---

## S2-05 — Alembic setup and initial migration

| Field          | Value               |
| -------------- | ------------------- |
| **Type**       | feature             |
| **Week**       | 1                   |
| **Priority**   | Must                |
| **Estimate**   | L                   |
| **Depends on** | S2-02, S2-03, S2-04 |

### New here: schema migrations (Alembic)

**Migrations** are versioned scripts that change the database schema (create tables, add columns, …). **Alembic** is SQLAlchemy’s migration tool.

Why not only `Base.metadata.create_all()`?

| Approach     | Pros                                                      | Cons                                                    |
| ------------ | --------------------------------------------------------- | ------------------------------------------------------- |
| `create_all` | Fast for first experiments                                | Does not upgrade existing DBs safely; teammates diverge |
| **Alembic**  | Shared history in Git; upgrade/downgrade; works in Docker | Slightly more setup                                     |

Typical workflow:

1. `alembic init` (or copy a template) → `alembic/` + `alembic.ini`
2. Point `env.py` at your `Base.metadata` and `DATABASE_URL`
3. `alembic revision --autogenerate -m "initial"` → review the script
4. `alembic upgrade head` → apply to the database

**Commit migration files**—they are source code for your schema.

**Docs & tutorials:**

- [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/) — overview and configuration
- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) — `init`, `revision`, `upgrade`
- [Auto Generating Migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) — `--autogenerate` (review before applying)
- [FastAPI + Alembic (community guide)](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-tables) — creating tables in a FastAPI project (pair with Alembic for upgrades)

### Your task

Initialize Alembic and commit the first revision so every teammate and every Docker environment applies the same schema. `create_all` is fine for a first experiment; Alembic is how you share schema changes. Your deliverable is Alembic config plus a reviewed initial migration that creates `users`, `activity_types`, `unit_types`, and `activity_type_unit_types`.

### Instructions

1. Add Alembic (`alembic` in `requirements.txt`) and initialize it against your SQLAlchemy metadata (`User`, `ActivityType`, `UnitType`, `ActivityTypeUnitType`).
2. Point `alembic/env.py` at the same `DATABASE_URL` as the app, and import the model modules so `Base.metadata` is complete.
3. Generate the first revision creating `users`, `activity_types`, `unit_types`, and `activity_type_unit_types` (`alembic revision --autogenerate -m "initial"`).
4. **Review** the autogenerated file (autogenerate is helpful, not perfect). Confirm all four tables and expected unique/FK constraints are present.
5. Document `alembic upgrade head` and where to run it—host vs API container. In Compose, a typical path is `docker compose exec api alembic upgrade head`.
6. Commit the migration files. Verify on a **fresh** database (new Compose volume or dropped schema): upgrade applies cleanly with no leftover `create_all`-only tables.

### Stay in scope

- Leave catalog seed data for S2-06.
- Leave SQLAdmin for S2-07.
- You may still call `create_all` briefly while prototyping; Alembic should be the documented path before the sprint demo.

### Hints

- Point Alembic at the same `DATABASE_URL` as the app.
- Empty metadata usually means models were not imported in `env.py`.
- You may still call `create_all` briefly while prototyping, but Alembic should be the documented path before the sprint demo.

### Acceptance criteria

- [ ] Alembic initialized and documented
- [ ] Fresh DB applies migration cleanly
- [ ] Migration is checked into the repo

### Suggested paths

`backend/alembic/`, `backend/alembic.ini`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-05` in the message, for example `S2-05: short summary`. Never commit `.env` or secrets.

---

## S2-06 — Seed system catalog

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 1            |
| **Priority**   | Must         |
| **Estimate**   | M            |
| **Depends on** | S2-04, S2-05 |

### New here: seed / reference data

**Seeding** inserts known rows so every environment starts with the same baseline data. Without seeds, demos break (“my activity type dropdown is empty”) and SQLAdmin has nothing useful to show.

**Idempotent seed:** running the seed twice must not create duplicates. Seed in order: **unit types → activity types → activity↔unit links**.

System activity types for this course (exercise-level; adjust names but keep the idea):

Cardio examples: `running`, `cycling` (optional: `swimming`, `hiking`)  
Strength examples: `bench_press`, `barbell_curl`, `hammer_curl`, `incline_curl`, `face_pull`  
Optional catch-all: `other`

Do **not** rely on a single coarse `gym` activity for strength—seed concrete exercises.

System unit types: `duration_min`, `distance_km`, `reps`, `weight_kg` (with sensible labels).

**Docs & tutorials:**

- [ORM Data Manipulation (SQLAlchemy)](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html) — insert rows with a `Session`
- [SELECT / querying (SQLAlchemy)](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html) — look up existing rows by `slug` before insert
- [PostgreSQL INSERT … ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT) — DB-level upsert if you prefer SQL

### Your task

Seed the system unit types, **exercise-level** activity types, and their M:N links so every environment starts with the same catalog. Without those rows, Sprint 3 cannot know which inputs to show for Running vs Bench press, and SQLAdmin looks empty. Your deliverable is an idempotent seed path (service + repositories) documented in the README.

### Instructions

1. Seed the four system unit types, idempotent by `slug`: `duration_min`, `distance_km`, `reps`, `weight_kg` (with sensible labels such as `min`, `km`, `kg`).
2. Seed system activity types with `name`, `slug`, and `is_system=True` covering at least: cardio (`running`, `cycling`, …) and several strength exercises (`bench_press`, `barbell_curl`, `hammer_curl`, `incline_curl`, `face_pull`, …), plus optional `other`.
3. Seed M:N links:
   - Cardio exercises → `duration_min` + `distance_km` (typically `per_set=False`)
   - Strength exercises → `reps` + `weight_kg` (both `per_set=True`)
   - Other → e.g. `duration_min`
4. Implement in `backend/app/services/seed.py` using repositories (`activity_type`, `unit_type`). Call from a thin `backend/app/db/init_db.py` and/or a documented script. Upsert or get-or-create by `slug`; skip existing links on re-run.
5. Document the seed path in the README (how to run it after `alembic upgrade head`).
6. Check your work: run seed twice. Confirm four units, exercise activities present, Running linked to duration + distance, at least one strength exercise linked to reps + weight with `per_set`, and no duplicate rows.

### Stay in scope

- Leave SQLAdmin views for S2-07 (seed first so `/admin` has rows to show).
- Leave session logging and custom user-created activities for Sprint 3.
- Leave charts and AI for Sprints 4–5.

### Hints

- Upsert or “get-or-create” by `slug` for system rows; skip existing links on re-run.
- You can keep a small demo hook now and still add a fuller `seed.py` in optional Sprint 6.

### Acceptance criteria

- [ ] All four unit types exist after seed
- [ ] Exercise-level system activities exist (not only a coarse `gym` type)
- [ ] Running (or equivalent cardio) is linked to duration and distance; a strength exercise to reps and weight (`per_set`)
- [ ] Re-running does not duplicate rows or links
- [ ] Seed path documented

### Suggested paths

`backend/app/services/seed.py`, `backend/app/repositories/activity_type.py`, `backend/app/repositories/unit_type.py`, `backend/app/db/init_db.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-06` in the message, for example `S2-06: short summary`. Never commit `.env` or secrets.

---

## S2-07 — SQLAdmin UI for Postgres

| Field          | Value                                    |
| -------------- | ---------------------------------------- |
| **Type**       | feature                                  |
| **Week**       | 1                                        |
| **Priority**   | Must                                     |
| **Estimate**   | L                                        |
| **Depends on** | S2-01, S2-02, S2-03, S2-04, S2-05, S2-06 |

### New here: SQLAdmin (database admin UI)

**SQLAdmin** is a FastAPI/Starlette admin package that mounts a browser UI (usually at `/admin`) on top of your SQLAlchemy models. You can list, search, create, edit, and delete rows without installing pgAdmin or writing SQL by hand.

It is **not** the same as JWT user auth:

| System                   | Who uses it                          | How you log in                                        |
| ------------------------ | ------------------------------------ | ----------------------------------------------------- |
| **SQLAdmin**             | Developers / demos inspecting the DB | Env username/password (`SQLADMIN_*`) + session cookie |
| **JWT auth** (weeks 2–3) | App end-users                        | Register/login API → Bearer token                     |

**`ModelView`:** tells SQLAdmin how to present one model (columns, search, sort). Add views for `User`, `ActivityType`, `UnitType`, and the activity↔unit link (or inspect links via related views).

**`SessionMiddleware` + `SQLADMIN_SECRET_KEY`:** admin login uses signed cookies; Starlette needs a secret key. Put it in env—never commit a production secret.

**`itsdangerous`:** often pulled in for cookie signing; list it explicitly if your installer does not.

Hide sensitive columns (e.g. `password_hash`) from detail/list views where sensible.

**Docs & tutorials:**

- [SQLAdmin documentation](https://aminalaee.dev/sqladmin/) — install, mount, and `ModelView`
- [SQLAdmin authentication](https://aminalaee.dev/sqladmin/authentication/) — env-based admin login
- [Starlette SessionMiddleware](https://www.starlette.io/middleware/#sessionmiddleware) — signed cookies for `/admin` login
- [itsdangerous](https://itsdangerous.palletsprojects.com/) — cookie signing used under the hood

### Your task

Mount SQLAdmin at `/admin` with env-based login so you can browse Postgres in the browser during demos and debugging. This is a Sprint 2 Must—not a leftover from Sprint 1. Your deliverable is `/admin` showing users, unit types, activity types, and links after seed (Running → duration + distance; a strength exercise → per-set reps/weight). JWT app auth arrives in Week 2; keep the two logins separate.

### Instructions

1. Add `sqladmin` and `itsdangerous` to `backend/requirements.txt`.
2. Mount SQLAdmin on the FastAPI app at `/admin` (typically from `backend/app/admin.py`, wired in `backend/app/main.py`).
3. Add `ModelView`s for `User`, `ActivityType`, `UnitType`, and activity↔unit links. Exclude sensitive fields from views where sensible (hide `password_hash`).
4. Protect `/admin` with SQLAdmin’s authentication backend using env credentials (`SQLADMIN_USERNAME` / `SQLADMIN_PASSWORD`).
5. Add Starlette `SessionMiddleware` with `SQLADMIN_SECRET_KEY`. Put the key in env—never commit a production secret.
6. Pass SQLAdmin env vars into the Compose `api` service and document them in `.env.example`.
7. Check your work: open `http://localhost:8000/admin`, log in with the env credentials, and confirm system exercise activity types, four unit types, and Running’s dual units (plus a strength exercise’s per-set links) are visible after seed.

### Stay in scope

- Leave JWT register/login/`me` for S2-08 … S2-12. SQLAdmin credentials are a separate login.
- Leave sessions, plans, and goals out of `/admin` until those models exist (Sprint 3). Stretch S2-S4 covers keeping views in sync later.
- Default `admin`/`admin` is fine for local learning—document changing it for shared machines.

### Hints

- Default `admin`/`admin` is fine for local learning—document changing it for shared machines.
- After seed, you should see system exercise activity types, four unit types, and their links in the UI.
- If `/admin` 500s, check middleware order and that models are imported before views register.

### Acceptance criteria

- [ ] `/admin` opens and requires login
- [ ] Users, activity types, unit types (and links) are manageable in the UI
- [ ] Credentials and secret key come from env / `.env.example`
- [ ] Compose `api` service receives the SQLAdmin env vars
- [ ] Seeded catalog (including Running’s dual units and a strength exercise’s `per_set` links) is visible after login

### Suggested paths

`backend/app/admin.py`, `backend/app/main.py`, `docker-compose.yml`, `.env.example`, `backend/requirements.txt`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-07` in the message, for example `S2-07: short summary`. Never commit `.env` or secrets.

---

## S2-08 — Password hashing helpers

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 2       |
| **Priority**   | Must    |
| **Estimate**   | S       |
| **Depends on** | S2-02   |

### New here: password hashing (bcrypt)

You must **never** store passwords in plain text. Instead you store a **hash**—a one-way transformation. On login you hash the attempt and compare.

**bcrypt** is a widely used password hashing algorithm (slow on purpose, which resists brute-force). Use it directly or via **passlib**—either is fine if verify/hash behavior is correct.

Typical helpers:

```python
def hash_password(plain: str) -> str: ...
def verify_password(plain: str, password_hash: str) -> bool: ...
```

Keep them as plain functions so you can unit-test without spinning up HTTP.

Never log the raw password. Avoid returning it in API errors.

**Docs & tutorials:**

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) — why slow hashes (bcrypt/argon2)
- [passlib — bcrypt](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html) — hash/verify helpers (if you use passlib)
- [bcrypt (PyPI / docs)](https://github.com/pyca/bcrypt) — using the `bcrypt` library directly
- [FastAPI security intro](https://fastapi.tiangolo.com/tutorial/security/) — password handling context in APIs

### Your task

Implement shared `hash_password` / `verify_password` helpers with bcrypt so register and login hash the same way. Storing plain passwords is a hard fail in demos and in real systems. Your deliverable is two unit-testable functions in `core/security.py` (or equivalent)—no HTTP routes yet.

### Instructions

1. Add bcrypt (direct library or via passlib) to `backend/requirements.txt`.
2. Implement `hash_password(plain: str) -> str` and `verify_password(plain: str, password_hash: str) -> bool` in `backend/app/core/security.py`.
3. Keep them as plain functions so you can call them without FastAPI or a database.
4. Smoke-test: hash a sample string → `verify_password` returns true; a wrong password returns false. Never log the raw password.
5. Confirm `User.password_hash` is the only password-related column (from S2-02)—helpers write into that field in S2-10.

### Stay in scope

- Leave JWT issue/verify and `get_current_user` for S2-09.
- Leave `POST /auth/register` and `POST /auth/login` for S2-10 / S2-11.
- Leave password-complexity rules for stretch S2-S1.

### Hints

- Bcrypt needs consistent `str`/`bytes` handling—watch encoding.
- Very long passwords may be truncated by bcrypt; documenting a max length (e.g. 72 bytes) is a good habit.
- On some platforms, `bcrypt` version pins matter—if install fails, check the error and pin a known-good pair of packages.

### Acceptance criteria

- [ ] Hashing uses bcrypt
- [ ] Verify returns false for wrong passwords
- [ ] Helpers are unit-testable without HTTP

### Suggested paths

`backend/app/core/security.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-08` in the message, for example `S2-08: short summary`. Never commit `.env` or secrets.

---

## S2-09 — JWT helpers and current user dependency

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 2       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S2-08   |

### New here: JWT and FastAPI security dependencies

**JWT** (JSON Web Token) is a signed string the server issues after login. The client sends it on later requests as:

`Authorization: Bearer <token>`

The server verifies the signature and expiry, then trusts claims such as `sub` (subject = user id).

Typical settings (env):

- `SECRET_KEY` / `JWT_SECRET` — signing key (long random string; never commit real secrets)
- `ACCESS_TOKEN_EXPIRE_MINUTES` — how long tokens stay valid

**`get_current_user`:** a FastAPI dependency that:

1. Extracts the Bearer token (HTTPBearer / OAuth2 password flow in OpenAPI)
2. Decodes and validates it
3. Loads the `User` from the DB (clearest for learning) or trusted claims
4. Raises `401` if missing/invalid/expired

Libraries commonly used: `python-jose` or `PyJWT`—pick one and stick to it.

**Docs & tutorials:**

- [Introduction to JSON Web Tokens](https://jwt.io/introduction) — what a JWT is and what claims mean
- [FastAPI — OAuth2 with Password (and hashing), Bearer with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) — end-to-end JWT pattern
- [PyJWT documentation](https://pyjwt.readthedocs.io/en/stable/) — encode/decode if you choose PyJWT
- [python-jose](https://python-jose.readthedocs.io/en/latest/) — encode/decode if you choose jose
- [FastAPI — Security / HTTPBearer](https://fastapi.tiangolo.com/reference/security/) — Bearer scheme for OpenAPI Authorize

### Your task

Add JWT encode/decode helpers and a `get_current_user` dependency so protected routes share one “who is calling?” check. Sprint 3 sessions and plans will reuse this same dependency. Your deliverable is token create/verify plus a 401 on missing, invalid, or expired tokens, with secret/expiry documented in `.env.example`.

### Instructions

1. Add a JWT library (`PyJWT` or `python-jose`) to `backend/requirements.txt`. Pick one and stick to it.
2. Add settings placeholders in `.env.example`: `SECRET_KEY` / `JWT_SECRET` and `ACCESS_TOKEN_EXPIRE_MINUTES`. Use a strong random secret in the real `.env`; never commit it.
3. Implement create/decode helpers in `backend/app/core/security.py`: subject = user id, expiry from settings. Keep the payload minimal—leave password hashes out of the token.
4. Implement `get_current_user` in `backend/app/core/deps.py`: extract Bearer token (prefer HTTPBearer so OpenAPI’s **Authorize** button works), decode/validate, load the `User` from the DB, raise `401` if missing/invalid/expired.
5. Check your work: call the decode helper with a garbage string and confirm it fails; a token you just created should decode to the same subject. Wire it onto `/auth/me` in S2-12.

### Stay in scope

- Leave `POST /auth/login` (the route that issues tokens) for S2-11.
- Leave `GET /auth/me` for S2-12.
- Leave refresh tokens for later—access tokens alone are enough for Sprint 2.

### Hints

- Prefer the HTTP Bearer scheme so OpenAPI’s **Authorize** button works in `/docs`.
- Use a strong random secret in real `.env`; rotate it if it ever leaks into Git.
- Keep token payload minimal—leave password hashes out of JWTs.

### Acceptance criteria

- [ ] Token includes subject and expiry
- [ ] Invalid/missing token → 401
- [ ] JWT settings documented in `.env.example`

### Suggested paths

`backend/app/core/security.py`, `backend/app/core/deps.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-09` in the message, for example `S2-09: short summary`. Never commit `.env` or secrets.

---

## S2-10 — Register endpoint

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 2            |
| **Priority**   | Must         |
| **Estimate**   | M            |
| **Depends on** | S2-08, S2-02 |

### New here: auth request/response schemas (Pydantic)

**Pydantic models** (schemas) define the JSON shape of requests and responses. They validate types and required fields before your route logic runs—invalid bodies become HTTP 422 automatically.

Typical split:

- `UserCreate` / `RegisterRequest` — email, password, display_name (input)
- `UserPublic` / `UserRead` — id, email, display_name (output; **no** password fields)

**`POST /auth/register`:** create a user row with `password_hash=hash_password(...)`. On duplicate email, return a clear **400** or **409** (pick one and stick to it).

Decide whether register returns only the public user, or user + access token (auto-login). Document the choice for the frontend team.

**Docs & tutorials:**

- [Pydantic models](https://docs.pydantic.dev/latest/) — request/response validation
- [FastAPI — Request body](https://fastapi.tiangolo.com/tutorial/body/) — Pydantic bodies on POST
- [FastAPI — Response Model](https://fastapi.tiangolo.com/tutorial/response-model/) — public schemas without password fields
- [HTTP status codes — 409 Conflict (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/409) — duplicate email option

### Your task

Implement `POST /auth/register` so demo users can be created through the API. Validation and hashing here set the security baseline for the whole app. Your deliverable is a layered register route (`api` → `services` → `repositories`) that stores bcrypt hashes and never returns password fields.

### Instructions

1. Add Pydantic schemas in `backend/app/schemas/auth.py`: register body (`email`, `password`, `display_name`) and a public user response (`id`, `email`, `display_name`—no `password` or `password_hash`).
2. Add `backend/app/repositories/user.py` with lookup-by-email and create-user helpers.
3. Put register logic in `backend/app/services/auth.py`: hash with S2-08 helpers, persist via the repository. On duplicate email, raise a clear error the router can map to **400** or **409** (pick one and stick to it).
4. Add a thin `backend/app/api/auth.py` router (`APIRouter(prefix="/auth")`): `POST /auth/register` validates → calls the service → maps errors to HTTP. Include the router in `main.py`.
5. Decide the success body: public user fields only, or user + access token (auto-login). Document the choice for the frontend (S2-14).
6. Check your work in `/docs`: register once (200/201, no password fields); register the same email again (400/409). Confirm the hashed value in SQLAdmin is not the plain password.

### Stay in scope

- Leave `POST /auth/login` for S2-11 and `GET /auth/me` for S2-12.
- Leave the Register page for S2-14.
- Leave stronger password complexity for stretch S2-S1 and email lowercasing for S2-S2.

### Hints

- Responses must never include `password` or `password_hash`.
- Basic email format validation in the schema catches typos early.
- Use a dedicated auth router (`APIRouter(prefix="/auth")`) so `main.py` stays thin.

### Acceptance criteria

- [ ] Duplicate email returns a clear client error
- [ ] Password never appears in logs or responses
- [ ] Response shape documented and consistent

### Suggested paths

`backend/app/api/auth.py`, `backend/app/services/auth.py`, `backend/app/repositories/user.py`, `backend/app/schemas/auth.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-10` in the message, for example `S2-10: short summary`. Never commit `.env` or secrets.

---

## S2-11 — Login endpoint

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 2            |
| **Priority**   | Must         |
| **Estimate**   | M            |
| **Depends on** | S2-08, S2-09 |

### New here: issuing tokens (login flow)

**Login** checks credentials and returns an access token the client will store and reuse.

Standard success body (OAuth2-ish, works well with OpenAPI):

```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```

**Account enumeration:** returning different errors for “unknown email” vs “bad password” helps attackers discover valid accounts. Prefer the **same generic 401 message** for both cases (document if your team deliberately chooses otherwise).

After login, immediately test the token against `/auth/me` (next ticket) in `/docs`.

**Docs & tutorials:**

- [FastAPI — Simple OAuth2 with Password and Bearer](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/) — login → token response shape
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) — generic error messages / account enumeration
- [HTTP 401 Unauthorized (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/401) — failed credential response

### Your task

Implement `POST /auth/login` so a valid email/password returns a bearer JWT the frontend can store. Wrong credentials must fail with a generic 401. Your deliverable is a layered login route that verifies bcrypt hashes and issues the token from S2-09.

### Instructions

1. Add a Pydantic login body in `backend/app/schemas/auth.py` (`email`, `password`) and a token response (`access_token`, `token_type`).
2. Put login logic in `backend/app/services/auth.py`: look up the user via `repositories/user.py`, `verify_password`, create a JWT with the S2-09 helper.
3. Keep `POST /auth/login` in `backend/app/api/auth.py` thin: validate → call service → map errors to HTTP.
4. On success return `{ "access_token": "<jwt>", "token_type": "bearer" }`. On unknown email or bad password, return **401** with the **same generic message**.
5. Wire OpenAPI so the token can be used via **Authorize** if you configured Bearer security.
6. Check your work in `/docs`: wrong password → 401; successful login returns a token. You will send that token to `/auth/me` in S2-12.

### Stay in scope

- Leave `GET /auth/me` for S2-12.
- Leave the Login page and `localStorage` for S2-15.
- Leave refresh-token complexity for later—access tokens alone are enough for Sprint 2.

### Hints

- Timing differences can still leak info in theory; for this course, generic messages are the main requirement.
- Access tokens alone are enough for Sprint 2.

### Acceptance criteria

- [ ] Wrong credentials → 401 with documented behavior
- [ ] Successful login returns a bearer token usable by `/auth/me`
- [ ] Request validated with Pydantic

### Suggested paths

`backend/app/api/auth.py`, `backend/app/services/auth.py`, `backend/app/repositories/user.py`, `backend/app/schemas/auth.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-11` in the message, for example `S2-11: short summary`. Never commit `.env` or secrets.

---

## S2-12 — Me endpoint

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 2       |
| **Priority**   | Must    |
| **Estimate**   | S       |
| **Depends on** | S2-09   |

### New here: protected routes

A **protected route** depends on `get_current_user` (or equivalent). Unauthenticated callers get **401**; authenticated callers get their profile.

`GET /auth/me` is the smallest useful protected endpoint: it proves JWT wiring and gives the UI someone to display after refresh.

Return **public fields only**—id, email, display_name (and `created_at` if useful). Never return `password_hash`.

**Docs & tutorials:**

- [FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) — `Depends(get_current_user)` on routes
- [FastAPI — Security](https://fastapi.tiangolo.com/tutorial/security/) — protecting endpoints with schemes
- [FastAPI — OAuth2 JWT (current user)](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#update-the-dependencies) — load the user from a token

### Your task

Implement `GET /auth/me` as the first protected route so the UI can learn who is logged in after refresh. It also proves `get_current_user` works before you add more APIs. Your deliverable is a secured endpoint that returns public profile fields only.

### Instructions

1. Add `GET /auth/me` on the auth router, depending on `get_current_user` (thin router; load the user in deps/service as you prefer).
2. Return public fields only via the `UserPublic` / `UserRead` schema: `id`, `email`, `display_name` (and `created_at` if useful). Leave `password_hash` out of the response.
3. Confirm the route shows as secured in `/docs` (lock icon / Authorize required). Declare the same `Security` / `Depends` scheme on the route if OpenAPI does not show it.
4. Check three cases: no `Authorization` header → 401; garbage token → 401; valid token from S2-11 → 200 with public fields only.

### Stay in scope

- Leave the profile UI and logout for S2-17.
- Leave sessions and other protected resources for Sprint 3—they will reuse this same dependency.
- Leave CORS allowlist tightening for S2-13 if the browser cannot call this yet.

### Hints

- If OpenAPI does not show security, you may need to declare the same `Security` / `Depends` scheme on the route.
- Test three cases: no header → 401; garbage token → 401; valid token → 200.

### Acceptance criteria

- [ ] Requires valid JWT
- [ ] Returns public profile fields only
- [ ] Visible as secured in OpenAPI

### Suggested paths

`backend/app/api/auth.py`, `backend/app/services/auth.py`, `backend/app/repositories/user.py`, `backend/app/schemas/auth.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-12` in the message, for example `S2-12: short summary`. Never commit `.env` or secrets.

---

## S2-13 — CORS lockdown

| Field          | Value                       |
| -------------- | --------------------------- |
| **Type**       | feature                     |
| **Week**       | 2                           |
| **Priority**   | Must                        |
| **Estimate**   | S                           |
| **Depends on** | Sprint 1 frontend URL known |

### New here: CORS (cross-origin resource sharing)

Browsers enforce the **same-origin policy**. Your Vite app (`http://localhost:5173`) and API (`http://localhost:8000`) are **different origins** (different ports). The browser will block JavaScript `fetch` unless the API responds with CORS headers that allow that frontend origin.

**FastAPI `CORSMiddleware`** sets those headers. Configure an **allowlist** from env (e.g. `CORS_ORIGINS=http://localhost:5173`) instead of `*` for credentialed or production-like apps.

Exact match matters:

- `http://localhost:5173` ≠ `http://127.0.0.1:5173`
- `http://` ≠ `https://`

With **Bearer tokens in `Authorization` headers** (not cookies), you typically need `allow_origins=[...]` and appropriate `allow_methods` / `allow_headers`. Cookie-based sessions would also need `allow_credentials=True`—not required for the JWT approach in this sprint.

**Docs & tutorials:**

- [CORS (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) — why browsers block cross-origin `fetch`
- [FastAPI — CORS](https://fastapi.tiangolo.com/tutorial/cors/) — `CORSMiddleware` allowlists
- [Same-origin policy (MDN)](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) — what “origin” means (scheme + host + port)

### Your task

Lock CORS to your documented frontend origin so Week 3 Register/Login pages can call the API from the browser. `/docs` can succeed while the SPA fails if the allowlist is wrong or too open. Your deliverable is `CORSMiddleware` driven by env/settings—not a wildcard default.

### Instructions

1. Configure `CORSMiddleware` on the FastAPI app in `backend/app/main.py` with an allowlist from settings/env (e.g. `CORS_ORIGINS`).
2. Include your Vite/dev and Compose frontend origins as needed for local work. Exact match matters: `http://localhost:5173` is not `http://127.0.0.1:5173`.
3. Allow the methods and headers the SPA needs (`POST`, `GET`, `OPTIONS`, and `Authorization` for Bearer tokens). Cookie `allow_credentials` is not required for this sprint’s JWT approach.
4. Document the env var in `.env.example`. Leave `*` out of the default setup.
5. Check your work: from the frontend origin, `fetch` register or login should succeed (you can confirm fully in S2-14 / S2-15). If it fails, open DevTools → Network and look for a failed preflight `OPTIONS`.

### Stay in scope

- Leave the Register/Login pages for S2-14 / S2-15—this ticket is the API allowlist.
- Leave cookie-based auth and `allow_credentials` for a later design if you ever switch away from Bearer tokens.
- Compose `web` URL must be the origin you allowlist, not the Docker service hostname.

### Hints

- If the UI calls fail, open DevTools → Network and look for CORS errors (often a failed preflight `OPTIONS` request).
- Compose `web` URL must be the origin you allowlist, not the Docker service hostname.

### Acceptance criteria

- [ ] Allowed origin comes from env/settings
- [ ] Arbitrary origins are not allowed in the default setup
- [ ] Frontend on that origin can call auth endpoints

### Suggested paths

`backend/app/main.py`, `.env.example`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-13` in the message, for example `S2-13: short summary`. Never commit `.env` or secrets.

---

## S2-14 — Register page

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 3            |
| **Priority**   | Must         |
| **Estimate**   | M            |
| **Depends on** | S2-10, S2-13 |

### New here: forms talking to your API

A **Register page** is a React form that collects email/password/display name and `POST`s JSON to `/auth/register`. This is your first real UI → API write path.

UX basics that save demo time:

- Disable submit while the request is in flight (prevents double accounts)
- Show API error messages (duplicate email, validation)
- Decide success behavior: navigate to Login **or** auto-login if register returns a token—document the choice

Use the shared API base URL from Sprint 1 (`VITE_API_BASE_URL`).

**Docs & tutorials:**

- [React — Controlled components](https://react.dev/reference/react-dom/components/input#controlling-an-input-with-a-state-variable) — form inputs driven by state
- [Using the Fetch API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) — `POST` JSON to your API
- [React Router — Navigating](https://reactrouter.com/start/library/navigating) — redirect after successful register
- [Vite — Env variables](https://vite.dev/guide/env-and-mode.html) — `VITE_API_BASE_URL`

### Your task

Add a `/register` page that posts to `/auth/register` so demos no longer depend on `/docs` to create a user. Graders and classmates expect a browser path. Your deliverable is a form with the fields your API requires, visible API errors, and a documented success path (navigate to Login or auto-login).

### Instructions

1. Add a `/register` route and `frontend/src/pages/RegisterPage.tsx` with the fields your API requires (email, password, display name).
2. POST JSON to `{VITE_API_BASE_URL}/auth/register` using the shared client from Sprint 1. Disable submit while the request is in flight.
3. Show field/API errors (duplicate email, 422 validation). Map structured 422 bodies to fields when you can; otherwise show a single banner.
4. On success, navigate to Login **or** auto-login if register returns a token. Write the choice down in a short comment or README note.
5. Keep basic client-side required checks (empty fields) before calling the API. Confirm the happy path in the browser: submit → success path; duplicate email → visible error.

### Stay in scope

- Leave token storage and the Login page for S2-15.
- Leave the protected layout for S2-16.
- Leave sessions, plans, and charts off this page.

### Hints

- Prefer controlled inputs.
- Map 422 validation errors to fields when the API returns a structured body; otherwise show a single alert/banner.

### Acceptance criteria

- [ ] Required fields present
- [ ] Success path continues to login or auto-login (documented)
- [ ] API errors shown to the user

### Suggested paths

`frontend/src/pages/RegisterPage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-14` in the message, for example `S2-14: short summary`. Never commit `.env` or secrets.

---

## S2-15 — Login page and token storage

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 3            |
| **Priority**   | Must         |
| **Estimate**   | M            |
| **Depends on** | S2-11, S2-13 |

### New here: SPA token storage (`localStorage`)

After login, the SPA must **remember** the JWT across page refreshes. The agreed learning approach for this course is **`localStorage`**:

- `setToken(token)` after successful login
- `getToken()` when building API requests
- `clearToken()` on logout or 401

**Centralize** these helpers and teach your API client to attach:

`Authorization: Bearer <token>`

whenever a token exists. Forgetting the header on later pages is a common Sprint 3 bug—fix the client once here.

**Security note (awareness):** `localStorage` is vulnerable to XSS if hostile scripts run on your origin. HttpOnly cookies are an alternative used in many production apps. Optional Sprint 6 can document the trade-off in `docs/security.md`; for now, localStorage is the agreed learning choice—still avoid `dangerouslySetInnerHTML` and untrusted HTML.

**Docs & tutorials:**

- [Window: localStorage (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) — `getItem` / `setItem` / `removeItem`
- [Authorization — Bearer (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Authorization) — `Authorization: Bearer <token>`
- [OWASP HTML5 Security — Local Storage](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html#local-storage) — XSS risk awareness
- [FastAPI CORS / frontend auth flow](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) — how the token is meant to be used

### Your task

Build the Login page and store the JWT in `localStorage` so the SPA stays logged in across refresh. A shared client that attaches `Authorization: Bearer <token>` prevents forgotten headers on Sprint 3 pages. Your deliverable is Login + centralized token helpers; `localStorage` is the agreed learning choice for this course.

### Instructions

1. Add `frontend/src/pages/LoginPage.tsx` that POSTs email/password to `/auth/login`.
2. On success, save the JWT with a `setToken` helper. Store only the token—leave the password out of `localStorage`.
3. Centralize get/set/clear in `frontend/src/auth/token.ts` (or equivalent).
4. Teach `frontend/src/api/client.ts` to send `Authorization: Bearer <token>` whenever a token exists.
5. Show a clear message on failed login. On success, redirect to a protected home/dashboard (S2-16 will harden the gate). Confirm: login → refresh → token still present; failed login → visible error.

### Stay in scope

- Leave the protected-route gate for S2-16.
- Leave header profile display and logout for S2-17.
- Leave HttpOnly-cookie auth for optional Sprint 6 documentation; `localStorage` is the Sprint 2 learning choice.

### Hints

- Store only the token in `localStorage`—not the password.
- After login, redirect to a protected route (S2-16 will harden the gate).

### Acceptance criteria

- [ ] Token persists across refresh
- [ ] Shared client attaches the header
- [ ] Failed login shows a clear message

### Suggested paths

`frontend/src/pages/LoginPage.tsx`, `frontend/src/auth/token.ts`, `frontend/src/api/client.ts`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-15` in the message, for example `S2-15: short summary`. Never commit `.env` or secrets.

---

## S2-16 — Protected layout

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 3       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S2-15   |

### New here: protected routes in React Router

A **protected route** (or layout) wraps pages that require login. Pattern:

1. Check for a token (and optionally validate with `GET /auth/me`)
2. If missing/invalid → `<Navigate to="/login" />`
3. If OK → render child routes (dashboard shell, etc.)

Keep **Login** and **Register** **outside** the protector—or you will create redirect loops.

When `/auth/me` returns 401: clear the token, then redirect to Login (stale tokens after secret rotation or expiry).

This pattern scales: every Sprint 3+ page can nest under the same layout.

**Docs & tutorials:**

- [React Router — Routing](https://reactrouter.com/start/library/routing) — nested routes and layouts
- [React Router — `<Navigate>`](https://reactrouter.com/api/components/Navigate) — redirect unauthenticated users to Login
- [React Router — Outlet](https://reactrouter.com/api/components/Outlet) — render child routes inside a protected layout

### Your task

Add a protected layout so unauthenticated visitors cannot open the app shell. Sprint 3 session and plan pages will nest under this same gate. Your deliverable is a `ProtectedRoute` (or layout) that redirects to Login when the token is missing or invalid, while Login and Register stay public.

### Instructions

1. Create `frontend/src/auth/ProtectedRoute.tsx` (or a layout) that checks for a token and optionally calls `GET /auth/me`.
2. If the token is missing or `/auth/me` returns 401, clear the token and `<Navigate to="/login" />`.
3. Keep `/login` and `/register` **outside** the protector so you do not create redirect loops.
4. Put at least one placeholder protected page behind the gate (home/dashboard). Show a short loading state while `/auth/me` is in flight to prevent UI flicker.
5. Check your work: open a protected URL logged out → Login; log in → the shell renders; Login/Register still load without a token.

### Stay in scope

- Leave header profile display and logout for S2-17.
- Leave session, plan, Progress, and Insights pages for later sprints—they will nest under this layout.
- Leave server-side JWT denylists for later; clearing the client token is enough here.

### Hints

- Avoid infinite redirect loops (Login must not be wrapped by the protector).
- Show a short loading state while `/auth/me` is in flight to prevent UI flicker.

### Acceptance criteria

- [ ] Unauthenticated visit to a protected route → Login
- [ ] Authenticated users can open the protected shell
- [ ] Login/Register remain public

### Suggested paths

`frontend/src/auth/ProtectedRoute.tsx`, `frontend/src/App.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-16` in the message, for example `S2-16: short summary`. Never commit `.env` or secrets.

---

## S2-17 — User display and logout

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 3            |
| **Priority**   | Must         |
| **Estimate**   | S            |
| **Depends on** | S2-12, S2-16 |

### New here: session end (logout)

**Logout** on a JWT SPA is mostly client-side: delete the stored token and send the user to Login. The server cannot “invalidate” a pure JWT until it expires unless you add a denylist (out of scope)—clearing the client token is enough for course demos.

Showing **display name or email** from `/auth/me` confirms auth works end-to-end and sets up Sprint 3’s two-user demos (log out → log in as someone else).

**Docs & tutorials:**

- [localStorage.removeItem (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Storage/removeItem) — clear the token on logout
- [React — You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) — when to fetch profile data vs derive UI from auth state
- [React Router — useNavigate](https://reactrouter.com/api/hooks/useNavigate) — send the user to Login after logout

### Your task

Show the logged-in user’s display name or email and add logout that clears the token. Seeing the profile proves the happy path; logout is required for multi-user demos in Sprint 3. Your deliverable is a header (or Settings) label plus logout that resets both `localStorage` and in-memory React state.

### Instructions

1. Fetch `GET /auth/me` when logged in and show display name or email in a shared `Header` (or Settings page) so every protected page can display it.
2. Add Logout: call `clearToken()`, reset any in-memory user state, and navigate to Login.
3. If `/auth/me` returns 401 (stale/expired token), clear the token and redirect to Login.
4. Check your work: log in → name/email visible; logout → Login, and a protected URL redirects; log in as a second user and confirm the label updates.

### Stay in scope

- Leave a server-side JWT denylist for later—clearing the client token is enough for course demos.
- Leave session history and goals for Sprint 3.
- Leave charts and AI for Sprints 4–5.

### Hints

- Put the user label in a shared `Header` so every protected page shows it.
- After logout, reset React state too, not only `localStorage`—a cached in-memory user object can keep looking logged in.

### Acceptance criteria

- [ ] Display name or email visible when logged in
- [ ] Logout clears token and returns to Login
- [ ] Stale/invalid token handled

### Suggested paths

`frontend/src/components/Header.tsx`, `frontend/src/pages/SettingsPage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-17` in the message, for example `S2-17: short summary`. Never commit `.env` or secrets.

---

## S2-18 — Auth + SQLAdmin README notes

| Field          | Value               |
| -------------- | ------------------- |
| **Type**       | docs                |
| **Week**       | 3                   |
| **Priority**   | Should              |
| **Estimate**   | S                   |
| **Depends on** | S2-07, S2-10, S2-13 |

### New here: documenting two login systems

Your README must make it obvious that **two different logins** exist:

1. **App users** — Register/Login UI → JWT → `/auth/me`
2. **SQLAdmin** — `/admin` → env username/password → browse tables

Classmates who mix them up waste lab time (“my JWT doesn’t open `/admin`”).

Also document: copy env template, run migrations + **catalog seed**, CORS origin, and a “create first app user” path. Briefly note what `/admin` should show after seed (unit types, activities, links).

**Docs & tutorials:**

- [About READMEs (GitHub Docs)](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) — what belongs in a project README
- [Make a README](https://www.makeareadme.com/) — practical structure checklist
- [12-Factor App — Config](https://12factor.net/config) — document env vars, not secrets in Git

### Your task

Extend the Sprint 1 README so a classmate can migrate, seed, open `/admin`, and create the first app user without guessing. Undocumented secrets and URLs block demos. Your deliverable is README + `.env.example` covering JWT, CORS, SQLAdmin, and the catalog seed.

### Instructions

1. Document JWT/secret, CORS origin, and SQLAdmin variables in `README.md` and `.env.example`.
2. Add a short “create first user” path (UI steps: Register → Login → profile visible).
3. Document the `/admin` URL and default admin credentials, and note that they must be changed for shared use. Spell out that a JWT will not open `/admin`.
4. Mention `alembic upgrade head` plus catalog seed (units, activities, links) if not already covered.
5. Note that SQLAdmin should show the seeded unit/activity catalog used by Sprint 3 (four units, exercise-level activities, Running → duration + distance, strength → reps/weight). Prefer a small table (URL → purpose → credentials) over a long paragraph. Link back to this sprint’s ticket intro for the demo script.

### Stay in scope

- Leave session, plan, and measurement runbooks for Sprint 3.
- Leave charts, AI, and production hardening docs for Sprints 4–6.
- Keep real secrets out of Git; placeholders belong in `.env.example`.

### Hints

- A small table (URL → purpose → credentials) beats a long paragraph.
- Link back to this sprint’s ticket intro for the demo script.

### Acceptance criteria

- [ ] JWT/secret env vars mentioned
- [ ] First-user path documented
- [ ] CORS origin env var documented
- [ ] SQLAdmin URL + login documented
- [ ] Migrations + catalog seed mentioned

### Suggested paths

`README.md`, `.env.example`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-18` in the message, for example `S2-18: short summary`. Never commit `.env` or secrets.

---

## Stretch tickets

Optional extras after Must/Should. Same ticket shape; skip them if you are out of time.

## S2-S1 — Stronger password rules

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | —       |
| **Priority**   | Stretch |
| **Estimate**   | S       |
| **Depends on** | S2-10   |

### New here: input validation beyond “non-empty”

Enforce minimum length / complexity in the Pydantic schema (and optionally on the Register page) with clear **422** messages. Example rules: min 8 characters, reject common passwords—keep rules documented so demos stay predictable.

**Docs & tutorials:**

- [Pydantic validators](https://docs.pydantic.dev/latest/concepts/validators/) — custom field/model validation
- [Pydantic — Field constraints](https://docs.pydantic.dev/latest/concepts/fields/) — `min_length`, patterns, etc.
- [OWASP Authentication — password complexity](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#implement-proper-password-strength-controls) — practical password rules

### Your task

Add documented password rules on register (schema first, UI optional) so weak passwords fail with a clear 422.

### Instructions

1. Add constraints on the register schema (e.g. `min_length=8`) in `backend/app/schemas/auth.py`.
2. Return a clear 422 message; optionally mirror the rule on the Register page.
3. Document the rules so demos stay predictable.
4. Confirm in `/docs`: too-short password → 422; a valid password still registers.

### Stay in scope

- Leave full OWASP policy packs and breach-password lists for later.
- Access-token login still uses the same hash helpers from S2-08.

### Hints

- Keep the demo password in the README compatible with your rules.

### Acceptance criteria

- [ ] Weak passwords are rejected with HTTP 422
- [ ] Rules are documented for classmates
- [ ] A valid password still registers

### Suggested paths

`backend/app/schemas/auth.py`, `frontend/src/pages/RegisterPage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-S1` in the message, for example `S2-S1: short summary`. Never commit `.env` or secrets.

---

## S2-S2 — Email normalization

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | —       |
| **Priority**   | Stretch |
| **Estimate**   | S       |
| **Depends on** | S2-10, S2-11 |

### New here: canonical emails

Store emails **lowercased**; look up case-insensitively on login so `Alex@Example.com` and `alex@example.com` are the same account. Apply normalization in one place (schema validator or service layer) so register and login never disagree.

**Docs & tutorials:**

- [Pydantic — `EmailStr`](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.EmailStr) — email validation helpers
- [Pydantic before/after validators](https://docs.pydantic.dev/latest/concepts/validators/#field-validators) — normalize on input (e.g. `.lower()`)

### Your task

Lowercase emails on register and look them up the same way on login so case variants are one account.

### Instructions

1. Normalize in one place (Pydantic validator or `services/auth.py`)—`.lower()` before persist and before lookup.
2. Use the same path for register and login so they cannot disagree.
3. Confirm: register `Alex@Example.com`, then login `alex@example.com` succeeds.

### Stay in scope

- Leave a separate “change email” flow for later.

### Hints

- Unique indexes on email should use the normalized value, or duplicates will sneak in.

### Acceptance criteria

- [ ] Stored email is lowercased
- [ ] Login is case-insensitive
- [ ] Register and login share one normalization path

### Suggested paths

`backend/app/schemas/auth.py`, `backend/app/services/auth.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-S2` in the message, for example `S2-S2: short summary`. Never commit `.env` or secrets.

---

## S2-S3 — API test: register → login → me

| Field          | Value   |
| -------------- | ------- |
| **Type**       | test    |
| **Week**       | —       |
| **Priority**   | Stretch |
| **Estimate**   | M       |
| **Depends on** | S2-10, S2-11, S2-12 |

### New here: automated API smoke tests

Add an automated test (pytest + FastAPI `TestClient`, or similar) covering register → login → `/auth/me`. This catches auth regressions before the UI demo. A fuller suite is optional in Sprint 6—one happy-path test is enough here.

**Docs & tutorials:**

- [FastAPI — Testing](https://fastapi.tiangolo.com/tutorial/testing/) — `TestClient` and dependency overrides
- [pytest documentation](https://docs.pytest.org/en/stable/) — write and run tests
- [HTTPX (used by TestClient)](https://www.python-httpx.org/) — underlying HTTP client

### Your task

Add one automated happy-path test: register → login → `GET /auth/me` with the returned token.

### Instructions

1. Add pytest (and use FastAPI `TestClient`) with a test module under `backend/`.
2. Cover register → login → `/auth/me`; assert 401 without a token.
3. Override `get_db` or point at a test database so you do not need a manual UI demo.
4. Leave a full suite and CI matrix for Sprint 6.

### Stay in scope

- One happy-path test is enough here; production hardening waits for Sprint 6.

### Hints

- Unique emails per test run (uuid suffix) avoid collisions if the DB is reused.

### Acceptance criteria

- [ ] `pytest` covers register → login → `/auth/me`
- [ ] Unauthenticated `/auth/me` fails (401)
- [ ] Test does not require clicking the UI

### Suggested paths

`backend/tests/test_auth.py`, `backend/requirements.txt`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-S3` in the message, for example `S2-S3: short summary`. Never commit `.env` or secrets.

---

## S2-S4 — Keep SQLAdmin views in sync

| Field          | Value   |
| -------------- | ------- |
| **Type**       | chore   |
| **Week**       | —       |
| **Priority**   | Stretch |
| **Estimate**   | S       |
| **Depends on** | S2-07   |

### New here: admin UI as living documentation

When you add ORM modules later (Sprint 3 sessions, plans, measurements, goals, etc.), update `/admin` `ModelView`s so demos stay useful. Keep password hashes out of detail columns. Treat SQLAdmin as part of the feature checklist, not a one-time setup.

**Docs & tutorials:**

- [SQLAdmin — ModelView configurations](https://aminalaee.dev/sqladmin/configurations/) — columns, search, exclude sensitive fields
- [SQLAdmin — Adding views](https://aminalaee.dev/sqladmin/) — register new models as you add them

### Your task

Make “update `/admin` when we add a model” a habit so later demos still have a working admin UI.

### Instructions

1. After any new ORM model, register a `ModelView` in `backend/app/admin.py`.
2. Keep `password_hash` (and similar secrets) out of list/detail columns.
3. Note the checklist in the README or a short comment next to the admin views.
4. You do not need Sprint 3 models in this sprint—wire the habit now; add those views when the tables exist.

### Stay in scope

- Leave sessions, plans, measurements, and goals for Sprint 3. This ticket is the admin habit, not those features.

### Hints

- SQLAdmin login stays env-based and separate from JWT.

### Acceptance criteria

- [ ] README or comment describes updating `/admin` when models are added
- [ ] Password hashes are not shown in admin columns
- [ ] Current Sprint 2 models remain registered

### Suggested paths

`backend/app/admin.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S2-S4` in the message, for example `S2-S4: short summary`. Never commit `.env` or secrets.

---

## Related

- Previous tickets: [sprint-01-tickets.md](sprint-01-tickets.md)
- Next tickets: [sprint-03-tickets.md](sprint-03-tickets.md)
