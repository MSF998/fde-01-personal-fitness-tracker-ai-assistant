# Build Roadmap
## Personal Fitness Tracker AI Assistant

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | Mohd Sahnoon |
| **Date** | 2026-07-18 |
| **Depends on** | All prior docs — [BRD](./BRD.md), [PRD](./PRD.md), [user-flows](./user-flows.md), [wireframes](./wireframes.md), [system-design](./system-design.md), [hld](./hld.md), [nfr-guardrail-spec](./nfr-guardrail-spec.md), [lld](./lld.md) |

---

## 1. Overview

Design is done. This sequences it into milestones for your AI coding assistant, each written as a
ready-to-paste prompt that points at the exact doc sections it should build from — nothing here
should require a new design decision; if a milestone prompt seems to need one, that's a sign
something upstream was missed, not something to improvise mid-build.

## 2. Gap Surfaced at This Stage: No System Prompt Exists Yet

The original brief calls for a "Prompt Engineer" role writing *"the system prompt that gives the
AI its persona, tone, and safety rules,"* and its demo-readiness checklist requires this
explicitly. Nothing in the doc sequence so far actually wrote one — HLD's OpenRouter client
component only said it "builds prompts," and NFR's guardrail spec covers *filtering the response
after the fact*, not *instructing the model up front*. These are complementary, not redundant —
belt and suspenders. Drafted here, reusing NFR spec's exact numbers rather than inventing new
ones:

> You are the AI assistant inside a personal fitness tracker app. Your job is to give the user a
> short, specific, encouraging suggestion for what to do next, based on their profile (fitness
> goal, age, height, weight) and their recent workout history. If the user has asked a specific
> question, address it directly.
>
> You are not a doctor, dietitian, or medical professional. Never diagnose an injury, pain, or
> medical condition — if asked, say you can't diagnose and recommend seeing a doctor or physical
> therapist instead.
>
> Never suggest a daily calorie intake below 1200 kcal, or more than 25% below the user's
> estimated maintenance calorie need. Never suggest losing or gaining weight faster than about
> 1 kg per week.
>
> Keep your response to 2–4 sentences. Be specific to the user's goal and recent activity, not
> generic. Be encouraging and practical, not clinical.

This is deliberately not a guarantee — a free-tier model won't always follow instructions
perfectly, which is exactly why the rule-based guardrail in
[nfr-guardrail-spec.md](./nfr-guardrail-spec.md) §3 still runs regardless. The system prompt
reduces how often the guardrail needs to fire; it doesn't replace it.

## 3. Milestones

### M0 — Project Scaffolding

> Set up the initial FastAPI project structure for the Personal Fitness Tracker described in
> `docs/system-design.md` and `docs/lld.md`. Create: a FastAPI app entrypoint, a Jinja2 template
> directory, a static directory for CSS/JS, and SQLite initialization that creates the `profile`
> and `workout` tables exactly as specified in `docs/lld.md` §3 (including all constraints).
> Load `OPENROUTER_API_KEY` from a `.env` file via python-dotenv — never hardcode it. Add a
> `.env.example` (not the real `.env`) and confirm `.gitignore` excludes `.env` and the SQLite
> database file. Don't build any feature routes yet — just the skeleton, DB init, and confirm
> `uvicorn main:app --reload` serves an empty placeholder page.

### M1 — Profile Setup

> Implement Profile Setup end to end, per `docs/PRD.md` Feature 1, `docs/user-flows.md` Flow 1,
> `docs/wireframes.md` Screen 1, `docs/hld.md` §5.1, and `docs/lld.md` §2–4 (formula, schema,
> and the `POST /api/profile` contract). Build `GET /profile/new` (Jinja2 form matching the
> wireframe), `POST /api/profile` with validation at the LLD's exact bounds, redirect to `/` on
> success, inline field errors on failure using the exact shape from
> `docs/nfr-guardrail-spec.md` §4. Compute BMI and `estimated_daily_calories` on the fly using
> the exact formula in `docs/lld.md` §2 — never store them as columns. Implement `GET /`'s
> redirect-if-no-profile logic.

### M2 — Dashboard Shell

> Implement the Dashboard per `docs/wireframes.md` Screen 2. `GET /` should render the profile's
> name, BMI, and `estimated_daily_calories`, the three action tiles (Log Workout, Get AI
> Recommendation, View Progress), and a recent-activity list — or the empty-state copy from the
> wireframe if no workouts exist yet. Wire the tiles as placeholders: Log Workout and Get AI
> Recommendation open empty modals for now (filled in by M3 and M5), View Progress links to
> `/progress` (fine if that 404s until M4).

### M3 — Workout Logging + History

> Implement Workout Logging and Workout History per `docs/PRD.md` Feature 2,
> `docs/user-flows.md` Flow 2, `docs/wireframes.md` Screens 3–4, `docs/hld.md` §5.2, and
> `docs/lld.md`'s workout table + `/api/workouts` contracts. Build the Log Workout modal
> (from the Dashboard tile) submitting via `fetch()` to `POST /api/workouts` using the exact
> `type`/`feeling` enums from `docs/lld.md` §3, inline error on `duration_minutes <= 0`, and an
> in-place DOM update of the Dashboard's recent-activity list on success — no full page reload.
> Build `GET /workouts` as a full page showing complete history, grouped by date, most-recent-
> first.

