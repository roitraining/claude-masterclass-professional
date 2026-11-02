# Brightwater Health Supply: Organization Brief

Fictional company. Every person, customer and figure here is invented for training. This is the shared case for every demo and lab today.

## The company

Brightwater Health Supply distributes medical and lab supplies to clinics, hospital networks and care homes. It has about 2,600 employees and 140 contractors. Headquarters and the main warehouse are in Ohio, a second warehouse is in Texas, and a Dublin, Ireland office (about 180 staff) runs EU sales and support.

## Departments and what they handle

- **Sales** (about 210): contract renewals and pricing. About 60 inside-sales reps use personal phones for work messaging.
- **Customer Support** (about 160): tickets that contain clinic contact details, order notes and sometimes health-related details a clinic typed in.
- **Operations and Warehousing** (about 900, plus most contractors): stock, shipping, supplier orders.
- **Finance** (about 70): ledgers, invoices, customer payment references and card data handled by the payment processor.
- **HR** (about 45): hiring, performance and pay records for US and EU staff.
- **Legal and Compliance** (about 22): contracts, customer audits.
- **IT and Security** (about 85): identity, network, endpoints.
- **Engineering** (about 70): internal ordering and logistics software.
- **Marketing** (about 40): content, campaigns, images.
- **Clinical Affairs and Quality** (about 35): product complaints and adverse-event reports.

## Data classes

| Class | Examples |
|---|---|
| Public | Product sheets, published prices |
| Internal | Org charts, meeting notes without customer detail |
| Confidential | Contract terms, negotiated pricing, source code, financials |
| Regulated | Health-related details in tickets and complaints, payment card data, employee personal data, any personal data of people in the EU |

## One customer that matters

Halvern Hospital Network (fictional) is Brightwater's largest customer. Its contract requires 30 days' written notice before its data is used in any new automated processing, and gives Halvern the right to audit how its data is handled with 30 days' notice. Legal owns the contract. No process yet turns that clause into action.

## AI use today

- Claude Enterprise: a 400-seat pilot bought in March (Sales 90, Engineering 70, Marketing 40, Support 80, Finance 30, Legal 15, HR 20, Operations 55). Identity, roles and groups are managed through the company identity provider.
- Engineering also uses Claude Code on internal repositories.
- Sales reps use free consumer chatbots on personal phones to draft renewal emails, sometimes with contract excerpts pasted in.
- Support agents installed a browser extension that summarizes tickets. IT did not approve it and does not know the vendor.
- The applicant tracking vendor switched on an AI ranking feature by default. HR uses it for US and Dublin hiring.
- A meeting transcription assistant records calls in Dublin. Nobody is recorded as its owner.
- Marketing pays for an image generator on a personal subscription, expensed on a card.
- Finance analysts paste ledger extracts into Claude Enterprise for variance commentary.

## The people and what each wants

| Person | Role | Position |
|---|---|---|
| Dana Whitfield | CEO | "AI-enabled by year end." |
| Marcus Oyelaran | Chief Revenue Officer (CRO) | No approval step longer than 2 business days. Sales loses deals to speed. |
| Priya Raman | General Counsel | Legal sign-off before any AI use touches customer or employee data. |
| Tomas Lindqvist | CISO | Block unapproved tools and give every approved tool an owner. |
| Elena Rossi | CFO | Flat budget. The program gets 0.5 of a full-time person, no new headcount. |
| Ben Adeyemi | COO | Proposed chair of an AI Governance Board. |
| Aisha Karim | CHRO | Wants HR to keep using the ranking feature. |
| Ciaran Doyle | Head of Dublin | Dublin employee representatives expect to be consulted before anything monitors staff. |
| Margaret Sloan | Audit Committee chair | Wants a written report every quarter. |

## What the company can already do (capabilities, not tasks)

Professional 4 covered these. In this course they are things that exist and can be cited as evidence sources. Nobody here configures them. See `technical_capabilities_card.md`.

## Ground rules for today

- Work only from this brief and the files in your pack. Do not invent facts about Brightwater. If you need a fact that is missing, write it as an assumption and label it.
- Regulation is awareness only. Nothing in this course is legal advice. Counsel confirms current dates and duties.
