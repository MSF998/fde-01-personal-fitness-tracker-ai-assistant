from datetime import datetime, timedelta


def group_by_day_label(workouts: list[dict]) -> list[tuple[str, list[dict]]]:
    """Groups already-most-recent-first workouts into (day_label, [workouts]) pairs,
    preserving order. Labels: Today / Yesterday / 'Jul 15' (docs/wireframes.md Screen 4).

    logged_at is stored in UTC; grouping uses local time since this is a single-user
    local app — the server's local time is the user's local time.
    """
    today = datetime.now().astimezone().date()
    groups: list[tuple[str, list[dict]]] = []
    for workout in workouts:
        logged_local = datetime.fromisoformat(workout["logged_at"]).astimezone()
        day = logged_local.date()
        if day == today:
            label = "Today"
        elif day == today - timedelta(days=1):
            label = "Yesterday"
        else:
            label = logged_local.strftime("%b %d")

        if groups and groups[-1][0] == label:
            groups[-1][1].append(workout)
        else:
            groups.append((label, [workout]))
    return groups
