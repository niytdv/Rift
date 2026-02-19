"""
Test deterministic output - run analysis multiple times and compare results.
"""
import subprocess
import json
import sys
import os

def run_analysis(csv_file):
    """Run analysis and return JSON output with PYTHONHASHSEED=0."""
    env = os.environ.copy()
    env['PYTHONHASHSEED'] = '0'  # Force deterministic hash seed
    
    result = subprocess.run(
        ['python', 'python-engine/main.py', csv_file],
        capture_output=True,
        text=True,
        env=env
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout

def main():
    csv_file = sys.argv[1] if len(sys.argv) > 1 else 'data.csv'
    num_runs = 5
    
    print(f"Testing determinism with {num_runs} runs on {csv_file}...")
    print("="*60)
    
    outputs = []
    for i in range(num_runs):
        print(f"Run {i+1}/{num_runs}...", end=' ')
        output = run_analysis(csv_file)
        if output:
            outputs.append(output)
            print("✓")
        else:
            print("✗")
            return
    
    # Compare all outputs
    print("\n" + "="*60)
    print("DETERMINISM TEST RESULTS")
    print("="*60)
    
    all_identical = all(output == outputs[0] for output in outputs)
    
    if all_identical:
        print("✓ SUCCESS: All outputs are IDENTICAL")
        print(f"  - {num_runs} runs produced byte-for-byte identical JSON")
        print(f"  - Output length: {len(outputs[0])} bytes")
        
        # Parse and show summary
        data = json.loads(outputs[0])
        print(f"\nOutput Summary:")
        print(f"  - Suspicious Accounts: {data['summary']['suspicious_accounts_flagged']}")
        print(f"  - Fraud Rings: {data['summary']['fraud_rings_detected']}")
        print(f"  - Processing Time: {data['summary']['processing_time_seconds']}s")
    else:
        print("✗ FAILURE: Outputs differ between runs")
        for i, output in enumerate(outputs):
            print(f"  Run {i+1} length: {len(output)} bytes")
        
        # Find first difference
        for i in range(1, len(outputs)):
            if outputs[i] != outputs[0]:
                print(f"\nFirst difference found between Run 1 and Run {i+1}")
                # Show first 500 chars of each
                print(f"\nRun 1 (first 500 chars):\n{outputs[0][:500]}")
                print(f"\nRun {i+1} (first 500 chars):\n{outputs[i][:500]}")
                break

if __name__ == "__main__":
    main()
