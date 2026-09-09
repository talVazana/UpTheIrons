"use client";

import { useEffect, useState, useTransition } from "react";
import Link from "next/link";
import { fetchArticles, syncAllRSSFeeds, ArticleItem, RSSSyncSummaryItem } from "@/lib/api";

const CATEGORIES = [
  { id: "all", label: "All Knowledge" },
  { id: "materials", label: "Materials & Steel" },
  { id: "heat-treatment", label: "Heat Treatment" },
  { id: "tools", label: "Tools & Anvils" },
  { id: "bladesmithing", label: "Bladesmithing" },
  { id: "guides", label: "Craft Guides" },
];

export default function GuidesPage() {
  const [articles, setArticles] = useState<ArticleItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState("all");

  const [isSyncing, startSync] = useTransition();
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);
  const [activeArticle, setActiveArticle] = useState<ArticleItem | null>(null);

  const loadArticles = async (cat = selectedCategory) => {
    setLoading(true);
    setError(null);
    try {
      const categoryParam = cat === "all" ? undefined : cat;
      const res = await fetchArticles({ category: categoryParam });
      setArticles(res.articles);
    } catch (err: any) {
      setError(err?.message || "Failed loading articles from knowledge vault.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadArticles(selectedCategory);
  }, [selectedCategory]);

  const handleSyncAll = () => {
    startSync(async () => {
      setSyncFeedback("Syncing approved RSS feeds...");
      try {
        const summaries: RSSSyncSummaryItem[] = await syncAllRSSFeeds();
        const totalNew = summaries.reduce((acc, s) => acc + s.new_items, 0);
        const totalDupes = summaries.reduce((acc, s) => acc + s.duplicates, 0);
        setSyncFeedback(
          `Feeds synced! Added ${totalNew} new article(s), ${totalDupes} duplicate(s) skipped.`
        );
        await loadArticles(selectedCategory);
      } catch (err: any) {
        setSyncFeedback(`Sync failed: ${err.message}`);
      }
    });
  };

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-neutral-800 pb-8 mb-8">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full">
              The Knight&apos;s Library
            </span>
            <span className="text-xs text-neutral-400 bg-neutral-900 border border-neutral-800 px-2.5 py-0.5 rounded">
              Controlled RSS Pipeline
            </span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Practical Knowledge &amp; Articles
          </h1>
          <p className="text-neutral-400 mt-2 max-w-2xl text-sm sm:text-base">
            Curated articles from approved guild publications and maker feeds. Clean technical reference with strict source attribution.
          </p>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-3">
          <Link
            href="/sources"
            className="rounded-lg border border-neutral-700 bg-neutral-800/80 px-3.5 py-2 text-xs font-semibold text-neutral-200 hover:bg-neutral-700 hover:text-white transition-colors"
          >
            Manage Feed Sources &rarr;
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
                Syncing Feeds...
              </>
            ) : (
              <>
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Sync Feeds Now
              </>
            )}
          </button>
        </div>
      </div>

      {/* Sync Feedback */}
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

      {/* Categories */}
      <div className="flex items-center gap-2 overflow-x-auto pb-4 mb-6 border-b border-neutral-900 scrollbar-none">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            type="button"
            onClick={() => setSelectedCategory(cat.id)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
              selectedCategory === cat.id
                ? "bg-[#FF5722] text-white shadow"
                : "bg-neutral-900 text-neutral-400 hover:text-white hover:bg-neutral-800"
            }`}
          >
            {cat.label}
          </button>
        ))}
        <span className="ml-auto text-xs text-neutral-500 hidden sm:inline">
          {articles.length} article{articles.length === 1 ? "" : "s"} in vault
        </span>
      </div>

      {/* Content */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="animate-pulse rounded-xl border border-neutral-800 bg-[#171717] h-64" />
          ))}
        </div>
      ) : error ? (
        <div className="rounded-xl border border-red-900/40 bg-red-950/20 p-8 text-center text-red-300">
          <p className="font-semibold text-base mb-2">Error Loading Knowledge Vault</p>
          <p className="text-xs text-neutral-400 mb-4">{error}</p>
          <button
            type="button"
            onClick={() => loadArticles(selectedCategory)}
            className="rounded bg-neutral-800 px-4 py-2 text-xs text-white hover:bg-neutral-700"
          >
            Retry
          </button>
        </div>
      ) : articles.length === 0 ? (
        <div className="rounded-2xl border border-neutral-800 bg-[#161616] p-12 text-center max-w-xl mx-auto my-8">
          <div className="w-12 h-12 rounded-full bg-[#FF5722]/10 text-[#FF5722] flex items-center justify-center mx-auto mb-4 font-bold text-xl">
            &#128214;
          </div>
          <h2 className="text-lg font-bold text-white mb-2">Knowledge Vault Awaiting Articles</h2>
          <p className="text-xs text-neutral-400 mb-6 leading-relaxed">
            No articles ingested yet. Register approved RSS feeds in the Source Registry and trigger synchronization to harvest verified metallurgy, heat treatment, and workshop guides.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <button
              type="button"
              onClick={handleSyncAll}
              disabled={isSyncing}
              className="rounded-lg bg-[#FF5722] px-4 py-2 text-xs font-semibold text-white shadow hover:bg-[#F4511E]"
            >
              Sync All Feeds Now
            </button>
            <Link
              href="/sources"
              className="rounded-lg border border-neutral-700 bg-neutral-800 px-4 py-2 text-xs font-medium text-neutral-300 hover:text-white"
            >
              Configure RSS Sources
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((art) => {
            const externalUrl = art.source?.source_url || art.metadata?.article_url;
            const author = art.metadata?.author || art.source?.source_name || "Guild Author";

            return (
              <div
                key={art.id}
                className="group flex flex-col rounded-xl border border-neutral-800 bg-[#181818] p-5 hover:border-[#FF5722]/40 transition-all shadow-sm hover:shadow-md"
              >
                {/* Meta header */}
                <div className="flex items-center justify-between gap-2 text-xs text-neutral-400 mb-3">
                  <span className="font-semibold text-[#FF8A65] truncate max-w-[60%]">
                    {art.source?.source_name || "RSS Source"}
                  </span>
                  <span className="capitalize text-[11px] bg-neutral-850 px-2 py-0.5 rounded text-neutral-300">
                    {art.category}
                  </span>
                </div>

                {/* Title */}
                <h3 className="text-base font-bold text-white line-clamp-2 mb-2 group-hover:text-[#FF8A65] transition-colors">
                  {art.title}
                </h3>

                {/* Summary */}
                <p className="text-xs text-neutral-400 line-clamp-3 mb-4 leading-relaxed flex-1">
                  {art.summary}
                </p>

                {/* Attribution & Link Footer */}
                <div className="pt-3 border-t border-neutral-850 flex items-center justify-between text-xs">
                  <div className="text-[11px] text-neutral-500 truncate max-w-[60%]">
                    By <span className="text-neutral-400">{author}</span>
                  </div>

                  {externalUrl && (
                    <a
                      href={externalUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 font-semibold text-[#FF5722] hover:text-[#F4511E] transition-colors"
                    >
                      Read Full &rarr;
                    </a>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
