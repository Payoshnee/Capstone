# Active Context — PrepPilot

> Update this file at the end of every work session, however small. This is the file that lets a teammate's
> agent session (or your own, a week later) pick up exactly where things were left off instead of re-deriving
> context from scratch or guessing.

## Current Phase & Branch
- **Active Branch**: `frontend` (staged UI migration from stitch designs)
- **Staging / Integration Branch**: `dev`
- **Architecture Branch**: `microservices`
- **Current Milestone**: Staged migration of stitch design templates to Next.js App Router using Obsidian Gloss Enterprise design tokens.

## Current Focus
Converting imported stitch frontend designs from `stitch_ai_interview_prep_platform/` in sequential stages into the Next.js App Router, using PrepPilot branding and Obsidian Gloss Enterprise theme tokens.

## Recent Decisions & Architecture
- **Branding**: Replaced all occurrences of "ExpertHire" with **PrepPilot** ("PrepPilot — AI & Mentor Career Matrix").
- **Design System**: Configured Tailwind CSS v4 `@theme` in `app/globals.css` with exact tokens from `obsidian_gloss_enterprise/DESIGN.md`:
  - Obsidian foundations: `#11131b`, `#0c0e16`, `#191b24`, `#1d1f28`, `#282a32`, `#33343d`
  - Electric Indigo (`#c0c1ff`, `#8083ff`) and Violet (`#d0bcff`, `#571bc1`)
  - Status Emerald (`#4edea3`), Error Crimson (`#ffb4ab`), Slate outlines (`#908fa0`)
  - Fonts: Plus Jakarta Sans, Inter, JetBrains Mono, Google Material Symbols Outlined
- **Staging Rollout Plan**:
  - Stage 1: Design tokens + Platform Hub (`ai_mentor_interview_prep_platform` -> `app/page.tsx`) [COMPLETE]
  - Stage 2: Resume Review & ATS Diagnostic Suite (`resume_review_ats_diagnostic_suite` -> `app/resume/`) [COMPLETE]
  - Stage 3: AI Adaptive Mock Interviewer (`24_7_ai_adaptive_mock_interviewer` -> `app/mock-interview/`) [COMPLETE]
  - Stage 4: Mentor Marketplace (`human_mentor_marketplace_webrtc_prep` -> `app/mentors/`) [COMPLETE]
  - Stage 5: Holistic Readiness Report (`holistic_candidate_readiness_report` -> `app/report/`) [NEXT]
  - Stage 6: Suggested Jobs Matcher (`suggested_jobs_scraper_matcher` -> `app/jobs/`)
  - Stage 7: JD Analyzer & Custom Interview Designer (`jd_analyzer_custom_interview_designer` -> `app/jd-analyzer/`)
  - Stage 8: Connected Teams Enterprise OS (`connected_teams_institutional_enterprise_os` -> `app/teams/`)

## Recent Accomplishments
1. Switched to dedicated branch `frontend`.
2. Mapped all 10 stitch directories to Next.js App Router routes.
3. Added Obsidian Gloss Enterprise tokens in `frontend/app/globals.css` and font loaders in `frontend/app/layout.tsx`.
4. Stage 1: Converted `ai_mentor_interview_prep_platform` to `frontend/app/page.tsx` with interactive tab switcher, 7 microservices cards, pricing grid, and footer.
5. Stage 2: Converted `resume_review_ats_diagnostic_suite` to `frontend/app/resume/page.tsx` and `frontend/app/resume/report/page.tsx`.
6. Stage 3: Converted `24_7_ai_adaptive_mock_interviewer` to `frontend/app/mock-interview/page.tsx`.
7. Stage 4: Converted `human_mentor_marketplace_webrtc_prep` to `frontend/app/mentors/page.tsx`:
   - Live Upcoming Callout Card: Warm call in 42 mins, JITSI-E2EE-8492 session with Marcus Vance (L7 Staff Eng, Google Cloud Infra), hardware diagnostics (4K Brio, Shure MV7, AES-256 E2EE, <22ms latency), attached blueprint selector.
   - 3 Feedback Assurance Cards: Turnaround SLA (60-Min Written Rubric), Calibration Matrix (Staff & Principal Calibrated), Private Replay Archive (Dual-Stream Recording).
   - Search & Filters Toolbar: Dynamic query search across names/domains/frameworks, company filter chips (All FAANG+, Google, Stripe, Meta, OpenAI, Netflix, Apple), track filter chips (Distributed Systems, AI & LLM Systems, Engineering Leadership), and sorting criteria.
   - Calibrated Enterprise Mentors Grid: Alex Rivera, Dr. Elena Rostova, Kenji Takahashi, Sarah Jenkins with live ratings, hourly rates, verified badges, offer ratios, comp increase sparklines, and interactive slot selection.
   - Interactive Jitsi WebRTC Preflight Modal: Signaling, bar-raiser token validation, E2EE key provisioning (SHA-256), whiteboard sync, and direct transition to the mock interview room.
   - Interactive Mentor Booking Modal: Slot confirmation, interview track selection, resume/blueprint attachment, instant booking confirmation with dynamic room identifier.
   - Recent Mock Interview Rubric Report (#EXP-89021-CALIBRATED): Architecture, Concurrency, and Executive Presence breakdown with simulated rubric PDF download.
8. Verification: `npm run build` compiled cleanly with 0 errors across all 11 routes.
9. Committed Stage 4: `feat(frontend): implement human mentor marketplace webrtc prep (stage 4)`.

## Next Steps
1. Present Stage 4 to user for review and verification.
2. On confirmation, proceed to Stage 5: Convert `holistic_candidate_readiness_report` to `frontend/app/report/page.tsx`.
