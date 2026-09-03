# Sprint 5 tickets — AI-Assisted Insights (Ollama)

Backlog for Sprint 5 ([index](../README.md)). Copy tickets into your issue tracker if you like; keep the IDs (`S5-01`, …) in branch and PR titles.

## Your task for Sprint 5

The gym now has a membership desk, a training floor, lockers, and a scoreboard. What it still lacks is a **house coach** who has read *this member’s* log—not a stranger on the internet with no context.

Sprint 5 hires that coach as **local Ollama**. Pack the member’s **sessions**, **goals**, and Sprint 4 **stats** into a prompt, call a model through an **`AIProvider` abstraction**, and show a **structured** insight (`summary`, `strengths`, `recommendations`, `caveats`). Routers depend on a protocol, not Ollama specifically, so a cloud stub (and later a real cloud LLM) can plug in behind the same interface.

If the coach is out or slow, the gym stays open: people still log sessions and read the scoreboard. You are not shipping rate limits, a paid cloud LLM, or a broader test harness yet—those wait for optional Sprint 6. You are also not rebuilding sessions, goals, or stats—Sprint 5 consumes that data.

```text
Sprint 3–4 data                         Sprint 5
────────────────                        ────────
WorkoutSession (+ items/measurements) → context builder
Goal (unit_type_id)                   → period prompt pack
/stats summary / streaks (optional)   → AIProvider.generate_insight
                                      → POST /ai/insights
                                      → Insights UI (soft-fail)
```

**Teaching rules (aligned with earlier sprints):**

- Use **sessions / measurements / period goals**—not flat “workouts” or free-text metrics
- Prefer **actual** measurement values in context packs when present; document planned fallback if any
- Context is **always user-scoped** (same ownership mindset as Sprint 3 IDOR)
- Prefer sessions with **non-null** `session_at` for period-based coaching unless you document otherwise
- Do not pack separate “template” entities—Sprint 3 has none; reuse is clone snapshots
- **AI is optional:** when Ollama is down, sessions, plans, calendar, and stats must keep working

### Prerequisites from Sprint 4

This backlog assumes you already have:

- Authenticated session CRUD with items + planned/actual measurements, clone, plans via `plan_id`, calendar (Sprint 3)
- Goals model + API keyed by `unit_type_id` (Sprint 3; UI may still be optional)
- `/stats/summary`, `/stats/progress`, `/stats/streaks` (or equivalent analytics you can call from a service)
- JWT + protected React layout; TanStack Query; Dashboard with recent sessions / widgets
- Layered backend (`api` → `services` → `repositories` → `models`/`db`)

If those are missing, finish or stabilize [Sprint 4 tickets](sprint-04-tickets.md) (and earlier) first—AI on empty or leaky data wastes the sprint.

Sprint 1 Compose and Sprint 2 auth/catalog are still assumed underneath.

### What success looks like

When you finish Sprint 5, you should be able to demo:

1. With Ollama + a pulled model + session history, `POST /ai/insights` returns structured fields (`summary`, `strengths`, `recommendations`, `caveats`)
2. Without Ollama / on timeout, API and UI fail softly (clear error; app process stays up)
3. `CloudProvider` stub exists; `AI_PROVIDER` env selects the provider
4. Insights page supports week/month (optional focus) and renders the four sections
5. Insights use **only** the logged-in user’s sessions, goals, and stats

That demo unlocks a course handoff—or optional Sprint 6 (tests, rate limits, deployment docs).

**Suggested demo flow:** start Ollama → log in → request a weekly insight → show structured sections → stop Ollama → request again → friendly error → point at the provider abstraction in code.

### New tools & technologies

| Tool / technology              | Role in this sprint                                      |
| ------------------------------ | -------------------------------------------------------- |
| **Ollama**                     | Local LLM runtime for insights                           |
| **`AIProvider` protocol**      | Swap Ollama vs cloud stub without rewriting routers      |
| **httpx** (or equivalent)      | Call Ollama’s HTTP API from the backend                  |
| **Compose profiles** (optional)| Optional `ollama` service beside `db` / `api` / `web`    |
| **Structured JSON insights**   | `summary` / `strengths` / `recommendations` / `caveats`  |

*(Carried forward: session history, goals, Sprint 4 stats as prompt context.)* See also the matching section in the [sprint index](../README.md).

### What you will learn

- Install and smoke-test **Ollama** locally (pull a small model)
- Define an `AIProvider` abstraction with Ollama + a cloud stub
- Pack personal **session / goal / stats** context for prompting (user-scoped)
- Expose `POST /ai/insights` with a structured response
- Handle timeouts and downtime in API and UI
- Document local model setup and env configuration

### Backend layered architecture

AI features must follow the same call direction as auth, sessions, and stats. **Outer layers may call inward; inward layers must not import outward.**

```text
api/ai.py  →  services/ai/insights.py (or similar)  →  context builder + AIProvider
                      ↓
              services/ai/ollama.py | cloud.py | factory.py
                      ↓
         repositories / existing session, goal, stats loaders
                      ↑
               schemas/ai.py
```

| Layer             | Responsibility                                                      |
| ----------------- | ------------------------------------------------------------------- |
| `api/`            | HTTP only — parse input, call a service, map errors to status codes |
| `schemas/`        | Pydantic DTOs for requests/responses                                |
| `services/ai/`    | Orchestrate context + provider; map soft failures                   |
| Provider impl     | HTTP calls to Ollama (or the cloud stub)                            |
| `repositories/`   | SQLAlchemy reads of the **current user’s** data (reuse Sprint 3–4)  |

Do **not** put prompt assembly or Ollama HTTP inside thin routers. Do **not** accept another user’s id from the client when building context.

### Out of scope (intentionally later / already done)

| Topic                                                 | When it arrives            |
| ----------------------------------------------------- | -------------------------- |
| Broader API/UI test harness, **rate limits**, deploy  | Sprint 6 (optional)        |
| Real paid cloud LLM wiring (beyond stub)              | Later / optional           |
| New session/plan/calendar/clone or catalog redesign | Sprints 2–3 (already done) |
| Replacing JWT / `localStorage`                        | optional Sprint 6          |
| Rebuilding Compose, health, auth, stats charts        | Sprints 1–4 (already done) |

