"use client";

import React, { useId } from "react";

interface MarkdownRendererProps {
  content: string;
}

export default function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const componentId = useId();
  if (!content) return null;

  const lines = content.split("\n");
  const renderedElements: React.ReactNode[] = [];

  let i = 0;
  while (i < lines.length) {
    const line = lines[i];

    // Fenced code blocks
    if (line.trim().startsWith("```")) {
      const codeLines: string[] = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith("```")) {
        codeLines.push(lines[i]);
        i++;
      }
      i++; // skip closing ```
      renderedElements.push(
        <pre
          key={`code-${i}-${componentId}`}
          className="my-6 overflow-x-auto rounded-xl border border-neutral-800 bg-[#0d0d0d] p-4 text-xs sm:text-sm font-mono text-neutral-300 shadow-inner"
        >
          <code>{codeLines.join("\n")}</code>
        </pre>
      );
      continue;
    }

    // Horizontal Rule
    if (line.trim() === "---" || line.trim() === "***" || line.trim() === "___") {
      renderedElements.push(
        <hr key={`hr-${i}-${componentId}`} className="my-8 border-t border-neutral-800" />
      );
      i++;
      continue;
    }

    // Headings
    if (line.startsWith("# ")) {
      renderedElements.push(
        <h1
          key={`h1-${i}-${componentId}`}
          className="mt-8 mb-4 text-2xl sm:text-3xl font-black text-white tracking-tight"
        >
          {parseInlineText(line.substring(2))}
        </h1>
      );
      i++;
      continue;
    }

    if (line.startsWith("## ")) {
      const text = line.substring(3).trim();
      const slug = text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
      renderedElements.push(
        <h2
          key={`h2-${i}-${componentId}`}
          id={slug}
          className="mt-10 mb-4 scroll-mt-24 text-xl sm:text-2xl font-extrabold text-white tracking-tight border-b border-neutral-800 pb-2 flex items-center justify-between group"
        >
          <span>{parseInlineText(text)}</span>
          <a
            href={`#${slug}`}
            className="text-neutral-600 hover:text-[#FF5722] opacity-0 group-hover:opacity-100 transition-opacity text-sm ml-2 font-mono"
            aria-label={`Link to ${text}`}
          >
            #
          </a>
        </h2>
      );
      i++;
      continue;
    }

    if (line.startsWith("### ")) {
      renderedElements.push(
        <h3
          key={`h3-${i}-${componentId}`}
          className="mt-6 mb-3 text-base sm:text-lg font-bold text-neutral-100 tracking-tight"
        >
          {parseInlineText(line.substring(4))}
        </h3>
      );
      i++;
      continue;
    }

    // Callout blocks (> [!NOTE], > [!WARNING], > [!TIP], > [!CAUTION])
    if (line.startsWith("> [!")) {
      const typeMatch = line.match(/^>\s*\[!(NOTE|WARNING|TIP|CAUTION)\]/i);
      const alertType = (typeMatch ? typeMatch[1].toUpperCase() : "NOTE") as
        | "NOTE"
        | "WARNING"
        | "TIP"
        | "CAUTION";
      const calloutLines: string[] = [];
      i++;
      while (i < lines.length && lines[i].startsWith(">")) {
        calloutLines.push(lines[i].replace(/^>\s?/, ""));
        i++;
      }

      const alertStyles = {
        NOTE: {
          border: "border-sky-500/40 bg-sky-950/20",
          titleColor: "text-sky-300",
          icon: "ℹ️",
          label: "Forge Note",
        },
        TIP: {
          border: "border-emerald-500/40 bg-emerald-950/20",
          titleColor: "text-emerald-300",
          icon: "💡",
          label: "Workshop Tip",
        },
        WARNING: {
          border: "border-[#FF5722]/50 bg-[#FF5722]/10",
          titleColor: "text-[#FF8A65]",
          icon: "⚠️",
          label: "Important Warning",
        },
        CAUTION: {
          border: "border-red-600/50 bg-red-950/30",
          titleColor: "text-red-300",
          icon: "🛑",
          label: "Critical Caution",
        },
      }[alertType];

      renderedElements.push(
        <aside
          key={`callout-${i}-${componentId}`}
          className={`my-6 rounded-xl border p-4 sm:p-5 ${alertStyles.border} shadow-sm`}
        >
          <div className={`flex items-center gap-2 font-mono text-xs font-bold uppercase tracking-wider mb-2 ${alertStyles.titleColor}`}>
            <span>{alertStyles.icon}</span>
            <span>{alertStyles.label}</span>
          </div>
          <div className="text-xs sm:text-sm text-neutral-200 leading-relaxed space-y-2">
            {calloutLines.map((cL, cIdx) => (
              <p key={cIdx}>{parseInlineText(cL)}</p>
            ))}
          </div>
        </aside>
      );
      continue;
    }

    // Standard blockquote
    if (line.startsWith("> ")) {
      const quoteLines: string[] = [line.substring(2)];
      i++;
      while (i < lines.length && lines[i].startsWith("> ")) {
        quoteLines.push(lines[i].substring(2));
        i++;
      }
      renderedElements.push(
        <blockquote
          key={`quote-${i}-${componentId}`}
          className="my-4 border-l-4 border-[#FF5722] bg-[#161616] p-4 text-xs sm:text-sm italic text-neutral-300 rounded-r-lg"
        >
          {quoteLines.join(" ")}
        </blockquote>
      );
      continue;
    }

    // Bullet Lists
    if (line.trim().startsWith("- ") || line.trim().startsWith("* ")) {
      const listItems: string[] = [];
      while (
        i < lines.length &&
        (lines[i].trim().startsWith("- ") || lines[i].trim().startsWith("* "))
      ) {
        listItems.push(lines[i].trim().substring(2));
        i++;
      }
      renderedElements.push(
        <ul key={`ul-${i}-${componentId}`} className="my-4 list-disc list-inside space-y-1.5 text-xs sm:text-sm text-neutral-300 pl-2">
          {listItems.map((item, lIdx) => (
            <li key={lIdx} className="leading-relaxed">
              {parseInlineText(item)}
            </li>
          ))}
        </ul>
      );
      continue;
    }

    // Numbered Lists
    if (/^\s*\d+\.\s+/.test(line)) {
      const listItems: string[] = [];
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        listItems.push(lines[i].replace(/^\s*\d+\.\s+/, ""));
        i++;
      }
      renderedElements.push(
        <ol key={`ol-${i}-${componentId}`} className="my-4 list-decimal list-inside space-y-2 text-xs sm:text-sm text-neutral-300 pl-2">
          {listItems.map((item, lIdx) => (
            <li key={lIdx} className="leading-relaxed">
              {parseInlineText(item)}
            </li>
          ))}
        </ol>
      );
      continue;
    }

    // Paragraph
    if (line.trim().length > 0) {
      renderedElements.push(
        <p key={`p-${i}-${componentId}`} className="my-3 text-xs sm:text-base leading-relaxed text-neutral-300">
          {parseInlineText(line)}
        </p>
      );
    }

    i++;
  }

  return <div className="prose-forge font-sans leading-relaxed">{renderedElements}</div>;
}

