# Blacksmith Knight Forging Heaven --- UI/UX Redesign Specification

## Document Purpose

This document defines the complete visual redesign direction for the
**Blacksmith Knight Forging Heaven** website.

The existing application is functional and the current information
architecture is already useful. The primary problem is not
functionality. The primary problem is that the visual presentation
currently looks like a generic dark technical/documentation website.

The new goal is:

> **Keep the existing functionality and transform the frontend into a
> distinctive modern blacksmithing experience.**

The visual reference supplied for this redesign is a dark blacksmith
forge scene with:

-   forged iron
-   anvil
-   hammer
-   hot orange steel
-   sparks
-   deep black surroundings
-   warm firelight
-   industrial workshop atmosphere

The website should feel like a **modern digital workshop built around
the craft of blacksmithing**, not like a generic software dashboard.

------------------------------------------------------------------------

# 1. Core Design Vision

## 1.1 Target feeling

The website should communicate these qualities immediately:

-   Blacksmithing
-   Craftsmanship
-   Fire
-   Forged steel
-   Workshop
-   Knowledge
-   Apprenticeship
-   Practicality
-   Technical credibility
-   Exploration
-   Modern usability

The desired visual formula is:

**Dark forged iron + fire orange + photography + clean modern
typography + subtle industrial details**

The site should be atmospheric but still highly readable.

## 1.2 Design principle

Do not turn the website into a fantasy game UI.

Avoid:

-   medieval fantasy styling
-   excessive flames
-   excessive orange
-   decorative fonts everywhere
-   fake metal effects on every element
-   glowing neon interfaces
-   unnecessary animations
-   visual clutter

The desired style is:

> **Modern technical website inside a blacksmith's workshop.**

------------------------------------------------------------------------

# 2. Current UI Assessment

The current homepage already has several good qualities:

-   clear navigation
-   strong headline
-   logical content hierarchy
-   dark background
-   readable text
-   clear Forge Pillars section
-   simple cards
-   useful footer
-   functional buttons
-   reasonable information density

However, it currently feels too much like:

> Dark developer documentation / technical portal

instead of:

> Blacksmithing knowledge platform / digital forge.

## 2.1 Main problems to solve

### Problem 1 --- Too much flat dark space

The background is mostly a flat dark color.

### Solution

Introduce controlled visual depth:

-   hero photography
-   subtle metal texture
-   gradients
-   image-backed cards
-   shadows
-   layered surfaces
-   controlled orange light

------------------------------------------------------------------------

### Problem 2 --- Cards are visually identical

The six Forge Pillars currently look like repeated documentation boxes.

### Solution

Create several card variants:

-   image card
-   video card
-   knowledge card
-   feature card
-   large bento card
-   compact information card

Not every card should look identical.

------------------------------------------------------------------------

### Problem 3 --- The homepage has no strong visual centerpiece

The current hero is primarily text inside a dark rectangle.

### Solution

Make the hero the main visual statement of the website.

Use a large blacksmith/forge photograph with a dark readability overlay.

------------------------------------------------------------------------

### Problem 4 --- Orange is used mostly as an accent

Orange should remain an accent, but it should also visually represent
the site's "fire" identity.

Use orange as:

-   active navigation indicator
-   button accent
-   hover glow
-   section label
-   small icon
-   border highlight
-   ember effect
-   hot-steel visual cue

Do not make large areas orange.

------------------------------------------------------------------------

# 3. Color System

Create a centralized design-token system.

Do not scatter arbitrary colors through components.

If using Tailwind CSS, define the project's visual tokens centrally.
Tailwind supports theme variables for colors, typography, spacing,
shadows and related design tokens, making this approach appropriate for
a consistent visual system.

Reference: Tailwind theme variables documentation:
https://tailwindcss.com/docs/theme

## 3.1 Primary palette

Recommended starting palette:

  Token          Color       Purpose
  -------------- ----------- ------------------------
  Forge Black    `#080807`   global page background
  Charcoal       `#11110F`   major surfaces
  Dark Iron      `#191917`   cards
  Iron           `#292824`   secondary surfaces
  Forged Steel   `#45423C`   borders/details
  Steel Gray     `#706B62`   secondary text
  Ash            `#A9A39A`   muted text
  Forge White    `#F1EEE8`   primary text
  Fire Orange    `#FF5722`   primary accent
  Hot Iron       `#FF7A32`   hover/highlight
  Ember          `#C83B12`   dark orange accent

## 3.2 Color rules

### Background

Use:

`#080807`

for the global page.

### Surface

Use:

`#11110F`

for major sections.

### Card

Use:

`#191917`

with a subtle border.

### Primary text

Use:

`#F1EEE8`

### Secondary text

Use:

`#A9A39A`

### Accent

Use:

`#FF5722`

### Important rule

Orange should normally occupy a small percentage of the screen.

The page should remain predominantly:

-   black
-   charcoal
-   iron
-   gray

with orange appearing like **fire inside a dark forge**.

------------------------------------------------------------------------

# 4. Global Background

## 4.1 Base background

The entire site should have a very dark forged-metal base.

Example conceptual layering:

``` text
Base:
#080807

+
very subtle radial gradient

+
very subtle iron texture

+
occasional section-specific photography
```

## 4.2 Do not use strong texture everywhere

Texture should be almost invisible at normal viewing distance.

The user should feel:

> "This feels like iron."

not:

> "There is a metal texture behind the text."

------------------------------------------------------------------------

# 5. Hero Section

The hero is the most important redesign.

## 5.1 Target layout

Use a large visual hero.

Concept:

``` text
---------------------------------------------------------
|                                                       |
|              FORGE PHOTOGRAPH                         |
|                                                       |
|      BLACKSMITH KNIGHT                                |
|      FORGING HEAVEN                                   |
|                                                       |
|      Knowledge. Steel. Fire. Craftsmanship.           |
|                                                       |
|      Digital workshop and reference for               |
|      modern blacksmiths and apprentices.              |
|                                                       |
|      [ ENTER THE FORGE ] [ EXPLORE KNOWLEDGE ]        |
|                                                       |
---------------------------------------------------------
```

## 5.2 Hero image

Use a high-quality blacksmith image showing:

-   hammer
-   anvil
-   sparks
-   hot steel
-   dark environment

The supplied reference image is the visual direction.

## 5.3 Image treatment

Do not place text directly over a bright image.

Use a gradient overlay:

``` text
left side:
very dark

center:
dark transparent

right side:
image remains visible
```

The exact treatment can be adjusted according to the image.

## 5.4 Hero height

Desktop:

-   approximately 600--750px depending on viewport

Mobile:

-   approximately 500--650px

Do not force an extremely tall hero.

## 5.5 Hero typography

Primary title:

``` text
BLACKSMITH KNIGHT
FORGING HEAVEN
```

Supporting headline:

``` text
Knowledge. Steel. Fire. Craftsmanship.
```

Supporting description:

``` text
A practical digital workshop for learning,
building and understanding the craft of blacksmithing.
```

Keep the text concise.

------------------------------------------------------------------------

# 6. Hero Buttons

Create two button levels.

## 6.1 Primary button

Example:

``` text
⚒ ENTER THE FORGE
```

Characteristics:

-   fire orange background
-   dark text or white text depending on contrast
-   medium rounded corners
-   subtle shadow
-   slight hover lift
-   subtle orange glow

Hover:

``` text
translateY(-2px)
slightly brighter orange
slightly stronger shadow
```

## 6.2 Secondary button

Example:

``` text
EXPLORE KNOWLEDGE
```

Characteristics:

-   transparent/dark background
-   iron border
-   light text
-   orange border or glow on hover

------------------------------------------------------------------------

# 7. Navigation Redesign

The current navigation is functional but visually resembles a technical
documentation site.

Keep the information architecture, but improve hierarchy and identity.

## 7.1 Brand area

Left side:

``` text
⚒ BLACKSMITH KNIGHT
   FORGING HEAVEN
```

The logo can be simple.

Do not overcomplicate it.

## 7.2 Navigation

Possible structure:

``` text
FORGE
KNOWLEDGE
MATERIALS
VIDEOS
PROJECTS
WORKSHOP
TOOLS
RULES
SEARCH
```

The current sections can remain if functionality depends on them.

## 7.3 Active navigation

Use a small fire-orange indicator.

Example:

``` text
FORGE
─────
```

or a subtle orange glow under the active item.

Avoid large orange blocks.

## 7.4 Navigation background

Use:

-   almost-black background
-   subtle bottom border
-   slight transparency if appropriate
-   optional backdrop blur

The navigation should feel attached to the page rather than like a
separate admin bar.

------------------------------------------------------------------------

# 8. Forge Pillars Section

Current structure:

``` text
The Forge Pillars

six identical cards
```

New direction:

> Create a visual "foundation of the craft."

## 8.1 Section header

Example:

``` text
THE FORGE

Six foundations of the craft.
```

Add a small orange eyebrow label:

``` text
THE DIGITAL WORKSHOP
```

## 8.2 Card layout

Use Bento Grid principles.

Do not make every card identical.

Possible desktop layout:

``` text
┌───────────────────┬───────────────────┬───────────────────┐
│                   │                   │                   │
│ MATERIALS         │ VIDEO FORGE       │ TECHNIQUES        │
│                   │                   │                   │
├───────────────────┼───────────────────┴───────────────────┤
│                   │                                       │
│ APPRENTICE        │ WORKSHOP / TOOLS                      │
│ PROJECTS          │                                       │
│                   │                                       │
├───────────────────┴───────────────────────────────────────┤
│                                                           │
│ SAFETY & RULES                                            │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

Exact layout can change according to content.

------------------------------------------------------------------------

# 9. Forge Card Design

## 9.1 Image area

Cards should often have a visual area.

Recommended image ratio:

-   16:9 for normal cards
-   4:3 or full-height image for large feature cards

## 9.2 Image overlay

Images should have a dark gradient.

Text should remain readable.

## 9.3 Card label

Use:

``` text
01 · METALLURGY
```

Small uppercase text.

Orange.

## 9.4 Card title

Example:

``` text
Materials & Steel
```

Use a strong readable heading.

## 9.5 Description

Keep it short.

Avoid large paragraphs inside cards.

## 9.6 CTA

Use:

``` text
EXPLORE →
```

or:

``` text
READ GUIDE →
```

Avoid large generic buttons inside every card.

------------------------------------------------------------------------

# 10. Image Direction for Each Forge Pillar

Use imagery intentionally.

## 10.1 Materials & Steel

Possible imagery:

-   steel billets
-   glowing metal
-   cut steel
-   grain structure
-   forged bars

Mood:

technical + hot metal

------------------------------------------------------------------------

## 10.2 Curated Video Forge

Possible imagery:

-   blacksmith hammering
-   sparks
-   forge fire
-   anvil

Mood:

active workshop

------------------------------------------------------------------------

## 10.3 Knowledge & Technique Guides

Possible imagery:

-   hammer on anvil
-   close-up of forged steel
-   hand tools
-   workbench

Mood:

technical craftsmanship

------------------------------------------------------------------------

## 10.4 Apprentice Projects

Possible imagery:

-   beginner knife
-   simple hook
-   forged bracket
-   first projects
-   hand tools

Mood:

learning + achievement

------------------------------------------------------------------------

## 10.5 Tools & Workshop

Possible imagery:

-   anvil
-   forge
-   tongs
-   hammers
-   workshop wall

Mood:

practical workshop

------------------------------------------------------------------------

## 10.6 Safety & Rules

Possible imagery:

-   safety glasses
-   gloves
-   forge ventilation
-   workshop PPE

Mood:

serious and responsible

------------------------------------------------------------------------

# 11. Apprentice's Rule Section

Keep this content.

It is valuable because it communicates the site's philosophy.

Current idea:

> You do not need an expensive shop to start learning.

Turn it into a visually distinctive quote/rule panel.

## 11.1 Design

Use:

-   dark iron surface
-   thin orange accent line
-   large heading
-   concise explanatory text
-   small CTA

Example:

``` text
THE APPRENTICE'S RULE

You do not need an expensive shop
to start learning.

A solid striking surface, a 2 lb cross-peen hammer,
basic tongs and a small fire are enough to begin.

                         [ VIEW MINIMUM SETUP → ]
```

------------------------------------------------------------------------

# 12. Typography

Typography should remain modern and highly readable.

## 12.1 Headings

Use a strong modern sans-serif.

Characteristics:

-   bold
-   compact
-   high contrast
-   modern
-   readable

Avoid highly decorative blackletter fonts.

## 12.2 Body

Use a clean sans-serif.

Priorities:

1.  readability
2.  comfortable line height
3.  moderate font size
4.  strong contrast

## 12.3 Technical labels

Small labels can use a monospaced font.

Example:

``` text
01 · METALLURGY
```

This creates a subtle technical/workshop feeling.

Do not use monospace for normal paragraphs.

------------------------------------------------------------------------

# 13. Typography Scale

Suggested starting scale:

``` text
Hero title:
48–72px desktop
36–48px mobile

Section title:
30–40px

Card title:
18–24px

Body:
14–17px

Small description:
12–14px

Technical label:
10–12px
```

Adjust based on actual content.

The current site appears somewhat compressed. Give major headings and
sections more breathing room.

------------------------------------------------------------------------

# 14. Spacing

Use a consistent spacing system.

Suggested base:

``` text
4px
8px
12px
16px
24px
32px
48px
64px
96px
```

Avoid arbitrary values everywhere.

## 14.1 Section spacing

Desktop:

``` text
section-to-section:
72–110px
```

Mobile:

``` text
section-to-section:
48–72px
```

## 14.2 Card spacing

Use consistent:

``` text
16px
24px
32px
```

depending on card size.

------------------------------------------------------------------------

# 15. Borders

The current site uses many visible thin borders.

Keep borders but make them more intentional.

Recommended:

``` text
border:
rgba(255,255,255,0.08)
```

Hover:

``` text
border:
rgba(255,87,34,0.45)
```

Avoid bright gray borders.

The border should be discovered rather than dominate.

------------------------------------------------------------------------

# 16. Shadows

Use shadows to establish depth.

Example conceptual layers:

``` text
normal:
0 10px 30px rgba(0,0,0,0.25)

