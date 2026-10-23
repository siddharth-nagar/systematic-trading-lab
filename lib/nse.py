"""Parse NSE daily bhavcopy files (F&O and cash market) into tidy tables.

NSE published two formats:
- legacy (to 2024-07-05): fo{DD}{MON}{YYYY}bhav.csv.zip and cm{DD}{MON}{YYYY}bhav.csv.zip;
- UDiFF "common bhavcopy" (from 2024-07-08): BhavCopy_NSE_FO_0_0_0_{YYYYMMDD}_F_0000.csv.zip
  and BhavCopy_NSE_CM_0_0_0_{YYYYMMDD}_F_0000.csv.zip.

The format is detected from each file's header, never from its date, and a file with
unexpected columns raises an error instead of being guessed at. The UDiFF column names
below follow NSE's UDiFF catalogue as used in public code; they are checked on every file.
"""
import io
import zipfile
from datetime import date

import numpy as np
import pandas as pd

UDIFF_START = date(2024, 7, 8)

_ARCHIVE_OLD = 'https://archives.nseindia.com/content/historical'
_ARCHIVE_NEW = 'https://nsearchives.nseindia.com/content'


# --- URLs ---------------------------------------------------------------------

def bhavcopy_urls(kind, d):
    """Candidate URLs for one trading day, most likely format first. kind: 'fo' or 'cm'."""
    if kind not in ('fo', 'cm'):
        raise ValueError("kind must be 'fo' or 'cm'")
    mon = d.strftime('%b').upper()
    folder = 'DERIVATIVES' if kind == 'fo' else 'EQUITIES'
    legacy = f'{_ARCHIVE_OLD}/{folder}/{d:%Y}/{mon}/{kind}{d:%d}{mon}{d:%Y}bhav.csv.zip'
    udiff = f'{_ARCHIVE_NEW}/{kind}/BhavCopy_NSE_{kind.upper()}_0_0_0_{d:%Y%m%d}_F_0000.csv.zip'
    return [udiff, legacy] if d >= UDIFF_START else [legacy, udiff]


# --- Reading ------------------------------------------------------------------

def read_bhavcopy(path_or_bytes):
    """Read the single CSV inside a bhavcopy zip (or a plain CSV) into a DataFrame."""
    if isinstance(path_or_bytes, (bytes, bytearray)):
        raw = bytes(path_or_bytes)
    else:
        with open(path_or_bytes, 'rb') as f:
            raw = f.read()
    if raw[:2] == b'PK':
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            names = [n for n in z.namelist() if n.lower().endswith('.csv')]
            if len(names) != 1:
                raise ValueError(f'expected one CSV in the zip, found {names}')
            raw = z.read(names[0])
    df = pd.read_csv(io.BytesIO(raw))
    df.columns = [c.strip() for c in df.columns]
    return df.loc[:, ~df.columns.str.startswith('Unnamed')]


def _require(df, cols, what):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f'{what}: missing columns {missing}; found {list(df.columns)}')


# --- F&O ----------------------------------------------------------------------

_FO_LEGACY = ['INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PR', 'OPTION_TYP', 'OPEN', 'HIGH', 'LOW',
              'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT', 'CHG_IN_OI', 'TIMESTAMP']
_FO_UDIFF = ['TradDt', 'FinInstrmTp', 'TckrSymb', 'XpryDt', 'StrkPric', 'OptnTp', 'OpnPric', 'HghPric',
             'LwPric', 'ClsPric', 'SttlmPric', 'OpnIntrst', 'ChngInOpnIntrst', 'TtlTradgVol', 'TtlTrfVal',
             'NewBrdLotQty']
_FO_TYPE = {'IDF': 'FUTIDX', 'IDO': 'OPTIDX', 'STF': 'FUTSTK', 'STO': 'OPTSTK'}


