#!/usr/bin/env python3
"""Lab 2 offline checker.

Usage:
  python3 check_lab2.py --findings findings_lab2.json --control control_proxy_spec.json
  python3 check_lab2.py --findings findings_lab2.json --control control_desktop_policy.json
  (--export defaults to activity_export.json next to this script)

Scoring (100): four anomalies x 15 (actor 6, evidence event ids 5, explanation 4),
decoys 10 (minus 5 for each benign actor reported as medium or high), and the
control task 30. The planted events are found by rule from the export, so the
export can be regenerated. This script holds the answer logic: hand it to
students after they submit. Standard library only.
"""
import argparse
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
APPROVED = {"00000000-0000-4000-8000-0000000000a1", "00000000-0000-4000-8000-0000000000a2",
            "00000000-0000-4000-8000-0000000000a3"}
RETIRED = "00000000-0000-4000-8000-0000000000f9"
HOSTS = {"claude.ai", "api.anthropic.com", "claude.com", "anthropic.com"}


def low(v):
    return str(v or "").strip().lower()


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- findings --
def planted(events):
    a1 = [e["event_id"] for e in events if e["actor"].startswith("dana.whitfield") and e["event_type"] == "file_downloaded"
          and e["timestamp"].startswith("2026-09-12T02:")]
    a2 = [e["event_id"] for e in events if e["actor"].startswith("marcus.bell") and e["source_ip"] == "203.0.113.55"]
    a3 = [e["event_id"] for e in events if e["event_type"] == "project_shared" and e["details"].get("external") is True]
    a4 = [e["event_id"] for e in events if e["actor"].startswith("lee.ortega") and e["source_ip"] == "203.0.113.88"
          and e["event_type"] in ("login_sso_failed", "login_sso_success")]
    return [
        ("A1 after-hours bulk download", "dana.whitfield@example.com", a1, lambda t: "download" in t),
        ("A2 API key created and used from a new location", "marcus.bell@example.com", a2,
         lambda t: "key" in t and any(k in t for k in ("location", "ip", "country", "new", "romania", "ro "))),
        ("A3 project shared outside the organization", "hana.kobayashi@example.com", a3,
         lambda t: any(k in t for k in ("external", "outside", "third part", "outside-example"))),
        ("A4 failed then successful SSO sequence", "lee.ortega@example.com", a4,
         lambda t: "fail" in t and any(k in t for k in ("success", "then", "after", "brute", "spray", "guess"))),
    ]


DECOYS = ["priya.nair@example.com", "sam.okafor@example.com", "jun.park@example.com", "omar.haddad@example.com"]


def score_findings(path, export):
    events = load(export)["events"]
    data = load(path)
    findings = data.get("findings", [])
    total = 0
    for label, actor, ids, concept in planted(events):
        best = 0
        note = "not found"
        need = min(3, len(ids))
        for f in findings:
            if low(f.get("actor")) != actor or low(f.get("severity")) in ("info", "informational", "benign"):
                continue
            pts = 6
            cited = set(f.get("event_ids", [])) & set(ids)
            if len(cited) >= need:
                pts += 5
            text = low(f.get("title")) + " " + low(f.get("summary"))
            if concept(text):
                pts += 4
            if pts > best:
                best, note = pts, "actor ok, %d planted event ids cited (need %d), explanation %s" % (
                    len(cited), need, "ok" if concept(text) else "missing the key point")
        total += best
        print("%s: %d / 15   (%s)" % (label, best, note))
    flagged = {low(f.get("actor")) for f in findings
               if low(f.get("actor")) in DECOYS and low(f.get("severity")) in ("high", "medium")}
    decoy = max(0, 10 - 5 * len(flagged))
    total += decoy
    print("Benign activity not over-reported: %d / 10   %s" % (decoy, ("(flagged: %s)" % ", ".join(sorted(flagged))) if flagged else ""))
    return total


