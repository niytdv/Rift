"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { gsap } from "gsap";
import UploadDropzone from "@/components/UploadDropzone";

export default function HomePage() {
  const router = useRouter();
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const titleRef = useRef<HTMLHeadingElement>(null);
  const subtitleRef = useRef<HTMLParagraphElement>(null);
  const dropzoneRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLDivElement>(null);
  const particlesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Clear any previous analysis data when landing on home page
    sessionStorage.removeItem("analysisResult");

    // Create timeline for entrance animation
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    // Animate title with split effect
    tl.fromTo(
      titleRef.current,
      { 
        opacity: 0, 
        y: -100,
        scale: 0.8,
        rotationX: -90
      },
      { 
        opacity: 1, 
        y: 0,
        scale: 1,
        rotationX: 0,
        duration: 1.2,
        ease: "back.out(1.7)"
      }
    )
    // Animate subtitle
    .fromTo(
      subtitleRef.current,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.8 },
      "-=0.6"
    )
    // Animate dropzone with scale
    .fromTo(
      dropzoneRef.current,
      { 
        opacity: 0, 
        scale: 0.8,
        y: 50
      },
      { 
        opacity: 1, 
        scale: 1,
        y: 0,
        duration: 1,
        ease: "elastic.out(1, 0.5)"
      },
      "-=0.4"
    )
    // Animate button
    .fromTo(
      buttonRef.current,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.6 },
      "-=0.3"
    );

    // Floating animation for particles
    if (particlesRef.current) {
      const particles = particlesRef.current.children;
      Array.from(particles).forEach((particle, i) => {
        gsap.to(particle, {
          y: "random(-20, 20)",
          x: "random(-20, 20)",
          duration: "random(2, 4)",
          repeat: -1,
          yoyo: true,
          ease: "sine.inOut",
          delay: i * 0.1
        });
      });
    }

    // Hover effect for title
    if (titleRef.current) {
      titleRef.current.addEventListener("mouseenter", () => {
        gsap.to(titleRef.current, {
          scale: 1.05,
          color: "#3b82f6",
          duration: 0.3,
          ease: "power2.out"
        });
      });
      
      titleRef.current.addEventListener("mouseleave", () => {
        gsap.to(titleRef.current, {
          scale: 1,
          color: "#1f2937",
          duration: 0.3,
          ease: "power2.out"
        });
      });
    }
  }, []);

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
      sessionStorage.setItem("analysisResult", JSON.stringify(result));
      router.push("/results");
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
      sessionStorage.setItem("analysisResult", JSON.stringify(result));
      router.push("/results");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <main className="relative min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-100 p-8 overflow-hidden">
      {/* Animated background particles */}
      <div ref={particlesRef} className="absolute inset-0 pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-2 h-2 bg-blue-400/20 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
          />
        ))}
      </div>

      <div className="relative max-w-4xl mx-auto">
        <h1 
          ref={titleRef}
          className="text-6xl font-bold text-gray-800 mb-2 text-center cursor-pointer"
          style={{ perspective: "1000px" }}
        >
          Money Mule Detector
        </h1>
        
        <p 
          ref={subtitleRef}
          className="text-xl text-gray-600 mb-12 text-center"
        >
          Upload transaction CSV to detect fraud rings
        </p>

        <div ref={dropzoneRef}>
          <UploadDropzone onFileSelect={handleFileUpload} isLoading={isAnalyzing} />
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 animate-shake">
            {error}
          </div>
        )}

        <div ref={buttonRef} className="mt-8 text-center">
          <button
            onClick={handleRunSample}
            disabled={isAnalyzing}
            className="px-8 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 transform transition-all hover:scale-105 hover:shadow-xl"
          >
            {isAnalyzing ? "Analyzing..." : "Run Sample Data"}
          </button>
        </div>
      </div>
    </main>
  );
}
