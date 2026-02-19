"use client";

import { SuspiciousAccount } from "@/lib/types";

interface AccountModalProps {
  account: SuspiciousAccount;
  onClose: () => void;
}

export default function AccountModal({ account, onClose }: AccountModalProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">Account Risk Analysis</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 text-2xl">
            ×
          </button>
        </div>
        
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Account ID</p>
              <p className="font-mono font-semibold">{account.account_id}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Suspicion Score</p>
              <p className={`text-2xl font-bold ${account.suspicion_score > 50 ? "text-red-600" : "text-green-600"}`}>
                {account.suspicion_score.toFixed(1)}
              </p>
            </div>
          </div>

          {account.ring_id && (
            <div>
              <p className="text-sm text-gray-600 mb-2">Ring Membership</p>
              <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-mono">
                {account.ring_id}
              </span>
            </div>
          )}

          {account.detected_patterns.length > 0 && (
            <div>
              <p className="text-sm text-gray-600 mb-2">Detected Patterns</p>
              <div className="space-y-2">
                {account.detected_patterns.map((pattern, idx) => {
                  const [patternType, value] = pattern.split(':');
                  const bgColor = patternType === 'cycle_participation' ? 'bg-red-50' : 'bg-yellow-50';
                  const textColor = patternType === 'cycle_participation' ? 'text-red-800' : 'text-yellow-800';
                  
                  return (
                    <div key={idx} className={`${bgColor} p-2 rounded text-sm`}>
                      <p className={`font-semibold ${textColor}`}>
                        {patternType.replace('_', ' ').toUpperCase()}
                      </p>
                      <p className="text-gray-600 text-xs">
                        {value ? `Count: ${value}` : 'Detected'}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          <div className="bg-blue-50 p-3 rounded">
            <p className="text-xs text-blue-800 font-semibold mb-1">SCORING METHOD</p>
            <p className="text-xs text-gray-600">
              Suspicion score calculated as weighted average:
              <br />• Cycle participation: 60% weight
              <br />• Temporal velocity: 40% weight
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
