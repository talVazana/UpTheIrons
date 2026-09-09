"use client";

import { SafetyPrecaution } from "@/lib/types";

interface SafetySectionProps {
  precautions: SafetyPrecaution[];
}

export default function SafetySection({ precautions }: SafetySectionProps) {
  if (!precautions || precautions.length === 0) return null;

  const getLevelStyle = (level: string) => {
    switch (level.toLowerCase()) {
      case "critical":
        return {
          border: "border-red-600/60 bg-red-950/20",
          badge: "bg-red-900/60 text-red-200 border-red-700/80",
          icon: "🔥",
          label: "Critical Hazard",
        };
      case "warning":
        return {
          border: "border-[#FF5722]/50 bg-[#FF5722]/10",
          badge: "bg-[#FF5722]/20 text-[#FF8A65] border-[#FF5722]/40",
          icon: "⚠️",
          label: "Forge Warning",
        };
      case "caution":
      default:
        return {
          border: "border-amber-600/40 bg-amber-950/15",
          badge: "bg-amber-900/40 text-amber-200 border-amber-700/60",
          icon: "🛡️",
          label: "Workshop Caution",
        };
    }
  };

  return (
    <section aria-labelledby="safety-precautions-title" className="my-8">
      <div className="rounded-2xl border-2 border-red-900/40 bg-linear-to-b from-[#1c1414] to-[#141414] p-6 sm:p-8 shadow-xl">
        {/* Section Header */}
        <div className="flex items-center gap-3 border-b border-red-900/30 pb-4 mb-6">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-red-900/40 text-red-400 text-xl border border-red-700/40 shadow-inner">
            🛡️
          </div>
          <div>
            <h2 id="safety-precautions-title" className="text-lg sm:text-xl font-black text-white tracking-tight flex items-center gap-2">
              Mandatory Workshop Safety Protocol
            </h2>
            <p className="text-xs text-neutral-400 mt-0.5">
              Strict craft guardrails per Blacksmith Knight Safety Standards (ANSI Z87.1 / NRR 28+).
            </p>
          </div>
        </div>

        {/* Precautions Cards */}
        <div className="space-y-4">
          {precautions.map((p, idx) => {
            const style = getLevelStyle(p.level);
            return (
              <div
                key={idx}
                className={`rounded-xl border ${style.border} p-4 sm:p-5 transition-all shadow-xs`}
              >
                <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                  <span className={`inline-flex items-center gap-1.5 rounded-md border px-2.5 py-0.5 text-xs font-mono font-bold uppercase tracking-wider ${style.badge}`}>
                    <span>{style.icon}</span>
                    <span>{style.label}</span>
                  </span>

                  {p.ppe && p.ppe.length > 0 && (
                    <div className="flex flex-wrap items-center gap-1.5">
                      <span className="text-[11px] font-mono text-neutral-400 uppercase">PPE:</span>
                      {p.ppe.map((gear, gIdx) => (
                        <span
                          key={gIdx}
                          className="rounded bg-neutral-900/90 border border-neutral-700 px-2 py-0.5 text-[11px] font-medium text-neutral-200"
                        >
                          {gear}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="mt-2">
                  <h3 className="text-sm sm:text-base font-bold text-white mb-1.5">
                    {p.hazard}
                  </h3>
                  <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed">
                    <strong className="text-neutral-100 font-semibold">Mitigation: </strong>
                    {p.mitigation}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
