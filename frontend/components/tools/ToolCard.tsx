"use client";

import Link from "next/link";
import { ToolItem } from "@/lib/types";

interface ToolCardProps {
  tool: ToolItem;
}

export default function ToolCard({ tool }: ToolCardProps) {
  const meta = tool.metadata;

  const categoryConfigs: Record<
    string,
    { label: string; badgeClass: string; icon: string }
  > = {
    forging: {
      label: "Forging Tool",
      badgeClass: "bg-[#FF5722]/10 text-[#FF8A65] border-[#FF5722]/30",
      icon: "⚒️",
    },
    heating: {
      label: "Heating & Fire",
      badgeClass: "bg-amber-500/10 text-amber-400 border-amber-500/30",
      icon: "🔥",
    },
    grinding: {
      label: "Grinding & Abrasive",
      badgeClass: "bg-sky-500/10 text-sky-400 border-sky-500/30",
      icon: "⚡",
    },
    finishing: {
      label: "Finishing & Polish",
      badgeClass: "bg-purple-500/10 text-purple-400 border-purple-500/30",
      icon: "✨",
    },
    infrastructure: {
      label: "Infrastructure",
      badgeClass: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
      icon: "🏛️",
    },
  };

  const cat = categoryConfigs[meta.tool_category || "forging"] || {
    label: (meta.tool_category || "Tool").toUpperCase(),
    badgeClass: "bg-neutral-800 text-neutral-300 border-neutral-700",
    icon: "🔧",
  };

  return (
    <div className="group relative flex flex-col justify-between rounded-xl border border-neutral-800 bg-[#181818] p-5 transition-all duration-200 hover:border-[#FF5722]/50 hover:bg-[#1f1f1f]">
      <div>
        {/* Header Badges */}
        <div className="flex items-start justify-between gap-2 mb-3">
          <div className="flex flex-wrap items-center gap-1.5">
            <span
              className={`inline-flex items-center gap-1 rounded-md border px-2 py-0.5 text-[11px] font-mono font-medium uppercase tracking-wider ${cat.badgeClass}`}
            >
              <span>{cat.icon}</span>
              <span>{cat.label}</span>
            </span>

            {meta.beginner_friendly ? (
              <span className="inline-flex items-center rounded-md border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 text-[11px] font-mono text-emerald-400">
                Beginner Friendly
              </span>
            ) : (
              <span className="inline-flex items-center rounded-md border border-amber-500/30 bg-amber-500/10 px-2 py-0.5 text-[11px] font-mono text-amber-400">
                Advanced Workshop
              </span>
            )}
          </div>

          {meta.diy_buildable && (
            <span className="inline-flex items-center rounded bg-neutral-800/80 px-1.5 py-0.5 text-[10px] font-mono text-neutral-300 border border-neutral-700/60" title="Can be forged or built in a home workshop">
              DIY Buildable
            </span>
          )}
        </div>

        {/* Title & Purpose */}
        <Link href={`/workshop/${tool.slug}`} className="block group-hover:text-white">
          <h3 className="text-xl font-bold text-white transition-colors group-hover:text-[#FF8A65]">
            {tool.title}
          </h3>
          <p className="text-xs text-neutral-300 mt-2 line-clamp-2 leading-relaxed">
            {tool.summary}
          </p>
        </Link>

        {/* Essential For Chips */}
        {meta.essential_for && meta.essential_for.length > 0 && (
          <div className="mt-4 pt-3 border-t border-neutral-800/80">
            <span className="text-[10px] font-mono uppercase tracking-wider text-neutral-500 block mb-1.5">
              Essential For:
            </span>
            <div className="flex flex-wrap gap-1.5">
              {meta.essential_for.slice(0, 3).map((item, idx) => (
                <span
                  key={idx}
                  className="rounded bg-neutral-900/80 px-2 py-0.5 text-[11px] font-mono text-neutral-300 border border-neutral-800"
                >
                  {item}
                </span>
              ))}
              {meta.essential_for.length > 3 && (
                <span className="rounded bg-neutral-900/50 px-1.5 py-0.5 text-[10px] font-mono text-neutral-500">
                  +{meta.essential_for.length - 3} more
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="mt-5 pt-3 border-t border-neutral-800 flex items-center justify-between text-xs font-mono">
        <span className="text-neutral-500 text-[11px]">
          {meta.selection_criteria?.length || 0} Selection Rules
        </span>

        <Link
          href={`/workshop/${tool.slug}`}
          className="font-semibold text-[#FF5722] hover:text-[#FF8A65] inline-flex items-center gap-1 transition-colors"
        >
          <span>Tool Guide</span>
          <span>→</span>
        </Link>
      </div>
    </div>
  );
}
