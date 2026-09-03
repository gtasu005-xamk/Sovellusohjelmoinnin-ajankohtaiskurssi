# Sprint 2 report — Auth, catalog, SQLAdmin

Copy this file to `docs/reports/sprint-02.md` in **your** repo and fill the blanks. Keep it a process log: no pasted source, no secrets, no `.env` values.

| Field        | Your answer |
| ------------ | ----------- |
| **Dates**    |             |
| **Names**    |             |
| **Repo URL** |             |
| **Branch**   |             |

Tickets: [sprint-02-tickets.md](../tickets/sprint-02-tickets.md) · Index: [../README.md](../README.md)

## Sprint goal

From the tickets: add identity, schema (including the unit catalog), SQLAdmin, and JWT auth so sessions can belong to real users next sprint. You are done when migrations and seed work; `/admin` shows units, activities, and links; register / login / `/auth/me` work with bcrypt + JWT; the UI can register, log in, and show a profile.

In your words (2–3 sentences): did you meet that, and what is still rough?

## Tickets

For **each** ticket fill **Status** and **PR / commit**.

Fill **Demonstration** only where this template includes that section. Follow the numbered steps exactly. Store images under `docs/reports/images/sprint-02/` using the suggested filename. Crop secrets, password hashes, and full JWTs.

For **every** ticket: set **Used AI?** to `Yes` or `No`. Write the sprint-level **AI usage** reflection at the end of this report (not under each ticket).

Skip stretch tickets you did not do. Stretch: Status, PR, and Used AI? for each stretch you did; add a Demonstration only where listed below.

### S2-01 — SQLAlchemy engine, session, and Base (Must)

- **Status:** Done / deferred (why):
- **PR / commit:**
- **Used AI?** Yes / No

