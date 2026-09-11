# Active Context — PrepPilot

> Update this file at the end of every work session, however small. This is the file that lets a teammate's
> agent session (or your own, a week later) pick up exactly where things were left off instead of re-deriving
> context from scratch or guessing.

## Current Phase & Branch
- **Active Branch**: `dev` (integration & staging testing branch before `main`)
- **Architecture Branch**: `microservices`
- **Current Milestone**: Microservice Architecture Setup, Shared Core PostgreSQL Schema, and Resume Review Isolation

## Current Focus
Establishing the microservice boundaries for the 7 platform services, shared Postgres database schema (Core + Service Tables), and maintaining clean isolation in `/backend/app/services/<service_name>/`.

## Recent Decisions & Architecture
- **Git Branching Strategy**:
  - `main`: Production release branch.
  - `dev`: Testing & integration branch where all microservices and features are tested before merging into `main`.
  - `microservices` / `<module>/<feature>`: Individual service and feature development branches.
- **Microservices Model**:
  - The platform is structured around 7 distinct microservices:
    1. Mentor Interview Service
    2. AI Mock Interview Service
    3. Resume Review Service (Isolated & Functional)
    4. Overall Report Service (Readiness Engine)
    5. Suggested Jobs Scraper Service
    6. JD Analyzer & Custom Interview Designer
    7. Connected Teams Preparation Service (Universities / Bootcamps)
- **Shared PostgreSQL Schema (Supabase)**:
  - Core tables (`users`, `profiles`, `institutions`, `institution_members`) hold shared identity, target roles, experience tier, and skills to eliminate duplicate user state.
  - Each microservice owns its dedicated tables (`resume_reports`, `ai_interview_*`, `mentor_*`, etc.) referencing `profile_id` / `user_id`.
- **Modular Monorepo Layout**:
  - Allows full domain isolation and container-readiness while enabling $0 free-tier deployment on Render/Railway behind the FastAPI API Gateway.

## Recent Accomplishments
1. Created git branches: `microservices` and `dev`.
2. Created comprehensive architectural blueprints:
   - `memory-bank/microservicesPlan.md`
   - `memory-bank/tasks.md`
3. Refactored and isolated Service 3 (Resume Review) into `/backend/app/services/resume_review/`:
   - Dedicated schemas (`schemas.py`), models (`models.py`), service logic (`service.py`), and router (`api.py`).
   - Extended shared core models in `/backend/app/models/user.py` (`User`, `Profile`, `Institution`, `InstitutionMember`).
   - Backwards-compatible router forwarding in `app/api/resume.py` and `app/services/resume_service.py`.
4. Verification:
   - Isolated resume service health (`/api/resume/health`) returns healthy.
   - Real binary PDF upload and AI analysis return 200 OK.
   - Next.js 16 frontend build compiles cleanly with 0 errors across all 9 static routes.

## Next Steps
1. Advance to Phase 2: Implement Service 2 (`/backend/app/services/ai_interview`) with the adaptive conversational mock interview loop and rubric scoring.
2. Connect live Supabase project credentials (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_JWT_SECRET`) and AI keys (`GEMINI_API_KEY`, `GROQ_API_KEY`) when ready.
