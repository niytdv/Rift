# MuleRift Contract Quick Reference

## For Developers

### Python: Generating Contract Output

```python
from output import generate_json_output

# Your analysis results
accounts = [...]  # List of account dicts
rings = [...]     # List of ring dicts
graph = ...       # NetworkX graph
processing_time = 123  # milliseconds

# Generate contract-compliant JSON
json_output = generate_json_output(accounts, rings, graph, processing_time)
print(json_output)
```

### TypeScript: Consuming Contract Data

```typescript
import { AnalysisResult, SuspiciousAccount, FraudRing } from '@/lib/types';

// Parse API response
const result: AnalysisResult = await response.json();

// Access data
const accounts: SuspiciousAccount[] = result.suspicious_accounts;
const rings: FraudRing[] = result.fraud_rings;
const summary = result.summary;

// Use in components
<SummaryStats summary={result.summary} />
<FraudRingTable rings={result.fraud_rings} />
<AccountModal account={accounts[0]} onClose={() => {}} />
```

---

## Contract Keys Reference

### Root Level
```typescript
{
  suspicious_accounts: SuspiciousAccount[]
  fraud_rings: FraudRing[]
  summary: Summary
}
```

### SuspiciousAccount
```typescript
{
  account_id: string              // "ACC001"
  suspicion_score: number         // 0-100 (weighted average)
  detected_patterns: string[]     // ["cycle_participation:2", "temporal_velocity:1"]
  ring_id: string                 // "RING_001" or ""
}
```

### FraudRing
```typescript
{
  ring_id: string                 // "RING_001" (format: RING_XXX)
  member_accounts: string[]       // ["ACC001", "ACC002", "ACC003"]
  pattern_type: string            // "cycle" | "smurfing" | "shell"
  risk_score: number              // 0-100 (average of members)
}
```

### Summary
```typescript
{
  total_accounts_analyzed: number         // 14
  suspicious_accounts_flagged: number     // 11 (score > 50)
  fraud_rings_detected: number            // 4
  processing_time_seconds: number         // 0.023
}
```

---

## Common Patterns

### Filter High-Risk Accounts
```typescript
const highRisk = result.suspicious_accounts.filter(
  acc => acc.suspicion_score > 70
);
```

### Get Accounts in Ring
```typescript
const ringMembers = result.suspicious_accounts.filter(
  acc => acc.ring_id === 'RING_001'
);
```

### Sort Rings by Risk
```typescript
const sortedRings = [...result.fraud_rings].sort(
  (a, b) => b.risk_score - a.risk_score
);
```

### Parse Detected Patterns
```typescript
account.detected_patterns.forEach(pattern => {
  const [type, count] = pattern.split(':');
  console.log(`${type}: ${count} occurrences`);
});
```

---

## Validation

### Validate Python Output
```bash
python python-engine/main.py data.csv | python validate_contract.py
```

### Check TypeScript Types
```bash
npm run build
```

### Manual Inspection
```bash
python python-engine/main.py data.csv | jq '.suspicious_accounts[0]'
```

---

## Scoring Formula

### Suspicion Score (Weighted Average)
```
Pattern Scores (0-100):
  cycle_participation = min(num_cycles * 60, 100)
  temporal_velocity = min(num_velocity * 50, 100)

Weights:
  cycle_participation: 0.6 (60%)
  temporal_velocity: 0.4 (40%)

Formula:
  suspicion_score = (cycle_score * 0.6 + velocity_score * 0.4) / 1.0
```

### Risk Score (Ring Average)
```
risk_score = average(member_suspicion_scores)
```

---

## Pattern Types

### Currently Implemented
- **cycle**: Transaction cycles (A → B → C → A)

### Future Implementation
- **smurfing**: Structured layering patterns
- **shell**: Shell account networks

---

## Ring ID Format

**Format:** `RING_` + 3-digit zero-padded number

**Valid:**
- `RING_001`
- `RING_042`
- `RING_999`

**Invalid:**
- `RING_1` (not zero-padded)
- `ring_001` (lowercase)
- `RING-001` (wrong separator)

---

## Common Mistakes

### ❌ Don't Use camelCase
```typescript
// WRONG
const suspicionScore = account.suspicionScore;
const fraudRings = result.fraudRings;

// CORRECT
const suspicion_score = account.suspicion_score;
const fraud_rings = result.fraud_rings;
```

### ❌ Don't Assume ring_id Exists
```typescript
// WRONG
const ringId = account.ring_id.toUpperCase();

// CORRECT
const ringId = account.ring_id ? account.ring_id.toUpperCase() : 'None';
```

### ❌ Don't Modify Contract Structure
```python
# WRONG - Adding extra fields
output = {
    'suspicious_accounts': [...],
    'fraud_rings': [...],
    'summary': {...},
    'extra_data': {...}  # Don't add this!
}

# CORRECT - Use contract structure only
output = {
    'suspicious_accounts': [...],
    'fraud_rings': [...],
    'summary': {...}
}
```

---

## Testing Checklist

- [ ] Run `validate_contract.py` on output
- [ ] Check all keys are snake_case
- [ ] Verify ring_id format (RING_XXX)
- [ ] Confirm suspicion_score is 0-100
- [ ] Ensure pattern_type is valid enum
- [ ] Test with empty rings (ring_id = "")
- [ ] Test with zero patterns (suspicion_score = 0)
- [ ] Verify TypeScript compilation passes

---

## Resources

- **Full Specification:** `DATA_CONTRACT.md`
- **Migration Guide:** `CONTRACT_MIGRATION.md`
- **Compliance Report:** `CONTRACT_COMPLIANCE_REPORT.md`
- **Validation Script:** `validate_contract.py`
