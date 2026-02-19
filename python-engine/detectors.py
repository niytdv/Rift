import networkx as nx
from datetime import timedelta
from collections import defaultdict
import pandas as pd

def detect_cycles(G, max_length=5, time_window_hours=72):
    """
    Detect cycles where all transactions occur within 72 hours.
    
    Returns:
        cycle_nodes: set of nodes involved in cycles
        cycle_groups: list of cycle node lists
        cycle_metadata: dict mapping account_id to pattern description
    """
    cycle_nodes = set()
    cycle_groups = []
    cycle_metadata = {}
    
    try:
        cycles = list(nx.simple_cycles(G))
    except:
        return cycle_nodes, cycle_groups, cycle_metadata
    
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
            
            # Add metadata
            for node in cycle:
                cycle_metadata[node] = f"cycle_length_{len(cycle)}"
    
    return cycle_nodes, cycle_groups, cycle_metadata

def is_merchant(G, node, df, long_term_days=30):
    """
    Check if a node is a legitimate merchant (long-term high-degree node).
    
    Criteria:
    - Consistent high volume over >30 days
    - High in-degree (many unique senders)
    """
    # Get all transactions involving this node
    node_txns = df[(df['sender_id'] == node) | (df['receiver_id'] == node)]
    
    if len(node_txns) == 0:
        return False
    
    # Check time span
    timestamps = pd.to_datetime(node_txns['timestamp'])
    time_span = (timestamps.max() - timestamps.min()).days
    
    if time_span < long_term_days:
        return False
    
    # Check if consistently high degree
    in_degree = G.in_degree(node)
    
    # Merchant threshold: >50 unique senders over 30+ days
    if in_degree > 50:
        return True
    
    return False

def detect_smurfing_fan_in(G, df, min_senders=10, burst_window_hours=72, velocity_ratio=0.7):
    """
    Detect Fan-In (Aggregation) smurfing patterns.
    
    Criteria:
    - unique_senders >= 10 within burst_window <= 72h
    - velocity_ratio >= 0.7 (Total Out / Total In)
    - Not a long-term merchant
    
    Returns:
        smurfing_nodes: set of collector nodes
        smurfing_groups: list of [collector + senders]
        smurfing_metadata: dict mapping account_id to pattern description
    """
    smurfing_nodes = set()
    smurfing_groups = []
    smurfing_metadata = {}
    
    for node in G.nodes():
        # Skip if merchant
        if is_merchant(G, node, df):
            continue
        
        # Get all incoming transactions
        predecessors = list(G.predecessors(node))
        
        if len(predecessors) < min_senders:
            continue
        
        # Check burst window
        incoming_txns = []
        for pred in predecessors:
            if G.has_edge(pred, node):
                edge_data = G[pred][node]
                incoming_txns.append({
                    'sender': pred,
                    'timestamp': edge_data['timestamp'],
                    'amount': edge_data['amount']
                })
        
        # Sort by timestamp
        incoming_txns.sort(key=lambda x: x['timestamp'])
        
        # Check for burst window
        for i in range(len(incoming_txns) - min_senders + 1):
            window_txns = incoming_txns[i:i + min_senders]
            time_span = window_txns[-1]['timestamp'] - window_txns[0]['timestamp']
            
            if time_span <= timedelta(hours=burst_window_hours):
                # Calculate velocity ratio
                total_in = sum(G[pred][node]['amount'] for pred in predecessors)
                total_out = sum(G[node][succ]['amount'] for succ in G.successors(node))
                
                if total_in == 0:
                    continue
                
                velocity = total_out / total_in
                
                if velocity >= velocity_ratio:
                    smurfing_nodes.add(node)
                    
                    # Create ring: collector + all senders in burst
                    burst_senders = [txn['sender'] for txn in window_txns]
                    ring_members = [node] + burst_senders
                    smurfing_groups.append(ring_members)
                    
                    # Add metadata
                    smurfing_metadata[node] = f"fan_in_{len(burst_senders)}_senders"
                    for sender in burst_senders:
                        smurfing_metadata[sender] = "fan_in_participant"
                    
                    break
    
    return smurfing_nodes, smurfing_groups, smurfing_metadata

