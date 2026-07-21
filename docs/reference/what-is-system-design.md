# What Is System Design?

A reusable reference — not tied to any one project. Use this whenever starting a new project's
design docs from scratch, right after Wireframes are confirmed.

## Purpose

System Design answers **"what runs where, what talks to what, and why?"** It's the first stage
that moves from product/design language into engineering language: architecture shape, tech
stack, and how the major pieces connect. Its audience is anyone who needs to understand the
system's shape before diving into component-level detail — you, validating the architecture can
actually support the flows already defined, or an implementer who needs the big picture before
the component breakdown.

Where Wireframes answer "what's on each screen," System Design answers "what serves that screen,
and what does it talk to." It deliberately stays at the architecture level — naming components
and their responsibilities, not their internals. That's HLD next. And it names entities, not
schemas — that's LLD.

**The test:** if a decision is about *what component exists and what it's responsible for*, it's
System Design-level. If it's about *how a component works internally* (its sub-steps, its exact
sequence of calls), that's HLD. If it's about *exact data shapes* (columns, types, request/
response bodies), that's LLD.

## Standard Components

| Section | Answers | Guiding questions |
|---|---|---|
| **Overview** | What does this document decide, and what does it hand off to next? | One paragraph — architecture and stack, not component internals |
| **Decisions Locked In** | What are the concrete architectural choices, and why? | A table: decision, choice, rationale — every choice needs a reason, not just an answer |
| **Architecture Diagram** | How do the pieces connect? | One diagram (e.g. Mermaid flowchart) showing components and data flow between them |
| **Component Responsibilities** | What is each piece actually responsible for? | One row per component — if two components share a responsibility, the boundary is probably wrong |
| **Request Lifecycle (representative flow)** | Does the architecture actually support the hardest flow? | Pick the most architecturally interesting flow (usually the one with an external dependency or a conditional branch) and trace it end to end — validates the design before committing further |
| **Data Entities (named, not modeled)** | What are the core "things" the system persists? | Name them, don't schema them — full modeling is LLD |
| **Non-Functional Notes (architecture-level only)** | What NFRs directly shape this architecture? | Concurrency, secrets handling, failure isolation — anything that would change the diagram if answered differently. Full NFR treatment comes later; only capture what's load-bearing *here* |
| **Out of Scope** | What are we deliberately not designing for? | Scaling, caching, multi-tenancy, etc. — name what's excluded and why, so it isn't mistaken for an oversight |
| **Open Questions** | What's deferred to HLD/LLD? | Anything you considered but didn't decide — hand it off explicitly rather than leaving it implicit |

## How to Write Each Section Well

- **Every decision needs a reason, not just an answer.** "SQLite" isn't a decision until it's
  "SQLite, because zero-config and no hosting account fits the solo/no-budget constraint." The
  reason is what lets a reader (including future-you) evaluate whether the decision still holds
  when circumstances change.

- **Ground the stack choice in who owns the code, not just what's conventional.** The "standard"
  industry stack isn't automatically right for a solo project — if you're the one who has to read,
  debug, and extend this code, a stack you can actually reason about beats one that's merely
  popular. This is the same principle as [what-is-a-prd.md](./what-is-a-prd.md)'s ownership
  guidance, applied to technology choices.

- **Diagram the architecture, don't just describe it in prose.** A flowchart showing components
  and connections surfaces missing pieces and wrong boundaries faster than a paragraph will —
  drawing "Browser → API → Database" forces you to notice, for example, that an external AI call
  needs its own box, and that a guardrail has to sit somewhere specific in the data flow, not just
  "somewhere in the backend."

- **Trace one real flow through the architecture before moving on.** Don't just draw the static
  diagram — pick the flow with the most moving parts (usually the one touching an external
  service, or with a conditional branch) and walk a request through it step by step. If the
  architecture can't cleanly support that flow, better to find out now than during HLD.

- **Name entities, resist the urge to model them.** "Profile, Workout" is a System Design-level
  entity list. Columns, types, and constraints are LLD's job — pulling that detail in early tends
  to lock in decisions before the API contracts that should inform them exist.

- **Surface deviations from earlier decisions explicitly, don't silently absorb them.** If a new
  constraint conflicts with something already decided upstream (e.g. a brief that names a specific
  AI provider, and you're now using a different one), name the conflict, make the call, and record
  why — the same discipline carried through every stage of this sequence. A flagged, reasoned
  deviation is a decision; a silent one is scope drift.

- **Only capture NFRs that are load-bearing for the architecture itself.** Concurrency model,
  secrets handling, and failure isolation belong here because they'd change the diagram if
  answered differently. Performance targets, accessibility, and browser support don't need to be
  answered yet — defer them to a dedicated NFR stage rather than padding this document.

## Common Mistakes to Avoid

1. **Decisions without rationale** — a stack/architecture choice with no "why" can't be
   re-evaluated later when circumstances change.
2. **Defaulting to the "standard" stack without considering ownership** — picking what's
   conventional over what the actual owner can maintain.
3. **Describing architecture only in prose** — skipping the diagram, which is what actually
   surfaces missing components and wrong boundaries.
4. **Never tracing a real flow through the design** — discovering the architecture can't support
   a key flow only once HLD or LLD is underway.
5. **Modeling data instead of naming it** — writing full schemas here, which locks in detail
   before it's earned and duplicates LLD's job.
6. **Silently absorbing conflicts with earlier decisions** — swapping a provider, stack, or
   constraint without noting that it deviates from something already agreed.
7. **Padding with NFRs that don't affect the architecture** — turning this into a shadow NFR
   document instead of deferring non-architectural NFRs to their own stage.

## Blank Template

```markdown
# System Design
## <Project Name>

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | |
| **Date** | |
| **Depends on** | PRD.md, user-flows.md, wireframes.md |

## 1. Overview

## 2. Decisions Locked In

| Decision | Choice | Why |
|---|---|---|

## 3. Architecture Diagram

\`\`\`mermaid
flowchart LR
    ...
\`\`\`

## 4. Component Responsibilities

| Component | Responsibility |
|---|---|

## 5. Request Lifecycle — <representative flow>

\`\`\`mermaid
sequenceDiagram
    ...
\`\`\`

## 6. Data Entities (named, not modeled)

## 7. Non-Functional Notes (architecture-level only)

## 8. Out of Scope for This Design

## 9. Open Questions (deferred to HLD/LLD)
```

## Where This Fits in the Larger Design Sequence

**BRD → PRD → User Flows → Wireframes → UI/UX Design → System Design → HLD → NFRs & Guardrail
Spec → LLD → Build Roadmap**

System Design is the hinge point of the whole sequence — everything before it (including a
dedicated visual design pass, if the project has one) is product/design language, everything
after it is engineering language built on the shape decided here. Note NFRs
sit *after* HLD and *before* LLD, not at the very end: LLD's concrete API contracts and data
models should be written against a settled NFR/guardrail spec, not the reverse — getting this
order backwards means LLD gets built without a spec to follow, then NFRs retroactively second-
guess it.
