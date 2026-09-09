import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Workshop Infrastructure — Blacksmith Knight",
  description: "Setting up a practical home forge: layout, ventilation, fire safety, and essential equipment.",
};

export default function WorkshopPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3">
          Workshop Setup
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Workshop Infrastructure &amp; Safety
        </h1>
        <p className="text-neutral-400 mt-2 max-w-2xl text-base sm:text-lg">
          Practical advice on building an efficient, safe workspace without requiring an expensive industrial setup.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <h2 className="text-xl font-bold text-white mb-2">Forge Ventilation &amp; Airflow</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Carbon monoxide risks, side-draft chimneys, hooded extractors, and airflow considerations for garage and shed setups.
          </p>
          <div className="text-xs text-[#FF5722] font-semibold">Priority: Essential Workshop Safety</div>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <h2 className="text-xl font-bold text-white mb-2">Anvil Stands &amp; Height Ergonomics</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Setting the correct anvil height to your knuckles, securing to timber rounds or sand-filled steel drums, and vibration dampening.
          </p>
          <div className="text-xs text-neutral-400 font-semibold">Focus: Joint &amp; Tendon Longevity</div>
        </div>
      </div>
    </div>
  );
}
