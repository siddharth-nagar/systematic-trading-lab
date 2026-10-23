# Kaufman Chapter 8 — Trend Systems

## Status

**Chapter complete (Level 2 — Replicate).** Notes checked against the printed text, pp. 309–368.
Lab: [`ch08_lab.ipynb`](ch08_lab.ipynb) — Kaufman's main tests repeated on NIFTY daily data.

## Chapter map (Kaufman's own headings)

| Section | Pages |
|---|---|
| Why trend systems work (fat tail, market maturity) | 309–313 |
| Basic buy and sell signals | 314–320 |
| Bands and channels (Keltner, percentage, volatility, Bollinger) | 320–330 |
| Applications of a single trend (momentum, MPTDI, volatility system, Keltner 10-day, TRIX, Raschke) | 330–336 |
| Comparison of major trend systems | 336–349 |
| Techniques using two trendlines (Donchian, Golden Cross, ROC, crowd) | 350–356 |
| Multiple trends and common sense; comprehensive studies | 356–359 |
| Selecting the right trend method and speed | 359–363 |
| Moving average sequences (signal progression) | 363–366 |
| Early exits; moving average projected crossovers | 366–368 |

---

## 1. Why trend systems work (pp. 309–313)

Trend systems work because:

1. **Long-term trends come from fundamentals** — mostly government interest-rate policy, which is slow and persistent.
2. **Prices have a fat tail** — more long runs than a random series would produce.
3. **Money moves markets** — fund flows extend trends once the public notices them.

**Runs in 100 coin tosses:** ~50 single, ~25 runs of 2, ~12.5 of 3, ~6 of 4, ~3 of 5, 1–2 of 6. Real prices have **fewer short runs and more long ones** (Figure 8.1). That is enough to make trend trading profitable.

**Distribution of trade profits** (40-day MA, five markets): many small losses, a long tail of large profits. One S&P profit in the $18,750 bin offset more than 30 losses (Figure 8.2, Table 8.1).

[
\boxed{\text{A pure trend strategy needs the fat tail to be profitable}}
]

- *"Trend trading works when the market is trending. It doesn't work in markets that are not trending."*
- Most trend methods have **similar returns over time but different risk profiles and trading frequency**.
- A trend is relative to the trader's horizon and tolerance for noise. *A trend exists if you can profit from it with a trending strategy.*

**Time intervals and market maturity (p. 313):**
- Trends are clearer on weekly than daily, and daily than hourly, charts.
- Interest rates trend longest (policy-driven); FX shorter; individual stocks noisiest (earnings, index arbitrage).
- New, thinly traded markets trend clearly; as the public arrives, noise rises and longer periods are needed.
- **Longer periods, lower-frequency data and fundamentally linked markets perform better.**

---

## 2. Basic buy and sell signals (pp. 314–320)

**Two ways to get a signal from a moving average:**

| Price penetration | Trendline direction |
|---|---|
| Buy when price (closes) above the MA | Buy when the MA turns up |
| Sell short when price (closes) below | Sell short when the MA turns down |
| Faster, more trades | Fewer, later, more stable signals |

**Amazon, 10 years (Table 8.2):** the trendline method had **26–37% fewer trades** and mostly better results for slower periods. For the 5-day MA the price penetration lost less — for fast trading the trendline's lag may be too costly.

