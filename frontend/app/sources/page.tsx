"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  fetchSources,
  createSource,
  updateSource,
  deleteSource,
  testSourceConnection,
  SourceItem,
} from "@/lib/api";

export default function SourcesPage() {
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterType, setFilterType] = useState<string>("all");

  // Form state
  const [showAddModal, setShowAddModal] = useState(false);
  const [formName, setFormName] = useState("");
  const [formType, setFormType] = useState<string>("youtube_channel");
  const [formPlatform, setFormPlatform] = useState("youtube");
  const [formUrl, setFormUrl] = useState("");
  const [formPriority, setFormPriority] = useState(10);
  const [formCategories, setFormCategories] = useState("blacksmithing");
  const [submitting, setSubmitting] = useState(false);
  const [testingId, setTestingId] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<string | null>(null);

  async function loadSources() {
    setLoading(true);
    setError(null);
    try {
      const typeParam = filterType === "all" ? undefined : filterType;
      const data = await fetchSources({ type: typeParam });
      setSources(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load sources");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadSources();
  }, [filterType]);

  async function handleAddSource(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await createSource({
        name: formName,
        type: formType,
        platform: formPlatform,
        url: formUrl,
        priority: Number(formPriority),
        categories: formCategories.split(",").map((c) => c.trim()).filter(Boolean),
        enabled: true,
      });

      setShowAddModal(false);
      setFormName("");
      setFormUrl("");
      await loadSources();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to create source");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleToggleEnabled(source: SourceItem) {
    try {
      await updateSource(source.id, { enabled: !source.enabled });
      await loadSources();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to update source");
    }
  }

  async function handleDeleteSource(id: string) {
    if (!confirm("Are you sure you want to delete this source from the registry?")) return;
    try {
      await deleteSource(id);
      await loadSources();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to delete source");
    }
  }

  async function handleTestSource(id: string) {
    setTestingId(id);
    setTestResult(null);
    try {
      const res = await testSourceConnection(id);
      setTestResult(`${res.reachable ? "Reachable" : "Unreachable"}: ${res.details}`);
      await loadSources();
    } catch (err: unknown) {
      setTestResult(`Test failed: ${err instanceof Error ? err.message : "Error"}`);
    } finally {
      setTestingId(null);
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-neutral-800 pb-6 mb-8">
        <div>
          <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3">
            Controlled Ingestion Registry
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Approved Source Registry
          </h1>
          <p className="text-neutral-400 mt-2 max-w-2xl text-sm sm:text-base">
            Manage approved YouTube channels, RSS feeds, and product providers. Content is only ingested from sources configured here.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <Link
            href="/videos/channels"
            className="inline-flex items-center justify-center rounded-lg border border-neutral-700 bg-neutral-850 px-3.5 py-2.5 text-xs font-semibold text-neutral-200 hover:text-white hover:bg-neutral-800 transition-colors"
          >
            &#9658; YouTube Channels
          </Link>
          <button
            type="button"
            onClick={() => setShowAddModal(true)}
            className="inline-flex items-center justify-center rounded-lg bg-[#FF5722] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[#FF7043] transition-colors focus-visible:ring-2 focus-visible:ring-[#FF5722] shadow-md shadow-[#FF5722]/20 shrink-0"
          >
            + Add Approved Source
          </button>
        </div>
      </div>

      {/* Anti-crawling policy alert */}
      <div className="rounded-xl border border-neutral-800 bg-[#161616] p-4 mb-8 flex items-start gap-3">
        <div className="text-[#FF5722] text-lg font-bold">&#x26A0;</div>
        <div className="text-xs text-neutral-400 leading-relaxed">
          <strong className="text-white">Strict No-Crawling Policy:</strong> Blacksmith Knight does not perform open-web crawling or autonomous source discovery. External data is acquired deterministically only from the sources explicitly enabled below.
        </div>
      </div>

      {/* Notification / Error / Test banner */}
      {testResult && (
        <div className="rounded-lg bg-neutral-900 border border-neutral-700 p-3 text-xs text-neutral-200 mb-6 flex justify-between items-center">
          <span>{testResult}</span>
          <button type="button" onClick={() => setTestResult(null)} className="text-neutral-400 hover:text-white ml-4">
            &times;
          </button>
        </div>
      )}
      {error && (
        <div className="rounded-lg bg-red-950/40 border border-red-800/50 p-3 text-xs text-red-300 mb-6 flex justify-between items-center">
          <span>{error}</span>
          <button type="button" onClick={() => setError(null)} className="text-red-400 hover:text-white ml-4">
            &times;
          </button>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex flex-wrap gap-2 mb-6 border-b border-neutral-800 pb-4">
        {[
          { key: "all", label: "All Sources" },
          { key: "youtube_channel", label: "YouTube Channels" },
          { key: "rss_feed", label: "RSS Feeds" },
          { key: "product_api", label: "Shop Providers" },
        ].map((tab) => (
          <button
            key={tab.key}
            type="button"
            onClick={() => setFilterType(tab.key)}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
              filterType === tab.key
                ? "bg-neutral-800 text-[#FF5722] font-semibold border-b-2 border-[#FF5722]"
                : "text-neutral-400 hover:bg-neutral-850 hover:text-white"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Sources Grid */}
      {loading ? (
        <div className="text-neutral-500 text-sm py-12 text-center">Loading sources from registry...</div>
      ) : sources.length === 0 ? (
        <div className="rounded-xl border border-dashed border-neutral-800 p-12 text-center text-neutral-500 text-sm">
          No sources registered in this category yet. Click &ldquo;+ Add Approved Source&rdquo; above to register one.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sources.map((source) => (
            <div
              key={source.id}
              className={`rounded-xl border p-6 flex flex-col justify-between transition-colors ${
                source.enabled
                  ? "bg-[#1a1a1a] border-neutral-800 hover:border-neutral-700"
                  : "bg-[#141414] border-neutral-900 opacity-60"
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="inline-block font-mono text-[10px] uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-2 py-0.5 rounded">
                    {source.platform}
                  </span>
                  <span
                    className={`text-[10px] font-mono px-2 py-0.5 rounded-full uppercase ${
                      source.status === "healthy"
                        ? "bg-emerald-950/60 text-emerald-400 border border-emerald-800/40"
                        : source.status === "warning"
                        ? "bg-amber-950/60 text-amber-400 border border-amber-800/40"
                        : "bg-neutral-800 text-neutral-400"
                    }`}
                  >
                    {source.status}
                  </span>
                </div>

                <h3 className="text-lg font-bold text-white mb-1 truncate" title={source.name}>
                  {source.name}
                </h3>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs text-neutral-500 hover:text-neutral-300 transition-colors truncate block mb-4"
                  title={source.url}
                >
                  {source.url}
                </a>

                <div className="flex flex-wrap gap-1 mb-4">
                  {source.categories.map((c) => (
                    <span key={c} className="text-[10px] bg-neutral-850 text-neutral-400 px-2 py-0.5 rounded">
                      {c}
                    </span>
                  ))}
                  <span className="text-[10px] text-neutral-500 self-center ml-auto">
                    Priority: {source.priority}
                  </span>
                </div>
              </div>

              <div className="border-t border-neutral-800/80 pt-4 mt-2 flex items-center justify-between text-xs">
                <button
                  type="button"
                  onClick={() => handleToggleEnabled(source)}
                  className={`px-3 py-1 rounded font-medium transition-colors ${
                    source.enabled
                      ? "bg-emerald-900/40 text-emerald-400 hover:bg-emerald-900/60"
                      : "bg-neutral-800 text-neutral-400 hover:bg-neutral-700"
                  }`}
                >
                  {source.enabled ? "Active" : "Disabled"}
                </button>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    disabled={testingId === source.id}
                    onClick={() => handleTestSource(source.id)}
                    className="text-neutral-400 hover:text-white px-2 py-1 rounded hover:bg-neutral-800 transition-colors disabled:opacity-50"
                  >
                    {testingId === source.id ? "Pinging..." : "Test"}
                  </button>

                  <button
                    type="button"
                    onClick={() => handleDeleteSource(source.id)}
                    className="text-red-400 hover:text-red-300 px-2 py-1 rounded hover:bg-red-950/30 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Source Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
          <div className="w-full max-w-md rounded-2xl border border-neutral-800 bg-[#171717] p-6 shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-bold text-white">Add Approved Source</h2>
              <button
                type="button"
                onClick={() => setShowAddModal(false)}
                className="text-neutral-400 hover:text-white text-lg"
              >
                &times;
              </button>
            </div>

            <form onSubmit={handleAddSource} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-neutral-300 mb-1">
                  Source Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Black Bear Forge"
                  value={formName}
                  onChange={(e) => setFormName(e.target.value)}
                  className="w-full rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-sm text-white placeholder-neutral-500 focus-visible:ring-2 focus-visible:ring-[#FF5722]"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-neutral-300 mb-1">
                    Family / Type
                  </label>
                  <select
                    value={formType}
                    onChange={(e) => {
                      setFormType(e.target.value);
                      if (e.target.value === "youtube_channel") setFormPlatform("youtube");
                      if (e.target.value === "rss_feed") setFormPlatform("rss");
                      if (e.target.value === "product_api") setFormPlatform("amazon");
                    }}
                    className="w-full rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-sm text-white focus-visible:ring-2 focus-visible:ring-[#FF5722]"
                  >
                    <option value="youtube_channel">YouTube Channel</option>
                    <option value="rss_feed">RSS Feed</option>
                    <option value="product_api">Product API</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-neutral-300 mb-1">
                    Platform
                  </label>
                  <input
                    type="text"
                    required
                    value={formPlatform}
                    onChange={(e) => setFormPlatform(e.target.value)}
                    className="w-full rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-sm text-white focus-visible:ring-2 focus-visible:ring-[#FF5722]"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-neutral-300 mb-1">
                  Source Target URL
                </label>
                <input
                  type="url"
                  required
                  placeholder="https://www.youtube.com/@blackbearforge"
                  value={formUrl}
                  onChange={(e) => setFormUrl(e.target.value)}
                  className="w-full rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-sm text-white placeholder-neutral-500 focus-visible:ring-2 focus-visible:ring-[#FF5722]"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-neutral-300 mb-1">
                    Priority (1-100)
                  </label>
                  <input
                    type="number"
                    min={1}
                    max={100}
                    value={formPriority}
                    onChange={(e) => setFormPriority(Number(e.target.value))}
                    className="w-full rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-sm text-white focus-visible:ring-2 focus-visible:ring-[#FF5722]"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-neutral-300 mb-1">
                    Categories (comma separated)
                  </label>
                  <input
                    type="text"
                    value={formCategories}
                    onChange={(e) => setFormCategories(e.target.value)}
                    className="w-full rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-sm text-white focus-visible:ring-2 focus-visible:ring-[#FF5722]"
                  />
                </div>
              </div>

              <div className="pt-4 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 text-sm text-neutral-400 hover:text-white transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="rounded-lg bg-[#FF5722] px-4 py-2 text-sm font-semibold text-white hover:bg-[#FF7043] transition-colors focus-visible:ring-2 focus-visible:ring-[#FF5722] disabled:opacity-50"
                >
                  {submitting ? "Adding..." : "Add Source"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
