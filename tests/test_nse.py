"""Tests for lib/nse.py on small hand-made bhavcopy files (not market data).

Each fixture has the column layout of one NSE format; the numbers are invented so the
expected results can be checked by hand.
"""
import importlib.util
import io
import zipfile
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from lib import nse

ROOT = Path(__file__).resolve().parents[1]


def zipped(csv_text, name='file.csv'):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        z.writestr(name, csv_text)
    return buf.getvalue()


def fo_legacy(day='02-JAN-2024', oi=(1000.0, 500.0), close=(21800.0, 21950.0)):
    # Two NIFTY futures expiries, one option row and one stock future (both must be ignored).
    return (
        'INSTRUMENT,SYMBOL,EXPIRY_DT,STRIKE_PR,OPTION_TYP,OPEN,HIGH,LOW,CLOSE,SETTLE_PR,CONTRACTS,VAL_INLAKH,OPEN_INT,CHG_IN_OI,TIMESTAMP,\n'
        f'FUTIDX,NIFTY,25-Jan-2024,0,XX,21700,21850,21650,{close[0]},{close[0]},100,1635,{oi[0]},10,{day},\n'
        f'FUTIDX,NIFTY,29-Feb-2024,0,XX,21850,21990,21800,{close[1]},{close[1]},20,329.25,{oi[1]},5,{day},\n'
        f'OPTIDX,NIFTY,25-Jan-2024,22000,CE,100,120,90,110,110,5000,99999,7000,0,{day},\n'
        f'FUTSTK,INFY,25-Jan-2024,0,XX,1500,1510,1490,1505,1505,50,375,900,0,{day},\n')


def fo_udiff(day='2024-07-08', oi=(1100.0, 450.0), close=(24300.0, 24400.0), lot=25, vol_is_units=True):
    # Value is set so that value / (volume x price) reveals the unit of TtlTradgVol.
    rows = []
    for (expiry, c, o, contracts) in [('2024-07-25', close[0], oi[0], 80), ('2024-08-29', close[1], oi[1], 10)]:
        vol = contracts * lot if vol_is_units else contracts
        value = contracts * lot * c
        rows.append(f'{day},{day},FO,NSE,IDF,35001,,NIFTY,,{expiry},{expiry},,,NIFTY24JULFUT,{c - 50},{c + 60},{c - 80},{c},{c},{c - 20},{c},{c},{o},12,{vol},{value},300,F1,{lot},,,,,')
    rows.append(f'{day},{day},FO,NSE,IDO,35002,,NIFTY,,2024-07-25,2024-07-25,24500,CE,NIFTY24JUL24500CE,100,120,90,110,110,100,24300,110,7000,0,5000,99999,10,F1,25,,,,,')
    header = ('TradDt,BizDt,Sgmt,Src,FinInstrmTp,FinInstrmId,ISIN,TckrSymb,SctySrs,XpryDt,FininstrmActlXpryDt,'
              'StrkPric,OptnTp,FinInstrmNm,OpnPric,HghPric,LwPric,ClsPric,LastPric,PrvsClsgPric,UndrlygPric,'
              'SttlmPric,OpnIntrst,ChngInOpnIntrst,TtlTradgVol,TtlTrfVal,TtlNbOfTxsExctd,SsnId,NewBrdLotQty,'
              'Rmks,Rsvd1,Rsvd2,Rsvd3,Rsvd4')
    return header + '\n' + '\n'.join(rows) + '\n'


def cm_legacy(day='02-JAN-2024', closes=None):
    # AAA up, BBB down, CCC flat, DDD up (BE series: excluded from EQ breadth), NIFTYBEES up.
    closes = closes or {'AAA': 105, 'BBB': 48, 'CCC': 20, 'DDD': 11, 'NIFTYBEES': 240}
    prev = {'AAA': 100, 'BBB': 50, 'CCC': 20, 'DDD': 10, 'NIFTYBEES': 238}
    series = {'DDD': 'BE'}
    vol = {'AAA': 1000, 'BBB': 3000, 'CCC': 500, 'DDD': 70, 'NIFTYBEES': 9000}
    lines = ['SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,TOTTRDQTY,TOTTRDVAL,TIMESTAMP,TOTALTRADES,ISIN,']
    for s, c in closes.items():
        lines.append(f'{s},{series.get(s, "EQ")},{prev[s]},{max(c, prev[s]) + 1},{min(c, prev[s]) - 1},{c},{c},{prev[s]},'
                     f'{vol[s]},{vol[s] * c},{day},10,INE000000000,')
    return '\n'.join(lines) + '\n'


