"""Download NSE daily bhavcopy files (F&O and cash market) into data/downloads/nse/.

Run from the repository root, on a machine that can reach nseindia.com:

    python data/fetch_nse.py --start 2024-06-24 --end 2024-07-19          # small test across the format change
    python data/fetch_nse.py --start 2002-01-01 --end 2026-03-31          # full history (slow: ~12,000 requests)

Then build the daily tables with `python data/build_nse_daily.py`.

- Files already downloaded are skipped, so the script can be stopped and resumed.
- Weekends are skipped; a 404 on a weekday is recorded as a likely holiday, not an error.
- Every attempt is logged in data/downloads/nse/manifest.csv (date, kind, url, status, bytes).
- Be polite: the default pause between requests is 1 second. Do not lower it much.
"""
import argparse
import csv
import http.cookiejar
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lib.nse import bhavcopy_urls  # noqa: E402

OUT = ROOT / 'data' / 'downloads' / 'nse'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/124.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nseindia.com/all-reports',
}


def opener():
    jar = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    op.addheaders = list(HEADERS.items())
    try:                                   # NSE sets session cookies on the home page
        op.open('https://www.nseindia.com/', timeout=20).read()
    except (urllib.error.URLError, TimeoutError) as e:
        print(f'warning: could not open nseindia.com home page ({e}); trying archives anyway')
    return op


def fetch(op, url, retries=3):
    """Return (status, bytes). Retries timeouts and 5xx with backoff; 404 returns immediately."""
    for attempt in range(retries + 1):
        try:
            with op.open(url, timeout=30) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 404) or attempt == retries:
                return e.code, b''
        except (urllib.error.URLError, TimeoutError):
            if attempt == retries:
                return 0, b''
        time.sleep(2 ** (attempt + 1))
    return 0, b''


def trading_days(start, end):
    d = start
    while d <= end:
        if d.weekday() < 5:
            yield d
        d += timedelta(days=1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--start', required=True, type=lambda s: datetime.strptime(s, '%Y-%m-%d').date())
    p.add_argument('--end', default=date.today().isoformat(), type=lambda s: datetime.strptime(s, '%Y-%m-%d').date())
    p.add_argument('--kinds', nargs='+', default=['fo', 'cm'], choices=['fo', 'cm'])
    p.add_argument('--sleep', type=float, default=1.0, help='seconds between requests')
    args = p.parse_args()

    manifest = OUT / 'manifest.csv'
    OUT.mkdir(parents=True, exist_ok=True)
    new_manifest = not manifest.exists()
    op = opener()
    got = missing = blocked = failed = 0
    with open(manifest, 'a', newline='') as mf:
        log = csv.writer(mf)
        if new_manifest:
            log.writerow(['date', 'kind', 'url', 'status', 'bytes', 'fetched_at'])
        for d in trading_days(args.start, args.end):
            for kind in args.kinds:
                target = OUT / kind / f'{kind}_{d:%Y%m%d}.csv.zip'
                if target.exists():
                    continue
                statuses = []
                for url in bhavcopy_urls(kind, d):
                    status, body = fetch(op, url)
                    statuses.append(status)
                    log.writerow([d.isoformat(), kind, url, status, len(body), datetime.now().isoformat(timespec='seconds')])
                    time.sleep(args.sleep)
                    if status == 200 and body[:2] == b'PK':
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(body)
                        got += 1
                        break
                    if status == 403:
                        blocked += 1
                else:
                    if all(s == 404 for s in statuses):
                        missing += 1
                    else:
                        failed += 1
            mf.flush()
            if failed >= 10 and got == 0:
                sys.exit('Every request failed at the network level (no HTTP response). Check that this '
                         'machine can reach archives.nseindia.com and nsearchives.nseindia.com.')
            if blocked >= 20 and got == 0:
                sys.exit('NSE is refusing every request (403). Check your network/VPN, or download '
                         'the bhavcopy zips manually into data/downloads/nse/fo and .../cm as '
                         'fo_YYYYMMDD.csv.zip / cm_YYYYMMDD.csv.zip.')
    print(f'downloaded {got} files; {missing} weekday files not found (404: holidays or gaps); '
          f'{failed} failed (network/403, re-run to retry); log: {manifest}')


if __name__ == '__main__':
    main()