hover:
0 16px 40px rgba(0,0,0,0.35)
```

Orange glow should be very subtle.

Do not make every card glow orange.

------------------------------------------------------------------------

# 17. Card Hover Effects

Cards should feel interactive.

Suggested:

``` text
transform:
translateY(-3px)

transition:
200–300ms

border:
slightly brighter

image:
scale(1.02–1.04)

orange accent:
slightly brighter
```

Do not use aggressive scaling.

------------------------------------------------------------------------

# 18. Images

Images are a major part of the redesign.

## 18.1 Image requirements

Prefer:

-   high resolution
-   dark workshop environments
-   real blacksmithing
-   real tools
-   real materials
-   realistic photography

Avoid:

-   generic stock images
-   cartoon blacksmiths
-   overly artificial fantasy imagery
-   unrelated industrial photographs

## 18.2 Image consistency

Images should share a similar visual tone:

-   dark
-   warm
-   high contrast
-   orange firelight

This creates a coherent visual identity.

------------------------------------------------------------------------

# 19. Image Treatment

A consistent image treatment should be applied.

Example:

``` text
image
+
dark overlay
+
slight warm tone
+
optional gradient
```

Do not apply excessive filters.

The original subject should remain recognizable.

------------------------------------------------------------------------

# 20. Buttons --- Complete System

Create reusable button variants.

## Primary

``` text
bg-fire-orange
text-dark
```

## Secondary

``` text
dark background
iron border
light text
```

## Ghost

``` text
transparent
muted text
orange hover
```

## Icon button

For:

-   search
-   menu
-   settings
-   navigation

All buttons should share:

-   consistent height
-   consistent radius
-   consistent typography
-   consistent transition behavior

Do not style each button independently.

------------------------------------------------------------------------

# 21. Inputs and Forms

Internal pages may contain:

-   search
-   filters
-   material lookup
-   forms
-   project creation
-   admin controls

These should use the same forged UI language.

Example:

``` text
┌──────────────────────────────────────┐
│ Search steel, tools, techniques...  │
└──────────────────────────────────────┘
```

Dark surface.

Subtle border.

Orange focus ring.

Avoid default browser styling.

------------------------------------------------------------------------

# 22. Search

Search should feel like a workshop tool.

Example:

``` text
⚒ SEARCH THE FORGE
```

Search results should use:

-   image
-   category
-   title
-   short description
-   relevance/action

Do not make search results look like raw database rows unless the page
specifically requires that.

------------------------------------------------------------------------

# 23. Internal Pages

The visual redesign must continue beyond the homepage.

## Materials

Visual identity:

-   steel
-   metallurgy
-   charts
-   specifications
-   hot metal imagery

Possible layout:

``` text
MATERIALS & STEEL

Search materials...

Featured steels
───────────────

[ Steel card ] [ Steel card ] [ Steel card ]

Material database
```

------------------------------------------------------------------------

## Videos

Use visual thumbnails.

Cards should show:

-   image
-   creator
-   duration
-   publication date
-   category
-   title

Video pages should feel like a curated forge library, not a raw YouTube
feed.

------------------------------------------------------------------------

## Guides

Guides need the strongest readability.

Do not over-style the actual article text.

Use:

-   wide readable content column
-   strong headings
-   code/technical blocks where needed
-   diagrams/images
-   table of contents
-   related guides

Background can remain dark, but article content should have high
contrast.

------------------------------------------------------------------------

## Projects

Projects should feel like workshop builds.

Card information:

``` text
PROJECT
Difficulty
Time
Materials
Tools
Status
```

Use project images prominently.

------------------------------------------------------------------------

## Workshop

This section should feel like entering the physical shop.

Potential content:

-   forge
-   anvil
-   hammers
-   tongs
-   grinder
-   safety
-   ventilation
-   workshop layout

------------------------------------------------------------------------

## Tools

Tool cards can show:

-   image
-   name
-   purpose
-   beginner/advanced
-   recommended use
-   related projects

------------------------------------------------------------------------

## Rules

Safety information should be visually clear and serious.

Do not bury safety warnings inside decorative styling.

Safety-critical content must have strong contrast and clear hierarchy.

------------------------------------------------------------------------

# 24. Footer

The current footer is acceptable structurally.

Improve:

-   typography
-   spacing
-   logo
-   section grouping
-   subtle iron divider

Possible footer:

``` text
⚒ BLACKSMITH KNIGHT
FORGING HEAVEN

