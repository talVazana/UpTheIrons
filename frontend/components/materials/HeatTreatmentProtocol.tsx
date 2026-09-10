"use client";

import { HeatTreatmentRecipe } from "@/lib/types";

interface HeatTreatmentProtocolProps {
  heatTreatment?: HeatTreatmentRecipe | null;
  steelName: string;
}

const TEMPER_COLORS: Record<string, { bg: string; text: string; label: string }> = {
  pale_straw: { bg: "#FFF8DC", text: "#000000", label: "Pale Straw (~375°F)" },
  straw: { bg: "#EEDC82", text: "#000000", label: "Straw (~400°F)" },
  dark_straw: { bg: "#C5A059", text: "#000000", label: "Dark Straw (~450°F)" },
  brown: { bg: "#8B4513", text: "#FFFFFF", label: "Brown / Bronze (~480°F)" },
  purple: { bg: "#800080", text: "#FFFFFF", label: "Purple (~500°F)" },
  blue: { bg: "#4169E1", text: "#FFFFFF", label: "Bright Blue (~540°F)" },
  dark_blue: { bg: "#00008B", text: "#FFFFFF", label: "Dark Blue (~600°F)" },
};

export default function HeatTreatmentProtocol({
  heatTreatment,
  steelName,
}: HeatTreatmentProtocolProps) {
  if (!heatTreatment) {
    return (
      <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6 text-neutral-400">
        <p className="text-sm">No certified heat treatment protocol recorded for this alloy.</p>
      </div>
    );
  }

  const ht = heatTreatment;

  return (
    <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6 border-b border-neutral-800/80 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span className="text-[#FF5722]">🔥</span> Heat Treatment Protocol — {steelName}
          </h3>
          <p className="text-xs text-neutral-400 mt-0.5">
            Strict thermal cycle sequence for grain refinement, martensitic conversion, and stress relief.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded-md border border-[#FF5722]/40 bg-[#FF5722]/10 px-2.5 py-1 text-xs font-mono font-semibold text-[#FF8A65]">
            Target: {ht.target_hardness_hrc || "58–61 HRC"}
          </span>
        </div>
      </div>

      {/* 4-Phase Forge Timeline */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        {/* Step 1: Normalizing */}
        <div className="rounded-lg border border-neutral-800 bg-neutral-900/50 p-4 relative overflow-hidden">
          <div className="text-[10px] font-mono uppercase tracking-wider text-neutral-500 mb-1 flex items-center justify-between">
            <span>Phase 1</span>
            <span className="text-neutral-400">Structural Reset</span>
          </div>
          <h4 className="text-sm font-bold text-white mb-1">Normalizing</h4>
          <div className="text-lg font-mono font-bold text-amber-400 mb-2">
            {ht.normalizing_temp_f ? `${ht.normalizing_temp_f}°F` : "1600°F – 1650°F"}
          </div>
          <p className="text-[11px] text-neutral-400 leading-relaxed">
            Refines coarse grains from heavy forging blows. Heat uniformly, soak briefly, then air cool in still shop air until black.
          </p>
        </div>

        {/* Step 2: Annealing */}
        <div className="rounded-lg border border-neutral-800 bg-neutral-900/50 p-4 relative overflow-hidden">
          <div className="text-[10px] font-mono uppercase tracking-wider text-neutral-500 mb-1 flex items-center justify-between">
            <span>Phase 2</span>
            <span className="text-neutral-400">Softening</span>
          </div>
          <h4 className="text-sm font-bold text-white mb-1">Annealing</h4>
          <div className="text-lg font-mono font-bold text-yellow-400 mb-2">
            {ht.annealing_temp_f ? `${ht.annealing_temp_f}°F` : "1450°F – 1500°F"}
          </div>
          <p className="text-[11px] text-neutral-400 leading-relaxed">
            Relieves internal stress for clean drilling, grinding, and filing. Cool very slowly inside vermiculite, lime, or furnace ramp down.
          </p>
        </div>

        {/* Step 3: Austenitizing & Hardening */}
        <div className="rounded-lg border border-[#FF5722]/40 bg-[#FF5722]/5 p-4 relative overflow-hidden ring-1 ring-[#FF5722]/20">
          <div className="text-[10px] font-mono uppercase tracking-wider text-[#FF8A65] mb-1 flex items-center justify-between">
            <span>Phase 3</span>
            <span className="text-[#FF8A65] font-bold">Critical</span>
          </div>
          <h4 className="text-sm font-bold text-white mb-1">Hardening</h4>
          <div className="text-lg font-mono font-bold text-[#FF5722] mb-2">
            {ht.hardening_temp_f ? `${ht.hardening_temp_f}°F` : "1475°F – 1525°F"}
          </div>
          <p className="text-[11px] text-neutral-300 leading-relaxed">
            {ht.soak_time_minutes ? `Hold for ${ht.soak_time_minutes} min soak.` : "Soak 5–10 minutes."} Watch for decalescence shadow line (~{ht.decalescence_temp_f || 1450}°F) as steel dissolves carbon into austenite.
          </p>
        </div>

        {/* Step 4: Quench */}
        <div className="rounded-lg border border-neutral-800 bg-neutral-900/50 p-4 relative overflow-hidden">
          <div className="text-[10px] font-mono uppercase tracking-wider text-neutral-500 mb-1 flex items-center justify-between">
            <span>Phase 4</span>
            <span className="text-sky-400">Martensite Freeze</span>
          </div>
          <h4 className="text-sm font-bold text-white mb-1">Quench Protocol</h4>
          <div className="text-xs font-mono font-bold text-sky-300 mb-2 truncate" title={ht.quench_medium || "Oil Quench"}>
            {ht.quench_medium ? ht.quench_medium.split("(")[0].trim() : "Medium Quench Oil"}
          </div>
          <p className="text-[11px] text-neutral-400 leading-relaxed">
            Agitate vertically edge-first. Avoid lateral slicing to prevent warping. Cool below 125°F before immediate temper.
          </p>
        </div>
      </div>

      {/* Detailed Quench & Safety Callout */}
      <div className="mb-6 rounded-lg border border-neutral-800 bg-neutral-900/80 p-4">
        <h5 className="text-xs font-mono uppercase font-bold text-neutral-300 mb-1 flex items-center gap-2">
          <span>🛡</span> Quench Medium &amp; Safety Spec:
        </h5>
        <p className="text-xs text-neutral-300 leading-relaxed">
          {ht.quench_medium || "Fast or medium speed quench oil."}
        </p>
        {ht.notes && (
          <p className="text-xs text-neutral-400 mt-2 font-mono border-t border-neutral-800 pt-2">
            <strong className="text-neutral-300">Smith Note:</strong> {ht.notes}
          </p>
        )}
      </div>

      {/* Tempering Schedule Table */}
      {ht.tempering_table && ht.tempering_table.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-3">
            <h5 className="text-sm font-bold text-white flex items-center gap-2">
              <span>📉</span> Tempering Calibration Curve &amp; Oxide Colors
            </h5>
            <span className="text-xs font-mono text-neutral-400">
              Standard: 2 cycles × 2 hours each
            </span>
          </div>

          <div className="overflow-x-auto rounded-lg border border-neutral-800">
            <table className="w-full text-left text-xs">
              <thead className="bg-neutral-900/90 text-neutral-400 font-mono uppercase text-[10px]">
                <tr>
                  <th className="px-4 py-2.5">Oven Temperature</th>
                  <th className="px-4 py-2.5">Resulting Hardness</th>
                  <th className="px-4 py-2.5">Toughness Profile</th>
                  <th className="px-4 py-2.5">Oxide Temper Color</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-800/80 font-mono">
                {ht.tempering_table.map((row, idx) => {
                  const colorConfig = TEMPER_COLORS[row.color] || {
                    bg: "#d4d4d4",
                    text: "#000000",
                    label: row.color.replace(/_/g, " "),
                  };

                  return (
                    <tr
                      key={idx}
                      className="transition-colors hover:bg-neutral-800/40"
                    >
                      <td className="px-4 py-3 font-bold text-white">
                        {row.temp_f}°F ({Math.round(((row.temp_f - 32) * 5) / 9)}°C)
                      </td>
                      <td className="px-4 py-3">
                        <span className="inline-flex items-center rounded bg-neutral-800 px-2 py-0.5 font-bold text-[#FF8A65]">
                          {row.hrc} HRC
                        </span>
                      </td>
                      <td className="px-4 py-3 text-neutral-300 capitalize">
                        {row.toughness}
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[11px] font-medium shadow-xs"
                          style={{
                            backgroundColor: colorConfig.bg,
                            color: colorConfig.text,
                          }}
                        >
                          <span
                            className="inline-block h-2 w-2 rounded-full border border-black/20"
                            style={{ backgroundColor: colorConfig.bg }}
                          />
                          {colorConfig.label}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
