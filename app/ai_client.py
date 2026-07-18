"""docs/hld.md §4.2 — builds prompts, calls OpenRouter, never returns unchecked to the browser
(the guardrail, not this module, is what enforces that — see app/guardrail.py and
routes/recommendation_api.py)."""

import httpx

from app import config

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT_SECONDS = 15  # docs/nfr-guardrail-spec.md §5

# docs/build-roadmap.md §2 — reuses the NFR spec's exact numeric thresholds so the model's
# own instructions and the rule-based guardrail agree with each other.
SYSTEM_PROMPT = """You are the AI assistant inside a personal fitness tracker app. Your job is to give the user a short, specific, encouraging suggestion for what to do next, based on their profile (fitness goal, age, height, weight) and their recent workout history. If the user has asked a specific question, address it directly.

You are not a doctor, dietitian, or medical professional. Never diagnose an injury, pain, or medical condition — if asked, say you can't diagnose and recommend seeing a doctor or physical therapist instead.

Never suggest a daily calorie intake below 1200 kcal, or more than 25% below the user's estimated maintenance calorie need. Never suggest losing or gaining weight faster than about 1 kg per week.

Keep your response to 2-4 sentences. Be specific to the user's goal and recent activity, not generic. Be encouraging and practical, not clinical."""

GOAL_LABELS = {"lose_weight": "lose weight", "build_strength": "build strength"}


class AIServiceError(Exception):
    """Raised on any OpenRouter failure — caught by a dedicated handler (app/errors.py) that
    returns the ai_service_unavailable shape (docs/nfr-guardrail-spec.md §4)."""


def build_user_message(profile: dict, workouts: list[dict], user_request: str | None) -> str:
    lines = [f"My fitness goal is to {GOAL_LABELS[profile['fitness_goal']]}."]
    if workouts:
        lines.append("My recent workouts:")
        lines.extend(
            f"- {w['type']}, {w['duration_minutes']} min, felt {w['feeling']}" for w in workouts
        )
    else:
        lines.append("I haven't logged any workouts yet.")
    lines.append(f"Specific request: {user_request}" if user_request else "Give me a suggestion for what to do next.")
    return "\n".join(lines)


async def get_ai_response(system_prompt: str, user_message: str) -> str:
    if not config.OPENROUTER_API_KEY:
        raise AIServiceError("OPENROUTER_API_KEY is not configured")

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.post(
                OPENROUTER_URL,
                headers={"Authorization": f"Bearer {config.OPENROUTER_API_KEY}"},
                json={
                    "model": config.OPENROUTER_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message},
                    ],
                },
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise AIServiceError(str(exc)) from exc

    try:
        return response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as exc:
        raise AIServiceError("Unexpected OpenRouter response shape") from exc
