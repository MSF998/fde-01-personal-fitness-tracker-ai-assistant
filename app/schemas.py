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


WorkoutType = Literal["run", "walk", "strength_training", "swim", "cycle", "other"]
Feeling = Literal["great", "good", "okay", "tough", "exhausting"]


class WorkoutCreateRequest(BaseModel):
    """docs/lld.md §4 — POST /api/workouts request; enums/bounds from §3's schema."""

    type: WorkoutType
    duration_minutes: int = Field(..., gt=0)
    feeling: Feeling


class WorkoutResponse(BaseModel):
    """docs/lld.md §4 — POST /api/workouts response."""

    id: int
    type: WorkoutType
    duration_minutes: int
    feeling: Feeling
    logged_at: str


class WorkoutListResponse(BaseModel):
    """docs/lld.md §4 — GET /api/workouts response."""

    workouts: list[WorkoutResponse]


ProgressRange = Literal["week", "month", "year"]


class ProgressFrequencyPoint(BaseModel):
    period: str
    count: int


class ProgressDurationPoint(BaseModel):
    period: str
    minutes: int


class ProgressResponse(BaseModel):
    """docs/lld.md §4 — GET /api/progress response."""

    range: ProgressRange
    total_workouts: int
    total_duration_minutes: int
    workout_frequency: list[ProgressFrequencyPoint]
    duration_trend: list[ProgressDurationPoint]


GuardrailCategory = Literal["crash_diet", "medical_diagnosis", "unrealistic_timeline"]


class RecommendationRequest(BaseModel):
    """docs/lld.md §4 — POST /api/recommendation request. PRD Feature 3 AC5's optional field."""

    message: str | None = Field(default=None, max_length=500)


class RecommendationResponse(BaseModel):
    """docs/lld.md §4 — POST /api/recommendation response."""

    recommendation: str
    guardrail_triggered: bool
    guardrail_category: GuardrailCategory | None = None
