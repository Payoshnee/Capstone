# Active Context — PrepPilot

> Update this file at the end of every work session, however small. This is the file that lets a teammate's
> agent session (or your own, a week later) pick up exactly where things were left off instead of re-deriving
> context from scratch or guessing.

## Current phase
Phase 3 — Booking & Availability foundation (implemented ahead of expert discovery UI)

## Current focus
Production booking/availability flow: authenticated expert slot management, candidate reservations, and booking lifecycle.

## Recent decisions
- Project renamed to PrepPilot. Roadmap re-sequenced to deliver end-to-end resume intelligence as Phase 1 before interview features.
- Stack locked: Next.js + FastAPI (Python), Supabase for DB/Auth/Storage, Gemini (primary) + Groq (fallback)
  for AI, Jitsi for video.
- Expert model confirmed as hybrid: real experts AND an AI interviewer, not either/or.
- Team of 5 — module ownership proposed in `ROADMAP.md`, not yet confirmed with actual names.
- Payments explicitly out of scope for MVP — using a credits system instead of real money.

## Recent accomplishments
- Added production booking and availability vertical slice:
  - PostgreSQL-backed `availability_slots` and `bookings` models plus initial Alembic migration.
  - Approved-expert authorization, timezone-aware slot validation, overlap protection, row-lock-based atomic booking, active-booking uniqueness, cancellation, and slot reopening.
  - Authenticated availability and booking APIs using Supabase JWTs and standard API envelopes.
  - Expert availability manager (`/availability`), candidate booking screen (`/experts/[expertId]/book`), and candidate/expert booking manager (`/bookings`).
  - Wired login/signup screens to Supabase Auth and added backend account bootstrap.
  - Frontend production build and focused ESLint checks pass; backend imports, compiles, exposes all new OpenAPI routes, and reports one Alembic head.
  - Local runtime verified on 2026-10-09: FastAPI health/sample endpoints and the landing, availability, and bookings pages all return HTTP 200 (frontend on port 3001 because port 3000 was occupied).
  - Booking integration verified against PostgreSQL 16: migration, availability creation/listing, overlap rejection, booking, double-booking rejection, cancellation, slot reopening/rebooking, history retention, JWT enforcement (401), and authenticated API access (200) all passed.
  - Local development no longer depends on Supabase: a durable `preppilot-postgres` Docker container runs on port 5433, local email/password auth uses scrypt password hashing plus 12-hour JWTs, and local experts auto-approve through an environment-only flag. Demo expert/candidate accounts and an open slot were created for manual testing.
- Phase 1 End-to-End Candidate flow built and tested:
  - High-converting Landing page (`/`)
  - Login & Signup pages (`/login`, `/signup`)
  - Candidate Profile page (`/profile`)
  - Resume Upload scanner with drag & drop and animated scanner (`/resume`)
  - Resume Diagnostic Report with radial score, 4-pillar breakdown, strengths/weaknesses, actionable suggestions, and mock interview CTA (`/resume/report`)
  - FastAPI backend (`/backend`) with async architecture, standard `{ data, error }` response schema, PDF text extractor (`pypdf`), and Gemini/Groq/mock AI resume analyzer
  - Verification: Frontend Next.js build passes with 0 errors across all 9 routes; Backend API endpoints (`/api/health`, `/api/resume/sample`, `/api/resume/analyze`, `/api/auth/me`, `/api/users/profile`) tested and passing with actual PDF payloads.

## Next steps
1. Add expert discovery/profile UI so candidates can reach `/experts/[expertId]/book` naturally and admins can approve expert applications.
2. Restore Supabase as an optional production authentication/storage provider when deployment work begins; local development currently uses PostgreSQL auth.
3. Add Resend booking confirmation/reminder notifications.
4. Advance the AI Mock Interview module.

## Open questions (resolve before Phase 1 ends)
- Exact scoring rubric for feedback (what does a "technical_score" of 7/10 mean, concretely?) — needs a
  written rubric so AI-generated and expert-authored feedback stay comparable.
- Credits system mechanics: do candidates get a fixed number per week, or earn them somehow?
