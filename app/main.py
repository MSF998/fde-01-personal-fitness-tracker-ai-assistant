from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from app import config  # noqa: F401  (loads .env / OPENROUTER_API_KEY on import)
from app.database import init_db
from app.errors import validation_error_handler
from app.routes import pages, profile_api, progress_api, workout_api
from app.templating import BASE_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Personal Fitness Tracker", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.add_exception_handler(RequestValidationError, validation_error_handler)

app.include_router(pages.router)
app.include_router(profile_api.router)
app.include_router(workout_api.router)
app.include_router(progress_api.router)
