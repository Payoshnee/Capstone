# Progress — PrepPilot

> Keep this a living checklist, not a diary. Check items off as they're genuinely done (built + working, not
> just started). Add new items if scope shifts.

## What works
- **Frontend Scaffolding & Design System**: Next.js 16 + TypeScript + Tailwind CSS v4 + Obsidian Gloss Enterprise design tokens (`#11131b` dark surfaces, electric indigo `#c0c1ff`/`#8083ff`, violet, emerald `#4edea3`, Plus Jakarta Sans, Inter, JetBrains Mono, Google Material Symbols). Production build verified with 0 errors.
- **Master Platform Ecosystem Landing Page** (`/`): High-converting hero with atmospheric glows, interactive split hero demo (target JD blueprint vs live session switcher between 24/7 AI Interviewer with live audio waveform & rubric scores, and Mentor Room), 7-microservice expansive showcase cards (Resume ATS, AI Mock, Mentor Marketplace, Readiness Radar, Jobs Scraper, Custom JD Designer, Institutional Teams OS), 4-step evidence loop, testimonials, transparent pricing, and enterprise footer.
- **Auth Flow** (`/login`, `/signup`): Authentication pages with candidate/expert role selection and guest/demo flow.
- **Candidate Profile** (`/profile`): Personal info, target role, experience level, target companies, key skill chips, recent reports sidebar, interview cards.
- **Resume Review & ATS Diagnostic Suite** (`/resume`, `/resume/report`): Complete Obsidian Gloss Enterprise conversion of `resume_review_ats_diagnostic_suite`. 4-card Bento Matrix (ATS Compatibility radial score with Greenhouse/Lever/Ashby/Workday badges, Quantified Impact, Brevity & Density, Hard Skill Match), parsed resume heatmaps with inline before/after line-through diffs and skill cloud, 4-pillar diagnostic engine (Quantified Impact XYZ formula, word length histogram SVG, verb velocity bars, keyword taxonomy table with quick inject), live state synchronization between diff acceptance and preview pane, Re-scan with Target JD dropzone modal, and PDF export.
- **24/7 AI Adaptive Mock Interviewer** (`/mock-interview`): Complete Obsidian Gloss Enterprise conversion of `24_7_ai_adaptive_mock_interviewer`. Live proctor session bar with running timer, dual-core stream grid (Neural AI Proctor with animated equalizer visualizer bars + challenge injection indicator, Candidate camera/mic stream controls), live transcript stream with real-time speech telemetry (WPM, filler word count, audio input buffer indicator), System Architecture Whiteboard modal with ASCII diagram editor and broadcast action, live 3-pillar evaluation telemetry (System Depth, Structural Clarity, STAR Execution), 6-axis SVG competency radar chart, and Finish Round evaluation summary modal.
- **Human Mentor Marketplace & WebRTC Prep** (`/mentors`): Complete Obsidian Gloss Enterprise conversion of `human_mentor_marketplace_webrtc_prep`. Upcoming Jitsi session banner (Marcus Vance, Google Cloud Infra L7, pre-flight hardware diagnostics, attached blueprint selector), 3 evaluation assurance pillars (60-Min SLA, Calibration Matrix, Private Replay), fast multi-tag filtering (FAANG+ companies, Distributed Systems / AI / Leadership domains), sort dropdown, 4 calibrated mentor cards with dynamic slot selection, interactive Jitsi WebRTC pre-flight connection modal, dynamic booking & schedule confirmation modal, and recent calibrated rubric showcase (#EXP-89021-CALIBRATED) with simulated PDF export.
- **Backend Core**: FastAPI layered architecture (`api/`, `services/`, `models/`, `schemas/`, `core/`), standard `{ data, error }` response schema, CORS middleware, health check endpoint.
- **Resume Analysis Engine**: PDF extraction via `pypdf`, Gemini Flash integration + Groq fallback + dev mock engine for offline/free-tier resiliency, tested with real PDF payloads.
- **Documentation & Memory Bank**: PrepPilot branding across all documentation, `/memory-bank` persistent context created, `ROADMAP.md` re-sequenced, `implementation_plan.md` created.

## What's left (mirrors the MVP scope in `projectbrief.md`)

### Phase 1: Polish & Integration
- [x] Landing page (hero, features, how-it-works, FAQ)
- [x] Login & Signup pages
- [x] Candidate profile page
- [x] Resume upload page with drag-and-drop
- [x] Backend: Resume PDF extraction
- [x] Backend: AI resume analysis (Gemini/Groq/mock)
- [x] Resume diagnostic report page
- [x] Backend & frontend scaffolding
- [ ] Connect Supabase Auth live project credentials
- [ ] Connect Postgres database via Alembic migration

### Auth & users
- [ ] Supabase Auth wired into Next.js (signup/login/logout)
- [ ] Role selection (candidate/expert) on signup
- [ ] Admin approval flow for expert applications

### Expert discovery
- [ ] Expert profile creation form
- [ ] Expert browse/filter page (by domain)

### Booking & availability
- [ ] Expert availability calendar (set weekly slots)
- [ ] Candidate booking flow (pick slot, confirm)
- [ ] Booking confirmation email

### Video sessions
- [ ] Jitsi room creation per booking
- [ ] Join-call UI for both candidate and expert

### AI interviewer
- [ ] Domain/role selection UI for "Practice now"
- [ ] Resume upload + Gemini-based parsing
- [ ] Adaptive question/follow-up loop
- [ ] AI-generated feedback report

### Feedback & dashboards
- [ ] Structured feedback form for experts
- [ ] Feedback report view (shared component for AI + expert feedback)
- [ ] Candidate dashboard (session history + trend)
- [ ] Expert dashboard (bookings + ratings)

### Notifications
- [ ] Email on booking confirmed
- [ ] Email/in-app reminder before session
- [ ] Email/in-app alert when feedback is ready

## Known issues
- None yet — nothing built.
