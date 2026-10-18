# NIFTY 50 daily dataset — provenance

- File: `nifty50_daily_2002_2026.csv` (Date, Open, High, Low, Close), 5,977 trading days, 2002-01-01 to 2026-03-30.
- Assembled: 2026-10-18 from the same two secondary sources documented in `02_nifty_seasonality/data/DATA_PROVENANCE.md`:
  - https://github.com/Gajapathy-Selvaraj/Stock_Market_Datasets_NSE — `NIFTY_50(INDEX)from2000.csv`, commit c73de0e6c9acca1330a19cd41ee3d7dbd5100260 (used before 2015-01-01)
  - https://github.com/Hareeshkesavan/Stock-Market-Dataset — `Nifty 50 Historical Data.csv`, commit aa60b746f089c3f54df6760bf021708c2d3ce1e8 (used from 2015-01-01)
- Overlap 2015-01-01 to 2021-01-25: 1,498 days; Open/High/Low identical; 1 close mismatch (max 20.6 points). Newer source preferred.
- Starts in 2002 because the older source is missing whole months in 2000–2001 (gaps of 34–123 days), which would break daily indicators.
- Remaining gaps over 5 calendar days: 2002-09-02 (7 days), 2014-10-07 (6 days, holidays).
- 0 rows with inconsistent OHLC. Before 2007, 5–10% of opens equal the prior close (likely source artefact) — affects next-open fills slightly in early years.
- Price index, not total return. Secondary data, not verified against NSE Indices.