def cm_udiff(day='2024-07-08'):
    header = ('TradDt,BizDt,Sgmt,Src,FinInstrmTp,FinInstrmId,ISIN,TckrSymb,SctySrs,XpryDt,FininstrmActlXpryDt,'
              'StrkPric,OptnTp,FinInstrmNm,OpnPric,HghPric,LwPric,ClsPric,LastPric,PrvsClsgPric,UndrlygPric,'
              'SttlmPric,OpnIntrst,ChngInOpnIntrst,TtlTradgVol,TtlTrfVal,TtlNbOfTxsExctd,SsnId,NewBrdLotQty,'
              'Rmks,Rsvd1,Rsvd2,Rsvd3,Rsvd4')
    rows = [f'{day},{day},CM,NSE,STK,1,INE1,AAA,EQ,,,,,AAA LTD,100,106,99,105,105,100,,105,,,1000,105000,10,F1,1,,,,,',
            f'{day},{day},CM,NSE,STK,2,INE2,BBB,EQ,,,,,BBB LTD,50,51,47,48,48,50,,48,,,3000,144000,10,F1,1,,,,,',
            f'{day},{day},CM,NSE,STK,3,INE3,CCC,EQ,,,,,CCC LTD,20,21,19,20,20,20,,20,,,500,10000,10,F1,1,,,,,',
            f'{day},{day},CM,NSE,STK,4,INE4,DDD,BE,,,,,DDD LTD,10,12,9,11,11,10,,11,,,70,770,10,F1,1,,,,,',
            f'{day},{day},CM,NSE,STK,5,INE5,NIFTYBEES,EQ,,,,,NIFTYBEES,238,241,237,240,240,238,,240,,,9000,2160000,10,F1,1,,,,,']
    return header + '\n' + '\n'.join(rows) + '\n'


# --- URLs ---------------------------------------------------------------------

def test_urls_pick_format_by_date():
    old = nse.bhavcopy_urls('fo', date(2024, 1, 2))
    assert old[0] == 'https://archives.nseindia.com/content/historical/DERIVATIVES/2024/JAN/fo02JAN2024bhav.csv.zip'
    new = nse.bhavcopy_urls('cm', date(2024, 7, 8))
    assert new[0] == 'https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_20240708_F_0000.csv.zip'
    assert len(old) == len(new) == 2            # the other format is always tried as a fallback


# --- F&O ----------------------------------------------------------------------

def test_parse_fo_legacy_from_zip():
    fo = nse.parse_fo(nse.read_bhavcopy(zipped(fo_legacy())))
    assert len(fo) == 4 and (fo['format'] == 'legacy').all()
    assert fo.loc[0, 'value_inr'] == 1635 * 1e5
    assert fo.loc[0, 'expiry'] == pd.Timestamp('2024-01-25')


def test_parse_fo_udiff_maps_instrument_codes():
    fo = nse.parse_fo(nse.read_bhavcopy(zipped(fo_udiff())))
    assert set(fo['instrument']) == {'FUTIDX', 'OPTIDX'}
    assert (fo['format'] == 'udiff').all() and fo['lot_size'].iloc[0] == 25


def test_index_futures_daily_front_month_and_totals():
    fo = nse.parse_fo(nse.read_bhavcopy(zipped(fo_legacy())))
    d = nse.index_futures_daily(fo, 'NIFTY').iloc[0]
    assert d['close'] == 21800                       # nearest expiry
    assert d['total_open_interest'] == 1500          # both expiries, no options, no stock futures
    assert d['total_contracts'] == 120
    assert np.isclose(d['total_value_inr'], (1635 + 329.25) * 1e5)


@pytest.mark.parametrize('units', [True, False])
def test_fo_volume_unit_detection(units):
    fo = nse.parse_fo(nse.read_bhavcopy(zipped(fo_udiff(vol_is_units=units))))
    assert nse.fo_volume_unit(nse.index_futures_daily(fo)) == ('units' if units else 'contracts')


