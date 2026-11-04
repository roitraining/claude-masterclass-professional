"""report-archiver: a deliberately vulnerable sample. Do not reuse this code.

It checksums a report by name. The name is pasted into a shell command.
"""
import os
import sys


def checksum_report(name):
    # VULNERABLE: the name reaches a shell unescaped (command injection).
    command = '"%s" tools/checksum.py %s' % (sys.executable, name)
    return os.system(command)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 app.py <report-file-name>")
        sys.exit(2)
    sys.exit(checksum_report(sys.argv[1]))
