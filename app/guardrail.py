"""docs/nfr-guardrail-spec.md §3 — exact, testable guardrail rules.

Runs against the concatenation of the user's typed request and the AI's response
(§2's amendment over HLD's original response-only design) — either side triggering
is enough, since a well-aligned model often won't produce a clean diagnosis on its
own for an output-only check to catch.
"""

import re

CRASH_DIET_PHRASES = [
    "crash diet",
    "starve",
    "starving",
    "skip meals",
    "skip breakfast",
    "water fast",
    "zero calorie",
    "extremely low calorie",
    "very low calorie diet",
]
CALORIE_PATTERN = re.compile(r"(\d{3,4})\s*(?:kcal|calories?)", re.IGNORECASE)

DIAGNOSIS_SEEKING_PHRASES = [
    "what's wrong with",
    "whats wrong with",
    "diagnose",
    "is this a",
    "do i have a",
]
BODY_PART_OR_SYMPTOM_WORDS = [
    "knee",
    "back",
    "shoulder",
    "ankle",
    "hip",
    "wrist",
    "pain",
    "injury",
]
DIAGNOSTIC_CLAIM_PHRASES = [
    "you have a",
    "you're suffering from",
    "this is a diagnosis",
    "sounds like you have",
    "you likely have",
    "diagnosis:",
    "you're diagnosed with",
]

TIMELINE_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*(kg|kilograms|lbs|pounds)\s*(?:in|over)\s*"
    r"(\d+)\s*(day|days|week|weeks|month|months)",
    re.IGNORECASE,
)
LBS_TO_KG = 0.453592
WEEKS_PER_MONTH = 4.345
SAFE_KG_PER_WEEK_CEILING = 1.0

FALLBACK_MESSAGES = {
    "crash_diet": (
        "A large calorie deficit isn't safe to sustain. Instead, aim for a moderate "
        "deficit paired with your current activity level."
    ),
    "medical_diagnosis": (
        "I can't diagnose pain or injuries — please consult a doctor or physical "
        "therapist for that. In the meantime, general low-impact activity and rest "
        "as needed is a safe default until you've been seen."
    ),
    "unrealistic_timeline": (
        "That pace isn't a safe or sustainable rate of weight change. A safer target "
        "is roughly 0.5-1 kg per week — consistent, moderate activity paired with a "
        "modest calorie adjustment will get you there safely."
    ),
}


def _check_crash_diet(text: str, estimated_daily_calories: int) -> bool:
    lowered = text.lower()
    if any(phrase in lowered for phrase in CRASH_DIET_PHRASES):
        return True
    for match in CALORIE_PATTERN.finditer(text):
        value = int(match.group(1))
        if value < 1200 or value < 0.75 * estimated_daily_calories:
            return True
    return False


def _check_medical_diagnosis(text: str) -> bool:
    lowered = text.lower()
    seeking = any(phrase in lowered for phrase in DIAGNOSIS_SEEKING_PHRASES)
    body_or_symptom = any(word in lowered for word in BODY_PART_OR_SYMPTOM_WORDS)
    if seeking and body_or_symptom:
        return True
    return any(phrase in lowered for phrase in DIAGNOSTIC_CLAIM_PHRASES)


def _check_unrealistic_timeline(text: str) -> bool:
    for match in TIMELINE_PATTERN.finditer(text):
        amount = float(match.group(1))
        unit = match.group(2).lower()
        period_num = int(match.group(3))
        period_unit = match.group(4).lower()

        kg = amount * LBS_TO_KG if unit in ("lbs", "pounds") else amount

        if period_unit.startswith("day"):
            weeks = period_num / 7
        elif period_unit.startswith("week"):
            weeks = period_num
        else:
            weeks = period_num * WEEKS_PER_MONTH

        if weeks > 0 and (kg / weeks) > SAFE_KG_PER_WEEK_CEILING:
            return True
    return False


def check_guardrail(combined_text: str, estimated_daily_calories: int) -> dict | None:
    """Runs the three checks in order, short-circuiting on first trigger (§3.4).
    Returns None if nothing triggers, else {"category": ..., "message": ...}."""
    if _check_crash_diet(combined_text, estimated_daily_calories):
        return {"category": "crash_diet", "message": FALLBACK_MESSAGES["crash_diet"]}
    if _check_medical_diagnosis(combined_text):
        return {"category": "medical_diagnosis", "message": FALLBACK_MESSAGES["medical_diagnosis"]}
    if _check_unrealistic_timeline(combined_text):
        return {
            "category": "unrealistic_timeline",
            "message": FALLBACK_MESSAGES["unrealistic_timeline"],
        }
    return None
