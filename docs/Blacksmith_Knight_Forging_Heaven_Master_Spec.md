# Blacksmith Knight — Forging Heaven
## Complete Product, Architecture, Content, Data, AI, and Development Specification

**Document type:** Master Product & Technical Specification  
**Project:** Blacksmith Knight — Forging Heaven  
**Primary purpose:** A personal, amateur-friendly digital home for blacksmithing, bladesmithing, forging, metallurgy, heat treatment, grinding, workshop tools, materials, techniques, projects, videos, articles, and practical knowledge.  
**Audience:** Hobbyists, beginners, intermediate makers, DIY users, and people learning blacksmithing for personal enjoyment.  
**Commercial orientation:** **Non-commercial / personal-use first.** The website should help people learn, experiment responsibly, build skills, and enjoy the craft—not operate as a marketplace or business platform.

---

# 1. Vision

Blacksmith Knight — Forging Heaven should feel like entering a **digital blacksmith's workshop, forge, library, and knowledge vault**.

It is not intended to be a generic blog, social network, e-commerce store, or traditional forum.

The experience should communicate:

- Fire
- Steel
- Iron
- Craftsmanship
- Old-world blacksmithing
- Modern workshop knowledge
- Discovery
- Experimentation
- Respect for materials
- Respect for tools
- Respect for safety
- Practical learning

The central concept is:

> **A place where an amateur blacksmith can learn almost everything needed to understand, practice, and enjoy forging.**

The site should combine the atmosphere of a medieval forge with the usefulness of a modern technical reference library.

The visual identity should suggest:

- A dark forge at night
- Hot steel glowing in the fire
- Hammer marks
- Anvil surfaces
- Charcoal and iron
- Sparks
- Burnished metal
- Medieval craftsmanship
- A knight's workshop
- A technical engineering notebook

However, the website must remain highly usable. The theme should enhance the information rather than make the interface difficult to read.

---

# 2. Target Audience

The primary audience is **amateur and personal-use makers**.

## 2.1 Beginner

Someone who:

- Has never forged before
- Is considering buying a forge
- Wants to understand anvils
- Wants to learn basic hammer technique
- Wants to understand steel
- Wants to make simple tools
- Wants to learn knife-making eventually
- Needs explanations without assuming professional knowledge

The site should explain terminology rather than assuming expertise.

Example:

Instead of only:

> Normalize 1084 before hardening.

Explain:

> Normalizing is a heat-treatment step used to refine and reset the steel's structure before hardening. For a beginner, think of it as preparing the steel for more predictable behavior during the next heat-treatment stage.

---

## 2.2 Intermediate Hobbyist

Someone who already knows:

- Basic forging
- Basic hammer control
- Basic heat treatment
- Grinding
- Basic steel identification

They want:

- Better techniques
- More detailed metallurgy
- Comparisons
- Tool recommendations
- Workshop improvements
- Project ideas
- Troubleshooting
- Advanced tutorials

---

## 2.3 Experienced Amateur

The site should also provide enough depth for advanced hobbyists.

Content can include:

- Phase transformations
- Carbon content
- Alloying elements
- Hardenability
- Grain refinement
- Tempering behavior
- Quenching media
- Heat-treatment cycles
- Forging temperatures
- Decalescence/recalescence
- Grain growth
- Abrasive selection
- Power hammer technique
- Grinder setup
- Tool steel selection

The website should never deliberately make technical material simplistic merely because beginners are welcome.

Instead:

**Simple first → detailed second → technical reference available.**

---

# 3. Core Philosophy

The site should follow these principles.

## 3.1 Amateur First

Every major feature should answer:

> "Will this help a person working in their own workshop?"

Avoid building features primarily for:

- Companies
- Industrial production
- Professional manufacturing businesses
- Inventory management
- CRM
- Commercial sales
- Business analytics

Industrial information can still be included when it teaches the craft.

---

## 3.2 Knowledge Over Advertising

Commercial links may exist where useful, but the site should never feel like an advertising portal.

Product information should answer:

- What is this tool?
- Why would I need it?
- What are the alternatives?
- What should a beginner look for?
- What are the limitations?
- Is an expensive version actually useful for a hobbyist?

---

## 3.3 Safety Is Part of the Craft

Safety information should be integrated throughout the site.

Important areas include:

- Heat
- Fire
- Hot metal
- Sparks
- Scale
- Grinding dust
- Noise
- Eye protection
- Hearing protection
- Ventilation
- Respiratory protection
- Gas equipment
- Electrical equipment
- Quenching
- Oil/fire hazards
- Workshop layout
- Emergency procedures

Safety should never be treated as an annoying disclaimer.

It should be treated as:

> **Part of becoming a competent craftsman.**

---

# 4. Brand Identity

## Name

**Blacksmith Knight — Forging Heaven**

Possible short references:

- Blacksmith Knight
- Forging Heaven
- The Forge
- The Knight's Forge
- Forge Heaven

The full name should be used prominently on the home page.

---

# 5. Visual Direction

## 5.1 Primary Theme

Dark industrial / forge aesthetic.

Primary background:

```text
#121212
```

Supporting tones:

```text
Charcoal
Dark iron grey
Graphite
Steel grey
Gunmetal
Muted silver
Warm metal grey
```

Accent:

```text
#FF5722
```

The orange should resemble:

- Hot steel
- Forge fire
- Sparks
- Molten metal
- Ember glow

---

## 5.2 Visual Hierarchy

The interface should feel dark but not flat.

Use:

- Layered dark surfaces
- Subtle borders
- Slight metallic gradients
- Orange highlights
- Soft shadows
- Occasional ember-like glow
- Large workshop photography
- Steel textures where appropriate

Do not overuse glowing effects.

The site should feel like a **serious workshop**, not a gaming website.

---

# 6. Frontend Technology

## Framework

Next.js using the App Router.

Recommended stack:

- Next.js
- React
- TypeScript
- Tailwind CSS
- Framer Motion

---

# 7. Frontend Architecture

Suggested structure:

```text
frontend/
├── app/
│   ├── page.tsx
│   ├── materials/
│   │   └── page.tsx
│   ├── videos/
│   │   └── page.tsx
│   ├── shop/
│   │   └── page.tsx
│   ├── rules/
│   │   └── page.tsx
│   ├── guides/
│   │   └── page.tsx
│   ├── projects/
│   │   └── page.tsx
│   └── api/
│
├── components/
│   ├── bento/
│   ├── cards/
│   ├── navigation/
│   ├── search/
│   ├── filters/
│   ├── workshop/
│   └── ui/
│
├── lib/
│   ├── api.ts
│   ├── types.ts
│   └── utils.ts
│
└── styles/
```

---

# 8. Main User Experience

The home page should immediately feel like a living forge.

Instead of a conventional blog:

```text
Header
Hero
Article list
Article list
Article list
Footer
```

use:

```text
Forge Header
      ↓
Featured Forge Knowledge
      ↓
Dynamic Bento Feed
      ↓
Materials / Videos / Guides / Tools
      ↓
Workshop Knowledge
      ↓
Footer
```

---

# 9. Bento Grid

The primary dashboard is a dynamic Bento Grid.

Cards have different sizes depending on importance and media type.

Example:

```text
┌───────────────────────┬───────────────┐
│                       │ Video         │
│ Featured Guide        │               │
│                       ├───────────────┤
│                       │ Material      │
├───────────────┬───────┴───────────────┤
│ Steel         │ Workshop Tip          │
│ Knowledge     │                       │
├───────────────┴───────────────┬───────┤
│ Project / Tutorial            │ Tool  │
│                               │       │
└───────────────────────────────┴───────┘
```

The layout should be responsive.

Desktop:

- Dense information
- Large feature cards
- Multiple columns

Tablet:

- Reduced column count

Mobile:

- Single-column or compact two-column arrangement

---

# 10. Card System

Cards are polymorphic.

Every card has a common shell but a specialized content renderer.

Supported types:

```text
product
video
article
guide
rule
material
project
workshop_tip
reference
```

---

# 11. Product / Gear Cards

A product card may contain:

- Image
- Product name
- Category
- Platform
- Price
- Price timestamp
- Short explanation
- Pros
- Cons
- Suitable for beginner/intermediate/advanced
- Purchase link

Example:

```json
{
  "id": "grinder-001",
  "type": "product",
  "category": "workshop-tools",
  "title": "2x72 Belt Grinder",
  "platform": "Amazon",
  "price": 599.00,
  "currency": "USD",
  "purchase_url": "...",
  "audience": ["intermediate", "advanced"]
}
```

The website must distinguish:

**Product information**

from

**Affiliate/commercial information.**

The site should not pretend that a product is objectively "best" merely because it provides an affiliate opportunity.

---

# 12. Video System — User-Managed YouTube Channels

The video section follows a deliberate **controlled-source architecture**.

Blacksmith Knight should **not use AI to continuously search the internet or YouTube for videos**. The system should gather videos only from a list of YouTube channels selected and maintained by the user.

This makes the video library predictable, inexpensive, transparent, and controllable.

## 12.1 Video Source Principle

```text
User-managed channel list
          ↓
   YouTube Data API
          ↓
     New videos
          ↓
   Normalize metadata
          ↓
      Store video
          ↓
 Optional AI enrichment
          ↓
      Video feed
```

The **channel registry is the source of truth** for video discovery.

The system should never silently add arbitrary YouTube channels simply because an AI model considers them relevant.

## 12.2 Channel Management

The user should have a dedicated **Video Channels / Channel Manager** interface.

Capabilities:

- Add YouTube channel
- Search for a channel
- Add by channel URL or channel ID
- Enable / disable a channel
- Remove a channel
- Mark a channel as favorite or priority
- Assign one or more categories
- Set optional synchronization priority
- View last synchronization time
- View synchronization status
- View number of videos collected
- Manually trigger **Sync Now**
- Trigger **Sync All Channels**

Example UI:

```text
VIDEO CHANNELS

+ Add YouTube Channel       Sync All

● Black Bear Forge          ON
  124 videos · Last sync 2h ago

● Alec Steele               ON
  86 videos · Last sync 2h ago

● Torbjörn Åhman            ON
  51 videos · Last sync 2h ago

○ Example Channel           OFF
```

## 12.3 Channel Data Model

A dedicated channel entity should exist rather than treating channels as ordinary video metadata.

```json
{
  "id": "channel-001",
  "platform": "youtube",
  "youtube_channel_id": "UC...",
  "name": "Example Blacksmith",
  "handle": "@exampleblacksmith",
  "url": "https://www.youtube.com/@exampleblacksmith",
  "thumbnail": "...",
  "enabled": true,
  "priority": 10,
  "categories": ["blacksmithing", "bladesmithing"],
  "last_synced_at": "2026-09-07T05:00:00Z",
  "created_at": "2026-09-01T10:00:00Z"
}
```

## 12.4 Video Metadata

Video cards contain:

- Thumbnail
- Title
- Creator
- Channel
- Duration
- Published date
- Topic/category
- Tags
- Original YouTube URL
- Channel reference
- Optional AI summary
- Optional AI classification
- Optional difficulty
- Optional material/technique tags

Example:

```json
{
  "id": "yt-123",
  "type": "video",
  "youtube_video_id": "abc123",
  "channel_id": "channel-001",
  "title": "Forging a Viking Axe",
  "creator": "Example Blacksmith",
  "duration": 842,
  "published_at": "2026-09-06T18:30:00Z",
  "thumbnail": "...",
  "source": {
    "type": "youtube",
    "url": "https://www.youtube.com/watch?v=abc123"
  },
  "category": "forging",
  "tags": ["axe", "forging", "blacksmithing"],
  "ai": {
    "processed": false
  }
}
```

## 12.5 AI Is Optional Enrichment, Not Discovery

AI may be used after a video has been collected to improve metadata. It should not decide whether the internet should be searched for new channels.

Possible enrichment:

```text
YouTube metadata
      ↓
Optional AI enrichment
      ├── category
      ├── tags
      ├── difficulty
      ├── techniques
      ├── materials mentioned
      └── short summary
```

If AI is disabled, unavailable, or fails, the video must still be usable.

**Video ingestion must never depend on AI availability.**

This is important for cost, reliability, and simplicity.

## 12.6 What the Video Worker Does

The deterministic worker should:

1. Load enabled channels.
2. Query the official YouTube Data API.
3. Fetch the latest videos for each channel.
4. Compare video IDs with existing records.
5. Insert only new videos.
6. Update changed metadata where appropriate.
7. Record synchronization status.
8. Optionally send new videos to AI enrichment.
9. Publish the resulting video records to the API/feed.

No internet-wide video discovery is required.

## 12.7 Video Synchronization

Example schedule:

```text
Every 6 hours
      ↓
Load enabled channels
      ↓
Fetch recent uploads
      ↓
Deduplicate by YouTube video ID
      ↓
Store new videos
      ↓
Optional AI enrichment
```

The actual frequency should respect YouTube API quotas and platform policies.

## 12.8 Video Feed Behavior

The video page can provide:

```text
VIDEOS

[All Channels]
[Blacksmithing]
[Bladesmithing]
[Forging]
[Heat Treatment]
[Grinding]
[Workshop]

Latest from Your Channels

┌────────────┐ ┌────────────┐ ┌────────────┐
│   VIDEO    │ │   VIDEO    │ │   VIDEO    │
│            │ │            │ │            │
└────────────┘ └────────────┘ └────────────┘
```

Users should also be able to filter by a specific channel.

## 12.9 Copyright and Source Handling

Videos should link to the original YouTube source.

Do not download and redistribute copyrighted videos.

The website stores metadata and links/embeds according to applicable platform rules.

## 12.10 Why Controlled Channels Are Preferred

This design provides:

- Lower AI cost
- Predictable API usage
- Better source quality
- User control
- Easier debugging
- Easier moderation
- No noisy internet-wide discovery
- No dependence on AI for basic video collection
- A personal curated video library

Blacksmith Knight is therefore a **curated forge library**, not an autonomous video crawler.

---

# 13. Knowledge / Guide Cards

Guides are central to the project.

Possible topics:

- How an anvil works
- Choosing a forge
- Coal vs gas forge
- Propane forge fundamentals
- Hammer selection
- Tongs
- Steel identification
- Carbon steel
- Stainless steel
- Tool steel
- Heat treatment
- Normalizing
- Hardening
- Tempering
- Quenching
- Grinding
- Sharpening
- Damascus
- Pattern welding
- Rust prevention
- Workshop organization

---

# 14. Material Knowledge System

One of the most important areas should be the **Material Library**.

Each material entry should ideally contain:

```text
Material
├── Composition
├── Carbon content
├── Alloying elements
├── Typical applications
├── Forging characteristics
├── Heat treatment
├── Hardening behavior
├── Tempering
├── Quenching considerations
├── Grinding characteristics
├── Welding considerations
├── Corrosion resistance
├── Availability
├── Beginner suitability
└── Common mistakes
```

Example:

```json
{
  "type": "material",
  "name": "1095",
  "classification": "high-carbon steel",
  "carbon": "approximately 0.95%",
  "tags": [
    "knife-making",
    "high-carbon",
    "heat-treatment"
  ]
}
```

All material data should be treated as technical reference information, not as a substitute for manufacturer data or laboratory testing.

---

# 15. Steel Database

A dedicated steel database should eventually exist.

Potential fields:

```text
Name
AISI designation
EN designation
JIS designation
Carbon
Chromium
Manganese
Silicon
Molybdenum
Vanadium
Nickel
Tungsten
Forging range
Heat-treatment guidance
Typical hardness
Common applications
Availability
Difficulty
Notes
Sources
```

Important:

Do not invent missing metallurgical values.

When exact values matter, show:

- Source
- Approximate range
- Manufacturer specification
- Confidence level

---

# 16. Workshop Tools Library

Create a knowledge section for workshop tools.

Categories:

### Forging

- Anvils
- Hammers
- Tongs
- Punches
- Drifts
- Fullers
- Swages
- Chisels
- Hardy tools
- Power hammers
- Presses

### Heating

- Coal forge
- Coke forge
- Gas forge
- Propane burners
- Refractory
- Insulation
- Thermocouples
- Temperature measurement

### Grinding

- Belt grinders
- Angle grinders
- Bench grinders
- Files
- Abrasives
- Grinding belts
- Wheels

### Finishing

- Files
- Sandpaper
- Buffing equipment
- Polishing
- Etching
- Rust treatment

### Workshop Infrastructure

- Vises
- Workbenches
- Lighting
- Ventilation
- Storage
- Fire extinguishers
- Electrical equipment

---

# 17. Learning Path

The website should not merely show random content.

Create a progression.

## Level 1 — The Apprentice

Topics:

1. Workshop safety
2. Basic tools
3. Forge operation
4. Fire control
5. Heating steel
6. Basic hammer technique
7. Drawing out
8. Upsetting
9. Bending
10. Cutting

## Level 2 — The Smith

Topics:

1. Tongs
2. Punching
3. Drifting
4. Fullering
5. Basic tool making
6. Simple hooks
7. Nails
8. Bottle openers
9. Small tools
10. Basic blades

## Level 3 — The Bladesmith

Topics:

1. Steel selection
2. Grain control
3. Normalizing
4. Hardening
5. Tempering
6. Grinding
7. Edge geometry
8. Handle construction
9. Finishing
10. Testing

## Level 4 — The Craftsperson

Topics:

- Pattern welding
- Damascus
- Complex tooling
- Advanced heat treatment
- Metallurgy
- Power hammer technique
- Press forging
- Tool design
- Experimental metallurgy

---

# 18. Projects Library

The project system should encourage hands-on learning.

Each project should contain:

```text
Project
├── Difficulty
├── Estimated time
├── Required tools
├── Required material
├── Safety considerations
├── Skills learned
├── Steps
├── Troubleshooting
├── Variations
└── Reference material
```

Example projects:

### Beginner

- S-hook
- Nail
- Leaf
- Simple poker
- Bottle opener
- Small hook

### Intermediate

- Fire poker
- Chisel
- Punch
- Tongs
- Small knife

### Advanced

- Axe
- Complex blade
- Damascus billet
- Specialized workshop tool

---

# 19. Workshop Tips

Create a stream of small pieces of knowledge.

Examples:

- Why scale forms
- Why steel cracks during quenching
- Why an edge overheats
- Why a belt grinder pulls material unevenly
- Why an anvil rebounds
- Why tongs slip
- How to read sparks cautiously
- Why forge atmosphere matters

These should be short and highly practical.

---

# 20. Search

Search should eventually operate across the entire knowledge system.

Search targets:

- Articles
- Materials
- Steel
- Tools
- Videos
- Projects
- Rules
- Workshop tips

Example:

```text
Search: "1095"

Results:

Material
├── 1095 steel
├── Heat treatment of 1095
├── 1095 vs 1084
├── 1095 videos
├── 1095 knife projects
└── Related workshop tips
```

---

# 21. Filtering

Filtering should be instantaneous.

Primary filters:

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

Secondary filters:

```text
Beginner
Intermediate
Advanced
Forge
Anvil
Steel
Heat Treatment
Grinding
Knife Making
Bladesmithing
Metallurgy
Workshop
Safety
```

No full-page reload should be required.

---

# 22. Backend

The backend is Python.

The architecture should separate **deterministic ingestion** from **optional AI enrichment**.

```text
                 SOURCE CONFIGURATION
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          YouTube       RSS      Product APIs
          Channels
             │           │           │
             └───────────┼───────────┘
                         ▼
                    Collector
                         ▼
                    Normalizer
                         ▼
                   Deduplicator
                         ▼
                      Rules
                         ▼
                 Optional AI Layer
                         ▼
                  Quality / Validation
                         ▼
                       Storage
                         ▼
                         API
```

The important change is that **not every source needs AI**.

YouTube channel ingestion, duplicate detection, scheduling, database writes, and API operations should be deterministic wherever possible.

---

# 23. Backend Responsibilities

The backend should:

1. Read source configuration.
2. Read `rules.md`.
3. Load the user-managed YouTube channel registry.
4. Fetch external content from approved sources.
5. Normalize source data.
6. Remove duplicates deterministically.
7. Apply source-specific rules.
8. Optionally invoke AI enrichment where it provides value.
9. Validate structured output.
10. Store processed content.
11. Record ingestion and synchronization logs.
12. Expose content to Next.js.

AI should be treated as a processing component, not as the system's primary controller.

---

# 24. YouTube Data Source

Use the official YouTube Data API where available.

Unlike a general web crawler, the YouTube collector operates only on channels present in the **user-managed channel registry**.

```text
Channel Registry
      │
      ├── Enabled channel A
      ├── Enabled channel B
      ├── Disabled channel C
      └── Enabled channel D
               │
               ▼
        YouTube Data API
               │
               ▼
        Recent videos
```

Track:

- YouTube channel ID
- Channel name
- Channel handle
- Channel URL
- Channel thumbnail
- Enabled/disabled state
- Priority
- Categories
- Last synchronization time
- Synchronization status
- Video count

For each video track:

- Video ID
- Title
- Description
- Thumbnail
- Publication date
- Duration
- Channel ID
- Channel name
- Original URL

The collector must:

- Respect API quotas
- Avoid unnecessary repeated requests
- Deduplicate by video ID
- Preserve the original source
- Keep previous data if synchronization fails

There is **no requirement for AI-powered YouTube search**.

---

# 25. RSS

RSS should be the preferred method for websites that provide feeds.

Potential sources:

- Blacksmithing blogs
- Bladesmithing websites
- Metallurgy resources
- Workshop publications
- Tool manufacturers
- Educational websites

The system should:

- Respect feed frequency
- Cache results
- Avoid duplicate downloads
- Preserve source attribution
- Link to original articles

---

# 26. E-Commerce

Product integrations can support:

- Amazon
- AliExpress
- Other legitimate affiliate/product APIs

The system should focus on **useful workshop equipment** rather than turning the website into an online shop.

Examples:

- Hammers
- Tongs
- Files
- Abrasives
- PPE
- Anvils
- Vises
- Grinders
- Forge components
- Measuring tools

Product prices should always be treated as dynamic.

Store:

```text
price
currency
timestamp
source
```

Never present an old price as if it were current.

---

# 27. AI Processing

AI is an editorial assistant, not the ultimate authority.

Pipeline:

```text
Raw item
   ↓
Relevance classification
   ↓
Topic classification
   ↓
Duplicate detection
   ↓
Summary generation
   ↓
Quality assessment
   ↓
Safety assessment
   ↓
Structured output
```

---

# 28. AI Relevance Score

Example:

```text
0.95 - 1.00
Exceptional relevance

0.85 - 0.94
Highly relevant

0.75 - 0.84
Relevant

0.60 - 0.74
Possibly useful

< 0.60
Usually reject
```

The threshold should be configurable.

---

# 29. AI Must Not Hallucinate Technical Facts

This is particularly important for metallurgy.

AI-generated content must not invent:

- Chemical compositions
- Heat-treatment temperatures
- Hardness values
- Material properties
- Safety procedures
- Manufacturer specifications

When technical precision matters, the system should retain source references.

AI can summarize source material, but should not silently turn uncertainty into fact.

---

# 30. Rules Engine

Central configuration:

```text
backend/config/rules.md
```

The rules file governs:

- Topics
- Relevance
- Exclusions
- Safety
- Content quality
- Source quality
- Duplicate handling
- Product criteria
- Editorial priorities

This allows the site's behavior to evolve without rewriting the worker.