### Week-by-week map

| Week  | Focus                                                              | Ticket IDs    | Checkpoint                                                    |
| ----- | ------------------------------------------------------------------ | ------------- | ------------------------------------------------------------- |
| **1** | Install Ollama locally + provider layer (+ optional Compose profile) | S5-01 … S5-06 | Local Ollama + model ready; script or temporary call reaches it |
| **2** | Context + `/ai/insights` + soft failure (+ optional cache)         | S5-07 … S5-11 | OpenAPI success path + controlled error when Ollama is down   |
| **3** | Insights UI, docs, Dashboard CTA                                   | S5-12 … S5-16 | Demo success path and soft-fail path without reading source   |

### How the tickets fit together

```text
Week 1                         Week 2                      Week 3
────────                       ────────                    ────────
Install Ollama + pull model    Context builder             Insights page
AIProvider protocol            POST /ai/insights           Render 4 sections
Ollama provider                Structured parse            Loading / error UX
Cloud stub                     Timeouts / soft failure     Ollama setup docs
Factory + env                  Optional AiInsight cache    Dashboard CTA
Optional Compose profile
```

Do **Must** tickets first, then **Should** (S5-06, S5-16), then **Stretch** if you have time.

**How to read each ticket:** **New here** explains the concept and lists **Docs & tutorials**. **Your task** states the deliverable. **Instructions** walk through the work. **Stay in scope** keeps later-sprint features out of this ticket. **Commit** means create a new Git commit when the ticket is done (ticket ID in the message).

### Ticket index

