import Link from "next/link";
import Image from "next/image";

export default function HomePage() {
  return (
    <div className="bg-[var(--bg-primary)] text-[var(--text-primary)] min-h-screen relative">
      <Link href="/admin" className="fixed bottom-4 right-4 z-50 bg-[var(--bg-surface)] border border-[var(--border-muted)] p-2 rounded-full hover:border-[var(--accent-forge)] shadow-lg shadow-black/50 transition-colors">
        <Image src="/kiko.png" alt="Admin Login" width={32} height={32} className="object-contain" />
      </Link>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10 sm:py-16">
        {/* Forge Pillars Section */}
        <section className="mb-20">
          <div className="mb-10">
            <div className="text-xs font-bold uppercase tracking-widest text-[var(--accent-forge)] mb-2">
              THE DIGITAL WORKSHOP
            </div>
            <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-primary)]">
              THE FORGE
            </h2>
            <p className="text-base text-[var(--text-secondary)] mt-2">
              Six foundations of the craft.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Card 1: Materials */}
            <Link
              href="/materials"
              className="group relative rounded-sm border-[4px] border-[var(--border-focus)] shadow-2xl shadow-black/60 relative before:absolute before:inset-1 before:border before:border-[var(--border-muted)] before:pointer-events-none bg-[var(--bg-card)] overflow-hidden hover:border-[var(--border-focus)] transition-all flex flex-col"
            >
              <div className="relative aspect-video w-full overflow-hidden">
                <Image src="/images/materials_steel.jpg" alt="Materials and Steel" fill className="object-cover group-hover:scale-105 transition-transform duration-500" />
                <div className="absolute inset-0 bg-gradient-to-t from-[var(--bg-card)] to-transparent" />
              </div>
              <div className="p-6 relative z-10 flex-grow flex flex-col justify-end -mt-16">
                <div className="text-xs font-mono uppercase text-[var(--accent-forge)] mb-2 tracking-wider">
                  01 &middot; METALLURGY
                </div>
                <h3 className="text-2xl font-bold text-[var(--text-primary)] mb-2 group-hover:text-[var(--accent-forge)] transition-colors">
                  Materials &amp; Steel
                </h3>
                <p className="text-sm text-[var(--text-secondary)] leading-relaxed mb-4">
                  Chemical compositions, heat treatment, and predictable metallurgy.
                </p>
                <div className="mt-auto text-xs text-[var(--text-muted)] font-medium flex items-center gap-1 group-hover:text-[var(--text-primary)] group-hover:translate-x-1 transition-all">
                  EXPLORE &rarr;
                </div>
              </div>
            </Link>

            {/* Card 2: Videos */}
            <Link
              href="/videos"
              className="group relative rounded-sm border-[4px] border-[var(--border-focus)] shadow-2xl shadow-black/60 relative before:absolute before:inset-1 before:border before:border-[var(--border-muted)] before:pointer-events-none bg-[var(--bg-card)] overflow-hidden hover:border-[var(--border-focus)] transition-all flex flex-col"
            >
              <div className="relative aspect-video w-full overflow-hidden">
                <Image src="/images/video_forge.jpg" alt="Video Forge" fill className="object-cover group-hover:scale-105 transition-transform duration-500" />
                <div className="absolute inset-0 bg-gradient-to-t from-[var(--bg-card)] to-transparent" />
              </div>
              <div className="p-6 relative z-10 flex-grow flex flex-col justify-end -mt-16">
                <div className="text-xs font-mono uppercase text-[var(--accent-forge)] mb-2 tracking-wider">
                  02 &middot; VISUAL LEARNING
                </div>
                <h3 className="text-2xl font-bold text-[var(--text-primary)] mb-2 group-hover:text-[var(--accent-forge)] transition-colors">
                  Curated Video Forge
                </h3>
                <p className="text-sm text-[var(--text-secondary)] leading-relaxed mb-4">
                  Controlled YouTube ingestion from master smiths.
                </p>
                <div className="mt-auto text-xs text-[var(--text-muted)] font-medium flex items-center gap-1 group-hover:text-[var(--text-primary)] group-hover:translate-x-1 transition-all">
                  EXPLORE &rarr;
                </div>
              </div>
            </Link>

            {/* Card 3: Guides */}
            <Link
              href="/guides"
              className="group relative rounded-sm border-[4px] border-[var(--border-focus)] shadow-2xl shadow-black/60 relative before:absolute before:inset-1 before:border before:border-[var(--border-muted)] before:pointer-events-none bg-[var(--bg-card)] overflow-hidden hover:border-[var(--border-focus)] transition-all flex flex-col"
            >
              <div className="relative aspect-video w-full overflow-hidden">
                <Image src="/images/knowledge_guides.jpg" alt="Technique Guides" fill className="object-cover group-hover:scale-105 transition-transform duration-500" />
                <div className="absolute inset-0 bg-gradient-to-t from-[var(--bg-card)] to-transparent" />
              </div>
              <div className="p-6 relative z-10 flex-grow flex flex-col justify-end -mt-16">
                <div className="text-xs font-mono uppercase text-[var(--accent-forge)] mb-2 tracking-wider">
                  03 &middot; TECHNIQUE
                </div>
                <h3 className="text-2xl font-bold text-[var(--text-primary)] mb-2 group-hover:text-[var(--accent-forge)] transition-colors">
                  Knowledge Guides
                </h3>
                <p className="text-sm text-[var(--text-secondary)] leading-relaxed mb-4">
                  Progressive disclosure: simple explanations to deep mechanics.
                </p>
                <div className="mt-auto text-xs text-[var(--text-muted)] font-medium flex items-center gap-1 group-hover:text-[var(--text-primary)] group-hover:translate-x-1 transition-all">
                  READ GUIDE &rarr;
                </div>
              </div>
            </Link>

            {/* Card 4: Projects */}
            <Link
              href="/projects"
              className="group relative rounded-sm border-[4px] border-[var(--border-focus)] shadow-2xl shadow-black/60 relative before:absolute before:inset-1 before:border before:border-[var(--border-muted)] before:pointer-events-none bg-[var(--bg-card)] overflow-hidden hover:border-[var(--border-focus)] transition-all flex flex-col"
            >
              <div className="relative aspect-video w-full overflow-hidden">
                <Image src="/images/apprentice_projects.jpg" alt="Apprentice Projects" fill className="object-cover group-hover:scale-105 transition-transform duration-500" />
                <div className="absolute inset-0 bg-gradient-to-t from-[var(--bg-card)] to-transparent" />
              </div>
              <div className="p-6 relative z-10 flex-grow flex flex-col justify-end -mt-16">
                <div className="text-xs font-mono uppercase text-[var(--accent-forge)] mb-2 tracking-wider">
                  04 &middot; PROGRESSION
                </div>
                <h3 className="text-2xl font-bold text-[var(--text-primary)] mb-2 group-hover:text-[var(--accent-forge)] transition-colors">
                  Apprentice Projects
                </h3>
                <p className="text-sm text-[var(--text-secondary)] leading-relaxed mb-4">
                  Step-by-step projects from Level 1 to Level 4 pattern welding.
                </p>
                <div className="mt-auto text-xs text-[var(--text-muted)] font-medium flex items-center gap-1 group-hover:text-[var(--text-primary)] group-hover:translate-x-1 transition-all">
                  EXPLORE &rarr;
                </div>
              </div>
            </Link>

            {/* Card 5: Tools */}
            <Link
              href="/tools"
              className="group relative rounded-sm border-[4px] border-[var(--border-focus)] shadow-2xl shadow-black/60 relative before:absolute before:inset-1 before:border before:border-[var(--border-muted)] before:pointer-events-none bg-[var(--bg-card)] overflow-hidden hover:border-[var(--border-focus)] transition-all flex flex-col md:col-span-2 lg:col-span-1"
            >
              <div className="relative aspect-video w-full overflow-hidden">
                <Image src="/images/tools_workshop.jpg" alt="Tools and Workshop" fill className="object-cover group-hover:scale-105 transition-transform duration-500" />
                <div className="absolute inset-0 bg-gradient-to-t from-[var(--bg-card)] to-transparent" />
              </div>
              <div className="p-6 relative z-10 flex-grow flex flex-col justify-end -mt-16">
                <div className="text-xs font-mono uppercase text-[var(--accent-forge)] mb-2 tracking-wider">
                  05 &middot; EQUIPMENT
                </div>
                <h3 className="text-2xl font-bold text-[var(--text-primary)] mb-2 group-hover:text-[var(--accent-forge)] transition-colors">
                  Tools &amp; Workshop
                </h3>
                <p className="text-sm text-[var(--text-secondary)] leading-relaxed mb-4">
                  Anvil anatomy, hammer selection, and workshop construction advice.
                </p>
                <div className="mt-auto text-xs text-[var(--text-muted)] font-medium flex items-center gap-1 group-hover:text-[var(--text-primary)] group-hover:translate-x-1 transition-all">
                  EXPLORE &rarr;
                </div>
              </div>
            </Link>

            {/* Card 6: Rules */}
            <Link
              href="/rules"
              className="group relative rounded-sm border-[4px] border-[var(--border-focus)] shadow-2xl shadow-black/60 relative before:absolute before:inset-1 before:border before:border-[var(--border-muted)] before:pointer-events-none bg-[var(--bg-card)] overflow-hidden hover:border-[var(--border-focus)] transition-all flex flex-col md:col-span-2 lg:col-span-1"
            >
              <div className="relative aspect-video w-full overflow-hidden">
                <Image src="/images/safety_rules.jpg" alt="Safety and Rules" fill className="object-cover group-hover:scale-105 transition-transform duration-500" />
                <div className="absolute inset-0 bg-gradient-to-t from-[var(--bg-card)] to-transparent" />
              </div>
              <div className="p-6 relative z-10 flex-grow flex flex-col justify-end -mt-16">
                <div className="text-xs font-mono uppercase text-[var(--accent-forge)] mb-2 tracking-wider">
                  06 &middot; CODEX
                </div>
                <h3 className="text-2xl font-bold text-[var(--text-primary)] mb-2 group-hover:text-[var(--accent-forge)] transition-colors">
                  Safety &amp; Rules
                </h3>
                <p className="text-sm text-[var(--text-secondary)] leading-relaxed mb-4">
                  Safety protocols, controlled sources, and anti-hallucination rules.
                </p>
                <div className="mt-auto text-xs text-[var(--text-muted)] font-medium flex items-center gap-1 group-hover:text-[var(--text-primary)] group-hover:translate-x-1 transition-all">
                  READ RULES &rarr;
                </div>
              </div>
            </Link>
          </div>
        </section>

        {/* Apprentice Note Banner */}
        <section className="rounded-sm bg-[var(--bg-surface)] border-l-4 border-[var(--accent-forge)] p-8 sm:p-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-8 shadow-xl">
          <div className="max-w-3xl">
            <div className="text-xs font-bold uppercase tracking-widest text-[var(--accent-forge)] mb-2">
              THE APPRENTICE'S RULE
            </div>
            <h3 className="text-2xl sm:text-3xl font-bold text-[var(--text-primary)] mb-4">
              You do not need an expensive shop to start learning.
            </h3>
            <p className="text-base text-[var(--text-secondary)] leading-relaxed">
              A solid striking surface, a 2 lb cross-peen hammer, basic tongs, and a small fire are enough to begin.
            </p>
          </div>

          <Link
            href="/workshop"
            className="shrink-0 inline-flex items-center justify-center rounded-md border border-[var(--border-muted)] bg-[var(--bg-card)] px-6 py-3 text-sm font-bold text-[var(--text-primary)] hover:border-[var(--border-focus)] hover:bg-[var(--bg-surface-hover)] hover:text-white transition-all"
          >
            VIEW MINIMUM SETUP &rarr;
          </Link>
        </section>

      </div>
    </div>
  );
}
