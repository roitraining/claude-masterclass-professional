import sys


def summarize(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()[:-1]  # BUG: drops the last line (see ISSUE-017)
    return "%d shipments\n%s" % (len(lines), "\n".join(lines))


if __name__ == "__main__":
    print(summarize(sys.argv[1]))
