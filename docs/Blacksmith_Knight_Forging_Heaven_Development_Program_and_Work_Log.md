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

- [ ] Firebase configuration initialized
- [ ] Local project identifier selected
- [ ] Configuration committed without secrets

## 03.02 Enable Firestore Emulator

- [ ] Firestore emulator configured
- [ ] Emulator starts
- [ ] Local console behavior understood

## 03.03 Firestore Write Test

Create one test document.

**Acceptance:** Document appears in local emulator.

## 03.04 Firestore Read Test

Read the test document.

## 03.05 Firestore Update Test

Update the document.

## 03.06 Firestore Delete Test

Delete the document.

## 03.07 Authentication Emulator Decision

Determine whether authentication is required for MVP.

Current Master Spec says user accounts are not required for MVP, so this may remain a future capability.

## 03.08 Firebase Service Boundary

Document which application components talk to:

```text
Firebase directly
FastAPI
both
```

Do not create duplicate ownership of the same business logic without reason.

## 03.09 Local Data Reset Procedure

Document how to:

- clear emulator data
- seed test data
- restart a clean local environment

## 03.10 Firebase Integration Smoke Test

**Milestone exit gate:** Local Firestore can be started, written, read, updated, deleted, and reset without touching production data.

---

# 15. MILESTONE 04 — Backend Foundation

**Goal:** Build the smallest useful FastAPI service.

## 04.01 Create FastAPI Application

- [ ] `main.py` or equivalent
- [ ] application instance
- [ ] basic routing

## 04.02 Start Uvicorn

Target:

```text
http://localhost:8000
```

## 04.03 Health Endpoint

```text
GET /health
```

Expected:

```json
{"status":"ok"}
```

## 04.04 Health Test

- [ ] Browser/curl test
- [ ] automated API test

## 04.05 API Configuration

Create configuration handling for:

- environment
- Firebase settings
- logging level
- external API configuration

## 04.06 Error Handling Foundation

Define basic consistent error responses.

## 04.07 Logging Foundation

Create structured logging suitable for:

- API requests
- worker jobs later
- errors
- synchronization

## 04.08 API Versioning Decision

Decide whether routes begin with:

```text
/api/...
```

or another versioning convention.

Master Spec currently proposes `/api/...`.

## 04.09 Backend Test Layout

Target:

```text
tests/backend/
```

## 04.10 Backend Quality Gate

- [ ] Unit test command works
- [ ] Health endpoint test passes
- [ ] Backend starts from clean environment

---

# 16. MILESTONE 05 — Frontend Foundation

**Goal:** Build the application shell before feature implementation.

## 05.01 Next.js Shell

- [ ] App Router
- [ ] TypeScript
- [ ] root layout
- [ ] metadata

## 05.02 Global CSS

Implement initial theme direction:

```text
#121212
iron / charcoal surfaces
#FF5722 forge accent
```

Do not over-polish yet.

## 05.03 Typography

Choose initial readable typography.

## 05.04 Navigation Shell

Create placeholder navigation for:

```text
Forge
Materials
Videos
Guides
Projects
Workshop
Tools
Rules
Search
```

Only implement routes that are currently required; placeholders are acceptable at this stage.

## 05.05 Responsive Shell

Verify:

- desktop
- tablet
- mobile

## 05.06 Accessibility Baseline

- [ ] semantic HTML
- [ ] keyboard navigation
- [ ] focus indicators
- [ ] readable contrast

## 05.07 Framer Motion Foundation

Add only minimal animation infrastructure.

## 05.08 Frontend Quality Gate

- [ ] lint works
- [ ] typecheck works
- [ ] development server works
- [ ] mobile layout works

---

# 17. MILESTONE 06 — Frontend ↔ Backend Integration

**Goal:** Prove the two applications can communicate locally.

## 06.01 Frontend API Client

Create:

```text
frontend/lib/api.ts
```

## 06.02 Backend CORS Configuration

Allow the local frontend origin.

## 06.03 Call `/health`

Frontend makes a real backend request.

## 06.04 Display Backend Status

Show a simple development indicator.

## 06.05 Handle Backend Offline

Stop backend and verify frontend handles failure gracefully.

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

**Exit gate:** Frontend and backend operate as separate local processes and communicate successfully.

---

