# Sprint 1 report — Foundation

Copy this file to `docs/reports/sprint-01.md` in **your** repo and fill the blanks. Keep it a process log: no pasted source, no secrets, no `.env` values.

| Field        | Your answer |
| ------------ | ----------- |
| **Dates**    |             |
| **Names**    |             |
| **Repo URL** |             |
| **Branch**   |  Master     |

Tickets: [sprint-01-tickets.md](../tickets/sprint-01-tickets.md) · Index: [../README.md](../README.md)

## Sprint goal

From the tickets: ship a runnable skeleton so later sprints can focus on features. You are done when Compose starts `db`, `api`, and `web`; `GET /health` returns JSON; the frontend opens; the README covers clone → `.env` → Compose → URLs.

In your words (2–3 sentences): did you meet that, and what is still rough?

## Tickets

For **each** ticket fill **Status** and **PR / commit**.

Fill **Demonstration** only where this template includes that section. Follow the numbered steps exactly. Store images under `docs/reports/images/sprint-01/` using the suggested filename. Crop secrets.

For **every** ticket: set **Used AI?** to `Yes` or `No`. Write the sprint-level **AI usage** reflection at the end of this report (not under each ticket).

Skip stretch tickets you did not do. Stretch: Status, PR, and Used AI? for each stretch you did; add a Demonstration only where listed below.

### S1-01 — Create monorepo layout and root `.gitignore` (Must)

- **Status:** Done
- **commit:** S1-01: Monorepo layout + .gitignore
- **Used AI?** No

### S1-02 — FastAPI app skeleton (Must)

- **Status:** Done
- **commit:** S1-02: FastAPI app skeleton
- **Demonstration:**
  1. **Do this:** From `backend/`, start Uvicorn (`uvicorn app.main:app --reload` or your documented command). Open `http://localhost:8000/docs` in a browser.
  2. **Capture:** Screenshot of the OpenAPI / Swagger UI page.
  3. **Must show:** The `/docs` page loaded (title or Swagger chrome visible) and that the API is reachable (page is not a connection error).
  4. **Must not show:** `.env` contents, database passwords, or unrelated desktop clutter with secrets.
  5. **Save as:** `docs/reports/images/sprint-01/s1-02-docs.png`
  6. **Caption (1–2 sentences):** Terminal komento käytetty uvicorn starttaamiseen:  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
- **Used AI?**  No

### S1-03 — Health endpoint (Must)

- **Status:** Done
- **commit:** S1-03: Health endpoint
- **Demonstration:**
  1. **Do this:** With the API running, open `http://localhost:8000/health` in the browser, or use Try it out on `GET /health` in `/docs`.
  2. **Capture:** Screenshot of the JSON response (browser or `/docs` response panel).
  3. **Must show:** HTTP success and a JSON body for `/health` (fields as in your ticket acceptance criteria, for example status).
  4. **Must not show:** Stack traces, env dumps, or secrets.
  5. **Save as:** `docs/reports/images/sprint-01/s1-03-health.png`
  6. **Caption (1–2 sentences):** Toimiva API health-check
- **Used AI?** No

### S1-04 — Python dependencies (Must)

- **Status:** Done
- **commit:** S1-04: Python dependencies
- **Used AI?** No

### S1-06 — Env example and settings (Must)

- **Status:** Done
- **commit:** S1-06: Env example and settings
- **Used AI?** No

### S1-07: Docker Compose for db and api (Must)

- **Status:** Done
- **commit:** S1-07 — Docker Compose for db and api
- **Demonstration:**
  1. **Do this:** From the repo root, run `docker compose up --build` (or your documented equivalent). Wait until services settle. Run `docker compose ps` (or show the Docker Desktop containers view).
  2. **Capture:** Screenshot of the terminal `ps` output or Docker UI listing services.
  3. **Must show:** Both `db` and `api` listed as running / healthy (or equivalent status for your Compose file).
  4. **Must not show:** Full `.env` values, Postgres passwords in clear text, or cloud credentials.
  5. **Save as:** `docs/reports/images/sprint-01/s1-07-compose-db-api.png`
  6. **Caption (1–2 sentences):** Docker Desktop näkymä pyörivistä konteista.
- **Used AI?** Yes. 

### S1-08 — API reaches Postgres (Must)

- **Status:** Done
- **commit:** S1-08: API reaches Postgres
- **Demonstration:**
  1. **Do this:** With Compose up, open API logs (`docker compose logs api`) and/or hit a healthcheck that talks to Postgres if you already have one. Confirm the connection string host inside Compose is the service name `db`, not `localhost`.
  2. **Capture:** Screenshot of logs or health output that proves the API reached Postgres.
  3. **Must show:** Evidence the API talks to host `db` (successful connect message, healthcheck pass, or equivalent)—not a connection refused to the wrong host.
  4. **Must not show:** Full `DATABASE_URL` with real passwords; redact credentials.
  5. **Save as:** `docs/reports/images/sprint-01/s1-08-api-db.png`
  6. **Caption (1–2 sentences):** docker compose ps tulostus
- **Used AI?** Yes 

