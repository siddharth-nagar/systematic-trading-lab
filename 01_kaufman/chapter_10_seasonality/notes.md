# Kaufman Chapter 10 — Seasonality and Calendar Patterns

## Status

**Chapter covered (Level 2 — Replicate).** Notes checked against the printed text, pp. 427–484 (2026-10-20). An earlier version, rebuilt from study sessions, overstated the need for detrending and mixed in statistical tests that are not Kaufman's; both are corrected below and extras are marked *(extra)*.

Replication: [`02_nifty_seasonality/`](../../02_nifty_seasonality/) — a provisional NIFTY baseline. Deep validation (Level 3) is deferred until the book is finished.

## Chapter map (Kaufman's own headings)

| Section | Pages |
|---|---|
| Introduction; a consistent factor; the seasonal pattern | 427–429 |
| Popular methods for calculating seasonality (data, decomposition, detrending, averages, cash vs futures, indexing, first differences, yearly averages, link relatives, moving average method, X-11/X-12, Winter's) | 430–451 |
| Changes in seasonal patterns; seasonal volatility; weather sensitivity | 452–456 |
| Seasonal filters (heating oil, years with similar characteristics, seasonal vs nonseasonal years, December corn, continuous futures, stocks, key dates, studies) | 456–478 |
| Seasonality and the stock market (holiday effect, month-end, Hirsch, January barometer, McGinley, September/October) | 478–483 |
| Common sense and seasonality; being too specific about targets | 483–484 |

---

## 1. What seasonality is (pp. 427–429)

**Seasonality is a cycle that repeats every year.** It is most reliable when it comes from nature or fixed habits:
- Agriculture: low at harvest (forced selling, limited storage), higher in the growing season; forward prices include **carrying charges** (storage), even when temporarily inverted.
- Energy and consumer demand: heating oil in winter, gasoline and airlines in summer.
- Industrial metals: copper tied to housing.
- Stocks: only companies with a single seasonal source of income (airlines, travel, retail at Christmas).

Price components (Ch. 6): trend, seasonal, cycle, chance.

[
P_t = T_t + S_t + C_t + \epsilon_t
]

Seasonal patterns are easier to find than cycles because they **must repeat each calendar year**. Kaufman uses the calendar year for uniformity (crop year is better for grains).

**Currency matters:** a world price in USD looks different to buyers in other currencies — sometimes the currency move must be separated from the commodity move (Argentine peso example, p. 465).

---

## 2. Data rules (pp. 430, 433–434, 465–468)

- Use **monthly** data — shorter periods add noise.
- **Back-adjusted futures cannot be used for percentages** (old prices can be far off or negative). Cash prices give the traditional seasonal pattern; futures patterns can differ sharply (wheat: cash shows the classic pattern, back-adjusted futures do not). *"Futures prices may work for some markets, but cash prices are safer."*
- But if you trade futures, use **futures patterns** — the futures price already discounts expectations.
- Stock prices must be split-adjusted.

---

## 3. Methods for calculating seasonality (pp. 430–451)

| Method | How | Note |
|---|---|---|
| Seasonal differences / decomposition | Statistical software, period 12 (monthly) or ~252 (daily) | Separates trend, seasonal, cycle, noise |
| **Average prices** | Year × month table; average and **median** each month; divide by the average of all months → adjusted average/median | Simple; high-price years dominate |
| **Indexing** | Chain monthly % changes into an index starting at 100, then average | Interpreted as % — needs cash or stock prices |
| **Detrending** | Linear regression of price on 1, 2, 3, …; seasonal table of the residuals | See the lesson below |
| **First differences** (Bernstein) | Month-to-month changes; average per month; **% of years up** | Removes trend; distorted when price level changes a lot (Amazon) |
| **Yearly averages** | Each month ÷ that year's average − 1 | Works with back-adjusted futures |
| **Link relatives** | Month ÷ previous month → average → chain relatives (Jan = 1.00) → correct for trend → index of seasonal variation | Thorough; same idea as average monthly % change |
| **Moving average method** | Centred 12-month average (lag 6, average of rows 6 and 7); seasonal factor = price − midpoint; index = 1 + factor/100 | Simple and "equally as good as the best" |
| X-11 / X-12-ARIMA | Census method with repeated MA estimates, outlier weights, Henderson MA | Used for CPI, housing, etc. |
| Winter's method | (X_t = (a + bt) \times S_t + e_t), updated with each observation | Self-correcting trend × seasonal model |

**Average Percentage Price (method of yearly averages):**

[
APP_i = \frac{100}{N}\sum_{n=1}^{N}\frac{P_{n,i}}{\frac{1}{12}\sum_{j=1}^{12}P_{n,j}}, \qquad i = 1,\dots,12
]

### Lesson on detrending (corrected)

- Kaufman calls detrending "theoretically essential" because a strong trend can overwhelm the seasonal moves.
- **But in his Amazon test the detrended and raw patterns had the same shape** (Nov–Dec strongest either way). He concludes *"for finding the overall seasonal pattern for trading, it is not necessary to detrend prices."*
- A modest steady trend adds roughly equally to every month, so it shifts the level but not the pattern (wheat: 0.42% a year).
- The **median** is preferred to the mean: it shows the typical result, not one or two extreme years.

*(extra)* For a market with strong drift, such as NIFTY, "positive in 60% of years" says little on its own; compare each month with the unconditional average.

---

## 4. Robustness of a seasonal pattern (pp. 440–441, 452–454)

- **A few volatile years distort averages** — cotton 2009–2011 vs 1973–2011. Plot each month's max and min moves and the sorted monthly changes.
- **Patterns change:** wheat's low moved from June (1966–2010) to April (2001–2010) as South American production grew. Systems need a **broad window**, not an exact month.
- **Seasonal volatility confirms a pattern:** a steady build-up of volatility into the peak month (heating oil, Dec–Jan) indicates a genuine seasonal concern; a single price shock shows a one-month spike without build-up. Uses: trade only longs in winter, cut size in the riskier months, buy options volatility.
- **Weather sensitivity:** a measure of potential volatility, not direction. Heating and cooling degree days:
  [
  HDD_t = \max(0, 65°F - T_t), \qquad CDD_t = \max(0, T_t - 65°F)
  ]
  accumulated over the critical months.

---

## 5. Seasonal filters and strategies (pp. 456–478)

- **Seasonal filter:** favour longs or shorts in the periods where the (detrended, median) pattern is clear, confirmed by volatility.
- **Heating oil (1984–2011):** % of up months and average change → long end Feb–end Mar, end May–end Aug, end Oct–end Dec; short end Mar–end May and end Aug–end Oct. Average into positions; month-end prices are more practical than monthly averages.
- **Years with similar characteristics:** split corn years into **bull and bear** (July–Dec average vs Jan–Jun): 16 bull, 25 bear; bear years show the "normal" pattern.
- **Seasonal vs nonseasonal years (corn):** position of the month-end price in the past **5-year high–low range** (like a raw stochastic):
  - Seasonal year: end-April in the lower 50% → buy end-April, exit end-July; end-July in the upper 35% → sell end-July, exit end-October.
  - Nonseasonal year: end-January in the upper 35% → sell end-January, exit end-October.
- **"Not quite so easy":** cash corn cannot be traded directly. **December corn futures** show a different pattern (lows in June and September): sell end-Feb → end-July was consistently profitable; buy end-July → end-Oct was break-even.
- Back-adjusted continuous futures can be used with price differences only, and recent volatile years dominate.
- **Stocks:** AMR (American Airlines) peaks in April and Nov–Dec, lows in September; removing crisis months changed little — but removing outliers is a form of data manipulation. *Caveat emptor.*
- **Must have a fundamental reason:** the coffee-crop/European-wheat "18 years in a row" story was overfitting from testing hundreds of combinations. *"The computer is used to validate a belief, not to create one."*
- **Key dates and published studies** (Grushcow & Smith, ContiCommodity, Bernstein): prefer patterns reliable over many years; agricultural products are the most seasonal; copper is the only consistent non-agricultural market. Bernstein's weekly calendar: ≥ 64% up = upward week, ≤ 36% = downward.

---

## 6. Seasonality and the stock market (pp. 478–483)

- S&P (back-adjusted e-mini, 1982–2010): summer weakness 1982–2000; October–November strength persists; "sell in May" no longer reliable. DJIA cash: peak end of April, rally in October.
- **Holiday effect (Merrill, 1897–1964):** day before holidays up **67.9%** vs 50.8% after; Thanksgiving to New Year 74%. Fosback: buy 2 days before, exit the day before the holiday. Kaeppel: buy the close 3 days before, sell 2 days later.
- **Month-end:** buy the last (or second-to-last) day of the month, exit on the 4th trading day of the new month — still viable but weaker since 1975 (Freeburg).
- **Hirsch:** long 1 November – 30 April; almost all gains came in those six months.
- **January barometer:** first 5 days + rest of January predict the year (better 1938–1989 than 1900–1937; weak 1999–2010). **McGinley:** first five days all up → hold the S&P all year (~81–82% right since 1942).
- **September** consistently weak; **October** most volatile but most "ricochet" rallies (17 since 1950).

---

## 7. Common sense (pp. 483–484)

- Study seasonality only where weather, nature or consumer behaviour drives it. Financial markets (bonds, yen) have no reason to be seasonal — players can choose when to act.
- *"If you find a pattern in a market that cannot be clearly explained by fundamentals, it is best to avoid it."*
- **Don't be too specific:** no "optimal day". The corn high is usually July but sometimes June or August; use monthly data, a window, and average into positions or use timing tools inside the window.

---

## 8. NIFTY replication (provisional)

- Monthly close-to-close returns 2000–2025 (302 returns) — equivalent to Kaufman's first-differences / link-relative idea in percent.
- *(extra)* Omnibus within-year permutation test (5,000 replicates): **p ≈ 0.575** — no evidence that calendar-month means differ.
- Data still needs reconciliation against official NSE records (six missing months, two conflicting closes).
- Kaufman would ask first: *is there a fundamental reason for NIFTY to be seasonal?* An equity index has weaker reasons than a crop — consistent with the null result.

See [`omnibus_report.md`](../../02_nifty_seasonality/results/omnibus_report.md).

---

## 9. Model-building lessons

1. Seasonality needs a fundamental cause; otherwise the pattern is probably overfitting.
2. Use monthly data, medians, and a window rather than exact dates.
3. Data type changes the answer (cash vs futures vs back-adjusted).
4. A few extreme years can create or hide a pattern; patterns drift over decades.
5. Volatility build-up is a useful confirmation.
6. A descriptive table is not a backtest: tradable instruments, costs and carry matter (cash corn vs December futures).

---

## Chapter 10 completion test

- Why are seasonal patterns easier to find than cycles?
- Why can't back-adjusted futures be used for percentage seasonality?
- What did Kaufman conclude about detrending from the Amazon example?
- How does the method of link relatives work, step by step?
- How does seasonal volatility help confirm a pattern?
- How does the corn model decide between a seasonal and a nonseasonal year?
- What are the holiday, month-end and Hirsch effects?
- Why does Kaufman say to avoid patterns without a fundamental explanation?
