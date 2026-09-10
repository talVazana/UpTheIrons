"use client";

interface SparkProfileCardProps {
  sparkProfile?: string | null;
  steelName: string;
}

export default function SparkProfileCard({
  sparkProfile,
  steelName,
}: SparkProfileCardProps) {
  return (
    <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
      <div className="flex items-center justify-between mb-4 border-b border-neutral-800/80 pb-3">
        <h4 className="text-base font-bold text-white flex items-center gap-2">
          <span className="text-[#FF5722]">✨</span> Spark Testing Signature — {steelName}
        </h4>
        <span className="text-[11px] font-mono uppercase tracking-wider text-neutral-400 bg-neutral-800 px-2 py-0.5 rounded">
          Shop Identification
        </span>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-start">
        {/* Spark Icon & Indicator */}
        <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl border border-[#FF5722]/30 bg-[#FF5722]/10 text-2xl shadow-inner">
          ⚡
        </div>

        <div className="flex-1">
          <p className="text-sm text-neutral-200 leading-relaxed font-sans mb-3">
            {sparkProfile ||
              "Dense bursts of branching sparks with bright starburst explosions indicating active carbon content."}
          </p>

          <div className="rounded-lg border border-neutral-800 bg-neutral-900/60 p-3 text-xs font-mono text-neutral-400">
            <strong className="text-neutral-300 block mb-1">Smith Diagnostic Rule:</strong>
            Touch the workpiece lightly to a high-speed aluminum oxide wheel in a darkened shop. Pure iron creates long uninterrupted straw-yellow shafts. Increasing carbon multiplies bursting starbursts close to the wheel. Chromium introduces red tips; tungsten creates short dark orange tails.
          </div>
        </div>
      </div>
    </div>
  );
}
