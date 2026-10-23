# Kaufman Chapter 12 — Volume, Open Interest, and Breadth

## Status

**Notes and synthetic lab complete; NIFTY replication pending data.** Notes checked against the printed text, pp. 527–564 (2026-10-23).

- Code: [`lib/volume.py`](../lib/volume.py) (tests in `tests/test_volume.py`; On-Balance Volume reproduces Table 12.2 exactly).
- Lab: [`labs/ch12_lab.ipynb`](../labs/ch12_lab.ipynb) (synthetic data with known answers).
- NIFTY data pipeline: `data/fetch_nse.py` → `data/build_nse_daily.py`. Pre-registered tests: [`research/003-nifty-volume-breadth/HYPOTHESIS.md`](../research/003-nifty-volume-breadth/HYPOTHESIS.md).

Items marked *(extra)* are not from Kaufman.

## Chapter map (Kaufman's own headings)

| Section | Pages |
|---|---|
| Introduction; a special case for futures volume; tick volume | 527–529 |
| Variations from the normal patterns (W intraday pattern, variance in volume, volume spikes, drop in volume) | 529–531 |
| Standard interpretation (volume and open interest, exceptions, Equivolume, Herrick Payoff Index, volume predicts volatility) | 531–534 |
| Volume indicators (average, normalising, momentum, Force Index, volume oscillator, OBV, MFI, volume count, volume accumulator, A/D, intraday intensity, PVT, PVI/NVI, Aspray, tick volume, VWMACD, eVWMA, open interest instead of volume, VWAP) | 535–546 |
| Breadth indicators (A/D, Sibbett, Bolton-Tremblay, Schultz, McClellan, UDR, TRIN, Thrust, new highs and lows, baskets; is one better; breadth as countertrend) | 546–554 |
| Interpreting volume and breadth systematically (volume spikes, moving average approaches, A/D system, breadth as counter-trend) | 554–558 |
| An integrated probability model | 558–559 |
| Intraday volume patterns (time stamps, patterns, relative changes) | 559–562 |
| Filtering low volume (low-volume periods, small price moves) | 562–564 |
| Market Facilitation Index | 564 |

---

## 1. Data and its quirks (pp. 527–531)

- **Futures:** use **total** volume and **total** open interest (all delivery months). Single-contract volume rises as a contract becomes the nearby and falls before expiry. Spread trades are not in reported volume. Volume and OI are official one day late.
- **Stocks:** the equivalent of total volume is the sector's combined volume.
- **Tick volume** (number of price changes) is a good substitute for real volume intraday.
- **Intraday W/U pattern:** volume is always high at the open and close and low at midday, so "rising volume" must be compared with the **same time of day** on earlier days.
- **Seasonal patterns** in volume, OI and breadth (summer lull, year-end positioning, crop hedging) are not signals.
- **Volume is erratic:** Microsoft 1998–2003 averaged 71 million shares a day with a daily standard deviation of about 28 million (~38%), against a price standard deviation under 3%. Almost every volume indicator smooths.
- **Volume spike:** a day with 2–4× the previous volume. Usually marks the **end** of a move, a climax when everyone has acted ("the boat sinks"). It does not say how far the reversal goes.
- **Drop in volume:** lack of conviction or equilibrium (fair value). AOL rose on half the volume in late 1999 and then sold off.

## 2. Standard interpretation (pp. 531–534)

| Volume | Price | Reading |
|---|---|---|
| Rising | Rising | Confirms the rise |
| Rising | Falling | Confirms the drop |
| Falling | Rising | Weak rally |
| Falling | Falling | Weak pullback |

*"Volume confirms direction"*, so *"volume normally leads price."*

**Open interest** (futures only) changes only when a new buyer meets a new seller (+) or an old long meets an old short (−).

| Volume | OI | Reading |
|---|---|---|
| Rising | Rising | Confirms the trend |
| Rising | Falling | Liquidation (at extremes) |
| Falling | Rising | Slow accumulation |
| Falling | Falling | Congestion |

| Price | Volume | OI | Reading |
|---|---|---|---|
| Rising | Rising | Rising | New buyers entering |
| Falling | Falling | Falling | Longs forced out; ends when they have liquidated |
| Rising | Falling | Falling | Short covering; money leaving |
| Falling | Rising | Rising | New short selling |

- Exceptions: lower volume on Mondays, before holidays and in summer; higher volume on triple and quadruple witching days.
- **Equivolume** (Arms) replaces time with volume on the chart. No systematic rules.
- **Herrick Payoff Index** combines price, volume and OI (covered in Ch 9).
- **High volume = high risk**, even on days when price closes unchanged: it is potential volatility.

## 3. Volume indicators (pp. 535–546)

