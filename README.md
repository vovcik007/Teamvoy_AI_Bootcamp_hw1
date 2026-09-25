# Homework 1: Health Tracker and Agent Skills

This homework began with a small full-stack project and then expanded into AI agent skill development. The project is a daily health tracker: you record wellness data, review previous entries, and see simple insights based on your logs. The included skill demonstrates how an agent can analyze a GitHub repository.

## What I built

- **Health Tracker:** A React and TypeScript interface for recording water intake, meals, sugar, sleep, work hours, and mood. It displays recent logs and summary statistics.
- **API and storage:** A FastAPI backend with SQLAlchemy and SQLite. It creates or updates one log per date, lists logs, and calculates average mood, sleep, and water intake. Its sleep insight compares mood on lower-sleep and higher-sleep days; it is a simple comparison, not a medical conclusion.
- **Agent skill:** [`github-repo-analyzer`](.agents/skills/github-repo-analyzer/SKILL.md) fetches repository structure and selected files to guide a structured technical report. It includes instructions, scripts, and output templates and schemas.

## Explore the code

| Path | Purpose |
| --- | --- |
| [`frontend/`](frontend/) | React UI and API client |
| [`backend/`](backend/) | FastAPI endpoints, data models, and SQLite setup |
| [`.agents/skills/`](.agents/skills/) | The repository analyzer skill and its supporting assets |
| [`output/`](output/) | Example analysis and review artifacts |

## Run the health tracker

Use Python 3 and Node.js. Open two terminals from this directory:

```bash
cd backend
python -m venv .venv
# Activate .venv for your shell, then:
pip install -r requirements.txt
uvicorn main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (normally `http://localhost:5173`). The API runs at `http://localhost:8000`; interactive API documentation is available at `/docs`. SQLite data is stored in `backend/health_tracker.db` relative to the backend working directory.

The agent skill is separate from the health tracker. Its `SKILL.md` explains the required GitHub access and how to run the helper scripts.
