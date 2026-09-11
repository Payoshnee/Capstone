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
  - Stage 3: AI Adaptive Mock Interviewer (`24_7_ai_adaptive_mock_interviewer` -> `app/mock-interview/`) [NEXT]
  - Stage 4: Mentor Marketplace (`human_mentor_marketplace_webrtc_prep` -> `app/mentors/`)
  - Stage 5: Holistic Readiness Report (`holistic_candidate_readiness_report` -> `app/report/`)
  - Stage 6: Suggested Jobs Matcher (`suggested_jobs_scraper_matcher` -> `app/jobs/`)
  - Stage 7: JD Analyzer & Custom Interview Designer (`jd_analyzer_custom_interview_designer` -> `app/jd-analyzer/`)
  - Stage 8: Connected Teams Enterprise OS (`connected_teams_institutional_enterprise_os` -> `app/teams/`)

## Recent Accomplishments
1. Switched to dedicated branch `frontend`.
2. Mapped all 10 stitch directories to Next.js App Router routes.
3. Added Obsidian Gloss Enterprise tokens in `frontend/app/globals.css` and font loaders in `frontend/app/layout.tsx`.
4. Stage 1: Converted `ai_mentor_interview_prep_platform` to `frontend/app/page.tsx` with interactive tab switcher, 7 microservices cards, pricing grid, and footer.
5. Stage 2: Converted `resume_review_ats_diagnostic_suite` to `frontend/app/resume/page.tsx` and `frontend/app/resume/report/page.tsx`:
   - 4-card Bento Matrix: ATS Compatibility (92/100, Greenhouse/Lever/Ashby/Workday badges), Quantified Impact (91/100), Brevity & Density (84/100), Hard Skill Match (94%).
   - Left Panel: Parsed resume stream with interactive flag highlights, before/after strikethrough previews, technical taxonomy chips.
   - Right Panel: 4-Pillar Diagnostic Engine with interactive tabs, diff acceptance actions (live state sync with preview pane), word length histogram SVG, verb velocity bars, keyword matrix table with quick inject.
   - Modals: "Re-scan with Target JD" drag-and-drop PDF dropzone and "Raw Semantic Differential" comparison modal.
   - Sticky Action Deck: Download ATS-Guaranteed PDF with animated compiling state.
6. Verification: `npm run build` compiled cleanly with 0 errors across all 9 routes.
7. Committed Stage 2 changes: `feat(frontend): implement resume review ats diagnostic suite (stage 2)`.

## Next Steps
1. Await user verification for Stage 2.
2. Proceed to Stage 3: Convert `24_7_ai_adaptive_mock_interviewer` to `frontend/app/mock-interview/page.tsx`.
