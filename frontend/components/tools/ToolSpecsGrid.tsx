"use client";

interface ToolSpecsGridProps {
  specifications?: Record<string, any>;
  toolName: string;
}

export default function ToolSpecsGrid({
  specifications,
  toolName,
}: ToolSpecsGridProps) {
  if (!specifications || Object.keys(specifications).length === 0) {
    return null;
  }

  const entries = Object.entries(specifications);

  return (
    <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
      <div className="flex items-center justify-between mb-4 border-b border-neutral-800/80 pb-3">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <span className="text-[#FF5722]">📐</span> Technical Specifications — {toolName}
        </h3>
        <span className="text-[11px] font-mono uppercase tracking-wider text-neutral-400 bg-neutral-800 px-2 py-0.5 rounded">
          Engineering Benchmark
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {entries.map(([key, val]) => {
          const formattedKey = key.replace(/_/g, " ").toUpperCase();
          const displayVal = typeof val === "object" ? JSON.stringify(val) : String(val);

          return (
            <div
              key={key}
              className="rounded-lg border border-neutral-800/80 bg-neutral-900/50 p-3"
            >
              <span className="text-[10px] font-mono uppercase tracking-wider text-neutral-500 block mb-0.5">
                {formattedKey}
              </span>
              <span className="text-xs sm:text-sm font-mono font-semibold text-neutral-200 block">
                {displayVal}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
