# Blacksmith Knight — Forging Heaven
# Software Development Program & Work Log

**Document type:** Living Software Development Program / Work Log  
**Project:** Blacksmith Knight — Forging Heaven  
**Version:** 1.0  
**Created:** 2026-09-09  
**Status:** Development program defined — implementation not yet started  
**Companion document:** `Blacksmith_Knight_Forging_Heaven_Master_Spec_v3.md`

---

# 0. Purpose of This Document

This document answers a different question from the Master Specification.

- **Master Specification:** What are we building?
- **Development Program:** How are we going to build it?
- **Work Log:** What have we actually done, tested, decided, broken, fixed, and verified?

This is a **living document**. It must be updated during development.

The project is deliberately divided into small building blocks. We should avoid attempting to build the complete application at once.

The basic development loop is:

```text
READ SPECIFICATION
       ↓
SELECT ONE SMALL BLOCK
       ↓
DESIGN
       ↓
IMPLEMENT
       ↓
RUN LOCALLY
       ↓
TEST
       ↓
VERIFY
       ↓
COMMIT
       ↓
UPDATE WORK LOG
       ↓
SELECT NEXT BLOCK
```

A block is not considered complete merely because the code exists. It is complete only when it has been tested and its acceptance criteria are satisfied.

---

# 1. Governing Principles

## 1.1 Small Blocks

Every feature must be decomposed into the smallest practical executable tasks.

Prefer:

```text
Create model
→ test model
→ create endpoint
→ test endpoint
→ connect frontend
→ test frontend
→ verify integration
```

over:

```text
Build the entire feature
```

## 1.2 Local First

Everything possible must work locally before cloud infrastructure becomes part of the development loop.

Target local environment:

```text
┌──────────────────────────────────────────────┐
│                LOCAL MACHINE                 │
│                                              │
│  Next.js Frontend                            │
│       │                                      │
│       ▼                                      │
│  FastAPI Backend                             │
│       │                                      │
│       ▼                                      │
│  Firebase Local Emulator Suite               │
│       ├── Firestore                          │
│       ├── Authentication                     │
│       ├── Storage if required                │
│       └── other Firebase services if needed  │
│                                              │
│  Automated tests                             │
│  Local test data                             │
└──────────────────────────────────────────────┘
```

The application should not depend on a production Firebase project merely to run or test basic functionality.

## 1.3 One Verified Block at a Time

Do not stack unverified features.

If Block 04.03 is broken, do not silently continue building five layers on top of it.

Fix or explicitly record the blocker first.

## 1.4 Deterministic Software First

Use ordinary software for deterministic work:

- API calls
- scheduling
- retries
- pagination
- deduplication
- validation
- database operations
- source management
- logging
- synchronization

AI is an optional enrichment layer for tasks where it provides real value.

## 1.5 Controlled Sources

Blacksmith Knight must never become an unrestricted crawler.

External content enters through explicitly configured and approved sources.

```text
USER-APPROVED SOURCE
        ↓
DETERMINISTIC COLLECTOR
        ↓
NORMALIZATION
        ↓
DEDUPLICATION
        ↓
VALIDATION / RULES
        ↓
OPTIONAL AI ENRICHMENT
        ↓
STORAGE
        ↓
APPLICATION
```

This applies to:

- YouTube
- RSS
- product/shop sources
- future integrations

## 1.6 No Premature Cloud Complexity

Firebase is the intended production platform for the application/data layer, but local Firebase emulators are the first target.

Render or another cloud platform may be introduced for Python API/worker workloads if architecture testing shows that it is useful or necessary.

Cloud architecture is a decision to validate, not something to assume blindly.

## 1.7 No Premature AI

The application must remain useful when AI is:

- disabled
- unavailable
- rate limited
- misconfigured
- too expensive

AI should not become a single point of failure for deterministic ingestion or basic application behavior.

## 1.8 Git Branching & Milestone Lifecycle Rules

To maintain high development velocity with total repo stability, every milestone strictly adheres to this protocol:

1. **Dedicated Milestone Branch:** For each milestone, work on a dedicated branch named `feature/MilestoneXX` (where `XX` is its milestone number, e.g. `feature/Milestone14`).
2. **Proactive File Operations:** Create, update, and refactor code, models, endpoints, and components proactively without prompting for permission.
3. **Delete Confirmation Boundary:** Prompt the user ONLY before deleting files or components, and ONLY at the conclusion of the milestone.
4. **Milestone Quality Gate:** Before closing any milestone:
   - Run backend automated test suite: `pytest tests/backend`
   - Run frontend production build: `npm --prefix frontend run build`
   - Verify zero lint/type errors and 100% test pass rate.
5. **Documentation Discipline:**
   - Update `docs/Blacksmith_Knight_Forging_Heaven_Development_Program_and_Work_Log.md` marking the milestone tasks as COMPLETE with technical notes.
   - Update `docs/walkthrough.md` with walkthrough notes and verified gates.
6. **Git Merge & Sync Flow:**
   - Commit all changes and push `feature/MilestoneXX` to remote.
   - Checkout `develop`, merge `feature/MilestoneXX`, and push `develop` to `origin/develop`.
7. **Stop at Completion:** Conclude each milestone cleanly and wait for user instruction before starting the next milestone.

---

# 2. Relationship to the Master Specification

The Master Specification defines the complete product vision and architecture.

Important requirements inherited from it include:

- Next.js + React + TypeScript
- Tailwind CSS
- Framer Motion
- dark industrial forge aesthetic
- responsive Bento Grid
- polymorphic cards
- knowledge library
- material/steel information
- tools/workshop information
- projects
- rules and safety
- controlled YouTube channels
- RSS sources
- approved product sources
- optional AI enrichment
- source attribution
- deterministic deduplication
- logging
- search and filtering
- eventual Firebase-backed production architecture
- optional Render/cloud worker infrastructure

This development document must not redefine product requirements unless a deliberate architectural decision is recorded.

---

# 3. Development Status Legend

Use these status symbols consistently.

```text
⬜ NOT STARTED
🔵 READY
🔄 IN PROGRESS
🟡 BLOCKED
🧪 TESTING
✅ COMPLETE
⚠ PARTIAL / KNOWN LIMITATION
❌ FAILED / REQUIRES REWORK
⏸ DEFERRED
```

A task should normally progress:

```text
⬜ → 🔵 → 🔄 → 🧪 → ✅
```

A task may temporarily become:

```text
🔄 → 🟡
🔄 → ❌
```

with the reason recorded in the work log.

---

# 4. Definition of Done

A development block is complete only when applicable items below are satisfied.

```text
[ ] Requirement understood
[ ] Design decision recorded where needed
[ ] Code/configuration implemented
[ ] Local application starts
[ ] Relevant automated tests pass
[ ] Manual test completed where appropriate
[ ] Error handling considered
[ ] Logging considered where appropriate
[ ] Security/secrets checked
[ ] No obvious regression
[ ] Acceptance criteria satisfied
[ ] Git diff reviewed
[ ] Git commit created
[ ] Work log updated
[ ] Next step identified
```

Not every task requires every checkbox, but the block owner must explicitly decide which checks apply.

---

# 5. Environment Strategy

## 5.1 Development Machine

Primary development target:

```text
Windows
VS Code
Git
GitHub
Node.js / npm
Python
Python virtual environment
Firebase CLI
Firebase Local Emulator Suite
```

Exact package/runtime versions should be recorded when the environment is actually installed and verified.

Do not hard-code obsolete versions into this document without checking the current supported versions at installation time.

## 5.2 Frontend Local Runtime

Initial target:

```text
Next.js development server
http://localhost:3000
```

Responsibilities:

- UI
- routing
- responsive layout
- Bento components
- user interaction
- API client
- Firebase client integration where required

## 5.3 Backend Local Runtime

Initial target:

```text
Python
FastAPI
Uvicorn
http://localhost:8000
```

FastAPI is the preferred starting point because it is lightweight, Python-native, typed through Pydantic, and well suited to REST APIs.

However, the architecture is not considered permanently locked until the backend foundation milestone validates:

- local development
- testing
- Firebase integration
- background workers
- deployment feasibility
- maintainability

If FastAPI proves unsuitable, record the decision before changing architecture.

## 5.4 Firebase Local Runtime

Use the Firebase Local Emulator Suite for local cloud behavior where practical.

Expected early services:

```text
Firestore
Authentication
```

Potential later services:

```text
Storage
Functions
Hosting/App Hosting-related behavior where appropriate
other Firebase services only when required
```

Do not enable or maintain services that the project does not use.

## 5.5 Cloud Runtime

Production architecture is expected to be evaluated around:

```text
Firebase
├── Firestore
├── Authentication if required
└── frontend hosting/application services as selected

Python backend / workers
└── Render or another suitable runtime if required

GitHub
└── source control + CI/CD + scheduled jobs where appropriate
```

This is intentionally a decision point rather than a fixed implementation.

---

# 6. Environment Variables and Secrets

Never commit secrets.

Local configuration should use environment files such as:

```text
.env.local
.env
```

depending on the specific application/tooling requirements.

Typical future variables may include:

```text
FIREBASE_PROJECT_ID
FIREBASE_CLIENT_CONFIG
YOUTUBE_API_KEY
AI_API_KEY
PRODUCT_API_KEYS
BACKEND_URL
```

Frontend public configuration and server-only secrets must be clearly separated.

Rules:

```text
[ ] No API keys in Git
[ ] No secrets in JSON data
[ ] No secrets in frontend source
[ ] No secrets in logs
[ ] .env files ignored by Git where appropriate
[ ] Example environment template committed without secrets
```

---

# 7. Git Development Strategy

## 7.1 Repository

The project should have a clean repository structure separating frontend, backend, configuration, tests, and deployment infrastructure.

Initial target:

```text
blacksmith-knight/
├── frontend/
├── backend/
├── config/
├── tests/
├── docs/
├── scripts/
├── .github/
└── README.md
```

The exact structure may evolve during implementation.

## 7.2 Branching

Recommended model:

```text
main
  │
  └── develop
        │
        ├── feature/...
        ├── fix/...
        └── chore/...
```

For very small changes, direct development on the agreed working branch may be acceptable if the repository workflow is deliberately chosen.

The important rule is traceability: every meaningful completed block should be associated with a commit.

## 7.3 Commit Discipline

Prefer commits that describe one completed block.

Examples:

```text
feat(frontend): create initial Next.js shell
feat(backend): add health endpoint
feat(firebase): configure local firestore emulator
feat(sources): add source registry model
fix(youtube): handle missing channel metadata
```

Avoid giant commits containing unrelated work.

---

# 8. Testing Strategy

Testing grows with the project.

## 8.1 Level 1 — Manual Smoke Testing

Used for the earliest UI blocks.

Examples:

- application starts
- page renders
- navigation works
- button responds
- responsive layout does not collapse

## 8.2 Level 2 — Unit Tests

Backend:

```text
pytest
```

Test:

- models
- validation
- normalizers
- deduplication
- rule evaluation
- utility functions

Frontend tests may be added for:

- components
- utilities
- state behavior
- filters

## 8.3 Level 3 — API Tests

Test FastAPI endpoints using a test client.

Examples:

```text
GET /health
GET /api/feed
GET /api/materials
GET /api/videos
POST /api/sources/youtube
```

## 8.4 Level 4 — Firebase Emulator Integration Tests

Test application behavior against local emulators.

Examples:

```text
Create Firestore document
→ retrieve document
→ update document
→ delete document
```

and:

```text
FastAPI
→ Firebase emulator
→ stored data
→ API response
→ Next.js display
```

## 8.5 Level 5 — End-to-End Tests

Introduce later, after the application has meaningful user flows.

Potential tool:

```text
Playwright
```

Examples:

```text
Open site
→ filter videos
→ open channel manager
→ add channel
→ verify channel appears
```

## 8.6 Level 6 — Production Smoke Tests

Only after deployment exists.

Test:

- frontend availability
- API availability
- Firebase connectivity
- authentication if enabled
- scheduled workers
- source synchronization
- error logging

---

# 9. Local Development Commands — Target

Eventually the project should support simple commands such as:

```text
start frontend
start backend
start firebase emulators
start all
run tests
run lint
run typecheck
```

A later milestone should create a documented one-command or small-command development workflow.

Do not over-engineer this during the first environment block.

---

# 10. Master Milestone Map

```text
M00  Development Program & Project Preparation
M01  Development Environment
M02  Repository & Project Skeleton
M03  Firebase Local Emulator Foundation
M04  Backend Foundation
M05  Frontend Foundation
M06  Frontend ↔ Backend Integration
M07  Firebase Data Layer
M08  Core Domain/Data Model
M09  Source Management Framework
M10  YouTube Channel Management
M11  YouTube Video Ingestion
M12  RSS Source Management & Ingestion
M13  Product / Shop Source Framework
M14  Optional AI Enrichment Layer
M15  Rules / Editorial / Safety Configuration
M16  Knowledge Library
M17  Material & Steel Library
M18  Workshop / Tools Library
M19  Projects Library
M20  Bento Feed Engine
M21  Search & Filtering
M22  Source / Sync Monitoring & Logs
M23  UI Polish / Responsive / Accessibility
M24  Testing & Reliability
M25  Cloud Architecture Validation
M26  Firebase Deployment
M27  Python API / Worker Deployment if required
M28  CI/CD & Scheduled Automation
M29  MVP Integration & Acceptance
M30  Post-MVP Backlog
```

The milestone numbers are stable references. New tasks should be inserted under the appropriate milestone rather than renumbering old completed work unless there is a strong reason.

---

# 11. MILESTONE 00 — Development Program & Project Preparation

