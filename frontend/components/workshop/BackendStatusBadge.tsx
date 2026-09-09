"use client";

import { useEffect, useState } from "react";
import { checkBackendHealth, HealthResponse } from "@/lib/api";

export function BackendStatusBadge() {
  const [loading, setLoading] = useState(true);
  const [online, setOnline] = useState<boolean | null>(null);
  const [data, setData] = useState<HealthResponse | null>(null);

  async function verifyConnection() {
    setLoading(true);
    const res = await checkBackendHealth();
    setOnline(res.ok);
    setData(res.data || null);
    setLoading(false);
  }

  useEffect(() => {
    verifyConnection();
  }, []);

  if (loading) {
    return (
      <div className="inline-flex items-center gap-2 rounded-full border border-neutral-800 bg-neutral-900 px-2.5 py-1 text-[11px] text-neutral-400">
        <span className="h-1.5 w-1.5 rounded-full bg-neutral-500 animate-ping"></span>
        <span>Connecting to Forge API...</span>
      </div>
    );
  }

  if (online && data) {
    const emuReachable =
      data.diagnostics?.firestore_emulator?.reachable ?? false;
    return (
      <button
        type="button"
        onClick={verifyConnection}
        title={`FastAPI ${data.version} (${data.environment}) | Firestore: ${
          emuReachable ? "Connected" : "Not Reachable"
        } — Click to refresh`}
        className="inline-flex items-center gap-2 rounded-full border border-emerald-900/40 bg-emerald-950/30 px-2.5 py-1 text-[11px] text-emerald-400 hover:bg-emerald-900/40 transition-colors cursor-pointer focus-visible:ring-1 focus-visible:ring-emerald-400"
      >
        <span className="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
        <span className="font-mono font-medium">
          API v{data.version}
        </span>
        {emuReachable && (
          <span className="hidden sm:inline text-neutral-400 font-normal">
            &bull; Firestore OK
          </span>
        )}
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={verifyConnection}
      title="Backend is currently offline or unreachable. Frontend operates in standalone mode. Click to re-check."
      className="inline-flex items-center gap-2 rounded-full border border-neutral-800 bg-neutral-900 px-2.5 py-1 text-[11px] text-neutral-400 hover:border-neutral-700 hover:text-neutral-200 transition-colors cursor-pointer focus-visible:ring-1 focus-visible:ring-[#FF5722]"
    >
      <span className="h-1.5 w-1.5 rounded-full bg-amber-500"></span>
      <span>API Offline (Standalone)</span>
      <span className="text-[10px] text-neutral-500">&#x21bb;</span>
    </button>
  );
}
