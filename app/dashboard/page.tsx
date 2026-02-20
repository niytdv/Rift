"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Dashboard3D from "@/components/Dashboard3D";
import { AnalysisResult } from "@/lib/types";
import { loadTransactionEdges, GraphEdge } from "@/lib/graphUtils";

export default function DashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<AnalysisResult | null>(null);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if there's analysis data from upload
    const storedData = sessionStorage.getItem("analysisResult");
    const storedEdges = sessionStorage.getItem("graphEdges");
    
    if (storedData) {
      try {
        const analysisResult = JSON.parse(storedData);
        setData(analysisResult);
        
        // First check if we have stored edges
        if (storedEdges) {
          const parsedEdges = JSON.parse(storedEdges);
          console.log("✅ Using stored edges:", parsedEdges.length);
          setEdges(parsedEdges);
          setLoading(false);
          return;
        }
        
        // Try to load edges from CSV, fallback to generated edges
        loadTransactionEdges("/sample_data.csv")
          .then((loadedEdges) => {
            if (loadedEdges.length > 0) {
              console.log("✅ Loaded edges from CSV:", loadedEdges.length);
              setEdges(loadedEdges);
            } else {
              console.log("⚠️ No edges from CSV, generating from analysis data");
              const { generateGraphEdges } = require("@/lib/graphUtils");
              const generatedEdges = generateGraphEdges(analysisResult);
              console.log("✅ Generated edges:", generatedEdges.length);
              setEdges(generatedEdges);
            }
            setLoading(false);
          })
          .catch((err) => {
            console.error("❌ Failed to load CSV edges:", err);
            const { generateGraphEdges } = require("@/lib/graphUtils");
            const generatedEdges = generateGraphEdges(analysisResult);
            console.log("✅ Generated fallback edges:", generatedEdges.length);
            setEdges(generatedEdges);
            setLoading(false);
          });
      } catch (err) {
        console.error("Failed to parse stored data:", err);
        sessionStorage.removeItem("analysisResult");
        sessionStorage.removeItem("graphEdges");
        router.push("/");
        setLoading(false);
      }
    } else {
      // No data, redirect to upload page
      router.push("/");
      setLoading(false);
    }
  }, [router]);

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
          <p className="text-cyan-400 text-sm">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return null; // Will redirect to home
  }

  return <Dashboard3D data={data} edges={edges} />;
}
