#!/usr/bin/env python3
"""
Contract Validation Script for MuleRift
Validates that Python output matches the Locked Data Contract
"""

import json
import sys
import re

def validate_contract(data):
    """Validate JSON output against Locked Data Contract."""
    errors = []
    
    # Check root structure
    required_root_keys = {'suspicious_accounts', 'fraud_rings', 'summary'}
    if not required_root_keys.issubset(data.keys()):
        errors.append(f"Missing root keys. Expected: {required_root_keys}, Got: {set(data.keys())}")
        return errors
    
    # Validate suspicious_accounts
    for idx, account in enumerate(data['suspicious_accounts']):
        prefix = f"suspicious_accounts[{idx}]"
        
        # Check required fields
        required = {'account_id', 'suspicion_score', 'detected_patterns', 'ring_id'}
        if not required.issubset(account.keys()):
            errors.append(f"{prefix}: Missing fields. Expected: {required}, Got: {set(account.keys())}")
        
        # Check types
        if not isinstance(account.get('account_id'), str):
            errors.append(f"{prefix}.account_id: Must be string")
        
        if not isinstance(account.get('suspicion_score'), (int, float)):
            errors.append(f"{prefix}.suspicion_score: Must be number")
        elif not (0 <= account['suspicion_score'] <= 100):
            errors.append(f"{prefix}.suspicion_score: Must be 0-100, got {account['suspicion_score']}")
        
        if not isinstance(account.get('detected_patterns'), list):
            errors.append(f"{prefix}.detected_patterns: Must be array")
        
        if not isinstance(account.get('ring_id'), str):
            errors.append(f"{prefix}.ring_id: Must be string")
        elif account['ring_id'] and not re.match(r'^RING_\d{3}$', account['ring_id']):
            errors.append(f"{prefix}.ring_id: Invalid format '{account['ring_id']}'. Must be 'RING_XXX'")
    
    # Validate fraud_rings
    for idx, ring in enumerate(data['fraud_rings']):
        prefix = f"fraud_rings[{idx}]"
        
        # Check required fields
        required = {'ring_id', 'member_accounts', 'pattern_type', 'risk_score'}
        if not required.issubset(ring.keys()):
            errors.append(f"{prefix}: Missing fields. Expected: {required}, Got: {set(ring.keys())}")
        
        # Check ring_id format
        if not re.match(r'^RING_\d{3}$', ring.get('ring_id', '')):
            errors.append(f"{prefix}.ring_id: Invalid format '{ring.get('ring_id')}'. Must be 'RING_XXX'")
        
        # Check member_accounts
        if not isinstance(ring.get('member_accounts'), list):
            errors.append(f"{prefix}.member_accounts: Must be array")
        elif len(ring['member_accounts']) < 2:
            errors.append(f"{prefix}.member_accounts: Must have at least 2 members")
        
        # Check pattern_type
        valid_patterns = {'cycle', 'smurfing', 'shell'}
        if ring.get('pattern_type') not in valid_patterns:
            errors.append(f"{prefix}.pattern_type: Must be one of {valid_patterns}, got '{ring.get('pattern_type')}'")
        
        # Check risk_score
        if not isinstance(ring.get('risk_score'), (int, float)):
            errors.append(f"{prefix}.risk_score: Must be number")
        elif not (0 <= ring['risk_score'] <= 100):
            errors.append(f"{prefix}.risk_score: Must be 0-100, got {ring['risk_score']}")
    
    # Validate summary
    summary = data['summary']
    required_summary = {'total_accounts_analyzed', 'suspicious_accounts_flagged', 
                       'fraud_rings_detected', 'processing_time_seconds'}
    
    if not required_summary.issubset(summary.keys()):
        errors.append(f"summary: Missing fields. Expected: {required_summary}, Got: {set(summary.keys())}")
    
    # Check types
    for field in ['total_accounts_analyzed', 'suspicious_accounts_flagged', 'fraud_rings_detected']:
        if not isinstance(summary.get(field), int):
            errors.append(f"summary.{field}: Must be integer")
    
    if not isinstance(summary.get('processing_time_seconds'), (int, float)):
        errors.append(f"summary.processing_time_seconds: Must be number")
    
    # Check for camelCase (should be snake_case)
    def has_camel_case(obj, path=""):
        issues = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                if re.search(r'[a-z][A-Z]', key):
                    issues.append(f"{path}.{key}: Uses camelCase (should be snake_case)")
                issues.extend(has_camel_case(value, f"{path}.{key}"))
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                issues.extend(has_camel_case(item, f"{path}[{idx}]"))
        return issues
    
    errors.extend(has_camel_case(data))
    
    return errors

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)
    
    errors = validate_contract(data)
    
    if errors:
        print("❌ CONTRACT VALIDATION FAILED")
        print(f"\nFound {len(errors)} error(s):\n")
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)
    else:
        print("✅ CONTRACT VALIDATION PASSED")
        print(f"\n  • {len(data['suspicious_accounts'])} suspicious accounts")
        print(f"  • {len(data['fraud_rings'])} fraud rings")
        print(f"  • All keys use snake_case")
        print(f"  • All ring_id formats valid (RING_XXX)")
        print(f"  • All pattern_types valid")
        sys.exit(0)
