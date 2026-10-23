# Research 003 — Volume, open interest and breadth on NIFTY (Kaufman Ch.12)

**Status: protocol pre-registered; waiting for data.** Nothing has been run.

- Protocol, hypotheses and tests: [HYPOTHESIS.md](HYPOTHESIS.md), written before any NSE data was downloaded.
- Data pipeline: `data/fetch_nse.py` → `data/build_nse_daily.py` (see [data provenance](../../data/DATA_PROVENANCE.md)).
- Indicators: `lib/volume.py`; mechanics on synthetic data in [`labs/ch12_lab.ipynb`](../../labs/ch12_lab.ipynb).

Next step: download the NSE files on a machine that can reach nseindia.com, run the build, read `build_report.txt`, then implement the six tests exactly as written.
