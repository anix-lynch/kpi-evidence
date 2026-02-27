#!/usr/bin/env python3
"""Count DQ rules/gates across churn, coffeeverse, cocktailverse. Run from kpi_scripts."""
import os
import re

BASE = os.path.join(os.path.dirname(__file__), "..")
REPOS = ["churn-ml-pipeline", "coffeeverse", "cocktailverse"]

def count_validators(path, pattern_func):
    count = 0
    for root, _, files in os.walk(path):
        for f in files:
            if not f.endswith(".py"):
                continue
            p = os.path.join(root, f)
            try:
                with open(p, "r") as fh:
                    content = fh.read()
                count += len(pattern_func(content))
            except Exception:
                pass
    return count

def main():
    total = 0
    for repo in REPOS:
        path = os.path.join(BASE, repo)
        if not os.path.isdir(path):
            continue
        # Explicit validation: def validate_*, def check_*, ValidationError
        def patterns(c):
            return re.findall(r"def\s+(validate_\w+|check_\w+)|raise\s+ValidationError|ValidationError\(", c)
        n = count_validators(path, patterns)
        # GE / dbt
        ge = 0
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".json"):
                    try:
                        with open(os.path.join(root, f), "r") as fh:
                            if "expectation_type" in fh.read():
                                ge += 1
                    except Exception:
                        pass
        repo_total = n + ge
        total += repo_total
        print(f"{repo}: validation_funcs/checks={n}, GE_expectations={ge} -> {repo_total}")
    print(f"DQ_RULES={total}")
    return 0

if __name__ == "__main__":
    main()
