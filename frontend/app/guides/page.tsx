"use client";

import { useEffect, useState, useTransition } from "react";
import Link from "next/link";
import {
  fetchGuides,
  fetchArticles,
  syncAllRSSFeeds,
  enrichPendingContent,
  GuideItem,
  ArticleItem,
  RSSSyncSummaryItem,
} from "@/lib/api";
import TrustBadge from "@/components/guides/TrustBadge";

const CATEGORIES = [
  { id: "all", label: "All Knowledge" },
  { id: "tools", label: "Tools & Anvils" },
  { id: "heat-treatment", label: "Heat Treatment" },
  { id: "materials", label: "Materials & Steel" },
  { id: "bladesmithing", label: "Bladesmithing" },
  { id: "guides", label: "Craft Guides" },
];

const DIFFICULTIES = [
  { id: "all", label: "All Levels" },
  { id: "beginner", label: "Beginner" },
  { id: "intermediate", label: "Intermediate" },
  { id: "advanced", label: "Advanced" },
];

const TRUST_FILTERS = [
  { id: "all", label: "All Trust" },
  { id: "fact", label: "Physical Fact" },
  { id: "source_backed_recommendation", label: "Source-Backed" },
  { id: "craft_practice", label: "Craft Practice" },
  { id: "personal_experience", label: "Workshop Experience" },
];

