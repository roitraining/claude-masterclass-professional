# Retrieval stand-in

A local MCP server that does TF-IDF keyword search over `docs/`. It exists so Day 1 Module 7 runs on any laptop with no external service.

Tools it exposes:

- `search_docs(query, top_k=3)` returns a JSON list of `doc_id`, `title`, `score` and `snippet`.
- `read_doc(doc_id)` returns the full text of one document.

Run it by itself to check that it starts (it waits for a client on stdin, so stop it with Ctrl+C):

```
python3 server.py
```

An agent starts it as a child process through the `mcpServers` option. See `python/demo4_retrieval_agent.py`.

## Swapping in a real vector store

Keep the two tool signatures. Replace the body of `Index.search` with a call to your vector store, and have `read_doc` fetch the stored document. The agent only sees a tool, so nothing in the agent changes. Retrieval is an MCP integration pattern, not a first-party Anthropic feature.

The documents are fictional. `bw-returns-handbook-2024` is marked superseded on purpose: a retriever returns old and current text side by side, and the agent has to prefer the current one.
