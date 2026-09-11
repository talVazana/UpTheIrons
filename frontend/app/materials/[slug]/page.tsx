import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { fetchMaterialBySlug } from "@/lib/api";
import CompositionBreakdown from "@/components/materials/CompositionBreakdown";
import HeatTreatmentProtocol from "@/components/materials/HeatTreatmentProtocol";
import SparkProfileCard from "@/components/materials/SparkProfileCard";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  try {
    const mat = await fetchMaterialBySlug(slug);
    return {
      title: `${mat.title} — Metallurgy Vault — Kiko's BlackSmith Heaven`,
      description: mat.summary,
    };
  } catch {
    return {
      title: `${slug.toUpperCase()} Steel Spec — Kiko's BlackSmith Heaven`,
      description: "Technical metallurgy and heat treatment reference.",
    };
  }
}

export default async function MaterialDetailPage({ params }: PageProps) {
  const { slug } = await params;

  let material;
  try {
    material = await fetchMaterialBySlug(slug);
  } catch (err) {
    console.error("Failed to fetch material:", err);
    notFound();
  }

  const meta = material.metadata;
  const ht = meta.heat_treatment;
  const carbonPct = meta.carbon_pct ?? 0;
  const sourceStandard = meta.source_metadata?.standard || meta.classification;

  // Category styling
  const categoryLabels: Record<string, { label: string; badgeClass: string }> = {
    carbon_steel: {
      label: "Carbon Steel",
      badgeClass: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    },
    tool_steel: {
      label: "Tool Steel",
      badgeClass: "bg-sky-500/10 text-sky-400 border-sky-500/30",
    },
    spring_steel: {
      label: "Spring Steel",
      badgeClass: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    },
    alloy_steel: {
      label: "Alloy Steel",
      badgeClass: "bg-purple-500/10 text-purple-400 border-purple-500/30",
    },
    stainless_steel: {
      label: "Stainless Steel",
      badgeClass: "bg-cyan-500/10 text-cyan-400 border-cyan-500/30",
    },
  };

  const categoryInfo = categoryLabels[meta.steel_category || "carbon_steel"] || {
    label: (meta.steel_category || "Steel").replace(/_/g, " "),
    badgeClass: "bg-neutral-800 text-neutral-300 border-neutral-700",
  };

  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Breadcrumb Navigation */}
      <nav className="mb-6 flex items-center gap-2 text-xs font-mono text-neutral-500">
        <Link href="/materials" className="hover:text-white transition-colors">
          Metallurgy Vault
        </Link>
        <span>/</span>
        <span className="text-neutral-400">{categoryInfo.label}</span>
        <span>/</span>
        <span className="text-[#FF8A65] font-semibold">{material.title}</span>
      </nav>

      {/* Hero Dossier Header */}
      <div className="rounded-2xl border border-neutral-800 bg-[#161616] p-6 sm:p-8 mb-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 h-48 w-48 bg-[#FF5722]/5 blur-3xl pointer-events-none rounded-full" />

        <div className="flex flex-wrap items-center gap-2 mb-3">
          <span
            className={`inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-mono font-medium uppercase tracking-wider ${categoryInfo.badgeClass}`}
          >
            {categoryInfo.label}
          </span>

          {meta.beginner_suitability ? (
            <span className="inline-flex items-center gap-1.5 rounded-md border border-emerald-500/30 bg-emerald-500/10 px-2.5 py-0.5 text-xs font-mono text-emerald-400">
              <span>✓</span> Beginner Suitable
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 rounded-md border border-amber-500/30 bg-amber-500/10 px-2.5 py-0.5 text-xs font-mono text-amber-400">
              <span>⚠</span> Advanced Forging Required
            </span>
          )}

          {meta.confidence_level && (
            <span className="inline-flex items-center gap-1 rounded-md border border-sky-500/30 bg-sky-500/10 px-2 py-0.5 text-xs font-mono text-sky-300">
              <span>⚖</span> Handbook Verified ({Math.round((meta.confidence_score || 0.95) * 100)}%)
            </span>
          )}
        </div>

        <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
          {material.title}
        </h1>
        <p className="text-sm sm:text-base font-mono text-neutral-400 mt-1 mb-4">
          {meta.classification}
        </p>
        <p className="text-sm sm:text-base text-neutral-300 leading-relaxed max-w-3xl">
          {material.summary}
        </p>

        {/* Technical Specification Ribbon */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-neutral-800 font-mono text-xs">
          <div className="rounded-lg border border-neutral-800/80 bg-neutral-900/60 p-3">
            <span className="text-neutral-500 block text-[10px] uppercase">Carbon (C)</span>
            <span className="text-base font-bold text-white mt-0.5 block">
              {carbonPct.toFixed(2)}%
            </span>
          </div>

          <div className="rounded-lg border border-neutral-800/80 bg-neutral-900/60 p-3">
            <span className="text-neutral-500 block text-[10px] uppercase">Forging Range</span>
            <span className="text-sm font-semibold text-neutral-200 mt-0.5 block truncate">
              {meta.forging_temp_range_f || "1650°F – 2050°F"}
            </span>
          </div>

          <div className="rounded-lg border border-neutral-800/80 bg-neutral-900/60 p-3">
            <span className="text-neutral-500 block text-[10px] uppercase">Hardening Temp</span>
            <span className="text-sm font-semibold text-[#FF8A65] mt-0.5 block">
              {ht?.hardening_temp_f ? `${ht.hardening_temp_f}°F` : "1475°F – 1525°F"}
            </span>
          </div>

          <div className="rounded-lg border border-neutral-800/80 bg-neutral-900/60 p-3">
            <span className="text-neutral-500 block text-[10px] uppercase">Target Hardness</span>
            <span className="text-sm font-semibold text-emerald-400 mt-0.5 block">
              {ht?.target_hardness_hrc || "58–61 HRC"}
            </span>
          </div>
        </div>
      </div>

      {/* Main Dossier Grid */}
      <div className="space-y-8">
        {/* Chemical Composition & Alloying Metallurgy */}
        <CompositionBreakdown
          carbonPct={carbonPct}
          alloyingElements={meta.alloying_elements || {}}
          sourceStandard={sourceStandard}
        />

        {/* Heat Treatment Sequence */}
        <HeatTreatmentProtocol
          heatTreatment={meta.heat_treatment}
          steelName={material.title}
        />

        {/* Spark Testing Profile */}
        <SparkProfileCard
          sparkProfile={meta.spark_testing_profile}
          steelName={material.title}
        />

        {/* Workshop & Smithing Characteristics */}
        <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
          <h3 className="text-lg font-bold text-white flex items-center gap-2 mb-4 border-b border-neutral-800/80 pb-3">
            <span className="text-[#FF5722]">⚒️</span> Workshop Behavior &amp; Machinability
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs leading-relaxed">
            <div className="rounded-lg border border-neutral-800 bg-neutral-900/50 p-4">
              <h4 className="font-mono uppercase font-bold text-neutral-300 mb-1 flex items-center gap-1.5">
                <span>⚡</span> Forge Weldability &amp; Damascus:
              </h4>
              <p className="text-neutral-400">
                {meta.weldability ||
                  "Clean forge weldability when protected with anhydrous borax. Responds well to solid-state diffusion welding."}
              </p>
            </div>

            <div className="rounded-lg border border-neutral-800 bg-neutral-900/50 p-4">
              <h4 className="font-mono uppercase font-bold text-neutral-300 mb-1 flex items-center gap-1.5">
                <span>⚙️</span> Grinding &amp; Abrasive Wear:
              </h4>
              <p className="text-neutral-400">
                {meta.grinding_characteristics ||
                  "Grinds cleanly with ceramic and aluminum oxide abrasive belts. Keep cool during bevel grinding to prevent temper draw."}
              </p>
            </div>

            <div className="rounded-lg border border-neutral-800 bg-neutral-900/50 p-4">
              <h4 className="font-mono uppercase font-bold text-neutral-300 mb-1 flex items-center gap-1.5">
                <span>🛡️</span> Corrosion &amp; Patina Resistance:
              </h4>
              <p className="text-neutral-400">
                {meta.corrosion_resistance ||
                  "Non-stainless carbon steel. Readily develops an oxidation patina with food acids. Protect in shop with camellia oil, paste wax, or boiled linseed oil."}
              </p>
            </div>

            <div className="rounded-lg border border-neutral-800 bg-neutral-900/50 p-4">
              <h4 className="font-mono uppercase font-bold text-neutral-300 mb-1 flex items-center gap-1.5">
                <span>🔥</span> Forging Thermal Caution:
              </h4>
              <p className="text-neutral-400">
                Operate strictly between {meta.forging_temp_range_f || "1650°F and 2050°F"}. Forging below dull cherry red induces micro-fractures; heating into blinding spark heat permanently burns carbon out of the steel.
              </p>
            </div>
          </div>
        </div>

        {/* Practical Applications & Beginner Pitfalls */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Applications */}
          <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
            <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
              <span className="text-emerald-400">✓</span> Recommended Applications
            </h4>
            <ul className="space-y-2 text-xs text-neutral-300">
              {(meta.common_applications && meta.common_applications.length > 0
                ? meta.common_applications
                : ["Hand-forged blades", "Workshop drifts and punches", "Small hand tools"]
              ).map((app, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-emerald-400 font-bold">•</span>
                  <span>{app}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Common Traps */}
          <div className="rounded-xl border border-amber-500/20 bg-amber-950/10 p-6">
            <h4 className="text-sm font-bold text-amber-400 mb-3 flex items-center gap-2">
              <span>⚠</span> Common Smithing Traps &amp; Pitfalls
            </h4>
            <ul className="space-y-2 text-xs text-neutral-300">
              {(meta.common_mistakes && meta.common_mistakes.length > 0
                ? meta.common_mistakes
                : ["Overheating during forge soaking causes rapid austenite grain enlargement."]
              ).map((mistake, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-amber-500 font-bold">•</span>
                  <span>{mistake}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Source Reference & Handbook Citation */}
        <div className="rounded-xl border border-neutral-800 bg-neutral-900/60 p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs font-mono">
          <div>
            <span className="text-neutral-500 uppercase text-[10px] block">
              Handbook Source Citation
            </span>
            <p className="text-neutral-300 mt-0.5 font-medium">
              {meta.source_reference ||
                "ASM Handbook Volume 1: Properties and Selection of Irons, Steels, and High-Performance Alloys"}
            </p>
          </div>
          <Link
            href="/materials"
            className="shrink-0 rounded-lg border border-neutral-700 bg-neutral-800 px-3.5 py-1.5 text-neutral-300 hover:border-neutral-600 hover:text-white transition-colors"
          >
            ← Back to Database
          </Link>
        </div>
      </div>
    </div>
  );
}