| Indicator | Formula (per day, then accumulated where noted) |
|---|---|
| Average volume | 50 days, or the same period as the price MA; under 50 is not smooth |
| Normalised volume | (100 \cdot V_t / \overline{V}_N) |
| Volume momentum / % | (V_t - V_{t-n}), (V_t/V_{t-n} - 1); must be smoothed |
| Force Index (Elder) | ((C_t - C_{t-1})V_t); EMA 2 for timing (buy low, sell high), EMA 13 as a trend (zero cross) |
| Volume oscillator | MA(14) − MA(34), or sum(14)/sum(34) |
| **On-Balance Volume** (Granville) | (\pm V_t) by the sign of the close change, accumulated. Table 12.2 replicated exactly |
| OBV trend | MA of OBV (up to 100 weeks) crossing; OBV can replace price in an MA system (Fig. 12.4) |
| Money Flow Index | typical price (TP=(H+L+C)/3); flows (TP\cdot V) split by TP direction; RSI-like 0–100 |
| Volume Count | (\pm1) by the sign of the volume change, accumulated |
| Volume Accumulator (Chaikin) | (((C-L)/(H-L) - 0.5)\cdot2V), accumulated |
| Accumulation/Distribution (Chaikin) | ((C-O)/(H-L)\cdot V), accumulated (previous close if no open) |
| Intraday Intensity | (((C-L)-(H-C))/(H-L)\cdot V), accumulated |
| Price-Volume Trend | ((C_t/C_{t-1}-1)V_t), accumulated; not for back-adjusted futures |
| PVI / NVI | two indices; Fosback 1941–1975: PVI up → 79% bull, NVI up → 96% bull; trend = 127- or 255-day MA |
| Aspray Demand Oscillator | BP − SP, losing side's volume ÷ (K·|% change|), (K = 3C / \text{10-day avg 2-day range}) |
| Tick Volume Indicator (Blau) | double-smoothed up minus down ticks, ±100 |
| VWMACD | VWMA(12) − VWMA(26), signal smoothing 0.20 |
| eVWMA (Fries) | (((OS-V)\cdot eVWMA_{t-1} + V\cdot C)/OS), OS = shares outstanding |
| Open interest for volume | futures volume trends for years with the market; total OI is steadier and can replace volume |
| VWAP / TWAP | execution benchmarks, not indicators |

### OBV interpretation (Table 12.3)

Price up and OBV up: clear uptrend. Price up and OBV down: weak uptrend, near reversal. Price sideways and OBV up: accumulation (bottom). Price sideways and OBV down: distribution (top). The down cases mirror these.

## 4. Breadth (pp. 546–554)

Breadth is the balance of advancing and declining issues. It **confirms** price the same way volume does (breadth up and price up = confirmed). It must match what you trade: Dow breadth says little about small caps. Appel: use an **equally weighted** count.

| Indicator | Formula |
|---|---|
| A/D oscillator | (A_t - D_t) |
| **A/D line** | (ADI_{t-1} + (A_t - D_t)) (book misprints the sign) |
| Sibbett Demand Index | (\sum_{10} \text{up volume} / \sum_{10} \text{down volume}) (Merrill: 5) |
| Bolton-Tremblay | (BT = (A-D)/U); index adds (\pm\sqrt{|BT|}); spikes when unchanged is small |
| Schultz | (100 \cdot A / \text{total issues}) |
| **McClellan Oscillator** | (EMA_{0.10}(A-D) - EMA_{0.05}(A-D)) (19/39 days) |
| Upside/Downside Ratio | up volume / down volume; unbounded above, 0–1 below |
| **TRIN (Arms)** | ((A/D) / (AV/DV)) |
| Thrust Oscillator (Chande) | (100(A\cdot AV - D\cdot DV)/(A\cdot AV + D\cdot DV)); ±30 overbought/oversold |
| High-Low Index | (HLX_{t-1} + NH - NL) (52-week highs/lows) |
| High-Low Ratio (Appel) | (\sum_{10} NH / \sum_{10}(NH+NL)); buy above 0.80–0.90 |
| Baskets | long new-high stocks, short new-low stocks, equal volatility (Ch 13) |

- Kaufman suggests expressing TRIN and Thrust components as **percentages of the total**, so inactive days don't distort them.
- **Is one better?** OBV and Bolton-Tremblay assign all volume on a tiny price change; Chaikin's proportional split and Sibbett's 10-day sums are more sensible. *"A collection of minor manipulation of data"*: volume and breadth are **as hard to interpret as price** and must be tested in a system.

## 5. Systematic use (pp. 554–559)

