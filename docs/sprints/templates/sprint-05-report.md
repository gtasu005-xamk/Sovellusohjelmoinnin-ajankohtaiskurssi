# Sprint 5 report — AI insights with Ollama

Copy this file to `docs/reports/sprint-05.md` in **your** repo and fill the blanks. Keep it a process log: no pasted source, no secrets, no API keys, no `.env` values.

| Field | Your answer |
| ----- | ----------- |
| **Dates** | |
| **Names** | |
| **Repo URL** | |
| **Branch** | |

Tickets: [sprint-05-tickets.md](../tickets/sprint-05-tickets.md) · Index: [../README.md](../README.md)

## Sprint goal

From the tickets: give users personalized feedback from local AI, with a clean path to a future cloud LLM. You are done when Ollama + history yields structured insight fields; downtime/timeout fails softly; a `CloudProvider` stub exists and `AI_PROVIDER` selects the provider; the Insights page renders results from **only** the logged-in user’s data; classmate-facing pull docs exist.

In your words (2–3 sentences): did you meet that, and what is still rough?

## Tickets

For **each** ticket fill **Status** and **PR / commit**.

Fill **Demonstration** only where this template includes that section. Follow the numbered steps exactly. Store images under `docs/reports/images/sprint-05/` using the suggested filename. Crop tokens and raw prompts (especially prompts that embed personal training history).

For **every** ticket: set **Used AI?** to `Yes` or `No` (coding assistants such as Cursor, ChatGPT, Copilot—not product Insights via Ollama alone). Write the sprint-level **AI usage** reflection at the end of this report (not under each ticket).

Skip stretch tickets you did not do. Stretch: Status, PR, and Used AI? for each stretch you did; add a Demonstration only where listed below. S5-11 remains Stretch—fill it only if you did that ticket.

### S5-01 — Install Ollama locally (Must)

