# What Is a Wireframe?

A reusable reference — not tied to any one project. Use this whenever starting a new project's
design docs from scratch, right after User Flows are confirmed.

## Purpose

A wireframe answers **"what does each screen actually contain, and where?"** It takes a user
flow's steps and turns each one into a concrete layout — what elements exist, roughly where they
sit, and what they say. Its audience is anyone who needs to picture the product's actual screens
before deciding how it's built: you sanity-checking a layout works before committing to it, or an
implementer (human or AI) who needs to know what a screen contains without guessing.

Where a user flow answers "in what order," a wireframe answers "what's on it." It deliberately
stays low-fidelity: **layout and content, not visual design.** No color palette, no typography
system, no branding — those are a separate design pass, if you ever want one, and conflating them
with structure makes both worse. A wireframe that looks "finished" is usually a sign visual
decisions crept in before they should have.

**The test:** if a decision is about *what element is where, and what it says*, it's
wireframe-level. If it's about *color, font, spacing polish, or brand feel*, it's a later (and
optional) visual design pass. If it's about *what happens when you click something*, that's
already been decided upstream in the user flow — the wireframe just needs to render each state
the flow already defined.

## Standard Components

| Section | Answers | Guiding questions |
|---|---|---|
| **Screen Inventory** | What screens exist, and which flow/feature does each belong to? | One row per screen; a screen with no flow/feature behind it is speculative |
| **Legend** | What do the notation conventions mean? | Define input/button/error/placeholder symbols once, up front, so every screen after it is unambiguous |
| **One wireframe per screen** | What's on this specific screen? | Elements, their rough position, and their actual copy (not lorem ipsum) |
| **States per screen** | What does this screen look like in each state the flow requires? | Default, empty, error, loading — whichever the flow's branches actually call for |
| **"Maps to" line per screen** | Which flow step / PRD acceptance criteria does this satisfy? | Same discipline as user flows — every screen should be traceable, not invented here |
| **Notes per screen** | What's deliberately left undecided? | Exact formulas, chart types, copy polish — call out what's pushed to LLD/build so it isn't mistaken for a decision made here |
| **Open Questions** | What doesn't fit yet? | Anywhere a layout reveals a gap in the flow or PRD |

## How to Write Each Wireframe Well

- **Every state the flow branches on gets its own wireframe, not just the happy path.** If the
  user flow has an empty-state branch or an error branch, draw it — a wireframe that only shows
  the populated, successful state is only half-specified. This is the same discipline carried
  over from user flows: branches are first-class, not decoration.

- **Use real content, never lorem ipsum.** Placeholder Latin text hides layout problems that real
  content would expose — a name field labeled "Lorem ipsum dolor" doesn't tell you if a long name
  will wrap awkwardly, but "e.g. Priya Shah" does. Pull real copy from the PRD's user stories and
  acceptance criteria wherever they specify it.

- **Stay low-fidelity on purpose.** No color, no chosen typeface, no polish — a plain grayscale
  box-and-line layout communicates structure without implying the visual design is settled.
  Skipping this discipline (jumping straight to a polished-looking mock) tends to make
  stakeholders react to color and font choices instead of the actual layout question being asked.

- **Anchor every screen to a flow step and PRD acceptance criteria.** Same rule as user flows —
  if you can't point to which flow step or AC a screen satisfies, ask whether you're inventing UI
  at the wrong stage.

- **Pick a wireframing medium that matches how the docs get reviewed and versioned.** Plain-text
  box-drawing (ASCII) wireframes are git-diffable and need no tooling — good as the source of
  truth in a docs repo. A rendered visual pass (a static HTML/SVG mockup, or a tool like Figma) is
  easier to actually *look at* — good as a companion, not necessarily the versioned source. Doing
  both isn't overkill for anything beyond a handful of screens; the text version stays the
  reviewable source, the visual version is what you'd actually show someone.

- **Keep a consistent legend across every screen.** Define input/button/error/placeholder
  notation once, at the top, rather than re-explaining conventions screen by screen.

## Common Mistakes to Avoid

1. **Happy-path-only wireframes** — skipping empty/error/loading states the flow already defined.
2. **Lorem ipsum instead of real content** — hides the layout problems real copy would expose.
3. **Sneaking in visual design** — color choices, font pairing, or polish before structure is
   agreed on, which derails review toward the wrong questions.
4. **Screens with no flow/AC anchor** — inventing UI that doesn't trace back to a requirement.
5. **Inconsistent notation** — a different symbol or convention on every screen instead of one
   legend applied uniformly.
6. **No screen inventory** — a pile of individual wireframes with no table showing how they
   relate to flows/features, making it hard to verify coverage.

## Blank Template

```markdown
# Wireframes
## <Project Name>

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | |
| **Date** | |
| **Depends on** | user-flows.md |

**Legend:** define input/button/error/placeholder notation here.

## Screen Inventory

| Screen | Flow | PRD Feature |
|---|---|---|

## 1. <Screen Name>

**Maps to:** <flow name>; PRD Feature N, ACx–ACy.

<wireframe — default state>

<wireframe — each additional state the flow requires>

**Notes**
-

## Open Questions
-
```

## Where This Fits in the Larger Design Sequence

**BRD → PRD → User Flows → Wireframes → System Design → HLD → LLD → NFRs/Guardrails → Build
Roadmap**

Wireframes are the last stage before the documents shift from product/design language into
engineering language. Getting states and content right here is cheap; getting them wrong and
discovering it once System Design or LLD is underway is not — a missing empty state or an
unanchored screen surfaces as a scramble mid-build instead of a five-minute fix on a wireframe.
