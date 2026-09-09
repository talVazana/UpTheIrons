"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  fetchYouTubeChannels,
  createYouTubeChannel,
  updateYouTubeChannel,
  deleteYouTubeChannel,
  resolveYouTubeChannel,
  syncYouTubeChannel,
  YouTubeChannelItem,
  ResolveChannelResult,
} from "@/lib/api";

const PRESET_CATEGORIES = [
  "Blacksmithing",
  "Bladesmithing",
  "Anvil Techniques",
  "Tool Making",
  "Heat Treatment",
  "Joinery",
  "Power Hammer",
  "Metallurgy",
];

export default function YouTubeChannelsPage() {
  const [channels, setChannels] = useState<YouTubeChannelItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterEnabled, setFilterEnabled] = useState<"all" | "active" | "disabled">("all");
  const [filterCategory, setFilterCategory] = useState<string>("all");
  const [feedback, setFeedback] = useState<{ type: "success" | "error"; message: string } | null>(null);

  // Add Channel Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [inputQuery, setInputQuery] = useState("");
  const [priority, setPriority] = useState(15);
  const [selectedCategories, setSelectedCategories] = useState<string[]>(["Blacksmithing"]);
  const [resolving, setResolving] = useState(false);
  const [resolvedPreview, setResolvedPreview] = useState<ResolveChannelResult | null>(null);
  const [creating, setCreating] = useState(false);

  // Syncing state tracker
  const [syncingId, setSyncingId] = useState<string | null>(null);

  useEffect(() => {
    loadChannels();
  }, []);

  async function loadChannels() {
    try {
      setLoading(true);
      const res = await fetchYouTubeChannels();
      setChannels(res.channels);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to load channels";
      setFeedback({ type: "error", message: msg });
    } finally {
      setLoading(false);
    }
  }

  async function handleResolve() {
    if (!inputQuery.trim()) return;
    setResolving(true);
    setFeedback(null);
    try {
      const preview = await resolveYouTubeChannel(inputQuery.trim());
      setResolvedPreview(preview);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Unable to resolve channel identifier.";
      setFeedback({ type: "error", message: msg });
      setResolvedPreview(null);
    } finally {
      setResolving(false);
    }
  }

  async function handleCreateChannel(e: React.FormEvent) {
    e.preventDefault();
    if (!inputQuery.trim()) return;
    setCreating(true);
    setFeedback(null);

    try {
      await createYouTubeChannel({
        url_or_handle: inputQuery.trim(),
        name: resolvedPreview?.name,
        priority,
        categories: selectedCategories,
        thumbnail_url: resolvedPreview?.thumbnail_url,
      });

      setFeedback({ type: "success", message: `Channel successfully registered in the forge vault!` });
      setModalOpen(false);
      setInputQuery("");
      setResolvedPreview(null);
      await loadChannels();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to register channel.";
      setFeedback({ type: "error", message: msg });
    } finally {
      setCreating(false);
    }
  }

  async function handleToggleEnabled(channel: YouTubeChannelItem) {
    try {
      const newEnabled = !channel.enabled;
      await updateYouTubeChannel(channel.id, { enabled: newEnabled });
      setChannels((prev) =>
        prev.map((c) => (c.id === channel.id ? { ...c, enabled: newEnabled } : c))
      );
      setFeedback({
        type: "success",
        message: `Channel '${channel.name}' ${newEnabled ? "enabled" : "disabled"} for video collection.`,
      });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to toggle channel status.";
      setFeedback({ type: "error", message: msg });
    }
  }

  async function handleSync(channel: YouTubeChannelItem) {
    if (!channel.enabled) {
      setFeedback({ type: "error", message: "Cannot sync a disabled channel. Enable it first." });
      return;
    }
    setSyncingId(channel.id);
    setFeedback(null);
    try {
      const result = await syncYouTubeChannel(channel.id);
      setChannels((prev) =>
        prev.map((c) =>
          c.id === channel.id
            ? { ...c, status: "healthy", last_synced_at: result.last_synced_at }
            : c
        )
      );
      setFeedback({
        type: "success",
        message: `Sync triggered for '${channel.name}'. Baseline sync verified.`,
      });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to trigger sync.";
      setFeedback({ type: "error", message: msg });
    } finally {
      setSyncingId(null);
    }
  }

  async function handleDelete(channel: YouTubeChannelItem) {
    if (!confirm(`Remove '${channel.name}' from approved channels? Historical videos in the vault will be retained.`)) {
      return;
    }

    try {
      await deleteYouTubeChannel(channel.id);
      setChannels((prev) => prev.filter((c) => c.id !== channel.id));
      setFeedback({ type: "success", message: `Channel '${channel.name}' removed.` });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to remove channel.";
      setFeedback({ type: "error", message: msg });
    }
  }

  function toggleCategorySelection(cat: string) {
    setSelectedCategories((prev) =>
      prev.includes(cat) ? prev.filter((c) => c !== cat) : [...prev, cat]
    );
  }

  const filteredChannels = channels.filter((c) => {
    if (filterEnabled === "active" && !c.enabled) return false;
    if (filterEnabled === "disabled" && c.enabled) return false;
    if (filterCategory !== "all" && !c.categories.includes(filterCategory.toLowerCase())) {
      return false;
    }
    return true;
  });

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Navigation Breadcrumb */}
      <div className="mb-6 flex items-center gap-2 text-xs text-neutral-400">
        <Link href="/" className="hover:text-white transition-colors">
          Forge
        </Link>
        <span>/</span>
        <Link href="/videos" className="hover:text-white transition-colors">
          Videos
        </Link>
        <span>/</span>
        <span className="text-[#FF5722] font-semibold">Approved Channels</span>
      </div>

      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-neutral-800 pb-6 mb-8">
        <div>
          <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-2">
            Section 88 &bull; Controlled Pipeline
          </span>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Approved YouTube Channels
          </h1>
          <p className="text-neutral-400 mt-1 max-w-2xl text-sm">
            Strict user-approved channel registry. Video collectors ingest strictly from enabled channels here. No open-web crawling.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setModalOpen(true)}
            className="inline-flex items-center gap-2 rounded-md bg-[#FF5722] px-4 py-2.5 text-sm font-semibold text-white shadow hover:bg-[#F4511E] transition-colors focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[#FF5722]"
          >
            <span>+</span>
            <span>Add Approved Channel</span>
          </button>
        </div>
      </div>

      {/* Feedback Banner */}
      {feedback && (
        <div
          className={`mb-6 rounded-lg p-4 text-sm flex items-center justify-between ${
            feedback.type === "success"
              ? "bg-emerald-950/40 border border-emerald-800/60 text-emerald-300"
              : "bg-rose-950/40 border border-rose-800/60 text-rose-300"
          }`}
        >
          <span>{feedback.message}</span>
          <button
            onClick={() => setFeedback(null)}
            className="text-xs font-bold uppercase opacity-80 hover:opacity-100 ml-4"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div className="flex items-center gap-1 border-b border-neutral-800 pb-1">
          <button
            onClick={() => setFilterEnabled("all")}
            className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
              filterEnabled === "all"
                ? "bg-neutral-800 text-white font-semibold"
                : "text-neutral-400 hover:text-white"
            }`}
          >
            All Channels ({channels.length})
          </button>
          <button
            onClick={() => setFilterEnabled("active")}
            className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
              filterEnabled === "active"
                ? "bg-neutral-800 text-emerald-400 font-semibold"
                : "text-neutral-400 hover:text-white"
            }`}
          >
            Enabled ({channels.filter((c) => c.enabled).length})
          </button>
          <button
            onClick={() => setFilterEnabled("disabled")}
            className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
              filterEnabled === "disabled"
                ? "bg-neutral-800 text-neutral-400 font-semibold"
                : "text-neutral-400 hover:text-white"
            }`}
          >
            Disabled ({channels.filter((c) => !c.enabled).length})
          </button>
        </div>

        {/* Category Filter */}
        <div className="flex items-center gap-2">
          <label htmlFor="cat-filter" className="text-xs text-neutral-400 font-medium">
            Category:
          </label>
          <select
            id="cat-filter"
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="rounded-md border border-neutral-800 bg-[#171717] px-2.5 py-1 text-xs text-neutral-200 focus:border-[#FF5722] focus:outline-none"
          >
            <option value="all">All Categories</option>
            {PRESET_CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Loading Skeleton */}
      {loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-48 rounded-xl border border-neutral-800 bg-[#171717] animate-pulse" />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && filteredChannels.length === 0 && (
        <div className="rounded-xl border border-dashed border-neutral-800 bg-[#141414] p-12 text-center max-w-lg mx-auto">
          <div className="w-12 h-12 rounded-full bg-[#FF5722]/10 text-[#FF5722] flex items-center justify-center mx-auto mb-4 font-bold text-xl">
            &#9658;
          </div>
          <h3 className="text-base font-bold text-white mb-1">No Channels Found</h3>
          <p className="text-xs text-neutral-400 mb-6">
            Add trusted blacksmithing channels such as @BlackBearForge or @TorbjornAhman to establish your video knowledge stream.
          </p>
          <button
            onClick={() => setModalOpen(true)}
            className="rounded-md bg-neutral-800 hover:bg-neutral-700 text-white px-4 py-2 text-xs font-semibold transition-colors"
          >
            Add Your First Channel
          </button>
        </div>
      )}

      {/* Channel Grid */}
      {!loading && filteredChannels.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredChannels.map((channel) => (
            <div
              key={channel.id}
              className={`flex flex-col justify-between rounded-xl border bg-[#171717] p-5 transition-all ${
                channel.enabled
                  ? "border-neutral-800 hover:border-neutral-700"
                  : "border-neutral-850 opacity-60 bg-[#141414]"
              }`}
            >
              <div>
                {/* Header with Avatar & Status */}
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="flex items-center gap-3">
                    <img
                      src={channel.thumbnail_url || `https://api.dicebear.com/7.x/identicon/svg?seed=${channel.id}`}
                      alt={channel.name}
                      className="w-11 h-11 rounded-full object-cover border border-neutral-800 bg-neutral-900"
                      onError={(e) => {
                        (e.target as HTMLImageElement).src = `https://api.dicebear.com/7.x/identicon/svg?seed=${channel.id}`;
                      }}
                    />
                    <div>
                      <h2 className="text-sm font-bold text-white hover:text-[#FF5722] transition-colors line-clamp-1">
                        <a href={channel.url} target="_blank" rel="noopener noreferrer">
                          {channel.name}
                        </a>
                      </h2>
                      <div className="flex items-center gap-1.5 text-xs text-neutral-400">
                        <span>{channel.handle || `@${channel.id}`}</span>
                      </div>
                    </div>
                  </div>

                  {/* Enabled Toggle Switch */}
                  <button
                    type="button"
                    onClick={() => handleToggleEnabled(channel)}
                    className={`relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-[#FF5722] ${
                      channel.enabled ? "bg-emerald-600" : "bg-neutral-700"
                    }`}
                    role="switch"
                    aria-checked={channel.enabled}
                    title={channel.enabled ? "Channel Enabled" : "Channel Disabled"}
                  >
                    <span
                      aria-hidden="true"
                      className={`pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                        channel.enabled ? "translate-x-4" : "translate-x-0"
                      }`}
                    />
                  </button>
                </div>

                {/* Badges & Meta */}
                <div className="flex flex-wrap items-center gap-2 mb-3 text-[11px]">
                  <span className="rounded bg-neutral-800/80 px-2 py-0.5 text-neutral-300 font-mono">
                    Priority: {channel.priority}
                  </span>
                  <span
                    className={`rounded px-2 py-0.5 font-medium ${
                      channel.status === "healthy"
                        ? "bg-emerald-950/60 text-emerald-400 border border-emerald-800/40"
                        : channel.status === "warning"
                        ? "bg-amber-950/60 text-amber-400 border border-amber-800/40"
                        : "bg-neutral-800 text-neutral-300"
                    }`}
                  >
                    {channel.status}
                  </span>
                  {channel.video_count > 0 && (
                    <span className="text-neutral-400">
                      {channel.video_count} videos
                    </span>
                  )}
                </div>

                {/* Category Tags */}
                {channel.categories.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-4">
                    {channel.categories.map((cat) => (
                      <span
                        key={cat}
                        className="rounded-full bg-neutral-800/60 px-2 py-0.5 text-[10px] text-neutral-400 uppercase tracking-wider"
                      >
                        {cat}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Card Footer Actions */}
              <div className="border-t border-neutral-800/80 pt-3 flex items-center justify-between text-xs text-neutral-400">
                <span className="truncate text-[11px]">
                  {channel.last_synced_at
                    ? `Synced: ${new Date(channel.last_synced_at).toLocaleDateString()}`
                    : "Not yet synced"}
                </span>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleSync(channel)}
                    disabled={syncingId === channel.id || !channel.enabled}
                    className="rounded bg-neutral-800 px-2 py-1 text-xs font-medium text-neutral-200 hover:bg-neutral-700 hover:text-white disabled:opacity-50 transition-colors"
                  >
                    {syncingId === channel.id ? "Syncing..." : "Sync"}
                  </button>
                  <button
                    onClick={() => handleDelete(channel)}
                    className="rounded px-2 py-1 text-xs font-medium text-neutral-400 hover:text-rose-400 transition-colors"
                    title="Delete channel"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Channel Modal */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4 backdrop-blur-xs">
          <div className="w-full max-w-lg rounded-xl border border-neutral-800 bg-[#171717] p-6 shadow-2xl">
            <div className="flex items-center justify-between border-b border-neutral-800 pb-3 mb-5">
              <h2 className="text-base font-bold text-white">Add Approved YouTube Channel</h2>
              <button
                onClick={() => setModalOpen(false)}
                className="text-neutral-400 hover:text-white text-sm"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateChannel} className="space-y-4">
              {/* Channel Input & Resolve Preview */}
              <div>
                <label className="block text-xs font-medium text-neutral-300 mb-1.5">
                  Channel URL or @Handle <span className="text-[#FF5722]">*</span>
                </label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    required
                    placeholder="@BlackBearForge or https://youtube.com/@..."
                    value={inputQuery}
                    onChange={(e) => {
                      setInputQuery(e.target.value);
                      setResolvedPreview(null);
                    }}
                    className="flex-1 rounded-md border border-neutral-800 bg-[#121212] px-3 py-2 text-sm text-white focus:border-[#FF5722] focus:outline-none placeholder:text-neutral-600"
                  />
                  <button
                    type="button"
                    onClick={handleResolve}
                    disabled={resolving || !inputQuery.trim()}
                    className="rounded-md border border-neutral-700 bg-neutral-800 px-3 py-2 text-xs font-semibold text-neutral-200 hover:bg-neutral-700 disabled:opacity-50 transition-colors"
                  >
                    {resolving ? "Resolving..." : "Inspect"}
                  </button>
                </div>
                <p className="text-[11px] text-neutral-500 mt-1">
                  Inspect to verify channel metadata before registering.
                </p>
              </div>

              {/* Resolved Preview Card */}
              {resolvedPreview && (
                <div className="rounded-lg border border-neutral-800 bg-[#121212] p-3 flex items-center gap-3">
                  <img
                    src={resolvedPreview.thumbnail_url}
                    alt={resolvedPreview.name}
                    className="w-10 h-10 rounded-full border border-neutral-800"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-bold text-white truncate">{resolvedPreview.name}</p>
                    <p className="text-[11px] text-neutral-400 truncate">{resolvedPreview.handle || resolvedPreview.canonical_url}</p>
                  </div>
                  <span className="text-[10px] uppercase font-bold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">
                    Verified
                  </span>
                </div>
              )}

              {/* Priority */}
              <div>
                <label className="block text-xs font-medium text-neutral-300 mb-1.5">
                  Ingestion Priority: {priority}
                </label>
                <input
                  type="range"
                  min="1"
                  max="50"
                  value={priority}
                  onChange={(e) => setPriority(Number(e.target.value))}
                  className="w-full accent-[#FF5722]"
                />
                <div className="flex justify-between text-[10px] text-neutral-500">
                  <span>Standard (1)</span>
                  <span>Recommended (15)</span>
                  <span>High Priority (50)</span>
                </div>
              </div>

              {/* Categories */}
              <div>
                <label className="block text-xs font-medium text-neutral-300 mb-1.5">
                  Categories
                </label>
                <div className="flex flex-wrap gap-1.5">
                  {PRESET_CATEGORIES.map((cat) => {
                    const isSelected = selectedCategories.includes(cat);
                    return (
                      <button
                        key={cat}
                        type="button"
                        onClick={() => toggleCategorySelection(cat)}
                        className={`rounded-full px-2.5 py-1 text-xs font-medium transition-colors ${
                          isSelected
                            ? "bg-[#FF5722] text-white"
                            : "bg-neutral-800 text-neutral-400 hover:text-white"
                        }`}
                      >
                        {cat}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Form Buttons */}
              <div className="flex items-center justify-end gap-3 pt-4 border-t border-neutral-800">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="rounded-md border border-neutral-800 px-4 py-2 text-xs font-medium text-neutral-400 hover:text-white transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={creating || !inputQuery.trim()}
                  className="rounded-md bg-[#FF5722] px-4 py-2 text-xs font-semibold text-white hover:bg-[#F4511E] disabled:opacity-50 transition-colors"
                >
                  {creating ? "Registering..." : "Confirm & Register"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
