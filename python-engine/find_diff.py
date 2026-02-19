"""Find exact difference between two JSON outputs."""
import subprocess
import os

env = os.environ.copy()
env['PYTHONHASHSEED'] = '0'

# Run twice
result1 = subprocess.run(['python', 'python-engine/main.py', 'test_large.csv'], 
                        capture_output=True, text=True, env=env)
result2 = subprocess.run(['python', 'python-engine/main.py', 'test_large.csv'], 
                        capture_output=True, text=True, env=env)

out1 = result1.stdout
out2 = result2.stdout

print(f"Length 1: {len(out1)}, Length 2: {len(out2)}")

if out1 == out2:
    print("✓ IDENTICAL")
else:
    print("✗ DIFFERENT")
    # Find first difference
    for i, (c1, c2) in enumerate(zip(out1, out2)):
        if c1 != c2:
            print(f"\nFirst difference at position {i}:")
            print(f"Context: ...{out1[max(0,i-100):i+100]}...")
            print(f"\nChar 1: {repr(c1)}")
            print(f"Char 2: {repr(c2)}")
            break
