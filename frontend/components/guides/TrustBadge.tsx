"use client";

import { TrustLabel } from "@/lib/types";

interface TrustBadgeProps {
  label: TrustLabel | string;
  size?: "sm" | "md" | "lg";
  showTooltip?: boolean;
}

interface TrustConfig {
  name: string;
  badgeStyle: string;
  icon: string;
  description: string;
}

const TRUST_CONFIGS: Record<string, TrustConfig> = {
  fact: {
    name: "Physical Fact",
    badgeStyle: "border-sky-500/40 bg-sky-950/30 text-sky-300",
    icon: "⚖️",
    description: "Empirically verified metallurgical law or measurable physics (e.g. phase temperatures, Curie point, density).",
  },
  source_backed_recommendation: {
    name: "Source-Backed",
    badgeStyle: "border-emerald-500/40 bg-emerald-950/30 text-emerald-300",
    icon: "📚",
    description: "Backed by peer-reviewed metallurgical literature, published engineering handbooks, or certified manufacturer data.",
  },
  craft_practice: {
    name: "Craft Practice",
    badgeStyle: "border-[#FF5722]/50 bg-[#FF5722]/10 text-[#FF8A65]",
    icon: "⚒️",
    description: "Traditional blacksmith guild convention refined across generations of workshop practice.",
  },
  personal_experience: {
    name: "Workshop Experience",
    badgeStyle: "border-purple-500/40 bg-purple-950/30 text-purple-300",
    icon: "🪵",
    description: "Direct observation or shop trial by an individual craftsman. Results may vary with tooling or fire conditions.",
  },
  historical_interpretation: {
    name: "Historical Record",
    badgeStyle: "border-amber-600/40 bg-amber-950/30 text-amber-300",
    icon: "🏛️",
    description: "Archaeological, metallurgical, or historical period reconstruction of antique smithing methods.",
  },
  ai_summary: {
    name: "AI Synthesis",
    badgeStyle: "border-indigo-500/40 bg-indigo-950/30 text-indigo-300",
    icon: "✦",
    description: "Synthesized or categorized by an automated AI model; check cited human references for safety-critical dimensions.",
  },
  opinion: {
    name: "Subjective Opinion",
    badgeStyle: "border-neutral-700 bg-neutral-800 text-neutral-300",
    icon: "💭",
    description: "Subjective craftsman preference or ergonomic choice. Not an absolute standard.",
  },
};

export default function TrustBadge({ label, size = "sm", showTooltip = true }: TrustBadgeProps) {
  const config = TRUST_CONFIGS[label] || {
    name: label.replace(/_/g, " "),
    badgeStyle: "border-neutral-700 bg-neutral-800 text-neutral-300",
    icon: "🏷️",
    description: "Technical trust classification.",
  };

  const sizeClasses = {
    sm: "text-[11px] px-2 py-0.5 gap-1.5",
    md: "text-xs px-2.5 py-1 gap-1.5",
    lg: "text-sm px-3.5 py-1.5 gap-2 font-medium",
  }[size];

  return (
    <span
      className={`group relative inline-flex items-center rounded-md border font-mono uppercase tracking-wider font-semibold ${config.badgeStyle} ${sizeClasses} cursor-help transition-all shadow-xs`}
      title={showTooltip ? `${config.name}: ${config.description}` : undefined}
    >
      <span className="text-[12px] leading-none" aria-hidden="true">
        {config.icon}
      </span>
      <span>{config.name}</span>

      {showTooltip && (
        <span className="pointer-events-none absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 rounded-lg border border-neutral-700 bg-[#161616] p-2.5 text-[11px] font-normal normal-case leading-relaxed text-neutral-200 opacity-0 shadow-2xl transition-all duration-200 group-hover:opacity-100 z-50 text-left">
          <span className="font-bold text-white block mb-0.5 flex items-center gap-1.5">
            <span>{config.icon}</span> {config.name}
          </span>
          <span className="text-neutral-400">{config.description}</span>
          <span className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-[#161616]" />
        </span>
      )}
    </span>
  );
}
