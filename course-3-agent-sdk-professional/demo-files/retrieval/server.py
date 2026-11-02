"""Local stand-in retrieval MCP server (stdio): TF-IDF keyword search over a folder of Markdown documents.

No external service and no vector database. The agent sees two tools: search_docs and read_doc.
A real vector store would sit behind the same two tool signatures. Only the body of search() would change.

Run by an agent as a child process. Never print to stdout; stdout carries the protocol.
Set DOCS_DIR to point at another folder of .md files.
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # newer releases
    from mcp.server import MCPServer as FastMCP  # type: ignore

HERE = Path(__file__).resolve().parent
DOCS_DIR = Path(os.environ.get("DOCS_DIR") or HERE / "docs")
TOKEN_RE = re.compile(r"[a-z0-9]+")
STOP = {"a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how", "in", "is", "it", "of", "on", "or",
        "that", "the", "to", "what", "when", "which", "with", "do", "does", "i", "my", "me", "can", "you", "your"}


def stem(token: str) -> str:
    """Crude plural stripping so 'returns' matches 'return'. A real retriever would use a proper stemmer or embeddings."""
    return token[:-1] if len(token) > 3 and token.endswith("s") and not token.endswith("ss") else token


def tokenize(text: str) -> list[str]:
    return [stem(t) for t in TOKEN_RE.findall(text.lower()) if t not in STOP]


class Index:
    def __init__(self, folder: Path) -> None:
        self.docs: dict[str, dict] = {}
        for path in sorted(folder.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            title = next((ln.lstrip("# ").strip() for ln in text.splitlines() if ln.startswith("#")), path.stem)
            tokens = tokenize(text)
            self.docs[path.stem] = {"title": title, "text": text, "tf": Counter(tokens), "len": max(len(tokens), 1)}
        n = len(self.docs)
        df: Counter = Counter()
        for d in self.docs.values():
            df.update(d["tf"].keys())
        self.idf = {t: math.log((n + 1) / (c + 1)) + 1.0 for t, c in df.items()}

    def search(self, query: str, top_k: int) -> list[dict]:
        q = tokenize(query)
        scored = []
        for doc_id, d in self.docs.items():
            score = sum((1.0 + math.log(d["tf"][t])) * self.idf.get(t, 0.0) for t in q if t in d["tf"]) / math.sqrt(d["len"])
            if score > 0:
                scored.append((score, doc_id))
        scored.sort(reverse=True)
        out = []
        for score, doc_id in scored[:top_k]:
            d = self.docs[doc_id]
            best = max(d["text"].splitlines(), key=lambda ln: sum(t in tokenize(ln) for t in q), default="")
            out.append({"doc_id": doc_id, "title": d["title"], "score": round(score, 4), "snippet": best.strip()[:240]})
        return out


INDEX = Index(DOCS_DIR)
mcp = FastMCP("retrieval")


@mcp.tool()
def search_docs(query: str, top_k: int = 3) -> str:
    """Search the Brightwater knowledge base by keywords and return the best matching documents as JSON: doc_id, title, score and a snippet. Use this first for any question about store policy, product care or services. Then call read_doc on the best match before answering. Documents marked superseded are old drafts: prefer documents marked current."""
    hits = INDEX.search(query, max(1, min(int(top_k), 10)))
    return json.dumps(hits) if hits else "No matching documents."


@mcp.tool()
def read_doc(doc_id: str) -> str:
    """Return the full text of one knowledge-base document. Input: a doc_id returned by search_docs, such as bw-returns-handbook."""
    doc = INDEX.docs.get(doc_id)
    return doc["text"] if doc else f"No document with id {doc_id!r}. Call search_docs to find valid ids."


if __name__ == "__main__":
    print(f"retrieval server: {len(INDEX.docs)} documents from {DOCS_DIR}", file=sys.stderr, flush=True)
    mcp.run(transport="stdio")
