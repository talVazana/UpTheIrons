import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Projects Library — Blacksmith Knight",
  description: "Hands-on projects organized by progressive skill levels, from basic hooks to forged blades.",
};

export default function ProjectsPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3">
          Apprentice Path
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Projects Library
        </h1>
        <p className="text-neutral-400 mt-2 max-w-2xl text-base sm:text-lg">
          Practical workshop builds designed to build muscle memory, hammer control, and forging discipline.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-1">
            Level 1 &bull; Apprentice
          </div>
          <h2 className="text-lg font-bold text-white mb-2">Classic S-Hook</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Master the fundamentals: drawing out a square taper, rounding, and bending over the horn.
          </p>
          <div className="text-xs text-neutral-500 font-mono">Time: 45 min &bull; Material: 3/8&quot; Mild Steel</div>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-1">
            Level 1 &bull; Apprentice
          </div>
          <h2 className="text-lg font-bold text-white mb-2">Forged Leaf Keychain</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Learn beveling, shoulder work, fullering with the anvil edge, and delicate scroll finishing.
          </p>
          <div className="text-xs text-neutral-500 font-mono">Time: 1 hr &bull; Material: 1/4&quot; Round Stock</div>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-1">
            Level 2 &bull; Smith
          </div>
          <h2 className="text-lg font-bold text-white mb-2">Center Punch &amp; Chisel</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Your first self-made workshop tools using high-carbon coil spring steel and basic differential tempering.
          </p>
          <div className="text-xs text-neutral-500 font-mono">Time: 2 hrs &bull; Material: 5160 Spring</div>
        </div>
      </div>
    </div>
  );
}
