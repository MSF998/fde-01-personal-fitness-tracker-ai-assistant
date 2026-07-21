# What Is a User Flow / Flowchart?

A reusable reference — not tied to any one project. Use this whenever starting a new project's
design docs from scratch, right after the PRD is confirmed.

## Purpose

A user flow answers **"what does the user actually see and decide, screen to screen?"** It takes
each PRD feature's acceptance criteria and turns them into a visual path through the product —
entry point, decisions, branches, and exit. Its audience is anyone who needs to picture the
product in motion before screens exist: designers about to wireframe, engineers about to design
data flow, or you sanity-checking that the acceptance criteria actually cohere into a usable
journey.

Where the PRD lives at the level of "what can the user do and how do we verify it," a user flow
lives at "in what order, with what branches." It still stops short of *how it's built* — no API
calls, no data models, no component names. That's System Design/HLD next.

**The test:** if a step is something the user sees or decides, it's flow-level. If it's something
a server does internally (validate payload, query database, commit transaction), push it down to
HLD/sequence-diagram level instead — even if you already have that detail written somewhere
(e.g. from an earlier scoping exercise), don't duplicate it here.

## Standard Components

| Section | Answers | Guiding questions |
|---|---|---|
| **Navigation Map (overview)** | How do the individual flows connect? | One diagram showing entry point and how each feature-level flow is reached from it |
| **One flow per feature** | What's the step-by-step path through this specific feature? | Start node → decisions → branches → end node(s) |
| **"Maps to" line per flow** | Which PRD feature/AC does this trace back to? | Every flow should cite specific acceptance criteria — a flow with no PRD anchor is speculative, not derived |
| **Notes per flow** | What's deliberately left undecided, and why? | Call out anything pushed downstream (exact validation rules, formulas, copy) so it isn't mistaken for a decision made here |
| **Open Questions** | What doesn't fit yet? | Anything where the flow reveals a gap or contradiction in the PRD |

## How to Write Each Flow Well

- **Anchor every flow to specific acceptance criteria.** Write "Maps to: Feature 3, AC1–AC4"
  before drawing anything. If you can't point to which AC a branch satisfies, ask whether the
  branch is actually in scope or whether you're inventing requirements at the wrong stage.

- **Include error and empty states as first-class branches, not afterthoughts.** If the PRD's
  acceptance criteria test an empty state or a failure path (they usually do), that branch
  belongs in the diagram with the same weight as the happy path — not a footnote. A flow that
  only shows the happy path is only checking half the acceptance criteria.

- **Stay at user-journey level.** "Validate the request payload," "commit the transaction," "read
  from the database" are implementation steps — they belong in a sequence diagram at HLD, not
  here, even when you already have that level of detail written down from earlier scoping. Resist
  pulling it in early; it makes the flow harder to read as a *user* journey and duplicates work
  you'll redo more precisely later.

- **One flow per feature, plus one navigation map.** Don't try to cram every feature into a single
  mega-diagram — it becomes unreadable and hides the branches that actually matter. The nav map's
  only job is showing how the individual flows connect; keep it shallow.

- **Mermaid syntax, if you're using it (recommended — renders natively on GitHub and most
  markdown viewers):**
  - **Never put a raw line break inside a node label.** Mermaid parses each new line as a new
    statement, so `A[Some text\nmore text]` written across two physical lines breaks the parser.
    Use `<br/>` inside the label instead: `A["Some text<br/>more text"]`.
  - **Wrap any label containing punctuation in double quotes** — apostrophes, colons, slashes, or
    parentheses inside an unquoted label can be misread as syntax (e.g. `(` inside `[...]` looks
    like a shape delimiter). `B["Tap 'Get Recommendation'"]` is safe; `B[Tap 'Get Recommendation']`
    is not, reliably.
  - Keep decision nodes (`{...}`) genuinely binary or small-enumerable where possible — a diamond
    with five outgoing branches is usually a sign the flow should be split into two diagrams.

## Common Mistakes to Avoid

1. **Flows with no PRD anchor** — drawing a journey that isn't traceable to any acceptance
   criterion, effectively inventing scope at the wrong stage.
2. **Happy-path-only diagrams** — omitting empty/error states that the PRD already requires you
   to test.
3. **Mixing in implementation detail** — API calls, database steps, or validation logic pulled in
   from an earlier technical scoping exercise, duplicating what HLD sequence diagrams should own.
4. **One giant diagram instead of one-per-feature** — impossible to review, hides branch logic.
5. **Mermaid rendering silently breaking** — raw newlines in labels, or unquoted punctuation —
   catch this before calling the doc done; always preview-render before moving on.

## Blank Template

```markdown
# User Flows / Flowcharts
## <Project Name>

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | |
| **Date** | |
| **Depends on** | PRD.md |

## 0. Navigation Map (overview)

\`\`\`mermaid
flowchart TD
    Start([User opens app]) --> ...
\`\`\`

## 1. <Flow Name>

**Maps to:** PRD Feature N, AC1–ACn.

\`\`\`mermaid
flowchart TD
    A([Start]) --> B{Decision?}
    B -- Yes --> C[...]
    B -- No --> D[...]
\`\`\`

**Notes**
-

## Open Questions
-
```

## Where This Fits in the Larger Design Sequence

**BRD → PRD → User Flows → Wireframes → UI/UX Design → System Design → HLD → NFRs & Guardrail
Spec → LLD → Build Roadmap**

User flows are the bridge between requirements (PRD) and visuals (Wireframes) — they answer "in
what order" before Wireframes answer "what does it look like." Skipping this stage tends to
produce wireframes that look fine individually but don't connect into a coherent journey when
someone actually tries to use the product end-to-end.
