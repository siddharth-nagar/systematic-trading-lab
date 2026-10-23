# Kaufman Lab

A deliberately small research repository for learning Perry Kaufman's *Trading Systems and Methods* and gradually turning the ideas into tested systematic-trading components.

## Current objective

**Finish the book before building a production trading bot.**

> Learn → Explain → Implement → Visualise → Test lightly → Record → Move on

Standing rules (for you and for Claude) are in [CLAUDE.md](CLAUDE.md).

## Progress

| Chapter | Notes | Lab / replication | Checked against printed text |
|---|---|---|---|
| 8 — Trend systems | [notes](notes/ch08-trend-systems.md) | [ch08_lab.ipynb](labs/ch08_lab.ipynb) (Kaufman's tests on NIFTY) | yes, pp. 309–368 |
| 9 — Momentum and oscillators | [notes](notes/ch09-momentum-oscillators.md) | [ch09_lab.ipynb](labs/ch09_lab.ipynb) (synthetic) | yes, pp. 369–426 |
| 10 — Seasonality and calendar patterns | [notes](notes/ch10-seasonality.md) | [Research 001](research/001-nifty-seasonality/README.md), [ch10_seasonal_index.py](labs/ch10_seasonal_index.py) | yes, pp. 427–484 |
| 11 — Cycle analysis | [notes](notes/ch11-cycle-analysis.md) | [ch11_lab.ipynb](labs/ch11_lab.ipynb) (synthetic), [ch11_extras.ipynb](labs/ch11_extras.ipynb), [Research 002](research/002-nifty-cycle-tools/README.md) | yes, pp. 485–526 |
| 12 — Volume, open interest, breadth | next | data pipeline ready: `data/fetch_nse.py` → `data/build_nse_daily.py` (not yet run on real data) | — |

## Research findings so far

- **Research 001 — NIFTY seasonality:** no evidence that calendar-month means differ (omnibus permutation p ≈ 0.575, 2000–2025, provisional secondary data).
- **Ch.8 lab — trend systems on NIFTY:** Kaufman's fat tail holds (long runs and a few big trades drive profits); long-only 40-day MA trend filter Sharpe 0.96 vs 0.76 buy & hold with a much smaller drawdown; on NIFTY, price-cross signals and same-day-close entries beat Kaufman's preferred trendline signals and delayed entries.
- **Research 002 — Ch.11 cycle tools on NIFTY:** no cycle tool beat buy & hold with next-open fills and costs; trend filters survived (a plain 50-day MA filter was best); look-ahead versions showed fake Sharpe ratios of 2.9–3.3.
- **Ch.11 extras:** the book's copper cycle (8.4 quarters) does not reproduce from its own table (~10 quarters); smoothing a random walk creates convincing fake cycles; NIFTY monthly returns show no cycle (p ≈ 0.80).

Every test run is logged in [`experiments/log.csv`](experiments/log.csv) (one row per run) and [`experiments/log.md`](experiments/log.md) (narrative).

## Guardrails

1. One active learning objective at a time.
2. No parameter optimisation while reading the book.
3. Replicate important ideas before trying to improve them.
4. Separate an indicator from the trading hypothesis built around it.
5. Record failure modes, not only successful examples.
6. Put new strategy ideas in [`strategies/PARKING_LOT.md`](strategies/PARKING_LOT.md) instead of pursuing them immediately.
7. A chapter is complete when you can:
   - explain the main ideas;
   - write the essential formulas;
   - implement the major concepts;
   - visualise their behaviour;
   - explain when they should fail.

## Structure

```text
systematic-trading-lab/
├── CLAUDE.md               # standing instructions for Claude
├── README.md               # this progress map
├── notes/                  # chapter summaries, formulas, completion tests
├── labs/                   # chapter notebooks/scripts
│   └── results/
├── lib/                    # shared, tested building blocks
│   ├── indicators.py       # MAs, regression slope, RSI, stochastic, MACD, ATR, ADX, efficiency ratio, CCI, Fisher, Hilbert
│   ├── cycles.py           # periodogram, trig regression, cycle permutation test, high-pass detrend, MESA (Burg), cycle mode
│   ├── signals.py          # crossovers, entry/exit → position
│   ├── backtest.py         # the one backtest engine (close / next-open / next-close fills)
│   ├── nse.py              # NSE bhavcopy parsers (legacy + UDiFF), futures totals, breadth
│   └── metrics.py          # CAGR, Sharpe, max DD, MAR, profit factor, win rate
├── research/
│   ├── 001-nifty-seasonality/
│   └── 002-nifty-cycle-tools/
├── strategies/
│   ├── _template/          # HYPOTHESIS.md, config.yaml, strategy.py, RESULTS.md
│   └── PARKING_LOT.md
├── experiments/
│   ├── log.csv             # one row per run: date, id, commit, params, result
│   └── log.md              # narrative entries
├── tests/                  # unit tests for lib/
├── data/                   # small curated data + provenance; fetch_nse.py / build_nse_daily.py; data/downloads/ is gitignored
└── pyproject.toml          # pinned dependencies
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest                     # lib/ must pass before any research
python data/fetch_nse.py --start 2024-06-24 --end 2024-07-19   # NSE data for Ch 12 (needs access to nseindia.com)
python data/build_nse_daily.py       # then read data/downloads/nse/build_report.txt
jupyter nbconvert --to notebook --execute --inplace labs/ch11_extras.ipynb
```

Synthetic data are used in the labs where possible, so the focus stays on mechanics and the true answer is known.
