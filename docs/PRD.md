# Product Requirements Document (PRD)
## Personal Fitness Tracker AI Assistant

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | Mohd Sahnoon |
| **Date** | 2026-07-18 |
| **Depends on** | [BRD.md](./BRD.md) |

---

## 1. Overview

This PRD translates the BRD's objectives into concrete features, user stories, and testable
acceptance criteria for the 5 in-scope features: User Profile Setup, Workout/Activity Logging,
AI Recommendations, Progress View, and a Safety Guardrail.

## 2. Goals (from BRD, made concrete)

- The full loop — profile → log → progress → AI recommendation — works end-to-end.
- AI Recommendations ship as **MVP**, not a stretch feature — this overrides `breakdown.md`'s
  earlier "secondary" classification. The brief lists it as a core suggested feature and it
  carries 15% of the evaluation weight, so it's in the first build.
- The safety guardrail is demonstrable live against a specific, known input (see Feature 5).

## 3. Personas

**Primary persona (from BRD):** Busy professional, 25–45, exercises 1–4x/week inconsistently,
wants low-friction tracking + light guidance.

**Decision made — flag for review:** the brief's demo checklist requires the UI to "work for at
least two different types of users." Rather than introduce a second persona that conflicts with
the BRD's single-persona scope, this PRD uses **two variants of the same primary persona**,
differentiated by fitness goal:

| Variant | Goal | Implication for design |
|---|---|---|
| A — Weight loss | "Lose weight" | Recommendations and guardrail lean toward calorie/deficit safety checks |
| B — Strength | "Build strength" | Recommendations lean toward progressive overload, less calorie-focused |

