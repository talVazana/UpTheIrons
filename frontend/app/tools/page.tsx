"use client";

import { useEffect, useState, useTransition } from "react";
import Link from "next/link";
import { fetchProducts, syncAllProductSources, ProductItem, ProductSyncSummaryItem } from "@/lib/api";

const TAG_FILTERS = [
  { id: "all", label: "All Gear" },
  { id: "anvil", label: "Anvils" },
  { id: "forge", label: "Forges" },
  { id: "grinder", label: "Belt Grinders" },
  { id: "tongs", label: "Tongs" },
];

export default function ToolsPage() {
  const [products, setProducts] = useState<ProductItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedTag, setSelectedTag] = useState("all");
  const [beginnerOnly, setBeginnerOnly] = useState(false);
  const [maxPrice, setMaxPrice] = useState<number | undefined>(undefined);

  const [isSyncing, startSync] = useTransition();
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);

  const loadProducts = async () => {
    setLoading(true);
    setError(null);
    try {
      const tagParam = selectedTag === "all" ? undefined : selectedTag;
      const res = await fetchProducts({
        tag: tagParam,
        beginner_only: beginnerOnly || undefined,
        max_price: maxPrice,
      });
      setProducts(res.products);
    } catch (err: any) {
      setError(err?.message || "Failed loading tools from knowledge vault.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, [selectedTag, beginnerOnly, maxPrice]);

  const handleSyncAll = () => {
    startSync(async () => {
      setSyncFeedback("Syncing approved vendor catalogs...");
      try {
        const summaries: ProductSyncSummaryItem[] = await syncAllProductSources();
        const totalNew = summaries.reduce((acc, s) => acc + s.new_items, 0);
        const totalUpdates = summaries.reduce((acc, s) => acc + s.price_updates, 0);
        const totalDupes = summaries.reduce((acc, s) => acc + s.duplicates, 0);
        setSyncFeedback(
          `Catalogs synced! Added ${totalNew} item(s), updated ${totalUpdates} price(s), skipped ${totalDupes} unchanged.`
        );
        await loadProducts();
      } catch (err: any) {
        setSyncFeedback(`Sync failed: ${err.message}`);
      }
    });
  };

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-neutral-800 pb-8 mb-8">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full">
              Hardware &amp; Equipment
            </span>
            <span className="text-xs text-neutral-400 bg-neutral-900 border border-neutral-800 px-2.5 py-0.5 rounded">
              Amateur First &bull; Zero Sponsored Bias
            </span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Tools &amp; Equipment Guide
          </h1>
          <p className="text-neutral-400 mt-2 max-w-2xl text-sm sm:text-base">
            Transparent tool evaluations for makers. Every recommendation answers what it is, why you need it, honest pros/cons, and cheaper alternatives.
          </p>
        </div>

        {/* Sync / Actions */}
        <div className="flex items-center gap-3">
          <Link
            href="/sources"
            className="rounded-lg border border-neutral-700 bg-neutral-800/80 px-3.5 py-2 text-xs font-semibold text-neutral-200 hover:bg-neutral-700 hover:text-white transition-colors"
          >
            Manage Vendor Sources &rarr;
          </Link>

          <button
            type="button"
            onClick={handleSyncAll}
            disabled={isSyncing}
            className="rounded-lg bg-[#FF5722] hover:bg-[#F4511E] disabled:opacity-50 px-4 py-2 text-xs font-semibold text-white shadow transition-all flex items-center gap-2"
          >
            {isSyncing ? (
              <>
                <svg className="animate-spin h-3.5 w-3.5 text-white" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Syncing Catalogs...
              </>
            ) : (
              <>
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Sync Catalogs
              </>
            )}
          </button>
        </div>
      </div>

      {/* Sync Feedback Toast */}
      {syncFeedback && (
        <div className="mb-6 rounded-lg border border-[#FF5722]/30 bg-[#FF5722]/10 p-3 text-xs text-[#FF8A65] flex items-center justify-between">
          <span>{syncFeedback}</span>
          <button
            type="button"
            onClick={() => setSyncFeedback(null)}
            className="text-neutral-400 hover:text-white ml-4"
          >
            &times;
          </button>
        </div>
      )}

      {/* Filter Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 mb-6 border-b border-neutral-900">
        {/* Tag pills */}
        <div className="flex items-center gap-2 overflow-x-auto scrollbar-none">
          {TAG_FILTERS.map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setSelectedTag(tab.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
                selectedTag === tab.id
                  ? "bg-[#FF5722] text-white shadow"
                  : "bg-neutral-900 text-neutral-400 hover:text-white hover:bg-neutral-800"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Secondary filters */}
        <div className="flex items-center gap-4 text-xs">
          <label className="flex items-center gap-2 cursor-pointer text-neutral-300 select-none">
            <input
              type="checkbox"
              checked={beginnerOnly}
              onChange={(e) => setBeginnerOnly(e.target.checked)}
              className="rounded border-neutral-700 bg-neutral-900 text-[#FF5722] focus:ring-0"
            />
            Beginner Friendly
          </label>

          <select
            value={maxPrice ?? ""}
            onChange={(e) => setMaxPrice(e.target.value ? Number(e.target.value) : undefined)}
            className="rounded border border-neutral-800 bg-neutral-900 px-2.5 py-1 text-xs text-neutral-300 focus:outline-none focus:border-[#FF5722]"
          >
            <option value="">Any Budget</option>
            <option value="100">Under $100</option>
            <option value="400">Under $400</option>
            <option value="1000">Under $1,000</option>
          </select>
        </div>
      </div>

      {/* Product Cards Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="animate-pulse rounded-xl border border-neutral-800 bg-[#171717] h-80" />
          ))}
        </div>
      ) : error ? (
        <div className="rounded-xl border border-red-900/40 bg-red-950/20 p-8 text-center text-red-300">
          <p className="font-semibold text-base mb-2">Error Loading Gear Catalog</p>
          <p className="text-xs text-neutral-400 mb-4">{error}</p>
          <button
            type="button"
            onClick={loadProducts}
            className="rounded bg-neutral-800 px-4 py-2 text-xs text-white hover:bg-neutral-700"
          >
            Retry
          </button>
        </div>
      ) : products.length === 0 ? (
        <div className="rounded-2xl border border-neutral-800 bg-[#161616] p-12 text-center max-w-xl mx-auto my-8">
          <div className="w-12 h-12 rounded-full bg-[#FF5722]/10 text-[#FF5722] flex items-center justify-center mx-auto mb-4 font-bold text-xl">
            &#9874;
          </div>
          <h2 className="text-lg font-bold text-white mb-2">No Tools Found Matching Filter</h2>
          <p className="text-xs text-neutral-400 mb-6 leading-relaxed">
            Synchronize approved vendor catalogs or configure new sources to evaluate anvils, forges, grinders, and tongs.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <button
              type="button"
              onClick={handleSyncAll}
              disabled={isSyncing}
              className="rounded-lg bg-[#FF5722] px-4 py-2 text-xs font-semibold text-white shadow hover:bg-[#F4511E]"
            >
              Sync Vendor Catalogs Now
            </button>
            <Link
              href="/sources"
              className="rounded-lg border border-neutral-700 bg-neutral-800 px-4 py-2 text-xs font-medium text-neutral-300 hover:text-white"
            >
              Configure Vendor Sources
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((prod) => {
            const meta = prod.metadata;
            const priceFormatted = new Intl.NumberFormat("en-US", {
              style: "currency",
              currency: meta?.currency || "USD",
            }).format(meta?.price || 0);

            return (
              <div
                key={prod.id}
                className="group flex flex-col rounded-xl border border-neutral-800 bg-[#181818] overflow-hidden hover:border-[#FF5722]/40 transition-all shadow-sm hover:shadow-md"
              >
                {/* Header bar: Platform & Price */}
                <div className="flex items-center justify-between p-4 border-b border-neutral-850 bg-neutral-900/50">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-neutral-300">
                      {meta?.platform || "Forge Vendor"}
                    </span>
                    {meta?.beginner_suitable && (
                      <span className="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">
                        Beginner Suitable
                      </span>
                    )}
                  </div>
                  <span className="text-sm font-mono font-extrabold text-[#FF8A65]">
                    {priceFormatted}
                  </span>
                </div>

                {/* Body Content */}
                <div className="p-5 flex flex-col flex-1">
                  <h3 className="text-base font-bold text-white mb-2 group-hover:text-[#FF8A65] transition-colors line-clamp-2">
                    {prod.title}
                  </h3>

                  <p className="text-xs text-neutral-400 line-clamp-3 mb-4 leading-relaxed">
                    {prod.summary}
                  </p>

                  {/* Pros & Cons Checklist */}
                  <div className="space-y-2 mb-4 bg-neutral-900/60 p-3 rounded-lg border border-neutral-850 text-xs">
                    {meta?.pros && meta.pros.length > 0 && (
                      <div>
                        <span className="font-semibold text-emerald-400 text-[11px] block mb-1">
                          &bull; Strengths:
                        </span>
                        <ul className="list-disc list-inside space-y-0.5 text-neutral-300 text-[11px]">
                          {meta.pros.slice(0, 2).map((pro, idx) => (
                            <li key={idx} className="truncate">{pro}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {meta?.cons && meta.cons.length > 0 && (
                      <div className="pt-2 border-t border-neutral-800">
                        <span className="font-semibold text-amber-400 text-[11px] block mb-1">
                          &bull; Limitations:
                        </span>
                        <ul className="list-disc list-inside space-y-0.5 text-neutral-400 text-[11px]">
                          {meta.cons.slice(0, 2).map((con, idx) => (
                            <li key={idx} className="truncate">{con}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>

                  {/* Alternatives if available */}
                  {meta?.alternatives && meta.alternatives.length > 0 && (
                    <div className="text-[11px] text-neutral-500 mb-4">
                      <span className="text-neutral-400 font-medium">Alternatives: </span>
                      {meta.alternatives.slice(0, 2).join(", ")}
                    </div>
                  )}

                  {/* Footer Action & Disclosure */}
                  <div className="mt-auto pt-3 border-t border-neutral-850 flex items-center justify-between text-xs">
                    <span className="text-[10px] text-neutral-500">
                      {meta?.affiliate ? "Affiliate Partner Link" : "Independent Vendor Link"}
                    </span>

                    <a
                      href={meta?.purchase_url || "#"}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 font-semibold text-[#FF5722] hover:text-[#F4511E] transition-colors"
                    >
                      View Tool &rarr;
                    </a>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
