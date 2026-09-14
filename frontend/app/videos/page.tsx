"use client";

import { useEffect, useState, useTransition } from "react";
import Link from "next/link";
import {
  fetchVideos,
  fetchYouTubeChannels,
  syncAllYouTubeChannels,
  addDirectVideo,
  deleteVideo,
  VideoItem,
  YouTubeChannelItem,
} from "@/lib/api";

function formatDuration(seconds?: number): string {
  if (!seconds || seconds <= 0) return "";
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
}

export default function VideosPage() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [channels, setChannels] = useState<YouTubeChannelItem[]>([]);
  const [loading, setLoading] = useState(true);

  // Syncer
  const [isSyncing, startSync] = useTransition();
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);

  // Navigation state
  const [activeGallery, setActiveGallery] = useState<"direct" | string | null>(null);
  
  // Add direct link state
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [linkUrl, setLinkUrl] = useState("");
  const [isAdding, setIsAdding] = useState(false);

  // Guide state
  const [isGuideOpen, setIsGuideOpen] = useState(false);

  // Embed player state
  const [activeVideo, setActiveVideo] = useState<VideoItem | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const [vidRes, chanRes] = await Promise.all([
        fetchVideos({ limit: 100 }),
        fetchYouTubeChannels()
      ]);
      setVideos(vidRes.videos || []);
      setChannels(chanRes.channels || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let isMounted = true;
    const token = localStorage.getItem("admin_token");
    if (token) setIsAdmin(true);

    loadData();
    // Auto-sync
    syncAllYouTubeChannels().catch(() => {});
    return () => { isMounted = false; };
  }, []);

  const handleSyncAll = () => {
    startSync(async () => {
      setSyncFeedback("Syncing channels...");
      try {
        await syncAllYouTubeChannels();
        setSyncFeedback("Sync complete!");
        await loadData();
      } catch (err: any) {
        setSyncFeedback(`Sync failed: ${err.message}`);
      }
    });
  };

  const handleAddDirectLink = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!linkUrl) return;
    setIsAdding(true);
    try {
      const token = localStorage.getItem("admin_token") || "";
      await addDirectVideo({ url_or_id: linkUrl }, token);
      setLinkUrl("");
      setIsAddModalOpen(false);
      await loadData();
    } catch (err: any) {
      alert(err.message);
    } finally {
      setIsAdding(false);
    }
  };

  const handleDeleteVideo = async (vidId: string) => {
    if (!confirm("Remove video?")) return;
    try {
      const token = localStorage.getItem("admin_token") || "";
      await deleteVideo(vidId, token);
      await loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  // Grouping logic
  const directVideos = videos.filter(v => v.metadata?.channel_id === "direct" || v.tags?.includes("direct"));
  const latestDirect = directVideos[0];

  const channelCards = channels.map(ch => {
    const chVideos = videos.filter(v => v.metadata?.channel_id === ch.youtube_channel_id || v.source?.source_id === ch.youtube_channel_id);
    return {
      channel: ch,
      latestVideo: chVideos[0],
      videos: chVideos
    };
  });

  const renderVideoCard = (vid: VideoItem, hideChannelName = false) => {
    const ytId = vid.metadata?.youtube_video_id || vid.id.replace("yt_", "");
    const duration = formatDuration(vid.metadata?.duration_seconds);
    return (
      <div key={vid.id} className="group flex flex-col rounded-xl border border-neutral-800 bg-[#181818] overflow-hidden hover:border-[#FF5722]/40 transition-all shadow-sm">
        <div className="relative aspect-video w-full bg-neutral-900 overflow-hidden cursor-pointer" onClick={() => setActiveVideo(vid)}>
          {vid.image_url ? (
            <img src={vid.image_url} alt={vid.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" loading="lazy" />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-neutral-600">Forge Video</div>
          )}
          {duration && <span className="absolute bottom-2 right-2 rounded bg-black/80 backdrop-blur-xs px-2 py-0.5 text-[10px] font-mono text-white">{duration}</span>}
          <div className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity">
            <div className="w-12 h-12 rounded-full bg-[#FF5722] text-white flex items-center justify-center shadow-lg transform group-hover:scale-110"><span className="ml-0.5 text-lg">&#9658;</span></div>
          </div>
        </div>
        <div className="flex flex-col flex-1 p-4">
          {!hideChannelName && (
            <span className="text-xs font-medium text-[#FF8A65] truncate mb-2">{vid.source?.source_name || vid.metadata?.channel_name || "Direct Link"}</span>
          )}
          <h3 className="text-sm font-bold text-white line-clamp-2 mb-2">{vid.title}</h3>
          <div className="mt-auto pt-3 flex items-center justify-between">
             <a href={`https://www.youtube.com/watch?v=${ytId}`} target="_blank" rel="noopener noreferrer" className="text-xs font-semibold text-[#FF5722] hover:text-[#F4511E]">Watch on YT &rarr;</a>
             {isAdmin && <button onClick={() => handleDeleteVideo(vid.id)} className="text-xs font-semibold text-red-500 hover:text-red-400">Remove</button>}
          </div>
        </div>
      </div>
    );
  };

  if (activeGallery) {
    let galleryTitle = "";
    let galleryVideos: VideoItem[] = [];
    if (activeGallery === "direct") {
      galleryTitle = "Direct Links";
      galleryVideos = directVideos;
    } else {
      const ch = channels.find(c => c.id === activeGallery);
      if (ch) {
        galleryTitle = ch.name;
        galleryVideos = videos.filter(v => v.metadata?.channel_id === ch.youtube_channel_id || v.source?.source_id === ch.youtube_channel_id);
      }
    }

    return (
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
        <button onClick={() => setActiveGallery(null)} className="mb-6 text-sm text-neutral-400 hover:text-white underline">&larr; Back to Galleries</button>
        <div className="flex justify-between items-center mb-8 border-b border-neutral-800 pb-4">
          <h1 className="text-3xl font-bold text-white">{galleryTitle}</h1>
          {activeGallery === "direct" && isAdmin && (
             <button onClick={() => setIsAddModalOpen(true)} className="bg-[#FF5722] text-white px-4 py-2 font-bold text-sm hover:bg-[#F4511E] rounded">
               + Add Direct Link
             </button>
          )}
        </div>
        {galleryVideos.length === 0 ? (
          <p className="text-neutral-400 text-center py-20">No videos in this gallery yet.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {galleryVideos.map(v => renderVideoCard(v, activeGallery !== "direct"))}
          </div>
        )}
        
        {/* Video Player Modal */}
        {activeVideo && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4 backdrop-blur-sm overflow-y-auto py-10" onClick={() => setActiveVideo(null)}>
            <div className="w-full max-w-5xl bg-[#141414] rounded-xl overflow-hidden shadow-2xl relative flex flex-col" onClick={e => e.stopPropagation()}>
              <button onClick={() => setActiveVideo(null)} className="absolute top-4 right-4 z-10 text-white/70 hover:text-white bg-black/50 rounded-full w-10 h-10 flex items-center justify-center backdrop-blur-md">✕</button>
              <div className="w-full aspect-video bg-black relative">
                {activeVideo.metadata?.embed_url ? (
                  <iframe src={`${activeVideo.metadata.embed_url}?autoplay=1`} className="w-full h-full border-0" allow="autoplay; encrypted-media; picture-in-picture" allowFullScreen></iframe>
                ) : (
                  <div className="w-full h-full flex flex-col items-center justify-center text-white">
                    <p>No video source available.</p>
                    {activeVideo.source?.source_url && (
                      <a href={activeVideo.source.source_url} target="_blank" rel="noopener noreferrer" className="mt-4 text-[#FF5722] hover:underline">Watch on YouTube &rarr;</a>
                    )}
                  </div>
                )}
              </div>
              <div className="p-6 border-t border-neutral-800">
                <h2 className="text-xl font-bold text-white mb-2">{activeVideo.title}</h2>
                <p className="text-sm text-neutral-400 mb-4">{activeVideo.summary}</p>
                <div className="flex gap-4 text-xs font-mono text-neutral-500">
                  <span>ID: {activeVideo.id}</span>
                  {activeVideo.source?.source_url && (
                    <a href={activeVideo.source.source_url} target="_blank" rel="noopener noreferrer" className="text-[#FF5722] hover:underline">Open Original Link</a>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
        
        {isAddModalOpen && (
           <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4">
             <div className="bg-neutral-900 border border-neutral-700 p-6 rounded-lg w-full max-w-md">
               <h2 className="text-white font-bold mb-4">Add Direct Link</h2>
               <form onSubmit={handleAddDirectLink} className="flex flex-col gap-4">
                 <input type="text" value={linkUrl} onChange={e => setLinkUrl(e.target.value)} placeholder="YouTube URL" className="w-full bg-black border border-neutral-700 p-2 text-white" />
                 <div className="flex justify-end gap-2">
                   <button type="button" onClick={() => setIsAddModalOpen(false)} className="text-neutral-400 hover:text-white px-3 py-1">Cancel</button>
                   <button type="submit" disabled={isAdding || !linkUrl} className="bg-[#FF5722] text-white px-4 py-1 font-bold rounded hover:bg-[#F4511E] disabled:opacity-50">{isAdding ? "Adding..." : "Add"}</button>
                 </div>
               </form>
             </div>
           </div>
        )}
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-neutral-800 pb-8 mb-8">
        <div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">Curated Forge Videos</h1>
          <p className="text-neutral-400 mt-2 text-sm">Select a gallery to view videos.</p>
        </div>
        {isAdmin && (
          <div className="flex gap-3">
             <button onClick={() => setIsGuideOpen(true)} className="rounded border border-neutral-700 bg-neutral-800 px-3 py-2 text-xs font-semibold text-white hover:bg-neutral-700">
               Page Guide
             </button>
             <Link href="/videos/channels" className="rounded border border-neutral-700 bg-neutral-800 px-3 py-2 text-xs font-semibold text-white hover:bg-neutral-700">
               Manage Channels
             </Link>
             <button onClick={handleSyncAll} disabled={isSyncing} className="rounded bg-[#FF5722] hover:bg-[#F4511E] disabled:opacity-50 px-4 py-2 text-xs font-semibold text-white">
               {isSyncing ? "Syncing..." : "Manual Sync All"}
             </button>
          </div>
        )}
      </div>

      {isGuideOpen && isAdmin && (
        <div className="mb-8 p-6 bg-[#161616] border border-neutral-700 text-sm leading-relaxed space-y-4 rounded-lg shadow-inner relative">
          <button type="button" onClick={() => setIsGuideOpen(false)} className="absolute top-4 right-4 text-neutral-500 hover:text-white text-lg leading-none">✕</button>
          <h2 className="text-xl font-bold text-[#FF5722] mb-4">Videos Page Guide (Admin Only)</h2>
          
          <div className="space-y-4 text-neutral-300">
            <div>
              <h3 className="text-white font-bold text-base mb-1">1. How Things Are Organized (Galleries)</h3>
              <p>The videos are grouped into <strong>Gallery Cards</strong>. The first card is always <strong>Direct Links</strong>, containing individual videos manually added by an admin. The rest of the cards are <strong>YouTube Channels</strong> you have approved. Clicking on any card opens its specific gallery containing all associated videos.</p>
            </div>
            
            <div>
              <h3 className="text-white font-bold text-base mb-1">2. How to Add or Remove a YouTube Channel</h3>
              <p>Click the <strong>Manage Channels</strong> button above to go to the Channels configuration page. There, you can click <strong>+ Add Approved Channel</strong>, enter a YouTube URL or @handle (like <code>@BlackBearForge</code>), and the server will fetch its details and add it. To remove one, click <strong>Delete</strong> on the channel's card on that same management page. Once added, the channel automatically gets its own Gallery Card on this page.</p>
            </div>

            <div>
              <h3 className="text-white font-bold text-base mb-1">3. How to Add or Remove a Specific Video (Direct Links)</h3>
              <p>Click the <strong>Direct Links</strong> gallery card. In the top right of that gallery, click <strong>+ Add Direct Link</strong> and paste the YouTube video URL. It will instantly be added to the Direct Links gallery. To remove <strong>any video</strong> (direct or from a channel), simply open its gallery and click the red <strong>Remove</strong> button under the video card.</p>
            </div>

            <div>
              <h3 className="text-white font-bold text-base mb-1">4. Synchronization & API Keys</h3>
              <p>Every time you load this page, it silently asks YouTube for new videos for all approved channels. You can also force it using the <strong>Manual Sync All</strong> button. <strong>Important:</strong> This requires a valid YouTube API Key. The API Key must be entered and saved in the main <strong>Admin Portal</strong> (where you change your password).</p>
            </div>
          </div>
        </div>
      )}

      {syncFeedback && <div className="mb-6 bg-neutral-800 p-3 text-xs text-white rounded">{syncFeedback}</div>}

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1,2,3].map(i => <div key={i} className="animate-pulse h-64 bg-[#171717] rounded-xl border border-neutral-800" />)}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          
          <div className="group cursor-pointer rounded-xl border border-neutral-700 bg-[#181818] p-5 hover:border-[#FF5722] transition-colors" onClick={() => setActiveGallery("direct")}>
             <div className="text-[#FF5722] font-bold text-lg mb-2">Direct Links</div>
             <p className="text-xs text-neutral-400 mb-4">Standalone videos added by Admin.</p>
             {latestDirect ? (
               <div className="border-t border-neutral-800 pt-4">
                 <p className="text-xs text-neutral-500 mb-1">Latest Upload:</p>
                 <div className="flex items-center gap-3">
                   <div className="w-16 h-10 bg-neutral-900 rounded overflow-hidden flex-shrink-0">
                     {latestDirect.image_url ? <img src={latestDirect.image_url} className="w-full h-full object-cover" /> : null}
                   </div>
                   <p className="text-sm font-semibold text-white line-clamp-2">{latestDirect.title}</p>
                 </div>
               </div>
             ) : (
               <p className="text-sm text-neutral-500 border-t border-neutral-800 pt-4">No direct links uploaded.</p>
             )}
             <div className="mt-4 text-xs font-bold text-[#FF5722] group-hover:underline">Open Gallery &rarr;</div>
          </div>

          {channelCards.map(cc => (
             <div key={cc.channel.id} className="group cursor-pointer rounded-xl border border-neutral-800 bg-[#181818] p-5 hover:border-[#FF5722] transition-colors" onClick={() => setActiveGallery(cc.channel.id)}>
               <div className="flex items-center gap-3 mb-2">
                 {cc.channel.thumbnail_url ? (
                   <img src={cc.channel.thumbnail_url} className="w-8 h-8 rounded-full" />
                 ) : (
                   <div className="w-8 h-8 rounded-full bg-neutral-700"></div>
                 )}
                 <div className="text-white font-bold text-lg truncate">{cc.channel.name}</div>
               </div>
               <p className="text-xs text-neutral-400 mb-4">{cc.videos.length} videos synced</p>
               {cc.latestVideo ? (
                 <div className="border-t border-neutral-800 pt-4">
                   <p className="text-xs text-neutral-500 mb-1">Latest Upload:</p>
                   <div className="flex items-center gap-3">
                     <div className="w-16 h-10 bg-neutral-900 rounded overflow-hidden flex-shrink-0">
                       {cc.latestVideo.image_url ? <img src={cc.latestVideo.image_url} className="w-full h-full object-cover" /> : null}
                     </div>
                     <p className="text-sm font-semibold text-white line-clamp-2">{cc.latestVideo.title}</p>
                   </div>
                 </div>
               ) : (
                 <p className="text-sm text-neutral-500 border-t border-neutral-800 pt-4">No videos found.</p>
               )}
               <div className="mt-4 text-xs font-bold text-[#FF5722] group-hover:underline">Open Gallery &rarr;</div>
             </div>
          ))}

        </div>
      )}
    </div>
  );
}
