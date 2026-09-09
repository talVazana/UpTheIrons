# Blacksmith Knight — Forging Heaven

A personal, amateur-friendly digital home and technical knowledge vault for blacksmithing, bladesmithing, forging, metallurgy, heat treatment, workshop tools, and craft techniques.

---

## 1. Project Purpose

Provide amateur and hobbyist makers with a practical reference library and curated workshop companion:
- **Atmosphere:** Dark industrial forge aesthetic (`#121212` background, `#FF5722` forge ember accent).
- **Core Experience:** Dynamic Bento feed, polymorphic card system (videos, guides, materials, tools, projects, rules).
- **Controlled Ingestion:** Ingests strictly from user-managed YouTube channels and approved RSS/product feeds. No autonomous crawler.
- **Enrichment:** Optional AI enrichment layer for categorization and summaries; core system remains fully functional without AI.

---

## 2. Architecture Overview

```text
┌─────────────────────────────────────────────────────────┐
│                     LOCAL WORKSPACE                     │
│                                                         │
│  Frontend (Next.js App Router + TypeScript + Tailwind)  │
│       │                                                 │
│       ▼                                                 │
│  Backend (FastAPI + Pydantic + Uvicorn)                 │
│       │                                                 │
│       ▼                                                 │
│  Firebase Local Emulator Suite (Firestore, Auth)        │
└─────────────────────────────────────────────────────────┘
```

- **`frontend/`**: Next.js App Router, React, Tailwind CSS, Framer Motion.
- **`backend/`**: FastAPI REST API, background ingestion workers, data normalization.
- **`config/`**: Configuration templates, source manifests, local settings.
- **`docs/`**: Master Specification, Development Program & Work Log, walkthroughs.
- **`tests/`**: Unit, integration, and contract tests for backend and frontend.
- **`scripts/`**: Automation and local operational tooling.

---

## 3. Development Guidelines

1. **Local First:** All services run locally via emulators before cloud deployment.
2. **Small Verified Blocks:** One small, tested block at a time. No unverified feature stacking.
3. **Deterministic First:** Normalization, deduplication, and storage rely on deterministic code, not AI.
4. **Zero Secrets in Git:** Never commit `.env` files or API keys. Keep secrets in local `.env` files matching `.gitignore`.

---

## 4. Local Startup (Target Workflow)

### Prerequisites
- Node.js (v20+) & npm
- Python (3.11+) & virtual environment
- Firebase CLI (`firebase-tools`) & Java runtime (for Firestore emulator)

### Frontend
```bash
cd frontend
npm install
npm run dev
# Target: http://localhost:3000
```

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Target: http://localhost:8000
```

### Firebase Local Emulators
```bash
firebase emulators:start --only firestore
```

---

## 5. Environment Variables

Store secrets locally in uncommitted `.env` files:

| Variable | Scope | Description |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Frontend | Backend API base URL (`http://localhost:8000`) |
| `FIREBASE_PROJECT_ID` | Shared | Firebase project / emulator target ID |
| `YOUTUBE_API_KEY` | Backend | YouTube Data API v3 key |
| `GEMINI_API_KEY` | Backend | Optional AI enrichment key |

See full specifications in [`docs/`](./docs/).
