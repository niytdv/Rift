import sys
import json
import time
from graph_builder import build_graph, prune_isolated_nodes
from detectors import detect_all_patterns
from ring_grouper import group_rings_by_pattern

def calculate_suspicion_score(patterns, aggressive_mode=False):
    """Calculate weighted suspicion score based on detected patterns.
    
    Args:
        patterns: List of detected pattern strings
        aggressive_mode: If True, use higher weights for single-pattern detection
    
    Returns:
        Suspicion score (0-100)
    """
    score = 0
    
    if aggressive_mode:
        # Aggressive weights - single pattern can flag account
        pattern_weights = {
            'cycle': 60,      # High risk - circular routing
            'smurfing': 55,   # High risk - structuring
            'shell': 50,      # Medium-high risk - layering
            'velocity': 45    # Medium risk - pass-through
        }
    else:
        # Conservative weights - need multiple patterns
        pattern_weights = {
            'cycle': 40,
            'smurfing': 40,
            'shell': 30,
            'velocity': 30
        }
    
    for pattern in patterns:
        pattern_lower = pattern.lower()
        if 'cycle' in pattern_lower:
            score += pattern_weights['cycle']
        elif 'fan_in' in pattern_lower or 'fan_out' in pattern_lower:
            score += pattern_weights['smurfing']
        elif 'shell' in pattern_lower:
            score += pattern_weights['shell']
        elif 'velocity' in pattern_lower:
            score += pattern_weights['velocity']
    
    return min(score, 100)

def main():
    """MuleRift - Graph-based money muling detection engine.
    
    Analyzes transaction CSV to detect:
    - Circular Fund Routing (Cycles)
    - Smurfing Patterns (Fan-in / Fan-out)
    - Layered Shell Networks
    
    Usage:
        python main.py <csv_path> [--aggressive]
    """
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python main.py <csv_path> [--aggressive]"}), file=sys.stderr)
        sys.exit(1)

    csv_path = sys.argv[1]
    aggressive_mode = '--aggressive' in sys.argv
    start_time = time.time()
    
    # Build graph
    G, df = build_graph(csv_path)
    
    # Prune isolated nodes
    G = prune_isolated_nodes(G)
    
    # Run detection algorithms
    results = detect_all_patterns(G, df)
    
    # Group rings with merging and deterministic sorting
    ring_data = group_rings_by_pattern(results)
    account_to_ring = ring_data['ring_assignments']
    
    # Build suspicious_accounts list
    suspicious_accounts = []
    all_suspicious_nodes = (
        results['cycle_nodes'] | 
        results['smurfing_nodes'] | 
        results['shell_nodes'] |
        results['velocity_nodes']
    )
    
    for account_id in all_suspicious_nodes:
        detected_patterns = []
        
        # Add descriptive pattern names
        if account_id in results['cycle_nodes']:
            pattern_name = results['cycle_metadata'].get(account_id, 'cycle')
            detected_patterns.append(pattern_name)
        
        if account_id in results['smurfing_nodes']:
            pattern_name = results['smurfing_metadata'].get(account_id, 'smurfing')
            detected_patterns.append(pattern_name)
        
        if account_id in results['shell_nodes']:
            pattern_name = results['shell_metadata'].get(account_id, 'shell')
            detected_patterns.append(pattern_name)
        
        if account_id in results['velocity_nodes']:
            pattern_name = results['velocity_metadata'].get(account_id, 'high_velocity')
            detected_patterns.append(pattern_name)
        
        suspicion_score = calculate_suspicion_score(detected_patterns, aggressive_mode)
        
        # Only include accounts with score > 50
        if suspicion_score > 50:
            suspicious_accounts.append({
                "account_id": account_id,
                "suspicion_score": float(round(suspicion_score, 1)),
                "detected_patterns": detected_patterns,
                "ring_id": account_to_ring.get(account_id, "")
            })
    
    # Sort by suspicion_score descending
    suspicious_accounts.sort(key=lambda x: x['suspicion_score'], reverse=True)
    
    # Build final fraud_rings output
    fraud_rings_output = []
    for ring_info in ring_data['rings_by_pattern']:
        ring_id = ring_info['ring_id']
        members = ring_info['members']
        pattern_type = ring_info['pattern_type']
        
        # Calculate risk score as simple average of member suspicion scores
        member_scores = []
        for account_id in members:
            # Find this account's suspicion_score from suspicious_accounts list
            account_data = next((acc for acc in suspicious_accounts if acc['account_id'] == account_id), None)
            if account_data:
                member_scores.append(account_data['suspicion_score'])
            else:
                # If not in suspicious_accounts, calculate score
                detected_patterns = []
                
                if account_id in results['cycle_nodes']:
                    pattern_name = results['cycle_metadata'].get(account_id, 'cycle')
                    detected_patterns.append(pattern_name)
                
                if account_id in results['smurfing_nodes']:
                    pattern_name = results['smurfing_metadata'].get(account_id, 'smurfing')
                    detected_patterns.append(pattern_name)
                
                if account_id in results['shell_nodes']:
                    pattern_name = results['shell_metadata'].get(account_id, 'shell')
                    detected_patterns.append(pattern_name)
                
                if account_id in results['velocity_nodes']:
                    pattern_name = results['velocity_metadata'].get(account_id, 'high_velocity')
                    detected_patterns.append(pattern_name)
                
                score = calculate_suspicion_score(detected_patterns)
                member_scores.append(score)
        
        # Simple average: sum(member_scores) / len(member_scores)
        # No multipliers, no structural weighting, no randomness
        risk_score = round(sum(member_scores) / len(member_scores), 1) if member_scores else 0.0
        
        fraud_rings_output.append({
            "ring_id": ring_id,
            "member_accounts": members,
            "pattern_type": pattern_type,
            "risk_score": float(risk_score)
        })
    
    processing_time = time.time() - start_time
    
    # Build final output matching MuleRift contract
    output = {
        "suspicious_accounts": suspicious_accounts,
        "fraud_rings": fraud_rings_output,
        "summary": {
            "total_accounts_analyzed": G.number_of_nodes(),
            "suspicious_accounts_flagged": len(suspicious_accounts),
            "fraud_rings_detected": len(fraud_rings_output),
            "processing_time_seconds": float(round(processing_time, 1))
        }
    }
    
    # Print with custom formatting to ensure .0 for whole number floats
    json_str = json.dumps(output, indent=2, ensure_ascii=False)
    print(json_str)

if __name__ == "__main__":
    main()
