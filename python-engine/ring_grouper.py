from collections import defaultdict

def merge_overlapping_rings(ring_groups):
    """
    Merge rings that share common members.
    
    If a node is a 'Collector' in a Fan-In and also a 'Participant' in a Cycle,
    merge all involved accounts into one single Ring.
    """
    if not ring_groups:
        return []
    
    # Convert to sets for easier merging
    ring_sets = [set(ring) for ring in ring_groups]
    
    # Merge overlapping sets
    merged = []
    while ring_sets:
        current = ring_sets.pop(0)
        
        # Check for overlaps with remaining rings
        i = 0
        while i < len(ring_sets):
            if current & ring_sets[i]:  # If there's overlap
                current = current | ring_sets.pop(i)  # Merge
            else:
                i += 1
        
        merged.append(current)
    
    return merged

def deterministic_sort_rings(ring_sets):
    """
    Apply deterministic sorting logic:
    1. Sort members alphabetically within each ring
    2. Sort rings by their smallest member
    
    Returns list of sorted member lists
    """
    sorted_rings = []
    
    for ring_set in ring_sets:
        # Sort members alphabetically
        sorted_members = sorted(list(ring_set))
        sorted_rings.append(sorted_members)
    
    # Sort rings by smallest member
    sorted_rings.sort(key=lambda ring: ring[0] if ring else "")
    
    return sorted_rings

def assign_ring_ids(sorted_rings):
    """
    Assign RING_001, RING_002, etc. to sorted rings.
    
    Returns:
        ring_assignments: dict mapping account_id to ring_id
        ring_list: list of dicts with ring_id and members
    """
    ring_assignments = {}
    ring_list = []
    
    for idx, members in enumerate(sorted_rings, start=1):
        ring_id = f"RING_{idx:03d}"
        
        # Assign ring_id to all members
        for member in members:
            ring_assignments[member] = ring_id
        
        ring_list.append({
            'ring_id': ring_id,
            'members': members
        })
    
    return ring_assignments, ring_list

def group_rings_by_pattern(results):
    """
    Group rings by pattern type with merging and deterministic sorting.
    
    Args:
        results: dict from detect_all_patterns containing:
            - cycle_groups
            - smurfing_groups
            - shell_groups
    
    Returns:
        dict with:
            - ring_assignments: account_id -> ring_id mapping
            - rings_by_pattern: list of rings with pattern_type
    """
    all_rings = []
    pattern_map = {}  # Track which pattern each ring belongs to
    
    # Collect all rings with their pattern types
    for cycle_group in results.get('cycle_groups', []):
        ring_id = len(all_rings)
        all_rings.append(cycle_group)
        pattern_map[ring_id] = 'cycle'
    
    for smurfing_group in results.get('smurfing_groups', []):
        ring_id = len(all_rings)
        all_rings.append(smurfing_group)
        pattern_map[ring_id] = 'smurfing'
    
    for shell_group in results.get('shell_groups', []):
        ring_id = len(all_rings)
        all_rings.append(shell_group)
        pattern_map[ring_id] = 'shell'
    
    # Merge overlapping rings
    merged_rings = merge_overlapping_rings(all_rings)
    
    # Determine pattern type for merged rings
    merged_pattern_map = {}
    for idx, merged_ring in enumerate(merged_rings):
        # Find which original rings contributed to this merged ring
        contributing_patterns = set()
        for orig_idx, orig_ring in enumerate(all_rings):
            if set(orig_ring) & merged_ring:  # If overlap
                contributing_patterns.add(pattern_map[orig_idx])
        
        # Priority: cycle > smurfing > shell
        if 'cycle' in contributing_patterns:
            merged_pattern_map[idx] = 'cycle'
        elif 'smurfing' in contributing_patterns:
            merged_pattern_map[idx] = 'smurfing'
        else:
            merged_pattern_map[idx] = 'shell'
    
    # Apply deterministic sorting
    sorted_rings = deterministic_sort_rings(merged_rings)
    
    # Assign ring IDs
    ring_assignments, ring_list = assign_ring_ids(sorted_rings)
    
    # Add pattern types to ring_list
    rings_by_pattern = []
    for idx, ring_info in enumerate(ring_list):
        rings_by_pattern.append({
            'ring_id': ring_info['ring_id'],
            'members': ring_info['members'],
            'pattern_type': merged_pattern_map.get(idx, 'unknown')
        })
    
    return {
        'ring_assignments': ring_assignments,
        'rings_by_pattern': rings_by_pattern
    }