---

# 31. Example Rules

```markdown
# Content Rules

## Mission

Prioritize information that helps amateur blacksmiths
learn, practice, understand materials, improve workshops,
and safely enjoy forging.

## Priority Topics

- blacksmithing
- bladesmithing
- forging
- metallurgy
- steel
- heat treatment
- grinding
- abrasives
- anvils
- hammers
- tongs
- workshop construction
- tool making

## Audience

Primary:
- beginners
- hobbyists
- amateur smiths
- DIY makers

Secondary:
- experienced hobbyists

## Reject

Reject content that is:
- unrelated
- spam
- duplicate
- low quality
- primarily advertising
- misleading
- unsafe without appropriate context

## Commercial Policy

Commercial content may be included when it provides
genuine value to hobbyists.

Never rank an item highly solely because it produces
affiliate revenue.
```

---

# 32. Data Model

The data model should distinguish between **sources**, **channels**, and **content items**.

For YouTube, the channel is a first-class entity. Videos reference the channel that produced them.

## 32.1 YouTube Channel Entity

```json
{
  "id": "channel-001",
  "type": "youtube_channel",
  "platform": "youtube",
  "youtube_channel_id": "UC...",
  "name": "Example Blacksmith",
  "url": "https://www.youtube.com/@exampleblacksmith",
  "enabled": true,
  "priority": 10,
  "categories": ["blacksmithing"],
  "last_synced_at": "2026-09-07T05:00:00Z"
}
```

## 32.2 Polymorphic Content Envelope

```json
{
  "id": "unique-id",
  "type": "video",
  "category": "heat-treatment",
  "title": "...",
  "description": "...",
  "image": "...",
  "source": {
    "type": "youtube",
    "url": "..."
  },
  "published_at": "...",
  "tags": [],
  "difficulty": "beginner",
  "ai": {
    "relevance": 0.92
  }
}
```

Each entity can then have specialized fields.

---


---

# 33. Storage

The first version should favor simplicity.

Possible initial storage:

```text
data/
├── raw/
├── processed/
├── feed.json
├── materials.json
├── videos.json
├── products.json
└── articles.json
```

This is suitable for an early hobby project.

As the dataset grows, move to a database.

A future database could use PostgreSQL.

Do not introduce database complexity before it is needed.

---

# 34. API

The backend should expose endpoints such as:

```text
GET /api/feed
GET /api/materials
GET /api/materials/{id}
GET /api/videos
GET /api/products
GET /api/guides
GET /api/projects
GET /api/rules
GET /api/search?q=...
```

Example:

```http
GET /api/feed?category=heat-treatment
```

---

# 35. API Response

Example:

```json
{
  "items": [
    {
      "id": "1095-guide",
      "type": "guide",
      "category": "heat-treatment",
      "title": "Understanding 1095 Heat Treatment",
      "difficulty": "intermediate"
    }
  ],
  "meta": {
    "count": 1,
    "generated_at": "2026-09-07T05:00:00Z"
  }
}
```

---

# 36. Scheduling

The backend worker should run automatically.

Possible environments:

- GitHub Actions
- Lightweight cloud server
- Scheduled container
- Cron
- Serverless scheduled execution

Example schedule:

```text
YouTube channel sync → every 6 hours
RSS                → every 6 hours
Products            → every 12–24 hours
AI enrichment       → only for newly collected/changed items
Full cleanup        → once per day
```

The YouTube job should load only **enabled user-selected channels**.

The actual frequency should respect API limits and source policies.

AI processing should not run over the entire video library on every scheduled job. It should normally process only new or explicitly reprocessed items.

---

# 37. GitHub Actions

Example conceptual pipeline:

```text
Scheduled trigger
       ↓
Install Python
       ↓
Load secrets
       ↓
Load enabled YouTube channels
       ↓
Fetch approved sources
       ↓
Normalize + deduplicate
       ↓
Apply rules
       ↓
Optional AI enrichment
       ↓
Validate data
       ↓
Update storage / database
       ↓
Log results
```

The worker must be able to complete successfully even when the AI service is unavailable, provided deterministic ingestion can continue.

Secrets must never be stored in source code.

Examples:

```text
YOUTUBE_API_KEY
AMAZON_API_KEY
ALIEXPRESS_API_KEY
AI_API_KEY
```

---

# 38. Frontend Performance

The website should feel instant.

Requirements:

- No heavy background processing in browser
- Avoid unnecessary client-side computation
- Use server components where appropriate
- Use client components only when interaction requires them
- Optimize images
- Lazy-load media
- Paginate or virtualize extremely large feeds
- Cache API responses
- Avoid unnecessary animation

---

# 39. Framer Motion

Use animation for craftsmanship and polish.

Examples:

- Card entrance
- Staggered Bento appearance
- Hover lift
- Small image zoom
- Filter transitions
- Modal transitions
- Page transitions where useful

Avoid:

- Constant pulsing
- Excessive glowing
- Large distracting animations
- Animations that make reading slower

---

# 40. Navigation

Primary navigation:

```text
FORGE
MATERIALS
VIDEOS
GUIDES
PROJECTS
WORKSHOP
TOOLS
RULES
```

Possible additional:

```text
SEARCH
ABOUT
```

The navigation should remain simple.

---

# 41. Home Page Sections

Recommended home page:

```text
┌─────────────────────────────────────┐
│ BLACKSMITH KNIGHT                   │
│ FORGING HEAVEN                      │
│                                     │
│ Enter the Forge                     │
└─────────────────────────────────────┘

Featured Knowledge

Dynamic Bento Feed

Latest Forge Videos

Material of the Day

Workshop Tip

Featured Project

Recommended Tools

Beginner's Path

Forge Library

Footer
```

---

# 42. Hero Section

The hero should establish the identity immediately.

Possible copy:

> **ENTER THE FORGE**

> Knowledge, steel, fire and craftsmanship.

> Learn the craft. Understand the material. Build your workshop. Forge your own path.

The hero should not sound like a commercial business.

---

# 43. Content Tone

The tone should be:

- Knowledgeable
- Practical
- Respectful
- Enthusiastic
- Slightly legendary
- Never pretentious

The "Knight" theme can provide personality.

Example:

> **THE APPRENTICE'S NOTE**

> Before you worry about making the perfect blade, learn to control the fire and move the steel.

But technical explanations should remain accurate and clear.

---

# 44. Safety Architecture

Every potentially hazardous guide should support a safety section.

Example:

```text
⚠ SAFETY

This process involves high temperatures and hot metal.

Wear appropriate eye protection.
Keep combustible materials away from the forge.
Provide appropriate ventilation.
Have suitable fire-control equipment available.
Never handle hot steel as though it is cold.
```

Safety information should be context-specific.

---

# 45. Source Attribution

Every externally derived piece of information should retain source metadata.

Example:

```json
{
  "source": {
    "name": "Example Source",
    "url": "...",
    "published_at": "...",
    "retrieved_at": "..."
  }
}
```

For material specifications, sources are particularly important.

---

# 46. Content Quality

The system should prefer:

1. Primary sources
2. Manufacturer technical documents
3. Reputable educational sources
4. Experienced craftspeople
5. Established workshop publications
6. Community discussions as supplementary material

Community content should not automatically be treated as authoritative.

---

# 47. Duplicate Detection

The ingestion pipeline must prevent duplicate content.

Possible duplicate keys:

- Canonical URL
- Video ID
- YouTube channel ID
- Product ID
- Source ID
- Normalized title
- Content fingerprint

Example:

```text
Same YouTube video
→ same video ID
→ one database record
```

---

# 48. Content Lifecycle

Each item should have a state.

```text
discovered
    ↓
normalized
    ↓
evaluated
    ↓
approved
    ↓
published
    ↓
stale
    ↓
archived
```

Products can become stale quickly because prices and availability change.

YouTube videos are normally retained as historical content once collected; their metadata may be refreshed, but a video should not disappear simply because it is no longer new. Disabled channels should normally stop future ingestion without deleting already collected videos unless the user explicitly chooses to remove them.

