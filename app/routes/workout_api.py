from fastapi import APIRouter

from app.data_access import create_workout, list_workouts
from app.schemas import WorkoutCreateRequest, WorkoutListResponse, WorkoutResponse

router = APIRouter(prefix="/api")


@router.post("/workouts", response_model=WorkoutResponse)
def log_workout(payload: WorkoutCreateRequest) -> WorkoutResponse:
    return WorkoutResponse(**create_workout(payload.model_dump()))


@router.get("/workouts", response_model=WorkoutListResponse)
def get_workouts() -> WorkoutListResponse:
    return WorkoutListResponse(workouts=[WorkoutResponse(**w) for w in list_workouts()])
