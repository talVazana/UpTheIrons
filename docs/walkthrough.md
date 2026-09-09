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

---

## Milestone 04 — Backend Foundation

Implemented the structured FastAPI service foundation according to specification:

- **04.01 - 04.04 FastAPI Application & Health**:
  - Application entrypoint in [`backend/app/main.py`](file:///C:/Doron/UpTheIrons/backend/app/main.py).
  - Root `/` and `/health` endpoints.
  - Sub-router `/api/health` and `/api/v1/health` with Firestore emulator socket diagnostics.
- **04.05 API Configuration**:
  - Created [`backend/app/core/config.py`](file:///C:/Doron/UpTheIrons/backend/app/core/config.py) handling `APP_ENV`, `FIREBASE_PROJECT_ID`, `FIRESTORE_EMULATOR_HOST`, `CORS_ORIGINS`, `LOG_LEVEL`, and external API secret placeholders.
- **04.06 Error Handling Foundation**:
  - Created [`backend/app/core/errors.py`](file:///C:/Doron/UpTheIrons/backend/app/core/errors.py) defining standard error response envelopes (`error.code`, `error.message`, `error.details`), custom exceptions (`AppException`, `NotFoundError`, `BadRequestError`, `ValidationError`, `SourceError`), and handlers for 422 validation errors, HTTP exceptions, and uncaught 500 errors.
- **04.07 Structured Logging Foundation**:
  - Created [`backend/app/core/logging.py`](file:///C:/Doron/UpTheIrons/backend/app/core/logging.py) with JSON-formatted `StructuredFormatter` and `RequestLoggingMiddleware` capturing method, route path, status code, duration in milliseconds (`X-Process-Time-Ms`), and metadata.
- **04.08 API Versioning & Routing**:
  - Established `/api` and `/api/v1` routers in [`backend/app/api/router.py`](file:///C:/Doron/UpTheIrons/backend/app/api/router.py) and [`backend/app/api/v1/router.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/router.py).
- **04.09 & 04.10 Test Suite & Quality Gate**:
  - Created [`tests/backend/test_health.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_health.py), [`tests/backend/test_errors.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_errors.py), [`tests/backend/test_config.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_config.py), and [`tests/backend/test_logging.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_logging.py).
  - 10 passing tests in 0.55s via `pytest`.

---

## Milestone 05 — Frontend Foundation

Implemented the Next.js application shell, navigation framework, theme tokens, and accessible responsive layout:

- **05.01 & 05.02 Next.js Shell & Global Forge Theme**:
  - Updated [`frontend/app/globals.css`](file:///C:/Doron/UpTheIrons/frontend/app/globals.css) with Master Spec forge palette variables (`--bg-primary: #121212`, `--bg-surface: #1a1a1a`, `--accent-forge: #FF5722`, etc.), accessible `:focus-visible` styling, and reduced-motion media query.
- **05.03 Typography & Semantic HTML**:
  - Readable system typography stack, semantic headings, and high-contrast color ratios across all viewports.
- **05.04 & 05.05 Navigation Shell & Primary Route Placeholders**:
  - Created [`frontend/components/navigation/Navbar.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Navbar.tsx): sticky navigation with forge branding, desktop item indicators, and mobile drawer with accessible ARIA states.
  - Created [`frontend/components/navigation/Footer.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Footer.tsx): four-column responsive footer with craft ethos, quick navigation, and local architecture status.
  - Implemented 8 primary section page shells:
    - [`frontend/app/materials/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/materials/page.tsx)
    - [`frontend/app/videos/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/videos/page.tsx)
    - [`frontend/app/guides/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/guides/page.tsx)
    - [`frontend/app/projects/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/projects/page.tsx)
    - [`frontend/app/workshop/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/workshop/page.tsx)
    - [`frontend/app/tools/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/tools/page.tsx)
    - [`frontend/app/rules/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/rules/page.tsx)
    - [`frontend/app/search/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/search/page.tsx)
  - Updated [`frontend/app/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/page.tsx) with hero section, Bento pillars, and Apprentice Rule banner.
- **05.06 Accessibility Baseline**:
  - Added skip-to-content accessible landmark (`#main-content`) in [`frontend/app/layout.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/layout.tsx).
  - Keyboard navigation and high-contrast focus rings on interactive elements.
- **05.08 Quality Gate**:
  - Ran `npm run build` in `frontend/`: compiled successfully in 1238ms; all 11 static pages generated with exit code 0.

---

## Milestone 06 — Frontend ↔ Backend Integration

Verified local communication between Next.js and FastAPI:

- **06.01 Frontend API Client**:
  - Created [`frontend/lib/api.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/api.ts) exporting `fetchApi`, `checkBackendHealth`, and custom `ApiError` class parsing structured JSON error envelopes. Configured `BACKEND_URL` from `NEXT_PUBLIC_BACKEND_URL` with `http://localhost:8000` fallback.
- **06.02 Backend CORS Configuration**:
  - Verified backend `CORSMiddleware` in `backend/app/main.py` explicitly allows local origins (`http://localhost:3000`, `http://127.0.0.1:3000`).
- **06.03 & 06.04 Live Backend Status & Health Call**:
  - Created [`frontend/components/workshop/BackendStatusBadge.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/workshop/BackendStatusBadge.tsx) calling `/api/health` and displaying live API version and Firestore connection diagnostics.
  - Mounted badge directly in [`frontend/components/navigation/Navbar.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Navbar.tsx).
- **06.05 Graceful Offline Handling**:
  - Verified that when the backend is offline or unreachable, the frontend gracefully degrades to "API Offline (Standalone)" with a refresh trigger without throwing unhandled exceptions or breaking the UI.
- **06.06 Quality Gate & Build Verification**:
  - Frontend compiled in 807ms (`npm run build`, exit code 0).
  - Backend passed all 10 unit/integration tests in 0.55s (`pytest tests/backend`).

---

## Milestone 07 — Firebase Data Layer

Implemented storage abstraction and local Firestore emulator integration:

- **07.01 Firebase Backend Configuration**:
  - Leveraged `FIREBASE_PROJECT_ID` and `FIRESTORE_EMULATOR_HOST` from [`backend/app/core/config.py`](file:///C:/Doron/UpTheIrons/backend/app/core/config.py). Zero production credential exposure.
- **07.02 Repository Abstraction**:
  - Created [`backend/app/repositories/base.py`](file:///C:/Doron/UpTheIrons/backend/app/repositories/base.py) defining abstract CRUD methods (`create`, `get`, `update`, `delete`, `list`).
  - Created [`backend/app/repositories/firestore.py`](file:///C:/Doron/UpTheIrons/backend/app/repositories/firestore.py) implementing `FirestoreRepository` using high-speed async REST transport without heavy cloud dependencies.
  - Implemented bidirectional serialization (`to_firestore_value`, `from_firestore_value`, `dict_to_firestore`, `firestore_to_dict`).
- **07.03 - 07.07 Unit & CRUD Tests**:
  - Created [`tests/backend/test_firestore_repository.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_firestore_repository.py) verifying full roundtrip serialization across all native Python primitives (strings, ints, floats, booleans, lists, maps, nulls).
  - Verified `create`, `get`, `update`, `delete`, and `list` operations with HTTP transport mocks.
- **Milestone Quality Gate**:
  - Backend test suite: 13 passed in 0.57s (`pytest tests/backend`).
  - Frontend build: exit code 0 (`npm run build`).

---

## Milestone 08 — Core Domain / Data Model

Implemented typed domain entities, validation schemas, deterministic deduplication engine, and local seeding fixtures:

- **08.01 Common Content Envelope**:
  - Created [`backend/app/models/enums.py`](file:///C:/Doron/UpTheIrons/backend/app/models/enums.py) defining `ContentType`, `ContentStatus`, `DifficultyLevel`, `SourceType`, `SourceStatus`.
  - Created [`backend/app/models/content.py`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) with polymorphic `ContentEnvelope` (`id`, `type`, `title`, `slug`, `summary`, `category`, `tags`, `difficulty`, `source`, `status`, `metadata`).
  - Specialized domain metadata: `MaterialMetadata` with chemical composition & `HeatTreatmentRecipe`, `VideoMetadata`, `ProjectMetadata`.
- **08.02 & 08.03 Source & YouTube Channel Entities**:
  - Created [`backend/app/models/source.py`](file:///C:/Doron/UpTheIrons/backend/app/models/source.py) defining `SourceProvenance` tracking origin, `SourceEntity`, and `YouTubeChannelEntity`.
- **08.05 Schema Validation**:
  - Pydantic validation enforcing non-empty titles, automatic slug normalization, and metallurgical boundary checks.
- **08.06 Deterministic Deduplication Engine**:
  - Created [`backend/app/models/deduplication.py`](file:///C:/Doron/UpTheIrons/backend/app/models/deduplication.py) generating canonical unique keys (`video:youtube:{id}`, `material:{slug}`, `{type}:url:{hash}`, `{type}:title:{hash}`) preventing ingestion duplication.
- **08.07 Seeding Strategy**:
  - Created [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py) containing baseline fixtures for high-carbon steels (1084, 1095, 5160) and Level 1 projects (S-Hook) with `seed_initial_data()` loader.
- **Frontend Synchronization**:
  - Created matching TypeScript interfaces in [`frontend/lib/types.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/types.ts).
- **Milestone Quality Gate**:
  - Backend test suite: 18 passed in 0.62s (`pytest tests/backend`).
  - Frontend build: exit code 0 (`npm run build`).

---

## Milestone 09 — Source Management Framework

Implemented source management backend endpoints, validation schemas, repository integration, frontend API client, and Source Registry user interface:

- **09.01 - 09.03 Source Management API & Validation**:
  - Created [`backend/app/api/v1/sources.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/sources.py) providing full REST endpoints:
    - `POST /api/sources`: Register new source with URL validation, slug derivation, and initial `PENDING`/`ACTIVE` status.
    - `GET /api/sources`: Query sources with filters (`source_type`, `status`).
    - `GET /api/sources/{id}`: Fetch individual source by ID.
    - `PATCH /api/sources/{id}`: Update source configuration or toggle enabled/disabled status.
    - `DELETE /api/sources/{id}`: Remove source from the registry.
    - `POST /api/sources/{id}/test`: Health/connection probe verifying network reachability.
  - Mounted router in [`backend/app/api/v1/router.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/router.py).
- **09.04 & 09.05 Testing & Quality Gate**:
  - Created [`tests/backend/test_sources_api.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_sources_api.py) covering creation, validation rejection of invalid URLs, type filtering, toggle updates, and deletions.
  - 23 backend tests passed in 0.75s (`pytest tests/backend`).
- **09.06 Frontend Source Registry UI**:
  - Extended [`frontend/lib/api.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/api.ts) with `fetchSources`, `createSource`, `updateSource`, `deleteSource`, `testSourceConnection`, and `SourceItem` interface.
  - Created [`frontend/app/sources/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/sources/page.tsx) with:
    - Filter tabs (All, YouTube Channels, RSS Feeds, Manual / APIs).
    - Source status badges (`active`, `pending`, `disabled`, `error`).
    - Source creation modal with input validation.
    - Connection testing trigger.
    - Toggle enable/disable switch and deletion action with UI feedback.
  - Linked `/sources` in [`Navbar.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Navbar.tsx) and [`Footer.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Footer.tsx).
- **Milestone Quality Gate**:
  - Frontend production build: all 12 routes compiled cleanly (`npm run build`, exit code 0).
  - Backend test suite: 23 passed in 0.75s.






