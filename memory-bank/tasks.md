# Tasks Tracker — PrepPilot

> **Living Document**: This file tracks the active tasks, completed milestones, and upcoming deliverables across all microservices and infrastructure components in PrepPilot. Update this file at the start and end of every work session.

---

## Active Sprint & Branch
- **Active Branch**: `architecture/microservice-integration`
- **Current Objective**: Isolate the existing Resume Review service, establish the shared PostgreSQL database structure (Core + Service Tables), and prepare service interfaces for parallel microservice development.

---

## Phase 1: Foundation & Resume Review Service (COMPLETED ✅)
- [x] Brand & documentation rename (PrepArena → PrepPilot)
- [x] Initial `/memory-bank` context files created
- [x] Next.js 16 frontend scaffolding with TypeScript, Tailwind CSS, and shadcn/ui
- [x] Landing page (`/`) with Hero, Feature Pillars, Workflow timeline, Resume Preview, and FAQ
- [x] Auth pages (`/login`, `/signup`) with Candidate & Mentor role selection
- [x] Candidate Profile page (`/profile`) with target roles, experience tier, and key skills
- [x] Resume upload page (`/resume`) with drag-and-drop and 4-step animated scanner
- [x] Resume diagnostic report page (`/resume/report`) with radial gauge, 4-pillar breakdown, strengths/weaknesses, and before/after bullet revisions
- [x] FastAPI backend scaffolding with standard `{ data, error }` API response envelope
- [x] Resume PDF text extraction via `pypdf`
- [x] AI resume analysis engine (Gemini Flash primary, Groq fallback, offline mock fallback)
- [x] Integration verification: Frontend builds with 0 errors across all 9 static routes; Backend endpoints tested with PDF payloads

---

## Phase 2: Microservice Isolation & Database Architecture (UPCOMING / PENDING APPROVAL)

### Git & Configuration
- [ ] Create and checkout git branch `architecture/microservice-integration`
- [ ] Update `systemPatterns.md` and `ROADMAP.md` (root & `/memory-bank`) with the 7-microservice architecture

### Shared Core Database (PostgreSQL / Supabase)
- [ ] Define shared core models in `/backend/app/models/common.py`:
  - `User` (`id`, `email`, `role`, `created_at`)
  - `Profile` (`id`, `user_id`, `full_name`, `target_role`, `experience_level`, `skills`, `bio`)
  - `Institution` (`id`, `name`, `type`, `admin_user_id`)
  - `InstitutionMember` (`id`, `institution_id`, `user_id`, `batch_name`, `status`)

### Service 3: Resume Review Isolation (Current Working Codebase)
- [ ] Reorganize current resume service into `/backend/app/services/resume_review/`:
  - `schemas.py`: `ResumeAnalysisReport`, `ResumeScoreCategory`, `ResumeImprovement`
  - `models.py`: `ResumeReport` (linked to `profiles.id`)
  - `service.py`: `extract_text_from_pdf`, `analyze_resume`
  - `api.py`: `POST /analyze`, `GET /reports/{id}`, `GET /sample`
- [ ] Verify existing frontend `/resume` and `/resume/report` remain fully functional through gateway

---

## Phase 3: AI Mock Interview Service (Service 2)
- [ ] Directory: `/backend/app/services/ai_interview/`
- [ ] Database tables: `ai_interview_sessions`, `ai_interview_turns`
- [ ] Adaptive question prompt engineering based on `profiles.skills` and `resume_reports.recommended_interview_topics`
- [ ] Conversational turn API (`POST /api/ai-interview/turn`): evaluates answer, updates rubric, generates dynamic follow-up
- [ ] Interview report generator with technical depth, communication, and problem-solving scoring
- [ ] Frontend: Domain/Role selection UI (`/interview/new`)
- [ ] Frontend: Live conversational interview screen with speech-to-text / text response modes
- [ ] Frontend: Post-interview session feedback report view

---

