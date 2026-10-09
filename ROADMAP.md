# Roadmap — PrepPilot

## Branching & Release Strategy
- **`main`**: Production-ready, stable releases.
- **`dev`**: Active integration & testing branch. All features and microservices are merged and tested here before release to `main`.
- **`microservices` / `<module>/<feature>`**: Feature and architectural development branches (e.g., `microservices`, `interview/ai-loop`, `jobs/scraper`).

---

## Microservice Architecture Phased Roadmap

### Phase 1 — Foundation & Resume Review Service (Service 3) — COMPLETED ✅
- Landing page, auth flow, candidate profile.
- Resume upload, PDF extraction, 4-pillar ATS scoring, actionable diff revisions, report generation.
- Isolated service directory: `/backend/app/services/resume_review/`.
- **Done when:** Candidate can visit landing page, sign up, upload resume, and view full diagnostic report.

### Phase 2 — AI Mock Interview Service (Service 2)
- Conversational adaptive mock interview engine (voice and text response modes).
- Dynamic follow-up questioning driven by candidate profile and resume gap analysis.
- Multi-pillar real-time rubric scoring and post-session feedback report.
- Isolated service directory: `/backend/app/services/ai_interview/`.
- **Done when:** Candidate can launch an instant AI mock interview, answer adaptive questions, and receive a granular feedback report.

### Phase 3 — Mentor Interview Service (Service 1)
- Industry mentor application, credential vetting, and admin approval.
- Mentor availability calendar, slot booking with slot-locking.
- Embedded Jitsi Meet video call room generation (`preppilot-mentor-<booking_id>`).
- Structured mentor evaluation submission form.
- Isolated service directory: `/backend/app/services/mentor_interview/`.
- **Done when:** Candidate can browse approved mentors, book a time slot, participate in a video interview, and receive mentor feedback.

### Phase 4 — JD Analyzer & Custom Interview Designer (Service 6)
- Raw Job Description (JD) text parser extracting core competencies and tech stack markers.
- Candidate profile and resume gap benchmarking against the specific JD.
- Automated generation of tailored interview question blueprints targeting the job.
- 1-click bridge launching custom question sets directly in the AI Mock Interviewer.
- Isolated service directory: `/backend/app/services/jd_analyzer/`.
- **Done when:** Candidate can paste a job posting, see matching score, and launch a tailored mock interview targeting that specific role.

### Phase 5 — Suggested Jobs Scraper Service (Service 5)
- Automated tech job board scraper extracting live job openings.
- Profile-to-job matching algorithm computing match percentages based on candidate skills.
- Missing skill gap recommendations with 1-click prep suggestions.
- Isolated service directory: `/backend/app/services/job_scraper/`.
- **Done when:** Candidate can browse recommended jobs matched to their skills with actionable gap analysis.

### Phase 6 — Overall Report & Readiness Engine (Service 4)
- Aggregation of Resume ATS scores + AI Mock interview performance + Mentor feedback.
- Computation of the **PrepPilot Readiness Index (0-100)**.
- Multi-axis Competency Radar (DSA, System Design, Communication, Problem Solving, Tooling).
- Longitudinal progress tracking across practice history.
- Isolated service directory: `/backend/app/services/overall_report/`.
- **Done when:** Candidate dashboard displays consolidated readiness index, competency radar, and historical progress trends.

### Phase 7 — Connected Teams Preparation Service (Service 7)
- Institutional B2B portal for universities, placement cells, and bootcamps.
- Student cohort management (e.g., "Class of 2026", "Batch 14").
- Placement coordinator dashboard tracking student readiness scores and mock interview completion rates.
- Aggregate cohort skill gap analytics and institutional placement reports.
- Isolated service directory: `/backend/app/services/teams_prep/`.
- **Done when:** Placement coordinators can onboard batches of students, track aggregate readiness, and download placement analytics.

### Buffer & Demo Preparation
- End-to-end regression testing across all 7 services.
- Final deployment verification (Vercel frontend + Render/Railway backend).
- Demo presentation script preparation.