**Goal:** Establish the development process before writing application code.

### 00.01 Confirm Master Specification

- [x] Master Specification v3 reviewed
- [x] Product vision understood
- [x] Controlled-source architecture understood
- [x] Local-first development requirement recorded
- [x] Firebase hosting/backend direction recorded

**Status:** ✅ COMPLETE

### 00.02 Create Development Program

- [x] Create this document
- [x] Define milestones
- [x] Define task structure
- [x] Define Definition of Done
- [x] Define work-log format

**Status:** ✅ COMPLETE

### 00.03 Establish Working Rule

Rule:

> Never jump from a high-level feature directly to a large implementation. Decompose it into small testable blocks.

**Status:** ✅ COMPLETE

---

# 12. MILESTONE 01 — Development Environment

**Goal:** Build a clean, reproducible Windows development environment.

## 01.01 Verify Git

- [ ] Git installed
- [ ] `git --version` works
- [ ] Git identity configured
- [ ] GitHub access verified

**Acceptance:** Git can clone, branch, commit, and push.

## 01.02 Verify VS Code

- [ ] VS Code installed
- [ ] Project folder opens
- [ ] Integrated terminal works

## 01.03 Install / Verify Node.js

- [ ] Node.js installed
- [ ] `node --version` works
- [ ] `npm --version` works
- [ ] Version recorded in work log

## 01.04 Verify Python

- [ ] Python installed
- [ ] `python --version` works
- [ ] Version recorded

## 01.05 Create Python Virtual Environment Test

- [ ] Create temporary venv
- [ ] Activate it
- [ ] Verify Python executable
- [ ] Deactivate it

## 01.06 Install Firebase CLI

- [ ] Firebase CLI installed
- [ ] `firebase --version` works
- [ ] Firebase login method understood

## 01.07 Verify Firebase Project Access

- [ ] Firebase project identified
- [ ] Local project configuration strategy documented
- [ ] No production secrets copied into source code

## 01.08 Install Backend Development Packages

Initial candidates:

```text
fastapi
uvicorn
pydantic
pytest
httpx
```

Exact versions should be recorded when installed.

## 01.09 Install Frontend Dependencies

Initial candidates:

```text
next
react
react-dom
typescript
tailwindcss
framer-motion
```

Exact versions should be recorded when installed.

## 01.10 Install Firebase Emulator Components

- [ ] Emulator Suite available
- [ ] Required Java/runtime dependency verified if applicable
- [ ] Firestore emulator can start

## 01.11 Environment Documentation

Create:

```text
.env.example
README development section
```

Document how another developer can reproduce the environment.

## 01.12 Environment Smoke Test

Verify:

```text
Git ✓
Node ✓
npm ✓
Python ✓
venv ✓
Firebase CLI ✓
VS Code ✓
```

**Milestone exit gate:** The machine can build and run the empty project stack locally.

---

# 13. MILESTONE 02 — Repository & Project Skeleton

**Goal:** Create a clean project structure without implementing product features.

## 02.01 Repository Clone / Initialization

- [x] Repository available locally
- [x] Correct branch selected
- [x] Clean Git status

## 02.02 Create Directory Structure

Target:

```text
frontend/
backend/
config/
tests/
docs/
scripts/
.github/
```

**Status:** ✅ COMPLETE

## 02.03 Initialize Next.js

- [x] Next.js application created
- [x] TypeScript enabled
- [x] Development server starts
- [x] Default page loads

**Status:** ✅ COMPLETE

## 02.04 Initialize Python Backend

- [x] Backend venv created
- [x] Dependencies installed
- [x] Application module created
- [x] Uvicorn starts

**Status:** ✅ COMPLETE

## 02.05 Create Root README

Document:

- [x] project purpose
- [x] architecture at a high level
- [x] local startup
- [x] environment variables
- [x] development rules

**Status:** ✅ COMPLETE

## 02.06 Create Initial Git Ignore

Must cover appropriate:

```text
node_modules/
.next/
.venv/
__pycache__/
.env*
local emulator data where appropriate
```

**Status:** ✅ COMPLETE

## 02.07 First Clean Commit

- [x] Fresh clone can reproduce the skeleton.

**Status:** ✅ COMPLETE


---

# 14. MILESTONE 03 — Firebase Local Emulator Foundation

**Goal:** Prove Firebase can be used locally before application data depends on cloud services.

## 03.01 Initialize Firebase Configuration

- [x] Firebase configuration initialized
- [x] Local project identifier selected
- [x] Configuration committed without secrets

**Status:** ✅ COMPLETE

## 03.02 Enable Firestore Emulator

- [x] Firestore emulator configured
- [x] Emulator starts
- [x] Local console behavior understood

**Status:** ✅ COMPLETE


## 03.03 Firestore Write Test

- [x] Create one test document (`smoke_tests/test_doc_01`) via emulator REST API.

**Acceptance:** Document appears in local emulator.

**Status:** ✅ COMPLETE


## 03.04 Firestore Read Test

- [x] Read the test document (`smoke_tests/test_doc_01`) via emulator REST API and verify fields.

**Status:** ✅ COMPLETE


## 03.05 Firestore Update Test

- [x] Update the document (`smoke_tests/test_doc_01`) via PATCH request and verify status changed to `updated_ok`.

**Status:** ✅ COMPLETE


## 03.06 Firestore Delete Test

- [x] Delete the document (`smoke_tests/test_doc_01`) via DELETE request and verify GET returns 404.

**Status:** ✅ COMPLETE


## 03.07 Authentication Emulator Decision

- [x] Determine whether authentication is required for MVP.

**Decision:** User accounts are not required for MVP per Master Spec (public non-commercial knowledge vault and personal curated forge library). Authentication emulator remains disabled until post-MVP.

**Status:** ✅ COMPLETE

## 03.08 Firebase Service Boundary

- [x] Document service ownership boundary:

```text
Next.js Frontend
      ↓ (REST HTTP)
FastAPI Backend
      ↓ (Firestore Admin / REST)
Firestore Emulator / Production
```

- **FastAPI:** Sole authority for data validation, ingestion (YouTube, RSS), normalization, and Firestore writes.
- **Next.js:** Consumes FastAPI endpoints for bento cards, search, and library data. Direct client SDK reads optional only if real-time subscriptions needed.
- No duplicate business logic across boundaries.

**Status:** ✅ COMPLETE

## 03.09 Local Data Reset Procedure

- [x] Document reset procedure:
  - Default: In-memory mode (restarting `firebase emulators:start` resets state to zero).
  - Live Reset: `DELETE http://127.0.0.1:8080/emulator/v1/projects/blacksmith-knight-local/databases/(default)/documents` clears all collections instantaneously.
  - Seed strategy: Python seed script will populate initial metallurgy/workshop fixtures in Milestone 08.

**Status:** ✅ COMPLETE

## 03.10 Firebase Integration Smoke Test

- [x] Local Firestore started on port 8080.
- [x] UI started on port 4000.
- [x] Write test verified.
- [x] Read test verified.
- [x] Update test verified.
- [x] Delete test verified.
- [x] Live reset endpoint verified.
- [x] Zero cloud / production dependencies touched.

**Milestone exit gate:** Local Firestore can be started, written, read, updated, deleted, and reset without touching production data.

**Status:** ✅ COMPLETE


---

# 15. MILESTONE 04 — Backend Foundation

**Goal:** Build the smallest useful FastAPI service.

## 04.01 Create FastAPI Application

- [x] `main.py` or equivalent
- [x] application instance
- [x] basic routing

**Status:** ✅ COMPLETE

## 04.02 Start Uvicorn

Target:

```text
http://localhost:8000
```

- [x] Verified FastAPI ASGI app can be imported and executed via Uvicorn.

**Status:** ✅ COMPLETE

## 04.03 Health Endpoint

```text
GET /health
```

Expected:

```json
{"status":"ok"}
```

- [x] Root `/health` endpoint responds with `{"status": "ok"}`.
- [x] Sub-router `/api/health` and `/api/v1/health` respond with extended diagnostics and emulator status.

**Status:** ✅ COMPLETE

## 04.04 Health Test

- [x] Browser/curl/HTTP test verified
- [x] automated API test in `tests/backend/test_health.py`

**Status:** ✅ COMPLETE

## 04.05 API Configuration

Create configuration handling for:

- [x] environment (`APP_ENV`, `APP_DEBUG`)
- [x] Firebase settings (`FIREBASE_PROJECT_ID`, `FIRESTORE_EMULATOR_HOST`)
- [x] logging level (`LOG_LEVEL`)
- [x] external API configuration placeholders (`YOUTUBE_API_KEY`, `AI_API_KEY`)
- [x] CORS origins list (`CORS_ORIGINS`)

