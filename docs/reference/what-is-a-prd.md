# What Is a PRD (Product Requirements Document)?

A reusable reference — not tied to any one project. Use this whenever starting a new project's
design docs from scratch, right after the BRD is confirmed.

## Purpose

A PRD answers **"what exactly are we building, and how do we know each piece works?"** It takes
the BRD's why/who and turns it into concrete features, user stories, and testable acceptance
criteria. Its audience is anyone who needs to build or verify the product — designers, engineers,
an AI coding assistant, or you reviewing your own scope later.

Where the BRD stays above screens and features, the PRD lives at the feature level — but still
stops short of *how* something is technically implemented (architecture, data models, endpoints).
That's System Design / HLD / LLD, further downstream.

**The test:** if a sentence describes *what the user can do and how we'd verify it*, it's
PRD-level. If it describes *why it matters to the business*, push it up to the BRD. If it
describes *how it's built* (database, API, framework), push it down to System Design/HLD/LLD.

## Standard Components

| Section | Answers | Guiding questions |
|---|---|---|
| **Overview** | What is this document translating, and from where? | One paragraph linking back to the BRD it's derived from |
| **Goals** | What must be true when this ships? | BRD objectives made concrete — often where BRD/reality conflicts get resolved (see below) |
| **Personas** | Who, specifically, are we designing for? | Inherited from BRD; expand only if the product genuinely needs to serve distinguishable user types |
| **Features + User Stories** | What can the user do? | One section per feature; stories in "As a [user], I want [action], so that [outcome]" form |
| **Acceptance Criteria** | How do we verify each story works? | Given/When/Then per story — see below; this is the PRD's most important discipline |
| **Prioritization (MoSCoW)** | What ships first if time is short? | Must / Should / Could / Won't — forces an explicit cut line before you're under time pressure |
| **Assumptions Carried Downstream** | What are we implicitly deciding that the next stage needs to know? | Anything inferred rather than explicitly stated (e.g. "no login" inferred from "no multi-user") — flag it, don't bury it |
| **Out of Scope** | What's still excluded? | Usually inherited from BRD, restated for completeness |
| **Open Questions** | What's still unresolved? | Anything you made a judgment call on that the reader should get a chance to overrule |

## How to Write Each Section Well

- **Every feature gets user stories, every story gets acceptance criteria.** A feature listed
  without a story is a label, not a requirement. A story without acceptance criteria is a wish,
  not something anyone can verify — it's the PRD-level version of "falsifiable objectives" from
  the BRD (see [what-is-a-brd.md](./what-is-a-brd.md)).

- **Write acceptance criteria as Given/When/Then.**
  *Given* a starting state, *when* an action happens, *then* an observable outcome follows.
  This format forces you to specify the state before, the trigger, and the exact result — which
  is exactly what an implementer (human or AI) needs to build against without guessing, and
  exactly what you need to check a demo against without ambiguity.

  ```
  Given a user with a saved profile and at least one logged workout,
  when they request a recommendation,
  then the response references their specific goal and recent activity.
  ```

  A bad acceptance criterion just restates the story ("the recommendation should be good") — if
  it doesn't name a specific state and a specific observable result, rewrite it.

- **Prioritize with MoSCoW, and use "Won't" deliberately.** Must/Should/Could/Won't isn't just
  Must vs. everything else — "Won't" is where you explicitly park things so they don't quietly
  creep back in later. If every feature ends up "Must," that's a sign scope hasn't actually been
  narrowed yet.

- **Surface conflicts between source documents instead of silently resolving them.** If the BRD,
  an existing draft, or a source brief disagree on something (e.g. a feature classified secondary
  in one place but core in another), name the conflict, make a call, and say why — don't just
  pick one silently. The reader needs to be able to overrule you cheaply.

- **Flag inferred assumptions before they harden into architecture.** Some decisions aren't
  explicitly stated anywhere but are implied by scope (e.g. "no multi-user accounts" implies "no
  login system"). These are exactly the assumptions that are expensive to unwind once System
  Design has been built on top of them — so call them out explicitly and get them confirmed
  *before* moving downstream, not after.

- **Keep acceptance criteria demo-checkable.** For a small or solo project, a good sanity check
  is: could you literally perform the Given/When/Then steps live in front of someone? If not,
  it's probably still too vague or too technical for PRD level.

## Common Mistakes to Avoid

1. **Features without acceptance criteria** — leaves "done" undefined, so nothing can be verified.
2. **Restating the story as its own acceptance criterion** — no new information, not falsifiable.
3. **Silently resolving source conflicts** — deciding a discrepancy between BRD/brief/earlier
   drafts without telling the reader a decision was even made.
4. **Every feature marked "Must have"** — means prioritization didn't actually happen.
5. **Smuggling implementation details into the PRD** — naming specific databases, frameworks, or
   API shapes here belongs in System Design/HLD/LLD instead.
6. **Leaving inferred assumptions unflagged** — letting a downstream stage (System Design) build
   on a guess nobody actually confirmed.

## Blank Template

```markdown
# Product Requirements Document (PRD)
## <Project Name>

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | |
| **Date** | |
| **Depends on** | BRD.md |

## 1. Overview

## 2. Goals

## 3. Personas

## 4. Features, User Stories & Acceptance Criteria

### Feature 1 — <Name>
**User stories**
-

**Acceptance criteria**
1. Given ___, when ___, then ___.

## 5. Prioritization (MoSCoW)

| Priority | Features |
|---|---|
| Must have | |
| Should have | |
| Could have | |
| Won't have | |

## 6. Assumptions Carried Downstream

## 7. Out of Scope

## 8. Open Questions
```

## Where This Fits in the Larger Design Sequence

**BRD → PRD → User Flows → Wireframes → System Design → HLD → LLD → NFRs/Guardrails → Build
Roadmap**

The PRD is the last stage that's still product-language, not engineering-language. Everything
from User Flows onward starts translating these acceptance criteria into diagrams, screens, and
eventually data models and API contracts — so vagueness left unresolved here compounds at every
later stage.
