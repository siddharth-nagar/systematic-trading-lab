# Kaufman Chapter 11 — Cycle Analysis

## Status

**Chapter complete (Level 2 — Replicate).** Notes checked against the printed text, pp. 485–526.
NIFTY replication: [`03_nifty_cycle_tools/`](../../03_nifty_cycle_tools/).

## Chapter map (Kaufman's own headings)

| Part | Kaufman section | Pages |
|---|---|---|
| 1 | Cycle Basics | 485–494 |
| 2 | Uncovering the Cycle (detrending, trigonometric regression) | 494–505 |
| 3 | Fourier Analysis (spectral analysis) | 505–513 |
| 4 | Maximum Entropy (MESA, phase angle, Hilbert, Fisher) | 514–520 |
| 5 | Cycle Channel Index, Short Cycle Indicator, Phasing | 520–526 |

Items marked *(extra)* are good research practice but are not from Kaufman.

---

## Part 1 — Cycle Basics (pp. 485–494)

Trend, seasonality and cycle are the three orderly components of price; noise is the rest.

[
P_t = T_t + S_t + C_t + \epsilon_t
]

- To find one component, remove the others: first differences remove trend; subtracting a 1-year average removes seasonality.
- Cycles combine as **harmonics**: a smaller cycle is often ½, ⅓, ¼ … of a larger one. Synchronised cycles peak together.
- Observe a cycle *and know why it exists* before trusting it (cattle: production/feeding schedule; Swiss franc: no clear fundamental cause, period drifted from 24–35 to 30–52 weeks).
- Ehrlich Cycle Finder: need **at least 8 repetitions** before concluding a cycle is valid.
- Business cycle ~8.6 years (Princeton Economic Institute); Kondratieff wave ~54 years — only ~3 completed cycles, so timing is impractical (a 10% period error = 5 years).
- Presidential election cycle: pre-election year strongest historically; treat as a claim needing fresh validation.

[
\boxed{\text{Longer period} \Rightarrow \text{fewer repetitions} \Rightarrow \text{weaker validation}}
]

---

## Part 2 — Uncovering the Cycle (pp. 494–505)

**Simple detrending:** subtract a moving average of the cycle length, or take (P_t - P_{t-n}). Oscillators reveal an n-day cycle only if their period is ≤ n/2.

**Two-EMA method (p. 495):** longer EMA = **half the dominant cycle**, shorter EMA = **half the longer one**; their difference is a synthetic, less-lagged detrended series.

**Triangular weighting (p. 495):** centre weight 2.0, weights fall linearly to the ends (P = 10 → 0.4, 0.8, 1.2, 1.6, 2.0, 1.6, 1.2, 0.8, 0.4; oldest price dropped to keep an odd count). **Triangular MACD** = difference of a full and a half-period triangular average (20-10 on IBM, 252-126 on corn). Smooth, but behaves like momentum: uneven peaks and amplitudes.

**Terminology (p. 496):** amplitude a, period T, frequency (Kaufman) = 360/T degrees per day, phase = starting offset, phase angle = clock minute hand with **0° at three o'clock**.

[
y = a\sin(\omega\phi + b), \qquad y = a_1\sin(\omega_1\phi+b_1) + a_2\sin(\omega_2\phi+b_2)
]

Turning points of a compound wave: first derivative = 0; second derivative sign tells max (<0) or min (>0).

**Single-frequency regression (copper, pp. 499–502):**
1. Detrend with least squares: (y = 28.89 + 0.267x).
2. Fit (y_t = a\cos\omega t + b\sin\omega t).
3. Kaufman finds ω directly by solving (\cos\omega - \tfrac{1}{2}\alpha = 0) with (\alpha\sum c^2 = \sum cd), (c = y_n), (d = y_{n-1}+y_{n+1}) → α = 1.464, **ω = 42.9°, T = 8.4 quarters**.
4. Solve the normal equations for a, b → (a=-0.603, b=1.831). Matches 7 of 8 copper peaks — "not much more than the Ehrlich Cycle Finder".

