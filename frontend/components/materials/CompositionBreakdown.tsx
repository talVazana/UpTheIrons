"use client";

import { useMemo } from "react";

interface CompositionBreakdownProps {
  carbonPct: number;
  alloyingElements: Record<string, number>;
  sourceStandard?: string;
}

interface ElementInfo {
  symbol: string;
  name: string;
  role: string;
  color: string;
}

const ELEMENT_METALLURGY: Record<string, ElementInfo> = {
  carbon: {
    symbol: "C",
    name: "Carbon",
    role: "The prime hardening element in steel. Dissolves into austenite during heating and traps in a strained body-centered tetragonal lattice (martensite) during rapid quenching to provide extreme cutting hardness.",
    color: "#FF5722",
  },
  chromium: {
    symbol: "Cr",
    name: "Chromium",
    role: "Increases hardenability and wear resistance by forming hard chromium carbides. Retards grain growth during high forge heats and enhances oxidation and corrosion resistance.",
    color: "#0284c7",
  },
  manganese: {
    symbol: "Mn",
    name: "Manganese",
    role: "Essential deoxidizer during smelting. Significantly increases hardenability and allows slower quench speeds (e.g. oil instead of water) by moving the pearlite nose to the right on TTT diagrams.",
    color: "#d97706",
  },
  vanadium: {
    symbol: "V",
    name: "Vanadium",
    role: "A potent grain refiner. Forms microscopic, ultra-hard vanadium carbides that resist dissolution at high austenitizing temperatures, preventing grain coarsening and boosting edge longevity.",
    color: "#8b5cf6",
  },
  tungsten: {
    symbol: "W",
    name: "Tungsten",
    role: "Forms exceptionally hard, heat-stable tungsten carbides. Preserves cutting keenness and abrasion resistance even under high frictional heat.",
    color: "#ec4899",
  },
  silicon: {
    symbol: "Si",
    name: "Silicon",
    role: "Deoxidizer that strengthens the ferrite matrix. Substantially elevates the elastic limit and yield strength, making it crucial for impact shock tools and spring steels.",
    color: "#10b981",
  },
  nickel: {
    symbol: "Ni",
    name: "Nickel",
    role: "Enhances low-temperature fracture toughness without reducing ductility. In pattern welding (Damascus), nickel resists acid etching to produce shimmering bright silver layers (e.g. 15N20).",
    color: "#06b6d4",
  },
  molybdenum: {
    symbol: "Mo",
    name: "Molybdenum",
    role: "Improves deep hardenability, hot strength, and resistance to temper embrittlement. Often combined with chromium for heavy-duty shock resistance.",
    color: "#f59e0b",
  },
  phosphorus: {
    symbol: "P",
    name: "Phosphorus",
    role: "Residual element restricted to minimal levels (<0.035%) to avoid cold-shortness and brittle grain boundaries.",
    color: "#78716c",
  },
  sulfur: {
    symbol: "S",
    name: "Sulfur",
    role: "Residual element kept to minimal levels (<0.040%) in blade steels to prevent hot-short cracking during forging.",
    color: "#78716c",
  },
};

