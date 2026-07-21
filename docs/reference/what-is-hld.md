# What Is an HLD (High-Level Design)?

A reusable reference — not tied to any one project. Use this whenever starting a new project's
design docs from scratch, right after System Design is confirmed.

## Purpose

An HLD answers **"how does each component actually work, and how do the flows move through
them?"** System Design named the components and validated one representative flow; HLD breaks
every component into its internal responsibilities, defines the route/API-level contract (paths
and purpose, not full schemas), and produces a sequence diagram for *every* flow — not just a
sample. Its audience is anyone about to implement or review implementation: it's the last stop
before exact data shapes and field-level detail take over.

Where System Design answers "what components exist and how do they connect," HLD answers "what
does each one do, step by step, for every flow." It deliberately stops short of exact request/
response bodies, column types, and numeric thresholds — that's LLD (and, for anything safety/
guardrail-related, the NFR & Guardrail Spec stage in between).

**The test:** if a decision is about *the sequence of steps a component performs, or which route
handles what*, it's HLD-level. If it's about *exact field names, types, or numeric thresholds*,
that's LLD or the NFR/Guardrail Spec. If it's about *which components exist at all*, that already
happened in System Design — don't redecide it here.

## Standard Components

| Section | Answers | Guiding questions |
|---|---|---|
| **Overview** | What does this document resolve that System Design deferred? | Name the open questions being closed out here |
| **Decisions Locked In (HLD-level)** | What component-internal choices are being made, and why? | Same discipline as System Design's decisions table — every choice needs a reason |
| **Route-Level API Contract** | What are the actual endpoints, and what does each do? | Path, purpose, what it calls — not the request/response body shape yet |
| **Component Internals** | How does each non-trivial component work internally? | Break cross-cutting or multi-step components (a guardrail, a multi-stage validator) into their own diagram |
| **Sequence Diagrams (per flow)** | How does a request move through the system, for *every* flow? | One diagram per flow from User Flows — not just the hardest one, that was System Design's job |
| **Error Handling Pattern** | What consistent shape do failures take across routes? | Establish the pattern (e.g. "validation failures return 422 with field errors") without specifying the exact schema yet |
| **Open Questions** | What's still deferred, and to which later stage specifically? | Be precise about *which* stage owns each remaining gap — NFR/Guardrail Spec vs. LLD aren't interchangeable |

## How to Write Each Section Well

- **Resolve what System Design explicitly deferred — and only that, don't relitigate settled
  decisions.** System Design should have left a short, named list of open questions. HLD's first
  job is closing those out with a reasoned decision, not reopening the architecture itself.

- **Produce a sequence diagram for every flow, not just the hard one.** System Design traced one
  representative flow to validate the architecture holds up. HLD is where the remaining flows
  from [User Flows](./what-is-a-user-flow.md) each get their own diagram, now with actual route
  names and component calls instead of generic boxes — and still with the same discipline of
  including failure/validation branches, not just the happy path.

- **Give cross-cutting components their own internal diagram.** Something like a guardrail,
  multi-stage validator, or permission check often doesn't map to a single flow — it's invoked
  from multiple places. Diagram it once, on its own, rather than repeating its internals inside
  every sequence diagram that calls it.

- **Name routes and their purpose; don't specify their bodies yet.** "`POST /api/recommendation` —
  orchestrates the AI Recommendation flow" is HLD-level. The exact JSON shape of the request and
  response is LLD's job — pulling it in early tends to lock in field names before the NFR/
  guardrail spec (if one exists) has had a chance to shape them.

- **Establish patterns, not values.** "Validation failures return a structured error with
  field-level messages" is a pattern worth stating at HLD level, because every route should follow
  it consistently. The exact error-code vocabulary or JSON key names are values — defer them to
  whichever stage owns exact contracts.

- **Be specific about which later stage owns each open question.** "TBD" isn't good enough once a
  project has multiple downstream stages — say explicitly whether a gap belongs to LLD (data
  shapes), an NFR/Guardrail Spec (thresholds, safety rules), or the Build Roadmap (sequencing/
  cut lines), so nothing falls through a gap between two documents each assuming the other owns it.

## Common Mistakes to Avoid

1. **Re-deciding architecture that System Design already settled** — HLD should close open
   questions, not reopen closed ones.
2. **Only diagramming the flows that seem hard** — every flow from User Flows needs its own
   sequence diagram here, including the "boring" ones.
3. **Burying a cross-cutting component inside one flow's diagram** — if multiple flows call it,
   it deserves its own internal diagram.
4. **Specifying exact request/response schemas** — that's LLD's job; naming the route and its
   purpose is enough here.
5. **Vague open questions** — leaving a gap unattributed to a specific downstream stage, so it
   risks never being picked up by either LLD or the NFR spec.
6. **Skipping the failure path in a sequence diagram** — an HLD sequence diagram that only shows
   the success case doesn't reflect what the PRD's acceptance criteria actually require.

## Blank Template

```markdown
# High-Level Design (HLD)
## <Project Name>

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | |
| **Date** | |
| **Depends on** | system-design.md |

## 1. Overview

## 2. Decisions Locked In (HLD-level)

| Decision | Choice | Why |
|---|---|---|

## 3. Route-Level API Contract

| Method & Path | Purpose | Calls |
|---|---|---|

## 4. Component Internals

### 4.1 <Cross-cutting component>

\`\`\`mermaid
flowchart TD
    ...
\`\`\`

## 5. Sequence Diagrams (per flow)

### 5.1 <Flow name>

\`\`\`mermaid
sequenceDiagram
    ...
\`\`\`

## 6. Error Handling Pattern

## 7. Open Questions (deferred to <specific later stage>)
```

## Where This Fits in the Larger Design Sequence

**BRD → PRD → User Flows → Wireframes → UI/UX Design → System Design → HLD → NFRs & Guardrail
Spec → LLD → Build Roadmap**

HLD is the last stage before exact values take over. Everything through HLD is still about
*shape and sequence* — components, routes, steps, patterns. Starting with NFRs & Guardrail Spec,
the documents shift to *exact, testable values* (thresholds, schemas, response bodies) — which is
why HLD deliberately names patterns without filling in the numbers: filling them in here would
mean guessing at what the next stage should be deciding deliberately.
