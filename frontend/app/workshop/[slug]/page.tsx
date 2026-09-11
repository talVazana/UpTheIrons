import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { fetchToolBySlug } from "@/lib/api";
import ToolSpecsGrid from "@/components/tools/ToolSpecsGrid";
import ToolSafetyNotice from "@/components/tools/ToolSafetyNotice";
import MaintenanceGuide from "@/components/tools/MaintenanceGuide";
import DiyAlternativesCard from "@/components/tools/DiyAlternativesCard";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  try {
    const tool = await fetchToolBySlug(slug);
    return {
      title: `${tool.title} — Workshop Guide — Kiko's BlackSmith Heaven`,
      description: tool.summary,
    };
  } catch {
    return {
      title: "Workshop Tool Guide — Kiko's BlackSmith Heaven",
      description: "Technical tool specifications and safety guide.",
    };
  }
}

export default async function ToolDetailPage({ params }: PageProps) {
  const { slug } = await params;

  let tool;
  try {
    tool = await fetchToolBySlug(slug);
  } catch (err) {
    console.error("Failed fetching tool:", err);
    notFound();
  }

  const meta = tool.metadata;

  const categoryConfigs: Record<
    string,
    { label: string; badgeClass: string; icon: string }
  > = {
    forging: {
      label: "Forging Tool",
      badgeClass: "bg-[#FF5722]/10 text-[#FF8A65] border-[#FF5722]/30",
      icon: "⚒️",
    },
    heating: {
      label: "Heating & Fire",
      badgeClass: "bg-amber-500/10 text-amber-400 border-amber-500/30",
      icon: "🔥",
    },
    grinding: {
      label: "Grinding & Abrasive",
      badgeClass: "bg-sky-500/10 text-sky-400 border-sky-500/30",
      icon: "⚡",
    },
    finishing: {
      label: "Finishing & Polish",
      badgeClass: "bg-purple-500/10 text-purple-400 border-purple-500/30",
      icon: "✨",
    },
    infrastructure: {
      label: "Infrastructure",
      badgeClass: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
      icon: "🏛️",
    },
  };

  const cat = categoryConfigs[meta.tool_category || "forging"] || {
    label: (meta.tool_category || "Tool").toUpperCase(),
    badgeClass: "bg-neutral-800 text-neutral-300 border-neutral-700",
    icon: "🔧",
  };

  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Breadcrumb */}
      <nav className="mb-6 flex items-center gap-2 text-xs font-mono text-neutral-500">
        <Link href="/workshop" className="hover:text-white transition-colors">
          Workshop Knowledge
        </Link>
        <span>/</span>
        <span className="text-neutral-400">{cat.label}</span>
        <span>/</span>
        <span className="text-[#FF8A65] font-semibold">{tool.title}</span>
      </nav>

      {/* Hero Dossier */}
      <div className="rounded-2xl border border-neutral-800 bg-[#161616] p-6 sm:p-8 mb-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 h-48 w-48 bg-[#FF5722]/5 blur-3xl pointer-events-none rounded-full" />

        <div className="flex flex-wrap items-center gap-2 mb-3">
          <span
            className={`inline-flex items-center gap-1.5 rounded-md border px-2.5 py-0.5 text-xs font-mono font-medium uppercase tracking-wider ${cat.badgeClass}`}
          >
            <span>{cat.icon}</span>
            <span>{cat.label}</span>
          </span>

          {meta.beginner_friendly ? (
            <span className="inline-flex items-center gap-1 rounded-md border border-emerald-500/30 bg-emerald-500/10 px-2.5 py-0.5 text-xs font-mono text-emerald-400">
              ✓ Beginner Friendly
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 rounded-md border border-amber-500/30 bg-amber-500/10 px-2.5 py-0.5 text-xs font-mono text-amber-400">
              ⚠ Advanced Equipment
            </span>
          )}

          {meta.diy_buildable && (
            <span className="inline-flex items-center rounded-md border border-neutral-700 bg-neutral-800 px-2.5 py-0.5 text-xs font-mono text-neutral-300">
              DIY Forgeable / Buildable
            </span>
          )}
        </div>

        <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
          {tool.title}
        </h1>

        <p className="text-sm sm:text-base text-neutral-300 mt-4 leading-relaxed max-w-3xl">
          {tool.summary}
        </p>

        {/* Primary Purpose Card */}
        <div className="mt-6 rounded-xl border border-neutral-800/80 bg-neutral-900/60 p-4">
          <span className="text-[10px] font-mono uppercase tracking-wider text-[#FF8A65] block mb-1">
            Primary Workshop Purpose
          </span>
          <p className="text-xs sm:text-sm text-neutral-200 leading-relaxed font-sans">
            {meta.primary_purpose}
          </p>
        </div>
      </div>

      {/* Main Content Sections */}
      <div className="space-y-8">
        {/* Selection Criteria Checklist */}
        {meta.selection_criteria && meta.selection_criteria.length > 0 && (
          <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
            <h3 className="text-lg font-bold text-white flex items-center gap-2 mb-4 border-b border-neutral-800/80 pb-3">
              <span className="text-[#FF5722]">🔎</span> Selection &amp; Buying Criteria
            </h3>
            <p className="text-xs text-neutral-400 mb-4">
              What to inspect before purchasing, salvaging, or building this tool:
            </p>
            <ul className="space-y-2.5 text-xs text-neutral-200">
              {meta.selection_criteria.map((criterion, idx) => (
                <li
                  key={idx}
                  className="flex items-start gap-2.5 rounded-lg border border-neutral-850 bg-neutral-900/40 p-3"
                >
                  <span className="text-emerald-400 font-bold mt-0.5">✓</span>
                  <span>{criterion}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Beginner Guidance Callout */}
        {meta.beginner_guidance && (
          <div className="rounded-xl border border-emerald-500/20 bg-emerald-950/20 p-6">
            <h3 className="text-base font-bold text-emerald-300 flex items-center gap-2 mb-2">
              <span>💡</span> Apprentice Advice &amp; Beginner Traps
            </h3>
            <p className="text-xs sm:text-sm text-neutral-200 leading-relaxed font-sans">
              {meta.beginner_guidance}
            </p>
          </div>
        )}

        {/* Specifications Grid */}
        <ToolSpecsGrid specifications={meta.specifications} toolName={tool.title} />

        {/* Safety Protocols (Milestone 18.07) */}
        <ToolSafetyNotice safetyPrecautions={meta.safety_precautions} toolName={tool.title} />

        {/* Maintenance Guide */}
        <MaintenanceGuide
          maintenanceProtocols={meta.maintenance_protocols}
          toolName={tool.title}
        />

        {/* DIY Alternatives */}
        <DiyAlternativesCard
          diyAlternatives={meta.diy_alternatives}
          diyBuildable={meta.diy_buildable}
          toolName={tool.title}
        />

        {/* Related Tools (Milestone 18.08) */}
        {meta.related_tools && meta.related_tools.length > 0 && (
          <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
            <h3 className="text-base font-bold text-white flex items-center gap-2 mb-4 border-b border-neutral-800/80 pb-3">
              <span className="text-[#FF5722]">🔗</span> Related Workshop Tools &amp; Equipment
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {meta.related_tools.map((rel, idx) => (
                <Link
                  key={idx}
                  href={`/workshop/${rel.slug}`}
                  className="group flex items-center justify-between rounded-lg border border-neutral-800 bg-neutral-900/60 p-3 hover:border-[#FF5722]/40 transition-colors"
                >
                  <div>
                    <span className="text-xs font-bold text-white group-hover:text-[#FF8A65] transition-colors block">
                      {rel.title}
                    </span>
                    <span className="text-[10px] font-mono text-neutral-500 capitalize">
                      {rel.relationship.replace(/_/g, " ")}
                    </span>
                  </div>
                  <span className="text-xs text-[#FF5722] font-mono font-bold group-hover:translate-x-0.5 transition-transform">
                    →
                  </span>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Citations & Navigation Footer */}
        <div className="rounded-xl border border-neutral-800 bg-neutral-900/60 p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs font-mono">
          <div>
            <span className="text-neutral-500 uppercase text-[10px] block">
              Reference Citation
            </span>
            <p className="text-neutral-300 mt-0.5 font-medium">
              {meta.source_references?.[0]?.title
                ? `${meta.source_references[0].title} — ${meta.source_references[0].author || "Guild Master"}`
                : "Kiko's BlackSmith Heaven Workshop Standard & Tooling Reference"}
            </p>
          </div>
          <Link
            href="/workshop"
            className="shrink-0 rounded-lg border border-neutral-700 bg-neutral-800 px-3.5 py-1.5 text-neutral-300 hover:border-neutral-600 hover:text-white transition-colors"
          >
            ← Back to Workshop Hub
          </Link>
        </div>
      </div>
    </div>
  );
}