### S1-09 — Vite React TypeScript scaffold (Must)

- **Status:** Done
- **commit:** S1-09: Vite React TypeScript scaffold
- **Demonstration:**
  1. **Do this:** Start the frontend (`npm run dev` in `frontend/` or via Compose if `web` already exists). Open the printed localhost URL in a browser.
  2. **Capture:** Screenshot of the browser showing the default Vite/React app shell.
  3. **Must show:** Browser address bar with the frontend URL and the running React/Vite page (not a blank error page).
  4. **Must not show:** API tokens or `.env` panels.
  5. **Save as:** `docs/reports/images/sprint-01/s1-09-frontend.png`
  6. **Caption (1–2 sentences):** Default viten sivun pyörimässä localhost:5173
- **Used AI?** No

### S1-10 — Router and placeholder home (Must)

- **Status:** Done
- **commit:** S1-10: Router and placeholder home
- **Demonstration:**
  1. **Do this:** With the frontend running, open the home route (usually `/`). Confirm your placeholder home content is what appears (not only the stock Vite counter if you replaced it).
  2. **Capture:** Screenshot of the home page including the URL bar.
  3. **Must show:** Placeholder home content and the route URL.
  4. **Must not show:** Secrets or unrelated authenticated data (none expected yet).
  5. **Save as:** `docs/reports/images/sprint-01/s1-10-home.png`
  6. **Caption (1–2 sentences):** Uusi etusivu, localhost:5173/ 
- **Used AI?**  No

### S1-11 — API base URL and health indicator (Should)

- **Status:**
- **PR / commit:**
- **Demonstration:** (only if you did this ticket)
  1. **Do this:** Open the home page with API and frontend running. Trigger or wait for the health fetch so the UI shows API status (and/or the configured base URL if you display it).
  2. **Capture:** Screenshot of the home page after the health indicator updates.
  3. **Must show:** Visible API health status (healthy/unhealthy or equivalent) on the home page; include the base URL on screen if your UI shows it.
  4. **Must not show:** Bearer tokens or `.env` files.
  5. **Save as:** `docs/reports/images/sprint-01/s1-11-health-ui.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S1-12 — Web service in Compose (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Run `docker compose up --build` so `db`, `api`, and `web` start. Open the frontend URL published by Compose (see your README / `.env` ports, often `http://localhost:5173`).
  2. **Capture:** One screenshot of `docker compose ps` (or Docker UI) showing all three services, and one of the frontend loaded from that URL—or a single collage if both fit.
  3. **Must show:** `db`, `api`, and `web` running; browser showing the frontend from the Compose-published URL.
  4. **Must not show:** Secrets from env files in the terminal scrollback.
  5. **Save as:** `docs/reports/images/sprint-01/s1-12-compose-web.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S1-13 — Root README (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the root `README.md` in the editor or on your Git host.
  2. **Capture:** Screenshot of the section that covers prerequisites, `.env`, Compose, and the URL / demo-path table.
  3. **Must show:** Clone → `.env` → Compose (or equivalent) steps and a table or list of service URLs a classmate can follow.
  4. **Must not show:** Real passwords committed in the README.
  5. **Save as:** `docs/reports/images/sprint-01/s1-13-readme.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### Stretch (only if you did them)

For each stretch below that you completed: Status, PR / commit, Used AI? Add Demonstration only where steps are listed.

#### S1-S1 — DB-aware health (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** With Compose up and Postgres reachable, open `http://localhost:8000/health/db` (or your documented path).
  2. **Capture:** Screenshot of the JSON response.
  3. **Must show:** Successful JSON indicating DB connectivity (not only process liveness).
  4. **Must not show:** Connection strings with passwords.
  5. **Save as:** `docs/reports/images/sprint-01/s1-s1-health-db.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

#### S1-S2 — Multi-stage API image (if done)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

#### S1-S3 — Smoke CI (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the CI run on your Git host for the workflow that smoke-tests the API (or installs and runs a documented check).
  2. **Capture:** Screenshot of a green / successful job.
  3. **Must show:** Workflow name and success status for the smoke job.
  4. **Must not show:** Secrets in logs.
  5. **Save as:** `docs/reports/images/sprint-01/s1-s3-ci.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

## How we worked

Sprint 1 is **two weeks**.

- **Week 1** (backend shell & Compose):
- **Week 2** (frontend shell & README):
- Who did what:
- One blocker and how you unblocked it:

## Decisions

Two to four technical choices with why (for example Vite in Compose vs build + nginx).

1.
2.

## What we learned

Note what you actually used. Tools this sprint: Git / monorepo, Python venv + `requirements.txt`, FastAPI + Uvicorn, OpenAPI (`/docs`), Pydantic / pydantic-settings, PostgreSQL, Docker Compose, React + TypeScript + Vite, React Router, `.env` / `.env.example`.

- What clicked:
- One thing you would do differently:

## Carry-over

Deferred Must/Should, stretch leftovers, risks for [Sprint 2 tickets](../tickets/sprint-02-tickets.md) (auth, catalog, SQLAdmin).

## AI usage (sprint-level reflection)

07

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

