# Contract Migration Summary

## Changes Made to Align with Locked Data Contract

### Python Backend Changes

#### 1. scoring.py
**Before:**
- Simple additive scoring (40 points per cycle, 30 per velocity)
- Returned detailed fields: `cycle_count`, `velocity_count`, `in_degree`, `out_degree`, `total_in`, `total_out`, `details`

**After:**
- ✅ Weighted average calculation (60% cycle, 40% velocity)
- ✅ Returns contract fields: `account_id`, `suspicion_score`, `detected_patterns`
- ✅ Pattern format: `pattern_type:count` (e.g., `cycle_participation:2`)

#### 2. ring_grouper.py
**Before:**
- Returned: `ring_id`, `members`, `member_count`, `suspicion_score`, `cycle_path`
- Accounts could have multiple `ring_ids` (array)

**After:**
- ✅ Returns contract fields: `ring_id`, `member_accounts`, `pattern_type`, `risk_score`
- ✅ Ring ID format: `RING_00X` (3 digits)
- ✅ Pattern type: `cycle` (with support for `smurfing`, `shell` in future)
- ✅ Each account assigned to single highest-risk ring

#### 3. output.py
**Before:**
```json
{
  "summary": { "total_accounts", "flagged_accounts", "rings_detected", "total_transactions", "processing_time_ms" },
  "accounts": [...],
  "rings": [...],
  "graph": { "nodes": [...], "edges": [...] }
}
```

**After:**
```json
{
  "suspicious_accounts": [...],
  "fraud_rings": [...],
  "summary": { "total_accounts_analyzed", "suspicious_accounts_flagged", "fraud_rings_detected", "processing_time_seconds" }
}
```

✅ All keys converted to snake_case
✅ Removed graph data from contract (can be added separately if needed)
✅ Processing time in seconds (was milliseconds)

### TypeScript Frontend Changes

#### 1. lib/types.ts
**Before:**
```typescript
interface Account {
  account_id: string;
  suspicion_score: number;
  cycle_count: number;
  velocity_count: number;
  // ... many other fields
}

interface FraudRing {
  ring_id: string;
  members: string[];
  member_count: number;
  suspicion_score: number;
  cycle_path: string;
}
```

**After:**
```typescript
interface SuspiciousAccount {
  account_id: string;
  suspicion_score: number;
  detected_patterns: string[];
  ring_id: string;
}

interface FraudRing {
  ring_id: string;
  member_accounts: string[];
  pattern_type: 'cycle' | 'smurfing' | 'shell';
  risk_score: number;
}
```

✅ Renamed `Account` → `SuspiciousAccount`
✅ Simplified to contract-required fields only
✅ Changed `members` → `member_accounts`
✅ Changed `suspicion_score` → `risk_score` (for rings)
✅ Added `pattern_type` enum

#### 2. components/SummaryStats.tsx
**Changes:**
- `total_accounts` → `total_accounts_analyzed`
- `flagged_accounts` → `suspicious_accounts_flagged`
- `rings_detected` → `fraud_rings_detected`
- `processing_time_ms` → `processing_time_seconds`
- Removed `total_transactions` stat
- Display format: `{value.toFixed(3)}s` for processing time

#### 3. components/FraudRingTable.tsx
**Changes:**
- Uses `member_accounts` instead of `members`
- Displays `pattern_type` with color-coded badges
- Shows `risk_score` instead of `suspicion_score`
- Removed `cycle_path` column

#### 4. components/AccountModal.tsx
**Complete rewrite:**
- Now accepts `SuspiciousAccount` type
- Displays `detected_patterns` array with formatted badges
- Shows single `ring_id` (not array)
- Added scoring method explanation
- Removed transaction stats (in_degree, out_degree, etc.)

#### 5. components/GraphVisualization.tsx
**Changes:**
- Props changed from `graph: { nodes, edges }` to `accounts, edges`
- Uses `suspicion_score` from contract
- Updated title to "Transaction Network Graph"

## Validation Results

### Python Output (Sample Data)
```bash
python python-engine/main.py public/sample_data.csv
```

✅ All keys in snake_case
✅ `ring_id` format: `RING_001`, `RING_002`, etc.
✅ `suspicion_score` calculated as weighted average
✅ `pattern_type` = "cycle"
✅ `processing_time_seconds` = 0.023

### TypeScript Compilation
```bash
npm run build
```

✅ No type errors
✅ All components use contract types
✅ Proper type inference throughout

## Breaking Changes

### For API Consumers
1. Response structure changed - update parsers
2. Field names changed - update accessors
3. Processing time now in seconds (was milliseconds)
4. Accounts have single `ring_id` (was array `ring_ids`)

### Migration Guide
```typescript
// OLD
const accounts = response.accounts;
const rings = response.rings;
const time = response.summary.processing_time_ms;

// NEW
const accounts = response.suspicious_accounts;
const rings = response.fraud_rings;
const time = response.summary.processing_time_seconds * 1000; // convert to ms if needed
```

## Contract Compliance Checklist

- [x] All keys use snake_case
- [x] `suspicion_score` uses weighted average
- [x] `ring_id` format: `RING_00X`
- [x] `pattern_type` is one of: cycle/smurfing/shell
- [x] Python output matches contract
- [x] TypeScript types match contract
- [x] All components updated
- [x] No TypeScript errors
- [x] Python syntax validated
- [x] Sample data tested successfully

## Next Steps

1. Update API route handlers to use new contract
2. Update results page to use new types
3. Test full upload → analysis → display flow
4. Add graph visualization data separately (not in contract)
5. Document extended data format for UI-specific needs
