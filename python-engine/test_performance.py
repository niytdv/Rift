"""
Performance test for MuleRift fraud detection on large datasets.
Generates test data and measures processing time.
"""
import pandas as pd
import random
import time
from datetime import datetime, timedelta
import sys

def generate_large_test_data(num_transactions=12000, output_file='test_large.csv'):
    """Generate a large test dataset with various fraud patterns."""
    print(f"Generating {num_transactions} transactions...")
    
    transactions = []
    txn_id = 1
    base_time = datetime(2024, 1, 1, 0, 0, 0)
    
    # Generate cycles (10 cycles of 3 accounts each)
    for cycle_num in range(10):
        acc_base = 1000 + (cycle_num * 10)
        acc_a = f"ACC_{acc_base:05d}"
        acc_b = f"ACC_{acc_base+1:05d}"
        acc_c = f"ACC_{acc_base+2:05d}"
        
        # A -> B -> C -> A within 72 hours
        t1 = base_time + timedelta(hours=cycle_num * 100)
        transactions.append({
            'transaction_id': f"TXN_{txn_id:08d}",
            'sender_id': acc_a,
            'receiver_id': acc_b,
            'amount': round(random.uniform(10000, 20000), 2),
            'timestamp': t1.strftime('%Y-%m-%d %H:%M:%S')
        })
        txn_id += 1
        
        t2 = t1 + timedelta(hours=24)
        transactions.append({
            'transaction_id': f"TXN_{txn_id:08d}",
            'sender_id': acc_b,
            'receiver_id': acc_c,
            'amount': round(random.uniform(9500, 19500), 2),
            'timestamp': t2.strftime('%Y-%m-%d %H:%M:%S')
        })
        txn_id += 1
        
        t3 = t2 + timedelta(hours=24)
        transactions.append({
            'transaction_id': f"TXN_{txn_id:08d}",
            'sender_id': acc_c,
            'receiver_id': acc_a,
            'amount': round(random.uniform(9000, 19000), 2),
            'timestamp': t3.strftime('%Y-%m-%d %H:%M:%S')
        })
        txn_id += 1
    
    # Generate smurfing patterns (5 fan-in patterns)
    for smurf_num in range(5):
        collector = f"SMURF_{smurf_num:03d}"
        t_base = base_time + timedelta(hours=smurf_num * 200)
        
        # 15 senders -> 1 collector within 72 hours
        for sender_num in range(15):
            sender = f"ACC_{2000 + smurf_num * 20 + sender_num:05d}"
            t = t_base + timedelta(hours=sender_num * 4)
            transactions.append({
                'transaction_id': f"TXN_{txn_id:08d}",
                'sender_id': sender,
                'receiver_id': collector,
                'amount': round(random.uniform(500, 2000), 2),
                'timestamp': t.strftime('%Y-%m-%d %H:%M:%S')
            })
            txn_id += 1
    
    # Fill remaining with random normal transactions
    remaining = num_transactions - len(transactions)
    print(f"Generated {len(transactions)} pattern transactions, adding {remaining} normal transactions...")
    
    for i in range(remaining):
        sender = f"ACC_{random.randint(5000, 9999):05d}"
        receiver = f"ACC_{random.randint(5000, 9999):05d}"
        
        if sender == receiver:
            receiver = f"ACC_{random.randint(5000, 9999):05d}"
        
        t = base_time + timedelta(hours=random.randint(0, 720))
        transactions.append({
            'transaction_id': f"TXN_{txn_id:08d}",
            'sender_id': sender,
            'receiver_id': receiver,
            'amount': round(random.uniform(100, 50000), 2),
            'timestamp': t.strftime('%Y-%m-%d %H:%M:%S')
        })
        txn_id += 1
    
    # Create DataFrame and save
    df = pd.DataFrame(transactions)
    df.to_csv(output_file, index=False)
    print(f"Generated {len(transactions)} transactions -> {output_file}")
    return output_file

if __name__ == "__main__":
    # Generate test data
    num_txns = 12000 if len(sys.argv) < 2 else int(sys.argv[1])
    test_file = generate_large_test_data(num_txns)
    
    # Run analysis
    print(f"\nRunning fraud detection on {num_txns} transactions...")
    start = time.time()
    
    import subprocess
    result = subprocess.run(
        ['python', 'python-engine/main.py', test_file],
        capture_output=True,
        text=True
    )
    
    elapsed = time.time() - start
    
    print(f"\n{'='*60}")
    print(f"PERFORMANCE TEST RESULTS")
    print(f"{'='*60}")
    print(f"Transactions: {num_txns}")
    print(f"Processing Time: {elapsed:.2f} seconds")
    print(f"Throughput: {num_txns/elapsed:.0f} transactions/second")
    print(f"{'='*60}")
    
    if elapsed > 30:
        print(f"⚠️  WARNING: Processing took {elapsed:.2f}s (target: <30s)")
    else:
        print(f"✓ SUCCESS: Processing completed in {elapsed:.2f}s")
    
    # Show summary from output
    if result.returncode == 0:
        import json
        output = json.loads(result.stdout)
        summary = output['summary']
        print(f"\nDetection Summary:")
        print(f"  Accounts Analyzed: {summary['total_accounts_analyzed']}")
        print(f"  Suspicious Accounts: {summary['suspicious_accounts_flagged']}")
        print(f"  Fraud Rings: {summary['fraud_rings_detected']}")
    else:
        print(f"\n❌ ERROR: {result.stderr}")
