# NIFTY 50 monthly seasonality

**Research 001 — documented baseline.** Generated from actual secondary source daily prices and summarised into monthly data. Main statistical table uses months ending through **December 2025**. 2026 observations are **partial** and excluded from rankings.

Start with [RESULTS.md](RESULTS.md), [HYPOTHESIS.md](HYPOTHESIS.md), and [the data provenance](../../data/DATA_PROVENANCE.md).

Run from the repository root after `pip install -e ".[dev]"`:

```bash
python research/001-nifty-seasonality/analyse.py
```

It reproduces tables and charts in `results/`. No live broker or automated trading integration.

## Avoid scope creep

Our objective is to document **what the history actually says**. Do not optimise calendar windows or combine ten filters until the hypothesis protocol and holdout data are fixed.

## Files
- `data/nifty50_monthly_2000_2026_partial.csv`: dated price-index monthly OHLC and close-to-close return.
- `results/monthly_seasonality.csv`: descriptive summary through 2025.
- `results/subperiods.csv`: the same statistics for 2000–2012 and 2013–2025.
- `results/year_month_matrix.csv`: year × calendar-month return matrix.
- `results/mean_monthly_returns.png`, `results/positive_frequency.png`: charts.
- `results/omnibus_test.csv`, `results/omnibus_report.md`: omnibus month-effect test and write-up.
- `RESULTS.md`: interpretations and limitations.
- `HYPOTHESIS.md`: the neutral research protocol, written before testing.
- `analyse.py`: reproducible descriptive analysis.
- `seasonality_tests.py`: omnibus permutation test.

## Statistical tests

Run `python research/001-nifty-seasonality/seasonality_tests.py` to reproduce a neutral omnibus calendar-month test (5,000 within-year permutations) and prespecified two-block descriptive comparison. See [omnibus findings](results/omnibus_report.md). Do not interpret month-by-month differences as confirmed effects without independent validation.