- Accumulation indices + long-term smoothing → trend confirmation. Extreme volume → reversal. Volume peak before price peak → trend change.
- **Volume spike rule:** (V_t > T \times \text{average volume of } n \text{ days ending 5 days ago}); lagging the average stops a 2–3 day build-up from raising its own threshold. Spikes are milder in futures and indexes.
- **Volume filter (Saitta):** 20-day trend signal taken only if today's volume exceeds its 10-day average. Fewer trades, less risk, the same idea of participation.
- **Waxenberg:** 10-day average volume is normal; a trend change needs +20%, extremes appear near +40%; or use Bollinger bands on volume. Alternatively, 13-day up volume − down volume as momentum.
- **CHADTP (Connors-Hayward):** ((\sum_5 A - \sum_5 D)/5); ±400 extremes on NYSE; sell short above +400 when S&P trades 10 bp below the prior low, buy below −400 when 10 bp above the prior high; 5–7 day horizon. Developed in 1995; thresholds need scaling for today's volatility.
- **Breadth as countertrend (Connors, 1996–2003):** declines > advances for 3+ days → S&P +0.50% next week; NASDAQ 2+ days → NDX +0.80%; declines ≥ 2× advances → S&P +0.60%; the opposite cases ≈ 0. A/D ratio rule: sell above 2.0, buy below 0.5.
- **Integrated probability model:** 1-day-ahead forecasts of price, volume, OI and OBV, each = value + regression slope over n days, combined with weights (w_1 \dots w_4) found by backtest. *(extra)* Choosing n and four weights by backtest is optimisation; it needs out-of-sample validation (Ch 21).

## 6. Intraday volume (pp. 559–562)

- Bar time stamps can mark the start or the end of the bar; the last bar may hold only one minute of trading.
- 15-minute tick-volume patterns are U-shaped (open and close heavy, lunch light) and differ by market and session overlap (DAX, crude, NASDAQ, bonds).
- Compare each intraday bar with the **same bar** on previous days, or with the first bar. A high-volume open predicts a high-volume, more volatile day.

## 7. Filtering low volume (pp. 562–564)

- Ignore low-volume days in an accumulation index: skip days with (V < \overline{V}_n - k\,\sigma_n(V)).
- Ignore days with very small price moves (price-filtered OBV).
- **Market Facilitation Index** (Williams): ((H-L)/V). Volume up and MFI up confirm direction; both down means a false move; volume up and MFI down may be a new trend; volume down and MFI up means poor timing.

---

## Book errors found

- **p. 547:** A/D index printed as (ADI_{t-1} - A_t - D_t); it is (ADI_{t-1} + (A_t - D_t)).
- **p. 548:** Bolton-Tremblay subtracts (\sqrt{BT}) when BT < 0, the root of a negative number; it should be (\sqrt{|BT|}).
- **p. 548:** Schultz is said to range 0–100, but the formula has no ×100.
- **p. 540:** Money Flow Index flows are accumulated over all history, with no period. The standard version uses n-day (usually 14) sums; `lib` uses that.
- **p. 542:** PVI/NVI variation 2 ("+ (C_t/C_{t-1}) × V_t") is not Fosback's index, which compounds the day's % price change. `lib` offers variation 1 and Fosback's form.
- **p. 563:** "a 2 standard deviation filter removes 32% of the days" is wrong. For a normal distribution a one-sided 2σ cut removes ≈2.3% (and 1σ ≈16%). 32% is the two-sided 1σ figure. Volume is skewed, so check it on real data.
- **p. 555:** the lagged-average sum runs from (t-n-5) to (t-5), which is n+1 days, divided by n.

## Model-building lessons

1. Volume and breadth are noisier than price: smoothing is mandatory, and every smoothing choice is a parameter.
2. Many indicators reuse the sign of the price change (OBV, PVT, PVI/NVI). *(extra)* On synthetic data where volume is pure noise, OBV still tracks price closely. Much of OBV's "information" is price.
3. Use **total** futures volume and OI; use **value** or OI × price across lot-size changes. *(extra)* NIFTY lots have changed several times.
4. Compare like with like: same time of day intraday, same season across years.
5. Breadth must match the traded instrument (NIFTY 50 vs all NSE stocks).
6. The literature mostly reads breadth as confirmation; Connors reads it as countertrend. Only a pre-declared test decides which holds for NIFTY.

## Chapter 12 completion test

- Why use total futures volume and open interest rather than one contract's?
- What does rising price, falling volume and falling open interest mean?
- Calculate OBV for Table 12.2 by hand.
- How do Chaikin's Volume Accumulator and Granville's OBV differ, and why does Kaufman prefer the proportional split?
- Write the A/D line, McClellan Oscillator and TRIN formulas. Where does the book misprint the A/D line?
- Why is the volume-spike average lagged five days?
- What share of days does a one-sided 2σ low-volume filter remove, and why does the book's 32% not apply?
- What did Connors find about declining breadth, and why is that a countertrend claim?
