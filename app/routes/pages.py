from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.data_access import get_profile, list_workouts
from app.formatting import group_by_day_label
from app.formulas import calculate_bmi, calculate_estimated_daily_calories
from app.templating import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    """docs/wireframes.md Screen 2. Log Workout / Get AI Recommendation tiles open placeholder
    modals until M3/M5 fill them in; View Progress links to /progress (404 until M4)."""
    profile = get_profile()
    if profile is None:
        return RedirectResponse(url="/profile/new", status_code=303)

    context = {
        "profile": profile,
        "bmi": calculate_bmi(profile["weight_kg"], profile["height_cm"]),
        "estimated_daily_calories": calculate_estimated_daily_calories(
            profile["weight_kg"], profile["height_cm"], profile["age"]
        ),
        "workouts": list_workouts(limit=5),
    }
    return templates.TemplateResponse(request, "index.html", context)


@router.get("/profile/new", response_class=HTMLResponse)
def profile_new(request: Request):
    """docs/wireframes.md Screen 1."""
    if get_profile() is not None:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(request, "profile_new.html", {})


@router.get("/workouts", response_class=HTMLResponse)
def workout_history(request: Request):
    """docs/wireframes.md Screen 4 — most-recent-first, grouped by date."""
    groups = group_by_day_label(list_workouts())
    return templates.TemplateResponse(request, "workouts.html", {"groups": groups})