export default function GuidesPage() {
  const [activeTab, setActiveTab] = useState<"guides" | "articles">("guides");
  const [guides, setGuides] = useState<GuideItem[]>([]);
  const [articles, setArticles] = useState<ArticleItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedDifficulty, setSelectedDifficulty] = useState("all");
  const [selectedTrust, setSelectedTrust] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  const [isSyncing, startSync] = useTransition();
  const [isEnriching, startEnrich] = useTransition();
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);

  // Load Guides
  const loadGuides = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchGuides({
        category: selectedCategory === "all" ? undefined : selectedCategory,
        difficulty: selectedDifficulty === "all" ? undefined : selectedDifficulty,
        trust_label: selectedTrust === "all" ? undefined : selectedTrust,
        q: searchQuery.trim() || undefined,
      });
      setGuides(res.guides);
    } catch (err: any) {
      setError(err?.message || "Failed loading master craft guides from vault.");
    } finally {
      setLoading(false);
    }
  };

  // Load Articles (RSS feed items)
  const loadArticles = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchArticles({
        category: selectedCategory === "all" ? undefined : selectedCategory,
      });
      setArticles(res.articles);
    } catch (err: any) {
      setError(err?.message || "Failed loading articles from RSS vault.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === "guides") {
      loadGuides();
    } else {
      loadArticles();
    }
  }, [activeTab, selectedCategory, selectedDifficulty, selectedTrust, searchQuery]);

  const handleSyncAllFeeds = () => {
    startSync(async () => {
      setSyncFeedback("Syncing approved RSS feeds...");
      try {
        const summaries: RSSSyncSummaryItem[] = await syncAllRSSFeeds();
        const totalNew = summaries.reduce((acc, s) => acc + s.new_items, 0);
        const totalDupes = summaries.reduce((acc, s) => acc + s.duplicates, 0);
        setSyncFeedback(
          `Feeds synced! Added ${totalNew} new article(s), ${totalDupes} duplicate(s) skipped.`
        );
        if (activeTab === "articles") await loadArticles();
      } catch (err: any) {
        setSyncFeedback(`Sync failed: ${err.message}`);
      }
    });
  };

  const handleEnrichGuides = () => {
    startEnrich(async () => {
      setSyncFeedback("Running AI enrichment on pending items...");
      try {
        const res = await enrichPendingContent({ limit: 10, content_type: "article" });
        setSyncFeedback(
          `AI Enrichment complete! Processed ${res.processed} item(s), ${res.success} enriched.`
        );
        if (activeTab === "articles") await loadArticles();
      } catch (err: any) {
        setSyncFeedback(`AI Enrichment failed: ${err.message}`);
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
              The Knight&apos;s Knowledge Vault
            </span>
            <span className="text-xs text-neutral-400 bg-neutral-900 border border-neutral-800 px-2.5 py-0.5 rounded font-mono">
              Milestone 16 • Editorial Codex
            </span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Blacksmithing &amp; Bladesmithing Library
          </h1>
          <p className="text-neutral-400 mt-2 max-w-2xl text-sm sm:text-base leading-relaxed">
            In-depth master guides with explicit Technical Trust Classifications, peer-reviewed citations, and mandatory safety protocols.
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-3">
          <Link
            href="/sources"
            className="rounded-lg border border-neutral-700 bg-neutral-800/80 px-3.5 py-2 text-xs font-semibold text-neutral-200 hover:bg-neutral-700 hover:text-white transition-colors"
          >
            Source Registry &rarr;
          </Link>

          {activeTab === "articles" && (
            <>
              <button
                type="button"
                onClick={handleEnrichGuides}
                disabled={isEnriching}
                className="rounded-lg border border-purple-900/60 bg-purple-950/40 hover:bg-purple-900/40 disabled:opacity-50 px-3 py-2 text-xs font-semibold text-purple-300 shadow transition-all flex items-center gap-2"
              >
                {isEnriching ? "Enriching..." : "✦ AI Enrich"}
              </button>

              <button
                type="button"
                onClick={handleSyncAllFeeds}
                disabled={isSyncing}
                className="rounded-lg bg-[#FF5722] hover:bg-[#F4511E] disabled:opacity-50 px-4 py-2 text-xs font-semibold text-white shadow transition-all flex items-center gap-2"
              >
                {isSyncing ? "Syncing..." : "Sync Feeds"}
              </button>
            </>
          )}
        </div>
      </div>

      {/* Sync Feedback Alert */}
      {syncFeedback && (
        <div className="mb-6 rounded-lg border border-[#FF5722]/30 bg-[#FF5722]/10 p-3 text-xs text-[#FF8A65] flex items-center justify-between">
          <span>{syncFeedback}</span>
          <button
            type="button"
            onClick={() => setSyncFeedback(null)}
            className="text-neutral-400 hover:text-white ml-4 font-bold"
          >
            &times;
          </button>
        </div>
      )}

      {/* Vault Tabs */}
      <div className="flex border-b border-neutral-800 mb-8">
        <button
          type="button"
          onClick={() => setActiveTab("guides")}
          className={`flex items-center gap-2 pb-4 px-4 text-sm font-bold transition-colors border-b-2 ${
            activeTab === "guides"
              ? "border-[#FF5722] text-white"
              : "border-transparent text-neutral-400 hover:text-neutral-200"
          }`}
        >
          <span>📜 Master Craft Guides</span>
          <span className="rounded-full bg-neutral-800 px-2 py-0.5 text-xs text-neutral-400 font-mono">
            {guides.length}
          </span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("articles")}
          className={`flex items-center gap-2 pb-4 px-4 text-sm font-bold transition-colors border-b-2 ${
            activeTab === "articles"
              ? "border-[#FF5722] text-white"
              : "border-transparent text-neutral-400 hover:text-neutral-200"
          }`}
        >
          <span>📰 Guild Dispatches &amp; RSS</span>
          <span className="rounded-full bg-neutral-800 px-2 py-0.5 text-xs text-neutral-400 font-mono">
            {articles.length}
          </span>
        </button>
      </div>

      {/* Search & Filter Controls */}
      <div className="space-y-4 mb-8 bg-[#141414] border border-neutral-800/80 rounded-2xl p-5 shadow-xs">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search guides, rebound testing, normalizing, metallurgy..."
              className="w-full rounded-xl border border-neutral-700/80 bg-neutral-900/90 px-4 py-2.5 pl-10 text-xs sm:text-sm text-white placeholder-neutral-500 focus:border-[#FF5722] focus:ring-1 focus:ring-[#FF5722] transition-colors"
            />
            <svg
              className="absolute left-3.5 top-3 h-4 w-4 text-neutral-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery("")}
                className="absolute right-3.5 top-3 text-neutral-400 hover:text-white text-xs"
              >
                Clear
              </button>
            )}
          </div>

          {activeTab === "guides" && (
            <>
              {/* Difficulty Filter */}
              <select
                value={selectedDifficulty}
                onChange={(e) => setSelectedDifficulty(e.target.value)}
                className="rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 text-xs text-neutral-200 focus:border-[#FF5722]"
                aria-label="Filter by difficulty"
              >
                {DIFFICULTIES.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.label}
                  </option>
                ))}
              </select>

              {/* Trust Label Filter */}
              <select
                value={selectedTrust}
                onChange={(e) => setSelectedTrust(e.target.value)}
                className="rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 text-xs text-neutral-200 focus:border-[#FF5722]"
                aria-label="Filter by technical trust label"
              >
                {TRUST_FILTERS.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.label}
                  </option>
                ))}
              </select>
            </>
          )}
        </div>

        {/* Category Filter Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
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
        </div>
      </div>

      {/* Main Content Area */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="animate-pulse rounded-2xl border border-neutral-800 bg-[#161616] h-72" />
          ))}
        </div>
      ) : error ? (
        <div className="rounded-2xl border border-red-900/40 bg-red-950/20 p-8 text-center text-red-300">
          <p className="font-semibold text-base mb-2">Error Loading Knowledge Vault</p>
          <p className="text-xs text-neutral-400 mb-4">{error}</p>
          <button
            type="button"
            onClick={activeTab === "guides" ? loadGuides : loadArticles}
            className="rounded bg-neutral-800 px-4 py-2 text-xs text-white hover:bg-neutral-700"
          >
            Retry
          </button>
        </div>
      ) : activeTab === "guides" ? (
        /* Guides Catalog View */
        guides.length === 0 ? (
          <div className="rounded-2xl border border-neutral-800 bg-[#161616] p-12 text-center max-w-xl mx-auto my-8">
            <div className="w-12 h-12 rounded-full bg-[#FF5722]/10 text-[#FF5722] flex items-center justify-center mx-auto mb-4 font-bold text-xl">
              📜
            </div>
            <h2 className="text-lg font-bold text-white mb-2">No Guides Match Filter Criteria</h2>
            <p className="text-xs text-neutral-400 mb-6 leading-relaxed">
              Try adjusting your category, difficulty, or free-text search filters to browse our comprehensive craft guides.
            </p>
            <button
              type="button"
              onClick={() => {
                setSelectedCategory("all");
                setSelectedDifficulty("all");
                setSelectedTrust("all");
                setSearchQuery("");
              }}
              className="rounded-lg bg-[#FF5722] px-4 py-2 text-xs font-semibold text-white shadow hover:bg-[#F4511E]"
            >
              Reset All Filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {guides.map((guide) => {
              const meta = guide.metadata || {};
              const readingTime = meta.reading_time_minutes || 8;
              const trustLabel = meta.trust_label || "craft_practice";
              const author = meta.author || "Guild Master";

              return (
                <div
                  key={guide.id}
                  className="group flex flex-col justify-between rounded-2xl border border-neutral-800 bg-[#161616] p-6 hover:border-[#FF5722]/50 hover:bg-[#1a1a1a] transition-all shadow-sm hover:shadow-md"
                >
                  <div>
                    {/* Header Chips */}
                    <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                      <TrustBadge label={trustLabel} size="sm" />

                      <div className="flex items-center gap-1.5">
                        {guide.difficulty && (
                          <span className="rounded bg-neutral-900 border border-neutral-700/80 px-2 py-0.5 text-[11px] font-mono uppercase text-neutral-300">
                            {guide.difficulty}
                          </span>
                        )}
                        <span className="rounded bg-neutral-900/60 border border-neutral-800 px-2 py-0.5 text-[11px] font-mono text-neutral-400">
                          ⏱️ {readingTime} min
                        </span>
                      </div>
                    </div>

                    {/* Title */}
                    <h2 className="text-lg sm:text-xl font-bold text-white group-hover:text-[#FF8A65] transition-colors leading-snug">
                      <Link href={`/guides/${guide.slug}`}>
                        {guide.title}
                      </Link>
                    </h2>

                    {/* Summary */}
                    <p className="text-xs sm:text-sm text-neutral-300 mt-2.5 line-clamp-3 leading-relaxed">
                      {guide.summary}
                    </p>
                  </div>

                  {/* Footer & Read Link */}
                  <div className="mt-6 pt-4 border-t border-neutral-800/80 flex items-center justify-between text-xs text-neutral-400">
                    <span className="truncate">By <strong className="text-neutral-200">{author}</strong></span>

                    <Link
                      href={`/guides/${guide.slug}`}
                      className="inline-flex items-center gap-1.5 font-semibold text-[#FF5722] group-hover:text-[#FF8A65] transition-colors"
                    >
                      <span>Read Master Guide</span>
                      <span className="transition-transform group-hover:translate-x-1">&rarr;</span>
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        )
      ) : (
        /* Articles (RSS Feed) View */
        articles.length === 0 ? (
          <div className="rounded-2xl border border-neutral-800 bg-[#161616] p-12 text-center max-w-xl mx-auto my-8">
            <div className="w-12 h-12 rounded-full bg-[#FF5722]/10 text-[#FF5722] flex items-center justify-center mx-auto mb-4 font-bold text-xl">
              📰
            </div>
            <h2 className="text-lg font-bold text-white mb-2">RSS Feeds Awaiting Ingestion</h2>
            <p className="text-xs text-neutral-400 mb-6 leading-relaxed">
              No RSS feed articles matching your filters. Synchronize registered feeds or check your Source Registry.
            </p>
            <button
              type="button"
              onClick={handleSyncAllFeeds}
              disabled={isSyncing}
              className="rounded-lg bg-[#FF5722] px-4 py-2 text-xs font-semibold text-white shadow hover:bg-[#F4511E]"
            >
              Sync All Feeds Now
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((art) => {
              const externalUrl = art.source?.source_url || art.metadata?.article_url;
              const author = art.metadata?.author || art.source?.source_name || "Guild Author";

              return (
                <div
                  key={art.id}
                  className="flex flex-col justify-between rounded-xl border border-neutral-800 bg-[#181818] p-5 hover:border-[#FF5722]/40 transition-all shadow-xs"
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 text-xs text-neutral-400 mb-3">
                      <span className="font-semibold text-[#FF8A65] truncate max-w-[65%]">
                        {art.source?.source_name || "RSS Source"}
                      </span>
                      {art.published_at && (
                        <span className="font-mono text-[11px] text-neutral-500">
                          {new Date(art.published_at).toLocaleDateString()}
                        </span>
                      )}
                    </div>

                    <h3 className="text-base font-bold text-white leading-snug line-clamp-2">
                      {art.title}
                    </h3>

                    <p className="text-xs text-neutral-300 mt-2 line-clamp-3 leading-relaxed">
                      {art.summary}
                    </p>
                  </div>

                  <div className="mt-5 pt-3 border-t border-neutral-800 flex items-center justify-between text-xs">
                    <span className="text-neutral-500 truncate max-w-[50%]">{author}</span>
                    {externalUrl && (
                      <a
                        href={externalUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 font-semibold text-[#FF8A65] hover:text-[#FF5722]"
                      >
                        <span>Full Article</span>
                        <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </a>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )
      )}
    </div>
  );
}
