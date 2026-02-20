"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import UploadDropzone from "@/components/UploadDropzone";

export default function HomePage() {
  const router = useRouter();
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    setIsAnalyzing(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const result = await response.json();
      
      // Generate edges from analysis result
      const { generateGraphEdges } = await import("@/lib/graphUtils");
      const edges = generateGraphEdges(result);
      
      // Store both result and edges
      sessionStorage.setItem("analysisResult", JSON.stringify(result));
      sessionStorage.setItem("graphEdges", JSON.stringify(edges));
      
      console.log("✅ CSV analyzed:", {
        accounts: result.suspicious_accounts?.length,
        rings: result.fraud_rings?.length,
        edges: edges.length
      });
      
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleRunSample = async () => {
    setIsAnalyzing(true);
    setError(null);

    try {
      const response = await fetch("/api/sample", { method: "POST" });
      if (!response.ok) throw new Error("Sample analysis failed");

      const result = await response.json();
      
      // Generate edges from analysis result since we're using sample data
      const { generateGraphEdges } = await import("@/lib/graphUtils");
      const edges = generateGraphEdges(result);
      
      // Store both result and edges
      sessionStorage.setItem("analysisResult", JSON.stringify(result));
      sessionStorage.setItem("graphEdges", JSON.stringify(edges));
      
      console.log("✅ Sample data loaded:", {
        accounts: result.suspicious_accounts?.length,
        rings: result.fraud_rings?.length,
        edges: edges.length
      });
      
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8 relative overflow-hidden">
      {/* Blurred Background Image */}
      <div className="fixed inset-0 z-0">
        <img
          src="/backgroundImage.png"
          alt="Background"
          className="w-full h-full object-cover blur-sm scale-105 opacity-30"
        />
      </div>
      
      {/* Dark Overlay */}
      <div className="fixed inset-0 bg-black/60 z-0" />

      <div className="relative max-w-4xl mx-auto z-10">
        <div className="text-center mb-8">
          <h1 className="text-6xl font-bold text-cyan-400 mb-2">
            MuleRift
          </h1>
          <p className="text-xl text-slate-300">
            Upload transaction CSV to detect fraud rings
          </p>
        </div>

        <UploadDropzone onFileSelect={handleFileUpload} isLoading={isAnalyzing} />

        {error && (
          <div className="mt-4 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400">
            {error}
          </div>
        )}

        <div className="mt-8 text-center">
          <button
            onClick={handleRunSample}
            disabled={isAnalyzing}
            className="px-8 py-3 bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-xl font-semibold hover:from-cyan-700 hover:to-blue-700 disabled:opacity-50 transform transition-all hover:scale-105 hover:shadow-xl disabled:hover:scale-100"
          >
            {isAnalyzing ? "Analyzing..." : "Run Sample Data"}
          </button>
        </div>
      </div>
    </main>
  );
}
