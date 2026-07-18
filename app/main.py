import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from app import config  # noqa: F401  (loads .env / OPENROUTER_API_KEY on import)
from app.ai_client import AIServiceError
from app.database import init_db
from app.errors import ai_service_error_handler, validation_error_handler
from app.routes import pages, profile_api, progress_api, recommendation_api, workout_api
from app.templating import BASE_DIR

# docs/nfr-guardrail-spec.md §5 — guardrail triggers and AI-service failures are logged
# to console with category + timestamp. No external logging infra needed (solo/local scope).
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Personal Fitness Tracker", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(AIServiceError, ai_service_error_handler)

app.include_router(pages.router)
app.include_router(profile_api.router)
app.include_router(workout_api.router)
app.include_router(progress_api.router)
app.include_router(recommendation_api.router)
