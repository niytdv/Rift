// Locked Data Contract - MuleRift Analysis Results
// All keys must be snake_case

export interface SuspiciousAccount {
  account_id: string;
  suspicion_score: number; // float (0-100) - weighted average of detected patterns
  detected_patterns: string[];
  ring_id: string;
}

export interface FraudRing {
  ring_id: string; // format: 'RING_00X'
  member_accounts: string[];
  pattern_type: 'cycle' | 'smurfing' | 'shell';
  risk_score: number; // float (0-100)
}

export interface AnalysisResult {
  suspicious_accounts: SuspiciousAccount[];
  fraud_rings: FraudRing[];
  summary: {
    total_accounts_analyzed: number;
    suspicious_accounts_flagged: number;
    fraud_rings_detected: number;
    processing_time_seconds: number;
  };
}

// Extended types for internal use (graph visualization)
export interface GraphNode {
  id: string;
  label: string;
  suspicion_score: number;
  detected_patterns: string[];
  ring_id: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  transaction_count: number;
  total_amount: number;
  earliest_timestamp: string;
  latest_timestamp: string;
}

export interface Transaction {
  amount: number;
  timestamp: string;
}