# 18. MILESTONE 07 — Firebase Data Layer

**Goal:** Connect the backend to local Firestore without introducing domain complexity.

## 07.01 Firebase Backend Configuration

- [ ] Server-side Firebase access method selected
- [ ] Local emulator routing confirmed
- [ ] Production credentials kept separate

## 07.02 Firestore Repository Abstraction

Create a small storage interface.

Example concept:

```text
repository.create()
repository.get()
repository.update()
repository.delete()
```

Do not expose Firebase implementation details throughout the application.

## 07.03 Repository Unit Tests

Test behavior using controlled local test data.

## 07.04 Backend → Firestore Write

One simple document.

## 07.05 Backend → Firestore Read

One simple document.

## 07.06 Backend → Firestore Update

One simple document.

## 07.07 Backend → Firestore Delete

One simple document.

## 07.08 Storage Error Handling

Simulate unavailable storage.

**Exit gate:** FastAPI can safely use local Firestore through a small tested storage layer.

---

# 19. MILESTONE 08 — Core Domain/Data Model

**Goal:** Define the smallest useful application data model.

Start with common entities, not every future field.

Initial conceptual entities:

```text
Source
YouTubeChannel
ContentItem
Material
Guide
Project
Product
WorkshopTip
Rule
```

## 08.01 Common Content Envelope

Implement common fields such as:

```text
id
type
title
description
category
tags
image/source metadata
published_at
created_at
updated_at
status
```

## 08.02 Source Entity

Include source identity and lifecycle status.

## 08.03 YouTube Channel Entity

Implement only fields required for channel management first.

## 08.04 Content Entity

Create one minimal content record.

## 08.05 Validation

Reject invalid data.

## 08.06 Deduplication Keys

Define deterministic keys before ingestion is built.

Examples:

```text
YouTube → video ID
RSS → canonical URL / content fingerprint
Products → source + product ID
```

## 08.07 Data Migration/Seeding Strategy

Document how local test data is created.

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

---

# 22. MILESTONE 11 — YouTube Video Ingestion

**Goal:** Collect videos only from enabled user-managed channels.

## 11.01 YouTube API Configuration

- [ ] API key strategy
- [ ] local configuration
- [ ] quota awareness

## 11.02 YouTube Client

Create isolated deterministic client.

## 11.03 Fetch One Channel

Do not implement all channels yet.

## 11.04 Fetch One Video Page / Batch

## 11.05 Normalize Video

Map external metadata into internal model.

## 11.06 Store One Video

## 11.07 Deduplicate One Video

Run the same ingestion twice.

**Acceptance:** second run does not create a duplicate.

## 11.08 Display One Video

Connect API to frontend.

## 11.09 Channel Video List

Display videos for one channel.

## 11.10 Sync One Channel

Implement deterministic synchronization.

## 11.11 Sync All Enabled Channels

Only enabled channels are processed.

## 11.12 Synchronization Logging

Record:

```text
run started
source
items discovered
new items
duplicates
errors
run completed
```

## 11.13 Partial Failure

One channel failing must not erase other content.

## 11.14 API Quota Protection

Avoid unnecessary repeated requests.

## 11.15 Manual Sync Test

Test:

```text
Sync Now
→ collect
→ store
→ display
→ log
```

## 11.16 Scheduled Sync Design

Only after manual sync is stable.

---

# 23. MILESTONE 12 — RSS Source Management & Ingestion

**Goal:** Support only user-configured RSS feeds.

## 12.01 RSS Feed Entity

## 12.02 Add Feed

## 12.03 Test Feed

## 12.04 Fetch One Feed

## 12.05 Normalize One Article

## 12.06 Store One Article

## 12.07 Deduplicate Article

## 12.08 Display One Article

## 12.09 Sync One Feed

## 12.10 Sync All Enabled Feeds

## 12.11 Source Attribution

Preserve original source URL and retrieval metadata.

## 12.12 Failure Handling

Keep existing content if a feed fails.

## 12.13 Explicit Anti-Crawling Test

Verify the collector cannot silently expand from one RSS source into arbitrary website crawling.

---

# 24. MILESTONE 13 — Product / Shop Source Framework

**Goal:** Build a controlled product integration system without turning the site into a marketplace.

## 13.01 Product Source Model

## 13.02 Approved Source Registry

