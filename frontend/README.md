# PrepPilot — Frontend App

The frontend client for **PrepPilot**, a hybrid AI + human-expert mock interview platform. Built with **Next.js 16 (App Router)**, **Tailwind CSS v4**, **TypeScript**, and the **Obsidian Gloss Enterprise** design system.

---

## Tech Stack

- **Framework**: Next.js 16 (App Router, Turbopack)
- **Styling**: Tailwind CSS v4 (configured via `@theme` in `app/globals.css`)
- **Design Tokens**: Obsidian Gloss Enterprise (`#11131b` dark surfaces, electric indigo `#c0c1ff`/`#8083ff`, violet `#d0bcff`, emerald `#4edea3`)
- **Typography**: Plus Jakarta Sans, Inter, JetBrains Mono
- **Icons**: Google Material Symbols Outlined, Lucide React
- **Video Calls**: Jitsi Meet WebRTC (`@jitsi/react-sdk`)
- **Auth & State**: Supabase Auth client, React Context / Hooks

---

## App Routes

| Route | Description |
|---|---|
| `/` | Master Platform Hub & Landing Page |
| `/resume` | ATS Diagnostic Suite & 4-Pillar Resume Evaluation |
| `/resume/report` | Resume Diagnostic Report Stream |
| `/mock-interview` | 24/7 AI Adaptive Mock Interviewer (AURA Proctor) |
| `/mentors` | Human Mentor Marketplace & WebRTC Prep |
| `/report` | Holistic Candidate Readiness Report & Competency Radar *(in progress)* |
| `/jobs` | Suggested Jobs Scraper & Matcher *(in progress)* |
| `/jd-analyzer` | Custom JD Analyzer & Interview Designer *(in progress)* |
| `/teams` | Institutional Teams & Enterprise OS *(in progress)* |
| `/profile` | Candidate Profile & Target Role Configuration |
| `/login` / `/signup` | Authentication & Role Selection |

---

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Configuration

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Configure your variables:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000).

### 4. Production Build

```bash
npm run build
npm run start
```

---

For full platform architecture and backend setup, see the root [`README.md`](../README.md).
