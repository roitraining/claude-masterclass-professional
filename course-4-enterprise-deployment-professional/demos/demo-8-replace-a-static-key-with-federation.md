# Demo 8: Replace a Static Key With Federation

**Course:** Claude Enterprise Deployment and Security Operations Professional (Claude MasterClass Professional, Course 4)
**Demo:** 8 of 8
**Time:** about 15 minutes

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Replace a static key with a short-lived credential obtained at run time, and compare it with a CI credential from `claude setup-token`. Time: about 15 minutes.

**Files:** none; the sample scripts are inline below.

**Context:** Moving from Console keys to an Enterprise deployment means removing leftover Console credentials (API key variables and `apiKeyHelper`), signing in with `/login`, verifying with `/status`, and moving CI to a `claude setup-token` credential or keeping Console keys for automation. Secure credential storage uses Keychain on macOS and a mode-0600 file on Linux.

**Steps:**

1. Show a settings file with a key placed directly in it. Ask the class what is wrong: it is long-lived, copyable, and unaudited.
2. Show the pattern that replaces it. A helper script obtains a short-lived credential from a broker when it is needed. The local stand-in below issues a fake token with an expiry:

```python
import datetime, secrets
exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
print("FAKE-TOKEN-DO-NOT-USE-%s" % secrets.token_hex(4))
print("expires", exp.isoformat(), file=__import__("sys").stderr)
```

3. Run it twice and show two different values and the expiry on stderr. Point out that the token is fictional and does not authenticate.
4. Show where a helper is referenced in settings (the `apiKeyHelper` setting) and what removes the static key.
5. On the board, compare three CI options: a `claude setup-token` credential, a Console key for automation, and a broker-issued credential. Fill in what each costs to rotate, who owns it, and what the audit trail shows.
6. Ask who owns the credential when its holder leaves the company.

**Expected result:** Two runs produce two different short-lived values, and the class completes a three-row comparison with an owner and rotation plan for each option.

**Fallback (no live tenant):** The demo runs fully offline. If the class asks to see a real federated login, show a screenshot outline of `/login` and `/status` captured on the sandbox.

> **Instructor note:** Federation features on the Anthropic side (for example, exchanging a cloud identity for a Claude credential), the lifetime of a `claude setup-token` credential, and how often `apiKeyHelper` is called are not in the verified facts: UNVERIFIED. This demo teaches the pattern with a local stand-in and does not claim a product feature. Rehearse any real federated path before presenting it as one.

**Why this matters:** The credential that leaks is the one that lives longest. Short life, a named owner, and an audit trail are what make a leak survivable.

---

**Previous:** [Demo 7: Read the Sandbox Audit Trail](demo-7-read-the-sandbox-audit-trail.md)


*Demo 8 of 8*
