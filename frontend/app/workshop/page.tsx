"use client";

import { useEffect, useState, useMemo } from "react";
import Link from "next/link";
import { fetchTools } from "@/lib/api";
import { ToolItem } from "@/lib/types";
import ToolCard from "@/components/tools/ToolCard";

const CATEGORY_TABS = [
  { id: "all", label: "All Workshop Tools", icon: "🛠️" },
  { id: "forging", label: "Forging & Anvils", icon: "⚒️" },
  { id: "heating", label: "Heating & Forges", icon: "🔥" },
  { id: "grinding", label: "Grinding & Abrasives", icon: "⚡" },
  { id: "infrastructure", label: "Infrastructure", icon: "🏛️" },
  { id: "finishing", label: "Finishing", icon: "✨" },
];

export default function WorkshopPage() {
  const [tools, setTools] = useState<ToolItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters state
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [beginnerOnly, setBeginnerOnly] = useState<boolean>(false);
  const [diyOnly, setDiyOnly] = useState<boolean>(false);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setError(null);

    fetchTools({ limit: 100 })
      .then((res) => {
        if (isMounted) {
          setTools(res.tools || []);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err.message || "Failed to load workshop equipment catalog.");
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const filteredTools = useMemo(() => {
    return tools.filter((tool) => {
      const meta = tool.metadata;
      const q = searchQuery.toLowerCase().trim();

      // Category filter
      if (selectedCategory !== "all") {
        if (meta.tool_category !== selectedCategory) return false;
      }

      // Beginner filter
      if (beginnerOnly && !meta.beginner_friendly) {
        return false;
      }

      // DIY filter
      if (diyOnly && !meta.diy_buildable) {
        return false;
      }

      // Search query
      if (q) {
        const title = (tool.title || "").toLowerCase();
        const summary = (tool.summary || "").toLowerCase();
        const purpose = (meta.primary_purpose || "").toLowerCase();
        const guidance = (meta.beginner_guidance || "").toLowerCase();
        const essential = (meta.essential_for || []).join(" ").toLowerCase();
        const tags = (tool.tags || []).join(" ").toLowerCase();

        if (
          !title.includes(q) &&
          !summary.includes(q) &&
          !purpose.includes(q) &&
          !guidance.includes(q) &&
          !essential.includes(q) &&
          !tags.includes(q)
        ) {
          return false;
        }
      }

      return true;
    });
  }, [tools, selectedCategory, beginnerOnly, diyOnly, searchQuery]);

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Header Banner */}
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3 border border-[#FF5722]/20 font-mono">
              Workshop &amp; Equipment Knowledge
            </span>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Workshop Tools &amp; Infrastructure
            </h1>
            <p className="text-neutral-400 mt-2 max-w-2xl text-sm sm:text-base leading-relaxed">
              Essential knowledge on selecting, maintaining, and operating anvils, hammers, forges, grinders, and post vises for personal craft and bladesmithing.
            </p>
          </div>

          <Link
            href="/tools"
            className="rounded-lg border border-neutral-700 bg-neutral-800/80 px-4 py-2 text-xs font-mono font-semibold text-neutral-300 hover:border-neutral-600 hover:text-white transition-colors"
          >
            Commercial Vendor Catalog &rarr;
          </Link>
        </div>
      </div>

      {/* Workshop Golden Triangle Guide Box */}
      <div className="mb-8 rounded-xl border border-neutral-800 bg-[#161616] p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-start gap-3.5">
          <span className="text-2xl mt-0.5">📐</span>
          <div>
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <span>The Smith's Golden Triangle Layout</span>
              <span className="text-[10px] font-mono uppercase text-[#FF5722] bg-[#FF5722]/10 px-2 py-0.5 rounded">
                Ergonomics
              </span>
            </h2>
            <p className="text-xs text-neutral-300 mt-1 leading-relaxed max-w-3xl">
              Arrange your <strong className="text-[#FF8A65]">Forge</strong>, <strong className="text-[#FF8A65]">Anvil</strong>, and <strong className="text-[#FF8A65]">Post Vise</strong> within one or two comfortable pivot steps of each other. Position your quench tank directly adjacent to the anvil to catch critical quench windows in under 1 second without tripping over cords.
            </p>
          </div>
        </div>
      </div>

      {/* Search & Filter Toolbar */}
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
              placeholder="Search tools (e.g. anvil, cross-peen, grinder, propane, vise)..."
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

          {/* Quick Checkbox Filters */}
          <div className="flex items-center gap-2">
            <label className="flex items-center gap-2 px-3 py-2 rounded-lg border border-neutral-700 bg-neutral-900/60 cursor-pointer select-none hover:border-neutral-600 transition-colors">
              <input
                type="checkbox"
                checked={beginnerOnly}
                onChange={(e) => setBeginnerOnly(e.target.checked)}
                className="h-4 w-4 rounded-sm border-neutral-700 bg-neutral-800 text-[#FF5722] focus:ring-[#FF5722]"
              />
              <span className="text-xs font-mono text-neutral-300">
                Beginner Friendly
              </span>
            </label>

            <label className="flex items-center gap-2 px-3 py-2 rounded-lg border border-neutral-700 bg-neutral-900/60 cursor-pointer select-none hover:border-neutral-600 transition-colors">
              <input
                type="checkbox"
                checked={diyOnly}
                onChange={(e) => setDiyOnly(e.target.checked)}
                className="h-4 w-4 rounded-sm border-neutral-700 bg-neutral-800 text-[#FF5722] focus:ring-[#FF5722]"
              />
              <span className="text-xs font-mono text-neutral-300">
                DIY Buildable
              </span>
            </label>
          </div>
        </div>

        {/* Category Tabs */}
        <div className="flex flex-wrap items-center gap-1.5 border-t border-neutral-800/80 pt-3 text-xs font-mono">
          <span className="text-neutral-500 text-[11px] uppercase mr-1">Category:</span>
          {CATEGORY_TABS.map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setSelectedCategory(tab.id)}
              className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 transition-colors ${
                selectedCategory === tab.id
                  ? "bg-[#FF5722] text-black font-bold"
                  : "bg-neutral-800 text-neutral-400 hover:bg-neutral-700 hover:text-white"
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Tools Grid */}
      {loading ? (
        <div className="py-20 text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-neutral-700 border-t-[#FF5722]" />
          <p className="mt-4 text-xs font-mono text-neutral-400">Loading workshop inventory...</p>
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
      ) : filteredTools.length === 0 ? (
        <div className="rounded-xl border border-neutral-800 bg-[#161616] p-12 text-center">
          <span className="text-3xl">🔍</span>
          <h3 className="mt-2 text-base font-bold text-white">No Workshop Tools Found</h3>
          <p className="mt-1 text-xs text-neutral-400">
            No tools match the selected filters or search terms.
          </p>
          <button
            type="button"
            onClick={() => {
              setSelectedCategory("all");
              setSearchQuery("");
              setBeginnerOnly(false);
              setDiyOnly(false);
            }}
            className="mt-4 rounded-lg bg-neutral-800 px-4 py-2 text-xs font-mono text-white hover:bg-neutral-700 transition-colors"
          >
            Reset All Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTools.map((tool) => (
            <ToolCard key={tool.id} tool={tool} />
          ))}
        </div>
      )}
    </div>
  );
}