*(extra)* Equivalent intuition: for a fixed ω the fit is linear; amplitude (A=\sqrt{a^2+b^2}). A period-by-period SSE search is a teaching device, not Kaufman's method.

**Two-frequency regression (pp. 502–505):** ω₁, ω₂ from a quadratic in (x=\cos\omega); copper → 10.6 and 2.6 quarters. More flexible → better in-sample fit, more overfitting risk.

---

## Part 3 — Fourier Analysis (pp. 505–513)

- Fourier = complex trigonometric regression: any series as a sum of sines and cosines.
- **Only reliable on stationary data** — agricultural products more suitable than stocks that change structure; may need to remove inflation or FX.
- Coefficients (p. 506): (u_k, v_k) for k = 1 … N/2.
- **Phase** between cycles: 180° = out of phase; 0° = coincident.
- **Periodogram → spectral density**: peak height ≈ amplitude²; noise of the same size as the cycle would obscure it.
- **Remove the trend** (first differences or linear regression) or it shows up as the dominant cycle. Seasonal component need not be removed.
- Longer cycles have **wider peaks** — wider does not mean more important.
- Need at least one full cycle of data (12 months for seasonality); more is better.

**Weighting factors (p. 509):**

[
\hat y(\omega)=\frac{1}{\pi}\left(\lambda_0c_0+2\sum_{k=1}^{M}\lambda_k c_k\cos\omega k\right),\quad c_k=\sum\frac{(y_t-\bar y)(y_{t-k}-\bar y)}{N}
]

Truncation point M < N; lag window λ_k: Tukey (\tfrac12(1+\cos\tfrac{\pi k}{M})) or Parzen.

**FFT practice (pp. 510–513):** detrend, taper the endpoints with a bell-shaped window, pre-filter with a moving average (an n-day MA removes cycles shorter than **2n** days). 40-day cycle = 9° per day. Excel: power-of-2 sample ≤ 4,096, use returns if prices trended, IMABS for magnitude.

*(extra)* Testable periods are N/k; off-grid cycles leak into neighbouring bins; market spectra rise towards long periods (red noise).

---

## Part 4 — Maximum Entropy (pp. 514–520)

- **MESA** (Ehlers): finds cycles in small windows where FFT needs ≥ 256 points and ~16 cycles. Useful cycles exist ~20% of the time.
- **Phase angle:** a pure cycle gives a rising **sawtooth**; erratic phase = cycle breaking down.
- **Ehlers' lateral shift:** *if a short-term cycle exists, the market is not trending.* Use cycles to classify trend vs sideways, not to trade the cycle.
- **Hilbert transform (p. 516):**
  [
  Q = 0.0962P_t + 0.5769P_{t-2} - 0.5769P_{t-4} - 0.0962P_{t-6},\quad I = P_{t-3},\quad \theta=\arctan(Q/I)
  ]
  Peak ≈ 270°, trough ≈ 90°. Needs ~4 bars. Sharp peaks suit mean reversion; behaves like momentum (big peaks after quiet periods).
- **Fisher transform (pp. 518–519):**
  [
  X_t = 0.5\cdot2\left(\frac{P_t-\text{MinL}}{\text{MaxH}-\text{MinL}}-0.5\right)+0.5X_{t-1},\qquad y = 0.5\ln\frac{1+x}{1-x}
  ]
  U-shaped channel position → bell shape. Trigger = previous value; best signals just after an extreme. Output is unbounded (book says ±1 — that is the input); clip x below ±1.
- **Inverse Fisher (p. 520):** (x = (e^{2y}-1)/(e^{2y}+1)) on RSI(20) of 10-bar momentum, rescaled 0.1·(RSI−50), 30-bar WMA.

---

## Part 5 — CCI, Short Cycle Indicator, Phasing (pp. 520–526)

**Commodity Channel Index (Lambert):**

