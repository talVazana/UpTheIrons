"use client";

import { useEffect, useState, useTransition } from "react";
import Link from "next/link";
import {
  fetchRules,
  fetchRuleDetail,
  reloadRules,
  validateContentAgainstRules,
  RuleSummaryItem,
  RuleDocumentItem,
  ContentValidationResponse,
} from "@/lib/api";

const RULE_ICONS: Record<string, string> = {
  mission: "🛡️",
  rules: "📜",
  content_rules: "⚖️",
  safety_rules: "🦺",
  source_rules: "📡",
  product_rules: "🔨",
  metallurgy_rules: "🔬",
  editorial_style: "✒️",
};

export default function RulesPage() {
  const [ruleSummaries, setRuleSummaries] = useState<RuleSummaryItem[]>([]);
  const [selectedRuleId, setSelectedRuleId] = useState<string>("mission");
  const [activeRuleDoc, setActiveRuleDoc] = useState<RuleDocumentItem | null>(null);
  const [loadingRules, setLoadingRules] = useState(true);
  const [loadingDoc, setLoadingDoc] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Active view mode: "reader" or "testbed"
  const [activeTab, setActiveTab] = useState<"reader" | "testbed">("reader");

  // Reload state
  const [isReloading, startReload] = useTransition();
  const [reloadFeedback, setReloadFeedback] = useState<string | null>(null);

  // Testbed state
  const [testTitle, setTestTitle] = useState("Forging an S-Hook from 3/8 Inch Mild Steel");
  const [testText, setTestText] = useState(
    "Beginner taper forging, scroll forming on anvil horn, and quenching in water. Wear ANSI Z87.1 eye protection."
  );
  const [isValidating, startValidate] = useTransition();
  const [validationResult, setValidationResult] = useState<ContentValidationResponse | null>(null);

  const loadAllRules = async () => {
    setLoadingRules(true);
    setError(null);
    try {
      const summaries = await fetchRules();
      setRuleSummaries(summaries);
      if (summaries.length > 0 && !selectedRuleId) {
        setSelectedRuleId(summaries[0].id);
      }
    } catch (err: any) {
      setError(err?.message || "Failed loading rule documents from backend.");
    } finally {
      setLoadingRules(false);
    }
  };

  const loadRuleDetail = async (id: string) => {
    setLoadingDoc(true);
    try {
      const doc = await fetchRuleDetail(id);
      setActiveRuleDoc(doc);
    } catch (err: any) {
      setError(`Failed loading rule '${id}': ${err.message}`);
    } finally {
      setLoadingDoc(false);
    }
  };

  useEffect(() => {
    loadAllRules();
  }, []);

  useEffect(() => {
    if (selectedRuleId) {
      loadRuleDetail(selectedRuleId);
    }
  }, [selectedRuleId]);

  const handleReload = () => {
    startReload(async () => {
      setReloadFeedback("Reloading rules from disk...");
      try {
        const fresh = await reloadRules();
        setRuleSummaries(fresh);
        if (selectedRuleId) {
          await loadRuleDetail(selectedRuleId);
        }
        setReloadFeedback(`Reloaded ${fresh.length} rule documents successfully!`);
      } catch (err: any) {
        setReloadFeedback(`Reload failed: ${err.message}`);
      }
    });
  };

  const handleRunValidation = (e: React.FormEvent) => {
    e.preventDefault();
    if (!testTitle.trim() || !testText.trim()) return;

    startValidate(async () => {
      try {
        const res = await validateContentAgainstRules({
          title: testTitle,
          text: testText,
        });
        setValidationResult(res);
      } catch (err: any) {
        alert(`Validation error: ${err.message}`);
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
              Codex &amp; Standards
            </span>
            <span className="text-xs text-neutral-400 bg-neutral-900 border border-neutral-800 px-2.5 py-0.5 rounded">
              Master Spec Section 30 &bull; Modular Markdown Rules
            </span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Rules, Editorial &amp; Safety Codex
          </h1>
          <p className="text-neutral-400 mt-2 max-w-2xl text-sm sm:text-base">
            Explicit craft principles governing content inclusion, safety verification, metallurgical accuracy, and zero-commercial bias.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => setActiveTab(activeTab === "reader" ? "testbed" : "reader")}
            className={`rounded-lg px-3.5 py-2 text-xs font-semibold transition-all flex items-center gap-2 ${
              activeTab === "testbed"
                ? "bg-purple-600 text-white shadow-lg shadow-purple-600/20"
                : "border border-neutral-700 bg-neutral-800 text-neutral-200 hover:bg-neutral-700 hover:text-white"
            }`}
          >
            <span>⚖️</span>
            {activeTab === "testbed" ? "View Rulebook" : "Rule Validator Testbed"}
          </button>

          <button
            type="button"
            onClick={handleReload}
            disabled={isReloading}
            className="rounded-lg border border-neutral-700 bg-neutral-800 hover:bg-neutral-700 px-3.5 py-2 text-xs font-semibold text-neutral-200 hover:text-white disabled:opacity-50 transition-all flex items-center gap-2"
          >
            {isReloading ? "Reloading..." : "↻ Reload from Disk"}
          </button>
        </div>
      </div>

      {/* Reload Feedback */}
      {reloadFeedback && (
        <div className="mb-6 rounded-lg border border-[#FF5722]/30 bg-[#FF5722]/10 p-3 text-xs text-[#FF8A65] flex items-center justify-between">
          <span>{reloadFeedback}</span>
          <button
            type="button"
            onClick={() => setReloadFeedback(null)}
            className="text-neutral-400 hover:text-white ml-4"
          >
            &times;
          </button>
        </div>
      )}

      {/* Main View Mode */}
      {activeTab === "testbed" ? (
        /* Testbed Interactive Mode */
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
            <h2 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
              <span>⚖️</span> Content Compliance Tester
            </h2>
            <p className="text-xs text-neutral-400 mb-6 leading-relaxed">
              Input sample draft text or video descriptions to test them deterministically against our safety rules, anti-spam filters, and craft relevance scoring.
            </p>

            <form onSubmit={handleRunValidation} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-neutral-300 mb-1">
                  Content Title
                </label>
                <input
                  type="text"
                  value={testTitle}
                  onChange={(e) => setTestTitle(e.target.value)}
                  className="w-full rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-sm text-white focus:border-[#FF5722] focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-neutral-300 mb-1">
                  Content Body / Transcript / Notes
                </label>
                <textarea
                  rows={6}
                  value={testText}
                  onChange={(e) => setTestText(e.target.value)}
                  className="w-full rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-sm text-white focus:border-[#FF5722] focus:outline-none font-mono text-xs"
                  required
                />
              </div>

              <div className="flex gap-2 pt-2">
                <button
                  type="submit"
                  disabled={isValidating}
                  className="rounded-lg bg-[#FF5722] px-5 py-2 text-xs font-semibold text-white shadow hover:bg-[#F4511E] disabled:opacity-50 transition-all flex items-center gap-2"
                >
                  {isValidating ? "Validating..." : "Evaluate Against Codex"}
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setTestTitle("Forging a Poker from Galvanized Pipe");
                    setTestText("Tossing a zinc-plated pipe into the coal forge without any acid soak or respirator.");
                  }}
                  className="rounded-lg border border-neutral-700 bg-neutral-800 px-3 py-2 text-xs text-neutral-300 hover:text-white"
                >
                  Load Hazard Example
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setTestTitle("Insane Miracle Blade 50% Off");
                    setTestText("You won't believe how sharp this unbreakable knife is! Use promo code KNIGHT50 to order now!");
                  }}
                  className="rounded-lg border border-neutral-700 bg-neutral-800 px-3 py-2 text-xs text-neutral-300 hover:text-white"
                >
                  Load Spam Example
                </button>
              </div>
            </form>
          </div>

          {/* Validation Result Box */}
          <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
            <h2 className="text-lg font-bold text-white mb-4">Compliance Verdict</h2>

            {validationResult ? (
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                      validationResult.valid
                        ? "bg-emerald-950/70 border border-emerald-800 text-emerald-300"
                        : "bg-red-950/70 border border-red-800 text-red-300"
                    }`}
                  >
                    {validationResult.valid ? "✓ Approved for Vault" : "✕ Flagged for Review"}
                  </span>

                  <span className="text-xs text-neutral-400">
                    Suggested Status:{" "}
                    <strong className="text-white capitalize">{validationResult.suggested_status}</strong>
                  </span>

                  <span className="ml-auto text-xs text-neutral-400">
                    Craft Score:{" "}
                    <strong className="text-[#FF8A65]">
                      {Math.round(validationResult.relevance_score * 100)}%
                    </strong>
                  </span>
                </div>

                {/* Issues List */}
                {validationResult.issues.length > 0 ? (
                  <div className="space-y-2">
                    <p className="text-xs font-semibold text-neutral-300">Violations &amp; Warnings:</p>
                    {validationResult.issues.map((issue, idx) => (
                      <div
                        key={idx}
                        className={`rounded-lg p-3 text-xs border ${
                          issue.severity === "error"
                            ? "bg-red-950/20 border-red-900/50 text-red-300"
                            : "bg-amber-950/20 border-amber-900/50 text-amber-300"
                        }`}
                      >
                        <div className="font-bold uppercase text-[10px] mb-1">
                          [{issue.severity}] {issue.rule_category}
                        </div>
                        <p>{issue.message}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="rounded-lg bg-emerald-950/20 border border-emerald-900/50 p-4 text-xs text-emerald-300">
                    ✓ Clean craft submission. Zero safety violations, marketing spam, or clickbait hype detected.
                  </div>
                )}

                {/* Keywords Found */}
                <div>
                  <p className="text-xs font-semibold text-neutral-400 mb-2">Recognized Craft Elements:</p>
                  <div className="flex flex-wrap gap-1.5">
                    {validationResult.craft_keywords_found.map((kw) => (
                      <span
                        key={kw}
                        className="rounded bg-neutral-800 border border-neutral-700 px-2 py-0.5 text-[11px] text-neutral-300 font-mono"
                      >
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-64 flex flex-col items-center justify-center text-center text-neutral-500">
                <span className="text-3xl mb-2">⚖️</span>
                <p className="text-xs">Run an evaluation on the left to see safety and policy analysis.</p>
              </div>
            )}
          </div>
        </div>
      ) : (
        /* Codex Reader Mode */
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Rules Sidebar Pills */}
          <div className="lg:col-span-1 space-y-2">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-3">
              Master Rule Files ({ruleSummaries.length})
            </h3>
            {loadingRules ? (
              <div className="space-y-2 animate-pulse">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                  <div key={i} className="h-10 bg-neutral-850 rounded-lg" />
                ))}
              </div>
            ) : (
              ruleSummaries.map((rule) => {
                const icon = RULE_ICONS[rule.id] || "📄";
                const isSelected = selectedRuleId === rule.id;

                return (
                  <button
                    key={rule.id}
                    type="button"
                    onClick={() => setSelectedRuleId(rule.id)}
                    className={`w-full text-left p-3 rounded-xl text-xs font-medium transition-all flex items-start gap-3 ${
                      isSelected
                        ? "bg-[#FF5722] text-white shadow-md shadow-[#FF5722]/20"
                        : "bg-[#181818] text-neutral-300 hover:bg-neutral-800 border border-neutral-800 hover:border-neutral-700"
                    }`}
                  >
                    <span className="text-base">{icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="font-semibold truncate">{rule.title}</div>
                      <div
                        className={`text-[10px] mt-0.5 truncate ${
                          isSelected ? "text-orange-100" : "text-neutral-500"
                        }`}
                      >
                        {rule.filename} &bull; {rule.section_count} sections
                      </div>
                    </div>
                  </button>
                );
              })
            )}
          </div>

          {/* Rule Content Reader */}
          <div className="lg:col-span-3 rounded-2xl border border-neutral-800 bg-[#171717] p-6 sm:p-8">
            {loadingDoc ? (
              <div className="space-y-4 animate-pulse">
                <div className="h-8 bg-neutral-800 rounded w-1/3 mb-6" />
                <div className="h-24 bg-neutral-800 rounded" />
                <div className="h-40 bg-neutral-800 rounded" />
              </div>
            ) : activeRuleDoc ? (
              <div className="space-y-8">
                {/* Rule Title & Overview */}
                <div className="border-b border-neutral-800 pb-6">
                  <div className="flex items-center gap-2 text-xs text-[#FF8A65] mb-2 font-mono">
                    <span>{RULE_ICONS[activeRuleDoc.id] || "📄"}</span>
                    <span>config/{activeRuleDoc.filename}</span>
                  </div>
                  <h2 className="text-2xl font-extrabold text-white tracking-tight">
                    {activeRuleDoc.title}
                  </h2>
                  {activeRuleDoc.description && (
                    <p className="text-sm text-neutral-400 mt-2 leading-relaxed">
                      {activeRuleDoc.description}
                    </p>
                  )}
                </div>

                {/* Parsed Sections */}
                <div className="space-y-6">
                  {activeRuleDoc.sections.map((sec, idx) => (
                    <div
                      key={idx}
                      className="rounded-xl border border-neutral-800/80 bg-[#121212] p-5 hover:border-neutral-700 transition-colors"
                    >
                      <h3 className="text-base font-bold text-white mb-3 flex items-center gap-2">
                        <span className="text-[#FF5722] text-sm">&bull;</span>
                        {sec.title}
                      </h3>
                      <div className="text-xs text-neutral-300 leading-relaxed whitespace-pre-line font-sans">
                        {sec.content}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="p-12 text-center text-neutral-500">
                Select a rule file on the left to view its governing directives.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