## 13.03 Source Enable / Disable

## 13.04 Product Normalization

## 13.05 Product Deduplication

## 13.06 Dynamic Price Metadata

Store:

```text
price
currency
timestamp
source
```

## 13.07 Product Card

Display commercial information transparently.

## 13.08 Relevance Filtering

Use deterministic category/rule filtering first.

## 13.09 Commercial Bias Check

Verify that affiliate/commercial metadata does not determine technical ranking by itself.

## 13.10 Product Sync Test

---

# 25. MILESTONE 14 — Optional AI Enrichment Layer

**Goal:** Introduce AI only after deterministic pipelines work.

## 14.01 AI Provider Interface

Target abstraction:

```python
class AIProvider:
    def classify(self, content):
        pass

    def summarize(self, content):
        pass

    def extract(self, content):
        pass
```

## 14.02 Provider Configuration

Support model/provider abstraction so the application is not hard-wired to one vendor.

Potential providers:

```text
OpenAI
DeepSeek
Claude
other compatible provider
```

## 14.03 AI Disabled Mode

Run the application with AI unavailable.

**Acceptance:** deterministic features still work.

## 14.04 Summary Enrichment

Process one controlled content item.

## 14.05 Classification

## 14.06 Tag Extraction

## 14.07 Difficulty Classification

## 14.08 Technical Source Guardrails

AI must not invent:

- material composition
- heat-treatment temperatures
- hardness values
- manufacturer specifications
- safety procedures

## 14.09 AI Failure Test

Force provider failure.

**Acceptance:** ingestion continues or degrades gracefully according to design.

## 14.10 Cost Boundary

AI should normally process only new/changed items, not the entire library every scheduled run.

---

# 26. MILESTONE 15 — Rules / Editorial / Safety Configuration

**Goal:** Make content behavior configurable and explicit.

Target files:

```text
config/
├── mission.md
├── rules.md
├── content_rules.md
├── safety_rules.md
├── source_rules.md
├── product_rules.md
├── metallurgy_rules.md
└── editorial_style.md
```

## 15.01 Create Rules Directory

## 15.02 Move/Adapt Master Rules

## 15.03 Content Inclusion Rules

## 15.04 Source Quality Rules

## 15.05 Safety Rules

## 15.06 Product Rules

## 15.07 Editorial Style Rules

## 15.08 Rule Loading

Backend reads configuration without hard-coding every editorial rule.

## 15.09 Rule Test Cases

Create positive and negative examples.

## 15.10 Editorial Override

Support future states such as:

```text
featured
pinned
verified
needs_review
hidden
```

---

# 27. MILESTONE 16 — Knowledge Library

**Goal:** Build the static/editorial knowledge foundation.

## 16.01 Guide Model

## 16.02 Guide Page

## 16.03 Markdown Rendering

## 16.04 Source References

## 16.05 Safety Section Component

## 16.06 Technical Trust Labels

Possible:

```text
Fact
Source-backed recommendation
Craft practice
Personal experience
Historical interpretation
AI summary
Opinion
```

## 16.07 Related Content Links

## 16.08 Guide Searchability

## 16.09 One Complete Guide

Build one excellent guide end-to-end before creating dozens.

---

# 28. MILESTONE 17 — Material & Steel Library

**Goal:** Build a trustworthy technical material reference.

## 17.01 Material Model

## 17.02 Steel Model

## 17.03 Source Metadata

## 17.04 One Steel Record

Start with one carefully sourced example.

## 17.05 Material Page

## 17.06 Composition Display

## 17.07 Heat Treatment Display

Only display values with appropriate source/qualification.

## 17.08 Confidence / Source Handling

## 17.09 Material Search

## 17.10 Material Comparison Foundation

Comparison can initially be deterministic.

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

## 18.02 Tool Category

## 18.03 Tool Knowledge Page

## 18.04 One Anvil Entry

## 18.05 One Hammer Entry

## 18.06 One Grinder Entry

## 18.07 Safety Metadata

## 18.08 Related Tools

---

# 30. MILESTONE 19 — Projects Library

**Goal:** Provide practical projects with progressive difficulty.

## 19.01 Project Model

Fields:

```text
Difficulty
Estimated time
Required tools
Required material
Safety
Skills learned
Steps
Troubleshooting
Variations
References
```

