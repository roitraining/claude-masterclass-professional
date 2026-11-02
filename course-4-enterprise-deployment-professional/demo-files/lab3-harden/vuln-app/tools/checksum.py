import hashlib
import os
import sys

name = sys.argv[1] if len(sys.argv) > 1 else ""
path = os.path.join("reports", name)
if not os.path.isfile(path):
    print("no such report: %s" % name)
    sys.exit(1)
with open(path, "rb") as f:
    print("%s  %s" % (hashlib.sha256(f.read()).hexdigest(), name))
