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
