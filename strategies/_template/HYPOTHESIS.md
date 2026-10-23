# NNN-strategy-name — hypothesis

**Write and commit this file before running any backtest.** The commit hash proves it came first.

## Question
What single question does this test answer?

## Market behaviour
What behaviour should make this work, and why should it persist? Cite the Kaufman chapter.

## Rules (exact)
- Indicator(s) and formulas, with `lib/` functions used:
- Entry:
- Exit:
- Stop / invalidation:
- Position size:
- Timing: signal on the close of bar t, trade at that close (the `lib.backtest` convention).

## Data
Instrument(s), frequency, date range, source. In-sample and out-of-sample split, fixed now.

## Parameters
List every parameter and its value. Taken from the book, not optimised.

## Costs
Commission, spread and slippage in bps per unit traded.

## Success criteria (decided now)
What result would make you keep, reject, or need more evidence? Compare against a benchmark (e.g. buy and hold).

## Expected failure modes
When should this lose money?
