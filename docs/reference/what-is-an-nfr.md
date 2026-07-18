# What Is an NFR (Non-Functional Requirement)?

A reusable reference — not tied to any one project. Use this whenever starting a new project's
design docs from scratch, right after HLD is confirmed.

## Purpose

An NFR document answers **"how well, and under what constraints, does the system do what the PRD
says it does?"** Functional requirements (the PRD) answer *what* the system does — log a workout,
generate a recommendation. Non-functional requirements answer *how* — how fast, how secure, how
it fails, what it costs to run, what bar of accessibility it meets. Same feature, different
question: "the app generates a recommendation" is functional; "the recommendation returns within
3 seconds" or "the API key is never exposed to the browser" is non-functional.

Its job at this point in the sequence is narrower than it sounds: turn the patterns HLD already
established (validation returns structured errors, a guardrail exists with named categories) into
**exact, testable values** — precise thresholds, exact JSON shapes, concrete keyword/pattern
lists. Nothing here should be a new architectural decision; that already happened in System
Design and HLD. If drafting this document surfaces something that changes the architecture,
that's a sign to go back and amend the earlier stage explicitly, not to quietly absorb it here.

**The test:** if a requirement is about *what the system does*, it's PRD-level, not here. If it's
about *what components exist or how they connect*, it's System Design/HLD-level, not here. If
it's about *an exact number, shape, or rule that makes a behavior checkable*, it belongs here.

## NFRs Aren't One Moment

Pieces of NFR-relevant scope typically surface throughout the whole sequence, as a side effect of
other decisions, well before a dedicated NFR document exists:
- **BRD constraints** (budget, timeline, platform) are NFRs in disguise.
- **PRD assumptions** (e.g. "no auth") are often NFR trade-offs dressed as functional scope calls.
- **System Design's architecture-level NFR notes** (concurrency model, secrets handling, failure
  isolation) are NFRs that would change the diagram if answered differently — they belong there,
  not deferred, because they're load-bearing for the architecture itself.

A dedicated NFR document isn't inventing something new — it's **consolidating** what's already
been decided piecemeal, and filling in what hasn't been addressed (performance targets,
accessibility bar, exact security/error contracts, the guardrail's precise rules if the project
has one).

## Standard Components

| Section | Answers | Guiding questions |
|---|---|---|
| **Overview** | What patterns is this document turning into exact values? | Name what HLD deferred here specifically |
| **Design Refinements (if any)** | Did writing exact specs expose a gap in an earlier stage? | Be honest about this — see below; don't silently patch it |
| **Guardrail/Safety Spec (if applicable)** | What are the precise, falsifiable trigger rules? | Exact thresholds, exact keyword/pattern lists, exact fallback behavior — each with a literal example that would trigger it |
| **API Contract (exact shapes)** | What does every error/response body actually look like? | Real JSON, not prose describing JSON |
| **NFR Table** | What's the bar for performance, security, accessibility, reliability, etc.? | One row per category: requirement + rationale — a number with no reason attached can't be revisited later |
| **Out of Scope** | What NFRs are explicitly not being designed for? | Name what's excluded (e.g. horizontal scaling, formal accessibility audit) so it isn't mistaken for an oversight |
| **Open Questions** | What's left for LLD? | Ideally very little — LLD should be implementing this spec, not making further judgment calls |

## How to Write This Document Well

- **Make every rule falsifiable, the same discipline as [what-is-a-brd.md](./what-is-a-brd.md)'s
  objectives.** "The
  guardrail should catch unsafe advice" isn't a spec. "Trigger if a calorie figure in the text is
  below 1200" is — you can type an input and check whether it fires.

- **Give every rule a literal test case.** Especially for anything that needs to be demoed live —
  a rule with no example input is a rule nobody has actually verified fires.

- **Write real JSON/schemas, not descriptions of them.** "Errors return a structured object with a
  code and message" is vague enough that two implementers would build it differently. Write the
  actual shape.

- **If writing the exact spec reveals a gap upstream, say so and fix it there — don't patch
  silently.** Trying to make something testable is often what exposes that it was never fully
  designed. If the fix changes an earlier document (a missing input field, a placement that turns
  out unreliable), amend that document explicitly with a dated note, then reference it here —
  same discipline carried through every stage of this sequence. A section of this document titled
  "Design Refinements" is a good place to be upfront about this rather than pretending the
  original design anticipated everything.

- **Test demoability specifically, not just correctness, for anything safety/guardrail-related.**
  A rule can be logically correct and still be undemoable — e.g. checking only a model's output
  for a behavior the model rarely exhibits on its own. If a guardrail needs to be shown working
  live, ask "what's the exact input I'd type to trigger this, right now, reliably" for every rule
  — if you can't answer that concretely, the rule isn't finished.

- **Only give a category a bar proportionate to the project's actual stakes.** A full WCAG AA
  audit or a formal load-testing pass is appropriate for a real product with real users; for a
  solo demo project, a lightweight, explicit bar ("semantic HTML, keyboard operable, visible
  focus") is more honest than padding the document with unearned rigor.

## Common Mistakes to Avoid

1. **Vague rules with no literal test case** — "handles unsafe input gracefully" instead of an
   exact trigger condition and example.
2. **Prose describing a schema instead of the schema itself** — ambiguity two implementers would
   resolve differently.
3. **Silently absorbing a design gap instead of fixing it upstream** — patching a missing
   capability inside the NFR doc instead of amending the PRD/flow/wireframe that should have had
   it, with a dated note explaining why.
4. **Correctness without demoability** — a rule that's technically right but relies on behavior
   that's unlikely to actually occur during a live demonstration.
5. **Over-speccing a category beyond the project's stakes** — formal audits and SLAs for a solo
   learning project that doesn't need them.
6. **Leaving real judgment calls for LLD** — LLD should implement this spec, not make further
   product decisions; if it would need to, that's unfinished NFR work.

## Blank Template

```markdown
# NFRs & Guardrail Spec
## <Project Name>

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | |
| **Date** | |
| **Depends on** | hld.md |

## 1. Overview

## 2. Design Refinements (if any)

## 3. Guardrail/Safety Spec (if applicable)

### 3.1 <Rule category>
**Trigger if:**
**Fallback:**
**Demo test case:**

## 4. API Contract (exact shapes)

\`\`\`json
{}
\`\`\`

## 5. Non-Functional Requirements

| Category | Requirement | Rationale |
|---|---|---|

## 6. Out of Scope

## 7. Open Questions (deferred to LLD)
```

## Where This Fits in the Larger Design Sequence

**BRD → PRD → User Flows → Wireframes → System Design → HLD → NFRs & Guardrail Spec → LLD →
Build Roadmap**

NFRs sit *after* HLD and *before* LLD, not at the end of the sequence — LLD's concrete data models
and API contracts should be written against a settled spec, not the reverse. Placing NFRs last
means LLD gets built without a spec to follow, and NFRs end up retroactively second-guessing
implementation decisions instead of driving them.
