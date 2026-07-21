# Personal Fitness Tracker AI Assistant

A web-based fitness tracker that lets users log workouts, track progress, and get AI-generated
recommendations — with a rule-based safety guardrail that intercepts unsafe or unrealistic advice
before it ever reaches the user.

Originally scoped from the FDE Academy Vibe Coding Lab hackathon brief, then developed through a
full pre-code design sequence (BRD → PRD → ... → Build Roadmap) before any implementation began.

## Features

- **User Profile Setup** — name, age, fitness goal, height, weight; BMI and estimated daily
  calorie need computed on the fly
- **Workout Logging** — record activity type, duration, and how it felt; full history grouped by
  date
- **Progress Dashboard** — workout frequency and duration trend charts across week/month/year
  ranges
- **AI Recommendations** — personalized next-step suggestions based on profile and recent
  activity, with an optional free-text request field
- **Safety Guardrail** — deterministic checks that catch crash-diet framing, medical diagnosis
  requests, and unrealistic weight-change timelines, substituting a safe response and flagging it
  transparently — never a silent swap

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) (Python) |
| Frontend | Jinja2 server-rendered templates + vanilla JavaScript |
| Charts | [Chart.js](https://www.chartjs.org/) (CDN) |
| Database | SQLite (embedded, zero-config) |
| AI provider | [OpenRouter](https://openrouter.ai/) — model configurable via env var |
| Deployment | Local only — no hosting/cloud dependency |

No authentication — this is a single-user, local application by design.

## Getting Started

### Prerequisites

- Python 3.11+
- An [OpenRouter](https://openrouter.ai/keys) API key (free-tier models available)

### Installation

```bash
git clone https://github.com/MSF998/fde-01-personal-fitness-tracker-ai-assistant.git
cd fde-01-personal-fitness-tracker-ai-assistant

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
```

Edit `.env` and set `OPENROUTER_API_KEY` to your own key. `OPENROUTER_MODEL` is optional and
defaults to a free-tier model.

### Run

```bash
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000**. A SQLite database file is created automatically on first run at
`data/fitness_tracker.db`.

## Project Structure

```
app/
├── main.py                 # FastAPI app, router registration, exception handlers
├── config.py                # Environment/secrets loading
├── database.py               # SQLite connection + schema
├── data_access.py             # All reads/writes to SQLite
├── formulas.py                 # BMI / estimated calorie need
├── formatting.py                # Day-label grouping, duration display
├── progress.py                    # Progress chart bucketing (week/month/year)
├── guardrail.py                    # Safety guardrail rules
├── ai_client.py                     # OpenRouter client + system prompt
├── schemas.py                        # Pydantic request/response models
├── errors.py                          # Structured error responses
├── routes/                             # Page routes + JSON API routes
├── templates/                           # Jinja2 templates
└── static/                               # CSS + vanilla JS
docs/                                     # Full design documentation (see below)
```

## Design Documentation

This project was built from a complete pre-code design sequence, kept in [`docs/`](docs/):

| Stage | Document |
|---|---|
| Business Requirements | [BRD.md](docs/BRD.md) |
| Product Requirements | [PRD.md](docs/PRD.md) |
| User Flows | [user-flows.md](docs/user-flows.md) |
| Wireframes | [wireframes.md](docs/wireframes.md) / [wireframes.html](docs/wireframes.html) |
| System Design | [system-design.md](docs/system-design.md) |
| High-Level Design | [hld.md](docs/hld.md) |
| NFRs & Guardrail Spec | [nfr-guardrail-spec.md](docs/nfr-guardrail-spec.md) |
| Low-Level Design | [lld.md](docs/lld.md) |
| Build Roadmap | [build-roadmap.md](docs/build-roadmap.md) |
| Design Improvement Plan | [design-improvement-plan.md](docs/design-improvement-plan.md) |

A reusable, project-agnostic reference guide for each document type (what it is, how to write one,
common mistakes) is also kept under [`docs/reference/`](docs/reference/).

## Status

All core features (M0–M6 in the build roadmap) are implemented and verified: profile setup,
workout logging, progress view, and AI recommendations with the safety guardrail. A UI/UX design
pass is planned next — see [design-improvement-plan.md](docs/design-improvement-plan.md).

## Safety & Ethics

The AI recommendation feature is clearly labeled as AI-generated and includes a disclaimer that it
is not medical advice. The guardrail's exact trigger rules and fallback behavior are fully
documented and testable — see [nfr-guardrail-spec.md](docs/nfr-guardrail-spec.md) §3.

## License

[MIT](LICENSE)

## Acknowledgments

Built as part of the FDE Academy Vibe Coding Lab. Implementation assisted by Claude Code, directed
against the design documents in `docs/`.
