import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Rules & Safety Philosophy — Blacksmith Knight",
  description: "Our non-commercial rules, editorial criteria, safety policies, and anti-crawling guarantees.",
};

export default function RulesPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3">
          Codex &amp; Standards
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Rules &amp; Safety Philosophy
        </h1>
        <p className="text-neutral-400 mt-2 max-w-2xl text-base sm:text-lg">
          Clear principles governing content quality, metallurgical accuracy, safety, and source provenance.
        </p>
      </div>

      <div className="space-y-6 max-w-4xl">
        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <h2 className="text-xl font-bold text-white mb-2">1. Amateur First &amp; Non-Commercial</h2>
          <p className="text-sm text-neutral-400 leading-relaxed">
            Every feature must answer: &ldquo;Will this help a person working in their own workshop?&rdquo;
            We do not prioritize commercial sales or advertising over craft knowledge.
          </p>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <h2 className="text-xl font-bold text-white mb-2">2. Controlled Sources — No Open Web Crawling</h2>
          <p className="text-sm text-neutral-400 leading-relaxed">
            External content enters solely through user-approved YouTube channels, RSS feeds, and approved APIs.
            AI is never used to autonomously crawl the internet or add arbitrary sources.
          </p>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <h2 className="text-xl font-bold text-white mb-2">3. Metallurgical &amp; Technical Integrity</h2>
          <p className="text-sm text-neutral-400 leading-relaxed">
            AI models are strictly forbidden from inventing chemical compositions, heat treatment temperatures,
            or hardness numbers. When exact specifications matter, primary source references must be provided.
          </p>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <h2 className="text-xl font-bold text-white mb-2">4. Safety Is Part of the Craft</h2>
          <p className="text-sm text-neutral-400 leading-relaxed">
            Eye protection, respiratory safety against silica/grinding dust, forge ventilation, hearing protection,
            and fire emergency readiness are essential elements of craftsman competence, not annoying disclaimers.
          </p>
        </div>
      </div>
    </div>
  );
}
