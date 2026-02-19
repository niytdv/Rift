"use client";

import { useState, useEffect, useRef } from "react";
import { Search, Download, Upload } from "lucide-react";
import { gsap } from "gsap";
import { AnalysisResult, SuspiciousAccount } from "@/lib/types";
import GraphDisplayCard from "./GraphDisplayCard";
import ExplainableRiskPanel from "./ExplainableRiskPanel";
import FraudRingTableCard from "./FraudRingTableCard";
import TimeVelocityCard from "./TimeVelocityCard";
import AIChatbotPanel from "./AIChatbotPanel";

interface Dashboard3DProps {
  data: AnalysisResult;
  edges: Array<{
    source: string;
    target: string;
    total_amount: number;
    earliest_timestamp: string;
    latest_timestamp: string;
  }>;
}

export default function Dashboard3D({ data, edges }: Dashboard3DProps) {
  const [selectedAccount, setSelectedAccount] = useState<SuspiciousAccount | null>(null);
  const [selectedRingId, setSelectedRingId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [hideWhitelisted, setHideWhitelisted] = useState(false);
  const [timeVelocityFilter, setTimeVelocityFilter] = useState(72);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Refs for GSAP animations
  const headerRef = useRef<HTMLElement>(null);
  const controlsRef = useRef<HTMLDivElement>(null);
  const graphRef = useRef<HTMLDivElement>(null);
  const sliderRef = useRef<HTMLDivElement>(null);
  const tableRef = useRef<HTMLDivElement>(null);
  const sidebarRef = useRef<HTMLDivElement>(null);
  const bgRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Create master timeline
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    // Animate background with zoom effect
    tl.fromTo(
      bgRef.current,
      { scale: 1.2, opacity: 0 },
      { scale: 1.05, opacity: 1, duration: 1.5, ease: "power2.out" }
    );

    // Animate header sliding down
    tl.fromTo(
      headerRef.current,
      { y: -100, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8, ease: "back.out(1.2)" },
      "-=1.2"
    );

    // Animate controls sliding in from left
    tl.fromTo(
      controlsRef.current,
      { x: -100, opacity: 0 },
      { x: 0, opacity: 1, duration: 0.6 },
      "-=0.4"
    );

    // Animate graph with scale and fade
    tl.fromTo(
      graphRef.current,
      { scale: 0.9, opacity: 0, y: 30 },
      { scale: 1, opacity: 1, y: 0, duration: 1, ease: "back.out(1.1)" },
      "-=0.3"
    );

    // Animate slider
    tl.fromTo(
      sliderRef.current,
      { x: -50, opacity: 0 },
      { x: 0, opacity: 1, duration: 0.5 },
      "-=0.5"
    );

    // Animate table
    tl.fromTo(
      tableRef.current,
      { y: 50, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.6 },
      "-=0.3"
    );

    // Animate sidebar sliding in from right
    tl.fromTo(
      sidebarRef.current,
      { x: 100, opacity: 0 },
      { x: 0, opacity: 1, duration: 0.8, ease: "power2.out" },
      "-=0.8"
    );

    // Add subtle floating animation to graph after entrance
    gsap.to(graphRef.current, {
      y: -5,
      duration: 2,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
      delay: 2
    });
  }, []);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const result = await response.json();
      
      // Reload the page with new data
      window.location.reload();
    } catch (error) {
      console.error("Upload error:", error);
      alert("Failed to analyze CSV file. Please try again.");
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleDownloadJSON = () => {
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `mulerift-analysis-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="h-screen overflow-hidden bg-slate-950 text-white relative">
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

      {/* Grid Layout Container */}
      <div className="relative z-10 h-full grid grid-cols-[1fr_350px]">
        {/* Left Content Area (Main Dashboard) */}
        <div className="flex flex-col h-full overflow-hidden">
          {/* Header */}
          <header className="border-b border-white/10 bg-white/5 backdrop-blur-xl">
            <div className="px-6 py-4">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-2xl font-bold">
                    <span className="text-cyan-400">MULE RIFT</span>
                    <span className="text-white/60 text-sm ml-3">
                      - REAL-TIME FINANCIAL ANOMALY DETECTION
                    </span>
                  </h1>
                </div>
                <div className="flex items-center gap-3">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                  <button
                    onClick={handleUploadClick}
                    disabled={isUploading}
                    className="flex items-center gap-2 px-4 py-2 bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 rounded-xl transition-colors backdrop-blur-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Upload size={16} className="text-cyan-400" />
                    <span className="text-sm text-cyan-400">
                      {isUploading ? "UPLOADING..." : "UPLOAD CSV"}
                    </span>
                  </button>
                  <button
                    onClick={handleDownloadJSON}
                    className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/20 rounded-xl transition-colors backdrop-blur-sm"
                  >
                    <Download size={16} />
                    <span className="text-sm">DOWNLOAD JSON EXPORT</span>
                  </button>
                </div>
              </div>
            </div>
          </header>

          {/* Main Content Area - Scrollable */}
          <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
            {/* Top Controls */}
            <div className="flex items-center gap-4">
              {/* Search Bar */}
              <div className="flex-1 relative">
                <Search
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-white/40"
                  size={18}
                />
                <input
                  type="text"
                  placeholder="Search Account ID..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-white/5 backdrop-blur-xl border border-white/20 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white placeholder-white/40 focus:outline-none focus:border-cyan-500/50 transition-colors"
                />
              </div>

              {/* Whitelist Toggle */}
              <label className="flex items-center gap-3 bg-white/5 backdrop-blur-xl border border-white/20 rounded-xl px-4 py-2.5 cursor-pointer hover:bg-white/10 transition-colors">
                <div className="relative">
                  <input
                    type="checkbox"
                    checked={hideWhitelisted}
                    onChange={(e) => setHideWhitelisted(e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-white/10 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyan-500"></div>
                </div>
                <span className="text-sm text-white/80">
                  Hide Known Business Nodes
                </span>
              </label>
            </div>

            {/* 3D Graph Container with Glassmorphism */}
            <GraphDisplayCard
              accounts={data.suspicious_accounts}
              rings={data.fraud_rings}
              edges={edges}
              onNodeClick={setSelectedAccount}
              selectedRingId={selectedRingId}
              searchQuery={searchQuery}
              hideWhitelisted={hideWhitelisted}
              timeVelocityFilter={timeVelocityFilter}
            />

            {/* Time Velocity Slider with Glassmorphism */}
            <TimeVelocityCard
              value={timeVelocityFilter}
              onChange={setTimeVelocityFilter}
            />

            {/* Fraud Ring Table with Glassmorphism */}
            <FraudRingTableCard
              rings={data.fraud_rings}
              selectedRingId={selectedRingId}
              onRingSelect={setSelectedRingId}
            />
          </div>
        </div>

        {/* Right Sidebar (AI Chatbot) */}
        <AIChatbotPanel />
      </div>

      {/* Explainable Risk Panel */}
      {selectedAccount && (
        <ExplainableRiskPanel
          account={selectedAccount}
          onClose={() => setSelectedAccount(null)}
        />
      )}
    </div>
  );
}