[
\text{CCI}_t=\frac{x_t-\bar x_t}{0.015\times MD_t},\qquad x_t=\frac{H_t+L_t+C_t}{3}
]

N < ¼ of the cycle; use a **simple** MA (fixed window fits a cycle; EMA keeps old data). 0.015 is meant to put 70–80% of values inside ±100. **Rule: above +100 = cyclic turn UP; below −100 = turn DOWN** — Lambert goes *with* the move, the opposite of the popular "overbought" reading.

**Short Cycle Indicator (Lorca-Susino):** intraday bars, multiple time frames. Fast EMA 8, slow EMA 20, LH = lowest high, HL = highest low over 20 bars.

[
\text{Lorca1}=\frac{(XS-LH)^2+(XS-HL)^2}{XS}\times\frac{XF-XS}{XF}\times SF_1
]

= (distance of the slow trend from the channel — a volatility term) × (normalised fast–slow EMA gap — a MACD term). Sell signals need a volatility-expansion pattern (three conditions with 12/14/16/32-bar lookbacks). Many fixed constants → high overfitting risk.

**Hurst phasing:**
- Full span F ≈ average distance between tops; half span H = F/2.
- An F-day MA describes price **F/2 days ago**. *Phasing* plots each MA half its length back so it overlays price.
- Crossings of the phased MAs → regression line = projected trend (Y_T = a + bX_T).
- Project the half-span from its last extreme A (Y_C = c + dX_C); solve for the next crossing X.
- D = furthest price went beyond the trend since the last crossing; **objective = crossing ∓ D**.
- Rules: long when the half-span MA turns up; short when it turns down; close if the objective is reached (allow 10% of cycle height).
- **The last F/2 days of a centred MA do not exist yet** — they must be projected. Using the centred line as if known is look-ahead.

---

## Tested on NIFTY (daily 2002–2026, causal, next-open fills, costs)

| Tool | Result |
|---|---|
| MESA | 27% of days the "dominant cycle" = search limit (red noise); price hit rate 49% vs 56.5% "always up" |
| Phase angle | Regular 38% of the time, but episodes last ~6 days |
| Lateral shift | Did not predict choppier next 20 days; regime switching lowered Sharpe 0.66 → 0.27 |
| Hilbert | Next-10-day return after buy signals = any random day (0.55% vs 0.56%) |
| Fisher | Distribution works; trigger trading = 174 trades/yr, edge lost overnight |
| Inverse Fisher | Trend filter (Sharpe 0.85) — beaten by a 50-day MA (1.09) |
| CCI | Only 54% inside ±100 (book: 70–80%); signals = random days; no rule beat buy & hold |
| Hurst (honest) | Long-only Sharpe 0.92 — a 20-day MA slope trend filter; turns arrive ~7 days after the centred turn |
| **Look-ahead** | Full-sample FFT Hilbert: Sharpe 3.25; centred-MA Hurst: Sharpe 2.88 |

**Lessons that matter for the model**

1. Detrending, smoothing and window choices are model parameters — document them.
2. Every frequency search is a multiple-testing problem; test forecasts against **price**, not the filter.
3. Stationary-cycle tools struggle with drifting, short-lived market cycles.
4. **Centred or full-sample filters create spectacular, fake backtests.** Use only data available at the decision time.
5. On NIFTY the tools that survived were trend/momentum filters, not cycle timers.

---

## Chapter 11 completion test

- Why do long cycles have weak statistical support?
- What does Kaufman's two-EMA rule say about EMA lengths?
- How does Kaufman find ω for copper, and what period did he get?
- Why must data be stationary for Fourier analysis?
- What do the Tukey and Parzen lag windows do?
- What is Ehlers' lateral shift?
- Why does a Fisher transform make extremes meaningful — and why doesn't that create an edge?
- Does a CCI above +100 mean buy or sell in Lambert's rules?
- Why is a centred moving average look-ahead in a backtest?
