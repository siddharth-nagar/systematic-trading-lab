# NIFTY seasonality — neutral research protocol

**Principle:** no month, direction, or previously discussed relationship is privileged. The analysis starts with all 12 months on equal terms and reports null, positive and negative results.

## Stage 1 — Exploratory, descriptive (completed on secondary data)

Calculate the same statistics for all 12 months:
- observation count and data completeness;
- mean and median close-to-close price-index return;
- positive, negative and zero-return frequencies;
- standard deviation, worst/best outcome, and quantiles;
- entire year-by-month return matrix;
- subperiod summaries and uncertainty.

Do **not** call a month an 'edge' merely because its mean or hit rate is high. Report all months, including weak or inconclusive patterns.

## Stage 2 — Data quality (required before confirmatory tests)

- Reconcile missing months and two source disagreements with official NSE NIFTY 50 daily data.
- Confirm holiday/calendar completeness, return convention and price-index (not total-return) basis.
- Exclude partially observed months from full-month comparisons.
- Keep a provenance log for any edits. Never quietly fill missing prices.

## Stage 3 — Predefined omnibus hypotheses

Primary null:
`H0: mean calendar-month returns do not differ, apart from sampling error`.
Alternative:
`H1: at least one calendar month differs`.

Additional **separate** questions:
- Do calendar-month return distributions differ in downside tail risk or volatility?
- Are any observed calendar effects stable across pre-specified time blocks?
- Does a calendar model predict future returns better than an unconditional benchmark out of sample?

Use confidence intervals and, where appropriate, resampling that respects time dependence. Consider tests of all twelve months together before post-hoc month comparisons.

## Stage 4 — Explanations and conditional tests

After the broad analysis, register economically motivated explanations or conditional relationships prospectively. Record:
- ex-ante hypothesis and specific outcome;
- indicator definitions and **information availability time**;
- evaluation window and comparison/control group;
- minimum sample requirements;
- multiple-testing corrections or explicit exploratory status;
- out-of-sample/holdout performance and limitations.

Prior informal investigations of particular month combinations are not included as pre-registered hypotheses, and must not guide model selection.

## Stage 5 — Trading relevance (later)

Only after robust statistical evidence: translate a narrowly defined signal into an executable strategy and include futures/ETF/option-specific financing, dividends, fees, slippage, liquidity and risk sizing.

## Decision log

- **2026-10-13:** Standardise the research framework to month-neutral, symmetric hypothesis testing. No preferred seasonal months or previously explored conditional relationships.
- **Current stage:** descriptive baseline / data audit, not validated trading signal.