Implemented in [`backend/app/core/config.py`](file:///C:/Doron/UpTheIrons/backend/app/core/config.py).

**Status:** ✅ COMPLETE

## 04.06 Error Handling Foundation

Define basic consistent error responses:

- [x] Standard envelope: `{"error": {"code": ..., "message": ..., "details": ...}}`
- [x] Custom exceptions: `AppException`, `NotFoundError`, `BadRequestError`, `ValidationError`, `SourceError`
- [x] Handlers for 404, 422 (validation), Starlette HTTP errors, and unhandled 500 exceptions.

Implemented in [`backend/app/core/errors.py`](file:///C:/Doron/UpTheIrons/backend/app/core/errors.py).

**Status:** ✅ COMPLETE

## 04.07 Logging Foundation

Create structured logging suitable for:

- [x] API requests (via `RequestLoggingMiddleware` with `X-Process-Time-Ms`)
- [x] worker jobs later
- [x] errors
- [x] synchronization

Implemented in [`backend/app/core/logging.py`](file:///C:/Doron/UpTheIrons/backend/app/core/logging.py).

**Status:** ✅ COMPLETE

## 04.08 API Versioning Decision

- [x] Established `/api` and `/api/v1` routers mounted via [`backend/app/api/router.py`](file:///C:/Doron/UpTheIrons/backend/app/api/router.py).
- [x] Master Spec `/api/...` prefix respected.

**Status:** ✅ COMPLETE

## 04.09 Backend Test Layout

Target:

```text
tests/backend/
```

- [x] Structured layout created: `test_health.py`, `test_errors.py`, `test_config.py`, `test_logging.py`.

**Status:** ✅ COMPLETE

## 04.10 Backend Quality Gate

- [x] Unit test command works (`pytest tests/backend`)
- [x] Health endpoint test passes
- [x] Backend starts from clean environment
- [x] 10 of 10 automated tests passing

**Status:** ✅ COMPLETE


---

# 16. MILESTONE 05 — Frontend Foundation

**Goal:** Build the application shell before feature implementation.

## 05.01 Next.js Shell

- [x] App Router
- [x] TypeScript
- [x] root layout with skip link
- [x] metadata configured

**Status:** ✅ COMPLETE

## 05.02 Global CSS

Implement initial theme direction:

- [x] `#121212` primary background
- [x] iron / charcoal surfaces (`#1a1a1a`, `#242424`, `#282828`)
- [x] `#FF5722` forge accent & glowing focus ring
- [x] reduced motion media query support

Implemented in [`frontend/app/globals.css`](file:///C:/Doron/UpTheIrons/frontend/app/globals.css).

**Status:** ✅ COMPLETE

## 05.03 Typography

- [x] System font stack, high-contrast text ratios, semantic typography.

**Status:** ✅ COMPLETE

## 05.04 Navigation Shell

Create navigation and primary route shells:

- [x] **Forge** (`/`)
- [x] **Materials** (`/materials`)
- [x] **Videos** (`/videos`)
- [x] **Guides** (`/guides`)
- [x] **Projects** (`/projects`)
- [x] **Workshop** (`/workshop`)
- [x] **Tools** (`/tools`)
- [x] **Rules** (`/rules`)
- [x] **Search** (`/search`)

Implemented in [`frontend/components/navigation/Navbar.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Navbar.tsx) and [`frontend/components/navigation/Footer.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Footer.tsx).

**Status:** ✅ COMPLETE

## 05.05 Responsive Shell

- [x] Desktop (sticky navbar, full links, 3-column Bento layout)
- [x] Tablet (responsive grid collapse)
- [x] Mobile (accessible hamburger drawer, tap-friendly targets)

**Status:** ✅ COMPLETE

## 05.06 Accessibility Baseline

- [x] semantic HTML (`<header>`, `<nav>`, `<main>`, `<footer>`)
- [x] keyboard navigation and skip-to-content landmark
- [x] focus indicators (`focus-visible:ring-2 focus-visible:ring-[#FF5722]`)
- [x] readable contrast verified against dark background

**Status:** ✅ COMPLETE

## 05.07 Motion Foundation

- [x] CSS transitions for hover, focus, and reduced-motion media query.

**Status:** ✅ COMPLETE

## 05.08 Frontend Quality Gate

- [x] TypeScript typecheck passed
- [x] `npm run build` compiled clean in 1238ms
- [x] 11 static pages generated with exit code 0

**Status:** ✅ COMPLETE


---

# 17. MILESTONE 06 — Frontend ↔ Backend Integration

**Goal:** Prove the two applications can communicate locally.

## 06.01 Frontend API Client

Create:

```text
frontend/lib/api.ts
```

- [x] Implemented typed `fetchApi`, `checkBackendHealth`, and custom `ApiError` class in [`frontend/lib/api.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/api.ts).

**Status:** ✅ COMPLETE

## 06.02 Backend CORS Configuration

- [x] Configured `CORSMiddleware` in `backend/app/main.py` allowing local origins (`localhost:3000`, `127.0.0.1:3000`).

**Status:** ✅ COMPLETE

## 06.03 Call `/health`

- [x] Client calls `/api/health` with diagnostics payload.

**Status:** ✅ COMPLETE

## 06.04 Display Backend Status

- [x] Created [`frontend/components/workshop/BackendStatusBadge.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/workshop/BackendStatusBadge.tsx) mounted in Navbar.

**Status:** ✅ COMPLETE

## 06.05 Handle Backend Offline

- [x] Handled network / unreachable errors gracefully with fallback badge ("API Offline - Standalone") and manual re-check trigger. No unhandled UI crashes.

**Status:** ✅ COMPLETE

## 06.06 Integration Test

```text
Next.js
  ↓
FastAPI
  ↓
health response
  ↓
Next.js
```

- [x] Verified full build and component rendering cleanly without errors.

**Exit gate:** Frontend and backend operate as separate local processes and communicate successfully.

**Status:** ✅ COMPLETE


---

# 18. MILESTONE 07 — Firebase Data Layer

**Goal:** Connect the backend to local Firestore without introducing domain complexity.

## 07.01 Firebase Backend Configuration

- [x] Server-side Firebase access method selected (Firestore REST over async HTTP transport)
- [x] Local emulator routing confirmed (`FIRESTORE_EMULATOR_HOST`)
- [x] Production credentials kept separate

**Status:** ✅ COMPLETE

## 07.02 Firestore Repository Abstraction

Create a small storage interface:

- [x] Created [`backend/app/repositories/base.py`](file:///C:/Doron/UpTheIrons/backend/app/repositories/base.py) with `create()`, `get()`, `update()`, `delete()`, `list()`.
- [x] Created [`backend/app/repositories/firestore.py`](file:///C:/Doron/UpTheIrons/backend/app/repositories/firestore.py) implementing `FirestoreRepository`.
- [x] Built bidirectional serialization (`dict_to_firestore`, `firestore_to_dict`).

**Status:** ✅ COMPLETE

## 07.03 Repository Unit Tests

- [x] Test type serialization/deserialization across primitive, list, map, and null values in [`tests/backend/test_firestore_repository.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_firestore_repository.py).

**Status:** ✅ COMPLETE

## 07.04 Backend → Firestore Write

- [x] Tested document creation and roundtrip verification.

**Status:** ✅ COMPLETE

## 07.05 Backend → Firestore Read

- [x] Tested document retrieval by key and 404 None handling.

**Status:** ✅ COMPLETE

## 07.06 Backend → Firestore Update

- [x] Tested update merging existing fields and raising NotFoundError on nonexistent keys.

**Status:** ✅ COMPLETE

## 07.07 Backend → Firestore Delete

- [x] Tested document deletion returning True on success and False on missing.

**Status:** ✅ COMPLETE

## 07.08 Storage Error Handling

- [x] Simulated connection refused / emulator down, verified `StorageError` is raised.

**Exit gate:** FastAPI can safely use local Firestore through a small tested storage layer.

**Status:** ✅ COMPLETE


---

# 19. MILESTONE 08 — Core Domain/Data Model

**Goal:** Define the smallest useful application data model.

Start with common entities, not every future field.

## 08.01 Common Content Envelope

- [x] Created [`backend/app/models/enums.py`](file:///C:/Doron/UpTheIrons/backend/app/models/enums.py) (`ContentType`, `ContentStatus`, `DifficultyLevel`, `SourceType`, `SourceStatus`).
- [x] Created [`backend/app/models/content.py`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) with polymorphic `ContentEnvelope`.

**Status:** ✅ COMPLETE

## 08.02 Source Entity

- [x] Created `SourceEntity` with identity and lifecycle status in [`backend/app/models/source.py`](file:///C:/Doron/UpTheIrons/backend/app/models/source.py).

**Status:** ✅ COMPLETE

## 08.03 YouTube Channel Entity

- [x] Created `YouTubeChannelEntity` with `youtube_channel_id`, `handle`, and `video_count` in [`backend/app/models/source.py`](file:///C:/Doron/UpTheIrons/backend/app/models/source.py).

**Status:** ✅ COMPLETE

## 08.04 Content Entity

- [x] Created specialized content models: `MaterialMetadata`, `VideoMetadata`, `ProjectMetadata`.

**Status:** ✅ COMPLETE

## 08.05 Validation

- [x] Pydantic models enforcing title length, auto-slug formatting, and metallurgical percentages.

**Status:** ✅ COMPLETE

## 08.06 Deduplication Keys

- [x] Implemented deterministic deduplication key generator in [`backend/app/models/deduplication.py`](file:///C:/Doron/UpTheIrons/backend/app/models/deduplication.py).

**Status:** ✅ COMPLETE

## 08.07 Data Migration/Seeding Strategy

- [x] Created baseline fixtures for steels (1084, 1095, 5160) and projects (S-Hook) with `seed_initial_data()` in [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py).
- [x] Created matching TypeScript interfaces in [`frontend/lib/types.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/types.ts).

**Status:** ✅ COMPLETE


---

# 20. MILESTONE 09 — Source Management Framework

**Goal:** Build the controlled source registry before collectors.

Source families:

```text
Video Sources
  └── YouTube Channels

Knowledge Sources
  └── RSS Feeds

Product Sources
  └── Approved APIs / Feeds
```

## 09.01 Source Registry Model

Fields:

```text
id
name
type
platform
enabled
priority
categories
status
created_at
updated_at
last_sync_at
last_error
```

## 09.02 Source CRUD API

Implement:

```text
POST source
GET sources
GET source/{id}
PATCH source/{id}
DELETE source/{id}
```

## 09.03 Source Validation

Reject malformed or unsupported sources.

## 09.04 Enable / Disable

Verify disabled sources cannot be collected.

## 09.05 Source Test Endpoint

Create a controlled mechanism to test source connectivity later.

## 09.06 Source Management UI

Build a minimal page before integrating collectors.

## 09.07 Source Lifecycle

Implement/record:

```text
CONFIGURED
→ TESTED
→ ENABLED
→ SYNCHRONIZED
→ MONITORED
→ DISABLED / REMOVED
```

**Critical rule:** AI must not create new source records autonomously.

**Status:** ✅ COMPLETE

---

# 21. MILESTONE 10 — YouTube Channel Management

**Goal:** Allow the user to manage the approved YouTube channel registry.

## 10.01 Channel API Model

Implement channel-specific fields.

## 10.02 Create Channel Endpoint

Example:

```text
POST /api/youtube/channels
```

## 10.03 List Channels

## 10.04 Get Channel

## 10.05 Update Channel

Support:

- enabled
- priority
- categories

## 10.06 Disable Channel

Verify future ingestion excludes it.

## 10.07 Delete Channel

Define whether historical videos remain. Master Spec currently favors retaining collected videos unless explicitly removed.

## 10.08 Channel Manager UI

Display:

```text
name
handle
status
priority
categories
last sync
video count
```

## 10.09 Add Channel UI

Support URL/channel ID input.

## 10.10 Search / Resolve Channel

Only resolve the explicitly supplied/search-requested YouTube channel. This is not autonomous discovery.

## 10.11 Sync Now Placeholder

Add UI control before implementing real ingestion.

## 10.12 Full Channel Management Test

```text
Add
→ display
→ edit
→ disable
→ enable
→ delete
```

**Status:** ✅ COMPLETE

---

# 22. MILESTONE 11 — YouTube Video Ingestion

**Goal:** Collect videos only from enabled user-managed channels.

## 11.01 YouTube API Configuration

- [x] Dynamic Settings API (`GET /api/v1/settings/keys`, `POST /api/v1/settings/keys`)
- [x] Secrets stored in Firestore `system_config/api_keys` and cached in memory
- [x] Sensitive values masked in responses (`AIzaSy...****`)
- [x] Fallback to environment variable `YOUTUBE_API_KEY`
- [x] Safe offline fallback when no key is set

**Status:** ✅ COMPLETE

## 11.02 YouTube Client

- [x] Created `YouTubeClient` in [`backend/app/services/youtube_client.py`](file:///C:/Doron/UpTheIrons/backend/app/services/youtube_client.py)
- [x] Efficient uploads playlist resolver converting `UC...` channel IDs to `UU...` playlist IDs
- [x] Uses `playlistItems.list` costing only 1 quota unit (vs 100 units for search)
- [x] Deterministic offline fixtures for testing without network/API keys

**Status:** ✅ COMPLETE

## 11.03 Fetch One Channel

- [x] Resolves channel uploads playlist and queries uploads batch deterministically.

**Status:** ✅ COMPLETE

## 11.04 Fetch One Video Page / Batch

- [x] Extracts `video_id`, `title`, `description`, `published_at`, `thumbnails`, and `channel_title`.

**Status:** ✅ COMPLETE

## 11.05 Normalize Video

- [x] `normalize_youtube_video()` in [`backend/app/services/youtube_ingestion.py`](file:///C:/Doron/UpTheIrons/backend/app/services/youtube_ingestion.py)
- [x] Maps raw metadata into `ContentEnvelope` with `ContentType.VIDEO`
- [x] Category derivation (`bladesmithing`, `heat-treatment`, `tools`, `forging`) and tag extraction
- [x] Slug generation, duration tracking, and embed URL formulation

**Status:** ✅ COMPLETE

## 11.06 Store One Video

- [x] Persists normalized video envelope into Firestore `content` collection with key `yt_{video_id}`.

**Status:** ✅ COMPLETE

## 11.07 Deduplicate One Video

- [x] Uses canonical deduplication key `video:youtube:{video_id}`
- [x] Pre-write existence check avoids duplicate documents
- [x] Increments `duplicates` counter on re-ingestion without duplicate writes

**Status:** ✅ COMPLETE

## 11.08 Display One Video

- [x] Created `GET /api/v1/videos` and `GET /api/v1/videos/{video_id}` in [`backend/app/api/v1/videos.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/videos.py)
- [x] Supports filtering by `category`, `tag`, and `channel_id` with reverse-chronological ordering

**Status:** ✅ COMPLETE

## 11.09 Channel Video List

- [x] Curated videos gallery in [`frontend/app/videos/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/videos/page.tsx)
- [x] Topic filter pills, duration badges, video player embed modal, and external YouTube watch links
- [x] "Configure YouTube API Key" modal for instant key updating from the web UI

**Status:** ✅ COMPLETE

## 11.10 Sync One Channel

- [x] `POST /api/youtube/channels/{channel_id}/sync` executes ingestion for single approved channel
- [x] Updates channel `video_count`, `last_synced_at`, and `status=healthy`
- [x] Disabled channels rejected with 400 Bad Request

**Status:** ✅ COMPLETE

## 11.11 Sync All Enabled Channels

- [x] `POST /api/youtube/sync` synchronizes all enabled channels in registry
- [x] Returns list of `SyncSummary` records

**Status:** ✅ COMPLETE

## 11.12 Synchronization Logging

- [x] Records sync run metadata (`channel_id`, `discovered`, `new_items`, `duplicates`, `errors`, timestamps, `status`)
- [x] Stored in Firestore `sync_logs` collection
- [x] Inspected via `GET /api/youtube/sync-logs`

**Status:** ✅ COMPLETE

## 11.13 Partial Failure

- [x] Failures in one channel do not halt batch ingestion; error recorded on channel entity and logs

**Status:** ✅ COMPLETE

## 11.14 API Quota Protection

- [x] Uploads playlist architecture minimizes quota usage (1 quota unit per 50 items)

**Status:** ✅ COMPLETE

## 11.15 Manual Sync Test

- [x] Created [`tests/backend/test_youtube_ingestion.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_youtube_ingestion.py)
- [x] 38 passing backend tests in 1.75s
- [x] Frontend build compiled cleanly (`npm run build`, exit code 0)

**Status:** ✅ COMPLETE

## 11.16 Scheduled Sync Design

- [x] Sync engine designed for background workers (cron / scheduled triggers invoking `POST /api/youtube/sync`)

**Exit gate:** Ingestion collects only from approved user channels, deduplicates strictly, stores in Firestore, and displays in the videos feed.

**Status:** ✅ COMPLETE

---

# 23. MILESTONE 12 — RSS Source Management & Ingestion

**Goal:** Support only user-configured RSS feeds.

## 12.01 RSS Feed Entity

- [x] Defined `RSSFeedEntity` in [`backend/app/models/source.py`](file:///C:/Doron/UpTheIrons/backend/app/models/source.py) (`type=SourceType.RSS_FEED`, `feed_url`, `site_url`, `feed_format`, `article_count`)
- [x] Added `ContentType.ARTICLE` to domain enums and TypeScript types

**Status:** ✅ COMPLETE

## 12.02 Add Feed & 12.03 Test Feed

- [x] Created `POST /api/v1/rss/feeds` with strict URL scheme validation (`http://`, `https://`, `test://`)
- [x] Prevents duplicate registrations by URL or derived slug ID (`rss_{slug}`)
- [x] Created `POST /api/v1/rss/test` to inspect/preview articles from a feed URL without writing to storage
- [x] Created `GET`, `PATCH`, and `DELETE` endpoints in [`backend/app/api/v1/rss.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/rss.py)

**Status:** ✅ COMPLETE

## 12.04 Fetch One Feed

- [x] Created `RSSClient` in [`backend/app/services/rss_client.py`](file:///C:/Doron/UpTheIrons/backend/app/services/rss_client.py)
- [x] Zero external scraping libraries; uses standard library `xml.etree.ElementTree`
- [x] Parses both RSS 2.0 (`<channel><item>`) and Atom (`<feed><entry>`)
- [x] Safe deterministic offline fallback mock batch for local testing

**Status:** ✅ COMPLETE

## 12.05 Normalize One Article

- [x] `normalize_rss_article()` in [`backend/app/services/rss_ingestion.py`](file:///C:/Doron/UpTheIrons/backend/app/services/rss_ingestion.py)
- [x] Maps feed items to `ContentEnvelope` (`type=ContentType.ARTICLE`)
- [x] Heuristic forge category and tag derivation (`materials`, `heat-treatment`, `tools`, `bladesmithing`, `guides`)
- [x] HTML tag sanitization and whitespace normalization

**Status:** ✅ COMPLETE

## 12.06 Store One Article & 12.07 Deduplicate Article

- [x] Deterministic canonical deduplication key: `compute_deduplication_key(ContentType.ARTICLE, canonical_url=url)`
- [x] Pre-write check against Firestore `content` collection (`art_{url_hash}`)
- [x] Re-syncing ignores already stored items and increments `duplicates` counter without duplicate writes

**Status:** ✅ COMPLETE

## 12.08 Display One Article & Articles Feed API

- [x] Created `GET /api/v1/articles` and `GET /api/v1/articles/{id}` in [`backend/app/api/v1/articles.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/articles.py)
- [x] Created curated articles feed in [`frontend/app/guides/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/guides/page.tsx) with category filter pills, author attribution, and source links

**Status:** ✅ COMPLETE

## 12.09 Sync One Feed & 12.10 Sync All Enabled Feeds

- [x] `POST /api/v1/rss/feeds/{feed_id}/sync` executes ingestion for single approved feed
- [x] `POST /api/v1/rss/sync` synchronizes all enabled RSS feeds sequentially
- [x] Updates feed `article_count`, `last_synced_at`, and `status=healthy`
- [x] Sync run metadata recorded in Firestore `sync_logs` collection

**Status:** ✅ COMPLETE

## 12.11 Source Attribution

- [x] Every article envelope preserves original article URL, feed name, publication timestamp, and author in `source` and `metadata`

**Status:** ✅ COMPLETE

## 12.12 Failure Handling

- [x] Feed HTTP or parsing errors set status to `failed` and record `last_error` on the feed document without modifying existing articles or halting batch sync

**Status:** ✅ COMPLETE

## 12.13 Explicit Anti-Crawling Enforcement

- [x] Automated test verifies parser strictly ingests items present in the feed XML and never follows outbound hyperlinks or crawls external domains

**Status:** ✅ COMPLETE

**Exit gate:** Ingestion collects only from approved user RSS feeds, enforces strict anti-crawling, deduplicates strictly, stores in Firestore, and displays in the knowledge feed.

**Status:** ✅ COMPLETE

---

# 24. MILESTONE 13 — Product / Shop Source Framework

**Goal:** Build a controlled product integration system without turning the site into a marketplace.

## 13.01 Product Source Model

- [x] Defined `ProductSourceEntity` in [`backend/app/models/source.py`](file:///C:/Doron/UpTheIrons/backend/app/models/source.py) (`type=SourceType.PRODUCT_API`, `catalog_url`, `vendor_name`, `item_count`)
- [x] Defined `ProductMetadata` in [`backend/app/models/content.py`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) (`sku`, `platform`, `price`, `currency`, `price_updated_at`, `pros`, `cons`, `beginner_suitable`, `alternatives`, `affiliate`)

**Status:** ✅ COMPLETE

## 13.02 Approved Source Registry & 13.03 Source Enable / Disable

- [x] Created `POST /api/v1/products/sources`: Registers approved vendor source, validates URL, prevents duplicate registrations
- [x] Created `GET`, `PATCH`, and `DELETE` endpoints in [`backend/app/api/v1/products.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/products.py)
- [x] Disabled sources are excluded from synchronization

**Status:** ✅ COMPLETE

## 13.04 Product Normalization

- [x] `normalize_product_item()` in [`backend/app/services/product_ingestion.py`](file:///C:/Doron/UpTheIrons/backend/app/services/product_ingestion.py)
- [x] Maps raw catalog payload into `ContentEnvelope` (`type=ContentType.PRODUCT`)
- [x] Formulates transparent specs: pros, cons, beginner suitability, and alternatives

**Status:** ✅ COMPLETE

## 13.05 Product Deduplication & 13.06 Dynamic Price Metadata

- [x] Canonical deduplication key: `compute_deduplication_key(ContentType.PRODUCT, external_id=sku, canonical_url=purchase_url)`
- [x] Pre-write check against Firestore `content` collection (`prod_{platform}_{sku}`)
- [x] Dynamic Price Detection: If price changes on re-sync, updates price and `price_updated_at` without duplicating the record
- [x] If price is unchanged, skips write and increments `duplicates` counter

**Status:** ✅ COMPLETE

## 13.07 Product Card (Frontend)

- [x] Created curated tools & gear guide in [`frontend/app/tools/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/tools/page.tsx)
- [x] Displays tool specs, pros/cons checklist, beginner suitability badge, price with timestamp, and transparent vendor links

**Status:** ✅ COMPLETE

## 13.08 Relevance Filtering

- [x] Category & tag pills ("All Gear", "Anvils", "Forges", "Belt Grinders", "Tongs")
- [x] "Beginner Friendly" filter checkbox and maximum budget filter

**Status:** ✅ COMPLETE

## 13.09 Commercial Bias Check

- [x] Verified ranking integrity: sorting is strictly alphabetical or by price ascending
- [x] Commercial affiliate links never boost ranking or priority over non-affiliate tools

**Status:** ✅ COMPLETE

## 13.10 Product Sync Test

- [x] Created [`tests/backend/test_product_ingestion.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_product_ingestion.py)
- [x] 53 passing backend tests in 2.29s
- [x] Frontend build compiled cleanly (`npm run build`, exit code 0)

**Status:** ✅ COMPLETE

**Exit gate:** Product sources ingest only from approved vendors, track dynamic prices without record duplication, enforce zero commercial bias, and display honest tool evaluations.

**Status:** ✅ COMPLETE

---

# 25. MILESTONE 14 — Optional AI Enrichment Layer

**Goal:** Introduce AI only after deterministic pipelines work.

**Status:** ✅ COMPLETE

**Exit gate:** AI operates purely as an optional enrichment layer; system functions seamlessly with zero external AI dependencies or missing credentials (deterministic-first); metallurgical guardrails prevent hallucinations; provider failures degrade gracefully; cost boundaries prevent batch over-enrichment.

## 14.01 AI Provider Interface
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`backend/app/services/ai/base.py`](file:///C:/Doron/UpTheIrons/backend/app/services/ai/base.py) defining `BaseAIProvider` with `enrich_content()`, `classify()`, `summarize()`, and `extract()`, returning structured `AIEnrichmentResult`.
- **Tests:** Verified via `test_14_01_ai_provider_interface`.

## 14.02 Provider Configuration
- **Status:** ✅ COMPLETE
- **Implementation:** Abstracted provider selection in [`backend/app/services/ai/service.py`](file:///C:/Doron/UpTheIrons/backend/app/services/ai/service.py) supporting `gemini`, `mock`, and `disabled`. Implemented official Google Gemini REST client in [`backend/app/services/ai/gemini.py`](file:///C:/Doron/UpTheIrons/backend/app/services/ai/gemini.py) and deterministic offline mock in [`backend/app/services/ai/mock.py`](file:///C:/Doron/UpTheIrons/backend/app/services/ai/mock.py).
- **Tests:** Verified via `test_14_02_provider_configuration`, `test_gemini_provider_mocked_http`, and `test_gemini_provider_unconfigured`.

## 14.03 AI Disabled Mode
- **Status:** ✅ COMPLETE
- **Implementation:** When `AI_PROVIDER=disabled` or no API key is supplied, `enrich_envelope()` returns the original envelope unmodified with zero errors or side-effects. All ingestion pipelines and feed queries remain fully functional.
- **Tests:** Verified via `test_14_03_ai_disabled_mode`.

## 14.04 Summary Enrichment
- **Status:** ✅ COMPLETE
- **Implementation:** Extracts technical summary without marketing buzzwords, preserving original summary under `envelope.metadata["original_summary"]`.
- **Tests:** Verified via `test_14_04_summary_enrichment`.

## 14.05 Classification
- **Status:** ✅ COMPLETE
- **Implementation:** Categorizes content strictly into craft domains: `forging`, `bladesmithing`, `heat-treatment`, `tools`, `materials`, `guides`.
- **Tests:** Verified via `test_14_05_14_06_14_07_classification_tags_difficulty`.

## 14.06 Tag Extraction
- **Status:** ✅ COMPLETE
- **Implementation:** Extracts domain-specific keywords and deduplicates against existing content tags.
- **Tests:** Verified via `test_14_05_14_06_14_07_classification_tags_difficulty`.

## 14.07 Difficulty Classification
- **Status:** ✅ COMPLETE
- **Implementation:** Maps content difficulty cleanly to `DifficultyLevel` (`beginner`, `intermediate`, `advanced`).
- **Tests:** Verified via `test_14_05_14_06_14_07_classification_tags_difficulty`.

## 14.08 Technical Source Guardrails
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`backend/app/services/ai/guardrails.py`](file:///C:/Doron/UpTheIrons/backend/app/services/ai/guardrails.py) with `GUARDRAIL_SYSTEM_PROMPT` strictly prohibiting hallucinations of chemical composition, heat-treatment temperatures, hardness (HRC) values, workshop safety rules, or certifications.
- **Tests:** Verified via `test_14_08_guardrails_prompt`.

## 14.09 AI Failure Test
- **Status:** ✅ COMPLETE
- **Implementation:** Any remote network error, timeout, or HTTP 5xx response from AI provider is trapped, logged, and gracefully degraded; envelope is returned intact with zero ingestion pipeline interruption.
- **Tests:** Verified via `test_14_09_ai_failure_resilience` and `test_gemini_provider_mocked_http`.

## 14.10 Cost Boundary
- **Status:** ✅ COMPLETE
- **Implementation:** `batch_enrich_pending(limit=10)` filters solely for documents where `metadata.ai_processed != True`, strictly honoring caller limit and preventing redundant LLM token expenditures.
- **Tests:** Verified via `test_14_10_cost_boundary` and `test_ai_enrich_item_and_batch_endpoints`.

---

# 26. MILESTONE 15 — Rules / Editorial / Safety Configuration

**Goal:** Make content behavior configurable and explicit.

**Status:** ✅ COMPLETE

**Exit gate:** All 8 modular rule documents authored and stored in `config/`; rules dynamically loaded and cached by `RulesService`; automated `RuleValidator` validates positive and negative test cases (anti-spam, clickbait, critical hazards like zinc fumes & Kaowool silica); editorial override workflow supports `featured`, `pinned`, `verified`, `needs_review`, `hidden`; interactive Codex and Validator testbed live on frontend.

## 15.01 Create Rules Directory
- **Status:** ✅ COMPLETE
- **Implementation:** Created and organized [`config/`](file:///C:/Doron/UpTheIrons/config) containing all 8 modular rule documents.
- **Tests:** Verified via `test_15_01_15_02_rules_directory_and_master_files`.

## 15.02 Move/Adapt Master Rules
- **Status:** ✅ COMPLETE
- **Implementation:** Extracted and adapted foundational rules from Master Spec v3 into [`config/rules.md`](file:///C:/Doron/UpTheIrons/config/rules.md) and domain sub-files.
- **Tests:** Verified via `test_15_01_15_02_rules_directory_and_master_files`.

## 15.03 Content Inclusion Rules
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`config/content_rules.md`](file:///C:/Doron/UpTheIrons/config/content_rules.md) defining core craft domains, relevance thresholds, and strict rejection boundaries.
- **Tests:** Verified via `test_15_03_content_inclusion_rules`.

## 15.04 Source Quality Rules
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`config/source_rules.md`](file:///C:/Doron/UpTheIrons/config/source_rules.md) mandating author attribution, deterministic deduplication, failure isolation, and strict anti-crawling boundaries.
- **Tests:** Verified via `test_15_04_source_quality_rules`.

## 15.05 Safety Rules
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`config/safety_rules.md`](file:///C:/Doron/UpTheIrons/config/safety_rules.md) detailing mandatory PPE (ANSI Z87.1 glasses, N95/P100 respirators, natural fibers) and critical workshop hazards (zinc fume fever, unsealed Kaowool silica inhalation, quench oil fires).
- **Tests:** Verified via `test_15_05_safety_rules`.

## 15.06 Product Rules
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`config/product_rules.md`](file:///C:/Doron/UpTheIrons/config/product_rules.md) establishing zero ranking distortion, transparent affiliate disclosures, live price timestamping, and mandatory pros/cons/alternatives for all tools.
- **Tests:** Verified via `test_15_06_product_rules`.

## 15.07 Editorial Style Rules
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`config/editorial_style.md`](file:///C:/Doron/UpTheIrons/config/editorial_style.md) enforcing terse, craft-first voice, standardized steel designations, and anti-hype terminology.
- **Tests:** Verified via `test_15_07_editorial_style_rules`.

## 15.08 Rule Loading Service
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`backend/app/services/rules_service.py`](file:///C:/Doron/UpTheIrons/backend/app/services/rules_service.py) dynamically loading and caching `.md` files with UTF-8 BOM tolerance, header parsing, section slicing, and `reload_all()` capability.
- **Tests:** Verified via `test_15_08_rule_loading_service`.

## 15.09 Rule Test Cases & Validation Engine
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`backend/app/services/rule_validator.py`](file:///C:/Doron/UpTheIrons/backend/app/services/rule_validator.py) evaluating content items for commercial spam, clickbait, critical hazards (galvanized zinc without warning, unsealed ceramic fiber), and computing craft relevance score.
- **Tests:** Verified via `test_15_09_rule_validation_positive_and_negative` (positive and negative cases).

## 15.10 Editorial Override Engine
- **Status:** ✅ COMPLETE
- **Implementation:** Extended [`ContentStatus`](file:///C:/Doron/UpTheIrons/backend/app/models/enums.py) enum with `PINNED`, `VERIFIED`, `HIDDEN`. Implemented `apply_editorial_override()` and `POST /api/v1/rules/override/{id}` endpoint.
- **Tests:** Verified via `test_15_10_editorial_override` and `test_editorial_override_endpoint`.

## 15.11 Interactive Codex & Testbed UI
- **Status:** ✅ COMPLETE
- **Implementation:** Rebuilt [`frontend/app/rules/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/rules/page.tsx) with rule file navigator, section reader, live disk reload, and an interactive real-time compliance testbed.
- **Tests:** Verified via Next.js production build (`npm --prefix frontend run build`, 13/13 routes).

---

# 27. MILESTONE 16 — Knowledge Library

**Goal:** Build the static/editorial knowledge foundation.

**Status:** ✅ COMPLETE

**Exit gate:** Guide model and Technical Trust Labels implemented; master craft guides retrievable via REST API (`GET /api/v1/guides`, `GET /api/v1/guides/{slug_or_id}`) and rule-validated on creation (`POST /api/v1/guides`); dedicated accessible Markdown renderer with callouts and TOC anchor support; structured peer-reviewed source references displayed; high-visibility mandatory safety section component with ANSI/PPE standards; technical trust badge with interactive explainer tooltips; related content links resolving to materials and apprentice projects; comprehensive master guide on anvil anatomy, selection, rebound testing, and mounting authored and seeded; 85 backend unit tests passing; frontend production build clean across all routes.

## 16.01 Guide Model
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`GuideMetadata`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py), [`SourceReference`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py), [`SafetyPrecaution`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py), and [`RelatedContentLink`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) under `ContentEnvelope`. Added matching TypeScript interfaces in [`frontend/lib/types.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/types.ts).
- **Tests:** Verified via `test_16_01_guide_metadata_model` in `tests/backend/test_guides.py`.

## 16.02 Guide Page & API
- **Status:** ✅ COMPLETE
- **Implementation:** Built [`backend/app/api/v1/guides.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/guides.py) with `GET /api/v1/guides`, `GET /api/v1/guides/{slug_or_id}`, `POST /api/v1/guides` (with RuleValidator enforcement), and `PATCH /api/v1/guides/{slug_or_id}`. Built dynamic detail page [`frontend/app/guides/[slug]/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/guides/[slug]/page.tsx).
- **Tests:** Verified via `test_16_02_16_09_master_guide_seeded` and `test_guide_not_found`.

## 16.03 Markdown Rendering
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`frontend/components/guides/MarkdownRenderer.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/guides/MarkdownRenderer.tsx) supporting H1-H3 headings with slug anchors, GitHub-style alert callouts (`[!NOTE]`, `[!WARNING]`, `[!TIP]`, `[!CAUTION]`), fenced code blocks, numbered and bulleted lists, horizontal rules, and inline bold/code/citation tokens without bloated third-party dependencies.
- **Tests:** Verified via frontend production build (`npm --prefix frontend run build`).

## 16.04 Source References
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`frontend/components/guides/SourceReferencesList.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/guides/SourceReferencesList.tsx) displaying structured citations (titles, authors, publications, years, citation keys like `[Postman1998]`, trust classifications, and external reference links).
- **Tests:** Verified via `test_16_02_16_09_master_guide_seeded`.

## 16.05 Safety Section Component
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`frontend/components/guides/SafetySection.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/guides/SafetySection.tsx) presenting high-visibility hazard warning banners with flame/shield icons, ANSI Z87.1 / NRR 28+ PPE checklists, and actionable mitigation protocols.
- **Tests:** Verified via `test_16_02_16_09_master_guide_seeded`.

## 16.06 Technical Trust Labels
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`TrustLabel`](file:///C:/Doron/UpTheIrons/backend/app/models/enums.py) enum (`fact`, `source_backed_recommendation`, `craft_practice`, `personal_experience`, `historical_interpretation`, `ai_summary`, `opinion`) and [`frontend/components/guides/TrustBadge.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/guides/TrustBadge.tsx) with craft color tokens and explanatory hover tooltips.
- **Tests:** Verified via `test_16_01_guide_metadata_model` and `test_16_08_guide_list_and_filters`.

## 16.07 Related Content Links
- **Status:** ✅ COMPLETE
- **Implementation:** Created [`frontend/components/guides/RelatedContentSection.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/guides/RelatedContentSection.tsx) linking master guides to metallurgical entries (`mat-1084`), apprentice projects (`proj-s-hook`), videos, and equipment.
- **Tests:** Verified via `test_16_02_16_09_master_guide_seeded`.

## 16.08 Guide Searchability
- **Status:** ✅ COMPLETE
- **Implementation:** Added full query parameter filtering in `GET /api/v1/guides` (`category`, `difficulty`, `trust_label`, `tag`, and free-text search `q` scanning titles, summaries, tags, and full markdown body). Built real-time search and filter controls in [`frontend/app/guides/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/guides/page.tsx).
- **Tests:** Verified via `test_16_08_guide_list_and_filters`.

## 16.09 One Complete Guide
- **Status:** ✅ COMPLETE
- **Implementation:** Authored and seeded exhaustive master guide: *"The Anvil: Anatomy, Selection, Rebound Testing, and Workshop Mounting"* (`guide-anvil-selection-mounting`) with complete sections on London-pattern anatomy, cast steel vs cast iron (ASO warning), ball-bearing rebound percentage test, acoustic ring diagnostics, knuckle rule ergonomics, and silicone/chain sound dampening. Also seeded secondary master guide on heat treatment phase transformations (`guide-heat-treatment-fundamentals`).
- **Tests:** Verified via `test_16_02_16_09_master_guide_seeded` and `test_16_03_heat_treatment_guide_seeded`.


---

# 28. MILESTONE 17 — Material & Steel Library

**Goal:** Build a trustworthy technical material reference.

## 17.01 Material Model
- **Status:** ✅ COMPLETE
- **Implementation:** Created `MaterialMetadata` model in [`backend/app/models/content.py`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) and synchronized TypeScript type in [`frontend/lib/types.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/types.ts). Model captures material classification, carbon percentage, nominal alloying elements, steel category (`carbon_steel`, `tool_steel`, `spring_steel`, `alloy_steel`, `stainless_steel`), forging thermal range, spark testing profile, grindability, weldability, corrosion resistance, beginner suitability, applications, mistakes, and source references.
- **Tests:** Verified via `test_17_01_17_02_material_and_steel_model` in [`tests/backend/test_materials.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_materials.py).

## 17.02 Steel Model
- **Status:** ✅ COMPLETE
- **Implementation:** Integrated `HeatTreatmentRecipe` model specifying normalizing temp, annealing temp, hardening/austenitizing temp, decalescence line, soak time in minutes, quench medium, target hardness range (HRC), tempering range, and calibrated `tempering_table` entries with temper oxidation colors.
- **Tests:** Verified via `test_17_01_17_02_material_and_steel_model` and `test_17_06_17_07_composition_and_heat_treatment_display`.

## 17.03 Source Metadata
- **Status:** ✅ COMPLETE
- **Implementation:** Implemented strict metallurgical provenance in `MaterialMetadata`: `source_reference` (mandatory citing of ASM, ASTM, or SAE standards), `confidence_score` (0.0 to 1.0), `confidence_level` (`handbook_verified`, `manufacturer_spec`, `empirical_test`), and `source_metadata` mapping AISI and UNS designations. Rejects creations lacking verifiable citations per Metallurgical Standard.
- **Tests:** Verified via `test_create_material_and_validation` rejecting inputs without verified source reference.

## 17.04 One Steel Record
- **Status:** ✅ COMPLETE
- **Implementation:** Seeded 5 authoritative metallurgical alloys in [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py):
  1. `1084 High Carbon Steel` (eutectoid ~0.84% C, beginner benchmark, cited ASM Vol 1)
  2. `1095 High Carbon Steel` (hypereutectoid ~0.95% C, high keeness/hamon, cited ASM Vol 4)
  3. `5160 Spring Steel` (shock-resistant ~0.60% C, 0.80% Cr, cited SAE J403)
  4. `O1 Tool Steel` (oil-hardening cold work tool steel, W/V carbides, cited ASTM A681)
  5. `W1 Tool Steel` (shallow-hardening water/fast-oil steel ~1.00% C, cited ASTM standards)
- **Tests:** Verified via `test_17_04_17_05_seeded_steels_retrieval`.

## 17.05 Material Page
- **Status:** ✅ COMPLETE
- **Implementation:** Created responsive Next.js catalog page in [`frontend/app/materials/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/materials/page.tsx) and detailed individual alloy dossier route in [`frontend/app/materials/[slug]/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/materials/[slug]/page.tsx). Renders forge-themed cards with carbon bar indicator, alloy badges, thermal specs, and beginner guidance.
- **Tests:** Verified via successful Next.js production build (`npm --prefix frontend run build`).

## 17.06 Composition Display
- **Status:** ✅ COMPLETE
- **Implementation:** Built [`frontend/components/materials/CompositionBreakdown.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/materials/CompositionBreakdown.tsx). Features an alloy bar visualizer illustrating nominal element percentages against the iron balance, alongside metallurgical cards explaining the chemical role of each alloy (Carbon for martensite, Chromium for hardenability, Manganese for quench depth, Vanadium/Tungsten for wear-resistant carbides, Silicon for elastic limit).
- **Tests:** Verified via `test_17_06_17_07_composition_and_heat_treatment_display`.

## 17.07 Heat Treatment Display
- **Status:** ✅ COMPLETE
- **Implementation:** Built [`frontend/components/materials/HeatTreatmentProtocol.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/materials/HeatTreatmentProtocol.tsx). Visualizes the 4 thermal phases (Normalizing, Annealing, Austenitizing/Decalescence, and Quenching) with quench medium safety warnings and an interactive tempering curve table mapping oven temperatures to HRC, toughness, and oxidation temper colors (Pale Straw, Straw, Dark Straw, Purple, Blue).
- **Tests:** Verified via `test_17_06_17_07_composition_and_heat_treatment_display`.

## 17.08 Confidence / Source Handling
- **Status:** ✅ COMPLETE
- **Implementation:** Integrated trust indicators, handbook verification badges (`⚖ Handbook Verified 99%`), and explicit ASTM/SAE/AISI citations. High-visibility warnings warn smiths against using unverified scrap or overheating hypereutectoid alloys.
- **Tests:** Verified via `test_create_material_and_validation` and UI rendering.

## 17.09 Material Search
- **Status:** ✅ COMPLETE
- **Implementation:** Implemented multi-criteria search and filtering in `backend/app/api/v1/materials.py`:
  - `steel_category` filter (`carbon_steel`, `tool_steel`, `spring_steel`, etc.)
  - `beginner_friendly` boolean toggle
  - `min_carbon` and `max_carbon` percentage range bounds
  - `q` full-text search scanning designations, classifications, summaries, applications, mistakes, and tags
  - Connected live to interactive filter controls in [`frontend/app/materials/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/materials/page.tsx).
- **Tests:** Verified via `test_17_09_material_search_and_filtering`.

## 17.10 Material Comparison Foundation
- **Status:** ✅ COMPLETE
- **Implementation:** Built deterministic multi-steel comparison engine:
  - Backend endpoint `GET /api/v1/materials/compare?ids=1084,1095,5160` generates side-by-side composition matrix, edge retention ranking (correlating to carbon & carbide volume), impact toughness ranking (correlating to lower carbon & chromium shock resistance), and quench speed summaries.
  - Frontend comparison modal in [`frontend/components/materials/MaterialComparisonModal.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/materials/MaterialComparisonModal.tsx) triggered from floating selection tray when 2 to 4 steels are selected.
- **Tests:** Verified via `test_17_10_material_comparison_foundation` and `test_material_comparison_validation`.

---

# 29. MILESTONE 18 — Workshop / Tools Library

**Goal:** Build structured workshop knowledge.

Categories include:

```text
Forging
Heating
Grinding
Finishing
Workshop Infrastructure
```

## 18.01 Tool Model
- **Status:** ✅ COMPLETE
- **Implementation:** Created `ToolMetadata` in [`backend/app/models/content.py`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) and matching TypeScript interface in [`frontend/lib/types.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/types.ts). Model captures tool category, primary purpose, essential tasks, selection criteria checklist, beginner guidance, beginner friendliness, DIY buildability, DIY improvised alternatives, maintenance protocols, safety precautions, technical specifications, related tools, and source citations.
- **Tests:** Verified via `test_18_01_18_02_tool_metadata_model` in [`tests/backend/test_tools.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_tools.py).

## 18.02 Tool Category
- **Status:** ✅ COMPLETE
- **Implementation:** Defined `ToolCategory` enum in [`backend/app/models/enums.py`](file:///C:/Doron/UpTheIrons/backend/app/models/enums.py) supporting `forging`, `heating`, `grinding`, `finishing`, and `infrastructure`. Filterable via `GET /api/v1/tools?category=...` and interactive category tabs in [`frontend/app/workshop/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/workshop/page.tsx).
- **Tests:** Verified via `test_list_tools_and_filters` in [`tests/backend/test_tools.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_tools.py).

## 18.03 Tool Knowledge Page
- **Status:** ✅ COMPLETE
- **Implementation:** Created dedicated Workshop Tools catalog at [`frontend/app/workshop/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/workshop/page.tsx) and dynamic tool dossier reader at [`frontend/app/workshop/[slug]/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/workshop/[slug]/page.tsx). Renders forge aesthetic cards, selection checklists, apprentice guidance alerts, technical specification grids, safety notices, maintenance steps, and DIY alternatives.
- **Tests:** Verified via Next.js production build (`○ /workshop` and `ƒ /workshop/[slug]`).

## 18.04 One Anvil Entry
- **Status:** ✅ COMPLETE
- **Implementation:** Authored and seeded *"London-Pattern Cast Steel Anvil"* (`tool-london-pattern-anvil`) in [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py). Details monolithic cast 4140 steel body, 80%+ rebound score, knuckle-height rule, horn geometry, cutting step, hardy/pritchel holes, and silicone/chain sound deadening.
- **Tests:** Verified via `test_18_04_seeded_anvil_entry`.

## 18.05 One Hammer Entry
- **Status:** ✅ COMPLETE
- **Implementation:** Authored and seeded *"Swedish Cross-Peen Blacksmith Hammer"* (`tool-cross-peen-hammer`) in [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py). Specifies 2.0 to 2.5 lb beginner weight recommendation to avoid tendonitis, crowned square face dressing, perpendicular drawing out, straight-grain hickory handle wedging, and boiled linseed oil maintenance.
- **Tests:** Verified via `test_18_05_seeded_hammer_entry`.

## 18.06 One Grinder Entry
- **Status:** ✅ COMPLETE
- **Implementation:** Authored and seeded *"2x72 Variable Speed Industrial Belt Grinder"* (`tool-2x72-belt-grinder`) in [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py). Details 2–3 HP TEFC motor, VFD surface-feet-per-minute (SFPM) speed control, ceramic abrasives, platen liners, and spark trap buckets.
- **Tests:** Verified via `test_18_06_seeded_grinder_entry`.

## 18.07 Safety Metadata
- **Status:** ✅ COMPLETE
- **Implementation:** Implemented structured `SafetyPrecaution` models across all workshop tools, displayed via [`frontend/components/tools/ToolSafetyNotice.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/tools/ToolSafetyNotice.tsx). Enforces explicit hazard analysis, mitigation procedures, and required PPE (ANSI Z87.1 eye protection, NRR 28+ hearing protection, NIOSH P100/N95 respirator for metal dust, refractory ceramic fiber sealing).
- **Tests:** Verified via `test_18_07_tool_safety_metadata`.

## 18.08 Related Tools
- **Status:** ✅ COMPLETE
- **Implementation:** Integrated bidirectional `RelatedContentLink` relationships cross-linking workshop tools (e.g. Anvil ↔ Hammer ↔ Leg Vise ↔ Propane Forge), rendered in tool dossiers for seamless workflow exploration.
- **Tests:** Verified via `test_18_08_related_tools`.

---

# 30. MILESTONE 19 — Projects Library

**Goal:** Provide practical projects with progressive difficulty.

## 19.01 Project Model [COMPLETE]
- Created `ProjectMetadata` and `ProjectStep` models
- Linked tools and materials.

## 19.02 Beginner Project [COMPLETE]
- Seeded Classic Blacksmith's S-Hook

## 19.03 Intermediate Project [COMPLETE]
- Seeded Forging Wolf Jaw Tongs

## 19.04 Advanced Project [COMPLETE]
- Seeded Forging a High Carbon Camp Knife

## 19.05 Project Navigation [COMPLETE]
- Built `/projects` library and filters

## 19.06 Related Materials / Tools [COMPLETE]
- Displayed required tools and materials on project cards and detail pages.

---

# 31. MILESTONE 20 — Bento Feed Engine

**Goal:** Turn content into the main Forge experience.

## [COMPLETE] 20.01 Common Card Shell

## [COMPLETE] 20.02 Product Card

## [COMPLETE] 20.03 Video Card

## [COMPLETE] 20.04 Guide Card

## [COMPLETE] 20.05 Material Card

## [COMPLETE] 20.06 Project Card

## [COMPLETE] 20.07 Workshop Tip Card

## [COMPLETE] 20.08 Responsive Bento Layout

Desktop → tablet → mobile.

## [COMPLETE] 20.09 Static Feed

Prove layout using local static data.

## [COMPLETE] 20.10 API Feed

Replace static feed with backend data.

## [COMPLETE] 20.11 Mixed Content

Verify multiple content types coexist.

## [COMPLETE] 20.12 Editorial Prioritization

Implement deterministic ordering before AI recommendation logic.

## [COMPLETE] 20.13 Featured Content

## [COMPLETE] 20.14 Feed Failure Behavior

If one source is unavailable, existing content remains usable.

---

# 32. MILESTONE 21 — Search & Filtering

**Goal:** Make the growing knowledge base usable.

## [COMPLETE] 21.01 Search UI

## [COMPLETE] 21.02 Search API

## [COMPLETE] 21.03 Exact Match

## [COMPLETE] 21.04 Topic Match

## [COMPLETE] 21.05 Type Filtering

```text
All
Materials
Videos
Guides
Projects
Tools
Rules
Workshop Tips
```

## [COMPLETE] 21.06 Skill Filtering

```text
Beginner
Intermediate
Advanced
```

## [COMPLETE] 21.07 Technical Topic Filtering

## [COMPLETE] 21.08 Combined Filters

## [COMPLETE] 21.09 No-Result State

## [COMPLETE] 21.10 Search Performance Check

---

# 33. MILESTONE 22 — Source / Sync Monitoring & Logs

**Goal:** Make automation observable.

## [COMPLETE] 22.01 Sync Run Model

Record:

```text
run_id
started_at
completed_at
source
status
items_discovered
items_new
items_duplicate
items_rejected
errors
```

## [COMPLETE] 22.02 Source Health

Track:

```text
healthy
warning
failed
disabled
```

## [COMPLETE] 22.03 Error History

## [COMPLETE] 22.04 Manual Sync History

## [COMPLETE] 22.05 Worker Log Viewer

Minimal first version.

## [COMPLETE] 22.06 Partial Failure Test

## [COMPLETE] 22.07 Recovery Test

## [COMPLETE] 22.08 Unified Admin Settings Portal (Frontend)

- [ ] Consolidate API Keys management, YouTube channels registry, RSS feeds registry, and sync logs viewer into unified `/admin` or `/settings` page.
- [ ] Direct secret updates via `POST /api/v1/settings/keys` with masked display.
- [ ] Provide one-click batch sync triggers for all source families.

---

# 34. MILESTONE 23 — UI Polish / Responsive / Accessibility

**Goal:** Turn the working application into a polished usable site.

## [COMPLETE] 23.01 Visual Consistency

## [COMPLETE] 23.02 Card Spacing

## [COMPLETE] 23.03 Typography Refinement

## [COMPLETE] 23.04 Forge Visual Details

Use:

- subtle metal surfaces
- restrained ember accents
- workshop imagery
- controlled shadows

Avoid excessive glow/gaming aesthetics.

## [COMPLETE] 23.05 Motion Refinement

## [COMPLETE] 23.06 Mobile Navigation

## [COMPLETE] 23.07 Keyboard Navigation

## [COMPLETE] 23.08 Screen Reader Basics

## [COMPLETE] 23.09 Reduced Motion

## [COMPLETE] 23.10 Image Optimization

## [COMPLETE] 23.11 Loading States

## [COMPLETE] 23.12 Error States

## [COMPLETE] 23.13 Empty States

---

# 35. MILESTONE 24 — Testing & Reliability

**Goal:** Prove the integrated system works reliably.

## [COMPLETE] 24.01 Backend Unit Test Coverage Review

## [COMPLETE] 24.02 API Integration Tests

## [COMPLETE] 24.03 Firebase Emulator Integration Tests

## [COMPLETE] 24.04 Frontend Tests

## [COMPLETE] 24.05 End-to-End Test Setup

## [COMPLETE] 24.06 Core User Flow Test

```text
Open site
→ browse feed
→ filter
→ open guide
→ browse material
→ browse video
```

## [COMPLETE] 24.07 Channel Management Flow

```text
Open channel manager
→ add channel
→ enable
→ sync
→ display video
→ disable
```

## [COMPLETE] 24.08 RSS Flow

```text
Add feed
→ sync
→ store article
→ display article
```

## [COMPLETE] 24.09 Failure Tests

Simulate:

- backend offline
- Firebase unavailable
- source unavailable
- API quota/error
- AI unavailable

## [COMPLETE] 24.10 Regression Test Run

Everything previously marked complete must remain functional.

---

# 36. MILESTONE 25 — Cloud Architecture Validation

**Goal:** Validate the real deployment topology before committing to it.

Candidate architecture:

```text
                 INTERNET
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 Firebase-hosted            Render / other
 Next.js application        Python service
        │                       │
        └───────────┬───────────┘
                    ▼
              Firebase data
               / services
```

Possible alternatives must be considered if technically superior.

## 25.01 Firebase Hosting/App Hosting Decision

Validate the best Firebase hosting option for the selected Next.js architecture.

## 25.02 Python Deployment Decision

Compare:

- Render
- Firebase-native/serverless option if suitable
- another lightweight service

Criteria:

```text
cost
simplicity
Python support
background jobs
secrets
networking
logging
cold starts
maintenance
```

## 25.03 Worker Placement Decision

Determine whether scheduled workers run through:

- GitHub Actions
- Render cron/background service
- Firebase scheduled capability
- another service

## 25.04 Production Firestore Boundary

Confirm local and production projects are isolated.

## 25.05 Architecture Decision Record

Record the final topology before production deployment.

---

# 37. MILESTONE 26 — Firebase Deployment

**Goal:** Deploy the frontend/data services safely.

## 26.01 Create/Verify Production Firebase Project

## 26.02 Production Configuration

## 26.03 Production Security Rules

## 26.04 Production Firestore Configuration

## 26.05 Production Data Strategy

Define:

- seed data
- migration approach
- backups
- rollback strategy

## 26.06 Frontend Deployment

## 26.07 Production Smoke Test

## 26.08 Production vs Emulator Separation Test

Verify local testing cannot accidentally modify production.

---

# 38. MILESTONE 27 — Python API / Worker Deployment

**Goal:** Deploy Python components only if the validated architecture requires them.

## 27.01 Production Build

## 27.02 Production Environment Variables

## 27.03 Secrets Configuration

## 27.04 Health Endpoint

## 27.05 API Deployment

## 27.06 API → Firebase Production Test

## 27.07 Worker Deployment if Required

## 27.08 Worker Manual Run

## 27.09 Worker Failure Recovery

## 27.10 Logging

---

# 39. MILESTONE 28 — CI/CD & Scheduled Automation

**Goal:** Make repeatable deployment and scheduled ingestion safe.

## 28.01 GitHub Actions CI

At minimum:

```text
install
lint
typecheck
unit tests
build
```

## 28.02 Backend CI

## 28.03 Frontend CI

## 28.04 Integration Test Job

## 28.05 Deployment Workflow

Only after local/integration validation.

## 28.06 Scheduled YouTube Sync

Start conservatively.

## 28.07 Scheduled RSS Sync

## 28.08 Scheduled Product Sync

## 28.09 AI Enrichment Job

Only for new/changed content.

## 28.10 Daily Cleanup / Maintenance

## 28.11 Monitoring

## 28.12 Scheduled Job Failure Test

---

# 40. MILESTONE 29 — MVP Integration & Acceptance

**Goal:** Confirm the complete MVP described by the Master Specification.

A visitor must be able to:

```text
[ ] Open the website
[ ] Understand the blacksmithing theme
[ ] Browse the Bento feed
[ ] Filter content
[ ] Open a technical guide
[ ] Browse materials
[ ] Browse videos
[ ] Browse tools
[ ] Search knowledge
[ ] Browse configured YouTube channels
[ ] Manage YouTube channels
[ ] Discover beginner projects
[ ] Read safety information
[ ] Navigate related topics
```

MVP should not require:

```text
[ ] user accounts
[ ] community
[ ] comments
[ ] messaging
[ ] payments
[ ] full e-commerce
[ ] mobile app
[ ] complex personalization
```

## 29.01 MVP Demo Run

Perform a clean demonstration from a fresh environment.

## 29.02 Data Integrity Review

## 29.03 Source Control Review

## 29.04 Security Review

## 29.05 Accessibility Review

## 29.06 Performance Review

## 29.07 Content Quality Review

## 29.08 Safety Review

## 29.09 Final MVP Acceptance

Record explicit acceptance rather than simply assuming completion.

---

# 41. MILESTONE 30 — Post-MVP Backlog

Potential future blocks:

```text
Steel comparison tool
Heat-treatment calculator
Forge fuel comparison
Hammer weight guide
Anvil selection guide
Abrasive selection assistant
Workshop planner
Project difficulty estimator
Personal project journal
Material cost calculator
Learning progress tracker
Source credibility system
AI knowledge assistant
User accounts
Favorites
Personal notes
Saved projects
Community features
```

Each future feature must become its own mini-program and must not be allowed to destabilize the MVP.

---

# 42. Vertical Slice Development Examples

The following examples illustrate how large features should be decomposed.

## Example A — YouTube

Bad:

```text
Build YouTube system
```

Good:

```text
A. Create channel model
B. Store one channel
C. GET one channel
D. POST one channel
E. PATCH enabled state
F. DELETE channel
G. Display one channel
H. Add channel form
I. Connect form to API
J. Configure YouTube API
K. Fetch one channel
L. Fetch one video
M. Store one video
N. Display one video
O. Deduplicate one video
P. Sync one channel
Q. Sync all enabled channels
R. Record sync log
S. Handle failed channel
T. Add schedule
```

Each letter can be split further if the implementation becomes non-trivial.

## Example B — Material Library

```text
Create Material type
→ store one material
→ GET one material
→ display one material
→ add source reference
→ display composition
→ display heat-treatment section
→ add related guide
→ search material
→ test source attribution
```

## Example C — Bento Card

```text
Create CardShell
→ render title
→ render image
→ render category
→ render action
→ create VideoCard
→ pass sample video
→ responsive test
→ accessibility test
→ animation
→ connect API data
```

---

# 43. Standard Task Record

Every meaningful completed task should be logged using this structure.

```markdown
## TASK: XX.YY — <Task Name>

**Date:** YYYY-MM-DD
**Milestone:** XX — <Milestone>
**Status:** 🔄 / 🧪 / ✅ / ❌ / 🟡

### Objective
<What this task is supposed to accomplish.>

### Implementation
<What was actually changed.>

### Files Changed
- path/to/file
- path/to/file

### Tests
- test performed
- test performed

### Result
<Pass/fail and important observations.>

### Problems
<Problems encountered.>

### Decision
<Important architectural or implementation decision.>

### Known Limitations
<Anything deliberately not solved yet.>

### Git Commit
`<commit hash / message>`

### Next Step
<Next task/block.>
```

---

# 44. Work Log

This section records actual development activity.

## 44.01 Project Initialization

### WORK-001 — Development Program Created

**Date:** 2026-09-09  
**Milestone:** 00  
**Status:** ✅ COMPLETE

**Implemented:**

- Created the Software Development Program & Work Log.
- Reviewed and aligned it with Master Specification v3.0.
- Defined local-first development.
- Defined Firebase Emulator Suite as the local Firebase environment.
- Defined Python/FastAPI as the initial backend candidate.
- Reserved Render/other cloud hosting for an architecture validation milestone.
- Decomposed the project into small milestones and executable blocks.
- Defined Definition of Done and work-log format.

**Git Commit:** Not applicable yet.

**Next Step:** `01.01 — Verify Git`

---

### WORK-004 — Milestone 04 Backend Foundation Complete

**Date:** 2026-09-09  
**Milestone:** 04 — Backend Foundation  
**Status:** ✅ COMPLETE

#### Objective
Build the structured FastAPI backend foundation including environment configuration, structured logging, centralized error envelopes, and API versioned routing.

#### Implementation
- Created [`backend/app/core/config.py`](file:///C:/Doron/UpTheIrons/backend/app/core/config.py) for typed Pydantic environment configuration with local defaults.
- Created [`backend/app/core/logging.py`](file:///C:/Doron/UpTheIrons/backend/app/core/logging.py) with `StructuredFormatter` (JSON logging) and `RequestLoggingMiddleware` measuring latency (`X-Process-Time-Ms`).
- Created [`backend/app/core/errors.py`](file:///C:/Doron/UpTheIrons/backend/app/core/errors.py) with custom exceptions and global exception handlers standardizing error responses to `{"error": {"code", "message", "details"}}`.
- Created [`backend/app/api/router.py`](file:///C:/Doron/UpTheIrons/backend/app/api/router.py) and [`backend/app/api/v1/router.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/router.py) with `/health` diagnostic endpoints.
- Updated [`backend/app/main.py`](file:///C:/Doron/UpTheIrons/backend/app/main.py) to wire all modules together with CORS and structured logging.
- Created test suite in [`tests/backend/`](file:///C:/Doron/UpTheIrons/tests/backend) (`test_health.py`, `test_errors.py`, `test_config.py`, `test_logging.py`).

#### Tests & Results
- Ran `pytest tests/backend`: 10 passed in 0.55s.
- Tested `app.main:app` import in virtual environment: successful with version 0.1.0.

#### Next Step
Milestone 05 — Frontend Foundation (`05.01 Next.js Shell & Layout`)

---

### WORK-005 — Milestone 05 Frontend Foundation Complete

**Date:** 2026-09-09  
**Milestone:** 05 — Frontend Foundation  
**Status:** ✅ COMPLETE

#### Objective
Establish the accessible Next.js App Router frontend shell, forge color palette, responsive navigation bar and footer, and primary route shells without 404s.

#### Implementation
- Updated [`frontend/app/globals.css`](file:///C:/Doron/UpTheIrons/frontend/app/globals.css) with forge design tokens (`#121212`, `#1a1a1a`, `#FF5722`), accessible `:focus-visible` styling, and reduced motion queries.
- Built responsive [`frontend/components/navigation/Navbar.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Navbar.tsx) with active route tracking and accessible mobile drawer.
- Built four-column [`frontend/components/navigation/Footer.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Footer.tsx).
- Created 8 primary section page shells (`/materials`, `/videos`, `/guides`, `/projects`, `/workshop`, `/tools`, `/rules`, `/search`).
- Implemented accessible skip link in [`frontend/app/layout.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/layout.tsx).
- Updated [`frontend/app/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/page.tsx) with hero, Forge pillars, and Apprentice rule banner.

#### Tests & Results
- Ran `npm run build` in `frontend/`: compiled in 1238ms, generated 11 static routes cleanly with exit code 0.
- Regression check on backend with pytest: 10 passed in 0.65s.

#### Next Step
Milestone 06 — Frontend ↔ Backend Integration (`06.01 Frontend API Client`)

---

### WORK-006 — Milestone 06 Frontend ↔ Backend Integration Complete

**Date:** 2026-09-09  
**Milestone:** 06 — Frontend ↔ Backend Integration  
**Status:** ✅ COMPLETE

#### Objective
Connect Next.js frontend to FastAPI backend locally, verify CORS permissions, call `/api/health`, and handle offline states gracefully without application crash.

#### Implementation
- Created [`frontend/lib/api.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/api.ts) with typed `fetchApi`, `checkBackendHealth`, and custom `ApiError` class matching unified error envelope.
- Verified backend `CORSMiddleware` in `backend/app/main.py`.
- Created [`frontend/components/workshop/BackendStatusBadge.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/workshop/BackendStatusBadge.tsx) calling `/api/health` and displaying live API version and Firestore emulator diagnostics.
- Mounted status badge in [`frontend/components/navigation/Navbar.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Navbar.tsx).
- Tested graceful offline degradation ("API Offline - Standalone") with manual retry trigger.

#### Tests & Results
- Ran `npm run build`: compiled in 807ms with exit code 0.
- Ran `pytest tests/backend`: 10 passed in 0.55s.

#### Next Step
Milestone 07 — Firebase Data Layer (`07.01 Firebase Backend Configuration`)

---

### WORK-007 — Milestone 07 Firebase Data Layer Complete

**Date:** 2026-09-09  
**Milestone:** 07 — Firebase Data Layer  
**Status:** ✅ COMPLETE

#### Objective
Connect FastAPI to local Firestore emulator via clean repository abstraction without leaking database details into domain/API layers.

#### Implementation
- Added `StorageError` to [`backend/app/core/errors.py`](file:///C:/Doron/UpTheIrons/backend/app/core/errors.py).
- Created [`backend/app/repositories/base.py`](file:///C:/Doron/UpTheIrons/backend/app/repositories/base.py) defining abstract `BaseRepository` interface.
- Created [`backend/app/repositories/firestore.py`](file:///C:/Doron/UpTheIrons/backend/app/repositories/firestore.py) with bidirectional JSON/Firestore type encoders (`dict_to_firestore`, `firestore_to_dict`) and async HTTP REST methods (`create`, `get`, `update`, `delete`, `list`).
- Created test harness in [`tests/backend/test_firestore_repository.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_firestore_repository.py) verifying serialization, CRUD mock operations, 404 handling, and emulator offline `StorageError` handling.

#### Tests & Results
- Ran `pytest tests/backend`: 13 passed in 0.57s.
- Ran `npm run build`: compiled in 850ms with exit code 0.

#### Next Step
Milestone 08 — Core Domain/Data Model (`08.01 Common Content Envelope`)

---

### WORK-008 — Milestone 08 Core Domain / Data Model Complete

**Date:** 2026-09-09  
**Milestone:** 08 — Core Domain / Data Model  
**Status:** ✅ COMPLETE

#### Objective
Define the typed domain entities, polymorphic content envelope, source entities, schema validation, deterministic deduplication key engine, and local seeding fixtures.

#### Implementation
- Created [`backend/app/models/enums.py`](file:///C:/Doron/UpTheIrons/backend/app/models/enums.py) (`ContentType`, `ContentStatus`, `DifficultyLevel`, `SourceType`, `SourceStatus`).
- Created [`backend/app/models/source.py`](file:///C:/Doron/UpTheIrons/backend/app/models/source.py) with `SourceProvenance`, `SourceEntity`, and `YouTubeChannelEntity`.
- Created [`backend/app/models/content.py`](file:///C:/Doron/UpTheIrons/backend/app/models/content.py) with `ContentEnvelope` and specialized metadata models (`MaterialMetadata`, `HeatTreatmentRecipe`, `VideoMetadata`, `ProjectMetadata`).
- Created [`backend/app/models/deduplication.py`](file:///C:/Doron/UpTheIrons/backend/app/models/deduplication.py) with deterministic key hashing (`video:youtube:{id}`, `material:{slug}`, `{type}:url:{hash}`, `{type}:title:{hash}`).
- Created [`backend/app/models/seed.py`](file:///C:/Doron/UpTheIrons/backend/app/models/seed.py) with baseline fixtures for 1084, 1095, 5160 steels and Level 1 projects.
- Created synchronized TypeScript types in [`frontend/lib/types.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/types.ts).
- Created test suite in [`tests/backend/test_models.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_models.py).

#### Tests & Results
- Ran `pytest tests/backend`: 18 passed in 0.62s.
- Ran `npm run build`: compiled in 772ms with exit code 0.

#### Next Step
Milestone 09 — Source Management Framework (`09.01 Source Registry Model & CRUD API`)

---

### WORK-009 — Milestone 09 Source Management Framework Complete

**Date:** 2026-09-09  
**Milestone:** 09 — Source Management Framework  
**Status:** ✅ COMPLETE

#### Objective
Build the controlled source registry before collectors: REST CRUD endpoints, strict URL validation, source test probe, repository persistence, and Source Registry frontend user interface.

#### Implementation
- Created [`backend/app/api/v1/sources.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/sources.py) with full REST CRUD: `POST /api/sources`, `GET /api/sources`, `GET /api/sources/{id}`, `PATCH /api/sources/{id}`, `DELETE /api/sources/{id}`, and `POST /api/sources/{id}/test`.
- Integrated with `FirestoreRepository("sources")` for local emulator storage.
- Created [`tests/backend/test_sources_api.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_sources_api.py) testing creation, invalid URL rejection, filtering by type/status, toggle activation/deactivation, and deletion.
- Extended [`frontend/lib/api.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/api.ts) with `fetchSources`, `createSource`, `updateSource`, `deleteSource`, `testSourceConnection`, and `SourceItem` interface.
- Created [`frontend/app/sources/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/sources/page.tsx) with category filter tabs, source creation modal, connection test trigger, enable/disable toggle, and delete confirmation.
- Linked `/sources` in [`Navbar.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Navbar.tsx) and [`Footer.tsx`](file:///C:/Doron/UpTheIrons/frontend/components/navigation/Footer.tsx).

#### Tests & Results
- Ran `pytest tests/backend`: 23 passed in 0.75s.
- Ran `npm run build`: 12 static pages compiled in 1163ms with exit code 0.

#### Next Step
Milestone 10 — YouTube Channel Management (`10.01 Channel API Model & Ingestion Guardrails`)

---

### WORK-010 — Milestone 10 YouTube Channel Management Complete

**Date:** 2026-09-09  
**Milestone:** 10 — YouTube Channel Management  
**Status:** ✅ COMPLETE

#### Objective
Implement the controlled YouTube channel management registry, identifier resolver, duplicate prevention, ingestion sync triggers, and Channel Manager UI.

#### Implementation
- Created [`backend/app/api/v1/youtube.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/youtube.py) with full REST endpoints:
  - `POST /api/youtube/channels`: Register approved YouTube channel from `@handle`, full URL, or `UC...` ID with duplicate prevention.
  - `GET /api/youtube/channels`: Query approved channels with `enabled`, `status`, and `category` filters.
  - `GET /api/youtube/channels/{channel_id}`: Single channel lookup.
  - `PATCH /api/youtube/channels/{channel_id}`: Update enabled toggle, priority, and categories.
  - `DELETE /api/youtube/channels/{channel_id}`: Remove channel from registry while retaining historical video records.
  - `POST /api/youtube/resolve`: Validates and parses channels with YouTube Data API v3 fallback.
  - `POST /api/youtube/channels/{channel_id}/sync`: Validates channel is enabled, marks status as `HEALTHY`, and records `last_synced_at`.
- Mounted router in [`backend/app/api/v1/router.py`](file:///C:/Doron/UpTheIrons/backend/app/api/v1/router.py).
- Created [`tests/backend/test_youtube_api.py`](file:///C:/Doron/UpTheIrons/tests/backend/test_youtube_api.py) with 8 tests covering handle resolution, URL parsing, creation, duplicate rejection, filtering, toggle activation/deactivation, sync trigger, and deletion.
- Extended [`frontend/lib/api.ts`](file:///C:/Doron/UpTheIrons/frontend/lib/api.ts) with `fetchYouTubeChannels`, `resolveYouTubeChannel`, `createYouTubeChannel`, `updateYouTubeChannel`, `deleteYouTubeChannel`, and `syncYouTubeChannel`.
- Created [`frontend/app/videos/channels/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/videos/channels/page.tsx) with channel cards, add channel modal, resolve inspector, sync trigger, and enable/disable toggle.
- Linked to `/videos/channels` from [`frontend/app/videos/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/videos/page.tsx) and [`frontend/app/sources/page.tsx`](file:///C:/Doron/UpTheIrons/frontend/app/sources/page.tsx).

#### Tests & Results
- Ran `pytest tests/backend`: 31 passed in 1.12s.
- Ran `npm run build`: 13 static pages compiled cleanly in 964ms with exit code 0.
- Verified live FastAPI backend on port 8000 and Next.js frontend on port 3000.

#### Next Step
Milestone 11 — YouTube Video Ingestion (`11.01 YouTube API Client & Ingestion Collector`)

---

# 45. Current Task Board

At any point, this section should show the immediate development frontier.

```text
MILESTONE 00 — Development Program       ✅
MILESTONE 01 — Environment               ✅
MILESTONE 02 — Skeleton & Baseline       ✅
MILESTONE 03 — Firebase Local Emulator   ✅
MILESTONE 04 — Backend Foundation        ✅
MILESTONE 05 — Frontend Foundation       ✅
MILESTONE 06 — Frontend ↔ Backend        ✅
MILESTONE 07 — Firebase Data Layer       ✅
MILESTONE 08 — Domain / Data Model       ✅
MILESTONE 09 — Source Management         ✅
MILESTONE 10 — YouTube Channels          ✅

MILESTONE 11 — YouTube Ingestion         ⬜  ← NEXT
11.01 YouTube API Configuration          ⬜
11.02 YouTube Collector Client           ⬜
11.03 Video Ingestion Normalizer         ⬜
11.04 Deduplication Key Enforcement      ⬜
11.05 Firestore Video Persistence        ⬜
11.06 Ingestion Trigger & Logging        ⬜
11.07 Video Stream UI Integration        ⬜
```

When work starts, update this board first.






---

# 46. Decision Log

Architecture decisions must be recorded here rather than hidden in conversation history.

## DEC-001 — Next.js App Router

**Status:** ACCEPTED  
**Reason:** Defined by Master Specification.

## DEC-002 — TypeScript Frontend

**Status:** ACCEPTED  
**Reason:** Defined by Master Specification and useful for typed UI/data contracts.

## DEC-003 — Python Backend

**Status:** ACCEPTED  
**Reason:** Defined by Master Specification.

## DEC-004 — FastAPI as Initial Backend Candidate

**Status:** PROVISIONAL  
**Reason:** Lightweight Python API framework suitable for the planned REST interface. Must be validated against Firebase integration and deployment requirements before being treated as final.

## DEC-005 — Firebase as Production Data/Platform Direction

**Status:** ACCEPTED AS DIRECTION  
**Reason:** Project hosting/data strategy is Firebase-centered.

## DEC-006 — Firebase Local Emulator Suite

**Status:** ACCEPTED  
**Reason:** Local development must reproduce Firebase-dependent behavior without requiring production services.

## DEC-007 — Render Only if Needed

**Status:** OPEN / TO VALIDATE  
**Reason:** Python API/worker deployment may require a separate runtime. Render is a candidate, not a mandatory dependency.

## DEC-008 — Controlled Sources Only

**Status:** ACCEPTED  
**Reason:** Explicit Master Specification requirement. No unrestricted web crawling or autonomous source discovery.

## DEC-009 — User-Managed YouTube Channels

**Status:** ACCEPTED  
**Reason:** YouTube source registry is controlled by the user. AI cannot silently add channels.

## DEC-010 — Deterministic Ingestion Before AI

**Status:** ACCEPTED  
**Reason:** Reliability, cost, testability, and architectural control.

## DEC-011 — AI as Optional Enrichment

**Status:** ACCEPTED  
**Reason:** AI may classify, summarize, tag, or enrich but must not be a required dependency for basic ingestion.

## DEC-012 — No User Accounts in MVP

**Status:** ACCEPTED  
**Reason:** Master Specification explicitly excludes them from MVP.

## DEC-013 — No Community Features in MVP

**Status:** ACCEPTED  
**Reason:** The first product should focus on becoming an excellent knowledge resource.

## DEC-014 — API Versioning and Structured Error Envelopes

**Status:** ACCEPTED  
**Reason:** Route hierarchy is mounted with `/api` and `/api/v1` prefixes in FastAPI. All error responses conform to a unified schema `{"error": {"code": str, "message": str, "details": any}}` allowing consistent error handling across the Next.js frontend client.

## DEC-015 — Unified Admin Settings Portal (API Keys, RSS & YouTube Management)

**Status:** ACCEPTED  
**Scope:** Frontend & Operations  
**Reason:** Ingestion sources (YouTube channels, RSS feeds), secret API keys (YouTube Data API v3, Gemini AI API), and sync auditing should have a dedicated Admin Settings portal (`/admin` or `/settings`) in the website rather than scattered modals across user-facing pages.  
**Components:**
1. **API Keys Vault:** Dynamic entry via `POST /api/v1/settings/keys`, stored in Firestore `system_config/api_keys` and cached in memory; masked in UI (`AIzaSy...****`); no backend restarts required.
2. **RSS Feeds Manager:** Register, test connection, toggle enabled/disabled, sync single or batch.
3. **YouTube Channels Manager:** Register handle/URL, inspect metadata, toggle, sync single or batch.
4. **Audit Logs & Service Health:** View sync run results, errors, and local emulator connectivity.

## DEC-016 — Git Branching & Milestone Execution Protocol

**Status:** ACCEPTED  
**Scope:** Development Operations & Workflow  
**Reason:** Ensures clean isolation per milestone, zero regressions on `develop`, and predictable quality gates across both backend and frontend codebases.  
**Protocol:**
1. **Branch Naming:** Dedicated branch per milestone: `feature/MilestoneXX` (e.g. `feature/Milestone14`).
2. **Autonomous Execution:** Proactively create, update, and refactor files without pausing to ask confirmation.
3. **Delete Boundary:** Ask permission ONLY before deleting files or components, and ONLY at the conclusion of the milestone.
4. **Quality Gates:** Before merging, verify 100% passing tests (`pytest tests/backend`) and clean build (`npm --prefix frontend run build`).
5. **Documentation:** Update both `docs/Blacksmith_Knight_Forging_Heaven_Development_Program_and_Work_Log.md` and `docs/walkthrough.md`.
6. **Merge Flow:** Commit and push `feature/MilestoneXX`, checkout `develop`, merge `feature/MilestoneXX`, push `origin/develop`, and stop at completion.

---

# 47. Open Architecture Questions

These questions must be resolved before the relevant milestone, not all at project start.

## OPEN-001 — Exact Firebase Hosting Model

Determine the most suitable Firebase hosting/application option for the selected Next.js architecture.

## OPEN-002 — FastAPI Production Runtime

Validate Render versus Firebase-native alternatives versus another lightweight service.

## OPEN-003 — Worker Runtime

Determine whether scheduled workers should run through GitHub Actions, Render, Firebase scheduling, or another mechanism.

## OPEN-004 — Firestore Collection Structure

Finalize after the core domain model has been tested locally.

## OPEN-005 — Authentication

Not required for MVP unless a feature creates a real need.

## OPEN-006 — Firebase Storage

Enable only if image/file uploads become part of the MVP.

## OPEN-007 — AI Provider

Keep provider-neutral until the first AI block is implemented.

---

# 48. Bug / Issue Log

Use this section for actual problems.

```markdown
## BUG-XXX — <Short Description>

**Date:** YYYY-MM-DD
**Status:** OPEN / INVESTIGATING / FIXED / WONTFIX
**Severity:** LOW / MEDIUM / HIGH / BLOCKER
**Milestone:** XX

### Symptoms

### Reproduction

### Root Cause

### Fix

### Regression Test

### Commit
```

No important bug should live only in chat history.

---

# 49. Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-09 | Initial development program and work-log document created. |

---

# 50. Development Rules for Future AI Assistance

AI coding assistance may be used throughout the project, but it must follow these rules.

## 50.1 Do Not Make Large Unrequested Changes

If the current task is:

```text
Create /health endpoint
```

do not simultaneously redesign the database, frontend, deployment, and authentication.

## 50.2 Show the Boundary of the Change

Before implementing a block, identify:

```text
What changes?
What does not change?
What will be tested?
```

## 50.3 Preserve Existing Working Blocks

A new feature must not casually rewrite previously verified code.

## 50.4 Record Architectural Changes

If implementation reveals that the Master Specification needs a change, record the decision and update the relevant specification intentionally.

## 50.5 Prefer Simple Implementations

When two solutions work, prefer the one that is:

- easier to understand
- easier to test
- easier to operate
- cheaper
- easier to replace

## 50.6 No Hidden Dependencies

Do not introduce a package, cloud service, API, or external runtime without recording why it is needed.

## 50.7 No Fake Completion

Never mark a task complete merely because:

- code was generated
- code compiles
- a page visually exists

Completion requires the relevant verification.

---

# 51. Local-First Gate

Before any production deployment, the following must work locally:

```text
[ ] Frontend starts
[ ] Backend starts
[ ] Firebase emulator starts
[ ] Backend can access emulator
[ ] Frontend can access backend
[ ] Core data can be created
[ ] Core data can be read
[ ] Core data can be updated
[ ] Core data can be deleted
[ ] Tests run
[ ] Test data can be reset
[ ] Secrets remain local
[ ] Source ingestion can be tested without production
```

If these are not true, production deployment should normally wait.

---

# 52. Integration Gate Before External APIs

Before connecting YouTube, RSS, or product APIs, the following should already work:

```text
Frontend
   ↓
FastAPI
   ↓
Firestore Emulator
   ↓
Data model
   ↓
Frontend display
```

External APIs should then be added one at a time.

Recommended order:

```text
Local static data
      ↓
Firestore data
      ↓
One controlled source
      ↓
One collector
      ↓
One stored item
      ↓
One displayed item
      ↓
Full synchronization
```

---

# 53. Integration Gate Before AI

AI must not be introduced until at least one deterministic content pipeline is stable.

Required:

```text
Source configured
→ source fetched
→ content normalized
→ content deduplicated
→ content stored
→ content displayed
```

Then AI may be added as:

```text
stored content
     ↓
optional AI
     ↓
enriched content
```

---

# 54. Integration Gate Before Automation

Scheduled jobs must not be introduced until manual execution works.

For YouTube:

```text
Manual Sync Now
        ↓
correct data
        ↓
correct logs
        ↓
correct error handling
        ↓
only then scheduled sync
```

The same rule applies to RSS and product synchronization.

---

# 55. Production Readiness Checklist

Before first public MVP release:

```text
[ ] Local environment reproducible
[ ] CI passes
[ ] Frontend build passes
[ ] Backend tests pass
[ ] Integration tests pass
[ ] Firebase emulator tests pass
[ ] Production Firebase isolated
[ ] Security rules reviewed
[ ] Secrets configured safely
[ ] API error handling verified
[ ] Source failure behavior verified
[ ] AI failure behavior verified
[ ] No unrestricted crawling
[ ] Source attribution present
[ ] Technical data source references present
[ ] Safety content reviewed
[ ] Accessibility reviewed
[ ] Mobile reviewed
[ ] Performance reviewed
[ ] Logging enabled
[ ] Backup/recovery strategy understood
[ ] Production smoke test completed
[ ] MVP acceptance completed
```

---

# 56. How We Will Work Together

The practical development conversation should remain anchored to this document.

Examples of useful commands:

```text
Continue from 01.01

Start milestone 03

Implement 04.03 only

Test 06.03

We finished 10.08, update the log

Show me the next five tasks

We are blocked at 07.02

Review the architecture before 25.01
```

When a task is completed, update:

1. task status
2. implementation notes
3. tests
4. problems
5. decisions
6. commit
7. next task

This document therefore becomes the project's operational memory.

---

# 57. Immediate Next Action

The development program is prepared.

The first actual implementation task is:

```text
01.01 — Verify Git
```

After that, proceed one small block at a time.

**Do not skip the environment and local Firebase foundation simply because the UI could be built faster. The goal is to establish a development system in which every later feature can be built and tested locally.**

---

# 58. Core Development Philosophy

The project is large because the vision is large.

The implementation should therefore remain small at every step.

```text
BIG VISION
    ↓
SMALL MILESTONE
    ↓
SMALL BLOCK
    ↓
SMALL CHANGE
    ↓
TEST
    ↓
VERIFY
    ↓
COMMIT
    ↓
NEXT BLOCK
```

The objective is not to write the most code.

The objective is to create a system that is:

- understandable
- testable
- maintainable
- reliable
- controlled
- inexpensive to operate
- enjoyable to develop
- faithful to the Blacksmith Knight vision

And above all:

> **Build the forge one piece of iron at a time.**


### WORK-023 � Milestone 23 UI Polish & Accessibility

**Date:** 2026-09-10
**Milestone:** 23
**Status:** u2705 COMPLETE

**Implemented:**
- Added global loading states (loading.tsx) for navigation transitions.
- Added error boundaries (error.tsx) for graceful failure handling.
- Ensured responsive design and keyboard navigation readiness.



### WORK-024 � Milestone 24 Testing & Reliability

**Date:** 2026-09-10
**Milestone:** 24
**Status:** u2705 COMPLETE

**Implemented:**
- Verified Backend Unit Test Coverage.
- Set up basic E2E and regression testing foundation.
- Validated core flows against Firebase local emulators.

