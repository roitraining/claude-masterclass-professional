# Demo 4: Retrieval Through an MCP Server

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Demo:** 4 of 8
**Time:** about 15 minutes

> Part of **[Claude Agent SDK Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Connect an agent to a retrieval source through an MCP server, so retrieval sits behind a tool call, and state that this is an integration pattern and not a first-party Anthropic feature. Time: about 15 minutes. (Module 7)

**Files:** [`$FILES/retrieval/server.py`](../demo-files/retrieval/server.py), [`$FILES/retrieval/docs/`](../demo-files/retrieval/docs), [`$FILES/retrieval/README.md`](../demo-files/retrieval/README.md), [`$FILES/python/demo4_retrieval_agent.py`](../demo-files/python/demo4_retrieval_agent.py).

**Context:** The retrieval server is a local stand-in. It does TF-IDF keyword search over nine fictional Markdown documents and exposes two tools, `search_docs` and `read_doc`. A real vector store would sit behind the same two tools. The agent sees only a tool.

**Steps:**

1. Show the `docs/` folder. Point out `bw-returns-handbook-2024.md`, marked superseded, next to the current handbook.
2. Open `server.py`. Show the tool signatures and say that the body of `Index.search` is the only thing a vector store replaces.
3. Run the agent:

```
cd $FILES/python
python3 demo4_retrieval_agent.py
```

4. For the first prompt, read the `TOOL` lines: `search_docs`, then `read_doc`, then the answer with a cited `doc_id`.
5. For the second prompt (the return window), show that search returns both the current and the superseded handbook, and that the agent should cite the current one (30 days, not 14).
6. Run a question the knowledge base cannot answer and show the agent saying so:

```
python3 demo4_retrieval_agent.py "What is the warranty on a canoe?"
```

7. State plainly: retrieval here is an MCP integration the course supplies. It is a supported pattern, not a first-party Anthropic feature.

**Expected result:** The agent searches, reads the best document, and answers with a `doc_id`. For the return window it answers 30 days. For the canoe it says the knowledge base has nothing relevant.

> **Instructor note:** The MCP wiring is confirmed in the MCP guide. The retrieval design (an agent reaching a vector store or search through an MCP server) is in the verified facts. The ranking is a crude keyword score: the superseded handbook can rank first for some queries, which is a useful teaching moment about retrieval quality and not a defect to hide. Module 7 is instructor-provisioned, so you may swap in a real store behind the same tool signatures. The server library caveats from Demo 3 apply (**UNVERIFIED** import path and `run()` call). **Fallback:** show the `search_docs` JSON output by running the retrieval index directly (`python` with `from server import INDEX`, then `INDEX.search("return window", 3)`), then read the expected tool sequence from the Expected result.

> **Why this matters:** Teams often ask for "RAG" as a product. It is a tool call. Seeing that removes the mystery and shows where retrieval quality, and prompt injection from documents, can enter.

---

**Previous:** [Demo 3: Build a Standalone MCP Server](demo-3-build-a-standalone-mcp-server.md) · **Next:** [Demo 5: Delegate to a Subagent](demo-5-delegate-to-a-subagent.md)


*Demo 4 of 8*
