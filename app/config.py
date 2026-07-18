import os

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
# docs/hld.md §2 — model name read from env var, not hardcoded; falls back to the model
# decided in docs/build-roadmap.md.
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemma-4-31b-it:free")