## Phase 4: Mentor Interview Service (Service 1)
- [ ] Directory: `/backend/app/services/mentor_interview/`
- [ ] Database tables: `mentor_profiles`, `mentor_availability`, `mentor_bookings`, `mentor_feedbacks`
- [ ] Mentor application and admin approval workflow
- [ ] Weekly slot availability calendar management
- [ ] Candidate booking flow with slot locking
- [ ] Jitsi Meet video room generation (`preppilot-mentor-<booking_id>`)
- [ ] Frontend: Mentor discovery & filter page by domain (`/mentors`)
- [ ] Frontend: Mentor public profile & slot booking modal (`/mentors/[id]`)
- [ ] Frontend: Embedded Jitsi video call room (`/room/[booking_id]`)
- [ ] Frontend: Structured mentor evaluation submission form

---

## Phase 5: JD Analyzer & Custom Interview Designer (Service 6)
- [ ] Directory: `/backend/app/services/jd_analyzer/`
- [ ] Database tables: `job_descriptions`, `custom_interview_blueprints`
- [ ] JD text parser: extracts required skills, seniority, and technical stacks
- [ ] Gap analysis against candidate `profiles.skills` and uploaded resume
- [ ] Dynamic interview blueprint generator (custom tailored question set targeting the JD)
- [ ] Direct launch bridge into Service 2 (AI Mock Interview) using the custom blueprint
- [ ] Frontend: JD upload / paste interface (`/jd/analyze`)
- [ ] Frontend: Gap analysis scorecard & interview plan preview

---

## Phase 6: Suggested Jobs Scraper Service (Service 5)
- [ ] Directory: `/backend/app/services/job_scraper/`
- [ ] Database tables: `scraped_jobs`, `candidate_job_matches`
- [ ] Job board scraping worker with skill keyword extraction
- [ ] Matching algorithm: compares job requirements with candidate `profiles.skills`
- [ ] Match percentage scoring (0-100%) and missing prerequisite skill tags
- [ ] Frontend: Job board view with match percentage chips (`/jobs`)
- [ ] Frontend: Job detail card with "Practice for this Job" 1-click button (triggers Service 6)

---

## Phase 7: Overall Report & Readiness Engine (Service 4)
- [ ] Directory: `/backend/app/services/overall_report/`
- [ ] Database tables: `candidate_readiness_reports`, `competency_history`
- [ ] Cross-service aggregation: weights Resume ATS score (25%) + AI Mock Interviews (40%) + Mentor Reviews (35%)
- [ ] Multi-axis Competency Radar calculation (DSA, System Design, Communication, Problem Solving, Tooling)
- [ ] Longitudinal progress tracking across mock sessions
- [ ] Frontend: Candidate comprehensive readiness dashboard (`/dashboard`)
- [ ] Frontend: Interactive radar chart and historical growth trend visualization

---

## Phase 8: Connected Teams Preparation Service (Service 7)
- [ ] Directory: `/backend/app/services/teams_prep/`
- [ ] Database tables: `team_cohorts`, `cohort_members`, `cohort_analytics`
- [ ] Institutional onboarding (Universities, Bootcamps, Corporate Training)
- [ ] Batch & cohort management by placement coordinators
- [ ] Aggregate cohort analytics: average readiness, completion velocity, top cohort-wide skill deficiencies
- [ ] Frontend: Institution Admin Portal (`/teams/dashboard`)
- [ ] Frontend: Batch management and student readiness roster view
- [ ] Frontend: Cohort exportable placement readiness reports (PDF/CSV)

---

## Supporting Infrastructure & Cross-Cutting Concerns
- [ ] **API Gateway & Auth Router**: Unified route dispatcher and Supabase JWT verification
- [ ] **Notification Worker**: Transactional email dispatch via Resend (booking alerts, report ready reminders)
- [ ] **Async Worker Queue**: Non-blocking background execution for job scrapers and batch cohort analytics
