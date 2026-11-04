#!/usr/bin/env python3
"""Build the Lab 2 review fixture: a small git repository with a main branch and
eleven pull request branches. All people and data are fictional.

Usage:
    python build_fixture.py TARGET_DIR
    python build_fixture.py --emit-key DIR      # facilitator: (re)write diffs/ and facilitator/answer_key.json into DIR

TARGET_DIR must not exist. The script runs `git init`, `git commit` and `git branch`
inside TARGET_DIR only. It does not contact a remote and does not call a model.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

GIT = ["git", "-c", "user.name=Fixture Author", "-c", "user.email=fixture@example.invalid",
       "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false"]

BASE = {}

BASE["CLAUDE.md"] = '''# Harborview Library lending service

Fictional example service for Lab 2.

- Money is integer cents. Never use floats for money that is stored or compared.
- Fine policy LIB-7: a prorated fine is truncated to whole cents and never rounded up.
- Every handler on the public router must call `require_role` before it reads or changes data.
  Routes on a `Router` created with `guard_role=...` are guarded by the router itself.
- No credentials in code. Read them from `lending/config.py`, which reads the environment.
- Database access uses bound parameters. Placeholders may be generated, values may not.
- Tests use `unittest`. Run them with `python -m unittest`.
'''

BASE["lending/__init__.py"] = ""

BASE["lending/config.py"] = '''import os

SMTP_HOST = os.environ.get("LENDING_SMTP_HOST", "localhost")
SMTP_USER = os.environ.get("LENDING_SMTP_USER", "lending")
SMTP_PASSWORD = os.environ.get("LENDING_SMTP_PASSWORD", "")

LOAN_DAYS = 21
FINE_CENTS_PER_DAY = 25
FINE_CAP_CENTS = 1000
WAIVER_THRESHOLD_CENTS = 200
'''

BASE["lending/auth.py"] = '''class Forbidden(Exception):
    """Raised when the caller lacks a required role."""


def require_role(user, role):
    if user is None or role not in user.get("roles", ()):
        raise Forbidden(role)
'''

BASE["lending/web.py"] = '''from dataclasses import dataclass, field

from lending.auth import require_role


@dataclass
class Request:
    method: str
    path: str
    user: dict = None
    params: dict = field(default_factory=dict)


class Router:
    def __init__(self, guard_role=None):
        self.guard_role = guard_role
        self.routes = {}

    def route(self, method, path):
        def register(handler):
            self.routes[(method, path)] = handler
            return handler
        return register

    def dispatch(self, request):
        if self.guard_role:
            require_role(request.user, self.guard_role)
        return self.routes[(request.method, request.path)](request)
'''

BASE["lending/fines.py"] = '''from lending.config import FINE_CAP_CENTS, FINE_CENTS_PER_DAY


def days_late(due, returned):
    return max(0, (returned - due).days)


def fine_cents(due, returned):
    return min(FINE_CAP_CENTS, days_late(due, returned) * FINE_CENTS_PER_DAY)
'''

BASE["lending/members.py"] = '''from dataclasses import dataclass


@dataclass
class Member:
    member_id: str
    name: str
    is_senior: bool = False


class MemberStore:
    def __init__(self):
        self._members = {}

    def add(self, member):
        self._members[member.member_id] = member

    def get(self, member_id):
        return self._members.get(member_id)

    def remove(self, member_id):
        return self._members.pop(member_id, None)

    def all(self):
        return list(self._members.values())
'''

BASE["lending/catalog.py"] = '''def search_titles(conn, term):
    sql = "SELECT id, title FROM books WHERE title LIKE ? ORDER BY title"
    return conn.execute(sql, (f"%{term}%",)).fetchall()
'''

BASE["lending/notify.py"] = '''import smtplib

from lending import config


def send_email(to, subject, body):
    message = f"Subject: {subject}\\n\\n{body}"
    with smtplib.SMTP(config.SMTP_HOST) as smtp:
        smtp.login(config.SMTP_USER, config.SMTP_PASSWORD)
        smtp.sendmail("library@example.invalid", [to], message)
'''

BASE["lending/reports.py"] = '''def overdue_titles(loans, today):
    return sorted(loan["title"] for loan in loans if loan["due"] < today)
'''

BASE["lending/api.py"] = '''from lending.auth import require_role
from lending.members import Member, MemberStore
from lending.web import Router

router = Router()
store = MemberStore()


@router.route("POST", "/members")
def create_member(request):
    require_role(request.user, "librarian")
    member = Member(request.params["id"], request.params["name"])
    store.add(member)
    return {"id": member.member_id}


@router.route("PUT", "/members")
def update_member(request):
    require_role(request.user, "librarian")
    member = store.get(request.params["id"])
    member.name = request.params["name"]
    return {"id": member.member_id}


@router.route("GET", "/members")
def list_members(request):
    require_role(request.user, "librarian")
    return {"members": [m.member_id for m in store.all()]}
'''

BASE["lending/admin_api.py"] = '''from lending.web import Router

# Every route registered here is guarded by the router (guard_role), not by the handler.
admin = Router(guard_role="librarian")
waived = []


@admin.route("POST", "/admin/waive")
def waive_fine(request):
    waived.append(request.params["member_id"])
    return {"waived": request.params["member_id"]}
'''

BASE["tests/__init__.py"] = ""

BASE["tests/test_fines.py"] = '''import unittest
from datetime import date

from lending.fines import days_late, fine_cents


class FineTests(unittest.TestCase):
    def test_on_time_is_free(self):
        self.assertEqual(fine_cents(date(2026, 3, 1), date(2026, 3, 1)), 0)

    def test_three_days_late(self):
        self.assertEqual(fine_cents(date(2026, 3, 1), date(2026, 3, 4)), 75)

    def test_cap(self):
        self.assertEqual(fine_cents(date(2026, 3, 1), date(2026, 6, 1)), 1000)

    def test_days_late_never_negative(self):
        self.assertEqual(days_late(date(2026, 3, 5), date(2026, 3, 1)), 0)


if __name__ == "__main__":
    unittest.main()
'''

BASE["tests/test_members.py"] = '''import unittest

from lending.members import Member, MemberStore


class MemberTests(unittest.TestCase):
    def test_add_get_remove(self):
        store = MemberStore()
        store.add(Member("m1", "Ada Test"))
        self.assertEqual(store.get("m1").name, "Ada Test")
        store.remove("m1")
        self.assertIsNone(store.get("m1"))


if __name__ == "__main__":
    unittest.main()
'''

BASE["README.md"] = "# Harborview Library lending service\n\nFictional fixture for Lab 2. Run `python -m unittest`.\n"


def rep(path, old, new):
    """Return a transform that replaces `old` with `new` in a file, or appends when old is None."""
    def go(text):
        if old is None:
            return text + new
        assert old in text, f"{path}: anchor not found: {old!r}"
        return text.replace(old, new, 1)
    return (path, go)


def add(path, text):
    return (path, lambda _t, text=text: text)


PRS = []

# ------------------------------------------------------------------ planted bugs
PRS.append(dict(
    branch="pr-01-senior-waiver", kind="bug", title="Waive small fines for senior members",
    changes=[
        rep("lending/fines.py", "from lending.config import FINE_CAP_CENTS, FINE_CENTS_PER_DAY",
            "from lending.config import FINE_CAP_CENTS, FINE_CENTS_PER_DAY, WAIVER_THRESHOLD_CENTS"),
        rep("lending/fines.py", None, '''

def fine_with_waiver(is_senior, due, returned):
    """Senior members have fines under the waiver threshold waived. Everyone else pays in full."""
    fee = fine_cents(due, returned)
    if is_senior or fee < WAIVER_THRESHOLD_CENTS:
        return 0
    return fee
'''),
        rep("tests/test_fines.py", "\n\nif __name__", '''
    def test_senior_small_fine_waived(self):
        from lending.fines import fine_with_waiver
        self.assertEqual(fine_with_waiver(True, date(2026, 3, 1), date(2026, 3, 3)), 0)


if __name__'''),
    ],
    bug=dict(id="B1", category="logic error", file="lending/fines.py", marker="if is_senior or fee",
             keywords=["senior", "waive", "waiver", "all seniors", "everyone"],
             summary="The waiver condition uses 'or'. Every senior has any fine waived, and every member has fines under the threshold waived. The docstring says seniors with small fines only, so it must be 'and'."),
))

PRS.append(dict(
    branch="pr-02-catalog-paging", kind="bug", title="Add paging to catalog search",
    changes=[
        rep("lending/catalog.py", None, '''

def page_of(items, page, size):
    """Return one page of items. Pages are numbered from 1."""
    start = (page - 1) * size
    return items[start:start + size + 1]
'''),
        add("tests/test_catalog.py", '''import unittest

from lending.catalog import page_of


class PagingTests(unittest.TestCase):
    def test_first_page_has_items(self):
        self.assertTrue(len(page_of(list(range(10)), 1, 3)) >= 3)


if __name__ == "__main__":
    unittest.main()
'''),
    ],
    bug=dict(id="B2", category="off-by-one", file="lending/catalog.py", marker="start + size + 1",
             keywords=["off-by-one", "size + 1", "extra item", "one too many", "slice"],
             summary="The slice ends at start + size + 1, so every page returns one item too many and pages overlap by one. The test only checks 'at least' the page size, so it passes."),
))

PRS.append(dict(
    branch="pr-03-delete-member", kind="bug", title="Add an endpoint to delete a member",
    changes=[
        rep("lending/api.py", None, '''

@router.route("DELETE", "/members")
def delete_member(request):
    store.remove(request.params["id"])
    return {"deleted": request.params["id"]}
'''),
    ],
    bug=dict(id="B3", category="missing authorization check", file="lending/api.py", marker="def delete_member",
             keywords=["require_role", "authorization", "auth", "librarian", "unauthenticated", "permission"],
             summary="delete_member never calls require_role. It is on the public router, where every sibling handler checks the librarian role first, so anyone can delete members."),
))

PRS.append(dict(
    branch="pr-04-overdue-email", kind="bug", title="Email members when a loan is overdue",
    changes=[
        rep("lending/notify.py", None, '''

SMTP_PASSWORD = "FAKE-TOKEN-DO-NOT-USE"


def send_overdue_notice(to, title):
    message = f"Subject: Overdue: {title}\\n\\nPlease return {title}."
    with smtplib.SMTP(config.SMTP_HOST) as smtp:
        smtp.login(config.SMTP_USER, SMTP_PASSWORD)
        smtp.sendmail("library@example.invalid", [to], message)
'''),
    ],
    bug=dict(id="B4", category="hard-coded secret", file="lending/notify.py", marker='SMTP_PASSWORD = "FAKE-TOKEN-DO-NOT-USE"',
             keywords=["hard-coded", "hardcoded", "credential", "password", "secret", "config", "environment"],
             summary="A credential is written into the source (the value is a deliberate fake placeholder). Credentials must come from lending/config.py, which reads the environment."),
))

PRS.append(dict(
    branch="pr-05-genre-filter", kind="bug", title="Filter catalog search by genre",
    changes=[
        rep("lending/catalog.py", None, '''

def search_by_genre(conn, term, genre):
    sql = f"SELECT id, title FROM books WHERE title LIKE ? AND genre = '{genre}' ORDER BY title"
    return conn.execute(sql, (f"%{term}%",)).fetchall()
'''),
    ],
    bug=dict(id="B5", category="SQL injection", file="lending/catalog.py", marker="genre = '{genre}'",
             keywords=["sql injection", "injection", "f-string", "parameter", "bound", "genre"],
             summary="genre is formatted into the SQL text with an f-string. The title value is bound, the genre is not, so a crafted genre changes the query."),
))

# ------------------------------------------------------------------ false-positive bait
PRS.append(dict(
    branch="pr-06-bulk-lookup", kind="bait", title="Look up several books by id",
    changes=[
        rep("lending/catalog.py", None, '''

def books_by_ids(conn, ids):
    placeholders = ",".join("?" * len(ids))
    sql = f"SELECT id, title FROM books WHERE id IN ({placeholders})"
    return conn.execute(sql, tuple(ids)).fetchall()
'''),
    ],
    bait=dict(id="F1", looks_like="SQL injection", file="lending/catalog.py", marker="IN ({placeholders})",
              why_fine="The f-string inserts only a run of '?' characters generated from len(ids). Every value is bound through the parameter tuple. CLAUDE.md allows generated placeholders."),
))

PRS.append(dict(
    branch="pr-07-notify-tests", kind="bait", title="Test the email sender with a fake SMTP server",
    changes=[
        add("tests/test_notify.py", '''import unittest
from unittest import mock

from lending import notify

TEST_PASSWORD = "test-password-not-a-secret"


class NotifyTests(unittest.TestCase):
    def test_send_email_logs_in_and_sends(self):
        fake = mock.MagicMock()
        fake.__enter__.return_value = fake
        with mock.patch("lending.notify.smtplib.SMTP", return_value=fake), \\
                mock.patch.object(notify.config, "SMTP_PASSWORD", TEST_PASSWORD):
            notify.send_email("reader@example.invalid", "Hello", "Body")
        fake.login.assert_called_once_with(notify.config.SMTP_USER, TEST_PASSWORD)
        fake.sendmail.assert_called_once()


if __name__ == "__main__":
    unittest.main()
'''),
    ],
    bait=dict(id="F2", looks_like="hard-coded secret", file="tests/test_notify.py", marker="TEST_PASSWORD =",
              why_fine="A placeholder used only against a mocked SMTP object inside a unit test. It opens nothing and no real credential is involved."),
))

PRS.append(dict(
    branch="pr-08-loan-gaps", kind="bait", title="Report the longest gap between due dates",
    changes=[
        rep("lending/reports.py", None, '''

def longest_gap_days(due_dates):
    """Largest number of days between two consecutive due dates, or 0 for fewer than two."""
    dates = sorted(due_dates)
    longest = 0
    for i in range(len(dates) - 1):
        longest = max(longest, (dates[i + 1] - dates[i]).days)
    return longest
'''),
    ],
    bait=dict(id="F3", looks_like="off-by-one", file="lending/reports.py", marker="range(len(dates) - 1)",
              why_fine="Comparing consecutive pairs needs n - 1 iterations. i + 1 stays in range, and fewer than two dates returns 0. This is correct."),
))

PRS.append(dict(
    branch="pr-09-waive-all", kind="bait", title="Add a bulk fine waiver for a member list",
    changes=[
        rep("lending/admin_api.py", None, '''

@admin.route("POST", "/admin/waive-many")
def waive_many(request):
    ids = request.params["member_ids"]
    waived.extend(ids)
    return {"waived": len(ids)}
'''),
    ],
    bait=dict(id="F4", looks_like="missing authorization check", file="lending/admin_api.py", marker="def waive_many",
              why_fine="The handler has no require_role call, but it is registered on `admin`, a Router created with guard_role='librarian'. Router.dispatch checks the role for every route."),
))

PRS.append(dict(
    branch="pr-10-prorated-fine", kind="bait", title="Prorate a fine for a partial day rate",
    changes=[
        rep("lending/fines.py", None, '''

def prorated_fine_cents(days, rate_cents_per_day):
    """Fine for a fractional rate. Policy LIB-7: truncate to whole cents, never round up.

    The round(..., 6) guards float representation error before truncating, so an
    exact 29.00 does not become 28. It does not round up: 28.7 still truncates to 28.
    """
    return int(round(days * rate_cents_per_day, 6))
'''),
    ],
    bait=dict(id="F5", looks_like="logic error (float to int truncation)", file="lending/fines.py", marker="return int(round(days * rate_cents_per_day, 6))",
              why_fine="int() truncates toward zero on purpose. CLAUDE.md and the docstring state policy LIB-7: truncate, never round up. The result is stored as integer cents."),
))

PRS.append(dict(
    branch="pr-11-docstrings", kind="clean", title="Add docstrings to the fines module",
    changes=[
        rep("lending/fines.py", "def days_late(due, returned):\n",
            'def days_late(due, returned):\n    """Whole days between the due date and the return date, never negative."""\n'),
        rep("lending/fines.py", "def fine_cents(due, returned):\n",
            'def fine_cents(due, returned):\n    """Fine in cents for a loan, capped at FINE_CAP_CENTS."""\n'),
    ],
))


def git(cwd, *args, check=True):
    return subprocess.run([*GIT, *args], cwd=cwd, check=check, capture_output=True, text=True).stdout


def write(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def build(target):
    target = Path(target)
    if target.exists():
        sys.exit(f"{target} already exists. Choose a new folder.")
    target.mkdir(parents=True)
    git(target, "init", "-q", "-b", "main")
    for rel, text in BASE.items():
        write(target, rel, text)
    git(target, "add", "-A")
    git(target, "commit", "-q", "-m", "Baseline lending service")
    key = dict(tolerance_lines=3, bugs=[], bait=[], clean=[])
    for pr in PRS:
        git(target, "checkout", "-q", "-b", pr["branch"], "main")
        for path, fn in pr["changes"]:
            f = target / path
            old = f.read_text(encoding="utf-8") if f.exists() else ""
            write(target, path, fn(old))
        git(target, "add", "-A")
        git(target, "commit", "-q", "-m", pr["title"])
        entry = dict(pr=pr["branch"], title=pr["title"])
        for slot in ("bug", "bait"):
            if slot in pr:
                item = dict(pr[slot])
                lines = (target / item["file"]).read_text(encoding="utf-8").splitlines()
                hits = [i for i, ln in enumerate(lines, 1) if item["marker"] in ln]
                assert hits, f"marker not found for {pr['branch']}"
                item["line"] = hits[0]
                entry.update(item)
                key["bugs" if slot == "bug" else "bait"].append(entry)
        if pr["kind"] == "clean":
            key["clean"].append(entry)
        git(target, "checkout", "-q", "main")
    return target, key


def emit(target, key, out):
    out = Path(out)
    (out / "diffs").mkdir(parents=True, exist_ok=True)
    for pr in PRS:
        diff = git(target, "diff", "-U25", f"main...{pr['branch']}")
        (out / "diffs" / f"{pr['branch']}.diff").write_text(diff, encoding="utf-8", newline="\n")
    (out / "facilitator").mkdir(exist_ok=True)
    (out / "facilitator" / "answer_key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8", newline="\n")


def main(argv):
    if len(argv) == 2 and argv[0] == "--emit-key":
        with tempfile.TemporaryDirectory() as tmp:
            target, key = build(Path(tmp) / "repo")
            emit(target, key, argv[1])
            print(f"Wrote diffs/ and facilitator/answer_key.json to {argv[1]}")
            import shutil
            shutil.rmtree(target, ignore_errors=True)
        return 0
    if len(argv) != 1:
        print(__doc__)
        return 2
    target, key = build(argv[0])
    print(f"Built {target}")
    print("Branches: " + ", ".join(p["branch"] for p in PRS))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
