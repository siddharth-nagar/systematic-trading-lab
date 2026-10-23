# Kaufman Chapter 11 — Cycle Analysis

## Status

**Lab complete.** The notes and lab are written. Answer the completion test from memory before moving to Chapter 12.

Lab: [`labs/ch11_lab.ipynb`](../labs/ch11_lab.ipynb). Code: [`lib/indicators.py`](../lib/indicators.py), [`lib/cycles.py`](../lib/cycles.py). Copper data and provenance: [`data/`](../data/DATA_PROVENANCE.md).

---

## 1. Price components

[
\text{Price} = \text{Trend} + \text{Seasonal} + \text{Cycle} + \text{Noise}
]

To see the cycle, remove the trend (and the seasonal component, unless it is the cycle you want). Seasonality is the most regular cycle, because it has a physical cause.

Before trusting a cycle:
- know **why** it should exist (cattle breeding, inventory, elections);
- see **at least 8 repetitions**;
- expect the period to drift. The Swiss franc cycle moved from 24–35 weeks to 30–52 weeks.

---

## 2. Describing a cycle

[
y = a\sin(\omega\phi + b)
]

- amplitude (a), period (T), frequency (\omega = 1/T) (or (360°/T) per bar), phase (b);
- a compound wave is a sum of waves: (y = a_1\sin(\omega_1\phi+b_1) + a_2\sin(\omega_2\phi+b_2));
- the peaks of the components rarely line up, so the compound wave never reaches (a_1 + a_2).

---

## 3. Removing the trend

| Method | Formula |
|---|---|
| MA residual | (P_t - MA_n(P)_t) |
| n-bar difference | (P_t - P_{t-n}), which also deletes cycles of length (n) |
| Two-EMA MACD | long EMA = ½ dominant cycle, short = ½ long |
| Least-squares line | (P_t - (a + bt)) |
| Triangular MACD | (TMA_P - TMA_{P/2}) |

An oscillator meant to show a cycle of length (T) needs a period of at most (T/2).

### Triangular weights

Weights step up by (2/(P/2)) to 2.0 at the centre and back down. For (P = 10): 0.4, 0.8, …, 2.0, …, 0.4 (9 values, summing to 10).

[
TMA_t = \frac{w_1P_{t-P+2} + w_2P_{t-P+3} + \dots + w_{P-1}P_t}{P}
]

The book prints `×` between the terms by mistake.

---

## 4. Single-frequency trigonometric regression

1. Detrend with a least-squares line.
2. (\alpha = \Sigma cd / \Sigma c^2), with (c = y_n), (d = y_{n-1} + y_{n+1}).
3. (\cos\omega = \alpha/2), so (T = 360°/\omega).
4. Fit (y_t = a\cos\omega t + b\sin\omega t) by least squares.

Why it works: (\sin\omega(t-1) + \sin\omega(t+1) = 2\cos\omega\,\sin\omega t).

**Replication result:** the trend line reproduces (28.92 + 0.265x on the first 67 quarters vs the book's 28.89 + 0.267x), but α does not. The data give a period of about 10 quarters, against the book's 8.4. The fitted cycle explains only about 10% of the detrended variance.

---

## 5. Fourier analysis and the periodogram

- Fourier analysis writes a series as a sum of sine and cosine waves. Spectral power is proportional to amplitude squared.
- It assumes **stationarity**, so detrend first. A trend appears as a huge "cycle" as long as the data.
- Resolution: FFT bins sit at periods (N/k). Periods are only measured to within a bin.
- Lag windows (Tukey, Parzen) smooth the estimate because long-lag autocorrelations are unreliable.

**Book error (pp. 511–513):** Excel FFT rows 1–12 are labelled Jan–Dec. Row (k) is a cycle of (N/k) bars, not month (k). Seasonality appears only near the 12-month period.

---

## 6. Smoothing creates cycles (Slutsky–Yule)

A band-pass filter (any MA difference) applied to a random walk produces a regular-looking cycle in the filter's pass band. In the lab, a triangular MACD 40-20 on a random walk shows "cycles" about 23–39 bars apart.

[
\boxed{\text{A cycle seen through a filter may belong to the filter}}
]

Defence: pre-declare a test, for example the largest periodogram value against shuffled returns.

**NIFTY result:** monthly log returns 2002-02 to 2025-12, periods 3–60 months, 5,000 shuffles. Largest peak at 4.8 months, p ≈ 0.80. No evidence of a cycle.

---

## 7. Ehlers: MESA and the Hilbert transform

- MESA finds cycles from short samples. Ehlers uses it to **classify the market**: *if a short-term cycle exists, the market is not trending.*
- Hilbert transform: (I = P_{t-3}), (Q = 0.0962P_t + 0.5769P_{t-2} - 0.5769P_{t-4} - 0.0962P_{t-6}).
- The phase angle forms a sawtooth while the cycle holds, and breaks down when it ends.
- Missing from the book: Q needs a gain correction of (0.075\cdot\text{Period} + 0.54). The angle direction depends on the convention (the book measures it clockwise).
- A filtered random walk can also produce a clean sawtooth for a while.

---

## 8. Fisher and inverse Fisher transforms

- A sine wave spends most of its time near its extremes, so its distribution is U-shaped.
- Fisher: (X_t = 0.5\cdot2\cdot(\text{channel position} - 0.5) + 0.5X_{t-1}), then (y = 0.5\ln\frac{1+X}{1-X}). This gives sharper turning points. The trigger is the previous value.
- Inverse Fisher on RSI: (x_2 = WMA(0.1(RSI - 50))), output (100\cdot\frac{e^{2x_2}-1}{e^{2x_2}+1}). The values cluster near ±100.

---

## 9. Commodity Channel Index (Lambert)

[
CCI_t = \frac{x_t - \bar x_t}{0.015\,MD_t}, \qquad x_t = \frac{H_t+L_t+C_t}{3}
]

- (N) should be less than ¼ of the cycle; values above +100 or below −100 mark a cyclic turn.
- The book prints (\bar x_t) as a sum. It must be the **average**.

---

## 10. Hurst's phasing

- Plot the full-span and half-span MAs half their length back in time, so they sit on the price swings.
- Fit a trend through their crossings, project the half-span average, and measure the distance (D) above the trend to set a symmetric price target below it.
- **Look-ahead:** the phased MA has no value for the last (F/2) bars. A backtest must use only the projection that was available at the time.

---

## 11. Not implemented

- Full MESA (Burg's algorithm).
- The Short Cycle Indicator (Lorca-Susino): the formula on p. 522 uses a term (C) that is never defined.

---

## Failure modes

1. The trend is mistaken for a long cycle.
2. Differencing or smoothing creates or deletes cycles.
3. Too few repetitions, or the period drifts.
4. Picking the tallest periodogram peak without a null test.
5. Centred or phased averages look ahead.
6. Cycle indicators often duplicate momentum (Chapter 9).
7. Published numbers may not reproduce (the copper α).

---

## Chapter 11 completion test

- What are amplitude, period, frequency and phase?
- Name three ways to remove a trend, and say what each one does to cycles.
- How does the single-frequency method get the period from (\alpha)?
- What does an FFT output row mean? Why is the Jan–Dec label wrong?
- Explain the Slutsky–Yule effect in one sentence.
- What null hypothesis was used for NIFTY, and what are its limits?
- What does a broken Hilbert phase sawtooth mean to Ehlers?
- Why can't Hurst's phased averages be used directly in a backtest?
