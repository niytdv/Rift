def calculate_scores(G, patterns):
    """Calculate suspicion scores for each account using weighted average.
    
    Pattern weights (for weighted average):
    - cycle_participation: weight 0.6
    - temporal_velocity: weight 0.4
    
    Each pattern contributes 0-100 points, then weighted average is calculated.
    
    Returns: List of account dicts with scores and detected_patterns
    """
    accounts = []
    cycles = patterns['cycles']
    velocity = patterns['velocity']
    
    # Build account participation maps
    cycle_participation = {}
    for cycle in cycles:
        for account in cycle:
            if account not in cycle_participation:
                cycle_participation[account] = []
            cycle_participation[account].append(cycle)
    
    # Calculate scores for each account
    for account in G.nodes():
        detected_patterns = []
        pattern_scores = {}
        
        # Cycle participation pattern (0-100 scale)
        if account in cycle_participation:
            num_cycles = len(cycle_participation[account])
            # Scale: 1 cycle = 60, 2+ cycles = 100
            cycle_score = min(num_cycles * 60, 100)
            pattern_scores['cycle_participation'] = cycle_score
            detected_patterns.append(f'cycle_participation:{num_cycles}')
        
        # Temporal velocity pattern (0-100 scale)
        if account in velocity:
            num_velocity = len(velocity[account])
            # Scale: 1 event = 50, 2+ events = 100
            velocity_score = min(num_velocity * 50, 100)
            pattern_scores['temporal_velocity'] = velocity_score
            detected_patterns.append(f'temporal_velocity:{num_velocity}')
        
        # Calculate weighted average suspicion score
        if pattern_scores:
            weights = {
                'cycle_participation': 0.6,
                'temporal_velocity': 0.4
            }
            
            total_weight = 0
            weighted_sum = 0
            
            for pattern, score in pattern_scores.items():
                weight = weights.get(pattern, 0.5)
                weighted_sum += score * weight
                total_weight += weight
            
            suspicion_score = weighted_sum / total_weight if total_weight > 0 else 0
        else:
            suspicion_score = 0
        
        accounts.append({
            'account_id': account,
            'suspicion_score': suspicion_score,
            'detected_patterns': detected_patterns,
            'cycle_count': len(cycle_participation.get(account, [])),
            'velocity_count': len(velocity.get(account, []))
        })
    
    return accounts
