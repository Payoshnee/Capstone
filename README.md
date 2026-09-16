# PrepPilot 🚀

> **The Hybrid AI + Human-Expert Mock Interview Platform**  
> Prepare for high-stakes technical interviews with real-time AI adaptive simulations and calibrated FAANG+ human mentor mock sessions — backed by structured rubric telemetry and ATS diagnostics.

[![Next.js](https://img.shields.io/badge/Next.js-16.3.4-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4.0-38bdf8?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square&logo=python)](https://python.org/)
[![Supabase](https://img.shields.io/badge/Supabase-Postgres_%26_Auth-3ecf8e?style=flat-square&logo=supabase)](https://supabase.com/)
[![WebRTC](https://img.shields.io/badge/Video-Jitsi_Meet_WebRTC-17a2b8?style=flat-square)](https://jitsi.org/)
[![AI Models](https://img.shields.io/badge/AI-Gemini_Flash_%2B_Groq-8e44ad?style=flat-square)](https://deepmind.google/technologies/gemini/)
[![Budget](https://img.shields.io/badge/Budget-$0_Free_Tier_Stack-brightgreen?style=flat-square)](#tech-stack--0-budget-design)

---

## 📖 Overview

Technical interview preparation today is bifurcated between two extremes:
1. **Shallow AI bots & LeetCode grinds**: Algorithmic puzzle-solving without realistic architectural probing, behavioral follow-ups, or holistic candidate leveling.
2. **Expensive human mock platforms**: $250–$400/hour sessions with uncalibrated feedback and long turnaround times.

**PrepPilot** solves this with a **dual-engine preparation matrix**:
- **Continuous AI Proctoring (24/7)**: Adaptive conversational simulations powered by Google Gemini and Groq that probe trade-offs, concurrency bugs, and system architecture with live speech telemetry and whiteboard diagrams.
- **Calibrated Human Mentors**: Real FAANG+ Bar-Raisers and Principal Engineers delivering 1-on-1 mock interviews over end-to-end encrypted WebRTC video, backed by an enforceable **60-minute written rubric SLA**.
- **Unified Readiness Analytics**: Candidate progress synthesized into an ATS Diagnostic Score, a 6-axis Competency Radar, and a holistic Readiness Index.

---

## 🧩 The 7 Platform Microservices

PrepPilot is built around a modular architecture spanning 7 specialized services:

```
                                  ┌───────────────────────────────┐
                                  │   Target Job Description (JD) │
                                  └───────────────┬───────────────┘
                                                  │
                                                  ▼
                                    [Custom JD Blueprint Analyzer]
                                                  │
                 ┌────────────────────────────────┼────────────────────────────────┐
                 ▼                                ▼                                ▼
     [ATS Resume Diagnostic]            [24/7 AI Mock Proctor]           [Calibrated Mentor Room]
     • 4-Pillar Diff Engine             • AURA Adaptive Voice Loop       • 1-on-1 Jitsi WebRTC
     • Strikethrough Heatmaps           • Live ASCII Whiteboard Canvas   • FAANG Bar-Raisers
     • Greenhouse/Ashby Checks          • Real-time Speech Telemetry     • 60-min Rubric SLA
                 │                                │                                │
                 └────────────────────────────────┼────────────────────────────────┘
                                                  │
                                                  ▼
                                   [Candidate Readiness Report]
                                   • 6-Axis Competency Radar
                                   • Leveling Prediction (L5/L6/L7)
                                                  │
                                                  ▼
                                   [Suggested Jobs Matcher & Scraper]
                                   • Live Tech Openings & Gap Detection
```

| # | Service | Route | Status | Description |
|---|---|---|:---:|---|
| **1** | **Master Platform Hub** | `/` | ✅ Live | High-converting landing page with split-screen live session preview, microservice showcases, and pricing. |
| **2** | **Resume Review & ATS Suite** | `/resume`, `/resume/report` | ✅ Live | 4-card Bento Matrix, strikethrough diffs, XYZ formula rewrite acceptance, and ATS parser checks. |
| **3** | **24/7 AI Mock Interviewer** | `/mock-interview` | ✅ Live | Neural AI proctor (AURA), live speech transcription, ASCII architecture whiteboard, and 6-axis radar. |
| **4** | **Mentor Marketplace & WebRTC** | `/mentors` | ✅ Live | Verified bar-raiser directory, pre-flight hardware diagnostics, instant scheduling, and Jitsi launcher. |
| **5** | **Readiness Report Engine** | `/report` | 🟡 Next | Multi-round score aggregation, competency breakdown, and percentile benchmarking against target roles. |
| **6** | **Suggested Jobs Matcher** | `/jobs` | ⚪ Queued | Live tech job scraping, semantic skill matching, and gap mitigation plans. |
| **7** | **Custom JD Analyzer** | `/jd-analyzer` | ⚪ Queued | Custom rubric generator that tailors interview questions to specific corporate job descriptions. |
| **—** | **Institutional Teams OS** | `/teams` | ⚪ Queued | University and bootcamp cohort dashboard for tracking student readiness and placement pipelines. |

---

## 🛠️ Tech Stack ($0 Budget Principle)

Every technology in PrepPilot was deliberately selected to achieve enterprise capability under a **hard $0 budget constraint**:

| Domain | Technology | Free Tier Provision | Rationale |
|---|---|---|---|
| **Frontend** | **Next.js 16** (App Router, Turbopack) | Vercel Free Tier | Fast SSR/SSG, modern React 19 architecture. |
| **Styling** | **Tailwind CSS v4** | Open Source | Custom `@theme` tokens matching Obsidian Gloss Enterprise. |
| **Design Tokens** | **Obsidian Gloss Enterprise** | Custom Design System | Dark surface depths (`#11131b`), Indigo (`#c0c1ff`), Emerald (`#4edea3`). |
| **Backend** | **FastAPI** (Python 3.11+) | Render / Railway Free Tier | Async, high performance, automatic OpenAPI documentation. |
| **Database** | **PostgreSQL (via Supabase)** | 500MB DB, 2 projects free | Relational integrity, row-level security (RLS). |
| **Auth** | **Supabase Auth** | 50,000 MAU free | Email/Password, Google OAuth, JWT verification. |
| **Video Calls** | **Jitsi Meet WebRTC** (`@jitsi/react-sdk`) | Free, no API key or usage cap | Zero cost WebRTC mesh, peer-to-peer encryption, zero setup overhead. |
| **AI (Primary)** | **Google Gemini 1.5 Flash** | 15 RPM, 1M TPM free | Fast multimodal reasoning, JSON structured outputs. |
| **AI (Fallback)** | **Groq API** (Llama 3.3 70B) | Generous free tier | Ultra low-latency conversational backup for speech loops. |
| **Local Mock AI** | Built-in Dev Mock Engine | $0, fully offline | Zero-dependency offline mode for CI and development. |
| **File Storage** | **Supabase Storage** | 1GB free | Resume PDF and avatar uploads. |
| **Email** | **Resend** | 3,000 emails/month free | Booking confirmations and rubric alerts. |

---

## 📁 Repository Structure

```
├── .gitignore                      # Root ignore rules for node, python, secrets, and caches
├── AGENTS.md                       # Single source of truth for multi-agent vibe-coding conventions
├── README.md                       # Project overview, architecture, and quickstart (this file)
├── ROADMAP.md                      # Phased development roadmap and module ownership
│
├── frontend/                       # Next.js 16 App Router application
│   ├── app/
│   │   ├── globals.css             # Tailwind v4 theme variables & obsidian gloss tokens
│   │   ├── layout.tsx              # Root HTML layout with Google Fonts & Material Symbols
│   │   ├── page.tsx                # Stage 1: Master Platform Landing Page
│   │   ├── resume/                 # Stage 2: Resume Review & ATS Diagnostic Suite
│   │   │   ├── page.tsx            # Interactive 4-Pillar Diagnostic Workspace
│   │   │   └── report/page.tsx     # Diagnostic Report Stream
│   │   ├── mock-interview/         # Stage 3: 24/7 AI Adaptive Mock Interviewer
│   │   │   └── page.tsx            # Live Proctor Room, Whiteboard, & Competency Radar
│   │   ├── mentors/                # Stage 4: Calibrated Mentor Marketplace & WebRTC Prep
│   │   │   └── page.tsx            # Mentor Directory, Slot Booking, & Jitsi Launcher
│   │   ├── login/ & signup/        # Candidate & Expert authentication flows
│   │   └── profile/                # Candidate profile & target role settings
│   ├── components/ui/              # Modular UI components (buttons, dialogs, badges, cards)
│   ├── lib/
│   │   ├── api.ts                  # Fetch client with { data, error } normalization
│   │   ├── supabase.ts             # Supabase browser client
│   │   └── types.ts                # TypeScript type definitions
│   ├── package.json
│   └── .env.example                # Frontend environment variable blueprint
│
├── backend/                        # FastAPI Python backend
│   ├── app/
│   │   ├── api/                    # API endpoints by resource (auth, resume, users)
│   │   ├── core/                   # App config, database session, JWT security
│   │   ├── models/                 # SQLAlchemy 2.0 models (User, Profile, Resume)
│   │   ├── schemas/                # Pydantic v2 validation schemas
│   │   ├── services/               # Business logic
│   │   │   ├── ai_service.py       # Gemini Flash + Groq + Mock AI fallback cascade
│   │   │   ├── resume_service.py   # PDF text extraction & parsing
│   │   │   └── resume_review/      # Isolated Resume Microservice package
│   │   └── main.py                 # FastAPI application factory & CORS middleware
│   ├── alembic/                    # Database migrations
│   ├── requirements.txt            # Python dependencies
│   └── .env.example                # Backend environment variable blueprint
│
└── memory-bank/                    # Persistent project memory & architecture context
    ├── activeContext.md            # Current sprint state & next actions
    ├── progress.md                 # Living checklist of working vs pending features
    ├── projectbrief.md             # Core goals, scope, and non-negotiables
    ├── productContext.md           # User personas, problem statement, and experience goals
    ├── systemPatterns.md           # Architecture, data flows, and design patterns
    ├── techContext.md              # Detailed stack limits, credentials, and constraints
    ├── microservicesPlan.md        # Comprehensive 7-service decomposition plan
    └── tasks.md                    # Work breakdown structure
```

---

## 🚀 Quickstart

### Prerequisites

- **Node.js**: `v18.18+` or `v20+`
- **npm**: `v9+`
- **Python**: `v3.11+`
- **Git**

---

### 1. Clone & Branch

```bash
git clone https://github.com/devp-with-V/Capstone.git
cd Capstone
git checkout frontend
```

---

### 2. Backend Setup (FastAPI)

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

Edit `backend/.env` with your credentials (or leave AI keys blank to use the built-in offline mock engine):

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/preppilot
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
GEMINI_API_KEY=your-gemini-api-key       # Optional: Falls back to mock if blank
GROQ_API_KEY=your-groq-api-key           # Optional: Secondary fallback
CORS_ORIGINS=http://localhost:3000
```

Start the backend development server:

```bash
uvicorn app.main:app --reload --port 8000
```

Verify backend health:
- Health check: [http://localhost:8000/api/health](http://localhost:8000/api/health)
- Interactive Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3. Frontend Setup (Next.js 16)

In a separate terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
```

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

To verify a production build:

```bash
npm run build
```

---

## 📋 API Standards

All backend endpoints strictly follow a standardized envelope:

### Success Response (`HTTP 200/201`)
```json
{
  "data": {
    "score": 92,
    "verdict": "Strong Hire",
    "recommendations": [...]
  },
  "error": null
}
```

### Error Response (`HTTP 4xx/5xx`)
```json
{
  "data": null,
  "error": {
    "message": "Invalid PDF formatting: no extractable text found."
  }
}
```

---

## 🤝 Development Workflow & Guidelines

1. **Memory Bank First**: Before starting any task, read [`memory-bank/activeContext.md`](memory-bank/activeContext.md) and [`memory-bank/progress.md`](memory-bank/progress.md).
2. **Post-Session Updates**: At the end of every session, update `activeContext.md` and `progress.md` with what changed and what is next.
3. **Branching Convention**: Use `<module>/<feature-description>`, e.g., `frontend`, `booking/add-slot-locking`, `ai/resume-parser`.
4. **Conventional Commits**: Format commit messages as `feat:`, `fix:`, `chore:`, or `docs:`.
5. **No Secret Leaks**: Never commit real keys. All new environment variables must be documented in both `.env.example` files.
6. **Design Integrity**: All UI components must honor the Obsidian Gloss Enterprise design tokens defined in `frontend/app/globals.css`.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