### S2-02 — User model (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Prefer `/admin` after env-based SQLAdmin login showing the Users (or `user`) table. If `/admin` is not ready yet, show the Alembic migration file (or `alembic history`) listing the `user` table create.
  2. **Capture:** Screenshot of `/admin` Users list or the migration/editor view of the `user` table.
  3. **Must show:** Proof a `user` (or Users) table exists in the schema or admin UI.
  4. **Must not show:** Password hashes, SQLAdmin password fields filled in, or JWT tokens.
  5. **Save as:** `docs/reports/images/sprint-02/s2-02-user.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-03 — ActivityType model (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open `/admin` activity types view, or show activity types in `/docs` if you already expose a list endpoint.
  2. **Capture:** Screenshot of activity types listed.
  3. **Must show:** At least one activity type row (name/slug visible) in `/admin` or `/docs`.
  4. **Must not show:** Secrets or unrelated user password data.
  5. **Save as:** `docs/reports/images/sprint-02/s2-03-activity-types.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-04 — UnitType model and activity links (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** In `/admin`, open unit types and the activity↔unit link (or activity detail) so Running → duration + distance (or your equivalent pair) is visible.
  2. **Capture:** Screenshot showing Running (or one activity) linked to at least two unit types such as duration and distance.
  3. **Must show:** The M:N link clearly (activity + allowed units), not only an empty units list.
  4. **Must not show:** SQLAdmin credentials in the shot.
  5. **Save as:** `docs/reports/images/sprint-02/s2-04-unit-links.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-05 — Alembic setup and initial migration (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Either (a) show `alembic upgrade head` succeeding in the terminal, (b) open the initial migration file in the editor, or (c) after a fresh Compose migrate, show tables present in `/admin` or `psql` `\dt`.
  2. **Capture:** Screenshot of one of those proofs.
  3. **Must show:** Migration tooling in use and schema applied (command success, migration file, or tables after upgrade).
  4. **Must not show:** Database passwords in the command line history.
  5. **Save as:** `docs/reports/images/sprint-02/s2-05-alembic.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-06 — Seed system catalog (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** After seed runs (startup or documented command), open `/admin` and browse unit types and activity types (and links if shown).
  2. **Capture:** Screenshot of seeded units and activities (enough rows to prove the catalog, for example six activities and four units).
  3. **Must show:** Seeded catalog data present—not empty tables after seed.
  4. **Must not show:** Admin password typed into a form in clear text if avoidable.
  5. **Save as:** `docs/reports/images/sprint-02/s2-06-seed.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-07 — SQLAdmin UI for Postgres (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open `http://localhost:8000/admin` (or your documented URL). Log in with **SQLAdmin env credentials** (not the app JWT Login page). Land on the admin home or a model list.
  2. **Capture:** Screenshot of `/admin` after successful env login.
  3. **Must show:** SQLAdmin UI loaded and authenticated; URL includes `/admin`.
  4. **Must not show:** The password you typed; crop the login form after submit if the password field is still visible. Do not show JWT Bearer tokens—this login is separate from app auth.
  5. **Save as:** `docs/reports/images/sprint-02/s2-07-admin.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-08 — Password hashing helpers (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S2-09 — JWT helpers and current user (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S2-10 — Register endpoint (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** In `/docs`, run `POST /auth/register` with a new email and password. Confirm HTTP 201 (or your documented success).
  2. **Capture:** Screenshot of the `/docs` request/response for register.
  3. **Must show:** Successful register response (201) and that a user was created (response body without password).
  4. **Must not show:** The password value in the request body—crop or blank it before saving.
  5. **Save as:** `docs/reports/images/sprint-02/s2-10-register.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-11 — Login endpoint (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** In `/docs`, run `POST /auth/login` with a valid user. Confirm a token field is present in the response.
  2. **Capture:** Screenshot showing login succeeded and a token **key** exists.
  3. **Must show:** Successful login and evidence a token was returned (you may blur/crop the token **value**).
  4. **Must not show:** The full JWT string pasted into the report or left readable in the image. Never paste the token into the Markdown.
  5. **Save as:** `docs/reports/images/sprint-02/s2-11-login.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-12 — Me endpoint (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** In `/docs`, authorize with a valid Bearer token (Authorize button). Call `GET /auth/me`. Confirm 200 and your user profile fields.
  2. **Capture:** Screenshot of `/auth/me` response.
  3. **Must show:** 200 response with the current user (for example email/id)—proving the token was accepted.
  4. **Must not show:** The Authorize dialog with a full token visible; crop tokens.
  5. **Save as:** `docs/reports/images/sprint-02/s2-12-me.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-13 — CORS lockdown (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** From the frontend origin, trigger an API call (for example health or `/auth/me`). Open DevTools → Network. Select the API request and open Headers.
  2. **Capture:** Screenshot of the request/response headers showing the allowed origin behavior for your SPA origin.
  3. **Must show:** The frontend origin and that the API response allows it (for example `Access-Control-Allow-Origin` matching your Vite origin, or a successful cross-origin call from that origin).
  4. **Must not show:** Authorization Bearer values—collapse or crop that header.
  5. **Save as:** `docs/reports/images/sprint-02/s2-13-cors.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-14 — Register page (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the Register page in the SPA. Optionally submit once with a test user, then crop any password fields.
  2. **Capture:** Screenshot of the Register UI.
  3. **Must show:** Register form (email/password fields visible as UI chrome, not filled secrets).
  4. **Must not show:** Typed passwords or confirmation codes.
  5. **Save as:** `docs/reports/images/sprint-02/s2-14-register-ui.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-15 — Login page and token storage (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the Login page. Log in successfully so the app stores the JWT in `localStorage` (do not open Application → Local Storage for the screenshot if the token value is visible).
  2. **Capture:** Screenshot of the Login UI (before or after login, without exposing the token value).
  3. **Must show:** Login page UI for the SPA.
  4. **Must not show:** `localStorage` panel with a readable JWT, or password fields filled in.
  5. **Save as:** `docs/reports/images/sprint-02/s2-15-login-ui.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-16 — Protected layout (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** While logged out, open a gated route (for example Dashboard or Settings). Confirm you are redirected or blocked. Then log in and open the same route; confirm the protected layout appears.
  2. **Capture:** Two screenshots (logged-out bounce + logged-in layout) or one collage.
  3. **Must show:** Logged-out user cannot stay on the gated page; logged-in user sees the protected shell.
  4. **Must not show:** Tokens in the URL or DevTools.
  5. **Save as:** `docs/reports/images/sprint-02/s2-16-protected.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-17 — User display and logout (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** While logged in, show the header or Settings with the current user identity. Then log out and show the post-logout state (login page or cleared header).
  2. **Capture:** Two screenshots (before and after logout).
  3. **Must show:** User identity visible when logged in; after logout the user is gone from the chrome and protected content is inaccessible.
  4. **Must not show:** Tokens or password fields.
  5. **Save as:** `docs/reports/images/sprint-02/s2-17-logout.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S2-18 — Auth + SQLAdmin README notes (Should)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the README section that documents auth (register/login) and `/admin` (env credentials, separate from JWT).
  2. **Capture:** Screenshot of that README section.
  3. **Must show:** Auth and SQLAdmin documented (URLs / purpose; placeholder credentials only if they match `.env.example`, not production secrets).
  4. **Must not show:** Real production passwords.
  5. **Save as:** `docs/reports/images/sprint-02/s2-18-readme.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### Stretch (only if you did them)

For each stretch below that you completed: Status, PR / commit, Used AI? Add Demonstration only where steps are listed. [S2-S2](../tickets/sprint-02-tickets.md#s2-s2--email-normalization) and [S2-S4](../tickets/sprint-02-tickets.md#s2-s4--keep-sqladmin-views-in-sync) are Status, PR, and Used AI? only.

#### S2-S1 — Stronger password rules (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** In `/docs` or the Register UI, submit a deliberately weak password that your rules reject.
  2. **Capture:** Screenshot of HTTP 422 (or your documented validation error) with the password value cropped.
  3. **Must show:** Validation failure for a weak password (422 or equivalent).
  4. **Must not show:** The weak password text if it is still readable—crop it.
  5. **Save as:** `docs/reports/images/sprint-02/s2-s1-weak-password.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

#### S2-S2 — Email normalization (if done)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

#### S2-S3 — API test register / login / me (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Run the documented `pytest` command for auth API tests.
  2. **Capture:** Terminal screenshot showing tests passed.
  3. **Must show:** Passing auth-related tests (register/login/me or equivalent names).
  4. **Must not show:** Secrets in the command line.
  5. **Save as:** `docs/reports/images/sprint-02/s2-s3-pytest.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

#### S2-S4 — Keep SQLAdmin views in sync (if done)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

## How we worked

Sprint 2 is **three weeks**.

- **Week 1** (schema, seed, SQLAdmin):
- **Week 2** (bcrypt, JWT, CORS):
- **Week 3** (Login/Register UI, `localStorage`, gated layout):
- Who did what:
- One blocker and how you unblocked it:

## Decisions

Two to four technical choices with why (for example JWT library, CORS origin, what you store in `localStorage`).

1.
2.

## What we learned

Note what you actually used. Tools this sprint: SQLAlchemy, Alembic, psycopg, SQLAdmin, bcrypt (or passlib), JWT, FastAPI security (`HTTPBearer`), CORSMiddleware, `localStorage`.

- What clicked:
- One thing you would do differently:

## Carry-over

Deferred Must/Should, stretch leftovers, risks for [Sprint 3 tickets](../tickets/sprint-03-tickets.md) (sessions, planned/actual, clone, plans via `plan_id`, calendar, ownership).

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

