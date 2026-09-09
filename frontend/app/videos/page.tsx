"use client";

import { useEffect, useState, useTransition } from "react";
import Link from "next/link";
import {
  fetchVideos,
  fetchApiKeysStatus,
  updateApiKeys,
  syncAllYouTubeChannels,
  VideoItem,
  ApiKeysStatus,
  SyncSummaryItem,
} from "@/lib/api";

const CATEGORIES = [
  { id: "all", label: "All Topics" },
  { id: "forging", label: "Forging" },
  { id: "bladesmithing", label: "Bladesmithing" },
  { id: "heat-treatment", label: "Heat Treatment" },
  { id: "tools", label: "Tools & Anvils" },
];

function formatDuration(seconds?: number): string {
  if (!seconds || seconds <= 0) return "";
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
}

export default function VideosPage() {
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState("all");

  // Sync state
  const [isSyncing, startSync] = useTransition();
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);

  // API Key Settings Modal
  const [keysStatus, setKeysStatus] = useState<ApiKeysStatus | null>(null);
  const [isKeyModalOpen, setIsKeyModalOpen] = useState(false);
  const [apiKeyInput, setApiKeyInput] = useState("");
  const [isSavingKey, setIsSavingKey] = useState(false);
  const [keyFeedback, setKeyFeedback] = useState<string | null>(null);

  // Active video embed preview
  const [activeVideo, setActiveVideo] = useState<VideoItem | null>(null);

  const loadData = async (cat = selectedCategory) => {
    setLoading(true);
    setError(null);
    try {
      const categoryParam = cat === "all" ? undefined : cat;
      const res = await fetchVideos({ category: categoryParam });
      setVideos(res.videos);
    } catch (err: any) {
      setError(err?.message || "Failed loading videos from knowledge vault.");
    } finally {
      setLoading(false);
    }
  };

  const loadKeys = async () => {
    try {
      const status = await fetchApiKeysStatus();
      setKeysStatus(status);
    } catch {
      // Backend may be offline
    }
  };

  useEffect(() => {
    loadData(selectedCategory);
    loadKeys();
  }, [selectedCategory]);

  const handleSaveKey = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!apiKeyInput.trim()) return;
    setIsSavingKey(true);
    setKeyFeedback(null);
    try {
      const res = await updateApiKeys({ youtube_api_key: apiKeyInput.trim() });
      setKeysStatus(res);
      setKeyFeedback("YouTube API Key saved successfully to Firestore & runtime cache!");
      setApiKeyInput("");
      setTimeout(() => {
        setIsKeyModalOpen(false);
        setKeyFeedback(null);
      }, 1500);
    } catch (err: any) {
      setKeyFeedback(`Error: ${err.message}`);
    } finally {
      setIsSavingKey(false);
    }
  };

  const handleSyncAll = () => {
    startSync(async () => {
      setSyncFeedback("Syncing all approved channels...");
      try {
        const summaries: SyncSummaryItem[] = await syncAllYouTubeChannels();
        const totalNew = summaries.reduce((acc, s) => acc + s.new_items, 0);
        const totalDupes = summaries.reduce((acc, s) => acc + s.duplicates, 0);
        setSyncFeedback(
          `Sync complete! Added ${totalNew} new video(s), skipped ${totalDupes} duplicate(s).`
        );
        await loadData(selectedCategory);
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
              Controlled Ingestion
            </span>
            {keysStatus?.youtube_api_key_configured ? (
              <span className="text-xs font-medium text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded border border-emerald-500/20">
                API Key Active ({keysStatus.youtube_api_key_masked})
              </span>
            ) : (
              <span className="text-xs font-medium text-amber-400 bg-amber-500/10 px-2.5 py-0.5 rounded border border-amber-500/20">
                Offline Mode / Fallback Fixtures
              </span>
            )}
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Curated Forge Videos
          </h1>
          <p className="text-neutral-400 mt-2 max-w-2xl text-sm sm:text-base">
            Ingested strictly from user-approved channels. Deterministically deduplicated and stored in the forge vault.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={() => setIsKeyModalOpen(true)}
            className="rounded-lg border border-neutral-700 bg-neutral-800/80 px-3 py-2 text-xs font-semibold text-neutral-200 hover:bg-neutral-700 hover:text-white transition-colors flex items-center gap-2"
          >
            <svg className="w-4 h-4 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
            </svg>
            API Key
          </button>

          <Link
            href="/videos/channels"
            className="rounded-lg border border-neutral-700 bg-neutral-800/80 px-3 py-2 text-xs font-semibold text-neutral-200 hover:bg-neutral-700 hover:text-white transition-colors"
          >
            Manage Channels &rarr;
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
                Syncing Vault...
              </>
            ) : (
              <>
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Sync All Channels
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

      {/* Category Tabs */}
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
          {videos.length} video{videos.length === 1 ? "" : "s"} in vault
        </span>
      </div>

      {/* Main Content Area */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="animate-pulse rounded-xl border border-neutral-800 bg-[#171717] h-72" />
          ))}
        </div>
      ) : error ? (
        <div className="rounded-xl border border-red-900/40 bg-red-950/20 p-8 text-center text-red-300">
          <p className="font-semibold text-base mb-2">Error Loading Knowledge Vault</p>
          <p className="text-xs text-neutral-400 mb-4">{error}</p>
          <button
            type="button"
            onClick={() => loadData(selectedCategory)}
            className="rounded bg-neutral-800 px-4 py-2 text-xs text-white hover:bg-neutral-700"
          >
            Retry
          </button>
        </div>
      ) : videos.length === 0 ? (
        <div className="rounded-2xl border border-neutral-800 bg-[#161616] p-12 text-center max-w-xl mx-auto my-8">
          <div className="w-12 h-12 rounded-full bg-[#FF5722]/10 text-[#FF5722] flex items-center justify-center mx-auto mb-4 font-bold text-xl">
            &#9658;
          </div>
          <h2 className="text-lg font-bold text-white mb-2">Knowledge Vault Awaiting Videos</h2>
          <p className="text-xs text-neutral-400 mb-6 leading-relaxed">
            No videos matching this filter yet. Sync approved channels to ingest high-quality tutorials into your local repository.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <button
              type="button"
              onClick={handleSyncAll}
              disabled={isSyncing}
              className="rounded-lg bg-[#FF5722] px-4 py-2 text-xs font-semibold text-white shadow hover:bg-[#F4511E] transition-all"
            >
              Sync All Channels Now
            </button>
            <Link
              href="/videos/channels"
              className="rounded-lg border border-neutral-700 bg-neutral-800 px-4 py-2 text-xs font-medium text-neutral-300 hover:text-white"
            >
              Configure Channels
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {videos.map((vid) => {
            const ytId = vid.metadata?.youtube_video_id || vid.id.replace("yt_", "");
            const watchUrl = vid.source?.source_url || `https://www.youtube.com/watch?v=${ytId}`;
            const duration = formatDuration(vid.metadata?.duration_seconds);

            return (
              <div
                key={vid.id}
                className="group flex flex-col rounded-xl border border-neutral-800 bg-[#181818] overflow-hidden hover:border-[#FF5722]/40 transition-all shadow-sm hover:shadow-md"
              >
                {/* Thumbnail container */}
                <div className="relative aspect-video w-full bg-neutral-900 overflow-hidden">
                  {vid.image_url ? (
                    <img
                      src={vid.image_url}
                      alt={vid.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      loading="lazy"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-neutral-600">
                      Forge Video
                    </div>
                  )}

                  {/* Duration badge */}
                  {duration && (
                    <span className="absolute bottom-2 right-2 rounded bg-black/80 backdrop-blur-xs px-2 py-0.5 text-[10px] font-mono text-white">
                      {duration}
                    </span>
                  )}

                  {/* Play trigger overlay */}
                  <button
                    type="button"
                    onClick={() => setActiveVideo(vid)}
                    className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity"
                    aria-label={`Preview ${vid.title}`}
                  >
                    <div className="w-12 h-12 rounded-full bg-[#FF5722] text-white flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform">
                      <span className="ml-0.5 text-lg">&#9658;</span>
                    </div>
                  </button>
                </div>

                {/* Content body */}
                <div className="flex flex-col flex-1 p-4">
                  {/* Category & Channel Info */}
                  <div className="flex items-center justify-between gap-2 text-xs text-neutral-400 mb-2">
                    <span className="font-medium text-[#FF8A65] truncate">
                      {vid.source?.source_name || vid.metadata?.channel_name || "Approved Creator"}
                    </span>
                    <span className="capitalize text-[11px] bg-neutral-800/80 px-2 py-0.5 rounded text-neutral-300">
                      {vid.category}
                    </span>
                  </div>

                  {/* Video Title */}
                  <h3 className="text-sm font-bold text-white line-clamp-2 mb-2 group-hover:text-[#FF8A65] transition-colors">
                    {vid.title}
                  </h3>

                  {/* Video Summary */}
                  <p className="text-xs text-neutral-400 line-clamp-2 mb-4 leading-relaxed">
                    {vid.summary}
                  </p>

                  {/* Tags and Watch button */}
                  <div className="mt-auto pt-3 border-t border-neutral-850 flex items-center justify-between gap-2">
                    <div className="flex flex-wrap gap-1 max-w-[65%]">
                      {vid.tags?.slice(0, 2).map((tag) => (
                        <span key={tag} className="text-[10px] text-neutral-400 bg-neutral-900 px-1.5 py-0.5 rounded">
                          #{tag}
                        </span>
                      ))}
                    </div>

                    <a
                      href={watchUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs font-semibold text-[#FF5722] hover:text-[#F4511E] transition-colors"
                    >
                      Watch
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </a>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Video Embed Modal */}
      {activeVideo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-xs p-4">
          <div className="relative w-full max-w-3xl rounded-2xl border border-neutral-800 bg-[#141414] overflow-hidden shadow-2xl">
            <div className="flex items-center justify-between p-4 border-b border-neutral-800">
              <h3 className="text-sm font-bold text-white truncate max-w-lg">
                {activeVideo.title}
              </h3>
              <button
                type="button"
                onClick={() => setActiveVideo(null)}
                className="text-neutral-400 hover:text-white p-1"
                aria-label="Close modal"
              >
                &times;
              </button>
            </div>
            <div className="relative aspect-video w-full bg-black">
              <iframe
                src={`https://www.youtube.com/embed/${activeVideo.metadata?.youtube_video_id || activeVideo.id.replace("yt_", "")}?autoplay=1`}
                title={activeVideo.title}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="w-full h-full border-0"
              />
            </div>
          </div>
        </div>
      )}

      {/* API Key Modal */}
      {isKeyModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-xs p-4">
          <div className="w-full max-w-md rounded-2xl border border-neutral-800 bg-[#161616] p-6 shadow-2xl">
            <div className="flex items-center justify-between pb-4 border-b border-neutral-800 mb-4">
              <h3 className="text-base font-bold text-white">Configure YouTube API Key</h3>
              <button
                type="button"
                onClick={() => setIsKeyModalOpen(false)}
                className="text-neutral-400 hover:text-white text-lg font-bold"
              >
                &times;
              </button>
            </div>

            <p className="text-xs text-neutral-400 mb-4 leading-relaxed">
              Provides YouTube Data API v3 credentials for live synchronization. Stored securely in local Firestore and runtime cache. Does not require server restart.
            </p>

            <form onSubmit={handleSaveKey} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-neutral-300 mb-1">
                  YouTube API Key
                </label>
                <input
                  type="password"
                  value={apiKeyInput}
                  onChange={(e) => setApiKeyInput(e.target.value)}
                  placeholder={keysStatus?.youtube_api_key_masked || "AIzaSy..."}
                  className="w-full rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-2 text-xs text-white placeholder-neutral-500 focus:border-[#FF5722] focus:outline-none"
                />
                {keysStatus?.youtube_api_key_configured && (
                  <p className="mt-1 text-[11px] text-emerald-400">
                    Currently active: {keysStatus.youtube_api_key_masked}
                  </p>
                )}
              </div>

              {keyFeedback && (
                <div className={`p-2.5 rounded text-xs ${keyFeedback.startsWith("Error") ? "bg-red-950/40 text-red-400 border border-red-900/40" : "bg-emerald-950/40 text-emerald-400 border border-emerald-900/40"}`}>
                  {keyFeedback}
                </div>
              )}

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsKeyModalOpen(false)}
                  className="rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-1.5 text-xs text-neutral-300 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSavingKey || !apiKeyInput.trim()}
                  className="rounded-lg bg-[#FF5722] hover:bg-[#F4511E] disabled:opacity-50 px-4 py-1.5 text-xs font-semibold text-white shadow"
                >
                  {isSavingKey ? "Saving..." : "Save Key"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