def detect_smurfing_fan_out(G, df, min_receivers=10, burst_window_hours=72, velocity_ratio=0.7):
    """
    Detect Fan-Out (Dispersion) smurfing patterns.
    
    Criteria:
    - unique_receivers >= 10 within burst_window <= 72h
    - velocity_ratio >= 0.7 (Total Out / Total In)
    
    Returns:
        smurfing_nodes: set of disperser nodes
        smurfing_groups: list of [disperser + receivers]
        smurfing_metadata: dict mapping account_id to pattern description
    """
    smurfing_nodes = set()
    smurfing_groups = []
    smurfing_metadata = {}
    
    for node in G.nodes():
        # Get all outgoing transactions
        successors = list(G.successors(node))
        
        if len(successors) < min_receivers:
            continue
        
        # Check burst window
        outgoing_txns = []
        for succ in successors:
            if G.has_edge(node, succ):
                edge_data = G[node][succ]
                outgoing_txns.append({
                    'receiver': succ,
                    'timestamp': edge_data['timestamp'],
                    'amount': edge_data['amount']
                })
        
        # Sort by timestamp
        outgoing_txns.sort(key=lambda x: x['timestamp'])
        
        # Check for burst window
        for i in range(len(outgoing_txns) - min_receivers + 1):
            window_txns = outgoing_txns[i:i + min_receivers]
            time_span = window_txns[-1]['timestamp'] - window_txns[0]['timestamp']
            
            if time_span <= timedelta(hours=burst_window_hours):
                # Calculate velocity ratio
                total_in = sum(G[pred][node]['amount'] for pred in G.predecessors(node))
                total_out = sum(G[node][succ]['amount'] for succ in successors)
                
                if total_in == 0:
                    continue
                
                velocity = total_out / total_in
                
                if velocity >= velocity_ratio:
                    smurfing_nodes.add(node)
                    
                    # Create ring: disperser + all receivers in burst
                    burst_receivers = [txn['receiver'] for txn in window_txns]
                    ring_members = [node] + burst_receivers
                    smurfing_groups.append(ring_members)
                    
                    # Add metadata
                    smurfing_metadata[node] = f"fan_out_{len(burst_receivers)}_receivers"
                    for receiver in burst_receivers:
                        smurfing_metadata[receiver] = "fan_out_participant"
                    
                    break
    
    return smurfing_nodes, smurfing_groups, smurfing_metadata

def detect_velocity(G, pass_through_threshold=0.85, avg_time_hours=24):
    """
    Detect high-velocity pass-through accounts.
    
    Criteria:
    - pass_through_rate = total_out / total_in > 0.85
    - Average time between receive and send < 24 hours
    
    Returns:
        velocity_nodes: set of flagged nodes
        velocity_metadata: dict mapping account_id to pattern description
    """
    velocity_nodes = set()
    velocity_metadata = {}
    
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
                velocity_metadata[node] = "high_velocity"
    
    return velocity_nodes, velocity_metadata

def is_ghost_account(G, node, df, max_transactions=3):
    """
    Check if an account is a 'Ghost Account' (shell with no outside life).
    
    Criteria:
    - total_transactions <= 3
    - Not active outside detected chains
    
    Returns True if account is a ghost (potential shell)
    """
    # Count total transactions involving this node
    node_txns = df[(df['sender_id'] == node) | (df['receiver_id'] == node)]
    total_transactions = len(node_txns)
    
    # Ghost accounts have very few transactions
    if total_transactions > max_transactions:
        return False
    
    return True

def calculate_intermediate_velocity(G, node):
    """
    Calculate velocity window for intermediate node.
    
    velocity_window = outgoing_time - incoming_time
    
    Returns average velocity in hours
    """
    in_times = [G[pred][node]['timestamp'] for pred in G.predecessors(node)]
    out_times = [G[node][succ]['timestamp'] for succ in G.successors(node)]
    
    if not in_times or not out_times:
        return None
    
    # Calculate time between first incoming and first outgoing
    min_in = min(in_times)
    min_out = min(out_times)
    
    if min_out <= min_in:
        return 0
    
    velocity_hours = (min_out - min_in).total_seconds() / 3600
    return velocity_hours

