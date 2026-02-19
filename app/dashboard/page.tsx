"use client";

import { useEffect, useState } from "react";
import Dashboard3D from "@/components/Dashboard3D";
import { AnalysisResult } from "@/lib/types";
import { loadTransactionEdges, GraphEdge } from "@/lib/graphUtils";

export default function DashboardPage() {
  const [data, setData] = useState<AnalysisResult | null>(null);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load analysis data and transaction edges
    Promise.all([
      fetch("/api/sample").then((res) => res.json()),
      loadTransactionEdges("/test_data.csv"),
    ])
      .then(([analysisResult, transactionEdges]) => {
        setData(analysisResult);
        setEdges(transactionEdges);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to load data:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center relative overflow-hidden">
        {/* Blurred Background Image */}
        <div className="fixed inset-0 z-0">
          <img
            src="/backgroundImage.png"
            alt="Background"
            className="w-full h-full object-cover blur-sm scale-105"
          />
        </div>
        
        {/* Dark Overlay */}
        <div className="fixed inset-0 bg-black/50 z-0" />

        <div className="text-center relative z-10">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-400 mb-4"></div>
          <p className="text-cyan-400 text-sm">Loading analysis data...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center relative overflow-hidden">
        {/* Blurred Background Image */}
        <div className="fixed inset-0 z-0">
          <img
            src="/backgroundImage.png"
            alt="Background"
            className="w-full h-full object-cover blur-sm scale-105"
          />
        </div>
        
        {/* Dark Overlay */}
        <div className="fixed inset-0 bg-black/50 z-0" />

        <div className="text-center relative z-10">
          <p className="text-red-400 text-lg mb-2">Failed to load data</p>
          <p className="text-slate-400 text-sm">Please try again later</p>
        </div>
      </div>
    );
  }

  return <Dashboard3D data={data} edges={edges} />;
}
