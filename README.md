# EvalBench — Human Evaluation Workbench

Three core workflows:
1. **Text annotation:** consistent sentiment, intent, relevance, and text-quality labels.
2. **AI response evaluation and ranking:** rate A and B for accuracy, relevance, clarity, and instruction-following (1–5), choose A/B/Tie/Both bad, and record a rationale.
3. **Quality assurance:** validate required fields and rating ranges, flag duplicate prompts, inspect issues, then export structured CSV/JSON.

Stack: React + Vite, FastAPI, SQLAlchemy + SQLite, pandas. This MVP collects human feedback; it does not train a reward model or perform reinforcement learning.

## Local setup (Windows PowerShell)
Open two terminals in VS Code.

### Terminal 1 — backend
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# If PowerShell blocks activation: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python seed.py
uvicorn app.main:app --reload
```
API: http://127.0.0.1:8000 — docs: http://127.0.0.1:8000/docs

### Terminal 2 — frontend
```powershell
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

macOS/Linux: backend activation is `source .venv/bin/activate`; create the venv with `python3 -m venv .venv`. Run `npm install && npm run dev` in frontend.

## Workflow
Overview → Annotation queue → open task → assign four text labels → rate both responses → choose preference → explain rationale → Validate & complete → Quality checks → export.

CSV/JSON import requires `prompt`; optional fields are `text`, `response_a`, `response_b`, and `source`. A sample CSV is included. SQLite lives at `backend/evalbench.db`; stop the API and delete that file to reset, then rerun `python seed.py`.

## Scope
No login/multi-user identity in this local MVP. Agreement is not calculated because each task has one annotation. Duplicate prompts are warnings for human review. Production next steps: authentication, independent multi-annotator records, review/adjudication, migrations, PostgreSQL, audit logs, automated tests.
