export default function HomePage() {
  return (
    <main className="min-h-screen px-6 py-12 max-w-6xl mx-auto">
      <header className="border-b border-neutral-800 pb-8 mb-10">
        <div className="inline-block px-3 py-1 text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 rounded-full mb-4">
          The Knight&apos;s Forge
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white mb-3">
          Blacksmith Knight
        </h1>
        <p className="text-lg text-neutral-400 max-w-2xl">
          Forging Heaven — Digital workshop, forge library, and technical vault for amateur blacksmithing, metallurgy, and craft.
        </p>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-xl bg-neutral-900 border border-neutral-800">
          <h2 className="text-xl font-bold text-white mb-2">Knowledge Library</h2>
          <p className="text-sm text-neutral-400">
            Metallurgy, steel specifications, heat treatment recipes, and practical guides.
          </p>
        </div>

        <div className="p-6 rounded-xl bg-neutral-900 border border-neutral-800">
          <h2 className="text-xl font-bold text-white mb-2">Curated Forge Feed</h2>
          <p className="text-sm text-neutral-400">
            Controlled video ingestion from approved YouTube master blacksmiths.
          </p>
        </div>

        <div className="p-6 rounded-xl bg-neutral-900 border border-neutral-800">
          <h2 className="text-xl font-bold text-white mb-2">Workshop &amp; Tools</h2>
          <p className="text-sm text-neutral-400">
            Anvil selection, forge design, tongs, hammers, and safety fundamentals.
          </p>
        </div>
      </section>

      <footer className="mt-16 pt-6 border-t border-neutral-800 text-xs text-neutral-500 flex justify-between items-center">
        <span>Blacksmith Knight &bull; Milestone 02 Initialized</span>
        <span>Local-first &bull; Non-commercial</span>
      </footer>
    </main>
  );
}
