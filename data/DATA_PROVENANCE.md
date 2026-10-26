# Data provenance

Small curated datasets are committed here so published results reproduce. Large or re-downloadable data goes in `data/downloads/` (gitignored), fetched by a committed script.

## `nifty50_monthly_2000_2026_partial.csv` — NIFTY 50 price-index monthly

- Assembled: 2026-10-13.
- Series: NIFTY 50 price index, daily close/high/low consolidated to last observed trading-day close and monthly extrema.
- Sources:
  - 2000 onward: https://github.com/Gajapathy-Selvaraj/Stock_Market_Datasets_NSE/blob/main/NIFTY_50(INDEX)from2000.csv (Google Finance-derived; blob fc51a9331ee2b72c430724d5e0bdd0237f91103a)
  - 2015 through 2026-03-30: https://github.com/Hareeshkesavan/Stock-Market-Dataset/blob/main/Nifty%2050%20Historical%20Data.csv (third-party compiled data; blob 98818f1f9c0e298401a7238d22f19c4d7e392fa5)
- Source overlap checked by exact matching date and numerical close, tolerance INR 0.01: 1498 overlapping daily rows, 2 mismatches, maximum absolute difference 20.6000 points.
- Overlap policy: favour the newer dataset on identical dates.
- Dates are ISO YYYY-MM-DD; imported source date formats were US month/day/year.
- Data is **secondary**, not independently NSE-verified. Validate against NSE Indices before publication or live trading.
- Coverage: 2000-01 to 2026-03. The 2026-03 month is **incomplete**; the monthly return is displayed for reference but excluded from the full-year calendar study.
- For January 2000 no December 1999 baseline exists; January 2000 return is null, not zero.
- Study ranking period: through 2025-12; 302 valid contiguous monthly returns. January has one fewer observation because its 2000 baseline is absent.
- This is a **price index**, not an NSE NIFTY Total Returns Index (dividends excluded).
- Return convention: simple close-to-close percentage return, 100*(current month final close/prior month final close - 1).
- Daily extrema are preserved in the monthly CSV to support later October/September low-break event tests.
- **Caveat:** monthly highs and lows cannot tell which intramonth event occurred first; event studies need the daily dataset.
- No futures costs, options execution/slippage or live trading rules have been tested.

### Gaps and return validation

Missing months between January 2000 and December 2025: **2000-08, 2001-01, 2001-09, 2001-10, 2001-11, 2001-12**. Returns that would incorrectly span missing months are left blank (2000-09, 2001-02, 2002-01); initial January 2000 is also blank. Missing-month months themselves are absent and must not be treated as zero returns. This first release has no claim of complete 2000–2025 monthly coverage.

**Missingness is probably not random.** The 2001-09 to 2001-12 gap coincides with the post-9/11 market sell-off. Data missing during a stress period can bias the statistics of the affected calendar months (here Sep–Dec, plus Jan/Feb through blanked returns), so the gaps must be filled from official NSE data before any month-level conclusion is treated as reliable.

Daily overlap mismatch count: 2; largest absolute close-price difference 20.60 index points. Source precedence resolves these but the discrepancy needs independent official verification. Do not interpret the series as error-free.

## `nifty50_daily_2002_2026.csv` — NIFTY 50 price-index daily (Research 002, Chapter 8 lab)

- File: `nifty50_daily_2002_2026.csv` (Date, Open, High, Low, Close), 5,977 trading days, 2002-01-01 to 2026-03-30.
- Assembled: 2026-10-18 from the same two secondary sources documented in the NIFTY monthly section above:
  - https://github.com/Gajapathy-Selvaraj/Stock_Market_Datasets_NSE — `NIFTY_50(INDEX)from2000.csv`, commit c73de0e6c9acca1330a19cd41ee3d7dbd5100260 (used before 2015-01-01)
  - https://github.com/Hareeshkesavan/Stock-Market-Dataset — `Nifty 50 Historical Data.csv`, commit aa60b746f089c3f54df6760bf021708c2d3ce1e8 (used from 2015-01-01)
