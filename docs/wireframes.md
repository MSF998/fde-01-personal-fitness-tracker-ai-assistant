# Wireframes
## Personal Fitness Tracker AI Assistant

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | Mohd Sahnoon |
| **Date** | 2026-07-18 |
| **Depends on** | [user-flows.md](./user-flows.md) |

---

A rendered visual version of these same screens is at [wireframes.html](./wireframes.html) —
open it in a browser (or view via GitHub's raw link) for the actual mockups; this file is the
versioned text spec they're derived from.

Low-fidelity, structural wireframes — layout and content, not visual design (no color, type
system, or branding decisions here; that's a separate design pass if you ever want one). Each
screen is annotated with the flow step and PRD acceptance criteria it satisfies, and every state
a flow requires (empty, error, loading, guardrail-triggered) is wireframed explicitly, not just
the happy path — same discipline as the flows themselves.

**Legend:** `[______]` = text input · `▾` = dropdown · `( Button )` = primary action ·
`⚠` = inline error · `┄┄` = placeholder/loading content

---

## Screen Inventory

| Screen | Flow | PRD Feature |
|---|---|---|
| 1. Profile Setup | Onboarding | Feature 1 |
| 2. Dashboard / Home | Navigation Map | (hub — all features) |
| 3. Log Workout (form + error) | Log a Workout | Feature 2 |
| 4. Workout History | Log a Workout | Feature 2, AC3 |
| 5. AI Recommendation (loading / result / guardrail / error) | Request AI Recommendation | Feature 3 & 5 |
| 6. Progress View (empty / populated) | View Progress | Feature 4 |

---

## 1. Profile Setup

**Maps to:** Onboarding flow; PRD Feature 1, AC1–AC3.

```
┌───────────────────────────────────────────────┐
│  Fitness Tracker — Set Up Your Profile         │
├───────────────────────────────────────────────┤
│                                                 │
│  Name            [__________________________]  │
│  Age             [______]                       │
│  Fitness Goal    [ Lose weight            ▾ ]  │
│  Height (cm)     [______]                       │
│  Weight (kg)     [______]                       │
│                                                 │
│                        ( Save & Continue )     │
└───────────────────────────────────────────────┘
```

**Error state** (AC2 — invalid age/height/weight):

```
┌───────────────────────────────────────────────┐
│  Age             [ -5___ ]                      │
│  ⚠ Age must be a positive, realistic number     │
└───────────────────────────────────────────────┘
```

**Notes**
- Fitness Goal dropdown drives the two persona variants from PRD §3 ("Lose weight" /
  "Build strength") — this is the single field that differentiates them.
- Field-level errors appear inline, form is not submitted until resolved (matches flow branch).

---

## 2. Dashboard / Home

**Maps to:** Navigation Map — hub screen all other flows return to.

```
┌───────────────────────────────────────────────┐
│  Fitness Tracker                    [Profile]  │
├───────────────────────────────────────────────┤
│  Hi, <Name>                                    │
│  BMI: 23.4          Est. daily calories: 2,100 │
│                                                 │
│  ┌────────────┐ ┌───────────────┐ ┌──────────┐ │
│  │ Log         │ │ Get AI         │ │ View     │ │
│  │ Workout     │ │ Recommendation │ │ Progress │ │
│  └────────────┘ └───────────────┘ └──────────┘ │
│                                                 │
│  Recent Activity                               │
│  • Run — 30 min — felt good                    │
│  • Strength training — 45 min — felt tough      │
│  • (empty if no workouts yet — see Screen 6)   │
└───────────────────────────────────────────────┘
```

**Notes**
- BMI/calorie estimate computed once at profile save (Flow 1), displayed here every visit.
- The three primary actions map 1:1 to the three feature flows that branch off the Navigation Map.

---

## 3. Log Workout

**Maps to:** Log a Workout flow; PRD Feature 2, AC1–AC2.

```
┌───────────────────────────────────────────────┐
│  Log a Workout                          [ × ]  │
├───────────────────────────────────────────────┤
│  Type          [ Run                      ▾ ]  │
│  Duration (min) [______]                        │
│  How did it feel? [ Good  ▾ ]                   │
│                                                 │
│                          ( Save Workout )      │
└───────────────────────────────────────────────┘
```

**Error state** (AC2 — duration ≤ 0):

```
┌───────────────────────────────────────────────┐
│  Duration (min) [ 0___ ]                        │
│  ⚠ Duration must be greater than zero           │
└───────────────────────────────────────────────┘
```

---

## 4. Workout History

**Maps to:** Log a Workout flow (post-save); PRD Feature 2, AC3.

```
┌───────────────────────────────────────────────┐
│  Workout History                    [ + Log ]  │
├───────────────────────────────────────────────┤
│  Today                                         │
│   Run — 30 min — felt good                     │
│                                                 │
│  Yesterday                                     │
│   Strength training — 45 min — felt tough       │
│                                                 │
│  Jul 15                                        │
│   Swim — 20 min — felt okay                     │
└───────────────────────────────────────────────┘
```

**Notes**
- Most-recent-first ordering, grouped by date (AC3's explicit ordering requirement).

---

## 5. AI Recommendation

**Maps to:** Request AI Recommendation flow; PRD Feature 3 AC1–AC5, Feature 5 AC1–AC4.

**Default state — before requesting** (AC5 — optional free-text request, added 2026-07-18: this
is what makes the guardrail demoable by typing an unsafe request live, instead of only hoping the
AI volunteers something unsafe on its own):

```
┌───────────────────────────────────────────────┐
│  Ask something specific? (optional)            │
│  [_____________________________________]       │
│                                                 │
│                    ( Get Recommendation )      │
└───────────────────────────────────────────────┘
```

**Loading state:**

```
┌───────────────────────────────────────────────┐
│  Getting your recommendation…                  │
│  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄  │
└───────────────────────────────────────────────┘
```

**Normal result** (AC4 — labeled + disclaimer):

```
┌───────────────────────────────────────────────┐
│  🤖 AI Recommendation                           │
├───────────────────────────────────────────────┤
│  Based on your recent runs, try adding one      │
│  short strength session this week to balance    │
│  your training.                                 │
│                                                 │
│  ⓘ AI-generated — not medical advice            │
│                        ( Back to Dashboard )   │
└───────────────────────────────────────────────┘
```

**Guardrail-triggered result** (Feature 5 AC1–AC4 — visibly transparent, not silent):

```
┌───────────────────────────────────────────────┐
│  🤖 AI Recommendation                           │
├───────────────────────────────────────────────┤
│  ⚠ Safety check adjusted this response          │
│                                                 │
│  A large calorie deficit isn't safe to sustain. │
│  Instead, aim for a moderate deficit paired      │
│  with your current activity level.               │
│                                                 │
│  ⓘ AI-generated — not medical advice            │
│                        ( Back to Dashboard )   │
└───────────────────────────────────────────────┘
```

**Error state** (Feature 3 AC3 — service failure):

```
┌───────────────────────────────────────────────┐
│  ⚠ Couldn't get a recommendation right now.     │
│     Please try again.                          │
│                              ( Retry )         │
└───────────────────────────────────────────────┘
```

---

## 6. Progress View

**Maps to:** View Progress flow; PRD Feature 4, AC1–AC3.

**Empty state** (AC2 — zero logged workouts):

```
┌───────────────────────────────────────────────┐
│  Progress                                      │
├───────────────────────────────────────────────┤
│                                                 │
│         You haven't logged a workout yet.       │
│              ( Log Your First Workout )        │
│                                                 │
└───────────────────────────────────────────────┘
```

**Populated state** (AC1 & AC3):

```
┌───────────────────────────────────────────────┐
│  Progress            [ Week  Month  Year ▾ ]   │
├───────────────────────────────────────────────┤
│  Total workouts: 12     Total duration: 6h 40m │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │        [ Workout frequency chart ]       │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │        [ Volume / duration trend ]       │   │
│  └─────────────────────────────────────────┘   │
└───────────────────────────────────────────────┘
```

**Notes**
- Time-range selector (Week/Month/Year) reloads chart data in place (flow's filter branch) —
  exact chart types are a System Design/LLD decision, placeholders shown here.

---

## Open Questions

- None currently — every screen and state traces to a specific flow step and PRD AC. Flag
  anything here if a layout doesn't match how you pictured the feature working.