def parse_fo(df):
    """Normalise an F&O bhavcopy. Returns one row per contract with common column names.

    value_inr is traded value in rupees in both formats. contracts is only in the legacy file;
    volume_reported and lot_size only in UDiFF (see fo_volume_unit for what volume_reported counts).
    """
    if 'INSTRUMENT' in df.columns:
        _require(df, _FO_LEGACY, 'legacy F&O bhavcopy')
        out = pd.DataFrame({
            'date': pd.to_datetime(df['TIMESTAMP'], format='%d-%b-%Y'),
            'instrument': df['INSTRUMENT'].str.strip(),
            'symbol': df['SYMBOL'].str.strip(),
            'expiry': pd.to_datetime(df['EXPIRY_DT'], format='%d-%b-%Y'),
            'open': df['OPEN'], 'high': df['HIGH'], 'low': df['LOW'], 'close': df['CLOSE'],
            'settle': df['SETTLE_PR'],
            'contracts': df['CONTRACTS'].astype(float),
            'volume_reported': np.nan,
            'lot_size': np.nan,
            'value_inr': df['VAL_INLAKH'].astype(float) * 1e5,
            'open_interest': df['OPEN_INT'].astype(float),
            'format': 'legacy',
        })
    elif 'FinInstrmTp' in df.columns:
        _require(df, _FO_UDIFF, 'UDiFF F&O bhavcopy')
        out = pd.DataFrame({
            'date': pd.to_datetime(df['TradDt']),
            'instrument': df['FinInstrmTp'].str.strip().map(_FO_TYPE).fillna(df['FinInstrmTp']),
            'symbol': df['TckrSymb'].str.strip(),
            'expiry': pd.to_datetime(df['XpryDt']),
            'open': df['OpnPric'], 'high': df['HghPric'], 'low': df['LwPric'], 'close': df['ClsPric'],
            'settle': df['SttlmPric'],
            'contracts': np.nan,
            'volume_reported': df['TtlTradgVol'].astype(float),
            'lot_size': df['NewBrdLotQty'].astype(float),
            'value_inr': df['TtlTrfVal'].astype(float),
            'open_interest': df['OpnIntrst'].astype(float),
            'format': 'udiff',
        })
    else:
        raise ValueError(f'unrecognised F&O bhavcopy columns: {list(df.columns)}')
    return out


def index_futures_daily(fo, symbol='NIFTY'):
    """One row per day for an index future: front-month prices plus totals over all expiries.

    Kaufman (pp. 528, 545-546) recommends total volume and total open interest across delivery
    months, so the roll from one contract to the next does not distort the series.
    """
    fut = fo[(fo['instrument'] == 'FUTIDX') & (fo['symbol'] == symbol)]
    if fut.empty:
        raise ValueError(f'no FUTIDX rows for {symbol}')
    rows = []
    for d, g in fut.groupby('date'):
        front = g.sort_values('expiry').iloc[0]
        rows.append({'date': d, 'front_expiry': front['expiry'],
                     'open': front['open'], 'high': front['high'], 'low': front['low'],
                     'close': front['close'], 'settle': front['settle'],
                     'total_value_inr': g['value_inr'].sum(),
                     'total_contracts': g['contracts'].sum(min_count=1),
                     'total_volume_reported': g['volume_reported'].sum(min_count=1),
                     'lot_size': front['lot_size'],
                     'total_open_interest': g['open_interest'].sum(),
                     'format': front['format']})
    return pd.DataFrame(rows).set_index('date').sort_index()


def fo_volume_unit(daily):
    """Infer what UDiFF volume_reported counts, from value / (volume x price).

    Returns 'units' when the ratio is ~1 (shares/index units), 'contracts' when it is ~lot size,
    or 'unknown'. Use it before comparing volume across the 2024-07-08 format change.
    """
    u = daily[daily['format'] == 'udiff'].dropna(subset=['total_volume_reported', 'lot_size'])
    if u.empty:
        return 'unknown'
    ratio = (u['total_value_inr'] / (u['total_volume_reported'] * u['settle'])).median()
    lot = u['lot_size'].median()
    if abs(ratio - 1) < 0.2:
        return 'units'
    if abs(ratio / lot - 1) < 0.2:
        return 'contracts'
    return 'unknown'


# --- Cash market --------------------------------------------------------------

_CM_LEGACY = ['SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'PREVCLOSE', 'TOTTRDQTY',
              'TOTTRDVAL', 'TIMESTAMP']
_CM_UDIFF = ['TradDt', 'TckrSymb', 'SctySrs', 'OpnPric', 'HghPric', 'LwPric', 'ClsPric',
             'PrvsClsgPric', 'TtlTradgVol', 'TtlTrfVal']