Knowledge articles generally have a longer lifespan.

---

# 49. Content Categories

Recommended top-level categories:

```text
Blacksmithing
Bladesmithing
Metallurgy
Materials
Heat Treatment
Grinding
Tools
Workshop
Projects
Safety
History
Traditional Craft
Modern Techniques
```

---

# 50. Historical Knowledge

Because of the "Knight" identity, historical blacksmithing can be an important secondary area.

Possible subjects:

- Medieval blacksmithing
- Viking-era forging
- Traditional tools
- Historical anvils
- Historical forge construction
- Traditional fuels
- Sword-making history
- Tool evolution
- Historical metallurgy

Historical information should clearly distinguish:

```text
Historically documented
Likely reconstruction
Modern interpretation
Speculation
```

Avoid presenting popular myths as established history.

---

# 51. Traditional vs Modern

The website can deliberately compare:

```text
Traditional Forge
vs
Modern Gas Forge

Hand Hammer
vs
Power Hammer

Charcoal
vs
Coal
vs
Propane

File Finishing
vs
Belt Grinding

Traditional Heat Judgment
vs
Thermocouple / Temperature Measurement
```

This is especially useful for amateurs deciding how to build their own workshop.

---

# 52. Workshop Builder

A future feature can help users plan a personal workshop.

Inputs:

```text
Available space
Budget
Indoor/outdoor
Fuel
Noise tolerance
Power availability
Primary projects
Skill level
```

Output:

```text
Suggested basic setup
Essential tools
Optional tools
Safety equipment
Suggested progression
```

This should remain educational rather than functioning as a commercial sales funnel.

---

# 53. Beginner Workshop Philosophy

The website should repeatedly communicate:

> You do not need an expensive workshop to begin learning.

A beginner setup can be discussed in tiers.

### Minimal

- Hammer
- Suitable anvil/suitable striking surface
- Tongs
- Forge
- PPE
- Basic hand tools

### Developing

- Better anvil
- More hammers
- Vise
- Files
- Grinder
- Measuring tools

### Advanced Hobby Workshop

- Belt grinder
- Power hammer or press
- Heat-treatment equipment
- Better ventilation
- Dedicated tooling
- Specialized tooling

---

# 54. Product Recommendation Philosophy

Product recommendations should be evaluated on:

```text
Quality
Price
Durability
Suitability
Beginner friendliness
Availability
Repairability
Value
```

Not simply:

```text
Highest price = best
```

The site should be comfortable saying:

> A cheaper tool may be entirely adequate for a hobbyist.

---

# 55. Community — Future Possibility

A community system could eventually include:

- User projects
- Workshop photographs
- Build logs
- Questions
- Comments
- Project journals

However, this should **not** be part of the first MVP.

The first version should focus on becoming an excellent knowledge resource.

---

# 56. User Accounts

Not required for the first version.

Potential future features:

- Saved projects
- Favorite materials
- Saved articles
- Workshop profile
- Personal learning path
- Personal tool inventory
- Notes

---

# 57. Personal Workshop Journal

A future feature could allow:

```text
Project
├── Photos
├── Material used
├── Heat-treatment cycle
├── Problems
├── What worked
├── What failed
└── Lessons learned
```

This would make the site useful as a personal craft notebook.

---

# 58. Responsible Content Policy

The site is about **craftsmanship and education**.

Content involving blades, historical weapons, or forging should be presented primarily through:

- Materials
- Craft
- Metallurgy
- History
- Toolmaking
- Workshop technique
- Safety
- Responsible personal use

Avoid turning the platform into a source for harmful instructions or glorification of violence.

---

# 59. Accessibility

The site must remain accessible.

Requirements:

- Strong text contrast
- Keyboard navigation
- Meaningful alt text
- Focus indicators
- Semantic HTML
- Reduced-motion support
- Readable typography
- Avoid relying on color alone
- Mobile-friendly controls

The dark theme must not sacrifice readability.

---

# 60. Responsive Design

## Desktop

Use the full Bento experience.

## Tablet

Reduce:

- Card size
- Navigation width
- Number of columns

## Mobile

Prioritize:

```text
Title
Image
Summary
Category
Action
```

Cards should remain easy to read.

---

# 61. SEO

The knowledge portion should be search-engine friendly.

Each guide/material/project should have:

- Unique title
- Description
- Canonical URL
- Structured metadata
- Relevant headings
- Internal links
- Source references

Example:

```text
/knowledge/materials/1095
/guides/heat-treatment/normalizing
/projects/beginner/s-hook
/tools/anvils
```

---

# 62. Internal Linking

Knowledge should form a graph.

Example:

```text
1095
 ↓
Heat Treatment
 ↓
Hardening
 ↓
Quenching
 ↓
Tempering
 ↓
Grinding
 ↓
Knife Project
```

A user should naturally discover related information.

---

# 63. Recommendation Engine

Initially use deterministic rules.

Example:

```text
If user reads:
"1095"

Recommend:
- 1095 heat treatment
- 1095 vs 1084
- hardening fundamentals
- quenching
- beginner blade projects
```

AI can later improve recommendations.

---

# 64. Search Ranking

Possible ranking:

```text
Exact title match
+
Topic relevance
+
Source quality
+
Content quality
+
Freshness
+
User interest
```

Avoid ranking solely by popularity.

---

# 65. Data Freshness

Different data types require different refresh policies.

```text
Products       → high frequency
Videos         → medium/high for enabled channels; metadata refresh as needed
RSS articles   → medium
Material specs → low
Historical info → very low
Guides         → manual/editorial
```

---

# 66. Editorial Override

The system should allow manually marking content:

```text
featured
pinned
verified
needs_review
hidden
```

This prevents automated processing from having total control over the homepage.

---

# 67. Verification

Technical articles can have a status:

```text
Community
AI summarized
Source backed
Reviewed
Verified
```

Do not claim "verified" unless a defined verification process actually occurred.

---

# 68. Logging

The worker should log:

```text
Run started
Source fetched
Items discovered
Items rejected
Items duplicated
Items approved
AI failures
API failures
Storage changes
Run completed
```

Example:

```text
2026-09-07 05:00
YouTube:
  38 discovered
  11 relevant
  4 duplicates
  23 rejected

RSS:
  21 discovered
  9 relevant
```

---

# 69. Error Handling

A failed source must not destroy the feed.

Example:

```text
YouTube API unavailable
       ↓
Log error
       ↓
Keep previous YouTube content
       ↓
Process remaining sources
       ↓
Complete worker
```

Partial failure should be normal.

---

# 70. Secrets

Never put API keys in:

```text
Git
JSON
Frontend code
Public environment variables
Logs
```

Use environment variables or a secrets manager.

---

# 71. Development Environment

Recommended:

```text
Node.js
npm
Python 3.x
Git
VS Code
```

Run locally:

```text
Frontend
http://localhost:3000

Backend API
http://localhost:8000
```

---

# 72. Development Phases

## Phase 1 — Visual Prototype

Build:

- Header
- Hero
- Bento grid
- Cards
- Navigation
- Filters
- Responsive layout

Use static JSON.

Goal:

**Make the website feel like Forging Heaven.**

---

## Phase 2 — Real Backend

Build:

- Python API
- Feed endpoint
- Material endpoint
- Video endpoint
- Product endpoint

---

## Phase 3 — Controlled Ingestion

Add:

- YouTube channel registry
- User channel management UI
- YouTube Data API collector
- RSS
- Product APIs
- Deterministic deduplication
- Source synchronization logs

For YouTube, only user-enabled channels are collected.

---

## Phase 4 — Optional AI Enrichment

Add AI only where it provides real value:

- Content classification
- Relevance scoring for sources where needed
- Summaries
- Tag extraction
- Technical-content assistance
- Metadata enrichment

YouTube discovery is **not** an AI task.

Video ingestion must work without AI.

---

