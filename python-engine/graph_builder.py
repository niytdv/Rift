import pandas as pd
import networkx as nx
from datetime import datetime

def build_graph(csv_path):
    """
    Build a directed graph from transaction CSV.
    
    Returns:
        G: NetworkX DiGraph with transaction edges
        df: Original DataFrame
    """
    df = pd.read_csv(csv_path)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    G = nx.DiGraph()
    
    # Add edges with attributes
    for _, row in df.iterrows():
        G.add_edge(
            row['sender_id'],
            row['receiver_id'],
            amount=float(row['amount']),
            timestamp=row['timestamp'],
            transaction_id=row['transaction_id']
        )
    
    return G, df

def prune_isolated_nodes(G):
    """
    Remove nodes with in_degree == 0 OR out_degree == 0.
    
    Returns:
        Pruned graph
    """
    nodes_to_remove = [
        node for node in G.nodes()
        if G.in_degree(node) == 0 or G.out_degree(node) == 0
    ]
    
    G.remove_nodes_from(nodes_to_remove)
    return G
