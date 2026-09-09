import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Materials & Steel Database — Blacksmith Knight",
  description: "Comprehensive metallurgical reference, carbon steels, alloy compositions, and heat treatment temperatures.",
};

export default function MaterialsPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3">
          Metallurgy Vault
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Materials &amp; Steel Database
        </h1>
        <p className="text-neutral-400 mt-2 max-w-2xl text-base sm:text-lg">
          Accurate, source-backed metallurgical references for high-carbon steels, tool steels, and alloying elements.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-mono uppercase text-[#FF5722] mb-1">Carbon Steel</div>
          <h2 className="text-xl font-bold text-white mb-2">1084 High Carbon</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Forgiving eutectoid steel ideal for beginners learning heat treatment and knife making.
          </p>
          <div className="text-xs text-neutral-500 font-mono">Carbon: ~0.84% &bull; Quench: Fast Oil</div>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-mono uppercase text-[#FF5722] mb-1">Carbon Steel</div>
          <h2 className="text-xl font-bold text-white mb-2">1095 High Carbon</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Hypereutectoid carbon steel capable of high hardness, hamon lines, and clean edge holding.
          </p>
          <div className="text-xs text-neutral-500 font-mono">Carbon: ~0.95% &bull; Quench: Fast Oil</div>
        </div>

        <div className="rounded-xl border border-neutral-800 bg-[#1a1a1a] p-6">
          <div className="text-xs font-mono uppercase text-[#FF5722] mb-1">Spring Steel</div>
          <h2 className="text-xl font-bold text-white mb-2">5160 Spring Steel</h2>
          <p className="text-sm text-neutral-400 mb-4">
            Tough chromium-bearing alloy suitable for larger blades, swords, axes, and striking tools.
          </p>
          <div className="text-xs text-neutral-500 font-mono">Carbon: ~0.60% &bull; Quench: Medium Oil</div>
        </div>
      </div>
    </div>
  );
}
