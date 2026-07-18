from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

FIELD_MESSAGES = {
    "name": "Name must be between 1 and 100 characters.",
    "age": "Age must be a positive, realistic number (13-100).",
    "fitness_goal": "Fitness goal must be 'lose_weight' or 'build_strength'.",
    "height_cm": "Height must be a realistic number in cm (100-250).",
    "weight_kg": "Weight must be a realistic number in kg (30-300).",
    "type": "Type must be one of: run, walk, strength_training, swim, cycle, other.",
    "duration_minutes": "Duration must be greater than zero.",
    "feeling": "Feeling must be one of: great, good, okay, tough, exhausting.",
    "range": "Range must be one of: week, month, year.",
}


async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """docs/nfr-guardrail-spec.md §4 — exact structured validation-error shape."""
    fields: dict[str, str] = {}
    for err in exc.errors():
        field = str(err["loc"][-1])
        fields[field] = FIELD_MESSAGES.get(field, err["msg"])
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_error",
                "message": "One or more fields are invalid.",
                "fields": fields,
            }
        },
    )
