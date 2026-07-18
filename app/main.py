from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import config  # noqa: F401  (loads .env / OPENROUTER_API_KEY on import)
from app.database import init_db

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Personal Fitness Tracker", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
def placeholder(request: Request):
    """M0 scaffolding placeholder — replaced by the real Dashboard/redirect logic in M1/M2."""
    return templates.TemplateResponse(request, "index.html", {})
