# Kaufman Chapter 10 — Seasonality

## Status

**Chapter complete (notes written retrospectively).**

The applied work for this chapter lives in [`02_nifty_seasonality/`](../../02_nifty_seasonality/README.md). This folder records the chapter's core concepts and replicates the book's ratio-to-moving-average seasonal index in [`seasonal_index.py`](seasonal_index.py).

These notes were written after the NIFTY study. Check the formulas against the book text before relying on them.

---

## 1. Price components

[
\text{Price} = \text{Trend} + \text{Seasonal} + \text{Cycle} + \text{Noise}
]

Seasonality is the most regular cycle: a calendar (12-month) cycle with a physical or institutional cause (harvests, weather, tax years, fiscal year-ends, holidays).

To see one component, remove the others first. Chapter 11 starts from exactly this step.

---

## 2. Removing the trend

A raw monthly average of prices or returns mixes seasonality with long-run drift. Two standard ways to remove the trend:

- **Moving-average detrending:** compare price with a 12-month moving average.
- **Annual differences:** (P_t - P_{t-12}) on monthly data, or (P_t - P_{t-252}) on daily data.

On an upward-drifting equity index, almost every month has a positive average return. That reflects the drift, not seasonality.

---

## 3. Simple average method

For each calendar month (m):

[
\bar r_m = \frac{1}{n_m}\sum_{y} r_{y,m}
]

Also record the **frequency** of positive returns (how consistent the pattern is), not only the average size.

This is what `02_nifty_seasonality/analyse.py` computes.

---

## 4. Ratio-to-moving-average seasonal index

1. Compute a **centred** 12-month moving average. Because 12 is even, use a 2×12 average so it lines up with a month:

[
CMA_t = \tfrac12\left(\overline{P}_{t-6..t+5} + \overline{P}_{t-5..t+6}\right)
]

2. Ratio of price to trend:

[
R_t = 100 \cdot \frac{P_t}{CMA_t}
]

3. Average (R_t) for each calendar month.
4. Normalise the 12 averages so they sum to 1200 (they average 100).

An index of 103 means that month's price typically sits about 3% above trend.

**Deseasonalise:** divide price by its month's index (×100).

**Look-ahead warning:** the centred MA uses the *next* 6 months. That is fine for describing history, but the index cannot be used as a real-time signal without rebuilding it from past data only.

### NIFTY result (2000–2025, see `results/seasonal_index.csv`)

The index runs from about 98.2 (Mar) to 103.2 (Dec). Each month's ratios have a standard deviation of about 5–8 points across 23 years, so the uncertainty in each monthly average is roughly ±1.3 points. Most of the pattern is within noise. This matches the omnibus test in `02_nifty_seasonality` (p ≈ 0.57).

Note that a **level** index and **return** averages answer different questions. December has the highest level relative to trend, so January (the move away from that level) shows the weakest average return.

---

## 5. Other calendar effects

- Day-of-week, turn-of-month and pre-holiday effects use the same logic on daily data.
- Seasonal **volatility** can matter more than seasonal direction (for example, crop weather markets).
- A seasonal pattern needs a **cause**. Without one, assume it is data-mined.

---

## 6. Failure modes

1. Drift is mistaken for seasonality.
2. Twelve months are compared and the best one is picked afterwards (a multiple-testing problem).
3. The sample is too small: about 25 years gives about 25 observations per month.
4. The pattern changes over time (compare subperiods).
5. Indices built from centred averages look ahead.
6. Missing data is not random (see the 2001 gaps in the NIFTY data).
7. Costs, carry and dividends are ignored.

---

## Chapter 10 completion test

- Why must the trend be removed before measuring seasonality?
- What does a seasonal index of 97 mean?
- Why is the moving average centred, and why 2×12?
- Why can't a centred-MA index be used as a live signal?
- Why is "the best month" not a valid hypothesis after you have seen the data?
- What did the NIFTY omnibus test conclude, and why doesn't that prove there is no seasonality?
