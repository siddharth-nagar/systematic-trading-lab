# Kaufman Chapter 9 — Momentum and Oscillators

## Status

**Chapter complete.**

This note captures the concepts to retain before moving on. It is not intended to reproduce every variation in the chapter.

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
