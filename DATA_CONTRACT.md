# MuleRift Locked Data Contract

## Overview
This document defines the **immutable data contract** between the Python backend and Next.js frontend for MuleRift analysis results.

## Contract Version: 1.0

### Root Structure
```json
{
  "suspicious_accounts": [...],
  "fraud_rings": [...],
  "summary": {...}
}
```

### 1. suspicious_accounts (Array)

Each account object contains:

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `account_id` | string | Unique account identifier | Required, non-empty |
| `suspicion_score` | float | Risk score (0-100) | **Must be weighted average** of detected patterns |
| `detected_patterns` | string[] | Array of pattern identifiers | Format: `pattern_type:count` |
| `ring_id` | string | Associated fraud ring ID | Format: `RING_00X` or empty string |

**Example:**
```json
{
  "account_id": "ACC001",
  "suspicion_score": 56.0,
  "detected_patterns": [
    "cycle_participation:1",
    "temporal_velocity:1"
  ],
  "ring_id": "RING_001"
}
```

### 2. fraud_rings (Array)

Each ring object contains:

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `ring_id` | string | Unique ring identifier | **Format: `RING_00X`** (3 digits) |
| `member_accounts` | string[] | Array of account IDs in ring | Minimum 2 members |
| `pattern_type` | string | Type of fraud pattern | **Must be: `cycle`, `smurfing`, or `shell`** |
| `risk_score` | float | Aggregated risk (0-100) | Average of member suspicion scores |

**Example:**
```json
{
  "ring_id": "RING_001",
  "member_accounts": ["ACC001", "ACC002", "ACC003"],
  "pattern_type": "cycle",
  "risk_score": 64.0
}
```

### 3. summary (Object)

| Field | Type | Description |
|-------|------|-------------|
| `total_accounts_analyzed` | int | Total number of accounts processed |
| `suspicious_accounts_flagged` | int | Accounts with suspicion_score > 50 |
| `fraud_rings_detected` | int | Number of fraud rings identified |
| `processing_time_seconds` | float | Analysis duration in seconds |

**Example:**
```json
{
  "total_accounts_analyzed": 14,
  "suspicious_accounts_flagged": 11,
  "fraud_rings_detected": 4,
  "processing_time_seconds": 0.023
}
```

## Critical Rules

### 1. Naming Convention
- **ALL keys MUST use snake_case**
- ❌ NEVER use camelCase (e.g., `suspicionScore`)
- ✅ ALWAYS use snake_case (e.g., `suspicion_score`)

### 2. Suspicion Score Calculation
The `suspicion_score` **MUST** be calculated as a weighted average:

```python
weights = {
    'cycle_participation': 0.6,  # 60% weight
    'temporal_velocity': 0.4     # 40% weight
}

suspicion_score = (cycle_score * 0.6 + velocity_score * 0.4) / total_weight
```

### 3. Ring ID Format
- Format: `RING_` + 3-digit zero-padded number
- Examples: `RING_001`, `RING_042`, `RING_999`
- ❌ Invalid: `RING_1`, `ring_001`, `RING-001`

### 4. Pattern Types
Valid values for `pattern_type`:
- `cycle` - Transaction cycles (A → B → C → A)
- `smurfing` - Structured layering (future)
- `shell` - Shell account networks (future)

## Implementation Status

### Python Backend (✅ Compliant)
- `output.py` - Generates contract-compliant JSON
- `scoring.py` - Implements weighted average calculation
- `ring_grouper.py` - Formats ring_id correctly

### TypeScript Frontend (✅ Compliant)
- `lib/types.ts` - Defines contract interfaces
- `components/SummaryStats.tsx` - Uses snake_case keys
- `components/FraudRingTable.tsx` - Displays contract data
- `components/AccountModal.tsx` - Shows contract fields

## Validation

### Python Output Validation
```bash
python python-engine/main.py public/sample_data.csv | jq '.suspicious_accounts[0]'
```

Expected keys: `account_id`, `suspicion_score`, `detected_patterns`, `ring_id`

### TypeScript Type Checking
```bash
npm run build
```

Should compile without type errors when using contract interfaces.

## Breaking Changes Policy

⚠️ **This contract is LOCKED**. Any changes require:
1. Version increment
2. Migration guide
3. Backward compatibility layer
4. Team approval

## Contact

For contract questions or change requests, contact the Lead Architect.
