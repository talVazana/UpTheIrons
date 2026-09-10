"use client";

interface MaintenanceGuideProps {
  maintenanceProtocols?: string[];
  toolName: string;
}

export default function MaintenanceGuide({
  maintenanceProtocols,
  toolName,
}: MaintenanceGuideProps) {
  if (!maintenanceProtocols || maintenanceProtocols.length === 0) {
    return null;
  }

  return (
    <div className="rounded-xl border border-neutral-800 bg-[#161616] p-6">
      <div className="flex items-center justify-between mb-4 border-b border-neutral-800/80 pb-3">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <span className="text-[#FF5722]">⚙️</span> Maintenance &amp; Upkeep — {toolName}
        </h3>
        <span className="text-[11px] font-mono uppercase tracking-wider text-neutral-400 bg-neutral-800 px-2 py-0.5 rounded">
          Longevity Protocol
        </span>
      </div>

      <ul className="space-y-2.5 text-xs text-neutral-300 leading-relaxed font-sans">
        {maintenanceProtocols.map((protocol, idx) => (
          <li key={idx} className="flex items-start gap-2.5 rounded-lg border border-neutral-850 bg-neutral-900/40 p-3">
            <span className="text-[#FF5722] font-mono font-bold text-xs mt-0.5">
              0{idx + 1}.
            </span>
            <span>{protocol}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
