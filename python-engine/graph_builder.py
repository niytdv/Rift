import pandas as pd
import networkx as nx
from datetime import datetime

def build_graph(csv_path):
    """Build directed transaction graph from CSV.
    
    Expected CSV columns: from_account, to_account, amount, timestamp
    Returns: (NetworkX DiGraph, DataFrame)
    """
    df = pd.read_csv(csv_path)
    
    # Validate required columns
    required_cols = ['from_account', 'to_account', 'amount', 'timestamp']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Parse timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Build directed graph
    G = nx.DiGraph()
    
    for _, row in df.iterrows():
        from_acc = row['from_account']
        to_acc = row['to_account']
        amount = float(row['amount'])
        timestamp = row['timestamp']
        
        # Add nodes if they don't exist
        if not G.has_node(from_acc):
            G.add_node(from_acc)
        if not G.has_node(to_acc):
            G.add_node(to_acc)
        
        # Add edge with transaction data
        # Support multiple transactions between same accounts
        if G.has_edge(from_acc, to_acc):
            # Append to existing transactions
            G[from_acc][to_acc]['transactions'].append({
                'amount': amount,
                'timestamp': timestamp
            })
            G[from_acc][to_acc]['total_amount'] += amount
        else:
            G.add_edge(from_acc, to_acc, 
                      transactions=[{'amount': amount, 'timestamp': timestamp}],
                      total_amount=amount)
    
    return G, df
