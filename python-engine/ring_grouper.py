def group_rings(accounts, patterns):
    """Group detected cycles into fraud rings matching Locked Data Contract.
    
    Contract requirements:
    - ring_id format: 'RING_00X'
    - pattern_type: 'cycle' (for transaction cycles)
    - risk_score: average of member suspicion scores
    
    Returns: List of ring dicts matching contract schema
    """
    rings = []
    cycles = patterns['cycles']
    
    for idx, cycle in enumerate(cycles, 1):
        ring_id = f"RING_{idx:03d}"
        
        # Get scores for accounts in this cycle
        member_scores = []
        for acc in accounts:
            if acc['account_id'] in cycle:
                member_scores.append(acc['suspicion_score'])
        
        # Calculate ring risk score (average of member scores)
        risk_score = sum(member_scores) / len(member_scores) if member_scores else 0
        
        # Determine pattern type (currently only 'cycle' is detected)
        # Future: add 'smurfing' and 'shell' detection
        pattern_type = 'cycle'
        
        rings.append({
            'ring_id': ring_id,
            'member_accounts': cycle,
            'pattern_type': pattern_type,
            'risk_score': risk_score
        })
        
        # Tag accounts with their ring membership (single ring_id per account)
        for acc in accounts:
            if acc['account_id'] in cycle:
                # Assign to highest risk ring if account is in multiple
                if 'ring_id' not in acc or acc.get('temp_risk', 0) < risk_score:
                    acc['ring_id'] = ring_id
                    acc['temp_risk'] = risk_score
    
    # Clean up temporary fields
    for acc in accounts:
        if 'temp_risk' in acc:
            del acc['temp_risk']
        # Ensure ring_id exists (empty string if not in any ring)
        if 'ring_id' not in acc:
            acc['ring_id'] = ''
    
    # Sort rings by risk score (highest first)
    rings.sort(key=lambda r: r['risk_score'], reverse=True)
    
    return rings
