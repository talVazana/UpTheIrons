import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Tools & Equipment — Blacksmith Knight",
  description: "Anvils, forging hammers, tongs, swages, and belt grinders evaluated for amateur makers.",
};

export default function ToolsPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3">
          Hardware &amp; Equipment
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Tools &amp; Equipment Encyclopedia
        </h1>
        <p className="text-neutral-400 mt-2 max-w-2xl text-base sm:text-lg">
          Unbiased tool recommendations. Value and durability first—expensive does not always mean better for a hobbyist.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-mono uppercase text-[#FF5722] mb-1">Striking Face</div>
          <h2 className="text-lg font-bold text-white mb-2">Anvil Anatomy &amp; Rebound</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Cast steel vs ductile iron, London pattern horn, pritchel and hardy holes, and ball-bearing rebound testing.
          </p>
          <div className="text-xs text-neutral-500 font-mono">Category: Forging Anvils</div>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-mono uppercase text-[#FF5722] mb-1">Impact</div>
          <h2 className="text-lg font-bold text-white mb-2">Cross-Peen Hammers</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Dressing the face to prevent sharp gouges, balance, handle alignment, and weight selection (2 lb vs 3 lb).
          </p>
          <div className="text-xs text-neutral-500 font-mono">Category: Hand Hammers</div>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-mono uppercase text-[#FF5722] mb-1">Grip &amp; Control</div>
          <h2 className="text-lg font-bold text-white mb-2">Essential Tongs</h2>
          <p className="text-sm text-neutral-400 mb-4">
            V-bit bolt tongs, flat-jaw tongs, and wolf-jaw tongs. Why gripping security is your primary safety defense.
          </p>
          <div className="text-xs text-neutral-500 font-mono">Category: Tongs</div>
        </div>
      </div>
    </div>
  );
}
