# PrepPilot Backend API ⚡

> High-performance FastAPI backend microservice ecosystem powering PrepPilot's ATS resume diagnostic engine, adaptive AI mock proctoring, mentor marketplace, and readiness analytics.

---

## 🛠️ Tech Stack & Prerequisites

- **Python**: 3.11 or 3.12+
- **Framework**: FastAPI with Pydantic v2
- **Database & ORM**: SQLAlchemy 2.0 (async engine) + Alembic
- **PDF Extraction & ATS Engine**: `pypdf` + regex heuristic parsing + SDE/Data keyword matching
- **AI Integrations**: Google Gemini Flash (primary) + Groq LLaMA (fallback) with deterministic offline fallbacks

---

## 🚀 Quickstart: Starting the Backend Server

### 1. Navigate to the Backend Directory
```bash
cd backend
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
.\venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example environment file:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

> **Note**: External keys (`GEMINI_API_KEY`, `GROQ_API_KEY`, `DATABASE_URL`) are completely **optional** for local development. The backend is designed with resilient offline fallbacks and an in-memory repository cache so all ATS features work out-of-the-box with **$0 budget**.

### 5. Launch the Server

Start the FastAPI server with live hot-reloading:

```bash
uvicorn app.main:app --reload --port 8000
```
*(Alternatively: `python -m uvicorn app.main:app --reload --port 8000`)*

The server will be live at:
- **API Root**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs (OpenAPI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Interactive UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

## 🧪 Testing the ATS Engine & Endpoints

You can verify the backend installation and the complete ATS scoring engine using the built-in test suites:

### Run the Core ATS Diagnostic Suite
Tests PDF parsing, contact extraction, SDE/Data keyword matching, formatting evaluation, candidate database logging, and applicant ranking:
```bash
python tests/test_ats_engine.py
```

### Run FastAPI HTTP Endpoint Integration Tests
Tests live API routes (`/health`, `/keywords`, `/analyze`, `/candidates`, `/rank`, `/match-jd`):
```bash
python tests/test_api_endpoints.py
```

---

## 📡 Key ATS API Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/api/resume/analyze` | Upload a PDF resume (`multipart/form-data`) with optional `target_role` and `job_description`. Returns structured contact details, work history, education, categorized skills, ATS score (0-100), and logs the applicant. |
| `GET` | `/api/resume/keywords` | Returns the standardized keyword pool and taxonomy for 9 SDE and Data roles, 29 programming languages, frameworks, databases, and cloud tools. |
| `GET` | `/api/resume/candidates` | Returns all applicants logged in the candidate database with ATS scores and contact details. |
| `POST` | `/api/resume/rank` | Ranks all logged applicants against a target role or Job Description from highest to lowest score. |
| `POST` | `/api/resume/match-jd` | Compares raw resume text or an applicant ID against a custom pasted Job Description to compute keyword overlap. |
| `GET` | `/api/resume/reports/{id}` | Fetches an existing resume analysis report by ID. |
| `GET` | `/api/resume/health` | Health check for the resume microservice. |

### Example: Uploading a Resume via `curl`

```bash
curl -X POST "http://localhost:8000/api/resume/analyze" \
  -F "file=@/path/to/resume.pdf" \
  -F "target_role=sde" \
  -F "job_description=Looking for a Senior Backend Engineer proficient in Python, FastAPI, Docker, and PostgreSQL."
```

### Example: Ranking Applicants for a Job Description

```bash
curl -X POST "http://localhost:8000/api/resume/rank" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior Software Engineer with Python, Redis, System Design, and Kubernetes experience."
  }'
```

---

## 📂 Project Architecture

```
backend/
├── app/
│   ├── api/                           # Public API routers forwarding to microservices
│   ├── core/                          # Config, security, and database session setup
│   ├── models/                        # SQLAlchemy database models
│   ├── schemas/                       # Pydantic v2 request & response schemas
│   ├── services/
│   │   ├── resume_review/             # Isolated ATS Resume Review Microservice
│   │   │   ├── keyword_pool.py        # SDE & Data taxonomies, tools, and action verbs
│   │   │   ├── parser.py              # PDF text extraction, contact, history & education parser
│   │   │   ├── matcher.py             # Keyword matching against JDs & role profiles
│   │   │   ├── evaluator.py           # Formatting, section completeness & impact evaluator
│   │   │   ├── models.py              # CandidateApplicant & ResumeReport models
│   │   │   ├── schemas.py             # Pydantic schemas for the service
│   │   │   ├── service.py             # Pipeline orchestrator & applicant ranking logic
│   │   │   └── api.py                 # Service HTTP endpoints
│   │   └── ai_service.py              # Gemini & Groq LLM integration with mock fallback
│   └── main.py                        # FastAPI application entrypoint & CORS middleware
├── tests/
│   ├── test_ats_engine.py             # End-to-end ATS scoring & ranking unit tests
│   └── test_api_endpoints.py          # FastAPI endpoint integration tests
├── requirements.txt                   # Production dependencies
├── .env.example                       # Environment template
└── README.md                          # Backend instructions (this file)
```
