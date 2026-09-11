# Project Brief — PrepPilot

## One-line pitch
An all-in-one AI & Human Expert interview preparation and placement intelligence ecosystem where candidates, mentors, and institutions prepare for placements with microservice-powered diagnostic and practice tools.

## Problem statement
Students preparing for placements/internships struggle to get realistic, targeted interview practice: real mentors are hard to schedule, generic practice question sites give no live adaptive feedback, resumes fail automated ATS filters, and universities lack visibility into student cohort readiness. PrepPilot solves this by combining 7 specialized microservices into a unified platform.

## Target users
- **Candidate** — student or job-seeker preparing for technical, system design, and behavioral interviews.
- **Mentor / Expert** — senior student, alumnus, or industry professional offering mock interviews and structured reviews.
- **Institution / University Coordinator** — university placement departments, bootcamp administrators, and cohort coordinators tracking student batch readiness.
- **Admin** — platform administrator vetting mentors, monitoring system health, and resolving issues.

## The 7 Microservices Scope
1. **Mentor Interview Service**: Mentor discovery, calendar scheduling, embedded Jitsi video calls, and structured mentor feedback.
2. **AI Mock Interview Service**: 24/7 adaptive mock interview loop (voice/text) with dynamic follow-up questioning and real-time rubric scoring.
3. **Resume Review Service** *(Active & Isolated)*: Deep ATS diagnostic scanning, 4-pillar evaluation, actionable before/after bullet revisions, and skill extraction.
4. **Overall Report Service**: Holistic readiness intelligence engine computing the **Readiness Index (0-100)**, competency radar, and longitudinal progress trends.
5. **Suggested Jobs Scraper Service**: Tech job board aggregator matching candidate profile skills with live market openings and highlighting prerequisite gaps.
6. **JD Analyzer & Custom Interview Designer**: Job Description parser generating hyper-targeted interview question sets tailored for specific company postings.
7. **Connected Teams Preparation Service**: Institutional B2B portal for universities and bootcamps to manage cohorts, track student batch readiness, and monitor placement statistics.

## Supporting Infrastructure
- **API Gateway & Auth Router**: Supabase JWT validation, route forwarding, rate limiting, and unified error handling.
- **Shared PostgreSQL Database (Supabase)**: Core tables (`users`, `profiles`, `institutions`) with isolated tables per microservice.
- **Notification Worker**: Transactional email dispatch via Resend (booking confirmations, reminders, report alerts).

## Explicitly out of scope for MVP
- Real currency payments (credits system used for student capstone).
- Native mobile app (web-responsive Next.js 16 client).
- Multi-language translation support.

## Success criteria
- Candidate can complete an end-to-end preparation journey: upload resume → view ATS diagnostic → analyze target JD → launch tailored AI mock interview → book human mentor → view unified readiness report.
- Placement coordinators can onboard a cohort, view student readiness indices, and track mock interview completion rates.
- All services run within $0 free-tier constraints (Supabase, Gemini Flash, Groq, Jitsi, Vercel, Render/Railway).
