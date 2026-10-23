# NIFTY 50 — first omnibus seasonality test

**Run date:** 2026-10-13  
**Dataset:** recorded monthly price-index closes, 2000–2025 (2026 partial excluded)  
**Data status:** provisional secondary sources, six missing calendar months in 2000–2001, two conflicting daily close observations from overlapped data.
**Analysis status:** exploratory implementation of neutral predeclared omnibus null. Not a confirmatory, official-source-verified result.

## Hypothesis

H0: mean returns are identical across the 12 calendar months.  
H1: at least one calendar-month mean differs.

**Unconditional benchmark**: average across all observed complete-contiguous monthly returns.

## Results

- Valid calendar-month returns: **302**.
- Unconditional mean return: **1.119732%**.
- One-way ANOVA-style F ratio (effect of month, fixed group memberships): **0.829125**.
- Within-year shuffle, 5,000 replicates, Monte Carlo p value: **0.574885** (seed 7273).
- Under a conventional 0.05 threshold, **do not reject the omnibus equal-means null**.

## Interpretation and limits

No strong evidence of a difference among the 12 calendar-month means in **this test and dataset**. This does not prove a complete absence of seasonality: the sample is limited, power may be low and effects may change over time.

The within-year shuffle preserves each year's observed returns and missing-month pattern. It assumes return-month labels are exchangeable within a year under H0. Cyclic market dynamics and temporal dependence may violate this assumption; a year-block bootstrap/robust regression provides a sensitivity check.

The test is descriptive/inferential, **not** a trading backtest. It does not account for dividends, fees, futures carry or systematic execution.

We must resolve gaps and mismatched prices against NSE Indices official data before claiming an official-quality result. We must also preselect complementary tests and holdouts, and avoid treating the most attractive individual month as a new pre-planned hypothesis after seeing these outcomes.

## Subperiod stability

`analyse.py` saves the same descriptive statistics for all 12 months in two fixed calendar intervals:
- 2000–2012
- 2013–2025

Notable differences should be reported without preferentially selecting a month. The complete table is in [`subperiods.csv`](subperiods.csv).

## Next audit steps

1. Obtain official NIFTY 50 index daily history for the missing months and the two conflicting records, recording file provenance.
2. Reproduce all calculations on that independently sourced dataset.
3. Add year-block bootstrap uncertainty intervals and a sensitivity test for the omnibus null.
4. Evaluate out-of-sample predictive value against constant-mean forecast, using calendar-time splits.
