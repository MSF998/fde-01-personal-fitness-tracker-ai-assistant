# What Is a BRD (Business Requirements Document)?

A reusable reference — not tied to any one project. Use this whenever starting a new project's
design docs from scratch.

## Purpose

A BRD answers **"why are we building this, and what does the business/owner need from it?"**
before anything gets designed or built. Its audience is decision-makers and anyone downstream
(PM, designers, engineers) who need to understand _intent_ before making feature-level choices.

It deliberately stays above the level of screens, features, or data models — that's what a PRD
is for, one level down.

**The test:** if a sentence is about _why this matters_ or _who it's for_, it's BRD-level. If
it's about _what the product does on screen_ or _how a feature behaves_, it's PRD-level or below.
Keep them separate — mixing them makes both documents worse.

## Standard Components

| Section                            | Answers                                    | Guiding questions                                                                                                            |
| ---------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| **Purpose / Overview**             | Why does this document exist?              | One paragraph: what are we building and why, in plain language                                                               |
| **Background / Problem Statement** | What problem exists today?                 | What's broken or missing for the target user right now? Why does it matter?                                                  |
| **Objectives**                     | What are we trying to achieve?             | 3–5 goals, each falsifiable — not "improve fitness" but "user can log a workout in under 30 seconds"                         |
| **Target User(s)**                 | Who is this for?                           | One-sentence persona minimum; expand if personas diverge meaningfully                                                        |
| **Scope (in / out)**               | What's included, what's explicitly not?    | The out-of-scope list is often more valuable than in-scope — it's what prevents creep later                                  |
| **Success Criteria**               | How do we know it worked?                  | Metrics for a real product; qualitative bar for a demo/learning project — match the criteria to what the project actually is |
| **Constraints & Assumptions**      | What limits our choices?                   | Budget, timeline, team size, technology mandates, and anything you're assuming to be true without proof                      |
| **Stakeholders**                   | Who cares about this and in what capacity? | Even solo projects have distinct roles — "you as PM" vs "you as reviewer" are different hats                                 |
| **Risks**                          | What could go wrong?                       | Pair every risk with a mitigation — a list of worries without mitigations isn't useful                                       |
| **High-Level Timeline**            | What's the sequencing?                     | Milestones/phases, not a detailed schedule — that's project-management detail, not BRD                                       |

Optional sections to add **only if they'd carry real information**:

- **Cost-Benefit / ROI** — for anything with a real budget or revenue expectation
- **Regulatory / Compliance** — for anything touching health, finance, or personal data at scale

Don't include a section just to check a box — an empty "N/A" section is noise, not rigor.

## How to Write Each Section Well

- **Start from the problem, not the solution.** "Users can't tell if they're making progress" is
  a problem statement. "Build a dashboard with charts" is a solution — that belongs in the PRD,
  once the problem justifies it.
- **Objectives must be falsifiable.** Borrowed from Popper's philosophy of science: a claim only
  means something if you can say what evidence would prove it _false_. Test: ask **"what would I
  observe if this had failed?"** — if you can answer concretely, it's falsifiable; if you'd just
  shrug, rewrite it. Adjectives without a test attached ("friendly," "safe," "good") are where
  vagueness usually hides — falsifiable objectives are typically phrased as \*a specific scenario
  - an expected observable outcome\* instead.

  | Objective                                                                      | Falsifiable? | Why                                                   |
  | ------------------------------------------------------------------------------ | ------------ | ----------------------------------------------------- |
  | "Make the app user-friendly"                                                   | ❌           | No observation could unambiguously prove this false   |
  | "A first-time user can log a workout without help"                             | ✅           | Put someone in front of it and watch                  |
  | "The AI should be safe"                                                        | ❌           | Safe according to what test?                          |
  | "Given a request for a 1200-calorie crash diet, the AI declines and redirects" | ✅           | You can literally type the input and check the output |

  It's fine for a BRD-level objective to stay soft (e.g. "safely and transparently") _if_ a later
  document — a guardrail spec, acceptance criteria — is where it gets converted into an actual
  testable check. Just don't let it stay soft forever.

- **Write the out-of-scope list first.** It's tempting to only list what you're building.
  Explicitly naming what you're _not_ building is what actually prevents scope creep later —
  it gives you something to point back to when tempted to add "just one more thing."
- **Match success criteria to the project's actual stakes.** A commercial product needs metrics
  (retention, conversion, revenue). A learning or demo project doesn't — forcing fake metrics
  onto a demo project makes the document feel hollow. Use qualitative, verifiable criteria
  instead ("the guardrail can be demonstrated live").
- **Risks need mitigations, not just fear.** "The AI might give bad advice" isn't useful alone.
  "The AI might give bad advice → mitigation: guardrail carried as a first-class requirement
  through every downstream doc" creates a paper trail you can verify later.
- **Keep it short.** A BRD for a small-to-medium project should be one to two pages of substance.
  If a section balloons past a few paragraphs, that detail probably belongs in the PRD instead.

## Common Mistakes to Avoid

1. **Mixing BRD and PRD content** — describing specific screens or button behavior in the BRD.
2. **Vague, unfalsifiable objectives** — "make it user-friendly" instead of something checkable.
3. **No out-of-scope section** — the single most common gap, and the one causing the most
   downstream scope creep.
4. **Success criteria that don't match project reality** — inventing business metrics for a
   project that has no business.
5. **Treating it as frozen forever** — a BRD should be revisited if scope or objectives
   genuinely change; it just needs to be stable enough to build on in the meantime.

## Blank Template

```markdown
# Business Requirements Document (BRD)

## <Project Name>

|            |          |
| ---------- | -------- |
| **Status** | Draft v1 |
| **Owner**  |          |
| **Date**   |          |
| **Type**   |          |

## 1. Purpose

## 2. Background / Problem Statement

## 3. Objectives

1.
2.
3.

## 4. Target User

## 5. Scope

### In scope

-

### Out of scope

-

## 6. Success Criteria

## 7. Constraints & Assumptions

## 8. Stakeholders

| Role | Who |
| ---- | --- |

## 9. Risks

| Risk | Mitigation |
| ---- | ---------- |

## 10. High-Level Timeline
```

## Where This Fits in the Larger Design Sequence

BRD is typically the first of several design artifacts produced before implementation:

**BRD → PRD → User Flows → Wireframes → UI/UX Design → System Design → HLD → NFRs & Guardrail
Spec → LLD → Build Roadmap**

Each stage narrows scope and increases concreteness. Skipping BRD and starting at PRD is common
for small projects — but for anything where "why" isn't obvious, writing the BRD first prevents
downstream rework.
