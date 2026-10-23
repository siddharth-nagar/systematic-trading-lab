# Kaufman Lab

A deliberately small research repository for learning Perry Kaufman's *Trading Systems and Methods* and gradually turning the ideas into tested systematic-trading components.

## Current objective

**Finish the book before building a production trading bot.**

> Learn → Explain → Implement → Visualise → Test lightly → Record → Move on

Standing rules (for you and for Claude) are in [CLAUDE.md](CLAUDE.md).

## Progress

| Chapter | Notes | Lab | Status |
|---|---|---|---|
| 9 — Momentum and oscillators | [notes](notes/ch09-momentum-oscillators.md) | [ch09_lab.ipynb](labs/ch09_lab.ipynb) | Complete |
| 10 — Seasonality | [notes](notes/ch10-seasonality.md) | [ch10_seasonal_index.py](labs/ch10_seasonal_index.py), [research 001](research/001-nifty-seasonality/README.md) | Complete |
| 11 — Cycle analysis | [notes](notes/ch11-cycle-analysis.md) | [ch11_lab.ipynb](labs/ch11_lab.ipynb) | Lab complete |
| 12 — Volume, open interest and breadth | — | — | Next (needs data: NIFTY futures volume/OI, NSE advance-decline) |

| Research / strategy | Status | Result |
|---|---|---|
| [001 — NIFTY monthly seasonality](research/001-nifty-seasonality/README.md) | Paused at data audit | No evidence of a month effect (p ≈ 0.57) |
| Strategies | None yet | Start from [`strategies/_template/`](strategies/_template/HYPOTHESIS.md) |

Every test run is logged in [`experiments/log.csv`](experiments/log.csv).

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
├── labs/                   # chapter notebooks/scripts (import from lib/)
│   └── results/
├── lib/                    # shared, tested building blocks
│   ├── indicators.py       # MAs, RSI, stochastic, MACD, ATR, ADX, efficiency ratio, CCI, Fisher, Hilbert
│   ├── cycles.py           # periodogram, trig regression, cycle permutation test
│   ├── signals.py          # crossovers, entry/exit → position
│   ├── backtest.py         # the one backtest engine
│   └── metrics.py          # CAGR, Sharpe, max DD, MAR, profit factor, win rate
├── research/
│   └── 001-nifty-seasonality/
├── strategies/
│   ├── _template/          # HYPOTHESIS.md, config.yaml, strategy.py, RESULTS.md
│   └── PARKING_LOT.md
├── experiments/
│   └── log.csv             # one row per run: date, id, commit, params, result
├── tests/                  # unit tests for lib/
├── data/                   # small curated data + provenance; data/downloads/ is gitignored
└── pyproject.toml          # pinned dependencies
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest                     # lib/ must pass before any research
jupyter nbconvert --to notebook --execute --inplace labs/ch11_lab.ipynb
```

Synthetic data are used in the labs where possible, so the focus stays on mechanics and the true answer is known.
