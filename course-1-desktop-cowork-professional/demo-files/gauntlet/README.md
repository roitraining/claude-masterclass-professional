# Gauntlet folder

- `gauntlet.py`: the runner. See `scorecard.md` for what it checks and how to run it.
- `scorecard.md`: the scoring rules and tiers (hand this to students).
- `products.json`: the contract for each product: plugin name, server key, skill, agents, commands, tools.
- `evals/<product-folder>/`: the eval suite for each product: cases `trig-*`, `qual-*`, `adv-*`, `cold-1-install`, and `mocks/<server>/<tool>.md`. Generated from the product datasets.
- `adversarial/ADVERSARIAL-PACK.md`: the same adversarial prompts as a checklist to run by hand in Cowork and chat.
- `SECURITY-CHECKLIST.md`: the manual checklist behind the Security section.
- `tools/build_evals.py`: instructor tool that regenerates `evals/`, `products.json`, and the adversarial pack from the datasets. Run it after you edit a dataset or a case.
- `sample-report/`: a worked Gauntlet report for Demo 6.

Instructor notes:

- The runner never modifies a student's folder. It works on a temporary copy.
- A full run is roughly 40 agent runs at the default 2 runs per case, plus judge calls. Measure the real cost on your sandbox account before the class and set `--max-cost-usd` accordingly. No full run has been priced yet.
