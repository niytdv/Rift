import json

def generate_json_output(accounts, rings, graph, processing_time):
    """Generate JSON output matching Locked Data Contract.
    
    Contract: snake_case keys, suspicion_score as weighted average,
    ring_id format 'RING_00X', pattern_type: cycle/smurfing/shell
    
    Returns: JSON string with suspicious_accounts, fraud_rings, summary
    """
    # Build suspicious_accounts array (contract format)
    suspicious_accounts = []
    for acc in accounts:
        suspicious_accounts.append({
            'account_id': acc['account_id'],
            'suspicion_score': round(acc['suspicion_score'], 2),
            'detected_patterns': acc['detected_patterns'],
            'ring_id': acc.get('ring_id', '')
        })
    
    # Build fraud_rings array (contract format)
    fraud_rings = []
    for ring in rings:
        fraud_rings.append({
            'ring_id': ring['ring_id'],
            'member_accounts': ring['member_accounts'],
            'pattern_type': ring['pattern_type'],
            'risk_score': round(ring['risk_score'], 2)
        })
    
    # Count flagged accounts (suspicion_score > 50)
    flagged_count = len([a for a in suspicious_accounts if a['suspicion_score'] > 50])
    
    # Build output matching Locked Data Contract
    output = {
        'suspicious_accounts': suspicious_accounts,
        'fraud_rings': fraud_rings,
        'summary': {
            'total_accounts_analyzed': len(suspicious_accounts),
            'suspicious_accounts_flagged': flagged_count,
            'fraud_rings_detected': len(fraud_rings),
            'processing_time_seconds': round(processing_time / 1000, 3)
        }
    }
    
    return json.dumps(output, indent=2)
