# JDC Cost Codes — Reference

**Two files in this folder hold the actual codes:**
- `JDC Cost Codes - Revised (Default).xlsx` — 484 items across 24 categories. **Use these by default.**
- `JDC Cost Codes - Full Library (Fallback).xlsx` — 4,639 items across 30 categories. Only pull from here if a needed item isn't in the revised set.

When in doubt, ask August before reaching into the fallback library.

## Categories (revised set — 24 divisions)

| # | Category | Item count | Notes |
|---|---|---|---|
| 01 | Plans and Permits | 1 | Catch-all line `01.0000.010` priced as needed |
| 02 | Site Preparation | 96 | Demo work — most-used category |
| 03 | Excavation | 6 | Sub work (Hall's, Kemper) |
| 04 | Concrete | 22 | Mix of materials, labor, sub |
| 05 | Masonry | 9 | Brick, block, stone veneer, parging |
| 06 | Floor Framing | 16 | Joists, beams, subfloor |
| 07 | Wall Framing | 5 | Bearing/non-bearing, sheathing |
| 08 | Roof Framing | 8 | Stick, trusses, sheathing |
| 09 | Roofing, Flashing | 17 | Shingles, metal, gutters |
| 10 | Exterior Trim, Decks | 23 | Fascia, soffit, decking, porch ceilings |
| 11 | Sidings | 13 | |
| 12 | Doors and Trim | 26 | |
| 13 | Windows and Trim | 27 | |
| 14 | Plumbing | 41 | Most fixtures sit here w/ allowance lines |
| 15 | Heating and Cooling | 11 | |
| 16 | Electrical | 32 | |
| 17 | Insulation | 8 | |
| 18 | Interior Walls | 12 | Drywall, tile backsplash live here |
| 19 | Ceiling Covering | 5 | |
| 20 | Millwork, Trim | 37 | Interior trim, doors |
| 21 | Kitchen Cabinets | 22 | Cabinets + countertops live here |
| 22 | Specialties | 16 | Mirrors, shelving, accessories |
| 23 | Floor Covering | 14 | Hardwood, LVP, tile, carpet |
| 24 | Painting | 17 | |

The revised set drops **25 Clean-up** and the placeholder **26–30 User divisions** that exist in the full library. Final clean is rolled into other lines or handled outside the cost code system.

## Code Format

Every code follows: `[Division].[Item].[Variant]` — e.g.:
- `02.4070.` — Remove toilet
- `14.1020.010` — Toilet, new work, 2 piece, white
- `21.4236.` — Countertop, 3/4" Quartz

A trailing dot (no variant) is the standard form. A trailing 3-digit suffix means a specific variant (e.g., `.010` for white toilet).

## Cost Code Suffix Convention (Old-Format Estimates Only)

Old-format estimates split a single revised code into multiple rows by cost type:
- `02 Site Preparation Labor`
- `04 Concrete Materials`
- `04 Concrete Labor`
- `04 Concrete Subcontract`
- `14 Plumbing Subcontract`

The **new Buildertrend format** does NOT use this suffix. Cost type is captured in a separate column (`Cost Type`) and the Cost Code stays as the bare division name (e.g., `04 Concrete`).

## Defaults

- **Markup:** 50% (yields 33.33% margin) on every line, both materials and labor, in the cost-code estimating system.
- **Markup type:** Percentage (`%`).
- **Taxable:** Non-taxable on all sample lines reviewed.
- **Allowances:** When a line carries an allowance (toilet, faucet, vanity, countertop), embed the allowance amount in the Description field with a newline, e.g.:
  ```
  Install new kitchen sink
  $500 allowance
  ```