## Phase 5 — Automation

Add:

- Cron/GitHub Actions
- Scheduled processing
- Logging
- Error recovery

---

## Phase 6 — Knowledge Library

Build:

- Steel database
- Material library
- Workshop library
- Project library
- Heat-treatment reference
- Tool encyclopedia

---

## Phase 7 — Personal Features

Potentially add:

- Favorites
- Personal notes
- Workshop journal
- Saved projects
- Personal learning path

---

# 73. MVP Definition

The MVP is successful when a visitor can:

1. Open the website.
2. Immediately understand the blacksmithing theme.
3. Browse the Bento feed.
4. Filter by category.
5. Open a technical guide.
6. Browse materials.
7. Watch/link to relevant videos.
8. Explore tools.
9. Search knowledge.
10. Browse videos from configured channels.
11. Add, disable, and manage YouTube channels.
12. Discover beginner projects.
13. Read safety information.
14. Navigate naturally between related topics.

The MVP does **not** require:

- User accounts
- Community
- Comments
- Messaging
- Payments
- Full e-commerce
- Complex personalization
- Mobile app

---

# 74. Example Unified Feed

```json
{
  "items": [
    {
      "id": "material-1095",
      "type": "material",
      "category": "materials",
      "title": "1095 Steel",
      "difficulty": "intermediate",
      "tags": ["steel", "carbon-steel", "bladesmithing"]
    },
    {
      "id": "video-001",
      "type": "video",
      "category": "forging",
      "title": "Forging a Small Axe",
      "difficulty": "intermediate",
      "source": {
        "type": "youtube"
      }
    },
    {
      "id": "guide-001",
      "type": "guide",
      "category": "heat-treatment",
      "title": "Understanding Normalizing",
      "difficulty": "beginner"
    },
    {
      "id": "tool-001",
      "type": "product",
      "category": "tools",
      "title": "Forging Hammer",
      "platform": "Amazon"
    }
  ]
}
```

---

# 75. Example Homepage Logic

```text
Fetch feed
    ↓
Include videos only from enabled channels
    ↓
Sort by editorial relevance
    ↓
Mix content types
    ↓
Prioritize fresh content
    ↓
Insert featured knowledge
    ↓
Render Bento
```

Do not simply display:

```text
latest item
latest item
latest item
latest item
```

The feed should feel curated.

---

# 76. Long-Term Knowledge Architecture

The ultimate site should become a connected knowledge graph.

```text
                     BLACKSMITHING
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
     MATERIALS          FORGING           WORKSHOP
        │                  │                  │
      STEEL             HAMMERS             FORGE
        │                  │                  │
  HEAT TREATMENT        ANVILS             GRINDER
        │                  │                  │
 HARDENING              TONGS             SAFETY
        │
   TEMPERING
        │
     PROJECTS
        │
    BLADES / TOOLS
```

This is the ultimate value of the website.

It should not merely collect links.

It should help users **understand how everything connects**.

---

# 77. "Forge Heaven" Experience

The site should periodically present special editorial modules.

Examples:

### Forge of the Day

A selected workshop, forge, tool, or technique.

### Steel of the Day

A material profile.

### Hammer Lesson

One practical forging technique.

### Workshop Wisdom

A concise practical tip.

### Apprentice Challenge

A beginner project.

### Old Master's Notebook

Historical or traditional technique.

### Metallurgy Corner

A deeper technical explanation.

These features provide personality without turning the site into social media.

---

# 78. Content Balance

The homepage should balance:

```text
40% Practical knowledge
20% Materials / metallurgy
15% Videos
10% Projects
10% Tools / equipment
5% History / culture
```

These percentages are starting targets, not rigid rules.

The actual distribution should be configurable.

---

# 79. Avoiding Information Overload

Although the goal is comprehensive knowledge, the interface should not dump everything on beginners.

Use progressive disclosure:

```text
Simple explanation
      ↓
Practical explanation
      ↓
Technical details
      ↓
References
```

Example:

### What is tempering?

**Simple:**
Tempering reduces some of the brittleness created during hardening.

**Practical:**
After hardening, steel may be very hard but too brittle for practical use. Tempering changes the balance between hardness and toughness.

**Technical:**
Detailed metallurgical discussion follows.

---

# 80. Trust Model

Every technical statement should belong to one of these categories:

```text
Fact
Source-backed recommendation
Craft practice
Personal experience
Historical interpretation
AI summary
Opinion
```

This distinction builds trust.

---

# 81. Future Advanced Features

Potential future systems:

- Steel comparison tool
- Heat-treatment calculator
- Forge fuel comparison
- Hammer weight guide
- Anvil selection guide
- Abrasive selection assistant
- Workshop planner
- Project difficulty estimator
- Personal project journal
- Material cost calculator
- Learning progress tracker
- Source credibility system
- AI knowledge assistant

Any calculator involving safety-critical or metallurgical values should clearly identify assumptions and sources.

---

# 82. Design Rules

The design must follow:

```text
Dark
Industrial
Warm
Technical
Craft-oriented
Readable
Minimal clutter
Strong typography
Controlled animation
Excellent imagery
```

Avoid:

```text
Generic SaaS appearance
Bright white dashboards
Corporate blue
Excessive rounded cards
Gaming UI
Overly medieval fantasy
Aggressive sales banners
Pop-up overload
```

The medieval/knight identity should be **atmospheric**, not childish fantasy.

---

# 83. Final Product Identity

Blacksmith Knight — Forging Heaven should feel like:

> **A blacksmith's workshop combined with an engineering library.**

It should be:

- A place to learn
- A place to research
- A place to discover
- A place to compare tools
- A place to understand steel
- A place to find projects
- A place to watch excellent craftsmen
- A place to improve a workshop
- A place to record personal experiments
- A place to appreciate the history of the craft

Most importantly:

> **It should make people want to go to their workshop and make something.**

---

# 84. Final Architectural Summary

```text
                     BLACKSMITH KNIGHT
                      FORGING HEAVEN
                            │
                            ▼
                  ┌──────────────────┐
                  │    Next.js UI    │
                  │    Bento Grid    │
                  └────────┬─────────┘
                           │
                           ▼
                     JSON / REST API
                           │
                           ▼
                  ┌──────────────────┐
                  │   Python API     │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Database / Data  │
                  │    Storage       │
                  └────────┬─────────┘
                           ▲
                           │
                  ┌────────┴────────┐
                  │ Ingestion Layer │
                  └────────┬────────┘
                           │
          ┌────────────────┼─────────────────┐
          ▼                ▼                 ▼
   YouTube Channels       RSS          Product APIs
          │
          │ ONLY channels
          │ selected/enabled
          │ by user
          ▼
     YouTube Videos
          │
          ▼
   Optional AI Enrichment
          │
          └───────────────┐
                          ▼
                    Rules / Quality
                          │
                          ▼
                       Storage
```

### Architectural Principle

The system has three distinct responsibilities:

```text
DETERMINISTIC SOFTWARE
├── scheduling
├── API calls
├── channel management
├── deduplication
├── database operations
├── validation
└── logging

AI
├── optional classification
├── optional summaries
├── optional tagging
├── optional technical enrichment
└── difficult reasoning when justified

USER
├── chooses trusted YouTube channels
├── enables/disables sources
├── controls editorial preferences
└── ultimately controls the personal library
```

AI should not be allowed to replace simple deterministic software when deterministic software is cheaper, more reliable, and easier to test.

---

# 85. The Core Principle

The project should always return to one question:

> **Does this make Blacksmith Knight a better place for an amateur to learn and enjoy blacksmithing?**

If yes, build it.

If it primarily serves advertising, unnecessary complexity, vanity features, or commercial users, reconsider it.

The ultimate objective is not to create another content website.

It is to create a **living digital forge and knowledge library for people who love working with fire, steel, tools, and their own hands.**

---

# 86. Recommended Initial Build

The first implementation should be:

```text
NEXT.JS
+
TAILWIND
+
FRAMER MOTION
+
PYTHON API
+
STATIC JSON
+
POLYMORPHIC BENTO CARDS
+
MATERIAL LIBRARY
+
VIDEO FEED + USER-MANAGED YOUTUBE CHANNELS
+
PROJECT LIBRARY
+
RULES.MD
```

Only after this foundation feels right should external APIs and autonomous workers be connected.

This keeps the architecture simple, testable, and enjoyable to develop while leaving room for the full Forging Heaven vision.

---



# 88. Controlled External Source Architecture — No Open Web Crawling

This is a core architectural rule for Blacksmith Knight — Forging Heaven.

> **Blacksmith Knight does not perform unrestricted web crawling or autonomous source discovery.**

External information enters the system through explicitly configured and approved sources. The user controls the source registry. Deterministic collectors acquire the data. AI may optionally enrich, classify, summarize, tag, or reason about content after acquisition, but AI is not the mechanism used to discover arbitrary external content.

## 88.1 Three Controlled Source Families

```text
SOURCE REGISTRY
│
├── YouTube Channels
│
├── RSS Feeds
│
└── Shop / Product API Sources
```

Each source family has its own collector and configuration, but all follow the same pipeline:

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
DATABASE
        ↓
NEXT.JS FEED
```

The architecture deliberately separates **acquisition** from **intelligence**. This makes the system predictable, testable, inexpensive, and transparent.

---

## 88.2 YouTube — User-Managed Channel Registry

YouTube is a controlled source system. The user explicitly adds channels that should become part of the Blacksmith Knight library.

```text
User-managed YouTube channels
        ↓
Official YouTube Data API
        ↓
New / changed videos
        ↓
Normalize + deduplicate
        ↓
Store
        ↓
Optional AI enrichment
```

The system must never silently add a channel because an AI model believes it is relevant.

The channel manager should support:

- Add channel by URL
- Add channel by channel ID
- Search/resolve a channel before adding it
- Enable / disable
- Remove
- Priority
- Categories
- Last synchronization time
- Synchronization status
- Number of collected videos
- Sync Now
- Sync All

AI can optionally extract topics, techniques, materials, difficulty, and summaries from available metadata. Video ingestion must remain functional when AI is unavailable.

---

## 88.3 RSS — User-Managed Knowledge Sources

RSS follows exactly the same philosophy as YouTube. RSS is **not** a license to crawl the open web.

The user maintains an approved list of feeds from trusted blacksmithing, bladesmithing, metallurgy, toolmaking, workshop, historical, and related sources.

```text
Approved RSS feed registry
        ↓
RSS collector
        ↓
Feed entries
        ↓
Normalize
        ↓
Deduplicate
        ↓
Rules / relevance validation
        ↓
Optional AI enrichment
        ↓
Knowledge database
```

### RSS Source Registry

Each feed should have a first-class source record:

```json
{
  "id": "rss-001",
  "name": "Example Blacksmithing Site",
  "feed_url": "https://example.com/feed.xml",
  "website_url": "https://example.com",
  "category": ["blacksmithing", "tools"],
  "enabled": true,
  "priority": 10,
  "last_checked_at": null,
  "last_success_at": null,
  "last_error": null
}
```

### RSS Manager

The application should eventually provide:

- Add RSS feed
- Test feed
- Enable / disable
- Edit metadata
- Set priority
- Assign categories
- Remove feed
- Sync Now
- View last successful sync
- View errors
- View number of imported entries

### RSS Rules

The collector should only read configured feeds. It should not:

- Search Google for new sites
- Search YouTube for related articles
- Follow arbitrary links to discover more sources
- Ask an AI agent to find websites automatically
- Crawl entire websites looking for content

An RSS article may contain a link to its original article. That link is metadata/source attribution, not permission for unrestricted crawling. If later processing requires the full article, the implementation must use an explicitly supported and permitted retrieval mechanism.

AI may classify an imported article, summarize its supplied content, identify topics, extract techniques/materials, and assign tags. AI does not decide that a new website should automatically become a source.

---

## 88.4 Shops and Products — Approved Product Sources, Not Crawling

The product system must also avoid unrestricted crawling.

Blacksmith Knight should not run an AI agent that continuously searches Amazon, AliExpress, Google Shopping, supplier websites, or the general web for products.

Instead, products enter through explicitly configured and permitted integrations such as:

- Official product APIs
- Official affiliate APIs
- Merchant/product feeds
- Approved partner integrations
- Other explicitly permitted structured data sources

```text
Approved shop/API source
        ↓
Product collector
        ↓
Normalize product data
        ↓
Deduplicate
        ↓
Deterministic relevance/filter rules
        ↓
Optional AI enrichment
        ↓
Product database
        ↓
Shop cards
```

### Product Source Registry

Each shop integration should be represented as a first-class source rather than hard-coded throughout the application.

Example:

```json
{
  "id": "shop-001",
  "name": "Example Shop",
  "platform": "amazon",
  "source_type": "api",
  "enabled": true,
  "priority": 10,
  "categories": ["tools", "abrasives"],
  "last_synced_at": null,
  "status": "not_configured"
}
```

The exact integration depends on the platform and the access available to the project. The architecture must never assume that scraping is acceptable merely because a website is publicly visible.

### Product Data

A product record can contain:

- Product ID
- Source/shop ID
- Product URL
- Product title
- Manufacturer/brand
- Image URL
- Current price when supplied by the source
- Currency
- Availability when supplied by the source
- Category
- Product specifications
- Source update timestamp
- Affiliate/reference metadata where applicable
- Relevance score
- Optional AI tags
- Optional AI summary

### Deterministic Filtering Comes First

Before AI is used, ordinary software should handle:

- Category filtering
- Missing required fields
- Duplicate products
- Duplicate URLs
- Source availability
- Price parsing
- Currency handling
- Timestamp handling
- Basic blacksmithing relevance rules
- Disabled sources
- Source/API failures

AI should only be used when it provides additional value, for example determining whether an unusual tool is genuinely relevant to blacksmithing or extracting useful characteristics from messy structured descriptions.

### Commercial Philosophy

The site is an amateur/personal knowledge platform, not a commercial marketplace. Product cards should therefore serve the maker's needs rather than drive the architecture.

Commercial links should be transparent and secondary to knowledge. The system should never distort technical recommendations simply because a product has an affiliate relationship.

---

## 88.5 Unified Source Management

The administration/settings area should expose the three source families clearly:

```text
SOURCE MANAGEMENT
│
├── Video Sources
│   └── YouTube Channels
│
├── Knowledge Sources
│   └── RSS Feeds
│
└── Product Sources
    └── Shop / API Integrations
```

A future unified source dashboard can show:

| Source | Type | Enabled | Priority | Last Sync | Status | Items |
|---|---|---:|---:|---|---|---:|
| Blacksmith channel | YouTube | Yes | 10 | recent | Healthy | 124 |
| Trusted workshop blog | RSS | Yes | 8 | recent | Healthy | 86 |
| Product provider | API | Yes | 5 | recent | Healthy | 312 |

The dashboard is an operational control panel, not a content-discovery engine.

---

## 88.6 Collector Architecture

Collectors should be independent Python modules with a common interface.

```text
backend/
└── ingestion/
    ├── youtube/
    │   ├── client.py
    │   ├── collector.py
    │   └── normalizer.py
    │
    ├── rss/
    │   ├── collector.py
    │   └── normalizer.py
    │
    └── shops/
        ├── base.py
        ├── amazon.py
        ├── aliexpress.py
        └── normalizer.py
```

The shop modules are adapters. The rest of the application should not need to know the details of a particular provider.

Conceptually:

```python
class SourceCollector:
    def sync(self, source):
        raise NotImplementedError