A practical digital workshop for
blacksmithing knowledge and craft.

KNOWLEDGE
Materials & Steel
Technical Guides
Apprentice Projects

FORGE LIBRARY
Curated Videos
Source Registry
Tools & Anvils
Rules & Safety
```

Keep it restrained.

------------------------------------------------------------------------

# 25. Responsive Design

The design must be designed for mobile, not simply shrunk.

## Desktop

Use:

-   large hero
-   bento grid
-   multiple columns
-   wide imagery

## Tablet

Use:

-   2-column cards
-   smaller hero
-   condensed navigation

## Mobile

Use:

-   one-column content
-   large readable buttons
-   hamburger navigation
-   hero image with strong dark overlay
-   cards stacked vertically
-   no tiny navigation text

------------------------------------------------------------------------

# 26. Mobile Navigation

Desktop navigation can remain horizontal.

Mobile:

``` text
⚒ BLACKSMITH KNIGHT                    ☰
```

Open:

``` text
FORGE
KNOWLEDGE
MATERIALS
VIDEOS
PROJECTS
WORKSHOP
TOOLS
RULES
SEARCH
```

The mobile menu should feel like part of the same design.

------------------------------------------------------------------------

# 27. Animation Philosophy

Animations should communicate polish, not distract.

## Use

-   fade-in
-   slight upward movement
-   image zoom
-   button lift
-   border transition
-   subtle glow
-   navigation indicator transition

## Avoid

-   spinning objects
-   constant background movement
-   excessive particle effects
-   large page transitions
-   bouncing buttons
-   animations that delay interaction

------------------------------------------------------------------------

# 28. Forge/Spark Animation

Optional enhancement.

A very subtle spark system can be used in the hero.

Rules:

-   extremely low density
-   short lifetime
-   mostly orange
-   low opacity
-   never obscure text
-   respect reduced-motion preferences

This is an enhancement, not a requirement for the MVP redesign.

------------------------------------------------------------------------

# 29. Accessibility

The visual redesign must not reduce usability.

Maintain:

-   strong text contrast
-   keyboard navigation
-   visible focus states
-   semantic buttons
-   semantic links
-   alt text
-   readable font sizes
-   sufficient touch targets

Do not use orange text on black if contrast is insufficient.

Do not communicate information by color alone.

------------------------------------------------------------------------

# 30. Performance

Large images can easily make the redesign slow.

Use:

-   properly sized images
-   modern formats where supported
-   lazy loading for below-the-fold images
-   responsive image sizes
-   optimized hero image
-   limited animation
-   no unnecessarily huge background files

For a Next.js project, use the framework's image optimization facilities
where appropriate.

Do not load a 5000px photograph just to display a 400px card.

------------------------------------------------------------------------

# 31. Component Architecture

The redesign should be implemented using reusable components.

Suggested structure:

``` text
components/
    layout/
        Header
        Footer
        PageContainer

    hero/
        ForgeHero

    ui/
        Button
        Badge
        SectionHeader
        Card
        ImageCard
        IconButton

    forge/
        ForgePillarCard
        ForgeBentoGrid
        ApprenticeRule

    media/
        VideoCard
        ImageWithOverlay

    content/
        GuideCard
        MaterialCard
        ProjectCard
        ToolCard
```

The exact structure should follow the existing project architecture.

Do not unnecessarily restructure the whole repository.

------------------------------------------------------------------------

# 32. Design Tokens

Create a single source of truth.

Example conceptual tokens:

``` css
:root {
  --forge-black: #080807;
  --charcoal: #11110f;
  --dark-iron: #191917;
  --iron: #292824;
  --steel: #45423c;
  --steel-gray: #706b62;
  --ash: #a9a39a;
  --forge-white: #f1eee8;

  --fire-orange: #ff5722;
  --hot-iron: #ff7a32;
  --ember: #c83b12;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;

  --shadow-card: 0 10px 30px rgba(0,0,0,.25);
  --shadow-card-hover: 0 16px 40px rgba(0,0,0,.35);

  --transition-fast: 150ms;
  --transition-normal: 250ms;
  --transition-slow: 400ms;
}
```

If using current Tailwind versions, consider expressing these as
Tailwind theme variables so the design tokens can generate reusable
utilities.

------------------------------------------------------------------------

# 33. Tailwind Implementation Guidance

If the project uses Tailwind, do not create dozens of arbitrary one-off
utility combinations.

Create reusable component patterns.

For example:

``` text
forge-card
forge-button-primary
forge-button-secondary
forge-section
forge-label
forge-container
```

Tailwind's theme system supports centralized color, typography, spacing,
radius, shadow and animation tokens.

Use the official Tailwind theme-variable approach rather than scattering
magic values throughout JSX.

------------------------------------------------------------------------

# 34. Page Container

Use a consistent maximum content width.

Suggested:

``` text
max-width:
1200–1400px
```

depending on the existing design.

Use comfortable side padding.

Desktop:

``` text
24–48px
```

Mobile:

``` text
16–20px
```

Do not allow text to stretch across the entire monitor.

------------------------------------------------------------------------

# 35. Homepage Information Architecture

Recommended final structure:

``` text
HEADER