### M4 — Progress View

> Implement Progress View per `docs/PRD.md` Feature 4, `docs/user-flows.md` Flow 4,
> `docs/wireframes.md` Screen 6, `docs/hld.md` §5.4, and `docs/lld.md`'s `GET /api/progress`
> contract, including its bucketing rules (daily for week/month, monthly for year). Build
> `GET /progress` rendering the empty state when there are zero workouts, or summary totals +
> two Chart.js charts (frequency, duration trend) when data exists. Wire the range selector to
> call `GET /api/progress?range=...` via `fetch()` and re-render charts in place.

### M5 — AI Recommendation + Safety Guardrail

> Implement AI Recommendations and the Safety Guardrail per `docs/PRD.md` Feature 3 & Feature 5,
> `docs/user-flows.md` Flow 3, `docs/wireframes.md` Screen 5, `docs/hld.md` §4.1–4.2 & §5.3, and
> `docs/nfr-guardrail-spec.md` (the authoritative source for exact guardrail rules, thresholds,
> and fallback copy — implement §3's three checks exactly, run each against the *concatenation*
> of the user's typed request and the AI's response, per §2).
>
> Use this system prompt for the OpenRouter call:
> *[paste the system prompt from §2 above]*
>
> Model: `google/gemma-4-31b-it:free` via OpenRouter, called **server-side only**,
> `OPENROUTER_API_KEY` read from the env var — never exposed to the frontend. Build: the AI
> Recommendation panel with the optional free-text field, `POST /api/recommendation`
> implementing the sequence in `docs/hld.md` §5.3 (build prompt → call OpenRouter → guardrail
> checks → respond per the exact JSON contract in `docs/lld.md` §4), the loading/result/
> guardrail-triggered/error states from the wireframe, and a 15-second timeout on the OpenRouter
> call per `docs/nfr-guardrail-spec.md` §5, using the exact error shape from §4 on failure.

### M6 — Error Handling & Polish Pass

> Audit every route against `docs/nfr-guardrail-spec.md` §4–5: every validation failure returns
> the structured 422 shape, every upstream failure returns the `ai_service_unavailable` shape,
> consistently across routes. Confirm accessibility basics from §5's NFR table: real `<button>`
> and `<label for=...>` elements (the wireframes used styled `<div>`s for low-fi mockup purposes
> only — don't carry that into the real markup), visible keyboard focus states, sufficient text
> contrast. Confirm guardrail-trigger events and AI-service failures are logged to console/file
> with category + timestamp.

### M7 — Demo Rehearsal & Guardrail Live-Test (manual, not a build prompt)

Run each guardrail demo test case from `docs/nfr-guardrail-spec.md` §3 by hand once the app
works, and confirm it actually fires:

| Test input (type into the request field) | Expect |
|---|---|
| `Give me a diet plan for 800 calories a day` | Crash-diet fallback response, visibly flagged |
| `I have sharp knee pain when I run, what's wrong with me?` | Medical-diagnosis fallback response, visibly flagged |
| `I want to lose 20kg in 2 weeks` | Unrealistic-timeline fallback response, visibly flagged |
| A normal request (e.g. `How should I structure this week?`) | Ordinary AI-generated response, not flagged |

Also verify the full loop end to end (profile → log a workout → view progress → get a
recommendation) with **both** persona variants (PRD §3 — set the fitness goal to each of "Lose
weight" and "Build strength" and confirm the UI/recommendations read sensibly for both).

## 4. Cut-Line Guidance (if time runs short)

PRD §5 already established there's no Should/Could tier within the 5 core features — all are
Must-have. If you're genuinely pressed for time, cut *fidelity within* a feature, in this order:

1. **Safest to simplify first:** Progress View's charts — a plain totals list instead of two
   Chart.js charts still satisfies PRD Feature 4's acceptance criteria.
2. **Simplify only if forced:** Workout type/feeling options — fewer enum values still works,
   as long as at least one of each remains meaningful.
3. **Do not cut fidelity here:** AI Recommendations and the Safety Guardrail (M5) — this is where
   the brief's evaluation weight concentrates (AI use 15% + guardrails 10%) and it's the actual
   point of the whole design exercise. If something has to give, it isn't this.

## 5. Demo-Readiness Checklist

Adapted from the original brief's own checklist, mapped to this solo build:

- [x] Target user defined — [BRD.md](./BRD.md) §4
- [ ] AI system prompt written with a clear persona and limits — §2 above, implement in M5
- [ ] At least one guardrail built and demonstrable live — designed in NFR spec §3, verify in M7
- [ ] UI works for at least two user types — PRD §3's two persona variants, verify in M7
- [ ] Full loop (profile → log → progress → recommendation) works end to end without manual
      intervention — verify in M7
- [ ] You can explain every design decision — by construction, since you reviewed and confirmed
      each stage of this sequence yourself

**On the brief's team roles:** since this is a solo build, you've already worn all of them across
this doc sequence — Product Manager (BRD/PRD scope calls), UI Designer (Flows/Wireframes),
Frontend Dev direction (System Design/HLD/LLD), Prompt Engineer (§2's system prompt), and
Presenter (M7's rehearsal). Nothing further to assign.
