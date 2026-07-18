import logging

from fastapi import APIRouter

from app.ai_client import SYSTEM_PROMPT, build_user_message, get_ai_response
from app.data_access import get_profile, list_workouts
from app.formulas import calculate_estimated_daily_calories
from app.guardrail import check_guardrail
from app.schemas import RecommendationRequest, RecommendationResponse

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@router.post("/recommendation", response_model=RecommendationResponse)
async def get_recommendation(payload: RecommendationRequest) -> RecommendationResponse:
    """docs/hld.md §5.3 — build prompt -> call OpenRouter -> guardrail checks -> respond.
    AIServiceError (missing key, timeout, upstream failure) is caught by the exception
    handler in app/errors.py, not here — matches the validation-error pattern already
    used for /api/profile and /api/workouts."""
    profile = get_profile()
    workouts = list_workouts(limit=5)
    estimated_daily_calories = calculate_estimated_daily_calories(
        profile["weight_kg"], profile["height_cm"], profile["age"]
    )

    user_message = build_user_message(profile, workouts, payload.message)
    ai_response = await get_ai_response(SYSTEM_PROMPT, user_message)

    combined_text = f"{payload.message or ''}\n{ai_response}"
    trigger = check_guardrail(combined_text, estimated_daily_calories)

    if trigger:
        logger.info("guardrail triggered category=%s", trigger["category"])
        return RecommendationResponse(
            recommendation=trigger["message"],
            guardrail_triggered=True,
            guardrail_category=trigger["category"],
        )
    return RecommendationResponse(
        recommendation=ai_response, guardrail_triggered=False, guardrail_category=None
    )
