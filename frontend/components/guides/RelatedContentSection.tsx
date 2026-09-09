"use client";

import Link from "next/link";
import { RelatedContentLink, ContentType } from "@/lib/types";

interface RelatedContentSectionProps {
  related: RelatedContentLink[];
}

export default function RelatedContentSection({ related }: RelatedContentSectionProps) {
  if (!related || related.length === 0) return null;

  const getTypeRoute = (type: ContentType | string, slug: string) => {
    switch (type) {
      case "material":
        return `/materials?slug=${encodeURIComponent(slug)}`;
      case "project":
        return `/projects?slug=${encodeURIComponent(slug)}`;
      case "video":
        return `/videos?slug=${encodeURIComponent(slug)}`;
      case "guide":
        return `/guides/${encodeURIComponent(slug)}`;
      case "product":
        return `/tools?slug=${encodeURIComponent(slug)}`;
      default:
        return `/search?q=${encodeURIComponent(slug)}`;
    }
  };

  const getRelationshipBadge = (rel: string) => {
    switch (rel) {
      case "requires_material":
        return { label: "Requires Material", style: "border-sky-500/30 bg-sky-950/40 text-sky-300" };
      case "prerequisite_project":
        return { label: "Core Project", style: "border-emerald-500/30 bg-emerald-950/40 text-emerald-300" };
      case "recommended_video":
        return { label: "Demonstration Video", style: "border-purple-500/30 bg-purple-950/40 text-purple-300" };
      case "related_technique":
      default:
        return { label: "Related Craft", style: "border-[#FF5722]/30 bg-[#FF5722]/10 text-[#FF8A65]" };
    }
  };

  return (
    <section aria-labelledby="related-content-title" className="my-10 border-t border-neutral-800 pt-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-neutral-800 border border-neutral-700 text-neutral-300 text-lg shadow-inner">
          🔗
        </div>
        <div>
          <h2 id="related-content-title" className="text-lg sm:text-xl font-bold text-white tracking-tight">
            Related Forge Knowledge &amp; Projects
          </h2>
          <p className="text-xs text-neutral-400">
            Connected steel alloys, hands-on apprentice projects, and tooling tutorials in the vault.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {related.map((item, idx) => {
          const href = getTypeRoute(item.type, item.slug);
          const badge = getRelationshipBadge(item.relationship);

          return (
            <Link
              key={idx}
              href={href}
              className="group flex flex-col justify-between rounded-xl border border-neutral-800 bg-[#161616] p-4.5 hover:border-[#FF5722]/50 hover:bg-[#1b1b1b] transition-all shadow-xs"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2.5">
                  <span className={`inline-flex items-center rounded px-2 py-0.5 text-[10px] font-mono font-bold uppercase tracking-wider border ${badge.style}`}>
                    {badge.label}
                  </span>
                  <span className="text-[11px] font-mono uppercase text-neutral-500">
                    {item.type}
                  </span>
                </div>

                <h3 className="text-sm font-bold text-white group-hover:text-[#FF8A65] transition-colors leading-snug">
                  {item.title}
                </h3>
              </div>

              <div className="mt-4 pt-2.5 flex items-center text-xs font-semibold text-neutral-400 group-hover:text-white transition-colors">
                <span>Explore in Vault</span>
                <span className="ml-1.5 transition-transform group-hover:translate-x-1">&rarr;</span>
              </div>
            </Link>
          );
        })}
      </div>
    </section>
  );
}
