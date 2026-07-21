# Design Improvement Plan
## Personal Fitness Tracker AI Assistant

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | Mohd Sahnoon |
| **Date** | 2026-07-19 |
| **Baseline** | `v0.1-functional-prototype` (commit `507a4a8`) — every change below is layered on top of this working, tagged checkpoint. Nothing here touches architecture, data models, or the guardrail logic. |

---

## 1. Overview

This plan turns the UI/UX critique's findings into concrete, sequenced changes. It's scoped
deliberately narrow: **CSS and small amounts of template/JS markup only** — no new dependencies,
no new features, no architectural changes. The functional prototype at `v0.1-functional-prototype`
already works correctly end-to-end; this plan is purely about making it *look and feel* like it
does.

Everything here traces back to a specific finding from the critique — if a change doesn't map to
a finding, it doesn't belong in this pass.

## 2. Design Direction

No visual identity existed before this plan (deliberately — see BRD/wireframes' scope). This
section proposes one, expressed as CSS custom properties so every later change references a
token, not a hardcoded value.

### Color

| Token | Value | Used for |
|---|---|---|
| `--color-bg` | `#ffffff` | Page background (unchanged from M6's contrast fix) |
| `--color-surface` | `#f8f9fa` | Card/tile backgrounds — subtle depth without shadows |
| `--color-text` | `#111111` | Body text (unchanged from M6) |
| `--color-muted` | `#5a6169` | Captions, day-labels, disclaimers |
| `--color-border` | `#d8dce1` | Default borders — lighter than the current flat `#333` |
| `--color-primary` | `#0d7a6c` | Primary actions only — a restrained teal, not the neon-green fitness-app cliché |
| `--color-primary-hover` | `#0b6358` | Primary button hover/active |
| `--color-danger` | `#b91c1c` | Errors and the guardrail warning badge — semantic color, kept separate from the accent (unchanged from M6) |

**Why teal, specifically:** it reads as "active/health" without being the generic neon-green-on-
black look most fitness apps default to, and it's restrained enough to use sparingly (primary
buttons only) rather than fighting with the guardrail's red for attention. It's a CSS variable —
trivial to swap later if you want something else.

### Type Scale

| Token | Value | Used for |
|---|---|---|
| `--font-size-xs` | `0.75rem` (12px) | Disclaimers, captions |
| `--font-size-sm` | `0.875rem` (14px) | Labels, day-labels, muted text |
| `--font-size-base` | `1rem` (16px) | Body text |
| `--font-size-lg` | `1.25rem` (20px) | h2 (section/modal headings) |
| `--font-size-xl` | `2rem` (32px) | h1 (page title) |

Font stack stays as-is (`system-ui` etc.) — no webfont needed, and introducing one would add
complexity disproportionate to what this pass is for.

### Button Hierarchy

Currently every button (Save Workout, Cancel, Get Recommendation, Retry, Log Your First Workout)
looks identical — the critique's top-priority finding. Two classes fix this:

- **`.btn-primary`** — solid `--color-primary` fill, white text. The one action per screen that
  actually moves you forward: Save Workout, Get Recommendation, Retry, Log Your First Workout.
- **`.btn-secondary`** — outline only (`--color-border`), transparent background,
  `--color-text`. Everything that dismisses or cancels: every Cancel button, every modal
  Close/Back-to-Dashboard action.

### Spacing

No change — the critique confirmed spacing is already consistent (`.field`, `.tiles`, `.kpis`,
`.chartbox` reused correctly across every page). Not touching what already works.

## 3. Prioritized Action Items

Organized into phases — later phases depend on earlier ones (the token system in Phase A is the
foundation everything else references), so implement in order.

### Phase A — Foundation (do first)

| # | Change | Finding addressed | Files |
|---|---|---|---|
| A1 | Add the color/type tokens from §2 as CSS custom properties on `:root` | — (foundation for everything below) | `static/css/style.css` |
| A2 | Replace every hardcoded color (`#333`, `#555`, `#666`, `#b91c1c`, `#f6f8fa`) with its token equivalent | Consistency — no more scattered one-off hex values | `static/css/style.css` |
| A3 | Add `.btn-primary` / `.btn-secondary` classes; apply to every button pair (Save/Cancel, Get Recommendation/Cancel, Retry/Cancel, Log Your First Workout) | 🟡 Primary/secondary actions look identical | `static/css/style.css`, `templates/index.html`, `templates/progress.html` |
| A4 | Apply the type scale to `h1`, `h2`, `.day-label`, `.chartbox .cap`, `.disclaimer` | Typography currently 100% browser defaults, no deliberate hierarchy | `static/css/style.css` |

**Verification:** open every screen; confirm exactly one solid-fill button per screen (the
primary action) and every other button is outlined; confirm h1 is visibly larger/heavier than h2
everywhere, not just by browser default.

### Phase B — Component-Level Fixes

| # | Change | Finding addressed | Files |
|---|---|---|---|
| B1 | Give the "View Progress" tile a distinct style from the two modal-trigger tiles (e.g. no border, or a subtle arrow affordance) — it navigates away, the other two open modals | 🟡 All three tiles look identical despite different roles | `templates/index.html`, `static/css/style.css` |
| B2 | Remove the emoji (🤖 ⚠ ⓘ) from the AI Recommendation panel, or commit to using consistent iconography everywhere — **recommended: remove**, since adding icons app-wide is disproportionate effort for this pass and the emoji currently reads as a one-off | Icon usage inconsistent — appears nowhere else in the app | `templates/index.html` |
| B3 | Bump `.tile` min-height to an explicit 48px (currently measures 47px, right at the accessible-minimum edge) | 🟢 Touch targets borderline | `static/css/style.css` |

**Verification:** tiles measure ≥48px via `getBoundingClientRect()`; View Progress is visually
distinguishable from the other two tiles at a glance; no emoji remain unless B2's alternative
(consistent icons everywhere) was chosen instead.

### Phase C — Interaction Polish

| # | Change | Finding addressed | Files |
|---|---|---|---|
| C1 | Disable "Save Workout" while its `fetch()` is in flight, re-enable on response | 🟢 No loading/disabled state — fast double-click could fire duplicate requests | `static/js/dashboard.js` |
| C2 | Add a brief inline confirmation (e.g. "Workout logged" text that appears and fades, or a simple `aria-live` region) after a successful save, beyond the modal just closing | 🟡 No explicit success feedback | `static/js/dashboard.js`, `templates/index.html`, `static/css/style.css` |

**Verification:** rapidly double-click Save Workout — confirm only one entry is created; confirm
some visible acknowledgment appears after a successful log, not just the modal closing silently.

### Phase D — Accessibility

| # | Change | Finding addressed | Files |
|---|---|---|---|
| D1 | Add an `aria-label` (or visually-hidden text summary) to each Chart.js canvas summarizing the data it shows (e.g. "Workout frequency, last 7 days: Jul 12 through Jul 17 zero, Jul 18 one workout") | 🟡 Canvas-based charts have no screen-reader-accessible equivalent — not covered by NFR's "lightweight bar" | `templates/progress.html`, `static/js/progress.js` |

**Verification:** inspect the DOM/accessibility tree for both canvases and confirm a text
alternative is present and accurate for whatever range is currently selected.

## 4. Out of Scope for This Pass

- Any new npm/pip dependency (no icon libraries, no CSS frameworks, no webfonts) — everything
  above is achievable with plain CSS custom properties and the existing vanilla JS.
- Any change to routes, data models, the guardrail, or the AI integration — this is a visual/UX
  pass only, layered entirely on top of `v0.1-functional-prototype`'s working functionality.
  If a change here seems to require touching those, stop and flag it rather than proceeding.
  Building on top of the already-complete system-design.md/hld.md/lld.md decisions.
- Responsive/mobile-specific breakpoints — BRD never confirmed mobile matters for this project;
  out of scope unless that changes.
- A full WCAG AA audit — D1 closes the one concrete gap the critique found; a formal audit is
  still explicitly out of scope per `nfr-guardrail-spec.md` §6.

## 5. Rollback

Every change in this plan sits on top of the tagged checkpoint. If anything in Phases A–D
regresses functionality, `git diff v0.1-functional-prototype` shows exactly what changed, and
`git checkout v0.1-functional-prototype` returns to the last known-good functional state.
