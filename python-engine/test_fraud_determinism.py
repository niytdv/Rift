"""Test that fraud detection results (not timing) are deterministic."""
import subprocess
import json
import os

env = os.environ.copy()
env['PYTHONHASHSEED'] = '0'

print("Testing fraud detection determinism (excluding processing_time)...")
print("="*60)

outputs = []
for i in range(5):
    result = subprocess.run(
        ['python', 'python-engine/main.py', 'test_large.csv'],
        capture_output=True,
        text=True,
        env=env
    )
    data = json.loads(result.stdout)
    
    # Remove processing_time for comparison
    data['summary'].pop('processing_time_seconds', None)
    
    outputs.append(json.dumps(data, sort_keys=True))
    print(f"Run {i+1}/5... ✓")

print("\n" + "="*60)
print("FRAUD DETECTION DETERMINISM TEST")
print("="*60)

all_identical = all(output == outputs[0] for output in outputs)

if all_identical:
    print("✓ SUCCESS: All fraud detection results are IDENTICAL")
    print("  - suspicious_accounts: deterministic")
    print("  - fraud_rings: deterministic")
    print("  - detected_patterns: deterministic")
    print("  - risk_scores: deterministic")
    print("\n  Note: processing_time_seconds varies (expected)")
else:
    print("✗ FAILURE: Fraud detection results differ")
    for i in range(1, len(outputs)):
        if outputs[i] != outputs[0]:
            print(f"  Difference found between Run 1 and Run {i+1}")
