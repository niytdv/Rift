"use client";

import { useEffect, useRef, useState } from "react";
import { gsap } from "gsap";

interface IntroVideoProps {
  onComplete: () => void;
}

export default function IntroVideo({ onComplete }: IntroVideoProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [isVideoLoaded, setIsVideoLoaded] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [showSkip, setShowSkip] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    const container = containerRef.current;

    if (!video || !container) return;

    // Show skip button after 2 seconds
    const skipTimer = setTimeout(() => {
      setShowSkip(true);
    }, 2000);

    // Preload and setup video
    video.load();

    // Handle video loaded
    const handleCanPlay = () => {
      setIsVideoLoaded(true);
      
      // Fade in from black
      gsap.fromTo(
        container,
        { opacity: 0 },
        { 
          opacity: 1, 
          duration: 0.8, 
          ease: "power2.inOut",
          onComplete: () => {
            // Start playing after fade-in
            video.play().then(() => {
              setIsPlaying(true);
            }).catch((error) => {
              console.error("Video playback failed:", error);
              // Fallback: skip intro if autoplay fails
              handleVideoEnd();
            });
          }
        }
      );
    };

    // Handle video end
    const handleVideoEnd = () => {
      setIsPlaying(false);
      
      // Smooth fade-out transition
      gsap.to(container, {
        opacity: 0,
        duration: 1,
        ease: "power2.inOut",
        onComplete: () => {
          onComplete();
        }
      });
    };

    // Event listeners
    video.addEventListener("canplaythrough", handleCanPlay);
    video.addEventListener("ended", handleVideoEnd);

    // Cleanup
    return () => {
      video.removeEventListener("canplaythrough", handleCanPlay);
      video.removeEventListener("ended", handleVideoEnd);
      clearTimeout(skipTimer);
    };
  }, [onComplete]);

  // Handle skip button
  const handleSkip = () => {
    const video = videoRef.current;
    const container = containerRef.current;
    
    if (!video || !container) return;
    
    video.pause();
    
    gsap.to(container, {
      opacity: 0,
      duration: 0.5,
      ease: "power2.inOut",
      onComplete: () => {
        onComplete();
      }
    });
  };

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 z-[9999] bg-black flex items-center justify-center"
      style={{
        opacity: 0,
        willChange: "opacity",
      }}
    >
      {/* Video Element */}
      <video
        ref={videoRef}
        className="absolute inset-0 w-full h-full cinematic-video gpu-accelerated"
        preload="auto"
        playsInline
        muted
        style={{
          willChange: "transform",
          objectFit: "contain", // Changed from "cover" to "contain" to show full video
        }}
      >
        <source src="/loading.mp4" type="video/mp4" />
      </video>

      {/* Fallback loading indicator (shown if video takes time to load) */}
      {!isVideoLoaded && (
        <div className="absolute inset-0 flex items-center justify-center bg-black">
          <div className="flex flex-col items-center gap-4">
            <div className="w-16 h-16 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin" />
            <p className="text-cyan-400 text-sm font-light tracking-wider">
              INITIALIZING SYSTEM
            </p>
          </div>
        </div>
      )}

      {/* Cinematic vignette overlay */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background:
            "radial-gradient(ellipse at center, transparent 0%, rgba(0,0,0,0.3) 100%)",
        }}
      />

      {/* Skip Button (appears after 2 seconds) */}
      {showSkip && isPlaying && (
        <button
          onClick={handleSkip}
          className="absolute bottom-8 right-8 z-50 px-6 py-2 bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/30 rounded-lg text-white text-sm font-light tracking-wider transition-all duration-300 hover:scale-105"
          style={{
            animation: "fadeIn 0.5s ease-in-out",
          }}
        >
          SKIP INTRO
        </button>
      )}

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}
