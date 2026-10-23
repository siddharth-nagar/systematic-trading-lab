# Kaufman Chapter 9 — Momentum and Oscillators

## Status

**Chapter complete.** Checked against the printed text, pp. 369–426 (2026-10-20): formulas below are correct; book details added where marked *(book)*, and section 11 covers material the original notes left out.

This note captures the concepts to retain before moving on. It is not intended to reproduce every variation in the chapter.

### Chapter map (Kaufman's own headings)

| Section | Pages |
|---|---|
| Momentum (as percentage, vs trend, as trend indicator, timing, fading extremes, risk, high-momentum trading, MACD) | 369–384 |
| Divergence index | 384–385 |
| Oscillators (RSI and variations, 2-day RSI, RSI of MACD, stochastics, Williams' oscillators, RVI) | 385–403 |
| Double-smoothed momentum (TSI, double-smoothed stochastic, TRIX, strength oscillator, volume) | 404–411 |
| Velocity and acceleration | 412–416 |
| Hybrid momentum techniques (directional parabolic, ADX filter, oscillator timing, Cambridge Hook) | 416–418 |
| Momentum divergence (rules, anticipation, multiple divergences, programming, slope divergence) | 418–426 |

---

## 1. Momentum

Basic n-period momentum:

[
M_t(n)=P_t-P_{t-n}
]

Percentage momentum:

[
M_t(n)=\frac{P_t}{P_{t-n}}-1
]

*(book)* Momentum = speed: a 100-point move in 5 days is a 5-day momentum of 100 but a speed of 20/day — always state the period. Percentages don't work on back-adjusted futures; use price differences there.

*(book)* **Momentum is not volatility:** $1200 → $1250 → $1200 in five days is zero momentum but high volatility.

Interpretation:

- (M>0): price is above its value n periods ago.
- (M<0): price is below its value n periods ago.
- Momentum measures **change**, not price level.

### Core lesson

Price can still be rising while momentum is falling. That means the trend is still positive, but its speed is weakening.

---

## 2. Speed versus noise

Shorter lookback:

[
n \downarrow \Rightarrow \text{faster response} + \text{more noise}
]

Longer lookback:

[
n \uparrow \Rightarrow \text{more smoothing} + \text{more lag}
]

This trade-off appears throughout the chapter.

---

## 3. RSI

Relative Strength:

[
RS=\frac{AU}{AD}
]

Relative Strength Index:

[
RSI=100-\frac{100}{1+RS}
]

Important distinction:

- RSI(14): slower, broader overbought/oversold measure.
- RSI(2): very fast, short-term mean-reversion style signal.

*(book)* Details:
- Wilder used **14 days = half of a monthly cycle**, thresholds **70 / 30**. AU and AD are updated by the "average-off" method: (AU_t = AU_{t-1} - AU_{t-1}/n + \max(P_t-P_{t-1},0)).
- Aan's study: average RSI(14) tops ≈ **72**, bottoms ≈ **32** → 50% of values lie between them, so 70/30 is too narrow. Kaufman suggests thresholds at ~**1.5 standard deviations**.
- If signals stay outside 70/30 too long, the period is too short; for more signals, shorten to 10 and widen to 80/20.
- Two different "2" RSIs: **Stokes's 2-day RSI** replaces each 1-day change with a 2-day change (thresholds 10/90, exit after one day; on the S&P it worked as a *trend* signal 1970–1998 and as *mean reversion* after 1998). The **standard 2-period RSI** uses 1-day changes over 2 periods.
- Stokes's scaling-in: buy 25/50/75/100% as RSI falls below 20/15/10/5 (mirror for shorts).

### Failure mode

An overbought market can become more overbought during a strong trend. Therefore:

[
\text{Extreme} \neq \text{Immediate reversal}
]

---

## 4. Stochastic

Raw %K:

[
\%K=100\frac{C-L_n}{H_n-L_n}
]

It answers:

> Where is the current close inside the recent high-low range?

*(book)* Lane's three lines, here over 5 days:
- %K (raw) as above — includes today's high and low, so it hits 0 or 100 when today is the extreme.
- **%D = "%K-slow"** = 3-day average of raw %K.
- **%D-slow** = 3-day average of %D.
- In practice "%K" and "%D" usually mean %K-slow and %D-slow; raw %K is rarely used (unstable).
- Traded like MACD (%D crossing %D-slow), with 80/20 thresholds, or as timing within a trend (e.g. 60-day MA trend + 20-day stochastic crossing down from above 80 to sell).
- Lane's patterns: left/right crossings, hinge, warning, extremes, bear set-up, %K-slow failure.

Momentum and Stochastic are related but not identical:

- Momentum measures **change**.
- Stochastic measures **location within a range**.

---

## 5. MACD

[
MACD=EMA_{fast}-EMA_{slow}
]

Signal line:

[
Signal=EMA(MACD)
]

Histogram:

[
Histogram=MACD-Signal
]

Interpretation:

- MACD is the difference between two smoothed trends.
- The signal line is smoothed momentum.
- The histogram measures MACD relative to its own smoothing.

*(book)* Appel's standard is **12/26 with a 9-day signal**; Kaufman's worked example uses 20/40/9 (smoothing constants 0.0476, 0.0243, 0.10 from s = 2/(n+1)). Main use: buy when MACD crosses above the signal line. To cut whipsaws, only take buys after MACD has been below a lower threshold and sells after above an upper one — but thresholds fitted to history are unreliable. Appel preferred 19/39 for the NASDAQ.

---

## 6. Trend-following versus countertrend use

The same momentum reading can support opposite hypotheses.

### Persistence hypothesis

[
\text{Strong momentum} \Rightarrow \text{continuation}
]

### Mean-reversion hypothesis

[
\text{Extreme momentum} \Rightarrow \text{reversal}
]

The indicator does not choose the hypothesis.

[
\boxed{\text{Indicator} \neq \text{Strategy}}
]

---

## 7. Regime + trigger

One of the strongest architectures in the chapter is:

[
\boxed{\text{Long-term direction} + \text{Short-term timing}}
]

Example:

1. Use a moving average to define trend.
2. Use a short stochastic or RSI to identify a pullback.
3. Take trades only in the direction permitted by the longer-term trend.

This separates **direction** from **entry timing**.

*(book, p. 418)* Kaufman's example: 40-day MA for trend, 5-day stochastic for timing — buy when the trend is up and stochastic < 20, sell when the trend is down and stochastic > 80. Exit immediately when the trend changes; add a rule that forces entry after n days so a trade is not missed. *(p. 380)* "The trend provides protection": if the pullback keeps going, the trend reverses and you exit, so no separate stop is needed.

---

## 8. Velocity and acceleration

Velocity:

[
v_t=P_t-P_{t-1}
]

Acceleration:

[
a_t=v_t-v_{t-1}
]

or:

[
a_t=P_t-2P_{t-1}+P_{t-2}
]

Possible states:

- (v>0, a>0): rising and accelerating.
- (v>0, a<0): rising but slowing.
- (v<0, a<0): falling and accelerating downward.
- (v<0, a>0): falling but slowing.

Higher derivatives may turn earlier, but they are usually noisier.

*(book)* **Sideways market = velocity and acceleration both near zero** — velocity alone can be zero while prices are still moving fast. Straight lines, simple/weighted MAs and exponential smoothing have constant velocity and zero acceleration (Table 9.4); only second-order (curved) fits give a usable acceleration.

---

## 9. Divergence

Bearish divergence:

[
Price \uparrow,\quad Momentum \downarrow
]

Bullish divergence:

[
Price \downarrow,\quad Momentum \uparrow
]

Divergence is best treated as a **setup**, not automatically as an entry.

A useful architecture is:

[
\boxed{\text{Setup} \rightarrow \text{Confirmation} \rightarrow \text{Trade}}
]

*(book)* Kaufman's divergence rules:
- Prices and momentum must move in **opposite** directions; the sharper the divergence, the sooner the reversal; longer divergences forecast bigger reversals.
- Best when momentum starts from an **extreme** and the signal comes while momentum is still far from neutral (50 or 0).
- MACD divergence: sell when MACD crosses below its signal after the second (lower) peak; exit at MACD = 0 or when MACD crosses back up.
- Exit if momentum makes a new high above the last peak — the divergence no longer exists.
- Divergence is usually seen too late; **anticipate** it when price breaks resistance while momentum is below its last peak, or scale in by thirds (new price high with lower MACD; MACD within 15–20% of its prior high; MACD crosses its signal).
- Double/triple divergences are more reliable; with alternating peaks (90, 60, 75) analysts use the 90–75 pair.
- **Slope divergence:** compare regression slopes of price and momentum over the same window — catches rounded tops that have no clear swing peaks.

---

## 10. Model-building lessons

1. More indicators do not necessarily mean more independent information.
2. RSI, Stochastic, Williams %R, MACD, TSI and TRIX are transformations of overlapping price information.
3. Smoothing lowers noise but adds lag.
4. Normalisation changes the meaning of an indicator.
5. Long and short effects should be tested separately.
6. Historical edges can decay across market regimes.
7. Parameter optimisation should wait until the research/validation framework is ready.
8. A chart pattern must become precise numerical rules before it can be systematic.

---

## 11. Additions from the book

**Using momentum (pp. 374–381)**
- Momentum crossing zero = the n-day MA turning (Ch. 8). Price minus its MA is also called "relative strength".
- Choosing a momentum period: ½ or ¼ of the natural peak-to-peak cycle.
- Fading extremes — entries: aggressive (penetrate the band), minor confirmation (first turn after penetrating), major confirmation (re-cross the band), timing (n days outside). Exits: opposite signal, partway to zero, **zero line (benchmark — mean reversion to the mean)**, or after crossing zero.
- **Scale problem:** momentum bands that fit 2006 (±30 on the S&P 20-day) were overrun in 2007 and 2008 (−150). Bands must adapt to volatility.
- A test that accidentally *bought* high momentum with a close stop was profitable; the intended aggressive fade was a losing strategy. *Declining momentum does not mean prices are falling.*
- High-momentum trading (buy strength, exit as volume fades) is a fast, full-time game.

**Divergence index (p. 384):** (DI = (\text{fast MA}-\text{slow MA}) / \text{StDev}(P_t-P_{t-1},\text{slow})^2); bands = ±1 × StDev(DI). Buy below the lower band in an uptrend; sell above the upper band in a downtrend; exit at zero.

**Oscillators (pp. 385–403)**
- Oscillator = momentum normalised to a fixed range (0–100, ±1) so it self-adjusts to price level.
- RSI countertrend: trade a fast change (RSI_t − RSI_{t-k} > a). Net momentum oscillator (Chande CMO) = 100 × (S_up − S_down)/(S_up + S_down).
- RSI of the MACD spread (5-day RSI of a 10/40-week MA difference, 30/70). StochRSI = (RSI − min RSI)/(max RSI − min RSI).
- **Williams' A/D oscillator:** DRF = (BP + SP)/(2(H − L)), BP = H − O, SP = C − L; gap days distort it — link to the prior close as in true range.
- **%R** = (highest high − close)/range over 10 days — upside down (0 = strongest). Used to add positions within a major trend.
- **Ultimate Oscillator:** buying pressure C − true low over true range, summed over 7, 14, 28 days, weighted 4:2:1. Sell on a failed second peak above 50; stop at 65.
- **Ehlers' RVI** = (C − O)/(H − L) with 4-bar symmetric weights, period ~10; signal line like MACD.

**Double smoothing (pp. 404–411)**
- **TSI (Blau):** (100 \times \text{EMA}_s(\text{EMA}_r(\Delta P)) / \text{EMA}_s(\text{EMA}_r(|\Delta P|))). Speed up with differences, slow down with smoothing → smooth with little lag. n-day differences smooth further (10-20-20 TSI).
- Anticipate the turn: act at "near-zero slope" of a very smooth line.
- Double-smoothed stochastic; TRIX (difference taken at the end → smoother than TSI).
- Strength oscillator = avg(C_t − C_{t−1}) / avg(H − L) — trend strength vs noise.
- Volume: momentum × average volume; volume-weighted RSI (money flow); Herrick Payoff Index (volume and open interest). Smooth volume first — it is erratic.

**Hybrid techniques (pp. 416–418)**
- Directional Parabolic (ADX direction + Parabolic stop).
- Kestner: 10/50 MA oscillator, trade it only when ADX(14) < 30 (no trend).
- Cambridge Hook: outside reversal + RSI > 60 + rising volume and open interest → reversal.

**Final comments (p. 426):** fast momentum is unstable; trading against price direction is high risk. Momentum works best as **timing inside a trend strategy** — e.g. a 3-day oscillator that gives 1–2 oversold signals in each 2-day entry window.

---

## Chapter 9 completion test

Before moving on, be able to answer from memory:

- What does momentum measure?
- Why can momentum peak before price?
- What is the difference between RSI and Stochastic?
- What exactly is MACD?
- Why can oscillator extremes fail in trends?
- Why is trend + oscillator a coherent architecture?
- What is bearish versus bullish divergence?
- Why are faster indicators usually noisier?
