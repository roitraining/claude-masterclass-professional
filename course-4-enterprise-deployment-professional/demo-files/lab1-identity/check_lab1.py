#!/usr/bin/env python3
"""Lab 1 offline checker: scores a student's findings and edited configuration.

Usage:  python3 check_lab1.py [DIR]
DIR holds the student's edited copies of the Lab 1 files and findings_lab1.json
(default: the folder this script is in).

Scoring (100): defects D1-D4 are 20 each (10 for the finding, 10 for the fix),
D5 is 10 (5 and 5), and 10 points are for leaving the correct rows untouched.
This script holds the answer key. Give it to students after they submit, or
remove the KEYWORDS table first. Standard library only.
"""
import csv
import json
import os
import re
import sys

DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))


def path(name):
    return os.path.join(DIR, name)


def read_csv(name):
    with open(path(name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def low(value):
    return (value or "").strip().lower()


def finding_texts():
    try:
        with open(path("findings_lab1.json"), encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as exc:
        print("  ! could not read findings_lab1.json: %s" % exc)
        return []
    out = []
    for item in data.get("findings", []):
        out.append(" ".join(str(item.get(k, "")) for k in ("file", "issue", "fix")).lower())
    return out


def has(texts, test):
    return any(test(t) for t in texts)


# ---- finding tests (keyword based, deliberately forgiving) -----------------
def f_d1(t):
    return "secops" in t and ("group" in t or "no permission" in t or "scim" in t)


def f_d2(t):
    return "it-operations" in t or ("owner" in t and any(k in t for k in ("broad", "too many", "least privilege", "over-privileg", "212")))


def f_d3(t):
    return ("idp" in t or "identity provider" in t) and any(
        k in t for k in ("unassign", "re-add", "readd", "re-provision", "next login", "next sso", "offboard"))


def f_d4(t):
    return "domain" in t and "verif" in t


def f_d5(t):
    return ("manage-members" in t or "write" in t) and ("auditor" in t or "role" in t or "read-only" in t)


# ---- fix tests (read the edited files) -------------------------------------
def fix_d1():
    mappings = read_csv("group_mappings.csv")
    groups = read_csv("claude_groups.csv")
    row = next((m for m in mappings if low(m["idp_group"]) == "claude-secops-analysts"), None)
    if row is None:
        return False, "mapping row for claude-secops-analysts was removed"
    if low(row["provisioning"]) == "scim":
        return True, "mapping moved to SCIM directory sync"
    target = low(row["claude_group"]) or "secops-analysts"
    for g in groups:
        if low(g["group_name"]) == target:
            try:
                members = int(g.get("member_count") or 0)
            except ValueError:
                members = 0
            if members >= 1 and "secops" in low(g.get("custom_role")):
                return True, "group %s exists with members and the custom role" % target
            return False, "group %s exists but has no members or no custom role" % target
    return False, "no Claude group named %s in claude_groups.csv" % target


def fix_d2():
    mappings = read_csv("group_mappings.csv")
    for m in mappings:
        if low(m["claude_role"]) == "owner":
            try:
                count = int(m["idp_member_count"])
            except ValueError:
                count = 999
            if count > 5:
                return False, "%s (%s members) is still mapped to Owner" % (m["idp_group"], count)
    return True, "no Owner mapping exceeds 5 members"


def fix_d3():
    for r in read_csv("offboarding_steps.csv"):
        if low(r["system"]) in ("idp", "identity provider", "exampleidp") and any(
                k in low(r["action"]) for k in ("unassign", "remove")):
            return True, "step %s unassigns the user in the IdP" % r["step"]
    return False, "no IdP unassign step in offboarding_steps.csv"


def fix_d4():
    rows = read_csv("rollout_plan.csv")

    def num(r):  # order in the file, not the step label
        return rows.index(r)

    # A verification row is one that names a domain and is not the enforce step.
    # Requiring both "verif" and "domain" in one cell rejected correct rewordings.
    def is_verify(r):
        a = low(r["action"])
        if "enforce" in a:
            return False
        return "verif" in a or ".example.net" in a or ".example.org" in a
    verify = [r for r in rows if is_verify(r)]
    enforce = [r for r in rows if "enforce" in low(r["action"])]
    if not verify:
        return False, "no domain verification step in rollout_plan.csv"
    if not enforce:
        return False, "the enforce step was removed"
    if min(num(r) for r in verify) >= min(num(r) for r in enforce):
        return False, "domain verification comes after SSO enforcement"
    if not any("northwind-labs.example.net" in low(r["action"]) for r in verify):
        return False, "the verification step does not name northwind-labs.example.net"
    return True, "domain verification precedes enforcement and names both domains"


def fix_d5():
    with open(path("custom_roles.json"), encoding="utf-8") as f:
        data = json.load(f)
    for role in data.get("roles", []):
        if role.get("name") == "SecOps Read-Only Auditor":
            bad = [p["id"] for p in role.get("permissions", []) if low(p.get("access")) != "read"]
            if bad:
                return False, "still has non-read permission(s): %s" % ", ".join(bad)
            if not role.get("permissions"):
                return False, "the role has no permissions at all"
            return True, "role is read-only and still has permissions"
    return False, "role SecOps Read-Only Auditor not found"


def decoys_intact():
    problems = []
    mappings = read_csv("group_mappings.csv")
    by = {low(m["idp_group"]): m for m in mappings}
    for name, role in (("claude-owners", "owner"), ("claude-admins", "admin"), ("claude-users-all", "user")):
        if name not in by or low(by[name]["claude_role"]) != role:
            problems.append("%s should still map to %s" % (name, role))
    domains = {low(r["domain"]): r for r in read_csv("domains.csv")}
    if "example.com" not in domains or low(domains["example.com"]["verified"]) != "yes":
        problems.append("example.com must remain verified")
    return problems


def main():
    texts = finding_texts()
    score = 0
    plan = [
        ("D1 JIT with a Custom role and no Claude group", 10, 10, f_d1, fix_d1),
        ("D2 Owner mapped to a broad group", 10, 10, f_d2, fix_d2),
        ("D3 Removal only in Claude, not in the IdP", 10, 10, f_d3, fix_d3),
        ("D4 Domain verification missing", 10, 10, f_d4, fix_d4),
        ("D5 Custom role exceeds its read-only description (bonus defect)", 5, 5, f_d5, fix_d5),
    ]
    for label, fpts, xpts, ftest, xfn in plan:
        found = has(texts, ftest)
        try:
            fixed, why = xfn()
        except Exception as exc:  # unreadable or malformed student file
            fixed, why = False, "could not check: %s" % exc
        got = (fpts if found else 0) + (xpts if fixed else 0)
        score += got
        print("%s" % label)
        print("   finding reported: %s (%d)   fix in files: %s (%d)" % (
            "yes" if found else "no", fpts if found else 0, "yes" if fixed else "no", xpts if fixed else 0))
        print("   %s" % why)
    try:
        problems = decoys_intact()
    except Exception as exc:
        problems = ["could not check: %s" % exc]
    if problems:
        print("Correct rows changed: " + "; ".join(problems))
    else:
        print("Correct rows left untouched: yes (10)")
        score += 10
    print("\nSCORE: %d / 100" % score)


if __name__ == "__main__":
    main()