# ----------------------------------------------------------------- control --
def score_proxy(c):
    pts = 0
    notes = []
    if low(c.get("header_name")) == "anthropic-allowed-org-ids":
        pts += 5
    else:
        notes.append("header name must be anthropic-allowed-org-ids")
    value = str(c.get("header_value", ""))
    parts = value.split(",")
    if value and " " not in value and "\t" not in value and all(p for p in parts) and all(UUID.match(p) for p in parts):
        pts += 5
    else:
        notes.append("header value must be comma-separated UUIDs with no spaces and no empty items")
    ids = {p.strip() for p in parts if p.strip()}
    if ids == APPROVED:
        pts += 6
    elif RETIRED in ids:
        notes.append("the retired organization is still allowed")
    else:
        notes.append("the approved organization set is not exact")
    hosts = {low(h) for h in c.get("applies_to_hosts", [])}
    if HOSTS <= hosts:
        pts += 5
    else:
        notes.append("hosts missing: %s" % ", ".join(sorted(HOSTS - hosts)))
    if c.get("tls_inspection_required") is True and "tls" in low(c.get("rollout_notes")):
        pts += 4
    else:
        notes.append("TLS inspection must be required and the rollout notes must say it has to be turned on")
    auth = low(" ".join(map(str, c.get("auth_methods_covered", []))))
    groups = [("web", "account", "sso"), ("desktop",), ("api key", "api-key", "apikey"), ("oauth",)]
    covered = sum(1 for g in groups if any(k in auth for k in g))
    pts += round(5 * covered / 4)
    if covered < 4:
        notes.append("authentication coverage incomplete")
    return pts, notes


def score_desktop(c):
    pts = 0
    notes = []
    mac = c.get("macos", {})
    win = c.get("windows", {})
    if low(mac.get("preference_domain")) == "com.anthropic.claudefordesktop":
        pts += 5
    else:
        notes.append("macOS domain must be com.anthropic.claudefordesktop")
    prec = low(win.get("hive_precedence"))
    if "hklm" in prec and any(k in prec for k in ("priority", "over", "precedence", "wins", "takes", "overrides")):
        pts += 5
    else:
        notes.append("state that machine-level HKLM takes priority over per-user HKCU")
    want = ["auto_update", "desktop_extensions", "local_dev_mcp"]
    for side in (mac, win):
        have = {k.get("purpose") for k in side.get("keys", []) if k.get("name") and "describe the key" not in low(k.get("name"))}
        pts += 4.5 * sum(1 for w in want if w in have) / 3
    invented = [k.get("name") for side in (mac, win) for k in side.get("keys", [])
                if k.get("name") and not low(k["name"]).startswith("unverified:")]
    filled = [k for side in (mac, win) for k in side.get("keys", [])
              if k.get("name") and "describe the key" not in low(k["name"])]
    if filled and not invented:
        pts += 5
    else:
        notes.append("key names not marked UNVERIFIED (invented): %s" % ", ".join(map(str, invented)))
    delivery = low(mac.get("delivery")) + " " + low(win.get("delivery")) + " " + low(mac.get("installer")) + " " + low(win.get("installer"))
    ok = (any(k in delivery for k in ("jamf", "kandji", "intune", "profile")) and
          any(k in delivery for k in ("group policy", "intune")) and ".pkg" in delivery and ".msix" in delivery)
    if ok:
        pts += 3
    else:
        notes.append("name the macOS delivery and .pkg, the Windows delivery and .msix")
    note = low(c.get("extension_allowlist_note"))
    if "override" in note and "allowlist" in note:
        pts += 3
    else:
        notes.append("say that user-machine policy overrides the in-app extension allowlist")
    return int(round(pts)), notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--findings", required=True)
    ap.add_argument("--control", required=True)
    ap.add_argument("--export", default=os.path.join(HERE, "activity_export.json"))
    a = ap.parse_args()
    total = score_findings(a.findings, a.export)
    c = load(a.control)
    pts, notes = score_proxy(c) if c.get("track") == "proxy" else score_desktop(c)
    print("Control task (%s track): %d / 30" % (c.get("track"), pts))
    for n in notes:
        print("   - " + n)
    total += pts
    print("\nSCORE: %d / 100" % total)


if __name__ == "__main__":
    main()
