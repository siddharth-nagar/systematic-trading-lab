# Kaufman Chapter 11 — Cycle Analysis

## Status

**In progress — Parts 1–3 covered (approx. printed pp. 485–513).**

- Part 1: cycle basics and identification
- Part 2: uncovering cycles mathematically (trigonometric regression)
- Part 3: Fourier and spectral analysis, MESA
- Part 4: phasing and using cycles in trading rules — *next*

This note captures the concepts to retain. It is not intended to reproduce every variation in the chapter.

---

## 1. What a cycle is

A cycle is an oscillation with an **approximately recurring period** that is not necessarily tied to the calendar.

| Component | Main characteristic |
|---|---|
| Trend | Persistent directional movement |
| Seasonality | Behaviour tied to recurring calendar periods |
| Cycle | Oscillation with an approximately recurring period |
| Noise | Irregular movement not explained above |

[
P_t = T_t + S_t + C_t + \epsilon_t
]

Three properties:

- **Period** (T): distance between repetitions.
- **Amplitude** (A): size of the oscillation.
- **Phase** (\phi): position within the cycle.

[
C_t = A\sin\left(\frac{2\pi t}{T}+\phi\right)
]

### Core lesson

Visible repetition on a chart is a **starting hypothesis**, not confirmation. Longer cycles can contain shorter ones.

---

## 2. Repetitions matter more than sample length

[
\text{Number of cycles} = \frac{N}{T}
]

A 55-year cycle in 165 years of data gives only 3 repetitions — far too few to time anything.

[
\boxed{\text{Longer period} \Rightarrow \text{fewer repetitions} \Rightarrow \text{weaker validation}}
]

Political/election and long economic cycles (business cycle, Kondratieff) are historical claims that need fresh validation.

---

## 3. Detrending before cycle analysis

[
R_t = P_t - \hat{T}_t
]

Methods from the chapter:

- Difference of two EMAs (MACD-like):
  [
  D_t = EMA_{short}(P_t) - EMA_{long}(P_t)
  ]
- Triangular weighting (weights 1, 2, 3, 2, 1 for 5 observations):
  [
  TMA_t = \frac{P_t+2P_{t-1}+3P_{t-2}+2P_{t-3}+P_{t-4}}{9}
  ]

### Failure mode

Smoothing and subtraction shift **timing and amplitude**. Peaks of a detrended series need not match price turning points.

The detrending method is part of the model specification.

---

## 4. Cycle mathematics

[
y_t = A\sin(\omega t+\phi), \qquad \omega=\frac{2\pi}{T}
]

- A phase difference of (\pi) = half a cycle (opposite peaks and troughs).
- Knowing the period **without the phase** is insufficient for timing a turn.

Compound waves:

[
y_t = \sum_{k=1}^{K} A_k\sin(\omega_k t+\phi_k)
]

Components reinforce and cancel, so observed peaks are unevenly spaced and sized. A large observed peak may be **interference**, not the dominant cycle's peak.

---

## 5. Trigonometric regression

For a fixed candidate frequency, the cycle becomes a **linear** regression:

[
R_t = a\cos(\omega t)+b\sin(\omega t)+\epsilon_t
]

[
A=\sqrt{a^2+b^2}, \qquad \phi = \operatorname{atan2}(a,b)
]

Procedure: for each candidate (T), set (\omega=2\pi/T), fit (a, b) by least squares, compute

[
SSE(T)=\sum_t (R_t-\hat{R}_t)^2
]

and compare. The lowest SSE is the best **in-sample** candidate only.

Adding a second frequency fits more shapes but adds parameters:

[
\boxed{\text{More flexible model} \Rightarrow \text{better fit, greater overfitting risk}}
]

### Failure modes

- Searching many frequencies on noise always finds a "best" one.
- Fitting the trend on the whole sample and then backtesting introduces **look-ahead bias**. Use rolling or expanding estimation windows.

---

## 6. Fourier analysis

The regression above, applied to all frequencies at once:

[
R_t = \sum_{k=0}^{N/2}\left[a_k\cos(\omega_k t)+b_k\sin(\omega_k t)\right], \qquad \omega_k=\frac{2\pi k}{N}
]

- Testable periods are fixed by sample length: (T_k = N/k).
- Longest usable period (\approx N/2); shortest (Nyquist) = 2 observations.
- The FFT is a fast algorithm for computing all (a_k, b_k).

**Periodogram:** power (\propto A_k^2) plotted against period. Doubling amplitude quadruples the spike.

### Three limits on market data

1. **Resolution** — a true period between grid points leaks power into neighbouring bins.
2. **Stationarity** — Fourier assumes fixed period, amplitude and phase; drifting market cycles smear the peak.
3. **Trend and endpoints** — undetrended data piles power into long periods; the sample's wrap-around creates false high-frequency power. Detrend first, taper the edges (e.g. Hann window).

---

## 7. MESA (Maximum Entropy Spectral Analysis)

Fits an autoregressive model and derives the spectrum from its coefficients:

[
R_t = \sum_{j=1}^{p} c_j R_{t-j} + \epsilon_t
]

- Sharper peaks from **short, rolling windows** — can track a changing cycle.
- Not confined to the (N/k) grid.
- Order (p) is a new overfitting risk: too low merges peaks, too high creates false ones.

---

## 8. Real cycle or noise?

| Test | Question |
|---|---|
| Size | Is the peak clearly above simulated-noise spectra? |
| Multiple testing | ~60 bins → ~3 clear 5% by chance |
| Stability | Same peak in the first and second halves? |
| Repetitions | At least ~10 full cycles, (N/T \ge 10)? |
| Tradability | Amplitude larger than costs over half a cycle? |

Market prices contain **red noise** (more power at long periods), so rising long-period power is often just noise.

[
\boxed{\text{Spectral peak} = \text{hypothesis, not edge}}
]

---

## 9. Model-building lessons

1. Detrending, smoothing and window choices are model parameters — document them.
2. Every frequency search is a multiple-testing problem.
3. Stationary-cycle tools struggle with drifting market cycles.
4. Estimation must use only data available at decision time.
5. Period alone does not time a trade; phase does — and phase is the hardest to estimate.

---

## Chapter 11 completion test (Parts 1–3)

- What are period, amplitude and phase?
- Why do long cycles have weak statistical support?
- Why must detrending be documented?
- Why combine sine and cosine in the regression?
- What fixes the set of periods an FFT can test?
- What is spectral leakage, and when does it happen?
- What does MESA gain over the FFT, and what does it risk?
- How would you tell a real cycle from a noise peak?
