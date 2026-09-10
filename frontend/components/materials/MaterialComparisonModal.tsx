"use client";

import { useEffect, useState } from "react";
import { compareMaterials } from "@/lib/api";
import { MaterialComparisonResponse } from "@/lib/types";

interface MaterialComparisonModalProps {
  selectedSlugs: string[];
  onClose: () => void;
  onRemoveSlug: (slug: string) => void;
}

export default function MaterialComparisonModal({
  selectedSlugs,
  onClose,
  onRemoveSlug,
}: MaterialComparisonModalProps) {
  const [data, setData] = useState<MaterialComparisonResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    if (selectedSlugs.length < 2) {
      setData(null);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    compareMaterials(selectedSlugs)
      .then((res) => {
        if (isMounted) {
          setData(res);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err.message || "Failed to load steel comparison data.");
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [selectedSlugs]);

  if (selectedSlugs.length < 2) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 sm:p-6 overflow-y-auto">
      <div className="relative w-full max-w-5xl rounded-2xl border border-neutral-800 bg-[#141414] p-6 shadow-2xl">
        {/* Modal Header */}
        <div className="flex items-center justify-between border-b border-neutral-800 pb-4 mb-6">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">⚔️</span>
              <h3 className="text-xl font-bold text-white">Side-by-Side Steel Comparison</h3>
            </div>
            <p className="text-xs text-neutral-400 mt-1">
              Comparing {selectedSlugs.length} alloys across carbon content, alloying elements, heat treatment, and edge vs. toughness trade-offs.
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="rounded-lg border border-neutral-700 bg-neutral-800/80 p-2 text-neutral-400 hover:border-neutral-600 hover:text-white transition-colors"
            title="Close modal"
          >
            ✕
          </button>
        </div>

        {/* Content Area */}
        {loading && (
          <div className="py-16 text-center">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-neutral-700 border-t-[#FF5722]" />
            <p className="mt-4 text-xs font-mono text-neutral-400">Loading metallurgy matrix...</p>
          </div>
        )}

        {error && (
          <div className="rounded-lg border border-rose-500/30 bg-rose-950/20 p-4 text-rose-300 text-sm">
            {error}
          </div>
        )}

        {!loading && data && (
          <div className="space-y-6">
            {/* Main Side-by-Side Table */}
            <div className="overflow-x-auto rounded-xl border border-neutral-800">
              <table className="w-full text-left text-xs">
                <thead className="bg-neutral-900/90 text-neutral-400 font-mono uppercase text-[10px]">
                  <tr>
                    <th className="px-4 py-3 min-w-[140px]">Property</th>
                    {data.items.map((item) => (
                      <th key={item.id} className="px-4 py-3 min-w-[180px]">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-bold text-white lowercase capitalize font-sans">
                            {item.title}
                          </span>
                          <button
                            type="button"
                            onClick={() => onRemoveSlug(item.slug)}
                            className="text-neutral-500 hover:text-rose-400 font-normal ml-2"
                            title="Remove from comparison"
                          >
                            ×
                          </button>
                        </div>
                        <span className="text-[10px] text-neutral-400 font-mono block normal-case">
                          {item.steel_category.replace(/_/g, " ")}
                        </span>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-800/80 font-mono">
                  {/* Carbon % */}
                  <tr className="bg-neutral-900/40">
                    <td className="px-4 py-3 font-semibold text-neutral-300">Carbon (C)</td>
                    {data.items.map((item) => (
                      <td key={item.id} className="px-4 py-3 font-bold text-[#FF8A65]">
                        {item.carbon_pct.toFixed(2)}% C
                      </td>
                    ))}
                  </tr>

                  {/* Classification */}
                  <tr>
                    <td className="px-4 py-3 text-neutral-400">Classification</td>
                    {data.items.map((item) => (
                      <td key={item.id} className="px-4 py-3 text-neutral-300 text-[11px]">
                        {item.classification}
                      </td>
                    ))}
                  </tr>

                  {/* Forging Temp */}
                  <tr>
                    <td className="px-4 py-3 text-neutral-400">Forging Range</td>
                    {data.items.map((item) => (
                      <td key={item.id} className="px-4 py-3 text-neutral-300">
                        {item.forging_temp_range_f || "—"}
                      </td>
                    ))}
                  </tr>

                  {/* Hardening Temp */}
                  <tr>
                    <td className="px-4 py-3 text-neutral-400">Hardening Temp</td>
                    {data.items.map((item) => (
                      <td key={item.id} className="px-4 py-3 text-neutral-300">
                        {item.hardening_temp_f ? `${item.hardening_temp_f}°F` : "—"}
                      </td>
                    ))}
                  </tr>

                  {/* Quench Medium */}
                  <tr>
                    <td className="px-4 py-3 text-neutral-400">Quench Medium</td>
                    {data.items.map((item) => (
                      <td key={item.id} className="px-4 py-3 text-neutral-300">
                        {item.quench_medium ? item.quench_medium.split("(")[0].trim() : "Oil Quench"}
                      </td>
                    ))}
                  </tr>

                  {/* Target Hardness */}
                  <tr>
                    <td className="px-4 py-3 text-neutral-400">Target Hardness</td>
                    {data.items.map((item) => (
                      <td key={item.id} className="px-4 py-3 text-[#FF5722] font-semibold">
                        {item.target_hardness_hrc || "—"}
                      </td>
                    ))}
                  </tr>

                  {/* Beginner Friendly */}
                  <tr>
                    <td className="px-4 py-3 text-neutral-400">Beginner Friendly</td>
                    {data.items.map((item) => (
                      <td key={item.id} className="px-4 py-3">
                        {item.beginner_suitability ? (
                          <span className="text-emerald-400 font-bold">✓ Yes</span>
                        ) : (
                          <span className="text-amber-400 font-bold">⚠ Advanced</span>
                        )}
                      </td>
                    ))}
                  </tr>

                  {/* Alloying Elements Rows */}
                  {data.compared_elements
                    .filter((el) => el !== "carbon")
                    .map((element) => (
                      <tr key={element}>
                        <td className="px-4 py-2.5 text-neutral-400 capitalize">{element}</td>
                        {data.items.map((item) => {
                          const val = item.alloying_elements[element];
                          return (
                            <td key={item.id} className="px-4 py-2.5 text-neutral-300">
                              {val !== undefined ? `${val}%` : "—"}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>

            {/* Metallurgical Trade-Off Rankings */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Edge Retention Ranking */}
              <div className="rounded-xl border border-neutral-800 bg-neutral-900/60 p-4">
                <h4 className="text-xs font-mono uppercase font-bold text-neutral-300 mb-2 flex items-center gap-2">
                  <span>🔪</span> Edge Retention Ranking (Carbon &amp; Carbide Density)
                </h4>
                <div className="space-y-1.5 font-mono text-xs">
                  {data.edge_retention_rank.map((steel, idx) => (
                    <div
                      key={steel}
                      className="flex items-center justify-between rounded bg-neutral-800/60 px-3 py-1.5"
                    >
                      <span className="text-neutral-300">{steel}</span>
                      <span className="text-[#FF8A65] font-bold">#{idx + 1}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Toughness Ranking */}
              <div className="rounded-xl border border-neutral-800 bg-neutral-900/60 p-4">
                <h4 className="text-xs font-mono uppercase font-bold text-neutral-300 mb-2 flex items-center gap-2">
                  <span>🛡</span> Impact Toughness Ranking (Shock Resistance)
                </h4>
                <div className="space-y-1.5 font-mono text-xs">
                  {data.toughness_rank.map((steel, idx) => (
                    <div
                      key={steel}
                      className="flex items-center justify-between rounded bg-neutral-800/60 px-3 py-1.5"
                    >
                      <span className="text-neutral-300">{steel}</span>
                      <span className="text-sky-400 font-bold">#{idx + 1}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Modal Footer */}
        <div className="mt-6 flex items-center justify-end border-t border-neutral-800 pt-4">
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg bg-neutral-800 px-4 py-2 text-xs font-mono font-semibold text-white hover:bg-neutral-700 transition-colors"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