Both are demoed by switching the profile's fitness goal field — no separate onboarding flows
needed. *(If you want a genuinely distinct second persona — e.g. a true beginner vs. an
experienced lifter — say so and I'll revise this section before we go further.)*

## 4. Features, User Stories & Acceptance Criteria

Acceptance criteria are written Given/When/Then — each one should be directly checkable during
your demo or by the AI coding assistant during implementation.

### Feature 1 — User Profile Setup

**User stories**
- As a user, I want to enter my name, age, and fitness goal so the app can personalize my experience.
- As a user, I want to store my height and weight so the app can calculate BMI and estimated calorie needs.

**Acceptance criteria**
1. Given a new user with no profile, when they complete the form with valid name, age, goal, height, and weight, then the profile is saved and they're routed to the dashboard.
2. Given a user enters an invalid value (negative/zero age, negative or absurd height/weight), when they submit, then an inline validation error appears and the form is not submitted.
3. Given a saved profile, when the dashboard loads, then it displays calculated BMI and an estimated daily calorie need.

### Feature 2 — Workout / Activity Logging

**User stories**
- As a user, I want to record what I did, for how long, and how it felt, so I have a history of my activity.
- As a user, I want to view my workout history so I can see what I've logged.

**Acceptance criteria**
1. Given a logged-in user, when they submit a workout entry with type, duration, and how it felt, then the entry is saved with a timestamp and appears in their history.
2. Given a workout entry with an invalid value (duration ≤ 0), when submitted, then a validation error is shown and the entry is not saved.
3. Given at least one past workout exists, when the user opens their history, then entries are listed most-recent-first with type, duration, and how it felt.

### Feature 3 — AI Recommendations (MVP)

**User stories**
- As a user, I want AI-generated suggestions based on my profile and activity history, so I know what to do next.
- As a user, I want to optionally type a specific request (e.g. a diet or timeline question), so the AI addresses what I actually asked instead of only generic profile-based suggestions.

**Acceptance criteria**
1. Given a user with a saved profile and at least one logged workout, when they request a recommendation, then the response references their specific goal and recent activity — not generic boilerplate.
2. Given a user with a profile but zero logged workouts, when they request a recommendation, then the response is an appropriate starter suggestion, not an error.
3. Given the AI service call fails or times out, when a recommendation is requested, then the user sees a graceful error message, not a broken UI state.
4. Given a recommendation is generated, when it is displayed, then it is visibly labeled as AI-generated and includes a disclaimer that it isn't medical advice (ties to BRD ethics/transparency intent).
5. Given a user types a free-text request into the optional request field before requesting a recommendation, when they submit, then the AI's response addresses that specific request rather than ignoring it.

> **Amendment (2026-07-18):** AC5 and the second user story were added when drafting the NFR &
> Guardrail Spec exposed a gap — Feature 5's guardrail ACs describe a user *asking*/*requesting*
> something unsafe, but no free-text input existed anywhere in the design for a user to actually
> do that. Without it, the guardrail wasn't demoable by typing a bad request, only by hoping the
> AI spontaneously generated unsafe content. See [wireframes.md](./wireframes.md) Screen 5 and
> [user-flows.md](./user-flows.md) Flow 3 for the corresponding amendments.

### Feature 4 — Progress View

**User stories**
- As a user, I want to see how much I've accomplished, so I can tell if I'm making progress.

**Acceptance criteria**
1. Given a user with logged workouts, when they open the progress view, then they see a summary (total workouts, total duration/volume) and at least one chart.
2. Given a user with zero logged workouts, when they open the progress view, then an empty state with a "log your first workout" call-to-action is shown — not a blank or broken screen.
3. Given the user changes the time-range filter, when applied, then the displayed data updates to reflect only that range.

### Feature 5 — Safety Guardrail

Scope decided: the guardrail must catch **(a)** extreme calorie deficits / crash-diet framing,
**(b)** requests for medical diagnosis, and **(c)** unrealistic goal timelines. (Overtraining/
excessive-volume checks were considered and explicitly deferred — not in this iteration's scope.)

**User stories**
- As a user, I want the AI to refuse or redirect harmful or unrealistic requests, so I'm not given advice that could hurt me.

**Acceptance criteria**
1. Given a request implies an extreme calorie deficit or crash-diet framing, when the AI would generate a recommendation, then the guardrail intercepts it and returns a safe, bounded alternative instead of the raw suggestion.
2. Given a user asks the AI to diagnose pain, injury, or a medical condition, when the AI would respond, then the guardrail redirects to "consult a medical professional" and does not provide a diagnosis.
3. Given a user sets or requests an unrealistic goal timeline (e.g. "lose 20kg in 2 weeks"), when a recommendation is generated, then the guardrail flags the timeline as unrealistic and suggests a safer pace.
4. Given any guardrail trigger fires, when the adjusted response is shown to the user, then the app is transparent that a safety check modified the response — it is not silently swapped with no indication.

## 5. Prioritization (MoSCoW)

| Priority | Features |
|---|---|
| **Must have** | User Profile Setup, Workout/Activity Logging, AI Recommendations, Progress View, Safety Guardrail |
| **Should have** | — (none; all 5 brief features are must-have for this iteration) |
| **Could have** | Goals & streaks tracking, predefined workout plans/scheduling — deferred per BRD out-of-scope |
| **Won't have (this iteration)** | Multi-user accounts, native mobile, wearable integrations, payments |

There is no "should/could" tier within the 5 core features — if time runs short, cut fidelity
within a feature (e.g. fewer chart types in Progress View) rather than dropping a whole feature,
since all 5 are directly tied to the evaluation criteria in the brief.

## 6. Assumptions Carried Into System Design

These are decisions implied by scope but not yet explicitly confirmed — flagging before we move
downstream, since they materially affect the System Design stage:

1. **No authentication/login system.** BRD scope excludes multi-user accounts, which implies a
   single-user app (local profile, no account creation/sign-in). If that's wrong, say so now —
   it changes the System Design significantly.
2. **Data persistence is local to the single user** — no need for multi-tenant data isolation.
3. **"Fitness goal" here is a static profile field** (e.g. "lose weight"), distinct from the
   dynamic "Goals & streaks" feature in `breakdown.md`, which is out of scope this iteration.

## 7. Out of Scope

Unchanged from BRD §5 — restated here for completeness: multi-user accounts/social features,
native mobile apps, wearable integrations, payments/monetization, real medical diagnosis.

## 8. Open Questions

- Confirm the two-persona-variant resolution in §3, or provide a genuinely distinct second persona.
- Confirm the "no auth" assumption in §6 before System Design begins.
