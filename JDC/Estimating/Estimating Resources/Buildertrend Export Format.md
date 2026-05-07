# Buildertrend Export Format — JDC Standard

Reference file in this folder: `BT Export Template - Gullion (Reference).xls`. That's the working example pulled from the 2026 Gullion job. **All approved estimates get exported in this format for BT import.**

## File type

`.xls` (legacy Excel format — not `.xlsx`). Single sheet named `Sheet1`.

## Column structure (27 columns, exact order)

| # | Column | Notes |
|---|---|---|
| 1 | Category | "Real Codes" on every line (literal value JDC uses) |
| 2 | Cost Code | Full revised code division name, e.g. `02 Site Preparation`, `14 Plumbing`, `21 Kitchen Cabinets`. **No Labor/Materials/Subcontract suffix.** |
| 3 | Title | Numeric BT internal line ID. New lines: leave blank or use a placeholder; BT assigns on import |
| 4 | Parent Group | Short division name, e.g. `02 Site Prep`, `14 Plumbing`, `18 Interior Wall`, `21 Kitchen Cabinets` |
| 5 | Parent Group Description | Empty |
| 6 | Subgroup | Empty |
| 7 | Subgroup Description | Empty |
| 8 | Option Type | Empty |
| 9 | Line Item Type | `Estimate` on every line |
| 10 | Description | Plain-English line item. Allowances appended on a new line: `Install new kitchen sink\n$500 allowance` |
| 11 | Quantity | Decimal |
| 12 | Unit | `EA`, `LF`, `SF`, `+SF` (the +SF/+LF prefix means "per additional unit") |
| 13 | Unit Cost | Builder cost per unit (pre-markup) |
| 14 | Cost Type | Empty in samples — not consistently populated |
| 15 | Marked As | Empty |
| 16 | Builder Cost | = Quantity × Unit Cost |
| 17 | Markup | `50` (numeric, no % sign) |
| 18 | Markup Type | `%` |
| 19 | Unit Price | = Unit Cost × 1.5 (when markup is 50%) |
| 20 | Client Price | = Builder Cost × 1.5 |
| 21 | Margin | `0.3333` (decimal margin matching 50% markup) |
| 22 | Profit | = Client Price − Builder Cost |
| 23 | Taxable | `Non-taxable` on every JDC line |
| 24 | Tax Amount | `0.0` |
| 25 | Total Price | = Client Price (since non-taxable) |
| 26 | % Invoiced | `0.0` on a fresh export |
| 27 | Internal Notes | Empty for client-facing items; can hold ops notes |

## Math cheatsheet (50% markup standard)

```
Builder Cost  = Qty × Unit Cost
Unit Price    = Unit Cost × 1.5
Client Price  = Builder Cost × 1.5
Profit        = Client Price − Builder Cost  (= Builder Cost × 0.5)
Margin        = Profit / Client Price        (= 0.3333)
```

If JDC ever uses a different markup, recompute Margin as `markup / (100 + markup)`.

## Parent Group naming map

The Parent Group is the abbreviated category name. Observed mappings:

| Cost Code (col 2) | Parent Group (col 4) |
|---|---|
| 02 Site Preparation | 02 Site Prep |
| 14 Plumbing | 14 Plumbing |
| 18 Interior Walls | 18 Interior Wall |
| 21 Kitchen Cabinets | 21 Kitchen Cabinets |

Pattern: drop trailing `aration`/`s` where it abbreviates cleanly (Preparation → Prep, Walls → Wall). When uncertain, match the example file exactly for the divisions seen there; for any new division, ask August before guessing.

## When to produce the BT export

Only after August has reviewed and approved the draft estimate (the working `.xlsx` in the old 9-column format). The export is the final step — do not generate it alongside the draft. The flow is:

1. Build draft `.xlsx` (old 9-column format) → August reviews →
2. Apply revisions →
3. Generate BT export `.xls` in this 27-column format →
4. August imports into Buildertrend.
