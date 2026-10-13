# Research 001 — NIFTY calendar seasonality

**Status:** descriptive analysis completed on secondary index-price data; statistical testing and official NSE cross-check remain open.

## Baseline seasonal matrix

Computed from `data/nifty50_monthly_2000_2026_partial.csv`, ranking through December 2025 (Months following absent observations have no valid prior-month baseline; January 2000 likewise).
`n` is the observed number of monthly returns. Values in percentage points.

| Month | n | Mean | Median | Positive | Frequency | Std |
|---|---:|---:|---:|---:|---:|---:|
| Jan | 23 | -0.95% | -1.10% | 7 | 30.4% | 5.91% |
| Feb | 25 | -0.40% | 0.82% | 13 | 52.0% | 4.47% |
| Mar | 26 | 0.03% | 0.72% | 14 | 53.8% | 8.14% |
| Apr | 26 | 1.56% | 1.16% | 15 | 57.7% | 5.59% |
| May | 26 | 0.91% | 1.21% | 14 | 53.8% | 8.31% |
| Jun | 26 | 1.48% | 1.57% | 17 | 65.4% | 5.55% |
| Jul | 26 | 1.75% | 2.45% | 18 | 69.2% | 5.14% |
| Aug | 25 | 1.07% | 0.62% | 15 | 60.0% | 4.82% |
| Sep | 24 | 2.27% | 2.14% | 15 | 62.5% | 5.65% |
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

## Next experiment — neutral omnibus study

Audit the daily source against NSE; then compare all twelve calendar months using identical descriptive and inferential procedures. Compare against an unconditional return benchmark, examine uncertainty and multiple testing, and predefine sample splits. Do not favour months or conditional month sequences based on earlier exploratory discussions. Any secondary hypothesis arises from documented results and is labelled exploratory until validated out of sample.
