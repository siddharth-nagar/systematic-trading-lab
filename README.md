# Systematic Trading Lab

A deliberately small research repository for learning Perry Kaufman's *Trading Systems and Methods* and gradually converting ideas into testable systematic-trading components.

## Current objective

**Finish the book before building a production trading bot.**

Use this loop:

> Learn → Explain → Implement → Visualise → Test lightly → Record → Move on

## Guardrails

1. One active learning objective at a time.
2. No parameter optimisation while reading the book.
3. Replicate important ideas before trying to improve them.
4. Separate an indicator from the trading hypothesis built around it.
5. Record failure modes, not only successful examples.
6. Put new strategy ideas in `06_strategy_ideas/parking_lot.md` instead of pursuing them immediately.
7. A chapter is complete when you can:
   - explain the main ideas;
   - write the essential formulas;
   - implement the major concepts;
   - visualise their behaviour;
   - explain when they should fail.

## Progress

| Chapter | Notes | Lab / replication | Checked against printed text |
|---|---|---|---|
| 8 — Trend systems | `01_kaufman/chapter_08_trend_systems/` | `ch08_lab.ipynb` (Kaufman's tests on NIFTY) | yes, pp. 309–368 |
| 9 — Momentum and oscillators | `01_kaufman/chapter_09_momentum_oscillators/` | `ch09_lab.ipynb` (synthetic) | yes, pp. 369–426 |
| 10 — Seasonality and calendar patterns | `01_kaufman/chapter_10_seasonality/` | Research 001: `02_nifty_seasonality/` | yes, pp. 427–484 |
| 11 — Cycle analysis | `01_kaufman/chapter_11_cycles/` | `ch11_lab.ipynb` (synthetic) + Research 002: `03_nifty_cycle_tools/` | yes, pp. 485–526 |
| 12 — Volume, open interest, breadth | next | — | — |

## Research findings so far

- **Research 001 — NIFTY seasonality:** no evidence that calendar-month means differ (omnibus permutation p ≈ 0.575, 2000–2025, provisional secondary data).
- **Ch.8 lab — trend systems on NIFTY:** Kaufman's fat tail holds (long runs and a few big trades drive profits); long-only 40-day MA trend filter Sharpe 0.96 vs 0.76 buy & hold with a much smaller drawdown; on NIFTY, price-cross signals and same-day-close entries beat Kaufman's preferred trendline signals and delayed entries.
- **Research 002 — Ch.11 cycle tools on NIFTY:** no cycle tool beat buy & hold with next-open fills and costs; trend filters survived (a plain 50-day MA filter was best); look-ahead versions showed fake Sharpe ratios of 2.9–3.3.

## Structure

```text
systematic-trading-lab/
├── README.md
├── requirements.txt
├── 01_kaufman/
│   ├── chapter_08_trend_systems/
│   │   ├── notes.md
│   │   └── ch08_lab.ipynb
│   ├── chapter_09_momentum_oscillators/
│   │   ├── notes.md
│   │   └── ch09_lab.ipynb
│   ├── chapter_10_seasonality/
│   │   └── notes.md          # replication lives in 02_nifty_seasonality/
│   └── chapter_11_cycles/
│       ├── notes.md
│       └── ch11_lab.ipynb
├── 02_nifty_seasonality/     # Research 001 — provisional NIFTY baseline
├── 03_nifty_cycle_tools/     # Research 002 — Ch.11 cycle tools on NIFTY, no look-ahead
├── 05_research/
│   └── experiment_log.md
└── 06_strategy_ideas/
    └── parking_lot.md
```

## Chapter 9 implementation scope

The Chapter 9 notebook is intentionally a **learning notebook, not a strategy optimiser**. It covers:

- n-period momentum;
- RSI(14) and RSI(2);
- Stochastic %K/%D;
- MACD;
- one trend + oscillator entry architecture;
- basic sanity checks and failure-mode notes.

Synthetic data are used so the focus stays on understanding the mechanics rather than data sourcing.

## Chapter 11 implementation scope

The Chapter 11 notebook is a **learning notebook, not a strategy optimiser**. It plants known 20-day and 8-day cycles in synthetic data and checks whether each method recovers them:

- detrending (full-sample linear, EMA difference, triangular MA);
- trigonometric regression period search (one and two frequencies);
- FFT periodogram;
- spectral leakage and the Hann taper;
- a permutation test for whether the largest peak beats noise;
- basic sanity checks and failure-mode notes.

Status: chapter complete. NIFTY replication of Parts 4–5 in `03_nifty_cycle_tools/`.