HERO
    Forge image
    Brand
    Main statement
    Description
    Primary CTA
    Secondary CTA

FORGE PILLARS
    Materials
    Videos
    Techniques
    Projects
    Workshop
    Safety

FEATURED KNOWLEDGE
    selected guides/articles

LATEST FROM THE FORGE
    videos / materials / projects

APPRENTICE'S RULE
    philosophy statement

OPTIONAL:
    statistics / featured material / featured project

FOOTER
```

Do not put every available feature on the homepage.

The homepage should create curiosity and provide clear paths deeper into
the site.

------------------------------------------------------------------------

# 36. Homepage Content Hierarchy

The user's eye should encounter:

``` text
1. Visual identity
2. What the site is
3. Main action
4. Main areas of knowledge
5. Recent/interesting content
6. Site philosophy
7. Footer
```

Avoid presenting six equally important blocks.

There must be a clear hierarchy.

------------------------------------------------------------------------

# 37. Visual Hierarchy Rules

Use three levels.

## Level 1

Large:

-   hero
-   major section headings
-   featured content

## Level 2

Medium:

-   card titles
-   subsection headings
-   important CTAs

## Level 3

Small:

-   metadata
-   labels
-   dates
-   categories

This makes the site easier to scan.

------------------------------------------------------------------------

# 38. What Must NOT Change During UI Redesign

The redesign is primarily visual.

Do not break:

-   routing
-   backend APIs
-   database behavior
-   authentication
-   existing data structures
-   existing content
-   search functionality
-   filtering
-   video data flow
-   admin functionality
-   project creation
-   material data
-   rules
-   source registry
-   existing integrations

The redesign should preserve working behavior.

------------------------------------------------------------------------

# 39. Refactoring Rule

Before modifying a component:

1.  Understand what data it receives.
2.  Understand what actions it performs.
3.  Preserve its public behavior.
4.  Separate visual changes from functional changes.
5.  Test the existing functionality.
6.  Only then improve the visual implementation.

Do not rewrite working business logic simply because the UI component is
being redesigned.

------------------------------------------------------------------------

# 40. Development Strategy

Do the redesign incrementally.

## Step 1 --- Audit

Identify:

-   global CSS
-   Tailwind configuration
-   layout
-   header
-   footer
-   homepage
-   card components
-   button components
-   image handling
-   typography
-   current colors

## Step 2 --- Establish design tokens

Implement:

-   colors
-   typography
-   spacing
-   borders
-   radius
-   shadows
-   transitions

## Step 3 --- Build reusable UI primitives

Create/refactor:

-   Button
-   Badge
-   Card
-   SectionHeader
-   ImageOverlay
-   Container

## Step 4 --- Redesign header

Do not touch page functionality.

## Step 5 --- Redesign hero

This is the most visually important change.

## Step 6 --- Redesign Forge Pillars

Introduce images and Bento layout.

## Step 7 --- Redesign Apprentice's Rule

Create a distinctive visual block.

## Step 8 --- Redesign footer

Keep simple.

## Step 9 --- Apply system to internal pages

One section at a time.

## Step 10 --- Responsive pass

Test:

-   desktop
-   tablet
-   mobile

## Step 11 --- Accessibility pass

Check:

-   contrast
-   keyboard
-   focus
-   semantic markup
-   alt text

## Step 12 --- Performance pass

Check:

-   image sizes
-   loading
-   animations
-   bundle impact

------------------------------------------------------------------------

# 41. Git/Development Safety

Create a dedicated UI redesign branch.

Example:

``` bash
git checkout -b ui-forge-redesign
```

Commit in small logical steps.

Recommended commits:

``` text
ui: add forge design tokens
ui: redesign global typography
ui: redesign header
ui: redesign homepage hero
ui: redesign forge pillar cards
ui: add forge image treatment
ui: redesign apprentice rule
ui: redesign footer
ui: update responsive layout
ui: add subtle interactions
ui: accessibility polish
ui: performance polish
```

Do not combine the entire redesign into one enormous commit.

------------------------------------------------------------------------

# 42. Before/After Acceptance Criteria

The redesign is successful if a person can see the homepage for a few
seconds and immediately understand:

> This is a blacksmithing website.

It should no longer look like:

> A generic dark developer portal.

## Visual acceptance criteria

The new homepage should have:

-   strong forge hero
-   obvious blacksmithing imagery
-   consistent dark iron palette
-   fire-orange accents
-   improved card hierarchy
-   meaningful imagery
-   strong typography
-   comfortable spacing
-   clear navigation
-   modern buttons
-   subtle interaction
-   responsive design

------------------------------------------------------------------------

# 43. UX Acceptance Criteria

The redesign must remain:

-   easy to navigate
-   readable
-   comfortable
-   fast
-   responsive
-   accessible

The user should never have to sacrifice usability to obtain the visual
effect.

------------------------------------------------------------------------

# 44. Image Selection Rules

When adding new images, ask:

### Does it show real blacksmithing?

If no, reject it unless it serves a specific technical purpose.

### Does it fit the color mood?

Prefer:

-   dark
-   warm
-   iron
-   orange firelight

### Does it communicate something?

An image should help the user understand the section.

Do not use an image only because it looks attractive.

------------------------------------------------------------------------

# 45. AI-Generated Images

AI-generated imagery can be used when appropriate for decorative/hero
purposes.

However:

-   avoid fake-looking tools
-   avoid impossible anvils
-   avoid physically impossible hammer positions
-   avoid distorted hands
-   avoid unrealistic workshop geometry
-   avoid historical inaccuracies when the image is presented as
    educational

For educational content, prefer real/reference photography or clearly
labeled illustrative imagery.

------------------------------------------------------------------------

# 46. Design Personality

The site should feel:

``` text
70% modern technical
20% industrial workshop
10% fire / drama
```

Not:

``` text
70% fantasy
20% fire
10% technical
```

This balance is important.

The site's credibility comes from the technical content.

The visual identity comes from the forge.

------------------------------------------------------------------------

# 47. Recommended Visual Effects

Use:

### Subtle iron gradient

``` text
#11110F → #191917
```

### Fire glow

``` text
rgba(255,87,34,0.12)
```

### Focus glow

``` text
rgba(255,87,34,0.25)
```

### Image vignette

Dark edges to keep attention on content.

### Fine border

``` text
rgba(255,255,255,0.08)
```

These values are starting points, not mandatory exact values.

------------------------------------------------------------------------

# 48. Avoid Overdesign

A critical rule:

> If everything is visually special, nothing is visually special.

Therefore:

-   Hero = strongest visual
-   Featured cards = medium visual
-   Normal content = restrained
-   Article text = very restrained
-   Safety content = clarity first

This creates hierarchy.

------------------------------------------------------------------------

# 49. Recommended Homepage Composition

Final target:

``` text
┌──────────────────────────────────────────────────────┐
│ NAVIGATION                                           │
├──────────────────────────────────────────────────────┤
│                                                      │
│              HERO FORGE IMAGE                       │
│                                                      │
│         BLACKSMITH KNIGHT                            │
│         FORGING HEAVEN                               │
│                                                      │
│       Knowledge. Steel. Fire.                       │
│       Craftsmanship.                                 │
│                                                      │
│       [ ENTER THE FORGE ]                            │
│       [ EXPLORE KNOWLEDGE ]                          │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│ THE FORGE                                            │
│ Six foundations of the craft.                       │
│                                                      │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐        │
│ │   IMAGE    │ │   IMAGE    │ │   IMAGE    │        │
│ │ MATERIALS  │ │   VIDEOS   │ │ TECHNIQUE  │        │
│ └────────────┘ └────────────┘ └────────────┘        │
│                                                      │
│ ┌────────────┐ ┌─────────────────────────────┐       │
│ │  PROJECTS  │ │        WORKSHOP             │       │
│ └────────────┘ └─────────────────────────────┘       │
│                                                      │
├──────────────────────────────────────────────────────┤
│ FEATURED KNOWLEDGE                                   │
│                                                      │
│ [featured content] [featured content]                │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│ THE APPRENTICE'S RULE                                │
│                                                      │
│ You do not need an expensive shop to start learning.│
│                                                      │
│                              [ VIEW SETUP → ]         │
│                                                      │
├──────────────────────────────────────────────────────┤
│ FOOTER                                               │
└──────────────────────────────────────────────────────┘
```

------------------------------------------------------------------------

# 50. Final Design Target

The final site should feel like:

> **Walking into a dark blacksmith workshop at night.**

You see:

-   the black iron
-   the anvil
-   the hammer
-   the glow of hot steel
-   sparks flying
-   tools hanging in the background
-   knowledge organized clearly
-   a place where an apprentice can learn

But the interface itself remains:

-   modern
-   clean
-   technical
-   comfortable
-   responsive
-   easy to use

That combination is the identity of **Blacksmith Knight Forging
Heaven**.

------------------------------------------------------------------------

# 51. Implementation Priority

Priority order:

## P0 --- Essential

1.  Design tokens
2.  Global background
3.  Typography
4.  Header
5.  Hero
6.  Primary/secondary buttons
7.  Forge Pillars cards
8.  Image treatment
9.  Responsive homepage

## P1 --- Important

10. Featured knowledge
11. Apprentice Rule
12. Footer
13. Internal page cards
14. Search styling
15. Forms
16. Video cards
17. Material cards
18. Project cards

## P2 --- Polish

19. Hover effects
20. Micro animations
21. Image zoom
22. Subtle forge glow
23. Optional spark animation
24. Advanced responsive refinements
25. Performance optimization

------------------------------------------------------------------------

# 52. Definition of Done

The UI redesign is complete when:

-   [ ] Homepage clearly communicates blacksmithing
-   [ ] Hero uses strong forge imagery
-   [ ] Color palette is centralized
-   [ ] Buttons use a consistent design
-   [ ] Cards use a consistent design system
-   [ ] Forge Pillars no longer look like generic documentation boxes
-   [ ] Images are integrated into the visual hierarchy
-   [ ] Navigation feels part of the brand
-   [ ] Typography hierarchy is consistent
-   [ ] Spacing is consistent
-   [ ] Mobile layout works correctly
-   [ ] Internal pages use the same visual language
-   [ ] Existing functionality still works
-   [ ] No business logic was unnecessarily rewritten
-   [ ] Keyboard navigation works
-   [ ] Focus states are visible
-   [ ] Text contrast is sufficient
-   [ ] Images are optimized
-   [ ] Animations are subtle
-   [ ] Reduced-motion behavior is respected
-   [ ] No major layout shifts occur while images load
-   [ ] Homepage visually matches the "dark forge / hot iron / modern
    workshop" direction

------------------------------------------------------------------------

# 53. Important Instruction for Future Development

Whenever adding a new UI component, ask:

1.  Does it belong to the Forge visual language?
2.  Does it use the existing design tokens?
3.  Does it have a clear visual hierarchy?
4.  Does it remain readable?
5.  Does it work on mobile?
6.  Does it preserve the existing functionality?
7.  Does it need imagery?
8.  Is the animation actually useful?
9.  Is it visually consistent with the rest of the website?
10. Is the component becoming unnecessarily decorative?

Do not introduce a completely different visual style for individual
pages.

The entire website should feel like **one coherent digital forge**.

------------------------------------------------------------------------

# 54. Reference Documentation

Tailwind CSS provides centralized theme variables for colors,
typography, spacing, shadows, breakpoints and other design tokens. This
is useful for implementing the design system rather than hardcoding
visual values throughout the application.

-   Tailwind theme variables: https://tailwindcss.com/docs/theme
-   Tailwind dark mode: https://tailwindcss.com/docs/dark-mode
-   Tailwind colors: https://tailwindcss.com/docs/colors

These references are implementation guidance. The exact visual values in
this document are the project's design decisions and should take
precedence when implementing the Blacksmith Knight visual identity.

------------------------------------------------------------------------

# 55. Short Design Brief for AI/Coding Agents

When another AI coding agent is asked to modify this project, give it
this rule:

> **You are modifying the frontend of Blacksmith Knight Forging Heaven.
> Preserve all existing functionality and business logic. The visual
> target is a modern blacksmith workshop: dark forged iron, charcoal,
> steel, hot orange firelight, sparks, anvil and hammer imagery. The
> site must feel industrial, practical and technically credible, not
> fantasy or gaming themed. Use centralized design tokens, reusable
> components, strong visual hierarchy, high-quality blacksmith imagery,
> subtle animations and excellent readability. Do not introduce random
> colors, random gradients, excessive glow, excessive animations or
> unrelated design styles. Before changing functionality, understand and
> preserve the existing behavior. The homepage should have a dramatic
> forge hero, visual Bento-style Forge Pillars, meaningful imagery and a
> strong apprentice/workshop identity.**

------------------------------------------------------------------------

# 56. End State

The redesign is not intended to make the site "flashy."

It is intended to give the existing working website a **recognizable
identity**.

The user should open the site and immediately feel:

> **This is the forge.**

Then the interface should make it easy to:

-   learn
-   explore
-   watch
-   build
-   research
-   find tools
-   understand materials
-   follow projects
-   learn safe practices

The visual design should support the content rather than compete with
it.

**Primary design phrase:**

> **FORGED IN DARKNESS. BUILT FOR LEARNING.**
