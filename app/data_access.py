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
