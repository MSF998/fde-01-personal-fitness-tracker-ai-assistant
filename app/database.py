import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "fitness_tracker.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS profile (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK (length(name) BETWEEN 1 AND 100),
    age INTEGER NOT NULL CHECK (age BETWEEN 13 AND 100),
    fitness_goal TEXT NOT NULL CHECK (fitness_goal IN ('lose_weight', 'build_strength')),
    height_cm REAL NOT NULL CHECK (height_cm BETWEEN 100 AND 250),
    weight_kg REAL NOT NULL CHECK (weight_kg BETWEEN 30 AND 300),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS workout (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK (
        type IN ('run', 'walk', 'strength_training', 'swim', 'cycle', 'other')
    ),
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    feeling TEXT NOT NULL CHECK (
        feeling IN ('great', 'good', 'okay', 'tough', 'exhausting')
    ),
    logged_at TEXT NOT NULL
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create the profile/workout tables per docs/lld.md §3, if they don't exist yet."""
    DATA_DIR.mkdir(exist_ok=True)
    with get_connection() as conn:
        conn.executescript(SCHEMA)
