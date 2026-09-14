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

---

## Milestone 10 — YouTube Channel Management

Implemented the controlled YouTube channel management registry, identifier resolver, duplicate prevention, ingestion sync triggers, and user interface:

- **10.01 - 10.05 YouTube Channel API & Deduplication**:
  - Created [`backend/app/api/v1/youtube.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/youtube.py) providing endpoints:
    - `POST /api/youtube/channels`: Register approved YouTube channel from `@handle`, full URL, or `UC...` ID. Enforces duplicate rejection by deterministic ID.
    - `GET /api/youtube/channels`: Query approved channels with `enabled`, `status`, and `category` filters.
    - `GET /api/youtube/channels/{channel_id}`: Fetch single channel.
    - `PATCH /api/youtube/channels/{channel_id}`: Update enabled toggle, priority, and categories.
    - `DELETE /api/youtube/channels/{channel_id}`: Remove channel from registry while retaining historical video records in content vault.
  - Mounted router in [`backend/app/api/v1/router.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/router.py).
- **10.06 & 10.10 Identifier Resolution & Anti-Crawling Enforcement**:
  - `POST /api/youtube/resolve`: Validates and parses channels from URLs or handles; integrates with YouTube Data API v3 when `YOUTUBE_API_KEY` is present, with deterministic offline fallback for local tests. Strictly rejects autonomous crawling.
- **10.11 Ingestion Sync Placeholder**:
  - `POST /api/youtube/channels/{channel_id}/sync`: Validates channel is enabled, marks status as `HEALTHY`, and records `last_synced_at` timestamp. Rejects disabled channels with 400 Bad Request.
- **10.08 - 10.09 Channel Manager UI**:
  - Created [`frontend/app/videos/channels/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/videos/channels/page.tsx) with:
    - Channel cards with avatar/thumbnails, handles, priority badges, category chips, and live status.
    - Filter tabs ("All Channels", "Enabled", "Disabled") and category selector.
    - Add Channel Modal with handle/URL input, real-time metadata inspector/preview, and priority selector.
    - Enable/disable toggle switches, "Sync Now" trigger, and deletion action.
  - Linked to `/videos/channels` from [`frontend/app/videos/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/videos/page.tsx) and [`frontend/app/sources/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/sources/page.tsx).
- **Milestone Quality Gate**:
  - Backend test suite: 31 passed in 1.12s (`pytest tests/backend`).
  - Frontend production build: all 13 routes compiled cleanly (`npm run build`, exit code 0).
  - Live Firestore verification: Registered `@BlackBearForge` on port 8000/8080, verified sync trigger, and verified duplicate rejection.

---

## Milestone 11 — YouTube Video Ingestion

Implemented the controlled YouTube video ingestion pipeline, dynamic Settings API for API keys, normalization to `ContentEnvelope`, strict deduplication, sync logging, and frontend curated video feed:

- **11.01 Dynamic Settings API & Key Masking**:
  - Created [`backend/app/api/v1/settings.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/settings.py) providing:
    - `GET /api/v1/settings/keys`: Returns configuration status with masked keys (`AIzaSy...****`).
    - `POST /api/v1/settings/keys`: Dynamically sets YouTube / AI API keys without restarting the server. Persists to Firestore `system_config/api_keys` and caches in memory.
