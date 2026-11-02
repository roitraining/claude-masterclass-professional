# Demo 3: Start a Cloud Session and Teleport It

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Demo:** 3 of 9
**Time:** about 10 minutes

> Part of **[Claude Code Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Start work in a cloud session from the terminal, queue a follow-up to it, and bring it back to the terminal. Time: about 10 minutes.

**Files:** None. Use the sandbox repository from Demo 1, with the branch pushed.

**Context:** `claude --cloud "<task>"` starts a session on Anthropic's cloud. It clones the GitHub remote at your current branch, so push first. `claude --teleport` (or `/teleport`, `/tp`) pulls a cloud session into your terminal. Teleport needs a clean git state, the same repository, a pushed branch and the same claude.ai account. Handoff is one way from the command line. Cloud sessions are not available through Bedrock, Vertex or other providers.

**Steps:**

1. Check the branch is pushed and the working tree is clean: `git status`.
2. Start a cloud session:

```
claude --cloud "Add a biggest_income helper to tallybook with a test. Do not change anything else."
```

3. Copy the session ID that it prints, or find the session on claude.ai.
4. Queue a follow-up to the running session from another terminal:

```
claude -p "Also add one line to the README describing the helper" --cloud <session-id>
```

5. When the session has made progress, bring it back: `claude --teleport`, choose the session, and look at the branch it checked out.
6. Say what you cannot do: hand a local session up to the cloud mid-conversation.

**Expected result:** A session runs without your terminal, accepts a queued message, and appears in your terminal after `--teleport` with its branch and conversation.

**Instructor note:** Sandbox account only. Uses cloud session usage. The cloud environment's network access, variables and setup script are set per environment, and whether the sandbox's environment lets this task finish is unknown until you rehearse. Teleport refuses on a dirty tree or a different account. The `--remote` spelling is a deprecated alias for `--cloud`. If the live run fails or is slow, use a screenshot set from rehearsal, or a transcript outline: command, session ID, queued message, teleport, resulting branch. Plugin language servers do not start in cloud sessions, which matters again in Demo 8.

**Why this matters:** Where a task runs decides what it can reach and who sees it. A cloud session is not your laptop, and moving between them is one way.

---

**Previous:** [Demo 2: Review a Pull Request With a Skill](demo-2-review-a-pull-request-with-a-skill.md) · **Next:** [Demo 4: A Routine Versus an Actions Workflow](demo-4-a-routine-versus-an-actions-workflow.md)


*Demo 3 of 9*
