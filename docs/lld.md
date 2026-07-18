# Low-Level Design (LLD)
## Personal Fitness Tracker AI Assistant

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | Mohd Sahnoon |
| **Date** | 2026-07-18 |
| **Depends on** | [nfr-guardrail-spec.md](./nfr-guardrail-spec.md) |

---

## 1. Overview

This is where the sequence stops making judgment calls. Every schema, model, and formula below
implements a decision already locked in by an earlier stage — if something here doesn't trace
back to the PRD, HLD, or NFR spec, that's a sign it should have been decided upstream, not here.
One genuine fork was resolved before drafting this: BMI/calorie estimation needs biological sex
for the standard formula, but Profile Setup doesn't collect it — resolved as a sex-neutral
approximation (§2), no PRD/schema change needed.

## 2. Formula Decisions

**BMI:** `weight_kg / (height_cm / 100) ** 2` — standard formula, already sex-neutral, no change
needed.

**Estimated daily calorie need (maintenance, not goal-adjusted):** a sex-neutral variant of the
Mifflin-St Jeor equation — averaging the formula's male (+5) and female (−161) constants into a
single −78, then applying a flat activity multiplier since the profile doesn't collect an
activity-level field either (PRD Feature 1 deliberately scoped to name/age/goal/height/weight
only):

```
BMR = 10 × weight_kg + 6.25 × height_cm − 5 × age − 78
estimated_daily_calories = round(BMR × 1.4)
```

`1.4` is a flat "lightly-to-moderately active" assumption, chosen because it fits the BRD
persona (busy professional, exercises 1–4x/week inconsistently) better than a sedentary or
highly-active default. This is intentionally approximate — the UI already labels it "Est." daily
calories, never presented as precise.

**Important:** `estimated_daily_calories` is the **maintenance** figure, not adjusted for the
user's goal (e.g. not pre-reduced for "lose weight"). This is deliberate: the guardrail's
crash-diet check ([nfr-guardrail-spec.md](./nfr-guardrail-spec.md) §3.1.3) compares a mentioned
calorie figure against 75% of this value — if it were already goal-reduced, the safety floor
would drop too, silently weakening the check. Both BMI and this figure are computed on the fly
from stored profile fields, never cached as columns, so they can't go stale after a profile edit.

## 3. Data Models (SQLite)

### `profile` (single row)

| Column | Type | Constraint |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY |
| `name` | TEXT | NOT NULL, 1–100 chars |
| `age` | INTEGER | NOT NULL, 13–100 |
| `fitness_goal` | TEXT | NOT NULL, one of `lose_weight`, `build_strength` |
| `height_cm` | REAL | NOT NULL, 100–250 |
| `weight_kg` | REAL | NOT NULL, 30–300 |
| `created_at` | TEXT | NOT NULL, UTC ISO 8601, set on insert |
| `updated_at` | TEXT | NOT NULL, UTC ISO 8601, set on every save |

Bounds above are this stage's answer to PRD AC2's "positive, realistic number" — deliberately
generous (they should never block a real user) rather than clinically precise.

### `workout` (many rows)

| Column | Type | Constraint |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `type` | TEXT | NOT NULL, one of `run`, `walk`, `strength_training`, `swim`, `cycle`, `other` |
| `duration_minutes` | INTEGER | NOT NULL, > 0 |
| `feeling` | TEXT | NOT NULL, one of `great`, `good`, `okay`, `tough`, `exhausting` |
| `logged_at` | TEXT | NOT NULL, UTC ISO 8601, defaults to insert time |

`type` and `feeling` enums are this stage's answer to the dropdowns shown in
[wireframes.md](./wireframes.md) Screens 3–4 — the wireframes showed the interaction pattern, not
the exact option set.

## 4. API Request/Response Models

Field names below are authoritative — they're what the frontend's `fetch()` calls and the Jinja2
templates should be written against.

**`POST /api/profile`**
```
Request:  { name: str, age: int, fitness_goal: "lose_weight" | "build_strength",
            height_cm: float, weight_kg: float }
Response: { name, age, fitness_goal, height_cm, weight_kg,
            bmi: float, estimated_daily_calories: int }
```

**`POST /api/workouts`**
```
Request:  { type: "run"|"walk"|"strength_training"|"swim"|"cycle"|"other",
            duration_minutes: int, feeling: "great"|"good"|"okay"|"tough"|"exhausting" }
Response: { id: int, type, duration_minutes, feeling, logged_at: str }
```

**`GET /api/workouts`**
```
Response: { workouts: [ { id, type, duration_minutes, feeling, logged_at }, ... ] }
```
Ordered most-recent-first (PRD Feature 2 AC3) — enforced by the query, not left to the caller.

**`POST /api/recommendation`**
```
Request:  { message: str | null }   // optional free-text request, PRD Feature 3 AC5, max 500 chars
Response: { recommendation: str, guardrail_triggered: bool,
            guardrail_category: "crash_diet" | "medical_diagnosis" | "unrealistic_timeline" | null }
```
`guardrail_category` values are exactly the three category names defined in
[nfr-guardrail-spec.md](./nfr-guardrail-spec.md) §3 — nothing new introduced here.

**`GET /api/progress?range=week|month|year`**
```
Response: {
  range: "week" | "month" | "year",
  total_workouts: int,
  total_duration_minutes: int,
  workout_frequency: [ { period: str, count: int }, ... ],
  duration_trend:     [ { period: str, minutes: int }, ... ]
}
```
Bucketing: `week` and `month` bucket daily (last 7 / last 30 days); `year` buckets monthly (last
12 months). `total_workouts` / `total_duration_minutes` are sums over the whole selected range,
not per-bucket. Empty range (PRD Feature 4 AC2) returns the same shape with empty arrays and
zeroed totals — the frontend already has an empty-state to render for that case, not a special
error.

Validation-error and service-failure responses use the exact shapes already fixed in
[nfr-guardrail-spec.md](./nfr-guardrail-spec.md) §4 — not repeated here.

## 5. Open Questions (deferred to Build Roadmap)

None on schema or contracts — the Build Roadmap stage's job is sequencing implementation, not
further design decisions. One practical note to carry forward: reset-for-demo (deleting the
SQLite file to return to first-run state, per NFR spec §5's data-retention note) is worth a
documented step in that stage, not a design decision here.