| ID                                                          | Title                             | Week | Priority | Estimate |
| ----------------------------------------------------------- | --------------------------------- | ---- | -------- | -------- |
| [S5-01](#s5-01--install-ollama-locally)                     | Install Ollama locally            | 1    | Must     | M        |
| [S5-02](#s5-02--aiprovider-protocol)                        | AIProvider protocol               | 1    | Must     | S        |
| [S5-03](#s5-03--ollama-provider)                            | Ollama provider                   | 1    | Must     | L        |
| [S5-04](#s5-04--cloud-provider-stub)                        | Cloud provider stub               | 1    | Must     | S        |
| [S5-05](#s5-05--provider-factory-and-env)                   | Provider factory and env          | 1    | Must     | M        |
| [S5-06](#s5-06--optional-ollama-compose-profile)            | Optional Ollama Compose profile   | 1    | Should   | M        |
| [S5-07](#s5-07--context-builder)                            | Context builder                   | 2    | Must     | L        |
| [S5-08](#s5-08--ai-insights-endpoint)                       | AI insights endpoint              | 2    | Must     | M        |
| [S5-09](#s5-09--structured-response-parsing)                | Structured response parsing       | 2    | Must     | M        |
| [S5-10](#s5-10--timeouts-and-soft-failure)                  | Timeouts and soft failure         | 2    | Must     | M        |
| [S5-11](#s5-11--optional-aiinsight-cache)                   | Optional AiInsight cache          | 2    | Stretch  | M        |
| [S5-12](#s5-12--insights-page)                              | Insights page                     | 3    | Must     | M        |
| [S5-13](#s5-13--render-structured-insight)                  | Render structured insight         | 3    | Must     | M        |
| [S5-14](#s5-14--loading-and-error-ux)                       | Loading and error UX              | 3    | Must     | S        |
| [S5-15](#s5-15--ollama-setup-docs)                          | Ollama setup docs                 | 3    | Must     | M        |
| [S5-16](#s5-16--dashboard-cta-to-insights)                  | Dashboard CTA to Insights         | 3    | Should   | S        |
| [S5-S1](#s5-s1--sse-streaming)                              | SSE streaming                     | —    | Stretch  | L        |
| [S5-S2](#s5-s2--model-picker)                               | Model picker                      | —    | Stretch  | M        |

---

## S5-01 — Install Ollama locally

| Field          | Value                                                              |
| -------------- | ------------------------------------------------------------------ |
| **Type**       | chore                                                              |
| **Week**       | 1                                                                  |
| **Priority**   | Must                                                               |
| **Estimate**   | M                                                                  |
| **Depends on** | Sprint 1 machine can run Docker / browser (course laptop ready)    |

### New here: Ollama on your machine

**Ollama** is a local runtime for large language models. You install it on your **host** (Windows / macOS / Linux), pull a small model, and confirm the HTTP API answers—usually at `http://localhost:11434`. That is the primary demo path for this course: no paid API key, no cloud billing.

This ticket is **you setting up the tool**. Writing classmate-facing docs is [S5-15](#s5-15--ollama-setup-docs). An optional Docker Compose profile is [S5-06](#s5-06--optional-ollama-compose-profile)—useful later, not a substitute for knowing the host install.

Without a running Ollama + pulled model, you cannot verify `OllamaProvider`, soft-failure demos, or the Insights success path. Install early in Week 1 so coding is not blocked on a multi-GB download.

**Docs & tutorials:**

- [Ollama — Download](https://ollama.com/download) — install for your OS
- [Ollama](https://ollama.com/) — pull / run overview
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md) — quick smoke-test of generate/chat or tags

### Your task

Install Ollama on your development machine, pull a small model, and smoke-test the HTTP API so later tickets have a real endpoint to call. Your deliverable is a working local runtime plus a noted model name for `.env`—not application code, and not classmate-facing docs yet.

### Instructions

1. Install Ollama for your OS from the official download page.
2. Confirm the CLI works (`ollama --version` or equivalent) and the service is running.
3. Pull a **small** model suitable for demos (pick one and stick to it—e.g. a lightweight instruct model your machine can run).
4. Smoke-test the HTTP API (list tags or a short generate/chat call) so you know the base URL, usually `http://localhost:11434`.
5. Write down the model name you will put in `.env` / `.env.example` later ([S5-05](#s5-05--provider-factory-and-env)).

### Stay in scope

- Leave classmate-facing setup docs for S5-15; a personal note is enough here.
- Leave the optional Compose profile for S5-06. Host install is the Must path.
- Leave `OllamaProvider`, factory, and `/ai/insights` for later tickets this sprint.
- Do not treat a cloud LLM or paid API key as a substitute for this install.

### Hints

- Prefer a smaller model first; you can switch later (stretch model picker is optional).
- If disk/RAM is tight, still install the CLI and confirm the API responds—classmates may use a tiny model.
- Host URL for the API container is often `http://host.docker.internal:11434` (Docker Desktop) vs `http://localhost:11434` when the API runs on the host. You will wire that in S5-03 / S5-05; for this ticket, host → localhost is enough.
- Stopping Ollama later is how you demo soft failure ([S5-10](#s5-10--timeouts-and-soft-failure)).

### Acceptance criteria

- [ ] Ollama installed and runnable on your development machine
- [ ] At least one model pulled successfully
- [ ] HTTP API responds locally (documented base URL, usually port `11434`)
- [ ] Chosen model name written down for `.env.example` (even if env wiring is S5-05)

### Suggested paths

Local machine only (no repo path required). Optional notes: personal scratch in `docs/ollama.md` draft—finalize in S5-15.

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-01` in the message, for example `S5-01: short summary`. Never commit `.env` or secrets.

---

## S5-02 — AIProvider protocol

| Field          | Value                                                      |
| -------------- | ---------------------------------------------------------- |
| **Type**       | feature                                                    |
| **Week**       | 1                                                          |
| **Priority**   | Must                                                       |
| **Estimate**   | S                                                          |
| **Depends on** | Sprint 4 stats available (for later context packing)       |

### New here: provider abstraction

An **`AIProvider`** is a small interface (protocol or ABC) your routers and services depend on—not Ollama’s HTTP details. Implementations turn a **context dict** into a **structured insight dict**. That keeps Sprint 5 demoable on local Ollama and leaves a clean slot for a future cloud LLM.

Routers should depend on an interface, not a vendor. Swapping local and cloud providers must not mean rewriting `/ai/insights`.

**Docs & tutorials:**

- [typing — Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol) — structural interfaces
- [abc — Abstract Base Classes](https://docs.python.org/3/library/abc.html) — alternative to Protocol
- Layering reminder: keep routers thin (same as Sprints 1–4)

### Your task

Define the `AIProvider` protocol so later implementations (`OllamaProvider`, `CloudProvider`) share one method shape. Your deliverable is a dedicated module with an async `generate_insight` contract and a documented structured return type.

### Instructions

1. Define an `AIProvider` protocol/ABC with `async def generate_insight(self, context: dict) -> dict` (or a typed equivalent).
2. Document the return type as a structured insight dict (`summary`, `strengths`, `recommendations`, `caveats`—even if parsing lands in S5-09).
3. Place it in a dedicated module so routers/services can type-hint the protocol, not a concrete Ollama class.

### Stay in scope

- Leave the Ollama HTTP client for S5-03 and the cloud stub for S5-04.
- Leave the factory and `.env` wiring for S5-05.
- Leave `POST /ai/insights` for S5-08. A type that services can depend on is enough here.
- Do not hardcode Ollama URLs or model names on the protocol.

### Hints

- Prefer `typing.Protocol` or an ABC—both are fine if the factory returns implementations cleanly.
- Keep the method async from day one even if some stubs are sync wrappers.

### Acceptance criteria

- [ ] Protocol/ABC lives in a dedicated module
- [ ] Return type documented as structured insight dict
- [ ] Routers/services can depend on the protocol type (not a concrete Ollama class)

### Suggested paths

`backend/app/services/ai/base.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-02` in the message, for example `S5-02: short summary`. Never commit `.env` or secrets.

---

## S5-03 — Ollama provider

| Field          | Value      |
| -------------- | ---------- |
| **Type**       | feature    |
| **Week**       | 1          |
| **Priority**   | Must       |
| **Estimate**   | L          |
| **Depends on** | S5-01, S5-02 |

### New here: calling Ollama from Python

You already installed Ollama locally ([S5-01](#s5-01--install-ollama-locally)). Now implement **`OllamaProvider`**: turn a context pack into a prompt and call Ollama’s HTTP API so demos do not require paid API keys.

Local Ollama is the happy-path demo. Classmates must be able to pull a model and get insights without cloud billing.

**Docs & tutorials:**

- [Ollama](https://ollama.com/) — install / pull models
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md) — generate / chat HTTP
- [httpx](https://www.python-httpx.org/) — async HTTP client

### Your task

Implement `OllamaProvider` against the protocol from S5-02, reading base URL and model from settings. Your deliverable is a working local call that sends a prompt derived from the context dict.

### Instructions

1. Implement `OllamaProvider` calling the local Ollama HTTP API (generate or chat—pick one and document it).
2. Read `OLLAMA_BASE_URL` and `OLLAMA_MODEL` from settings/env.
3. Send a prompt derived from the context dict; verify against a pulled model in local/dev.
4. Keep HTTP client timeouts in mind—you will harden them in S5-10. A reasonable default now is fine.

### Stay in scope

- Leave the cloud stub for S5-04 and the factory for S5-05.
- Leave structured JSON parsing for S5-09 if the raw model text is still messy—getting a response back is the bar here.
- Leave timeout/503 mapping for S5-10; do not invent rate limiting (Sprint 6).
- Do not hardcode secrets or model names in source. Do not call a paid cloud API from this class.

### Hints

- Prefer **httpx** (async) for calls from an async FastAPI path.
- Model name belongs in env / `.env.example` (wired in S5-05 if you have not added the keys yet).

### Acceptance criteria

- [ ] Uses `OLLAMA_BASE_URL` and `OLLAMA_MODEL`
- [ ] Sends a prompt derived from context
- [ ] Works against a pulled model in local/dev
- [ ] Endpoint choice (generate vs chat) documented briefly

### Suggested paths

`backend/app/services/ai/ollama.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-03` in the message, for example `S5-03: short summary`. Never commit `.env` or secrets.

---

## S5-04 — Cloud provider stub

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 1       |
| **Priority**   | Must    |
| **Estimate**   | S       |
| **Depends on** | S5-02   |

### New here: stub vs fake coaching

A **stub** proves the abstraction is real. It must **not** invent coaching text that looks like a live cloud call, and it must **not** pretend to bill a paid API. Raising a clear “not configured” error when selected is the correct behavior for this sprint.

Without a stub, “provider abstraction” is only a diagram. Failing loudly when `AI_PROVIDER=cloud` teaches configuration honesty.

**Docs & tutorials:**

- Same Protocol/ABC docs as S5-02
- Optional later reading: your chosen cloud vendor’s “API keys in env” docs (do not implement billing here)

### Your task

Add a `CloudProvider` that implements `AIProvider` and fails with a documented “not configured” error. Your deliverable is a honest stub—not fake coaching and not a billed cloud client.

### Instructions

1. Implement `CloudProvider` conforming to `AIProvider`.
2. Raise or return a documented “not configured” error—no fake paid calls.
3. Comment/docstring future API-key env vars (names only; no secrets).

### Stay in scope

- Leave factory selection (`AI_PROVIDER=cloud`) for S5-05; the class just has to exist and fail clearly.
- Leave real vendor SDKs, billing, and production cloud wiring for later / optional work.
- Do not ship placeholder “You should rest more” fluff from this stub.

### Hints

- Keep the class small; optional Sprint 6 deployment docs can mention it as future config.

### Acceptance criteria

- [ ] Class exists implementing `AIProvider`
- [ ] Raises or returns a documented not-configured error
- [ ] Comment/docstring points to future API-key env vars (names only)

### Suggested paths

`backend/app/services/ai/cloud.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-04` in the message, for example `S5-04: short summary`. Never commit `.env` or secrets.

---

## S5-05 — Provider factory and env

| Field          | Value      |
| -------------- | ---------- |
| **Type**       | feature    |
| **Week**       | 1          |
| **Priority**   | Must       |
| **Estimate**   | M          |
| **Depends on** | S5-03, S5-04 |

### New here: factory + env selection

A **factory** returns the concrete `AIProvider` based on `AI_PROVIDER` (default `ollama`). Documented env vars are how classmates switch providers without reading your source—same config habit as Sprint 1 Compose / Sprint 2 JWT secrets.

Runtime selection keeps routers stable. Unknown provider values should fail fast with a clear error.

**Docs & tutorials:**

- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — env-backed settings
- [FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) — inject the provider

### Your task

Wire provider selection through settings so `AI_PROVIDER` chooses Ollama or the cloud stub without changing routers. Your deliverable is a factory plus `.env.example` keys (`AI_PROVIDER`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`).

### Instructions

1. Build a factory that returns Ollama or Cloud based on `AI_PROVIDER` (default `ollama`).
2. List `AI_PROVIDER`, `OLLAMA_BASE_URL`, and `OLLAMA_MODEL` in `.env.example`.
3. Fail fast with a clear error on unknown provider values.
4. Prefer injecting the provider via FastAPI `Depends` so later tests (optional Sprint 6) can mock it.

### Stay in scope

- Leave `POST /ai/insights` for S5-08; the factory only has to return the right implementation.
- Leave the optional Compose Ollama hostname for S5-06; document `localhost` / `host.docker.internal` as needed for the host path.
- Leave rate limits for Sprint 6.
- Do not commit real secrets. Names in `.env.example` only.

### Hints

- Default to ollama so local demos work out of the box.
- Reuse `pydantic-settings` patterns from Sprint 1 if you already have them.

### Acceptance criteria

- [ ] Factory returns the correct implementation
- [ ] `.env.example` lists `AI_PROVIDER`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
- [ ] Unknown provider value fails fast with a clear error

### Suggested paths

`backend/app/services/ai/factory.py`, `.env.example`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-05` in the message, for example `S5-05: short summary`. Never commit `.env` or secrets.

---

## S5-06 — Optional Ollama Compose profile

| Field          | Value                    |
| -------------- | ------------------------ |
| **Type**       | feature                  |
| **Week**       | 1                        |
| **Priority**   | Should                   |
| **Estimate**   | M                        |
| **Depends on** | Sprint 1 Compose stack   |

### New here: Compose profiles

A **Compose profile** lets demos start Ollama with the stack without forcing everyone to pull huge images on every `docker compose up`. Default path stays light; Ollama is opt-in.

Classmates with limited disk/RAM should still run `db` / `api` / `web`. Profiled Ollama is for demos that need the model in Docker. Host-installed Ollama from [S5-01](#s5-01--install-ollama-locally) remains the primary path.

**Docs & tutorials:**

- [Compose profiles](https://docs.docker.com/compose/how-tos/profiles/) — optional services
- [Compose networking](https://docs.docker.com/compose/networking/) — service DNS names

### Your task

Add an optional Compose profile/service for Ollama so the heavy image is opt-in. Your deliverable is a profiled service plus a documented start command—and a default `compose up` that still works without it.

### Instructions

1. Add an optional Compose profile/service for Ollama.
2. Keep default `compose up` working without the heavy image if profiled.
3. Document the command to start with the profile (e.g. `docker compose --profile ollama up`).
4. Point `OLLAMA_BASE_URL` at the service name inside the Compose network when using the profile, and confirm the API can reach that hostname.

### Stay in scope

- Do not make Ollama required on every `docker compose up`. Host install (S5-01) stays the Must path.
- Leave classmate-facing docs polish for S5-15; a short comment or README note for the profile command is enough here.
- Leave `/ai/insights` and Insights UI for Week 2–3.
- Do not replace the host install with “Compose only.”

### Hints

- Host-installed Ollama remains the primary path—document both host and profile if you support the profile.

### Acceptance criteria

- [ ] Default `compose up` still works without pulling huge images if profiled
- [ ] Documented command to start with Ollama profile
- [ ] API can reach Ollama service hostname when profiled

### Suggested paths

`docker-compose.yml`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-06` in the message, for example `S5-06: short summary`. Never commit `.env` or secrets.

---

## S5-07 — Context builder

| Field          | Value                                         |
| -------------- | --------------------------------------------- |
| **Type**       | feature                                       |
| **Week**       | 2                                             |
| **Priority**   | Must                                          |
| **Estimate**   | L                                             |
| **Depends on** | Sprint 3 sessions + goals, Sprint 4 stats     |

### New here: packing personal context

A **context builder** packs compact, JSON-friendly context for the model: the current user’s **sessions** (items/measurements as needed), **goals** (`unit_type_id` from Sprint 3), and **stats summaries** for a period. It is not a dump of the entire database.

Prefer non-null `session_at` for period windows (same calendar mindset as Sprint 4). Never accept another user’s id from the client. Good insights need personal, size-bounded context—huge prompts are slow, expensive later, and leaky if ownership is wrong.

**Docs & tutorials:**

- Reuse analytics from [Sprint 4 tickets](sprint-04-tickets.md) where helpful
- Goals model: [S3-02](sprint-03-tickets.md#s3-02--goal-model-and-migration) / [S3-09](sprint-03-tickets.md#s3-09--goals-crud-api)
- [json — JSON encoder](https://docs.python.org/3/library/json.html) — keep context JSON-serializable

### Your task

Build a user-scoped context pack from **sessions**, **goals**, and **stats** for `week` / `month`. Your deliverable is a testable function (or small module) that returns a JSON-friendly dict—not a new CRUD API and not a prompt dump of the whole database.

### Instructions

1. Build JSON-friendly context from the user’s **sessions**, **goals**, and **stats** for a period (`week` / `month`).
2. Include only the **current** user’s data (load via repositories / existing services—same ownership as Sprint 3).
3. Keep output size reasonable (truncate long notes; summarize rather than paste every measurement row).
4. Make it unit-testable with fixtures (plain dicts / dataclasses—reuse Sprint 4 fixture habits where helpful).
5. Name fields clearly (`sessions`, `goals`, `stats`)—avoid legacy “workouts” wording in new code.

### Stay in scope

- Leave `POST /ai/insights` for S5-08; this ticket only packs context.
- Do not invent free-text metrics or `unit_hint`. Goals stay keyed by `unit_type_id`.
- Do not accept `user_id` from the client. Do not load another user’s sessions or stats.
- Unscheduled sessions (`session_at` null) usually stay out of “this week’s coaching” unless you document including them. Prefer **actual** values in the packed history.
- New session/plan/calendar/clone redesign belongs in Sprint 3 (already done)—do not rebuild it here.
- Leave rate limits for Sprint 6.

### Hints

- Reuse Sprint 4 analytics helpers for summaries when possible instead of re-aggregating ad hoc in the prompt string.

### Acceptance criteria

- [ ] Only current user’s data included
- [ ] Period (week/month) respected
- [ ] Output size kept reasonable (truncate long notes if needed)
- [ ] Unit-testable with fixtures
- [ ] Domain language uses sessions / goals / stats (not flat “workouts”)

### Suggested paths

`backend/app/services/ai/context.py`, `backend/tests/test_ai_context.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-07` in the message, for example `S5-07: short summary`. Never commit `.env` or secrets.

---

## S5-08 — AI insights endpoint

| Field          | Value      |
| -------------- | ---------- |
| **Type**       | feature    |
| **Week**       | 2          |
| **Priority**   | Must       |
| **Estimate**   | M          |
| **Depends on** | S5-05, S5-07 |

### New here: generate via POST

`POST /ai/insights` is the public contract: **auth required**, body with `period` and optional `focus`, structured coaching back to the UI. POST fits better than GET for a slow “generate” action (and for later rate limits in optional Sprint 6).

OpenAPI becomes the classmate contract. A thin router + AI service keeps layering consistent with `/stats/*` and session routes.

**Docs & tutorials:**

- [FastAPI — Body](https://fastapi.tiangolo.com/tutorial/body/) — request models
- [FastAPI — Security](https://fastapi.tiangolo.com/tutorial/security/) — reuse JWT dependency from Sprint 2
- [OpenAPI /docs](https://fastapi.tiangolo.com/features/#automatic-docs) — verify the route appears

### Your task

Expose `POST /ai/insights` so the UI (and `/docs`) can request a structured insight for the logged-in user. Your deliverable is an authenticated, documented route that calls the context builder and provider.

### Instructions

1. Implement `POST /ai/insights` with body `{ period: "week"|"month", focus?: string }`.
2. Validate period/focus; require authentication (`Depends(get_current_user)`).
3. Call context builder + provider; document the route in OpenAPI.
4. Keep the response schema aligned with S5-09 (`summary`, `strengths`, `recommendations`, `caveats`).

### Stay in scope

- Do not accept `user_id` in the body. Use the current user only.
- Leave timeout/503 mapping for S5-10 if you have not hardened it yet; a success path through OpenAPI is the bar here.
- Leave Insights UI for S5-12. Leave caching for stretch S5-11.
- Leave **rate limits** for Sprint 6—do not add throttling in this ticket.
- Do not put prompt assembly or Ollama HTTP inside the router.

### Hints

- Focus is optional coaching emphasis (e.g. “recovery”, “running volume”)—still built only from the current user’s data.

### Acceptance criteria

- [ ] Validates period/focus
- [ ] Auth required; uses current user only
- [ ] Calls context builder + provider
- [ ] Documented in OpenAPI

### Suggested paths

`backend/app/api/ai.py`, `backend/app/services/ai/`, `backend/app/schemas/ai.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-08` in the message, for example `S5-08: short summary`. Never commit `.env` or secrets.

---

## S5-09 — Structured response parsing

| Field          | Value      |
| -------------- | ---------- |
| **Type**       | feature    |
| **Week**       | 2          |
| **Priority**   | Must       |
| **Estimate**   | M          |
| **Depends on** | S5-03, S5-08 |

### New here: structured insight shape

Normalize model output into **`summary`**, **`strengths`**, **`recommendations`**, and **`caveats`**. That keeps the UI scannable, mocks easy, and warnings visible—raw prose walls are hard to test and easy to mishandle.

Structured fields are the contract between Ollama and React. Missing sections should become empty strings/lists safely—not 500s after a partial parse.

**Docs & tutorials:**

- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/) — response DTOs
- [json.loads](https://docs.python.org/3/library/json.html#json.loads) — parse model text carefully

### Your task

Parse and enforce the four-field insight shape so the client always receives `summary`, `strengths`, `recommendations`, and `caveats`. Your deliverable is prompt guidance plus Pydantic (or equivalent) normalization—not a new endpoint.

### Instructions

1. Instruct the model (via prompt) to return the structured shape—JSON if possible.
2. Parse/normalize model output into `{ summary, strengths, recommendations, caveats }`.
3. Treat missing sections as empty strings/lists safely; enforce the schema to the client (Pydantic).
4. Strip common wrappers (e.g. markdown code fences) defensively.

### Stay in scope

- Do not add extra UI sections or a free-form “chat” blob as the primary contract.
- Leave Insights rendering for S5-13; this ticket is the API/schema contract.
- Leave rate limits for Sprint 6.
- Prefer failing soft into empty sections over crashing the request after a partial parse.

### Hints

- Keep caveats in the schema even when empty—UI decides visibility (S5-13).

### Acceptance criteria

- [ ] Response schema enforced to the client
- [ ] Missing sections become empty lists/strings safely
- [ ] Prompt instructs the model toward this structure

### Suggested paths

`backend/app/services/ai/ollama.py`, `backend/app/schemas/ai.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-09` in the message, for example `S5-09: short summary`. Never commit `.env` or secrets.

---

## S5-10 — Timeouts and soft failure

| Field          | Value      |
| -------------- | ---------- |
| **Type**       | feature    |
| **Week**       | 2          |
| **Priority**   | Must       |
| **Estimate**   | M          |
| **Depends on** | S5-03, S5-08 |

### New here: soft failure for optional AI

**Soft failure** means AI downtime does not take down the API process or block sessions/stats. Map connection errors and timeouts to a clear status (e.g. 503/502) with a message.

AI is an extra. Soft failure is part of the Definition of Done for this sprint. Rate limiting belongs in optional Sprint 6—not required here.

**Docs & tutorials:**

- [httpx timeouts](https://www.python-httpx.org/advanced/timeouts/) — connect/read timeouts
- [FastAPI — Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) — HTTPException / handlers

### Your task

Make Ollama downtime a predictable API error, not a crashed worker. Your deliverable is a configurable HTTP timeout plus mapped 503/502 (or similar) while sessions, stats, and health keep answering.

### Instructions

1. Apply a configurable HTTP timeout to Ollama calls.
2. Map connection errors / timeouts to a clear API error (e.g. 503/502) with a message.
3. Confirm other API routes (sessions, stats, health) still work while AI fails.
4. Do not let unhandled exceptions take down the Uvicorn worker.

### Stay in scope

- Leave Insights loading/error UI for S5-14; this ticket is the API behavior.
- Leave **rate limits** for Sprint 6. Timeout + connection errors are enough.
- Do not retry forever or block the request on a hung model with no timeout.
- Do not mark the whole API “unhealthy” solely because Ollama is down (unless you add a separate optional AI check).

### Hints

- Demo path: start Ollama → success → stop Ollama → friendly error.
- Expose timeout via settings/env if classmates need longer generations.

### Acceptance criteria

- [ ] Timeout value configurable
- [ ] Down Ollama → predictable 503/502 (or similar) with message
- [ ] Other API routes still work while AI fails

### Suggested paths

`backend/app/services/ai/ollama.py`, `backend/app/api/ai.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-10` in the message, for example `S5-10: short summary`. Never commit `.env` or secrets.

---

## S5-11 — Optional AiInsight cache

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 2       |
| **Priority**   | Stretch |
| **Estimate**   | M       |
| **Depends on** | S5-08   |

### New here: caching generated insights

An optional **`AiInsight`** row stores generated content so demos do not re-call the model for the same user/period every refresh. Key by user + period (+ `prompt_version`). Do **not** block Must tickets for this.

Caching reduces flaky demos and load. Bump `prompt_version` when prompts change so stale text is not reused forever.

**Docs & tutorials:**

- Alembic revision habits from Sprint 2–3
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/) — new model + relationship to User

### Your task

Add an optional user-scoped cache for generated insights keyed by user + period (+ prompt version). Your deliverable is a model + migration and documented reuse vs refresh behavior—skip this if Must tickets are still open.

### Instructions

1. Add an `AiInsight` model (`user_id`, `period_start`/`end`, `prompt_version`, `content_json`) plus Alembic migration.
2. Key the cache by user + period (+ prompt version).
3. Document when a cached insight is reused vs refreshed (optional force-refresh flag).
4. Keep rows user-owned (same ownership rules as sessions/goals).

### Stay in scope

- Do not block S5-08–S5-10 or Week 3 Must tickets on this cache.
- Do not cache another user’s insights under the wrong user id.
- Leave rate limits for Sprint 6. A cache is not a substitute for throttling.
- Skip this ticket entirely if you are short on time.

### Hints

- Provide a force-refresh query/body flag if demos need a fresh call.

### Acceptance criteria

- [ ] Migration + model exist
- [ ] Cache keyed by user + period (+ prompt version)
- [ ] Behavior documented (when reused vs refreshed)
- [ ] Rows are user-scoped

### Suggested paths

`backend/app/models/ai_insight.py`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-11` in the message, for example `S5-11: short summary`. Never commit `.env` or secrets.

---

## S5-12 — Insights page

| Field          | Value   |
| -------------- | ------- |
| **Type**       | feature |
| **Week**       | 3       |
| **Priority**   | Must    |
| **Estimate**   | M       |
| **Depends on** | S5-08   |

### New here: Insights as a protected page

An auth-gated **Insights** route is the standout UI surface: pick period, optional focus, submit, wait for structured coaching. Reuse protected layout + TanStack Query patterns from Sprints 2–4.

Without a page, classmates cannot demo the feature end-to-end. Prefill `week` for a quick demo.

**Docs & tutorials:**

- [TanStack Query — Mutations](https://tanstack.com/query/latest/docs/framework/react/guides/mutations) — POST generate
- [React Router](https://reactrouter.com/) — protected route (Sprint 2 pattern)

### Your task

Add a protected Insights page that posts to `/ai/insights` with period and optional focus. Your deliverable is the route + form + busy state—rendering of the four sections is S5-13.

### Instructions

1. Add an auth-gated Insights route (React Router).
2. Include period selector, optional focus field, and submit action calling `POST /ai/insights`.
3. Disable the form / show busy state while the request is in flight.
4. Do not accept or send another user’s id.

### Stay in scope

- Leave detailed four-section rendering for S5-13 (a simple JSON dump is acceptable temporarily).
- Leave polished error copy for S5-14 if you only have a busy state here.
- Do not auto-call the model on every page load (slow + noisy). POST on submit.
- Leave Dashboard CTA for S5-16. Leave rate-limit UX for Sprint 6.

### Hints

- POST fits better than GET for generate actions.
- Keep the page focused—one job: request and show insight.

### Acceptance criteria

- [ ] Auth-gated
- [ ] Calls `POST /ai/insights`
- [ ] Disabled/busy state while requesting

### Suggested paths

`frontend/src/pages/InsightsPage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-12` in the message, for example `S5-12: short summary`. Never commit `.env` or secrets.

---

## S5-13 — Render structured insight

| Field          | Value      |
| -------------- | ---------- |
| **Type**       | feature    |
| **Week**       | 3          |
| **Priority**   | Must       |
| **Estimate**   | M          |
| **Depends on** | S5-12, S5-09 |

### New here: four scannable sections

Display **`summary`**, **`strengths`**, **`recommendations`**, and **`caveats`** as distinct sections. List fields as bullets. Caveats stay visible whenever the API returns them—do not bury warnings to “clean up” the demo.

Structured UI matches the API contract and keeps coaching honest about limitations.

**Docs & tutorials:**

- [MDN — Lists](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul) — accessible bullets
- Keep presentation simple; no new chart library required here

### Your task

Render the four insight fields as distinct, scannable sections. Your deliverable is presentation of `summary`, `strengths`, `recommendations`, and `caveats`—not a new API and not a chart library.

### Instructions

1. Display all four fields as distinct UI sections when present.
2. Render list fields as bullets.
3. Keep caveats visible whenever the API returns them.
4. Empty lists may hide their section; empty summary may show a short “No summary returned.”

### Stay in scope

- Do not strip caveats for aesthetics.
- Do not add a second chart library or rebuild Progress/Dashboard widgets here.
- Leave loading/error chrome for S5-14 if you only render the success payload here.
- Avoid card clutter; one clear result layout is enough.

### Hints

- Match field names to the API contract so mocks and live responses look the same.

### Acceptance criteria

- [ ] All four fields visible when present
- [ ] Lists render as bullets
- [ ] Caveats stay visible (do not hide warnings from the user)

### Suggested paths

`frontend/src/components/InsightResult.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-13` in the message, for example `S5-13: short summary`. Never commit `.env` or secrets.

---

## S5-14 — Loading and error UX

| Field          | Value      |
| -------------- | ---------- |
| **Type**       | feature    |
| **Week**       | 3          |
| **Priority**   | Must       |
| **Estimate**   | S          |
| **Depends on** | S5-12, S5-10 |

### New here: slow-model UX

Model calls are slow and sometimes fail. Soft-fail UX is half the demo: success path and “Ollama down” path without a white-screen crash. Re-enable submit after errors so retries are easy.

A crashy Insights page makes AI look broken even when sessions/stats are fine.

**Docs & tutorials:**

- [TanStack Query — Mutations status](https://tanstack.com/query/latest/docs/framework/react/guides/mutations) — `isPending` / `isError`
- [MDN — ARIA busy](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-busy) — optional a11y polish

### Your task

Show a spinner while the model runs and an actionable error when it fails—without crashing the UI. Your deliverable is loading + error states on Insights so the soft-fail demo works from the browser.

### Instructions

1. Show spinner/progress while waiting on the model.
2. On failure, show an actionable message (check Ollama / try later); surface API error text when present.
3. Ensure failures never become uncaught UI crashes.
4. Re-enable the submit button after errors.

### Stay in scope

- Do not block navigation to Sessions / Progress / Dashboard when AI fails.
- Leave rate-limit messaging for Sprint 6; 503/502 “Ollama down / timeout” is the Must path.
- Do not auto-retry in a tight loop.
- Leave Dashboard CTA for S5-16.

### Hints

- Align messaging with S5-10 status codes (503/502).

### Acceptance criteria

- [ ] Spinner/progress during request
- [ ] Error message actionable (e.g. check Ollama / try later)
- [ ] No uncaught UI crash on failure

### Suggested paths

`frontend/src/pages/InsightsPage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-14` in the message, for example `S5-14: short summary`. Never commit `.env` or secrets.

---

## S5-15 — Ollama setup docs

| Field          | Value      |
| -------------- | ---------- |
| **Type**       | docs       |
| **Week**       | 3          |
| **Priority**   | Must       |
| **Estimate**   | M          |
| **Depends on** | S5-01, S5-05 |

### New here: docs as Done

You already installed Ollama for yourself in [S5-01](#s5-01--install-ollama-locally). This ticket turns that into **classmate-facing** setup: if others cannot `ollama pull` and hit Insights, the feature does not exist for them. Docs are part of Done—same spirit as Sprint 1 README and Sprint 3 IDOR notes.

Demos fail more often on missing model / wrong `OLLAMA_BASE_URL` than on React bugs. Document host vs Docker networking.

**Docs & tutorials:**

- [Ollama — Download](https://ollama.com/download) — install
- [About READMEs (GitHub Docs)](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) — keep it scannable

### Your task

Write classmate-facing Ollama setup so someone else can pull the model, set env vars, and run the success + “AI down” demo. Your deliverable is docs linked from the root README, with the model name matching `.env.example`.

### Instructions

1. Document `ollama pull <model>`, env vars (`AI_PROVIDER`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`), and how to hit Insights.
2. Match the model name to the `.env.example` default.
3. List success and “AI down” demo steps; link from the root README.
4. Note common failures: model not pulled, wrong base URL, timeout too low.

### Stay in scope

- Depends on S5-01 and S5-05 only. You do **not** need the optional Compose profile (S5-06) to finish this ticket.
- If you did S5-06, you may mention the profile command as an optional extra—host install remains the primary documented path.
- Leave rate-limit / deployment runbooks for Sprint 6.
- Do not treat “read the source” as setup documentation.

### Hints

- Include both “Ollama on host” and “Ollama via Compose profile” only if you actually support the profile.
- Point back to Insights soft-fail behavior so graders know what to expect.
- Host URL from the API container is often `http://host.docker.internal:11434` vs `http://localhost:11434` on the host.

### Acceptance criteria

- [ ] Model name matches `.env.example` default
- [ ] Success and “AI down” demo steps listed
- [ ] Linked from root README

### Suggested paths

`README.md`, `docs/ollama.md`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-15` in the message, for example `S5-15: short summary`. Never commit `.env` or secrets.

---

## S5-16 — Dashboard CTA to Insights

| Field          | Value                      |
| -------------- | -------------------------- |
| **Type**       | feature                    |
| **Week**       | 3                          |
| **Priority**   | Should                     |
| **Estimate**   | S                          |
| **Depends on** | S5-12, Sprint 4 Dashboard  |

### New here: discoverability from Dashboard

A simple “Get AI tip” (or similar) link from the **Dashboard** makes Insights discoverable during the full product demo. Place it near recent **sessions** or Sprint 4 stat widgets—not a second wall of promo clutter.

Graders follow the Dashboard path first. One clear CTA beats hidden nav-only discovery.

**Docs & tutorials:**

- Reuse Dashboard from [S3-17](sprint-03-tickets.md#s3-17--dashboard-recent-sessions) / [S4-13](sprint-04-tickets.md#s4-13--dashboard-stat-widgets)
- [React Router — Link](https://reactrouter.com/en/main/components/link) — in-app navigation

### Your task

Add a logged-in Dashboard call-to-action that navigates to Insights. Your deliverable is one clear link or button—not an auto-generated insight on every Dashboard load.

### Instructions

1. Add a Dashboard call-to-action linking to Insights.
2. Show it only to logged-in users (Dashboard is already protected).
3. Avoid leftover Sprint 1 placeholder clutter—replace or remove stale stubs.

### Stay in scope

- Do not auto-call `/ai/insights` on every Dashboard load (slow + noisy).
- Do not rebuild Dashboard widgets or Progress charts here.
- Leave rate limits for Sprint 6.
- One clear link/button is enough.

### Hints

- Place the CTA near recent sessions or stat widgets so the demo path is obvious.

### Acceptance criteria

- [ ] Link visible to logged-in users
- [ ] Navigates to Insights page
- [ ] Does not clutter Sprint 1-style placeholder leftovers

### Suggested paths

`frontend/src/pages/DashboardPage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-16` in the message, for example `S5-16: short summary`. Never commit `.env` or secrets.

---

## Stretch tickets

Optional extras after Must/Should. Same ticket shape; skip them if you are out of time.

## S5-S1 — SSE streaming

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | —            |
| **Priority**   | Stretch      |
| **Estimate**   | L            |
| **Depends on** | S5-08, S5-12 |

### New here: streaming tokens

**Server-sent events (SSE)** push tokens to the browser as they arrive so a long generation feels responsive instead of a silent spinner. You still keep auth and soft failure; if you parse at the end, do not break the structured final shape (`summary`, `strengths`, `recommendations`, `caveats`).

**Docs & tutorials:**

- [MDN — Server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) — SSE overview
- [FastAPI streaming](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse) — stream responses

### Your task

Stream tokens to the Insights UI as they arrive, without dropping auth or the four-field contract.

### Instructions

1. Stream from the API (SSE or equivalent) while the model generates.
2. Keep the request authenticated and user-scoped.
3. On failure, still fail softly (no crashed worker / white screen).

### Stay in scope

- Must Insights POST + structured JSON remain the default path.
- Rate limits still wait for Sprint 6.

### Hints

- You can stream tokens and still assemble the four fields at the end—do not invent a second response contract.

### Acceptance criteria

- [ ] Insights UI shows tokens as they arrive (SSE or equivalent)
- [ ] Request stays authenticated and user-scoped
- [ ] Final shape still has `summary`, `strengths`, `recommendations`, `caveats`
- [ ] Failure is soft (no crashed worker / white screen)

### Suggested paths

`backend/app/api/ai.py`, `frontend/src/pages/InsightsPage.tsx`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-S1` in the message, for example `S5-S1: short summary`. Never commit `.env` or secrets.

---

## S5-S2 — Model picker

| Field          | Value        |
| -------------- | ------------ |
| **Type**       | feature      |
| **Week**       | —            |
| **Priority**   | Stretch      |
| **Estimate**   | M            |
| **Depends on** | S5-01, S5-05 |

### New here: local model selection

Let the user pick a **local** Ollama model (Settings or similar) instead of editing `.env` every time. Persist the choice carefully so the documented default still matches classmate setup. This stays local-only—no cloud billing.

**Docs & tutorials:**

- [Ollama API — List Local Models](https://github.com/ollama/ollama/blob/main/docs/api.md#list-local-models) — tags / list endpoint
- Env / factory from [S5-05](#s5-05--provider-factory-and-env)

### Your task

Add a local model picker whose default still matches docs / `.env.example`.

### Instructions

1. List local Ollama models (tags API) in Settings.
2. Persist the choice without breaking the documented default.
3. Keep Cloud stub non-functional when selected.

### Stay in scope

- Cloud stub stays non-functional when selected. Do not require a paid API.
- Skip if Must docs (S5-15) are not done.

### Hints

- Fall back to the `.env` model name when the picker has no stored choice.

### Acceptance criteria

- [ ] Settings lists local Ollama models
- [ ] Choice persists without breaking the documented default
- [ ] Cloud stub remains non-functional when selected

### Suggested paths

`frontend/src/pages/SettingsPage.tsx`, `backend/app/api/ai.py`, `backend/app/services/ai/`

### Commit

When this ticket is done, create a **new Git commit** for it. Do not mix unrelated tickets in the same commit. Put `S5-S2` in the message, for example `S5-S2: short summary`. Never commit `.env` or secrets.

---

## Related

- Previous tickets: [sprint-04-tickets.md](sprint-04-tickets.md)
- Next tickets (optional): [sprint-06-tickets.md](sprint-06-tickets.md)
- Index: [../README.md](../README.md)
