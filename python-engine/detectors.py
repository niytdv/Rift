import networkx as nx
from collections import defaultdict
from datetime import timedelta

def detect_cycles(G):
    """Detect all cycles in the transaction graph.
    
    Returns: List of cycles, where each cycle is a list of account IDs
    """
    try:
        # Find all simple cycles (length >= 3)
        cycles = list(nx.simple_cycles(G))
        # Filter to cycles of length 3 or more
        cycles = [cycle for cycle in cycles if len(cycle) >= 3]
        return cycles
    except:
        return []

def detect_temporal_velocity(G, df):
    """Detect accounts with rapid pass-through (funds in/out within 72 hours).
    
    Returns: Dict mapping account_id to list of velocity events
    """
    velocity_events = defaultdict(list)
    
    for account in G.nodes():
        # Get incoming transactions
        incoming = []
        for pred in G.predecessors(account):
            edge_data = G[pred][account]
            for txn in edge_data['transactions']:
                incoming.append({
                    'from': pred,
                    'amount': txn['amount'],
                    'timestamp': txn['timestamp']
                })
        
        # Get outgoing transactions
        outgoing = []
        for succ in G.successors(account):
            edge_data = G[account][succ]
            for txn in edge_data['transactions']:
                outgoing.append({
                    'to': succ,
                    'amount': txn['amount'],
                    'timestamp': txn['timestamp']
                })
        
        # Check for rapid pass-through (within 72 hours)
        for in_txn in incoming:
            for out_txn in outgoing:
                time_diff = abs((out_txn['timestamp'] - in_txn['timestamp']).total_seconds())
                hours_diff = time_diff / 3600
                
                if hours_diff <= 72 and out_txn['timestamp'] >= in_txn['timestamp']:
                    velocity_events[account].append({
                        'from_account': in_txn['from'],
                        'to_account': out_txn['to'],
                        'in_amount': in_txn['amount'],
                        'out_amount': out_txn['amount'],
                        'hours': round(hours_diff, 2),
                        'in_timestamp': in_txn['timestamp'].isoformat(),
                        'out_timestamp': out_txn['timestamp'].isoformat()
                    })
    
    return velocity_events

def detect_all_patterns(G, df):
    """Run all detection algorithms and return results.
    
    Returns: Dict with 'cycles' and 'velocity' keys
    """
    cycles = detect_cycles(G)
    velocity = detect_temporal_velocity(G, df)
    
    return {
        'cycles': cycles,
        'velocity': velocity
    }
