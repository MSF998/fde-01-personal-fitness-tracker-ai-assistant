"""docs/lld.md §4 — GET /api/progress bucketing: daily for week/month, monthly for year."""

from datetime import datetime, timedelta

from app.data_access import list_workouts

RANGE_DAYS = {"week": 7, "month": 30}


def _shift_month(dt: datetime, months: int) -> datetime:
    total = dt.month - 1 + months
    year = dt.year + total // 12
    month = total % 12 + 1
    return dt.replace(year=year, month=month, day=1)


def _bucket_daily(workouts: list[dict], now: datetime, days: int):
    order: list[str] = []
    buckets: dict[str, dict] = {}
    for offset in range(days - 1, -1, -1):
        label = (now - timedelta(days=offset)).strftime("%b %d")
        buckets[label] = {"count": 0, "minutes": 0}
        order.append(label)

    for workout in workouts:
        label = datetime.fromisoformat(workout["logged_at"]).astimezone().strftime("%b %d")
        if label in buckets:
            buckets[label]["count"] += 1
            buckets[label]["minutes"] += workout["duration_minutes"]

    return order, buckets


def _bucket_monthly(workouts: list[dict], now: datetime):
    order: list[str] = []
    buckets: dict[str, dict] = {}
    base = now.replace(day=1)
    for offset in range(11, -1, -1):
        label = _shift_month(base, -offset).strftime("%b %Y")
        buckets[label] = {"count": 0, "minutes": 0}
        order.append(label)

    for workout in workouts:
        label = datetime.fromisoformat(workout["logged_at"]).astimezone().strftime("%b %Y")
        if label in buckets:
            buckets[label]["count"] += 1
            buckets[label]["minutes"] += workout["duration_minutes"]

    return order, buckets


def get_progress_stats(range_: str) -> dict:
    now = datetime.now().astimezone()
    window_days = 365 if range_ == "year" else RANGE_DAYS[range_]
    start = now - timedelta(days=window_days)

    in_range = [
        w
        for w in list_workouts()
        if datetime.fromisoformat(w["logged_at"]).astimezone() >= start
    ]

    if range_ == "year":
        order, buckets = _bucket_monthly(in_range, now)
    else:
        order, buckets = _bucket_daily(in_range, now, RANGE_DAYS[range_])

    return {
        "range": range_,
        "total_workouts": len(in_range),
        "total_duration_minutes": sum(w["duration_minutes"] for w in in_range),
        "workout_frequency": [{"period": p, "count": buckets[p]["count"]} for p in order],
        "duration_trend": [{"period": p, "minutes": buckets[p]["minutes"]} for p in order],
    }