```

Each collector should return normalized records and synchronization information.

---

## 88.7 Deterministic Pipeline vs AI Pipeline

The system should maintain a hard boundary between deterministic infrastructure and AI reasoning.

### Deterministic Software

Responsible for:

- Scheduling
- Authentication
- API requests
- RSS retrieval
- Pagination
- Rate limits
- Retries
- Source configuration
- Channel/feed/shop management
- Deduplication
- Database writes
- Data validation
- Price/timestamp handling
- Logging
- Failure detection
- Sync history

### AI

Responsible only where useful for:

- Classification
- Tagging
- Summarization
- Topic extraction
- Difficulty estimation
- Technique/material extraction
- Semantic relevance judgments
- Resolving difficult classification cases
- Technical enrichment when justified

### User

Controls:

- Trusted sources
- Enabled/disabled sources
- Priorities
- Categories
- Editorial preferences
- Commercial preferences
- What belongs in the personal library

> **AI must not replace deterministic software when deterministic software is cheaper, more reliable, and easier to test.**

---

## 88.8 No-Crawling Policy

This policy should be encoded in the project's permanent rules documentation.

### Forbidden by default

- Autonomous web crawling
- AI-generated source discovery
- Searching the entire internet for content
- Unbounded link following
- Scraping arbitrary product pages
- Automatically adding unknown websites
- Automatically adding unknown YouTube channels
- Using AI as a general-purpose web crawler

### Allowed

- User-configured YouTube channels
- User-configured RSS feeds
- Approved APIs
- Approved product feeds
- Explicitly supported partner integrations
- Direct user-provided URLs when the corresponding retrieval mechanism permits them

This policy is important both technically and philosophically: **Blacksmith Knight is a curated forge, not an uncontrolled internet scraper.**

---

## 88.9 Source Lifecycle

Every source should have a lifecycle:

```text
DISCOVERED BY USER
       ↓
CONFIGURED
       ↓
TESTED
       ↓
ENABLED
       ↓
SYNCHRONIZED
       ↓
MONITORED
       ↓
DISABLED / REMOVED
```

A source that repeatedly fails should be marked unhealthy and reported to the user rather than silently replaced by another source.

The system should preserve source identity and synchronization history so that failures can be diagnosed.

---

## 88.10 Freshness and Scheduling

Different source types can have different schedules.

Example starting policy:

```text
YouTube channels   → every few hours
RSS feeds          → every few hours
Product sources    → source-dependent
Manual Sync        → available for all sources
```

These are configurable values, not hard-coded requirements. The scheduler should respect source priority and provider rate limits.

GitHub Actions or another scheduled worker can execute the collectors. The scheduler should never require an AI model to decide whether a routine synchronization should happen.

---

## 88.11 Provenance and Trust

Every imported record must retain its source.

```text
content
  ├── source_type
  ├── source_id
  ├── source_name
  ├── source_url
  ├── imported_at
  └── source_updated_at
```

This allows the user to understand:

- Where information came from
- When it was imported
- Which source supplied it
- Whether it was AI-enriched
- Whether the original source can be opened

The system should distinguish clearly between:

```text
SOURCE FACT
AI INTERPRETATION
EDITORIAL JUDGMENT
USER PREFERENCE
```

AI summaries must never be presented as if they were original source text.

---

## 88.12 Failure Handling

External systems fail. The architecture must assume this.

A failed source should not stop the entire ingestion system.

```text
Source A fails ──┐
Source B works ──┼──→ continue synchronization
Source C works ──┘
```

Each source should have independent:

- Timeout
- Retry policy
- Error state
- Last successful sync
- Last failed sync
- Error message
- Item count

AI failure should also never prevent deterministic ingestion.

```text
Collector works
      ↓
Store record
      ↓
AI unavailable?
      ↓
Keep record + mark enrichment pending
```

---

## 88.13 Updated Architecture Diagram

```text
                         BLACKSMITH KNIGHT
                          FORGING HEAVEN
                                │
                                ▼
                       ┌─────────────────┐
                       │   USER CONTROL  │
                       │ Trusted Sources │
                       └────────┬────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
       YouTube Channels      RSS Feeds       Shop/API Sources
              │                 │                 │
              ▼                 ▼                 ▼
       YouTube Collector    RSS Collector    Product Collector
              │                 │                 │
              └─────────────────┼─────────────────┘
                                ▼
                         NORMALIZATION
                                │
                                ▼
                         DEDUPLICATION
                                │
                                ▼
                       RULES / VALIDATION
                                │
                                ▼
                     OPTIONAL AI ENRICHMENT
                                │
                                ▼
                         DATABASE / JSON
                                │
                                ▼
                         PYTHON API / REST
                                │
                                ▼
                         NEXT.JS BENTO UI
```

The critical point is that **AI sits after controlled acquisition, not before it**.

---

## 88.14 Updated Project Structure

```text
project/
├── frontend/
│   └── Next.js application
│
├── backend/
│   ├── api/
│   ├── worker/
│   │   ├── scheduler.py
│   │   ├── ingestion/
│   │   │   ├── youtube/
│   │   │   ├── rss/
│   │   │   └── shops/
│   │   ├── processing/
│   │   │   ├── relevance.py
│   │   │   ├── normalizer.py
│   │   │   └── ai_enrichment.py
│   │   └── storage/
│   │
│   ├── config/
│   │   ├── rules.md
│   │   ├── source_rules.md
│   │   ├── content_rules.md
│   │   ├── product_rules.md
│   │   └── editorial_style.md
│   │
│   └── data/
│
└── .github/
    └── workflows/
        └── content-worker.yml
```

---

## 88.15 Architectural Decision Record

**Decision:** Use controlled source registries rather than unrestricted crawling.

**Reason:**

- Better source quality
- User control
- Predictable cost
- Easier testing
- Easier debugging
- Better provenance
- Fewer irrelevant results
- Lower legal/operational risk
- Better alignment with a personal knowledge library
- Clear separation between data acquisition and AI reasoning

**Consequence:** The quality of the library depends partly on the quality of the source list. This is intentional. The system should make adding and maintaining good sources easy rather than attempting to discover everything automatically.

---

## 88.16 Final Source Philosophy

Blacksmith Knight should behave like a knowledgeable librarian in a blacksmith's workshop.

It should not wander the internet collecting everything it can find.

Instead:

```text
USER
  ↓
"I trust this channel."
"I trust this RSS feed."
"Use this product provider."
  ↓
BLACKSMITH KNIGHT
  ↓
Collect reliably
  ↓
Organize intelligently
  ↓
Enrich when useful
  ↓
Preserve provenance
  ↓
Present the best material
```

That principle should remain true even if the project eventually grows into a very sophisticated multi-agent system.

**More AI must never mean less control.**

---

# 89. Revision Notes — Controlled Sources for YouTube, RSS and Shops

**Document revision:** 3.0 — Unified Controlled Source Architecture

**Revision date:** 2026-09-07

This revision expands the controlled-source decision previously established for YouTube to the entire external-content architecture.

The project now formally defines three controlled source families:

1. User-managed YouTube channels
2. User-managed RSS feeds
3. Approved shop/product API or feed integrations

The central rule is:

> **Blacksmith Knight does not perform unrestricted web crawling. External content enters through explicitly configured sources. Deterministic collectors acquire and normalize it; AI optionally enriches it afterward.**

This is now a fundamental architectural requirement rather than an implementation detail.


# 87. Revision Notes — Controlled Video Source Architecture

This revision introduces a major architectural decision for the video section:

> **Blacksmith Knight does not perform open-ended AI video discovery.**

Videos are collected from a user-managed registry of known YouTube channels. The user can add, enable, disable, prioritize, or remove channels. The backend uses the official YouTube Data API to collect their videos.

AI may optionally enrich newly collected videos with tags, summaries, categories, difficulty, materials, or techniques, but AI is never required for basic video ingestion.

This decision reduces cost, improves reliability, makes the source set transparent, avoids unnecessary crawling, and keeps the site aligned with its purpose as a **personal curated blacksmithing knowledge forge**.

**Document revision:** 2.0 — Controlled Video Sources
**Revision date:** 2026-09-07
