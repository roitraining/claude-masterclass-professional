#!/usr/bin/env python3
"""INSTRUCTOR ONLY. Regenerates the SYNTHETIC activity export for Lab 2.

Do not give this file to students: it contains the planted anomalies.
Usage: python make_activity_export.py [OUTPUT_DIR]   (default: parent folder)
Every person, address, key, and resource is fictional. IPs use the documentation
ranges 192.0.2.0/24, 198.51.100.0/24 and 203.0.113.0/24. Event type names are
SYNTHETIC and are NOT the Compliance API schema (UNVERIFIED).
"""
import csv
import datetime as dt
import json
import os
import random
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
rnd = random.Random(20260914)

START = dt.datetime(2026, 9, 7, 0, 0, 0)  # a Monday; export covers 7 days
USERS = [
    ("alice.moreau", "192.0.2.11"), ("ben.alvarez", "192.0.2.12"), ("chloe.dubois", "192.0.2.13"),
    ("dana.whitfield", "198.51.100.21"), ("evan.park", "192.0.2.15"), ("farah.khan", "192.0.2.16"),
    ("gus.lindqvist", "192.0.2.17"), ("hana.kobayashi", "198.51.100.18"), ("ivan.petrov", "192.0.2.19"),
    ("jun.park", "192.0.2.20"), ("kira.novak", "192.0.2.22"), ("lee.ortega", "198.51.100.23"),
    ("marcus.bell", "198.51.100.17"), ("nia.owusu", "192.0.2.24"), ("omar.haddad", "192.0.2.25"),
    ("priya.nair", "192.0.2.26"), ("quinn.reyes", "192.0.2.27"), ("rosa.silva", "192.0.2.28"),
    ("sam.okafor", "192.0.2.30"), ("tara.lund", "192.0.2.31"), ("uma.rao", "192.0.2.32"),
    ("vic.hale", "192.0.2.33"), ("wen.zhao", "192.0.2.34"), ("xavi.ruiz", "192.0.2.35"),
]
SURFACES = ["claude.ai", "claude-code", "desktop", "cowork", "m365"]
TYPES = [("login_sso_success", 20), ("chat_created", 30), ("file_uploaded", 9), ("file_downloaded", 6),
         ("project_created", 3), ("project_shared", 3), ("claude_code_session_started", 14),
         ("cowork_session_started", 6), ("api_key_used", 9)]
RES = ["Quarterly Notes", "Onboarding FAQ", "Runbook Draft", "Vendor Review", "Roadmap Q4", "Test Plan", "Support Macros"]
events = []


def add(ts, user, ip, etype, surface="claude.ai", resource="", details=None, country="US", actor_type="user"):
    events.append(dict(timestamp=ts, actor="%s@example.com" % user if "@" not in user else user, actor_type=actor_type,
                       event_type=etype, surface=surface, source_ip=ip, country=country, resource=resource,
                       details=details or {}))


def stamp(day, h, m, s=0):
    return (START + dt.timedelta(days=day, hours=h, minutes=m, seconds=s)).strftime("%Y-%m-%dT%H:%M:%SZ")


names = [t for t, w in TYPES for _ in range(w)]
# Baseline: 290 events, weekdays 09:00-18:00 UTC
for _ in range(290):
    user, ip = rnd.choice(USERS)
    day = rnd.randint(0, 4)
    ts = stamp(day, rnd.randint(9, 17), rnd.randint(0, 59), rnd.randint(0, 59))
    et = rnd.choice(names)
    surface = "claude-code" if et == "claude_code_session_started" else "cowork" if et == "cowork_session_started" else rnd.choice(SURFACES[:3])
    details = {}
    resource = rnd.choice(RES)
    if et == "project_shared":
        details = {"shared_with": "team-%s@example.com" % rnd.choice(["eng", "support", "finance"]), "external": False, "permission": "view"}
    elif et == "api_key_used":
        k = "key-FAKE-%04d" % rnd.choice([11, 12, 13, 14])
        details = {"key_id": k}
        resource = "messages"
        surface = "api"
    elif et == "file_downloaded":
        details = {"bytes": rnd.randint(2000, 400000)}
        resource = "files/%s.pdf" % resource.lower().replace(" ", "-")
    add(ts, user, ip, et, surface, resource, details)

