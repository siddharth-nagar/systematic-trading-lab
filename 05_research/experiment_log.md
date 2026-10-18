# Experiment Log

Use one entry per experiment. Keep experiments small while reading the book.

## Template

### Experiment ID
`YYYY-MM-DD-short-name`

### Question
What single question am I testing?

### Hypothesis
What market behaviour should make this work?

### Indicator / rule
Write the exact formula or rule.

### Data
Instrument, frequency, date range, source.

### Parameters
List them explicitly.

### Costs
Commission, spread, slippage assumptions.

### Result
Record only the metrics needed to answer the question.

### Failure modes
When or why did it fail?

### Decision
- [ ] Keep for later research
- [ ] Reject
- [ ] Needs more evidence
- [ ] Educational only

### Next action
One action only.

---

### Experiment ID
`2026-10-18-ch11-cycle-tools-nifty`

### Question
Do Kaufman's Ch.11 Maximum Entropy tools (MESA, phase angle, lateral shift, Hilbert, Fisher, inverse Fisher) give a tradable edge on NIFTY daily data without look-ahead?

### Hypothesis
Short-term cycles exist part of the time; when present, cycle tools time turns and mark sideways regimes (Ehlers: "if a short-term cycle exists, the market is not trending").

### Indicator / rule
Book/Ehlers formulas, causal high-pass detrend. Rules in `03_nifty_cycle_tools/run_tests.py`.

### Data
NIFTY 50 price index, daily OHLC, 2002-09 to 2026-03, secondary sources (see provenance).

### Parameters
Book defaults only: high-pass 48, MESA window 60 / order 10, Fisher channel 10, inverse Fisher 10/20/30, cycle mode 8 of 10 bars with period 6–50.

### Costs
0.03% per side; stress 0.10%. Fill at next open.

### Result
No cycle tool beat buy & hold or a 50-day MA filter. MESA price hit rate 49% vs 56.5% base rate. Hilbert buy signals: next-10-day return 0.55% vs 0.56% unconditional. Fisher cross: 174 changes/yr, destroyed by costs. Inverse Fisher long-only Sharpe 0.85 (vs SMA50 long-only 1.09). Look-ahead FFT version: Sharpe 3.25.

### Failure modes
Red-noise spectrum (dominant period at search edge), cycle episodes of ~6 days, overnight gaps remove short-term edges, costs on high-turnover rules.

### Decision
- [ ] Keep for later research
- [ ] Reject
- [ ] Needs more evidence
- [x] Educational only

### Next action
Continue Kaufman Ch.11 Part 5 (CCI, Short Cycle Indicator, Hurst phasing) — test phasing for the same look-ahead trap.
