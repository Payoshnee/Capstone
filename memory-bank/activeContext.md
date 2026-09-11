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
  - Stage 2: Resume Review & ATS Diagnostic Suite (`resume_review_ats_diagnostic_suite` -> `app/resume/`) [NEXT]
  - Stage 3: AI Adaptive Mock Interviewer (`24_7_ai_adaptive_mock_interviewer` -> `app/mock-interview/`)
  - Stage 4: Mentor Marketplace (`human_mentor_marketplace_webrtc_prep` -> `app/mentors/`)
  - Stage 5: Holistic Readiness Report (`holistic_candidate_readiness_report` -> `app/report/`)
  - Stage 6: Suggested Jobs Matcher (`suggested_jobs_scraper_matcher` -> `app/jobs/`)
  - Stage 7: JD Analyzer & Custom Interview Designer (`jd_analyzer_custom_interview_designer` -> `app/jd-analyzer/`)
  - Stage 8: Connected Teams Enterprise OS (`connected_teams_institutional_enterprise_os` -> `app/teams/`)

## Recent Accomplishments
1. Switched to dedicated branch `frontend`.
2. Mapped all 10 stitch directories to Next.js App Router routes.
3. Added Obsidian Gloss Enterprise tokens in `frontend/app/globals.css` and font loaders in `frontend/app/layout.tsx`.
4. Converted `ai_mentor_interview_prep_platform` to `frontend/app/page.tsx`:
   - Interactive tab switcher (24/7 AI Interviewer vs Mentor Room with live simulated waveform and rubric scores).
   - Dynamic 7-service showcase with interactive cards, radar chart SVG, before/after diff highlights, and live postings.
   - Pricing grid, evidence loop pipeline, and verified testimonials.
5. Verification: `npm run build` compiled cleanly with 0 errors across all routes.
6. Committed Stage 1 changes: `feat(frontend): implement obsidian gloss theme and platform landing page (stage 1)`.

## Next Steps
1. Await user verification for Stage 1.
2. Proceed to Stage 2: Convert `resume_review_ats_diagnostic_suite` to `frontend/app/resume/page.tsx` and `frontend/app/resume/report/page.tsx`.
