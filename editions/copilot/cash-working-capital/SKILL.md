---
name: cash-working-capital
description: "Analyze operating cash, receivables, inventory and payables with reconciled working-capital metrics. Use for cash bridges, overdue aging, DSO/DIO/DPO, cash-conversion-cycle analysis, collection scenarios or short-term cash forecasts, with explicit stock-versus-flow and denominator checks."
---

# Cash and working capital

## Microsoft 365 Copilot edition

Default output: Give the requested result directly with concise source references, necessary calculations, recommendations, and material unresolved exceptions. Keep routine verification internal. Do not create audit tables, audit logs, audit text, new worksheets, or unrelated reports unless specifically requested; a requested data table, model, or report remains allowed. Preserve existing business logic and avoid filler, AI/process commentary, and unnecessary summaries or tables.

Use this skill in the approved work account and the current Microsoft 365 host. Prefer the open Excel workbook or PowerPoint presentation when native editing is available. A connection to SharePoint, a Power BI model, or a local computer exists only if this session exposes and authorizes it. A Microsoft 365 Copilot subscription does not imply GitHub Copilot or a VS Code agent.

For uploaded files, use available sandbox tools and preinstalled libraries only. Do not run installers or authenticated HTTP requests inside a cloud skill script. Use enabled work connectors for authorized SharePoint retrieval. Preserve source locators, the reporting cutoff and the actual permission scope. Never treat a search result or file preview as the complete source population.

Windows Python and VS Code are a separate, optional route. When the task needs local files or a package absent from this session, prepare an inspectable Python script or query for the user to run in the approved local environment. State that it has not run on their PC. Continue analysis only from returned results and reconciled control totals. A generated DAX measure or Power Query expression is a proposal until it has been applied and checked in the model.

Use the requested skill explicitly when available. If the tenant cannot import skills, the user can paste this workflow into a conversation or an authorized agent's instructions. A file attachment alone does not register a reusable skill. Do not claim this imported copy automatically tracks GitHub; updates require replacement or the host's documented folder refresh.

Build a management analysis using supplied balances, transactions and approved KPI definitions. Preserve the reporting boundary and distinguish observed cash movements, balance movements and modeled opportunities. Calculate with available tools when possible; otherwise provide formulas and mark results uncomputed. Do not invent bank balances, payment dates, contractual terms or missing source populations.

## Set the basis

Confirm the as-of date, analysis period, actual calendar-day count or approved convention, entities, currencies, consolidation boundary and unit scale. Establish whether balances are gross/net of tax, intercompany, impairment, factoring, disputed items, advances or credit notes. Match the same scope in each numerator and denominator. Ask for the approved KPI definition when alternatives materially change the result.

Inventory cash opening/closing balances and movements; AR/AP opening, closing and intermediate snapshots if available; invoice/payment details; credit sales; COGS; credit purchases; and inventory data. Record file version, source locator and extract time. Keep confidential balances and account details within the approved work environment.

## Reconcile before interpreting

1. **Cash bridge.** Reconcile opening cash plus receipts minus payments plus separately identified translation/reclassification effects to closing cash. Show unreconciled differences. Transfers between accounts within the same reporting boundary cancel in the consolidated bridge; do not treat both legs as external funding or operating cash. Keep restricted cash and cash equivalents aligned with the supplied policy and scope.
2. **Balance bridges.** Reconcile AR, inventory and AP opening balances to closing balances using the relevant transaction classes. Separate cash settlement from non-cash FX, write-offs, reclassifications, acquisitions/disposals and scope changes. A balance-sheet movement alone is not proof of cash generated or spent.
3. **Working capital.** If the agreed management definition is trade AR plus inventory minus trade AP, show each component and any explicitly included additions. Under a constant scope, increases in AR/inventory generally use cash and increases in AP generally release cash; quantify this only after separating non-cash and scope effects. Do not present this approximation as a completed statutory cash-flow statement.

## Calculate comparable metrics

Use the organization's approved method. When a conventional period-ratio method is requested, state the formulas and all substitutions:

| Metric | Period-ratio calculation | Required alignment |
|---|---|---|
| DSO | Average trade AR / credit sales in the period × days in the period | Match entities, currency and tax/sales scope; cash sales are not credit sales |
| DIO | Average inventory / COGS in the period × days in the period | Match inventory population and cost basis |
| DPO | Average trade AP / credit purchases in the period × days in the period | Purchases and COGS differ; label COGS as a proxy if used |
| Cash conversion cycle | DSO + DIO − DPO | Use comparable periods, days and populations |

Use time-weighted or sufficiently frequent balances when available and appropriate. If only opening and closing balances exist, label their arithmetic mean a two-point approximation and note seasonality or intra-period volatility. If only closing balances exist, report an explicitly named end-balance proxy; do not call it average-balance DSO. Do not average entity ratios to obtain a group ratio: aggregate aligned numerator balances and denominator flows first, using a consistent currency basis.

Do not sum monthly balance snapshots as though they were transactions. Do not use a monthly flow with an annual-day multiplier unless the flow is annualized consistently. Check zero, negative or implausible denominators; return not meaningful with an explanation when the metric's economic interpretation fails. Retain the underlying amounts even when the ratio is suppressed. Do not substitute zero for missing data.

## Analyze aging and forecast cash

Age invoices from the specified due-date or invoice-date basis and disclose which was used. Define bucket boundaries, the as-of timezone/date, treatment of partial payments, credits, disputes and missing due dates. Reconcile aging balances to the same-date subledger and explain differences from the GL. Do not assign missing terms from a customer name.

For a collection or payment forecast, use open-item amounts, agreed timing assumptions and explicit delay scenarios. Show opening cash, dated receipts/payments, financing assumptions if supplied, and closing cash for each interval. A forecast must distinguish contractual due dates from expected payment dates and committed flows from assumptions. Avoid double-counting collections already received or invoices already settled in the opening snapshot.

Translate a days improvement into a potential working-capital effect only with a stated stable flow basis. For example, a modeled DSO reduction multiplied by aligned daily credit sales is a sensitivity estimate; it is not evidence that cash has been collected. Do not add that estimate to an invoice-level collection forecast if the same improvement is already modeled there.

## Deliver

Return only the requested cash, working-capital, aging, KPI or scenario result. Include necessary formulas, units, source references and material residuals or limitations. Use a business-data table when requested or needed for the comparison; do not turn a single ratio question into a full bridge, KPI, aging and audit pack. Keep routine reconciliation checks internal and provide a separate check register or audit report only when specifically requested.

Example request: “Compare October and November working capital using these balances and credit sales. Calculate DSO, DIO and DPO with the available average balances, reconcile the aging, and estimate a five-day DSO improvement without treating it as realized cash.”

## Edition record

Finance skills 1.1.0; copilot edition; source review 2026-11-25. This date records the package review, not the freshness of a user's business data.