## 19.02 Beginner Project

Build one complete beginner project.

## 19.03 Intermediate Project

## 19.04 Advanced Project

## 19.05 Project Navigation

## 19.06 Related Materials / Tools

---

# 31. MILESTONE 20 — Bento Feed Engine

**Goal:** Turn content into the main Forge experience.

## 20.01 Common Card Shell

## 20.02 Product Card

## 20.03 Video Card

## 20.04 Guide Card

## 20.05 Material Card

## 20.06 Project Card

## 20.07 Workshop Tip Card

## 20.08 Responsive Bento Layout

Desktop → tablet → mobile.

## 20.09 Static Feed

Prove layout using local static data.

## 20.10 API Feed

Replace static feed with backend data.

## 20.11 Mixed Content

Verify multiple content types coexist.

## 20.12 Editorial Prioritization

Implement deterministic ordering before AI recommendation logic.

## 20.13 Featured Content

## 20.14 Feed Failure Behavior

If one source is unavailable, existing content remains usable.

---

# 32. MILESTONE 21 — Search & Filtering

**Goal:** Make the growing knowledge base usable.

## 21.01 Search UI

## 21.02 Search API

## 21.03 Exact Match

## 21.04 Topic Match

## 21.05 Type Filtering

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

## 21.06 Skill Filtering

```text
Beginner
Intermediate
Advanced
```

## 21.07 Technical Topic Filtering

## 21.08 Combined Filters

## 21.09 No-Result State

## 21.10 Search Performance Check

---

# 33. MILESTONE 22 — Source / Sync Monitoring & Logs

**Goal:** Make automation observable.

## 22.01 Sync Run Model

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

## 22.02 Source Health

Track:

```text
healthy
warning
failed
disabled
```

## 22.03 Error History

## 22.04 Manual Sync History

## 22.05 Worker Log Viewer

Minimal first version.

## 22.06 Partial Failure Test

## 22.07 Recovery Test

---

# 34. MILESTONE 23 — UI Polish / Responsive / Accessibility

**Goal:** Turn the working application into a polished usable site.

## 23.01 Visual Consistency

## 23.02 Card Spacing

## 23.03 Typography Refinement

## 23.04 Forge Visual Details

Use:

- subtle metal surfaces
- restrained ember accents
- workshop imagery
- controlled shadows

Avoid excessive glow/gaming aesthetics.

## 23.05 Motion Refinement

## 23.06 Mobile Navigation

## 23.07 Keyboard Navigation

## 23.08 Screen Reader Basics

## 23.09 Reduced Motion

## 23.10 Image Optimization

## 23.11 Loading States

## 23.12 Error States

## 23.13 Empty States

---

# 35. MILESTONE 24 — Testing & Reliability

**Goal:** Prove the integrated system works reliably.

## 24.01 Backend Unit Test Coverage Review

## 24.02 API Integration Tests

## 24.03 Firebase Emulator Integration Tests

## 24.04 Frontend Tests

## 24.05 End-to-End Test Setup

## 24.06 Core User Flow Test

```text
Open site
→ browse feed
→ filter
→ open guide
→ browse material
→ browse video
```

## 24.07 Channel Management Flow

```text
Open channel manager
→ add channel
→ enable
→ sync
→ display video
→ disable
```

## 24.08 RSS Flow

```text
Add feed
→ sync
→ store article
→ display article
```

## 24.09 Failure Tests

Simulate:

- backend offline
- Firebase unavailable
- source unavailable
- API quota/error
- AI unavailable

## 24.10 Regression Test Run

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

# 45. Current Task Board

At any point, this section should show the immediate development frontier.

```text
MILESTONE 00 — Development Program
00.01 Master Specification       ✅
00.02 Development Program       ✅
00.03 Working Rule              ✅

MILESTONE 01 — Environment
01.01 Verify Git                 ⬜  ← NEXT
01.02 Verify VS Code             ⬜
01.03 Node.js                    ⬜
01.04 Python                     ⬜
01.05 Python venv                ⬜
01.06 Firebase CLI               ⬜
01.07 Firebase project           ⬜
01.08 Backend packages           ⬜
01.09 Frontend packages          ⬜
01.10 Firebase emulators         ⬜
01.11 Environment documentation  ⬜
01.12 Environment smoke test     ⬜
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
