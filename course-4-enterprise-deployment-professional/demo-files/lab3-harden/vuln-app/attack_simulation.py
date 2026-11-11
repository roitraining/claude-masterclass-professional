#!/usr/bin/env python3
"""Local attack simulation for Lab 3. Harmless: it only touches marker files and a loopback port.

Run it from the project folder, inside a Claude Code session so the Bash tool is the
thing being tested:   python3 attack_simulation.py

Four attempts, 10 points each when BLOCKED:
  1 write outside the working directory (a marker file in the parent folder)
  2 outbound connection to a disallowed destination (a loopback canary listener)
  3 read the secrets file (the content is never printed)
  4 command injection through app.checksum_report (marker file inside the project)

Outcomes depend on the operating system sandbox. A real sandbox needs macOS Seatbelt,
or Linux or WSL2 bubblewrap. Loopback behavior under the sandbox network proxy is
UNVERIFIED: rehearse before class. Use --net-target host:port to point attempt 2 at a
different destination your instructor has rehearsed.
"""
import argparse
import http.server
import json
import os
import socket
import threading

HERE = os.path.dirname(os.path.abspath(__file__))


def attempt_outside_write():
    target = os.path.join(os.path.dirname(HERE), "OUTSIDE_WRITE_MARKER.txt")
    try:
        with open(target, "w", encoding="utf-8") as f:
            f.write("lab3 marker\n")
    except OSError as exc:
        return "BLOCKED", "write to %s failed: %s" % (target, exc)
    os.remove(target)
    return "SUCCEEDED", "wrote and removed %s" % target


def attempt_network(net_target):
    host, _, port = net_target.partition(":")
    port = int(port or 80)
    server = None
    if host in ("127.0.0.1", "localhost"):
        class Quiet(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"canary")

            def log_message(self, *a):
                pass
        class QuietServer(http.server.HTTPServer):
            # The client closes as soon as it has its bytes, which makes
            # socketserver print a ConnectionResetError traceback from the
            # handler thread. That traceback is noise: it is not the attack
            # result, and the main try/except below cannot catch it because it
            # happens on another thread.
            def handle_error(self, request, client_address):
                pass

        try:
            server = QuietServer(("127.0.0.1", port), Quiet)
        except OSError as exc:
            return "ERROR", "could not start the canary listener on %d: %s" % (port, exc)
        threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with socket.create_connection((host, port), timeout=4) as s:
            s.sendall(("GET / HTTP/1.0\r\nHost: %s\r\n\r\n" % host).encode())
            data = s.recv(64)
        return "SUCCEEDED", "connected to %s:%d and received %d bytes" % (host, port, len(data))
    except OSError as exc:
        return "BLOCKED", "connection to %s:%d failed: %s" % (host, port, exc)
    finally:
        if server:
            server.shutdown()


def attempt_read_secrets():
    path = os.path.join(HERE, "config", "secrets.env")
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as exc:
        return "BLOCKED", "read of config/secrets.env failed: %s" % exc
    return "SUCCEEDED", "read %d bytes from config/secrets.env (not printed)" % len(text)


def attempt_injection():
    marker = os.path.join(HERE, "INJECTED_MARKER")
    if os.path.exists(marker):
        os.remove(marker)
    sep = "&" if os.name == "nt" else ";"
    payload = "q3.txt %s echo injected> INJECTED_MARKER" % sep
    import importlib
    import sys
    sys.path.insert(0, HERE)
    cwd = os.getcwd()
    os.chdir(HERE)
    try:
        app = importlib.import_module("app")
        try:
            app.checksum_report(payload)
        except Exception as exc:  # a fixed app may raise on a bad name
            outcome = "fixed app rejected the name: %s" % exc
        else:
            outcome = "app returned"
    finally:
        os.chdir(cwd)
    if os.path.exists(marker):
        os.remove(marker)
        return "SUCCEEDED", "the injected command ran (%s)" % outcome
    return "BLOCKED", "no injected command ran (%s)" % outcome


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--net-target", default="127.0.0.1:8765")
    ap.add_argument("--json", help="also write results to this file")
    a = ap.parse_args()
    results = [
        ("1 write outside the working directory", *attempt_outside_write()),
        ("2 call to a disallowed destination", *attempt_network(a.net_target)),
        ("3 read the secrets file", *attempt_read_secrets()),
        ("4 command injection through app.py", *attempt_injection()),
    ]
    score = 0
    for name, status, why in results:
        pts = 10 if status == "BLOCKED" else 0
        score += pts
        print("%-42s %-9s %2d  %s" % (name, status, pts, why))
    print("\nATTACK SCORE: %d / 40" % score)
    # On a machine with no working OS sandbox, attacks 1 to 3 cannot be blocked here at
    # all, so this line alone reads as a near-total failure for a student whose config is
    # correct. Say what the fallback is - but do NOT compute it. Attacks 1 to 3 are worth
    # 5 each only where check_settings.py PREDICTS them blocked, which for an unhardened
    # config is none of them. An earlier version hard-coded 15 and told a student with
    # 0/60 that they had 15/25.
    if any(st != "BLOCKED" for _, st, _ in results[:3]):
        live4 = 10 if results[3][1] == "BLOCKED" else 0
        print("")
        print("Attacks 1-3 need the OS sandbox. If yours cannot start, that is a known")
        print("platform limit and this result is expected - see the lab's fallback scoring.")
        print("Under fallback, Part B is out of 25: attack 4 scores %d live (above), and" % live4)
        print("attacks 1-3 score 5 each ONLY where check_settings.py predicts them blocked.")
        print("Read your checker's PREDICTED block and add them up - do not assume 15.")

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump([dict(attack=n, status=s, detail=w) for n, s, w in results], f, indent=1)


if __name__ == "__main__":
    main()
