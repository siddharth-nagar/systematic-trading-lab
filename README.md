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

## Structure

```text
systematic-trading-lab/
├── README.md
├── requirements.txt
├── 01_kaufman/
│   ├── chapter_09_momentum_oscillators/
│   │   ├── notes.md
│   │   └── ch09_lab.ipynb
│   ├── chapter_10_seasonality/
│   │   └── notes.md          # replication lives in 02_nifty_seasonality/
│   └── chapter_11_cycles/
│       ├── notes.md
│       └── ch11_lab.ipynb
├── 02_nifty_seasonality/     # Research 001 — provisional NIFTY baseline
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

Status: Parts 1–3 covered; Part 4 (phasing and trading rules) next.
