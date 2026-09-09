import Link from "next/link";

export default function HomePage() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10 sm:py-16">
      {/* Hero Section */}
      <section className="relative rounded-2xl border border-neutral-800 bg-gradient-to-b from-neutral-900/90 via-[#161616] to-[#121212] p-8 sm:p-12 mb-16 overflow-hidden">
        <div className="absolute top-0 right-0 -mt-8 -mr-8 w-64 h-64 bg-[#FF5722]/5 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 border border-[#FF5722]/20 rounded-full mb-6">
            <span className="w-1.5 h-1.5 rounded-full bg-[#FF5722] animate-pulse"></span>
            The Digital Forge &amp; Knowledge Vault
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white mb-6 leading-tight">
            Knowledge, Steel, <br className="hidden sm:inline" />
            Fire &amp; Craftsmanship.
          </h1>

          <p className="text-base sm:text-xl text-neutral-300 mb-8 leading-relaxed">
            A digital blacksmith&apos;s workshop and engineering reference designed for amateur makers.
            Learn the craft, understand the metallurgy, build your workshop, and forge your own path.
          </p>

          <div className="flex flex-wrap gap-4">
            <Link
              href="/materials"
              className="inline-flex items-center justify-center rounded-lg bg-[#FF5722] px-5 py-3 text-sm font-semibold text-white hover:bg-[#FF7043] transition-colors focus-visible:ring-2 focus-visible:ring-[#FF5722] shadow-lg shadow-[#FF5722]/20"
            >
              Explore Materials
            </Link>

            <Link
              href="/projects"
              className="inline-flex items-center justify-center rounded-lg border border-neutral-700 bg-neutral-850 px-5 py-3 text-sm font-semibold text-neutral-200 hover:bg-neutral-800 hover:text-white transition-colors focus-visible:ring-2 focus-visible:ring-[#FF5722]"
            >
              Apprentice Projects
            </Link>

            <Link
              href="/guides"
              className="inline-flex items-center justify-center rounded-lg border border-transparent px-5 py-3 text-sm font-semibold text-neutral-400 hover:text-white transition-colors"
            >
              Read Guides &rarr;
            </Link>
          </div>
        </div>
      </section>

      {/* Bento Pillars Section */}
      <section className="mb-16">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
              The Forge Pillars
            </h2>
            <p className="text-sm text-neutral-400 mt-1">
              Explore technical references, curated videos, and hands-on projects.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: Materials */}
          <Link
            href="/materials"
            className="group rounded-xl border border-neutral-800 bg-[#171717] p-6 hover:border-[#FF5722]/50 hover:bg-[#1c1c1c] transition-all flex flex-col justify-between"
          >
            <div>
              <div className="text-xs font-mono uppercase text-[#FF5722] mb-2 tracking-wider">
                01 &bull; Metallurgy
              </div>
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-[#FF5722] transition-colors">
                Materials &amp; Steel Database
              </h3>
              <p className="text-sm text-neutral-400 leading-relaxed">
                Chemical compositions, carbon percentages, heating ranges, quenching media, and predictable heat treatment.
              </p>
            </div>
            <div className="mt-6 text-xs text-neutral-500 font-medium flex items-center gap-1 group-hover:translate-x-1 transition-transform">
              <span>Inspect steels</span> &rarr;
            </div>
          </Link>

          {/* Card 2: Videos */}
          <Link
            href="/videos"
            className="group rounded-xl border border-neutral-800 bg-[#171717] p-6 hover:border-[#FF5722]/50 hover:bg-[#1c1c1c] transition-all flex flex-col justify-between"
          >
            <div>
              <div className="text-xs font-mono uppercase text-[#FF5722] mb-2 tracking-wider">
                02 &bull; Visual Learning
              </div>
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-[#FF5722] transition-colors">
                Curated Video Forge
              </h3>
              <p className="text-sm text-neutral-400 leading-relaxed">
                Controlled YouTube ingestion strictly from master smith channels you approve. No noise, no open crawler spam.
              </p>
            </div>
            <div className="mt-6 text-xs text-neutral-500 font-medium flex items-center gap-1 group-hover:translate-x-1 transition-transform">
              <span>View channels</span> &rarr;
            </div>
          </Link>

          {/* Card 3: Guides */}
          <Link
            href="/guides"
            className="group rounded-xl border border-neutral-800 bg-[#171717] p-6 hover:border-[#FF5722]/50 hover:bg-[#1c1c1c] transition-all flex flex-col justify-between"
          >
            <div>
              <div className="text-xs font-mono uppercase text-[#FF5722] mb-2 tracking-wider">
                03 &bull; Technique
              </div>
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-[#FF5722] transition-colors">
                Knowledge &amp; Technique Guides
              </h3>
              <p className="text-sm text-neutral-400 leading-relaxed">
                Progressive disclosure: simple explanation first, practical steps second, and deep metallurgical mechanics third.
              </p>
            </div>
            <div className="mt-6 text-xs text-neutral-500 font-medium flex items-center gap-1 group-hover:translate-x-1 transition-transform">
              <span>Read guides</span> &rarr;
            </div>
          </Link>

          {/* Card 4: Projects */}
          <Link
            href="/projects"
            className="group rounded-xl border border-neutral-800 bg-[#171717] p-6 hover:border-[#FF5722]/50 hover:bg-[#1c1c1c] transition-all flex flex-col justify-between"
          >
            <div>
              <div className="text-xs font-mono uppercase text-[#FF5722] mb-2 tracking-wider">
                04 &bull; Progression
              </div>
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-[#FF5722] transition-colors">
                Apprentice Projects
              </h3>
              <p className="text-sm text-neutral-400 leading-relaxed">
                Step-by-step projects from Level 1 S-hooks and leaves to Level 4 pattern welding and complex tool making.
              </p>
            </div>
            <div className="mt-6 text-xs text-neutral-500 font-medium flex items-center gap-1 group-hover:translate-x-1 transition-transform">
              <span>Start forging</span> &rarr;
            </div>
          </Link>

          {/* Card 5: Workshop & Tools */}
          <Link
            href="/tools"
            className="group rounded-xl border border-neutral-800 bg-[#171717] p-6 hover:border-[#FF5722]/50 hover:bg-[#1c1c1c] transition-all flex flex-col justify-between"
          >
            <div>
              <div className="text-xs font-mono uppercase text-[#FF5722] mb-2 tracking-wider">
                05 &bull; Equipment
              </div>
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-[#FF5722] transition-colors">
                Tools &amp; Workshop Setup
              </h3>
              <p className="text-sm text-neutral-400 leading-relaxed">
                Anvil anatomy, hammer selection, tong geometries, forge ventilation, and practical workshop construction advice.
              </p>
            </div>
            <div className="mt-6 text-xs text-neutral-500 font-medium flex items-center gap-1 group-hover:translate-x-1 transition-transform">
              <span>Examine tools</span> &rarr;
            </div>
          </Link>

          {/* Card 6: Rules & Safety */}
          <Link
            href="/rules"
            className="group rounded-xl border border-neutral-800 bg-[#171717] p-6 hover:border-[#FF5722]/50 hover:bg-[#1c1c1c] transition-all flex flex-col justify-between"
          >
            <div>
              <div className="text-xs font-mono uppercase text-[#FF5722] mb-2 tracking-wider">
                06 &bull; Codex
              </div>
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-[#FF5722] transition-colors">
                Safety &amp; Rules Codex
              </h3>
              <p className="text-sm text-neutral-400 leading-relaxed">
                The non-commercial manifesto, safety protocols, controlled source architecture, and anti-hallucination rules.
              </p>
            </div>
            <div className="mt-6 text-xs text-neutral-500 font-medium flex items-center gap-1 group-hover:translate-x-1 transition-transform">
              <span>Read rules</span> &rarr;
            </div>
          </Link>
        </div>
      </section>

      {/* Apprentice Note Banner */}
      <section className="rounded-xl border border-neutral-800 bg-[#151515] p-6 sm:p-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        <div>
          <div className="text-xs font-bold uppercase tracking-wider text-[#FF5722] mb-1">
            The Apprentice&apos;s Rule
          </div>
          <h3 className="text-lg sm:text-xl font-bold text-white mb-2">
            You do not need an expensive shop to start learning.
          </h3>
          <p className="text-sm text-neutral-400 max-w-2xl">
            A solid striking surface, a 2 lb cross-peen hammer, basic tongs, personal protective equipment,
            and a small fire are all that is required to move hot steel.
          </p>
        </div>

        <Link
          href="/workshop"
          className="shrink-0 rounded-lg border border-neutral-700 bg-neutral-800 px-4 py-2 text-sm font-semibold text-neutral-200 hover:bg-neutral-700 hover:text-white transition-colors"
        >
          View Minimum Setup
        </Link>
      </section>
    </div>
  );
}
