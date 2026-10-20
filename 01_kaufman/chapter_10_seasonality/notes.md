# Kaufman Chapter 10 — Seasonality

## Status

**Chapter covered (Level 2 — Replicate).**

> **Verification:** these notes were rebuilt from the study sessions, not yet checked line by line against the printed Chapter 10 text (Chapter 11 has been). Check formulas and page references when the Chapter 10 PDF is available.

The replication for this chapter lives in [`02_nifty_seasonality/`](../../02_nifty_seasonality/) as a provisional research baseline. Deep validation (Level 3) is deliberately deferred until the book is finished.

This note captures the concepts to retain. It is not intended to reproduce every variation in the chapter.

---

## 1. What seasonality is

A seasonal effect is behaviour associated with a **recurring calendar period** (month, quarter, week, day of month).

Decomposition used throughout Chapters 10–11:

[
P_t = T_t + S_t + C_t + \epsilon_t
]

- (T_t): trend
- (S_t): seasonal component (calendar-locked)
- (C_t): cycle (recurring, not calendar-locked — Chapter 11)
- (\epsilon_t): noise

---

## 2. The monthly return matrix

Monthly return:

[
r_{y,m} = 100\left(\frac{C_{y,m}}{C_{\text{prior month}}}-1\right)
]

Arrange returns as a **year × month** matrix, then summarise each calendar month:

- mean and **median** (median resists outliers);
- **positive frequency**: (100 \cdot \#(r>0)/n);
- standard deviation;
- best / worst outcome.

### Core lesson

A high positive frequency in an upward-drifting index is **not** seasonality by itself. Compare each month with the **unconditional mean**, not with zero.

---

## 3. Detrending

Equity indices drift upward, so raw seasonal averages mix trend with season.

[
\text{Seasonal excess}_{m} = \bar{r}_m - \bar{r}
]

The detrending method is part of the model specification and must be documented — it changes the answer.

---

## 4. Stability and testing

1. Test **all months together** first (omnibus null), before looking at any individual month.
2. Check **subperiod stability**: does the pattern survive in separate fixed time blocks?
3. Twelve months give twelve chances for one to look extreme by luck — **multiple testing**.
4. A month chosen *after* seeing the data is an exploratory hypothesis, not a confirmed one.

[
\boxed{\text{Calendar mechanism} \neq \text{validated tradable effect}}
]

---

## 5. NIFTY replication result (provisional)

- 302 monthly returns, 2000–2025, secondary-source data.
- Omnibus within-year permutation test (5,000 replicates): **p ≈ 0.575**.
- Conclusion: **no evidence** that NIFTY calendar-month means differ, in this dataset.
- Data still needs reconciliation against official NSE records (six missing months, two conflicting closes).

See [`omnibus_report.md`](../../02_nifty_seasonality/results/omnibus_report.md).

---

## 6. Model-building lessons

1. Report null results as carefully as positive ones.
2. Never fill missing prices silently; keep a provenance log.
3. Predefine hypotheses and holdouts before testing.
4. Seasonal effects can decay or shift across regimes.
5. A descriptive table is not a backtest: costs, execution and carry are missing.

---

## Chapter 10 completion test

- Why is positive frequency misleading in a rising index?
- What does detrending change, and why must it be documented?
- Why test all twelve months together first?
- What is the difference between a seasonal and a cyclical component?
- What would make a seasonal pattern tradable rather than descriptive?
