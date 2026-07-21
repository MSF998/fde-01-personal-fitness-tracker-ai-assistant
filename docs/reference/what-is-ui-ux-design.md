# What Is UI/UX Design (the visual design pass)?

A reusable reference — not tied to any one project. Use this whenever starting a new project's
design docs from scratch, right after Wireframes are confirmed and before System Design begins.

## Purpose

UI/UX Design answers **"what does this actually look like, and what does it feel like to use?"**
It takes the same screens Wireframes already defined — the elements, their rough position, their
real content — and adds the layer wireframes deliberately excluded: color, typography, spacing
polish, a real component system, and every interaction state (hover, focus, active, disabled,
loading, error) styled, not just structurally listed.

Where a wireframe answers "what's on it," UI/UX Design answers "what does it look and feel like."
It stays in product/design language, same as everything before it — no API shapes, no data
models, no architecture. System Design, right after, is where the language shifts to engineering.

**The test:** if a decision is about *color, type, spacing, motion, or a component's visual/
interactive states*, it's UI/UX Design-level. If it's about *what element exists and roughly
where* (already decided), that was the wireframe's job — don't redecide it here. If it's about
*what serves this screen technically*, that's System Design, next.

## Standard Components

| Section | Answers | Guiding questions |
|---|---|---|
| **Design Tokens** | What's the color palette, type scale, and spacing system? | Named values (not one-off hex codes scattered per screen) — the same tokens should be reusable across every screen |
| **Component Library** | What are the reusable visual components, and their states? | Buttons (primary/secondary/disabled), inputs (default/focus/error), cards, badges — each with every state design ed, not just default |
| **High-Fidelity Screens** | What does each wireframed screen look like with the full visual treatment applied? | One high-fidelity mockup per wireframe screen — same coverage, now with real visual design |
| **Interaction/Motion Notes** | What moves, and how? | Transitions, hover feedback, loading states — only where it serves the product, not decoration for its own sake |
| **Design System Handoff** | What does an implementer need to build this accurately? | Exact values (hex, rem/px, easing curves) — the same "no ambiguity" discipline as an LLD, just for visual properties instead of data |

## How to Do It Well

- **Derive from the wireframes, don't restart from a blank canvas.** The wireframes already
  answered layout and content — revisiting those questions here means the two stages weren't
  actually building on each other. Bring the wireframe's screen inventory in as-is; add the visual
  layer on top of it.

- **Design every state a flow already requires, not just the happy path.** Same discipline as
  every earlier stage in this sequence — if the wireframe has an empty state, an error state, a
  loading state, the high-fidelity design needs all of them too. A polished-looking default state
  next to an undesigned error state is a common, avoidable gap.

- **Tokens first, screens second.** Naming a color palette and type scale before touching any
  individual screen means every screen draws from the same system — the alternative (picking
  colors per-screen as you go) is how inconsistency creeps in silently.

- **Bake accessibility in from the start, don't audit it in afterward.** Contrast ratios, touch
  target sizes, and focus states are cheap to get right while choosing tokens and expensive to
  retrofit once forty components already reference the wrong gray. See
  [what-is-an-nfr.md](./what-is-an-nfr.md)'s accessibility guidance for the bar to design against.

- **Match fidelity to the project's actual stakes.** A solo/demo project doesn't need the same
  design-system rigor as a multi-team product — but it still benefits from *some* deliberate
  token system rather than none. The gap between "no visual design pass" and "a full design
  system" is wide; most small projects only need the narrow, cheap end of it (see the note below).

## Common Mistakes to Avoid

1. **Re-deciding layout/content that the wireframes already settled** — redoing work instead of
   building on it.
2. **Happy-path-only high-fidelity screens** — a beautiful default state with no designed error/
   empty/loading equivalent.
3. **Picking colors and type per-screen instead of from a shared token system** — the fastest way
   to end up with inconsistent, hard-to-maintain visual design.
4. **Auditing accessibility after the fact instead of designing to a contrast/target-size bar from
   the start** — expensive to retrofit, cheap to bake in.
5. **Treating this stage as mandatory regardless of project size** — see below; skipping it
   consciously is a legitimate call for the right project, skipping it by accident is not.

## When to Skip This Stage (and What It Costs You)

This is the one stage in the sequence that's genuinely optional, and worth being honest about
when. It earns its keep when (a) a separate designer and engineer need a shared source of truth
to hand off between, or (b) the project needs to cheaply explore multiple visual directions
before committing engineering time to any of them. For a solo project where the same person
designs and implements, neither condition necessarily holds, and it's defensible to defer this
stage — proceed straight from Wireframes to System Design, and do a lightweight visual pass later,
directly against the implemented CSS, once the product works end-to-end.

**The cost of deferring:** doing it later means iterating on live CSS/templates across every
screen instead of cheaply throwing away directions in a design tool first — fine for a small
surface area (a handful of screens, a narrow token set), increasingly costly the larger the
product gets. If a deferred pass starts requiring changes to more than a few screens' worth of
markup, that's the signal it should have been its own stage after all.

## Blank Template

```markdown
# UI/UX Design
## <Project Name>

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | |
| **Date** | |
| **Depends on** | wireframes.md |

## 1. Design Tokens

### Color
| Token | Value | Used for |
|---|---|---|

### Type Scale
| Token | Value | Used for |
|---|---|---|

## 2. Component Library

### <Component> — states: default / hover / focus / disabled / error

## 3. High-Fidelity Screens

### Screen N — <Name>
(one mockup per wireframe screen and state)

## 4. Interaction/Motion Notes

## 5. Design System Handoff Notes
```

## Where This Fits in the Larger Design Sequence

**BRD → PRD → User Flows → Wireframes → UI/UX Design → System Design → HLD → NFRs & Guardrail
Spec → LLD → Build Roadmap**

This is the last stage in product/design language before everything after it shifts to
engineering language. It's also the one stage in the sequence that's legitimately optional
depending on project shape — see above — which is why every other reference doc in this library
notes its presence without assuming it always runs.
