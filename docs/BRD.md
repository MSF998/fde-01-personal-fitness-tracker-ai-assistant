# Business Requirements Document (BRD)
## Personal Fitness Tracker AI Assistant

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | Mohd Sahnoon |
| **Date** | 2026-07-18 |
| **Type** | Learning project (portfolio/practice) |

---

## 1. Purpose

Build a web-based fitness tracker that helps users log workouts, track progress, and receive
AI-generated recommendations — as a personal learning project to practice product thinking and
system design, with the app implemented end-to-end by an AI coding assistant under the owner's
direction.

This is **not** a commercial venture. There is no business model, revenue target, or external
stakeholder to satisfy. The "business" objective is the owner's own learning and a working demo.

## 2. Background / Problem Statement

Busy professionals want to stay active but struggle to:
- Keep a consistent, low-friction record of what they actually did (workouts are often forgotten
  or logged inconsistently in notes apps / spreadsheets)
- Understand whether they're making progress without manually crunching numbers
- Get guidance on what to do next without hiring a coach or parsing generic fitness content that
  doesn't account for their own history

A lightweight tracker that logs activity, visualizes progress, and gives personalized
next-step suggestions addresses this gap for someone who wants structure without overhead.

## 3. Objectives

1. Produce a working web app that demonstrates the full loop: **log activity → see progress →
   get a personalized recommendation** — safely and transparently.
2. Use this build as a vehicle to practice real system design — BRD through LLD — before writing
   any code, rather than jumping straight to implementation.
3. Have a demo-able artifact at the end: something that can be shown end-to-end in a few minutes.

## 4. Target User

**Primary persona:** A busy professional (25–45) who exercises somewhat regularly (1–4x/week) but
inconsistently, has limited time to plan workouts or analyze their own data, and wants a simple
tool that tells them "here's what you did, here's your progress, here's what to do next" without
requiring a personal trainer or a complex app.

They are not a competitive athlete and not a complete beginner — they know how to work out, they
just want low-friction tracking and light guidance layered on top.

## 5. Scope

### In scope (matches the hackathon brief's suggested features)
- User profile setup (name, age, fitness goal, physical stats)
- Workout / activity logging
- AI-generated recommendations based on profile + log history
- Progress view (visualize what's been done)
- At least one safety guardrail against harmful or unrealistic AI advice

### Out of scope (for this iteration)
- Multi-user accounts, social features, sharing/competing with others
- Native mobile apps (web only)
- Wearable/device integrations (Apple Health, Fitbit, etc.)
- Payments, subscriptions, or any monetization
- Real medical/clinical advice or diagnosis of any kind

Anything beyond the hackathon's 5 suggested features is explicitly deferred unless a future
BRD revision brings it back in.

## 6. Success Criteria

Since this is a demo/learning project, success is defined as:
- The full loop (profile → log → dashboard → AI recommendation) works end-to-end without manual
  intervention.
- The AI guardrail can be demonstrated live — i.e., you can show an unsafe/unrealistic input
  being caught and handled gracefully.
- The app is understandable and navigable by someone seeing it for the first time (a "busy
  professional" persona, not a power user).
- You (the owner) can explain every design decision — why a screen, flow, or data model looks the
  way it does — because you produced the design docs yourself.

There is no target user count, retention metric, or performance SLA — those belong to a real
product, not a learning demo.

## 7. Constraints & Assumptions

- **Team:** Solo build. One person owns product, design, and review; an AI coding assistant
  (Claude Code) performs implementation under direction.
- **Budget:** No budget beyond whatever AI API usage costs are already available to the owner.
  No paid infrastructure, no paid third-party services.
- **Platform:** Web application only, no native mobile.
- **Timeline:** No hard deadline; paced by the owner's availability for iterative design review.
- **Assumption:** The AI coding assistant will implement faithfully from the LLD once it exists —
  design quality directly determines build quality, which is why the upfront design work matters
  here.

## 8. Stakeholders

| Role | Who |
|---|---|
| Product owner / decision-maker | You (Mohd Sahnoon) |
| Implementation | AI coding assistant, directed by you |
| End user (persona, for design purposes) | Busy professional, 25–45 |
| Reviewer of design docs at each stage | You |

## 9. Risks

| Risk | Mitigation |
|---|---|
| Scope creep beyond the 5 core features slows down getting to a demo-able build | Explicit out-of-scope list above; revisit only after MVP works |
| AI recommendations give unsafe/unrealistic advice (extreme deficits, overtraining, medical claims) | Dedicated guardrail requirement carried through PRD → LLD as a first-class feature, not an afterthought |
| Design docs are too vague for the AI coding assistant to implement unambiguously | LLD stage will include concrete data models and API contracts, not just prose |
| Solo build means no second reviewer catches blind spots | Each stage reviewed against the original hackathon brief and this BRD before moving on |

## 10. High-Level Timeline

No fixed calendar dates. Sequence is design-doc-gated: each stage (PRD → Flows → Wireframes →
System Design → HLD → LLD → NFRs/Guardrails → Build Roadmap) is completed and reviewed before the
next begins, and before any implementation starts.
