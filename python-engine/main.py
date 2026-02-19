import sys
from graph_builder import build_graph, prune_isolated_nodes
from detectors import detect_all_patterns

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <csv_path>", file=sys.stderr)
        sys.exit(1)

    csv_path = sys.argv[1]
    
    # Build graph
    G, df = build_graph(csv_path)
    
    # Prune isolated nodes
    G = prune_isolated_nodes(G)
    
    # Run detection algorithms
    results = detect_all_patterns(G)
    
    # Output results (can be formatted as needed)
    print(f"Cycle nodes: {len(results['cycle_nodes'])}")
    print(f"Velocity nodes: {len(results['velocity_nodes'])}")
    print(f"Peel nodes: {len(results['peel_nodes'])}")
    print(f"Cycle groups: {len(results['cycle_groups'])}")
    print(f"Peel groups: {len(results['peel_groups'])}")

if __name__ == "__main__":
    main()