def test_unexpected_columns_raise():
    with pytest.raises(ValueError, match='unrecognised'):
        nse.parse_fo(pd.DataFrame({'foo': [1]}))
    broken = nse.read_bhavcopy(zipped(fo_udiff())).drop(columns=['OpnIntrst'])
    with pytest.raises(ValueError, match='OpnIntrst'):
        nse.parse_fo(broken)


# --- Cash market --------------------------------------------------------------

@pytest.mark.parametrize('text', [cm_legacy(), cm_udiff()])
def test_breadth_counts_eq_only(text):
    cm = nse.parse_cm(nse.read_bhavcopy(zipped(text)))
    b = nse.breadth_daily(cm).iloc[0]
    # EQ: AAA up, NIFTYBEES up, BBB down, CCC flat. DDD is BE and excluded.
    assert (b['advances'], b['declines'], b['unchanged'], b['issues']) == (2, 1, 1, 4)
    assert b['adv_volume'] == 1000 + 9000 and b['dec_volume'] == 3000


def test_both_cm_formats_parse_identically():
    a = nse.parse_cm(nse.read_bhavcopy(zipped(cm_legacy()))).drop(columns=['format', 'date'])
    b = nse.parse_cm(nse.read_bhavcopy(zipped(cm_udiff()))).drop(columns=['format', 'date'])
    pd.testing.assert_frame_equal(a.reset_index(drop=True), b.reset_index(drop=True), check_dtype=False)


def test_new_highs_lows_needs_history():
    days = pd.bdate_range('2024-01-01', periods=6)
    highs = [10, 11, 12, 11, 13, 9]                 # new 3-day highs on days 3 and 5
    cm = pd.DataFrame({'date': days, 'symbol': 'AAA', 'series': 'EQ', 'high': highs,
                       'low': [h - 1 for h in highs]})
    out = nse.new_highs_lows(cm, lookback=3)
    assert out['new_highs'].tolist() == [0, 0, 1, 0, 1, 0]
    assert out['new_lows'].tolist() == [0, 0, 0, 0, 0, 1]
    assert out['eligible'].tolist()[:2] == [0, 0]   # not enough history yet


def test_security_daily():
    cm = nse.parse_cm(nse.read_bhavcopy(zipped(cm_legacy())))
    bees = nse.security_daily(cm, 'NIFTYBEES')
    assert bees['close'].iloc[0] == 240 and bees['volume'].iloc[0] == 9000


# --- End to end: downloads folder -> daily tables ----------------------------

def test_build_script_across_format_change(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location('build', ROOT / 'data' / 'build_nse_daily.py')
    build = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build)
    src = tmp_path / 'downloads' / 'nse'
    for kind in ('fo', 'cm'):
        (src / kind).mkdir(parents=True)
    (src / 'fo' / 'fo_20240705.csv.zip').write_bytes(zipped(fo_legacy('05-JUL-2024')))
    (src / 'fo' / 'fo_20240708.csv.zip').write_bytes(zipped(fo_udiff()))
    (src / 'cm' / 'cm_20240705.csv.zip').write_bytes(zipped(cm_legacy('05-JUL-2024')))
    (src / 'cm' / 'cm_20240708.csv.zip').write_bytes(zipped(cm_udiff()))
    monkeypatch.setattr(build, 'SRC', src)
    monkeypatch.setattr(build, 'OUT', tmp_path)
    build.main()

    fut = pd.read_csv(tmp_path / 'nifty_futures_daily.csv', index_col='date')
    assert list(fut['format']) == ['legacy', 'udiff']
    assert fut['total_open_interest'].tolist() == [1500, 1550]
    breadth = pd.read_csv(tmp_path / 'nse_breadth_daily.csv', index_col='date')
    assert breadth['advances'].tolist() == [2, 2]
    assert (tmp_path / 'niftybees_daily.csv').exists()
    report = (src / 'build_report.txt').read_text()
    assert 'UDiFF volume_reported counts: units' in report
    assert 'total_open_interest: median after/before 2024-07-08 = 1.03' in report
