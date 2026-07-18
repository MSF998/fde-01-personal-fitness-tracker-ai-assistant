from fastapi import APIRouter

from app.data_access import save_profile
from app.formulas import calculate_bmi, calculate_estimated_daily_calories
from app.schemas import ProfileCreateRequest, ProfileResponse

router = APIRouter(prefix="/api")


@router.post("/profile", response_model=ProfileResponse)
def create_profile(payload: ProfileCreateRequest) -> ProfileResponse:
    saved = save_profile(payload.model_dump())
    return ProfileResponse(
        name=saved["name"],
        age=saved["age"],
        fitness_goal=saved["fitness_goal"],
        height_cm=saved["height_cm"],
        weight_kg=saved["weight_kg"],
        bmi=calculate_bmi(saved["weight_kg"], saved["height_cm"]),
        estimated_daily_calories=calculate_estimated_daily_calories(
            saved["weight_kg"], saved["height_cm"], saved["age"]
        ),
    )
