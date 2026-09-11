# Kiko's BlackSmith Heaven - Detailed User Manual

This manual provides step-by-step instructions on how to use every feature of the website, including exactly where to click and how to manage the forge as an Admin.

---

## 1. General Navigation & Viewing Content

The main navigation bar is located at the top of every page. You can click the **Kiko's BlackSmith Heaven** logo at the top left to return to the Home page at any time.

### Viewing Materials & Steel (Metallurgy Vault)
1. **How to access:** Click **MATERIALS** in the top navigation bar, or click the **Materials & Steel** image card on the Home page.
2. **What to do:** You will see a grid of steel types (like 1084, 1095). Click on any card to open the detailed dossier.
3. **Interactive Features:** Inside a material's page, scroll down to see the "Composition Breakdown" visualizer and the "Heat Treatment Protocol" timeline. 

### Watching Videos
1. **How to access:** Click **VIDEOS** in the top navigation menu.
2. **Filtering:** At the top of the video feed, click any of the category pills (e.g., "Forging", "Bladesmithing", "Tools") to filter the videos.
3. **Playback:** Click the play icon on any video card. A video player modal will pop up, allowing you to watch the video directly on the website without leaving.

### Reading Guides & Knowledge
1. **How to access:** Click **GUIDES** in the top navigation bar.
2. **Filtering:** Use the tabs at the top to switch between "Master Craft Guides" (our original articles) and "Guild Articles" (articles fetched from approved RSS feeds).
3. **Searching:** Type into the "Free-text Search" box at the top to instantly filter guides by keywords.
4. **Reading:** Click on a guide's title. Notice the colored **Trust Badges** (like "Fact" or "Opinion") and pay attention to any **Safety Alert** banners (flame/shield icons) before attempting the techniques described.

### Browsing Tools & Workshop Gear
1. **How to access:** Click **TOOLS** in the top menu.
2. **Filtering:** Click the category pills (e.g., "Anvils", "Forges") to narrow down the list.
3. **Beginner Mode:** Check the **"Beginner Friendly"** checkbox to hide advanced/expensive industrial tools and only show equipment recommended for starting out.
4. **Budgeting:** Use the "Max Budget" slider or input to filter tools that fit your budget.

---

## 2. Admin Capabilities & Management

As the Admin, you have full control over where the website gets its videos, articles, and product prices. 

### Logging In
1. Go to the Home page (`/`).
2. Scroll to the **bottom right corner** of your screen and click the floating circular button containing the **Kiko Logo**.
3. On the Admin Access screen, type your Username and Password in the text boxes (the defaults are `Kiko` and `Kiko`).
4. Click the orange **ENTER FORGE** button. 
5. *Note: You can click "Log out" at the bottom of the admin screen when you are finished.*

### Changing Your Password
1. Log into the Admin panel using the steps above.
2. Locate the "Change Password" section.
3. Type your current password into the **Old Password** box.
4. Type your desired new password into the **New Password** box.
5. Click the **UPDATE PASSWORD** button.

### Managing YouTube Channels (The Video Forge)
To prevent junk videos from flooding your site, videos are only fetched from specific channels you approve.
1. Navigate to the **VIDEOS** page.
2. Click the **Channels** button or link to open the Channel Manager.
3. **To add a channel:** Click the **+ Add YouTube Channel** button. Paste the channel's URL or handle (e.g., `@BlackBearForge`) into the box and click **Save/Register**.
4. **To disable/enable:** Next to each channel, click the **Toggle Switch** to turn it ON or OFF. Disabled channels will not bring in new videos.
5. **To sync a specific channel:** Click the **Sync Now** button next to a channel's name to immediately fetch its latest videos.
6. **To sync everything:** Click the **Sync All Channels** button at the top of the page. A loading spinner will appear while the site pulls new videos.

### Setting API Keys
If you need to update the YouTube Data API key or the AI (Gemini) API key:
1. Navigate to the **VIDEOS** page.
2. Click the **Configure YouTube API Key** button.
3. A modal will pop up. Paste your new API key into the text field and click **Save**. This updates the system instantly without needing a server restart.

### Managing RSS Feeds (Articles)
1. Navigate to the **GUIDES** page.
2. Locate the **Feed Manager / Sources** area (also accessible via the `Sources` link in the footer/navbar).
3. **To add a website:** Click **Add RSS Feed**, paste the URL of the blog/website feed, and click **Register**.
4. **To sync:** Click the **Sync Feeds Now** button to fetch the latest written articles.

### Syncing Tool Catalogs (Prices)
1. Navigate to the **TOOLS** page.
2. Click the **Sync Catalogs** button. The system will scan your approved vendor lists and update the tool cards with the latest live prices.

### Using AI Enrichment
1. Navigate to the **VIDEOS** or **GUIDES** page.
2. If there are new videos or articles that haven't been tagged or summarized yet, click the **Enrich Pending Content** (or AI Sync) button.
3. The AI will process up to 10 items at a time, generating short summaries, detecting the difficulty level, and applying appropriate tags.
