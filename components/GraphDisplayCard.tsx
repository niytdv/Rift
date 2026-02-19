"use client";

import { SuspiciousAccount, FraudRing } from "@/lib/types";
import Graph3D from "./Graph3D";

interface GraphDisplayCardProps {
  accounts: SuspiciousAccount[];
  rings: FraudRing[];
  edges: Array<{
    source: string;
    target: string;
    total_amount: number;
    earliest_timestamp: string;
    latest_timestamp: string;
  }>;
  onNodeClick: (account: SuspiciousAccount) => void;
  selectedRingId: string | null;
  searchQuery: string;
  hideWhitelisted: boolean;
  timeVelocityFilter: number;
}

export default function GraphDisplayCard({
  accounts,
  rings,
  edges,
  onNodeClick,
  selectedRingId,
  searchQuery,
  hideWhitelisted,
  timeVelocityFilter,
}: GraphDisplayCardProps) {
  return (
    <div className="relative h-[600px] bg-white/5 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl overflow-hidden flex justify-center items-center">
      <Graph3D
        accounts={accounts}
        rings={rings}
        edges={edges}
        onNodeClick={onNodeClick}
        selectedRingId={selectedRingId}
        searchQuery={searchQuery}
        hideWhitelisted={hideWhitelisted}
        timeVelocityFilter={timeVelocityFilter}
      />

      {/* Ring ID Indicator (when ring is selected) */}
      {selectedRingId && (
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-cyan-500/20 backdrop-blur-sm border border-cyan-500/50 rounded-lg px-6 py-3">
          <p className="text-cyan-400 text-sm font-semibold">
            RING ID: {selectedRingId} - CIRCULAR ROUTING
          </p>
        </div>
      )}
    </div>
  );
}
