# Walkthrough — Project Setup

Work log and verification for **Blacksmith Knight — Forging Heaven** inside `C:\Doron\UpTheIrons`.

## Step 02.02 — Folder Structure

Created root and sub-package directories with `.gitkeep` files:

```text
C:\Doron\UpTheIrons\
├── .github/
│   └── workflows/
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── models/
│       └── repositories/
├── config/
├── docs/                 (existing)
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   └── styles/
├── scripts/
└── tests/
    ├── backend/
    └── frontend/
```

### Verification
- Ran `Get-ChildItem -Directory -Recurse`: 20 directories verified.
- Pushed to remote Git.

---

## Step 02.06 — Root `.gitignore`

Created [`.gitignore`](file:///C:/Doron/UpTheIrons/.gitignore) covering:
- Node / Next.js (`node_modules/`, `.next/`, `out/`, `build/`, `dist/`, logs)
- Python (`.venv/`, `__pycache__/`, `*.pyc`, test/lint caches)
- Environment variables and secrets (`.env*`, `*.pem`)
- Firebase emulator logs and data (`.firebase/`, `*-debug.log`, `emulator-data/`)
- OS / Editor files (`.DS_Store`, `Thumbs.db`, `.idea/`, etc.)

### Verification
- Verified `.gitignore` properly positioned at repo root.

---

## Step 02.05 — Root `README.md`

Created [`README.md`](file:///C:/Doron/UpTheIrons/README.md) documenting:
- Project purpose and non-commercial ethos
- Architecture overview diagram (Next.js + FastAPI + Firebase emulators)
- Development principles (local first, small verified blocks, deterministic first)
- Local run commands for frontend, backend, and emulator suite
- Environment variable conventions

---

## Step 02.03 — Initialize Next.js

Configured Next.js App Router project in `frontend/`:
- **Core Packages:** Next.js 16.3.4, React 19.3.0, TypeScript, Tailwind CSS v4 (`@tailwindcss/postcss`).
- **Configuration Files:**
  - [`frontend/package.json`](file:///C:/Doron/UpTheIrons/frontend/package.json): scripts (`dev`, `build`, `start`).
  - [`frontend/next.config.mjs`](file:///C:/Doron/UpTheIrons/frontend/next.config.mjs): base Next.js config.
  - [`frontend/postcss.config.mjs`](file:///C:/Doron/UpTheIrons/frontend/postcss.config.mjs): PostCSS Tailwind v4 plugin.
  - [`frontend/tsconfig.json`](file:///C:/Doron/UpTheIrons/frontend/tsconfig.json): TypeScript path aliases (`@/*`).
- **App Baseline:**
  - [`frontend/app/globals.css`](file:///C:/Doron/UpTheIrons/frontend/app/globals.css): forge theme palette (`#121212`, accent `#FF5722`).
  - [`frontend/app/layout.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/layout.tsx): root metadata and theme styling.
  - [`frontend/app/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/page.tsx): forge home shell.

### Verification
- Ran `npm run build` in `frontend/`: succeeded with exit code 0.
- Static pages generated: `/` and `/_not-found`.

---

## Step 02.04 — Initialize Python Backend

Configured FastAPI backend in `backend/`:
- **Environment:** Created virtual environment in `backend/.venv` (Python 3.14.2).
- **Dependencies:** [`backend/requirements.txt`](file:///C:/Doron/UpTheIrons/backend/requirements.txt) (`fastapi`, `uvicorn[standard]`, `pydantic`, `pytest`, `httpx`).
- **Application:**
  - [`backend/app/__init__.py`](file:///C:/Doron/UpTheIrons/backend/app/__init__.py)
  - [`backend/app/main.py`](file:///C:/Doron/UpTheIrons/backend/app/main.py): Root (`/`) and health check (`/health`) endpoints.
- **Automated Tests:**
  - [`tests/backend/test_health.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_health.py): Validates `/` and `/health` responses.

### Verification
- Ran `pytest tests/backend`: 2 passed in 0.45s.

---

## Step 03.01 — Initialize Firebase Configuration

Created local configuration for Firebase Local Emulator Suite without cloud credentials:
- [`.firebaserc`](file:///C:/Doron/UpTheIrons/.firebaserc): Set local project ID `blacksmith-knight-local`.
- [`firebase.json`](file:///C:/Doron/UpTheIrons/firebase.json): Configured Firestore emulator (port 8080) and Emulator UI (port 4000).
- [`firestore.rules`](file:///C:/Doron/UpTheIrons/firestore.rules): Open local rules for development.
- [`firestore.indexes.json`](file:///C:/Doron/UpTheIrons/firestore.indexes.json): Initial indexes manifest.

---

## Step 03.02 — Enable & Verify Firestore Emulator

- Started Firestore emulator background process (`firebase emulators:start --only firestore`).
- Verified TCP connection on port `8080` (`TcpTestSucceeded: True`).
- Verified TCP connection on port `4000` (`TcpTestSucceeded: True`).
- Tested HTTP GET on `http://127.0.0.1:8080`: returned `Ok`.

---

## Step 03.03 — Firestore Write Test

- Created test document `smoke_tests/test_doc_01` via Firestore emulator REST API:
  - Path: `projects/blacksmith-knight-local/databases/(default)/documents/smoke_tests/test_doc_01`
  - Body: `{"title": "Anvil Technique Baseline", "status": "verified"}`
- Verified successful HTTP creation response with timestamp from emulator.

---

## Step 03.04 — Firestore Read Test

- Read test document `smoke_tests/test_doc_01` via GET request:
  - `http://127.0.0.1:8080/v1/projects/blacksmith-knight-local/databases/(default)/documents/smoke_tests/test_doc_01`
- Verified response:
  - Title: `Anvil Technique Baseline`
  - Status: `verified`

---

## Step 03.05 — Firestore Update Test

- Updated test document `smoke_tests/test_doc_01` via PATCH request:
  - Field: `status` -> `updated_ok`
- Verified response:
  - Status updated to `updated_ok`
  - Title preserved as `Anvil Technique Baseline`

---

## Step 03.06 — Firestore Delete Test

- Deleted test document `smoke_tests/test_doc_01` via DELETE request.
- Verified subsequent GET returns 404 (Not Found).

---

## Steps 03.07 - 03.10 — Decisions & Verification Gate

- **03.07 Auth Decision:** User auth deferred to post-MVP. Auth emulator stays disabled.
- **03.08 Service Boundary:** FastAPI is sole authority for writes, external ingestion, and normalization. Next.js reads via REST.
- **03.09 Reset Procedure:** In-memory mode + verified live reset endpoint (`DELETE http://127.0.0.1:8080/emulator/v1/projects/blacksmith-knight-local/databases/(default)/documents`).
- **03.10 Quality Gate:** All 10 Milestone 03 criteria satisfied locally without cloud credentials.