export default function CompositionBreakdown({
  carbonPct,
  alloyingElements,
  sourceStandard,
}: CompositionBreakdownProps) {
  const elements = useMemo(() => {
    const list: Array<{
      key: string;
      name: string;
      symbol: string;
      percentage: number;
      role: string;
      color: string;
    }> = [];

    // Carbon first
    list.push({
      key: "carbon",
      name: "Carbon",
      symbol: "C",
      percentage: carbonPct,
      role: ELEMENT_METALLURGY.carbon.role,
      color: ELEMENT_METALLURGY.carbon.color,
    });

    // Alloying elements
    for (const [key, pct] of Object.entries(alloyingElements)) {
      const lowerKey = key.toLowerCase();
      const meta = ELEMENT_METALLURGY[lowerKey] || {
        symbol: lowerKey.substring(0, 2).toUpperCase(),
        name: key.charAt(0).toUpperCase() + key.slice(1),
        role: "Alloying addition contributing to matrix strength and carbide balance.",
        color: "#94a3b8",
      };

      list.push({
        key: lowerKey,
        name: meta.name,
        symbol: meta.symbol,
        percentage: pct,
        role: meta.role,
        color: meta.color,
      });
    }

    return list;
  }, [carbonPct, alloyingElements]);

  // Compute Iron balance
  const totalAlloys = elements.reduce((sum, el) => sum + el.percentage, 0);
  const ironBalance = Math.max(0, 100 - totalAlloys);

  return (
    <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6 border-b border-neutral-800/80 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span className="text-[#FF5722]">⚖</span> Chemical Composition &amp; Metallurgy
          </h3>
          <p className="text-xs text-neutral-400 mt-0.5">
            Nominal alloy breakdown verified per metallurgical handbooks. Iron (Fe) constitutes the balance.
          </p>
        </div>
        {sourceStandard && (
          <span className="inline-flex items-center rounded-md border border-neutral-700 bg-neutral-800/60 px-2.5 py-1 text-xs font-mono text-neutral-300">
            Standard: {sourceStandard}
          </span>
        )}
      </div>

      {/* Visual Composition Bar */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-xs font-mono text-neutral-400 mb-2">
          <span>Base Matrix: Iron (~{ironBalance.toFixed(1)}% Fe)</span>
          <span className="text-[#FF8A65]">Active Alloys: {totalAlloys.toFixed(2)}%</span>
        </div>
        <div className="flex h-3 w-full overflow-hidden rounded-full bg-neutral-800">
          {elements.map((el) => {
            const visualWidth = Math.max(3, el.percentage * 15);
            return (
              <div
                key={el.key}
                style={{
                  width: `${visualWidth}%`,
                  backgroundColor: el.color,
                }}
                title={`${el.name} (${el.symbol}): ${el.percentage}%`}
                className="h-full transition-all duration-300 hover:brightness-125"
              />
            );
          })}
          <div
            style={{ width: "100%" }}
            className="h-full bg-neutral-700/60"
            title={`Iron balance: ~${ironBalance.toFixed(1)}%`}
          />
        </div>
        <div className="flex flex-wrap items-center gap-3 mt-2.5 text-[11px] font-mono">
          {elements.map((el) => (
            <div key={el.key} className="flex items-center gap-1.5">
              <span
                className="inline-block h-2 w-2 rounded-full"
                style={{ backgroundColor: el.color }}
              />
              <span className="text-neutral-300">
                {el.symbol}: <strong className="text-white">{el.percentage}%</strong>
              </span>
            </div>
          ))}
          <div className="flex items-center gap-1.5">
            <span className="inline-block h-2 w-2 rounded-full bg-neutral-600" />
            <span className="text-neutral-400">Fe: ~{ironBalance.toFixed(1)}% Bal</span>
          </div>
        </div>
      </div>

      {/* Metallurgical Element Roles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        {elements.map((el) => (
          <div
            key={el.key}
            className="rounded-lg border border-neutral-800/80 bg-neutral-900/50 p-3.5 transition-colors hover:border-neutral-700"
          >
            <div className="flex items-center justify-between mb-1.5">
              <div className="flex items-center gap-2">
                <span
                  className="flex h-6 w-6 items-center justify-center rounded text-xs font-mono font-bold text-black"
                  style={{ backgroundColor: el.color }}
                >
                  {el.symbol}
                </span>
                <span className="font-semibold text-white text-sm">{el.name}</span>
              </div>
              <span className="font-mono text-xs font-bold text-[#FF8A65] bg-[#FF5722]/10 px-2 py-0.5 rounded border border-[#FF5722]/20">
                {el.percentage}%
              </span>
            </div>
            <p className="text-xs text-neutral-400 leading-relaxed pl-8">
              {el.role}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
