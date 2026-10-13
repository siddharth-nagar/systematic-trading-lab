# NIFTY 50 monthly seasonality

**Research 001 — documented baseline.** Generated from actual secondary source daily prices and summarised into monthly data. Main statistical table uses months ending through **December 2025**. 2026 observations are **partial** and excluded from rankings.

Start with [research_notes.md](research_notes.md), [hypotheses.md](hypotheses.md), and [data/DATA_PROVENANCE.md](data/DATA_PROVENANCE.md).

Run locally after `pip install -r ../requirements.txt`:

```bash
python 02_nifty_seasonality/analyse.py
```

It reproduces tables and charts in `results/`. No live broker or automated trading integration.

## Avoid scope creep

Our objective is to document **what the history actually says**. Do not optimise calendar windows or combine ten filters until the hypothesis protocol and holdout data are fixed.

## Files
- `data/nifty50_monthly_2000_2026_partial.csv`: dated price-index monthly OHLC and close-to-close return.
- `results/monthly_seasonality.csv`: descriptive summary through 2025.
- `research_notes.md`: interpretations and limitations.
- `hypotheses.md`: prior research ideas, explicitly not validated.
- `analyse.py`: reproducible analysis.
