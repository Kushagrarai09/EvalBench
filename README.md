# EvalBench — Human Evaluation Workbench

**EvalBench** is a web-based platform for annotating text, evaluating AI-generated responses, comparing response quality, and checking dataset quality.

When an AI system generates multiple answers to the same question, how do we determine which answer is better? EvalBench provides a structured workspace where human evaluators can label text, score responses, record preferences, explain their decisions, and export the results for further analysis.

This project is an educational MVP built with **React, Vite, FastAPI, SQLAlchemy, SQLite, and pandas**.

## ✨ Key Features

### 1. Text Annotation
Apply consistent labels to text using predefined categories:

- **Sentiment:** Positive, negative, or neutral.
- **Intent:** Identify the purpose of the text.
- **Relevance:** Determine whether the text is relevant to the task.
- **Text quality:** Assess clarity and readability.

### 2. AI Response Evaluation & Ranking
Compare two AI-generated responses to the same prompt.

- Rate each response on factual accuracy, relevance, clarity, and instruction-following.
- Assign scores from **1 to 5** for each evaluation criterion.
- Select the preferred response: **A, B, Tie, or Both Bad**.
- Record an error category and a written rationale explaining the decision.
- Save the evaluation as structured data.

### 3. Quality Assurance
Improve dataset consistency through basic validation and quality checks.

- Validate required fields and rating ranges.
- Identify duplicate prompts for human review.
- Inspect potential data-quality issues.
- Track annotation progress and evaluation statistics.

### 4. Dataset Import & Export
- Import annotation tasks from CSV or JSON files.
- Export collected evaluation data as CSV or JSON.
- Use the included sample dataset to explore the workflow.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| React | Interactive user interface |
| Vite | Frontend development server and build tool |
| Python | Backend programming language |
| FastAPI | REST API |
| SQLAlchemy | Database access and ORM |
| SQLite | Local data storage |
| pandas | Tabular dataset processing |
| CSV / JSON | Dataset import and export |

## 📁 Project Structure

```text
evalbench/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── requirements.txt
│   ├── seed.py
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   └── vite.config.js
├── sample_dataset.csv
├── start-windows.ps1
├── .gitignore
└── README.md
```

## 🚀 Run Locally on Windows

### Prerequisites

Install the following:

- [Python](https://www.python.org/downloads/) — use a version compatible with the backend dependencies.
- [Node.js](https://nodejs.org/) — includes npm.
- [Git](https://git-scm.com/downloads) — optional, for cloning the repository.

### Step 1: Get the Project

Clone the repository:

```bash
git clone https://github.com/Kushagrarai09/EvalBench.git
cd EvalBench
```

Alternatively, download the repository ZIP from GitHub and extract it.

### Step 2: Start the Backend

Open the project in VS Code and open a terminal in the project root.

Run these commands **one at a time**:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create your local environment configuration if it does not already exist:

```powershell
Copy-Item .env.example .env
```

Initialize the sample data:

```powershell
python seed.py
```

Start the API server:

```powershell
uvicorn app.main:app --reload
```

The backend should now be available at:

- **API:** http://127.0.0.1:8000
- **Interactive API documentation:** http://127.0.0.1:8000/docs

Keep this terminal open.

### Step 3: Start the Frontend

Open a **second terminal** in VS Code. From the project root, run:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, usually:

**http://localhost:5173**

Keep both terminals running while using EvalBench.

### macOS / Linux

Create and activate the backend virtual environment using:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then configure the environment, initialize sample data, and start the backend as described above.

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

## 🔄 How to Use EvalBench

1. **Explore the overview:** Check the available tasks and evaluation statistics.
2. **Open a task:** Review its prompt, text, and candidate responses.
3. **Annotate the text:** Assign sentiment, intent, relevance, and text-quality labels.
4. **Evaluate responses:** Rate Responses A and B on the four evaluation criteria.
5. **Choose a preference:** Select A, B, Tie, or Both Bad.
6. **Explain your decision:** Record the relevant error category and rationale.
7. **Save and validate:** Submit the annotation and review any quality issues.
8. **Export the dataset:** Download the structured results as CSV or JSON for further analysis.

**Tip:** Start with `sample_dataset.csv` to understand the expected data format before importing your own dataset.

## 📄 Dataset Format

For CSV or JSON imports, each record must contain a `prompt` field.

Optional fields include:

- `text`
- `response_a`
- `response_b`
- `source`

Example:

```json
{
  "prompt": "What is the capital of France?",
  "response_a": "Paris is the capital of France.",
  "response_b": "Lyon is the capital of France.",
  "source": "sample"
}
```

## 🗄️ Database

EvalBench uses SQLite for local persistence. The database is stored at:

```text
backend/evalbench.db
```

To reset the local database, stop the backend, delete the database file, and rerun `python seed.py` from the backend directory.

**Warning:** Resetting the database deletes its stored data. Export anything you want to keep first.

## 🎯 Project Scope & Limitations

EvalBench is a local MVP focused on collecting structured human feedback.

- It does not train a reward model or perform reinforcement learning.
- It does not automatically improve an AI model.
- The local MVP does not include login or multi-user identity.
- Duplicate-prompt checks are warnings for human review, not proof that two records are identical in meaning.
- Annotation agreement is not calculated because tasks have only one annotation in the current workflow.

### Future Improvements

- User authentication and role-based access.
- Independent annotations from multiple reviewers.
- Review and adjudication workflows.
- PostgreSQL support and database migrations.
- Audit logs and automated tests.
- Advanced dataset analytics and reporting.

## 📌 Why This Project?

EvalBench demonstrates practical skills in full-stack development, REST API design, database integration, data validation, dataset processing, and AI evaluation workflows.

It provides a foundation for understanding how human feedback can be collected and organized to support AI quality assessment and future model-development experiments.

---

**Built with React, FastAPI, SQLite, and Python.**