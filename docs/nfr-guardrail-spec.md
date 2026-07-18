# NFRs & Guardrail Spec
## Personal Fitness Tracker AI Assistant

| | |
|---|---|
| **Status** | Draft v1 |
| **Owner** | Mohd Sahnoon |
| **Date** | 2026-07-18 |
| **Depends on** | [hld.md](./hld.md) |

---

## 1. Overview

This is where the patterns HLD established become exact, testable values: the guardrail's precise
trigger rules and fallback copy, the API error contract's exact shape, and the NFRs that don't
shape the architecture itself (so didn't belong in System Design) but still need a concrete,
checkable bar. LLD (next) builds data models and Pydantic/API schemas against what's decided here
— nothing here should be revisited there, only implemented.

## 2. Design Refinement: Guardrail Checks Input *and* Response

**HLD said** the guardrail checks only the AI's response text. Writing this spec exposed why
that's not reliable enough for one of the three categories: a well-aligned instruction-tuned model
usually *already* declines to give a clean medical diagnosis on its own — which means an
output-only check might simply never have anything to catch, regardless of whether the guardrail
code is correct. That makes the guardrail undemoable for that category specifically, which
conflicts with the brief's requirement that it be demonstrable live.

**Revised design:** the guardrail evaluates the **concatenation of the user's typed request (if
any) + the AI's response text** against all three rule sets below. Either side triggering is
enough. This doesn't change HLD's architecture (guardrail still runs once, inside the API route,
after the AI call returns) — it only changes what text the existing checks are run against. Both
[user-flows.md](./user-flows.md) and [hld.md](./hld.md) are amended to match (see their own
amendment notes).

## 3. Guardrail Rules (exact, testable)

### 3.1 Crash-diet / extreme-deficit

**Trigger if any of:**
1. Text contains any phrase from: `crash diet`, `starve`, `starving`, `skip meals`, `skip
   breakfast`, `water fast`, `zero calorie`, `extremely low calorie`, `very low calorie diet`
   (case-insensitive substring match).
2. Text contains a calorie figure (regex: `(\d{3,4})\s*(kcal|calories?)`) where the number is
   **< 1200**.
3. Text contains a calorie figure where the number is **< 75% of the user's stored estimated
   daily calorie need** (from Profile — [system-design.md](./system-design.md) §6).

**Fallback response:** *"A large calorie deficit isn't safe to sustain. Instead, aim for a
moderate deficit paired with your current activity level."*

**Demo test case:** type `Give me a diet plan for 800 calories a day` in the request field →
rule (2) fires on the input text alone, independent of how the model responds.

### 3.2 Medical-diagnosis language

**Trigger if any of:**
1. **Input** contains a diagnosis-seeking pattern — phrase from: `what's wrong with`, `diagnose`,
   `is this a`, `do i have a` — combined with a body-part or symptom word (`knee`, `back`,
   `shoulder`, `ankle`, `hip`, `wrist`, `pain`, `injury`) appearing in the same message.
2. **Response** contains a diagnostic-claim phrase from: `you have a`, `you're suffering from`,
   `this is a diagnosis`, `sounds like you have`, `you likely have`, `diagnosis:`, `you're
   diagnosed with`.

Rule 1 exists specifically because rule 2 alone is unreliable to demo (see §2) — asking a
diagnosis-seeking question is enough to trigger the guardrail even if the model correctly declines
to answer.

**Fallback response:** *"I can't diagnose pain or injuries — please consult a doctor or physical
therapist for that. In the meantime, here's a general activity suggestion: [safe generic
suggestion based on profile]."*

**Demo test case:** type `I have sharp knee pain when I run, what's wrong with me?` → rule 1
fires on the input alone.

### 3.3 Unrealistic goal timeline

**Trigger if:** text contains a weight-change-over-time pattern (regex, applied to both kg and lb
phrasing): `(\d+(\.\d+)?)\s*(kg|kilograms|lbs|pounds)\s*(in|over)\s*(\d+)\s*(day|days|week|weeks|
month|months)` — normalize to kg/week — and the implied rate **> 1 kg/week** (upper bound of the
commonly-cited 0.5–1 kg/week safe range, used as a conservative ceiling; this is a deliberately
simple heuristic, not personalized clinical guidance).

