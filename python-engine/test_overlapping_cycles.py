"""
Test script for overlapping cycle merging in ring_grouper.py.

This script demonstrates how accounts belonging to multiple cycles
are merged into a single ring with elevated risk scores.

Test scenario:
- Cycle 1: A → B → C → A
- Cycle 2: A → D → F → A
- Account A belongs to both cycles (should get +25 bonus)
- Both cycles should be merged into RING_001
"""

import networkx as nx
from ring_grouper import group_rings


def test_overlapping_cycles():
    """Test overlapping cycle merging with risk bonus."""
    
    # Create mock graph (not used in current implementation but kept for compatibility)
    G = nx.DiGraph()
    
    # Mock scores_dict
    scores_dict = {
        'A': {'score': 40, 'patterns': ['cycle_length_3']},
        'B': {'score': 40, 'patterns': ['cycle_length_3']},
        'C': {'score': 40, 'patterns': ['cycle_length_3']},
        'D': {'score': 40, 'patterns': ['cycle_length_3']},
        'F': {'score': 40, 'patterns': ['cycle_length_3']}
    }
    
    # Analysis results with overlapping cycles
    analysis_results = {
        'cycle_groups': [
            ['A', 'B', 'C'],  # Cycle 1
            ['A', 'D', 'F']   # Cycle 2 (shares A with Cycle 1)
        ],
        'smurfing_groups': [],
        'shell_groups': []
    }
    
    # Run ring grouping
    rings = group_rings(G, scores_dict, analysis_results)
    
    # Print results
    print("=== OVERLAPPING CYCLE MERGING TEST ===\n")
    
    print("Input:")
    print("  Cycle 1: A → B → C → A")
    print("  Cycle 2: A → D → F → A")
    print("  Account A belongs to BOTH cycles\n")
    
    print("Expected behavior:")
    print("  - Both cycles merged into single RING_001")
    print("  - Account A gets +25 risk bonus for multi-cycle membership")
    print("  - Members: [A, B, C, D, F]\n")
    
    print("Actual results:")
    for ring in rings:
        print(f"\nRing ID: {ring['ring_id']}")
        print(f"Pattern Type: {ring['pattern_type']}")
        print(f"Members: {ring['member_accounts']}")
        print(f"Risk Score: {ring['risk_score']}")
        
        # Calculate expected score
        base_avg = 40.0  # All accounts have score 40
        bonus = 25  # A is in 2 cycles, so +25 bonus
        expected = min(base_avg + bonus, 100)
        
        print(f"Expected Risk Score: {expected} (base {base_avg} + bonus {bonus})")
        
        if ring['risk_score'] == expected:
            print("✓ Risk score calculation CORRECT")
        else:
            print("✗ Risk score calculation INCORRECT")
    
    print("\n" + "="*50)


if __name__ == '__main__':
    test_overlapping_cycles()
