# Estimating Resources

Reference files for the Estimating workstation. Loaded automatically when Claude works on a JDC estimate.

## What's in here (as of 2026-05-04)

**Cost codes:**
- `JDC Cost Codes - Revised (Default).xlsx` — 484 items / 24 divisions. Default working library.
- `JDC Cost Codes - Full Library (Fallback).xlsx` — 4,639 items / 30 divisions. Fallback only.
- `JDC Cost Codes Reference.md` — How the codes are structured, suffix conventions, code format.

**Buildertrend export:**
- `BT Export Template - Gullion (Reference).xls` — Working example pulled from the 2026 Gullion job. The format JDC imports into Buildertrend.
- `Buildertrend Export Format.md` — All 27 columns documented with the math.

**Pricing:**
- `Pricing Library.md` — 2026 unit-cost benchmarks by code (demo, plumbing allowances, framing, concrete, etc.) plus the JDC sub/supplier shortlist with rep names.

**New builds:**
- `New House Estimating - Gap Notes.md` — Current state (lump-sum phase cost sheets) vs. where August wants to go (line-item cost code estimates). Open questions to resolve before the first new-build estimate.

## How Claude uses this folder

When you say "build an estimate for [job]", Claude will:
1. Read the reference docs in this folder (already condensed — Claude doesn't need to re-read the underlying Jobs folder unless something specific is needed).
2. Look at the job-specific intake in `JDC/Jobs/[year]/[client]/`.
3. Produce a draft `.xlsx` estimate in JDC's 9-column working format.
4. After your approval, generate a 27-column `.xls` Buildertrend import file.

## When to refresh these references

Re-run the research and update these files when:
- Cost codes are revised (add new items or change pricing)
- Buildertrend export format changes
- Markup policy changes
- New regular subs/suppliers come into rotation
- A new job type comes up that the current pricing library doesn't cover well

Otherwise, these references are good to use as-is.
