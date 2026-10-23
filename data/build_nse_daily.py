"""Build daily NIFTY futures, NIFTYBEES and market-breadth tables from downloaded bhavcopies.

Run after data/fetch_nse.py, from the repository root:

    python data/build_nse_daily.py

Reads data/downloads/nse/{fo,cm}/*.csv.zip and writes:
    data/nifty_futures_daily.csv   front-month OHLC/settle + totals over all expiries (value, volume, OI)
    data/niftybees_daily.csv       NIFTYBEES ETF OHLC, volume (shares) and value
    data/nse_breadth_daily.csv     EQ-series advances, declines, unchanged, up/down volume, 52-week highs/lows
    data/downloads/nse/build_report.txt   checks to read before using the data

The outputs are small enough to commit once the report's checks look right.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lib import nse  # noqa: E402

SRC = ROOT / 'data' / 'downloads' / 'nse'
OUT = ROOT / 'data'


def load(kind, parser, keep):
    frames, bad = [], []
    for path in sorted((SRC / kind).glob(f'{kind}_*.csv.zip')):
        try:
            df = parser(nse.read_bhavcopy(path))
        except ValueError as e:
            bad.append(f'{path.name}: {e}')
            continue
        frames.append(keep(df))
    if not frames:
        return None, bad
    return pd.concat(frames, ignore_index=True), bad


def continuity(series, cut=pd.Timestamp(nse.UDIFF_START), window=20):
    """Median after / median before the format change; ~1 means no level break."""
    before = series[series.index < cut].tail(window).median()
    after = series[series.index >= cut].head(window).median()
    return after / before if before and np.isfinite(before) else np.nan


def main():
    report = []
    say = lambda s='': (report.append(s), print(s))

    fo, bad_fo = load('fo', nse.parse_fo, lambda d: d[d['instrument'] == 'FUTIDX'])
    cm, bad_cm = load('cm', nse.parse_cm, lambda d: d[d['series'] == 'EQ'])
    for b in bad_fo + bad_cm:
        say(f'UNREADABLE {b}')
    if fo is None and cm is None:
        sys.exit(f'no bhavcopy files found under {SRC}; run data/fetch_nse.py first')

    if fo is not None:
        fut = nse.index_futures_daily(fo, 'NIFTY')
        fut.to_csv(OUT / 'nifty_futures_daily.csv', float_format='%.6f')
        unit = nse.fo_volume_unit(fut)
        say(f'NIFTY futures: {len(fut)} days, {fut.index[0]:%Y-%m-%d} to {fut.index[-1]:%Y-%m-%d}')
        say(f'  UDiFF volume_reported counts: {unit}  (legacy files report contracts)')
        for col in ('total_open_interest', 'total_value_inr'):
            r = continuity(fut[col])
            flag = '' if np.isnan(r) or 0.5 < r < 2 else '   <-- LEVEL BREAK: check units before using'
            say(f'  {col}: median after/before 2024-07-08 = {r:.2f}{flag}')
        spot_path = OUT / 'nifty50_daily_2002_2026.csv'
        if spot_path.exists():
            spot = pd.read_csv(spot_path, parse_dates=['Date'], index_col='Date')['Close']
            basis = (fut['close'] / spot.reindex(fut.index) - 1).dropna()
            say(f'  front-month basis vs NIFTY index: median {100 * basis.median():.2f}%, '
                f'95th pct |basis| {100 * basis.abs().quantile(0.95):.2f}%  (expect well under 2%)')

    if cm is not None:
        breadth = nse.breadth_daily(cm).join(nse.new_highs_lows(cm))
        breadth.to_csv(OUT / 'nse_breadth_daily.csv', float_format='%.6f')
        say(f'Breadth: {len(breadth)} days; issues per day median {breadth["issues"].median():.0f} '
            f'(min {breadth["issues"].min():.0f}, max {breadth["issues"].max():.0f})')
        r = continuity(breadth['issues'])
        say(f'  issues: median after/before 2024-07-08 = {r:.2f}')
        try:
            bees = nse.security_daily(cm, 'NIFTYBEES')
            bees.to_csv(OUT / 'niftybees_daily.csv', float_format='%.6f')
            say(f'NIFTYBEES: {len(bees)} days from {bees.index[0]:%Y-%m-%d}')
        except ValueError as e:
            say(f'NIFTYBEES: {e}')

    days = pd.Index(sorted((set(fut.index) if fo is not None else set()) |
                           (set(breadth.index) if cm is not None else set())))
    gaps = pd.Series(days[1:] - days[:-1], index=days[1:])
    long = gaps[gaps > pd.Timedelta(days=5)]
    say(f'Gaps over 5 calendar days: {len(long)}' + (' — ' + ', '.join(f'{d:%Y-%m-%d} ({g.days}d)' for d, g in long.items()) if len(long) else ''))
    (SRC / 'build_report.txt').write_text('\n'.join(report) + '\n')


if __name__ == '__main__':
    main()
