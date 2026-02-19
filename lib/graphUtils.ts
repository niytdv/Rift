import { AnalysisResult } from "./types";

export interface GraphEdge {
  source: string;
  target: string;
  total_amount: number;
  earliest_timestamp: string;
  latest_timestamp: string;
}

/**
 * Parse CSV file and extract transaction edges
 * This reads the actual transaction data from the CSV
 */
export async function loadTransactionEdges(csvPath: string): Promise<GraphEdge[]> {
  try {
    const response = await fetch(csvPath);
    const csvText = await response.text();
    
    const lines = csvText.trim().split('\n');
    const edges: GraphEdge[] = [];
    
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',');
      
      if (values.length >= 4) {
        edges.push({
          source: values[0].trim(),
          target: values[1].trim(),
          total_amount: parseFloat(values[2]) || 0,
          earliest_timestamp: values[3].trim(),
          latest_timestamp: values[3].trim(),
        });
      }
    }
    
    return edges;
  } catch (error) {
    console.error('Failed to load transaction edges:', error);
    return [];
  }
}

/**
 * Generate graph edges from analysis result (fallback method)
 * This is a helper function for when CSV is not available
 */
export function generateGraphEdges(data: AnalysisResult): GraphEdge[] {
  const edges: GraphEdge[] = [];
  
  // Generate edges based on fraud rings (cycles)
  data.fraud_rings.forEach((ring) => {
    if (ring.pattern_type === "cycle") {
      // Create edges connecting ring members in a cycle
      for (let i = 0; i < ring.member_accounts.length; i++) {
        const source = ring.member_accounts[i];
        const target = ring.member_accounts[(i + 1) % ring.member_accounts.length];
        
        // Generate realistic transaction data
        const amount = Math.random() * 10000 + 1000;
        const hoursAgo = Math.random() * 72;
        const timestamp = new Date(Date.now() - hoursAgo * 60 * 60 * 1000);
        
        edges.push({
          source,
          target,
          total_amount: amount,
          earliest_timestamp: timestamp.toISOString(),
          latest_timestamp: timestamp.toISOString(),
        });
      }
    }
  });
  
  // Add some random edges for non-ring accounts
  const nonRingAccounts = data.suspicious_accounts.filter(acc => !acc.ring_id);
  for (let i = 0; i < Math.min(nonRingAccounts.length - 1, 5); i++) {
    const source = nonRingAccounts[i].account_id;
    const target = nonRingAccounts[i + 1].account_id;
    const amount = Math.random() * 5000 + 500;
    const hoursAgo = Math.random() * 72;
    const timestamp = new Date(Date.now() - hoursAgo * 60 * 60 * 1000);
    
    edges.push({
      source,
      target,
      total_amount: amount,
      earliest_timestamp: timestamp.toISOString(),
      latest_timestamp: timestamp.toISOString(),
    });
  }
  
  return edges;
}