- **11.02 - 11.04 YouTube Client & Quota-Friendly Uploads Resolver**:
  - Created [`backend/app/services/youtube_client.py`](file:///C:/Doron/UpTheIrons/backend/app/services/youtube_client.py).
  - Automatically translates `UC...` channel IDs to `UU...` uploads playlist IDs.
  - Queries `playlistItems.list` costing only 1 quota unit (compared to 100 units for search).
  - Provides deterministic offline mock fixtures when no API key is configured or when running isolated tests.
- **11.05 - 11.07 Normalization & Deterministic Deduplication**:
  - Created [`backend/app/services/youtube_ingestion.py`](file:///C:/Doron/UpTheIrons/backend/app/services/youtube_ingestion.py).
  - `normalize_youtube_video()` maps raw items to `ContentEnvelope` with `ContentType.VIDEO`, `VideoMetadata`, forged category and tag heuristics, slug creation, and embed URL formulation.
  - Enforces `video:youtube:{video_id}` deduplication before write; subsequent syncs skip existing videos.
  - Stores unique items in Firestore `content` collection.
- **11.08 & 11.09 Videos Feed API & Frontend Vault UI**:
  - Created [`backend/app/api/v1/videos.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/videos.py) (`GET /api/v1/videos`, `GET /api/v1/videos/{video_id}`) with filtering by category, tag, and channel.
  - Rebuilt [`frontend/app/videos/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/videos/page.tsx) with:
    - Category filter pills ("All Topics", "Forging", "Bladesmithing", "Heat Treatment", "Tools & Anvils").
    - "Configure YouTube API Key" modal for immediate API key updates without touching config files.
    - "Sync All Channels" trigger with progress spinner and feedback toast.
    - Video cards with duration badges, tags, channel chips, direct YouTube links, and video player embed modal.
- **11.10 - 11.14 Channel Sync Triggers & Audit Logging**:
  - `POST /api/youtube/channels/{channel_id}/sync` executes ingestion for single approved channel.
  - `POST /api/youtube/sync` synchronizes all enabled channels with partial failure isolation.
  - `GET /api/youtube/sync-logs` retrieves sync audit logs from `sync_logs` collection.
- **11.15 Quality Gate & Acceptance**:
  - Backend test suite: 38 passed in 1.75s (`pytest tests/backend`).
  - Frontend production build: all 13 routes compiled cleanly (`npm run build`, exit code 0).

---

## Milestone 12 — RSS Source Management & Ingestion

Implemented the controlled RSS and Atom ingestion pipeline, article normalization to `ContentEnvelope`, duplicate prevention, strict anti-crawling boundaries, and frontend knowledge feed:

- **12.01 - 12.03 RSS Feed Entity & Registry API**:
  - Created `RSSFeedEntity` in [`backend/app/models/source.py`](file:///C:/Doron/UpTheIrons/backend/app/models/source.py) (`type=SourceType.RSS_FEED`, `feed_url`, `site_url`, `feed_format`, `article_count`).
  - Added `ContentType.ARTICLE` to domain enums and TypeScript types.
  - Created [`backend/app/api/v1/rss.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/rss.py) providing:
    - `POST /api/v1/rss/feeds`: Registers approved RSS feed, strictly validates URL scheme, enforces duplicate rejection by URL or derived slug.
    - `GET /api/v1/rss/feeds`: Lists approved feeds with category/enabled filters.
    - `GET /api/v1/rss/feeds/{id}`: Retrieves single feed.
    - `PATCH /api/v1/rss/feeds/{id}`: Updates enabled, priority, categories, and title.
    - `DELETE /api/v1/rss/feeds/{id}`: Removes feed from registry while retaining historical articles in vault.
    - `POST /api/v1/rss/test`: Tests connection and previews sample articles from feed XML without writing to database.
- **12.04 - 12.07 RSS Client, Parser, Normalization & Deduplication**:
  - Created [`backend/app/services/rss_client.py`](file:///C:/Doron/UpTheIrons/backend/app/services/rss_client.py) using Python's built-in `xml.etree.ElementTree` parser for RSS 2.0 and Atom feeds.
  - Zero heavy third-party spider dependencies. Sanitizes raw HTML content and parses standard date formats (RFC 822 and ISO 8601).
  - Created [`backend/app/services/rss_ingestion.py`](file:///C:/Doron/UpTheIrons/backend/app/services/rss_ingestion.py):
    - `normalize_rss_article()` maps feed items to `ContentEnvelope` (`type=ContentType.ARTICLE`), infers categories (`materials`, `heat-treatment`, `tools`, `bladesmithing`, `guides`), extracts tags, and preserves full source attribution.
    - Uses deterministic canonical deduplication key `compute_deduplication_key(ContentType.ARTICLE, canonical_url=url)`.
    - Skips existing articles on subsequent sync runs, preventing duplicate writes.
- **12.08 & 12.11 Articles API & Frontend Knowledge Feed**:
  - Created [`backend/app/api/v1/articles.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/articles.py) (`GET /api/v1/articles`, `GET /api/v1/articles/{id}`).
  - Built live knowledge library in [`frontend/app/guides/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/guides/page.tsx) with topic filters, author attribution, direct links to full external articles, and "Sync Feeds Now" trigger.
  - Extended [`frontend/lib/api.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/api.ts) with typed client methods for RSS feeds and articles.
- **12.09, 12.10, 12.12 Sync Ingestion & Partial Failure Isolation**:
  - `POST /api/v1/rss/feeds/{id}/sync`: Syncs a single approved feed.
  - `POST /api/v1/rss/sync`: Syncs all enabled feeds in sequence.
  - Partial failure shield: one failing feed logs an error and updates feed status to `failed` without interrupting other feeds.
- **12.13 Strict Anti-Crawling Enforcement**:
  - Validated by test that parser strictly ingests items present in the feed XML and never spider-crawls outward to external domains.
- **Milestone Quality Gate**:
  - Backend test suite: 47 passed in 1.86s (`pytest tests/backend`).
  - Frontend production build: all 13 routes compiled cleanly (`npm run build`, exit code 0).
  - Recorded **DEC-015** (Unified Admin Settings Portal) and scheduled task **22.08** in the master work log.

---

## Milestone 13 — Product / Shop Source Framework

Implemented the controlled product source integration, honest tool evaluation model, dynamic price tracking without record duplication, anti-commercial-bias ranking, and frontend tools guide:

- **13.01 - 13.03 Product Source Model & Vendor Registry**:
  - Created `ProductSourceEntity` in [`backend/app/models/source.py`](file:///C:/Doron/UpTheIrons/backend/app/models/source.py) (`type=SourceType.PRODUCT_API`, `catalog_url`, `vendor_name`, `item_count`).
  - Created `ProductMetadata` in [`backend/app/models/content.py`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) with specs, pros, cons, beginner suitability, alternatives, and affiliate disclosure.
  - Created [`backend/app/api/v1/products.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/products.py) (`POST /api/v1/products/sources`, `GET`, `PATCH`, `DELETE`).
- **13.04 - 13.06 Product Normalizer & Dynamic Price Tracking**:
  - Created [`backend/app/services/product_client.py`](file:///C:/Doron/UpTheIrons/backend/app/services/product_client.py) with verified tool catalog fixtures (cast steel anvils, dual-burner propane forges, 2x72 belt grinders, wolf jaw tongs).
  - Created [`backend/app/services/product_ingestion.py`](file:///C:/Doron/UpTheIrons/backend/app/services/product_ingestion.py):
    - `normalize_product_item()` produces `ContentEnvelope` (`type=ContentType.PRODUCT`).
    - Deterministic deduplication key: `compute_deduplication_key(ContentType.PRODUCT, external_id=sku, canonical_url=purchase_url)`.
    - Detects price changes dynamically: updates price and `price_updated_at` without creating duplicate records.
- **13.07 & 13.08 Frontend Tools & Equipment Guide**:
  - Rebuilt [`frontend/app/tools/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/tools/page.tsx) with:
    - Transparent tool evaluation cards with price badges, pros/cons checklist, and alternatives.
    - Category pills ("All Gear", "Anvils", "Forges", "Belt Grinders", "Tongs").
    - "Beginner Friendly" filter checkbox and max budget filter.
    - "Sync Catalogs" trigger.
  - Extended [`frontend/lib/api.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/api.ts) with typed client methods for products.
- **13.09 Commercial Bias Check**:
  - Sorting is strictly algorithmic (by price ascending, then title). Affiliate partnership status never boosts ranking or priority.
- **13.10 Milestone Quality Gate**:
  - Backend test suite: 53 passed in 2.29s (`pytest tests/backend`).
  - Frontend production build: all 13 routes compiled cleanly (`npm run build`, exit code 0).

---

## Milestone 14 — Optional AI Enrichment Layer

Implemented the optional AI enrichment layer enforcing deterministic-first local architecture, strict metallurgical guardrails, provider abstraction, failure resilience, cost boundary limiting, and frontend enrichment badges:

- **14.01 AI Provider Interface**:
  - Created `BaseAIProvider` and `AIEnrichmentResult` in [`backend/app/services/ai/base.py`](file:///C:/Doron/UpTheIrons/backend/app/services/ai/base.py) with methods `enrich_content()`, `classify()`, `summarize()`, and `extract()`.
- **14.02 Provider Configuration**:
  - Created [`backend/app/services/ai/gemini.py`](file:///C:/Doron/UpTheIrons/backend/app/services/ai/gemini.py) implementing Google Gemini REST client with structured JSON output and markdown un-wrapping.
  - Created [`backend/app/services/ai/mock.py`](file:///C:/Doron/UpTheIrons/backend/app/services/ai/mock.py) for offline deterministic pipeline testing.
  - Dynamic API key resolution integrated via `get_effective_ai_api_key()` from Firestore and environment.
- **14.03 AI Disabled Mode**:
  - Validated by test that when AI provider is disabled or no key is supplied, ingestion and vault operations continue cleanly with zero failures.
- **14.04 - 14.07 Structured Content Enrichment**:
  - Technical summary generation without marketing jargon (preserves original summary in metadata).
  - Categorization into craft domains (`forging`, `bladesmithing`, `heat-treatment`, `tools`, `materials`, `guides`).
  - Automated domain tag extraction and merging with existing content tags.
  - Difficulty classification mapping to `DifficultyLevel` (`beginner`, `intermediate`, `advanced`).
- **14.08 Technical Source Guardrails**:
  - Created [`backend/app/services/ai/guardrails.py`](file:///C:/Doron/UpTheIrons/backend/app/services/ai/guardrails.py) enforcing `GUARDRAIL_SYSTEM_PROMPT` prohibiting hallucinations of chemical composition, heat-treatment temperatures, Rockwell hardness values, and safety rules.
- **14.09 AI Failure Resilience**:
  - Full exception trapping and timeouts on external AI calls ensure zero pipeline failure or content data loss on network or LLM outage.
- **14.10 Cost Boundary & Batch Enrichment**:
  - `batch_enrich_pending(limit=10)` processes solely un-enriched documents (`metadata.ai_processed != True`), preventing repetitive token consumption.
- **AI Endpoints & Frontend Badges**:
  - Created [`backend/app/api/v1/ai.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/ai.py) (`GET /status`, `POST /preview`, `POST /enrich/{id}`, `POST /enrich-pending`).
  - Added AI enrichment controls and badges to [`frontend/app/videos/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/videos/page.tsx) and [`frontend/app/guides/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/guides/page.tsx).
  - Extended [`frontend/lib/api.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/api.ts) with typed client methods.
- **Milestone Quality Gate**:
  - Backend test suite: 66 passed in 2.61s (`pytest tests/backend`).
  - Frontend production build: all 13 routes compiled cleanly (`npm run build`, exit code 0).

---

## Milestone 15 — Rules / Editorial / Safety Configuration

Implemented the comprehensive rules, safety standards, and editorial configuration layer:

- **15.01 - 15.07 Modular Rule Documents (`config/`)**:
  - Created [`config/mission.md`](file:///C:/Doron/UpTheIrons/config/mission.md): Core vision, craft over commerce, non-commercial ethos, local-first principles.
  - Created [`config/rules.md`](file:///C:/Doron/UpTheIrons/config/rules.md): Master rule index linking all domain rule specifications.
  - Created [`config/content_rules.md`](file:///C:/Doron/UpTheIrons/config/content_rules.md): Priority craft topics, relevance scoring thresholds, and mandatory rejection boundaries.
  - Created [`config/safety_rules.md`](file:///C:/Doron/UpTheIrons/config/safety_rules.md): Mandatory PPE standards (ANSI Z87.1, N95/P100, natural fibers) and critical hazard warnings (toxic zinc fumes on galvanized steel, unsealed Kaowool silica inhalation, oil quench fire procedures).
  - Created [`config/source_rules.md`](file:///C:/Doron/UpTheIrons/config/source_rules.md): Controlled source criteria, author attribution, deduplication, and anti-crawling boundaries.
  - Created [`config/product_rules.md`](file:///C:/Doron/UpTheIrons/config/product_rules.md): Commercial neutrality, transparent affiliate disclosure, live pricing timestamping, mandatory pros/cons/alternatives for tools.
  - Created [`config/metallurgy_rules.md`](file:///C:/Doron/UpTheIrons/config/metallurgy_rules.md): Anti-hallucination mandate for chemistry and heat treatment, manufacturer reference requirements, scrap steel warnings.
  - Created [`config/editorial_style.md`](file:///C:/Doron/UpTheIrons/config/editorial_style.md): Terse, craft-first voice, standard steel designations, anti-hype terminology.
- **15.08 Rule Loading Service**:
  - Created [`backend/app/services/rules_service.py`](file:///C:/Doron/UpTheIrons/backend/app/services/rules_service.py) with dynamic scanning, UTF-8 BOM tolerance, section parsing, and disk reload.
- **15.09 Rule Test Cases & Validation Engine**:
  - Created [`backend/app/services/rule_validator.py`](file:///C:/Doron/UpTheIrons/backend/app/services/rule_validator.py) with automated evaluation for commercial spam, clickbait, critical hazards (galvanized steel without acid strip, raw Kaowool), and craft relevance scoring.
  - Validated via 11 automated test cases in [`tests/backend/test_rules.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_rules.py) covering positive and negative scenarios.
- **15.10 Editorial Override Engine**:
  - Extended [`ContentStatus`](file:///C:/Doron/UpTheIrons/backend/app/models/enums.py) enum with `PINNED`, `VERIFIED`, and `HIDDEN`.
  - Added editorial status and metadata override API (`POST /api/v1/rules/override/{id}`).
- **15.11 Interactive Codex & Safety Testbed UI**:
  - Rebuilt [`frontend/app/rules/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/rules/page.tsx) with rule file navigator, section reader, live disk reload, and real-time interactive compliance tester.
  - Extended [`frontend/lib/api.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/api.ts) with typed client methods for rules and overrides.
- **Milestone Quality Gate**:
  - Backend test suite: 77 passed in 2.74s (`pytest tests/backend`).
  - Frontend production build: all 13 routes compiled cleanly (`npm run build`, exit code 0).

---

## Milestone 16 — Knowledge Library

Implemented the static/editorial knowledge library foundation, Technical Trust Classifications, accessible Markdown renderer with callouts and TOC anchors, structured peer-reviewed source references, high-visibility safety alert components, and an initial master guide:

- **16.01 Guide Domain Model & Technical Trust Labels**:
  - Created [`TrustLabel`](file:///C:/Doron/UpTheIrons/backend/app/models/enums.py) enum (`fact`, `source_backed_recommendation`, `craft_practice`, `personal_experience`, `historical_interpretation`, `ai_summary`, `opinion`).
  - Created [`GuideMetadata`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py), [`SourceReference`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py), [`SafetyPrecaution`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py), and [`RelatedContentLink`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) under `ContentEnvelope`.
  - Added matching TypeScript interfaces in [`frontend/lib/types.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/types.ts).
- **16.02 & 16.08 Master Guides REST API**:
  - Created [`backend/app/api/v1/guides.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/guides.py) providing:
    - `GET /api/v1/guides`: Filter by craft category, difficulty level, trust label, and free-text search `q` scanning titles, summaries, tags, and full markdown body.
    - `GET /api/v1/guides/{slug_or_id}`: Retrieves complete guide by slug or ID with full markdown and metadata.
    - `POST /api/v1/guides`: Creates new guide with strict `RuleValidator` safety and commercial spam verification.
    - `PATCH /api/v1/guides/{slug_or_id}`: Partial update endpoint re-validating against editorial rules.
  - Mounted router in [`backend/app/api/v1/router.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/router.py).
- **16.03 Markdown Rendering Engine**:
  - Created [`frontend/components/guides/MarkdownRenderer.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/guides/MarkdownRenderer.tsx) rendering H1-H3 headers with jump-link slug anchors, GitHub-style alert callouts (`[!NOTE]`, `[!WARNING]`, `[!TIP]`, `[!CAUTION]`), fenced code blocks, numbered and bulleted lists, horizontal dividers, inline code tokens, and citation markers without heavy external libraries.
- **16.04 Source References Component**:
  - Created [`frontend/components/guides/SourceReferencesList.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/guides/SourceReferencesList.tsx) displaying structured academic and guild citations with citation keys (e.g. `[Postman1998]`), author attributions, publication dates, trust labels, and direct external references.
- **16.05 Safety Section Component**:
  - Created [`frontend/components/guides/SafetySection.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/guides/SafetySection.tsx) presenting high-visibility hazard warning banners with flame/shield icons, ANSI Z87.1 / NRR 28+ PPE checklists, and actionable mitigation procedures.
- **16.06 Technical Trust Badges**:
  - Created [`frontend/components/guides/TrustBadge.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/guides/TrustBadge.tsx) visually communicating trust level with craft color tokens and explanatory hover tooltips.
- **16.07 Related Content Links**:
  - Created [`frontend/components/guides/RelatedContentSection.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/guides/RelatedContentSection.tsx) linking master guides to metallurgical library entries (`mat-1084`), apprentice projects (`proj-s-hook`), and equipment tutorials.
- **16.09 Complete Master Guide Seeding**:
  - Authored and seeded exhaustive master guide: *"The Anvil: Anatomy, Selection, Rebound Testing, and Workshop Mounting"* (`guide-anvil-selection-mounting`) in [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py). Covers London-pattern geometry, cast steel vs cast iron (ASO warning), ball-bearing rebound percentage test, acoustic ring diagnostics, knuckle rule ergonomics, and silicone/chain sound dampening.
  - Seeded secondary master guide on heat treatment phase transformations (`guide-heat-treatment-fundamentals`).
- **Frontend Pages**:
  - Rebuilt [`frontend/app/guides/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/guides/page.tsx) with tabs for "Master Craft Guides" and "Guild Articles & RSS", free-text search input, category filters, difficulty filters, and trust classification selectors.
  - Created [`frontend/app/guides/[slug]/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/guides/[slug]/page.tsx) as the comprehensive master guide reader with quick navigation table of contents, safety warnings, markdown body, citations, and related content.
- **Milestone Quality Gate**:
  - Backend test suite: 85 passed in 2.90s (`pytest tests/backend -v`).
  - Frontend production build: all 13 routes compiled cleanly (`npm --prefix frontend run build`, exit code 0).

---

## Milestone 17 — Material & Steel Library

Implemented the complete technical metallurgy vault, chemical composition breakdown, four-phase heat treatment protocols, spark testing profiles, side-by-side multi-steel comparison engine, and responsive frontend catalog and dossier views:

- **17.01 - 17.03 Metallurgical Domain Models & Standard Provenance**:
  - Created [`MaterialMetadata`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) and [`HeatTreatmentRecipe`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) in backend, synchronized in [`frontend/lib/types.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/types.ts).
  - Captures carbon percentages, alloying elements map, steel category (`carbon_steel`, `tool_steel`, `spring_steel`, etc.), forging thermal ranges, quench speed and mediums, and ASTM/SAE standard cross-references.
  - Enforced strict validation requiring peer-reviewed metallurgical handbook citations for all created materials.
- **17.04 Seeded Metallurgy Vault**:
  - Authored and seeded 5 authoritative reference alloys in [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py):
    - `1084 High Carbon Steel` (`mat-1084`): Eutectoid carbon benchmark (~0.84% C), beginner-friendly, oil quench.
    - `1095 High Carbon Steel` (`mat-1095`): Hypereutectoid carbon steel (~0.95% C), fast oil quench (Parks 50), hamon activity.
    - `5160 Spring Steel` (`mat-5160`): Tough chromium spring alloy (~0.60% C, 0.80% Cr), deep hardenability, shock choppers.
    - `O1 Tool Steel` (`mat-o1`): Oil-hardening cold work tool steel (W, V carbides), 10 min soak time, keen edge stability.
    - `W1 Tool Steel` (`mat-w1`): High-carbon water/fast-oil steel (~1.00% C), shallow-hardening shock core.
- **17.05 - 17.08 Frontend Metallurgy Dossier & Interactive Protocols**:
  - Created [`frontend/components/materials/CompositionBreakdown.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/materials/CompositionBreakdown.tsx): visual percentage bar displaying nominal elements against the iron matrix with educational cards explaining the metallurgical role of each element (martensite formation, grain refinement, quench depth, wear resistance).
  - Created [`frontend/components/materials/HeatTreatmentProtocol.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/materials/HeatTreatmentProtocol.tsx): 4-phase thermal cycle timeline (Normalizing, Annealing, Austenitizing/Decalescence line, Quenching) and a calibrated tempering schedule table mapping temperatures to HRC, toughness, and oxide colors.
  - Created [`frontend/components/materials/SparkProfileCard.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/materials/SparkProfileCard.tsx): diagnostic spark testing guide for workshop identification of mystery steel.
  - Created [`frontend/components/materials/MaterialCard.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/materials/MaterialCard.tsx): catalog card with carbon visualizer, key alloy chips, thermal specs, beginner suitability badge, and comparison selector checkbox.
  - Created [`frontend/app/materials/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/materials/page.tsx): dynamic catalog with category tabs, beginner-friendly filter, carbon % presets, live search query, and floating comparison tray.
  - Created [`frontend/app/materials/[slug]/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/materials/[slug]/page.tsx): comprehensive single-steel technical dossier.
- **17.09 & 17.10 Multi-Criteria Search & Deterministic Steel Comparison**:
  - Implemented `GET /api/v1/materials` supporting category, carbon range, beginner toggle, and full-text search.
  - Implemented `GET /api/v1/materials/compare?ids=1084,1095,5160`: compares 2–4 steels side-by-side, generating composition matrices, edge retention rankings, and impact toughness rankings.
  - Created [`frontend/components/materials/MaterialComparisonModal.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/materials/MaterialComparisonModal.tsx): modal providing side-by-side metallurgical property tables and comparative rankings.
- **Milestone Quality Gate**:
  - Backend test suite: 92 passed in 3.00s (`pytest tests/backend -v`).
  - Frontend production build: all routes compiled cleanly including `○ /materials` and `ƒ /materials/[slug]` (`npm --prefix frontend run build`, exit code 0).

---

## Milestone 18 — Workshop / Tools Library

Implemented structured workshop knowledge covering tool selection criteria, apprentice guidance, technical specifications, hazard analysis with mandatory PPE, maintenance protocols, DIY alternatives, and cross-tool relationships:

- **18.01 & 18.02 Tool Domain Model & Tool Categories**:
  - Created [`ToolMetadata`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) and [`ToolCategory`](file:///C:/Doron/UpTheIrons/backend/app/models/enums.py) (`forging`, `heating`, `grinding`, `finishing`, `infrastructure`), synchronized in [`frontend/lib/types.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/types.ts).
  - Captures primary purpose, essential tasks, selection criteria, beginner guidance, beginner friendliness, DIY buildability, improvised alternatives, maintenance protocols, safety precautions, and engineering specifications.
- **18.03 Dedicated Workshop Knowledge Pages & UI Components**:
  - Created [`frontend/app/workshop/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/workshop/page.tsx): interactive catalog with category tabs, beginner-friendly toggle, DIY buildable filter, live text search, and the Smith's Golden Triangle layout guide (Forge ↔ Anvil ↔ Vise ↔ Quench).
  - Created [`frontend/app/workshop/[slug]/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/workshop/[slug]/page.tsx): comprehensive single-tool technical dossier.
  - Created [`frontend/components/tools/ToolCard.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/tools/ToolCard.tsx) displaying category icons, purpose, essential tasks, and links.
  - Created [`frontend/components/tools/ToolSpecsGrid.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/tools/ToolSpecsGrid.tsx) rendering formatted engineering parameters.
  - Created [`frontend/components/tools/MaintenanceGuide.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/tools/MaintenanceGuide.tsx) outlining upkeep protocols.
  - Created [`frontend/components/tools/DiyAlternativesCard.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/tools/DiyAlternativesCard.tsx) providing low-cost and improvised alternatives.
- **18.04 Seeded London-Pattern Anvil Entry**:
  - Seeded *"London-Pattern Cast Steel Anvil"* (`tool-london-pattern-anvil`) in [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py): monolithic cast alloy steel body, 80%+ rebound score, horn geometry, knuckle height rule, and silicone/chain sound deadening.
- **18.05 Seeded Swedish Cross-Peen Hammer Entry**:
  - Seeded *"Swedish Cross-Peen Blacksmith Hammer"* (`tool-cross-peen-hammer`) in [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py): 2.0 to 2.5 lb weight recommendation, crowned planishing face, perpendicular drawing out, and straight-grain hickory wedging.
- **18.06 Seeded 2x72 Industrial Belt Grinder Entry**:
  - Seeded *"2x72 Variable Speed Industrial Belt Grinder"* (`tool-2x72-belt-grinder`) in [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py): 2–3 HP TEFC motor, VFD surface-feet-per-minute control (400–4500 SFPM), platen options, and spark trap water trough.
- **18.07 Rigorous Workshop Safety Metadata**:
  - Built [`frontend/components/tools/ToolSafetyNotice.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/tools/ToolSafetyNotice.tsx) enforcing explicit hazard analysis, mitigation procedures, and mandatory PPE checklists (ANSI Z87.1 glasses, NRR 28+ hearing protection, NIOSH P100/N95 respirator for metal dust, refractory ceramic fiber sealing).
- **18.08 Related Tools Cross-Referencing**:
  - Wired bidirectional `RelatedContentLink` relationships cross-referencing tools across common forge workflows (Anvil ↔ Hammer ↔ Propane Forge ↔ Post Vise).
- **Backend API & Test Suite**:
  - Implemented `GET /api/v1/tools`, `GET /api/v1/tools/{slug_or_id}`, and `POST /api/v1/tools` in [`backend/app/api/v1/tools.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/tools.py).
  - Created [`tests/backend/test_tools.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_tools.py) with 10 comprehensive tests.
- **Milestone Quality Gate**:
  - Backend test suite: 102 passed in 3.12s (`pytest tests/backend -v`).
  - Frontend production build: all routes compiled cleanly including `○ /workshop` and `ƒ /workshop/[slug]` (`npm --prefix frontend run build`, exit code 0).









## Milestone 19 — Projects Library

Implemented progressive hands-on workshop projects:

- **19.01 Project Model**: Extended models to include `ProjectStep` with duration and warnings, and linked materials/tools.
- **19.02 Beginner Project**: Seeded Classic Blacksmith's S-Hook.
- **19.03 Intermediate Project**: Seeded Wolf Jaw Tongs.
- **19.04 Advanced Project**: Seeded High Carbon Camp Knife.
- **19.05 Project Navigation**: Created `frontend/app/projects/page.tsx` library grid with difficulty filters.
- **19.06 Related Materials/Tools**: Displayed tools and materials clearly on the project detail page at `frontend/app/projects/[slug]/page.tsx`.

## Milestone 20 - Bento Feed Engine

Implemented Bento Feed Engine. Created feed.py API endpoint. Updated UI. M20 complete.

## Milestone 21 - Search & Filtering

Implemented global search and filtering. Created search.py. M21 complete.

## Milestone 22 - Source / Sync Monitoring & Logs

Implemented sync logs monitoring. Created sync_logs.py. M22 complete.


---

## Milestone 18 � Admin Authentication & Rebranding

Implemented the initial Admin settings portal and visual branding updates:

- **18.01 Rebranding**:
  - Replaced all occurrences of "Blacksmith Knight" with "Kiko's BlackSmith Heaven" across the application.
  - Replaced legacy images (hero_forge.jpg, 	ools_workshop.jpg, ideo_forge.jpg) with new images keeping the forge motive but strictly removing human figures.
- **18.02 Admin Authentication**:
  - Created ackend/app/api/v1/auth.py providing /login, /change-password, and /verify.
  - Added simple MVP session tracking and Firestore fallback for credentials (default Kiko / Kiko).
- **18.03 Admin Portal UI**:
  - Created rontend/app/admin/page.tsx for login and password management.
  - Added a floating kiko.png logo button to the main page to access the admin portal.

---

## Milestone 25 - Admin Material Management

Implemented Admin Material Form and Delete abilities:

- **25.01 Add Material Form**: Created UI at rontend/app/admin/materials/new/page.tsx. Fields are optional. Added an interactive help guide.
- **25.02 Materials API Update**: Added DELETE /materials route. Removed strict source_reference lengths to allow flexible inputs.
- **25.03 Admin-Only Actions**: "Add Material" and "Remove" options render on the materials page and cards exclusively for logged-in admins.