# Benign weekend/off-hours singletons
add(stamp(5, 10, 3), "gus.lindqvist", "192.0.2.17", "chat_created", resource="Weekend Notes")
add(stamp(6, 20, 41), "tara.lund", "192.0.2.31", "chat_created", resource="Side Project Ideas")

# DECOY B1: business-hours bulk download, recurring weekly export (two days, same time)
for day in (1, 2):
    for i in range(25):
        add(stamp(day, 14, 5, i * 20), "priya.nair", "192.0.2.26", "file_downloaded", resource="files/weekly-metrics-%02d.csv" % (i + 1), details={"bytes": 51000 + i * 17})
# DECOY B2: API key created and used from the same known IP
add(stamp(2, 10, 12), "sam.okafor", "192.0.2.30", "api_key_created", "api", "key-FAKE-0031", {"key_id": "key-FAKE-0031", "scopes": "messages"})
for i in range(6):
    add(stamp(2, 10, 30 + i * 4), "sam.okafor", "192.0.2.30", "api_key_used", "api", "messages", {"key_id": "key-FAKE-0031"})
# DECOY B3: internal project share
add(stamp(3, 11, 2), "jun.park", "192.0.2.20", "project_shared", resource="Project: Finance Close", details={"shared_with": "team-finance@example.com", "external": False, "permission": "edit"})
# DECOY B4: single SSO failure then success from the same IP (typo)
add(stamp(3, 9, 14, 5), "omar.haddad", "192.0.2.25", "login_sso_failed", details={"reason": "bad_password_or_assertion"})
add(stamp(3, 9, 14, 41), "omar.haddad", "192.0.2.25", "login_sso_success")

# PLANTED A1: after-hours bulk download (Saturday 02:14-02:31 UTC, 64 files)
for i in range(64):
    add(stamp(5, 2, 14, i * 16), "dana.whitfield", "198.51.100.21", "file_downloaded", "claude.ai",
        "files/finance/board-pack-%02d.pdf" % (i + 1), {"bytes": 800000 + i * 311})
# PLANTED A2: API key created and used from a new location
add(stamp(2, 15, 41), "marcus.bell", "203.0.113.55", "api_key_created", "api", "key-FAKE-0042", {"key_id": "key-FAKE-0042", "scopes": "messages,files"}, country="RO")
for i in range(9):
    add(stamp(2, 15, 52 + i * 5), "marcus.bell", "203.0.113.55", "api_key_used", "api", "files", {"key_id": "key-FAKE-0042"}, country="RO")
# PLANTED A3: project shared outside the organization
add(stamp(4, 16, 22), "hana.kobayashi", "198.51.100.18", "project_shared", resource="Project: Q4 Pricing Strategy",
    details={"shared_with": "consultant@outside-example.net", "external": True, "permission": "edit"})
# PLANTED A4: failed then successful SSO sequence from a new IP (Thursday)
for i in range(8):
    add(stamp(3, 11, 20, i * 38), "lee.ortega", "203.0.113.88", "login_sso_failed", details={"reason": "bad_password_or_assertion"}, country="BR")
add(stamp(3, 11, 26, 10), "lee.ortega", "203.0.113.88", "login_sso_success", country="BR")
for i in range(3):
    add(stamp(3, 11, 28 + i, 5), "lee.ortega", "203.0.113.88", "file_downloaded", resource="files/hr/payroll-extract-%d.csv" % (i + 1), details={"bytes": 120000}, country="BR")

events.sort(key=lambda e: e["timestamp"])
for n, e in enumerate(events, 1):
    e["event_id"] = "evt-%04d" % n
cols = ["event_id", "timestamp", "actor", "actor_type", "event_type", "surface", "source_ip", "country", "resource", "details"]
ordered = [{c: e[c] for c in cols} for e in events]
meta = {
    "source": "SYNTHETIC export for training. Not Compliance API output. Event type names and fields are invented for the lab.",
    "timezone": "UTC",
    "org_business_hours_utc": "09:00-18:00 Monday to Friday",
    "org_known_locations": "US (192.0.2.0/24 and 198.51.100.0/24)",
    "event_count": len(ordered),
}
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "activity_export.json"), "w", encoding="utf-8") as f:
    json.dump({"export_meta": meta, "events": ordered}, f, indent=1)
with open(os.path.join(OUT, "activity_export.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for e in ordered:
        row = dict(e)
        row["details"] = json.dumps(e["details"], separators=(",", ":"))
        w.writerow(row)
print("wrote %d events to %s" % (len(ordered), os.path.abspath(OUT)))
