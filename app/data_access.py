from datetime import datetime, timezone

from app.database import get_connection


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_profile() -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM profile ORDER BY id LIMIT 1").fetchone()
        return dict(row) if row else None


def save_profile(data: dict) -> dict:
    """Single-user app (docs/system-design.md) — one row, inserted once, updated after."""
    now = _now()
    with get_connection() as conn:
        existing = conn.execute("SELECT id FROM profile ORDER BY id LIMIT 1").fetchone()
        if existing:
            conn.execute(
                """UPDATE profile
                   SET name = ?, age = ?, fitness_goal = ?, height_cm = ?, weight_kg = ?,
                       updated_at = ?
                   WHERE id = ?""",
                (
                    data["name"],
                    data["age"],
                    data["fitness_goal"],
                    data["height_cm"],
                    data["weight_kg"],
                    now,
                    existing["id"],
                ),
            )
        else:
            conn.execute(
                """INSERT INTO profile
                       (name, age, fitness_goal, height_cm, weight_kg, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    data["name"],
                    data["age"],
                    data["fitness_goal"],
                    data["height_cm"],
                    data["weight_kg"],
                    now,
                    now,
                ),
            )
        conn.commit()
        row = conn.execute("SELECT * FROM profile ORDER BY id LIMIT 1").fetchone()
        return dict(row)


def create_workout(data: dict) -> dict:
    """logged_at defaults to insert time (docs/lld.md §3) — never client-supplied."""
    now = _now()
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO workout (type, duration_minutes, feeling, logged_at)
               VALUES (?, ?, ?, ?)""",
            (data["type"], data["duration_minutes"], data["feeling"], now),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM workout WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return dict(row)


def list_workouts(limit: int | None = None) -> list[dict]:
    """Most-recent-first (docs/lld.md PRD Feature 2 AC3). Shared by Dashboard's recent-activity
    list (M2, limited) and the full Workout History page (M3, unlimited)."""
    query = "SELECT * FROM workout ORDER BY logged_at DESC, id DESC"
    params: tuple = ()
    if limit is not None:
        query += " LIMIT ?"
        params = (limit,)
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]
