# What Is an LLD (Low-Level Design)?

A reusable reference — not tied to any one project. Use this whenever starting a new project's
design docs from scratch, right after NFRs & Guardrail Spec is confirmed.

## Purpose

An LLD answers **"exactly what does the data look like, and exactly what does every contract
say?"** It's the stage where the sequence stops making judgment calls. Every schema, model, and
formula in an LLD should trace directly back to a decision an earlier stage already made — the
PRD's fields, HLD's routes, the NFR spec's exact rules. If something in an LLD doesn't trace back
to an earlier document, that's a sign it's a new decision sneaking in at the wrong stage, not a
detail being filled in.

Where the NFR & Guardrail Spec made behavior *testable* (exact thresholds, exact rules), LLD
makes it *implementable*: table schemas with real column types and constraints, request/response
models with real field names, and any remaining formulas needed to compute a value the app
displays. Its audience is whoever writes the code (human or AI) — it should be able to work from
this document without inventing a single field name, enum value, or bucketing rule.

**The test:** if a decision requires judgment about *what the product should do*, it's too late —
that belongs to an earlier stage. If it's *filling in the exact shape of something already
decided*, it's LLD. A genuinely new fork discovered while drafting the LLD (see below) should
still be resolved explicitly and flagged — it doesn't mean skip documenting it, it means be
honest that it's a real decision, not a formality.

## Standard Components

| Section | Answers | Guiding questions |
|---|---|---|
| **Overview** | What's being made exact here, and what (if anything) got resolved first? | Name any genuine fork that had to be settled before the rest could be written |
| **Formula Decisions** | Are there any derived values the app needs to compute? | Write the actual formula, not a description of it; state what's approximate and why |
| **Data Models (schema)** | What are the exact tables, columns, types, and constraints? | One table per entity named back in System Design; every constraint should trace to a PRD acceptance criterion or a sensible bound, not be invented arbitrarily |
| **API Request/Response Models** | What's the exact field-level shape of every request and response? | Real field names and types — this is what the frontend gets written against, so ambiguity here becomes a real bug later |
| **Cross-references to enums/contracts already fixed elsewhere** | Where do shared values (e.g. category names) come from? | Don't redefine something the NFR spec already named — reference it, so there's exactly one source of truth |
| **Open Questions** | What's left, and for which stage? | Should be close to empty — LLD is meant to close things out, not hand off further design work |

## How to Write Each Section Well

- **Resolve genuine forks explicitly, don't let them hide inside a formula.** Sometimes making a
  value exact (a formula, a computed field) surfaces a real decision an earlier stage didn't
  anticipate — e.g. a standard formula needing an input the PRD never collected. When this
  happens, resolve it deliberately (with a stated tradeoff) and say so in the Overview, rather
  than quietly picking a default and burying the reasoning in a footnote.

- **When a computed value feeds more than one consumer, define it once and think through every
  consumer before picking what it means.** If a derived figure (say, an estimated daily need) is
  displayed on a screen *and* used as a threshold somewhere else (a safety check), decide up front
  which variant — raw vs. adjusted — each consumer actually needs. Picking the wrong variant
  silently weakens or breaks the other consumer; this is worth a dedicated callout, not an
  assumption left implicit.

- **Field names here are authoritative, not illustrative.** Earlier stages could get away with
  prose ("the response includes a recommendation and whether the guardrail fired"). LLD cannot —
  write the literal field name (`guardrail_triggered`, not "a flag for whether it triggered"),
  because this is what code gets written against directly.

- **Every constraint needs a source.** A column's `NOT NULL, 13–100` bound should be traceable to
  either a PRD acceptance criterion ("positive, realistic number") or a stated, deliberately
  generous default reasoning — not an arbitrary number with no justification.

- **Treat empty states as a normal response shape, not an error.** If an earlier stage defined an
  empty state as part of a flow (no data yet), the corresponding LLD response should return the
  same shape with empty/zeroed values — not a special error code. Conflating "no data" with
  "something went wrong" undoes work already done upstream to treat empty states as first-class.

- **Reference shared vocabulary instead of redefining it.** If the NFR spec already named a set of
  category values, LLD's response model should say "these are exactly those three values" and
  link to them — not restate them independently, which risks the two documents drifting apart.

## Common Mistakes to Avoid

1. **New product decisions disguised as implementation detail** — deciding something that should
   have been a PRD/NFR call, but doing it silently while "just" writing a schema.
2. **Picking the wrong variant of a shared computed value** — using an adjusted figure where a raw
   one was needed (or vice versa) because the multiple consumers weren't thought through together.
3. **Vague field descriptions instead of literal names/types** — leaving ambiguity that different
   implementers (or an AI coding assistant on different days) would resolve differently.
4. **Unsourced constraints** — bounds or rules with no traceable justification.
5. **Treating an empty state as an error response** — breaking a distinction an earlier flow/
   wireframe stage deliberately established.
6. **Redefining values that already have a source of truth elsewhere** — restating an enum or
   category list instead of referencing where it's actually defined.

## Blank Template

```markdown
# Low-Level Design (LLD)
## <Project Name>

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | |
| **Date** | |
| **Depends on** | nfr-guardrail-spec.md |

## 1. Overview

## 2. Formula Decisions (if any)

## 3. Data Models (schema)

### `<table_name>`

| Column | Type | Constraint |
|---|---|---|

## 4. API Request/Response Models

**`<METHOD> <path>`**
\`\`\`
Request:  { }
Response: { }
\`\`\`

## 5. Open Questions (deferred to Build Roadmap)
```

## Where This Fits in the Larger Design Sequence

**BRD → PRD → User Flows → Wireframes → System Design → HLD → NFRs & Guardrail Spec → LLD →
Build Roadmap**

LLD is the last *design* document — everything after it (the Build Roadmap) is about sequencing
implementation, not deciding what the product does or how it's shaped. That's exactly why LLD's
"Open Questions" section should be nearly empty: if it isn't, something that should have been
settled by now is still unsettled, and the Build Roadmap will inherit a gap it isn't built to
close.
