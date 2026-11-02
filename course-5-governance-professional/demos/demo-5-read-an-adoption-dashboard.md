# Demo 5: Read an Adoption Dashboard

**Course:** Claude Governance, Compliance and Conformance Professional (Claude MasterClass Professional, Course 5)
**Demo:** 5 of 6
**Time:** about 15 minutes

> Part of **[Claude Governance, Compliance and Conformance Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Read a dashboard whose headline metric hides problems, sort metrics into activity, value and risk, and set a response. Time: about 15 minutes.

**Files:** [`$FILES/demo5_reading_sheet.md`](../demo-files/demo5_reading_sheet.md), [`$FILES/demo5_adoption_dashboard_monthly.csv`](../demo-files/demo5_adoption_dashboard_monthly.csv), [`$FILES/demo5_adoption_dashboard_by_department.csv`](../demo-files/demo5_adoption_dashboard_by_department.csv).

**Context:** The leadership dashboard says 78 percent of licensed seats are active weekly, up from 52 percent in March. All figures are synthetic. The class has the data behind the headline.

**Steps:**

1. Show the headline. Ask the room whether this is good news and what they would want to know.
2. Open the monthly file and read the last column. Ask what prompts per active user is doing while the active percent rises.
3. Open the department file. Ask the room to find the three departments that most worry them, and why.
4. Fill the metric-kind table together: activity, value or risk.
5. Ask the class to name at least three problems, each with the number that shows it.
6. Write one response per problem with an owner and a date. Close by asking for a value metric the dashboard lacks.

**Expected result:** The class finds that growth is broad and shallow: active percent keeps rising while prompts per active user peaked in June at 175 and fell to 164. They find that Sales and Engineering produce about 73 percent of all prompts (37,300 of 51,300). They find Sales at 98 percent active with only 2 intake requests and 9 of its 14 exceptions past expiry. They find Tier 3 evidence at 2 of 7 uses. They find Support, which handles Regulated data, only 49 percent active. They note 88 seats are idle on a flat budget.

> **Instructor note:**
> - Key to metric kinds. Weekly active percent, total prompts and prompts per active user are activity. Intake requests are a process count. Exceptions past expiry and Tier 3 uses with evidence are risk. No value metric exists on the dashboard. Suggested value metrics: a cycle time or handling time with a baseline, as in Demo 6's input pack.
> - All numbers are synthetic and invented. Do not present them as benchmarks for any real company.
> - A student may argue that low Sales intake means Sales is compliant. Point to the 9 past-expiry exceptions: heavy use with little intake suggests uses nobody registered.
> - Support's low activity is a different problem from Sales' high activity. One is a stall, the other is a control gap. A single adoption target would push the wrong way for both.

**Why this matters:** An adoption target set without a value or risk measure rewards logins. A stall can look like success and a risk can look like momentum.

---

**Previous:** [Demo 4: Trace a Policy Line to Evidence](demo-4-trace-a-policy-line-to-evidence.md) · **Next:** [Demo 6: Assemble a Board Report](demo-6-assemble-a-board-report.md)


*Demo 5 of 6*
