"""
Wrapper to run main.py with PYTHONHASHSEED=0 for deterministic output.
"""
import os
import sys
import subprocess

# Set hash seed to 0 for deterministic dict/set iteration
os.environ['PYTHONHASHSEED'] = '0'

# Run main.py with the same arguments
if len(sys.argv) < 2:
    print("Usage: python run_deterministic.py <csv_path>")
    sys.exit(1)

csv_path = sys.argv[1]

# Run with PYTHONHASHSEED=0
result = subprocess.run(
    ['python', 'python-engine/main.py', csv_path],
    env={**os.environ, 'PYTHONHASHSEED': '0'}
)

sys.exit(result.returncode)
