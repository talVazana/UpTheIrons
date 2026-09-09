import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Forge Videos — Blacksmith Knight",
  description: "Curated blacksmithing and bladesmithing videos collected from trusted user-managed channels.",
};

export default function VideosPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="border-b border-neutral-800 pb-6 mb-8">
        <span className="inline-block text-xs font-semibold uppercase tracking-wider text-[#FF5722] bg-[#FF5722]/10 px-3 py-1 rounded-full mb-3">
          Curated Stream
        </span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Curated Forge Videos
        </h1>
        <p className="text-neutral-400 mt-2 max-w-2xl text-base sm:text-lg">
          Predictable, high-quality video library collected exclusively from user-approved YouTube craftsman channels.
        </p>
      </div>

      <div className="rounded-xl border border-neutral-800 bg-[#171717] p-8 text-center max-w-xl mx-auto">
        <div className="w-12 h-12 rounded-full bg-[#FF5722]/10 text-[#FF5722] flex items-center justify-center mx-auto mb-4 font-bold text-xl">
          &#9658;
        </div>
        <h2 className="text-xl font-bold text-white mb-2">Controlled Channel Pipeline</h2>
        <p className="text-sm text-neutral-400 mb-6">
          No open-web crawling. Content enters strictly through user-approved YouTube channels. Manage your channel registry and review ingestion status.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link
            href="/videos/channels"
            className="rounded-md bg-[#FF5722] px-4 py-2 text-xs font-semibold text-white shadow hover:bg-[#F4511E] transition-colors"
          >
            Manage Approved Channels &rarr;
          </Link>
          <Link
            href="/sources"
            className="rounded-md border border-neutral-800 bg-neutral-900 px-4 py-2 text-xs font-medium text-neutral-300 hover:text-white transition-colors"
          >
            View Full Source Registry
          </Link>
        </div>
      </div>
    </div>
  );
}
