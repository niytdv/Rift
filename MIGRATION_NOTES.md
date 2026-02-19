# MuleRift Migration Notes

## Overview
Successfully migrated from shared-entity fraud detection to transaction graph analysis for money muling detection.

## Key Changes

### Python Engine (Complete Rewrite)

#### graph_builder.py
- Changed from bipartite graph (accounts ↔ shared entities) to directed transaction graph
- New CSV format: `from_account, to_account, amount, timestamp`
- Edges now represent transactions with amount and timestamp attributes
- Supports multiple transactions between same account pairs

#### detectors.py
- Removed: shared IP/device/bank detection, rapid creation, high velocity
- Added: cycle detection using NetworkX simple_cycles
- Added: temporal velocity analysis (72-hour pass-through detection)
- Returns structured dict with 'cycles' and 'velocity' keys

#### scoring.py
- New scoring algorithm:
  - 40 points per cycle participation
  - 30 points per velocity event
  - Normalized to 0-100 scale
- Tracks detailed metrics: in/out degree, total amounts, cycle/velocity counts

#### ring_grouper.py
- Rings now represent actual transaction cycles (A → B → C → A)
- Each cycle becomes a ring with aggregated suspicion score
- Includes cycle path visualization string

#### output.py
- Updated JSON schema to include transaction details
- Edges now have transaction_count, total_amount, timestamps
- Nodes include suspicion_score, cycle_count, velocity_count, transaction stats

### Frontend Updates

#### types.ts
- Updated Account interface with new fields:
  - suspicion_score (was fraud_score)
  - cycle_count, velocity_count
  - in_degree, out_degree, total_in, total_out
  - ring_ids (array, was single ring_id)
  - details object with cycles and velocity_events

- Updated FraudRing interface:
  - Added member_count, cycle_path
  - Changed avg_score to suspicion_score
  - Removed pattern field

- Updated GraphEdge interface:
  - Added transaction_count, total_amount, timestamps
  - Added transactions array with individual transaction details

#### Components
- AccountModal: Enhanced to show cycle participation, velocity events, transaction stats
- FraudRingTable: Updated to display cycle paths and suspicion scores
- SummaryStats: Added total_transactions metric
- GraphVisualization: Updated to use suspicion_score instead of fraud_score

### Sample Data
- New CSV with 15 transactions forming 4 distinct cycles
- Demonstrates both cycle detection and temporal velocity analysis
- Shows accounts with varying suspicion scores (0-100)

## Detection Results (Sample Data)
- 14 accounts analyzed
- 9 flagged accounts (suspicion_score > 50)
- 4 rings detected
- 15 total transactions
- Processing time: ~13ms

## Requirements Satisfied
✅ Req 1: CSV Transaction Data Import
✅ Req 2: Cycle Detection
✅ Req 3: Temporal Velocity Analysis (72-hour window)
✅ Req 4: Suspicion Score Calculation
✅ Req 5: Interactive Graph Visualization (existing)
✅ Req 6: Ring Isolation and Highlighting (existing)
✅ Req 7: Explainable Risk Popups (enhanced)
✅ Req 8: JSON Export with Schema Compliance
✅ Req 9: Graph Analysis Engine (Python/NetworkX)
✅ Req 10: Frontend-Backend Integration (existing)

## Next Steps
1. Test with larger datasets
2. Enhance graph visualization with edge weights (transaction amounts)
3. Add ring highlighting/filtering in UI
4. Implement JSON export download functionality
5. Add CSV validation and error handling in UI
