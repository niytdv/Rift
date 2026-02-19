# Risk Score Implementation - Simple Average Calculation

## Overview
Updated risk score calculation to use a simple average of member suspicion scores with no additional multipliers, structural weighting, or randomness.

## Implementation

### Location
**File**: `python-engine/main.py` - fraud_rings_output section

### Formula
```python
risk_score = round(sum(member_scores) / len(member_scores), 1)
```

Where:
- `member_scores` = list of `suspicion_score` values for all accounts in the ring
- No multipliers applied
- No structural weighting based on ring size or pattern type
- No randomness or variation
- Rounded to 1 decimal place

### Code
```python
# Calculate risk score as simple average of member suspicion scores
member_scores = []
for account_id in members:
    # Find this account's suspicion_score from suspicious_accounts list
    account_data = next((acc for acc in suspicious_accounts if acc['account_id'] == account_id), None)
    if account_data:
        member_scores.append(account_data['suspicion_score'])
    else:
        # If not in suspicious_accounts, calculate score
        detected_patterns = [...]
        score = calculate_suspicion_score(detected_patterns)
        member_scores.append(score)

# Simple average: sum(member_scores) / len(member_scores)
# No multipliers, no structural weighting, no randomness
risk_score = round(sum(member_scores) / len(member_scores), 1) if member_scores else 0.0
```

## Verification Example

### Ring: RING_001
**Members**: ACC001, ACC002, ACC003

**Member Suspicion Scores**:
- ACC001 = 70.0
- ACC002 = 100.0
- ACC003 = 100.0

**Calculation**:
```
risk_score = (70.0 + 100.0 + 100.0) / 3
risk_score = 270.0 / 3
risk_score = 90.0
```

**Result**: ✓ PASS

## JSON Schema Compliance

### Output Format
```json
{
  "fraud_rings": [
    {
      "ring_id": "RING_001",
      "member_accounts": ["ACC001", "ACC002", "ACC003"],
      "pattern_type": "cycle",
      "risk_score": 90.0
    }
  ]
}
```

### Requirements Met
- ✅ `risk_score` is a float with 1 decimal place
- ✅ Simple average calculation: `sum(scores) / count`
- ✅ No additional multipliers
- ✅ No structural weighting
- ✅ No randomness
- ✅ Deterministic output (same input = same output)
- ✅ snake_case keys
- ✅ RING_00X format for ring IDs

## API Float Formatting

### Implementation
**Files**: `app/api/sample/route.ts`, `app/api/analyze/route.ts`

### Regex Pattern
```typescript
jsonString.replace(
  /"(suspicion_score|risk_score|processing_time_seconds)":(\d+\.?\d*)([,\}])/g,
  (match, field, value, suffix) => {
    const num = parseFloat(value);
    return `"${field}":${num.toFixed(1)}${suffix}`;
  }
);
```

This ensures:
- `90` becomes `90.0`
- `90.0` stays `90.0`
- `90.5` stays `90.5`
- All numeric fields show exactly 1 decimal place

## Testing

### Test Command
```bash
python python-engine/main.py public/sample_data.csv
```

### Expected Output
```json
{
  "fraud_rings": [
    {
      "ring_id": "RING_001",
      "member_accounts": ["ACC001", "ACC002", "ACC003"],
      "pattern_type": "cycle",
      "risk_score": 90.0
    }
  ]
}
```

### API Test
```bash
curl -X POST http://localhost:3000/api/sample
```

Should return same format with `risk_score: 90.0`

## Key Changes

1. **Removed**: Complex risk calculation with multipliers
2. **Removed**: Structural weighting based on ring properties
3. **Removed**: Any randomness or variation
4. **Added**: Simple average of member suspicion scores
5. **Added**: Consistent rounding to 1 decimal place
6. **Added**: Deterministic calculation (same input = same output)

## Compliance Checklist

- [x] Simple average formula: `sum(scores) / count`
- [x] No multipliers
- [x] No structural weighting
- [x] No randomness
- [x] Float with 1 decimal place
- [x] Matches JSON schema
- [x] snake_case keys
- [x] RING_00X format
- [x] Deterministic output
- [x] API formatting preserved

## Files Modified

1. `python-engine/main.py` - Updated risk_score calculation
2. `app/api/sample/route.ts` - Added float formatting
3. `app/api/analyze/route.ts` - Added float formatting

## Result

✅ All tests pass
✅ Risk score = simple average of member suspicion scores
✅ No additional complexity
✅ Schema compliant
✅ Float formatting preserved in API responses
