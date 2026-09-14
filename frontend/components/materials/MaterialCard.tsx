"use client";

import Link from "next/link";
import { MaterialItem } from "@/lib/types";

interface MaterialCardProps {
  material: MaterialItem;
  isSelectedForCompare?: boolean;
  onToggleCompare?: (slug: string) => void;
  canSelectMore?: boolean;
  isAdmin?: boolean;
  onDelete?: (slug: string) => void;
}

export default function MaterialCard({
  material,
  isSelectedForCompare = false,
  onToggleCompare,
  canSelectMore = true,
  isAdmin = false,
  onDelete,
}: MaterialCardProps) {
  const meta = material.metadata;
  const carbonPct = meta.carbon_pct ?? 0;
  const ht = meta.heat_treatment;
  const alloyingKeys = Object.keys(meta.alloying_elements || {});

  // Category styling
  const categoryLabels: Record<string, { label: string; badgeClass: string }> = {
    carbon_steel: {
      label: "Carbon Steel",
      badgeClass: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    },
    tool_steel: {
      label: "Tool Steel",
      badgeClass: "bg-sky-500/10 text-sky-400 border-sky-500/30",
    },
    spring_steel: {
      label: "Spring Steel",
      badgeClass: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    },
    alloy_steel: {
      label: "Alloy Steel",
      badgeClass: "bg-purple-500/10 text-purple-400 border-purple-500/30",
    },
    stainless_steel: {
      label: "Stainless Steel",
      badgeClass: "bg-cyan-500/10 text-cyan-400 border-cyan-500/30",
    },
  };

  const categoryInfo = categoryLabels[meta.steel_category || "carbon_steel"] || {
    label: (meta.steel_category || "Steel").replace(/_/g, " "),
    badgeClass: "bg-neutral-800 text-neutral-300 border-neutral-700",
  };

  return (
    <div
      className={`group relative flex flex-col justify-between rounded-xl border bg-[#181818] p-5 transition-all duration-200 hover:border-[#FF5722]/50 hover:bg-[#1f1f1f] ${
        isSelectedForCompare
          ? "border-[#FF5722] ring-1 ring-[#FF5722]/40 shadow-lg shadow-[#FF5722]/10"
          : "border-neutral-800"
      }`}
    >
      <div>
        {/* Top Header & Badges */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex flex-wrap items-center gap-2">
            <span
              className={`inline-flex items-center rounded-md border px-2 py-0.5 text-[11px] font-mono font-medium uppercase tracking-wider ${categoryInfo.badgeClass}`}
            >
              {categoryInfo.label}
            </span>

            {meta.beginner_suitability ? (
              <span className="inline-flex items-center gap-1 rounded-md border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 text-[11px] font-mono text-emerald-400">
                <span>✓</span> Beginner Suitable
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 rounded-md border border-amber-500/30 bg-amber-500/10 px-2 py-0.5 text-[11px] font-mono text-amber-400">
                <span>⚠</span> Advanced Forging
              </span>
            )}
          </div>

          {/* Compare Toggle */}
          {onToggleCompare && (
            <button
              type="button"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                onToggleCompare(material.slug);
              }}
              disabled={!isSelectedForCompare && !canSelectMore}
              className={`flex items-center gap-1.5 rounded-md border px-2 py-1 text-xs font-mono transition-colors ${
                isSelectedForCompare
                  ? "border-[#FF5722] bg-[#FF5722]/20 text-[#FF8A65] font-semibold"
                  : canSelectMore
                  ? "border-neutral-700 bg-neutral-800/80 text-neutral-400 hover:border-neutral-600 hover:text-white"
                  : "border-neutral-800 bg-neutral-900 text-neutral-600 cursor-not-allowed"
              }`}
              title={
                isSelectedForCompare
                  ? "Remove from comparison"
                  : canSelectMore
                  ? "Add to comparison"
                  : "Maximum 4 steels selected"
              }
            >
              <span
                className={`h-3 w-3 rounded-xs border flex items-center justify-center text-[9px] ${
                  isSelectedForCompare
                    ? "border-[#FF5722] bg-[#FF5722] text-black font-black"
                    : "border-neutral-600"
                }`}
              >
                {isSelectedForCompare ? "✓" : ""}
              </span>
              <span>Compare</span>
            </button>
          )}
        </div>

        {/* Steel Title & Classification */}
        <Link href={`/materials/${material.slug}`} className="block group-hover:text-white">
          <h3 className="text-xl font-bold text-white transition-colors group-hover:text-[#FF8A65]">
            {material.title}
          </h3>
          <p className="text-xs font-mono text-neutral-400 mt-0.5 mb-2 line-clamp-1">
            {meta.classification}
          </p>
          <p className="text-xs text-neutral-300 line-clamp-2 leading-relaxed mb-4">
            {material.summary}
          </p>
        </Link>

        {/* Carbon Visualizer */}
        <div className="mb-4 rounded-lg border border-neutral-800/80 bg-neutral-900/60 p-2.5">
          <div className="flex items-center justify-between text-xs mb-1.5">
            <span className="font-mono text-neutral-400">Carbon Content:</span>
            <span className="font-mono font-bold text-white">{carbonPct.toFixed(2)}% C</span>
          </div>
          <div className="h-1.5 w-full overflow-hidden rounded-full bg-neutral-800">
            <div
              className="h-full rounded-full bg-gradient-to-r from-amber-500 to-[#FF5722]"
              style={{ width: `${Math.min(100, (carbonPct / 1.5) * 100)}%` }}
            />
          </div>
        </div>

        {/* Quick Tech Specs */}
        <div className="grid grid-cols-2 gap-2 text-xs font-mono mb-4">
          <div className="rounded-md border border-neutral-800 bg-neutral-900/40 p-2">
            <span className="text-neutral-500 block text-[10px] uppercase">Forging Range</span>
            <span className="text-neutral-200 font-semibold truncate block">
              {meta.forging_temp_range_f || "1650°F – 2050°F"}
            </span>
          </div>
          <div className="rounded-md border border-neutral-800 bg-neutral-900/40 p-2">
            <span className="text-neutral-500 block text-[10px] uppercase">Target Hardness</span>
            <span className="text-neutral-200 font-semibold truncate block">
              {ht?.target_hardness_hrc || "58 – 61 HRC"}
            </span>
          </div>
        </div>

        {/* Alloying Elements Badges */}
        {alloyingKeys.length > 0 && (
          <div className="mb-4">
            <span className="text-[10px] font-mono uppercase tracking-wider text-neutral-500 block mb-1.5">
              Key Alloying Elements:
            </span>
            <div className="flex flex-wrap gap-1.5">
              {alloyingKeys.slice(0, 4).map((element) => {
                const pct = meta.alloying_elements[element];
                return (
                  <span
                    key={element}
                    className="inline-flex items-center gap-1 rounded bg-neutral-800/80 px-1.5 py-0.5 text-[11px] font-mono text-neutral-300 border border-neutral-700/50"
                  >
                    <span className="capitalize">{element}:</span>
                    <span className="text-[#FF8A65] font-semibold">{pct}%</span>
                  </span>
                );
              })}
              {alloyingKeys.length > 4 && (
                <span className="inline-flex items-center rounded bg-neutral-800/60 px-1.5 py-0.5 text-[10px] font-mono text-neutral-500">
                  +{alloyingKeys.length - 4} more
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Card Footer: Quench & Handbook Citation */}
      <div className="border-t border-neutral-800/80 pt-3 mt-2 flex items-center justify-between text-xs">
        <div className="text-[11px] font-mono text-neutral-400 truncate max-w-[50%]">
          <span className="text-neutral-500">Quench: </span>
          <span className="text-neutral-300 font-medium">
            {ht?.quench_medium ? ht.quench_medium.split("(")[0].trim() : "Oil Quench"}
          </span>
        </div>

        <div className="flex items-center gap-3">
          {isAdmin && onDelete && (
            <button
              onClick={() => onDelete(material.slug)}
              className="font-mono text-xs font-semibold text-red-500 hover:text-red-400 transition-colors"
            >
              Remove
            </button>
          )}
          <Link
            href={`/materials/${material.slug}`}
            className="font-mono text-xs font-semibold text-[#FF5722] hover:text-[#FF8A65] inline-flex items-center gap-1 transition-colors"
          >
            <span>Dossier</span>
            <span>→</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
