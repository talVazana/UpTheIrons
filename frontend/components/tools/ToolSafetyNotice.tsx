"use client";

import { SafetyPrecaution } from "@/lib/types";

interface ToolSafetyNoticeProps {
  safetyPrecautions?: SafetyPrecaution[];
  toolName: string;
}

export default function ToolSafetyNotice({
  safetyPrecautions,
  toolName,
}: ToolSafetyNoticeProps) {
  if (!safetyPrecautions || safetyPrecautions.length === 0) {
    return null;
  }

  return (
    <div className="rounded-xl border border-rose-500/30 bg-rose-950/10 p-6 space-y-4">
      <div className="flex items-center justify-between border-b border-rose-500/20 pb-3">
        <h3 className="text-base font-bold text-rose-300 flex items-center gap-2">
          <span>⚠️</span> Workshop Safety Protocols &amp; Hazards — {toolName}
        </h3>
        <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400 bg-rose-500/20 px-2 py-0.5 rounded border border-rose-500/30">
          Mandatory Precautions
        </span>
      </div>

      <div className="space-y-4">
        {safetyPrecautions.map((p, idx) => {
          const isCritical = p.level === "critical";

          return (
            <div
              key={idx}
              className={`rounded-lg border p-4 ${
                isCritical
                  ? "border-rose-500/40 bg-rose-950/20"
                  : "border-amber-500/30 bg-amber-950/10"
              }`}
            >
              <div className="flex items-center gap-2 mb-2">
                <span
                  className={`inline-flex items-center rounded px-2 py-0.5 text-[10px] font-mono font-bold uppercase ${
                    isCritical
                      ? "bg-rose-500 text-black"
                      : "bg-amber-500 text-black"
                  }`}
                >
                  {p.level}
                </span>
                <h4 className="text-xs sm:text-sm font-bold text-white">
                  {p.hazard}
                </h4>
              </div>

              <p className="text-xs text-neutral-300 leading-relaxed pl-1 mb-3">
                <strong className="text-neutral-200">Mitigation:</strong> {p.mitigation}
              </p>

              {p.ppe && p.ppe.length > 0 && (
                <div className="pt-2 border-t border-neutral-800/80 flex flex-wrap items-center gap-1.5">
                  <span className="text-[10px] font-mono uppercase text-neutral-400 mr-1">
                    Required PPE:
                  </span>
                  {p.ppe.map((item, ppeIdx) => (
                    <span
                      key={ppeIdx}
                      className="inline-flex items-center gap-1 rounded bg-neutral-900 px-2 py-0.5 text-[11px] font-mono text-neutral-300 border border-neutral-700/60"
                    >
                      <span>🛡️</span>
                      <span>{item}</span>
                    </span>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