def detect_peel_chains(G, df, min_length=3, time_window_hours=72, max_velocity_hours=24):
    """
    Detect shell/layering chains with strict temporal and behavioral criteria.
    
    Refined Criteria:
    1. Temporal Chain: max_timestamp - min_timestamp <= 72h
    2. Intermediate Velocity: velocity_window <= 24h (funds pass quickly)
    3. Ghost Account Filter: total_transactions <= 3, no outside life
    4. Strict amount decay (each hop < previous)
    
    Returns:
        peel_nodes: set of nodes in valid shell chains
        peel_groups: list of valid shell chain paths
        peel_metadata: dict mapping account_id to pattern description
    """
    peel_nodes = set()
    peel_groups = []
    peel_metadata = {}
    
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
                
                # 1. Check temporal chain constraint (72 hours)
                timestamps = []
                for i in range(len(path) - 1):
                    src = path[i]
                    dst = path[i + 1]
                    edge_data = G[src][dst]
                    timestamps.append(edge_data['timestamp'])
                
                if not timestamps:
                    continue
                
                time_span = max(timestamps) - min(timestamps)
                if time_span > timedelta(hours=time_window_hours):
                    # Chain spans more than 72h - considered 'Normal Business'
                    continue
                
                # 2. Check intermediate node velocity
                valid_chain = True
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
                        valid_chain = False
                        break
                    
                    # Check intermediate node velocity (for nodes in the middle)
                    if i > 0 and i < len(path) - 2:  # Intermediate nodes only
                        node = path[i]
                        velocity = calculate_intermediate_velocity(G, node)
                        
                        if velocity is not None and velocity > max_velocity_hours:
                            # Node 'parks' money for too long - less suspicious
                            valid_chain = False
                            break
                    
                    prev_amount = amount
                    prev_time = timestamp
                
                if not valid_chain:
                    continue
                
                # 3. Ghost Account Activity Filter
                # Check if intermediate nodes are ghost accounts
                ghost_chain = True
                for i in range(1, len(path) - 1):  # Check intermediate nodes only
                    node = path[i]
                    if not is_ghost_account(G, node, df):
                        # Account has outside life - not a shell
                        ghost_chain = False
                        break
                
                if not ghost_chain:
                    continue
                
                # Valid shell chain found
                peel_nodes.update(path)
                peel_groups.append(path)
                
                # Add metadata
                for node in path:
                    peel_metadata[node] = f"shell_hop_{len(path)}"
    
    return peel_nodes, peel_groups, peel_metadata

def detect_all_patterns(G, df):
    """
    Run all detection algorithms on the graph.
    
    Returns:
        Dictionary with all detection results including metadata
    """
    cycle_nodes, cycle_groups, cycle_metadata = detect_cycles(G)
    
    smurfing_fan_in_nodes, smurfing_fan_in_groups, smurfing_fan_in_metadata = detect_smurfing_fan_in(G, df)
    smurfing_fan_out_nodes, smurfing_fan_out_groups, smurfing_fan_out_metadata = detect_smurfing_fan_out(G, df)
    
    # Merge smurfing results
    smurfing_nodes = smurfing_fan_in_nodes | smurfing_fan_out_nodes
    smurfing_groups = smurfing_fan_in_groups + smurfing_fan_out_groups
    smurfing_metadata = {**smurfing_fan_in_metadata, **smurfing_fan_out_metadata}
    
    velocity_nodes, velocity_metadata = detect_velocity(G)
    peel_nodes, peel_groups, peel_metadata = detect_peel_chains(G, df)
    
    return {
        "cycle_nodes": cycle_nodes,
        "cycle_groups": cycle_groups,
        "cycle_metadata": cycle_metadata,
        "smurfing_nodes": smurfing_nodes,
        "smurfing_groups": smurfing_groups,
        "smurfing_metadata": smurfing_metadata,
        "velocity_nodes": velocity_nodes,
        "velocity_metadata": velocity_metadata,
        "shell_nodes": peel_nodes,
        "shell_groups": peel_groups,
        "shell_metadata": peel_metadata
    }
