"use client";

export default function TestBackgroundPage() {
  return (
    <div className="relative min-h-screen bg-slate-950 overflow-hidden">
      {/* Test Background - Using img element with proper z-index */}
      <div className="fixed inset-0 z-0">
        <img
          src="/backgroundImage.png"
          alt="Background"
          className="w-full h-full object-cover blur-sm scale-105"
        />
      </div>
      
      {/* Dark Overlay */}
      <div className="fixed inset-0 bg-black/50 z-0" />
      
      {/* Content */}
      <div className="relative z-10 p-8">
        <h1 className="text-cyan-400 text-5xl mb-4 font-bold">
          BACKGROUND TEST (IMG Element - Fixed Z-Index)
        </h1>
        <p className="text-slate-400 text-xl">
          If you see a blurred background image behind this text, it's working!
        </p>
        <p className="text-slate-400 mt-4">
          If you only see a dark background, the image still isn't loading.
        </p>
        
        <div className="mt-8 p-4 bg-slate-800/80 rounded-lg">
          <h2 className="text-cyan-400 mb-2">Debug Info:</h2>
          <p className="text-slate-300 text-sm">
            Using: IMG element with z-0 (not negative)
          </p>
          <p className="text-slate-300 text-sm">
            Image URL: /backgroundImage.png
          </p>
          <p className="text-slate-300 text-sm">
            Image accessible at: http://localhost:3000/backgroundImage.png
          </p>
        </div>
        
        {/* Direct image test */}
        <div className="mt-8 p-4 bg-slate-800/80 rounded-lg">
          <h2 className="text-cyan-400 mb-2">Direct Image Test (no blur):</h2>
          <img 
            src="/backgroundImage.png" 
            alt="Test" 
            className="w-64 h-auto border border-cyan-500"
          />
        </div>
      </div>
    </div>
  );
}
