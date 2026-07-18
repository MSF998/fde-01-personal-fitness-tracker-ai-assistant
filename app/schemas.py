from typing import Literal

from pydantic import BaseModel, Field

FitnessGoal = Literal["lose_weight", "build_strength"]


class ProfileCreateRequest(BaseModel):
    """docs/lld.md §4 — POST /api/profile request; bounds from §3's schema constraints."""

    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=13, le=100)
    fitness_goal: FitnessGoal
    height_cm: float = Field(..., ge=100, le=250)
    weight_kg: float = Field(..., ge=30, le=300)


class ProfileResponse(BaseModel):
    """docs/lld.md §4 — POST /api/profile response."""

    name: str
    age: int
    fitness_goal: FitnessGoal
    height_cm: float
    weight_kg: float
    bmi: float
    estimated_daily_calories: int
