import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Search Knowledge Vault — Kiko's BlackSmith Heaven",
  description: "Search across materials, steels, videos, guides, projects, and workshop tools.",
};

export default function SearchPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3">
          Knowledge Vault
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Search the Knowledge Vault
        </h1>
        <p className="text-neutral-400 mt-2 max-w-2xl text-base sm:text-lg">
          Instant search across steels, heat-treat recipes, YouTube videos, beginner projects, and tools.
        </p>
      </div>

      <div className="max-w-2xl mb-8">
        <div className="relative">
          <input
            type="search"
            placeholder="Search by steel grade (e.g. 1095), technique, or tool..."
            className="w-full rounded-lg border border-neutral-700 bg-neutral-900 px-4 py-3 text-white placeholder-neutral-500 focus-visible:border-[#FF5722] focus-visible:ring-2 focus-visible:ring-[#FF5722] text-sm"
          />
        </div>

        <div className="flex flex-wrap gap-2 mt-4 text-xs">
          <span className="text-neutral-500 self-center mr-1">Quick Filters:</span>
          {["All", "Steels", "Heat Treatment", "Anvils", "Beginner Projects", "Curated Videos"].map(
            (filter, i) => (
              <button
                key={filter}
                type="button"
                className={`px-3 py-1 rounded-full font-medium transition-colors ${
                  i === 0
                    ? "bg-[#FF5722] text-white"
                    : "bg-neutral-800 text-neutral-300 hover:bg-neutral-700 hover:text-white"
                }`}
              >
                {filter}
              </button>
            )
          )}
        </div>
      </div>

      <div className="rounded-xl border border-dashed border-neutral-800 p-8 text-center text-neutral-500 text-sm">
        Type a query or select a category above to query the forge knowledge database.
      </div>
    </div>
  );
}
