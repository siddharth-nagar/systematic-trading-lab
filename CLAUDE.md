# Instructions for Claude

This is a student's learning lab for Perry Kaufman's *Trading Systems and Methods*. The goal is understanding first and tested building blocks second. Profitable strategies come later.

## Workflow

Learn → Explain → Implement → Visualise → Test lightly → Record → Move on.

- Work on one chapter or one research question at a time. New ideas go in `strategies/PARKING_LOT.md`.
- Do not optimise parameters while reading the book. Use the book's values.
- Replicate the book before trying to improve it. If a number does not reproduce, say so and record it. Never tune inputs to force a match.
- Keep an indicator separate from the trading hypothesis built on it.
- Record failure modes and null results, not only successes.

## Where things go

| Path | Contents |
|---|---|
| `notes/chNN-topic.md` | Chapter summary: formulas, failure modes, completion test |
| `labs/` | Chapter notebooks/scripts. New labs import from `lib/` and define no indicator code of their own |
| `lib/` | Shared code. Every function needs a test in `tests/` |
| `research/NNN-name/` | Statistical studies (not strategies): README, protocol/hypothesis, results, scripts, results/ |
| `strategies/NNN-name/` | Copy `strategies/_template/`. Write HYPOTHESIS.md and commit it **before** any backtest |
| `experiments/log.csv`, `log.md` | One CSV row per test or backtest run (with the commit hash), plus a narrative entry |
| `data/` | Small curated data, committed, documented in `data/DATA_PROVENANCE.md`. Large or downloadable data goes in `data/downloads/` (gitignored), with a committed fetch script |

## Rules for code

- Use `lib.backtest.run` for every new backtest. A position is decided on bar t's close and filled at that close, the next open (default protocol for NIFTY work, `fill='next_open'`) or the next close. Never use same-bar returns.
- Code written before `lib/` existed (`labs/ch08_lab.ipynb`, `labs/ch11_lab.ipynb`, `research/001-*`, `research/002-*`) keeps its own functions so its published numbers reproduce exactly. Do not refactor it onto `lib/` unless the results are re-checked and the notes updated.
- No look-ahead. Centred or phased averages (Ch 10 seasonal index, Hurst phasing) are for description only.
- Never fill missing prices silently. Returns must not span gaps.
- Fix random seeds. Write CSVs with fixed precision (`float_format="%.6f"`) so re-runs are byte-identical.
- When changing `lib/`, add or update a test with a hand-checkable value. Run `python -m pytest` before committing.
- Re-execute any notebook you change (`jupyter nbconvert --to notebook --execute --inplace labs/NAME.ipynb`) and commit it with outputs.
- Statistical claims need a null hypothesis declared before the test, and a p-value or interval. "The tallest bar" is not evidence.

## Book errata found so far

- p. 495: the TMA formula prints `×` between the terms; they are added.
- p. 498: the text says `y₂ = 5 sin 6φ`; the figure and the derivative use `6 sin 5φ`.
- pp. 501–502: the copper α = 1.464 (period 8.4 quarters) does not reproduce from Table 11.4. The data give about 10 quarters.
- pp. 511–513: Excel FFT output rows are labelled Jan–Dec. Row k is a cycle of N/k bars, not a month.
- p. 516: the Hilbert Q needs Ehlers' gain correction (0.075·Period + 0.54), which the book omits.
- p. 519: the Fisher transform's output is unbounded; the ±1 range the book gives applies to its input.
- p. 521: the CCI mean x̄ is printed as a sum; it is an average.
- p. 540: the Money Flow Index accumulates flows over all history with no period; the standard version uses n-day sums.
- p. 542: PVI/NVI variation 2 is not Fosback's index, which compounds the day's % price change.
- p. 547: the A/D index is printed as ADI(t−1) − A − D; it is ADI(t−1) + (A − D).
- p. 548: Bolton-Tremblay takes √BT of a negative BT; use √|BT|. The Schultz ratio is said to be 0–100 but has no ×100.
- p. 563: a one-sided 2σ low-volume filter removes ≈2.3% of days (normal), not 32%.

## Commits

- One logical change per commit, with a message that says what and why.
- Do not commit generated files that the scripts cannot reproduce.
