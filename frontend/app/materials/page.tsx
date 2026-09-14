"use client";

import { useEffect, useState, useMemo } from "react";
import Link from "next/link";
import { fetchMaterials } from "@/lib/api";
import { MaterialItem } from "@/lib/types";
import MaterialCard from "@/components/materials/MaterialCard";
import MaterialComparisonModal from "@/components/materials/MaterialComparisonModal";

export default function MaterialsPage() {
  const [materials, setMaterials] = useState<MaterialItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters state
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [beginnerOnly, setBeginnerOnly] = useState(false);
  const [carbonRange, setCarbonRange] = useState<string>("all");

  // Comparison selection state (array of slugs)
  const [selectedForCompare, setSelectedForCompare] = useState<string[]>([]);
  const [isCompareModalOpen, setIsCompareModalOpen] = useState(false);

  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setError(null);

    const token = localStorage.getItem("admin_token");
    if (token) {
      setIsAdmin(true);
    }

    fetchMaterials({ limit: 100 })
      .then((res) => {
        if (isMounted) {
          setMaterials(res.materials || []);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err.message || "Failed to load metallurgy vault materials.");
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  // Filtered materials
  const filteredMaterials = useMemo(() => {
    return materials.filter((item) => {
      const meta = item.metadata;
      const q = searchQuery.toLowerCase().trim();

      // Category filter
      if (selectedCategory !== "all") {
        if (meta.steel_category !== selectedCategory) return false;
      }

      // Beginner friendly filter
      if (beginnerOnly) {
        if (!meta.beginner_suitability) return false;
      }

      // Carbon range filter
      if (carbonRange !== "all") {
        const c = meta.carbon_pct ?? 0;
        if (carbonRange === "medium" && c >= 0.7) return false;
        if (carbonRange === "high" && (c < 0.7 || c > 1.0)) return false;
        if (carbonRange === "ultra" && c <= 1.0) return false;
      }

      // Search query
      if (q) {
        const title = (item.title || "").toLowerCase();
        const classification = (meta.classification || "").toLowerCase();
        const summary = (item.summary || "").toLowerCase();
        const apps = (meta.common_applications || []).join(" ").toLowerCase();
        const tags = (item.tags || []).join(" ").toLowerCase();

        if (
          !title.includes(q) &&
          !classification.includes(q) &&
          !summary.includes(q) &&
          !apps.includes(q) &&
          !tags.includes(q)
        ) {
          return false;
        }
      }

      return true;
    });
  }, [materials, searchQuery, selectedCategory, beginnerOnly, carbonRange]);

  const handleToggleCompare = (slug: string) => {
    setSelectedForCompare((prev) => {
      if (prev.includes(slug)) {
        return prev.filter((s) => s !== slug);
      }
      if (prev.length >= 4) {
        return prev;
      }
      return [...prev, slug];
    });
  };

  const handleRemoveCompare = (slug: string) => {
    setSelectedForCompare((prev) => prev.filter((s) => s !== slug));
  };

  const handleDeleteMaterial = async (slug: string) => {
    if (!confirm("Are you sure you want to delete this material?")) return;
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000"}/api/v1/materials/${slug}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${localStorage.getItem("admin_token")}` }
      });
      if (res.ok) {
        setMaterials(prev => prev.filter(m => m.slug !== slug));
        setSelectedForCompare(prev => prev.filter(s => s !== slug));
      } else {
        alert("Failed to delete material.");
      }
    } catch (err) {
      alert("Network error while deleting material.");
    }
  };

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Header Banner */}
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3 border border-[#FF5722]/20 font-mono">
              Metallurgy Vault
            </span>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Materials &amp; Steel Database
            </h1>
            <p className="text-neutral-400 mt-2 max-w-2xl text-sm sm:text-base leading-relaxed">
              Source-backed chemical compositions, phase transformation ranges, quench parameters, and tempering calibration curves.
            </p>
          </div>

          {/* Quick Stats or Actions */}
          <div className="flex items-center gap-3">
            {isAdmin && (
              <Link
                href="/admin/materials/new"
                className="flex items-center gap-2 rounded-xl px-4 py-2.5 text-xs font-mono font-bold transition-all shadow-lg border border-[var(--accent-forge)] text-[var(--accent-forge)] hover:bg-[var(--accent-forge)] hover:text-white shadow-[#FF5722]/20"
              >
                <span>➕</span>
                <span>Add Material</span>
              </Link>
            )}
            {selectedForCompare.length > 0 && (
              <button
                type="button"
                onClick={() => setIsCompareModalOpen(true)}
                disabled={selectedForCompare.length < 2}
                className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-xs font-mono font-bold transition-all shadow-lg ${
                  selectedForCompare.length >= 2
                    ? "bg-[#FF5722] text-black hover:bg-[#FF7043] cursor-pointer shadow-[#FF5722]/20"
                    : "bg-neutral-800 text-neutral-400 cursor-not-allowed border border-neutral-700"
                }`}
              >
                <span>⚔️</span>
                <span>
                  Compare ({selectedForCompare.length}
                  {selectedForCompare.length < 2 ? " - select min 2" : " steels"})
                </span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Beginner Recommendation Banner */}
      <div className="mb-8 rounded-xl border border-emerald-500/20 bg-emerald-950/20 p-4 sm:p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-start gap-3.5">
          <span className="text-2xl mt-0.5">💡</span>
          <div>
            <h2 className="text-sm font-bold text-emerald-300">
              New to Bladesmithing or Tool Forging?
            </h2>
            <p className="text-xs text-neutral-300 mt-1 leading-relaxed">
              We recommend starting with <strong className="text-white">1084 High Carbon</strong>. Its eutectoid carbon ratio (~0.84% C) eliminates excess grain-boundary cementite and hardens reliably in warmed canola oil without requiring precision kiln soaking.
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={() => {
            setSearchQuery("1084");
            setSelectedCategory("all");
            setBeginnerOnly(true);
          }}
          className="shrink-0 rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-3 py-1.5 text-xs font-mono text-emerald-400 hover:bg-emerald-500/20 transition-colors"
        >
          View 1084 Spec →
        </button>
      </div>

      {/* Search & Filter Controls */}
      <div className="mb-8 space-y-4 rounded-xl border border-neutral-800 bg-[#161616] p-4 sm:p-5">
        <div className="flex flex-col md:flex-row items-stretch md:items-center gap-3">
          {/* Search Input */}
          <div className="relative flex-1">
            <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-neutral-500 text-sm">
              🔍
            </span>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search steel by name (e.g. 1084, 5160, O1), application, or standard..."
              className="w-full rounded-lg border border-neutral-700 bg-neutral-900/90 py-2.5 pl-10 pr-4 text-sm text-white placeholder-neutral-500 focus:border-[#FF5722] focus:outline-hidden focus:ring-1 focus:ring-[#FF5722]"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500 hover:text-white text-xs font-mono"
              >
                Clear
              </button>
            )}
          </div>

          {/* Beginner Suitable Checkbox */}
          <label className="flex items-center gap-2 px-3 py-2 rounded-lg border border-neutral-700 bg-neutral-900/60 cursor-pointer select-none hover:border-neutral-600 transition-colors">
            <input
              type="checkbox"
              checked={beginnerOnly}
              onChange={(e) => setBeginnerOnly(e.target.checked)}
              className="h-4 w-4 rounded-sm border-neutral-700 bg-neutral-800 text-[#FF5722] focus:ring-[#FF5722]"
            />
            <span className="text-xs font-mono text-neutral-300">
              Beginner Friendly Only
            </span>
          </label>
        </div>

        {/* Category & Carbon Filter Pills */}
        <div className="flex flex-wrap items-center justify-between gap-3 border-t border-neutral-800/80 pt-3">
          {/* Category Tabs */}
          <div className="flex flex-wrap items-center gap-1.5 text-xs font-mono">
            <span className="text-neutral-500 text-[11px] uppercase mr-1">Category:</span>
            {[
              { id: "all", label: "All Steels" },
              { id: "carbon_steel", label: "Carbon Steel" },
              { id: "tool_steel", label: "Tool Steel" },
              { id: "spring_steel", label: "Spring Steel" },
            ].map((cat) => (
              <button
                key={cat.id}
                type="button"
                onClick={() => setSelectedCategory(cat.id)}
                className={`rounded-md px-2.5 py-1 transition-colors ${
                  selectedCategory === cat.id
                    ? "bg-[#FF5722] text-black font-bold"
                    : "bg-neutral-800 text-neutral-400 hover:bg-neutral-700 hover:text-white"
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>

          {/* Carbon Presets */}
          <div className="flex flex-wrap items-center gap-1.5 text-xs font-mono">
            <span className="text-neutral-500 text-[11px] uppercase mr-1">Carbon %:</span>
            {[
              { id: "all", label: "All" },
              { id: "medium", label: "< 0.70%" },
              { id: "high", label: "0.70% – 1.00%" },
              { id: "ultra", label: "> 1.00%" },
            ].map((cr) => (
              <button
                key={cr.id}
                type="button"
                onClick={() => setCarbonRange(cr.id)}
                className={`rounded-md px-2.5 py-1 transition-colors ${
                  carbonRange === cr.id
                    ? "border border-[#FF5722] bg-[#FF5722]/10 text-[#FF8A65] font-bold"
                    : "bg-neutral-800/60 text-neutral-400 hover:bg-neutral-800 hover:text-white"
                }`}
              >
                {cr.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Floating Comparison Bar when items are selected */}
      {selectedForCompare.length > 0 && (
        <div className="sticky top-4 z-40 mb-6 flex items-center justify-between rounded-xl border border-[#FF5722]/50 bg-neutral-900/95 p-3.5 shadow-2xl backdrop-blur-md">
          <div className="flex items-center gap-2 overflow-x-auto">
            <span className="text-xs font-mono text-neutral-400">Selected for compare:</span>
            {selectedForCompare.map((slug) => (
              <span
                key={slug}
                className="inline-flex items-center gap-1.5 rounded-md border border-[#FF5722]/30 bg-[#FF5722]/10 px-2.5 py-1 text-xs font-mono text-[#FF8A65]"
              >
                <span className="font-bold uppercase">{slug}</span>
                <button
                  type="button"
                  onClick={() => handleRemoveCompare(slug)}
                  className="text-neutral-400 hover:text-white"
                >
                  ×
                </button>
              </span>
            ))}
            {selectedForCompare.length < 4 && (
              <span className="text-[11px] font-mono text-neutral-500">
                (select up to {4 - selectedForCompare.length} more)
              </span>
            )}
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setSelectedForCompare([])}
              className="text-xs font-mono text-neutral-500 hover:text-neutral-300 px-2 py-1"
            >
              Clear
            </button>
            <button
              type="button"
              onClick={() => setIsCompareModalOpen(true)}
              disabled={selectedForCompare.length < 2}
              className={`rounded-lg px-3.5 py-1.5 text-xs font-mono font-bold transition-colors ${
                selectedForCompare.length >= 2
                  ? "bg-[#FF5722] text-black hover:bg-[#FF7043]"
                  : "bg-neutral-800 text-neutral-500 cursor-not-allowed"
              }`}
            >
              Compare Now
            </button>
          </div>
        </div>
      )}

      {/* Materials Grid */}
      {loading ? (
        <div className="py-20 text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-neutral-700 border-t-[#FF5722]" />
          <p className="mt-4 text-xs font-mono text-neutral-400">Consulting metallurgy archives...</p>
        </div>
      ) : error ? (
        <div className="rounded-xl border border-rose-500/30 bg-rose-950/20 p-6 text-center text-rose-300">
          <p className="text-sm font-semibold">{error}</p>
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="mt-4 rounded-lg bg-neutral-800 px-4 py-2 text-xs font-mono text-white hover:bg-neutral-700"
          >
            Retry Connection
          </button>
        </div>
      ) : filteredMaterials.length === 0 ? (
        <div className="rounded-xl border border-neutral-800 bg-[#161616] p-12 text-center">
          <span className="text-3xl">🔍</span>
          <h3 className="mt-2 text-base font-bold text-white">No Matching Steels Found</h3>
          <p className="mt-1 text-xs text-neutral-400">
            No metallurgical alloy matches your current filter combination.
          </p>
          <button
            type="button"
            onClick={() => {
              setSearchQuery("");
              setSelectedCategory("all");
              setBeginnerOnly(false);
              setCarbonRange("all");
            }}
            className="mt-4 rounded-lg bg-neutral-800 px-4 py-2 text-xs font-mono text-white hover:bg-neutral-700 transition-colors"
          >
            Reset All Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredMaterials.map((mat) => (
            <MaterialCard
              key={mat.id}
              material={mat}
              isSelectedForCompare={selectedForCompare.includes(mat.slug)}
              onToggleCompare={handleToggleCompare}
              canSelectMore={selectedForCompare.length < 4}
              isAdmin={isAdmin}
              onDelete={handleDeleteMaterial}
            />
          ))}
        </div>
      )}

      {/* Comparison Modal */}
      {isCompareModalOpen && (
        <MaterialComparisonModal
          selectedSlugs={selectedForCompare}
          onClose={() => setIsCompareModalOpen(false)}
          onRemoveSlug={handleRemoveCompare}
        />
      )}
    </div>
  );
}
