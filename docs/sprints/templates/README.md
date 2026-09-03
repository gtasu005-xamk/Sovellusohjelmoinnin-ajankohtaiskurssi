# Sprint report templates

Use these files to document **how** you built each sprint—not a second README. Copy the matching template into **your** repo and fill the placeholders. Do not paste source code or secrets.

| Sprint       | Template                                   | Your filled copy            |
| ------------ | ------------------------------------------ | --------------------------- |
| 1            | [sprint-01-report.md](sprint-01-report.md) | `docs/reports/sprint-01.md` |
| 2            | [sprint-02-report.md](sprint-02-report.md) | `docs/reports/sprint-02.md` |
| 3            | [sprint-03-report.md](sprint-03-report.md) | `docs/reports/sprint-03.md` |
| 4            | [sprint-04-report.md](sprint-04-report.md) | `docs/reports/sprint-04.md` |
| 5            | [sprint-05-report.md](sprint-05-report.md) | `docs/reports/sprint-05.md` |
| 6 (optional) | [sprint-06-report.md](sprint-06-report.md) | `docs/reports/sprint-06.md` |

Sprint 6 only if you take that optional sprint.

Leave the files in this `templates/` folder blank in the course repo. Fill **your** copies under `docs/reports/`.

## What every ticket needs

1. **Status** — Done, or deferred with a short reason.
2. **PR / commit** — link or hash for that ticket’s commit(s).

### Demonstration (only where the template includes it)

Follow the numbered steps under **Demonstration** exactly. Do not invent a screenshot for plumbing, helpers, or review-only tickets that have no Demonstration section.

Each Demonstration uses this shape:

1. **Do this** — commands or clicks, in order
2. **Capture** — screenshot or short terminal paste
3. **Must show** — what graders need to see
4. **Must not show** — tokens, passwords, `.env`, full JWTs, raw AI prompts with secrets
5. **Save as** — path under `docs/reports/images/sprint-0N/` (for example `s1-03-health.png`)
6. **Caption** — 1–2 sentences stating what the image proves

Crop secrets before you commit images.

### Used AI? (every ticket)

For **every** ticket (including stretch you did):

- Set **Used AI?** to `Yes` or `No`.

“AI tools” means Cursor, ChatGPT, Copilot, local Ollama used for coding help, and similar assistants—not the product’s Sprint 5 Insights feature unless you also used an AI assistant to write the code.

### AI usage (once per sprint report)

At the **end** of each report template, fill the sprint-level **AI usage** section. Cover overall patterns for the sprint—not a ticket-by-ticket dump. If you marked **No** on every ticket, say so briefly.

Reflection prompts in that section:

- **Where AI helped most this sprint**
- **What I typically accepted**
- **What I typically rejected or reworked, and why**
- **How I verified AI-assisted work**
- **What I can now explain or do independently**
- **Anything I would do differently with AI next sprint**

Do not paste secrets, full JWTs, or `.env` values into reflection answers.
