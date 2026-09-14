"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function NewMaterialPage() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // Form State
  const [title, setTitle] = useState("");
  const [summary, setSummary] = useState("");
  const [classification, setClassification] = useState("");
  const [steelCategory, setSteelCategory] = useState("carbon_steel");
  const [beginnerSuitable, setBeginnerSuitable] = useState(true);
  const [carbonPct, setCarbonPct] = useState(0.8);
  const [forgingRange, setForgingRange] = useState("1650°F – 2050°F");
  const [targetHardness, setTargetHardness] = useState("58 – 61 HRC");
  const [quenchMedium, setQuenchMedium] = useState("Oil Quench (Canola)");
  const [sourceReference, setSourceReference] = useState("ASM Handbook / Manufacturer Spec");
  const [alloying, setAlloying] = useState("Mn:0.6, Cr:0.2"); // parsed later

  const [showHelp, setShowHelp] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("admin_token");
    if (!token) {
      router.push("/admin");
    } else {
      setIsLoggedIn(true);
    }
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      // Parse alloying elements "Mn:0.6, Cr:0.2" -> { mn: 0.6, cr: 0.2 }
      const alloying_elements: Record<string, number> = {};
      alloying.split(",").forEach(part => {
        const [k, v] = part.split(":");
        if (k && v) {
          alloying_elements[k.trim().toLowerCase()] = parseFloat(v.trim());
        }
      });

      const payload = {
        title,
        summary,
        category: "materials",
        tags: [],
        difficulty: beginnerSuitable ? "beginner" : "advanced",
        status: "published",
        metadata: {
          classification,
          carbon_pct: parseFloat(carbonPct.toString()),
          alloying_elements,
          steel_category: steelCategory,
          forging_temp_range_f: forgingRange,
          heat_treatment: {
            target_hardness_hrc: targetHardness,
            quench_medium: quenchMedium
          },
          beginner_suitability: beginnerSuitable,
          source_reference: sourceReference
        }
      };

      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000"}/api/v1/materials`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("admin_token")}`
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        setMessage("Material added successfully!");
        // reset form or redirect
      } else {
        const data = await res.json();
        setMessage(`Error: ${data.detail || "Failed to add"}`);
      }
    } catch (err: any) {
      setMessage(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  if (!isLoggedIn) return null;

  return (
    <div className="max-w-2xl mx-auto mt-10 mb-20 p-6 bg-[var(--bg-surface)] border-[4px] border-[var(--border-muted)] shadow-2xl">
      <div className="flex justify-between items-center mb-6 border-b border-[var(--border-muted)] pb-4">
        <h1 className="text-2xl font-bold flex items-center gap-3">
          Add New Material
          <button type="button" onClick={() => setShowHelp(!showHelp)} className="text-xs bg-neutral-800 border border-neutral-600 px-2 py-1 rounded hover:bg-neutral-700 transition-colors">
            {showHelp ? "Close Help" : "Help / Guide"}
          </button>
        </h1>
        <Link href="/admin" className="text-sm text-neutral-400 hover:text-white underline">
          &larr; Back to Admin
        </Link>
      </div>

      {showHelp && (
        <div className="mb-6 p-4 bg-[#161616] border border-neutral-700 text-sm leading-relaxed space-y-4 rounded-lg shadow-inner">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-bold text-[#FF5722]">Material Fields Guide</h2>
            <button type="button" onClick={() => setShowHelp(false)} className="text-neutral-500 hover:text-white text-lg leading-none">✕</button>
          </div>
          <p className="text-neutral-300">This form allows you to forge a new steel card. <strong className="text-[#FF5722]">No field is mandatory.</strong> The data will be saved to the database and immediately appear on the Materials page.</p>
          <ul className="list-disc pl-5 space-y-2 text-neutral-400">
            <li><strong className="text-white">Title:</strong> The common name of the steel (e.g. "1095 High Carbon", "5160 Spring Steel").</li>
            <li><strong className="text-white">Classification:</strong> How this steel is classified (e.g. "Water Hardening", "Oil Quench Spring Steel").</li>
            <li><strong className="text-white">Summary:</strong> A short description of the steel's properties and best uses.</li>
            <li><strong className="text-white">Steel Category:</strong> The main family (Carbon, Tool, Spring, Alloy, Stainless). Used for filtering tabs.</li>
            <li><strong className="text-white">Carbon %:</strong> The carbon content as a decimal. 0.84 = 0.84%. Used to draw the carbon visualizer bar.</li>
            <li><strong className="text-white">Beginner Suitable?:</strong> Check if this steel is forgiving for novices. Shows a green checkmark or a yellow warning.</li>
            <li><strong className="text-white">Forging Range:</strong> The safe temperature range for forging (e.g. "1650°F – 2050°F").</li>
            <li><strong className="text-white">Target Hardness:</strong> Expected Rockwell hardness after proper heat treat (e.g. "58 – 61 HRC").</li>
            <li><strong className="text-white">Quench Medium:</strong> The liquid used to cool the steel (e.g. "Oil Quench", "Water/Brine").</li>
            <li><strong className="text-white">Alloying Elements:</strong> Additional elements in the steel. Format exactly as <code>Symbol:Percentage</code> separated by commas (e.g. "Mn:0.6, Cr:0.2"). Appears as tags.</li>
            <li><strong className="text-white">Source Reference:</strong> A citation or source. Can be a link (URL) or free text (e.g. "ASM Handbook"). Not mandatory.</li>
          </ul>
        </div>
      )}

      {message && (
        <div className={`mb-6 p-3 text-center font-bold ${message.startsWith("Error") ? "text-red-500 bg-red-500/10" : "text-green-500 bg-green-500/10"}`}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        
        {/* Core fields */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-bold mb-1">Title (e.g. 1095 High Carbon)</label>
            <input type="text" value={title} onChange={e => setTitle(e.target.value)} className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2" />
          </div>
          <div>
            <label className="block text-sm font-bold mb-1">Classification (e.g. Water Hardening)</label>
            <input type="text" value={classification} onChange={e => setClassification(e.target.value)} className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-bold mb-1">Summary</label>
          <textarea rows={2} value={summary} onChange={e => setSummary(e.target.value)} className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2" />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-bold mb-1">Steel Category</label>
            <select value={steelCategory} onChange={e => setSteelCategory(e.target.value)} className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2 text-white">
              <option value="carbon_steel">Carbon Steel</option>
              <option value="tool_steel">Tool Steel</option>
              <option value="spring_steel">Spring Steel</option>
              <option value="alloy_steel">Alloy Steel</option>
              <option value="stainless_steel">Stainless Steel</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-bold mb-1">Carbon %</label>
            <input type="number" step="0.01" value={carbonPct} onChange={e => setCarbonPct(parseFloat(e.target.value))} className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2" />
          </div>
        </div>

        <label className="flex items-center gap-2 font-bold bg-[var(--bg-card)] border border-[var(--border-focus)] p-3 cursor-pointer">
          <input type="checkbox" checked={beginnerSuitable} onChange={e => setBeginnerSuitable(e.target.checked)} className="h-4 w-4" />
          Beginner Suitable?
        </label>

        {/* Tech specs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-bold mb-1">Forging Range</label>
            <input type="text" value={forgingRange} onChange={e => setForgingRange(e.target.value)} className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2" />
          </div>
          <div>
            <label className="block text-sm font-bold mb-1">Target Hardness</label>
            <input type="text" value={targetHardness} onChange={e => setTargetHardness(e.target.value)} className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2" />
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-bold mb-1">Quench Medium</label>
            <input type="text" value={quenchMedium} onChange={e => setQuenchMedium(e.target.value)} className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2" />
          </div>
          <div>
            <label className="block text-sm font-bold mb-1">Alloying Elements (Symbol:%)</label>
            <input type="text" value={alloying} onChange={e => setAlloying(e.target.value)} placeholder="Mn:0.6, Cr:0.2" className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-bold mb-1">Source Reference</label>
          <input type="text" value={sourceReference} onChange={e => setSourceReference(e.target.value)} className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2" placeholder="Link (URL) or Free Text (e.g. ASM Handbook)" />
        </div>

        <button type="submit" disabled={loading} className="mt-4 bg-[var(--accent-forge)] text-white p-3 font-bold hover:brightness-110 disabled:opacity-50">
          {loading ? "FORGING..." : "FORGE NEW MATERIAL"}
        </button>

      </form>
    </div>
  );
}