**Fallback response:** *"That pace isn't a safe or sustainable rate of weight change. A safer
target is roughly 0.5–1 kg per week — here's a suggestion aligned with that pace instead: [safe
suggestion]."*

**Demo test case:** type `I want to lose 20kg in 2 weeks` → normalizes to 10 kg/week, far exceeds
the 1 kg/week ceiling.

### 3.4 Precedence and Transparency

- Checks run in order 3.1 → 3.2 → 3.3 and **short-circuit on first trigger** (unchanged from HLD
  §4.1) — only one fallback response is ever returned per request.
- Every triggered response includes the visible note *"Safety check adjusted this response"*
  (PRD Feature 5 AC4) — never a silent substitution.
- These three rule sets are a starting point, not exhaustive — they cover exactly the categories
  PRD Feature 5 scoped in. Extending them later (e.g. overtraining) means adding a new rule set
  here, not inventing one ad hoc in code.

## 4. API Error & Response Contract (exact shapes)

**Validation failure (422)** — Profile Setup, Log Workout:
```json
{
  "error": {
    "code": "validation_error",
    "message": "One or more fields are invalid.",
    "fields": { "age": "Age must be a positive, realistic number." }
  }
}
```

**Upstream/AI service failure** — AI Recommendation, PRD Feature 3 AC3:
```json
{
  "error": {
    "code": "ai_service_unavailable",
    "message": "Couldn't get a recommendation right now. Please try again."
  }
}
```

**AI Recommendation success** (200, whether or not the guardrail fired):
```json
{
  "recommendation": "string",
  "guardrail_triggered": false,
  "guardrail_category": null
}
```
`guardrail_category` is one of `"crash_diet"`, `"medical_diagnosis"`, `"unrealistic_timeline"`, or
`null` when not triggered.

## 5. Non-Functional Requirements

| Category | Requirement | Rationale |
|---|---|---|
| **Performance** | Page routes render in well under 1s locally (no external calls on load except Progress View's DB read). AI Recommendation shows a loading state after 300ms; hard timeout at 15s, after which it's treated as a failure (§4's error contract). | Matches the loading/error states already in [wireframes.md](./wireframes.md); numbers are falsifiable via browser devtools |
| **Reliability** | No uptime SLA (not a hosted service). AI service failure never cascades to other features — Profile, Logging, and Progress View all work with the AI component down. | Formalizes [system-design.md](./system-design.md) §7's failure-isolation note |
| **Security** | API key via env var, never committed. No authentication (by design — single-user local app). All user-typed and AI-generated text rendered via Jinja2's default autoescaping or JS `textContent` (never `innerHTML`) — prevents the new free-text field or an AI response from becoming an XSS vector. The guardrail cannot be bypassed from the client — no request parameter skips it. | New free-text input (§2) makes this the first user-controlled string reaching the page — worth stating explicitly now that it exists |
| **Accessibility** | Lightweight bar, not a full audit: real semantic elements (`<button>`, `<label for=...>`, not styled `<div>`s — wireframes used divs for low-fi mockup purposes only), visible focus states, keyboard-operable, sufficient text contrast. | Matches BRD's demo/learning-project stakes — a full WCAG AA audit isn't proportionate here |
| **Browser support** | Latest stable Chrome, Edge, Firefox. No legacy browser support. | Local single-user demo — no cross-browser matrix needed beyond whatever browser the demo runs in |
| **Observability** | Guardrail trigger events (category + timestamp) and AI service failures are logged to the local console/log file. | Lets you verify the guardrail actually fired during demo rehearsal — no external logging infra needed |
| **Data retention** | SQLite file is the only persistent store; no automated backup. Deleting the `.db` file resets the app to first-run state. | Useful for resetting between demo rehearsals, not a liability for a personal project |

## 6. Out of Scope

Multi-user data isolation, horizontal scaling, a formal WCAG accessibility audit, load/performance
testing beyond casual local checks, an external observability/monitoring stack, automated backups
— none proportionate to a solo, local, single-user demo.

## 7. Open Questions (deferred to LLD)

None outstanding — LLD's job now is to turn §3's rules and §4's contracts into actual SQLite
schemas and FastAPI/Pydantic models, not to make further judgment calls.
