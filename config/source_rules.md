# Source Quality & Provenance Rules

## Controlled Ingestion Boundary
Blacksmith Knight never executes open web crawling or blind URL spidering. External content enters strictly through user-approved registered sources:
1. **YouTube Channels:** Must belong to verified bladesmiths, guilds, or reputable maker educators.
2. **RSS / Atom Feeds:** Must be published by regional blacksmithing associations, metallurgy institutions, or recognized makers.
3. **Product Catalogs:** Controlled vendor API or static fixtures; no scraping arbitrary commercial stores.

## Source Quality Standards
1. **Attribution:** Original author name, publisher, source URL, and timestamp must be fully preserved.
2. **Duplication Rejection:** Content items are deduplicated deterministically by platform key (e.g. `video:youtube:{id}`, `article:url:{hash}`). Duplicate ingest runs must update only dynamic fields (such as price or views) without creating new records.
3. **Failure Isolation:** A network timeout or HTTP error on one source feed must never interrupt the synchronization of other sources.
4. **Transparency:** If content is synthesized or enriched by AI, that status must be explicitly marked.
