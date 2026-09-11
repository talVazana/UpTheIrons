# Blacksmith Knight — UI Windows & Interactive Elements

A comprehensive map of all application windows and every interactive element (buttons, links, dialogs, sliders) within them.

## 1. Home Page (The Forge) `(/)`
The main dashboard acting as a dynamic entry point to all forge activities.
* **Interactive Elements:**
  * **"Explore Materials" Button:** Primary call-to-action routing to the materials database.
  * **"Apprentice Projects" Button:** Routes to beginner forging tasks.
  * **"Read Guides" Link:** Directs to the technical knowledge base.
  * **Bento Pillar Links (x6):** Large clickable cards for Materials, Videos, Guides, Projects, Tools, and Rules.
  * **"View Minimum Setup" Button:** Inside the Apprentice banner, links to the basic workshop guide.

## 2. Materials & Steel Database `(/materials)`
The interactive technical reference for metallurgy.
* **Interactive Elements:**
  * **Compare Checkboxes:** Multi-select toggles on each material card to enable side-by-side comparison mode.
  * **"View Protocol" Button:** Opens the 4-phase heat treatment timeline for a specific steel.
  * **"Show Spark Profile" Button:** Triggers a dialog modal showing visual spark testing characteristics.
  * **Material Cards (Links):** Clickable cards that route to the detailed dossier for a specific steel.

## 3. Curated Video Feed `(/videos)`
The vault for ingested YouTube videos from controlled master smith channels.
* **Interactive Elements:**
  * **Category Filter Pills (Buttons):** Toggle active state to filter videos by "Forging", "Bladesmithing", "Heat Treatment", etc.
  * **"Configure API Key" Button:** Opens a secure **Settings Modal** to update the YouTube Data API key without reloading.
  * **"Sync All Channels" Button:** Triggers backend ingestion; displays a progress spinner and feedback toast upon completion.
  * **Video Cards (Links/Buttons):** Clicking opens a **Video Player Modal** with an embedded iframe and metadata.
  * **"Manage Channels" Link:** Routes to the Video Channels Manager.

## 4. Video Channels Manager `(/videos/channels)`
Admin control panel for managing allowed YouTube sources.
* **Interactive Elements:**
  * **"Add YouTube Channel" Button:** Opens a **Creation Dialog** with text inputs for Handle/URL and priority selectors.
  * **Status Tabs (Links/Buttons):** Filter view by "All", "Enabled", "Disabled".
  * **ON/OFF Toggle Switches:** Instantly enables or disables a channel for future syncs.
  * **"Sync" Button (Per Channel):** Triggers an immediate fetch for that specific channel.
  * **"Delete" Action Button:** Removes the channel from the registry (requires confirmation).

## 5. Knowledge Guides `(/guides)`
The progressive technical article library.
* **Interactive Elements:**
  * **Source Tabs (Buttons):** Switch view between "Master Craft Guides" and "Guild Articles & RSS".
  * **Global Search Bar (Input):** Free-text field that filters results in real-time.
  * **Difficulty Dropdown/Filters:** Select Beginner, Intermediate, or Advanced.
  * **Trust Badges (Hover Tooltips):** Hovering over a badge reveals an explanatory tooltip regarding the factual nature of the content.
  * **Guide Links:** Clickable cards routing to the full article reader (`/guides/[slug]`).

## 6. Apprentice Projects `(/projects)`
Step-by-step practical forging tasks tracking progression.
* **Interactive Elements:**
  * **Level Filter Tabs:** Select difficulty levels (1 through 4).
  * **Interactive Checklist (Checkboxes):** Mark individual project steps (e.g., "Draw out taper") as completed. State is maintained locally.
  * **Related Materials Links:** Quick jump buttons to the steel requirements (e.g., "Requires: 1084 Steel").
  * **"Start Project" Button:** Enters focus mode for the specific tutorial.

## 7. Workshop & Tools `(/tools)`
Equipment evaluations, transparent reviews, and price tracking.
* **Interactive Elements:**
  * **Category Filter Pills:** Filter by "Anvils", "Forges", "Belt Grinders", "Tongs".
  * **"Beginner Friendly" Checkbox:** Toggles view to show only highly recommended starting gear.
  * **Max Budget Slider (Input Range):** Draggable slider to filter tools below a specific price threshold.
  * **"Sync Catalogs" Button:** Triggers backend script to update live pricing.
  * **"Purchase" / "View Store" Buttons:** External links to vendor sites.
  * **"View Alternatives" Link:** Expands a dropdown showing cheaper or premium alternatives.

## 8. Safety & Rules Codex `(/rules)`
The core manifesto and interactive safety testbed.
* **Interactive Elements:**
  * **Rule File Navigator (Sidebar Links):** Jump between Safety, Metallurgy, Product, and Content rules.
  * **"Reload Rules" Button:** Forces the backend to re-read markdown rule files from disk.
  * **Interactive Tester (Form):** Text input area and "Test Compliance" button to simulate validating external content against safety guardrails (results shown in a **Feedback Dialog**).

## 9. Sources Registry `(/sources)`
Manager for RSS feeds and other ingestion APIs.
* **Interactive Elements:**
  * **Filter Tabs:** Switch between "All", "YouTube", "RSS", "Manual/APIs".
  * **"Add Source" Button:** Opens a **Registration Modal** with URL validation.
  * **"Test Connection" Button:** Probes a source URL and displays a **Preview Dialog** with sample data before committing.
  * **ON/OFF Toggle Switches:** Enables/Disables individual sources.
  * **"Delete" Action Button:** Removes the source (requires confirmation).

## 10. Global Search `(/search)`
Cross-domain search interface.
* **Interactive Elements:**
  * **Main Search Bar (Input field):** Live-updating text input.
  * **Type Filter Checkboxes:** Check/uncheck to restrict results to Videos, Guides, Materials, or Tools.
  * **Result Links:** Direct links routing to the respective entity page.
