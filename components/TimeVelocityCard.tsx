"use client";

import TimeVelocitySlider from "./TimeVelocitySlider";

interface TimeVelocityCardProps {
  value: number;
  onChange: (value: number) => void;
}

export default function TimeVelocityCard({
  value,
  onChange,
}: TimeVelocityCardProps) {
  return (
    <div className="bg-white/5 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl p-6">
      <TimeVelocitySlider value={value} onChange={onChange} />
    </div>
  );
}
