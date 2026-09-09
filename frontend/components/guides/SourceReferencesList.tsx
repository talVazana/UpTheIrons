"use client";

import { SourceReference } from "@/lib/types";
import TrustBadge from "./TrustBadge";

interface SourceReferencesListProps {
  references: SourceReference[];
}

export default function SourceReferencesList({ references }: SourceReferencesListProps) {
  if (!references || references.length === 0) return null;

  return (
    <section aria-labelledby="source-references-title" className="my-10 border-t border-neutral-800 pt-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-neutral-800 border border-neutral-700 text-neutral-300 text-lg shadow-inner">
          📖
        </div>
        <div>
          <h2 id="source-references-title" className="text-lg sm:text-xl font-bold text-white tracking-tight">
            Academic &amp; Guild Source References
          </h2>
          <p className="text-xs text-neutral-400">
            Literature citations, historical records, and metallurgical handbooks backing this guide.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {references.map((ref, idx) => (
          <div
            key={idx}
            className="flex flex-col justify-between rounded-xl border border-neutral-800 bg-[#171717] p-4.5 hover:border-neutral-700 transition-all shadow-xs"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                {ref.citation_key ? (
                  <span className="font-mono text-xs font-bold text-[#FF8A65] bg-[#FF5722]/10 border border-[#FF5722]/30 px-2 py-0.5 rounded">
                    [{ref.citation_key}]
                  </span>
                ) : (
                  <span className="font-mono text-xs text-neutral-500">#{idx + 1}</span>
                )}

                {ref.trust_label && (
                  <TrustBadge label={ref.trust_label} size="sm" />
                )}
              </div>

              <h3 className="text-sm font-semibold text-white leading-snug">
                {ref.title}
              </h3>

              <div className="text-xs text-neutral-400 mt-2 space-y-0.5">
                {ref.author && (
                  <p>
                    <span className="text-neutral-500">Author:</span> {ref.author}
                  </p>
                )}
                {(ref.publication || ref.year) && (
                  <p>
                    <span className="text-neutral-500">Published:</span>{" "}
                    {[ref.publication, ref.year].filter(Boolean).join(", ")}
                  </p>
                )}
              </div>
            </div>

            {ref.url && (
              <div className="mt-4 pt-3 border-t border-neutral-800/80">
                <a
                  href={ref.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs font-medium text-[#FF8A65] hover:text-[#FF5722] hover:underline"
                >
                  <span>View Source Reference</span>
                  <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
