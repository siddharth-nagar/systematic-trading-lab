# NIFTY 50 price-index monthly dataset — provenance

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

## Gaps and return validation

Missing months between January 2000 and December 2025: **2000-08, 2001-01, 2001-09, 2001-10, 2001-11, 2001-12**. Returns that would incorrectly span missing months are left blank (2000-09, 2001-02, 2002-01); initial January 2000 is also blank. Missing-month months themselves are absent and must not be treated as zero returns. This first release has no claim of complete 2000–2025 monthly coverage.

Daily overlap mismatch count: 2; largest absolute close-price difference 20.60 index points. Source precedence resolves these but the discrepancy needs independent official verification. Do not interpret the series as error-free.
