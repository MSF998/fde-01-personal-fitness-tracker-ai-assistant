from fastapi import APIRouter, Query

from app.progress import get_progress_stats
from app.schemas import ProgressRange, ProgressResponse

router = APIRouter(prefix="/api")


@router.get("/progress", response_model=ProgressResponse)
def api_progress(range: ProgressRange = Query("week")) -> ProgressResponse:
    return ProgressResponse(**get_progress_stats(range))
