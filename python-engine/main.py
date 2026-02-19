import sys
import time
import json
from graph_builder import build_graph
from detectors import detect_all_patterns
from scoring import calculate_scores
from ring_grouper import group_rings
from output import generate_json_output

def main():
    """MuleRift - Graph-based money muling detection engine.
    
    Analyzes transaction CSV to detect:
    - Cycles in transaction flow (A → B → C → A)
    - Temporal velocity (rapid pass-through within 72 hours)
    - Suspicion scores combining structural and temporal signals
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <csv_path>", file=sys.stderr)
        sys.exit(1)

    csv_path = sys.argv[1]
    start_time = time.time()

    try:
        # Build transaction graph
        graph, df = build_graph(csv_path)
        
        # Detect patterns (cycles and velocity)
        patterns = detect_all_patterns(graph, df)
        
        # Calculate suspicion scores
        accounts = calculate_scores(graph, patterns)
        
        # Group cycles into rings
        rings = group_rings(accounts, patterns)
        
        # Generate output
        processing_time = int((time.time() - start_time) * 1000)
        output = generate_json_output(accounts, rings, graph, processing_time)
        
        print(output)
    
    except Exception as e:
        error_output = {
            'error': str(e),
            'message': 'Failed to process transaction data'
        }
        print(json.dumps(error_output), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
