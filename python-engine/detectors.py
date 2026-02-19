import networkx as nx
from datetime import timedelta
from collections import defaultdict
from datetime import timedelta

def detect_cycles(G, max_length=5, time_window_hours=72):
    """
    Detect cycles where all transactions occur within 72 hours.
    
    Returns:
        cycle_nodes: set of nodes involved in cycles
        cycle_groups: list of cycle node lists
    """
    cycle_nodes = set()
    cycle_groups = []
    
    try:
        cycles = list(nx.simple_cycles(G))
    except:
        return cycle_nodes, cycle_groups
    
    for cycle in cycles:
        if len(cycle) > max_length:
            continue
        
        # Get all edges in the cycle
        edges = []
        for i in range(len(cycle)):
            src = cycle[i]
            dst = cycle[(i + 1) % len(cycle)]
            
            if G.has_edge(src, dst):
                edge_data = G[src][dst]
                edges.append(edge_data)
        
        if not edges:
            continue
        
        # Check temporal constraint
        timestamps = [edge['timestamp'] for edge in edges]
        time_span = max(timestamps) - min(timestamps)
        
        if time_span <= timedelta(hours=time_window_hours):
            cycle_nodes.update(cycle)
            cycle_groups.append(list(cycle))
    
    return cycle_nodes, cycle_groups

def detect_velocity(G, pass_through_threshold=0.85, avg_time_hours=24):
    """
    Detect high-velocity pass-through accounts.
    
    Criteria:
    - pass_through_rate = total_out / total_in > 0.85
    - Average time between receive and send < 24 hours
    
    Returns:
        velocity_nodes: set of flagged nodes
    """
    velocity_nodes = set()
    
    for node in G.nodes():
        # Calculate total in and out
        total_in = sum(G[pred][node]['amount'] for pred in G.predecessors(node))
        total_out = sum(G[node][succ]['amount'] for succ in G.successors(node))
        
        if total_in == 0:
            continue
        
        pass_through_rate = total_out / total_in
        
        if pass_through_rate <= pass_through_threshold:
            continue
        
        # Calculate average time between receive and send
        in_times = [G[pred][node]['timestamp'] for pred in G.predecessors(node)]
        out_times = [G[node][succ]['timestamp'] for succ in G.successors(node)]
        
        if not in_times or not out_times:
            continue
        
        # Average time from first receive to first send
        time_diffs = []
        for in_time in in_times:
            for out_time in out_times:
                if out_time > in_time:
                    time_diffs.append((out_time - in_time).total_seconds() / 3600)
        
        if time_diffs:
            avg_time = sum(time_diffs) / len(time_diffs)
            if avg_time < avg_time_hours:
                velocity_nodes.add(node)
    
    return velocity_nodes

def detect_peel_chains(G, min_length=3, time_window_hours=12):
    """
    Detect peel chains with strict amount decay.
    
    Criteria:
    - Path length >= 3
    - Strict amount decay (each hop < previous)
    - Time between hops < 12 hours
    
    Returns:
        peel_nodes: set of nodes in peel chains
        peel_groups: list of peel chain paths
    """
    peel_nodes = set()
    peel_groups = []
    
    # Find all simple paths up to reasonable length
    for source in G.nodes():
        for target in G.nodes():
            if source == target:
                continue
            
            try:
                paths = list(nx.all_simple_paths(G, source, target, cutoff=10))
            except:
                continue
            
            for path in paths:
                if len(path) < min_length:
                    continue
                
                # Check amount decay and time constraints
                is_valid_peel = True
                prev_amount = None
                prev_time = None
                
                for i in range(len(path) - 1):
                    src = path[i]
                    dst = path[i + 1]
                    
                    edge_data = G[src][dst]
                    amount = edge_data['amount']
                    timestamp = edge_data['timestamp']
                    
                    # Check strict amount decay
                    if prev_amount is not None and amount >= prev_amount:
                        is_valid_peel = False
                        break
                    
                    # Check time window
                    if prev_time is not None:
                        time_diff = (timestamp - prev_time).total_seconds() / 3600
                        if time_diff >= time_window_hours:
                            is_valid_peel = False
                            break
                    
                    prev_amount = amount
                    prev_time = timestamp
                
                if is_valid_peel:
                    peel_nodes.update(path)
                    peel_groups.append(path)
    
    return peel_nodes, peel_groups

def detect_all_patterns(G):
    """
    Run all detection algorithms on the graph.
    
    Returns:
        Dictionary with all detection results
    """
    cycle_nodes, cycle_groups = detect_cycles(G)
    velocity_nodes = detect_velocity(G)
    peel_nodes, peel_groups = detect_peel_chains(G)
    
    return {
        "cycle_nodes": cycle_nodes,
        "velocity_nodes": velocity_nodes,
        "peel_nodes": peel_nodes,
        "cycle_groups": cycle_groups,
        "peel_groups": peel_groups
    }
