# Smurfing Detection Implementation - Fan-In/Fan-Out Patterns

## Overview
Implemented complex pattern detection for money muling networks using forensic thresholds for Fan-In (Aggregation) and Fan-Out (Dispersion) smurfing patterns.

## Implementation Details

### 1. Fan-In (Aggregation) Detection
**File**: `python-engine/detectors.py` - `detect_smurfing_fan_in()`

**Criteria**:
- `unique_senders >= 10` within `burst_window <= 72 hours`
- `velocity_ratio >= 0.7` (Total Out / Total In)
- **Merchant Filter**: Excludes long-term high-degree nodes (>50 unique senders over 30+ days)

**Logic**:
```python
For every receiver node R:
  1. Check if R has >= 10 unique senders
  2. Find burst window where 10+ transactions occur within 72h
  3. Calculate velocity_ratio = total_out / total_in
  4. If velocity_ratio >= 0.7 and not a merchant:
     - Mark as smurfing_fan_in
     - Create ring: {R + all senders in burst}
```

**Pattern Metadata**: `fan_in_{N}_senders` where N = number of senders

### 2. Fan-Out (Dispersion) Detection
**File**: `python-engine/detectors.py` - `detect_smurfing_fan_out()`

**Criteria**:
- `unique_receivers >= 10` within `burst_window <= 72 hours`
- `velocity_ratio >= 0.7` (Total Out / Total In)

**Logic**:
```python
For every sender node S:
  1. Check if S has >= 10 unique receivers
  2. Find burst window where 10+ transactions occur within 72h
  3. Calculate velocity_ratio = total_out / total_in
  4. If velocity_ratio >= 0.7:
     - Mark as smurfing_fan_out
     - Create ring: {S + all receivers in burst}
```

**Pattern Metadata**: `fan_out_{N}_receivers` where N = number of receivers

### 3. Ring Merging & Deterministic Sorting
**File**: `python-engine/ring_grouper.py`

**Merging Logic**:
- If a node is a 'Collector' in Fan-In AND 'Participant' in a Cycle:
  - Merge all involved accounts into ONE single Ring ID
- Uses set intersection to detect overlapping rings
- Iteratively merges until no more overlaps exist

**Deterministic Sorting**:
1. Sort members alphabetically within each ring
2. Sort rings by their smallest member (lexicographically)
3. Assign RING_001, RING_002, etc. in sorted order

**Pattern Priority** (for merged rings):
- Cycle > Smurfing > Shell

### 4. Scoring System
**File**: `python-engine/main.py` - `calculate_suspicion_score()`

**Pattern Weights**:
- Cycle: +40 points
- **Smurfing: +40 points** (base boost as specified)
- Shell: +30 points
- Velocity: +30 points

**Maximum Score**: 100 (capped)

## Frontend Impact

### Hub-and-Spoke Visualization
**Fan-In Pattern**:
```
SENDER01 ──┐
SENDER02 ──┤
SENDER03 ──┤
   ...     ├──> [COLLECTOR_A] (Neon Red Hub)
SENDER10 ──┤
SENDER11 ──┤
SENDER12 ──┘
```

**Fan-Out Pattern**:
```
                    ┌──> RECV01
                    ├──> RECV02
[DISPERSER_B] ──────┤──> RECV03
(Neon Red Hub)      ├──> ...
                    ├──> RECV10
                    └──> RECV12
```

### "Structural Collapse" Feature
When user clicks central hub node:
1. **Isolate Ring** feature highlights all 10+ connected nodes simultaneously
2. Demonstrates detection of entire criminal cell, not just one suspicious account
3. Visual representation shows the complete money muling network structure

## Data Contract Compliance

All outputs follow MuleRift Data Contract:
- ✅ `snake_case` keys
- ✅ `suspicion_score`: float with 1 decimal (e.g., 100.0, 70.0)
- ✅ `risk_score`: float with 1 decimal (e.g., 90.0, 40.0)
- ✅ `ring_id`: Format RING_001, RING_002, etc.
- ✅ `pattern_type`: "cycle", "smurfing", or "shell"
- ✅ `processing_time_seconds`: float with 1 decimal

## Testing

### Sample Dataset
**File**: `public/sample_data.csv`

Contains:
- 12 senders → 1 collector (Fan-In pattern)
- 1 disperser → 12 receivers (Fan-Out pattern)
- 1 cycle pattern (3 nodes)
- All within 72-hour burst windows
- Velocity ratios > 0.7

### Expected Detection
- **COLLECTOR_A**: Fan-In hub with 12 senders
- **DISPERSER_B**: Fan-Out hub with 12 receivers
- **ACC001-ACC003**: Cycle pattern
- Merged rings if nodes participate in multiple patterns

## API Endpoints

All endpoints return data with smurfing detection:
- `POST /api/sample` - Run sample data analysis
- `POST /api/analyze` - Upload custom CSV
- `GET /api/health` - Health check

## Dashboard URLs
- Main: http://localhost:3000
- Dashboard: http://localhost:3000/dashboard

## Key Files Modified
1. `python-engine/detectors.py` - Added Fan-In/Fan-Out detection
2. `python-engine/ring_grouper.py` - Added merging & sorting logic
3. `python-engine/main.py` - Updated scoring (+40 for smurfing)
4. `public/sample_data.csv` - Sample data with smurfing patterns

## Forensic Thresholds Summary
| Parameter | Value | Purpose |
|-----------|-------|---------|
| min_senders/receivers | 10 | Minimum connections for smurfing |
| burst_window | 72 hours | Time window for burst detection |
| velocity_ratio | 0.7 | Pass-through threshold |
| merchant_threshold | 50 senders | Exclude legitimate businesses |
| merchant_timespan | 30 days | Long-term activity check |

## Next Steps for Frontend
1. Implement hub-and-spoke visualization for smurfing patterns
2. Add "Isolate Ring" feature to highlight all connected nodes
3. Color-code central hubs (collectors/dispersers) in neon red
4. Show pattern metadata on node hover (fan_in_12_senders, etc.)
5. Demonstrate "Structural Collapse" reveal for judges
