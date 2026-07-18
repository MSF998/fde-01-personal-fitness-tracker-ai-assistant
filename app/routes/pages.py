from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.data_access import get_profile, has_logged_any_workout, list_workouts
from app.formatting import format_duration, group_by_day_label
from app.formulas import calculate_bmi, calculate_estimated_daily_calories
from app.progress import get_progress_stats
from app.templating import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    """docs/wireframes.md Screen 2. Get AI Recommendation tile opens a placeholder modal
    until M5 fills it in."""
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


@router.get("/progress", response_class=HTMLResponse)
def progress_page(request: Request):
    """docs/wireframes.md Screen 6. Empty state is based on whether the user has EVER logged
    a workout, not whether the default "week" range happens to be empty (see app/progress.py)."""
    has_data = has_logged_any_workout()
    stats = get_progress_stats("week") if has_data else None
    context = {
        "has_data": has_data,
        "stats": stats,
        "total_duration_display": format_duration(stats["total_duration_minutes"])
        if stats
        else None,
    }
    return templates.TemplateResponse(request, "progress.html", context)
