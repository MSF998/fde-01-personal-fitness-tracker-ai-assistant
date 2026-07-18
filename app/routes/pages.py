from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.data_access import get_profile
from app.formulas import calculate_bmi, calculate_estimated_daily_calories
from app.templating import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    """docs/user-flows.md Flow 1/0 — redirect-if-no-profile. Full Dashboard is M2's job."""
    profile = get_profile()
    if profile is None:
        return RedirectResponse(url="/profile/new", status_code=303)

    context = {
        "profile": profile,
        "bmi": calculate_bmi(profile["weight_kg"], profile["height_cm"]),
        "estimated_daily_calories": calculate_estimated_daily_calories(
            profile["weight_kg"], profile["height_cm"], profile["age"]
        ),
    }
    return templates.TemplateResponse(request, "index.html", context)


@router.get("/profile/new", response_class=HTMLResponse)
def profile_new(request: Request):
    """docs/wireframes.md Screen 1."""
    if get_profile() is not None:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(request, "profile_new.html", {})