/**
 * Parses bold (**text**), inline code (`code`), and citation markers ([Citation1998]).
 */
function parseInlineText(text: string): React.ReactNode {
  const parts: React.ReactNode[] = [];
  const regex = /(\*\*[^*]+\*\*|`[^`]+`|\[[A-Za-z0-9_-]+\])/g;

  let lastIdx = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIdx) {
      parts.push(text.substring(lastIdx, match.index));
    }

    const token = match[0];
    if (token.startsWith("**") && token.endsWith("**")) {
      parts.push(
        <strong key={`bold-${match.index}`} className="font-semibold text-white">
          {token.substring(2, token.length - 2)}
        </strong>
      );
    } else if (token.startsWith("`") && token.endsWith("`")) {
      parts.push(
        <code
          key={`code-${match.index}`}
          className="rounded bg-neutral-800 border border-neutral-700 px-1.5 py-0.5 text-xs font-mono text-[#FF8A65]"
        >
          {token.substring(1, token.length - 1)}
        </code>
      );
    } else if (token.startsWith("[") && token.endsWith("]")) {
      parts.push(
        <span
          key={`cite-${match.index}`}
          className="font-mono text-xs font-bold text-[#FF8A65] bg-[#FF5722]/10 border border-[#FF5722]/30 px-1.5 py-0.2 rounded"
        >
          {token}
        </span>
      );
    }

    lastIdx = regex.lastIndex;
  }

  if (lastIdx < text.length) {
    parts.push(text.substring(lastIdx));
  }

  return parts.length === 1 ? parts[0] : parts;
}
