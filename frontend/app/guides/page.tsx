import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Knowledge Guides — Blacksmith Knight",
  description: "Practical guides on fire control, hammer technique, heat treatment, and workshop practice.",
};

export default function GuidesPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3">
          The Knight&apos;s Library
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Practical Knowledge Guides
        </h1>
        <p className="text-neutral-400 mt-2 max-w-2xl text-base sm:text-lg">
          Clear, step-by-step technical guides: simple explanation first, practical steps second, metallurgical depth third.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-semibold uppercase tracking-wider text-[#FF5722] mb-1">
            Heat Treatment Baseline
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Understanding Normalizing</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Why resetting steel grain structure and relieving forging stress prevents warpage and catastrophic cracks during the quench.
          </p>
          <span className="text-xs text-neutral-500 font-mono">Difficulty: Beginner &bull; 6 min read</span>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-semibold uppercase tracking-wider text-[#FF5722] mb-1">
            Forge Fundamentals
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Fire Control &amp; Heat Colors</h2>
          <p className="text-sm text-neutral-400 mb-4">
            How to read incandescent steel colors, avoid excessive scale formation, and maintain proper atmospheric conditions in propane and solid fuel forges.
          </p>
          <span className="text-xs text-neutral-500 font-mono">Difficulty: Beginner &bull; 8 min read</span>
        </div>
      </div>
    </div>
  );
}
