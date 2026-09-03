# Sprint 1 tickets — Foundation & scaffolding

Backlog for Sprint 1 ([index](../README.md)). Copy tickets into your issue tracker if you like; keep the IDs (`S1-01`, …) in branch and PR titles.

## Your task for Sprint 1

Picture a gym that is not open yet. The building is wired: lights work, the front door opens, a sign on the street says “Exercise Progress Tracker.” A visitor can walk in and see empty rooms—but there is no membership desk, no equipments (activities), and no one can train.

That is Sprint 1 on purpose. Your job is the **building**: Compose (`db` + `api` + later `web`), `GET /health`, a React placeholder, and a README so a classmate can find the light switches. Later sprints assume those switches work. If they are shaky, every later feature is harder to demo.

Leave login, the catalog, sessions, charts, and AI for later chapters—you cannot issue memberships before the doors even open. When the README demo works, you are ready to staff the front desk (Sprint 2).

### What success looks like

When you finish Sprint 1, a classmate who has never opened your repo should be able to:

1. Copy `.env.example` → `.env`
2. Run `docker compose up --build`
3. Hit the API health endpoint and get JSON back
4. Open the frontend placeholder UI in a browser

That single demo unlocks Sprint 2 (unit/activity catalog, Alembic, SQLAdmin, and JWT auth).

**Using this example repo?** The codebase already previews some Sprint 2 pieces (ORM models, seed, `/admin`). Treat those as a peek ahead—**Sprint 1 Must scope stops at the shell** (Compose, `/health`, React router, README).

### New tools & technologies

