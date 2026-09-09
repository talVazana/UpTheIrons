import Link from "next/link";
import { notFound } from "next/navigation";
import { fetchGuideBySlug, GuideItem } from "@/lib/api";
import TrustBadge from "@/components/guides/TrustBadge";
import SafetySection from "@/components/guides/SafetySection";
import SourceReferencesList from "@/components/guides/SourceReferencesList";
import RelatedContentSection from "@/components/guides/RelatedContentSection";
import MarkdownRenderer from "@/components/guides/MarkdownRenderer";

interface GuideDetailPageProps {
  params: Promise<{ slug: string }>;
}

export default async function GuideDetailPage({ params }: GuideDetailPageProps) {
  const { slug } = await params;

  let guide: GuideItem;
  try {
    guide = await fetchGuideBySlug(slug);
  } catch (err) {
    notFound();
  }

  const meta = guide.metadata || {
    reading_time_minutes: 5,
    trust_label: "craft_practice",
    author: "Blacksmith Knight Guild",
    version: "1.0",
    content_markdown: "",
    source_references: [],
    safety_precautions: [],
    related_content: [],
  };

  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Breadcrumb Navigation */}
      <nav aria-label="Breadcrumb" className="mb-8 flex items-center gap-2 text-xs text-neutral-400">
        <Link href="/" className="hover:text-white transition-colors">
          Forge
        </Link>
        <span>/</span>
        <Link href="/guides" className="hover:text-white transition-colors">
          Knowledge Library
        </Link>
        <span>/</span>
        <span className="text-[#FF8A65] truncate max-w-xs">{guide.title}</span>
      </nav>

      {/* Guide Header */}
      <header className="border-b border-neutral-800 pb-8 mb-8">
        <div className="flex flex-wrap items-center gap-2.5 mb-4">
          <TrustBadge label={meta.trust_label || "craft_practice"} size="md" />

          {guide.difficulty && (
            <span className="rounded-md border border-neutral-700 bg-neutral-900 px-2.5 py-1 text-xs font-mono uppercase tracking-wider font-semibold text-neutral-300">
              {guide.difficulty}
            </span>
          )}

          <span className="rounded-md border border-neutral-800 bg-neutral-900/60 px-2.5 py-1 text-xs font-mono text-neutral-400">
            ⏱️ {meta.reading_time_minutes} min read
          </span>

          <span className="text-xs text-neutral-500 ml-auto hidden sm:inline font-mono">
            Version {meta.version || "1.0"}
          </span>
        </div>

        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight leading-tight">
          {guide.title}
        </h1>

        <p className="mt-4 text-base sm:text-lg text-neutral-300 leading-relaxed max-w-3xl">
          {guide.summary}
        </p>

        {/* Author & Provenance Info */}
        <div className="mt-6 flex flex-wrap items-center gap-4 text-xs text-neutral-400 border-t border-neutral-800/80 pt-4">
          <div className="flex items-center gap-2">
            <span className="h-6 w-6 rounded-full bg-[#FF5722]/20 text-[#FF8A65] flex items-center justify-center font-bold text-xs">
              ⚔️
            </span>
            <span>By <strong className="text-white font-medium">{meta.author || "Guild Master"}</strong></span>
          </div>

          <span>•</span>
          <span>Category: <strong className="text-neutral-200 capitalize">{guide.category}</strong></span>

          {guide.tags && guide.tags.length > 0 && (
            <div className="flex flex-wrap items-center gap-1.5 ml-auto">
              {guide.tags.map((tag, tIdx) => (
                <span
                  key={tIdx}
                  className="rounded bg-neutral-900 border border-neutral-800 px-2 py-0.5 text-[11px] font-mono text-neutral-400"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </header>

      {/* Table of Contents (if present) */}
      {meta.table_of_contents && meta.table_of_contents.length > 0 && (
        <aside aria-label="Table of Contents" className="mb-8 rounded-xl border border-neutral-800 bg-[#151515] p-5 shadow-xs">
          <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-neutral-400 mb-3 flex items-center gap-2">
            <span>📑</span> Quick Navigation
          </h2>
          <nav>
            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              {meta.table_of_contents.map((item, idx) => (
                <li key={idx}>
                  <a
                    href={`#${item.id}`}
                    className="text-neutral-300 hover:text-[#FF8A65] hover:underline flex items-center gap-1.5 transition-colors"
                  >
                    <span className="text-neutral-500 font-mono">&rsaquo;</span>
                    <span>{item.title}</span>
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </aside>
      )}

      {/* Mandatory Safety Section (16.05) */}
      {meta.safety_precautions && meta.safety_precautions.length > 0 && (
        <SafetySection precautions={meta.safety_precautions} />
      )}

      {/* Main Markdown Body (16.03) */}
      <article className="prose prose-invert max-w-none">
        <MarkdownRenderer content={meta.content_markdown || ""} />
      </article>

      {/* Source References (16.04) */}
      {meta.source_references && meta.source_references.length > 0 && (
        <SourceReferencesList references={meta.source_references} />
      )}

      {/* Related Content Links (16.07) */}
      {meta.related_content && meta.related_content.length > 0 && (
        <RelatedContentSection related={meta.related_content} />
      )}

      {/* Back to Top / Library */}
      <div className="mt-12 pt-6 border-t border-neutral-800 flex items-center justify-between">
        <Link
          href="/guides"
          className="inline-flex items-center gap-2 rounded-lg border border-neutral-700 bg-neutral-800 px-4 py-2 text-xs font-medium text-neutral-200 hover:bg-neutral-700 hover:text-white transition-colors"
        >
          &larr; Back to Knowledge Library
        </Link>
      </div>
    </div>
  );
}