- Overlap 2015-01-01 to 2021-01-25: 1,498 days; Open/High/Low identical; 1 close mismatch (max 20.6 points). Newer source preferred.
- Starts in 2002 because the older source is missing whole months in 2000–2001 (gaps of 34–123 days), which would break daily indicators.
- Remaining gaps over 5 calendar days: 2002-09-02 (7 days), 2014-10-07 (6 days, holidays).
- 0 rows with inconsistent OHLC. Before 2007, 5–10% of opens equal the prior close (likely source artefact) — affects next-open fills slightly in early years.
- Price index, not total return. Secondary data, not verified against NSE Indices.

## `copper_scrap_quarterly_1963_1979.csv` — Kaufman Table 11.4

- Source: Kaufman, *Trading Systems and Methods*, Table 11.4, "Dealer's Buying Price, No. 2 Heavy Copper Scrap at New York" (average quarterly price, cents per pound), based on prices from the American Metal Market.
- Transcribed by hand from the printed table, 1963 Q1 to 1979 Q4 (68 quarters). Check against the book if a value looks wrong.
- Used only to replicate the book's single-frequency trigonometric regression (`labs/ch11_lab.ipynb`). Not used for trading research.

## NSE bhavcopy downloads (Chapter 12) — pipeline ready, not yet run

- Source: NSE daily bhavcopies, F&O and cash market (CM), downloaded by `data/fetch_nse.py` into `data/downloads/nse/` (gitignored). Every attempt is logged in `data/downloads/nse/manifest.csv`.
- Two formats: legacy files up to 2024-07-05; UDiFF "common bhavcopy" from 2024-07-08 (NSE discontinued the old files w.e.f. 8 July 2024). `lib/nse.py` detects the format from each file's header and refuses files with unexpected columns.
- `data/build_nse_daily.py` builds:
  - `nifty_futures_daily.csv`: front-month NIFTY futures OHLC and settle, plus **total** traded value, volume and open interest across all expiries (Kaufman pp. 528, 545–546: total, not single-contract, figures avoid roll distortions);
  - `nse_breadth_daily.csv`: EQ-series advances, declines, unchanged, up/down volume (shares) and 52-week new highs/lows (needs a year of history before the first count);
  - `niftybees_daily.csv`: NIFTYBEES ETF OHLC, volume and value — a cleaner equity volume series than the index itself.
- **Confirmed on a real file** (`BhavCopy_NSE_FO_0_0_0_20240708_F_0000.csv`, downloaded by the user on 2026-10-26; an excerpt is kept as `tests/fixtures/nse_fo_udiff_20240708_excerpt.csv`):
  - the UDiFF F&O header matches `lib/nse.py` exactly (34 columns);
  - `TtlTradgVol` counts **contracts** (value ÷ (volume × price) = 24.98 with lot size 25), the same unit as legacy `CONTRACTS`, so `total_contracts` is one series across both formats;
  - `OpnIntrst` counts **units** (shares/index units), not contracts: every NIFTY value is a multiple of the lot size;
  - NIFTY front-month close 24,375.60 vs index 24,320.55 (basis 0.23%); the file's underlying price equals the close in `nifty50_daily_2002_2026.csv` for that day.
- **Still open, check in `build_report.txt` on the first full run:**
  - whether legacy `OPEN_INT` is also in units (if it were in contracts, total OI would jump at 2024-07-08 and the report flags it);
  - continuity of traded value across 2024-07-08;
  - the CM (stock) bhavcopy format, not yet seen on a real file.
- Legacy F&O contract counts change meaning when the lot size changes (NIFTY lots have been 200, 50, 75 and 25 at different times). Use traded **value** or OI × price for long-run comparisons.
- Breadth counts every EQ-series security, including ETFs; NSE's published advance/decline figures may differ slightly.
- Status: unit-tested on hand-made samples and checked on one real UDiFF F&O file; the full download has not been run yet (the cloud environment blocks nseindia.com).