**Profit factor** = gross profits ÷ gross losses (TradeStation's ratio). Information or Sharpe ratio is better.

### Execution timing (pp. 316–317)

- Signals computed on the close imply a fill on the close. Waiting for the next open means **you are not trading the system you tested**.
- Practical fix: calculate shortly before the close and execute on the close.
- **Anticipating the signal:** an n-day MA rises tomorrow if today's price > the price dropped off n days ago. Example: oldest price 30.25 → buy stop at 30.26.

**Table 8.3 (Eurodollar vs S&P, entries on today's close / next open / next close):**
- Eurodollars (trending, low noise): **today's close best**; delays hurt.
- S&P (noisy): **delaying to the next open or next close was often better** (except 5 days).

### Profile of a trend system (pp. 317–320)

NASDAQ 100, 40-day MA trendline, 10 years (Table 8.4): 150 trades, **34.7% winners**, win/loss ratio 2.22, winners held **31.65 bars** vs losers **6.64**, 10 consecutive losses vs 6 wins.

Typical profile:
- Low percentage of profitable trades (often < 30%).
- Average win must be much larger than average loss (at 30% winners, ratio > 100:30).
- Winners held much longer than losers.
- Long losing streaks.

This is **conservation of capital**: cut losses quickly, let profits run. Profit targets or tight stops reduce the chance of catching the fat tail.

---

## 3. Bands and channels (pp. 320–330)

Purpose: fewer false signals at the trend change, where indecision is greatest, without changing the overall profile.

**High–low bands (Table 8.5):** MA of highs and MA of lows; buy when the high crosses the MA of highs. Worse for Eurodollars (trending — enter early), **better for the S&P** (noisy — wait).

**Keltner channel (p. 321):** typical price (H+L+C)/3, 10-day average, band from the average daily range. *The formulas as printed show "MA + AP" for both bands — a printing error. Kaufman's description on p. 333 is the working version: 10-day MA of the typical price ± the 10-day average high–low range. Today use true range.*

**Percentage band:** (B = (1 \pm c) \times MA_t). Works for stocks, not back-adjusted futures (prices can go negative).

**Volatility bands (p. 322), with scaling factor s:**

[
\begin{aligned}
B &= MA_t \pm s\,c\,MA_t &&\text{(percentage of trendline)}\\
B &= MA_t \pm s\,c\,p_t &&\text{(percentage of price)}\\
B &= MA_t \pm s \times ATR_t &&\text{(average true range)}\\
B &= MA_t \pm s \times \sigma_t &&\text{(standard deviation)}
\end{aligned}
]

s > 1 widens the band, s < 1 narrows it. Percentage bands are smoothest; standard deviation reacts most.

**Bollinger bands:** 20-day MA ± 2 standard deviations. Prices are not normal, so 2σ ≈ **87%** containment, not 95.4%. *"If it's not a 20-day average and 2 standard deviations, it's not a Bollinger band."* Bands bulge after volatility spikes and narrow slowly.

**Modified Bollinger bands (McNicholl, p. 325), α = 0.15 ≈ 20 days:**

[
M_t=\alpha C_t+(1-\alpha)M_{t-1},\quad U_t=\alpha M_t+(1-\alpha)U_{t-1},\quad D_t=\frac{(2-\alpha)M_t-U_t}{1-\alpha}
]
[
m_t=\alpha|C_t-D_t|+(1-\alpha)m_{t-1},\quad u_t=\alpha m_t+(1-\alpha)u_{t-1},\quad d_t=\frac{(2-\alpha)m_t-u_t}{1-\alpha}
]
[
BU_t=D_t+f\,d_t,\qquad BL_t=D_t-f\,d_t,\qquad f=2.5
]

Corrects the bulge faster.

**Rules for using bands (pp. 326–328):**
1. **Reversal:** buy on a close above the upper band, sell short on a close below the lower band. Always in; risk = band width.
2. **Enter on the band, exit on the trendline:** buy above the upper band, exit longs below the MA (and vice versa). Neutral zone; risk = half the band; halves order size; allows re-entry in the same direction.
3. Intraday version: high penetrates upper band to buy, low penetrates MA to exit.

**Timing the order (pp. 328–329):** next open, delays of 1–3 days, 50% retracement, etc. In Kaufman's tests, **next-open entries gave better prices ~75% of the time but lower total profits** — fast breakouts that never retrace are missed. *A missed contingent order is guaranteed to be a profit.*

**Reliability vs delay:** wider bands → fewer, more reliable signals, but later entries, smaller average profit, larger risk per trade.

**Bollinger's own use:** usually **mean-reverting** — confirm a downside penetration with volume and breadth; volatility is cyclic, so sell a rally when expanded bandwidth begins to narrow.

**Williams' "Rattlesnake" combination:** Bollinger bands contract inside a 20-day Keltner channel, then a 21-day Chaikin oscillator crosses zero.

---

## 4. Applications of a single trend (pp. 330–336)

**The calculation period is the most important decision** — more important than the method. *"The computer is best for validating an idea, not for discovering one."* Traditional periods: 3, 5, 20–23, 63, 252 days; 20 days for implied volatility.

- **Simple momentum:** buy when (P_t - P_{t-n} > 0). For large n, similar to a moving average.
- **Step-weighted MA (Taylor's MPTDI, 1972):** period, weights, entry penetration and stop all step with the trading range (Table 8.6, gold). Self-adjusting but crude at the step edges → the idea behind adaptive methods (Ch. 17).
- **Volatility system (Bookstaber):** (V_t = \frac{1}{n}\sum TR); sell if the close drops more than (k \times V_{t-1}), buy if it rises more than (k \times V_{t-1}), k ≈ 3.
- **Keltner 10-day MA rule:** 10-day MA of typical price, band = 10-day MA of the high–low range, always reversing. Prices have become noisier since the late 1970s; volatility bands have held up better than short periods.
- **TRIX (Hutson):** triple exponential smoothing of ln(price), signal when it rises/falls two days running, or crosses a 3-day signal line. Recommended 6 days, (s = 2/(n+1)).
  [
  E1_t=E1_{t-1}+s(\ln p_t-E1_{t-1}),\; E2_t=E2_{t-1}+s(E1_t-E2_{t-1}),\; E3_t=E3_{t-1}+s(E2_t-E3_{t-1})
  ]
  [
  TRIX_t=(E3_t-E3_{t-1})\times 10{,}000
  ]
  *The book prints the third line as (E2_t - E1_{t-1}); it should be (E2_t - E3_{t-1}).*
- **Raschke's First Cross:** osc = fast MA − slow MA; buy on the **first pullback** (osc crosses below its average while the low is rising), sell on the mirror image. A selective entry into a new trend.

---

## 5. Comparison of major trend systems (pp. 336–349)

**Six systems, always in the market, entries on the close, no stops:**

| | System | Buy | Sell |
|---|---|---|---|
| M | N-day momentum | (C_t > C_{t-n}) | (C_t < C_{t-n}) |
| MA | Simple MA direction | (MA_t > MA_{t-1}) | (MA_t < MA_{t-1}) |
| EXP | Exponential direction | (E_t > E_{t-1}) | (E_t < E_{t-1}) |
| NDB | N-day breakout | high > highest high of n days and (C_t > C_{t-1}) | low < lowest low and (C_t < C_{t-1}) |
| SWG | Swing breakout | swing high > previous swing high | swing low < previous swing low |
| LRS | Regression slope | slope(n) > 0 | slope(n) < 0 |

MA, EXP, LRS and M are **time-driven** (a trend must evolve, lag). NDB and SWG are **event-driven** (new highs/lows, no lag, a single big move can trigger).

**Test standards:** periods 5–160 (or doubling 5, 10, 20, 40, 80, 160 to keep the percentage change constant), same start date for all, realistic costs ($20 per futures trade, $0.01/share).

**Findings:**
- Eurodollars: all methods profitable, MA best, momentum worst at 160 days. Profit factors of five methods almost identical and **improve as the period lengthens** (Fig. 8.16a).
- S&P: noisier; MA best, momentum the only loss. IBM and the other stocks: losses for nearly all periods; the index smooths individual-stock noise.
- Reliability: MA and momentum ~34% winners, slope and exponential ~43%, breakout just under 50%.
- Breakout: half the trades, much larger profits and **much larger risk** (risk = n-day high − n-day low).
- More than ~200 trades in 20 years → poorer profit factors (Fig. 8.21).
- Percentage-based swings fail on interest-rate futures quoted in price.

[
\boxed{\text{There is no best system, only trade-offs.}}
]

MA = many small losses, few large wins (conservation of capital). Breakout = more reliable, larger profits, much larger risk. Slope in between.

**Robust testing standards (p. 348):** same long test period with bull, bear and sideways markets; same start date; periods giving ~2–100 trades a year; realistic costs; judge by profit factor or information ratio.

---

## 6. Techniques using two trendlines (pp. 350–356)

Slow trend = direction; fast trend = timing.

1. **Crossover:** buy when the fast MA crosses above the slow; always in.
2. **Price vs both:** buy when price is above both MAs, exit when it falls below either. Neutral zone.
3. **Both directions agree:** buy when the fast turns up and the slow is up; exit when they disagree.

**Donchian 5- and 20-day (since 1961, p. 352):** entries need a close beyond both MAs by 1 ATR; exits when the close crosses either MA by 1 ATR. Volatility position sizing: **size = investment ÷ (ATR × big point value)**.

**Donchian 20/40 breakout (p. 353):** buy on a 40-day high, short on a 40-day low, exit longs on a 20-day low, shorts on a 20-day high — the basis of the Turtle method.

**Golden Cross / Death Cross (p. 354):** 50-day MA crossing the 200-day. Mid-1999 to 2010: passive S&P −7.8%, Golden Cross +66.7% (cash index), +36.7% (futures). Out of the market → earn T-bill rate.

**ROC method (Woodshedder):** buy when 5-day ROC < 252-day ROC two days in a row; exit when above two days in a row. Beat the Golden Cross on SPY 1994–2011.

**Staying ahead of the crowd:** 8/18 instead of 10/20, 4-9-18 instead of 5-10-20.

---

## 7. Multiple trends and common sense (pp. 356–359)

- Simpler is often better: a single long MA works because it catches the fat tail.
- If a 10-day and a 20-day are each unprofitable but their combination is, distrust it unless many combinations work or each trend has a clear purpose.
- **Eurodollars 60 + 20 days (Table 8.7):** trading the 20-day only in the 60-day's direction kept days held at 16 (vs 31), lifted profit per trade to $92 (vs $62), and kept the market exposure at ~50% → lower shock risk.
- **Three trends:** a fast third MA slope confirms entry direction (modified 3-crossover). 4-9-18 model. Eurobunds 1990–2011: 20-40-80 crossover had the best profit factor (2.80) with only 42 trades (Table 8.8).
- Appel: sum of three ROCs, buy above 4%.

---

## 8. Selecting the trend method and speed (pp. 359–363)

- The right speed depends on the user: a fund placing money monthly needs very slow trends; a speculator needs the best risk/return profile.
- Short periods that look best in tests are hardest to achieve live (costs, fast markets).
- **Seasonal markets:** use an MA shorter than **¼ of the move** you want to catch; a "best" period of 6 months or more means the test failed to capture the seasonal move.
- Differences between trend methods are small; differences in trade frequency and risk are large. *Sustained moves driven by interest-rate policy are why trend following works.*

**Choosing the speed from a chart (p. 361):** mark the swings you want; IBM July 2000–May 2002 had swings of ~2½ months ≈ a quarter → MA period = **¼ of the swing ≈ 16 days**. Result: 36 trades, 20 profitable, +$114/share, no costs (Table 8.9). Using the worst retracement (2 months → 42-day MA) avoided the correction but lost overall — *accept small losses rather than try to remove them.*

---

## 9. Moving average sequences (pp. 363–366)

- A signal from a 20-day MA is suspect if the 19- and 21-day MAs disagree.
- **Orderly trend change:** short periods turn first, then progressively longer ones (Table 8.10).
- Erratic alternation in the short periods (Table 8.11) or a jump ahead (Table 8.12) = less reliable.
- **Averaging the sequences:** take a range of periods around the target (e.g. 20–30 for a 30-day trend), average their directions or check for consistent progression. Confirmation at the cost of small lag. Alternatively, net several periods for a consensus.

---

## 10. Early exits and projected crossovers (pp. 366–368)

- Macro trends end when policy changes, often long before a slow MA turns (a 200-day MA lags 100 days). Exiting on a clear policy change can protect profits — but such calls are clear only afterwards (2010 vs 2011 bonds).
- **Price at which an n-day MA crosses price:**
  [
  CP1=\frac{\sum_{i=t-n+2}^{t}P_i}{n-1}
  ]
  (the (n-1)-day average).
- **Price at which MAs of periods m and n cross:**
  [
  CP2=m\left(\frac{\sum \text{last } m-1}{m}-\frac{\sum \text{last } n-1}{n}\right)
  ]
- **Lambert's Market Direction Indicator:** (MDI = 100\,(CP_{t-1}-CP_t)/\text{avg of last 2 prices}); buy when it crosses above zero.
- **Forecasting the turn (p. 368):** the MA trendline turns up when today's price > the price dropped n days ago. So **MA trendline direction = n-day momentum.** Using the trendline is usually better than price penetration because the line is smoother and generates fewer trades.

[
\boxed{MA_t > MA_{t-1} \iff P_t > P_{t-n}}
]

---

## Tested on NIFTY (`ch08_lab.ipynb`, daily 2002–2026, next-open fills, 0.03% per side)

| Kaufman's claim | NIFTY | Holds? |
|---|---|---|
| More long runs than random (fat tail) | Runs ≥ 6 days: 5.1% vs 2.8% random / 2.7% shuffled | ✓ |
| Profits come from a few big trades | 40-day MA: top 5 trades = 31% of gross profit, skew 5.8 | ✓ |
| ~35% winners, winners held longer | 37.6% winners, win/loss 2.79, 35.6 vs 8.3 bars | ✓ |
| Trendline beats price cross | Cross: more trades but higher Sharpe at every period | ✗ |
| Noisy index: delayed entry can help | Delay hurt: today's close > next open > next close | ✗ |
| MA direction = n-day momentum | Identical every day | ✓ |
| Longer periods → better profit factor | Up to 80 days for all systems | ✓ |
| Breakout most reliable, fewest trades | ~40% winners, fewest trades | ✓ |
| Bollinger 2σ contains ~87% | 90.8% | ≈ |

- No long/short trend system beat buy & hold's Sharpe (0.76) — shorting a rising index is costly.
- Long-only 40-day MA: Sharpe 0.96, max drawdown −36% vs −59% for buy & hold.
- Bollinger mean reversion lost 7.6%/yr despite 59.5% winning trades — high win rate, losses 2.4× wins.

---

## Chapter 8 completion test

- What three reasons does Kaufman give for why trend systems work?
- What is the fat tail, and why does a trend system need it?
- Trendline direction vs price penetration: which trades less, and when is each better?
- Why does the entry timing (today's close vs next open) matter more in noisy markets?
- What is the profile of a typical trend-following system?
- Why does 2σ give ~87% rather than 95% containment for Bollinger bands?
- How does a breakout system's risk differ from a moving average's?
- Why is the moving average trendline direction the same as n-day momentum?
- How do you choose a trend period from a chart?
