"use client";

interface DiyAlternativesCardProps {
  diyAlternatives?: string[];
  diyBuildable?: boolean;
  toolName: string;
}

export default function DiyAlternativesCard({
  diyAlternatives,
  diyBuildable,
  toolName,
}: DiyAlternativesCardProps) {
  if (!diyAlternatives || diyAlternatives.length === 0) {
    return null;
  }

  return (
    <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
      <div className="flex items-center justify-between mb-4 border-b border-neutral-800/80 pb-3">
        <div className="flex items-center gap-2">
          <span className="text-[#FF5722] text-lg">💡</span>
          <h3 className="text-base font-bold text-white">
            Budget &amp; DIY Alternatives — {toolName}
          </h3>
        </div>

        {diyBuildable ? (
          <span className="inline-flex items-center rounded-md border border-emerald-500/30 bg-emerald-500/10 px-2.5 py-0.5 text-xs font-mono text-emerald-400">
            ✓ Forge or Build Yourself
          </span>
        ) : (
          <span className="inline-flex items-center rounded-md border border-neutral-700 bg-neutral-800 px-2.5 py-0.5 text-xs font-mono text-neutral-400">
            Sourced / Salvaged
          </span>
        )}
      </div>

      <p className="text-xs text-neutral-400 mb-4 leading-relaxed">
        High-end professional blacksmithing tools can be cost-prohibitive for beginners. You can start crafting immediately using these tested workshop improvisations:
      </p>

      <div className="space-y-2">
        {diyAlternatives.map((alt, idx) => (
          <div
            key={idx}
            className="flex items-start gap-3 rounded-lg border border-neutral-800 bg-neutral-900/60 p-3 text-xs text-neutral-200 font-mono"
          >
            <span className="text-emerald-400 font-bold">➜</span>
            <span>{alt}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
