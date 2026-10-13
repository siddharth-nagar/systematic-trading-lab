# Research 001 — NIFTY calendar seasonality

**Status:** descriptive analysis completed on secondary index-price data; statistical testing and official NSE cross-check remain open.

## Baseline seasonal matrix

Computed from `data/nifty50_monthly_2000_2026_partial.csv`, ranking through December 2025 (January 2000 has no prior-month price).
`n` is the observed number of monthly returns. Values in percentage points.

| Month | n | Mean | Median | Positive | Frequency | Std |
|---|---:|---:|---:|---:|---:|---:|
| Jan | 24 | -0.83% | -0.84% | 8 | 33.3% | 5.81% |
| Feb | 26 | -0.12% | 0.94% | 14 | 53.8% | 4.61% |
| Mar | 26 | 0.03% | 0.72% | 14 | 53.8% | 8.14% |
| Apr | 26 | 1.56% | 1.16% | 15 | 57.7% | 5.59% |
| May | 26 | 0.91% | 1.21% | 14 | 53.8% | 8.31% |
| Jun | 26 | 1.48% | 1.57% | 17 | 65.4% | 5.55% |
| Jul | 26 | 1.75% | 2.45% | 18 | 69.2% | 5.14% |
| Aug | 25 | 1.07% | 0.62% | 15 | 60.0% | 4.82% |
| Sep | 25 | 1.98% | 2.00% | 15 | 60.0% | 5.72% |
| Oct | 25 | 0.54% | 1.47% | 15 | 60.0% | 8.33% |
| Nov | 25 | 2.44% | 3.20% | 15 | 60.0% | 5.60% |
| Dec | 25 | 2.63% | 2.07% | 17 | 68.0% | 4.66% |

These figures are *descriptive* rather than proof of exploitable alpha. They include overlapping broad bull and bear regimes across years, and no trading costs.

## Formulas

- Return: `r[y,m] = 100 * (close[y,m] / close[prior month] - 1)`
- Mean: `sum(r)/n`
- Median: middle sorted value (or average of two middle observations)
- Positive frequency: `100 * count(r>0)/n` (zero counts as non-positive)
- Sample standard deviation: `sqrt(sum((r-mean)**2)/(n-1))`
- Yearly price-index OHLC: month close = final available daily close; month high/low = extreme of daily high/low.

## Scientific caveats

1. NIFTY price-index history contains a long-run upward drift; distinguish positive returns from *excess returns relative to the unconditional monthly mean*.
2. A positive monthly mean across 12 sampled months is not independent evidence of seasonality because equities tend to drift upward.
3. Examine tail outcomes, medians, and uncertainty, not just positive frequency.
4. Subperiod stability: 2000–2012 versus 2013–2025 (with incomplete January 2000 handled).
5. For conditional September–October–November tests, define the event and null hypothesis **before** testing and avoid future-leaking conditions.
6. Carry out daily chronological event reconstruction before concluding whether October broke September's low before recovering.
7. Validate primary-source daily series and missing trading dates before high-stakes use.
8. This is about index-price behaviour; a derivatives strategy has execution costs, carry and options greeks not captured here.

## Learning connection to Kaufman Chapter 10

The workflow implements descriptive seasonal averages, frequency, distribution robustness, subperiod instability and conditional seasonal hypotheses. It separates a calendar *candidate effect* from an independently validated tradable rule.

## Next experiment

Complete a **pre-registered** conditional study:
- H1: November return differs conditional on September return and October intramonth breach of September low.
- Define October breach: **October daily LOW < minimum September daily LOW**.
- Candidate strata: October positive/negative close, September positive/negative, subsequent November outcome.
- Alternative outcome: November return relative to unconditional November average.
- Compare frequencies/means/medians with sample counts and bootstrap uncertainty.
- Ensure October signal is observed no later than October's final close; November performance is the forward target.
- Check if any apparent result survives the two subsamples and a holdout period.