- **Status:** Done / deferred (why):
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** On the host, run `ollama --version` and/or call the local tags/API (for example `http://localhost:11434`). Confirm a model is available if you already pulled one (`ollama list`).
  2. **Capture:** Terminal or browser screenshot of version/tags responding.
  3. **Must show:** Ollama installed and reachable (version and/or API/tags). You do **not** need the full model download progress bar.
  4. **Must not show:** Unrelated secrets; crop huge download logs if they clutter the proof.
  5. **Save as:** `docs/reports/images/sprint-05/s5-01-ollama.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-02 — AIProvider protocol (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S5-03 — Ollama provider (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** With Ollama up, run a successful generate/chat via your provider (small script, temporary call, or later `POST /ai/insights`).
  2. **Capture:** Screenshot of a successful response (terminal or `/docs`).
  3. **Must show:** Local Ollama returned a model response through your code path.
  4. **Must not show:** Full prompts that dump another user’s data; crop or redact long histories. No API keys (none required for local Ollama).
  5. **Save as:** `docs/reports/images/sprint-05/s5-03-ollama-provider.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-04 — Cloud provider stub (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S5-05 — Provider factory and env (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S5-06 — Optional Ollama Compose profile (Should)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** If you implemented the profile, start Compose with the `ollama` profile and show the service running. If you **skipped** this Should ticket, write `Skipped` in the caption and omit the image.
  2. **Capture:** `docker compose ps` (or equivalent) showing the ollama service—or note skipped.
  3. **Must show:** Profile running **or** an explicit skip note.
  4. **Must not show:** Secrets in Compose env output.
  5. **Save as:** `docs/reports/images/sprint-05/s5-06-compose-ollama.png` (omit if skipped)
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-07 — Context builder (Must)

- **Status:**
- **PR / commit:**
- **Used AI?** Yes / No

### S5-08 — AI insights endpoint (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** With Ollama up and session history for the logged-in user, call `POST /ai/insights` in `/docs`.
  2. **Capture:** Screenshot of a successful response in `/docs`.
  3. **Must show:** Authenticated success path for `/ai/insights` with Ollama available.
  4. **Must not show:** Full JWT; crop Authorize. Prefer not to paste huge raw prompts.
  5. **Save as:** `docs/reports/images/sprint-05/s5-08-insights-api.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-09 — Structured response parsing (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** From `/ai/insights` (or the Insights UI), show a parsed payload that includes `summary`, `strengths`, `recommendations`, and `caveats`.
  2. **Capture:** Screenshot of the JSON or UI sections naming all four fields.
  3. **Must show:** All four structured fields present (not a single undifferentiated blob of prose only).
  4. **Must not show:** Tokens or another user’s insights.
  5. **Save as:** `docs/reports/images/sprint-05/s5-09-structured.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-10 — Timeouts and soft failure (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Stop Ollama (or force a timeout). Call Insights (`/docs` or UI) and confirm a clear error. Then open Sessions and/or Progress and confirm they still load.
  2. **Capture:** Screenshot of the Insights error **and** Sessions or Progress still working.
  3. **Must show:** Soft failure on Insights; rest of the app remains usable.
  4. **Must not show:** Tokens or raw stack traces with secrets.
  5. **Save as:** `docs/reports/images/sprint-05/s5-10-soft-fail.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-11 — Optional AiInsight cache (Stretch)

Fill this block only if you did the cache stretch (otherwise skip).

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Show reuse of a cached insight vs a forced refresh (UI toggle, second identical request, or documented behavior).
  2. **Capture:** Screenshot proving cache hit vs refresh.
  3. **Must show:** Cache behavior distinguishable from a cold generate.
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-05/s5-11-cache.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-12 — Insights page (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** While logged out, confirm Insights is gated. Log in and open the Insights page.
  2. **Capture:** Screenshot of the auth-gated Insights page for the logged-in user.
  3. **Must show:** Insights route available only when authenticated.
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-05/s5-12-insights-page.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-13 — Render structured insight (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Generate an insight on the Insights page so all four fields render.
  2. **Capture:** Screenshot of the page with `summary`, `strengths`, `recommendations`, and `caveats` visible.
  3. **Must show:** All four fields on the page (labels or clear sections).
  4. **Must not show:** Tokens; crop unrelated PII if needed.
  5. **Save as:** `docs/reports/images/sprint-05/s5-13-insights.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-14 — Loading and error UX (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Trigger a request and capture the loading state. Then capture the downtime/timeout error state on the Insights page (Ollama stopped).
  2. **Capture:** Two screenshots (loading + error).
  3. **Must show:** Distinct loading UX and a friendly error on the page (not a blank crash).
  4. **Must not show:** Tokens or raw exception dumps with secrets.
  5. **Save as:** `docs/reports/images/sprint-05/s5-14-loading-error.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-15 — Ollama setup docs (Must)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the classmate-facing docs for installing Ollama, pulling a model, and setting URLs/env (`AI_PROVIDER`, Ollama base URL).
  2. **Capture:** Screenshot of that documentation section.
  3. **Must show:** Steps a classmate can follow without reading your source (`ollama pull`, ports/URLs).
  4. **Must not show:** Paid API keys (none should be required).
  5. **Save as:** `docs/reports/images/sprint-05/s5-15-ollama-docs.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### S5-16 — Dashboard CTA to Insights (Should)

- **Status:**
- **PR / commit:**
- **Demonstration:** (only if you did this ticket)
  1. **Do this:** Open Dashboard and use the link/CTA to Insights; confirm navigation works.
  2. **Capture:** Screenshot of the CTA and the Insights page after click.
  3. **Must show:** Dashboard entry point to Insights.
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-05/s5-16-cta.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

### Stretch (only if you did them)

For each stretch below that you completed: Status, PR / commit, Used AI? Add Demonstration for [S5-S1](../tickets/sprint-05-tickets.md#s5-s1--sse-streaming) (streaming UI) and [S5-S2](../tickets/sprint-05-tickets.md#s5-s2--model-picker). If you already filled S5-11 above, do not duplicate it here.

#### S5-S1 — SSE streaming (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Show streaming Insights UI updating as tokens arrive (or equivalent SSE demo).
  2. **Capture:** Screenshot or short sequence of streaming output.
  3. **Must show:** Streaming behavior distinct from a single final payload.
  4. **Must not show:** Tokens (JWT) or huge unredacted prompts.
  5. **Save as:** `docs/reports/images/sprint-05/s5-s1-streaming.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

#### S5-S2 — Model picker (if done)

- **Status:**
- **PR / commit:**
- **Demonstration:**
  1. **Do this:** Open the model picker; select a model; generate an insight.
  2. **Capture:** Screenshot of the picker and resulting insight.
  3. **Must show:** Model selection affecting the Insights request.
  4. **Must not show:** Tokens.
  5. **Save as:** `docs/reports/images/sprint-05/s5-s2-model-picker.png`
  6. **Caption (1–2 sentences):**
- **Used AI?** Yes / No

## How we worked

Sprint 5 is **three weeks**.

- **Week 1** (Ollama install, provider protocol, factory):
- **Week 2** (context, `/ai/insights`, structured parse, soft failure):
- **Week 3** (Insights UI + setup docs):
- Who did what:
- One blocker and how you unblocked it:

## Decisions

Two to four technical choices with why (for example timeout value, how you pack context, stub vs fake coaching).

1.
2.

## What we learned

Note what you actually used. Tools this sprint: Ollama, `AIProvider` protocol, httpx (or equivalent), Compose profiles (optional), structured JSON insights.

- What clicked:
- One thing you would do differently:

## Carry-over

Deferred Must/Should, stretch leftovers. Next is optional [Sprint 6 tickets](../tickets/sprint-06-tickets.md) (tests, security, deployment) or course handoff—say which you plan.

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