def parse_cm(df):
    """Normalise a cash-market bhavcopy: one row per security, volume in shares."""
    if 'SERIES' in df.columns:
        _require(df, _CM_LEGACY, 'legacy CM bhavcopy')
        out = pd.DataFrame({
            'date': pd.to_datetime(df['TIMESTAMP'], format='%d-%b-%Y'),
            'symbol': df['SYMBOL'].str.strip(), 'series': df['SERIES'].str.strip(),
            'open': df['OPEN'], 'high': df['HIGH'], 'low': df['LOW'], 'close': df['CLOSE'],
            'prev_close': df['PREVCLOSE'],
            'volume': df['TOTTRDQTY'].astype(float), 'value_inr': df['TOTTRDVAL'].astype(float),
            'format': 'legacy'})
    elif 'SctySrs' in df.columns:
        _require(df, _CM_UDIFF, 'UDiFF CM bhavcopy')
        out = pd.DataFrame({
            'date': pd.to_datetime(df['TradDt']),
            'symbol': df['TckrSymb'].str.strip(), 'series': df['SctySrs'].str.strip(),
            'open': df['OpnPric'], 'high': df['HghPric'], 'low': df['LwPric'], 'close': df['ClsPric'],
            'prev_close': df['PrvsClsgPric'],
            'volume': df['TtlTradgVol'].astype(float), 'value_inr': df['TtlTrfVal'].astype(float),
            'format': 'udiff'})
    else:
        raise ValueError(f'unrecognised CM bhavcopy columns: {list(df.columns)}')
    return out


def breadth_daily(cm, series=('EQ',)):
    """Advances, declines and up/down volume per day for the given series (default: EQ shares).

    A stock advances when close > previous close (NSE's previous close, adjusted for corporate
    actions). Breadth here is the whole EQ segment, an equally weighted count (Appel, p. 547).
    """
    s = cm[cm['series'].isin(series)].dropna(subset=['close', 'prev_close'])
    chg = np.sign(s['close'] - s['prev_close'])
    g = s.assign(up=chg > 0, down=chg < 0, flat=chg == 0).groupby('date')
    out = pd.DataFrame({
        'advances': g['up'].sum(), 'declines': g['down'].sum(), 'unchanged': g['flat'].sum(),
        'adv_volume': g.apply(lambda x: x.loc[x['up'], 'volume'].sum(), include_groups=False),
        'dec_volume': g.apply(lambda x: x.loc[x['down'], 'volume'].sum(), include_groups=False),
        'total_volume': g['volume'].sum(),
    })
    out['issues'] = out[['advances', 'declines', 'unchanged']].sum(axis=1)
    return out.astype(float).sort_index()


def new_highs_lows(cm, lookback=252, series=('EQ',), min_history=None):
    """Count stocks making a new `lookback`-day high (high above every prior high) or low.

    Needs the full history of daily files. A stock is counted only after it has `min_history`
    prior days (default: lookback - 1), so the first year of data gives no counts.
    """
    min_history = lookback - 1 if min_history is None else min_history
    s = cm[cm['series'].isin(series)]
    hi = s.pivot_table(index='date', columns='symbol', values='high').sort_index()
    lo = s.pivot_table(index='date', columns='symbol', values='low').sort_index()
    prior_hi = hi.shift(1).rolling(lookback - 1, min_periods=min_history).max()
    prior_lo = lo.shift(1).rolling(lookback - 1, min_periods=min_history).min()
    enough = prior_hi.notna()
    return pd.DataFrame({'new_highs': ((hi > prior_hi) & enough).sum(axis=1).astype(float),
                         'new_lows': ((lo < prior_lo) & enough).sum(axis=1).astype(float),
                         'eligible': enough.sum(axis=1).astype(float)})


def security_daily(cm, symbol, series='EQ'):
    """OHLC, volume and value for one security, e.g. the NIFTYBEES ETF."""
    s = cm[(cm['symbol'] == symbol) & (cm['series'] == series)]
    if s.empty:
        raise ValueError(f'no rows for {symbol} {series}')
    return s.set_index('date')[['open', 'high', 'low', 'close', 'prev_close', 'volume', 'value_inr']].sort_index()
