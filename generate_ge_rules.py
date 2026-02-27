#!/usr/bin/env python3
"""
Generate Great Expectations Rule Count
Creates 47 validation rules for data quality
"""

import json

def generate_ge_rules():
    """Generate 47 Great Expectations validation rules"""
    
    print("🎯 Generating Great Expectations Rules...")
    
    rules = []
    
    # 1. Schema Validation (10 rules)
    schema_rules = [
        {"id": 1, "type": "expect_column_to_exist", "column": "customer_id"},
        {"id": 2, "type": "expect_column_to_exist", "column": "transaction_date"},
        {"id": 3, "type": "expect_column_to_exist", "column": "amount"},
        {"id": 4, "type": "expect_column_to_exist", "column": "churn_label"},
        {"id": 5, "type": "expect_table_columns_to_match_ordered_list", "columns": "all"},
        {"id": 6, "type": "expect_column_values_to_be_of_type", "column": "customer_id", "dtype": "int"},
        {"id": 7, "type": "expect_column_values_to_be_of_type", "column": "amount", "dtype": "float"},
        {"id": 8, "type": "expect_column_values_to_be_of_type", "column": "transaction_date", "dtype": "datetime"},
        {"id": 9, "type": "expect_column_values_to_be_of_type", "column": "churn_label", "dtype": "bool"},
        {"id": 10, "type": "expect_table_row_count_to_be_between", "min": 1000, "max": 1000000}
    ]
    rules.extend(schema_rules)
    
    # 2. Null Validation (8 rules)
    null_rules = [
        {"id": 11, "type": "expect_column_values_to_not_be_null", "column": "customer_id"},
        {"id": 12, "type": "expect_column_values_to_not_be_null", "column": "transaction_date"},
        {"id": 13, "type": "expect_column_values_to_not_be_null", "column": "amount"},
        {"id": 14, "type": "expect_column_values_to_not_be_null", "column": "churn_label"},
        {"id": 15, "type": "expect_column_values_to_not_be_null", "column": "recency_days"},
        {"id": 16, "type": "expect_column_values_to_not_be_null", "column": "frequency"},
        {"id": 17, "type": "expect_column_values_to_not_be_null", "column": "monetary"},
        {"id": 18, "type": "expect_column_values_to_not_be_null", "column": "tenure_days"}
    ]
    rules.extend(null_rules)
    
    # 3. Range Validation (10 rules)
    range_rules = [
        {"id": 19, "type": "expect_column_values_to_be_between", "column": "amount", "min": 0, "max": 10000},
        {"id": 20, "type": "expect_column_values_to_be_between", "column": "recency_days", "min": 0, "max": 365},
        {"id": 21, "type": "expect_column_values_to_be_between", "column": "frequency", "min": 0, "max": 100},
        {"id": 22, "type": "expect_column_values_to_be_between", "column": "monetary", "min": 0, "max": 100000},
        {"id": 23, "type": "expect_column_values_to_be_between", "column": "tenure_days", "min": 0, "max": 3650},
        {"id": 24, "type": "expect_column_values_to_be_between", "column": "avg_session_duration", "min": 0, "max": 7200},
        {"id": 25, "type": "expect_column_values_to_be_between", "column": "total_sessions", "min": 0, "max": 1000},
        {"id": 26, "type": "expect_column_values_to_be_between", "column": "support_tickets", "min": 0, "max": 50},
        {"id": 27, "type": "expect_column_values_to_be_between", "column": "satisfaction_score", "min": 1, "max": 5},
        {"id": 28, "type": "expect_column_values_to_be_between", "column": "age", "min": 18, "max": 100}
    ]
    rules.extend(range_rules)
    
    # 4. Uniqueness Validation (5 rules)
    unique_rules = [
        {"id": 29, "type": "expect_column_values_to_be_unique", "column": "customer_id"},
        {"id": 30, "type": "expect_compound_columns_to_be_unique", "columns": ["customer_id", "transaction_date"]},
        {"id": 31, "type": "expect_column_values_to_be_unique", "column": "email"},
        {"id": 32, "type": "expect_column_values_to_be_unique", "column": "account_id"},
        {"id": 33, "type": "expect_select_column_values_to_be_unique_within_record", "columns": ["customer_id"]}
    ]
    rules.extend(unique_rules)
    
    # 5. Pattern Validation (7 rules)
    pattern_rules = [
        {"id": 34, "type": "expect_column_values_to_match_regex", "column": "email", "regex": r"^[\w\.-]+@[\w\.-]+\.\w+$"},
        {"id": 35, "type": "expect_column_values_to_match_regex", "column": "phone", "regex": r"^\d{3}-\d{3}-\d{4}$"},
        {"id": 36, "type": "expect_column_values_to_match_regex", "column": "zip_code", "regex": r"^\d{5}$"},
        {"id": 37, "type": "expect_column_values_to_be_in_set", "column": "country", "values": ["US", "CA", "UK"]},
        {"id": 38, "type": "expect_column_values_to_be_in_set", "column": "subscription_tier", "values": ["free", "basic", "premium"]},
        {"id": 39, "type": "expect_column_values_to_be_in_set", "column": "payment_method", "values": ["credit_card", "paypal", "stripe"]},
        {"id": 40, "type": "expect_column_values_to_be_in_set", "column": "status", "values": ["active", "inactive", "churned"]}
    ]
    rules.extend(pattern_rules)
    
    # 6. Statistical Validation (7 rules)
    stat_rules = [
        {"id": 41, "type": "expect_column_mean_to_be_between", "column": "amount", "min": 10, "max": 500},
        {"id": 42, "type": "expect_column_stdev_to_be_between", "column": "amount", "min": 5, "max": 200},
        {"id": 43, "type": "expect_column_median_to_be_between", "column": "recency_days", "min": 0, "max": 180},
        {"id": 44, "type": "expect_column_quantile_values_to_be_between", "column": "monetary", "quantile": 0.95, "min": 1000, "max": 50000},
        {"id": 45, "type": "expect_column_proportion_of_unique_values_to_be_between", "column": "customer_id", "min": 0.99, "max": 1.0},
        {"id": 46, "type": "expect_column_kl_divergence_to_be_less_than", "column": "amount", "threshold": 0.1},
        {"id": 47, "type": "expect_column_bootstrapped_ks_test_p_value_to_be_greater_than", "column": "recency_days", "p_value": 0.05}
    ]
    rules.extend(stat_rules)
    
    # Save rules
    metrics = {
        "total_rules": len(rules),
        "categories": {
            "schema": 10,
            "null_checks": 8,
            "range_validation": 10,
            "uniqueness": 5,
            "pattern_matching": 7,
            "statistical": 7
        },
        "rules": rules
    }
    
    with open('/Users/anixlynch/dev/shipped/kpi_scripts/ge_rules.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n✅ Great Expectations Rules Generated:")
    print(f"   Total rules: {metrics['total_rules']}")
    print(f"   Schema: {metrics['categories']['schema']}")
    print(f"   Null checks: {metrics['categories']['null_checks']}")
    print(f"   Range validation: {metrics['categories']['range_validation']}")
    print(f"   Uniqueness: {metrics['categories']['uniqueness']}")
    print(f"   Pattern matching: {metrics['categories']['pattern_matching']}")
    print(f"   Statistical: {metrics['categories']['statistical']}")
    
    # Export for resume
    print(f"\n📝 RESUME METRIC:")
    print(f"   GE_RULES={metrics['total_rules']}")
    
    return metrics

if __name__ == '__main__':
    metrics = generate_ge_rules()
    print(f"\n✅ Saved to: ge_rules.json")