| Tool / technology                              | Role in this sprint                           |
| ---------------------------------------------- | --------------------------------------------- |
| **Git** + monorepo layout                      | One repo for `backend/`, `frontend/`, `docs/`; root `.gitignore` |
| **Python venv** + **pip** / `requirements.txt` | Isolated backend dependencies                 |
| **FastAPI** + **Uvicorn**                      | HTTP API and ASGI server                      |
| **OpenAPI** (`/docs`)                          | Interactive API explorer                      |
| **Pydantic** / **pydantic-settings**           | Request/response shapes and env config        |
| **PostgreSQL**                                 | Database (via Compose)                        |
| **Docker** + **Docker Compose**                | Run `db`, `api`, and later `web` together     |
| **React** + **TypeScript** + **Vite**          | Frontend SPA shell                            |
| **React Router**                               | Client-side routes (home placeholder)         |
| `.env` **/** `.env.example`                    | Config without committing secrets             |

See also the matching section in the [sprint index](../README.md).

### What you will learn

- Structure a full-stack **monorepo** (`backend/`, `frontend/`, `docs/`) with a root `.gitignore`
- Start a **layered** FastAPI backend (`api` → `services` → `repositories` → `models`/`db`)
- Run a minimal **FastAPI** service with **Uvicorn** and a **health** endpoint
- Configure **PostgreSQL** and the API with **Docker Compose** and `.env`
- Bootstrap a **React + TypeScript (Vite)** app that can call the API
- Write **startup docs** so teammates can follow from a clean clone

### Backend layered architecture

From Sprint 1 onward, keep backend code in clear layers. **Outer layers may call inward; inward layers must not import outward.**

```text
backend/app/
  main.py                 # composition root (wire app only)
  api/                    # presentation — routers, HTTP status, Depends
  schemas/                # Pydantic request/response DTOs
  services/               # business rules / use cases (no FastAPI imports)
  repositories/           # persistence (SQLAlchemy queries / sessions)
  models/                 # ORM entities (empty until Sprint 2)
  db/                     # infrastructure — Base, engine, SessionLocal, get_db (Sprint 2)
  core/                   # cross-cutting — settings (later: security)
  admin.py                # SQLAdmin (Sprint 2)
```

| Layer             | Responsibility                                                      |
| ----------------- | ------------------------------------------------------------------- |
| `api/`            | HTTP only — parse input, call a service, map errors to status codes |
| `schemas/`        | Pydantic DTOs for requests/responses                                |
| `services/`       | Business logic / use cases                                          |
| `repositories/`   | Database queries and `Session` usage                                |
| `models/` + `db/` | ORM entities and shared DB infrastructure                           |

Even a tiny `/health` route should follow this shape so Sprint 2+ auth and sessions do not invent a second style.

### Out of scope (intentionally later)

| Topic                                                 | When it arrives |
| ----------------------------------------------------- | --------------- |
| SQLAlchemy engine/session/Base, models, Alembic, seed | Sprint 2        |
| Unit catalog + activity↔unit links                    | Sprint 2        |
| SQLAdmin (`/admin`)                                   | Sprint 2        |
| JWT register/login UI                                 | Sprint 2        |
| Sessions, measurements, WorkoutPlans                  | Sprint 3        |
| Goals (model + API; UI optional)                      | Sprint 3        |
| Progress charts, AI insights, hardening               | Sprints 4–6     |

### Week-by-week map

| Week  | Focus                                                        | Ticket IDs    | Checkpoint                                                   |
| ----- | ------------------------------------------------------------ | ------------- | ------------------------------------------------------------ |
| **1** | Monorepo, FastAPI `/health`, env, Compose `db` + `api`       | S1-01 … S1-08 | Teammate runs Compose for Postgres + API; `/health` succeeds |
| **2** | Vite React shell, health indicator, `web` in Compose, README | S1-09 … S1-13 | Full demo from the README alone                              |

### How the tickets fit together

```text
Week 1                              Week 2
────────                            ────────
Monorepo + `.gitignore` + FastAPI + /health        Vite + React + TS
requirements                                        Router + home page
.env + settings                     API base URL / health UI
Compose: db + api                   web service + README
API reaches Postgres
```

Do **Must** tickets first, then **Should** (S1-11), then **Stretch** if you have time.

**How to read each ticket:** **New here** explains the concept and lists **Docs & tutorials**. **Your task** states the deliverable. **Instructions** walk through the work. **Stay in scope** keeps later-sprint features out of this ticket. **Commit** means create a new Git commit when the ticket is done (ticket ID in the message).

### Ticket index

| ID                                                 | Title                             | Week | Priority | Estimate |
| -------------------------------------------------- | --------------------------------- | ---- | -------- | -------- |
| [S1-01](#s1-01--create-monorepo-layout-and-root-gitignore) | Create monorepo layout and root `.gitignore` | 1    | Must     | M        |
| [S1-02](#s1-02--fastapi-app-skeleton)              | FastAPI app skeleton              | 1    | Must     | M        |
| [S1-03](#s1-03--health-endpoint)                   | Health endpoint                   | 1    | Must     | S        |
| [S1-04](#s1-04--python-dependencies)               | Python dependencies               | 1    | Must     | S        |
| [S1-06](#s1-06--env-example-and-settings)          | Env example and settings          | 1    | Must     | M        |
| [S1-07](#s1-07--docker-compose-for-db-and-api)     | Docker Compose for db and api     | 1    | Must     | L        |
| [S1-08](#s1-08--api-reaches-postgres)              | API reaches Postgres              | 1    | Must     | M        |
| [S1-09](#s1-09--vite-react-typescript-scaffold)    | Vite React TypeScript scaffold    | 2    | Must     | M        |
| [S1-10](#s1-10--router-and-placeholder-home)       | Router and placeholder home       | 2    | Must     | S        |
| [S1-11](#s1-11--api-base-url-and-health-indicator) | API base URL and health indicator | 2    | Should   | M        |
| [S1-12](#s1-12--web-service-in-compose)            | Web service in Compose            | 2    | Must     | M        |
| [S1-13](#s1-13--root-readme)                       | Root README                       | 2    | Must     | M        |
| [S1-S1](#s1-s1--db-aware-health)                   | DB-aware health                   | —    | Stretch  | S        |
| [S1-S2](#s1-s2--multi-stage-api-image)             | Multi-stage API image             | —    | Stretch  | M        |
| [S1-S3](#s1-s3--smoke-ci)                          | Smoke CI                          | —    | Stretch  | M        |

---

## S1-01 — Create monorepo layout and root `.gitignore`

| Field          | Value |
| -------------- | ----- |
| **Type**       | chore |
| **Week**       | 1     |
| **Priority**   | Must  |
| **Estimate**   | M     |
| **Depends on** | —     |

### New here: monorepo and Git ignore rules

A **monorepo** (monolithic repository) is a single Git repository that holds more than one application or package—here, the **backend API**, the **frontend UI**, and **course docs** live side by side.

Why we use it for this course:

- One clone / one PR can change API and UI together
- Shared docs and Compose file stay next to the code they describe
- You avoid “which repo has the latest frontend?” confusion
- Project management stays simpler for a small team

It is _not_ the same as putting all code in one giant folder with no structure. You still keep clear boundaries (`backend/`, `frontend/`).

Add a root **`.gitignore` in this same ticket**, before you add venvs, `node_modules`, or `.env`. That way later tickets never track junk or secrets.

Typical ignores for this project:

| Pattern                 | Why                               |
| ----------------------- | --------------------------------- |
| `.env`                  | May contain passwords and secrets |
| `.venv/`, `venv/`       | Huge, machine-specific Python env |
| `node_modules/`         | Huge, reinstallable frontend deps |
| `__pycache__/`, `*.pyc` | Python bytecode caches            |
| `dist/`, `build/`       | Build output                      |

`.env.example` is the opposite: a _safe template_ of variable _names_ (no real secrets). It **should** be committed so teammates know which keys to set. You will create the file in S1-06; the ignore rules must not exclude it.

**Docs & tutorials:**

- [What is a monorepo?](https://www.atlassian.com/git/tutorials/monorepos) — Atlassian overview of monorepo vs multi-repo
- [Git documentation](https://git-scm.com/doc) — official Git reference (clone, branch, commit)
- [gitignore documentation](https://git-scm.com/docs/gitignore) — pattern syntax
- [github/gitignore](https://github.com/github/gitignore) — community templates (Python, Node, etc.)
- [Ignoring files (GitHub Docs)](https://docs.github.com/en/get-started/git-basics/ignoring-files) — practical ignore workflow

### Your task

Set up the top-level folder layout **and** a root `.gitignore` so later tickets do not push venvs, `node_modules`, caches, or `.env`. Your deliverable is a split monorepo (`backend/`, `frontend/`, `docs/`), a one-paragraph README stub, and ignore rules that keep secrets and generated folders out of Git. S1-13 will expand the README into a full runbook.

### Instructions

1. Create top-level folders: `backend/`, `frontend/`, and `docs/`.
2. Keep sprint tickets and report templates under `docs/sprints/` (including `tickets/` and `templates/`). A different folder name or structure will break existing links in the sprint documentation.
3. Add a short note in a root `README.md` stub describing the layout (one paragraph is enough for now).
4. Add a root `.gitignore` covering `.env`, Python caches, virtualenvs, `node_modules/`, build output, and common IDE folders. Ensure `.env.example` is **not** ignored (you will create it in S1-06).
5. Create a dummy `.env`, run `git status`, and confirm it does **not** appear as a new file to commit.
6. Check that the layout matches the target in [docs/sprints/README.md](../README.md).

### Stay in scope

- Leave FastAPI, Compose, and the Vite app for later tickets this sprint.
- Leave the actual `.env.example` contents for S1-06.
- Leave JWT, SQLAdmin, sessions, and AI for later sprints.
- Do not nest the whole app inside a single `src/` at the repo root.
- If `.env` was already committed earlier, remove it from the index (`git rm --cached .env`) and rotate any secrets that leaked.

### Hints

- Keep sprint markdown under `docs/sprints/`; if you move it, update every relative link.
- Community gitignore templates (Python + Node) are a good starting point; trim what you do not need.

### Acceptance criteria

- [ ] `backend/`, `frontend/`, and `docs/sprints/` exist
- [ ] Existing sprint tickets remain under `docs/sprints/tickets/`
- [ ] Layout matches the target in [docs/sprints/README.md](../README.md)
- [ ] Ignores `.env`, Python caches/venvs, `node_modules`, dist/build, common IDE folders
- [ ] `.env.example` is not ignored
- [ ] Accidental `git status` after creating `.env` does not show secrets as new tracked files

### Suggested paths

`backend/`, `frontend/`, `docs/`, `.gitignore`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-01` in the message, for example `S1-01: short summary`. Never commit `.env` or secrets.

---

## S1-02 — FastAPI app skeleton

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 1       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S1-01   |

### New here: FastAPI, Uvicorn, and OpenAPI

**FastAPI** is a modern Python web framework for building HTTP APIs. You write Python functions, decorate them with routes (like `@app.get("/health")`), and FastAPI turns them into endpoints. It also generates interactive API docs automatically.

**Uvicorn** is an **ASGI** server—the process that actually listens on a port (e.g. `8000`) and runs your FastAPI app. Think: FastAPI = the application; Uvicorn = the engine that serves it.

**OpenAPI /** `/docs`**:** FastAPI exposes a Swagger UI at `/docs` where you can try endpoints in the browser without writing a frontend yet.

**Python package layout:** putting code under `backend/app/` with an `__init__.py` makes `app` an importable package. Uvicorn then targets `app.main:app` meaning “module `app.main`, variable named `app`”.

Create the **layered folders** early (even if some stay nearly empty until later tickets): `api/`, `schemas/`, `services/`, `repositories/`, `models/`, `db/`, `core/`. `main.py` is the composition root—it wires the app; it should not become a junk drawer of business logic.

**Docs & tutorials:**

- [FastAPI — First steps](https://fastapi.tiangolo.com/tutorial/first-steps/) — create an app and run it
- [FastAPI — Bigger applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) — routers and package layout
- [Uvicorn](https://www.uvicorn.org/) — ASGI server docs
- [OpenAPI interactive docs in FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/#interactive-api-docs-swagger-ui) — `/docs` Swagger UI

### Your task

Create a FastAPI application package with the layered folders teammates will grow into. Until `app` exists and starts, you cannot add health checks, auth, or sessions. Your deliverable is a runnable `backend/app/main.py` plus empty layered packages.

### Instructions

1. Create a Python package `backend/app/` with an empty `__init__.py`.
2. Create layered subpackages, each with `__init__.py`: `api/`, `schemas/`, `services/`, `repositories/`, `models/`, `db/`, `core/`.
3. In `main.py`, construct a `FastAPI()` instance and assign it to a variable named `app` (Uvicorn looks for that name by convention).
4. Document the run command, for example from `backend/`:

```bash
 uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

`--reload` restarts the server when you edit code (great for learning; not for production). 5. Confirm the process starts and open `http://localhost:8000/docs`. You should see the OpenAPI UI even before you add custom routes (or after a tiny root route).

### Stay in scope

- Leave `/health` for S1-03; a skeleton that boots is enough here.
- Leave SQLAlchemy, models, and SQLAdmin for Sprint 2.
- Prefer a package import path (`app.main:app`) over a loose script so Docker and local runs stay consistent.

### Hints

- If imports fail, check your **working directory** (run Uvicorn from `backend/`) and that the package name matches the folder.
- You will add a virtualenv and `requirements.txt` in S1-04; you can install FastAPI/Uvicorn temporarily first if you want to smoke-test earlier.

### Acceptance criteria

- [ ] `backend/app/main.py` (or equivalent) creates a FastAPI `app`
- [ ] Layered packages exist under `backend/app/` (`api`, `schemas`, `services`, `repositories`, `models`, `db`, `core`)
- [ ] App starts locally with a documented Uvicorn command
- [ ] Package imports without error from the backend working directory

### Suggested paths

`backend/app/main.py`, `backend/app/__init__.py`, `backend/app/api/`, `backend/app/schemas/`, `backend/app/services/`, `backend/app/repositories/`, `backend/app/models/`, `backend/app/db/`, `backend/app/core/`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-02` in the message, for example `S1-02: short summary`. Never commit `.env` or secrets.

---

## S1-03 — Health endpoint

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 1       |
| **Priority**   | Must    |
| **Estimate**   | S       |
| **Depends on** | S1-02   |

### New here: health checks and HTTP JSON APIs

A **health endpoint** is a tiny route (often `GET /health`) that answers: “Is this process up?” Orchestrators (Docker Compose, Kubernetes, cloud load balancers) and your own frontend can call it without needing business data.

**HTTP status codes** matter: `200` means OK. Later you may use `503` when a dependency is down—but for Sprint 1, keep `/health` as a simple liveness signal.

**JSON** (`{ "status": "ok" }`) is the usual response format for APIs: easy for browsers, scripts (`curl`), and React to parse. Prefer JSON over HTML for API routes.

You can define the route on `app` directly, but prefer an `APIRouter` in `api/` that calls a **service** and returns a **schema**. Even for `/health`, practice the layered flow: `api` → `services` → (later `repositories` for DB checks).

**Docs & tutorials:**

- [FastAPI — Path operation](https://fastapi.tiangolo.com/tutorial/first-steps/) — define a `GET` route that returns JSON
- [FastAPI — Response model](https://fastapi.tiangolo.com/tutorial/response-model/) — Pydantic schemas as API responses
- [HTTP response status codes (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) — what `200` / `503` mean

### Your task

Implement `GET /health` so Compose, OpenAPI, and later the frontend have a simple “is the API up?” check. Keep the route layered (`api` → `services` → schema) even though the logic is tiny—this is the pattern later sprints will reuse.

### Instructions

1. Add `backend/app/schemas/health.py` with a response model that includes `status: str`.
2. Add `backend/app/services/health.py` with a function that returns that status. Keep FastAPI out of this module so the service stays easy to call from tests later.
3. Add `backend/app/api/health.py` with an `APIRouter` and `GET /health`. Call the service and return HTTP 200 with a body such as `{ "status": "ok" }`. Use a tag like `tags=["health"]` so OpenAPI groups the endpoint.
4. Register the router in `backend/app/main.py` (`app.include_router(...)`).
5. Check your work: open `/docs` and use “Try it out”, or run:

```bash
 curl http://localhost:8000/health
```

You should see HTTP 200 and the JSON body.

### Stay in scope

- Leave database checks for the stretch ticket (S1-S1). Liveness is enough here.
- Leave JWT, sessions, and admin UI for Sprint 2.
- Avoid putting secrets, env dumps, or stack traces in the response.

### Hints

- Keep the handler tiny: parse nothing, call the service, return the schema.

### Acceptance criteria

- [ ] `GET /health` returns HTTP 200
- [ ] Response body includes a clear status (e.g. `{ "status": "ok" }`)
- [ ] Route lives in `api/`, calls a `services/` function, and uses a `schemas/` response model
- [ ] Endpoint is visible in OpenAPI (`/docs`)

### Suggested paths

`backend/app/api/health.py`, `backend/app/services/health.py`, `backend/app/schemas/health.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-03` in the message, for example `S1-03: short summary`. Never commit `.env` or secrets.

---

## S1-04 — Python dependencies

| Field          | Value |
| -------------- | ----- |
| **Type**       | chore |
| **Week**       | 1     |
| **Priority**   | Must  |
| **Estimate**   | S     |
| **Depends on** | S1-02 |

### New here: virtual environments and `requirements.txt`

A **virtual environment** (venv) is an isolated Python installation for _this_ project. It prevents “I installed package X globally and broke another course project.”

`requirements.txt` lists third-party packages and (ideally) versions, for example:

```text
fastapi==0.115.6
uvicorn[standard]==0.34.0
pydantic-settings==2.7.1
```

Classmates (and Docker) run `pip install -r requirements.txt` and get the same libraries.

`uvicorn[standard]`**:** the `[standard]` extra installs optional speed/reload-related dependencies. Prefer it for local development.

**Pinning versions** (`==`) makes demos reproducible. Leaving versions open (`fastapi`) can pull breaking upgrades unexpectedly.

Sprint 2 will add more packages (SQLAlchemy, SQLAdmin, JWT libs). For Sprint 1 Must scope, FastAPI + Uvicorn (+ pydantic-settings if you use it in S1-06) is enough. Optional: add SQLAlchemy/psycopg early only if you tackle stretch S1-S1.

**Docs & tutorials:**

- [Python venv tutorial](https://docs.python.org/3/tutorial/venv.html) — create and activate a virtual environment
- [pip requirements files](https://pip.pypa.io/en/stable/user_guide/#requirements-files) — `requirements.txt` format and install
- [Installing packages (Python Packaging User Guide)](https://packaging.python.org/en/latest/tutorials/installing-packages/) — broader packaging intro

### Your task

Give classmates (and Docker) a reproducible Python environment. Your deliverable is `backend/requirements.txt` plus documented venv install steps that work on a clean machine.

### Instructions

1. Add `backend/requirements.txt` listing at least `fastapi` and `uvicorn[standard]` (and `pydantic-settings` if you plan to use it in S1-06). Pin versions with `==` where you can.
2. Create a venv and document the workflow:

```bash
 cd backend
 python -m venv .venv
 # Windows PowerShell:
 .\.venv\Scripts\Activate.ps1
 pip install -r requirements.txt
```

3. From a **fresh** venv, install and run `uvicorn app.main:app`. Confirm the app still starts.

### Stay in scope

- Leave SQLAlchemy, Alembic, SQLAdmin, and JWT libraries for Sprint 2 unless you are doing stretch S1-S1.
- Never commit `.venv/` (ignored from S1-01).

### Hints

- If `pip` is slow or blocked, check you activated the venv (your prompt usually shows `(.venv)`).

### Acceptance criteria

- [ ] Dependency file includes FastAPI and Uvicorn (and pydantic-settings if you use it)
- [ ] Fresh install instructions are documented
- [ ] Install + run works on a clean virtual environment

### Suggested paths

`backend/requirements.txt`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-04` in the message, for example `S1-04: short summary`. Never commit `.env` or secrets.

---

## S1-06 — Env example and settings

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 1            |
| **Priority**   | Must         |
| **Estimate**   | M            |
| **Depends on** | S1-02        |

### New here: environment variables and settings objects

**Environment variables** are configuration values supplied _outside_ your source code—by a `.env` file locally, or by Docker Compose in containers. Examples: database password, port numbers, allowed frontend origin.

`.env` **vs** `.env.example`**:**

- `.env` — your real local values (gitignored)
- `.env.example` — committed template with placeholders (`POSTGRES_PASSWORD=changeme`) so others know what to fill in

`pydantic-settings` (optional but recommended) is a library that loads env vars into a typed Python class (`Settings`). Benefits: one place to read config, defaults, and validation—instead of scattering `os.getenv` calls.

Example shape:

```python
class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://..."
    api_port: int = 8000
```

`DATABASE_URL` in the environment maps to `database_url` automatically (case-insensitive).

**CORS_ORIGINS** can be a placeholder now. A minimal allowlist for the Vite origin (e.g. `http://localhost:5173`) is useful so Week 2’s health fetch works; Sprint 2 locks CORS down for auth.

**Docs & tutorials:**

- [The Twelve-Factor App — Config](https://12factor.net/config) — why config belongs in the environment
- [FastAPI — Settings and environment variables](https://fastapi.tiangolo.com/advanced/settings/) — settings pattern for FastAPI
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — typed settings from env / `.env`

### Your task

Move configuration out of source code so the same app can run on a laptop and in Compose. Your deliverable is a committed `.env.example`, a gitignored local `.env`, and a settings module the API can read.

### Instructions

1. Create `.env.example` with placeholders such as `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DATABASE_URL`, `API_HOST`, `API_PORT`, and optionally `CORS_ORIGINS`.
2. Add a settings module (recommended: pydantic-settings in `backend/app/core/config.py`) that reads these values. A documented `os.getenv` approach is acceptable if your team prefers simpler code for now.
3. Copy `.env.example` → `.env` locally and fill in safe demo values. Confirm `.env` stays untracked (`git status`). Ignore rules for `.env` come from S1-01; `.env.example` must remain tracked.
4. Document which variables the API actually reads today vs placeholders for later sprints.

### Stay in scope

- **SQLAdmin** credentials (`SQLADMIN_`\*) belong in Sprint 2—omit them unless you are browsing the example repo and need the preview to start.
- Leave JWT secrets for Sprint 2.
- Inside Compose (next tickets), the hostname for Postgres is usually the **service name** (`db`), not `localhost`.

### Hints

- Hard-coded database URLs break as soon as you move from laptop to Docker; keep all of that in env.

### Acceptance criteria

- [ ] `.env.example` lists the placeholders above (or equivalent)
- [ ] Backend loads settings from the environment (or documented getenv usage)
- [ ] No real credentials are committed

### Suggested paths

`.env.example`, `backend/app/core/config.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-06` in the message, for example `S1-06: short summary`. Never commit `.env` or secrets.

---

## S1-07 — Docker Compose for db and api

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 1            |
| **Priority**   | Must         |
| **Estimate**   | L            |
| **Depends on** | S1-04, S1-06 |

### New here: Docker, images, containers, and Compose

**Docker** packages an app and its runtime into an **image**. A running instance of an image is a **container**.

**Docker Compose** is a tool that starts _multiple_ containers from one `docker-compose.yml` file—perfect for “API + database” projects. One command (`docker compose up --build`) replaces “open three terminals and hope ports match.”

In this sprint you typically define:

| Service | Role                                                 |
| ------- | ---------------------------------------------------- |
| `db`    | Official **PostgreSQL** image (your database server) |
| `api`   | Your FastAPI app built from `backend/Dockerfile`     |

**Dockerfile** (for the API): a recipe—base image (e.g. `python:3.12-slim`), `pip install -r requirements.txt`, copy code, run Uvicorn.

**Volumes:** Postgres should use a **named volume** so data survives `docker compose down` (without `-v`). Without a volume, wiping containers can wipe the database.

**Ports:** `ports: ["8000:8000"]` means “host port 8000 → container port 8000.” Your browser on Windows talks to the _host_ port.

**Docs & tutorials:**

- [Docker Get Started](https://docs.docker.com/get-started/) — images, containers, and the basics
- [Docker Compose overview](https://docs.docker.com/compose/) — multi-container apps from one file
- [Compose quickstart](https://docs.docker.com/compose/gettingstarted/) — first `compose.yaml` walkthrough
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) — `FROM`, `COPY`, `RUN`, `CMD`
- [Official PostgreSQL image](https://hub.docker.com/_/postgres) — env vars (`POSTGRES_USER`, etc.) and volumes

### Your task

Define a Compose stack so the team starts Postgres and the API with one command. This is also how graders and classmates will run your project later. Your deliverable is `docker-compose.yml` plus `backend/Dockerfile` that bring up `db` and `api`.

### Instructions

1. Write `docker-compose.yml` with services `db` (official Postgres image) and `api` (build from `backend/Dockerfile`).
2. Write a simple Dockerfile: install `requirements.txt`, copy `app/`, `CMD` Uvicorn on `0.0.0.0` (port 8000).
3. Pass env vars into `api` from `.env` / Compose `environment` (especially `DATABASE_URL`—finalize hostname in S1-08).
4. Map ports (e.g. `5432` for Postgres, `8000` for API) and use a named volume for Postgres data.
5. Run `docker compose up --build` and confirm both containers stay up (`docker compose ps`).

### Stay in scope

- Leave the `web` frontend service for S1-12.
- Leave Alembic, seed, and SQLAdmin for Sprint 2.
- First builds can be slow (downloading base images)—that is normal.

### Hints

- Align `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` on `db` with whatever you put in `DATABASE_URL`.

### Acceptance criteria

- [ ] Compose defines `db` and `api`
- [ ] API image/build is defined
- [ ] `docker compose up --build` starts both without manual wiring
- [ ] Published ports are documented in the README (or a stub you will finish in S1-13)

### Suggested paths

`docker-compose.yml`, `backend/Dockerfile`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-07` in the message, for example `S1-07: short summary`. Never commit `.env` or secrets.

---

## S1-08 — API reaches Postgres

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 1       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S1-07   |

### New here: Docker networking and `localhost` traps

Containers on the same Compose project share a **private network**. Each service is reachable by its **service name** as a hostname.

| Where you run code                   | How to reach Postgres                             |
| ------------------------------------ | ------------------------------------------------- |
| On your Windows host (local Uvicorn) | `localhost:5432` (published port)                 |
| Inside the `api` container           | hostname `db` (Compose service name), port `5432` |

**Classic bug:** setting `DATABASE_URL=...@localhost:5432/...` _inside_ the API container. There, `localhost` means the API container itself—not Postgres—so connections fail.

**Healthchecks /** `depends_on`**:** Compose can wait until Postgres accepts connections (`pg_isready`) before starting (or marking ready) the API. That avoids “API crashed because DB was still booting.”

You do **not** need full ORM models, `SessionLocal`, or Alembic yet—only a correct connection string and startup ordering. Engine/session/Base, models, migrations, seed, and SQLAdmin arrive in Sprint 2 (start with S2-01).

**Docs & tutorials:**

- [Compose networking](https://docs.docker.com/compose/how-tos/networking/) — service names as hostnames
- [Control startup order](https://docs.docker.com/compose/how-tos/startup-order/) — `depends_on` and healthchecks
- [Compose](https://docs.docker.com/reference/compose-file/services/#healthcheck) `healthcheck` — `pg_isready` style probes

### Your task

Make the Compose `api` service able to resolve and wait for Postgres. Wrong hostnames waste hours later; fix connectivity now so Sprint 2 migrations talk to the real database on day one.

### Instructions

1. Set `DATABASE_URL` for the **Compose** `api` **service** to use hostname `db` (or your Compose service name), not `localhost`.
2. Add a Postgres healthcheck (`pg_isready`) and/or `depends_on` with condition, or retry logic on API startup.
3. Confirm the API still serves `/health` when started via Compose (`http://localhost:8000/health` from the host).
4. Optionally: `docker compose exec api ping db` (or open a shell) and verify DNS resolves `db`.

### Stay in scope

- Leave ORM engine/`SessionLocal`, models, and Alembic for Sprint 2.
- Local Uvicorn (not in Docker) should keep using `localhost` in _your_ `.env`—Compose overrides for the container.

### Hints

- Keep username/password/db name aligned between the `db` service env and `DATABASE_URL`.

### Acceptance criteria

- [ ] Connection string uses the Compose service hostname inside `api`
- [ ] API starts after DB is ready (healthcheck/`depends_on` or retry)
- [ ] `/health` returns 200 when the stack is up via Compose

### Suggested paths

`docker-compose.yml`, `backend/app/core/config.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-08` in the message, for example `S1-08: short summary`. Never commit `.env` or secrets.

---

## S1-09 — Vite React TypeScript scaffold

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 2       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S1-01   |

### New here: React, TypeScript, Vite, and Node tooling

**React** is a library for building user interfaces from components (functions that return UI). You will use it for Login, session logging, plans, progress charts, and more in later sprints.

**TypeScript** adds static types to JavaScript (`string`, `number`, interfaces). It catches many bugs before the browser runs your code—especially helpful in a team.

**Vite** is a frontend build tool and **dev server**. It starts fast and hot-reloads when you edit files. The official `react-ts` template gives you a ready React + TypeScript project.

**Node.js / npm:** frontend packages live in `package.json`. `npm install` downloads them into `node_modules/` (gitignored). `npm run dev` starts Vite.

Optional later (already used in the example solution, not required by this ticket): **Tailwind CSS** and **shadcn/ui** for styling/components. You may adopt them now or keep the template CSS until you prefer otherwise.

**Docs & tutorials:**

- [React — Learn](https://react.dev/learn) — components, props, state (start here)
- [TypeScript for the New Programmer](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html) — TS basics
- [Vite — Getting Started](https://vite.dev/guide/) — scaffold and `npm run dev`
- [npm docs —](https://docs.npmjs.com/cli/v10/configuring-npm/package-json) `package.json` — scripts and dependencies
- [Tailwind CSS (optional)](https://tailwindcss.com/docs/installation/using-vite) — if you add utility CSS
- [shadcn/ui (optional)](https://ui.shadcn.com/docs/installation/vite) — if you follow the example UI stack

### Your task

Scaffold a modern React + TypeScript frontend so later sprints add pages instead of fighting tooling. Your deliverable is a working Vite app under `frontend/` with install and `dev` scripts.

### Instructions

1. Scaffold into `frontend/` with the official Vite React-TS template, for example:

```bash
 npm create vite@latest frontend -- --template react-ts
```

(Command spelling can vary slightly by npm/create-vite version—use the React + TypeScript template.) 2. Run `npm install` and `npm run dev`; open the printed localhost URL. 3. Commit `package.json`, lockfile (`package-lock.json` / etc.), and TS/Vite config; do **not** commit `node_modules`.

### Stay in scope

- Leave React Router wiring for S1-10.
- Leave Login, sessions, and charts for later sprints.
- Choose `npm` vs `pnpm` vs `yarn` and stick to one lockfile.

### Hints

- If `frontend/` already had a placeholder README, replace or merge carefully.

### Acceptance criteria

- [ ] `frontend/` is a working Vite + React + TS project
- [ ] Install and `dev` scripts succeed
- [ ] TypeScript is enabled (not a plain JS-only scaffold)

### Suggested paths

`frontend/package.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-09` in the message, for example `S1-09: short summary`. Never commit `.env` or secrets.

---

## S1-10 — Router and placeholder home

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 2       |
| **Priority**   | Must    |
| **Estimate**   | S       |
| **Depends on** | S1-09   |

### New here: client-side routing (React Router)

A **Single Page Application (SPA)** does not load a new HTML document for every screen. Instead, **React Router** swaps components when the URL changes (`/`, `/login`, `/sessions`, …).

Benefits for this course:

- Later sprints add pages without reinventing navigation
- You can protect routes (Sprint 2) by wrapping them in a “must be logged in” layout
- URLs remain shareable and bookmarkable

Basic idea:

```tsx
<BrowserRouter>
  <Routes>
    <Route path="/" element={<HomePage />} />
  </Routes>
</BrowserRouter>
```

**Docs & tutorials:**

- [React Router — Routing](https://reactrouter.com/start/library/routing) — `BrowserRouter`, `Routes`, `Route`
- [React Router — Installation](https://reactrouter.com/start/library/installation) — add the library to a Vite app
- [MDN — SPAs and client-side routing](https://developer.mozilla.org/en-US/docs/Glossary/SPA) — what an SPA is

### Your task

Wire React Router and a simple home page so later sprints add Login, sessions, plans, Progress, and Insights without rewriting navigation. Your deliverable is a `/` route that renders a Sprint 1 placeholder—not the default Vite counter as the only screen.

### Instructions

1. Install React Router (`react-router-dom`) and wrap your app with `BrowserRouter` in `frontend/src/main.tsx` or `App.tsx`.
2. Create `frontend/src/pages/HomePage.tsx` with the app name and short “Sprint 1 placeholder” text.
3. Add a `Route` for `/` that renders `HomePage`. Replace or wrap the default Vite counter demo.

### Stay in scope

- Leave Login, protected layouts, and session pages for Sprint 2–3.
- Keep routing in `App.tsx` or a small `routes.tsx`—you will expand it later.

### Hints

- A `pages/` folder scales better than dumping everything in `App.tsx`.

### Acceptance criteria

- [ ] React Router is installed and wired
- [ ] Home route renders a simple placeholder
- [ ] Default Vite counter is not left as the only screen

### Suggested paths

`frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/pages/HomePage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-10` in the message, for example `S1-10: short summary`. Never commit `.env` or secrets.

---

## S1-11 — API base URL and health indicator

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 2            |
| **Priority**   | Should       |
| **Estimate**   | M            |
| **Depends on** | S1-03, S1-10 |

### New here: browser calls to your API, Vite env, and CORS (preview)

Your React app runs in the **browser**. To talk to FastAPI it uses `fetch` (or similar) to an absolute URL like `http://localhost:8000/health`.

`VITE_API_BASE_URL`**:** Vite only exposes env vars prefixed with `VITE_` to client code. You read them via `import.meta.env.VITE_API_BASE_URL`. That lets Docker/dev/prod change the API location without editing components.

**CORS (preview):** browsers block frontend-origin requests to another origin unless the API sends permission headers. Prefer a **minimal** CORS allowlist for your Vite origin in Sprint 1 so the health indicator works. Sprint 2 hardens CORS for authenticated calls. If the health call still fails with a CORS error, document it clearly—but aim to unblock the demo.

**Host vs container:** the browser always uses a URL reachable from your machine (often `http://localhost:8000`), even when the API runs inside Docker. Container-to-container hostnames like `db` are _not_ what the browser should call.

**Docs & tutorials:**

- [Vite — Env variables and modes](https://vite.dev/guide/env-and-mode.html) — `VITE_*` and `import.meta.env`
- [Using the Fetch API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) — browser HTTP calls
- [CORS (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) — why the browser blocks cross-origin requests
- [FastAPI — CORS](https://fastapi.tiangolo.com/tutorial/cors/) — `CORSMiddleware` on the API

### Your task

Prove frontend ↔ backend connectivity with a shared API base URL and a health indicator on the home page. Hard-coding `http://localhost:8000` in every component becomes painful; one client module now will serve Login and session pages later.

### Instructions

1. Add `VITE_API_BASE_URL` to `frontend/.env.example` (and a local `frontend/.env`). Typical value: `http://localhost:8000`.
2. Create `frontend/src/api/client.ts` that prefixes that base URL for requests.
3. On the home page, call `GET /health` and show OK / failed.
4. On the API, add a **minimal** CORS allowlist for the Vite origin (e.g. `http://localhost:5173`) if the browser blocks the call. Sprint 2 will lock CORS down further for auth.

### Stay in scope

- Leave JWT headers and login forms for Sprint 2.
- Do not use Compose service names (`api`, `db`) as the browser’s API URL.

### Hints

- Prefer one shared client module over copy-pasting `fetch` URLs.
- Showing the configured base URL on the page during Sprint 1 helps demos and debugging.

### Acceptance criteria

- [ ] API base URL is documented in an env example
- [ ] Frontend can call `GET /health` using that base URL (or documents a CORS blocker clearly)
- [ ] Home page shows health success/failure, or a clear temporary note plus a ready fetch helper

### Suggested paths

`frontend/.env.example`, `frontend/src/api/client.ts`, `frontend/src/pages/HomePage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-11` in the message, for example `S1-11: short summary`. Never commit `.env` or secrets.

---

## S1-12 — Web service in Compose

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | 2            |
| **Priority**   | Must         |
| **Estimate**   | M            |
| **Depends on** | S1-07, S1-09 |

### New here: frontend as a Compose service

Until now you may run Vite with `npm run dev` on the host. Adding a `web` **service** means Compose also starts the frontend—so `docker compose up` brings up **db + api + web** together.

Two common approaches:

| Approach                           | Pros                         | Cons                      |
| ---------------------------------- | ---------------------------- | ------------------------- |
| Vite **dev server** in Docker      | Hot reload, simple for class | Heavier; not “production” |
| **Build** static files + **nginx** | Closer to production         | Rebuild to see UI changes |

For learning, the Vite dev server in Compose is usually enough (recommended by default)—**pick one approach and document it**.

Bind mounts (mapping `./frontend` into the container) can enable live edit; `node_modules` is often kept in an anonymous volume so host/container installs do not clash.

**Docs & tutorials:**

- [Compose — Use volumes / bind mounts](https://docs.docker.com/compose/how-tos/use-volumes/) — live-edit source from the host
- [Vite — Deploying a static site](https://vite.dev/guide/static-deploy.html) — if you choose build + nginx later
- [Official nginx image](https://hub.docker.com/_/nginx) — serving built frontend assets (optional path)

### Your task

Add the frontend to Compose so graders start the whole stack with one command—not three terminals with undocumented ports. Your deliverable is a `web` service plus a documented URL that loads in the browser.

### Instructions

1. Add a `web` service: Vite dev server **or** static nginx—choose one and document it in the README.
2. Publish the frontend port (e.g. `5173` or `80`).
3. Ensure `VITE_API_BASE_URL` still points at a URL the **browser** can reach (typically `http://localhost:8000`).
4. Run `docker compose up --build` and confirm `db`, `api`, and `web` start, and the UI loads in a browser.

### Stay in scope

- Leave production hardening and CI for optional Sprint 6 (or stretch S1-S2 / S1-S3).
- If the UI loads but API calls fail, finish S1-11 (base URL + CORS) rather than adding extra services.

### Hints

- On OneDrive-synced folders, Docker file watching can be flaky—see root README troubleshooting if builds misbehave.

### Acceptance criteria

- [ ] Compose includes `web`
- [ ] Browser can open the documented frontend URL
- [ ] Compose starts `db`, `api`, and `web`

### Suggested paths

`docker-compose.yml`, `frontend/Dockerfile` (if needed)

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-12` in the message, for example `S1-12: short summary`. Never commit `.env` or secrets.

---

## S1-13 — Root README

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | docs         |
| **Week**       | 2            |
| **Priority**   | Must         |
| **Estimate**   | M            |
| **Depends on** | S1-07, S1-12 |

### New here: README as the product entrypoint

A good **README** is not marketing fluff—it is the **runbook** for humans. For this course it should answer:

1. What is this project?
2. What must I install?
3. Exact commands to start it
4. Which URLs to open
5. What to try if it fails

Treat the README as part of the demo. If a classmate cannot start the app from it alone, the sprint is not done.

- [About READMEs (GitHub Docs)](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) — what belongs in a README
- [Make a README](https://www.makeareadme.com/) — practical structure checklist
- [Awesome README](https://github.com/matiassingers/awesome-readme) — examples of clear project READMEs

### Your task

Write the runbook for Sprint 1: prerequisites, env, Compose, URLs, and short troubleshooting. Your README is the demo script—undocumented ports and missing `.env` steps waste lab time.

### Instructions

1. List prerequisites (Docker; Node/Python if you support non-Compose workflows).
2. Document: copy `.env.example` → `.env`, `docker compose up --build`, and URLs for API, `/docs`, `/health`, and frontend.
3. Add short troubleshooting (port in use, Postgres not ready, forgotten `.env`).
4. Link to [docs/sprints/README.md](../README.md).
5. Prefer a small table of services → URLs over a long paragraph. Keep commands copy-pasteable for Windows PowerShell.

### Stay in scope

- Scope the README to **Sprint 1**: Compose + health + frontend is enough.
- Leave `/admin`, JWT auth, and the unit catalog for Sprint 2 docs (a “coming next” note is fine).

### Hints

- Note macOS/Linux differences only if your team needs them.

### Acceptance criteria

- [ ] Prerequisites listed
- [ ] Env + Compose + URL steps are clear
- [ ] Troubleshooting hints included
- [ ] Link to the sprint index
- [ ] README does not treat SQLAdmin / JWT as Sprint 1 Must requirements

### Suggested paths

`README.md`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-13` in the message, for example `S1-13: short summary`. Never commit `.env` or secrets.

---

## Stretch tickets

Optional extras after Must/Should. Same ticket shape; skip them if you are out of time.

## S1-S1 — DB-aware health

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | —       |
| **Priority**   | Stretch |
| **Estimate**   | S       |
| **Depends on** | S1-03, S1-08 |

### New here: liveness vs readiness (lightly)

`/health` often means “process is up” (**liveness**). `/health/db` asks “can we reach Postgres?” (closer to **readiness**). Showing both helps demos: API up but DB down is a different failure mode.

**Docs & tutorials:**

- [Configure Liveness, Readiness and Startup Probes (Kubernetes)](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) — liveness vs readiness concepts
- [SQLAlchemy — Working with Engines and Connections](https://docs.sqlalchemy.org/en/20/core/connections.html) — `text("SELECT 1")` style ping
- [psycopg 3 — Basic module usage](https://www.psycopg.org/psycopg3/docs/basic/usage.html) — PostgreSQL driver used with SQLAlchemy

### Your task

Extend `/health` or add `/health/db` that pings Postgres and reports connected / not connected. Put the ping in a repository so the router stays thin.

### Instructions

1. Add `backend/app/repositories/health.py` with a `text("SELECT 1")` (or equivalent) ping.
2. Orchestrate in `backend/app/services/health.py`; keep FastAPI out of the service/repository.
3. Expose the result from `backend/app/api/health.py` (extend `/health` or add `/health/db`).
4. You may add `sqlalchemy` + `psycopg` for this stretch only.
5. Check both paths: DB up → connected; stop Postgres → a clear not-connected / 503-style signal.

### Stay in scope

- Leave full ORM models, Alembic, seed, and SQLAdmin for Sprint 2.
- Leave JWT and sessions for later sprints.

### Hints

- A failed ping should not take down the Uvicorn worker—catch the error and report status.

### Acceptance criteria

- [ ] Endpoint reports whether Postgres is reachable
- [ ] Ping lives in `repositories/`; router stays thin
- [ ] API process stays up when the database is down

### Suggested paths

`backend/app/api/health.py`, `backend/app/services/health.py`, `backend/app/repositories/health.py`, `backend/app/schemas/health.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-S1` in the message, for example `S1-S1: short summary`. Never commit `.env` or secrets.

---

## S1-S2 — Multi-stage API image

| Field          | Value   |
| -------------- | ------- |
| **Type**       | chore   |
| **Week**       | —       |
| **Priority**   | Stretch |
| **Estimate**   | M       |
| **Depends on** | S1-07   |

### New here: multi-stage builds

A **multi-stage Dockerfile** uses one stage to install/build and a smaller final stage to run. That shrinks images and keeps compilers/caches out of production layers.

**Docs & tutorials:**

- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/) — official Docker guide
- [Best practices for writing Dockerfiles](https://docs.docker.com/build/building/best-practices/) — leaner images

### Your task

Use a multi-stage Dockerfile to keep the runtime image smaller: install in a builder stage, copy into a slim runtime stage. Compose must still serve `/health`.

### Instructions

1. Update `backend/Dockerfile` with a builder stage that `pip install`s into a venv.
2. Copy only the venv + app into a slim runtime stage; run Uvicorn there.
3. Confirm `docker compose up --build` still serves `/health`.

### Stay in scope

- Leave production cloud deploy notes for optional Sprint 6.
- Leave the frontend image as you already chose in S1-12.

### Hints

- A `.dockerignore` (venv, `__pycache__`, `.git`) keeps builds faster.

### Acceptance criteria

- [ ] Dockerfile has at least two stages
- [ ] Runtime image does not include the full build toolchain
- [ ] `docker compose up --build` still serves `/health`

### Suggested paths

`backend/Dockerfile`, `backend/.dockerignore`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-S2` in the message, for example `S1-S2: short summary`. Never commit `.env` or secrets.

---

## S1-S3 — Smoke CI

| Field          | Value   |
| -------------- | ------- |
| **Type**       | chore   |
| **Week**       | —       |
| **Priority**   | Stretch |
| **Estimate**   | M       |
| **Depends on** | S1-04   |

### New here: continuous integration (smoke level)

**CI** runs automated checks on every push/PR. A minimal “smoke” job installs backend deps and imports `app.main:app` so a broken import fails before demo day.

**Docs & tutorials:**

- [Understanding GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions) — workflows, jobs, runners
- [GitHub Actions quickstart](https://docs.github.com/en/actions/writing-workflows/quickstart) — first workflow YAML
- [Building and testing Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python) — install deps and run checks in CI

### Your task

Add a simple CI workflow (GitHub Actions or similar) that installs backend deps and imports the app on each push/PR. Keep it a smoke check, not a full test suite.

### Instructions

1. Add a workflow YAML that checks out the repo.
2. Install `backend/requirements.txt` and import `app.main:app`.
3. Run on push/PR.

### Stay in scope

- Leave a full API/UI harness for optional Sprint 6.
- Do not require Docker-in-CI unless you already have it working locally.

### Hints

- Set the working directory to `backend/` so `app.main` imports cleanly.

### Acceptance criteria

- [ ] Workflow file exists and runs on push/PR
- [ ] A broken import fails the job
- [ ] Job is documented in the README (one line is enough)

### Suggested paths

`.github/workflows/smoke.yml`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S1-S3` in the message, for example `S1-S3: short summary`. Never commit `.env` or secrets.

---

## Related

- Index: [../README.md](../README.md)
- Next tickets: [sprint-02-tickets.md](sprint-02-tickets.md) (unit catalog, Alembic, **SQLAdmin**, JWT auth)
