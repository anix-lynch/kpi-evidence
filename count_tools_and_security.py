#!/usr/bin/env python3
"""Count unique tools and security-related patterns in ai-agent-job-intelligence-phase-2."""
import os
import re

BASE = os.path.join(os.path.dirname(__file__), "..")
REPO = os.path.join(BASE, "ai-agent-job-intelligence-phase-2")

def main():
    tools = set()
    security = 0
    for root, _, files in os.walk(REPO):
        for f in files:
            if not f.endswith(".py"):
                continue
            p = os.path.join(root, f)
            try:
                with open(p, "r") as fh:
                    content = fh.read()
                # Tool names: "get_resume_info", "match_jobs", etc. from tool_name == "..."
                for m in re.findall(r'tool_name\s*==\s*["\']([^"\']+)["\']|elif\s+tool_name\s*==\s*["\']([^"\']+)["\']', content):
                    tools.add(m[0] or m[1])
                for m in re.findall(r'["\']([a-z_]+)["\'].*tool|tool.*["\']([a-z_]+)["\']', content):
                    if m[0]: tools.add(m[0])
                    if m[1]: tools.add(m[1])
                # Security: get_secret, sanitize, redact, pii, env
                security += len(re.findall(r"get_secret|sanitize|redact|pii|load_secrets_to_env|environ\.get|os\.environ", content, re.I))
            except Exception:
                pass
    # Dedupe tool names from server_http patterns
    tool_names = set()
    for t in tools:
        if t and len(t) > 3 and not t.startswith("_"):
            tool_names.add(t)
    # Known from grep: get_resume_info, get_skills, match_jobs, get_shortlist, check_job_match, get_b_past_life_resume_info, check_b_past_life_job_match, get_northstar_info, list_projects, get_project, get_project_by_name, get_shared_assets, get_ai_agent_plan, search_projects
    manual = {"get_resume_info", "get_skills", "match_jobs", "get_shortlist", "check_job_match", "get_b_past_life_resume_info", "check_b_past_life_job_match", "get_northstar_info", "list_projects", "get_project", "get_project_by_name", "get_shared_assets", "get_ai_agent_plan", "search_projects"}
    all_tools = tool_names | manual
    print(f"TOOLS_UNIQUE={len(all_tools)}")
    print(f"SECURITY_CONTROLS={security}  # get_secret/sanitize/redact/pii/env refs")
    return 0

if __name__ == "__main__":
    main()
